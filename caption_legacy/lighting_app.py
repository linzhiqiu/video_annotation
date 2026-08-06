# lighting_app.py
import argparse
from streamlit_feedback import streamlit_feedback
from caption_policy.prompt_generator import (
    SubjectPolicy,
    ScenePolicy,
    ColorPolicy,
    LightingSetupPolicy,
    LightingEffectsPolicy,
    ColorPolicy,
    LightingSetupPolicy,
    LightingEffectsPolicy,
)

def convert_name_to_username(full_name):
    """Convert a full name to a username format (e.g., 'Siyuan Cen' to 'siyuan_cen')"""
    return full_name.lower().replace(" ", "_")

def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System for Lighting")
    parser.add_argument("--configs", type=str, default="lighting_configs.json", help="Path to the JSON config file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_all.json", help="Path to the test URLs file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=[
            # "video_urls/lighting_120_new/all_labels.json",
            # "video_urls/lighting_120_new/lighting_only.json",
            "video_urls/lighting_120_new/batch1.json",
            "video_urls/lighting_120_new/batch2.json",
            "video_urls/lighting_120_new/batch3.json",
            "video_urls/lighting_120_new/batch4.json",
            "video_urls/lighting_120_new/batch5.json",
            "video_urls/lighting_120_new/batch6.json",
            "video_urls/lighting_120_new/batch7.json",
            "video_urls/lighting_120_new/batch8.json",
            "video_urls/lighting_120_new/batch9.json",
            "video_urls/lighting_120_new/batch10.json",
            "video_urls/lighting_250_new/batch11.json",
            "video_urls/lighting_250_new/batch12.json",
            "video_urls/lighting_250_new/batch13.json",
            "video_urls/lighting_250_new/batch14.json",
            "video_urls/lighting_250_new/batch15.json",
            "video_urls/lighting_250_new/batch16.json",
            "video_urls/lighting_250_new/batch17.json",
            "video_urls/lighting_250_new/batch18.json",
            "video_urls/lighting_250_new/batch19.json",
            "video_urls/lighting_250_new/batch20.json",
            'video_urls/lighting_280_new/batch21.json',
            'video_urls/lighting_280_new/batch22.json',
            'video_urls/lighting_280_new/batch23.json',
            # "video_urls/lighting_120_new/invalid_videos.json",
            # "video_urls/lighting_250_new/invalid_videos.json",
            'video_urls/lighting_280_new/invalid_videos.json',
        ],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--main_project_output", type=str, default="output_captions", help="Path to the main project output directory")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    parser.add_argument("--diff_prompt", type=str, default="prompts/diff_prompt.txt", help="Path to the diff prompt file")
    parser.add_argument("--diff_cap_prompt", type=str, default="prompts/diff_cap_prompt.txt", help="Path to the caption diff prompt file")
    parser.add_argument("--video_data", type=str, default="video_data/20250406lighting_only/videos.json", help="Path to the video data file")
    # parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup", "lighting_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["lighting_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--personalize_output", action="store_true", default=False, help="Whether to personalize the output directory based on the logged-in user")
    return parser.parse_args()

# Load configuration
args = parse_args()

caption_programs = {
    # "subject_description": SubjectPolicy(),
    # "scene_composition_dynamics": ScenePolicy(),
    # "color_composition_dynamics": ColorPolicy(),
    # "lighting_setup_dynamics": LightingSetupPolicy(),
    # "lighting_effects_dynamics": LightingEffectsPolicy(),
    "raw_color_composition_dynamics": ColorPolicy(),
    "raw_lighting_setup_dynamics": LightingSetupPolicy(),
    "raw_lighting_effects_dynamics": LightingEffectsPolicy(),
}

from feedback_app import main

if __name__ == "__main__":
    main(args, caption_programs)
