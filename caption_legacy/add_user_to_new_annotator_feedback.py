import os
import json
import argparse
from pathlib import Path
from feedback_app import load_json, get_video_id, get_filename, FEEDBACK_FILE_POSTFIX, convert_name_to_username

# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Mapping of video URLs files to annotators
ANNOTATOR_MAPPING = {
    "video_urls/new_annotator_exam/exam.json": ["Tina Xu", "Mingyu Wang", "Zhenye Luo", "Kaibo Yang"]
}

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Add user information to new annotator feedback files")
    parser.add_argument("--output", type=str, default="output_new_annotator", help="Path to the output directory")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument("--dry_run", action="store_true", default=False, help="Only print what would be done without making changes")
    parser.add_argument("--personalize_output", action="store_true", default=True, help="Whether to use personalized output directories")
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
    
    # Process each video URLs file and its associated annotators
    for urls_file, annotators in ANNOTATOR_MAPPING.items():
        print(f"\nProcessing videos from {urls_file}")
        
        # Load video URLs
        try:
            video_urls = load_json(FOLDER / urls_file)
        except FileNotFoundError:
            print(f"Video URLs file not found: {urls_file}")
            continue
        
        # Process each annotator
        for annotator in annotators:
            print(f"\nProcessing for annotator: {annotator}")
            
            # Determine the output directory based on personalization
            base_output = args.output
            if args.personalize_output:
                username = convert_name_to_username(annotator)
                personalized_output = f"{base_output}_{username}"
                print(f"Using personalized output directory: {personalized_output}")
            else:
                personalized_output = base_output
            
            # Process each configuration
            for config in configs:
                config_name = config["name"]
                output_dir = os.path.join(FOLDER, personalized_output, config["output_name"])
                
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