from typing import List

class CameraMotionData:
    def __init__(self):
        # Is labeled?
        self.is_labeled = True # Boolean: True or False

        # Shot transition options
        self.shot_transition = None # Boolean: True or False

        # Scene movement options
        self.scene_movement = "unknown"  # Options: "static", "mostly_static", "dynamic", "unknown"

        # Camera steadiness options
        self.steadiness = "static"  # Options: "static", "very_smooth", "smooth", "unsteady", "very_unsteady"

        # Camera movement options
        self.camera_movement = "no"  # Options: "no", "major_complex", "major_simple", "minor"

        # Camera motion speed options
        self.camera_motion_speed = "regular"  # Options: "slow", "regular", "fast"

        # Camera tracking options
        self.is_tracking = None  # Boolean: True or False
        self.tracking_shot_types = []  # Options: "side", "tail", "lead", "aerial", "arc", "pan", "tilt"

        # Subject size change options (only for tracking shots)
        self.subject_size_change = "no"  # Options: "no", "larger", "smaller"

        # Camera direction movement options
        self.camera_forward_backward = "no"  # Options: "no", "forward", "backward"
        self.camera_forward_backward_cam_frame = "no"  # Options: "no", "forward", "backward", "unknown"
        self.camera_zoom = "no"  # Options: "no", "in", "out"
        self.camera_left_right = "no"  # Options: "no", "left_to_right", "right_to_left"
        self.camera_pan = "no"  # Options: "no", "left_to_right", "right_to_left"
        self.camera_up_down = "no"  # Options: "no", "up", "down"
        self.camera_up_down_cam_frame = "no"  # Options: "no", "up", "down", "unknown"
        self.camera_tilt = "no"  # Options: "no", "up", "down"
        self.camera_arc = "no"  # Options: "no", "clockwise", "counter_clockwise"
        self.camera_crane = "no"  # Options: "no", "crane_up", "crane_down"
        self.camera_roll = "no"  # Options: "no", "clockwise", "counter_clockwise"

        # Camera motion effects as booleans
        self.frame_freezing = None
        self.dolly_zoom = None
        self.motion_blur = None
        self.cinemagraph = None

        # Text box for complex descriptions
        self.complex_motion_description = ""

        # # Camera Motion List (ground_based)
        # self.camera_motion_list = [
        #     "forward", "backward", "zoom_in", "zoom_out", "up", "down",
        #     "tilt_up", "tilt_down","roll_cw", "roll_ccw",
        #     "pan_right", "pan_left", "left", "right"
        # ]
        #
        # # Camera motion List (camera_based)
        # self.camera_motion_cam_list = [
        #     "zoom_in", "zoom_out", "tilt_up", "tilt_down", "left", "right",
        #     "up_cam", "down_cam", "forward_cam", "backward_cam",
        #     "roll_cw", "roll_ccw", "pan_right", "pan_left"
        # ]

    def set_camera_motion_attributes(self):
        self.set_basic_camera_motion_attributes() # This must be called first
        self.set_steadiness_and_movement_attributes()
        self.set_scene_movement_attributes()
        self.set_object_centric_movement_attributes()
        self.set_motion_complexity_attributes()
    
    def set_motion_complexity_attributes(self):
        attributes = [
            'is_simple_motion', 'is_complex_motion', 'is_minor_motion', 
        ]
        # if shot_transition is True, all attributes should be None
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return
        
        self.is_simple_motion = self.camera_movement == 'major_simple'
        self.is_complex_motion = self.camera_movement == 'major_complex'
        if self.camera_movement == 'minor':
            self.is_minor_motion = True
        elif self.camera_movement != 'minor' and self.steadiness not in ['unsteady', 'very_unsteady']:
            self.is_minor_motion = False
        else:
            self.is_minor_motion = None

    def set_object_centric_movement_attributes(self):
        attributes = [
            'not_a_tracking_shot', 'aerial_tracking_shot', 'arc_tracking_shot', 'front_side_tracking_shot', 'rear_side_tracking_shot',
            'lead_tracking_shot', 'other_tracking_shots_than_lead', 'tail_tracking_shot', 'tilt_tracking_shot',
            'side_tracking_shot', 'pan_tracking_shot', 'other_tracking_shots_than_pan', 'side_but_not_pan_tracking_shot', 'other_tracking_shots_than_tilt',
            'other_tracking_shots_than_front_side', 'other_tracking_shots_than_rear_side', 'other_tracking_shots_than_side', 'other_tracking_shots_than_tail',
            'lead_but_not_side_tracking_shot', 'side_but_not_lead_tracking_shot',
            'aerial_but_not_tilt_tracking_shot', 'side_but_not_tilt_tracking_shot',
            'tail_but_not_side_tracking_shot', 'side_but_not_tail_tracking_shot', 'pan_but_not_side_tracking_shot',
            'side_tracking_shot_leftward', 'side_tracking_shot_rightward',
            'pan_left_but_not_side_tracking_shot', 'pan_right_but_not_side_tracking_shot',
            'tracking_shot', 'tracking_subject_larger_size', 'tracking_subject_smaller_size', 'tracking_subject_gets_smaller_or_same', 'tracking_subject_gets_larger_or_same'
        ]
        # if shot_transition is True, all attributes should be None
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return

        self.aerial_tracking_shot = "aerial" in self.tracking_shot_types
        self.arc_tracking_shot = 'arc' in self.tracking_shot_types
        if self.tracking_shot_types == ['lead']:
            self.lead_tracking_shot = True
        elif 'lead' not in self.tracking_shot_types:
            self.lead_tracking_shot = False
        else:
            self.lead_tracking_shot = None

        if self.tracking_shot_types == ['pan']:
            self.pan_tracking_shot = True
        elif 'pan' not in self.tracking_shot_types:
            self.pan_tracking_shot = False
        else:
            self.pan_tracking_shot = None
        
        if self.tracking_shot_types == ['side']:
            self.side_tracking_shot = True
        elif 'side' not in self.tracking_shot_types:
            self.side_tracking_shot = False
        else:
            self.side_tracking_shot = None
        
        if self.tracking_shot_types == ['tail']:
            self.tail_tracking_shot = True
        elif 'tail' not in self.tracking_shot_types:
            self.tail_tracking_shot = False
        else:
            self.tail_tracking_shot = None
            
        if self.tracking_shot_types == ['tilt']:
            self.tilt_tracking_shot = True
        elif 'tilt' not in self.tracking_shot_types:
            self.tilt_tracking_shot = False
        else:
            self.tilt_tracking_shot = None
            
        if self.is_tracking and 'side' in self.tracking_shot_types and self.left is True:
            self.side_tracking_shot_leftward = True
        elif not (self.is_tracking and 'side' in self.tracking_shot_types and self.left is True):
            self.side_tracking_shot_leftward = False
        else:
            self.side_tracking_shot_leftward = None
        
        if self.is_tracking and 'side' in self.tracking_shot_types and self.right is True:
            self.side_tracking_shot_rightward = True
        elif not (self.is_tracking and 'side' in self.tracking_shot_types and self.right is True):
            self.side_tracking_shot_rightward = False
        else:
            self.side_tracking_shot_rightward = None

        self.front_side_tracking_shot = set(self.tracking_shot_types) == {'lead', 'side'}
        self.rear_side_tracking_shot = set(self.tracking_shot_types) == {'tail', 'side'}
        
        self.tracking_shot = self.is_tracking
        self.tracking_subject_larger_size = self.is_tracking and self.subject_size_change == 'larger'
        self.tracking_subject_smaller_size = self.is_tracking and self.subject_size_change == 'smaller'
        
        # Unused attributes just for analysis
        self.not_a_tracking_shot = self.is_tracking is False
        self.other_tracking_shots_than_lead = self.is_tracking and 'lead' not in self.tracking_shot_types
        self.other_tracking_shots_than_pan = self.is_tracking and not 'pan' in self.tracking_shot_types
        self.other_tracking_shots_than_front_side = self.is_tracking and not ('lead' in self.tracking_shot_types and 'side' in self.tracking_shot_types)
        self.other_tracking_shots_than_rear_side = self.is_tracking and not ('tail' in self.tracking_shot_types and 'side' in self.tracking_shot_types)
        self.other_tracking_shots_than_side = self.is_tracking and not ('side' in self.tracking_shot_types)
        self.other_tracking_shots_than_tail = self.is_tracking and not ('tail' in self.tracking_shot_types)
        self.other_tracking_shots_than_tilt = self.is_tracking and not ('tilt' in self.tracking_shot_types)
        self.aerial_but_not_tilt_tracking_shot = 'aerial' in self.tracking_shot_types and 'tilt' not in self.tracking_shot_types
        self.side_but_not_tilt_tracking_shot = 'side' in self.tracking_shot_types and 'tilt' not in self.tracking_shot_types
        self.side_but_not_pan_tracking_shot = 'side' in self.tracking_shot_types and 'pan' not in self.tracking_shot_types
        self.lead_but_not_side_tracking_shot = 'lead' in self.tracking_shot_types and 'side' not in self.tracking_shot_types
        self.side_but_not_lead_tracking_shot = 'side' in self.tracking_shot_types and 'lead' not in self.tracking_shot_types
        self.tail_but_not_side_tracking_shot = 'tail' in self.tracking_shot_types and 'side' not in self.tracking_shot_types
        self.side_but_not_tail_tracking_shot = 'side' in self.tracking_shot_types and 'tail' not in self.tracking_shot_types
        self.pan_but_not_side_tracking_shot = 'pan' in self.tracking_shot_types and 'side' not in self.tracking_shot_types
        self.pan_left_but_not_side_tracking_shot = 'pan' in self.tracking_shot_types and self.pan_left is True and 'side' not in self.tracking_shot_types
        self.pan_right_but_not_side_tracking_shot = 'pan' in self.tracking_shot_types and self.pan_right is True and 'side' not in self.tracking_shot_types
        self.tracking_subject_gets_smaller_or_same = self.is_tracking and self.subject_size_change != 'larger'
        self.tracking_subject_gets_larger_or_same = self.is_tracking and self.subject_size_change != 'smaller'
        

    def set_scene_movement_attributes(self):
        attributes = [
            'static_scene', 'mostly_static_scene', 'dynamic_scene'
        ]
        # if shot_transition is True, all attributes should be None
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return

        if self.scene_movement in ['dynamic']:
            self.dynamic_scene = True
        elif self.scene_movement in ['static']:
            self.dynamic_scene = False
        else:
            self.dynamic_scene = None

        if self.scene_movement in ['mostly_static', 'static']:
            self.mostly_static_scene = True
        elif self.scene_movement in ['dynamic']:
            self.mostly_static_scene = False
        else:
            self.mostly_static_scene = None

        if self.scene_movement in ['static']:
            self.static_scene = True
        elif self.scene_movement in ['mostly_static', 'dynamic']:
            self.static_scene = False
        else:
            self.static_scene = None

    def set_steadiness_and_movement_attributes(self):
        attributes = [
            'clear_moving_camera', 'fast_moving_camera', 'fixed_camera_with_shake', 'not_fixed_camera', 'fixed_without_shaking', 'shaky_camera_that_moves',
            'fixed_camera', 'fixed_but_slightly_shaky', 'moving_camera', 'shaky_camera', 'not_shaky_camera_excluding_smooth', 'slow_moving_camera',
            'stable_camera_motion', 'fixed_camera_without_motion', 'quite_shaky_camera', 'very_shaky_camera', 'not_very_shaky_camera_excluding_smooth', 
            'very_stable_camera_motion', 'somewhat_shaky_camera', 'static_camera'
        ]
        # if shot_transition is True, all attributes should be None
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return

        if self.camera_movement in ['major_simple'] or (self.steadiness not in ['static'] and self.camera_movement in ['major_complex']):
            self.clear_moving_camera = True
        elif self.steadiness in ['static', 'smooth'] and self.camera_movement in ['no']:
            self.clear_moving_camera = False
        else:
            self.clear_moving_camera = None

        if (self.camera_movement in ['major_simple'] or (self.steadiness not in ['static'] and self.camera_movement in ['major_complex'])) and self.camera_motion_speed == 'fast':
            self.fast_moving_camera = True
        elif (self.steadiness in ['static', 'smooth'] and self.camera_movement in ['no']) or (self.camera_movement in ['major_simple', 'major_complex'] and self.camera_motion_speed != 'fast'):
            self.fast_moving_camera = False
        else:
            self.fast_moving_camera = None

        if self.steadiness in ['smooth', 'unsteady'] and self.camera_movement in ['no']:
            self.fixed_camera_with_shake = True
        elif self.steadiness in ['static', 'very_smooth'] or (self.steadiness in ['smooth', 'unsteady', 'very_unsteady'] and self.camera_movement not in ['no', 'minor']):
            self.fixed_camera_with_shake = False
        else:
            self.fixed_camera_with_shake = None

        if self.steadiness in ['static'] and self.camera_movement in ['no']:
            self.fixed_camera = True
        elif self.steadiness not in ['static']:
            self.fixed_camera = False
        else:
            self.fixed_camera = None

        if (self.steadiness not in ['static'] and self.camera_movement in ['minor', 'major_simple', 'major_complex']) or (self.steadiness in ['unsteady', 'very_unsteady'] and self.camera_movement in ['no']):
            self.moving_camera = True
        elif self.steadiness in ['static'] and self.camera_movement in ['no']:
            self.moving_camera = False
        else:
            self.moving_camera = None

        if self.steadiness in ['unsteady', 'very_unsteady']:
            self.shaky_camera = True
        elif self.steadiness not in ['unsteady', 'very_unsteady']:
            self.shaky_camera = False
        else:
            self.shaky_camera = None

        if (self.camera_movement in ['major_simple'] or (self.steadiness not in ['static'] and self.camera_movement in ['major_complex'])) and self.camera_motion_speed == 'slow':
            self.slow_moving_camera = True
        elif (self.steadiness in ['static', 'smooth'] and self.camera_movement in ['no']) or (self.camera_movement in ['major_simple', 'major_complex'] and self.camera_motion_speed != 'slow'):
            self.slow_moving_camera = False
        else:
            self.slow_moving_camera = None

        if self.steadiness in ['smooth', 'very_smooth'] and self.camera_movement not in ['no']:
            self.stable_camera_motion = True
        elif self.steadiness not in ['smooth', 'very_smooth'] or self.camera_movement in ['no']:
            self.stable_camera_motion = False
        else:
            self.stable_camera_motion = None

        if self.steadiness in ['very_unsteady']:
            self.very_shaky_camera = True
        elif self.steadiness not in ['very_unsteady', 'unsteady']:
            self.very_shaky_camera = False
        else:
            self.very_shaky_camera = None

        if self.steadiness in ['very_smooth'] and self.camera_movement not in ['no']:
            self.very_stable_camera_motion = True
        elif self.steadiness not in ['very_smooth', 'smooth'] or self.camera_movement in ['no']:
            self.very_stable_camera_motion = False
        else:
            self.very_stable_camera_motion = None

        # Unused attributes just for analysis
        self.not_fixed_camera = self.steadiness in ['static', 'very_smooth'] and self.camera_movement not in ['no']
        self.fixed_without_shaking = self.steadiness in ['static'] and self.camera_movement in ['no']
        self.shaky_camera_that_moves = self.steadiness in ['smooth', 'unsteady', 'very_unsteady'] and self.camera_movement not in ['no', 'minor']
        self.fixed_but_slightly_shaky = self.steadiness in ['smooth', 'unsteady'] and self.camera_movement in ['no']
        self.not_shaky_camera_excluding_smooth = self.steadiness not in ['smooth', 'unsteady', 'very_unsteady']
        self.fixed_camera_without_motion = self.steadiness in ['static'] or self.camera_movement in ['no']
        self.quite_shaky_camera = self.steadiness in ['unsteady', 'very_unsteady']
        self.not_very_shaky_camera_excluding_smooth = self.steadiness in ['smooth', 'very_smooth']
        self.somewhat_shaky_camera = self.steadiness in ['unsteady', 'very_unsteady']
        self.static_camera = self.steadiness in ['static'] and self.frame_freezing is False

    
    def set_basic_camera_motion_attributes(self):
        # Initialize all attributes to False
        attributes = [
            "forward", "backward", "zoom_in", "zoom_out", "up", "down", "tilt_up", "tilt_down", 
            "roll_cw", "roll_ccw", "crane_up", "crane_down", "arc_cw", "arc_ccw", "up_cam", "down_cam", 
            "forward_cam", "backward_cam", "pan_right", "pan_left", "left", "right"
        ]

        # if shot_transition is True, or is_labeled is False, all attributes should be None
        if self.shot_transition is True or self.is_labeled is False:
            for attr in attributes:
                setattr(self, attr, None)
            return

        # If steadiness is "static" or camera movement is "no", all should be False
        if self.steadiness == "static" or self.camera_movement == "no":
            for attr in attributes:
                setattr(self, attr, False)
            return

        # If arc or crane shot, all attributes except for arc and crane should be None
        if self.camera_arc != "no" or self.camera_crane != "no":
            for attr in attributes:
                setattr(self, attr, None)

            # Then set arc and crane motion. First because arc and crane will not co-occur, we can set them directly
            if self.camera_arc != "no":
                setattr(self, "arc_cw", self.camera_arc == "clockwise")
                setattr(self, "arc_ccw", self.camera_arc == "counter_clockwise")
            else:
                setattr(self, "crane_up", self.camera_crane == "crane_up")
                setattr(self, "crane_down", self.camera_crane == "crane_down")
        else:
            # First set arc and crane to False
            setattr(self, "arc_cw", False)
            setattr(self, "arc_ccw", False)
            setattr(self, "crane_up", False)
            setattr(self, "crane_down", False)

            uncertain_if_no = self.steadiness in ["unsteady", "very_unsteady"] or self.camera_movement in ["major_complex", "minor"]
            uncertain_if_gt = self.camera_movement in ["minor"]

            def set_motion(attr, answer, gt):
                if answer == "no" and uncertain_if_no:
                    value = None
                elif answer == "unknown":
                    value = None
                else:
                    value = answer == gt
                    if value and uncertain_if_gt:
                        value = None

                setattr(self, attr, value)

            set_motion("forward", self.camera_forward_backward, "forward")
            set_motion("backward", self.camera_forward_backward, "backward")
            set_motion("forward_cam", self.camera_forward_backward_cam_frame, "forward")
            set_motion("backward_cam", self.camera_forward_backward_cam_frame, "backward")
            set_motion("zoom_in", self.camera_zoom, "in")
            set_motion("zoom_out", self.camera_zoom, "out")
            set_motion("up", self.camera_up_down, "up")
            set_motion("down", self.camera_up_down, "down")
            set_motion("up_cam", self.camera_up_down_cam_frame, "up")
            set_motion("down_cam", self.camera_up_down_cam_frame, "down")
            set_motion("tilt_up", self.camera_tilt, "up")
            set_motion("tilt_down", self.camera_tilt, "down")
            set_motion("roll_cw", self.camera_roll, "clockwise")
            set_motion("roll_ccw", self.camera_roll, "counter_clockwise")
            set_motion("pan_right", self.camera_pan, "left_to_right")
            set_motion("pan_left", self.camera_pan, "right_to_left")
            set_motion("right", self.camera_left_right, "left_to_right")
            set_motion("left", self.camera_left_right, "right_to_left")

    def set_is_labeled(self, is_labeled):
        if isinstance(is_labeled, bool):
            self.is_labeled = is_labeled
        else:
            raise ValueError("is_labeled must be a boolean value")

    def set_steadiness(self, steadiness):
        valid_options = ["static", "very_smooth", "smooth", "unsteady", "very_unsteady"]
        if steadiness in valid_options:
            self.steadiness = steadiness
        else:
            raise ValueError(f"Invalid steadiness option: {steadiness}")

    def set_scene_movement(self, scene_movement):
        valid_options = ["static", "mostly_static", "dynamic", "unknown"]
        if scene_movement in valid_options:
            self.scene_movement = scene_movement
        else:
            raise ValueError(f"Invalid scene_movement option: {scene_movement}")

    def set_camera_movement(self, movement):
        valid_options = ["no", "major_complex", "major_simple", "minor"]
        if movement in valid_options:
            self.camera_movement = movement
        else:
            raise ValueError(f"Invalid camera movement option: {movement}")

    def set_camera_motion_speed(self, speed):
        valid_options = ["slow", "regular", "fast"]
        if speed in valid_options:
            self.camera_motion_speed = speed
        else:
            raise ValueError(f"Invalid camera motion speed option: {speed}")

    def set_shot_transition(self, shot_transition):
        if isinstance(shot_transition, bool):
            self.shot_transition = shot_transition
        else:
            raise ValueError("shot_transition must be a boolean value")

    def set_is_tracking(self, is_tracking):
        if isinstance(is_tracking, bool):
            self.is_tracking = is_tracking
        else:
            raise ValueError("is_tracking must be a boolean value")

    def set_subject_size_change(self, size_change):
        valid_options = ["no", "larger", "smaller"]
        if size_change in valid_options:
            self.subject_size_change = size_change
        else:
            raise ValueError(f"Invalid subject size change option: {size_change}")

    def set_camera_forward_backward(self, direction):
        valid_options = ["no", "forward", "backward"]
        if direction in valid_options:
            self.camera_forward_backward = direction
        else:
            raise ValueError(f"Invalid camera forward/backward option: {direction}")

    def set_camera_forward_backward_cam_frame(self, direction):
        valid_options = ["no", "forward", "backward", "unknown"]
        if direction in valid_options:
            self.camera_forward_backward_cam_frame = direction
        else:
            raise ValueError(f"Invalid camera forward/backward (camera-centric) option: {direction}")

    def set_camera_zoom(self, zoom):
        valid_options = ["no", "in", "out"]
        if zoom in valid_options:
            self.camera_zoom = zoom
        else:
            raise ValueError(f"Invalid camera zoom option: {zoom}")

    def set_camera_left_right(self, direction):
        valid_options = ["no", "left_to_right", "right_to_left"]
        if direction in valid_options:
            self.camera_left_right = direction
        else:
            raise ValueError(f"Invalid camera left_right option: {direction}")

    def set_camera_pan(self, direction):
        valid_options = ["no", "left_to_right", "right_to_left"]
        if direction in valid_options:
            self.camera_pan = direction
        else:
            raise ValueError(f"Invalid camera pan option: {direction}")

    def set_camera_up_down(self, direction):
        valid_options = ["no", "up", "down"]
        if direction in valid_options:
            self.camera_up_down = direction
        else:
            raise ValueError(f"Invalid camera up_down option: {direction}")

    def set_camera_up_down_cam_frame(self, direction):
        valid_options = ["no", "up", "down", "unknown"]
        if direction in valid_options:
            self.camera_up_down_cam_frame = direction
        else:
            raise ValueError(f"Invalid camera up_down (camera-centric) option: {direction}")

    def set_camera_tilt(self, direction):
        valid_options = ["no", "up", "down"]
        if direction in valid_options:
            self.camera_tilt = direction
        else:
            raise ValueError(f"Invalid camera tilt option: {direction}")

    def set_camera_arc(self, direction):
        valid_options = ["no", "clockwise", "counter_clockwise"]
        if direction in valid_options:
            self.camera_arc = direction
        else:
            raise ValueError(f"Invalid camera arc option: {direction}")

    def set_camera_crane(self, direction):
        valid_options = ["no", "crane_up", "crane_down"]
        if direction in valid_options:
            self.camera_crane = direction
        else:
            raise ValueError(f"Invalid camera crane option: {direction}")

    def set_camera_roll(self, direction):
        valid_options = ["no", "clockwise", "counter_clockwise"]
        if direction in valid_options:
            self.camera_roll = direction
        else:
            raise ValueError(f"Invalid camera roll option: {direction}")

    def set_tracking_shot_types(self, types):
        valid_options = ["side", "tail", "lead", "aerial", "arc", "pan", "tilt"]
        if all(t in valid_options for t in types):
            self.tracking_shot_types = types
        else:
            raise ValueError(f"Invalid tracking shot types: {types}")

    def set_frame_freezing(self, freezing):
        if isinstance(freezing, bool):
            self.frame_freezing = freezing
        else:
            raise ValueError("frame_freezing must be a boolean value")

    def set_dolly_zoom(self, dolly_zoom):
        if isinstance(dolly_zoom, bool):
            self.dolly_zoom = dolly_zoom
        else:
            raise ValueError("dolly_zoom must be a boolean value")

    def set_motion_blur(self, motion_blur):
        if isinstance(motion_blur, bool):
            self.motion_blur = motion_blur
        else:
            raise ValueError("motion_blur must be a boolean value")

    def set_cinemagraph(self, cinemagraph):
        if isinstance(cinemagraph, bool):
            self.cinemagraph = cinemagraph
        else:
            raise ValueError("cinemagraph must be a boolean value")

    def set_complex_motion_description(self, description):
        if isinstance(description, str):
            self.complex_motion_description = description
        else:
            raise ValueError("Complex motion description must be a string")

    def camera_motion_dict_cam(self):
        return{
            'forward_cam': self.forward_cam,
            'backward_cam': self.backward_cam,
            'zoom_in': self.zoom_in,
            'zoom_out': self.zoom_out,
            'up_cam': self.up_cam,
            'down_cam': self.down_cam,
            'tilt_up': self.tilt_up,
            'tilt_down': self.tilt_down,
            'pan_right': self.pan_right,
            'pan_left': self.pan_left,
            'roll_cw': self.roll_cw,
            'roll_ccw': self.roll_ccw,
            'left': self.left,
            'right': self.right
        }

    def camera_motion_dict(self):
        return{
            'forward': self.forward,
            'backward': self.backward,
            'zoom_in': self.zoom_in,
            'zoom_out': self.zoom_out,
            'up': self.up,
            'down': self.down,
            'tilt_up': self.tilt_up,
            'tilt_down': self.tilt_down,
            'roll_cw': self.roll_cw,
            'roll_ccw': self.roll_ccw,
            'pan_right': self.pan_right,
            'pan_left': self.pan_left,
            'left': self.left,
            'right': self.right
        }

    def check_if_no_motion(self, exclude: List[str] = []):
        return all(value == False for motion, value in self.camera_motion_dict().items() if motion not in exclude)

    def check_if_no_motion_cam(self, exclude: List[str] = []):
        return all(value == False for motion, value in self.camera_motion_dict_cam().items() if motion not in exclude)

    def get_raw_camera_motion_list(self):
        return [self.camera_forward_backward, self.camera_zoom, self.camera_left_right,
                self.camera_pan, self.camera_up_down, self.camera_tilt, self.camera_arc,
                self.camera_crane, self.camera_roll]

    @classmethod
    def create(cls, **kwargs):
        """Create a CameraMotionData instance ensuring all attributes are set using setters and are verified."""
        instance = cls()
        for key, value in kwargs.items():
            setter_method = getattr(instance, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        instance.verify()
        instance.set_camera_motion_attributes()
        return instance

    def update(self, **kwargs):
        """Update attributes of the CameraMotionData instance."""
        for key, value in kwargs.items():
            setter_method = getattr(self, f"set_{key}", None)
            if setter_method and callable(setter_method):
                setter_method(value)
            else:
                raise AttributeError(f"Invalid attribute: {key} or setter method not found")
        self.verify()
        self.set_camera_motion_attributes()

    def verify(self):
        if self.shot_transition is True or self.is_labeled is False:
            return # No need to verify if shot transition is True or is_labeled is False
        
        if self.steadiness == "static" and self.camera_movement in ["major_simple", "minor"]:
            raise ValueError("When steadiness is 'static', camera_movement cannot be 'major_simple' or 'minor'.")

        if not self.is_tracking:
            if self.tracking_shot_types:
                raise ValueError("When is_tracking is False, tracking_shot_types must be an empty list.")
            if self.subject_size_change != "no":
                raise ValueError("When is_tracking is False, subject_size_change must be 'no'.")

        if self.camera_movement == "major_complex":
            if not self.complex_motion_description:
                raise ValueError("When camera_movement is 'major_complex', complex_motion_description must not be empty.")
        else:
            if self.complex_motion_description:
                raise ValueError("When camera_movement is not 'major_complex', complex_motion_description must be empty.")

        camera_movements = self.get_raw_camera_motion_list()
        if self.camera_movement == "major_simple":
            if all(movement == "no" for movement in camera_movements):
                raise ValueError("When camera_movement is 'major_simple', at least one direction movement must be specified.")

        if self.camera_movement == "no":
            if any(movement != "no" for movement in camera_movements):
                raise ValueError("When camera_movement is 'no', all direction movements must be 'no'.")

            if self.steadiness in ["very_smooth"]:
                raise ValueError("When camera_movement is 'no', steadiness cannot be 'very_smooth'.")

        if self.dolly_zoom:
            if not ((self.camera_zoom == "out" and self.camera_forward_backward == "forward") or \
                (self.camera_zoom == "in" and self.camera_forward_backward == "backward")):
                raise ValueError("For dolly_zoom effect, camera_zoom and camera_forward_backward must be in opposite directions.")
            elif self.camera_zoom == "no" or self.camera_forward_backward == "no":
                raise ValueError("For dolly_zoom effect, both camera_zoom and camera_forward_backward must be specified.")

camera_motion_params_demo = {
    "shot_transition": False,
    "steadiness": "smooth",
    "scene_movement": "static",
    "camera_movement": "major_complex",
    "camera_motion_speed": "regular",
    "is_tracking": True,
    "tracking_shot_types": ["side", "tail"],
    "subject_size_change": "larger",
    "camera_forward_backward": "forward",
    "camera_forward_backward_cam_frame": "unknown",
    "camera_zoom": "out",
    "camera_left_right": "no",
    "camera_pan": "no",
    "camera_up_down": "no",
    "camera_up_down_cam_frame": "unknown",
    "camera_tilt": "no",
    "camera_arc": "no",
    "camera_crane": "no",
    "camera_roll": "no",
    "dolly_zoom": True,
    "motion_blur": True,
    "complex_motion_description": "The camera starts with a dolly-in and transitions to a crane-down."
}
def create_camera_motion_data_demo():
    data = CameraMotionData.create(**camera_motion_params_demo)
    return data

if __name__ == "__main__":
    create_camera_motion_data_demo()
