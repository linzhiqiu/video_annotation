#!/usr/bin/env python3
"""
Extract Static HTML Website for Video Annotations

This script generates a static HTML website showing:
- Videos that are completed (all 5 captions approved/rejected) with:
  * Video player (with download link)
  * Pre-caption
  * Human written feedback (final_feedback)
  * Final caption
  * Annotator and reviewer names
  * Crowd captions if available (from overlap section)
- Videos that are not fully completed with:
  * Status for each of the 5 caption types (subject, scene, motion, spatial, camera)

Usage:
    python extract_static_html.py <export_file> --output <output_html> \\
        --adobe-excel-files adobe_2_19.xlsx adobe_2_17.xlsx
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import html

# Try to import pandas for Excel reading
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def load_adobe_captions(adobe_excel_files: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Load crowd captions from Adobe Excel files.
    
    Returns:
        Dict mapping video filename to caption data
    """
    if not adobe_excel_files or not PANDAS_AVAILABLE:
        return {}
    
    adobe_captions = {}
    
    for excel_file in adobe_excel_files:
        print(f"Loading crowd captions from {excel_file}...")
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        for _, row in df.iterrows():
            # Extract filename from URL
            stock_url = None
            for col in df.columns:
                if 'stock_url' in col.lower():
                    stock_url = row[col]
                    break
            
            if not stock_url:
                continue
            
            filename = stock_url.split('/')[-1] if isinstance(stock_url, str) else ""
            
            caption_dict = {}
            
            # Map columns to caption types
            for col in df.columns:
                col_lower = col.lower()
                value = row[col]
                
                # Skip empty values
                if pd.isna(value) or value == "":
                    continue
                
                if 'content_id' in col_lower:
                    caption_dict['content_id'] = value
                elif ('subject' in col_lower and 'background' in col_lower) or 'who or what is in the image' in col_lower:
                    caption_dict['subject_background'] = value
                elif ('subject' in col_lower and 'action' in col_lower) or 'what are they doing' in col_lower:
                    caption_dict['subject_motion'] = value
                elif 'camera' in col_lower or 'how is it captured' in col_lower:
                    caption_dict['camera'] = value
            
            if filename and caption_dict:
                adobe_captions[filename] = caption_dict
    
    print(f"Loaded crowd captions for {len(adobe_captions)} videos")
    return adobe_captions


def get_video_filename(video_url: str) -> str:
    """Extract filename from video URL."""
    return video_url.split('/')[-1] if video_url else ""


def is_video_completed(captions: Dict[str, Any], required_types: List[str]) -> bool:
    """
    Check if all required caption types are completed (approved or rejected).
    """
    for caption_type in required_types:
        if caption_type not in captions:
            return False
        status = captions[caption_type].get("status", "not_completed")
        if status == "not_completed":
            return False
    return True


def has_any_completed_caption(captions: Dict[str, Any], required_types: List[str]) -> bool:
    """
    Check if video has at least one completed caption (approved or rejected).
    """
    for caption_type in required_types:
        if caption_type in captions:
            status = captions[caption_type].get("status", "not_completed")
            if status != "not_completed":
                return True
    return False


def get_caption_status_summary(captions: Dict[str, Any], required_types: List[str]) -> Dict[str, str]:
    """Get status summary for each caption type."""
    status_summary = {}
    for caption_type in required_types:
        if caption_type not in captions:
            status_summary[caption_type] = "not_started"
        else:
            status = captions[caption_type].get("status", "not_completed")
            status_summary[caption_type] = status
    return status_summary


def generate_completed_video_html(video_data: Dict[str, Any], adobe_captions: Dict[str, Dict[str, str]]) -> str:
    """Generate HTML for a completed video."""
    video_id = video_data.get("video_id", "unknown")
    video_url = video_data.get("video_url", "")
    captions = video_data.get("captions", {})
    
    # Get video filename for Adobe lookup
    video_filename = get_video_filename(video_url)
    crowd_caption = adobe_captions.get(video_filename, {})
    has_crowd_captions = bool(crowd_caption)
    
    html_parts = []
    
    # Video header
    html_parts.append(f'<div class="video-section" id="{html.escape(video_id)}">')
    html_parts.append(f'<h2 class="video-title">{html.escape(video_id)}</h2>')
    
    # Video player with download
    html_parts.append('<div class="video-container">')
    html_parts.append(f'<video controls width="100%">')
    html_parts.append(f'  <source src="{html.escape(video_url)}" type="video/mp4">')
    html_parts.append('  Your browser does not support the video tag.')
    html_parts.append('</video>')
    html_parts.append(f'<div class="download-link"><a href="{html.escape(video_url)}" download>📥 Download Video</a></div>')
    html_parts.append('</div>')
    
    # Crowd captions section (if available)
    if has_crowd_captions:
        html_parts.append('<div class="crowd-captions">')
        html_parts.append('<h3>👥 Crowd Captions (Adobe Annotations)</h3>')
        html_parts.append('<div class="crowd-caption-grid">')
        
        if 'subject_background' in crowd_caption:
            html_parts.append('<div class="crowd-caption-item">')
            html_parts.append('<strong>Subject & Background:</strong>')
            html_parts.append(f'<p>{html.escape(crowd_caption["subject_background"])}</p>')
            html_parts.append('</div>')
        
        if 'subject_motion' in crowd_caption:
            html_parts.append('<div class="crowd-caption-item">')
            html_parts.append('<strong>Subject Motion:</strong>')
            html_parts.append(f'<p>{html.escape(crowd_caption["subject_motion"])}</p>')
            html_parts.append('</div>')
        
        if 'camera' in crowd_caption:
            html_parts.append('<div class="crowd-caption-item">')
            html_parts.append('<strong>Camera:</strong>')
            html_parts.append(f'<p>{html.escape(crowd_caption["camera"])}</p>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
    
    # Caption details
    html_parts.append('<div class="caption-grid">')
    
    caption_type_names = {
        "subject": "Subject",
        "scene": "Scene",
        "motion": "Motion",
        "spatial": "Spatial",
        "camera": "Camera"
    }
    
    for caption_type in ["subject", "scene", "motion", "spatial", "camera"]:
        if caption_type not in captions:
            continue
        
        caption_info = captions[caption_type]
        status = caption_info.get("status", "unknown")
        caption_data = caption_info.get("caption_data", {})
        
        # Skip if not completed
        if status == "not_completed":
            continue
        
        html_parts.append(f'<div class="caption-card {status}">')
        html_parts.append(f'<h3>{caption_type_names.get(caption_type, caption_type.title())}</h3>')
        
        # Status badge
        status_emoji = "✅" if status == "approved" else "🔄" if status == "rejected" else "❓"
        html_parts.append(f'<div class="status-badge {status}">{status_emoji} {status.replace("_", " ").title()}</div>')
        
        # Pre-caption with score
        pre_caption = caption_data.get("pre_caption", "")
        pre_caption_score = caption_data.get("initial_caption_rating_score", "N/A")
        if pre_caption:
            html_parts.append('<div class="caption-field">')
            html_parts.append(f'<strong>Pre-Caption (Score: {pre_caption_score}/5):</strong>')
            html_parts.append(f'<p>{html.escape(pre_caption)}</p>')
            html_parts.append('</div>')
        
        # Initial human feedback (initial_feedback - raw user feedback)
        initial_feedback = caption_data.get("initial_feedback", "")
        if initial_feedback:
            html_parts.append('<div class="caption-field">')
            html_parts.append('<strong>Initial Human Feedback:</strong>')
            html_parts.append(f'<p>{html.escape(initial_feedback)}</p>')
            html_parts.append('</div>')
        
        # Final feedback (final_feedback - polished/final version)
        final_feedback = caption_data.get("final_feedback", "")
        if final_feedback:
            html_parts.append('<div class="caption-field">')
            html_parts.append('<strong>Final Feedback:</strong>')
            html_parts.append(f'<p>{html.escape(final_feedback)}</p>')
            html_parts.append('</div>')
        
        # Final caption
        final_caption = caption_data.get("final_caption", "")
        if final_caption:
            html_parts.append('<div class="caption-field">')
            html_parts.append('<strong>Final Caption:</strong>')
            html_parts.append(f'<p class="final-caption">{html.escape(final_caption)}</p>')
            html_parts.append('</div>')
        
        # User info
        annotator = caption_data.get("user", "Unknown")
        reviewer = caption_data.get("reviewer", "Not reviewed")
        
        html_parts.append('<div class="user-info">')
        html_parts.append(f'<span class="annotator">👤 Annotator: {html.escape(annotator)}</span>')
        if reviewer and reviewer != "Not reviewed":
            html_parts.append(f'<span class="reviewer">🔍 Reviewer: {html.escape(reviewer)}</span>')
        html_parts.append('</div>')
        
        html_parts.append('</div>')  # Close caption-card
    
    html_parts.append('</div>')  # Close caption-grid
    html_parts.append('</div>')  # Close video-section
    
    return '\n'.join(html_parts)


def generate_incomplete_video_html(video_data: Dict[str, Any], status_summary: Dict[str, str]) -> str:
    """Generate HTML for an incomplete video showing status."""
    video_id = video_data.get("video_id", "unknown")
    
    html_parts = []
    
    html_parts.append(f'<div class="video-section incomplete" id="{html.escape(video_id)}">')
    html_parts.append(f'<h2 class="video-title">{html.escape(video_id)} <span class="incomplete-badge">⏳ In Progress</span></h2>')
    
    html_parts.append('<div class="status-grid">')
    
    caption_type_names = {
        "subject": "Subject",
        "scene": "Scene",
        "motion": "Motion",
        "spatial": "Spatial",
        "camera": "Camera"
    }
    
    for caption_type in ["subject", "scene", "motion", "spatial", "camera"]:
        status = status_summary.get(caption_type, "not_started")
        
        status_display = {
            "approved": "✅ Approved",
            "rejected": "🔄 Rejected",
            "completed_not_reviewed": "⏳ Pending Review",
            "not_completed": "⬜ Not Completed",
            "not_started": "⬜ Not Started"
        }
        
        status_text = status_display.get(status, status)
        
        html_parts.append(f'<div class="status-item {status}">')
        html_parts.append(f'<strong>{caption_type_names.get(caption_type, caption_type.title())}:</strong>')
        html_parts.append(f'<span class="status-text">{status_text}</span>')
        html_parts.append('</div>')
    
    html_parts.append('</div>')
    html_parts.append('</div>')
    
    return '\n'.join(html_parts)


def generate_html(export_file: Path, output_file: Path, adobe_excel_files: Optional[List[str]] = None):
    """Generate the complete static HTML website."""
    
    # Hardcoded list of video filenames to include
    INCLUDED_VIDEOS = {
        "4PcpGxihPac.3.0.mp4", "O6_XM2Mn0lg.1.mp4", "47f4df7877163fa635cf93fa75853a526b9f738b9c08d43f0126b81b721045d7.0.mp4", "OCBYMQzG44U.2.7.mp4", "uWCGK4nneeU.2.3.mp4", "upC8hjr2b4g.0.0.mp4", "xhrAGJviQJA.0.7.mp4", "IyTv_SR2uUo.2.7.mp4", "kjI2gyb2hR4.0.1.mp4", "1934.1.25.mp4", "h1PjJ9_Yd2c.2.15.mp4", "X-keHLL75tg.3.6.mp4", "3esyihbPQm8.0.3.mp4", "cff54db6382ec81eaef2351f5319978651cec439bf358c937295d87986ab89b6.0.mp4", "TktL3QR8Yg8.0.9.mp4", "d31dc92ece2e873871190ee256e08745b036fb7c5d3b491aa355106a54e23318.2.mp4", "hk3sjN_k3-g.0.5.mp4", "BNzc6hG3yN4.1.4.mp4", "TktL3QR8Yg8.0.10.mp4", "1470.0.7.mp4", "mixkit-beautiful-dusk-on-a-large-lake-from-above-5005.0.mp4",
        "piQsdrDKzzM.2.3.mp4", "mIiPt1YVkP8.9.7.mp4", "e_ofen9SDeM.0.2.mp4", "bPZc7avrCT4.5.5.mp4", "nb69sgB5mG0.2.2.mp4", "cd248d6e8326130876d9f820943ac094463a938ba557ccff8171d483dbe01d14.0.mp4", "fSWFUFdV5TU.5.0.mp4", "kxcw0iSn0xw.1.2.mp4", "5qKYrajRNwo.3.3.mp4", "kxcw0iSn0xw.3.2.mp4", "LNHBMFCzznE.0.4.mp4", "iXzposKQzvs.2.8.mp4", "bX8GaZ3O4-Q.3.2.mp4", "pNGMY3xVkVE.0.1.mp4",
        "bX8GaZ3O4-Q.3.2.mp4", "iXzposKQzvs.2.8.mp4",
        "fSWFUFdV5TU.5.0.mp4", "fSWFUFdV5TU.5.0.mp4",
        "60.0.32.mp4", "IWv0EhEGmNI.3.3.mp4", "f4ZzHtww6Tc.5.0.mp4", "OCBYMQzG44U.2.10.mp4",
        "fT6olrwrjnI.0.0.mp4", "rs4B8-qoY1I.2.1.mp4", "K3U7Ybik1wM.1.6.mp4", "OCBYMQzG44U.21.4.mp4",
        "qMeHR2Dc4mQ.3.6.mp4", "GdRJCTR1KDQ.0.0.mp4", "MPX29k4uwSg.0.1.mp4",
        "67bfa4eec893c10cba8c4fb180735bf8adc0c7de5a0cfe1ee9d1c1b44c2e56c8.0.mp4",
        "3923c396290520b6dcedf49397a06682322bd225007879cdd4fa2b144116c293.0.mp4",
        "iXzposKQzvs.2.1.mp4", "B_8bbKn3amE.0.13.mp4", "TP_0Vv5F29I.0.0.mp4", "KdfhMulBsyk.5.3.mp4",
        "MPX29k4uwSg.2.3.mp4", "2KuVjf4uB9k.0.17.mp4", "kxcw0iSn0xw.2.2.mp4", "H4AZhS5WqKk.2.19.mp4",
        "DEypDAnnJL0.6.3.mp4", "TktL3QR8Yg8.0.4.mp4", "OCBYMQzG44U.30.3.mp4", "zk-eY5S1Nck.0.5.mp4",
        "x6P57x1gx94.0.7.mp4", "88vmzn_LufA.2.3.mp4", "-2uIa-XMJC0.6.10.mp4", "uWCGK4nneeU.0.7.mp4",
        "YBC2JaevzOI.6.4.mp4", "xo9p8p6deRI.6.2.mp4", "6YDWsGwz2lI.0.11.mp4", "VaSlqE0Nx2Q.12.4.mp4",
        "lz5xvWTodyw.2.0.mp4", "88vmzn_LufA.0.1.mp4", "H4AZhS5WqKk.0.16.mp4", "QaRnEZFM6ZQ.1.3.mp4",
        "VaSlqE0Nx2Q.4.0.mp4", "0UthxdAH0ks.3.1.mp4", "h1PjJ9_Yd2c.2.11.mp4",
        "016570694b24f7fefbc284e65d330e11e053542bd6ae8c24194ac0823b82c1eb.1.mp4",
        "hCr1JvdvBqs.1.9.mp4", "H4AZhS5WqKk.2.11.mp4", "338.2.14.mp4", "QHcK3oJGtCY.0.0.mp4"
    }
    
    # Load export data
    print(f"Loading export data from {export_file}...")
    with open(export_file, 'r') as f:
        all_video_data = json.load(f)
    
    # Filter to only include videos in the hardcoded list
    video_data_list = []
    for video_data in all_video_data:
        video_filename = get_video_filename(video_data.get("video_url", ""))
        if video_filename in INCLUDED_VIDEOS:
            video_data_list.append(video_data)
    
    print(f"Filtered to {len(video_data_list)} videos from the included list (out of {len(all_video_data)} total)")
    
    # Debug: Show which videos from the list were not found
    found_filenames = {get_video_filename(v.get("video_url", "")) for v in video_data_list}
    missing_filenames = INCLUDED_VIDEOS - found_filenames
    if missing_filenames:
        print(f"\nWarning: {len(missing_filenames)} videos from the included list were not found in export:")
        for filename in sorted(missing_filenames):
            print(f"  - {filename}")
    
    # Load Adobe captions if provided
    adobe_captions = {}
    if adobe_excel_files:
        adobe_captions = load_adobe_captions(adobe_excel_files)
    
    # Required caption types
    required_types = ["subject", "scene", "motion", "spatial", "camera"]
    
    # Separate fully completed and partially completed videos
    fully_completed_videos = []
    partially_completed_videos = []
    not_started_videos = []
    
    for video_data in video_data_list:
        captions = video_data.get("captions", {})
        if is_video_completed(captions, required_types):
            # All 5 captions are completed
            fully_completed_videos.append(video_data)
        elif has_any_completed_caption(captions, required_types):
            # At least one caption is completed
            status_summary = get_caption_status_summary(captions, required_types)
            partially_completed_videos.append((video_data, status_summary))
        else:
            # No captions completed yet
            status_summary = get_caption_status_summary(captions, required_types)
            not_started_videos.append((video_data, status_summary))
    
    print(f"\nProcessing {len(video_data_list)} videos from the included list:")
    print(f"  - {len(fully_completed_videos)} fully completed (all 5 captions)")
    print(f"  - {len(partially_completed_videos)} partially completed (1-4 captions)")
    print(f"  - {len(not_started_videos)} not started")
    
    # Combine all videos to display (we want to show everything from the hardcoded list)
    completed_videos = fully_completed_videos
    incomplete_videos = partially_completed_videos + not_started_videos
    
    # Generate HTML
    html_content = []
    
    # HTML header
    html_content.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Caption Annotations</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .summary {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 30px;
        }
        
        .summary-stats {
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
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
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
            transition: background 0.3s;
        }
        
        .navigation a:hover {
            background: rgba(52, 152, 219, 0.1);
        }
        
        .section-header {
            background: #3498db;
            color: white;
            padding: 15px 20px;
            border-radius: 6px;
            margin: 30px 0 20px 0;
            font-size: 1.5em;
        }
        
        .video-section {
            margin-bottom: 40px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 25px;
            background: #fafafa;
        }
        
        .video-section.incomplete {
            background: #f9f9f9;
            border-color: #ddd;
        }
        
        .video-title {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
            font-size: 1.8em;
        }
        
        .incomplete-badge {
            background: #f39c12;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.6em;
            margin-left: 10px;
        }
        
        .video-container {
            margin-bottom: 25px;
            background: white;
            padding: 15px;
            border-radius: 8px;
        }
        
        video {
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .download-link {
            margin-top: 10px;
            text-align: right;
        }
        
        .download-link a {
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }
        
        .download-link a:hover {
            text-decoration: underline;
        }
        
        .crowd-captions {
            background: #e8f4f8;
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }
        
        .crowd-captions h3 {
            color: #2980b9;
            margin-bottom: 15px;
        }
        
        .crowd-caption-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .crowd-caption-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
        }
        
        .crowd-caption-item strong {
            color: #2980b9;
            display: block;
            margin-bottom: 8px;
        }
        
        .caption-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .caption-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }
        
        .caption-card.approved {
            border-left-color: #27ae60;
        }
        
        .caption-card.rejected {
            border-left-color: #e74c3c;
        }
        
        .caption-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .status-badge.approved {
            background: #27ae60;
            color: white;
        }
        
        .status-badge.rejected {
            background: #e74c3c;
            color: white;
        }
        
        .status-badge.completed_not_reviewed {
            background: #f39c12;
            color: white;
        }
        
        .caption-field {
            margin-bottom: 15px;
        }
        
        .caption-field strong {
            display: block;
            color: #34495e;
            margin-bottom: 5px;
            font-size: 0.9em;
        }
        
        .caption-field p {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            border-left: 3px solid #3498db;
            margin: 0;
        }
        
        .final-caption {
            background: #e8f5e9 !important;
            border-left-color: #27ae60 !important;
            font-weight: 500;
        }
        
        .user-info {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.9em;
        }
        
        .annotator, .reviewer {
            background: #ecf0f1;
            padding: 5px 12px;
            border-radius: 15px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .status-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #bdc3c7;
        }
        
        .status-item.approved {
            border-left-color: #27ae60;
        }
        
        .status-item.rejected {
            border-left-color: #e74c3c;
        }
        
        .status-item.completed_not_reviewed {
            border-left-color: #f39c12;
        }
        
        .status-text {
            color: #7f8c8d;
            font-size: 0.95em;
        }
        
        @media (max-width: 768px) {
            .caption-grid, .status-grid, .crowd-caption-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📹 Video Caption Annotations</h1>
''')
    
    # Summary section
    html_content.append('<div class="summary">')
    html_content.append('<h2>📊 Summary</h2>')
    html_content.append('<div class="summary-stats">')
    html_content.append(f'<div class="stat-item"><div class="stat-number">{len(video_data_list)}</div><div class="stat-label">Total Videos</div></div>')
    html_content.append(f'<div class="stat-item"><div class="stat-number">{len(completed_videos)}</div><div class="stat-label">Completed</div></div>')
    html_content.append(f'<div class="stat-item"><div class="stat-number">{len(incomplete_videos)}</div><div class="stat-label">In Progress</div></div>')
    
    if adobe_captions:
        overlap_count = sum(1 for v in completed_videos if get_video_filename(v.get("video_url", "")) in adobe_captions)
        html_content.append(f'<div class="stat-item"><div class="stat-number">{overlap_count}</div><div class="stat-label">With Crowd Captions</div></div>')
    
    html_content.append('</div>')
    html_content.append('</div>')
    
    # Navigation
    html_content.append('<div class="navigation">')
    html_content.append('<strong>Quick Navigation:</strong> ')
    html_content.append('<a href="#completed">Completed Videos</a> | ')
    html_content.append('<a href="#incomplete">In Progress Videos</a>')
    html_content.append('</div>')
    
    # Completed videos section
    if completed_videos:
        html_content.append('<div id="completed" class="section-header">✅ Completed Videos</div>')
        for video_data in completed_videos:
            html_content.append(generate_completed_video_html(video_data, adobe_captions))
    
    # Incomplete videos section
    if incomplete_videos:
        html_content.append('<div id="incomplete" class="section-header">⏳ Videos In Progress</div>')
        for video_data, status_summary in incomplete_videos:
            html_content.append(generate_incomplete_video_html(video_data, status_summary))
    
    # HTML footer
    html_content.append('''
    </div>
</body>
</html>
''')
    
    # Write to file
    print(f"\nWriting HTML to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))
    
    print(f"✅ Static HTML website generated successfully!")
    print(f"📁 Output file: {output_file}")
    print(f"\nYou can now open {output_file} in a web browser or share it with others.")


def main():
    parser = argparse.ArgumentParser(
        description="Extract static HTML website for video caption annotations"
    )
    
    parser.add_argument(
        "export_file",
        type=str,
        help="Path to exported JSON file (e.g., all_videos_with_captions_20251004_0625.json)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output HTML file (default: same directory as input with .html extension)"
    )
    
    parser.add_argument(
        "--adobe-excel-files",
        nargs="+",
        type=str,
        default=None,
        help="Adobe Excel files containing crowd captions (e.g., adobe_2_19.xlsx adobe_2_17.xlsx)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    export_file = Path(args.export_file)
    if not export_file.exists():
        print(f"Error: File not found: {export_file}")
        return 1
    
    # Validate Adobe Excel files if provided
    if args.adobe_excel_files:
        if not PANDAS_AVAILABLE:
            print("Error: pandas is required for reading Adobe Excel files.")
            print("Install with: pip install pandas openpyxl")
            return 1
        
        for excel_file in args.adobe_excel_files:
            if not Path(excel_file).exists():
                print(f"Error: Adobe Excel file not found: {excel_file}")
                return 1
    
    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = export_file.parent / f"{export_file.stem}.html"
    
    # Generate HTML
    generate_html(export_file, output_file, args.adobe_excel_files)
    
    return 0


if __name__ == "__main__":
    exit(main())