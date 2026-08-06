"""
This script cleans up duplicate prev feedback files in the video captioning system.

Background:
- The prev feedback file (_feedback_prev.json) should only be used when a reviewer redoes a caption
- In this case, the annotator's version becomes the prev feedback, and the reviewer's version becomes current
- However, sometimes prev feedback files are created when they shouldn't be (e.g., same annotator)
- These duplicate prev feedback files can cause confusion and should be removed

Purpose:
- Identify and remove prev feedback files where both current and prev feedback are from the same annotator
- This ensures the prev feedback file is only used for its intended purpose: storing the annotator's version
  when a reviewer makes changes

Usage:
1. First run with DRY_RUN=True to see what would be removed
2. Review the output to ensure it's correct
3. Set DRY_RUN=False to actually remove the files
"""

import os
import json
from feedback_app import (
    parse_args, load_data, get_filename, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    load_config, load_video_data, get_video_id, load_json
)

# Set to False to actually remove files
DRY_RUN = False

def cleanup_prev_feedback(args):
    """
    Clean up duplicate prev feedback files where the current and previous feedback
    are from the same annotator. This should not happen as prev feedback should
    only be used when a reviewer redoes the caption.
    
    Args:
        args: Arguments from feedback_app.py
    """
    # Load configs and video data
    configs = load_config(FOLDER / args.configs)
    configs = [load_config(FOLDER / config) for config in configs]
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    
    # Track statistics
    total_checked = 0
    total_duplicates = 0
    
    # Process each config
    for config in configs:
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        if not os.path.exists(output_dir):
            continue
            
        # Get all feedback files for this config
        feedback_files = [f for f in os.listdir(output_dir) if f.endswith(FEEDBACK_FILE_POSTFIX)]
        
        for feedback_file in feedback_files:
            video_id = feedback_file.replace(FEEDBACK_FILE_POSTFIX, "")
            prev_feedback_file = f"{video_id}{PREV_FEEDBACK_FILE_POSTFIX}"
            
            # Check if prev feedback exists
            if os.path.exists(os.path.join(output_dir, prev_feedback_file)):
                total_checked += 1
                
                # Load both current and previous feedback
                current_feedback = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                
                # Check if both files exist and have user information
                if current_feedback and prev_feedback and "user" in current_feedback and "user" in prev_feedback:
                    current_user = current_feedback["user"]
                    prev_user = prev_feedback["user"]
                    
                    # If same user, this is a duplicate that should be removed
                    if current_user == prev_user:
                        total_duplicates += 1
                        print(f"Found duplicate prev feedback for video {video_id} in {config['name']}:")
                        print(f"  Current user: {current_user}")
                        print(f"  Previous user: {prev_user}")
                        print(f"  Current timestamp: {current_feedback.get('timestamp', 'unknown')}")
                        print(f"  Previous timestamp: {prev_feedback.get('timestamp', 'unknown')}")
                        
                        if not DRY_RUN:
                            # Remove the prev feedback file
                            os.remove(os.path.join(output_dir, prev_feedback_file))
                            print(f"  Removed {prev_feedback_file}")
                        else:
                            print(f"  Would remove {prev_feedback_file}")
    
    print("\nSummary:")
    print(f"Total files checked: {total_checked}")
    print(f"Total duplicates found: {total_duplicates}")
    if DRY_RUN:
        print("This was a dry run - no files were actually removed")
    else:
        print("Files have been removed")

if __name__ == "__main__":
    args = parse_args()
    cleanup_prev_feedback(args) 