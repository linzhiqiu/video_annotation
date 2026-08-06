#!/usr/bin/env python3
"""
Clean Caption Export Script - caption/export.py

Exports video captions organized by meaningful completion levels.
No legacy status-based categorization - focuses on task-level analysis.
"""

import os
import json
import argparse
from dotenv import load_dotenv
from huggingface_hub import HfApi
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Import from NEW modular structure
from caption.config import get_config
from caption.core.data_manager import DataManager

load_dotenv()

class CaptionExportError(Exception):
    """Custom exception for caption export issues"""
    pass


# Configuration mapping - includes ALL caption types (main + lighting)
CONFIG_TO_CAPTION = {
    # Main project caption types
    "Subject Description Caption": "subject",
    "Scene Composition and Dynamics Caption": "scene",
    "Subject Motion and Dynamics Caption": "motion",
    "Spatial Framing and Dynamics Caption": "spatial",
    "Camera Framing and Dynamics Caption": "camera",
    
    # Lighting project caption types
    "Color Composition and Dynamics Caption (Raw)": "color",
    "Lighting Setup and Dynamics Caption (Raw)": "lighting",
    "Lighting Effects and Dynamics Caption (Raw)": "effects"
}


def determine_task_status(video_id, config_output_dir, data_manager):
    """
    Determine the precise status of a single caption task.
    
    Returns:
        str: One of "not_completed", "completed_not_reviewed", "approved", "rejected"
        str: Error message if edge case detected, None otherwise
    """
    status, current_file, prev_file, current_user, prev_user = data_manager.get_video_status(video_id, config_output_dir)
    
    if status == "not_completed":
        return "not_completed", None
    elif status == "completed_not_reviewed":
        return "completed_not_reviewed", None
    elif status == "approved":
        return "approved", None
    elif status == "rejected":
        # Check for edge case: rejected but not improved yet
        review_file = data_manager.get_filename(video_id, config_output_dir, data_manager.REVIEWER_FILE_POSTFIX)
        if os.path.exists(review_file) and current_file and prev_file:
            try:
                with open(current_file, 'r') as f:
                    current_data = json.load(f)
                with open(prev_file, 'r') as f:
                    prev_data = json.load(f)
                with open(review_file, 'r') as f:
                    review_data = json.load(f)
                
                current_user = current_data.get("user")
                prev_user = prev_data.get("user")
                reviewer = review_data.get("reviewer_name", "Unknown")
                
                if current_user == prev_user:
                    error_msg = (f"Caption rejected by {reviewer} but annotator {current_user} "
                               f"hasn't provided improved version yet")
                    return "rejected_not_improved", error_msg
                    
            except Exception:
                pass
                
        return "rejected", None
    
    return "unknown", f"Unknown status: {status}"


def extract_complete_workflow_data(feedback_data):
    """
    Extract complete workflow data from feedback file.
    Preserves ALL important fields organized by workflow stages.
    """
    if not feedback_data:
        return {}
    
    # Determine workflow type
    initial_rating = feedback_data.get("initial_caption_rating_score")
    workflow_type = "perfect_precaption" if initial_rating == 5 else "improved_precaption"
    
    return {
        # Metadata
        "user": feedback_data.get("user", ""),
        "timestamp": feedback_data.get("timestamp", ""),
        "workflow_type": workflow_type,
        
        # Pre-caption stage (ALWAYS present)
        "pre_caption": feedback_data.get("pre_caption", ""),
        "pre_caption_prompt": feedback_data.get("pre_caption_prompt", ""),
        "pre_caption_llm": feedback_data.get("pre_caption_llm", ""),
        "pre_caption_mode": feedback_data.get("pre_caption_mode", ""),
        "initial_caption_rating_score": feedback_data.get("initial_caption_rating_score"),
        "feedback_is_needed": feedback_data.get("feedback_is_needed"),
        
        # Feedback and final caption stage (includes everything after pre-caption)
        "initial_feedback": feedback_data.get("initial_feedback", ""),
        "gpt_feedback": feedback_data.get("gpt_feedback", ""),
        "gpt_feedback_llm": feedback_data.get("gpt_feedback_llm", ""),
        "gpt_feedback_prompt": feedback_data.get("gpt_feedback_prompt", ""),
        "feedback_rating_score": feedback_data.get("feedback_rating_score"),
        "final_feedback": feedback_data.get("final_feedback", ""),
        "gpt_caption": feedback_data.get("gpt_caption", ""),
        "gpt_caption_prompt": feedback_data.get("gpt_caption_prompt", ""),
        "gpt_caption_llm": feedback_data.get("gpt_caption_llm", ""),
        "caption_rating_score": feedback_data.get("caption_rating_score"),
        "final_caption": feedback_data.get("final_caption", "")
    }


def extract_review_metadata(review_file_path):
    """Extract reviewer metadata from review file."""
    if not os.path.exists(review_file_path):
        return {}
    
    try:
        with open(review_file_path, 'r') as f:
            review_data = json.load(f)
        
        return {
            "reviewer": review_data.get("reviewer_name", ""),
            "review_timestamp": review_data.get("review_timestamp", ""),
            "reviewer_double_check": review_data.get("reviewer_double_check", True)
        }
    except Exception as e:
        print(f"Warning: Error loading review metadata: {e}")
        return {}


def extract_task_data(video_id, config_output_dir, data_manager):
    """
    Extract complete task data including negative examples for rejected captions.
    
    Returns:
        dict: Complete task data with status and workflow information
    """
    task_status, error_msg = determine_task_status(video_id, config_output_dir, data_manager)
    
    if error_msg:
        raise CaptionExportError(error_msg)
    
    result = {"status": task_status}
    
    if task_status == "not_completed":
        return result
    
    # Load current feedback data
    current_feedback_data = None
    current_file = data_manager.get_filename(video_id, config_output_dir, data_manager.FEEDBACK_FILE_POSTFIX)
    if os.path.exists(current_file):
        try:
            current_feedback_data = data_manager.load_data(video_id, config_output_dir, data_manager.FEEDBACK_FILE_POSTFIX)
        except Exception as e:
            print(f"Warning: Error loading current feedback for {video_id}: {e}")
    
    # Load review metadata if applicable
    review_metadata = {}
    if task_status in ["approved", "rejected"]:
        review_file = data_manager.get_filename(video_id, config_output_dir, data_manager.REVIEWER_FILE_POSTFIX)
        review_metadata = extract_review_metadata(review_file)
    
    if task_status == "completed_not_reviewed":
        # Single entry: annotator's work
        result["caption_data"] = extract_complete_workflow_data(current_feedback_data)
        
    elif task_status == "approved":
        # Single entry: annotator's work that was approved
        caption_data = extract_complete_workflow_data(current_feedback_data)
        caption_data.update(review_metadata)
        result["caption_data"] = caption_data
        
    elif task_status == "rejected":
        # Two entries: reviewer's version (main) + annotator's version (negative example)
        
        # Load previous feedback data (original annotator's version)
        prev_feedback_data = None
        prev_file = data_manager.get_filename(video_id, config_output_dir, data_manager.PREV_FEEDBACK_FILE_POSTFIX)
        if os.path.exists(prev_file):
            try:
                prev_feedback_data = data_manager.load_data(video_id, config_output_dir, data_manager.PREV_FEEDBACK_FILE_POSTFIX)
            except Exception as e:
                print(f"Warning: Error loading previous feedback for {video_id}: {e}")
        
        # Main entry: reviewer's improved version
        reviewer_data = extract_complete_workflow_data(current_feedback_data)
        reviewer_data.update(review_metadata)
        if prev_feedback_data:
            reviewer_data["original_annotator"] = prev_feedback_data.get("user", "")
        result["caption_data"] = reviewer_data
        
        # Negative example: original annotator's rejected version
        if prev_feedback_data:
            result["negative_example"] = extract_complete_workflow_data(prev_feedback_data)
    
    return result


def collect_all_video_data(video_urls, configs, data_manager, app_config):
    """
    Collect complete data for all videos with task-level organization.
    
    Returns:
        dict: {video_id: {video_url, captions: {caption_type: task_data}}}
    """
    all_videos_data = {}
    errors = []
    
    for video_url in video_urls:
        video_id = data_manager.get_video_id(video_url)
        
        video_data = {
            "video_id": video_id,
            "video_url": video_url,
            "captions": {}
        }
        
        for config in configs:
            config_name = config["name"]
            caption_type = CONFIG_TO_CAPTION.get(config_name)
            if not caption_type:
                continue
                
            config_output_dir = os.path.join(data_manager.folder, app_config.output_dir, config["output_name"])
            if not os.path.exists(config_output_dir):
                video_data["captions"][caption_type] = {"status": "not_completed"}
                continue
            
            try:
                task_data = extract_task_data(video_id, config_output_dir, data_manager)
                video_data["captions"][caption_type] = task_data
                    
            except CaptionExportError as e:
                errors.append(str(e))
                print(f"Error: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error for {video_id}, {config_name}: {e}")
                video_data["captions"][caption_type] = {"status": "error", "error": str(e)}
        
        all_videos_data[video_id] = video_data
    
    if errors:
        print(f"\nFound {len(errors)} videos with rejected captions that haven't been improved:")
        for error in errors[:3]:  # Show first 3 errors
            print(f"  - {error}")
        if len(errors) > 3:
            print(f"  ... and {len(errors) - 3} more")
        raise CaptionExportError(f"Found {len(errors)} rejected captions that haven't been improved")
    
    return all_videos_data


def organize_by_completion_level(all_videos_data):
    """
    Organize videos by meaningful completion levels.
    
    Returns:
        dict: {completion_level: [video_data]}
    """
    completion_categories = {
        "all_videos_with_captions": [],
        "reviewed_videos": [],
        "not_completed_videos": []
    }
    
    for video_data in all_videos_data.values():
        # Analyze task completion across all caption types
        has_any_captions = False
        has_reviewed_tasks = False
        all_tasks_not_completed = True
        
        for task_data in video_data["captions"].values():
            status = task_data.get("status", "not_completed")
            
            if status != "not_completed":
                has_any_captions = True
                all_tasks_not_completed = False
                
            if status in ["approved", "rejected"]:
                has_reviewed_tasks = True
        
        # Categorize based on meaningful completion levels
        if all_tasks_not_completed:
            completion_categories["not_completed_videos"].append(video_data)
        else:
            if has_any_captions:
                completion_categories["all_videos_with_captions"].append(video_data)
            if has_reviewed_tasks:
                completion_categories["reviewed_videos"].append(video_data)
    
    return completion_categories


def save_export_files(completion_categories, export_dir, all_videos_data, hf_dataset=None):
    """Save export files organized by completion level and optionally upload to HuggingFace."""
    # Load environment variables
    load_dotenv()
    
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    export_subdir = os.path.join(export_dir, f"export_{timestamp}")
    os.makedirs(export_subdir, exist_ok=True)
    
    saved_files = {}
    
    for category, video_list in completion_categories.items():
        if video_list:  # Only save non-empty categories
            filename = f"{category}_{timestamp}.json"
            filepath = os.path.join(export_subdir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(video_list, f, indent=2)
            
            saved_files[category] = filepath
            print(f"Exported {len(video_list)} videos to {filename}")
        else:
            print(f"No videos found for category: {category}")
    
    # Generate and save statistics inside the export directory
    print("Generating statistics...")
    stats = generate_comprehensive_statistics(all_videos_data)
    stats_file = os.path.join(export_subdir, f"comprehensive_statistics_{timestamp}.json")
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    saved_files["statistics"] = stats_file
    
    # Upload to HuggingFace if dataset specified (now includes statistics file)
    if hf_dataset:
        upload_to_huggingface(export_subdir, hf_dataset, timestamp)
    
    return saved_files, export_subdir

def upload_to_huggingface(local_dir, hf_dataset, timestamp):
    """Upload the export directory to HuggingFace dataset."""
    # Load environment variables
    load_dotenv()
    try:
        # Get HuggingFace token from environment
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            print("Warning: HF_TOKEN not found in environment. Skipping HuggingFace upload.")
            return
        
        # Initialize HuggingFace API
        api = HfApi()
        
        # Upload the entire export directory
        folder_name = os.path.basename(local_dir)  # e.g., "export_20250915_143022"
        
        print(f"Uploading to HuggingFace dataset: {hf_dataset}")
        print(f"Local directory: {local_dir}")
        print(f"Remote path: {folder_name}/")
        
        api.upload_folder(
            folder_path=local_dir,
            path_in_repo=folder_name,
            repo_id=hf_dataset,
            repo_type="dataset",
            token=hf_token
        )
        
        print(f"Successfully uploaded to https://huggingface.co/datasets/{hf_dataset}")
        print(f"Files will be visible at: https://huggingface.co/datasets/{hf_dataset}/tree/main/{folder_name}")
        
    except Exception as e:
        print(f"Error uploading to HuggingFace: {e}")
        print("Export completed locally, but HuggingFace upload failed.")


def generate_comprehensive_statistics(all_videos_data):
    """Generate comprehensive statistics by task and completion level."""
    stats = {
        "export_timestamp": datetime.now().isoformat(),
        "total_videos": len(all_videos_data),
        "task_completion_summary": {},
        "workflow_analysis": defaultdict(int),
        "quality_metrics": defaultdict(list),
        "completion_by_task": {}
    }
    
    # Analyze each caption type
    for caption_type in CONFIG_TO_CAPTION.values():
        task_stats = defaultdict(int)
        
        for video_data in all_videos_data.values():
            if caption_type in video_data["captions"]:
                task_info = video_data["captions"][caption_type]
                status = task_info.get("status", "not_completed")
                task_stats[status] += 1
                
                # Analyze workflow types and quality
                if "caption_data" in task_info:
                    caption_data = task_info["caption_data"]
                    workflow_type = caption_data.get("workflow_type", "unknown")
                    stats["workflow_analysis"][workflow_type] += 1
                    
                    # Collect quality metrics
                    initial_rating = caption_data.get("initial_caption_rating_score")
                    if initial_rating is not None:
                        stats["quality_metrics"]["initial_ratings"].append(initial_rating)
                    
                    final_rating = caption_data.get("caption_rating_score")
                    if final_rating is not None:
                        stats["quality_metrics"]["final_ratings"].append(final_rating)
        
        stats["completion_by_task"][caption_type] = dict(task_stats)
    
    # Calculate completion summary
    total_possible_tasks = len(all_videos_data) * len(CONFIG_TO_CAPTION)
    completed_tasks = sum(
        sum(1 for task in video["captions"].values() 
            if task.get("status") != "not_completed")
        for video in all_videos_data.values()
    )
    reviewed_tasks = sum(
        sum(1 for task in video["captions"].values() 
            if task.get("status") in ["approved", "rejected"])
        for video in all_videos_data.values()
    )
    
    stats["task_completion_summary"] = {
        "total_possible_tasks": total_possible_tasks,
        "completed_tasks": completed_tasks,
        "reviewed_tasks": reviewed_tasks,
        "completion_rate": (completed_tasks / total_possible_tasks) * 100,
        "review_rate": (reviewed_tasks / completed_tasks) * 100 if completed_tasks > 0 else 0
    }
    
    # Calculate quality averages
    if stats["quality_metrics"]["initial_ratings"]:
        stats["quality_metrics"]["avg_initial_rating"] = sum(stats["quality_metrics"]["initial_ratings"]) / len(stats["quality_metrics"]["initial_ratings"])
    if stats["quality_metrics"]["final_ratings"]:
        stats["quality_metrics"]["avg_final_rating"] = sum(stats["quality_metrics"]["final_ratings"]) / len(stats["quality_metrics"]["final_ratings"])
    
    return stats


def discover_videos_from_output(output_dir, configs, data_manager):
    """
    Discover all videos that have caption files in the output directory.
    
    Returns:
        set: Set of video_ids found across all config directories
    """
    all_video_ids = set()
    
    for config in configs:
        config_output_dir = os.path.join(data_manager.folder, output_dir, config["output_name"])
        if not os.path.exists(config_output_dir):
            continue
            
        # Find all feedback files in this config directory
        for filename in os.listdir(config_output_dir):
            if filename.endswith(data_manager.FEEDBACK_FILE_POSTFIX):
                video_id = filename.replace(data_manager.FEEDBACK_FILE_POSTFIX, "")
                all_video_ids.add(video_id)
    
    return all_video_ids


def print_export_summary(stats, saved_files):
    """Print a comprehensive export summary."""
    print("\n" + "="*80)
    print("EXPORT SUMMARY")
    print("="*80)
    
    print(f"Total Videos: {stats['total_videos']}")
    
    summary = stats["task_completion_summary"]
    print(f"Task Completion: {summary['completed_tasks']}/{summary['total_possible_tasks']} ({summary['completion_rate']:.1f}%)")
    print(f"Review Progress: {summary['reviewed_tasks']}/{summary['completed_tasks']} ({summary['review_rate']:.1f}%)")
    
    print(f"\nPer-Task Breakdown:")
    task_names = {
        "subject": "Subject Description",
        "scene": "Scene Composition", 
        "motion": "Subject Motion",
        "spatial": "Spatial Framing",
        "camera": "Camera Framing",
        "color": "Color Composition",
        "lighting": "Lighting Setup",
        "effects": "Lighting Effects"
    }
    
    for caption_type, task_name in task_names.items():
        if caption_type in stats["completion_by_task"]:
            task_stats = stats["completion_by_task"][caption_type]
            total_task = sum(task_stats.values())
            completed = sum(count for status, count in task_stats.items() if status != "not_completed")
            reviewed = sum(count for status, count in task_stats.items() if status in ["approved", "rejected"])
            
            print(f"  {task_name}: {completed}/{total_task} completed, {reviewed} reviewed")
    
    if "avg_initial_rating" in stats["quality_metrics"]:
        print(f"\nQuality Metrics:")
        print(f"  Average Initial Rating: {stats['quality_metrics']['avg_initial_rating']:.2f}/5")
        if "avg_final_rating" in stats["quality_metrics"]:
            print(f"  Average Final Rating: {stats['quality_metrics']['avg_final_rating']:.2f}/5")
    
    print(f"\nExported Files:")
    for category, filepath in saved_files.items():
        print(f"  {category.replace('_', ' ').title()}: {os.path.basename(filepath)}")
    
    print("="*80)


def main():
    parser = argparse.ArgumentParser(description="Export video captions organized by completion level")
    
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument("--configs", type=str, default="all_configs.json",
                      help="Path to the configs JSON file")
    # UPDATED: Change default directory
    parser.add_argument("--export_dir", type=str, default="caption_export",
                      help="Directory to save exported caption files")
    # NEW: Add HuggingFace dataset argument
    parser.add_argument("--hf_dataset", type=str, default="zhiqiulin/caption_export",
                      help="HuggingFace dataset repository to upload to")
    parser.add_argument("--only_reviewed", action="store_true", default=False,
                      help="If set, only export videos with reviewed tasks")
    parser.add_argument("--ignore_errors", action="store_true", default=False,
                      help="Continue export even if rejected-but-not-improved captions are found")
    
    args = parser.parse_args()
    
    print("Video Caption Export Script")
    print(f"Config Type: {args.config_type}")
    print(f"Export Directory: {args.export_dir}")
    
    # Initialize modular components
    folder_path = Path(__file__).parent  # caption/ directory
    root_path = folder_path.parent       # project root
    
    # Get configuration
    app_config = get_config(args.config_type)
    
    # Initialize data manager
    data_manager = DataManager(folder_path, root_path)
    
    # Load configs
    try:
        configs = data_manager.load_config(args.configs)
        configs = [data_manager.load_config(config) for config in configs]
        print(f"Loaded {len(configs)} caption configs")
    except Exception as e:
        print(f"Error loading configs: {e}")
        return
    
    # Get video URLs
    video_urls = []
    if app_config.video_urls_files:
        print(f"Loading videos from {len(app_config.video_urls_files)} URL files...")
        for urls_file in app_config.video_urls_files:
            try:
                file_videos = data_manager.load_json(urls_file)
                video_urls.extend(file_videos)
                print(f"  {urls_file}: {len(file_videos)} videos")
            except Exception as e:
                print(f"Error loading {urls_file}: {e}")
        print(f"Total videos: {len(video_urls)}")
    else:
        print("Discovering videos from output directory...")
        discovered_video_ids = discover_videos_from_output(app_config.output_dir, configs, data_manager)
        video_urls = [f"dummy_url/{video_id}.mp4" for video_id in discovered_video_ids]
        print(f"Discovered {len(video_urls)} videos")
    
    if not video_urls:
        print("No videos found to export")
        return
    
    # Collect video data
    print("\nAnalyzing video caption data...")
    try:
        all_videos_data = collect_all_video_data(video_urls, configs, data_manager, app_config)
    except CaptionExportError as e:
        if args.ignore_errors:
            print("Ignoring errors and continuing export...")
            return
        else:
            print("Export failed due to data integrity issues.")
            print("Fix the rejected captions or use --ignore_errors to continue.")
            return
    
    # Filter by review status if requested
    if args.only_reviewed:
        print("Filtering for only reviewed videos...")
        filtered_data = {}
        for video_id, video_data in all_videos_data.items():
            has_reviewed = any(
                task_data.get("status") in ["approved", "rejected"]
                for task_data in video_data["captions"].values()
            )
            if has_reviewed:
                filtered_data[video_id] = video_data
        all_videos_data = filtered_data
        print(f"{len(all_videos_data)} videos have reviewed tasks")
    
    # Organize and save
    print("\nOrganizing and exporting data...")
    completion_categories = organize_by_completion_level(all_videos_data)
    saved_files, export_subdir = save_export_files(completion_categories, args.export_dir, all_videos_data, args.hf_dataset)

    # # Generate and save statistics
    # print("\nGenerating statistics...")
    # stats = generate_comprehensive_statistics(all_videos_data)

    # timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    # stats_file = os.path.join(export_subdir, f"comprehensive_statistics_{timestamp}.json")
    # with open(stats_file, 'w') as f:
    #     json.dump(stats, f, indent=2)
    # saved_files["statistics"] = stats_file
    
    # Print summary (stats are now in saved_files from save_export_files)
    stats_file = saved_files.get("statistics")
    if stats_file:
        with open(stats_file, 'r') as f:
            stats = json.load(f)
        print_export_summary(stats, saved_files)

    print(f"\nExport completed successfully!")
    print(f"Files saved to: {export_subdir}")
    if args.hf_dataset:
        print(f"Uploaded to: https://huggingface.co/datasets/{args.hf_dataset}")


if __name__ == "__main__":
    main()