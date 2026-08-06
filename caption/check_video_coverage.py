#!/usr/bin/env python3

import json
import sys
import os
from pathlib import Path

def load_json_file(file_path):
    """Load JSON file and return list of URLs"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        sys.exit(1)

def load_main_config():
    """Load the main configuration dynamically"""
    try:
        # Add the project root to Python path
        script_dir = Path(__file__).parent
        project_root = script_dir.parent if script_dir.name == 'caption' else script_dir
        sys.path.insert(0, str(project_root))
        
        # Import the config
        from caption.config.main_config import DEFAULT_VIDEO_URLS_FILES
        return DEFAULT_VIDEO_URLS_FILES
        
    except ImportError as e:
        print(f"Error importing main_config.py: {e}")
        print("Make sure you're running this script from the project root or caption/ directory")
        sys.exit(1)

def get_video_coverage():
    """Get all videos from main config and track which file each comes from"""
    video_url_files = load_main_config()
    
    video_to_file = {}  # Maps video URL to the file it came from
    
    print(f"Loading videos from {len(video_url_files)} files in main_config.py...")
    
    for file_path in video_url_files:
        # Skip invalid files
        if 'invalid' in file_path:
            continue
            
        # Add caption/ prefix if not present
        if not file_path.startswith('caption/'):
            full_path = f"caption/{file_path}"
        else:
            full_path = file_path
            
        videos = load_json_file(full_path)
        filename = os.path.basename(file_path)
        
        # Map each video to its source file
        for video in videos:
            video_to_file[video] = filename
        
        print(f"  Loaded {len(videos)} videos from {filename}")
    
    print(f"Total videos in config: {len(video_to_file)}")
    return video_to_file

def check_video_coverage(input_file):
    """Check which videos in the input file are not covered by main config"""
    
    print(f"Checking coverage for: {input_file}")
    
    # Load the input file
    target_videos = load_json_file(input_file)
    print(f"Target file contains: {len(target_videos)} videos")
    
    # Get current coverage
    video_to_file = get_video_coverage()
    
    # Check coverage
    covered_videos = []
    missing_videos = []
    
    for video in target_videos:
        if video in video_to_file:
            covered_videos.append((video, video_to_file[video]))
        else:
            missing_videos.append(video)
    
    # Print results
    print(f"\n=== COVERAGE RESULTS ===")
    print(f"Total videos checked: {len(target_videos)}")
    print(f"Already covered: {len(covered_videos)}")
    print(f"Missing from config: {len(missing_videos)}")
    
    if covered_videos:
        print(f"\n=== VIDEOS ALREADY IN CONFIG ===")
        for video, source_file in covered_videos:
            print(f"  {video}")
            print(f"    → Found in: {source_file}")
    
    if missing_videos:
        print(f"\n=== VIDEOS NOT IN CONFIG ===")
        for video in missing_videos:
            print(f"  {video}")
    else:
        print(f"\n✓ All videos are already covered in main_config.py!")

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_video_coverage.py <json_file>")
        print("Example: python check_video_coverage.py caption/video_urls/20250406_setup_and_motion/1180_to_1190.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    check_video_coverage(input_file)

if __name__ == "__main__":
    main()