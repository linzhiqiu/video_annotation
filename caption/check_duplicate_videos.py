#!/usr/bin/env python3

import json
import sys
import os
import argparse
from pathlib import Path
from collections import defaultdict

def load_json_file(file_path):
    """Load JSON file and return list of URLs"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return []

def load_config(config_type):
    """Load the configuration dynamically"""
    try:
        # Add the project root to Python path
        script_dir = Path(__file__).parent
        project_root = script_dir.parent if script_dir.name == 'caption' else script_dir
        sys.path.insert(0, str(project_root))
        
        # Import the appropriate config
        if config_type == "main":
            from caption.config.main_config import DEFAULT_VIDEO_URLS_FILES
            return DEFAULT_VIDEO_URLS_FILES
        elif config_type == "lighting":
            from caption.config.lighting_config import LIGHTING_VIDEO_URLS_FILES
            return LIGHTING_VIDEO_URLS_FILES
        else:
            raise ValueError(f"Unknown config type: {config_type}")
        
    except ImportError as e:
        print(f"Error importing {config_type}_config.py: {e}")
        print("Make sure you're running this script from the project root or caption/ directory")
        sys.exit(1)

def check_for_duplicates(config_type):
    """Check for duplicate videos across all files in the config"""
    
    print(f"Checking for duplicate videos in {config_type} configuration...")
    
    # Load the config
    video_url_files = load_config(config_type)
    
    # Track video occurrences
    video_to_files = defaultdict(list)  # Maps video URL to list of files containing it
    file_stats = {}  # Maps filename to video count
    
    print(f"Analyzing {len(video_url_files)} files (including invalid files)...")
    
    for file_path in video_url_files:
        # Add caption/ prefix if not present
        if not file_path.startswith('caption/'):
            full_path = f"caption/{file_path}"
        else:
            full_path = file_path
            
        videos = load_json_file(full_path)
        filename = os.path.basename(file_path)
        file_stats[filename] = len(videos)
        
        # Track which files each video appears in
        for video in videos:
            video_to_files[video].append(filename)
        
        file_type = "(invalid)" if 'invalid' in file_path else "(batch)"
        print(f"  Processed {filename}: {len(videos)} videos {file_type}")
    
    # CORE LOGIC: Find videos that appear in more than one file
    duplicates = {video: files for video, files in video_to_files.items() if len(files) > 1}
    unique_videos = {video: files for video, files in video_to_files.items() if len(files) == 1}
    
    # Calculate statistics
    total_video_entries = sum(file_stats.values())
    total_unique_videos = len(video_to_files)
    total_duplicates = len(duplicates)
    duplicate_entries = sum(len(files) for files in duplicates.values())
    
    # Print results
    print(f"\n=== DUPLICATE VIDEO ANALYSIS ===")
    print(f"Configuration: {config_type}")
    print(f"Total video entries across all files: {total_video_entries}")
    print(f"Unique videos: {total_unique_videos}")
    print(f"Videos appearing in multiple files: {total_duplicates}")
    print(f"Extra duplicate entries: {duplicate_entries - total_duplicates}")
    print(f"Space that could be saved: {total_video_entries - total_unique_videos} entries")
    
    if duplicates:
        print(f"\n=== VIDEOS APPEARING IN MULTIPLE FILES ===")
        
        # Sort duplicates by number of occurrences (highest first)
        sorted_duplicates = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
        
        for video, files in sorted_duplicates:
            print(f"\nVideo: {video}")
            print(f"  Appears in {len(files)} files:")
            for filename in files:
                print(f"    - {filename}")
        
        print(f"\n=== FILES CONTAINING DUPLICATE VIDEOS ===")
        
        # Count how many duplicates each file contains
        file_duplicate_counts = defaultdict(int)
        for video, files in duplicates.items():
            for filename in files:
                file_duplicate_counts[filename] += 1
        
        # Sort files by duplicate count
        sorted_files = sorted(file_duplicate_counts.items(), key=lambda x: x[1], reverse=True)
        
        for filename, dup_count in sorted_files:
            total_videos = file_stats.get(filename, 0)
            percentage = (dup_count / total_videos * 100) if total_videos > 0 else 0
            print(f"  {filename}: {dup_count}/{total_videos} videos are duplicates ({percentage:.1f}%)")
            
    else:
        print(f"\n✓ No duplicate videos found! Each video URL appears in exactly one file.")
    
    print(f"\n=== FILE STATISTICS ===")
    print(f"Files analyzed: {len(file_stats)}")
    batch_files = [(f, c) for f, c in file_stats.items() if 'invalid' not in f]
    invalid_files = [(f, c) for f, c in file_stats.items() if 'invalid' in f]
    
    print(f"Batch files ({len(batch_files)}):")
    for filename, count in sorted(batch_files):
        print(f"  {filename}: {count} videos")
    
    if invalid_files:
        print(f"Invalid files ({len(invalid_files)}):")
        for filename, count in sorted(invalid_files):
            print(f"  {filename}: {count} videos")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Check for duplicate videos across configuration files")
    parser.add_argument("--config", 
                       choices=["main", "lighting"], 
                       required=True,
                       help="Configuration to check: 'main' for main_config.py or 'lighting' for lighting_config.py")
    
    return parser.parse_args()

def main():
    args = parse_args()
    check_for_duplicates(args.config)

if __name__ == "__main__":
    main()