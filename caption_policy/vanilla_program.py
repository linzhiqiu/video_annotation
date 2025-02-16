from video_data import VideoData
from typing import List, Dict
import json
import os

def read_text_file(file_path: str) -> str:
    """Reads and returns the content of a text file as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def read_json_file(file_path: str) -> Dict:
    """Reads and returns the content of a JSON file as a dictionary."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
class SocraticProgram:
    def __init__(self, name: str, info: str, caption_fields: List[str]):
        self.name = name
        self.info = info
        self.caption_fields = caption_fields
    
    def __str__(self):
        return f"{self.name}: {self.info} \n Caption Fields: {self.caption_fields}"

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        raise NotImplementedError("Subclasses must implement this method")

# class VanillaPolicy(SocraticProgram):
#     def __init__(self):
#         name = "Vanilla Program based on existing labels"
#         info = "A program that prompts VLMs to provide structured captions for Caption Everything."
#         self.caption_fields_dict = {
#             "subject_description": "subject description",
#             "subject_motion_dynamics": "subject motion and dynamics",
#             "scene_composition_dynamics": "scene composition and dynamics",
#             "spatial_framing_dynamic": "spatial framing and dynamics",
#             "camera_motion_dynamics": "camera motion and dynamics",
#         }
#         caption_fields = list(self.caption_fields_dict.keys())
#         super().__init__(name, info, caption_fields)
    
#     def __call__(self, data: VideoData) -> Dict[str, str]:
#         """Given a VideoData instance, return a dictionary of prompts for structured captions."""
#         if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
#             raise ValueError("Shot transitions are not supported in this policy.")

#         subject_description_policy = self.get_subject_description_policy(data)
#         subject_motion_dynamics_policy = self.get_subject_motion_dynamics_policy(data)
#         scene_composition_dynamics_policy = self.get_scene_composition_dynamics_policy(data)
#         spatial_framing_dynamics_policy = self.get_spatial_framing_dynamics_policy(data)
#         camera_framing_dynamics_policy = self.get_camera_framing_dynamics_policy(data)
#         return {**subject_description_policy, **scene_composition_dynamics_policy, **camera_framing_dynamics_policy}
        
#     def get_subject_description_policy(self, data: VideoData):
#         subject_policy = VanillaSubjectPolicy()
#         return subject_policy(data)
    
#     def get_subject_motion_dynamics_policy(self, data: VideoData):
#         subject_motion_policy = VanillaSubjectMotionPolicy()
#         return subject_motion_policy(data)
    
#     def get_scene_composition_dynamics_policy(self, data: VideoData):
#         scene_policy = VanillaScenePolicy()
#         return scene_policy(data)
    
#     def get_spatial_framing_dynamics_policy(self, data: VideoData):
#         spatial_policy = VanillaSpatialPolicy()
#         return spatial_policy(data)
    
#     def get_camera_framing_dynamics_policy(self, data: VideoData):
#         camera_policy = VanillaCameraPolicy()
#         return camera_policy(data)
    

class VanillaSubjectPolicy(SocraticProgram):
    def __init__(self):
        name = "Vanilla Subject Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Subject."
        caption_fields = ["subject_description"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "subject_description": self.get_description(data)
        }
    
    def get_description(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        if data.cam_setup.is_framing_subject is False:
            # This much be a Scenery shot
            return ("The video is a scenery shot. You do not need to describe the subject. "
                    "Please concisely specify the type of scenery shot (e.g., a landscape or cityscape scenery shot)."
                    "Explain why there is no main subject, such as the focus being on the environment, atmosphere, "
                    "or scale rather than a specific object. If relevant, describe the shot's purpose, whether it is an "
                    "establishing shot setting the scene or providing context, or a FPV shot that creates an immersive experience.")
        
        policy = read_text_file("caption_policy/policy/subject_description/policy.txt")
        if data.cam_setup.is_framing_subject is None:
            # Including complex shot with description others, or multiple subject without a clear focus
            # If is others description, then prompt to use this description to complement the subject description
            # Note that there may not be a subject in focus. 
            if data.cam_setup.shot_size_description_type == "others":
                pass # Do nothing
            elif data.cam_setup.is_just_many_subject_no_focus_shot:
                policy += "\n Please note that this video contains **multiple subjects without a clear main focus**. Briefly describe the salient subjects while providing a concise overview of secondary subjects, or describe all subjects collectively as a group if that is more appropriate."
                return policy
            else:
                raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        if data.cam_setup.is_just_human_shot:
            policy += "\n Please note that the video features salient **human** subjects, so the description should focus on them."
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n Please note that the video features salient **non-human** subjects, so the description should focus on them."
        elif data.cam_setup.is_just_change_of_subject_shot:
            if data.cam_setup.subject_revealing:
                policy += "\n Please note that the video is a **revealing shot of the subject**, so the description should reflect this by explaining how the subject is revealed through either subject movement or camera movement."
            elif data.cam_setup.subject_hiding:
                policy += "\n Please note that the video features the main subjects **disappearing from the frame**, so the description should reflect this by explaining how they exit, whether through subject movement or camera movement."
            elif data.cam_setup.subject_switching:
                policy += "\n Please note that the video features the main subjects **switching from one to another**, so the description should reflect this by explaining how the transition occurs, whether through subject movement or camera movement."
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_hiding, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n Please note that the **main subject’s framing is not stable** throughout the video, so the description should reflect this."
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n Please note that the main subjects in this video exhibit **atypical posture or anatomy**, so the description should reflect this."
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n Please note that the video features **multiple subjects with a clear main focus**, so the description should focus on the main subject while providing a concise overview of secondary subjects."
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n Please note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types and relationships."
        else:
            assert data.cam_setup.shot_size_description != ""
            policy += "\n" + read_text_file("caption_policy/policy/subject_description/has_shot_size_description.txt").format(shot_size_description=data.cam_setup.shot_size_description)
        return policy


class VanillaScenePolicy(SocraticProgram):
    def __init__(self):
        name = "Vanilla Scene Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Scene."
        caption_fields = ["scene_composition_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        policy = {
            "scene_composition_dynamics": self.get_description(data)
        }
        return policy

    def get_description(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        true_pov_attribute = data.cam_setup.true_pov_attribute
        pov_info = read_json_file(os.path.join("labels/cam_setup/point_of_view", f"{true_pov_attribute}.json"))['def_prompt'][0]
        
        policy = read_text_file("caption_policy/policy/scene_composition_dynamics/policy.txt").format(pov_description=pov_info)
        return policy


class VanillaSubjectMotionPolicy(SocraticProgram):
    def __init__(self):
        name = "Vanilla Subject Motion & Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Subject Motion and Dynamics."
        caption_fields = ["subject_motion_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "subject_motion_dynamics": self.get_description(data)
        }
    
    def get_description(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        if data.cam_setup.is_framing_subject is False:
            # This much be a Scenery shot
            return ("The video is a scenery shot. You do not need to describe the subject motion. ")
        
        
        policy = read_text_file("caption_policy/policy/subject_motion_dynamics/policy.txt")
        if data.cam_setup.is_framing_subject is None:
            # Including complex shot with description others, or multiple subject without a clear focus
            # If is others description, then prompt to use this description to complement the subject description
            # Note that there may not be a subject in focus. 
            if data.cam_setup.shot_size_description_type == "others":
                pass # Do nothing
            elif data.cam_setup.is_just_many_subject_no_focus_shot:
                policy += "\n Please note that this video contains **multiple subjects without a clear main focus**. Briefly describe the salient motions and dynamics of the primary subjects while providing a concise overview of secondary movements, or describe all subjects' collective motion if that is more appropriate."
                return policy
            else:
                raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        if data.cam_setup.is_just_human_shot:
            policy += "\n Please note that the video features salient **human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n Please note that the video features salient **non-human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_change_of_subject_shot:
            if data.cam_setup.subject_revealing:
                policy += "\n Please note that the video is a **revealing shot of the subject**, so the description should reflect this by explaining how the subject is revealed through either subject movement or camera movement."
            elif data.cam_setup.subject_hiding:
                policy += "\n Please note that the video features the main subjects **disappearing from the frame**, so the description should reflect this by explaining how they exit, whether through subject movement or camera movement."
            elif data.cam_setup.subject_switching:
                policy += "\n Please note that the video features the main subjects **switching from one to another**, so the description should first describe the first subject’s motion and dynamics, followed by the second’s."
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_hiding, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n Please note that the **main subject’s framing is not stable** throughout the video, so the description should reflect how their motion and dynamics contribute to this instability."
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n Please note that the main subjects in this video exhibit **atypical motion, posture, or anatomy**, so the description should reflect this."
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n Please note that the video features **multiple subjects with a clear main focus**, so the description should focus on the motion and dynamics of the main subject while providing a concise overview of secondary subjects' movements."
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n Please note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types, movement patterns, and interactions."
        else:
            # pass for complex shot with description
            pass
                
        assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        policy += "\n" + read_text_file("caption_policy/policy/subject_motion_dynamics/has_subject_description.txt").format(subject_description=data.cam_setup.subject_description)
        return policy


class VanillaSpatialPolicy(SocraticProgram):
    def __init__(self):
        name = "Vanilla Spatial Framing and Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Spatial Framing and Dynamics."
        caption_fields = ["spatial_framing_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "spatial_framing_dynamics": self.get_description(data)
        }
    
    def format_shot_size(self, shot_size: str) -> str:
        # Options: "unknown", "extreme_wide", "wide", "full", "medium_full", "medium",
        # "medium_close_up", "close_up", "extreme_close_up"
        shot_size_info = {
            "unknown": "unknown",
            "extreme_wide": "an extreme wide shot",
            "wide": "a wide shot",
            "full": "a full shot",
            "medium_full": "a medium full shot",
            "medium": "a medium shot",
            "medium_close_up": "a medium close-up shot",
            "close_up": "a close-up shot",
            "extreme_close_up": "an extreme close-up shot"
        }
        return shot_size_info[shot_size]
    
    def format_height_wrt_subject(self, height: str) -> str:
        # Options: "unknown", "above_subject", "at_subject", "below_subject"
        height_info = {
            "unknown": "unknown",
            "above_subject": "above the subject",
            "at_subject": "at the subject's level",
            "below_subject": "below the subject"
        }
        return height_info[height]
    
    def get_description(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        policy = ""
        policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_subject.txt")
        policy += "\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scene.txt")
        policy += "\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/movement.txt")
        # if data.cam_setup.is_framing_subject is False:
        #     # This much be a Scenery shot
        #     policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scene.txt")
        # else:
        #     policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_subject.txt")
        
        
        # if data.cam_setup.is_framing_subject is None:
        #     # Including complex shot with description others, or multiple subject without a clear focus
        #     # If is others description, then prompt to use this description to complement the subject description
        #     # Note that there may not be a subject in focus. 
        #     if data.cam_setup.shot_size_description_type == "others":
        #         pass # Do nothing
        #     elif data.cam_setup.is_just_many_subject_no_focus_shot:
        #         policy += "\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scenery.txt")
        #         policy += "\n Please note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
        #     else:
        #         raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        assert data.cam_setup.scene_description != "", "Scene description must be provided before subject motion and dynamics description."
        policy += "\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/has_subject_scene_description.txt").format(
            subject_description=data.cam_setup.subject_description,
            scene_description=data.cam_setup.scene_description
        )

        shot_size_change = data.cam_setup.shot_size_change
        subject_status = None # 'has_subject', 'no_subject', 'change_of_subject', 'has_description'
        is_height_wrt_subject_applicable = data.cam_setup.is_height_wrt_subject_applicable
        
        if data.cam_setup.is_just_human_shot:
            policy += "\n Please note that the video features **salient human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n Please note that the video features **salient non-human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_change_of_subject_shot:
            subject_status = "change_of_subject"
            if data.cam_setup.subject_revealing:
                policy += "\n Please note that the video is a **revealing shot of the subject**."
                policy += "\n Shot Size Information: The video begins with no subject. It then becomes {} of the subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_height_wrt_subject_applicable:
                    policy += "\n When the subject is revealed, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            elif data.cam_setup.subject_hiding:
                policy += "\n Please note that the video features **main subjects disappearing from the frame**."
                policy += "\n Shot Size Information: The video begins with {} of the subject. Then the subject disappears.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start'])
                )
                if is_height_wrt_subject_applicable:
                    policy += "\n Before the subject disappears, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_switching:
                policy += "\n Please note that the video features **main subjects switching from one to another**."
                policy += "\n Shot Size Information: The video begins with {} of the first subject. Then it becomes {} of the second subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_height_wrt_subject_applicable:
                    policy += "\n The camera is positioned {} when the first subject is in focus, and {} when the second subject is in focus.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_hiding, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n Please note that the **main subject’s framing (shot size) is not stable** throughout the video, so the description should emphasize this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n Please note that the **main subjects exhibit atypical posture or anatomy**, so the description should reflect this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n Please note that the video features **multiple subjects with a clear main focus**, so the description should focus on the main subject."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n Please note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types and relationships."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_no_focus_shot:
            policy += "\n Please note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
            subject_status = "no_subject"
        else:
            # pass for complex shot with description
            subject_status = "has_description"
            policy += "\n The description below already mentions the spatial framing information about the subjects or scenery in this video. Use this caption as a reference to draft the spatial framing and dynamics description. Simply expand on it to fully capture other spatial positions and movements. Do not infer the any spatial framing information already mentioned below."
            policy += f"\n\n Shot Size Information: {data.cam_setup.shot_size_description}"
            if is_height_wrt_subject_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n Camera Height Relative to Subjects: The camera is initially positioned {} and then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n Camera Height Relative to Subjects: The camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n Camera Height Relative to Subjects: {data.cam_setup.subject_height_description}"
                
        
        if subject_status == "has_subject":
            if shot_size_change:
                policy += "\n Shot Size Information: The video begins with {} of the subjects. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n Shot Size Information: The video shows {} of the subjects.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))
                
            if is_height_wrt_subject_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n Camera Height Relative to Subjects: The camera is initially positioned {}. It then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n Camera Height Relative to Subjects: The camera is positioned {}.".format(self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']))
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n Camera Height Relative to Subjects: {data.cam_setup.subject_height_description}"
        elif subject_status == None or subject_status == "no_subject":
            if shot_size_change:
                policy += "\n Shot Size Information: The video begins with {} of the scenery. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n Shot Size Information: The video shows {} of the scenery.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))
                
            if is_height_wrt_subject_applicable:
                raise ValueError("Height relative to subject is not applicable when there is no subject.")
        
        return policy

    

class VanillaCameraPolicy(SocraticProgram):
    def __init__(self):
        name = "Vanilla Camera Framing and Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Camera Framing and Dynamics."
        caption_fields = ["camera_framing_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "camera_framing_dynamics": self.get_description(data)
        }
        
    def format_playback_speed(self, speed: str, speed_dir="labels/cam_setup/video_speed/") -> str:
        # Options: "time_lapse", "fast_motion", "regular", "slow_motion", 
        # "stop_motion", "speed_ramp", "time_reversed"
        speed_info = {
            "time_lapse": "time_lapse",
            "fast_motion": "fast_motion_without_time_lapse",
            "regular": "regular_speed",
            "slow_motion": "slow_motion",
            "stop_motion": "stop_motion",
            "speed_ramp": "speed_ramp",
            "time_reversed": "time_reversed"
        }
        speed = speed_info[speed]
        speed_str = read_json_file(os.path.join(speed_dir, f"{speed}.json"))['def_prompt'][0]
        if speed == "regular_speed":
            speed_str += " (no need to mention)."
        return speed_str
    
    def format_lens_distortion(self, lens_distortion: str) -> str:
        # Options: "regular", "barrel", "fisheye"
        if lens_distortion == "regular":
            return "No lens distortion (no need to mention)."
        elif lens_distortion == "barrel":
            return "The video features mild barrel distortion causing straight lines near the edges to bow outward."
        elif lens_distortion == "fisheye":
            return "The video features noticable fisheye distortion causing straight lines to curve outward."
        raise ValueError("Invalid lens distortion type.")
    
    def format_camera_height_start(self, height: str) -> str:
        # Options: "unknown", "aerial_level", "overhead_level", "eye_level", 
        # "hip_level", "ground_level", "water_level", "underwater_level"
        height_info = {
            "aerial_level": "at an aerial level",
            "overhead_level": "at an overhead level (around second floor height)",
            "eye_level": "at an eye level (above the waist)",
            "hip_level": "at a hip level (below the waist and above the knees)",
            "ground_level": "at a ground level",
            "water_level": "above water",
            "underwater_level": "underwater"
        }
        if height == "unknown":
            raise ValueError("Camera height cannot be unknown.")
        return height_info[height]
    
    def format_camera_height_end(self, height: str) -> str:
        # Options: "unknown", "aerial_level", "overhead_level", "eye_level", 
        # "hip_level", "ground_level", "water_level", "underwater_level"
        height_info = {
            "aerial_level": "to an aerial level",
            "overhead_level": "to an overhead level (around second floor height)",
            "eye_level": "to an eye level (above the waist)",
            "hip_level": "to a hip level (below the waist and above the knees)",
            "ground_level": "to a ground level",
            "water_level": "above water",
            "underwater_level": "underwater"
        }
        if height == "unknown":
            raise ValueError("Camera height cannot be unknown.")
        return height_info[height]
    
    def format_camera_angle(self, angle: str) -> str:
        # Options: "unknown", "bird_eye_angle", "high_angle", "low_angle", "level_angle", "worm_eye_angle"
        angle_info = {
            "bird_eye_angle": "a bird's-eye view angle (looking down directly at the ground)",
            "high_angle": "a high angle (looking down from above)",
            "level_angle": "a level angle (looking straight ahead)",
            "low_angle": "a low angle (looking up from below)",
            "worm_eye_angle": "a worm's-eye view angle (looking directly up)"
        }
        if angle == "unknown":
            raise ValueError("Camera angle cannot be unknown.")
        return angle_info[angle]
    
    def format_focus_plane(self, plane: str) -> str:
        # Options: "unknown", "foreground", "middle_ground", "background", "out_of_focus"
        focus_plane_info = {
            "foreground": "focused on the foreground",
            "middle_ground": "focused on the midground",
            "background": "focused on the background",
            "out_of_focus": "out of focus"
        }
        if plane == "unknown":
            raise ValueError("Focus plane cannot be unknown.")
        return focus_plane_info[plane]

    def format_camera_steadiness(self, steadiness: str) -> str:
        # Options: "static", "very_smooth", "smooth", "unsteady", "very_unsteady"
        steadiness_info = {
            "very_smooth": "very smooth with no shaking",
            "smooth": "smooth with minimal shaking",
            "unsteady": "slightly unsteady with some shaking",
            "very_unsteady": "unsteady with noticeable shaking"
        }
        if steadiness == "static":
            raise ValueError("Camera steadiness cannot be static.")
        return steadiness_info[steadiness]

    def format_camera_motion_speed(self, speed: str) -> str:
        # Options: "slow", "regular", "fast"
        speed_info = {
            "slow": "moving slowly.",
            "regular": "moving at a regular speed (no need to mention).",
            "fast": "moving quickly."
        }
        return speed_info[speed]
    
    def get_movement_description(self, data: VideoData) -> str:
        # Get a video description using the existing labels.
        # Turn attributes like forward to a phrase like "moving forward"
        # Only call this function for simple or minor motion
        # attributes = [
        #     "forward", "backward", "zoom_in", "zoom_out", "up", "down", "tilt_up", "tilt_down", 
        #     "roll_cw", "roll_ccw", "crane_up", "crane_down", "arc_cw", "arc_ccw", "up_cam", "down_cam", 
        #     "forward_cam", "backward_cam", "pan_right", "pan_left", "left", "right"
        # ]
        movement_info = {
            "roll_cw": "rolling clockwise",
            "roll_ccw": "rolling counterclockwise",
            "forward": "moving forward",
            "backward": "moving backward",
            "zoom_in": "zooming in",
            "zoom_out": "zooming out",
            "up": "moving up",
            "down": "moving down",
            "tilt_up": "tilting up",
            "tilt_down": "tilting down",
            "pan_right": "panning right",
            "pan_left": "panning left",
            "left": "moving left",
            "right": "moving right",
            "crane_up": "craning up",
            "crane_down": "craning down",
            "arc_cw": "arcing clockwise",
            "arc_ccw": "arcing counterclockwise",
            # "up_cam": "moving the camera up",
            # "down_cam": "moving the camera down",
            # "forward_cam": "moving the camera forward",
            # "backward_cam": "moving the camera backward",
        }
        true_movement = [key for key in movement_info.keys() if getattr(data.cam_motion, key) is True]
        if len(true_movement) == 0:
            return "The camera shows no clear or intentional movement."
        else:
            # For one movement: The caption should be like "The camera is **moving forward**."
            # For two movements: The caption should be like "The camera is **moving forward** and **panning right**."
            # if more than three: The caption should be like "The camera is **moving forward**, **panning right**, and **tilting up**."
            if len(true_movement) == 1:
                return "The camera is {}.".format(movement_info[true_movement[0]])
            elif len(true_movement) == 2:
                return "The camera is {} and {}.".format(movement_info[true_movement[0]], movement_info[true_movement[1]])
            else:
                return "The camera is {}, {}, and {}.".format(
                    ", ".join([movement_info[m] for m in true_movement[:-1]]),
                    movement_info[true_movement[-1]]
                )
                
    def get_tracking_description(self, data: VideoData) -> str:
        # only call when data.cam_motion.is_tracking is True
        # Options: "side", "tail", "lead", "aerial", "arc", "pan", "tilt"
        # however, when both "side" and "tail"/"lead", this is "rear-side"/"front-side"
        if len(data.cam_motion.tracking_shot_types) == 1:
            if "side" in data.cam_motion.tracking_shot_types:
                if data.cam_motion.left is True:
                    description = "The camera is moving leftward to track the subject from the side."
                elif data.cam_motion.right is True:
                    description = "The camera is moving rightward to track the subject from the side."
                else:
                    description = "The camera is tracking the subject from the side."
            elif "tail" in data.cam_motion.tracking_shot_types:
                description = "The camera is following the subject from behind."
            elif "lead" in data.cam_motion.tracking_shot_types:
                description = "The camera is leading the subject from the front."
            elif "aerial" in data.cam_motion.tracking_shot_types:
                description = "The camera is tracking the subject from an aerial view."
            elif "arc" in data.cam_motion.tracking_shot_types:
                description = "The camera is tracking the subject while arcing around them."
            elif "pan" in data.cam_motion.tracking_shot_types:
                if data.cam_motion.pan_left is True:
                    description = "The camera is panning leftward to track the subject."
                elif data.cam_motion.pan_right is True:
                    description = "The camera is panning rightward to track the subject."
                else:
                    description = "The camera is tracking the subject by panning."
            elif "tilt" in data.cam_motion.tracking_shot_types:
                if data.cam_motion.tilt_up is True:
                    description = "The camera is tilting upward to track the subject."
                elif data.cam_motion.tilt_down is True:
                    description = "The camera is tilting downward to track the subject."
                else:
                    description = "The camera is tracking the subject by tilting."
            else:
                raise ValueError(f"Invalid tracking shot type: {data.cam_motion.tracking_shot_types[0]}")
        elif len(data.cam_motion.tracking_shot_types) == 2:
            if "side" in data.cam_motion.tracking_shot_types:
                if "tail" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the rear-side."
                elif "lead" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the front-side."
                elif "arc" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the side while moving in an arc."
                elif "pan" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the side while panning."
                elif "tilt" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the side while tilting."
                elif "aerial" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the side with an aerial perspective."
                else:
                    raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
            elif "tail" in data.cam_motion.tracking_shot_types:
                if "aerial" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from above and behind."
                elif "arc" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from behind while moving in an arc."
                elif "pan" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from behind while panning."
                elif "tilt" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from behind while tilting."
                else:
                    raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
            elif "lead" in data.cam_motion.tracking_shot_types:
                if "aerial" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from above and the front."
                elif "arc" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the front while moving in an arc."
                elif "pan" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the front while panning."
                elif "tilt" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from the front while tilting."
                else:
                    raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
            elif "aerial" in data.cam_motion.tracking_shot_types:
                if "arc" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from an aerial view while moving in an arc."
                elif "pan" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from an aerial view while panning."
                elif "tilt" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject from an aerial view while tilting."
                else:
                    raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
            elif "pan" in data.cam_motion.tracking_shot_types:
                if "tilt" in data.cam_motion.tracking_shot_types:
                    description = "The camera is tracking the subject while panning and tilting."
                else:
                    raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
            else:
                raise ValueError(f"Invalid tracking shot types: {data.cam_motion.tracking_shot_types}")
        else:
            # More than three types, therefore need to write a sentence with all types
            tracking_info = {
                "side": "positioning at the side",
                "tail": "following from behind",
                "lead": "leading from the front",
                "aerial": "taking an aerial perspective",
                "arc": "moving in an arc",
                "pan": "panning",
                "tilt": "tilting"
            }
            
            description = "The camera is tracking the subject by "
            for i, tracking_type in enumerate(data.cam_motion.tracking_shot_types):
                if i == len(data.cam_motion.tracking_shot_types) - 1:
                    description += f"and {tracking_info[tracking_type]}."
                else:
                    description += f"{tracking_info[tracking_type]}, "
            
        if data.cam_motion.subject_size_change == "larger":
            description += " During the tracking shot, the subject becomes larger in the frame."
        elif data.cam_motion.subject_size_change == "smaller":
            description += " During the tracking shot, the subject becomes smaller in the frame."
        return description
            
    def get_description(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        policy = ""
        policy += read_text_file("caption_policy/policy/camera_framing_dynamics/policy.txt")
        
        policy += "\n Crucially, instead of inferring these attributes from the video, we have already provided human-labeled ground truth for some of the elements specified above. You should directly use this information in your description and should not infer any details that are not already provided. Your description should be brief, and if anything is normal or unremarkable, you do not need to include it (e.g., if the video is at regular playback speed, there is no need to mention it)."

        # Add playback speed information
        policy += "\n **Playback Speed:** {}".format(self.format_playback_speed(data.cam_setup.video_speed))
        
        # Add lens distortion information
        policy += "\n **Lens Distortion:** {}".format(self.format_lens_distortion(data.cam_setup.lens_distortion))
        
        # Add camera height information
        if data.cam_setup.is_height_wrt_ground_applicable:
            if data.cam_setup.height_wrt_ground_change:
                policy += "\n **Camera Height:** The camera starts {} and then moves {}.".format(
                    self.format_camera_height_start(data.cam_setup.height_wrt_ground_info['start']),
                    self.format_camera_height_end(data.cam_setup.height_wrt_ground_info['end'])
                )
            else:
                try:
                    policy += "\n **Camera Height:** The camera is {}.".format(
                        self.format_camera_height_start((data.cam_setup.height_wrt_ground_info['start']))
                    )
                except:
                    import pdb; pdb.set_trace()
        elif data.cam_setup.overall_height_description != "":
            policy += "\n **Camera Height:** {}".format(data.cam_setup.overall_height_description)
        else:
            policy += "\n **Camera Height:** The camera height is unclear or not significant enough to mention (no need to mention)."
        
        
        # Add camera angle information
        if data.cam_setup.is_camera_angle_applicable:
            if data.cam_setup.camera_angle_change:
                policy += "\n **Camera Angle:** The camera angle is initially at {} and then changes to {} due to camera motion.".format(
                    self.format_camera_angle(data.cam_setup.camera_angle_info['start']),
                    self.format_camera_angle(data.cam_setup.camera_angle_info['end'])
                )
            else:
                policy += "\n **Camera Angle:** The camera angle is at {}.".format(
                    self.format_camera_angle(data.cam_setup.camera_angle_info['start'])
                )
            
            # check if dutch angle is applicable
            if data.cam_setup.is_dutch_angle_varying:
                policy += " The camera is also at a dutch angle that varies due to camera rolling."
            elif data.cam_setup.is_dutch_angle_fixed:
                policy += " The camera is also at a fixed dutch angle during the video."
        elif data.cam_setup.camera_angle_description != "":
            policy += "\n **Camera Angle:** {}".format(data.cam_setup.camera_angle_description)
        else:
            policy += "\n **Camera Angle:** The camera angle is unclear or not significant enough to mention (no need to mention)."
        
        # Add focus information
        if data.cam_setup.is_focus_applicable:
            if data.cam_setup.is_deep_focus:
                policy += "\n **Camera Focus:** The camera uses a deep focus with a large depth of field."
            else:
                if data.cam_setup.is_ultra_shallow_focus:
                    policy += "\n **Camera Focus:** The camera uses an extremely shallow depth of field."
                else:
                    policy += "\n **Camera Focus:** The camera uses a shallow depth of field."
                
                if data.cam_setup.focus_change:
                    policy += " The camera starts {}, and later becomes {}.".format(
                        self.format_focus_plane(data.cam_setup.focus_info['start']),
                        self.format_focus_plane(data.cam_setup.focus_info['end'])
                    )
                else:
                    policy += " The camera is {}.".format(
                        self.format_focus_plane(data.cam_setup.focus_info['start'])
                    )
                
                if data.cam_setup.is_rack_focus:
                    policy += " The focus plane changes through a rack focus."
                elif data.cam_setup.is_pull_focus:
                    policy += " The focus plane changes through a slow rack focus."
                elif data.cam_setup.is_focus_tracking:
                    policy += " The camera uses focus tracking to keep the subject in focus."
        elif data.cam_setup.camera_focus_description != "":
            policy += "\n **Camera Focus:** {}".format(data.cam_setup.camera_focus_description)
        else:
            policy += "\n **Camera Focus:** The camera focus is unclear or not significant enough to mention (no need to mention)."
    
        # Add camera motion information
        if data.cam_motion.camera_movement == "no":
            if data.cam_motion.steadiness == "static":
                policy += "\n **Camera Motion:** The camera is completely static, with no movement or shaking."
            elif data.cam_motion.steadiness in ['smooth', 'unsteady']:
                policy += "\n **Camera Motion:** The camera is fixed but slightly unsteady, with no intentional movement."
            elif data.cam_motion.steadiness in ['very unsteady']:
                policy += "\n **Camera Motion:** The camera is quite unsteady, but its motion lacks a clear pattern."
        else:
            
            if data.cam_motion.camera_movement == "major_complex":
                policy += "\n **Camera Motion:** {}".format(data.cam_motion.complex_motion_description)
            else:
                complex_motion_description = self.get_movement_description(data)
                if data.cam_motion.camera_movement == "minor":
                    policy += "\n **Camera Motion:** The camera shows some minor movement."
                elif data.cam_motion.camera_movement == "major_simple":
                    policy += "\n **Camera Motion:** The camera shows a clear movement pattern."
                else:
                    raise ValueError("Invalid camera movement type.")
                policy += " " + complex_motion_description
            
            # if tracking
            if data.cam_motion.is_tracking:
                policy += "\n **Subject Tracking:** {}.".format(
                    self.get_tracking_description(data)
                )
                
            policy += "\n **Camera Steadiness:** The camera movement is {}".format(
                self.format_camera_steadiness(data.cam_motion.steadiness)
            )
            
            if data.cam_motion.camera_motion_speed != "regular":
                policy += " \n **Camera Motion Speed**: The camera is {}".format(
                    self.format_camera_motion_speed(data.cam_motion.camera_motion_speed)
                )
        return policy    
        