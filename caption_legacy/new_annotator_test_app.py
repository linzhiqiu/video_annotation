import argparse
import streamlit as st
from feedback_app import main, caption_programs

def convert_name_to_username(full_name):
    """Convert a full name to a username format (e.g., 'Siyuan Cen' to 'siyuan_cen')"""
    return full_name.lower().replace(" ", "_")

def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=["video_urls/new_annotator_exam/exam.json"],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--main_project_output", type=str, default="output_captions", help="Path to the main project output directory")
    parser.add_argument("--output", type=str, default="output_new_annotator", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--show_feedback_prompt", type=bool, default=False, help="Whether to show and allow the annotator to edit the feedback prompt")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    parser.add_argument("--diff_prompt", type=str, default="prompts/diff_prompt.txt", help="Path to the diff prompt file")
    parser.add_argument("--diff_cap_prompt", type=str, default="prompts/diff_cap_prompt.txt", help="Path to the caption diff prompt file")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--personalize_output", type=bool, default=True, help="Whether to personalize the output directory based on the logged-in user")
    return parser.parse_args()

def new_annotator_main():
    args = parse_args()
    main(args, caption_programs)

if __name__ == "__main__":
    new_annotator_main()
