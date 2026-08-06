import os
import json
import argparse
from pathlib import Path
from feedback_app import (
    parse_args, load_video_data, get_video_id, load_json, get_filename,
    load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    load_config, config_names_to_short_names
)
from feedback_diff_app import calculate_accuracy_stats, get_video_status

def count_completed_captions(video_urls, output_dir, configs_path="all_configs.json"):
    """
    Count completed captions in the current project
    
    Args:
        video_urls: List of video URLs to check
        output_dir: Path to the output directory containing captions
        configs_path: Path to the JSON config file
    """
    # Load configs
    configs = load_config(FOLDER / configs_path)
    configs = [load_config(FOLDER / config) for config in configs]
    config_dict = {config["name"]: config for config in configs}
    
    # Calculate stats for each config
    all_stats = {}
    for config_name, config in config_dict.items():
        config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
        if not os.path.exists(config_output_dir):
            print(f"No output directory for {config_name}")
            continue
            
        stats = calculate_accuracy_stats(video_urls, config_output_dir)
        if not stats:
            print(f"No completed videos for {config_name}")
            continue
            
        all_stats[config_name] = stats
        
        print(f"\nStats for {config_name}:")
        total_completed = sum(data['total_completed'] for data in stats.values())
        total_reviewed = sum(data['total_reviewed'] for data in stats.values())
        total_approved = sum(data['approved'] for data in stats.values())
        total_rejected = sum(data['rejected'] for data in stats.values())
        
        print(f"Total videos: {len(video_urls)}")
        print(f"Total completed: {total_completed}")
        print(f"Total reviewed: {total_reviewed}")
        print(f"Total approved: {total_approved}")
        print(f"Total rejected: {total_rejected}")
        print("\nPer annotator stats:")
        for annotator, data in sorted(stats.items()):
            print(f"\n{annotator}:")
            print(f"  Completed: {data['total_completed']}")
            print(f"  Reviewed: {data['total_reviewed']}")
            print(f"  Approved: {data['approved']}")
            print(f"  Rejected: {data['rejected']}")
            if data['total_reviewed'] > 0:
                print(f"  Accuracy: {data['accuracy']:.1%}")
    
    return all_stats

# def extract_camera_motion_captions():
#     """Extract camera motion captions from CameraBench dataset"""
#     # Path to the training set
#     train_file = "/data3/zhiqiul/video_annotation/video_labels/motion_dataset/test_ratio_0.50_num_80_sampling_top/trainset.json"
    
#     # Load the training set
#     with open(train_file, 'r') as f:
#         train_data = json.load(f)
    
#     # Extract video IDs and camera motion captions
#     camera_motion_data = {}
#     for video_id, data in train_data.items():
#         if 'cam_motion' in data:
#             camera_motion_data[video_id] = data['cam_motion']
    
#     # Save to a new file
#     output_file = "camera_motion_captions.json"
#     with open(output_file, 'w') as f:
#         json.dump(camera_motion_data, f, indent=2)
    
#     print(f"Found {len(camera_motion_data)} videos with camera motion captions")
#     print(f"Saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Count completed captions")
    parser.add_argument("--video_urls_file", type=str, required=True,
                      help="Path to the video URLs file")
    parser.add_argument("--output", type=str, default="output_captions",
                      help="Path to the output directory")
    parser.add_argument("--configs", type=str, default="all_configs.json",
                      help="Path to the JSON config file")
    
    args = parser.parse_args()
    
    # Load video URLs
    video_urls = load_json(FOLDER / args.video_urls_file)
    
    # Count captions
    count_completed_captions(video_urls, args.output, args.configs)

if __name__ == "__main__":
    main() 