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
            
        # Validate required paths
        data_config = config.get('data', {})
        ndjson_dir = data_config.get('ndjson_dir')
        if not ndjson_dir or not os.path.isdir(ndjson_dir):
            raise FileNotFoundError(f"NDJSON directory not found: {ndjson_dir}")
        
        issues_dir = data_config.get('issues_dir')
        if not issues_dir or not os.path.isdir(issues_dir):
            raise FileNotFoundError(f"Issues directory not found: {issues_dir}")
        
        # Videos directory is now optional
        videos_dir = data_config.get('videos_dir')
        if videos_dir:
            logging.info(f"Checking videos directory: {videos_dir}")
            if not os.path.isdir(videos_dir):
                logging.warning(f"Videos directory not found: {videos_dir}")
        
        # Validate labels configuration
        if 'labels' not in config:
            raise ValueError("No labels specified in config")
        if not isinstance(config['labels'], list):
            raise ValueError("Labels must be a list")
        if not config['labels']:
            raise ValueError("Labels list is empty")
        
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
        
        return video_names

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