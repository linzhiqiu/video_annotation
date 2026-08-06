#!/usr/bin/env python3

import json
import sys
import os
import argparse
import glob
from pathlib import Path

def load_json_file(file_path):
    """Load JSON file and return list of URLs"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return []

def save_json_file(data, file_path):
    """Save JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} videos to: {file_path}")

def load_main_config():
    """Load the main configuration dynamically"""
    try:
        # Add the project root to Python path
        script_dir = Path(__file__).parent
        project_root = script_dir.parent if script_dir.name == 'caption' else script_dir
        sys.path.insert(0, str(project_root))
        
        # Import the config
        from caption.config.main_config import DEFAULT_VIDEO_URLS_FILES
        
        print(f"Loaded {len(DEFAULT_VIDEO_URLS_FILES)} file paths from main_config.py")
        return DEFAULT_VIDEO_URLS_FILES
        
    except ImportError as e:
        print(f"Error importing main_config.py: {e}")
        print("Make sure you're running this script from the project root or caption/ directory")
        sys.exit(1)

def get_all_existing_videos():
    """Get all videos from both overlap and nonoverlap sets"""
    
    # Load file paths from main_config.py
    video_url_files = load_main_config()
    
    all_existing = set()
    
    # Load all videos from the config files
    print("Loading existing videos from main_config.py...")
    for file_path in video_url_files:
        # Skip invalid files to avoid errors
        if 'invalid' in file_path:
            print(f"  Skipping invalid file: {file_path}")
            continue
            
        # Add caption/ prefix if not present
        if not file_path.startswith('caption/'):
            full_path = f"caption/{file_path}"
        else:
            full_path = file_path
            
        videos = load_json_file(full_path)
        all_existing.update(videos)
        print(f"  Loaded {len(videos)} videos from {file_path}")
    
    print(f"Total existing videos: {len(all_existing)}")
    return all_existing

def find_all_file(directory, mode):
    """Find the appropriate all_XXX.json file in the directory"""
    if mode == "overlap":
        pattern = f"{directory}/overlap_all_*.json"
    else:  # nonoverlap
        pattern = f"{directory}/nonoverlap_all_*.json"
    
    files = glob.glob(pattern)
    
    if not files:
        print(f"Error: No {mode}_all_*.json file found in {directory}")
        return None
    
    if len(files) > 1:
        print(f"Warning: Multiple {mode}_all_*.json files found: {files}")
        print(f"Using the first one: {files[0]}")
    
    return files[0]

def get_last_batch_number(mode):
    """Get the last batch number from main_config.py for the specified mode"""
    video_url_files = load_main_config()
    
    last_number = 0
    matching_files = []
    
    for file_path in video_url_files:
        if 'invalid' in file_path:
            continue
            
        filename = os.path.basename(file_path)
        
        try:
            if mode == "overlap" and filename.startswith("overlap_") and "_to_" in filename:
                # Extract end number from overlap_X_to_Y.json
                end_num = int(filename.split("_to_")[1].replace(".json", ""))
                matching_files.append((filename, end_num))
                last_number = max(last_number, end_num)
            elif mode == "nonoverlap" and not filename.startswith("overlap_") and "_to_" in filename:
                # Extract end number from X_to_Y.json (nonoverlap files)
                end_num = int(filename.split("_to_")[1].replace(".json", ""))
                matching_files.append((filename, end_num))
                last_number = max(last_number, end_num)
        except (ValueError, IndexError):
            continue
    
    print(f"Found {len(matching_files)} {mode} batch files:")
    for filename, end_num in sorted(matching_files, key=lambda x: x[1])[-5:]:  # Show last 5
        print(f"  {filename} (ends at {end_num})")
    
    print(f"Last {mode} batch number: {last_number}")
    return last_number

def calculate_videos_needed(last_number):
    """Calculate how many videos are needed to round up to the nearest 10"""
    remainder = last_number % 10
    if remainder == 0:
        print(f"Current last number: {last_number}")
        print(f"Already ends with 0 - no padding needed!")
        return 0, last_number  # Return tuple consistently
    
    needed = 10 - remainder
    target = last_number + needed
    
    print(f"Current last number: {last_number}")
    print(f"Target round number: {target}")
    print(f"Videos needed: {needed}")
    
    return needed, target

def process_directory(directory, mode):
    """Process the directory to create subset files"""
    
    print(f"\n=== Processing {directory} in {mode} mode ===")
    
    # Find the all_XXX.json file
    all_file = find_all_file(directory, mode)
    if not all_file:
        return
    
    print(f"Found {mode} file: {all_file}")
    
    # Get last batch number for this mode
    last_number = get_last_batch_number(mode)
    
    # Calculate videos needed
    videos_needed, target_number = calculate_videos_needed(last_number)
    
    if videos_needed == 0:
        print(f"✓ No padding needed for {mode} mode - already ends with 0!")
        print(f"✓ Your {mode} batches are perfectly aligned")
        print(f"✓ You can proceed directly with your process_new_videos script")
        
        # Still show how many new videos are available
        all_existing = get_all_existing_videos()
        new_videos = load_json_file(all_file)
        truly_new = [video for video in new_videos if video not in all_existing]
        
        if truly_new:
            print(f"\nℹ️  Available for future batches: {len(truly_new)} new videos")
            # Save all new videos for future use
            if mode == "overlap":
                future_filename = f"{directory}/overlap_future_{len(truly_new)}.json"
            else:
                future_filename = f"{directory}/nonoverlap_future_{len(truly_new)}.json"
            save_json_file(truly_new, future_filename)
            print(f"   Saved to: {future_filename}")
        
        return
    
    # Get all existing videos
    all_existing = get_all_existing_videos()
    
    # Load new videos from the all_XXX.json file
    print(f"\nLoading new videos from {all_file}...")
    new_videos = load_json_file(all_file)
    print(f"Loaded {len(new_videos)} potential new videos")
    
    # Find truly new videos
    truly_new = [video for video in new_videos if video not in all_existing]
    print(f"Found {len(truly_new)} truly new videos")
    
    if len(truly_new) < videos_needed:
        print(f"ERROR: Need {videos_needed} videos but only found {len(truly_new)} new videos")
        print("Cannot create subset files")
        return
    
    # Create subset files
    create_subset_files(directory, mode, truly_new, videos_needed, last_number, target_number)

def create_subset_files(directory, mode, truly_new, videos_needed, last_number, target_number):
    """Create the subset files with proper naming"""
    
    # Create only the padding file with the exact number of videos needed
    subset_videos = truly_new[:videos_needed]
    
    # Simple naming: just the count of videos needed for padding
    padding_filename = f"{directory}/{mode}_padding_{videos_needed}_videos.json"
    save_json_file(subset_videos, padding_filename)
    
    print(f"\n=== Created file for {mode} mode ===")
    print(f"File: {padding_filename}")
    print(f"Contains: {videos_needed} videos for padding from {last_number} to {target_number}")
    
    # Show info about remaining videos but don't save them
    remaining_videos = truly_new[videos_needed:]
    if remaining_videos:
        print(f"Note: {len(remaining_videos)} additional new videos available for future batches")
    
    print(f"\n=== Next steps ===")
    
    # Find the actual current file name from the config
    video_url_files = load_main_config()
    current_file = None
    
    for file_path in video_url_files:
        filename = os.path.basename(file_path)
        if mode == "overlap" and filename.startswith("overlap_") and filename.endswith(f"_to_{last_number}.json"):
            current_file = filename
            break
        elif mode == "nonoverlap" and not filename.startswith("overlap_") and filename.endswith(f"_to_{last_number}.json"):
            current_file = filename
            break
    
    if current_file:
        # Extract the start number from the current file
        if mode == "overlap":
            start_num = int(current_file.replace("overlap_", "").split("_to_")[0])
            target_file = f"overlap_{start_num}_to_{target_number}.json"
        else:
            start_num = int(current_file.split("_to_")[0])
            target_file = f"{start_num}_to_{target_number}.json"
        
        print(f"1. Add the {videos_needed} videos from {padding_filename}")
        print(f"   to your current file: {current_file}")
        print(f"2. Rename that file to: {target_file}")
        print(f"3. Update main_config.py to reference the new filename")
        print(f"4. Run your process_new_videos script which will start from {target_number}")
        
        print(f"\nDetails:")
        print(f"- Current: {current_file} has {last_number-start_num} videos (positions {start_num} to {last_number-1})")
        print(f"- After padding: {target_file} will have {target_number-start_num} videos (positions {start_num} to {target_number-1})")
    else:
        print(f"Warning: Could not find current file ending with _to_{last_number}.json")
        print(f"Manually find your file that ends with {last_number} and add the {videos_needed} videos to it")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Find new videos and create subset files for padding batch files to round numbers")
    parser.add_argument("directory", 
                       help="Directory containing the all_XXX.json files (e.g., caption/video_urls/20250912_setup_and_motion/)")
    parser.add_argument("--mode", 
                       choices=["overlap", "nonoverlap"], 
                       required=True,
                       help="Mode: 'overlap' for overlap_all_*.json or 'nonoverlap' for nonoverlap_all_*.json")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Validate directory exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory {args.directory} does not exist")
        sys.exit(1)
    
    # Process the directory
    process_directory(args.directory, args.mode)

if __name__ == "__main__":
    main()