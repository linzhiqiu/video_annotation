import os
import json
from pathlib import Path
import argparse
from feedback_app import (
    parse_args, load_video_data, get_video_id, load_json, get_filename,
    load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    load_config
)
from count_captions import count_completed_captions
from feedback_diff_app import get_video_status

def merge_captions(input_json_path, output_dir, output_json_path, configs_path="all_configs.json", only_reviewed=False):
    """
    Merge captions from input JSON and saved captions directory.
    
    Args:
        input_json_path: Path to input JSON file containing video captions
        output_dir: Path to the output directory containing captions
        output_json_path: Path to save merged captions
        configs_path: Path to configs JSON file
        only_reviewed: If True, only include captions that have been reviewed (approved or rejected)
    """
    # Load input JSON to get video URLs
    input_data = load_json(input_json_path)
    video_urls = [data["video"] for data in input_data]
    
    # First get statistics using count_captions functionality
    stats = count_completed_captions(video_urls, output_dir, configs_path)
    
    # Load configs to get output directory names
    configs = load_config(FOLDER / configs_path)
    configs = [load_config(FOLDER / config) for config in configs]
    config_dict = {config["name"]: config for config in configs}
    
    # Map config names to caption types
    config_to_caption = {
        "Subject Description Caption": "subject",
        "Scene Composition and Dynamics Caption": "scene",
        "Subject Motion and Dynamics Caption": "motion",
        "Spatial Framing and Dynamics Caption": "spatial",
        "Camera Framing and Dynamics Caption": "camera"
    }
    
    # Process each video
    merged_data = []
    for video_data in input_data:
        video_id = get_video_id(video_data["video"])
        merged_entry = {
            "video": video_data["video"],
            "camerabench": video_data.get("answer", "")
        }
        
        # Check each config for captions
        for config_name, config in config_dict.items():
            caption_type = config_to_caption.get(config_name)
            if not caption_type:
                continue
                
            config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
            feedback_file = get_filename(video_id, output_dir=config_output_dir, file_postfix="_feedback.json")
            
            if os.path.exists(feedback_file):
                # Check review status if only_reviewed is set
                status, _, _, _, _ = get_video_status(video_id, config_output_dir)
                if only_reviewed and status not in ["approved", "rejected"]:
                    continue
                try:
                    feedback_data = load_data(video_id, output_dir=config_output_dir, file_postfix="_feedback.json")
                    if feedback_data and "final_caption" in feedback_data:
                        merged_entry[f"{caption_type}_caption"] = feedback_data["final_caption"]
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse {feedback_file}")
                except Exception as e:
                    print(f"Error processing {feedback_file}: {str(e)}")
        
        merged_data.append(merged_entry)
    
    # Save merged data
    save_json(merged_data, output_json_path)
    print(f"\nMerged captions saved to {output_json_path}")

def save_json(data, file_path):
    """Save data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Merge and count video captions")
    parser.add_argument("--input_json", type=str,
                          default="video_labels/motion_dataset/test_ratio_0.50_num_80_sampling_top/train_caption.json",
                        # default="video_labels/motion_dataset/test_ratio_0.50_num_80_sampling_top/test_caption.json",
                      help="Path to input JSON file containing video captions")
    parser.add_argument("--output", type=str, default="output_captions",
                      help="Path to the output directory containing captions")
    parser.add_argument("--output_json", type=str,
                      default="merged_captions_camerabench.json",
                    #   default="merged_captions_camerabench_test.json",
                      help="Path to save merged captions")
    parser.add_argument("--configs", type=str, default="all_configs.json",
                      help="Path to the configs JSON file")
    parser.add_argument("--only-reviewed", action="store_true", default=False,
                      help="If set, only include captions that have been reviewed (approved or rejected)")
    
    args = parser.parse_args()
    # Create output directory if it doesn't exist
    if len(os.path.dirname(args.output_json)) > 0:
        os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
    
    # Merge captions
    merge_captions(args.input_json, args.output, args.output_json, args.configs, args.only_reviewed)

if __name__ == "__main__":
    main() 