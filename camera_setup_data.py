class CameraSetupData:
    def __init__(self):
        # Shot transition options
        self.shot_transition = False # Boolean: True or False
        
        # Lens distortion options
        self.lens_distortion = "regular"  # Options: "regular", "barrel", "fisheye"
        
        # Presence of text or watermarks
        self.has_overlays = False # Boolean: True or False

        # Video speed options
        # Options: "time_lapse", "fast_motion", "regular", "slow_motion", 
        # "stop_motion", "speed_ramp", "time_reversed"
        self.video_speed = "regular"

        # Camera point-of-view options:
        # Options: "unknown", "first_person", "third_person_full_body", "drone_pov",
        # "third_person_over_shoulder", "third_person_over_hip", 
        # "third_person_side_view", "third_person_top_down", 
        # "third_person_isometric", "broadcast_pov", "overhead_pov", 
        # "selfie_pov", "screen_recording", "dashcam_pov", "locked_on_pov"
        self.camera_pov = "unknown"
        
        # Shot type options
        self.shot_type = "human" # Options: "human", "non_human", "change_of_subject", "scenery", "complex"
        
        # Complex shot type options
        # Options: None, "clear_subject_dynamic_size", "different_subject_in_focus", 
        # "clear_subject_atypical", "many_subject_one_focus", "many_subject_no_focus", 
        # "description", "unknown"
        self.complex_shot_type = None # Default: None
        
        # Description type options
        # Options: None, "subject_scene_mismatch", "back_and_forth_change", "others"
        self.shot_size_description_type = None # Default: None

        # Shot size options (start and end)
        # Options: "unknown", "extreme_wide", "wide", "full", "medium_full", "medium",
        # "medium_close_up", "close_up", "extreme_close_up"
        self.shot_size_start = "unknown" 
        self.shot_size_end = "unknown"
        self.shot_size_description = "" # Complex description field

        # Camera height relative to subject (start and end)
        # Options: "unknown", "above_subject", "at_subject", "below_subject"
        self.subject_height_start = "unknown"
        self.subject_height_end = "unknown"
        self.subject_height_description = ""

        # Camera height relative to ground (start and end)
        # Options: "unknown", "aerial_level", "overhead_level", "eye_level", 
        # "hip_level", "ground_level", "water_level", "underwater_level"
        self.overall_height_start = "unknown"
        self.overall_height_end = "unknown"
        self.overall_height_description = ""

        # Camera angle (start and end)
        # Options: "unknown", "bird_eye_angle", "high_angle", "low_angle", "level_angle", "worm_eye_angle"
        self.camera_angle_start = "unknown"
        self.camera_angle_end = "unknown"
        self.camera_angle_description = ""

        # Dutch angle presence
        self.dutch_angle = "no" # Options: "yes", "no", "varying"

        # Camera focus type
        # Options: "unknown", "deep_focus", "shallow_focus", "ultra_shallow_focus"
        self.camera_focus = "unknown"

        # Focus plane at start and end
        # Options: "unknown", "foreground", "middle_ground", "background", "out_of_focus"
        self.focus_plane_start = "unknown"
        self.focus_plane_end = "unknown"
        
        # Focus change reason
        # Options: "no_change", "camera_subject_movement", "rack_focus", "pull_focus", "focus_tracking", "others"
        self.focus_change_reason = "no_change"
        
        self.camera_focus_description = ""

    def set_shot_transition(self, shot_transition):
        if isinstance(shot_transition, bool):
            self.shot_transition = shot_transition
        else:
            raise ValueError("shot_transition must be a boolean value")
    
    def set_lens_distortion(self, distortion):
        valid_options = ["regular", "barrel", "fisheye"]
        if distortion in valid_options:
            self.lens_distortion = distortion
        else:
            raise ValueError(f"Invalid lens distortion option: {distortion}")
    
    def set_has_overlays(self, has_overlays):
        if isinstance(has_overlays, bool):
            self.has_overlays = has_overlays
        else:
            raise ValueError("has_overlays must be a boolean value")
    
    def set_video_speed(self, speed):
        valid_options = ["time_lapse", "fast_motion", "regular", "slow_motion", "stop_motion", "speed_ramp", "time_reversed"]
        if speed in valid_options:
            self.video_speed = speed
        else:
            raise ValueError(f"Invalid video speed option: {speed}")
    
    def set_camera_pov(self, pov):
        valid_options = ["unknown", "first_person", "third_person_full_body", "third_person_over_shoulder",
                         "third_person_over_hip", "third_person_side_view", "third_person_top_down",
                         "third_person_isometric", "broadcast_pov", "overhead_pov", "selfie_pov", "drone_pov",
                         "screen_recording", "dashcam_pov", "locked_on_pov"]
        if pov in valid_options:
            self.camera_pov = pov
        else:
            raise ValueError(f"Invalid camera point-of-view option: {pov}")
    
    def set_shot_type(self, shot_type):
        valid_options = ["human", "non_human", "change_of_subject", "scenery", "complex"]
        if shot_type in valid_options:
            self.shot_type = shot_type
        else:
            raise ValueError(f"Invalid shot type option: {shot_type}")
    
    def set_complex_shot_type(self, complex_shot_type):
        valid_options = [None, "clear_subject_dynamic_size", "different_subject_in_focus", "clear_subject_atypical",
                         "many_subject_one_focus", "many_subject_no_focus", "description", "unknown"]
        if complex_shot_type in valid_options:
            self.complex_shot_type = complex_shot_type
        else:
            raise ValueError(f"Invalid complex shot type option: {complex_shot_type}")
    
    def set_shot_size_start(self, size):
        valid_options = ["unknown", "extreme_wide", "wide", "full", "medium_full", "medium",
                         "medium_close_up", "close_up", "extreme_close_up"]
        if size in valid_options:
            self.shot_size_start = size
        else:
            raise ValueError(f"Invalid shot size start option: {size}")
    
    def set_shot_size_end(self, size):
        valid_options = ["unknown", "extreme_wide", "wide", "full", "medium_full", "medium",
                         "medium_close_up", "close_up", "extreme_close_up"]
        if size in valid_options:
            self.shot_size_end = size
        else:
            raise ValueError(f"Invalid shot size end option: {size}")
    
    def set_shot_size_description_type(self, description_type):
        valid_options = [None, "subject_scene_mismatch", "back_and_forth_change", "others"]
        if description_type in valid_options:
            self.shot_size_description_type = description_type
        else:
            raise ValueError(f"Invalid shot size description type option: {description_type}")
    
    def set_shot_size_description(self, description):
        if isinstance(description, str):
            self.shot_size_description = description
        else:
            raise ValueError("Shot size description must be a string")
    
    def set_subject_height_start(self, height):
        valid_options = ["unknown", "above_subject", "at_subject", "below_subject"]
        if height in valid_options:
            self.subject_height_start = height
        else:
            raise ValueError(f"Invalid subject height start option: {height}")
    
    def set_subject_height_end(self, height):
        valid_options = ["unknown", "above_subject", "at_subject", "below_subject"]
        if height in valid_options:
            self.subject_height_end = height
        else:
            raise ValueError(f"Invalid subject height end option: {height}")
    
    def set_subject_height_description(self, description):
        if isinstance(description, str):
            self.subject_height_description = description
        else:
            raise ValueError("Subject height description must be a string")
    
    def set_overall_height_start(self, height):
        valid_options = ["unknown", "aerial_level", "overhead_level", "eye_level", "hip_level",
                         "ground_level", "water_level", "underwater_level"]
        if height in valid_options:
            self.overall_height_start = height
        else:
            raise ValueError(f"Invalid overall height start option: {height}")
    
    def set_overall_height_end(self, height):
        valid_options = ["unknown", "aerial_level", "overhead_level", "eye_level", "hip_level",
                         "ground_level", "water_level", "underwater_level"]
        if height in valid_options:
            self.overall_height_end = height
        else:
            raise ValueError(f"Invalid overall height end option: {height}")
    
    def set_overall_height_description(self, description):
        if isinstance(description, str):
            self.overall_height_description = description
        else:
            raise ValueError("Overall height description must be a string")
    
    def set_camera_angle_start(self, angle):
        valid_options = ["unknown", "bird_eye_angle", "high_angle", "low_angle", "level_angle", "worm_eye_angle"]
        if angle in valid_options:
            self.camera_angle_start = angle
        else:
            raise ValueError(f"Invalid camera angle start option: {angle}")
    
    def set_camera_angle_end(self, angle):
        valid_options = ["unknown", "bird_eye_angle", "high_angle", "low_angle", "level_angle", "worm_eye_angle"]
        if angle in valid_options:
            self.camera_angle_end = angle
        else:
            raise ValueError(f"Invalid camera angle end option: {angle}")
    
    def set_camera_angle_description(self, description):
        if isinstance(description, str):
            self.camera_angle_description = description
        else:
            raise ValueError("Camera angle description must be a string")
    
    def set_dutch_angle(self, dutch_angle):
        valid_options = ["yes", "no", "varying"]
        if dutch_angle in valid_options:
            self.dutch_angle = dutch_angle
        else:
            raise ValueError(f"Invalid dutch angle option: {dutch_angle}")
    
    def set_camera_focus(self, focus):
        valid_options = ["unknown", "deep_focus", "shallow_focus", "ultra_shallow_focus"]
        if focus in valid_options:
            self.camera_focus = focus
        else:
            raise ValueError(f"Invalid camera focus option: {focus}")
    
    def set_focus_plane_start(self, plane):
        valid_options = ["unknown", "foreground", "middle_ground", "background", "out_of_focus"]
        if plane in valid_options:
            self.focus_plane_start = plane
        else:
            raise ValueError(f"Invalid focus plane start option: {plane}")
    
    def set_focus_plane_end(self, plane):
        valid_options = ["unknown", "foreground", "middle_ground", "background", "out_of_focus"]
        if plane in valid_options:
            self.focus_plane_end = plane
        else:
            raise ValueError(f"Invalid focus plane end option: {plane}")
    
    def set_focus_change_reason(self, reason):
        valid_options = ["no_change", "camera_subject_movement", "rack_focus", "pull_focus", "focus_tracking", "others"]
        if reason in valid_options:
            self.focus_change_reason = reason
        else:
            raise ValueError(f"Invalid focus change reason option: {reason}")
    
    def set_camera_focus_description(self, description):
        if isinstance(description, str):
            self.camera_focus_description = description
        else:
            raise ValueError("Camera focus description must be a string")
    
    @classmethod
    def create(cls, **kwargs):
        """Create a CameraSetupData instance ensuring all attributes are set using setters."""
        instance = cls()
        for key, value in kwargs.items():
            setter_method = getattr(instance, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        instance.verify()
        return instance
    
    def verify(self):
        if self.shot_transition:
            return # No need to verify other fields if shot transition is present
    
        simple_shot_types = ["human", "non_human", "change_of_subject", "scenery"]
        # If shot type is not complex, there should be no complex shot type or description type
        if self.shot_type in simple_shot_types:
            if self.complex_shot_type is not None:
                raise ValueError("Complex shot type should be None for simple shot types")
            if self.shot_size_description_type is not None or self.shot_size_description != "":
                raise ValueError("Shot size description and its type should be None for simple shot types")
            
        else:
            # Complex shot type should not be None
            if self.complex_shot_type is None:
                raise ValueError("Complex shot type should not be None for complex shot types")
            
            if self.complex_shot_type == "description":
                # Description and its type should not be None
                if self.shot_size_description_type is None or self.shot_size_description == "":
                    raise ValueError("Shot size description and its type should not be None for complex shot type 'description'")
            
            if self.complex_shot_type in ["description", "unknown"]:
                # shot_sizes should be "unknown" for complex shot type "description" or "unknown"
                shot_sizes = [self.shot_size_start, self.shot_size_end]
                if any(size != "unknown" for size in shot_sizes):
                    raise ValueError("Shot sizes should be 'unknown' for complex shot type 'description' or 'unknown'")
                
        if self.shot_type == "scenery":
            # Must not have subject height or subject height description
            subject_heights = [self.subject_height_start, self.subject_height_end]
            if any(height != "unknown" for height in subject_heights) or self.subject_height_description != "":
                raise ValueError("Subject height should be 'unknown' for shot type 'scenery' and description should be empty")
            
        if (self.camera_angle_start == "bird_eye_angle" or self.camera_angle_start == "worm_eye_angle") and self.camera_angle_end == "unknown":
            # Bird's / Worm's eye angle should not have dutch angle
            if self.dutch_angle != "no":
                raise ValueError("Bird's eye angle should not have dutch angle")
        
        # Overall height start and end should not be the same unless for "unknown"
        if self.overall_height_start == self.overall_height_end and self.overall_height_start != "unknown":
            raise ValueError("Overall height start and end should not be the same")

        # Camera angle start and end should not be the same unless for "unknown"
        if self.camera_angle_start == self.camera_angle_end and self.camera_angle_start != "unknown":
            raise ValueError("Camera angle start and end should not be the same")

        # Focus plane start and end should not be the same unless for "unknown"
        if self.focus_plane_start == self.focus_plane_end and self.focus_plane_start != "unknown":
            raise ValueError("Focus plane start and end should not be the same")
        
        # For Deep focus, focus plane should be "unknown"
        if self.camera_focus == "deep_focus":
            if self.focus_plane_start != "unknown" or self.focus_plane_end != "unknown":
                raise ValueError("Focus plane should be 'unknown' for deep focus")
        
        # For Shallow/Ultra-Shallow Focus, focus plane start should not be "unknown"
        if self.camera_focus in ["shallow_focus", "ultra_shallow_focus"]:
            if self.focus_plane_start == "unknown":
                raise ValueError("Focus plane start should not be 'unknown' for shallow focus")


camera_setup_params_demo = {
    "shot_transition": False,
    "lens_distortion": "barrel",
    "has_overlays": False,
    "video_speed": "slow_motion",
    "camera_pov": "first_person",
    "shot_type": "complex",
    "complex_shot_type": "clear_subject_dynamic_size",
    "shot_size_start": "wide",
    "shot_size_end": "medium",
    "shot_size_description": "",
    "shot_size_description_type": None,
    "subject_height_start": "above_subject",
    "subject_height_end": "at_subject",
    "subject_height_description": "Subject height changes from above to at",
    "overall_height_start": "eye_level",
    "overall_height_end": "ground_level",
    "overall_height_description": "Overall height changes from eye level to ground level",
    "camera_angle_start": "high_angle",
    "camera_angle_end": "low_angle",
    "camera_angle_description": "Camera angle changes from high to low",
    "dutch_angle": "no",
    "camera_focus": "shallow_focus",
    "focus_plane_start": "foreground",
    "focus_plane_end": "middle_ground",
    "focus_change_reason": "rack_focus",
    "camera_focus_description": "Focus changes from foreground to middle ground"
}
def create_camera_setup_data_demo():
    data = CameraSetupData.create(**camera_setup_params_demo)
    return data

if __name__ == "__main__":
    create_camera_setup_data_demo()

