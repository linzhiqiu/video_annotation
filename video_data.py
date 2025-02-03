from camera_motion_data import CameraMotionData
from camera_setup_data import CameraSetupData
from lighting_setup_data import LightingSetupData
from workflow_data import WorkflowData
from typing import Optional

class VideoData:
    def __init__(self):
        self._cam_motion = None  # Short for camera_motion_data
        self._cam_setup = None   # Short for camera_setup_data
        self._light_setup = None  # Short for lighting_setup_data
        self._video_name: Optional[str] = None
        self._video_url: Optional[str] = None
        self._editing_url: Optional[str] = None
        self._workflow_details: Optional[WorkflowData] = None

    @property
    def cam_motion(self):
        if self._cam_motion is None:
            raise AttributeError("cam_motion has not been set")
        return self._cam_motion

    @cam_motion.setter
    def cam_motion(self, value):
        if isinstance(value, dict):
            self._cam_motion = CameraMotionData.create(**value)  # Auto-create instance
        elif isinstance(value, CameraMotionData):
            self._cam_motion = value
        else:
            raise TypeError("cam_motion must be a CameraMotionData instance or a dictionary of parameters")

    @property
    def cam_setup(self):
        if self._cam_setup is None:
            raise AttributeError("cam_setup has not been set")
        return self._cam_setup

    @cam_setup.setter
    def cam_setup(self, value):
        if isinstance(value, dict):
            self._cam_setup = CameraSetupData.create(**value)  # Auto-create instance
        elif isinstance(value, CameraSetupData):
            self._cam_setup = value
        else:
            raise TypeError("cam_setup must be a CameraSetupData instance or a dictionary of parameters")

    @property
    def light_setup(self):
        if self._light_setup is None:
            raise AttributeError("light_setup has not been set")
        return self._light_setup

    @light_setup.setter
    def light_setup(self, value):
        if isinstance(value, dict):
            self._light_setup = LightingSetupData.create(**value)  # Auto-create instance
        elif isinstance(value, LightingSetupData):
            self._light_setup = value
        else:
            raise TypeError("light_setup must be a LightingSetupData instance or a dictionary of parameters")

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
    def workflow_details(self) -> WorkflowData:
        if self._workflow_details is None:
            raise AttributeError("workflow_details has not been set")
        return self._workflow_details

    @workflow_details.setter
    def workflow_details(self, value):
        if isinstance(value, dict):
            self._workflow_details = WorkflowData.create(**value)
        elif isinstance(value, WorkflowData):
            self._workflow_details = value
        else:
            raise TypeError("workflow_details must be a WorkflowData instance or a dictionary")

    @classmethod
    def create(cls, **kwargs):
        """Create a VideoData instance with all available data."""
        instance = cls()
        
        # Set basic properties
        if 'video_name' in kwargs:
            instance.video_name = kwargs['video_name']
        if 'video_url' in kwargs:
            instance.video_url = kwargs['video_url']
        if 'editing_url' in kwargs:
            instance.editing_url = kwargs['editing_url']
            
        # Set workflow details
        if 'workflow_details' in kwargs:
            instance.workflow_details = kwargs['workflow_details']
            
        # Set existing properties
        if 'cam_motion' in kwargs:
            instance.cam_motion = kwargs['cam_motion']
        if 'cam_setup' in kwargs:
            instance.cam_setup = kwargs['cam_setup']
        if 'light_setup' in kwargs:
            instance.light_setup = kwargs['light_setup']
            
        return instance

def create_video_data_demo():
    video_sample = VideoData()
    from camera_motion_data import camera_motion_params_demo
    print(f"You can initialize cam_motion with a dictionary of parameters or a CameraMotionData instance.")
    print(f"However, you should never create a CameraMotionData instance directly without using its create() function.")
    video_sample.cam_motion = camera_motion_params_demo
    
    print(f"If you try to access cam_setup before setting it, it will raise an Error.")
    try:
        print(video_sample.cam_setup)
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return video_sample

if __name__ == "__main__":
    create_video_data_demo()