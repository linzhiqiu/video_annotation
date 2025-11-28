#!/usr/bin/env python3
"""
Newline Analysis Script - Analyze newline usage in critiques and captions

Analyzes the percentage of critiques and captions containing newline characters (\n)
for:
- Ground truth critiques (final_feedback)
- Generated negative critiques
- Final captions (final_caption)
- Revised captions (revised_caption_by_generated_critique)
- Worst captions (bad_caption)

Usage:
    python analyze_critique_newlines.py --export-folder caption_export/export_20251121_1332
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Analyze newline usage in critiques and captions")
    parser.add_argument("--export-folder", type=str, required=True,
                       help="Export folder containing the consolidated JSON file")
    parser.add_argument("--verbose", action="store_true", default=False,
                       help="Show detailed examples of critiques/captions with newlines")
    return parser.parse_args()


def find_consolidated_json(export_folder: Path) -> Path:
    """Find the all_videos_with_captions_and_critiques JSON file"""
    
    # Look for the consolidated file with critiques
    files = list(export_folder.glob("all_videos_with_captions_and_critiques_*.json"))
    
    if not files:
        raise FileNotFoundError(
            f"No consolidated critique file found in {export_folder}\n"
            f"Looking for: all_videos_with_captions_and_critiques_*.json\n"
            f"Make sure you've run the critique generation with --export-json flag"
        )
    
    if len(files) > 1:
        print(f"Warning: Multiple consolidated files found, using: {files[0].name}")
    
    return files[0]


def has_newline(text: str) -> bool:
    """Check if text contains newline character"""
    return '\n' in text if text else False


def analyze_newlines(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze newline usage across all critiques and captions"""
    
    # Define critique types to analyze (excluding worst_caption_generation for critiques)
    negative_critique_types = [
        "insertion_error_critique",
        "replacement_error_critique", 
        "deletion_error_critique",
        "nonconstructive_critique",
        "video_model_critique",
        "blind_model_critique"
    ]
    
    # Caption types to analyze
    caption_analysis_types = [
        "final_caption",  # The approved/rejected caption
    ] + [f"revised_{ct}" for ct in negative_critique_types] + ["worst_caption"]
    
    # Auto-detect caption types from actual data
    detected_caption_types = set()
    for video in data:
        captions = video.get("captions", {})
        for caption_type in captions.keys():
            detected_caption_types.add(caption_type)
    
    # Use detected types, fallback to default if none found
    if detected_caption_types:
        caption_types = sorted(list(detected_caption_types))
        print(f"  Detected caption types in data: {caption_types}")
    else:
        caption_types = [
            "subject",
            "scene", 
            "subject_motion",
            "spatial",
            "camera"
        ]
        print(f"  Using default caption types: {caption_types}")
    
    # Initialize tracking dictionaries
    results = {
        "overall": {},  # For critiques
        "by_caption_type": defaultdict(lambda: defaultdict(dict)),  # For critiques
        "caption_overall": {},  # For captions
        "caption_by_type": defaultdict(lambda: defaultdict(dict))  # For captions
    }
    
    # Track overall stats for each critique type
    for critique_type in ["final_feedback"] + negative_critique_types:
        results["overall"][critique_type] = {
            "total": 0,
            "with_newline": 0,
            "percentage": 0.0,
            "examples": []  # Store first few examples
        }
    
    # Track overall stats for each caption type
    for caption_analysis_type in caption_analysis_types:
        results["caption_overall"][caption_analysis_type] = {
            "total": 0,
            "with_newline": 0,
            "percentage": 0.0,
            "examples": []
        }
    
    # Process each video
    for video in data:
        video_id = video.get("video_id", "unknown")
        captions = video.get("captions", {})
        
        for caption_type in caption_types:
            if caption_type not in captions:
                continue
                
            caption_data = captions[caption_type]
            
            # Skip if not approved/rejected
            if caption_data.get("status") not in ["approved", "rejected"]:
                continue
            
            # === ANALYZE CRITIQUES ===
            
            # Analyze final_feedback (ground truth)
            final_feedback = caption_data.get("caption_data", {}).get("final_feedback", "")
            
            # Overall final_feedback stats
            results["overall"]["final_feedback"]["total"] += 1
            has_nl = has_newline(final_feedback)
            if has_nl:
                results["overall"]["final_feedback"]["with_newline"] += 1
                if len(results["overall"]["final_feedback"]["examples"]) < 3:
                    results["overall"]["final_feedback"]["examples"].append({
                        "video_id": video_id,
                        "caption_type": caption_type,
                        "text": final_feedback[:200]  # First 200 chars
                    })
            
            # By caption type for final_feedback
            if caption_type not in results["by_caption_type"]["final_feedback"]:
                results["by_caption_type"]["final_feedback"][caption_type] = {
                    "total": 0,
                    "with_newline": 0,
                    "percentage": 0.0
                }
            
            results["by_caption_type"]["final_feedback"][caption_type]["total"] += 1
            if has_nl:
                results["by_caption_type"]["final_feedback"][caption_type]["with_newline"] += 1
            
            # Analyze generated critiques
            for critique_type in negative_critique_types:
                if critique_type not in caption_data:
                    continue
                    
                critique_info = caption_data[critique_type]
                
                # Skip if not successfully generated
                if critique_info.get("status") != "success":
                    continue
                
                # Get the critique text
                critique_text = critique_info.get("generated_critique", "")
                
                # Overall stats
                results["overall"][critique_type]["total"] += 1
                has_nl = has_newline(critique_text)
                if has_nl:
                    results["overall"][critique_type]["with_newline"] += 1
                    if len(results["overall"][critique_type]["examples"]) < 3:
                        results["overall"][critique_type]["examples"].append({
                            "video_id": video_id,
                            "caption_type": caption_type,
                            "text": critique_text[:200]
                        })
                
                # By caption type
                if caption_type not in results["by_caption_type"][critique_type]:
                    results["by_caption_type"][critique_type][caption_type] = {
                        "total": 0,
                        "with_newline": 0,
                        "percentage": 0.0
                    }
                
                results["by_caption_type"][critique_type][caption_type]["total"] += 1
                if has_nl:
                    results["by_caption_type"][critique_type][caption_type]["with_newline"] += 1
            
            # === ANALYZE CAPTIONS ===
            
            # Analyze final_caption
            final_caption = caption_data.get("caption_data", {}).get("final_caption", "")
            
            results["caption_overall"]["final_caption"]["total"] += 1
            has_nl = has_newline(final_caption)
            if has_nl:
                results["caption_overall"]["final_caption"]["with_newline"] += 1
                if len(results["caption_overall"]["final_caption"]["examples"]) < 3:
                    results["caption_overall"]["final_caption"]["examples"].append({
                        "video_id": video_id,
                        "caption_type": caption_type,
                        "text": final_caption[:200]
                    })
            
            # By caption type for final_caption
            if caption_type not in results["caption_by_type"]["final_caption"]:
                results["caption_by_type"]["final_caption"][caption_type] = {
                    "total": 0,
                    "with_newline": 0,
                    "percentage": 0.0
                }
            
            results["caption_by_type"]["final_caption"][caption_type]["total"] += 1
            if has_nl:
                results["caption_by_type"]["final_caption"][caption_type]["with_newline"] += 1
            
            # Analyze revised captions from each critique type
            for critique_type in negative_critique_types:
                if critique_type not in caption_data:
                    continue
                    
                critique_info = caption_data[critique_type]
                
                if critique_info.get("status") != "success":
                    continue
                
                revised_caption = critique_info.get("revised_caption_by_generated_critique", "")
                revised_key = f"revised_{critique_type}"
                
                # Overall stats
                results["caption_overall"][revised_key]["total"] += 1
                has_nl = has_newline(revised_caption)
                if has_nl:
                    results["caption_overall"][revised_key]["with_newline"] += 1
                    if len(results["caption_overall"][revised_key]["examples"]) < 3:
                        results["caption_overall"][revised_key]["examples"].append({
                            "video_id": video_id,
                            "caption_type": caption_type,
                            "text": revised_caption[:200]
                        })
                
                # By caption type
                if caption_type not in results["caption_by_type"][revised_key]:
                    results["caption_by_type"][revised_key][caption_type] = {
                        "total": 0,
                        "with_newline": 0,
                        "percentage": 0.0
                    }
                
                results["caption_by_type"][revised_key][caption_type]["total"] += 1
                if has_nl:
                    results["caption_by_type"][revised_key][caption_type]["with_newline"] += 1
            
            # Analyze worst_caption_generation
            if "worst_caption_generation" in caption_data:
                worst_info = caption_data["worst_caption_generation"]
                
                if worst_info.get("status") == "success":
                    worst_caption = worst_info.get("bad_caption", "")
                    
                    # Overall stats
                    results["caption_overall"]["worst_caption"]["total"] += 1
                    has_nl = has_newline(worst_caption)
                    if has_nl:
                        results["caption_overall"]["worst_caption"]["with_newline"] += 1
                        if len(results["caption_overall"]["worst_caption"]["examples"]) < 3:
                            results["caption_overall"]["worst_caption"]["examples"].append({
                                "video_id": video_id,
                                "caption_type": caption_type,
                                "text": worst_caption[:200]
                            })
                    
                    # By caption type
                    if caption_type not in results["caption_by_type"]["worst_caption"]:
                        results["caption_by_type"]["worst_caption"][caption_type] = {
                            "total": 0,
                            "with_newline": 0,
                            "percentage": 0.0
                        }
                    
                    results["caption_by_type"]["worst_caption"][caption_type]["total"] += 1
                    if has_nl:
                        results["caption_by_type"]["worst_caption"][caption_type]["with_newline"] += 1
    
    # Calculate percentages for critiques
    for critique_type in results["overall"]:
        total = results["overall"][critique_type]["total"]
        if total > 0:
            with_nl = results["overall"][critique_type]["with_newline"]
            results["overall"][critique_type]["percentage"] = (with_nl / total) * 100
    
    for critique_type in results["by_caption_type"]:
        for caption_type in results["by_caption_type"][critique_type]:
            total = results["by_caption_type"][critique_type][caption_type]["total"]
            if total > 0:
                with_nl = results["by_caption_type"][critique_type][caption_type]["with_newline"]
                results["by_caption_type"][critique_type][caption_type]["percentage"] = (with_nl / total) * 100
    
    # Calculate percentages for captions
    for caption_analysis_type in results["caption_overall"]:
        total = results["caption_overall"][caption_analysis_type]["total"]
        if total > 0:
            with_nl = results["caption_overall"][caption_analysis_type]["with_newline"]
            results["caption_overall"][caption_analysis_type]["percentage"] = (with_nl / total) * 100
    
    for caption_analysis_type in results["caption_by_type"]:
        for caption_type in results["caption_by_type"][caption_analysis_type]:
            total = results["caption_by_type"][caption_analysis_type][caption_type]["total"]
            if total > 0:
                with_nl = results["caption_by_type"][caption_analysis_type][caption_type]["with_newline"]
                results["caption_by_type"][caption_analysis_type][caption_type]["percentage"] = (with_nl / total) * 100
    
    # Store source data for example extraction in markdown export
    results["_source_data"] = data
    
    return results


def print_results(results: Dict[str, Any], verbose: bool = False):
    """Print analysis results in a readable format"""
    
    print("=" * 80)
    print("NEWLINE ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    # Define header variable to avoid backslash in f-string
    newline_col = "With \\n"
    
    # Overall statistics - CRITIQUES
    print("CRITIQUE STATISTICS (final_feedback and generated critiques)")
    print("-" * 80)
    print(f"{'Critique Type':<35} {'Total':<10} {newline_col:<10} {'Percentage':<10}")
    print("-" * 80)
    
    for critique_type in sorted(results["overall"].keys()):
        stats = results["overall"][critique_type]
        print(f"{critique_type:<35} {stats['total']:<10} {stats['with_newline']:<10} {stats['percentage']:<10.2f}%")
    
    print()
    print()
    
    # Overall statistics - CAPTIONS
    print("CAPTION STATISTICS (final_caption and revised captions)")
    print("-" * 80)
    print(f"{'Caption Type':<35} {'Total':<10} {newline_col:<10} {'Percentage':<10}")
    print("-" * 80)
    
    for caption_type in sorted(results["caption_overall"].keys()):
        stats = results["caption_overall"][caption_type]
        print(f"{caption_type:<35} {stats['total']:<10} {stats['with_newline']:<10} {stats['percentage']:<10.2f}%")
    
    print()
    print()
    
    # By caption type breakdown - CRITIQUES
    print("CRITIQUE BREAKDOWN BY CAPTION TYPE")
    print("=" * 80)
    
    # Get all caption types that appear in the data
    all_caption_types = set()
    for critique_data in results["by_caption_type"].values():
        all_caption_types.update(critique_data.keys())
    all_caption_types = sorted(all_caption_types)
    
    for critique_type in sorted(results["by_caption_type"].keys()):
        print()
        print(f"{critique_type.upper()}")
        print("-" * 80)
        print(f"{'Caption Type':<20} {'Total':<10} {newline_col:<10} {'Percentage':<10}")
        print("-" * 80)
        
        for caption_type in all_caption_types:
            if caption_type in results["by_caption_type"][critique_type]:
                stats = results["by_caption_type"][critique_type][caption_type]
                print(f"{caption_type:<20} {stats['total']:<10} {stats['with_newline']:<10} {stats['percentage']:<10.2f}%")
            else:
                print(f"{caption_type:<20} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
    
    print()
    print()
    
    # By caption type breakdown - CAPTIONS
    print("CAPTION BREAKDOWN BY CAPTION TYPE")
    print("=" * 80)
    
    for revised_type in sorted(results["caption_by_type"].keys()):
        print()
        print(f"{revised_type.upper()}")
        print("-" * 80)
        print(f"{'Caption Type':<20} {'Total':<10} {newline_col:<10} {'Percentage':<10}")
        print("-" * 80)
        
        for caption_type in all_caption_types:
            if caption_type in results["caption_by_type"][revised_type]:
                stats = results["caption_by_type"][revised_type][caption_type]
                print(f"{caption_type:<20} {stats['total']:<10} {stats['with_newline']:<10} {stats['percentage']:<10.2f}%")
            else:
                print(f"{caption_type:<20} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
    
    # Examples if verbose
    if verbose:
        print()
        print()
        print("EXAMPLES OF CRITIQUES WITH NEWLINES")
        print("=" * 80)
        
        for critique_type in sorted(results["overall"].keys()):
            examples = results["overall"][critique_type]["examples"]
            if examples:
                print()
                print(f"{critique_type.upper()}")
                print("-" * 80)
                for i, example in enumerate(examples, 1):
                    print(f"\nExample {i}:")
                    print(f"  Video: {example['video_id']}")
                    print(f"  Caption Type: {example['caption_type']}")
                    print(f"  Text Preview: {repr(example['text'])}")
        
        print()
        print()
        print("EXAMPLES OF CAPTIONS WITH NEWLINES")
        print("=" * 80)
        
        for caption_type in sorted(results["caption_overall"].keys()):
            examples = results["caption_overall"][caption_type]["examples"]
            if examples:
                print()
                print(f"{caption_type.upper()}")
                print("-" * 80)
                for i, example in enumerate(examples, 1):
                    print(f"\nExample {i}:")
                    print(f"  Video: {example['video_id']}")
                    print(f"  Caption Type: {example['caption_type']}")
                    print(f"  Text Preview: {repr(example['text'])}")
    
    print()
    print("=" * 80)


def export_csv(results: Dict[str, Any], output_path: Path):
    """Export results to CSV for further analysis"""
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            "Data Type",
            "Specific Type",
            "Caption Type", 
            "Total Count",
            "With Newline",
            "Percentage"
        ])
        
        # Write critique overall stats (caption_type = "ALL")
        for critique_type in sorted(results["overall"].keys()):
            stats = results["overall"][critique_type]
            writer.writerow([
                "CRITIQUE",
                critique_type,
                "ALL",
                stats["total"],
                stats["with_newline"],
                f"{stats['percentage']:.2f}"
            ])
        
        # Write caption overall stats (caption_type = "ALL")
        for caption_analysis_type in sorted(results["caption_overall"].keys()):
            stats = results["caption_overall"][caption_analysis_type]
            writer.writerow([
                "CAPTION",
                caption_analysis_type,
                "ALL",
                stats["total"],
                stats["with_newline"],
                f"{stats['percentage']:.2f}"
            ])
        
        # Write critique by caption type
        for critique_type in sorted(results["by_caption_type"].keys()):
            for caption_type in sorted(results["by_caption_type"][critique_type].keys()):
                stats = results["by_caption_type"][critique_type][caption_type]
                writer.writerow([
                    "CRITIQUE",
                    critique_type,
                    caption_type,
                    stats["total"],
                    stats["with_newline"],
                    f"{stats['percentage']:.2f}"
                ])
        
        # Write caption by caption type
        for caption_analysis_type in sorted(results["caption_by_type"].keys()):
            for caption_type in sorted(results["caption_by_type"][caption_analysis_type].keys()):
                stats = results["caption_by_type"][caption_analysis_type][caption_type]
                writer.writerow([
                    "CAPTION",
                    caption_analysis_type,
                    caption_type,
                    stats["total"],
                    stats["with_newline"],
                    f"{stats['percentage']:.2f}"
                ])


def export_markdown(results: Dict[str, Any], output_path: Path):
    """Export results to beautifully formatted Markdown"""
    
    # Get all caption types that appear in the data
    all_caption_types = set()
    for critique_data in results["by_caption_type"].values():
        all_caption_types.update(critique_data.keys())
    all_caption_types = sorted(all_caption_types)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Newline Character Analysis Report\n\n")
        f.write("Analysis of `\\n` (newline) character usage in critiques and captions.\n\n")
        f.write("---\n\n")
        
        # Executive Summary
        f.write("## 📊 Executive Summary\n\n")
        
        # Calculate overall stats
        total_critiques = sum(stats["total"] for stats in results["overall"].values())
        critiques_with_nl = sum(stats["with_newline"] for stats in results["overall"].values())
        critique_pct = (critiques_with_nl / total_critiques * 100) if total_critiques > 0 else 0
        
        total_captions = sum(stats["total"] for stats in results["caption_overall"].values())
        captions_with_nl = sum(stats["with_newline"] for stats in results["caption_overall"].values())
        caption_pct = (captions_with_nl / total_captions * 100) if total_captions > 0 else 0
        
        f.write(f"- **Total Critiques Analyzed**: {total_critiques:,}\n")
        f.write(f"- **Critiques with Newlines**: {critiques_with_nl:,} ({critique_pct:.1f}%)\n")
        f.write(f"- **Total Captions Analyzed**: {total_captions:,}\n")
        f.write(f"- **Captions with Newlines**: {captions_with_nl:,} ({caption_pct:.1f}%)\n\n")
        
        f.write("---\n\n")
        
        # Overall Critique Statistics
        f.write("## 💬 Critique Statistics\n\n")
        f.write("Percentage of critiques containing newline characters.\n\n")
        
        f.write("| Critique Type | Total | With `\\n` | Percentage |\n")
        f.write("|---------------|------:|----------:|-----------:|\n")
        
        for critique_type in sorted(results["overall"].keys()):
            stats = results["overall"][critique_type]
            # Add visual indicator
            if stats["percentage"] > 50:
                indicator = "🔴"
            elif stats["percentage"] > 20:
                indicator = "🟡"
            elif stats["percentage"] > 0:
                indicator = "🟢"
            else:
                indicator = "✅"
            
            f.write(f"| {indicator} {critique_type} | {stats['total']:,} | {stats['with_newline']:,} | **{stats['percentage']:.1f}%** |\n")
        
        f.write("\n---\n\n")
        
        # Overall Caption Statistics
        f.write("## 📝 Caption Statistics\n\n")
        f.write("Percentage of captions containing newline characters.\n\n")
        
        f.write("| Caption Type | Total | With `\\n` | Percentage |\n")
        f.write("|--------------|------:|----------:|-----------:|\n")
        
        for caption_type in sorted(results["caption_overall"].keys()):
            stats = results["caption_overall"][caption_type]
            # Add visual indicator
            if stats["percentage"] > 50:
                indicator = "🔴"
            elif stats["percentage"] > 20:
                indicator = "🟡"
            elif stats["percentage"] > 0:
                indicator = "🟢"
            else:
                indicator = "✅"
            
            f.write(f"| {indicator} {caption_type} | {stats['total']:,} | {stats['with_newline']:,} | **{stats['percentage']:.1f}%** |\n")
        
        f.write("\n---\n\n")
        
        # Breakdown by Caption Type - Critiques
        f.write("## 🔍 Detailed Breakdown: Critiques by Caption Type\n\n")
        
        for critique_type in sorted(results["by_caption_type"].keys()):
            f.write(f"### {critique_type}\n\n")
            
            f.write("| Caption Type | Total | With `\\n` | Percentage |\n")
            f.write("|--------------|------:|----------:|-----------:|\n")
            
            for caption_type in all_caption_types:
                if caption_type in results["by_caption_type"][critique_type]:
                    stats = results["by_caption_type"][critique_type][caption_type]
                    
                    if stats["percentage"] > 50:
                        indicator = "🔴"
                    elif stats["percentage"] > 20:
                        indicator = "🟡"
                    elif stats["percentage"] > 0:
                        indicator = "🟢"
                    else:
                        indicator = "✅"
                    
                    f.write(f"| {indicator} {caption_type} | {stats['total']:,} | {stats['with_newline']:,} | {stats['percentage']:.1f}% |\n")
                else:
                    f.write(f"| ⚪ {caption_type} | N/A | N/A | N/A |\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        
        # Breakdown by Caption Type - Captions
        f.write("## 🔍 Detailed Breakdown: Captions by Caption Type\n\n")
        
        for revised_type in sorted(results["caption_by_type"].keys()):
            f.write(f"### {revised_type}\n\n")
            
            f.write("| Caption Type | Total | With `\\n` | Percentage |\n")
            f.write("|--------------|------:|----------:|-----------:|\n")
            
            for caption_type in all_caption_types:
                if caption_type in results["caption_by_type"][revised_type]:
                    stats = results["caption_by_type"][revised_type][caption_type]
                    
                    if stats["percentage"] > 50:
                        indicator = "🔴"
                    elif stats["percentage"] > 20:
                        indicator = "🟡"
                    elif stats["percentage"] > 0:
                        indicator = "🟢"
                    else:
                        indicator = "✅"
                    
                    f.write(f"| {indicator} {caption_type} | {stats['total']:,} | {stats['with_newline']:,} | {stats['percentage']:.1f}% |\n")
                else:
                    f.write(f"| ⚪ {caption_type} | N/A | N/A | N/A |\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        
        # Legend
        f.write("## 📖 Legend\n\n")
        f.write("- ✅ **0%** - No newlines found (clean)\n")
        f.write("- 🟢 **0-20%** - Low newline usage\n")
        f.write("- 🟡 **20-50%** - Moderate newline usage\n")
        f.write("- 🔴 **>50%** - High newline usage\n")
        f.write("- ⚪ **N/A** - No data available\n\n")
        
        # Notes
        f.write("---\n\n")
        f.write("## 📌 Notes\n\n")
        f.write("- **Critique Types**: Includes `final_feedback` (ground truth) and all generated negative critiques\n")
        f.write("- **Caption Types**: Includes `final_caption` (approved/rejected), revised captions, and worst captions\n")
        f.write("- **Caption Categories**: " + ", ".join(all_caption_types) + "\n")
        f.write("- Newline character is represented as `\\n`\n\n")
        
        # Examples Section
        f.write("---\n\n")
        f.write("## 📋 Examples of Content\n\n")
        f.write("Below are examples organized by type and caption category, showing both content WITH and WITHOUT newlines.\n\n")
        
        # Define newline removal strategies
        f.write("### 🔧 Newline Removal Strategies\n\n")
        f.write("We test three strategies for removing newline characters:\n\n")
        f.write("1. **Simple Strip**: `text.strip()` - Removes leading/trailing whitespace including newlines\n")
        f.write("2. **Replace with Space**: `text.replace('\\n', ' ')` - Replaces newlines with single space\n")
        f.write("3. **Smart Replace**: Replaces newlines with space, then collapses multiple spaces to one\n\n")
        f.write("```python\n")
        f.write("# Strategy 1: Simple Strip\n")
        f.write("cleaned = text.strip()\n\n")
        f.write("# Strategy 2: Replace with Space\n")
        f.write("cleaned = text.replace('\\n', ' ')\n\n")
        f.write("# Strategy 3: Smart Replace (RECOMMENDED)\n")
        f.write("import re\n")
        f.write("cleaned = text.replace('\\n', ' ')  # Replace newlines with space\n")
        f.write("cleaned = re.sub(r' +', ' ', cleaned)  # Collapse multiple spaces\n")
        f.write("cleaned = cleaned.strip()  # Remove leading/trailing whitespace\n")
        f.write("```\n\n")
        f.write("---\n\n")
        
        # Collect examples by critique type and caption type - BOTH with and without newlines
        examples_with_newline = {}
        examples_without_newline = {}
        
        for video in results.get("_source_data", []):
            video_id = video.get("video_id", "unknown")
            captions = video.get("captions", {})
            
            for caption_type in all_caption_types:
                if caption_type not in captions:
                    continue
                    
                caption_data = captions[caption_type]
                
                if caption_data.get("status") not in ["approved", "rejected"]:
                    continue
                
                # Check final_feedback
                final_feedback = caption_data.get("caption_data", {}).get("final_feedback", "")
                if final_feedback:
                    key = ("CRITIQUE", "final_feedback", caption_type)
                    
                    if has_newline(final_feedback):
                        if key not in examples_with_newline:
                            examples_with_newline[key] = []
                        if len(examples_with_newline[key]) < 3:
                            examples_with_newline[key].append({
                                "video_id": video_id,
                                "text": final_feedback
                            })
                    else:
                        if key not in examples_without_newline:
                            examples_without_newline[key] = []
                        if len(examples_without_newline[key]) < 3:
                            examples_without_newline[key].append({
                                "video_id": video_id,
                                "text": final_feedback
                            })
                
                # Check generated critiques
                for critique_type in ["insertion_error_critique", "replacement_error_critique", 
                                     "deletion_error_critique", "nonconstructive_critique",
                                     "video_model_critique", "blind_model_critique"]:
                    if critique_type not in caption_data:
                        continue
                    
                    critique_info = caption_data[critique_type]
                    if critique_info.get("status") != "success":
                        continue
                    
                    critique_text = critique_info.get("generated_critique", "")
                    if critique_text:
                        key = ("CRITIQUE", critique_type, caption_type)
                        
                        if has_newline(critique_text):
                            if key not in examples_with_newline:
                                examples_with_newline[key] = []
                            if len(examples_with_newline[key]) < 3:
                                examples_with_newline[key].append({
                                    "video_id": video_id,
                                    "text": critique_text
                                })
                        else:
                            if key not in examples_without_newline:
                                examples_without_newline[key] = []
                            if len(examples_without_newline[key]) < 3:
                                examples_without_newline[key].append({
                                    "video_id": video_id,
                                    "text": critique_text
                                })
                
                # Check final_caption
                final_caption = caption_data.get("caption_data", {}).get("final_caption", "")
                if final_caption:
                    key = ("CAPTION", "final_caption", caption_type)
                    
                    if has_newline(final_caption):
                        if key not in examples_with_newline:
                            examples_with_newline[key] = []
                        if len(examples_with_newline[key]) < 3:
                            examples_with_newline[key].append({
                                "video_id": video_id,
                                "text": final_caption
                            })
                    else:
                        if key not in examples_without_newline:
                            examples_without_newline[key] = []
                        if len(examples_without_newline[key]) < 3:
                            examples_without_newline[key].append({
                                "video_id": video_id,
                                "text": final_caption
                            })
                
                # Check revised captions
                for critique_type in ["insertion_error_critique", "replacement_error_critique",
                                     "deletion_error_critique", "nonconstructive_critique",
                                     "video_model_critique", "blind_model_critique"]:
                    if critique_type not in caption_data:
                        continue
                    
                    critique_info = caption_data[critique_type]
                    if critique_info.get("status") != "success":
                        continue
                    
                    revised_caption = critique_info.get("revised_caption_by_generated_critique", "")
                    if revised_caption:
                        key = ("CAPTION", f"revised_{critique_type}", caption_type)
                        
                        if has_newline(revised_caption):
                            if key not in examples_with_newline:
                                examples_with_newline[key] = []
                            if len(examples_with_newline[key]) < 3:
                                examples_with_newline[key].append({
                                    "video_id": video_id,
                                    "text": revised_caption
                                })
                        else:
                            if key not in examples_without_newline:
                                examples_without_newline[key] = []
                            if len(examples_without_newline[key]) < 3:
                                examples_without_newline[key].append({
                                    "video_id": video_id,
                                    "text": revised_caption
                                })
                
                # Check worst_caption
                if "worst_caption_generation" in caption_data:
                    worst_info = caption_data["worst_caption_generation"]
                    if worst_info.get("status") == "success":
                        worst_caption = worst_info.get("bad_caption", "")
                        if worst_caption:
                            key = ("CAPTION", "worst_caption", caption_type)
                            
                            if has_newline(worst_caption):
                                if key not in examples_with_newline:
                                    examples_with_newline[key] = []
                                if len(examples_with_newline[key]) < 3:
                                    examples_with_newline[key].append({
                                        "video_id": video_id,
                                        "text": worst_caption
                                    })
                            else:
                                if key not in examples_without_newline:
                                    examples_without_newline[key] = []
                                if len(examples_without_newline[key]) < 3:
                                    examples_without_newline[key].append({
                                        "video_id": video_id,
                                        "text": worst_caption
                                    })
        
        # Helper function for smart newline removal
        def clean_newlines(text):
            """Apply smart newline removal strategy"""
            import re
            cleaned = text.replace('\n', ' ')
            cleaned = re.sub(r' +', ' ', cleaned)
            cleaned = cleaned.strip()
            return cleaned
        
        # Write critique examples
        f.write("## 💬 Critique Examples\n\n")
        
        critique_types_all = sorted(set(k[1] for k in list(examples_with_newline.keys()) + list(examples_without_newline.keys()) if k[0] == "CRITIQUE"))
        
        for critique_type in critique_types_all:
            f.write(f"### {critique_type}\n\n")
            
            for caption_type in all_caption_types:
                key = ("CRITIQUE", critique_type, caption_type)
                
                has_with_examples = key in examples_with_newline and examples_with_newline[key]
                has_without_examples = key in examples_without_newline and examples_without_newline[key]
                
                if has_with_examples or has_without_examples:
                    f.write(f"#### {caption_type}\n\n")
                    
                    # Examples WITH newlines
                    if has_with_examples:
                        f.write("**✅ Examples WITH newlines (showing before/after removal):**\n\n")
                        
                        for i, example in enumerate(examples_with_newline[key], 1):
                            f.write(f"<details>\n")
                            f.write(f"<summary>Example {i} - Video: {example['video_id']}</summary>\n\n")
                            
                            f.write("**BEFORE (with newlines):**\n")
                            f.write("```\n")
                            f.write(example['text'])
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 1 - Simple Strip):**\n")
                            f.write("```\n")
                            f.write(example['text'].strip())
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 2 - Replace with Space):**\n")
                            f.write("```\n")
                            f.write(example['text'].replace('\n', ' '))
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 3 - Smart Replace - RECOMMENDED):**\n")
                            f.write("```\n")
                            f.write(clean_newlines(example['text']))
                            f.write("\n```\n\n")
                            
                            f.write(f"</details>\n\n")
                    
                    # Examples WITHOUT newlines
                    if has_without_examples:
                        f.write("**❌ Examples WITHOUT newlines (clean text):**\n\n")
                        
                        for i, example in enumerate(examples_without_newline[key], 1):
                            f.write(f"<details>\n")
                            f.write(f"<summary>Example {i} - Video: {example['video_id']}</summary>\n\n")
                            f.write("```\n")
                            f.write(example['text'])
                            f.write("\n```\n\n")
                            f.write(f"</details>\n\n")
                    
                    f.write("\n")
        
        # Write caption examples
        f.write("## 📝 Caption Examples\n\n")
        
        caption_types_all = sorted(set(k[1] for k in list(examples_with_newline.keys()) + list(examples_without_newline.keys()) if k[0] == "CAPTION"))
        
        for caption_analysis_type in caption_types_all:
            f.write(f"### {caption_analysis_type}\n\n")
            
            for caption_type in all_caption_types:
                key = ("CAPTION", caption_analysis_type, caption_type)
                
                has_with_examples = key in examples_with_newline and examples_with_newline[key]
                has_without_examples = key in examples_without_newline and examples_without_newline[key]
                
                if has_with_examples or has_without_examples:
                    f.write(f"#### {caption_type}\n\n")
                    
                    # Examples WITH newlines
                    if has_with_examples:
                        f.write("**✅ Examples WITH newlines (showing before/after removal):**\n\n")
                        
                        for i, example in enumerate(examples_with_newline[key], 1):
                            f.write(f"<details>\n")
                            f.write(f"<summary>Example {i} - Video: {example['video_id']}</summary>\n\n")
                            
                            f.write("**BEFORE (with newlines):**\n")
                            f.write("```\n")
                            f.write(example['text'])
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 1 - Simple Strip):**\n")
                            f.write("```\n")
                            f.write(example['text'].strip())
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 2 - Replace with Space):**\n")
                            f.write("```\n")
                            f.write(example['text'].replace('\n', ' '))
                            f.write("\n```\n\n")
                            
                            f.write("**AFTER (Strategy 3 - Smart Replace - RECOMMENDED):**\n")
                            f.write("```\n")
                            f.write(clean_newlines(example['text']))
                            f.write("\n```\n\n")
                            
                            f.write(f"</details>\n\n")
                    
                    # Examples WITHOUT newlines
                    if has_without_examples:
                        f.write("**❌ Examples WITHOUT newlines (clean text):**\n\n")
                        
                        for i, example in enumerate(examples_without_newline[key], 1):
                            f.write(f"<details>\n")
                            f.write(f"<summary>Example {i} - Video: {example['video_id']}</summary>\n\n")
                            f.write("```\n")
                            f.write(example['text'])
                            f.write("\n```\n\n")
                            f.write(f"</details>\n\n")
                    
                    f.write("\n")


def main():
    """Main entry point"""
    args = parse_args()
    
    try:
        # Find consolidated JSON file
        export_folder = Path(args.export_folder)
        if not export_folder.exists():
            print(f"Error: Export folder does not exist: {export_folder}")
            return 1
        
        consolidated_file = find_consolidated_json(export_folder)
        print(f"Loading data from: {consolidated_file}")
        print()
        
        # Load data
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} videos")
        print()
        
        # Analyze newlines
        results = analyze_newlines(data)
        
        # Print results
        print_results(results, verbose=args.verbose)
        
        # Export CSV
        csv_path = export_folder / "newline_analysis.csv"
        export_csv(results, csv_path)
        print(f"\nResults exported to CSV: {csv_path}")
        
        # Export Markdown
        md_path = export_folder / "newline_analysis.md"
        export_markdown(results, md_path)
        print(f"Results exported to Markdown: {md_path}")
        
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())