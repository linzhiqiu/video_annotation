"""
Script to generate reviewer files for videos where the current and previous feedback
were created by different users. This helps track which videos need review.

Created: 2024-03-21
Last Modified: 2024-03-21
"""

import os
import json
from datetime import datetime
from pathlib import Path
from feedback_app import (
    parse_args, load_video_data, get_video_id, load_json, 
    get_filename, load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    REVIEWER_FILE_POSTFIX, load_config
)

# Set to True to preview changes without making them
# This is useful to check the results before running the script
DRY_RUN = False

def generate_reviewer_files(args, dry_run=False):
    """Generate reviewer files for videos where current and previous feedback have different users"""
    # Load configurations
    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        print(f"Config file not found: {args.configs}")
        return

    # Load video URLs from all files
    video_urls = []
    for video_urls_file in args.video_urls_files:
        try:
            urls = load_json(FOLDER / video_urls_file)
            video_urls.extend(urls)
        except FileNotFoundError:
            print(f"Video URLs file not found: {video_urls_file}")
            continue

    video_ids = [get_video_id(video_url) for video_url in video_urls]

    # Statistics
    total_videos = 0
    videos_with_feedback = 0
    videos_with_prev_feedback = 0
    videos_with_different_users = 0
    videos_with_existing_reviewer = 0
    new_reviewer_files_created = 0

    # Process each configuration
    for config in configs:
        config_name = config["name"]
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        
        if not os.path.exists(output_dir):
            print(f"Output directory not found: {output_dir}")
            continue
        
        print(f"\nProcessing {config_name}...")
        
        # Process each video
        for video_id in video_ids:
            total_videos += 1
            
            # Get current and previous feedback files
            current_feedback_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
            prev_feedback_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
            reviewer_file = get_filename(video_id, output_dir, REVIEWER_FILE_POSTFIX)
            
            # Skip if current feedback doesn't exist
            if not os.path.exists(current_feedback_file):
                continue
            videos_with_feedback += 1
                
            # Load current feedback data
            current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
            if not current_data:
                continue
            
            current_user = current_data.get("user")
            if not current_user:
                continue
                
            # Check if reviewer file already exists
            if os.path.exists(reviewer_file):
                videos_with_existing_reviewer += 1
                continue
            
            # Check if previous feedback exists and has a different user
            prev_data = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
            if prev_data:
                videos_with_prev_feedback += 1
                prev_user = prev_data.get("user")
                
                if prev_user and prev_user != current_user:
                    videos_with_different_users += 1
                    print(f"    Found different users for {video_id}: {prev_user} -> {current_user}")
                    
                    # Create reviewer data
                    reviewer_data = {
                        "reviewer_name": current_user,  # The current user becomes the reviewer
                        "review_timestamp": datetime.now().isoformat(),
                        "reviewer_double_check": False
                    }
                    
                    if not dry_run:
                        # Save reviewer file
                        os.makedirs(output_dir, exist_ok=True)
                        with open(reviewer_file, 'w') as f:
                            json.dump(reviewer_data, f, indent=4)
                        new_reviewer_files_created += 1
                        print(f"    Created reviewer file for {video_id}")

    # Print statistics
    print("\nStatistics:")
    print(f"Total videos processed: {total_videos}")
    print(f"Videos with feedback: {videos_with_feedback}")
    print(f"Videos with previous feedback: {videos_with_prev_feedback}")
    print(f"Videos with different users: {videos_with_different_users}")
    print(f"Videos with existing reviewer files: {videos_with_existing_reviewer}")
    print(f"New reviewer files created: {new_reviewer_files_created}")

def main():
    args = parse_args()
    generate_reviewer_files(args, dry_run=DRY_RUN)

if __name__ == "__main__":
    main() 