import os
import json
import argparse
from pathlib import Path
from feedback_app import (
    get_video_id, get_filename, load_json, load_config, FOLDER,
    FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX, REVIEWER_FILE_POSTFIX,
    parse_args
)

# Constants
DRY_RUN = False  # Set to False to actually delete files

def check_reviewer_files(video_urls, output_dir):
    """Check for problematic reviewer files and optionally fix them.
    
    Args:
        video_urls: List of video URLs to check
        output_dir: Output directory to check
        
    Returns:
        tuple: (total_files_checked, problematic_files_found)
    """
    print(f"\nChecking reviewer files in {output_dir}")
    print("=" * 80)
    
    total_files_checked = 0
    problematic_files_found = 0
    
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        
        # Get all relevant files
        feedback_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
        prev_feedback_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
        reviewer_file = get_filename(video_id, output_dir, REVIEWER_FILE_POSTFIX)
        
        # Skip if no reviewer file
        if not os.path.exists(reviewer_file):
            continue
            
        total_files_checked += 1
        
        # Load reviewer data
        with open(reviewer_file, 'r') as f:
            reviewer_data = json.load(f)
            is_rejected = not reviewer_data.get("reviewer_double_check", False)
        
        # If rejected, check if prev feedback exists
        if is_rejected and not os.path.exists(prev_feedback_file):
            problematic_files_found += 1
            print(f"\nFound problematic reviewer file for {video_id}:")
            print(f"  - Reviewer file: {reviewer_file}")
            print(f"  - Status: Rejected")
            print(f"  - Missing prev feedback file: {prev_feedback_file}")
            
            if not DRY_RUN:
                print(f"  - Deleting reviewer file...")
                os.remove(reviewer_file)
                print(f"  - Deleted successfully")
            else:
                print(f"  - Would delete reviewer file in non-dry-run mode")
            
            # Print reviewer data for debugging
            print("\nReviewer data:")
            print(json.dumps(reviewer_data, indent=2))
            
            # Print feedback data if it exists
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                print("\nCurrent feedback data:")
                print(json.dumps(feedback_data, indent=2))
    
    return total_files_checked, problematic_files_found

def main():
    # Use the same argument parser as feedback_app.py
    args = parse_args()
    
    # Load configs
    configs = load_config(FOLDER / args.configs)
    configs = [load_config(FOLDER / config) for config in configs]
    
    # Load video URLs from all files
    all_video_urls = []
    for video_urls_file in args.video_urls_files:
        video_urls = load_json(FOLDER / video_urls_file)
        all_video_urls.extend(video_urls)
    
    # Statistics
    total_configs = len(configs)
    total_configs_checked = 0
    total_files_checked = 0
    total_problematic_files = 0
    
    print(f"\nStarting debug of reviewer files...")
    print(f"DRY RUN: {DRY_RUN}")
    print(f"Total configs to check: {total_configs}")
    print(f"Total videos to check: {len(all_video_urls)}")
    print("=" * 80)
    
    # Check each config
    for config in configs:
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        if not os.path.exists(output_dir):
            print(f"Skipping {output_dir} - directory does not exist")
            continue
            
        total_configs_checked += 1
        files_checked, problematic_files = check_reviewer_files(all_video_urls, output_dir)
        total_files_checked += files_checked
        total_problematic_files += problematic_files
    
    # Print final statistics
    print("\nFinal Statistics:")
    print("=" * 80)
    print(f"Total configs checked: {total_configs_checked}/{total_configs}")
    print(f"Total reviewer files checked: {total_files_checked}")
    print(f"Total problematic files found: {total_problematic_files}")
    if total_files_checked > 0:
        print(f"Problematic files percentage: {(total_problematic_files/total_files_checked)*100:.2f}%")
    print("=" * 80)

if __name__ == "__main__":
    main() 