import json
import os
import argparse
import random
from pathlib import Path

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return []

def save_json_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_existing_videos(args):
    # Load all existing batch files
    existing_videos = set()
    
    # Function to load videos from a file
    def load_videos_from_file(file_path):
        print(f"Loading videos from {file_path}")
        return set(load_json_file(file_path))
    
    # Load videos from specified batch files if provided
    if args.batch_files:
        print(f"Loading {len(args.batch_files)} batch files")
        for batch_file in args.batch_files:
            # batch_file is now a full path
            existing_videos.update(load_videos_from_file(batch_file))
    
    # Load existing invalid videos if filename provided
    invalid_videos = set()
    if args.invalid_filename:
        # invalid_filename is now a full path
        if os.path.exists(args.invalid_filename):
            invalid_videos.update(load_json_file(args.invalid_filename))
    
    # Load existing overlap invalid videos if filename provided
    overlap_invalid_videos = set()
    if args.invalid_filename_overlap:
        # invalid_filename_overlap is now a full path
        if os.path.exists(args.invalid_filename_overlap):
            overlap_invalid_videos.update(load_json_file(args.invalid_filename_overlap))
    
    # Load existing nonoverlap invalid videos if filename provided
    nonoverlap_invalid_videos = set()
    if args.invalid_filename_nonoverlap:
        # invalid_filename_nonoverlap is now a full path
        if os.path.exists(args.invalid_filename_nonoverlap):
            nonoverlap_invalid_videos.update(load_json_file(args.invalid_filename_nonoverlap))
    
    # Get the last batch number or index from the filenames based on naming mode
    last_batch_or_index = 0
    
    # Process batch files if provided
    if args.batch_files:
        for batch_file in args.batch_files:
            try:
                # Extract just the filename for processing
                filename = os.path.basename(batch_file)
                
                if args.naming_mode == "batch":
                    # For batchX.json format
                    batch_num = int(filename.replace("batch", "").replace(".json", ""))
                    last_batch_or_index = max(last_batch_or_index, batch_num)
                else:
                    # For overlap_X_to_Y.json or nonoverlap_X_to_Y.json format
                    # Count URLs in this file
                    urls_in_file = len(load_json_file(batch_file))
                    
                    # Extract the end number from filename for verification
                    end_num = int(filename.split("_to_")[1].replace(".json", ""))
                    start_num = int(filename.split("_to_")[0].replace("overlap_", "").replace("nonoverlap_", ""))
                    
                    # Verify that the file contains the expected number of URLs
                    expected_urls = end_num - start_num
                    if urls_in_file != expected_urls:
                        print(f"Warning: File {filename} contains {urls_in_file} URLs but name suggests {expected_urls}")
                    
                    last_batch_or_index = max(last_batch_or_index, end_num)
            except (ValueError, IndexError) as e:
                print(f"Error processing file {batch_file}: {e}")
                continue
    
    return existing_videos, invalid_videos, overlap_invalid_videos, nonoverlap_invalid_videos, last_batch_or_index

def process_new_videos(args):
    # Load existing videos
    existing_videos, existing_invalid, existing_overlap_invalid, existing_nonoverlap_invalid, last_batch_or_index = get_existing_videos(args)
    
    # Load new videos
    new_video = load_json_file(os.path.join(args.new_dir, args.valid_filename))
    
    # Load and process invalid videos if filename provided
    new_invalid_videos = []
    new_invalid_path = None
    if args.invalid_filename:
        # Load invalid videos from the specified path
        invalid_videos = load_json_file(args.invalid_filename)
        new_invalid_videos = [v for v in invalid_videos if v not in existing_invalid]
        print(f"Found {len(new_invalid_videos)} new invalid videos")
        
        # Always save invalid videos to the new directory
        # Get just the filename without the path
        invalid_filename = os.path.basename(args.invalid_filename)
        
        # Save to the new directory with the same filename
        new_invalid_path = os.path.join(args.new_dir, invalid_filename)
        save_json_file(invalid_videos, new_invalid_path)
        print(f"Saved {len(invalid_videos)} invalid videos to {new_invalid_path}")
    
    # Load and process overlap invalid videos if filename provided
    new_overlap_invalid_videos = []
    new_overlap_invalid_path = None
    if args.invalid_filename_overlap:
        # Load overlap invalid videos from the specified path
        overlap_invalid_videos = load_json_file(args.invalid_filename_overlap)
        new_overlap_invalid_videos = [v for v in overlap_invalid_videos if v not in existing_overlap_invalid]
        print(f"Found {len(new_overlap_invalid_videos)} new overlap invalid videos")
        
        # Always save overlap invalid videos to the new directory
        # Get just the filename without the path
        overlap_invalid_filename = os.path.basename(args.invalid_filename_overlap)
        
        # Save to the new directory with the same filename
        new_overlap_invalid_path = os.path.join(args.new_dir, overlap_invalid_filename)
        save_json_file(overlap_invalid_videos, new_overlap_invalid_path)
        print(f"Saved {len(overlap_invalid_videos)} overlap invalid videos to {new_overlap_invalid_path}")
    
    # Load and process nonoverlap invalid videos if filename provided
    new_nonoverlap_invalid_videos = []
    new_nonoverlap_invalid_path = None
    if args.invalid_filename_nonoverlap:
        # Load nonoverlap invalid videos from the specified path
        nonoverlap_invalid_videos = load_json_file(args.invalid_filename_nonoverlap)
        new_nonoverlap_invalid_videos = [v for v in nonoverlap_invalid_videos if v not in existing_nonoverlap_invalid]
        print(f"Found {len(new_nonoverlap_invalid_videos)} new nonoverlap invalid videos")
        
        # Always save nonoverlap invalid videos to the new directory
        # Get just the filename without the path
        nonoverlap_invalid_filename = os.path.basename(args.invalid_filename_nonoverlap)
        
        # Save to the new directory with the same filename
        new_nonoverlap_invalid_path = os.path.join(args.new_dir, nonoverlap_invalid_filename)
        save_json_file(nonoverlap_invalid_videos, new_nonoverlap_invalid_path)
        print(f"Saved {len(nonoverlap_invalid_videos)} nonoverlap invalid videos to {new_nonoverlap_invalid_path}")
    
    # Find new videos that aren't in existing batches
    new_valid_videos = [v for v in new_video if v not in existing_videos]
    print(f"\nFound {len(new_valid_videos)} new valid videos")
    
    # Shuffle new valid videos if requested
    if args.shuffle:
        print("Shuffling new valid videos...")
        random.shuffle(new_valid_videos)
    
    # Create new batches
    created_files = []
    for i in range(0, len(new_valid_videos), args.batch_size):
        batch = new_valid_videos[i:i + args.batch_size]
        
        # Use appropriate naming convention based on mode
        if args.naming_mode == "batch":
            last_batch_or_index += 1
            batch_file = os.path.join(args.new_dir, f"batch{last_batch_or_index}.json")
        elif args.naming_mode == "overlap":
            # For overlap mode, calculate start and end indices continuing from last index
            start_idx = last_batch_or_index
            end_idx = start_idx + len(batch)
            last_batch_or_index = end_idx
            batch_file = os.path.join(args.new_dir, f"overlap_{start_idx}_to_{end_idx}.json")
        elif args.naming_mode == "nonoverlap":  # nonoverlap mode
            # For nonoverlap mode, calculate start and end indices continuing from last index
            start_idx = last_batch_or_index
            end_idx = start_idx + len(batch)
            last_batch_or_index = end_idx
            batch_file = os.path.join(args.new_dir, f"{start_idx}_to_{end_idx}.json")
        
        save_json_file(batch, batch_file)
        created_files.append(batch_file)
        print(f"Created {batch_file} with {len(batch)} videos")
    
    # Print reminder about updating video_urls_files
    print("\n" + "="*80)
    print("REMINDER: Don't forget to update video_urls_files in feedback_app.py or new_feedback_app.py")
    print("Add the following files to the list:")
    
    # Function to remove 'caption/' prefix from paths
    def clean_path(path):
        if path.startswith("caption/"):
            return path[8:]  # Remove 'caption/' prefix
        return path
    
    # Add invalid files first if they exist
    if new_invalid_path:
        print(f"    '{clean_path(new_invalid_path)}',")
    if new_overlap_invalid_path:
        print(f"    '{clean_path(new_overlap_invalid_path)}',")
    if new_nonoverlap_invalid_path:
        print(f"    '{clean_path(new_nonoverlap_invalid_path)}',")
    
    # Add batch files
    for file in created_files:
        print(f"    '{clean_path(file)}',")
    print("="*80)

def parse_args():
    parser = argparse.ArgumentParser(description="Process and distribute videos into batches")
    
    # Directory structure
    parser.add_argument("--new-dir", type=str, default="caption/video_urls/20250406_setup_and_motion",
                        help="Directory for new batch files")
    
    # File names
    parser.add_argument("--valid-filename", type=str, default="lighting_only.json",
                        help="Filename for valid videos")
    parser.add_argument("--invalid-filename", type=str, default=None,
                        help="Optional filename for invalid videos (full path)")
    parser.add_argument("--invalid-filename-overlap", type=str, default=None,
                        help="Optional filename for overlap invalid videos (full path)")
    parser.add_argument("--invalid-filename-nonoverlap", type=str, default=None,
                        help="Optional filename for nonoverlap invalid videos (full path)")
    
    # Batch files - make it optional
    parser.add_argument("--batch-files", nargs="*", type=str,
                        default=[],
                        help="Optional list of batch files to process (full paths)")
    
    # Batch configuration
    parser.add_argument("--batch-size", type=int, default=10,
                        help="Number of videos per batch")
    
    # Naming mode
    parser.add_argument("--naming-mode", type=str, choices=["batch", "overlap", "nonoverlap"], default="batch",
                        help="Naming convention for batch files: 'batch' for batchX.json, 'overlap' for overlap_X_to_Y.json, or 'nonoverlap' for nonoverlap_X_to_Y.json")
    
    # Shuffle option
    parser.add_argument("--shuffle", type=bool, default=True,
                        help="Whether to shuffle new valid videos before creating batches (default: True)")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    process_new_videos(args) 