from camera_motion_data import CameraMotionData
from camera_setup_data import CameraSetupData
from lighting_setup_data import LightingSetupData
from workflow_data import WorkflowData

class VideoData:
    def __init__(self):
        # Data objects for each annotation type
        self._cam_motion = None  # Short for camera_motion_data
        self._cam_setup = None   # Short for camera_setup_data
        self._light_setup = None  # Short for lighting_setup_data
        
        # Single list to store all workflow data
        self._workflows = []

    @property
    def workflows(self):
        return self._workflows

    def add_workflow(self, workflow_data):
        """Add a workflow to the video's workflow list."""
        if isinstance(workflow_data, dict):
            workflow = WorkflowData.create(**workflow_data)
        elif isinstance(workflow_data, WorkflowData):
            workflow = workflow_data
        else:
            raise TypeError("workflow_data must be a WorkflowData instance or a dictionary of parameters")
        
        # Check if we already have a workflow for this project
        for existing_workflow in self._workflows:
            if existing_workflow.project_name == workflow.project_name:
                # If new workflow has more recent approval time, replace the old one
                if (workflow.approval_time and 
                    (not existing_workflow.approval_time or 
                     workflow.approval_time > existing_workflow.approval_time)):
                    self._workflows.remove(existing_workflow)
                    self._workflows.append(workflow)
                return
        
        # If no existing workflow for this project, add the new one
        self._workflows.append(workflow)

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

    def update_workflow_from_project(self, project_name: str, workflow_data: dict):
        """
        Update workflow data based on project name, using the mappings defined in project_mappings.yaml
        This method should be implemented by the batch processing code that has access to the mappings
        """
        pass

    def has_annotation_data(self) -> bool:
        """
        Check if the video has any annotation data besides workflows.
        Returns True if any of cam_motion, cam_setup, or light_setup are set.
        """
        if self._cam_motion is not None:
            return True
        if self._cam_setup is not None:
            return True
        if self._light_setup is not None:
            return True
        return False

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