"""
check_missing_annotators.py

One-off utility script to check for feedback files with missing annotators in a video captioning project.

- Scans all feedback files for all configs and all video batches (using DEFAULT_VIDEO_URLS_FILES from feedback_app.py).
- Reports which videos (and which config/task) are missing an annotator (the 'user' field).
- Optionally, with --add-user, fills in the missing 'user' field with a specified annotator (default: 'Zhiqiu Lin').
- Prints a summary grouped by config and by video batch file.

Typical usage:
    python check_missing_annotators.py
    python check_missing_annotators.py --add-user "Siyuan Cen"

This script is intended for one-time data repair and is not meant for regular use in the annotation workflow.
"""
import os
import json
import argparse
from pathlib import Path
from feedback_app import (
    DEFAULT_VIDEO_URLS_FILES, load_video_data, get_video_id, load_json, get_filename,
    load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX, REVIEWER_FILE_POSTFIX,
    load_config, ANNOTATORS
)
from feedback_diff_app import get_video_status

def check_missing_annotators(output_dir, configs_path="all_configs.json", add_user="Zhiqiu Lin"):
    """
    Check for missing annotators in feedback files, and optionally add user to those feedback files.
    
    Args:
        output_dir: Path to the output directory containing captions
        configs_path: Path to the configs JSON file
        add_user: Add this user to feedback files with missing annotators (default: Zhiqiu Lin)
    """
    # Validate add_user
    if add_user is not None and add_user not in ANNOTATORS:
        raise ValueError(f"User '{add_user}' is not in the list of annotators in feedback_app.py!")

    video_urls_files = DEFAULT_VIDEO_URLS_FILES
    
    # Load configs
    configs = load_config(FOLDER / configs_path)
    configs = [load_config(FOLDER / config) for config in configs]
    config_dict = {config["name"]: config for config in configs}
    
    # Track missing annotators
    missing_info = {}  # {config_name: {video_id: urls_file}}
    
    # Create a mapping of video_id to urls_file for quick lookup
    video_to_file = {}
    for urls_file in video_urls_files:
        try:
            video_urls = load_json(FOLDER / urls_file)
            for video_url in video_urls:
                video_id = get_video_id(video_url)
                video_to_file[video_id] = urls_file
        except Exception as e:
            print(f"Error loading {urls_file}: {str(e)}")
            continue
    
    # Check each config
    for config_name, config in config_dict.items():
        config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
        if not os.path.exists(config_output_dir):
            print(f"No output directory for {config_name}")
            continue
        
        # Initialize tracking for this config
        if config_name not in missing_info:
            missing_info[config_name] = {}
        
        # Check each video in all URLs files
        for video_id, urls_file in video_to_file.items():
            status, current_file, prev_file, current_user, prev_user = get_video_status(video_id, config_output_dir)
            
            # Skip if not completed
            if status == "not_completed":
                continue
            
            # Determine the annotator (original caption creator)
            annotator = prev_user if prev_file else current_user
            if annotator is None:
                missing_info[config_name][video_id] = urls_file
                feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
                if add_user:
                    # Only add user to feedback_file if it exists and doesn't already have a user
                    if os.path.exists(feedback_file):
                        try:
                            with open(feedback_file, 'r') as f:
                                data = json.load(f)
                            if not data.get("user"):
                                data["user"] = add_user
                                with open(feedback_file, 'w') as f:
                                    json.dump(data, f, indent=4)
                                print(f"Added user '{add_user}' to {feedback_file}")
                            else:
                                print(f"Skipped {feedback_file}: already has user '{data['user']}'")
                        except Exception as e:
                            print(f"Error updating {feedback_file}: {e}")
    
    # Print summary
    print("\nSummary of Missing Annotators:")
    print("=" * 80)
    
    total_missing = 0
    for config_name, missing_videos in missing_info.items():
        if missing_videos:
            print(f"\n{config_name}:")
            print("-" * 40)
            # Group by URLs file
            by_file = {}
            for video_id, urls_file in missing_videos.items():
                if urls_file not in by_file:
                    by_file[urls_file] = []
                by_file[urls_file].append(video_id)
            
            # Print grouped by file
            for urls_file, video_ids in by_file.items():
                print(f"\nFrom {urls_file}:")
                for video_id in sorted(video_ids):
                    print(f"  {video_id}")
            total_missing += len(missing_videos)
    
    print("\nTotal Statistics:")
    print("=" * 80)
    print(f"Total videos with missing annotators: {total_missing}")
    for config_name, missing_videos in missing_info.items():
        if missing_videos:
            print(f"{config_name}: {len(missing_videos)} videos")

def main():
    parser = argparse.ArgumentParser(description="Check for missing annotators in feedback files")
    parser.add_argument("--output", type=str, default="output_captions",
                      help="Path to the output directory")
    parser.add_argument("--configs", type=str, default="all_configs.json",
                      help="Path to the JSON config file")
    parser.add_argument("--add-user", type=str, default="Zhiqiu Lin",
                      help="Add this user to feedback files with missing annotators. Default: Zhiqiu Lin")
    
    args = parser.parse_args()
    check_missing_annotators(args.output, args.configs, args.add_user)

if __name__ == "__main__":
    main() 