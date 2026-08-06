"""
Unified Save to XLSX Script

This script collects completed video captions and exports them to Excel format.

Task Status Definitions:
- not_completed: No feedback file exists yet
- completed_not_reviewed: Feedback exists, but no reviewer has evaluated it yet  
- approved: Reviewer evaluated and approved the caption (reviewer_double_check: true)
- rejected: Reviewer evaluated and rejected the caption, providing improvements (reviewer_double_check: false)

Filtering Logic:
- Default: Includes all completed videos (with any status except not_completed)
- --skip_without_adobe: Excludes videos without matching Adobe caption data
- --only_reviewed: Only includes videos where ALL 5 tasks have been reviewed (approved OR rejected)

Review Status Column:
Shows detailed status with user information:
- "All Approved - Annotator: X, Reviewer: Y"
- "All Rejected - Annotator: X, Reviewer: Y"  
- "Mixed Review (3 Approved, 2 Rejected) - Annotators: X, Reviewers: Y"
- "Partially Reviewed (2/5) - Annotators: X, Reviewers: Y"
- "Not Reviewed - Annotator: X"
"""

import os
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# Import functions from the new modular structure
from caption.config import get_config
from caption.core.data_manager import DataManager

# Use functions from load_xlsx for Excel operations
from caption.load_xlsx import (
    load_captions_from_xlsx,
    get_caption_dict_by_filename,
    extract_filename,
    format_excel_file,
)


def get_task_status_and_users_old(video_id, task, task_to_output_dir, folder, app_config, data_manager):
    """OLD method: Manual file checking (for comparison)"""
    output_name = task_to_output_dir.get(task)
    if not output_name:
        return 'not_completed', None, None, False
    
    output_dir = folder / app_config.output_dir / output_name
    
    # Check file existence
    feedback_file = data_manager.get_filename(video_id, output_dir=output_dir, file_postfix="_feedback.json")
    prev_feedback_file = data_manager.get_filename(video_id, output_dir=output_dir, file_postfix="_feedback_prev.json")
    review_file = data_manager.get_filename(video_id, output_dir=output_dir, file_postfix="_review.json")
    
    # Case 1: No feedback file exists
    if not os.path.exists(feedback_file):
        return 'not_completed', None, None, False
    
    # Case 2: Feedback exists but no review file
    if not os.path.exists(review_file):
        try:
            feedback_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_feedback.json")
            annotator_name = feedback_data.get("user", "Unknown")
            return 'completed_not_reviewed', annotator_name, None, False
        except Exception:
            return 'completed_not_reviewed', "Unknown", None, False
    
    # Case 3 & 4: Review file exists, check approval status
    try:
        review_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_review.json")
        reviewer_double_check = review_data.get("reviewer_double_check", False)
        reviewer_name = review_data.get("reviewer_name", "Unknown")
        
        if reviewer_double_check:
            # Case 3: Approved - annotator is in feedback file, reviewer is in review file
            try:
                feedback_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_feedback.json")
                annotator_name = feedback_data.get("user", "Unknown")
                return 'approved', annotator_name, reviewer_name, True
            except Exception:
                return 'approved', "Unknown", reviewer_name, True
        else:
            # Case 4: Rejected - annotator is in prev feedback, reviewer is in current feedback
            annotator_name = "Unknown"
            if os.path.exists(prev_feedback_file):
                try:
                    prev_feedback_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_feedback_prev.json")
                    annotator_name = prev_feedback_data.get("user", "Unknown")
                except Exception:
                    pass
            return 'rejected', annotator_name, reviewer_name, True
    
    except Exception:
        return 'completed_not_reviewed', "Unknown", None, False


def get_task_status_and_users(video_id, task, task_to_output_dir, folder, app_config, data_manager):
    """NEW method: Using data_manager.get_video_status() (like export.py)"""
    output_name = task_to_output_dir.get(task)
    if not output_name:
        return 'not_completed', None, None, False, None
    
    output_dir = folder / app_config.output_dir / output_name
    
    # Use the same logic as export.py - call data_manager.get_video_status()
    try:
        status, current_file, prev_file, current_user, prev_user = data_manager.get_video_status(video_id, output_dir)
        
        # Check for edge cases like export.py does
        edge_case_info = None
        if status == "rejected":
            # Check for "rejected but not improved" edge case
            review_file = data_manager.get_filename(video_id, output_dir, "_review.json")
            if os.path.exists(review_file) and current_file and prev_file:
                try:
                    with open(current_file, 'r') as f:
                        current_data = json.load(f)
                    with open(prev_file, 'r') as f:
                        prev_data = json.load(f)
                    with open(review_file, 'r') as f:
                        review_data = json.load(f)
                    
                    current_user_check = current_data.get("user")
                    prev_user_check = prev_data.get("user")
                    reviewer = review_data.get("reviewer_name", "Unknown")
                    
                    if current_user_check == prev_user_check:
                        edge_case_info = f"Caption rejected by {reviewer} but annotator {current_user_check} hasn't provided improved version yet"
                        
                except Exception as e:
                    edge_case_info = f"Error analyzing rejected status: {e}"
        
        # Determine annotator and reviewer names based on status
        annotator_name = None
        reviewer_name = None
        is_reviewed = False
        
        if status == "not_completed":
            # No files exist yet
            pass
        elif status == "completed_not_reviewed":
            # Only feedback file exists, user in that file is the annotator
            annotator_name = current_user
        elif status == "approved":
            # Feedback + review files exist, reviewer approved annotator's work
            annotator_name = current_user
            # Get reviewer name from review file
            try:
                review_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_review.json")
                reviewer_name = review_data.get("reviewer_name", "Unknown")
            except Exception:
                reviewer_name = "Unknown"
            is_reviewed = True
        elif status == "rejected":
            # Feedback + prev_feedback + review files exist
            # Annotator is in prev_feedback, reviewer is in current feedback
            annotator_name = prev_user if prev_user else "Unknown"
            try:
                review_data = data_manager.load_data(video_id, output_dir=output_dir, file_postfix="_review.json")
                reviewer_name = review_data.get("reviewer_name", "Unknown")
            except Exception:
                reviewer_name = "Unknown"
            is_reviewed = True
        
        return status, annotator_name, reviewer_name, is_reviewed, edge_case_info
        
    except Exception as e:
        # Fallback to not_completed if there's any error
        edge_case_info = f"Error in status detection: {e}"
        return 'not_completed', None, None, False, edge_case_info
    """Convert a HuggingFace dataset resolve URL to a web viewable URL."""
    # Example input: https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/ce8071e2668c089f109b31ffaf1ca7a29a277bb87f6b5c4770dadf6d1fd3c5e7.1.mp4
    # Example output: https://huggingface.co/datasets/zhiqiulin/video_captioning/blob/main/ce8071e2668c089f109b31ffaf1ca7a29a277bb87f6b5c4770dadf6d1fd3c5e7.1.mp4

    # Check if it's a HuggingFace URL
    if "huggingface.co/datasets" in url:
        # Replace 'resolve' with 'blob' to make it web viewable
        return url.replace("/resolve/", "/blob/")
    return url


def get_caption_task_names(config_type: str) -> Dict[str, str]:
    """Get the appropriate caption task names based on config type."""
    if config_type == "lighting":
        return {
            "raw_color_composition_dynamics": "Color Composition",
            "raw_lighting_setup_dynamics": "Lighting Setup", 
            "raw_lighting_effects_dynamics": "Lighting Effects",
        }
    else:  # main project
        return {
            "subject_description": "Subject Description",
            "scene_composition_dynamics": "Scene Composition and Dynamics",
            "subject_motion_dynamics": "Subject Motion and Dynamics",
            "spatial_framing_dynamics": "Spatial Framing and Dynamics",
            "camera_framing_dynamics": "Camera Framing and Dynamics",
        }


def get_default_output_excel(config_type: str) -> str:
    """Get the default output Excel filename based on config type."""
    if config_type == "lighting":
        return "caption/output_caption_xlsx/lighting_caption_collection.xlsx"
    else:
        return "caption/output_caption_xlsx/main_caption_collection.xlsx"


def count_and_collect_captions(args):
    """Count completed videos and collect captions into a consolidated Excel file."""
    # Get the directory where this script is located
    folder = Path(__file__).parent
    
    # Initialize data manager
    data_manager = DataManager(folder, folder.parent)
    
    # Get config using new system
    app_config = get_config(args.config_type)
    
    # Load configs using new system
    configs = data_manager.load_config(app_config.configs_file)
    configs = [data_manager.load_config(config) for config in configs]
    config_dict = {config["name"]: config for config in configs}
    
    # Map tasks to their output directory names
    task_to_output_dir = {config["task"]: config["output_name"] for config in configs}
    
    # Get caption task names based on config type
    caption_task_names = get_caption_task_names(args.config_type)
    
    # Load Adobe Excel data
    adobe_captions_data = []
    for excel_file in args.adobe_excel_files:
        adobe_captions_data.extend(load_captions_from_xlsx(excel_file))
    
    print(f"\nLoaded {len(adobe_captions_data)} Adobe caption records from {len(args.adobe_excel_files)} files")
    
    # Get first Excel file to extract its structure
    template_df = pd.read_excel(args.adobe_excel_files[0], engine='openpyxl')
    adobe_columns = list(template_df.columns)
    
    # Define new columns for our captions
    new_columns = list(caption_task_names.values())
    
    # Add review status column
    new_columns.append("Review Status")
    
    # Create DataFrame with combined columns
    all_columns = adobe_columns + new_columns
    result_df = pd.DataFrame(columns=all_columns)
    
    # Track statistics
    total_videos = 0
    completed_videos = 0
    skipped_videos = 0
    no_adobe_count = 0
    processed_videos = 0  # Videos that were actually processed (not skipped)
    reviewed_videos = 0  # Videos that have all tasks reviewed (approved)
    edge_case_videos = 0  # Videos with edge cases detected
    task_completion = {task: 0 for task in caption_task_names.keys()}
    task_reviewed = {task: 0 for task in caption_task_names.keys()}
    edge_case_details = []  # Track specific edge cases
    method_differences = []  # Track differences between old and new methods
    
    # Use video URLs from config if not overridden
    video_urls_files = args.video_urls_files or app_config.video_urls_files
    
    # Process each video URLs file
    for urls_file in video_urls_files:
        file_path = folder / urls_file
        print(f"\nProcessing videos from {urls_file}...")
        
        # Load video URLs using data manager
        video_urls = data_manager.load_json(urls_file)
        file_total = len(video_urls)
        file_completed = 0
        file_skipped = 0
        file_no_adobe = 0
        file_processed = 0
        file_reviewed = 0
        
        for video_url in video_urls:
            video_id = data_manager.get_video_id(video_url)
            total_videos += 1
            
            # Get Adobe caption data for this video first to check if we should skip
            adobe_caption = get_caption_dict_by_filename(
                adobe_captions_data, video_id
            )
            
            # Skip if no Adobe data and skip_without_adobe is set
            if not adobe_caption and args.skip_without_adobe:
                skipped_videos += 1
                file_skipped += 1
                continue
            
            # This video will be processed, so count it
            processed_videos += 1
            file_processed += 1
            
            # Track videos without Adobe data
            if not adobe_caption:
                no_adobe_count += 1
                file_no_adobe += 1
            
            # Check if all tasks are completed for this video
            all_tasks_completed = True
            all_tasks_reviewed = True  # True if all tasks are either approved OR rejected
            video_captions = {}
            task_statuses = {}  # Track status for each task
            
            for task, task_name in caption_task_names.items():
                # Get status using BOTH methods for comparison (but quietly)
                status_old, annotator_old, reviewer_old, is_reviewed_old = get_task_status_and_users_old(
                    video_id, task, task_to_output_dir, folder, app_config, data_manager
                )
                status_new, annotator_new, reviewer_new, is_reviewed_new, edge_case_info = get_task_status_and_users(
                    video_id, task, task_to_output_dir, folder, app_config, data_manager
                )
                
                # Check for differences between old and new methods (but don't print immediately)
                if (status_old != status_new or is_reviewed_old != is_reviewed_new):
                    difference_info = {
                        'video_id': video_id,
                        'task': task,
                        'old_status': status_old,
                        'new_status': status_new,
                        'old_reviewed': is_reviewed_old,
                        'new_reviewed': is_reviewed_new,
                        'edge_case': edge_case_info
                    }
                    method_differences.append(difference_info)
                
                # Use the NEW method results for actual processing
                status, annotator, reviewer, is_reviewed = status_new, annotator_new, reviewer_new, is_reviewed_new
                
                # Track edge cases
                if edge_case_info:
                    edge_case_details.append({
                        'video_id': video_id,
                        'task': task,
                        'issue': edge_case_info
                    })
                
                task_statuses[task] = {
                    'status': status,
                    'annotator': annotator,
                    'reviewer': reviewer,
                    'is_reviewed': is_reviewed,
                    'edge_case': edge_case_info
                }
                
                # Update completion tracking
                if status == 'not_completed':
                    all_tasks_completed = False
                    all_tasks_reviewed = False
                else:
                    # Count as completed if any feedback exists
                    task_completion[task] += 1
                    
                    # Count as reviewed if approved or rejected
                    if is_reviewed:
                        task_reviewed[task] += 1
                    else:
                        all_tasks_reviewed = False
                    
                    # Load caption data for completed tasks
                    if status in ['completed_not_reviewed', 'approved', 'rejected']:
                        output_name = task_to_output_dir.get(task)
                        output_dir = folder / app_config.output_dir / output_name
                        try:
                            feedback_data = data_manager.load_data(
                                video_id, output_dir=output_dir, file_postfix="_feedback.json"
                            )
                            if feedback_data and "final_caption" in feedback_data:
                                video_captions[task_name] = feedback_data["final_caption"]
                            else:
                                all_tasks_completed = False
                        except Exception:
                            all_tasks_completed = False
            
            # Check if video has edge cases that should exclude it
            video_has_edge_cases = any(info['edge_case'] for info in task_statuses.values())
            if video_has_edge_cases:
                edge_case_videos += 1
            
            if all_tasks_completed:
                # Generate detailed review status with user information
                if all_tasks_reviewed:
                    # All tasks have been reviewed (approved or rejected)
                    status_counts = {}
                    all_annotators = set()
                    all_reviewers = set()
                    
                    for task_info in task_statuses.values():
                        status = task_info['status']
                        status_counts[status] = status_counts.get(status, 0) + 1
                        if task_info['annotator']:
                            all_annotators.add(task_info['annotator'])
                        if task_info['reviewer']:
                            all_reviewers.add(task_info['reviewer'])
                    
                    # Create detailed status description
                    if len(status_counts) == 1 and 'approved' in status_counts:
                        review_status = f"All Approved - Annotator: {', '.join(all_annotators)}, Reviewer: {', '.join(all_reviewers)}"
                    elif len(status_counts) == 1 and 'rejected' in status_counts:
                        review_status = f"All Rejected - Annotator: {', '.join(all_annotators)}, Reviewer: {', '.join(all_reviewers)}"
                    else:
                        # Mixed approved/rejected
                        approved_count = status_counts.get('approved', 0)
                        rejected_count = status_counts.get('rejected', 0)
                        review_status = f"Mixed Review ({approved_count} Approved, {rejected_count} Rejected) - Annotators: {', '.join(all_annotators)}, Reviewers: {', '.join(all_reviewers)}"
                    
                    reviewed_videos += 1
                    file_reviewed += 1
                else:
                    # Some tasks not reviewed yet
                    reviewed_count = sum(1 for task_info in task_statuses.values() if task_info['is_reviewed'])
                    not_reviewed_count = len(caption_task_names) - reviewed_count
                    
                    if reviewed_count == 0:
                        # No reviews yet, just show annotators
                        annotators = {task_info['annotator'] for task_info in task_statuses.values() 
                                    if task_info['annotator'] and task_info['status'] != 'not_completed'}
                        review_status = f"Not Reviewed - Annotator: {', '.join(annotators) if annotators else 'Unknown'}"
                    else:
                        # Partially reviewed
                        annotators = {task_info['annotator'] for task_info in task_statuses.values() 
                                    if task_info['annotator']}
                        reviewers = {task_info['reviewer'] for task_info in task_statuses.values() 
                                   if task_info['reviewer']}
                        review_status = f"Partially Reviewed ({reviewed_count}/{len(caption_task_names)}) - Annotators: {', '.join(annotators)}, Reviewers: {', '.join(reviewers) if reviewers else 'N/A'}"
                
                # Skip if only_reviewed is set and not all tasks are reviewed
                if args.only_reviewed and not all_tasks_reviewed:
                    continue
                
                file_completed += 1
                completed_videos += 1
                
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
                            # For lighting config, convert URLs to web viewable format
                            if args.config_type == "lighting":
                                row_data[col] = convert_to_huggingface_web_url(adobe_caption['stock_url'])
                            else:
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
                            row_data[col] = ""
                else:
                    # If no Adobe data, use video_url/video_id for stock_url and content_id
                    for col in adobe_columns:
                        if "stock_url" in col.lower():
                            # For lighting, convert to web viewable URL
                            if args.config_type == "lighting":
                                row_data[col] = convert_to_huggingface_web_url(video_url)
                            else:
                                row_data[col] = video_url
                        elif "content_id" in col.lower():
                            row_data[col] = video_id
                        else:
                            row_data[col] = ""
                
                # Add our captions
                for task_name, caption in video_captions.items():
                    row_data[task_name] = caption
                
                # Add review status
                row_data["Review Status"] = review_status
                
                # Add to DataFrame
                result_df = pd.concat([result_df, pd.DataFrame([row_data])], ignore_index=True)
        
        print(f"File: {Path(urls_file).name}, Total: {file_total}, Processed: {file_processed}, Completed: {file_completed}, Reviewed: {file_reviewed}, No Adobe: {file_no_adobe}, Skipped: {file_skipped}")
    
    # Print overall statistics
    print(f"\nOverall Statistics:")
    print(f"Total Videos: {total_videos}")
    if args.skip_without_adobe:
        print(f"Skipped Videos (no Adobe data): {skipped_videos}")
    if no_adobe_count > 0:
        print(f"Videos Without Adobe Data (included): {no_adobe_count}")
    
    valid_videos = total_videos - skipped_videos
    if valid_videos > 0:
        print(f"Fully Completed Videos: {completed_videos} ({completed_videos/valid_videos*100:.2f}% of processed)")
        print("\nTask Completion:")
        for task, count in task_completion.items():
            print(f"  {caption_task_names[task]}: {count}/{valid_videos} ({count/valid_videos*100:.2f}%)")
    
    # Save to Excel
    output_dir = os.path.dirname(args.output_excel)
    if output_dir:  # Only create directory if there's a directory component
        os.makedirs(output_dir, exist_ok=True)
    result_df.to_excel(args.output_excel, index=False, engine='openpyxl')
    
    # Format Excel file
    format_excel_file(result_df, args.output_excel)
    
    print(f"\nResults saved to {args.output_excel}")
    print(f"Total rows in Excel: {len(result_df)}")


def main():
    # Create an ArgumentParser instance
    parser = argparse.ArgumentParser(description="Unified Caption Collection System")
    
    # Add config type argument
    parser.add_argument(
        "--config-type", 
        type=str, 
        default="main", 
        choices=["main", "lighting"],
        help="Configuration type to use (main or lighting)"
    )
    
    # Add arguments (with defaults that will be set based on config type)
    parser.add_argument(
        "--video_urls_files",
        nargs="*",  # Use * to allow empty list, will fall back to config default
        type=str,
        help="List of paths to video URLs files (uses config default if not specified)"
    )
    
    parser.add_argument(
        "--adobe_excel_files",
        nargs="+",
        type=str,
        default=["adobe_2_19.xlsx", "adobe_2_17.xlsx"],
        help="List of Adobe Excel files"
    )
    
    parser.add_argument(
        "--output_excel",
        type=str,
        help="Path to the output Excel file (uses config-based default if not specified)"
    )
    
    parser.add_argument(
        "--skip_without_adobe",
        action="store_true",
        help="Skip videos that don't have an Adobe caption entry"
    )
    
    parser.add_argument(
        "--only_reviewed",
        action="store_true",
        help="Only include videos where all five tasks have been reviewed (approved OR rejected) by a reviewer"
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Set output_excel default based on config type if not provided
    if not args.output_excel:
        args.output_excel = get_default_output_excel(args.config_type)
    
    # Run the caption collection process
    count_and_collect_captions(args)


if __name__ == "__main__":
    main()