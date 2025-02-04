SHOT_SIZES = ["extreme_wide", "wide", "full", "medium_full", "medium", "medium_close_up", "close_up", "extreme_close_up"]
HEIGHT_RELATIVE_TO_SUBJECT = ["above_subject", "at_subject", "below_subject"]
HEIGHT_RELATIVE_TO_GROUND = ["aerial_level", "overhead_level", "eye_level", "hip_level", "ground_level"]
HEIGHT_RELATIVE_TO_WATER = ["water_level", "underwater_level"]
CAMERA_ANGLES = ["bird_eye_angle", "high_angle", "level_angle", "low_angle", "worm_eye_angle"]
FOCUS_PLANES = ["foreground", "middle_ground", "background"]

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
    
    def set_camera_setup_attributes(self):
        self._set_framing_subject_attributes()
        self._set_shot_type_attributes()
        self._set_shot_size_attributes()
        self._set_height_relative_to_subject_attributes()
        self._set_height_relative_to_ground_attributes()
        self._set_camera_angle_attributes()
        self._set_focus_attributes()
    
    def _set_framing_subject_attributes(self):
        self.is_framing_subject = None # "Does the video include one or more subjects in the frame at any point, instead of just a scenery shot with no clear subject?"
        if self.shot_type in ["human", "non_human", "change_of_subject"]:
            self.is_framing_subject = True
        elif self.shot_type in ["scenery"]:
            self.is_framing_subject = False
        elif self.shot_type in ["complex"]:
            if self.complex_shot_type in ["different_subject_in_focus", "clear_subject_dynamic_size", "clear_subject_atypical", "many_subject_one_focus"]:
                self.is_framing_subject = True
            elif self.complex_shot_type == "description" and self.shot_size_description_type in ['subject_scene_mismatch', 'back_and_forth_change']:
                self.is_framing_subject = True
        
        self.has_subject_change = False # "Does the subject change in the video, such as a revealing shot where a subject appears, disappears, or transitions to another subject?"
        if self.shot_type in ["change_of_subject"]:
            self.has_subject_change = True
        elif self.shot_type in ["complex"]:
            if self.complex_shot_type in ["description", "unknown"]:
                self.has_subject_change = None
                
        self.has_single_dominant_subject = None # "Is there a single dominant subject or group of subjects in the frame throughout the video?"
        if self.shot_type in ["human", "non_human"]:
            self.has_single_dominant_subject = True
        elif self.shot_type in ["change_of_subject", "scenery"]:
            self.has_single_dominant_subject = False
        elif self.shot_type in ["complex"]:
            if self.complex_shot_type in ["clear_subject_dynamic_size", "clear_subject_atypical", "many_subject_one_focus"]:
                self.has_single_dominant_subject = True
            elif self.complex_shot_type == "description" and self.shot_size_description_type in ['subject_scene_mismatch', 'back_and_forth_change']:
                self.has_single_dominant_subject = True
        
        self.has_many_subjects = None # "Does the video contain multiple subjects or multiple groups of subjects?"
        if self.shot_type in ["human", "non_human", "scenery"]:
            self.has_many_subjects = False
        elif self.shot_type in ["complex"]:
            if self.complex_shot_type in ["many_subject_one_focus", "many_subject_no_focus", "different_subject_in_focus"]:
                self.has_many_subjects = True
            elif self.complex_shot_type in ["clear_subject_dynamic_size", "clear_subject_atypical"]:
                self.has_many_subjects = False
            elif self.shot_type == "change_of_subject" and self.shot_size_info['start'] != "unknown" and self.shot_size_info['end'] != "unknown":
                self.has_many_subjects = True
            # elif self.complex_shot_type == "description" and self.shot_size_description_type in ['subject_scene_mismatch', 'back_and_forth_change']:
            #     self.has_many_subjects = False
    
    def _set_shot_type_attributes(self): 
        self.is_human_shot = None # "Is the shot focused on human subjects?"
        if self.shot_type in ["human"]:
            self.is_human_shot = True
        elif self.shot_type in ["non_human", "scenery"]:
            self.is_human_shot = False
        
        self.is_non_human_shot = None # "Is the shot focused on non-human subjects?"
        if self.shot_type in ["non_human"]:
            self.is_non_human_shot = True
        elif self.shot_type in ["human", "scenery"]:
            self.is_non_human_shot = False
        
        self.is_just_human_shot = self.shot_type == "human" # "Does the video consistently feature one dominant human subject or a single group of human subjects in the frame?"
        self.is_just_non_human_shot = self.shot_type == "non_human" # "Does the video consistently feature one dominant non-human subject or a single group of non-human subjects in the frame?"
        self.is_just_change_of_subject_shot = self.shot_type == "change_of_subject" # "Does the video include a subject change, such as a revealing shot where a subject appears, disappears, or transitions to another?"
        self.is_just_scenery_shot = self.shot_type == "scenery" # "Does the video focus on scenery or environment without emphasis on any subjects?"
        self.is_just_clear_subject_dynamic_size_shot = self.complex_shot_type == "clear_subject_dynamic_size" # "Does the video feature a clear subject, but changes in framing make shot size classification tricky?"
        self.is_just_different_subject_in_focus_shot = self.complex_shot_type == "different_subject_in_focus" # "Does the video feature different subjects in focus, making it difficult to classify shot size?"
        self.is_just_clear_subject_atypical_shot = self.complex_shot_type == "clear_subject_atypical" # "Is there a clear subject in the video, but its anatomy looks unnatural or exaggerated, as seen in games or CGI?"
        self.is_just_many_subject_one_focus_shot = self.complex_shot_type == "many_subject_one_focus" # "Does the video feature multiple subjects, but one clearly stands out as the main focus?"
        self.is_just_many_subject_no_focus_shot = self.complex_shot_type == "many_subject_no_focus" # "Does the video feature multiple subjects with no clear focus on any one subject?"
        self.is_just_subject_scene_mismatch_shot = self.shot_size_description_type == "subject_scene_mismatch" # "Does the video feature a subject and scene that do not match, making it difficult to classify shot size?"
        self.is_just_back_and_forth_change_shot = self.shot_size_description_type == "back_and_forth_change" # "Does the video have a clear subject with back-and-forth changes in shot size?"
    
    def _set_shot_size_attributes(self):
        self.shot_size_info = {'start': self.shot_size_start, 'end': self.shot_size_end}
        self.is_shot_size_applicable = self.complex_shot_type != "unknown" or (self.complex_shot_type == "description" and self.shot_size_description_type != "others") # "Is shot size classification possible for this video?"
        
        self.subject_revealing = False # "Does the video include a revealing shot where a subject appears?"
        self.subject_disappearing = False # "Does the main subject disappear from the shot?"
        self.subject_switching = False # "Does the main subject change to another subject?"
        self.shot_size_change = False # "Does the shot size change throughout the video?"
        self.shot_size_change_from_large_to_small = False # "Does the shot size change from large to small?"
        self.shot_size_change_from_small_to_large = False # "Does the shot size change from small to large?"
        if self.is_shot_size_applicable:
            if self.shot_type == "change_of_subject":
                if self.shot_size_info['start'] == "unknown":
                    self.subject_revealing = True
                elif self.shot_size_info['end'] == "unknown":
                    self.subject_disappearing = True
                else:
                    self.subject_switching = True
            else:
                if self.shot_size_description_type == "back_and_forth_change":
                    self.shot_size_change = True
                
                if self.shot_size_info['start'] != "unknown":
                    assert self.shot_size_info['end'] != self.shot_size_info['start']
                        
                    if self.shot_size_info['end'] == "unknown":
                        self.shot_size_info['end'] = self.shot_size_info['start']
                    else:
                        self.shot_size_change = True
                        if SHOT_SIZES.index(self.shot_size_info['end']) < SHOT_SIZES.index(self.shot_size_info['start']):
                            self.shot_size_change_from_large_to_small = True
                        else:
                            self.shot_size_change_from_small_to_large = True
        else:
            self.subject_revealing = self.subject_disappearing = self.subject_switching = None
            self.shot_size_change = self.shot_size_change_from_large_to_small = self.shot_size_change_from_small_to_large = None
            
    
    def _set_height_relative_to_subject_attributes(self):
        self.height_wrt_subject_info = {'start': self.subject_height_start, 'end': self.subject_height_end}
        self.is_height_wrt_subject_applicable = any(height != "unknown" for height in self.height_wrt_subject_info.values()) # "Is subject height classification possible for this video?"
        self.height_wrt_subject_change_from_high_to_low = None # "Does the camera height decrease noticeably in relation to the subject?"
        self.height_wrt_subject_change_from_low_to_high = None # "Does the camera height increase noticeably in relation to the subject?"
        if self.is_height_wrt_subject_applicable:
            if self.shot_type == "change_of_subject":
                # change "unknown" to "no_subject"
                for key in self.height_wrt_subject_info:
                    if self.height_wrt_subject_info[key] == "unknown":
                        self.height_wrt_subject_info[key] = "no_subject"
            else:
                if self.height_wrt_subject_info['end'] == "unknown":
                    self.height_wrt_subject_info['end'] = self.height_wrt_subject_info['start']
                else:
                    assert self.height_wrt_subject_info['start'] != self.height_wrt_subject_info['end']
                    if HEIGHT_RELATIVE_TO_SUBJECT.index(self.height_wrt_subject_info['end']) < HEIGHT_RELATIVE_TO_SUBJECT.index(self.height_wrt_subject_info['start']):
                        self.height_wrt_subject_change_from_high_to_low = True
                    else:
                        self.height_wrt_subject_change_from_low_to_high = True
        
    def _set_height_relative_to_ground_attributes(self):
        self.height_wrt_ground_info = {'start': self.overall_height_start, 'end': self.overall_height_end}
        self.is_height_wrt_ground_applicable = any(height != "unknown" for height in self.height_wrt_ground_info.values()) # "Is overall height classification possible for this video?"
        self.height_wrt_ground_change_from_high_to_low = None # "Does the camera height decrease noticeably in relation to the ground?"
        self.height_wrt_ground_change_from_low_to_high = None # "Does the camera height increase noticeably in relation to the ground?"
        self.above_water_to_underwater = None # "Does the camera transition from above water to underwater?"
        self.underwater_to_above_water = None # "Does the camera transition from underwater to above water?"
        if self.is_height_wrt_ground_applicable:
            if self.height_wrt_ground_info['end'] == "unknown":
                self.height_wrt_ground_info['end'] = self.height_wrt_ground_info['start']
                self.above_water_to_underwater = self.underwater_to_above_water = False
            else:
                assert self.height_wrt_ground_info['start'] != self.height_wrt_ground_info['end']
                if all(height in HEIGHT_RELATIVE_TO_WATER for height in self.height_wrt_ground_info.values()):
                    if self.height_wrt_ground_info['end'] == "underwater_level":
                        self.above_water_to_underwater = True
                        self.underwater_to_above_water = False
                    else:
                        self.underwater_to_above_water = True
                        self.above_water_to_underwater = False
                elif all(height in HEIGHT_RELATIVE_TO_GROUND for height in self.height_wrt_ground_info.values()):
                    if HEIGHT_RELATIVE_TO_GROUND.index(self.height_wrt_ground_info['end']) < HEIGHT_RELATIVE_TO_GROUND.index(self.height_wrt_ground_info['start']):
                        self.height_wrt_ground_change_from_high_to_low = True
                    else:
                        self.height_wrt_ground_change_from_low_to_high = True
        
    def _set_camera_angle_attributes(self):
        self.camera_angle_info = {'start': self.camera_angle_start, 'end': self.camera_angle_end}
        self.is_camera_angle_applicable = any(angle != "unknown" for angle in self.camera_angle_info.values()) # "Is camera angle classification possible for this video?"
        self.is_dutch_angle = None # "Is a Dutch angle present in the video?"
        self.is_dutch_angle_varying = None # "Does the degree of the Dutch angle shift throughout the video?"
        self.is_dutch_angle_fixed = None # "Does the Dutch angle remain the same throughout the video?"
        self.camera_angle_change_from_high_to_low = None # "Does the camera angle decrease noticeably relative to the ground?"
        self.camera_angle_change_from_low_to_high = None # "Does the camera angle increase noticeably relative to the ground?"
        if self.is_camera_angle_applicable:
            if self.camera_angle_info['end'] == "unknown":
                self.camera_angle_info['end'] = self.camera_angle_info['start']
            else:
                assert self.camera_angle_info['start'] != self.camera_angle_info['end']
                if CAMERA_ANGLES.index(self.camera_angle_info['end']) < CAMERA_ANGLES.index(self.camera_angle_info['start']):
                    # e.g. low_angle -> high_angle
                    self.camera_angle_change_from_low_to_high = True
                    self.camera_angle_change_from_high_to_low = False
                else:
                    self.camera_angle_change_from_low_to_high = False
                    self.camera_angle_change_from_high_to_low = True
                
            self.is_dutch_angle = self.dutch_angle in ["yes", "varying"]
            self.is_dutch_angle_varying = self.dutch_angle == "varying"
            self.is_dutch_angle_fixed = self.dutch_angle == "yes"
    
    def _set_focus_attributes(self):
        self.focus_info = {'start': self.focus_plane_start, 'end': self.focus_plane_end}
        self.is_focus_applicable = self.camera_focus != "unknown" # "Is camera focus classification possible for this video?"
        self.is_deep_focus = None # "Does the video have a deep depth of field, ensuring distant details remain sharp?"
        self.is_shallow_focus = None # "Is the camera using a shallow depth of field?"
        self.is_ultra_shallow_focus = None # "Does the video have an extremely shallow depth of field?"
        
        self.focus_change_from_near_to_far = None # "Does the focal plane transition from close to distant?"
        self.focus_change_from_far_to_near = None # "Does the focal plane transition from distant to close?"
        self.is_rack_pull_focus = None # "Is rack focus or pull focus used in the video?"
        self.is_focus_tracking = None # "Is there focus tracking on a moving subject in the video?"
        
        if self.is_focus_applicable:
            if self.camera_focus == "deep_focus":
                self.is_deep_focus = True
                self.is_shallow_focus = self.is_ultra_shallow_focus = False
                self.focus_change_from_far_to_near = self.focus_change_from_near_to_far = False
                self.is_rack_pull_focus = self.is_focus_tracking = False
            else:
                self.is_deep_focus = False
                self.is_shallow_focus = True
                self.is_ultra_shallow_focus = self.camera_focus == "ultra_shallow_focus"
                
                assert self.focus_info['start'] != "unknown"
                if self.focus_info['end'] == "unknown":
                    self.focus_info['end'] = self.focus_info['start']
                    # if not middleground or out-of-focus, then we know there is no change in focus
                    if self.focus_info['start'] not in ["middle_ground", "out_of_focus"]:
                        assert self.focus_change_reason == "no_change"
                        self.focus_change_from_near_to_far = self.focus_change_from_far_to_near = False
                        self.is_rack_pull_focus = self.is_focus_tracking = False
                else:
                    if self.focus_change_reason not in ["no_change", "others", "camera_subject_movement"]:
                        self.is_rack_pull_focus = self.focus_change_reason in ["rack_focus", "pull_focus"]
                        self.is_focus_tracking = self.focus_change_reason == "focus_tracking"
                        if all(plane in FOCUS_PLANES for plane in self.focus_info.values()):
                            if FOCUS_PLANES.index(self.focus_plane_end) < FOCUS_PLANES.index(self.focus_plane_start):
                                # e.g. background -> foreground
                                self.focus_change_from_near_to_far = False
                                self.focus_change_from_far_to_near = True
                            else:
                                self.focus_change_from_near_to_far = True
                                self.focus_change_from_far_to_near = False
                    
                    
                    
        
        

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
        instance.set_camera_setup_attributes()
        return instance
    
    def update(self, **kwargs):
        """Update attributes of the CameraSetupData instance."""
        for key, value in kwargs.items():
            setter_method = getattr(self, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        self.verify()
        self.set_camera_setup_attributes()
    
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
            
            if self.shot_type != 'change_of_subject':
                # If ending shot size is not "unknown", make sure it is different from starting shot size
                if self.shot_size_start == self.shot_size_end and self.shot_size_end != "unknown":
                    raise ValueError("Shot size start and end should not be the same for simple shot types")
            else:
                # For change of subject, starting shot size and ending shot size should not both be "unknown"
                if self.shot_size_start == "unknown" and self.shot_size_end == "unknown":
                    raise ValueError("Starting shot size and ending shot size should not both be 'unknown' for shot type 'change_of_subject'")
                
            if self.shot_type in ["non_human", "scenery"]:
                # should not use medium_close_up and medium_full
                if self.shot_size_start in ["medium_close_up", "medium_full"] or self.shot_size_end in ["medium_close_up", "medium_full"]:
                    raise ValueError("Medium close-up and medium full shot sizes should not be used for shot types 'non_human' and 'scenery'")
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
        elif self.shot_type == "change_of_subject":
            shot_size_info = [self.shot_size_start != "unknown", self.shot_size_end != "unknown"]
            subject_height_info = [self.subject_height_start != "unknown", self.subject_height_end != "unknown"]
            # For change of subject, subject_height_info must follow the shot_size_info
            if shot_size_info != subject_height_info:
                raise ValueError("Subject height should be 'unknown' if shot size is 'unknown' for shot type 'change_of_subject'")
        elif self.shot_type in ['human', 'non_human'] or self.complex_shot_type in ["many_subject_one_focus", "clear_subject_dynamic_size", "clear_subject_atypical"]:
            # starting subject height should not be "unknown"
            if self.subject_height_start == "unknown":
                raise ValueError("Subject height start should not be 'unknown' for shot types 'human', 'non_human', 'many_subject_one_focus', 'clear_subject_dynamic_size', 'clear_subject_atypical'")
        elif self.complex_shot_type in ["different_subject_in_focus"]:
            # if starting subject height is "unknown", must have a description
            if self.subject_height_start == "unknown" and self.subject_height_description == "":
                raise ValueError("Subject height start should not be 'unknown' without a description for complex shot type 'different_subject_in_focus'")
            
            
            
        if (self.camera_angle_start == "bird_eye_angle" or self.camera_angle_start == "worm_eye_angle") and self.camera_angle_end == "unknown":
            # Bird's / Worm's eye angle should not have dutch angle
            if self.dutch_angle != "no":
                raise ValueError("Bird's or worm's eye angle should not have dutch angle")
        
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
            if self.focus_change_reason != "no_change":
                raise ValueError("Focus change reason should be 'no_change' for deep focus")
        
        # For Shallow/Ultra-Shallow Focus, focus plane start should not be "unknown"
        if self.camera_focus in ["shallow_focus", "ultra_shallow_focus"]:
            if self.focus_plane_start == "unknown":
                raise ValueError("Focus plane start should not be 'unknown' for shallow focus")
            if self.focus_plane_start != self.focus_plane_end:
                if self.focus_change_reason == "no_change":
                    raise ValueError("Focus change reason should not be 'no_change' for focus plane change")
            if self.focus_plane_end == "unknown":
                # meaning there should be no focus plane change except for middleground
                if self.focus_change_reason != "no_change" and self.focus_plane_start not in ["middle_ground", "out_of_focus"]:
                    raise ValueError("Focus plane must not change except for middle ground")


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

