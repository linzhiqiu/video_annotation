#!/usr/bin/env python3
"""
Script to check for missing 'user' fields in feedback and prev_feedback files.
Prints all video_id and task combinations that don't have 'user' field.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Import the DEFAULT_VIDEO_URLS_FILES from main_config.py
try:
    import sys
    sys.path.append('/project_data/ramanan/zhiqiu/video_annotation')
    from caption.config.main_config import DEFAULT_VIDEO_URLS_FILES
except ImportError:
    # Fallback if import fails
    DEFAULT_VIDEO_URLS_FILES = []
    print("Warning: Could not import DEFAULT_VIDEO_URLS_FILES from main_config.py")

def load_json_file(file_path: Path) -> Dict:
    """Load JSON file and return data, or None if file doesn't exist or is invalid."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Warning: Could not load {file_path}: {e}")
    return None

def get_video_id_from_url(video_url: str) -> str:
    """Extract video ID from video URL - matching the original get_video_id function"""
    if video_url.endswith('.mp4'):
        return video_url.split('/')[-1][:-4]  # Remove .mp4 extension
    return video_url

def get_sheet_name_from_video_id(video_id: str, root_dir: str) -> str:
    """
    Get the sheet name from video_id by checking which DEFAULT_VIDEO_URLS_FILES contains it.
    
    Args:
        video_id: The video ID to search for (e.g., "0kpu6VM3rZU.2")
        root_dir: Root directory path
        
    Returns:
        Sheet name derived from the file path
    """
    root_path = Path(root_dir).parent  # Go up one level to find video_urls directory
    
    for video_urls_file in DEFAULT_VIDEO_URLS_FILES:
        video_urls_path = root_path / video_urls_file
        
        if video_urls_path.exists():
            try:
                with open(video_urls_path, 'r') as f:
                    video_urls = json.load(f)
                
                # Check ALL videos in this file (not just first 3)
                for video_url in video_urls:
                    current_video_id = get_video_id_from_url(video_url)
                    # Compare both with and without .mp4 extension
                    if (current_video_id == video_id or 
                        current_video_id == video_id.replace('.mp4', '') or
                        current_video_id + '.mp4' == video_id):
                        # Extract sheet name from file path
                        # Convert path like "video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json" 
                        # to sheet name like "overlap_0_to_94"
                        return video_urls_file.split('/')[-1].replace('.json', '')
                    
            except (json.JSONDecodeError, FileNotFoundError):
                continue
    
    return 'unknown_sheet'

def find_missing_user_fields(root_dir: str) -> List[Tuple[str, str, str, str, str]]:
    """
    Find all video_id and task combinations missing 'user' field.
    
    Args:
        root_dir: Root directory to search for feedback files
        
    Returns:
        List of tuples: (video_id, task, issue_type, file_path, sheet_name)
        where issue_type is 'feedback_missing_user' or 'prev_feedback_missing_user'
    """
    missing_user_files = []
    root_path = Path(root_dir)
    
    # Search for all feedback files
    feedback_files = list(root_path.rglob("*_feedback.json"))
    prev_feedback_files = list(root_path.rglob("*_feedback_prev.json"))
    
    print(f"Found {len(feedback_files)} feedback files")
    print(f"Found {len(prev_feedback_files)} prev_feedback files")
    print("-" * 60)
    
    # Check feedback files
    for feedback_file in feedback_files:
        data = load_json_file(feedback_file)
        if data and 'user' not in data:
            # Extract video_id and task from file path and data
            video_id = data.get('video_id', 'unknown_video_id')
            
            # Try to infer task from directory structure
            # Path structure: .../output_captions/task_name/video_id_feedback.json
            parts = feedback_file.parts
            task = 'unknown_task'
            
            # Look for the task name - it should be the directory right before the filename
            for i in range(len(parts) - 1, 0, -1):
                if parts[i - 1] == 'output_captions':
                    task = parts[i]
                    break
            
            # Get sheet name by finding which video_urls file contains this video_id
            sheet_name = get_sheet_name_from_video_id(video_id, root_dir)
            
            missing_user_files.append((
                video_id, 
                task, 
                'feedback_missing_user', 
                str(feedback_file),
                sheet_name
            ))
    
    # Check prev_feedback files
    for prev_feedback_file in prev_feedback_files:
        data = load_json_file(prev_feedback_file)
        if data and 'user' not in data:
            # Extract video_id and task from file path and data
            video_id = data.get('video_id', 'unknown_video_id')
            
            # Try to infer task from directory structure
            # Path structure: .../output_captions/task_name/video_id_feedback_prev.json
            parts = prev_feedback_file.parts
            task = 'unknown_task'
            
            # Look for the task name - it should be the directory right before the filename
            for i in range(len(parts) - 1, 0, -1):
                if parts[i - 1] == 'output_captions':
                    task = parts[i]
                    break
            
            # Get sheet name
            sheet_name = get_sheet_name_from_video_id(video_id, root_dir)
            
            missing_user_files.append((
                video_id, 
                task, 
                'prev_feedback_missing_user', 
                str(prev_feedback_file),
                sheet_name
            ))
    
    return missing_user_files

def print_summary_for_deletion(missing_files: List[Tuple[str, str, str, str, str]]) -> None:
    """Print a summary suitable for deletion decisions"""
    print("\n" + "="*80)
    print("FILES THAT CAN BE SAFELY DELETED (missing 'user' field)")
    print("="*80)
    
    if not missing_files:
        print("✅ No legacy files found that need deletion!")
        return
    
    # Group by issue type for easier deletion
    feedback_files = []
    prev_feedback_files = []
    
    for video_id, task, issue_type, file_path, sheet_name in missing_files:
        if issue_type == 'feedback_missing_user':
            feedback_files.append((video_id, task, file_path, sheet_name))
        else:
            prev_feedback_files.append((video_id, task, file_path, sheet_name))
    
    # Print feedback files
    if feedback_files:
        print(f"\n📁 FEEDBACK FILES TO DELETE ({len(feedback_files)} files):")
        print("-" * 50)
        for video_id, task, file_path, sheet_name in sorted(feedback_files):
            print(f"rm '{file_path}'")
            print(f"    # Video: {video_id} | Task: {task} | Sheet: {sheet_name}")
    
    # Print prev_feedback files  
    if prev_feedback_files:
        print(f"\n📁 PREV_FEEDBACK FILES TO DELETE ({len(prev_feedback_files)} files):")
        print("-" * 50)
        for video_id, task, file_path, sheet_name in sorted(prev_feedback_files):
            print(f"rm '{file_path}'")
            print(f"    # Video: {video_id} | Task: {task} | Sheet: {sheet_name}")
    
    print(f"\n📊 DELETION SUMMARY:")
    print(f"   Total files to delete: {len(missing_files)}")
    print(f"   Feedback files: {len(feedback_files)}")  
    print(f"   Prev-feedback files: {len(prev_feedback_files)}")
    
    # Show unique tasks and sheets affected
    tasks = set(task for _, task, _, _, _ in missing_files)
    sheets = set(sheet for _, _, _, _, sheet in missing_files if sheet != 'unknown_sheet')
    
    print(f"   Tasks affected: {sorted(tasks)}")
    print(f"   Sheets affected: {sorted(sheets)}")

def debug_specific_video(video_id: str, root_dir: str) -> None:
    """Debug a specific video ID to see exactly what's happening"""
    print(f"\n🎯 SPECIFIC DEBUG for video_id: '{video_id}'")
    print("=" * 60)
    
    root_path = Path(root_dir).parent
    
    # Check the specific file you mentioned
    target_file = "video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json"
    video_urls_path = root_path / target_file
    
    print(f"🔍 Checking specific file: {target_file}")
    print(f"📂 Full path: {video_urls_path}")
    print(f"📁 Exists: {video_urls_path.exists()}")
    
    if video_urls_path.exists():
        try:
            with open(video_urls_path, 'r') as f:
                video_urls = json.load(f)
            
            print(f"📊 Found {len(video_urls)} videos in file")
            
            # Search for the specific video
            matches = []
            for i, video_url in enumerate(video_urls):
                current_video_id = get_video_id_from_url(video_url)
                if video_id in current_video_id or current_video_id in video_id:
                    matches.append((i, video_url, current_video_id))
                    print(f"✅ POTENTIAL MATCH #{i}: {video_url} -> '{current_video_id}'")
                elif video_id.replace('.mp4', '') == current_video_id:
                    matches.append((i, video_url, current_video_id))
                    print(f"✅ EXACT MATCH #{i}: {video_url} -> '{current_video_id}'")
            
            if not matches:
                print(f"❌ No matches found for '{video_id}'")
                print("🔍 Let's check some sample videos from this file:")
                for i in range(min(10, len(video_urls))):
                    sample_url = video_urls[i]
                    sample_id = get_video_id_from_url(sample_url)
                    print(f"   {i}: {sample_url} -> '{sample_id}'")
                    
                # Also check if we can find it with different patterns
                print(f"\n🔍 Searching for any URL containing '{video_id.replace('.mp4', '')}':")
                for i, video_url in enumerate(video_urls):
                    if video_id.replace('.mp4', '') in video_url:
                        current_video_id = get_video_id_from_url(video_url)
                        print(f"   Found containing pattern #{i}: {video_url} -> '{current_video_id}'")
            else:
                print(f"🎉 Found {len(matches)} potential matches!")
                
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        print("❌ File does not exist!")
        
    print("\n" + "=" * 60)

def debug_sheet_detection(root_dir: str, sample_video_ids: List[str]) -> None:
    """Debug function to check sheet detection logic"""
    print("\n🔍 DEBUGGING SHEET DETECTION:")
    print("=" * 50)
    
    print(f"DEFAULT_VIDEO_URLS_FILES loaded: {len(DEFAULT_VIDEO_URLS_FILES)}")
    if DEFAULT_VIDEO_URLS_FILES:
        print("Sample files:")
        for i, file_path in enumerate(DEFAULT_VIDEO_URLS_FILES[:3]):
            print(f"  {i+1}. {file_path}")
        if len(DEFAULT_VIDEO_URLS_FILES) > 3:
            print(f"  ... and {len(DEFAULT_VIDEO_URLS_FILES) - 3} more files")
    else:
        print("❌ No DEFAULT_VIDEO_URLS_FILES found!")
        return
    
    # Debug the specific video you mentioned
    debug_specific_video("RYzkI_5ub58.3.0.mp4", root_dir)
    
    print(f"\nTesting with sample video IDs: {sample_video_ids[:5]}")
    print("-" * 30)
    
    root_path = Path(root_dir).parent
    for video_id in sample_video_ids[:2]:  # Test first 2 to save space
        print(f"\n🎬 Testing video_id: '{video_id}'")
        
        found_in_sheets = []
        
        # Search through ALL files thoroughly  
        for video_urls_file in DEFAULT_VIDEO_URLS_FILES:
            video_urls_path = root_path / video_urls_file
            
            if video_urls_path.exists():
                try:
                    with open(video_urls_path, 'r') as f:
                        video_urls = json.load(f)
                    
                    # Check ALL videos
                    for video_url in video_urls:
                        current_video_id = get_video_id_from_url(video_url)
                        if current_video_id == video_id or current_video_id == video_id.replace('.mp4', ''):
                            sheet_name = video_urls_file.split('/')[-1].replace('.json', '')
                            found_in_sheets.append(sheet_name)
                            print(f"    ✅ MATCH FOUND in {sheet_name}: {video_url} -> {current_video_id}")
                            break
                        
                except Exception as e:
                    print(f"    ❌ Error reading {video_urls_file}: {e}")
        
        if found_in_sheets:
            print(f"  🎯 Found in sheets: {found_in_sheets}")
        else:
            print(f"  ❌ Not found in any of {len(DEFAULT_VIDEO_URLS_FILES)} sheets")

def main():
    """Main function to run the check."""
    # You may need to adjust this path to your actual data directory
    root_directory = "/project_data/ramanan/zhiqiu/video_annotation/caption/output_captions"
    
    # Alternative: if running from the project root, try this:
    # root_directory = "./caption/output_captions"
    
    if not os.path.exists(root_directory):
        print(f"Error: Directory {root_directory} does not exist.")
        print("Please update the root_directory variable to point to your caption output directory.")
        return
    
    print(f"Checking for missing 'user' fields in: {root_directory}")
    print(f"Found {len(DEFAULT_VIDEO_URLS_FILES)} video URL files in config")
    print("=" * 80)
    
    missing_files = find_missing_user_fields(root_directory)
    
    if not missing_files:
        print("✅ No files found with missing 'user' fields!")
        return

    # Extract sample video IDs for debugging
    sample_video_ids = [video_id for video_id, _, _, _, _ in missing_files]
    
    # Run debug check
    debug_sheet_detection(root_directory, sample_video_ids)
    
    print(f"❌ Found {len(missing_files)} files with missing 'user' fields:")
    print()
    
    # Group by task for detailed view
    by_task = {}
    for video_id, task, issue_type, file_path, sheet_name in missing_files:
        if task not in by_task:
            by_task[task] = []
        by_task[task].append((video_id, issue_type, file_path, sheet_name))
    
    print("DETAILED VIEW BY TASK:")
    print("-" * 40)
    for task, files in sorted(by_task.items()):
        print(f"\nTask: {task}")
        print("~" * 30)
        for video_id, issue_type, file_path, sheet_name in sorted(files):
            print(f"  {video_id} | {sheet_name} | {issue_type}")
            print(f"    File: {file_path}")
    
    # Print deletion-ready summary
    print_summary_for_deletion(missing_files)

if __name__ == "__main__":
    main()