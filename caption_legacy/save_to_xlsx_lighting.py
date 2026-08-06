import os
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# Import functions from existing modules
from feedback_app import load_config, load_json, get_video_id, load_data, get_filename

# Use functions from paste_2.py for Excel operations
from load_xlsx import (
    load_captions_from_xlsx,
    get_caption_dict_by_filename,
    extract_filename,
    format_excel_file,
)


def convert_to_huggingface_web_url(url):
    """Convert a HuggingFace dataset resolve URL to a web viewable URL."""
    # Example input: https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/ce8071e2668c089f109b31ffaf1ca7a29a277bb87f6b5c4770dadf6d1fd3c5e7.1.mp4
    # Example output: https://huggingface.co/datasets/zhiqiulin/video_captioning/blob/main/ce8071e2668c089f109b31ffaf1ca7a29a277bb87f6b5c4770dadf6d1fd3c5e7.1.mp4

    # Check if it's a HuggingFace URL
    if "huggingface.co/datasets" in url:
        # Replace 'resolve' with 'blob' to make it web viewable
        return url.replace("/resolve/", "/blob/")
    return url


def count_and_collect_lighting_captions(args):
    """Count completed videos and collect lighting captions into a consolidated Excel file."""
    # Get the directory where this script is located
    folder = Path(__file__).parent

    # Load configs
    configs = load_config(folder / args.configs)
    configs = [load_config(folder / config) for config in configs]
    config_dict = {config["name"]: config for config in configs}

    # Map tasks to their output directory names
    task_to_output_dir = {config["task"]: config["output_name"] for config in configs}

    # Define our lighting caption program tasks
    caption_task_names = {
        "raw_color_composition_dynamics": "Color Composition",
        "raw_lighting_setup_dynamics": "Lighting Setup",
        "raw_lighting_effects_dynamics": "Lighting Effects",
    }

    # Load Adobe Excel data
    adobe_captions_data = []
    for excel_file in args.adobe_excel_files:
        adobe_captions_data.extend(load_captions_from_xlsx(excel_file))

    # Get first Excel file to extract its structure
    template_df = pd.read_excel(args.adobe_excel_files[0], engine="openpyxl")
    adobe_columns = list(template_df.columns)

    # Define columns for our lighting captions
    new_columns = ["Color Composition", "Lighting Setup", "Lighting Effects"]

    # Create DataFrame with combined columns
    all_columns = adobe_columns + new_columns
    result_df = pd.DataFrame(columns=all_columns)

    # Track statistics
    total_videos = 0
    completed_videos = 0
    skipped_videos = 0
    no_adobe_count = 0
    task_completion = {task: 0 for task in caption_task_names.keys()}

    # Process each video URLs file
    for urls_file in args.video_urls_files:
        file_path = folder / urls_file
        print(f"\nProcessing videos from {urls_file}...")

        # Load video URLs
        video_urls = load_json(file_path)
        file_total = len(video_urls)
        file_completed = 0
        file_skipped = 0
        file_no_adobe = 0

        for video_url in video_urls:
            # Use the original get_video_id function from feedback_app
            video_id = get_video_id(video_url)
            total_videos += 1

            # Check if all tasks are completed for this video
            all_tasks_completed = True
            video_captions = {}

            for task, task_name in caption_task_names.items():
                output_name = task_to_output_dir.get(task)
                if not output_name:
                    print(f"WARNING: No output directory found for task {task}")
                    all_tasks_completed = False
                    continue

                # Check if feedback exists for this task
                output_dir = folder / args.output / output_name
                feedback_filename = get_filename(
                    video_id, output_dir=output_dir, file_postfix="_feedback.json"
                )

                if os.path.exists(feedback_filename):
                    task_completion[task] += 1

                    # Load feedback data
                    feedback_data = load_data(
                        video_id, output_dir=output_dir, file_postfix="_feedback.json"
                    )
                    if feedback_data and "final_caption" in feedback_data:
                        video_captions[task_name] = feedback_data["final_caption"]
                    else:
                        all_tasks_completed = False
                else:
                    all_tasks_completed = False

            if all_tasks_completed:
                # Get Adobe caption data for this video
                adobe_caption = get_caption_dict_by_filename(
                    adobe_captions_data, video_id
                )

                # Skip if no Adobe data and skip_without_adobe is set
                if not adobe_caption and args.skip_without_adobe:
                    print(f"Skipping video (no Adobe data): {video_id}")
                    skipped_videos += 1
                    file_skipped += 1
                    continue

                # Track videos without Adobe data
                if not adobe_caption:
                    no_adobe_count += 1
                    file_no_adobe += 1

                file_completed += 1
                completed_videos += 1

                # Create row data combining Adobe data with our captions
                row_data = {}

                # Add Adobe data if available
                if adobe_caption:
                    # Map the caption fields to the original column names
                    for col in adobe_columns:
                        col_lower = col.lower()
                        if "content_id" in col_lower and "content_id" in adobe_caption:
                            row_data[col] = adobe_caption["content_id"]
                        elif "stock_url" in col_lower and "stock_url" in adobe_caption:
                            row_data[col] = adobe_caption["stock_url"]
                        elif (
                            "summary" in col_lower
                            or "what is the video about" in col_lower
                        ) and "summary_caption" in adobe_caption:
                            row_data[col] = adobe_caption["summary_caption"]
                        elif (
                            ("subject" in col_lower and "background" in col_lower)
                            or "who or what is in the image" in col_lower
                        ) and "subject_background_caption" in adobe_caption:
                            row_data[col] = adobe_caption["subject_background_caption"]
                        elif (
                            ("subject" in col_lower and "action" in col_lower)
                            or "what are they doing" in col_lower
                        ) and "subject_motion_caption" in adobe_caption:
                            row_data[col] = adobe_caption["subject_motion_caption"]
                        elif (
                            "camera" in col_lower or "how is it captured" in col_lower
                        ) and "camera_caption" in adobe_caption:
                            row_data[col] = adobe_caption["camera_caption"]
                        else:
                            row_data[col] = ""  # Default empty value for other columns
                else:
                    # If no Adobe data, use empty values but create HuggingFace link for stock_url column
                    for col in adobe_columns:
                        if "stock_url" in col.lower():
                            # Convert to HuggingFace web viewable URL
                            row_data[col] = convert_to_huggingface_web_url(video_url)
                        elif "content_id" in col.lower():
                            # Use video_id for content_id field if available
                            row_data[col] = video_id
                        else:
                            row_data[col] = ""

                # Add our lighting captions
                for task_name, caption in video_captions.items():
                    row_data[task_name] = caption

                # Add to DataFrame
                result_df = pd.concat(
                    [result_df, pd.DataFrame([row_data])], ignore_index=True
                )

        print(
            f"File: {Path(urls_file).name}, Total: {file_total}, Completed: {file_completed}, No Adobe: {file_no_adobe}, Skipped: {file_skipped}"
        )

    # Print overall statistics
    print(f"\nOverall Statistics:")
    print(f"Total Videos: {total_videos}")
    print(f"Skipped Videos (no Adobe data): {skipped_videos}")
    print(f"Videos Without Adobe Data (included): {no_adobe_count}")
    valid_videos = total_videos - skipped_videos
    if valid_videos > 0:
        print(
            f"Fully Completed Videos: {completed_videos} ({completed_videos/valid_videos*100:.2f}% of non-skipped)"
        )
        print("\nTask Completion:")
        for task, count in task_completion.items():
            print(
                f"  {caption_task_names[task]}: {count}/{valid_videos} ({count/valid_videos*100:.2f}%)"
            )

    # Save to Excel
    os.makedirs(os.path.dirname(args.output_excel), exist_ok=True)
    result_df.to_excel(args.output_excel, index=False, engine="openpyxl")

    # Format Excel file
    format_excel_file(result_df, args.output_excel)

    print(f"\nResults saved to {args.output_excel}")
    print(f"Total rows in Excel: {len(result_df)}")


def main():
    # Create an ArgumentParser instance
    parser = argparse.ArgumentParser(description="Lighting Caption Collection System")

    # Add arguments from feedback_app's parser
    parser.add_argument(
        "--configs",
        type=str,
        default="lighting_configs.json",
        help="Path to the JSON config file",
    )
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=[
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
            "video_urls/lighting_120_new/invalid_videos.json",
        ],
        help="List of paths to lighting video URLs files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_captions",
        help="Path to the output directory",
    )
    parser.add_argument(
        "--video_data",
        type=str,
        default="video_data/20250328_1455_lighting_120/videos.json",
        help="Path to the video data file",
    )
    parser.add_argument(
        "--label_collections",
        nargs="+",
        type=str,
        default=["lighting_setup"],
        help="List of label collections to load from the video data",
    )

    # Add our additional arguments - using the same defaults as the original script
    parser.add_argument(
        "--adobe_excel_files",
        nargs="+",
        type=str,
        default=["adobe_2_19.xlsx", "adobe_2_17.xlsx"],
        help="List of Adobe Excel files",
    )
    parser.add_argument(
        "--output_excel",
        type=str,
        default="caption/output_caption_xlsx/lighting_caption_collection.xlsx",
        help="Path to the output Excel file",
    )
    parser.add_argument(
        "--skip_without_adobe",
        action="store_true",
        help="Skip videos that don't have an Adobe caption entry",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the caption collection process
    count_and_collect_lighting_captions(args)


if __name__ == "__main__":
    main()
