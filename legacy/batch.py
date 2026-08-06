from typing import List, Dict, Optional, Union, Any, Set
from datetime import datetime
import json
import yaml
import os
import logging
import shutil
from video_data import VideoData
from scripts.sheet_utils import (
    SheetService, load_all_sheet_data, load_config,
    save_sheet_data, load_latest_sheet_data
)
from scripts.process_ndjson import process_ndjson_files

class Batch:
    """A class representing a batch of video objects."""
    
    def __init__(self, videos: Optional[Dict[str, VideoData]] = None):
        """
        Initialize a batch of videos.
        
        Args:
            videos: Optional dictionary mapping video names to VideoData objects
        """
        self.videos: Dict[str, VideoData] = videos if videos is not None else {}
        self._sheet_service = SheetService()

    @classmethod
    def from_configs(cls, config_paths: List[str], ndjson_dir: str, issues_dir: str, 
                    preloaded_sheet_path: Optional[str] = None,
                    save_sheet_data: bool = False,
                    save_batch: bool = False,
                    batch_name: Optional[str] = None) -> 'Batch':
        """Create a batch from NDJSON files and YAML configurations.
        
        Args:
            config_paths: List of paths to YAML configuration files
            ndjson_dir: Directory containing NDJSON files
            issues_dir: Directory containing issue NDJSON files
            preloaded_sheet_path: Optional path to JSON file containing preloaded sheet data
            save_sheet_data: Whether to save loaded sheet data to a JSON file
            save_batch: Whether to save this batch to disk
            batch_name: Name to use for the saved batch (timestamp will be appended)
            
        Returns:
            New Batch instance with filtered videos that meet requirements from configs.
            If no config paths are provided, returns all videos without filtering.
        """
        # Process NDJSON files with YAML configs
        logging.info("Processing NDJSON files...")
        all_videos = process_ndjson_files(
            ndjson_dir, 
            issues_dir, 
            yaml_paths=config_paths, 
            preloaded_sheet_path=preloaded_sheet_path,
            save_sheet_data=save_sheet_data
        )
        logging.info(f"Loaded {len(all_videos)} videos from NDJSON")
        
        # Filter out videos that only have workflow data
        filtered_videos = {}
        for name, video in all_videos.items():
            try:
                if video.has_annotation_data():
                    filtered_videos[name] = video
            except Exception as e:
                logging.warning(f"Error checking video data for {name}: {e}")
                continue
                
        logging.info(f"Filtered out {len(all_videos) - len(filtered_videos)} videos with only workflow data")
        
        # Create batch from filtered videos
        batch = cls(filtered_videos)
        
        # Save batch if requested
        if save_batch:
            if not batch_name:
                raise ValueError("batch_name must be provided when save_batch is True")
            batch.save_batch(batch_name, config_paths, ndjson_dir, issues_dir)
            
        return batch

    def save_batch(self, batch_name: str, config_paths: List[str], ndjson_dir: str, issues_dir: str) -> None:
        """Save the batch to disk.
        
        This creates a new directory under 'batches/' with the batch name and timestamp.
        The directory will contain:
        - The YAML config files used
        - A subset of the NDJSON files containing only the videos in this batch
        - A subset of the issues JSON files if any videos in this batch have issues
        
        Args:
            batch_name: Base name for the batch (timestamp will be appended)
            config_paths: List of paths to YAML config files used to create this batch
            ndjson_dir: Directory containing source NDJSON files
            issues_dir: Directory containing source issues JSON files
        """
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_dir = f"batches/{batch_name}_{timestamp}"
        
        # Create directory structure
        os.makedirs(f"{batch_dir}/batch_configs", exist_ok=True)
        os.makedirs(f"{batch_dir}/ndjson", exist_ok=True)
        os.makedirs(f"{batch_dir}/issues_ndjson", exist_ok=True)
        
        # Copy YAML config files
        for config_path in config_paths:
            config_name = os.path.basename(config_path)
            shutil.copy2(config_path, f"{batch_dir}/batch_configs/{config_name}")
            
        # Get set of video names in this batch
        batch_video_names = set(self.videos.keys())
        
        # Process NDJSON files
        for filename in os.listdir(ndjson_dir):
            if not filename.endswith('.ndjson'):
                continue
                
            input_path = os.path.join(ndjson_dir, filename)
            output_path = os.path.join(batch_dir, "ndjson", filename)
            
            with open(input_path, 'r', encoding='utf-8') as infile, \
                 open(output_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    try:
                        record = json.loads(line.strip())
                        video_id = record.get('data_row', {}).get('id')
                        video_name = record.get('data_row', {}).get('external_id', video_id)
                        if video_name in batch_video_names:
                            outfile.write(line)
                    except Exception as e:
                        logging.error(f"Error processing line in {filename}: {e}")
                        continue
                        
        # Process issues JSON files if they exist
        if os.path.exists(issues_dir):
            for filename in os.listdir(issues_dir):
                if not filename.endswith('_issues.json'):
                    continue
                    
                input_path = os.path.join(issues_dir, filename)
                output_path = os.path.join(batch_dir, "issues_ndjson", filename)
                
                try:
                    # Load all issues from the JSON file
                    with open(input_path, 'r', encoding='utf-8') as f:
                        all_issues = json.load(f)
                    
                    # Filter issues for videos in this batch
                    batch_issues = [
                        issue for issue in all_issues
                        if issue.get('externalDataRowId') in batch_video_names
                    ]
                    
                    # Only write the file if we have matching issues
                    if batch_issues:
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(batch_issues, f, indent=2)
                            
                except Exception as e:
                    logging.error(f"Error processing issues file {filename}: {e}")
                    continue
                            
        logging.info(f"Saved batch to {batch_dir}")

    @staticmethod
    def save_sheet_data(output_file: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Save sheet data to a JSON file for future use.
        
        Args:
            output_file: Path to save the sheet data JSON file
            
        Returns:
            The loaded sheet data that was saved
        """
        # Load config
        config = load_config()
        sheets_config = config.get('google_sheets', {})
        
        # Load all sheet data
        logging.info("Loading sheet data...")
        sheet_data = load_all_sheet_data(sheets_config)
        
        # Save using utility function
        save_sheet_data(sheet_data)
            
        return sheet_data

    @staticmethod
    def load_sheet_data(input_file: str = None) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Load sheet data from a JSON file.
        
        Args:
            input_file: Optional path to the sheet data JSON file. If not provided,
                       loads from the latest sheet data file.
            
        Returns:
            The loaded sheet data
        """
        if input_file:
            logging.info(f"Loading sheet data from {input_file}")
            with open(input_file, 'r') as f:
                return json.load(f)
        else:
            return load_latest_sheet_data()

    def add_video(self, name: str, video: VideoData) -> None:
        """Add a video to the batch."""
        self.videos[name] = video
    
    def remove_video(self, name: str) -> None:
        """Remove a video from the batch."""
        if name in self.videos:
            del self.videos[name]
    
    def get_video(self, name: str) -> Optional[VideoData]:
        """Get a video by name."""
        return self.videos.get(name)
    
    def get_all_videos(self) -> Dict[str, VideoData]:
        """Get all videos in the batch."""
        return self.videos
    
    def get_video_names(self) -> List[str]:
        """Get list of all video names in the batch."""
        return list(self.videos.keys())
    
    def size(self) -> int:
        """Get the number of videos in the batch."""
        return len(self.videos)
    
    def clear(self) -> None:
        """Remove all videos from the batch."""
        self.videos.clear()
    
    def search_videos(self, partial_name: str) -> List[str]:
        """Search for videos containing the given string in their name."""
        return [name for name in self.videos.keys() 
                if partial_name.lower() in name.lower()]

    def save_video_names(self, output_file: str) -> None:
        """Save the list of video names in the batch to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.get_video_names(), f, indent=2)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self):
        return iter(self.videos.items())

    def __getitem__(self, name: str) -> VideoData:
        return self.get_video(name)