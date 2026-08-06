# caption/core/data_manager.py
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from process_json import json_to_video_data


class DataManager:
    """Handles all data loading, saving, and status checking operations"""
    
    def __init__(self, folder_path: Path, root_path: Path = None):
        self.folder = folder_path  # caption/ directory
        self.root = root_path or folder_path.parent  # project root directory
        
        # File postfixes - must match original exactly
        self.FEEDBACK_FILE_POSTFIX = "_feedback.json"
        self.PREV_FEEDBACK_FILE_POSTFIX = "_feedback_prev.json"
        self.REVIEWER_FILE_POSTFIX = "_review.json"
        self.PREV_REVIEWER_FILE_POSTFIX = "_review_prev.json"
        self.PRECAPTION_FILE_POSTFIX = "_precaption.json"
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON file"""
        full_path = self.folder / file_path if not os.path.isabs(file_path) else file_path
        with open(full_path, 'r') as f:
            return json.load(f)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration file"""
        return self.load_json(config_path)
    
    def get_filename(self, video_id: str, output_dir: str, file_postfix: str) -> str:
        """Get the filename for saving/loading data"""
        return os.path.join(output_dir, f'{video_id}{file_postfix}')
    
    def save_data(self, video_id: str, data: Dict[str, Any], output_dir: str, file_postfix: str) -> str:
        """Save data to a JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        filename = self.get_filename(video_id, output_dir, file_postfix)
        
        # Add timestamp if not already present
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to: {filename}")
        return filename
    
    def load_data(self, video_id: str, output_dir: str, file_postfix: str) -> Optional[Dict[str, Any]]:
        """Load existing data for a video if it exists"""
        filename = self.get_filename(video_id, output_dir, file_postfix)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None
    
    def data_exists(self, video_id: str, output_dir: str, file_postfix: str) -> bool:
        """Check if data already exists"""
        filename = self.get_filename(video_id, output_dir, file_postfix)
        return os.path.exists(filename)
    
    def get_video_status(self, video_id: str, output_dir: str) -> Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]:
        """Get the status of a video's caption completion and previous iterations
        
        Returns: (status, current_file, prev_file, current_user, prev_user)
        Status can be: 'not_completed', 'completed_not_reviewed', 'approved', 'rejected'
        """
        # Initialize all variables to ensure consistent return
        status = "not_completed"
        current_file = None
        prev_file = None
        current_user = None
        prev_user = None
        
        # Check all relevant files
        feedback_file = self.get_filename(video_id, output_dir, self.FEEDBACK_FILE_POSTFIX)
        prev_feedback_file = self.get_filename(video_id, output_dir, self.PREV_FEEDBACK_FILE_POSTFIX)
        reviewer_file = self.get_filename(video_id, output_dir, self.REVIEWER_FILE_POSTFIX)
        
        # First check if main feedback file exists
        if not os.path.exists(feedback_file):
            return status, current_file, prev_file, current_user, prev_user
            
        # Load current feedback data
        current_file = feedback_file
        try:
            with open(feedback_file, 'r') as f:
                current_data = json.load(f)
                current_user = current_data.get("user")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading feedback file {feedback_file}: {e}")
            return status, current_file, prev_file, current_user, prev_user
        
        # Check if reviewed
        if not os.path.exists(reviewer_file):
            status = "completed_not_reviewed"
            return status, current_file, prev_file, current_user, prev_user
        
        # Load reviewer data
        try:
            with open(reviewer_file, 'r') as f:
                reviewer_data = json.load(f)
                reviewer_double_check = reviewer_data.get("reviewer_double_check", False)
                
                if reviewer_double_check:
                    status = "approved"
                    # For approved files, load previous feedback if it exists
                    if os.path.exists(prev_feedback_file):
                        try:
                            with open(prev_feedback_file, 'r') as pf:
                                prev_data = json.load(pf)
                                prev_user = prev_data.get("user")
                                prev_file = prev_feedback_file
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error reading previous feedback file {prev_feedback_file}: {e}")
                else:
                    status = "rejected"
                    # For rejected files, must have prev feedback with different user
                    if not os.path.exists(prev_feedback_file):
                        print(f"Warning: Rejected file {video_id} missing previous feedback")
                        # Treat as completed_not_reviewed if previous feedback is missing
                        status = "completed_not_reviewed"
                        return status, current_file, prev_file, current_user, prev_user
                    
                    try:
                        with open(prev_feedback_file, 'r') as pf:
                            prev_data = json.load(pf)
                            prev_user = prev_data.get("user")
                            prev_file = prev_feedback_file
                            
                            # Check if the caption was just rejected but not updated yet
                            if prev_user == current_user:
                                # Same user in both files means rejection happened but no correction yet
                                status = "completed_not_reviewed"
                                prev_user = None
                                prev_file = None
                                return status, current_file, prev_file, current_user, prev_user
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading previous feedback file {prev_feedback_file}: {e}")
                        status = "completed_not_reviewed"
                        return status, current_file, prev_file, current_user, prev_user
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading reviewer file {reviewer_file}: {e}")
            status = "completed_not_reviewed"
            return status, current_file, prev_file, current_user, prev_user
        
        return status, current_file, prev_file, current_user, prev_user
    
    def get_annotator_and_reviewer(self, video_id: str, output_dir: str) -> Tuple[Optional[str], Optional[str]]:
        """Determine who is the annotator and who is the reviewer based on feedback files
        
        Returns: (annotator, reviewer)
        """
        current_feedback = self.load_data(video_id, output_dir, self.FEEDBACK_FILE_POSTFIX)
        prev_feedback = self.load_data(video_id, output_dir, self.PREV_FEEDBACK_FILE_POSTFIX)
        
        if not current_feedback:
            return None, None
        
        if not prev_feedback:
            # Only current feedback exists - the user in current feedback is the annotator
            return current_feedback.get("user"), None
        
        # Both files exist - prev feedback user is annotator, current feedback user is reviewer
        return prev_feedback.get("user"), current_feedback.get("user")
    
    def check_video_completion_status(self, video_urls_file: str, configs: List[Dict[str, Any]], output_dir: str) -> Tuple[Dict[str, Tuple[bool, bool]], Dict[str, int], Dict[str, int]]:
        """Check completion status of videos in a file.
        
        Args:
            video_urls_file: Path to the video URLs file
            configs: List of configs to check
            output_dir: Output directory to check for feedback files
            
        Returns:
            Tuple of (is_completed, is_reviewed) for each video
            Dict of "annotators" and "reviewers" with the number of videos completed and reviewed by each
        """
        video_urls = self.load_json(video_urls_file)
        status_dict = {}
        annotators_dict = {}
        reviewers_dict = {}
        
        for video_url in video_urls:
            video_id = self.get_video_id(video_url)
            is_completed = True
            is_reviewed = True
            
            for config in configs:
                config_output_dir = os.path.join(self.folder, output_dir, config["output_name"])
                feedback_file = self.get_filename(video_id, config_output_dir, self.FEEDBACK_FILE_POSTFIX)
                review_file = self.get_filename(video_id, config_output_dir, self.REVIEWER_FILE_POSTFIX)
                
                if not os.path.exists(feedback_file):
                    is_completed = False
                    is_reviewed = False
                    break
                else:
                    # FIXED: Use existing get_annotator_and_reviewer method to get actual annotator
                    annotator, reviewer = self.get_annotator_and_reviewer(video_id, config_output_dir)
                    
                    # Count the actual annotator (not whoever's name is in _feedback.json)
                    if annotator:
                        if annotator not in annotators_dict:
                            annotators_dict[annotator] = 0
                        annotators_dict[annotator] += 1
                    
                # Review counting (unchanged - this logic was already correct)
                if not os.path.exists(review_file):
                    is_reviewed = False
                else:
                    try:
                        with open(review_file, 'r') as rf:
                            review_data = json.load(rf)
                            reviewer = review_data.get("reviewer_name")
                            if reviewer:
                                if reviewer not in reviewers_dict:
                                    reviewers_dict[reviewer] = 0
                                reviewers_dict[reviewer] += 1
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading review file {review_file}: {e}")
                        
            status_dict[video_url] = (is_completed, is_reviewed)
        
        return status_dict, annotators_dict, reviewers_dict

    def get_annotator_videos(self, annotator_name: str, configs: List[Dict[str, Any]], output_dir: str, 
                           not_yet_reviewed: bool = False, show_only_rejected: bool = False) -> List[str]:
        """Get all videos that have been completed by an annotator.
        
        Args:
            annotator_name: Name of the annotator
            configs: List of configs to check
            output_dir: Output directory to check for feedback files
            not_yet_reviewed: If True, only return videos that haven't been reviewed
            show_only_rejected: If True, only return videos that have been rejected
            
        Returns:
            List of video URLs that match the criteria, sorted appropriately
        """
        if not_yet_reviewed and show_only_rejected:
            raise ValueError("Cannot show both not yet reviewed and show only rejected videos")
        
        start_time = time.time()
        
        # Get all video URLs from all files
        try:
            # Try to get video URLs from a main config - this should be improved to pass video files properly
            from caption.config.main_config import DEFAULT_VIDEO_URLS_FILES
            all_video_urls = []
            for video_urls_file in DEFAULT_VIDEO_URLS_FILES:
                try:
                    video_urls = self.load_json(video_urls_file)
                    all_video_urls.extend(video_urls)
                except FileNotFoundError:
                    print(f"Warning: Video URLs file not found: {video_urls_file}")
                    continue
        except ImportError:
            print("Warning: Could not import DEFAULT_VIDEO_URLS_FILES, using empty list")
            all_video_urls = []
        
        print(f"Found {len(all_video_urls)} total videos to check")
        
        # Filter videos based on criteria
        matching_videos = []
        video_timestamps = {}  # Store timestamps for sorting
        video_reviewed = {}  # Track which videos have been reviewed
        
        for video_url in all_video_urls:
            video_id = self.get_video_id(video_url)
            has_completed_task = False
            all_tasks_reviewed = True
            is_rejected = False
            earliest_completion_time = None
            latest_review_time = None
            
            # Check each task for this video
            for config in configs:
                config_output_dir = os.path.join(self.folder, output_dir, config["output_name"])
                feedback_file = self.get_filename(video_id, config_output_dir, self.FEEDBACK_FILE_POSTFIX)
                review_file = self.get_filename(video_id, config_output_dir, self.REVIEWER_FILE_POSTFIX)
                
                # Skip if feedback file doesn't exist
                if not os.path.exists(feedback_file):
                    continue
                    
                try:
                    # Check if this annotator completed this task
                    with open(feedback_file, 'r') as f:
                        feedback_data = json.load(f)
                        if feedback_data.get("user") == annotator_name:
                            has_completed_task = True
                            # Store completion time if available
                            if "timestamp" in feedback_data:
                                completion_time = feedback_data["timestamp"]
                                if earliest_completion_time is None or completion_time < earliest_completion_time:
                                    earliest_completion_time = completion_time
                            
                            # Check review status
                            if not os.path.exists(review_file):
                                all_tasks_reviewed = False
                            else:
                                # Check if the video was rejected and get review time
                                try:
                                    with open(review_file, 'r') as rf:
                                        review_data = json.load(rf)
                                        if not review_data.get("reviewer_double_check", False):
                                            is_rejected = True
                                        if "review_timestamp" in review_data:
                                            review_time = review_data["review_timestamp"]
                                            if latest_review_time is None or review_time > latest_review_time:
                                                latest_review_time = review_time
                                except (json.JSONDecodeError, KeyError) as e:
                                    print(f"Error reading review file {review_file}: {e}")
                                    all_tasks_reviewed = False
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error reading feedback file {feedback_file}: {e}")
                    continue
            
            # Add video if it matches criteria
            if has_completed_task:
                if show_only_rejected and not is_rejected:
                    continue
                if not not_yet_reviewed or not all_tasks_reviewed:
                    matching_videos.append(video_url)
                    # Store appropriate timestamp based on sorting criteria
                    if not_yet_reviewed:
                        # For not_yet_reviewed=True, sort by earliest completion time
                        video_timestamps[video_url] = earliest_completion_time if earliest_completion_time else "0000-00-00"
                    else:
                        # For not_yet_reviewed=False, sort by latest review time with unreviewed at end
                        video_timestamps[video_url] = latest_review_time if latest_review_time else "0000-00-00"
                        video_reviewed[video_url] = bool(latest_review_time)
        
        # Sort videos based on criteria
        if video_timestamps:
            if not_yet_reviewed:
                # Sort by earliest completion time (oldest to latest)
                matching_videos.sort(key=lambda x: video_timestamps.get(x, "9999-99-99"))
            else:
                # Sort by latest review time (latest to oldest) with unreviewed at end
                matching_videos.sort(key=lambda x: (
                    not video_reviewed.get(x, False),  # First sort by reviewed status (False comes before True)
                    video_timestamps.get(x, "0000-00-00")  # Then by timestamp
                ))
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Found {len(matching_videos)} matching videos for annotator {annotator_name}")
        print(f"Total search time: {total_time:.2f} seconds ({total_time/len(all_video_urls):.3f} seconds per video)")
        return matching_videos
    
    def load_video_data(self, video_data_file: str, label_collections: List[str] = None) -> Dict[str, Any]:
        """Load video data with specified label collections"""
        if label_collections is None:
            label_collections = ["cam_motion", "cam_setup", "lighting_setup"]
        
        # Video data files are in root directory
        video_data_path = self.root / video_data_file
        video_data_dict = json_to_video_data(str(video_data_path), label_collections=label_collections)
        
        for video_data in video_data_dict.values():
            if hasattr(video_data, "cam_motion"):
                video_data.cam_motion.update()
            if hasattr(video_data, "cam_setup"):
                video_data.cam_setup.update()
                # Set default descriptions if missing - must match original exactly
                default_descriptions = {
                    "subject_description": "**{NO DESCRIPTION FOR SUBJECTS YET}**",
                    "scene_description": "**{NO DESCRIPTION FOR SCENE YET}**",
                    "motion_description": "**{NO DESCRIPTION FOR SUBJECT MOTION YET}**",
                    "spatial_description": "**{NO DESCRIPTION FOR SPATIAL FRAMING YET}**",
                    "camera_description": "**{NO DESCRIPTION FOR CAMERA FRAMING YET}**",
                    "color_description": "**{NO DESCRIPTION FOR COLOR COMPOSITION YET}**",
                    "lighting_description": "**{NO DESCRIPTION FOR LIGHTING SETUP YET}**",
                    "lighting_effects_description": "**{NO DESCRIPTION FOR LIGHTING EFFECTS YET}**",
                }
                for attr, default_val in default_descriptions.items():
                    if getattr(video_data.cam_setup, attr, None) is None:
                        setattr(video_data.cam_setup, attr, default_val)
            if hasattr(video_data, "lighting_setup"):
                video_data.lighting_setup.update()
                
        return video_data_dict
    
    def copy_to_prev_feedback(self, video_id: str, output_dir: str):
        """Copy current feedback to previous feedback file"""
        current_file = self.get_filename(video_id, output_dir, self.FEEDBACK_FILE_POSTFIX)
        prev_file = self.get_filename(video_id, output_dir, self.PREV_FEEDBACK_FILE_POSTFIX)
        
        if not os.path.exists(current_file):
            raise FileNotFoundError(f"Current feedback file does not exist: {current_file}")
        
        # If prev file exists, check if it's different from current
        if os.path.exists(prev_file):
            try:
                with open(current_file, 'r') as f:
                    current_data = json.load(f)
                with open(prev_file, 'r') as f:
                    prev_data = json.load(f)
                if current_data == prev_data:
                    print(f"Current and previous feedback files are identical for {video_id}, no action needed")
                    return  # If they're the same, no need to do anything
                else:
                    print(f"Warning: Current and previous feedback files are different for {video_id}")
                    # Continue with copying to preserve the flow
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error comparing feedback files for {video_id}: {e}")
                # Continue with copying
        
        # Copy current to prev
        try:
            with open(current_file, 'r') as f:
                current_data = json.load(f)
            with open(prev_file, 'w') as f:
                json.dump(current_data, f, indent=4)
            print(f"Copied current feedback to previous feedback: {prev_file}")
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error copying feedback files for {video_id}: {e}")
            raise
    
    @staticmethod
    def get_video_id(url: str) -> str:
        """Extract video ID from URL"""
        return url.split('/')[-1]
    
    @staticmethod
    def format_timestamp(iso_timestamp: str) -> str:
        """Format ISO timestamp to a readable format"""
        if not iso_timestamp:
            return 'N/A'
        try:
            return datetime.fromisoformat(iso_timestamp).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return 'Invalid date'