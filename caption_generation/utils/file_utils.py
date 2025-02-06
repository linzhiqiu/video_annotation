"""Utility functions for file operations in caption generation."""

import os
import logging
from typing import Set, Optional, Dict, Any
import json
from datetime import datetime

def find_video_files(base_dir: str, video_names: Optional[Set[str]] = None) -> Dict[str, str]:
    """Find video files in base directory and its subdirectories.
    
    Args:
        base_dir: Base directory to search in
        video_names: Optional set of video names to filter by
        
    Returns:
        Dictionary mapping video names to their full paths
    """
    video_paths = {}
    
    if not os.path.exists(base_dir):
        logging.warning(f"Base directory not found: {base_dir}")
        return video_paths
        
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.mp4'):
                if video_names is None or file in video_names:
                    video_paths[file] = os.path.join(root, file)
                    
    if video_names and len(video_paths) < len(video_names):
        missing = video_names - set(video_paths.keys())
        logging.warning(f"Could not find {len(missing)} videos: {missing}")
        
    return video_paths

def load_video_names(video_names_file: str) -> Set[str]:
    """Load list of video names from JSON file.
    
    Args:
        video_names_file: Path to JSON file containing video names
        
    Returns:
        Set of video names
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    if not os.path.exists(video_names_file):
        raise FileNotFoundError(f"Video names file not found: {video_names_file}")
        
    with open(video_names_file, 'r') as f:
        video_names = json.load(f)
        if not isinstance(video_names, list):
            raise ValueError("video_names_file must contain a JSON array")
        if not all(isinstance(name, str) for name in video_names):
            raise ValueError("All entries must be strings")
        return set(video_names)

def filter_videos_by_constraints(videos: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Filter videos based on configuration constraints.
    
    Args:
        videos: Dictionary mapping video names to video data
        config: Configuration dictionary with constraints
        
    Returns:
        Filtered dictionary of videos
    """
    filtered = videos.copy()
    
    # Filter by video names from file
    video_names_file = config.get('constraints', {}).get('video_names_file')
    if video_names_file:
        try:
            video_names = load_video_names(video_names_file)
            filtered = {
                name: video 
                for name, video in filtered.items() 
                if name in video_names
            }
            logging.info(f"Filtered to {len(filtered)} videos from {video_names_file}")
        except Exception as e:
            logging.error(f"Error loading video names: {str(e)}")
            return {}
    
    # Filter by approver if specified
    approver = config.get('constraints', {}).get('approver')
    if approver:
        filtered = {
            name: video
            for name, video in filtered.items()
            if hasattr(video, 'workflow_details') and 
               video.workflow_details.approver == approver
        }
        logging.info(f"Filtered to {len(filtered)} videos by approver: {approver}")
    
    # Filter by time range if specified
    time_range = config.get('constraints', {}).get('time_range')
    if time_range and time_range.get('start') and time_range.get('end'):
        start_time = datetime.fromisoformat(time_range['start'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(time_range['end'].replace('Z', '+00:00'))
        
        filtered = {
            name: video
            for name, video in filtered.items()
            if hasattr(video, 'workflow_details') and 
               start_time <= video.workflow_details.approval_time <= end_time
        }
        logging.info(f"Filtered to {len(filtered)} videos in time range")
    
    return filtered 