from typing import Optional, List, Any, Dict
from datetime import datetime
import yaml
import json
import os
import logging

class VisualizationParams:
    """Parameters for batch visualization, loaded from YAML configuration."""
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> Dict[str, Any]:
        """Load visualization parameters from a YAML file."""
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Config file not found: {yaml_path}")
            
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Validate videos directory exists
        videos_dir = config.get('data', {}).get('videos_dir')
        
        # Debug logging for videos directory
        logging.info(f"Checking videos directory: {videos_dir}")
        
        # Convert relative path to absolute path
        if videos_dir and not os.path.isabs(videos_dir):
            # Get the directory containing the YAML file
            yaml_dir = os.path.dirname(os.path.abspath(yaml_path))
            abs_videos_dir = os.path.abspath(os.path.join(yaml_dir, videos_dir))
            logging.info(f"Absolute path of videos directory: {abs_videos_dir}")
            logging.info(f"Directory exists: {os.path.exists(abs_videos_dir)}")
            
            # Update config with absolute path
            config['data']['videos_dir'] = abs_videos_dir
            videos_dir = abs_videos_dir
            
        if not videos_dir or not os.path.exists(videos_dir):
            raise FileNotFoundError(f"Videos directory not found: {videos_dir}")
            
        return config

    @staticmethod
    def get_video_names(config: Dict[str, Any]) -> Optional[List[str]]:
        """Load video names from JSON file and verify videos exist."""
        # Get video_names_file from constraints section
        video_names_file = config.get('constraints', {}).get('video_names_file')
        if not video_names_file:
            raise ValueError("video_names_file must be specified in constraints")
            
        if not os.path.exists(video_names_file):
            raise FileNotFoundError(f"Video names file not found: {video_names_file}")
            
        # First load the video names
        with open(video_names_file, 'r') as f:
            video_names = json.load(f)
            if not isinstance(video_names, list):
                raise ValueError(f"Video names file must contain a JSON array of strings")
            if not all(isinstance(name, str) for name in video_names):
                raise ValueError(f"All entries in video names file must be strings")
        
        # Then verify videos exist if videos_dir is provided in data config
        videos_dir = config.get('data', {}).get('videos_dir')
        if videos_dir:
            # Create a set of all video files in all subdirectories
            all_video_files = set()
            logging.info(f"Searching for videos in {videos_dir} and its subdirectories...")
            for root, _, files in os.walk(videos_dir):
                for file in files:
                    if file.endswith('.mp4'):  # Assuming videos are MP4 files
                        all_video_files.add(file)
            
            # Check which videos from our list are missing
            missing_videos = [
                name for name in video_names 
                if name not in all_video_files
            ]
            
            if missing_videos:
                raise FileNotFoundError(
                    f"The following videos were not found in {videos_dir} or its subdirectories:\n"
                    f"{json.dumps(missing_videos, indent=2)}"
                )
            
            # For videos that exist, find their actual paths
            video_paths = {}
            for name in video_names:
                for root, _, files in os.walk(videos_dir):
                    if name in files:
                        video_paths[name] = os.path.relpath(root, videos_dir)
                        break
            
            # Store the relative paths in the config for later use
            config['_video_paths'] = video_paths
            logging.info(f"Found all {len(video_names)} videos in subdirectories")
                
        return video_names

    @staticmethod
    def get_video_path(config: Dict[str, Any], video_name: str) -> str:
        """Get the full path to a video file."""
        videos_dir = config.get('data', {}).get('videos_dir')
        if not videos_dir:
            raise ValueError("Videos directory not specified in config")
            
        # Use stored path from earlier search if available
        video_paths = config.get('_video_paths', {})
        if video_name in video_paths:
            return os.path.join(videos_dir, video_paths[video_name], video_name)
            
        # Fallback to direct path if not found in stored paths
        return os.path.join(videos_dir, video_name)

    @staticmethod
    def get_time_range(config: Dict[str, Any]) -> Optional[tuple[datetime, datetime]]:
        """Get time range from config if specified."""
        time_range = config.get('time_range')
        if not time_range:
            return None
            
        # If time_range is explicitly set to null/None in YAML
        if time_range is None:
            return None
            
        start_time = time_range.get('start')
        end_time = time_range.get('end')
        
        if not (start_time and end_time):
            return None
            
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        return (start, end) 