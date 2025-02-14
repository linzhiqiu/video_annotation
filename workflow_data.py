from typing import List, Optional
from datetime import datetime
import logging

class WorkflowData:
    """Class for storing essential workflow-related data for a video."""
    
    def __init__(self):
        self._video_name: Optional[str] = None
        self._video_url: Optional[str] = None
        self._editing_url: Optional[str] = None
        self._approver: Optional[str] = None
        self._approval_time: Optional[datetime] = None
        self._labelers: List[str] = []
        self._project_name: Optional[str] = None

    @property
    def video_name(self) -> str:
        if self._video_name is None:
            raise AttributeError("video_name has not been set")
        return self._video_name

    @video_name.setter
    def video_name(self, value: str):
        self._video_name = value

    @property
    def video_url(self) -> str:
        if self._video_url is None:
            raise AttributeError("video_url has not been set")
        return self._video_url

    @video_url.setter
    def video_url(self, value: str):
        self._video_url = value

    @property
    def editing_url(self) -> str:
        if self._editing_url is None:
            raise AttributeError("editing_url has not been set")
        return self._editing_url

    @editing_url.setter
    def editing_url(self, value: str):
        self._editing_url = value

    @property
    def approver(self) -> str:
        if self._approver is None:
            raise AttributeError("approver has not been set")
        return self._approver

    @approver.setter
    def approver(self, value: str):
        self._approver = value

    @property
    def approval_time(self) -> datetime:
        return self._approval_time  # Allow None values

    @approval_time.setter
    def approval_time(self, value: str):
        if value is None:
            self._approval_time = None
            return
            
        if isinstance(value, str):
            try:
                self._approval_time = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError as e:
                logging.error(f"Invalid approval_time format: {value}")
                self._approval_time = None
        elif isinstance(value, datetime):
            self._approval_time = value
        else:
            raise TypeError("approval_time must be a string or datetime object")

    @property
    def labelers(self) -> List[str]:
        return self._labelers

    @labelers.setter
    def labelers(self, value: List[str]):
        self._labelers = value

    @property
    def project_name(self) -> str:
        if self._project_name is None:
            raise AttributeError("project_name has not been set")
        return self._project_name

    @project_name.setter
    def project_name(self, value: str):
        self._project_name = value

    @classmethod
    def create(cls, **kwargs):
        """Create a WorkflowData instance from a dictionary of parameters."""
        instance = cls()
        
        if 'video_name' in kwargs:
            instance.video_name = kwargs['video_name']
            
        if 'video_url' in kwargs:
            instance.video_url = kwargs['video_url']
            
        if 'editing_url' in kwargs:
            instance.editing_url = kwargs['editing_url']
            
        if 'approver' in kwargs:
            instance.approver = kwargs['approver']
            
        if 'approval_time' in kwargs:
            instance.approval_time = kwargs['approval_time']
            
        if 'labelers' in kwargs:
            instance.labelers = kwargs['labelers']
            
        if 'project_name' in kwargs:
            instance.project_name = kwargs['project_name']
            
        return instance

    def __repr__(self):
        return (
            f"WorkflowData(video_name='{self._video_name}', "
            f"video_url='{self._video_url}', "
            f"editing_url='{self._editing_url}', "
            f"approver='{self._approver}', "
            f"approval_time='{self._approval_time}', "
            f"project_name='{self._project_name}', "
            f"labelers={self._labelers})"
        ) 