#!/usr/bin/env python3
"""
Check critique file status and counts
"""

import json
from pathlib import Path
from collections import defaultdict

def analyze_critique_files(critique_type: str, output_dir: str = "output_critiques"):
    """Analyze critique files for a specific critique type"""
    
    base_path = Path("caption") / output_dir / critique_type
    
    if not base_path.exists():
        print(f"Directory does not exist: {base_path}")
        return
    
    print(f"Analyzing critique files for: {critique_type}")
    print(f"Base path: {base_path}")
    print("=" * 80)
    
    # Count by status
    status_counts = defaultdict(int)
    caption_type_counts = defaultdict(lambda: defaultdict(int))
    
    total_files = 0
    corrupted_files = []
    
    # Scan all subdirectories (caption types)
    for caption_type_dir in base_path.iterdir():
        if not caption_type_dir.is_dir():
            continue
        
        caption_type_name = caption_type_dir.name
        
        # Count files in this caption type
        for critique_file in caption_type_dir.glob("*_critique.json"):
            total_files += 1
            
            try:
                with open(critique_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                status = data.get("status", "unknown")
                status_counts[status] += 1
                caption_type_counts[caption_type_name][status] += 1
                
            except Exception as e:
                corrupted_files.append((str(critique_file), str(e)))
                status_counts["corrupted"] += 1
                caption_type_counts[caption_type_name]["corrupted"] += 1
    
    # Print summary
    print(f"\nTotal Files Found: {total_files}")
    print(f"\nStatus Breakdown:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    print(f"\nBy Caption Type:")
    for caption_type, statuses in sorted(caption_type_counts.items()):
        print(f"  {caption_type}:")
        for status, count in sorted(statuses.items()):
            print(f"    {status}: {count}")
    
    if corrupted_files:
        print(f"\nCorrupted Files ({len(corrupted_files)}):")
        for filepath, error in corrupted_files[:10]:  # Show first 10
            print(f"  {filepath}: {error}")
        if len(corrupted_files) > 10:
            print(f"  ... and {len(corrupted_files) - 10} more")
    
    return {
        "total_files": total_files,
        "status_counts": dict(status_counts),
        "caption_type_counts": {k: dict(v) for k, v in caption_type_counts.items()}
    }


def compare_with_expected(critique_type: str, export_folder: str):
    """Compare actual files with expected based on export data"""
    
    export_path = Path(export_folder)
    
    # Load export data
    export_files = list(export_path.glob("all_videos_with_captions_*.json"))
    if not export_files:
        print(f"No export file found in {export_folder}")
        return
    
    with open(export_files[0], 'r', encoding='utf-8') as f:
        export_data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(export_data, dict):
        export_data = list(export_data.values())
    
    # Count expected critiques
    expected_total = 0
    expected_by_caption_type = defaultdict(int)
    perfect_scores_by_caption_type = defaultdict(int)
    
    # Get all unique caption types from export data
    all_caption_types = set()
    for video_data in export_data:
        all_caption_types.update(video_data.get("captions", {}).keys())
    
    print(f"\nCaption types found in export: {sorted(all_caption_types)}")
    
    for video_data in export_data:
        for caption_type in all_caption_types:
            if caption_type in video_data.get("captions", {}):
                caption_info = video_data["captions"][caption_type]
                if caption_info.get("status") in ["approved", "rejected"]:
                    expected_total += 1
                    expected_by_caption_type[caption_type] += 1
                    
                    # Check if perfect score
                    caption_data = caption_info.get("caption_data", {})
                    if caption_data.get("initial_caption_rating_score") == 5:
                        perfect_scores_by_caption_type[caption_type] += 1
    
    print(f"\n" + "=" * 80)
    print(f"Expected vs Actual Comparison:")
    print(f"=" * 80)
    print(f"\nExpected total operations: {expected_total}")
    print(f"Expected perfect scores (should be skipped for {critique_type}): ", end="")
    
    # Check if this critique type skips perfect scores
    from caption.generate_critiques import CRITIQUE_TASKS
    skip_perfect = CRITIQUE_TASKS[critique_type]["skip_perfect"]
    
    total_perfect = sum(perfect_scores_by_caption_type.values())
    print(f"{total_perfect} ({'YES - will skip' if skip_perfect else 'NO - will process'})")
    
    print(f"\nExpected by caption type:")
    for caption_type, count in sorted(expected_by_caption_type.items()):
        perfect = perfect_scores_by_caption_type[caption_type]
        print(f"  {caption_type}: {count} total, {perfect} perfect scores")
    
    # Analyze actual files
    actual_data = analyze_critique_files(critique_type)
    
    if actual_data:
        print(f"\n" + "=" * 80)
        print(f"Gap Analysis:")
        print(f"=" * 80)
        
        actual_total = actual_data["total_files"]
        gap = expected_total - actual_total
        
        print(f"Expected: {expected_total}")
        print(f"Actual:   {actual_total}")
        print(f"Missing:  {gap}")
        
        if skip_perfect:
            print(f"\nNote: {critique_type} skips perfect scores ({total_perfect} operations)")
            print(f"Effective expected (non-perfect): {expected_total - total_perfect}")
            print(f"Gap after accounting for skips: {expected_total - total_perfect - actual_total}")
        
        print(f"\nConclusion:")
        if gap == total_perfect and skip_perfect:
            print(f"✓ The {gap} missing files correspond exactly to perfect scores that should be skipped")
            print(f"  Running without --dry-run will create {gap} skipped marker files")
        elif gap > 0:
            print(f"✗ Missing {gap} files")
            successful = actual_data["status_counts"].get("success", 0)
            failed = actual_data["status_counts"].get("failed", 0)
            skipped = actual_data["status_counts"].get("skipped", 0)
            
            print(f"  Current: {successful} success + {failed} failed + {skipped} skipped = {successful + failed + skipped}")
            
            if skip_perfect:
                print(f"  Expected: {expected_total - total_perfect} (excluding {total_perfect} perfect scores)")
                print(f"  Missing {gap} files likely include:")
                print(f"    - Failed generations that weren't saved ({gap} files)")
                print(f"    - Operations for perfect scores that should be skipped")
        else:
            print(f"✓ File count matches expected")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check critique file status")
    parser.add_argument("--critique-type", type=str, required=True,
                       help="Critique type to analyze")
    parser.add_argument("--export-folder", type=str, required=True,
                       help="Export folder to compare against")
    parser.add_argument("--output-dir", type=str, default="output_critiques",
                       help="Output directory for critiques")
    
    args = parser.parse_args()
    
    compare_with_expected(args.critique_type, args.export_folder)