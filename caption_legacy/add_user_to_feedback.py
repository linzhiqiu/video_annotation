import os
import json
import argparse
from pathlib import Path
from feedback_app import load_json, get_video_id, get_filename, FEEDBACK_FILE_POSTFIX

# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Mapping of video URLs files to annotators
ANNOTATOR_MAPPING = {
    # "video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json": "Yuhan Huang",
    # "video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json": "Siyuan Cen",
    # "video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json": "Irene Pi",
    # "video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json": "Zhiqiu Lin",
    # "video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json": "Hewei Wang",
    # "video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json": "Sunny Guo",
    # "video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json": "Yuhan Huang",
    # "video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json": "Yuhan Huang",
    # "video_urls/20250406_setup_and_motion/overlap_940_to_950.json": "Mingyu Wang",
    # "video_urls/20250406_setup_and_motion/overlap_950_to_960.json": "Mingyu Wang",
}

# ANNOTATOR_MAPPING = {
#     "video_urls/lighting_120_new/batch1.json": "Tiffany Ling",
#     "video_urls/lighting_120_new/batch2.json": "Xianya Dai",
#     "video_urls/lighting_120_new/batch3.json": "Yubo Wang",
#     "video_urls/lighting_120_new/batch4.json": "Zida Zhou",
#     "video_urls/lighting_120_new/batch10.json": "Zhiqiu Lin",
# }

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Add user information to feedback files")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    # parser.add_argument("--configs", type=str, default="lighting_configs.json", help="Path to the JSON config file")
    parser.add_argument("--dry_run", action="store_true", default=False, help="Only print what would be done without making changes")
    return parser.parse_args()

def load_config(config_file):
    """Load configuration from JSON file"""
    with open(FOLDER / config_file, 'r') as f:
        return json.load(f)

def add_user_to_feedback_files(args, dry_run=False):
    """Add user information to feedback files based on video URLs file"""
    # Load configurations
    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        print(f"Config file not found: {args.configs}")
        return
    
    # Process each annotator's video URLs file
    for urls_file, annotator in ANNOTATOR_MAPPING.items():
        print(f"\nProcessing videos for {annotator} from {urls_file}")
        
        # Load video URLs
        try:
            video_urls = load_json(FOLDER / urls_file)
        except FileNotFoundError:
            print(f"Video URLs file not found: {urls_file}")
            continue
        
        # Process each configuration
        for config in configs:
            config_name = config["name"]
            output_dir = os.path.join(FOLDER, args.output, config["output_name"])
            
            if not os.path.exists(output_dir):
                print(f"Output directory not found: {output_dir}")
                continue
            
            print(f"  Processing {config_name}...")
            
            # Process each video in the URLs file
            for video_url in video_urls:
                video_id = get_video_id(video_url)
                feedback_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
                
                if not os.path.exists(feedback_file):
                    print(f"    Skipping {video_id}: Feedback file not found")
                    continue
                
                # Load the feedback data
                with open(feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                
                # Check if user is already set
                if "user" in feedback_data and feedback_data["user"]:
                    print(f"    Skipping {video_id}: User already set to {feedback_data['user']}")
                    continue
                
                # Add user information
                print(f"    Adding user '{annotator}' to {video_id}")
                
                if not dry_run:
                    feedback_data["user"] = annotator
                    with open(feedback_file, 'w') as f:
                        json.dump(feedback_data, f, indent=4)
    
    if dry_run:
        print("\nThis was a dry run. No changes were made to the files.")
    else:
        print("\nUser information has been added to all feedback files.")

def main():
    args = parse_args()
    add_user_to_feedback_files(args, args.dry_run)

if __name__ == "__main__":
    main() 