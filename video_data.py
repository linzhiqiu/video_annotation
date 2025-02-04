from camera_motion_data import CameraMotionData
from camera_setup_data import CameraSetupData
from lighting_setup_data import LightingSetupData

class VideoData:
    def __init__(self):
        self._cam_motion = None  # Short for camera_motion_data
        self._cam_setup = None   # Short for camera_setup_data
        self._light_setup = None  # Short for lighting_setup_data

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
            # Return a default CameraSetupData instance instead of raising an error
            self._cam_setup = CameraSetupData()
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