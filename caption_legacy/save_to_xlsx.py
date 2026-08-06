import os
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import functions from existing modules
from feedback_app import (
    load_config, load_json, get_video_id, 
    load_data, get_filename
)

# Use functions from paste_2.py for Excel operations
from load_xlsx import (
    load_captions_from_xlsx, get_caption_dict_by_filename,
    extract_filename, format_excel_file
)


def count_and_collect_captions(args):
    """Count completed videos and collect captions into a consolidated Excel file."""
    # Get the directory where this script is located
    folder = Path(__file__).parent
    
    # Load configs
    configs = load_config(folder / args.configs)
    configs = [load_config(folder / config) for config in configs]
    config_dict = {config["name"]: config for config in configs}
    
    # Map tasks to their output directory names
    task_to_output_dir = {config["task"]: config["output_name"] for config in configs}
    
    # Define our caption program tasks - these should match the keys in caption_programs from feedback_app.py
    caption_task_names = {
        "subject_description": "Subject Description",
        "scene_composition_dynamics": "Scene Composition and Dynamics",
        "subject_motion_dynamics": "Subject Motion and Dynamics",
        "spatial_framing_dynamics": "Spatial Framing and Dynamics",
        "camera_framing_dynamics": "Camera Framing and Dynamics",
    }
    
    # Load Adobe Excel data
    adobe_captions_data = []
    for excel_file in args.adobe_excel_files:
        adobe_captions_data.extend(load_captions_from_xlsx(excel_file))
    
    # Get first Excel file to extract its structure
    template_df = pd.read_excel(args.adobe_excel_files[0], engine='openpyxl')
    adobe_columns = list(template_df.columns)
    
    # Define new columns for our captions
    new_columns = [
        "Subject Description",
        "Scene Composition and Dynamics",
        "Subject Motion and Dynamics",
        "Spatial Framing and Dynamics",
        "Camera Framing and Dynamics"
    ]
    
    # Create DataFrame with combined columns
    all_columns = adobe_columns + new_columns
    result_df = pd.DataFrame(columns=all_columns)
    
    # Track statistics
    total_videos = 0
    completed_videos = 0
    task_completion = {task: 0 for task in caption_task_names.keys()}
    
    # Process each video URLs file
    for urls_file in args.video_urls_files:
        file_path = folder / urls_file
        print(f"\nProcessing videos from {urls_file}...")
        
        # Load video URLs
        video_urls = load_json(file_path)
        file_total = len(video_urls)
        file_completed = 0
        
        for video_url in video_urls:
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
                feedback_filename = get_filename(video_id, output_dir=output_dir, file_postfix="_feedback.json")
                
                if os.path.exists(feedback_filename):
                    task_completion[task] += 1
                    
                    # Load feedback data using the existing function
                    feedback_data = load_data(video_id, output_dir=output_dir, file_postfix="_feedback.json")
                    if feedback_data and "final_caption" in feedback_data:
                        video_captions[task_name] = feedback_data["final_caption"]
                    else:
                        all_tasks_completed = False
                else:
                    all_tasks_completed = False
            
            if all_tasks_completed:
                file_completed += 1
                completed_videos += 1
                
                # Get Adobe caption data for this video
                adobe_caption = get_caption_dict_by_filename(adobe_captions_data, video_id)
                
                # Create row data combining Adobe data with our captions
                row_data = {}
                
                # Add Adobe data if available
                if adobe_caption:
                    # Map the caption fields to the original column names
                    for col in adobe_columns:
                        col_lower = col.lower()
                        if 'content_id' in col_lower and 'content_id' in adobe_caption:
                            row_data[col] = adobe_caption['content_id']
                        elif 'stock_url' in col_lower and 'stock_url' in adobe_caption:
                            row_data[col] = adobe_caption['stock_url']
                        elif ('summary' in col_lower or 'what is the video about' in col_lower) and 'summary_caption' in adobe_caption:
                            row_data[col] = adobe_caption['summary_caption']
                        elif (('subject' in col_lower and 'background' in col_lower) or 'who or what is in the image' in col_lower) and 'subject_background_caption' in adobe_caption:
                            row_data[col] = adobe_caption['subject_background_caption']
                        elif (('subject' in col_lower and 'action' in col_lower) or 'what are they doing' in col_lower) and 'subject_motion_caption' in adobe_caption:
                            row_data[col] = adobe_caption['subject_motion_caption']
                        elif ('camera' in col_lower or 'how is it captured' in col_lower) and 'camera_caption' in adobe_caption:
                            row_data[col] = adobe_caption['camera_caption']
                else:
                    # If no Adobe data, use empty values but ensure stock_url is set
                    for col in adobe_columns:
                        row_data[col] = video_url if 'stock_url' in col.lower() else ""
                
                # Add our captions
                for task_name, caption in video_captions.items():
                    row_data[task_name] = caption
                
                # Add to DataFrame
                result_df = pd.concat([result_df, pd.DataFrame([row_data])], ignore_index=True)
        
        print(f"File: {Path(urls_file).name}, Total Videos: {file_total}, Completed: {file_completed} ({file_completed/file_total*100:.2f}%)")
    
    # Print overall statistics
    print(f"\nOverall Statistics:")
    print(f"Total Videos: {total_videos}")
    print(f"Fully Completed Videos: {completed_videos} ({completed_videos/total_videos*100:.2f}%)")
    print("\nTask Completion:")
    for task, count in task_completion.items():
        print(f"  {caption_task_names[task]}: {count}/{total_videos} ({count/total_videos*100:.2f}%)")
    
    # Save to Excel
    os.makedirs(os.path.dirname(args.output_excel), exist_ok=True)
    result_df.to_excel(args.output_excel, index=False, engine='openpyxl')
    
    # Format Excel file
    format_excel_file(result_df, args.output_excel)
    
    print(f"\nResults saved to {args.output_excel}")


def main():
    # Create an ArgumentParser instance
    parser = argparse.ArgumentParser(description="Video Caption Collection System")
    
    # Add arguments from feedback_app's parser
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=[
            "video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json",
            "video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json",
            "video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json",
            "video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json",
            "video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json",
            "video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json",
            "video_urls/20250227_0507ground_and_setup/overlap_564_to_658.json",
            "video_urls/20250227_0507ground_and_setup/overlap_658_to_752.json",
            "video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json",
            "video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json",
        ],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    
    # Add our additional arguments
    parser.add_argument("--adobe_excel_files", nargs="+", type=str, default=["adobe_2_19.xlsx", "adobe_2_17.xlsx"], 
                        help="List of Adobe Excel files")
    parser.add_argument("--output_excel", type=str, default="caption/output_caption_xlsx/caption_collection_random_april_9.xlsx", 
                        help="Path to the output Excel file")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Run the caption collection process
    count_and_collect_captions(args)


if __name__ == "__main__":
    main()