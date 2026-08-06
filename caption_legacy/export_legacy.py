#!/usr/bin/env python3
"""
Complete Caption Export Script - caption/export.py

Exports video captions with proper status categorization and complete workflow data.
Handles all four status types and preserves complete annotation workflow.
Updated to use NEW modular structure - NO legacy dependencies!
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Import from NEW modular structure - NO legacy dependencies!
from caption.config import get_config
from caption.core.data_manager import DataManager
from caption.core.video_utils import VideoUtils


class CaptionExportError(Exception):
    """Custom exception for caption export issues"""
    pass


# Configuration mapping
CONFIG_TO_CAPTION = {
    "Subject Description Caption": "subject",
    "Scene Composition and Dynamics Caption": "scene",
    "Subject Motion and Dynamics Caption": "motion",
    "Spatial Framing and Dynamics Caption": "spatial",
    "Camera Framing and Dynamics Caption": "camera"
}


def determine_precise_status(video_id, config_output_dir, data_manager):
    """
    Determine the precise status of a video caption.
    
    Returns:
        str: One of "not_completed", "completed_not_reviewed", "approved", "rejected"
        str: Error message if edge case detected, None otherwise
    """
    status, current_file, prev_file, current_user, prev_user = data_manager.get_video_status(video_id, config_output_dir)
    
    # The status from get_video_status already uses the correct names
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
    
    # Extract user info
    user = feedback_data.get("user", "Unknown")
    timestamp = feedback_data.get("timestamp", "")
    
    # Prepare the output structure
    workflow_data = {
        "user": user,
        "timestamp": timestamp
    }
    
    # Check if feedback workflow was needed
    initial_feedback = feedback_data.get("initial_feedback")
    if initial_feedback:
        workflow_data["feedback_is_needed"] = True
        
        # Extract feedback stage data
        workflow_data["initial_feedback"] = initial_feedback
        workflow_data["gpt_feedback"] = feedback_data.get("gpt_feedback", "")
        workflow_data["gpt_feedback_llm"] = feedback_data.get("gpt_feedback_llm", "")
        workflow_data["gpt_feedback_prompt"] = feedback_data.get("gpt_feedback_prompt", "")
        workflow_data["feedback_rating_score"] = feedback_data.get("feedback_rating_score")
        workflow_data["final_feedback"] = feedback_data.get("final_feedback", "")
        
        # Extract caption generation data
        workflow_data["gpt_caption"] = feedback_data.get("gpt_caption", "")
        workflow_data["gpt_caption_prompt"] = feedback_data.get("gpt_caption_prompt", "")
        workflow_data["gpt_caption_llm"] = feedback_data.get("gpt_caption_llm", "")
        workflow_data["caption_rating_score"] = feedback_data.get("caption_rating_score")
    else:
        workflow_data["feedback_is_needed"] = False
    
    # Always include final caption
    workflow_data["final_caption"] = feedback_data.get("final_caption", "")
    
    return workflow_data


def export_videos_by_status(video_urls, configs, data_manager, app_config, only_reviewed=False, ignore_errors=False):
    """
    Export videos categorized by their completion status
    """
    # Initialize video utilities
    video_utils = VideoUtils()
    
    # Initialize status categories
    status_data = {
        "not_completed": [],
        "completed_not_reviewed": [],
        "approved": [],
        "rejected": []
    }
    
    # Track edge cases
    edge_cases = []
    
    # Track statistics
    stats = {
        "total_videos": len(video_urls),
        "total_tasks": len(configs),
        "total_possible_captions": len(video_urls) * len(configs),
        "status_counts": defaultdict(int),
        "task_completion": {config["name"]: defaultdict(int) for config in configs}
    }
    
    print(f"Processing {len(video_urls)} videos across {len(configs)} tasks...")
    
    # Process each video
    for video_url in video_urls:
        video_id = video_utils.get_video_id(video_url)
        
        # Create video entry
        video_entry = {
            "video_id": video_id,
            "video_url": video_url,
            "captions": {}
        }
        
        # Track video's overall status
        video_statuses = []
        has_any_caption = False
        
        # Check each config/task
        for config in configs:
            config_output_dir = os.path.join(data_manager.folder, app_config.output_dir, config["output_name"])
            caption_type = CONFIG_TO_CAPTION.get(config["name"])
            
            if not caption_type:
                continue
            
            # Determine status for this task
            status, error_msg = determine_precise_status(video_id, config_output_dir, data_manager)
            video_statuses.append(status)
            
            # Handle edge cases
            if error_msg:
                edge_cases.append({
                    "video_id": video_id,
                    "task": config["name"],
                    "error": error_msg
                })
                if not ignore_errors:
                    print(f"❌ Edge case found: {video_id} - {config['name']}: {error_msg}")
            
            # Extract caption data if it exists
            if status != "not_completed":
                has_any_caption = True
                feedback_data = data_manager.load_data(video_id, config_output_dir, data_manager.FEEDBACK_FILE_POSTFIX)
                
                if feedback_data:
                    caption_data = extract_complete_workflow_data(feedback_data)
                    caption_data["status"] = status
                    video_entry["captions"][caption_type] = caption_data
            else:
                video_entry["captions"][caption_type] = {"status": "not_completed"}
            
            # Update statistics
            stats["status_counts"][status] += 1
            stats["task_completion"][config["name"]][status] += 1
        
        # Determine overall video status priority: rejected > approved > completed_not_reviewed > not_completed
        if "rejected" in video_statuses:
            overall_status = "rejected"
        elif "approved" in video_statuses:
            overall_status = "approved"
        elif "completed_not_reviewed" in video_statuses:
            overall_status = "completed_not_reviewed"
        else:
            overall_status = "not_completed"
        
        # Add video to appropriate status category
        if only_reviewed and overall_status not in ["approved", "rejected"]:
            continue
        
        if overall_status == "not_completed" and not has_any_caption:
            status_data["not_completed"].append(video_entry)
        else:
            status_data[overall_status].append(video_entry)
    
    # Report edge cases
    if edge_cases and not ignore_errors:
        print(f"\n⚠️  Found {len(edge_cases)} edge cases!")
        print("Use --ignore_errors to continue export anyway.")
        return None, None, edge_cases
    
    return status_data, stats, edge_cases


def save_exports(status_data, stats, export_dir, edge_cases):
    """Save exported data to files"""
    os.makedirs(export_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    saved_files = []
    
    # Save status-based exports
    for status, videos in status_data.items():
        if videos:  # Only save non-empty categories
            filename = f"{status}_{timestamp}.json"
            filepath = os.path.join(export_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(videos, f, indent=2)
            
            saved_files.append(filepath)
            print(f"✅ Exported {len(videos)} videos with status '{status}' to {filename}")
    
    # Save comprehensive export (all videos with any captions)
    all_with_captions = []
    for status in ["completed_not_reviewed", "approved", "rejected"]:
        all_with_captions.extend(status_data[status])
    
    if all_with_captions:
        filename = f"all_with_captions_{timestamp}.json"
        filepath = os.path.join(export_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(all_with_captions, f, indent=2)
        
        saved_files.append(filepath)
        print(f"✅ Exported {len(all_with_captions)} videos with captions to {filename}")
    
    # Save statistics
    stats_filename = f"comprehensive_statistics_{timestamp}.json"
    stats_filepath = os.path.join(export_dir, stats_filename)
    
    # Add edge case summary to stats
    stats["edge_cases_found"] = len(edge_cases)
    stats["edge_case_details"] = edge_cases
    
    with open(stats_filepath, 'w') as f:
        json.dump(stats, f, indent=2)
    
    saved_files.append(stats_filepath)
    print(f"✅ Exported statistics to {stats_filename}")
    
    return saved_files


def print_export_summary(stats, edge_cases):
    """Print a comprehensive export summary"""
    print("\n" + "="*80)
    print("📊 EXPORT SUMMARY")
    print("="*80)
    
    print(f"📹 Total Videos: {stats['total_videos']}")
    print(f"📝 Total Tasks: {stats['total_tasks']}")
    print(f"📋 Total Possible Captions: {stats['total_possible_captions']}")
    
    print(f"\n📈 Status Distribution:")
    for status, count in stats["status_counts"].items():
        percentage = (count / stats['total_possible_captions']) * 100
        print(f"   {status}: {count} ({percentage:.1f}%)")
    
    if edge_cases:
        print(f"\n⚠️  Edge Cases Found: {len(edge_cases)}")
        for case in edge_cases[:5]:  # Show first 5
            print(f"   • {case['video_id']} - {case['task']}: {case['error']}")
        if len(edge_cases) > 5:
            print(f"   ... and {len(edge_cases) - 5} more")
    
    print("="*80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Export video captions with complete status categorization")
    
    # Use new config system - NO legacy dependencies!
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument("--configs", type=str, default="all_configs.json",
                      help="Path to the configs JSON file")
    parser.add_argument("--export_dir", type=str, default="exported_captions_complete",
                      help="Directory to save exported caption files")
    parser.add_argument("--only_reviewed", action="store_true", default=False,
                      help="If set, only export captions that have been reviewed")
    parser.add_argument("--ignore_errors", action="store_true", default=False,
                      help="Continue export even if rejected-but-not-improved captions are found")
    
    args = parser.parse_args()
    
    # Initialize new modular components
    folder_path = Path(__file__).parent  # caption/ directory
    root_path = folder_path.parent       # project root
    
    # Get configuration using new system
    app_config = get_config(args.config_type)
    
    # Initialize data manager and video utils
    data_manager = DataManager(folder_path, root_path)
    
    # Load configs using new system
    configs = data_manager.load_config(args.configs)
    configs = [data_manager.load_config(config) for config in configs]
    
    # Load video URLs from new config system
    all_video_urls = []
    for video_urls_file in app_config.video_urls_files:
        video_urls = data_manager.load_json(video_urls_file)
        all_video_urls.extend(video_urls)
    
    print(f"🎬 Loaded {len(all_video_urls)} videos from {len(app_config.video_urls_files)} URL files")
    print(f"📂 Using config type: {args.config_type}")
    print(f"📁 Output directory: {app_config.output_dir}")
    print(f"🏗️  Using NEW modular structure (no legacy dependencies!)")
    
    # Export videos
    status_data, stats, edge_cases = export_videos_by_status(
        all_video_urls, configs, data_manager, app_config,
        args.only_reviewed, args.ignore_errors
    )
    
    if status_data is None:
        print("❌ Export failed due to edge cases. Use --ignore_errors to continue anyway.")
        return
    
    # Save exports
    saved_files = save_exports(status_data, stats, args.export_dir, edge_cases)
    
    # Print summary
    print_export_summary(stats, edge_cases)
    
    print(f"\n🎉 Export completed successfully!")
    print(f"📁 All files saved to: {args.export_dir}")
    print(f"📄 Files created: {len(saved_files)}")


def demo_usage():
    """Show usage examples with various format options"""
    print("\n" + "="*80)
    print("📋 USAGE EXAMPLES")
    print("="*80)
    
    # Example for different status categories
    example_status_data = {
        "not_completed": [
            {
                "video_id": "video_001",
                "video_url": "https://example.com/video_001.mp4",
                "captions": {
                    "subject": {"status": "not_completed"},
                    "scene": {"status": "not_completed"},
                    "motion": {"status": "not_completed"},
                    "spatial": {"status": "not_completed"},
                    "camera": {"status": "not_completed"}
                }
            }
        ],
        "completed_not_reviewed": [
            {
                "video_id": "video_002", 
                "video_url": "https://example.com/video_002.mp4",
                "captions": {
                    "subject": {
                        "status": "completed_not_reviewed",
                        "user": "alice_smith",
                        "timestamp": "2025-06-28T14:22:00",
                        "feedback_is_needed": False,
                        "final_caption": "Person walking with dog in park"
                    }
                }
            }
        ],
        "approved": [
            {
                "video_id": "video_003",
                "video_url": "https://example.com/video_003.mp4", 
                "captions": {
                    "subject": {
                        "status": "approved",
                        "user": "bob_jones",
                        "reviewer": "jane_doe",
                        "review_timestamp": "2025-06-29T09:15:00",
                        "feedback_is_needed": True,
                        "initial_feedback": "Caption needs more detail about clothing",
                        "gpt_feedback": "The caption should include more specific details about the person's clothing and appearance to provide a more complete description",
                        "final_feedback": "Add clothing details and posture description",
                        "gpt_caption": "Person in blue jacket walking confidently with small brown dog on leash through sunny park",
                        "final_caption": "Person in blue jacket walking confidently with small brown dog on leash through sunny park"
                    }
                }
            }
        ],
        "rejected": [
            {
                "video_id": "video_004",
                "video_url": "https://example.com/video_004.mp4",
                "captions": {
                    "subject": {
                        "status": "rejected", 
                        "user": "charlie_doe",
                        "reviewer": "jane_doe",
                        "review_timestamp": "2025-06-29T11:45:00",
                        "feedback_is_needed": True,
                        "initial_feedback": "Caption is too generic",
                        "negative_example": {
                            "user": "charlie_doe",
                            # ... complete rejected workflow data
                            "final_caption": "Person and dog walking"
                        }
                    }
                },
                "spatial": {
                    "status": "not_completed"
                },
                "camera": {
                    "status": "approved",
                    "caption_data": {
                        "user": "diana_kim",
                        "reviewer": "jane_doe",
                        "review_timestamp": "2025-06-29T16:30:00",
                        # ... complete workflow data
                        "final_caption": "Static wide shot from slightly elevated position"
                    }
                }
            }
        ]
    }
    print(json.dumps(example_status_data, indent=2))


if __name__ == "__main__":
    main()