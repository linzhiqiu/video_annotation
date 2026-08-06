#!/usr/bin/env python3
"""
Detect Camera Angle/Height Order-Swapping Confusion Script

Analyzes final_feedback from caption export data to detect feedback that discusses
swapping or reordering camera angle/height terms without changing actual meaning.

Detects patterns like:
- Swapping: "high, eye-level angle" ↔ "eye-level, high angle"
- Wrong terminology: using "*-level angle" (e.g., "eye-level angle", "hip-level angle")

This is DIFFERENT from detecting actual angle/height changes like:
- "high angle" → "low angle" (actual change, NOT what we're looking for)

Uses GPT-4o to classify each critique as:
- "Yes": Feedback discusses order-swapping or terminology confusion
- "No": Feedback is about actual camera changes or other aspects

Output:
- sampled_data.jsonl: All analyzed samples with classifications
- report.md: Summary statistics and examples with pre/final captions
"""

import os
import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import difflib
import re

from llm import get_llm


CAMERA_NITPICK_DETECTION_PROMPT = """You are checking whether the FEEDBACK discusses nitpicky terminology changes about camera angle/level terms without changing the actual camera description.

Correct camera terminology:
- Camera ANGLES: high angle, low angle, bird's eye angle, worm's eye angle, Dutch angle, etc.
- Camera HEIGHTS/POSITIONS: hip level, eye level, ground level, overhead, aerial, waist level, etc.

WRONG/NITPICKY patterns we're looking for:
1. "*-level angle" (e.g., "eye-level angle", "hip-level angle") - mixes position term with "angle"
2. Swapping order: "high, eye-level angle" ↔ "eye-level, high angle" - same content, different order
3. Rewording without meaning change: "overhead angle" ↔ "overhead level" - just terminology change
4. Adding/removing "angle" or "level" words: "high angle" ↔ "high, overhead angle"

CRITICAL: We are looking for NITPICKY terminology changes, NOT actual camera position changes.

Examples of NITPICKY changes we're looking for (answer Yes):

Example 1 - Swapping order:
Pre-caption: "From a high, overhead angle"
Feedback: "Change to overhead, high angle"
→ Just swapping order of same terms → Yes

Example 2 - Rewording "angle" to "level":
Pre-caption: "From a high, overhead angle"
Feedback: "Change 'From a high, overhead angle' to 'From a high angle at an overhead level'"
→ Same meaning, just rewording "overhead angle" as "overhead level" → Yes

Example 3 - Wrong terminology:
Pre-caption: "From a high angle at eye level"
Feedback: "Combine as eye-level angle"
→ Suggests using wrong term "eye-level angle" → Yes

Example 4 - Adding redundant terms:
Pre-caption: "From overhead"
Feedback: "Say 'from an overhead, high angle' instead"
→ Adding redundant "high" when overhead already implies high → Yes

Example 5 - Splitting what should be together:
Pre-caption: "From a bird's eye angle"
Feedback: "Change to 'from a bird's eye view at a high angle'"
→ Splitting bird's eye (which already means high angle) → Yes

Example 6 - Points out the terminology issue:
Pre-caption: "Shot from a hip-level angle"
Feedback: "Don't say hip-level angle, that's confusing height with angle"
→ Discusses the terminology confusion → Yes

Examples that are NOT nitpicks (answer No):

Example 1 - Actually changing angle:
Pre-caption: "From a low angle"
Feedback: "Should be high angle, not low angle"
→ Actually changing the angle description → No

Example 2 - Actually changing height:
Pre-caption: "From eye level"
Feedback: "Should be ground level, not eye level"
→ Actually changing the height description → No

Example 3 - Changing both angle and height:
Pre-caption: "From a high angle at eye level"
Feedback: "Should be low angle at ground level"
→ Changing actual camera position → No

Example 4 - About camera movement:
Pre-caption: "From a high angle"
Feedback: "The camera should truck left"
→ Not about angle/level terminology → No

Example 5 - Adding genuinely new information:
Pre-caption: "The camera is static"
Feedback: "Add that it's from a high angle"
→ Adding new info that wasn't there before → No

Example 6 - Removing incorrect information:
Pre-caption: "From a low angle looking up at the sky"
Feedback: "Remove 'looking up at the sky' - that's redundant with low angle"
→ Removing redundancy, not nitpicking terminology → No

---

CRITICAL RULES:
1. Answer Yes if feedback discusses:
   - Swapping order of angle/height terms (same content, different order)
   - Rewording "angle" ↔ "level" without changing meaning (e.g., "overhead angle" ↔ "overhead level")
   - Using "*-level angle" terminology (mixing height word with "angle")
   - Adding redundant angle/height terms that don't change meaning
   - Pointing out this kind of terminology confusion

2. Answer No if feedback is about:
   - Actually changing the camera angle (high → low, etc.)
   - Actually changing the camera height (eye level → ground level, etc.)
   - Camera movement, framing, or other aspects
   - Adding genuinely new information that wasn't present
   - Removing incorrect or truly redundant information

3. The KEY distinction:
   - Yes: "overhead angle" → "overhead level" (same thing, different words - NITPICK)
   - Yes: "high, overhead angle" → "overhead, high angle" (same content, order swap - NITPICK)
   - No: "high angle" → "low angle" (different thing - ACTUAL CHANGE)
   - No: "eye level" → "ground level" (different thing - ACTUAL CHANGE)

---

Inputs:

Feedback:
{final_feedback}

Pre-caption:
{pre_caption}

Final caption:
{final_caption}

---

Output format (STRICT):

Rationale: [Check if feedback is about nitpicky terminology/wording changes (order-swapping, angle↔level rewording, etc.) OR about actual camera position changes. Quote the specific part of feedback that shows this.]
Classification: [Yes or No]"""


def load_video_url_files_mapping(video_urls_dir: Path) -> Dict[str, Dict[str, any]]:
    """
    Load all video URL files and create a mapping from video_id to sheet info.
    
    Args:
        video_urls_dir: Directory containing video URL JSON files
    
    Returns:
        Dict mapping video_id to {sheet, video_index}
    """
    video_mapping = {}
    
    # Hardcoded list of video URL files
    VIDEO_URL_FILES = [
        "caption/video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_564_to_658.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_658_to_752.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json",
        "caption/video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_940_to_950.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_950_to_960.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_960_to_970.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_970_to_980.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_980_to_990.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_990_to_1000.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_1000_to_1010.json",
        "caption/video_urls/20250406_setup_and_motion/overlap_1010_to_1020.json",
        "caption/video_urls/20250912_setup_and_motion/overlap_1020_to_1030.json",
        "caption/video_urls/20250912_setup_and_motion/overlap_1030_to_1040.json",
        "caption/video_urls/20250912_setup_and_motion/overlap_1040_to_1050.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1050_to_1060.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1060_to_1070.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1070_to_1080.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1080_to_1090.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1090_to_1100.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1100_to_1110.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1110_to_1120.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1120_to_1130.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1130_to_1140.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1140_to_1150.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1150_to_1160.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1160_to_1170.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1170_to_1180.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1180_to_1190.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1190_to_1200.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1200_to_1210.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1210_to_1220.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1220_to_1230.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1230_to_1240.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1240_to_1250.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1250_to_1260.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1260_to_1270.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1270_to_1280.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1280_to_1290.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1290_to_1300.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1300_to_1310.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1310_to_1316.json",
        "caption/video_urls/20250406_setup_and_motion/0_to_10.json",
        "caption/video_urls/20250406_setup_and_motion/10_to_20.json",
        "caption/video_urls/20250406_setup_and_motion/20_to_30.json",
        "caption/video_urls/20250406_setup_and_motion/30_to_40.json",
        "caption/video_urls/20250406_setup_and_motion/40_to_50.json",
        "caption/video_urls/20250406_setup_and_motion/50_to_60.json",
        "caption/video_urls/20250406_setup_and_motion/60_to_70.json",
        "caption/video_urls/20250406_setup_and_motion/70_to_80.json",
        "caption/video_urls/20250406_setup_and_motion/80_to_90.json",
        "caption/video_urls/20250406_setup_and_motion/90_to_100.json",
        "caption/video_urls/20250406_setup_and_motion/100_to_110.json",
        "caption/video_urls/20250406_setup_and_motion/110_to_120.json",
        "caption/video_urls/20250406_setup_and_motion/120_to_130.json",
        "caption/video_urls/20250406_setup_and_motion/130_to_140.json",
        "caption/video_urls/20250406_setup_and_motion/140_to_150.json",
        "caption/video_urls/20250406_setup_and_motion/150_to_160.json",
        "caption/video_urls/20250406_setup_and_motion/160_to_170.json",
        "caption/video_urls/20250406_setup_and_motion/170_to_180.json",
        "caption/video_urls/20250406_setup_and_motion/180_to_190.json",
        "caption/video_urls/20250406_setup_and_motion/190_to_200.json",
        "caption/video_urls/20250406_setup_and_motion/200_to_210.json",
        "caption/video_urls/20250406_setup_and_motion/210_to_220.json",
        "caption/video_urls/20250406_setup_and_motion/220_to_230.json",
        "caption/video_urls/20250406_setup_and_motion/230_to_240.json",
        "caption/video_urls/20250406_setup_and_motion/240_to_250.json",
        "caption/video_urls/20250406_setup_and_motion/250_to_260.json",
        "caption/video_urls/20250406_setup_and_motion/260_to_270.json",
        "caption/video_urls/20250406_setup_and_motion/270_to_280.json",
        "caption/video_urls/20250406_setup_and_motion/280_to_290.json",
        "caption/video_urls/20250406_setup_and_motion/290_to_300.json",
        "caption/video_urls/20250406_setup_and_motion/300_to_310.json",
        "caption/video_urls/20250406_setup_and_motion/310_to_320.json",
        "caption/video_urls/20250406_setup_and_motion/320_to_330.json",
        "caption/video_urls/20250406_setup_and_motion/330_to_340.json",
        "caption/video_urls/20250406_setup_and_motion/340_to_350.json",
        "caption/video_urls/20250406_setup_and_motion/350_to_360.json",
        "caption/video_urls/20250406_setup_and_motion/360_to_370.json",
        "caption/video_urls/20250406_setup_and_motion/370_to_380.json",
        "caption/video_urls/20250406_setup_and_motion/380_to_390.json",
        "caption/video_urls/20250406_setup_and_motion/390_to_400.json",
        "caption/video_urls/20250406_setup_and_motion/400_to_410.json",
        "caption/video_urls/20250406_setup_and_motion/410_to_420.json",
        "caption/video_urls/20250406_setup_and_motion/420_to_430.json",
        "caption/video_urls/20250406_setup_and_motion/430_to_440.json",
        "caption/video_urls/20250406_setup_and_motion/440_to_450.json",
        "caption/video_urls/20250406_setup_and_motion/450_to_460.json",
        "caption/video_urls/20250406_setup_and_motion/460_to_470.json",
        "caption/video_urls/20250406_setup_and_motion/470_to_480.json",
        "caption/video_urls/20250406_setup_and_motion/480_to_490.json",
        "caption/video_urls/20250406_setup_and_motion/490_to_500.json",
        "caption/video_urls/20250406_setup_and_motion/500_to_510.json",
        "caption/video_urls/20250406_setup_and_motion/510_to_520.json",
        "caption/video_urls/20250406_setup_and_motion/520_to_530.json",
        "caption/video_urls/20250406_setup_and_motion/530_to_540.json",
        "caption/video_urls/20250406_setup_and_motion/540_to_550.json",
        "caption/video_urls/20250406_setup_and_motion/550_to_560.json",
        "caption/video_urls/20250406_setup_and_motion/560_to_570.json",
        "caption/video_urls/20250406_setup_and_motion/570_to_580.json",
        "caption/video_urls/20250406_setup_and_motion/580_to_590.json",
        "caption/video_urls/20250406_setup_and_motion/590_to_600.json",
        "caption/video_urls/20250406_setup_and_motion/600_to_610.json",
        "caption/video_urls/20250406_setup_and_motion/610_to_620.json",
        "caption/video_urls/20250406_setup_and_motion/620_to_630.json",
        "caption/video_urls/20250406_setup_and_motion/630_to_640.json",
        "caption/video_urls/20250406_setup_and_motion/640_to_650.json",
        "caption/video_urls/20250406_setup_and_motion/650_to_660.json",
        "caption/video_urls/20250406_setup_and_motion/660_to_670.json",
        "caption/video_urls/20250406_setup_and_motion/670_to_680.json",
        "caption/video_urls/20250406_setup_and_motion/680_to_690.json",
        "caption/video_urls/20250406_setup_and_motion/690_to_700.json",
        "caption/video_urls/20250406_setup_and_motion/700_to_710.json",
        "caption/video_urls/20250406_setup_and_motion/710_to_720.json",
        "caption/video_urls/20250406_setup_and_motion/720_to_730.json",
        "caption/video_urls/20250406_setup_and_motion/730_to_740.json",
        "caption/video_urls/20250406_setup_and_motion/740_to_750.json",
        "caption/video_urls/20250406_setup_and_motion/750_to_760.json",
        "caption/video_urls/20250406_setup_and_motion/760_to_770.json",
        "caption/video_urls/20250406_setup_and_motion/770_to_780.json",
        "caption/video_urls/20250406_setup_and_motion/780_to_790.json",
        "caption/video_urls/20250406_setup_and_motion/790_to_800.json",
        "caption/video_urls/20250406_setup_and_motion/800_to_810.json",
        "caption/video_urls/20250406_setup_and_motion/810_to_820.json",
        "caption/video_urls/20250406_setup_and_motion/820_to_830.json",
        "caption/video_urls/20250406_setup_and_motion/830_to_840.json",
        "caption/video_urls/20250406_setup_and_motion/840_to_850.json",
        "caption/video_urls/20250406_setup_and_motion/850_to_860.json",
        "caption/video_urls/20250406_setup_and_motion/860_to_870.json",
        "caption/video_urls/20250406_setup_and_motion/870_to_880.json",
        "caption/video_urls/20250406_setup_and_motion/880_to_890.json",
        "caption/video_urls/20250406_setup_and_motion/890_to_900.json",
        "caption/video_urls/20250406_setup_and_motion/900_to_910.json",
        "caption/video_urls/20250406_setup_and_motion/910_to_920.json",
        "caption/video_urls/20250406_setup_and_motion/920_to_930.json",
        "caption/video_urls/20250406_setup_and_motion/930_to_940.json",
        "caption/video_urls/20250406_setup_and_motion/940_to_950.json",
        "caption/video_urls/20250406_setup_and_motion/950_to_960.json",
        "caption/video_urls/20250406_setup_and_motion/960_to_970.json",
        "caption/video_urls/20250406_setup_and_motion/970_to_980.json",
        "caption/video_urls/20250406_setup_and_motion/980_to_990.json",
        "caption/video_urls/20250406_setup_and_motion/990_to_1000.json",
        "caption/video_urls/20250406_setup_and_motion/1000_to_1010.json",
        "caption/video_urls/20250406_setup_and_motion/1010_to_1020.json",
        "caption/video_urls/20250406_setup_and_motion/1020_to_1030.json",
        "caption/video_urls/20250406_setup_and_motion/1030_to_1040.json",
        "caption/video_urls/20250406_setup_and_motion/1040_to_1050.json",
        "caption/video_urls/20250406_setup_and_motion/1050_to_1060.json",
        "caption/video_urls/20250406_setup_and_motion/1060_to_1070.json",
        "caption/video_urls/20250406_setup_and_motion/1070_to_1080.json",
        "caption/video_urls/20250406_setup_and_motion/1080_to_1090.json",
        "caption/video_urls/20250406_setup_and_motion/1090_to_1100.json",
        "caption/video_urls/20250406_setup_and_motion/1100_to_1110.json",
        "caption/video_urls/20250406_setup_and_motion/1110_to_1120.json",
        "caption/video_urls/20250406_setup_and_motion/1120_to_1130.json",
        "caption/video_urls/20250406_setup_and_motion/1130_to_1140.json",
        "caption/video_urls/20250406_setup_and_motion/1140_to_1150.json",
        "caption/video_urls/20250406_setup_and_motion/1150_to_1160.json",
        "caption/video_urls/20250406_setup_and_motion/1160_to_1170.json",
        "caption/video_urls/20250406_setup_and_motion/1170_to_1180.json",
        "caption/video_urls/20250406_setup_and_motion/1180_to_1190.json",
        "caption/video_urls/20250912_setup_and_motion/1190_to_1200.json",
        "caption/video_urls/20250912_setup_and_motion/1200_to_1210.json",
        "caption/video_urls/20250912_setup_and_motion/1210_to_1220.json",
        "caption/video_urls/20250912_setup_and_motion/1220_to_1230.json",
        "caption/video_urls/20250912_setup_and_motion/1230_to_1240.json",
        "caption/video_urls/20250912_setup_and_motion/1240_to_1250.json",
        "caption/video_urls/20250912_setup_and_motion/1250_to_1260.json",
        "caption/video_urls/20250912_setup_and_motion/1260_to_1270.json",
        "caption/video_urls/20250912_setup_and_motion/1270_to_1280.json",
        "caption/video_urls/20250912_setup_and_motion/1280_to_1290.json",
        "caption/video_urls/20250912_setup_and_motion/1290_to_1300.json",
        "caption/video_urls/20250912_setup_and_motion/1300_to_1310.json",
        "caption/video_urls/20250912_setup_and_motion/1310_to_1320.json",
        "caption/video_urls/20250912_setup_and_motion/1320_to_1330.json",
        "caption/video_urls/20250912_setup_and_motion/1330_to_1340.json",
        "caption/video_urls/20250912_setup_and_motion/1340_to_1350.json",
        "caption/video_urls/20250912_setup_and_motion/1350_to_1360.json",
        "caption/video_urls/20250912_setup_and_motion/1360_to_1370.json",
        "caption/video_urls/20250912_setup_and_motion/1370_to_1380.json",
        "caption/video_urls/20250912_setup_and_motion/1380_to_1390.json",
        "caption/video_urls/20250912_setup_and_motion/1390_to_1400.json",
        "caption/video_urls/20250912_setup_and_motion/1400_to_1410.json",
        "caption/video_urls/20250912_setup_and_motion/1410_to_1420.json",
        "caption/video_urls/20250912_setup_and_motion/1420_to_1430.json",
        "caption/video_urls/20250912_setup_and_motion/1430_to_1440.json",
        "caption/video_urls/20250912_setup_and_motion/1440_to_1450.json",
        "caption/video_urls/20250912_setup_and_motion/1450_to_1460.json",
        "caption/video_urls/20250912_setup_and_motion/1460_to_1470.json",
        "caption/video_urls/20250912_setup_and_motion/1470_to_1480.json",
        "caption/video_urls/20250912_setup_and_motion/1480_to_1490.json",
        "caption/video_urls/20250912_setup_and_motion/1490_to_1500.json",
        "caption/video_urls/20250912_setup_and_motion/1500_to_1510.json",
        "caption/video_urls/20250912_setup_and_motion/1510_to_1520.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1520_to_1530.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1530_to_1540.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1540_to_1550.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1550_to_1560.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1560_to_1570.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1570_to_1580.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1580_to_1590.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1590_to_1600.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1600_to_1610.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1610_to_1620.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1620_to_1630.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1630_to_1640.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1640_to_1650.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1650_to_1660.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1660_to_1670.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1670_to_1680.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1680_to_1690.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1690_to_1700.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1700_to_1710.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1710_to_1720.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1720_to_1730.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1730_to_1740.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1740_to_1750.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1750_to_1760.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1760_to_1770.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1770_to_1780.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1780_to_1790.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1790_to_1800.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1800_to_1810.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1810_to_1820.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1820_to_1830.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1830_to_1840.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1840_to_1850.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1850_to_1860.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1860_to_1870.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1870_to_1880.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1880_to_1890.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1890_to_1900.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1900_to_1910.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1910_to_1920.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1920_to_1930.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1930_to_1940.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1940_to_1950.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1950_to_1960.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1960_to_1970.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1970_to_1980.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1980_to_1990.json",
        "caption/video_urls/20251021_ground_and_setup_folder/1990_to_2000.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2000_to_2010.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2010_to_2020.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2020_to_2030.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2030_to_2040.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2040_to_2050.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2050_to_2060.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2060_to_2070.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2070_to_2080.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2080_to_2090.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2090_to_2100.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2100_to_2110.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2110_to_2120.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2120_to_2130.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2130_to_2140.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2140_to_2150.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2150_to_2160.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2160_to_2170.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2170_to_2180.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2180_to_2190.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2190_to_2200.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2200_to_2210.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2210_to_2220.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2220_to_2230.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2230_to_2240.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2240_to_2250.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2250_to_2260.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2260_to_2270.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2270_to_2280.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2280_to_2290.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2290_to_2300.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2300_to_2310.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2310_to_2320.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2320_to_2330.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2330_to_2340.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2340_to_2350.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2350_to_2360.json",
        "caption/video_urls/20251021_ground_and_setup_folder/2360_to_2370.json",
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_invalid.json",
        "caption/video_urls/20251021_ground_and_setup_folder/nonoverlap_invalid.json",
    ]
    
    print(f"Loading video URLs from {len(VIDEO_URL_FILES)} hardcoded sheet files...")
    
    for file_path_str in VIDEO_URL_FILES:
        file_path = Path(file_path_str)
        sheet_name = file_path.stem  # Filename without .json extension
        
        # Check if file exists
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        try:
            with open(file_path, 'r') as f:
                video_urls = json.load(f)
            
            # Process each video URL in this sheet
            for idx, video_url in enumerate(video_urls):
                # Extract video_id from URL (filename)
                # Handle both full URLs and just filenames
                if video_url:
                    # Get the last part after the last '/'
                    video_id = video_url.split('/')[-1] if '/' in video_url else video_url
                    
                    if video_id:
                        # Store both the filename and the full URL for matching
                        video_mapping[video_id] = {
                            'sheet': sheet_name,
                            'video_index': idx,
                            'full_url': video_url
                        }
            
            if idx % 50 == 0 or idx == len(video_urls) - 1:  # Print less frequently
                print(f"  {sheet_name}: {len(video_urls)} videos")
            
        except Exception as e:
            print(f"Warning: Error loading {file_path}: {e}")
    
    print(f"Total videos mapped: {len(video_mapping)}")
    return video_mapping


def load_caption_export(export_path: Path):
    """Load caption export JSON file. Can be either list or dict format."""
    with open(export_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_export_statistics(export_data, video_mapping: Dict[str, Dict[str, any]]) -> Dict:
    """
    Analyze export data to count feedback by status and rating.
    
    Returns dict with:
    - total_approved_rejected: Total feedback in approved/rejected status
    - score_4_count: Count of 4-score pre-captions in approved/rejected
    - all_samples_approved_rejected: All samples with approved/rejected status
    - score_4_samples: Samples with 4-score pre-captions
    """
    # Handle both list and dict formats
    if isinstance(export_data, list):
        video_list = export_data
    else:
        video_list = list(export_data.values())
    
    all_samples_approved_rejected = []
    score_4_samples = []
    
    for video_data in video_list:
        video_id = video_data.get('video_id', '')
        captions = video_data.get('captions', {})
        
        for caption_type, caption_data in captions.items():
            # Skip if no caption_data
            if 'caption_data' not in caption_data:
                continue
            
            status = caption_data.get('status', '')
            
            # Only look at approved or rejected status
            if status not in ['approved', 'rejected']:
                continue
            
            caption_info = caption_data['caption_data']
            
            # Skip perfect pre-captions (no feedback needed)
            feedback_is_needed = caption_info.get('feedback_is_needed', True)
            if not feedback_is_needed:
                continue
            
            final_feedback = caption_info.get('final_feedback', '')
            
            # Safely handle None or non-string types
            if final_feedback is None:
                final_feedback = ''
            elif not isinstance(final_feedback, str):
                final_feedback = str(final_feedback)
            
            final_feedback = final_feedback.strip()
            
            # Only include samples with non-empty final_feedback
            if not final_feedback:
                continue
            
            # Extract sheet and video_index from video_mapping
            video_id_key = video_id  # The video_id is the filename
            
            # Try exact match first
            if video_id_key in video_mapping:
                sheet = video_mapping[video_id_key].get('sheet', 'N/A')
                video_index = video_mapping[video_id_key].get('video_index', 'N/A')
            else:
                # Try to find by checking if any URL contains this video_id
                sheet = 'N/A'
                video_index = 'N/A'
                for mapped_id, mapped_info in video_mapping.items():
                    if video_id in mapped_info.get('full_url', ''):
                        sheet = mapped_info.get('sheet', 'N/A')
                        video_index = mapped_info.get('video_index', 'N/A')
                        break
            
            # Create sample dict
            sample = {
                'video_id': video_id,
                'sheet': sheet,
                'video_index': video_index,
                'caption_type': caption_type,
                'status': status,
                'final_feedback': final_feedback,
                'pre_caption': caption_info.get('pre_caption', ''),
                'final_caption': caption_info.get('final_caption', ''),
                'user': caption_info.get('user', ''),
                'reviewer': caption_info.get('reviewer', ''),  # Add reviewer
                'timestamp': caption_info.get('timestamp', ''),
                'feedback_length': len(final_feedback),
                'initial_caption_rating_score': caption_info.get('initial_caption_rating_score')
            }
            
            # Add to approved/rejected list
            all_samples_approved_rejected.append(sample)
            
            # Check if it's a 4-score pre-caption
            if sample['initial_caption_rating_score'] == 4:
                score_4_samples.append(sample)
    
    return {
        'total_approved_rejected': len(all_samples_approved_rejected),
        'score_4_count': len(score_4_samples),
        'all_samples_approved_rejected': all_samples_approved_rejected,
        'score_4_samples': score_4_samples
    }


def count_text_changes(pre_caption: str, final_caption: str) -> int:
    """
    Count the number of word-level changes between two captions.
    Uses difflib to find changed words.
    """
    pre_words = pre_caption.split()
    final_words = final_caption.split()
    
    matcher = difflib.SequenceMatcher(None, pre_words, final_words)
    changes = 0
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ['replace', 'delete', 'insert']:
            changes += max(i2 - i1, j2 - j1)
    
    return changes


def has_camera_pattern(caption: str) -> bool:
    """
    Check if caption contains camera angle/level patterns:
    1. "{level}-level angle" (e.g., "eye-level angle", "hip-level angle")
    2. Specific angle patterns: "aerial angle", "overhead angle", "eye angle", "hip angle", "ground angle"
    
    Returns True if any pattern is found, False otherwise.
    """
    levels = ['eye', 'hip', 'water', 'ground', 'aerial', 'overhead', 'underwater']
    specific_angles = ['aerial angle', 'overhead angle', 'eye angle', 'hip angle', 'ground angle']
    
    caption_lower = caption.lower()
    
    # Pattern 1: "{level}-level angle"
    for level in levels:
        pattern = f"{level}-level angle"
        if pattern in caption_lower:
            return True
    
    # Pattern 2: Specific angle patterns
    for angle_pattern in specific_angles:
        if angle_pattern in caption_lower:
            return True
    
    return False


def extract_samples_from_export(export_data, sample_count: int, seed: int, video_mapping: Dict[str, Dict[str, any]]) -> Tuple[List[Dict], int, Dict]:
    """
    Extract samples with final_feedback from export data.
    Extracts all approved/rejected samples that have camera pattern.
    
    Args:
        export_data: Can be either a list of video objects or a dict keyed by video_id
        sample_count: Number of samples to select (-1 for all)
        seed: Random seed
    
    Returns:
        (samples, total_count, statistics) where:
        - samples: list of sampled samples with camera pattern
        - total_count: total samples with camera pattern available
        - statistics: dict with counts by status and rating
    """
    random.seed(seed)
    
    # Get statistics
    stats = analyze_export_statistics(export_data, video_mapping)
    
    # Use all approved/rejected samples (not just 4-score)
    all_samples = stats['all_samples_approved_rejected']
    
    # Filter for samples with camera pattern
    camera_samples = [s for s in all_samples if has_camera_pattern(s['pre_caption'])]
    
    total_size = len(camera_samples)
    
    # Add change count to each sample
    for sample in camera_samples:
        sample['num_changes'] = count_text_changes(sample['pre_caption'], sample['final_caption'])
    
    # Update stats to include camera pattern info
    stats['with_camera_pattern'] = total_size
    
    # Sample
    if sample_count == -1:
        print(f"Using full dataset with camera pattern: {total_size} samples")
        return camera_samples, total_size, stats
    elif len(camera_samples) < sample_count:
        print(f"Warning: Only {len(camera_samples)} samples with camera pattern available, requested {sample_count}")
        return camera_samples, total_size, stats
    
    return random.sample(camera_samples, sample_count), total_size, stats


def classify_feedback_introduces_wrong_terminology(final_feedback: str, pre_caption: str, final_caption: str, 
                                                     model: str = "gpt-4o-2024-08-06", secrets=None) -> Tuple[str, str, str]:
    """
    Classify whether feedback introduces wrong camera angle/level terminology as a correction.
    
    Returns:
        (label, rationale, raw_response)
        label: "Yes" or "No" or "Unexpected"
    """
    prompt = CAMERA_NITPICK_DETECTION_PROMPT.format(
        final_feedback=final_feedback,
        pre_caption=pre_caption,
        final_caption=final_caption
    )
    
    # Load secrets from environment if not provided
    if secrets is None:
        import os
        secrets = {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "gemini_key": os.getenv("GEMINI_API_KEY")
        }
    
    llm = get_llm(model, secrets=secrets)
    
    try:
        try:
            response = llm.generate(prompt)
        except Exception as llm_error:
            print(f"LLM generation error: {llm_error}")
            import traceback
            traceback.print_exc()
            return "Unexpected", f"LLM Error: {str(llm_error)}", str(llm_error)
            
        raw_response = response.strip()
        
        # Parse response - look for "Rationale:" and "Classification:" markers
        rationale = ""
        classification = ""
        
        # Find the positions of the markers
        rationale_marker = "Rationale:"
        classification_marker = "Classification:"
        
        rationale_idx = raw_response.find(rationale_marker)
        classification_idx = raw_response.find(classification_marker)
        
        if rationale_idx != -1 and classification_idx != -1:
            # Extract text between markers
            rationale_start = rationale_idx + len(rationale_marker)
            rationale = raw_response[rationale_start:classification_idx].strip()
            
            # Extract classification after the marker
            classification_start = classification_idx + len(classification_marker)
            classification_text = raw_response[classification_start:].strip()
            
            # Get just the first word/line of classification
            classification = classification_text.split('\n')[0].strip()
            
            # Clean up classification - remove any extra punctuation
            classification = classification.replace('.', '').replace(',', '').strip()
        else:
            # Fallback: try to find Yes/No in the response
            raw_lower = raw_response.lower()
            if 'classification: yes' in raw_lower or raw_response.strip().lower() == 'yes':
                classification = "Yes"
                rationale = raw_response
            elif 'classification: no' in raw_lower or raw_response.strip().lower() == 'no':
                classification = "No"
                rationale = raw_response
            else:
                # Try to extract from anywhere in response
                lines = raw_response.split('\n')
                for line in lines:
                    line_clean = line.strip().lower()
                    if line_clean in ['yes', 'no']:
                        classification = line_clean.capitalize()
                        rationale = raw_response
                        break
        
        # Validate classification
        if classification in ["Yes", "No"]:
            return classification, rationale, raw_response
        else:
            return "Unexpected", f"Could not parse: {raw_response[:200]}", raw_response
            
    except Exception as e:
        print(f"Error classifying: {e}")
        import traceback
        return "Unexpected", f"Error: {str(e)}\n{traceback.format_exc()}", str(e)


def classify_sample_worker(sample: Dict, model: str, secrets: Dict) -> Dict:
    """Worker function to classify a single sample (for parallel processing)"""
    label, rationale, raw_response = classify_feedback_introduces_wrong_terminology(
        sample['final_feedback'],
        sample['pre_caption'],
        sample['final_caption'],
        model=model,
        secrets=secrets
    )
    sample['label'] = label
    sample['rationale'] = rationale
    sample['raw_response'] = raw_response
    return sample


def print_examples(samples: List[Dict], num_examples: int = 5):
    """Print example samples."""
    print(f"\n{'='*80}")
    print(f"Sample Examples (showing {min(num_examples, len(samples))} of {len(samples)})")
    print(f"{'='*80}\n")
    
    for i, sample in enumerate(samples[:num_examples], 1):
        print(f"Example {i}:")
        print(f"Video ID: {sample['video_id']}")
        print(f"Sheet: {sample.get('sheet', 'N/A')}")
        print(f"Video Index: {sample.get('video_index', 'N/A')}")
        print(f"Caption Type: {sample['caption_type']}")
        print(f"Status: {sample['status']}")
        print(f"User: {sample.get('user', 'N/A')}")
        print(f"Reviewer: {sample.get('reviewer', 'N/A')}")
        print(f"Rating Score: {sample.get('initial_caption_rating_score', 'N/A')}")
        print(f"Feedback Length: {sample['feedback_length']} chars")
        print(f"Number of Changes: {sample.get('num_changes', 'N/A')} words")
        print(f"Pre-caption snippet: {sample['pre_caption'][:200]}...")
        print(f"Final Feedback: {sample['final_feedback'][:200]}...")
        print()


def generate_report(samples: List[Dict], seed: int, timestamp: str, 
                   output_path: Path, total_dataset_size: int, export_file: str, stats: Dict):
    """Generate markdown report with statistics and examples."""
    
    # Calculate statistics
    total = len(samples)
    yes_samples = [s for s in samples if s['label'] == 'Yes']
    no_samples = [s for s in samples if s['label'] == 'No']
    unexpected_samples = [s for s in samples if s['label'] == 'Unexpected']
    
    yes_count = len(yes_samples)
    no_count = len(no_samples)
    unexpected_count = len(unexpected_samples)
    
    yes_pct = (yes_count / total * 100) if total > 0 else 0
    no_pct = (no_count / total * 100) if total > 0 else 0
    unexpected_pct = (unexpected_count / total * 100) if total > 0 else 0
    
    # Analyze feedback length and change count statistics
    yes_lengths = [s['feedback_length'] for s in yes_samples]
    no_lengths = [s['feedback_length'] for s in no_samples]
    yes_changes = [s['num_changes'] for s in yes_samples]
    no_changes = [s['num_changes'] for s in no_samples]
    
    avg_yes_length = sum(yes_lengths) / len(yes_lengths) if yes_lengths else 0
    avg_no_length = sum(no_lengths) / len(no_lengths) if no_lengths else 0
    avg_yes_changes = sum(yes_changes) / len(yes_changes) if yes_changes else 0
    avg_no_changes = sum(no_changes) / len(no_changes) if no_changes else 0
    
    # Start building report
    report = f"""# Camera Angle/Height Order-Swapping Confusion Detection Report

## Dataset Information

- **Source Export File**: {export_file}
- **Total Feedback (Approved/Rejected only)**: {stats['total_approved_rejected']}
- **With Camera Pattern**: {stats.get('with_camera_pattern', 0)} ({stats.get('with_camera_pattern', 0)/stats['total_approved_rejected']*100:.2f}% of approved/rejected)
- **Sampled for Analysis**: {total} samples (all from approved/rejected with camera pattern)
- **Random Seed**: {seed}
- **Timestamp**: {timestamp}

## What We're Detecting

This analysis looks for feedback that discusses **order-swapping or terminology confusion** with camera angle/height terms, such as:
- Swapping order: "high, eye-level angle" ↔ "eye-level, high angle" (same content, different order)
- Wrong terminology: using "*-level angle" (e.g., "eye-level angle", "hip-level angle")

This is **NOT** about detecting actual camera angle/height changes like:
- "high angle" → "low angle" (actual angle change)
- "eye level" → "ground level" (actual height change)

## Classification Prompt

The following prompt was used to classify critiques:
```
{CAMERA_NITPICK_DETECTION_PROMPT}
```

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage | Avg Feedback Length | Avg Word Changes |
|-------|-------|------------|---------------------|------------------|
| Yes (Order-Swap/Terminology Confusion) | {yes_count} | {yes_pct:.2f}% | {avg_yes_length:.0f} chars | {avg_yes_changes:.1f} words |
| No (Actual Changes or Other) | {no_count} | {no_pct:.2f}% | {avg_no_length:.0f} chars | {avg_no_changes:.1f} words |
| Unexpected | {unexpected_count} | {unexpected_pct:.2f}% | - | - |
| **Total** | {total} | 100.00% | - | - |

"""

    if unexpected_count > 0:
        report += f"\n⚠️ **Warning**: {unexpected_count} samples received unexpected responses from the classifier.\n\n"
    
    # Add sample examples section
    report += "## Sample Examples\n\n"
    
    # Show ALL examples for each category
    yes_examples = yes_samples  # Show all order-swap confusion
    no_examples = random.sample(no_samples, min(20, len(no_samples))) if no_samples else []  # Limit others to 20
    
    if yes_examples:
        report += f"### Order-Swap/Terminology Confusion - Yes ({len(yes_examples)} shown)\n\n"
        for i, example in enumerate(yes_examples, 1):
            report += f"#### Yes Example {i}\n\n"
            report += f"**Video ID**: {example['video_id']}\n\n"
            report += f"**Sheet**: {example.get('sheet', 'N/A')}\n\n"
            report += f"**Video Index**: {example.get('video_index', 'N/A')}\n\n"
            report += f"**Caption Type**: {example['caption_type']}\n\n"
            report += f"**Status**: {example['status']}\n\n"
            report += f"**User**: {example.get('user', 'N/A')}\n\n"
            report += f"**Reviewer**: {example.get('reviewer', 'N/A')}\n\n"
            report += f"**Rating Score**: {example.get('initial_caption_rating_score', 'N/A')}\n\n"
            report += f"**Feedback Length**: {example['feedback_length']} chars\n\n"
            report += f"**Number of Changes**: {example['num_changes']} words\n\n"
            report += f"**Final Feedback**: {example['final_feedback']}\n\n"
            report += f"**Pre-Caption**:\n```\n{example['pre_caption']}\n```\n\n"
            report += f"**Final Caption**:\n```\n{example['final_caption']}\n```\n\n"
            report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += f"**Classification**: {example['label']}\n\n"
            report += "---\n\n"
    
    if no_examples:
        report += f"### Actual Changes or Other - No ({len(no_examples)} shown)\n\n"
        for i, example in enumerate(no_examples, 1):
            report += f"#### No Example {i}\n\n"
            report += f"**Video ID**: {example['video_id']}\n\n"
            report += f"**Sheet**: {example.get('sheet', 'N/A')}\n\n"
            report += f"**Video Index**: {example.get('video_index', 'N/A')}\n\n"
            report += f"**Caption Type**: {example['caption_type']}\n\n"
            report += f"**Status**: {example['status']}\n\n"
            report += f"**User**: {example.get('user', 'N/A')}\n\n"
            report += f"**Reviewer**: {example.get('reviewer', 'N/A')}\n\n"
            report += f"**Rating Score**: {example.get('initial_caption_rating_score', 'N/A')}\n\n"
            report += f"**Feedback Length**: {example['feedback_length']} chars\n\n"
            report += f"**Number of Changes**: {example['num_changes']} words\n\n"
            report += f"**Final Feedback**: {example['final_feedback']}\n\n"
            report += f"**Pre-Caption**:\n```\n{example['pre_caption']}\n```\n\n"
            report += f"**Final Caption**:\n```\n{example['final_caption']}\n```\n\n"
            report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += f"**Classification**: {example['label']}\n\n"
            report += "---\n\n"
    
    # All samples in sequence
    report += "## All Samples (Complete Sequence)\n\n"
    for i, sample in enumerate(samples, 1):
        report += f"### Sample {i}/{total} - [{sample['label']}]\n\n"
        report += f"**Video ID**: {sample['video_id']}\n\n"
        report += f"**Sheet**: {sample.get('sheet', 'N/A')}\n\n"
        report += f"**Video Index**: {sample.get('video_index', 'N/A')}\n\n"
        report += f"**Caption Type**: {sample['caption_type']}\n\n"
        report += f"**Status**: {sample['status']}\n\n"
        report += f"**User**: {sample.get('user', 'N/A')}\n\n"
        report += f"**Reviewer**: {sample.get('reviewer', 'N/A')}\n\n"
        report += f"**Rating Score**: {sample.get('initial_caption_rating_score', 'N/A')}\n\n"
        report += f"**Feedback Length**: {sample['feedback_length']} chars\n\n"
        report += f"**Number of Changes**: {sample['num_changes']} words\n\n"
        report += f"**Final Feedback**: {sample['final_feedback']}\n\n"
        report += f"**Pre-Caption**:\n```\n{sample['pre_caption']}\n```\n\n"
        report += f"**Final Caption**:\n```\n{sample['final_caption']}\n```\n\n"
        report += f"**Rationale**: {sample.get('rationale', 'N/A')}\n\n"
        report += f"**Classification**: {sample['label']}\n\n"
        if sample['label'] == 'Unexpected':
            report += f"**Raw Response**: {sample.get('raw_response', 'N/A')}\n\n"
        report += "---\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def generate_html_report(samples: List[Dict], output_path: Path, video_mapping: Dict[str, Dict[str, any]]):
    """Generate an interactive HTML report with embedded videos."""
    import html as html_module
    
    # Separate Yes and No samples
    yes_samples = [s for s in samples if s.get('label') == 'Yes']
    no_samples = [s for s in samples if s.get('label') == 'No']
    
    html_content = []
    
    # HTML header with styling
    html_content.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Order-Swap Confusion Detection Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; margin-bottom: 20px; font-size: 2.5em; }
        h2 { color: #34495e; margin: 30px 0 15px 0; font-size: 1.8em; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .summary {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 30px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #3498db; }
        .stat-label { color: #7f8c8d; font-size: 0.9em; }
        .video-card {
            background: #fafafa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .video-card.yes { border-left: 4px solid #e74c3c; }
        .video-card.no { border-left: 4px solid #27ae60; }
        .video-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .video-container {
            margin: 20px 0;
            background: white;
            padding: 15px;
            border-radius: 8px;
        }
        video {
            width: 100%;
            max-width: 800px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 6px;
        }
        .metadata-item {
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .metadata-label {
            font-weight: bold;
            color: #34495e;
            font-size: 0.9em;
        }
        .metadata-value {
            color: #555;
        }
        .caption-box {
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 6px;
            border-left: 3px solid #3498db;
        }
        .caption-box h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        .caption-text {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 4px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
        }
        .rationale-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 6px;
        }
        .classification {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        .classification.yes { background: #e74c3c; color: white; }
        .classification.no { background: #27ae60; color: white; }
        .navigation {
            background: #34495e;
            color: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 30px;
        }
        .navigation a {
            color: #3498db;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
        }
        .navigation a:hover { background: rgba(52, 152, 219, 0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>📹 Camera Order-Swap Confusion Detection Report</h1>
''')
    
    # Summary section
    total = len(samples)
    yes_count = len(yes_samples)
    no_count = len(no_samples)
    
    html_content.append(f'''
        <div class="summary">
            <h2>📊 Summary</h2>
            <div class="summary-grid">
                <div class="stat-item">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">Total Samples</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{yes_count}</div>
                    <div class="stat-label">Order-Swap Confusion</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{no_count}</div>
                    <div class="stat-label">Actual Changes/Other</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{yes_count/total*100:.1f}%</div>
                    <div class="stat-label">Confusion Rate</div>
                </div>
            </div>
        </div>
''')
    
    # Navigation
    html_content.append('''
        <div class="navigation">
            <strong>Quick Navigation:</strong>
            <a href="#yes-samples">Order-Swap Confusion (Yes)</a> |
            <a href="#no-samples">Actual Changes/Other (No)</a>
        </div>
''')
    
    # Yes samples section
    if yes_samples:
        html_content.append(f'<h2 id="yes-samples">🔴 Order-Swap Confusion - Yes ({len(yes_samples)} samples)</h2>')
        
        for i, sample in enumerate(yes_samples, 1):
            # Get video URL from mapping
            video_url = video_mapping.get(sample['video_id'], {}).get('full_url', '')
            
            html_content.append(f'''
                <div class="video-card yes">
                    <div class="video-title">Sample {i}/{len(yes_samples)}: {html_module.escape(sample['video_id'])}</div>
                    
                    <div class="metadata">
                        <div class="metadata-item">
                            <div class="metadata-label">Sheet:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('sheet', 'N/A')))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Video Index:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('video_index', 'N/A')))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">User:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('user', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Reviewer:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('reviewer', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Status:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('status', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Rating Score:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('initial_caption_rating_score', 'N/A')))}/5</div>
                        </div>
                    </div>
''')
            
            # Video player if URL available
            if video_url:
                html_content.append(f'''
                    <div class="video-container">
                        <video controls>
                            <source src="{html_module.escape(video_url)}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <div style="margin-top: 10px; text-align: right;">
                            <a href="{html_module.escape(video_url)}" download style="color: #3498db; text-decoration: none;">📥 Download Video</a>
                        </div>
                    </div>
''')
            
            html_content.append(f'''
                    <div class="caption-box">
                        <h3>Pre-Caption:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('pre_caption', ''))}</div>
                    </div>
                    
                    <div class="caption-box">
                        <h3>Final Feedback:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('final_feedback', ''))}</div>
                    </div>
                    
                    <div class="caption-box">
                        <h3>Final Caption:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('final_caption', ''))}</div>
                    </div>
                    
                    <div class="rationale-box">
                        <strong>Rationale:</strong> {html_module.escape(sample.get('rationale', 'N/A'))}
                    </div>
                    
                    <div style="margin-top: 15px;">
                        <span class="classification yes">YES - Order-Swap Confusion</span>
                    </div>
                </div>
''')
    
    # No samples section
    if no_samples:
        html_content.append(f'<h2 id="no-samples">🟢 Actual Changes/Other - No ({len(no_samples)} samples)</h2>')
        
        # Show ALL No samples
        display_no_samples = no_samples
        
        for i, sample in enumerate(display_no_samples, 1):
            # Get video URL from mapping
            video_url = video_mapping.get(sample['video_id'], {}).get('full_url', '')
            
            html_content.append(f'''
                <div class="video-card no">
                    <div class="video-title">Sample {i}/{len(display_no_samples)}: {html_module.escape(sample['video_id'])}</div>
                    
                    <div class="metadata">
                        <div class="metadata-item">
                            <div class="metadata-label">Sheet:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('sheet', 'N/A')))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Video Index:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('video_index', 'N/A')))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">User:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('user', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Reviewer:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('reviewer', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Status:</div>
                            <div class="metadata-value">{html_module.escape(sample.get('status', 'N/A'))}</div>
                        </div>
                        <div class="metadata-item">
                            <div class="metadata-label">Rating Score:</div>
                            <div class="metadata-value">{html_module.escape(str(sample.get('initial_caption_rating_score', 'N/A')))}/5</div>
                        </div>
                    </div>
''')
            
            # Video player if URL available
            if video_url:
                html_content.append(f'''
                    <div class="video-container">
                        <video controls>
                            <source src="{html_module.escape(video_url)}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <div style="margin-top: 10px; text-align: right;">
                            <a href="{html_module.escape(video_url)}" download style="color: #3498db; text-decoration: none;">📥 Download Video</a>
                        </div>
                    </div>
''')
            
            html_content.append(f'''
                    <div class="caption-box">
                        <h3>Pre-Caption:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('pre_caption', ''))}</div>
                    </div>
                    
                    <div class="caption-box">
                        <h3>Final Feedback:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('final_feedback', ''))}</div>
                    </div>
                    
                    <div class="caption-box">
                        <h3>Final Caption:</h3>
                        <div class="caption-text">{html_module.escape(sample.get('final_caption', ''))}</div>
                    </div>
                    
                    <div class="rationale-box">
                        <strong>Rationale:</strong> {html_module.escape(sample.get('rationale', 'N/A'))}
                    </div>
                    
                    <div style="margin-top: 15px;">
                        <span class="classification no">NO - Actual Changes/Other</span>
                    </div>
                </div>
''')
    
    # HTML footer
    html_content.append('''
    </div>
</body>
</html>
''')
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))
    
    print(f"✅ HTML report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect camera angle/height order-swapping confusion in caption export data"
    )
    parser.add_argument(
        '--export-file',
        type=str,
        default='caption_export/export_20251104_0552/all_videos_with_captions_20251104_0552.json',
        help='Path to caption export JSON file (e.g., caption_export/export_20251104_0552/all_videos_with_captions_20251104_0552.json)'
    )
    parser.add_argument(
        '--video-urls-dir',
        type=str,
        default='video_urls',
        help='Directory containing video URL JSON files (default: video_urls)'
    )
    parser.add_argument(
        '--sample-count',
        type=int,
        default=-1,
        help='Number of samples to randomly select. Use -1 for full dataset (default: -1)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=100,
        help='Random seed for reproducibility (default: 100)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4o-2024-08-06',
        help='Model to use for classification (default: gpt-4o-2024-08-06)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=30,
        help='Number of parallel workers for classification (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Set random seed
    random.seed(args.seed)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Setup paths
    export_path = Path(args.export_file)
    if not export_path.exists():
        print(f"Error: Export file not found: {export_path}")
        return
    
    # Setup video URLs directory
    video_urls_dir = Path(args.video_urls_dir)
    if not video_urls_dir.is_absolute():
        # Make it relative to current working directory
        video_urls_dir = Path.cwd() / video_urls_dir
    
    print(f"Video URLs directory: {video_urls_dir}")
    
    # Generate run directory name
    export_basename = export_path.stem
    if args.sample_count == -1:
        run_dir = f"camera_order_swap_confusion_full_dataset_{timestamp}"
    else:
        run_dir = f"camera_order_swap_confusion_seed{args.seed}_{timestamp}"
    
    output_dir = export_path.parent / run_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Camera Angle/Height Order-Swapping Confusion Detection")
    print(f"{'='*80}\n")
    print(f"Export file: {export_path}")
    print(f"Output directory: {output_dir}")
    print(f"Model: {args.model}")
    print(f"Sample count: {'Full dataset' if args.sample_count == -1 else args.sample_count}")
    print(f"Random seed: {args.seed}")
    print(f"Parallel workers: {args.workers}")
    
    # Load export data
    print(f"\nLoading export data...")
    export_data = load_caption_export(export_path)
    
    # Load video URL files to get sheet and video_index mapping
    video_mapping = load_video_url_files_mapping(video_urls_dir)
    
    # Extract samples with statistics
    print(f"\nAnalyzing export data statistics...")
    samples, total_dataset_size, stats = extract_samples_from_export(
        export_data, args.sample_count, args.seed, video_mapping
    )
    
    print(f"\n{'='*80}")
    print("Dataset Statistics:")
    print(f"{'='*80}")
    print(f"Total feedback (approved/rejected status only): {stats['total_approved_rejected']}")
    print(f"With camera pattern: {stats.get('with_camera_pattern', 0)} ({stats.get('with_camera_pattern', 0)/stats['total_approved_rejected']*100:.2f}%)")
    print(f"Sampled for analysis: {len(samples)} (all from approved/rejected with camera pattern)")
    print(f"{'='*80}")
    
    # Print examples
    print_examples(samples, num_examples=5)
    
    # Load secrets for LLM
    secrets = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "gemini_key": os.getenv("GEMINI_API_KEY")
    }
    
    # Classify samples with parallel processing
    print(f"\n{'='*80}")
    print(f"Classifying critiques with {args.model} using {args.workers} workers...")
    print(f"{'='*80}\n")
    
    completed = 0
    progress_lock = Lock()
    
    # Create a mapping to track which sample corresponds to which future
    sample_to_index = {id(sample): idx for idx, sample in enumerate(samples)}
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_index = {}
        for idx, sample in enumerate(samples):
            future = executor.submit(classify_sample_worker, sample, args.model, secrets)
            future_to_index[future] = idx
        
        # Process completed tasks and update samples in place
        for future in as_completed(future_to_index):
            try:
                result = future.result()
                idx = future_to_index[future]
                # Update the original sample in the list
                samples[idx] = result
                
                with progress_lock:
                    completed += 1
                    if completed % 50 == 0 or completed == len(samples):
                        print(f"Progress: {completed}/{len(samples)} ({completed/len(samples)*100:.1f}%)")
            except Exception as e:
                print(f"Error processing sample: {e}")
                # Even on error, mark as unexpected
                idx = future_to_index[future]
                samples[idx]['label'] = 'Unexpected'
                samples[idx]['rationale'] = f'Error: {str(e)}'
                samples[idx]['raw_response'] = str(e)
    
    print(f"\n✅ Classified all {len(samples)} samples\n")
    
    # Save sampled data
    sampled_data_path = output_dir / 'sampled_data.jsonl'
    with open(sampled_data_path, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"✅ Sampled data saved to: {sampled_data_path}")
    
    # Generate report
    report_path = output_dir / 'report.md'
    generate_report(
        samples,
        args.seed,
        timestamp,
        report_path,
        total_dataset_size,
        str(export_path),
        stats
    )
    
    # Print summary
    yes_count = sum(1 for s in samples if s['label'] == 'Yes')
    no_count = sum(1 for s in samples if s['label'] == 'No')
    unexpected_count = sum(1 for s in samples if s['label'] == 'Unexpected')
    
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Order-Swap/Terminology Confusion (Yes): {yes_count} ({yes_count/len(samples)*100:.2f}%)")
    print(f"Actual Changes or Other (No): {no_count} ({no_count/len(samples)*100:.2f}%)")
    print(f"Unexpected: {unexpected_count} ({unexpected_count/len(samples)*100:.2f}%)")
    print(f"{'='*80}\n")
    
    # Generate HTML report
    html_path = output_dir / 'report.html'
    print(f"\nGenerating HTML report with embedded videos...")
    generate_html_report(samples, html_path, video_mapping)
    print(f"🌐 Open {html_path} in a web browser to view the interactive report with videos!")


if __name__ == "__main__":
    main()