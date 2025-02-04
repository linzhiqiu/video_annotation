from typing import List, Dict, Optional, Union
from datetime import datetime
from video_data import VideoData

class Batch:
    """A class representing a batch of video objects."""
    
    def __init__(self, videos: Optional[Dict[str, VideoData]] = None):
        """
        Initialize a batch of videos.
        
        Args:
            videos: Optional dictionary mapping video names to VideoData objects
        """
        self.videos: Dict[str, VideoData] = videos if videos is not None else {}

    @classmethod
    def create(cls, 
               all_videos: Dict[str, VideoData],
               video_names: Optional[List[str]] = None,
               approver: Optional[str] = None,
               time_range: Optional[tuple[datetime, datetime]] = None) -> 'Batch':
        """
        Create a batch of videos based on specified constraints.
        
        Args:
            all_videos: Dictionary of all available videos
            video_names: Optional list of specific video names to include
            approver: Optional approver name to filter by
            time_range: Optional tuple of (start_time, end_time) to filter by approval time
            
        Returns:
            A new Batch instance containing the filtered videos
        """
        filtered_videos = {}
        
        # Start with either specified videos or all videos
        videos_to_check = {name: video for name, video in all_videos.items() 
                          if video_names is None or name in video_names}
        
        # Apply filters
        for name, video in videos_to_check.items():
            try:
                workflow = video.workflow_details
                
                # Check approver constraint
                if approver and workflow.approver != approver:
                    continue
                    
                # Check time range constraint
                if time_range:
                    start_time, end_time = time_range
                    approval_time = workflow.approval_time
                    if not (start_time <= approval_time <= end_time):
                        continue
                
                # All constraints passed, add to filtered videos
                filtered_videos[name] = video
                
            except AttributeError:
                # Skip videos without workflow details
                continue
        
        return cls(filtered_videos)

    @classmethod
    def from_video_names(cls, all_videos: Dict[str, VideoData], video_names: List[str]) -> 'Batch':
        """Create a batch from a list of video names."""
        return cls.create(all_videos, video_names=video_names)

    @classmethod
    def from_approver(cls, all_videos: Dict[str, VideoData], approver: str) -> 'Batch':
        """Create a batch containing all videos approved by a specific approver."""
        return cls.create(all_videos, approver=approver)

    @classmethod
    def from_time_range(cls, all_videos: Dict[str, VideoData], 
                       start_time: datetime, end_time: datetime) -> 'Batch':
        """Create a batch containing all videos approved within a time range."""
        return cls.create(all_videos, time_range=(start_time, end_time))

    def add_video(self, name: str, video: VideoData) -> None:
        """
        Add a video to the batch.
        
        Args:
            name: Name/ID of the video
            video: VideoData object
        """
        self.videos[name] = video
    
    def remove_video(self, name: str) -> None:
        """
        Remove a video from the batch.
        
        Args:
            name: Name/ID of the video to remove
        """
        if name in self.videos:
            del self.videos[name]
    
    def get_video(self, name: str) -> Optional[VideoData]:
        """
        Get a video by name.
        
        Args:
            name: Name/ID of the video
            
        Returns:
            VideoData object if found, None otherwise
        """
        return self.videos.get(name)
    
    def get_all_videos(self) -> Dict[str, VideoData]:
        """
        Get all videos in the batch.
        
        Returns:
            Dictionary of all videos
        """
        return self.videos
    
    def get_video_names(self) -> List[str]:
        """
        Get list of all video names in the batch.
        
        Returns:
            List of video names
        """
        return list(self.videos.keys())
    
    def size(self) -> int:
        """
        Get the number of videos in the batch.
        
        Returns:
            Number of videos
        """
        return len(self.videos)
    
    def clear(self) -> None:
        """Remove all videos from the batch."""
        self.videos.clear()
    
    def search_videos(self, partial_name: str) -> List[str]:
        """
        Search for videos containing the given string in their name.
        
        Args:
            partial_name: String to search for in video names
            
        Returns:
            List of matching video names
        """
        return [name for name in self.videos.keys() 
                if partial_name.lower() in name.lower()]

    def __len__(self) -> int:
        return self.size()

    def __iter__(self):
        return iter(self.videos.items())

    def __getitem__(self, name: str) -> VideoData:
        return self.get_video(name)