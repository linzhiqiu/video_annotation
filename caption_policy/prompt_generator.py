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

class PromptGenerator:
    def __init__(self, name: str, info: str, caption_fields: List[str]):
        self.name = name
        self.info = info
        self.caption_fields = caption_fields
    
    def __str__(self):
        return f"{self.name}: {self.info} \nCaption Fields: {self.caption_fields}"

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        raise NotImplementedError("Subclasses must implement this method")

    def get_prompt_without_video_info(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class SubjectPolicy(PromptGenerator):
    def __init__(self):
        name = "Subject Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Subject."
        caption_fields = ["subject_description"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "subject_description": self.get_prompt(data)
        }
    
    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            # raise ValueError("Shot transitions are not supported in this policy.")
            policy = read_text_file("caption_policy/policy/subject_description/policy.txt")
            policy += "\n\nThis video contains one or more shot transitions. Please describe the subject of each segment in a single fluent paragraph."
            return policy

        if data.cam_setup.is_framing_subject is False:
            # This much be a Scenery shot
            # return ("The video is a scenery shot. You do not need to describe the subject. "
            #         "Please concisely specify the type of scenery shot (e.g., a landscape or cityscape scenery shot)."
            #         "Explain why there is no main subject, such as the focus being on the environment, atmosphere, "
            #         "or scale rather than a specific object. If relevant, describe the shot's purpose, whether it is an "
            #         "establishing shot setting the scene or providing context, or a FPV shot that creates an immersive experience.")
            policy = ("The video is a scenery shot. You do not need to describe the subject. "
                    "Please concisely specify the type of scenery shot (e.g., a landscape or cityscape scenery shot) in a single fluent paragraph."
                    "Also explain why there is no main subject, such as the focus being on the environment, atmosphere, "
                    "or scale rather than a specific object. Just note that briefly in one to three sentences.")
            policy += "\n\n" + read_text_file("caption_policy/policy/subject_description/format_instruction.txt")
            return policy
        
        policy = read_text_file("caption_policy/policy/subject_description/policy.txt")
        if data.cam_setup.is_framing_subject is None:
            # Including complex shot with description others, or multiple subject without a clear focus
            # If is others description, then prompt to use this description to complement the subject description
            # Note that there may not be a subject in focus. 
            if data.cam_setup.shot_size_description_type == "others" or data.cam_setup.complex_shot_type == "unknown":
                pass # Do nothing
            elif data.cam_setup.is_just_many_subject_no_focus_shot:
                policy += "\n\nPlease note that this video contains **multiple subjects with no clear main focus**. Because it does not emphasize any specific subject, please briefly describe the types of subjects without going into too much detail. You may also describe the subjects collectively as a group."
                policy += "\n\n" + read_text_file("caption_policy/policy/subject_description/format_instruction.txt")
                return policy
            else:
                raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        if data.cam_setup.is_just_human_shot:
            policy += "\n\nPlease note that the video features salient **human** subjects, so the description should focus on them."
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n\nPlease note that the video features salient **non-human** subjects, so the description should focus on them."
        elif data.cam_setup.is_just_change_of_subject_shot:
            if data.cam_setup.subject_revealing:
                policy += "\n\nPlease note that the video is a **revealing shot of the subject**, so the description should reflect this by explaining how the subject is revealed through either subject movement or camera movement."
            elif data.cam_setup.subject_disappearing:
                policy += "\n\nPlease note that the video features the main subjects **disappearing from the frame**, so the description should reflect this by explaining how they exit, whether through subject movement or camera movement."
            elif data.cam_setup.subject_switching:
                policy += "\n\nPlease note that the video features the main subjects **switching from one to another**, so the description should reflect this by explaining how the transition occurs, whether through subject movement or camera movement."
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_disappearing, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n\nPlease note that the video has a **main subject with dynamic size**, so the description should focus on them. Don't mention the background scene and other motion."
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n\nFocus on describing the **atypical appearance** of the main subjects in the video. Avoid mentioning the background or subject movements."
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n\nPlease note that the video features **multiple subjects with one clear main focus**, so you need to clarify who the main subject is. The description should focus on the details of the main subject while concisely summarizing secondary subjects and describing their relationship to the main subject if clear."
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n\nPlease note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types and relationships."
        elif data.cam_setup.complex_shot_type == "unknown":
            policy += "\n\nPlease note that the video features a **complex scenario** with ambiguous subjects or it is an abstract shot. Please try your best to describe the main subjects or objects in the video."
        else:
            assert data.cam_setup.shot_size_description != ""
            policy += "\n\n" + read_text_file("caption_policy/policy/subject_description/has_shot_size_description.txt").format(shot_size_description=data.cam_setup.shot_size_description)
        
        policy += "\n\n" + read_text_file("caption_policy/policy/subject_description/format_instruction.txt")
        return policy

    def get_prompt_without_video_info(self) -> str:
        policy = read_text_file("caption_policy/policy/subject_description/policy.txt")

        
        policy += "\n\nWhen shot transitions occur, describe the subject in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subjects change from one segment to the next."
        policy += "\n\nIf the video is a scenery shot without salient subjects, you do not need to describe a specific subject. Instead, concisely specify the type of scenery shot (e.g., landscape, cityscape) in a single fluent paragraph. Briefly explain why there is no main subject, for example by noting that the focus is on the environment, atmosphere, or scale rather than on a particular object, using one to three sentences."
        policy += "\n\nIf the video features salient human or non-human subjects, focus your description on them. If the video features multiple subjects with a clear focus, you may describe the main subject in detail and briefly mention the secondary subjects. If the video features multiple subjects without a clear main focus, describe the types of subjects without going into too much detail. You may also describe the subjects collectively as a group."
        policy += "\n\nIf the video features subjects revealing, disappearing, or switching, describe the transition in detail."
        return policy

class ScenePolicy(PromptGenerator):
    def __init__(self):
        name = "Scene Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Scene."
        caption_fields = ["scene_composition_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        policy = {
            "scene_composition_dynamics": self.get_prompt(data)
        }
        return policy

    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        true_pov_attribute = data.cam_setup.true_pov_attribute
        policy = read_text_file("caption_policy/policy/scene_composition_dynamics/policy.txt")
        policy += "\n\n" + read_text_file("caption_policy/policy/scene_composition_dynamics/format_instruction.txt")
        pov_info = read_json_file(os.path.join("labels/cam_setup/point_of_view", f"{true_pov_attribute}.json"))['def_prompt'][0]
        if true_pov_attribute == "objective_pov":
            pov_info += " (no need to mention)."
        if data.cam_setup.has_overlays is True:
            policy += "\n\nPlease note that the video includes overlay elements, such as text or visuals like titles, subtitles, captions, icons, watermarks, heads-up displays (HUD), or framing elements. In your description, specify that these are overlays (not part of the scene) and describe their content and placement."
        policy += "\n\n" + read_text_file("caption_policy/policy/scene_composition_dynamics/has_pov_info.txt").format(pov_description=pov_info)
        return policy

    def get_prompt_without_video_info(self) -> str:
        policy = read_text_file("caption_policy/policy/scene_composition_dynamics/policy.txt")

        policy += "\n\nWhen shot transitions occur, describe the scene in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the scene changes from one segment to the next."
        return policy


class SubjectMotionPolicy(PromptGenerator):
    def __init__(self):
        name = "Subject Motion & Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Subject Motion and Dynamics."
        caption_fields = ["subject_motion_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "subject_motion_dynamics": self.get_prompt(data)
        }
    
    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        if data.cam_setup.is_framing_subject is False:
            # This much be a Scenery shot
            return ("The video is a scenery shot. You do not need to describe the subject motion. Just note that briefly in one to three sentences. ")
        
        
        policy = read_text_file("caption_policy/policy/subject_motion_dynamics/policy.txt")
        if data.cam_setup.is_framing_subject is None:
            # Including complex shot with description others, or multiple subject without a clear focus
            # If is others description, then prompt to use this description to complement the subject description
            # Note that there may not be a subject in focus. 
            if data.cam_setup.shot_size_description_type == "others" or data.cam_setup.complex_shot_type == "unknown":
                pass # Do nothing
            elif data.cam_setup.is_just_many_subject_no_focus_shot:
                policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the salient motions and dynamics of the primary subjects while providing a concise overview of secondary movements, or describe all subjects' collective motion if that is more appropriate."
                return policy
            else:
                raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        if data.cam_setup.is_just_human_shot:
            policy += "\n\nPlease note that the video features salient **human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n\nPlease note that the video features salient **non-human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_change_of_subject_shot:
            if data.cam_setup.subject_revealing:
                policy += "\n\nPlease note that the video is a **revealing shot of the subject**, so the description should reflect this by explaining how the subject is revealed through either subject movement or camera movement."
            elif data.cam_setup.subject_disappearing:
                policy += "\n\nPlease note that the video features the main subjects **disappearing from the frame**, so the description should reflect this by explaining how they exit, whether through subject movement or camera movement."
            elif data.cam_setup.subject_switching:
                policy += "\n\nPlease note that the video features the main subjects **switching from one to another**, so the description should first describe the first subject’s motion and dynamics, followed by the second’s."
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_disappearing, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n\nPlease note that the **main subject’s framing is not stable** throughout the video, so the description should reflect how their motion and dynamics contribute to this instability."
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n\nPlease note that the main subjects in this video exhibit **atypical motion, posture, or anatomy**, so the description should reflect this."
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n\nPlease note that the video features **multiple subjects with a clear main focus**, so the description should focus on the motion and dynamics of the main subject while providing a concise overview of secondary subjects' movements."
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n\nPlease note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types, movement patterns, and interactions."
        else:
            # pass for complex shot with description
            pass
                
        assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        policy += "\n\n" + read_text_file("caption_policy/policy/subject_motion_dynamics/has_subject_description.txt").format(subject_description=data.cam_setup.subject_description)
        return policy
    
    def get_prompt_without_video_info(self) -> str:
        policy = read_text_file("caption_policy/policy/subject_motion_dynamics/policy.txt")

        
        policy += "\n\nWhen shot transitions occur, describe the motion of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subject’s motion changes between segments."
        policy += "\n\nIf the video is a scenery shot without salient subjects, you do not need to describe subject motion. Instead, briefly note this in one to three sentences."
        policy += "\n\nIf the video features salient human or non-human subjects, focus your description on their motion. When there are multiple subjects with a clear focus, describe the main subject’s motion in detail and briefly mention the motion of secondary subjects. If there are multiple subjects without a clear main focus, describe their motion collectively and concisely without going into excessive detail."
        policy += "\n\nIf the video features subjects revealing, disappearing, or switching, describe the transition in detail along with the description of their motion."
        return policy


class SpatialPolicy(PromptGenerator):
    def __init__(self):
        name = "Vanilla Spatial Framing and Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Spatial Framing and Dynamics."
        caption_fields = ["spatial_framing_dynamics"]
        super().__init__(name, info, caption_fields)

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "spatial_framing_dynamics": self.get_prompt(data)
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

    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")

        policy = ""
        # policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_subject.txt")
        # policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scene.txt")
        # policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/movement.txt")
        policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/policy.txt")
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
        #         policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scenery.txt")
        #         policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
        #     else:
        #         raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")

        assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        assert data.cam_setup.scene_description != "", "Scene description must be provided before subject motion and dynamics description."
        policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/has_subject_scene_description.txt").format(
            subject_description=data.cam_setup.subject_description,
            scene_description=data.cam_setup.scene_description
        )

        shot_size_change = data.cam_setup.shot_size_change
        subject_status = None # 'has_subject', 'no_subject', 'change_of_subject', 'has_description'
        is_subject_height_applicable = data.cam_setup.is_subject_height_applicable

        if data.cam_setup.is_just_human_shot:
            policy += "\n\nPlease note that the video features **salient human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n\nPlease note that the video features **salient non-human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_change_of_subject_shot:
            subject_status = "change_of_subject"
            if data.cam_setup.subject_revealing:
                policy += "\n\nPlease note that the video is a **revealing shot of the subject**."
                policy += "\n\nShot Size Information: The video begins with no subject. It then becomes {} of the subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nWhen the subject is revealed, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            elif data.cam_setup.subject_disappearing:
                policy += "\n\nPlease note that the video features **main subjects disappearing from the frame**."
                policy += "\n\nShot Size Information: The video begins with {} of the subject. Then the subject disappears.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nBefore the subject disappears, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_switching:
                policy += "\n\nPlease note that the video features **main subjects switching from one to another**."
                policy += "\n\nShot Size Information: The video begins with {} of the first subject. Then it becomes {} of the second subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nThe camera is positioned {} when the first subject is in focus, and {} when the second subject is in focus.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_disappearing, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n\nPlease note that the **main subject’s framing (shot size) is not stable** throughout the video, so the description should emphasize this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n\nPlease note that the **main subjects exhibit atypical posture or anatomy**, so the description should reflect this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n\nPlease note that the video features **multiple subjects with a clear main focus**, so the description should focus on the main subject."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n\nPlease note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types and relationships."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_no_focus_shot:
            policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_scenery_shot:
            policy += "\n\nPlease note that the video is a **scenery shot**. You do not need to describe the subjects. Just note that briefly in one to three sentences."
            subject_status = "no_subject"
        elif data.cam_setup.complex_shot_type == "unknown":
            policy += "\n\nPlease note that the video features a **complex scenario** with ambiguous subjects or it is an abstract shot. Please try your best to describe the spatial positions and movements of the main subjects or objects in the video."
            subject_status = None
        else:
            # pass for complex shot with description
            subject_status = "has_description"
            policy += "\n\nThe description below already mentions the spatial framing information about the subjects or scenery in this video. Use this caption as a reference to draft the spatial framing and dynamics description. Simply expand on it to fully capture other spatial positions and movements. Do not infer the any spatial framing information already mentioned below."
            policy += f"\n\nShot Size Information: {data.cam_setup.shot_size_description}"
            if is_subject_height_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is initially positioned {} and then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n\nCamera Height Relative to Subjects: {data.cam_setup.subject_height_description}"

        if subject_status == "has_subject":
            if shot_size_change:
                policy += "\n\nShot Size Information: The video begins with {} of the subjects. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n\nShot Size Information: The video shows {} of the subjects.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))

            if is_subject_height_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is initially positioned {}. It then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is positioned {}.".format(self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']))
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n\nCamera Height Relative to Subjects: {data.cam_setup.subject_height_description}"
        elif subject_status == "no_subject":
            if shot_size_change:
                policy += "\n\nShot Size Information: The video begins with {} of the scenery. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n\nShot Size Information: The video shows {} of the scenery.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))

            if is_subject_height_applicable:
                raise ValueError("Height relative to subject is not applicable when there is no subject.")
        elif subject_status == None:
            # Shot size does not apply to complex shots
            policy += "\n\nShot Size Information: The video features a complex scenario with ambiguous subjects or it is an abstract shot. Please try your best to describe the spatial positions and movements of the main subjects or objects in the video. Do not use shot size to describe the spatial framing."
            if is_subject_height_applicable:
                raise ValueError("Height relative to subject is not applicable when there is unknown subject.")

        return policy

    def get_prompt_without_video_info(self) -> str:
        policy = read_text_file("caption_policy/policy/spatial_framing_dynamics/policy.txt")

        
        policy += "\n\nWhen shot transitions occur, describe the spatial framing and movement of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how their framing, position, depth, and height relative to the camera change between segments."
        policy += "\n\nIf the video is a scenery shot without salient subjects, specify the shot size of the scenery (e.g., wide shot, close-up) and describe any movement within it."
        policy += "\n\nIf the video features salient human or non-human subjects, focus your description on their spatial framing and movement. When there are multiple subjects with a clear focus, describe the main subject’s spatial framing and movement in detail and briefly mention those of secondary subjects. If there are multiple subjects without a clear main focus, describe their spatial composition and movement collectively and concisely."
        policy += "\n\nIf the video features subjects revealing, disappearing, or switching, describe the transition in detail along with their spatial framing and movement."
        return policy


class RawSubjectMotionPolicy(PromptGenerator):
    def __init__(self):
        name = "Raw Subject Motion & Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Subject Motion and Dynamics."
        caption_fields = ["raw_subject_motion_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "raw_subject_motion_dynamics": self.get_prompt(data)
        }
    
    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        if data.cam_setup.is_framing_subject is False:
            # This much be a Scenery shot
            return ("The video is a scenery shot. You do not need to describe the subject motion. Just note that briefly in one to three sentences. ")
        
        
        policy = read_text_file("caption_policy/policy/subject_motion_dynamics/policy.txt")
        if data.cam_setup.is_framing_subject is None:
            # Including complex shot with description others, or multiple subject without a clear focus
            # If is others description, then prompt to use this description to complement the subject description
            # Note that there may not be a subject in focus. 
            if data.cam_setup.shot_size_description_type == "others" or data.cam_setup.complex_shot_type == "unknown":
                pass # Do nothing
            elif data.cam_setup.is_just_many_subject_no_focus_shot:
                policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the salient motions and dynamics of the primary subjects while providing a concise overview of secondary movements, or describe all subjects' collective motion if that is more appropriate."
                return policy
            else:
                raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        if data.cam_setup.is_just_human_shot:
            policy += "\n\nPlease note that the video features salient **human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n\nPlease note that the video features salient **non-human** subjects, so the description should focus on their motion and dynamics."
        elif data.cam_setup.is_just_change_of_subject_shot:
            if data.cam_setup.subject_revealing:
                policy += "\n\nPlease note that the video is a **revealing shot of the subject**, so the description should reflect this by explaining how the subject is revealed through either subject movement or camera movement."
            elif data.cam_setup.subject_disappearing:
                policy += "\n\nPlease note that the video features the main subjects **disappearing from the frame**, so the description should reflect this by explaining how they exit, whether through subject movement or camera movement."
            elif data.cam_setup.subject_switching:
                policy += "\n\nPlease note that the video features the main subjects **switching from one to another**, so the description should first describe the first subject’s motion and dynamics, followed by the second’s."
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_disappearing, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n\nPlease note that the **main subject’s framing is not stable** throughout the video, so the description should reflect how their motion and dynamics contribute to this instability."
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n\nPlease note that the main subjects in this video exhibit **atypical motion, posture, or anatomy**, so the description should reflect this."
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n\nPlease note that the video features **multiple subjects with a clear main focus**, so the description should focus on the motion and dynamics of the main subject while providing a concise overview of secondary subjects' movements."
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n\nPlease note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types, movement patterns, and interactions."
        else:
            # pass for complex shot with description
            pass
                
        # assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        # policy += "\n\n" + read_text_file("caption_policy/policy/subject_motion_dynamics/has_subject_description.txt").format(subject_description=data.cam_setup.subject_description)
        return policy


class RawSpatialPolicy(PromptGenerator):
    def __init__(self):
        name = "Raw Spatial Framing and Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Spatial Framing and Dynamics."
        caption_fields = ["raw_spatial_framing_dynamics"]
        super().__init__(name, info, caption_fields)
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "raw_spatial_framing_dynamics": self.get_prompt(data)
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
    
    
    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        policy = ""
        policy += read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_subject.txt")
        policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scene.txt")
        policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/movement.txt")
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
        #         policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/framing_scenery.txt")
        #         policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
        #     else:
        #         raise ValueError("When framing subject is None, the shot size description must be others or many_subject_no_focus.")
            
        # assert data.cam_setup.subject_description != "", "Subject description must be provided before subject motion and dynamics description."
        # assert data.cam_setup.scene_description != "", "Scene description must be provided before subject motion and dynamics description."
        # policy += "\n\n" + read_text_file("caption_policy/policy/spatial_framing_dynamics/has_subject_scene_description.txt").format(
        #     subject_description=data.cam_setup.subject_description,
        #     scene_description=data.cam_setup.scene_description
        # )

        shot_size_change = data.cam_setup.shot_size_change
        subject_status = None # 'has_subject', 'no_subject', 'change_of_subject', 'has_description'
        is_subject_height_applicable = data.cam_setup.is_subject_height_applicable
        
        if data.cam_setup.is_just_human_shot:
            policy += "\n\nPlease note that the video features **salient human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_non_human_shot:
            policy += "\n\nPlease note that the video features **salient non-human subjects**, so you should focus on describing the spatial framing and movements of them."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_change_of_subject_shot:
            subject_status = "change_of_subject"
            if data.cam_setup.subject_revealing:
                policy += "\n\nPlease note that the video is a **revealing shot of the subject**."
                policy += "\n\nShot Size Information: The video begins with no subject. It then becomes {} of the subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nWhen the subject is revealed, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            elif data.cam_setup.subject_disappearing:
                policy += "\n\nPlease note that the video features **main subjects disappearing from the frame**."
                policy += "\n\nShot Size Information: The video begins with {} of the subject. Then the subject disappears.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nBefore the subject disappears, the camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_switching:
                policy += "\n\nPlease note that the video features **main subjects switching from one to another**."
                policy += "\n\nShot Size Information: The video begins with {} of the first subject. Then it becomes {} of the second subject.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
                if is_subject_height_applicable:
                    policy += "\n\nThe camera is positioned {} when the first subject is in focus, and {} when the second subject is in focus.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
            else:
                raise ValueError("When is_just_change_of_subject_shot is True, either subject_revealing, subject_disappearing, or subject_switching must be True.")
        elif data.cam_setup.is_just_clear_subject_dynamic_size_shot:
            policy += "\n\nPlease note that the **main subject’s framing (shot size) is not stable** throughout the video, so the description should emphasize this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_clear_subject_atypical_shot:
            policy += "\n\nPlease note that the **main subjects exhibit atypical posture or anatomy**, so the description should reflect this."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_one_focus_shot:
            policy += "\n\nPlease note that the video features **multiple subjects with a clear main focus**, so the description should focus on the main subject."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_different_subject_in_focus_shot:
            policy += "\n\nPlease note that the video features **multiple different subjects in focus**, so the description should clearly distinguish their types and relationships."
            subject_status = "has_subject"
        elif data.cam_setup.is_just_many_subject_no_focus_shot:
            policy += "\n\nPlease note that this video contains **multiple subjects without a clear main focus**. Briefly describe the spatial positions and movements of salient subjects while providing a concise overview of secondary subjects, or describe all the spatial composition of all subjects collectively as a group if that is more appropriate."
            subject_status = "no_subject"
        elif data.cam_setup.is_just_scenery_shot:
            policy += "\n\nPlease note that the video is a **scenery shot**. You do not need to describe the subjects. Just note that briefly in one to three sentences."
            subject_status = "no_subject"
        elif data.cam_setup.complex_shot_type == "unknown":
            policy += "\n\nPlease note that the video features a **complex scenario** with ambiguous subjects or it is an abstract shot. Please try your best to describe the spatial positions and movements of the main subjects or objects in the video."
            subject_status = None
        else:
            # pass for complex shot with description
            subject_status = "has_description"
            policy += "\n\nThe description below already mentions the spatial framing information about the subjects or scenery in this video. Use this caption as a reference to draft the spatial framing and dynamics description. Simply expand on it to fully capture other spatial positions and movements. Do not infer the any spatial framing information already mentioned below."
            policy += f"\n\nShot Size Information: {data.cam_setup.shot_size_description}"
            if is_subject_height_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is initially positioned {} and then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is positioned {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start'])
                    )
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n\nCamera Height Relative to Subjects: {data.cam_setup.subject_height_description}"
                
        
        if subject_status == "has_subject":
            if shot_size_change:
                policy += "\n\nShot Size Information: The video begins with {} of the subjects. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n\nShot Size Information: The video shows {} of the subjects.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))
                
            if is_subject_height_applicable:
                if data.cam_setup.height_wrt_subject_change:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is initially positioned {}. It then changes to {}.".format(
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']),
                        self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['end'])
                    )
                else:
                    policy += "\n\nCamera Height Relative to Subjects: The camera is positioned {}.".format(self.format_height_wrt_subject(data.cam_setup.height_wrt_subject_info['start']))
            elif data.cam_setup.subject_height_description != "":
                policy += f"\n\nCamera Height Relative to Subjects: {data.cam_setup.subject_height_description}"
        elif subject_status == "no_subject":
            if shot_size_change:
                policy += "\n\nShot Size Information: The video begins with {} of the scenery. It then changes to {}.".format(
                    self.format_shot_size(data.cam_setup.shot_size_info['start']),
                    self.format_shot_size(data.cam_setup.shot_size_info['end'])
                )
            else:
                policy += "\n\nShot Size Information: The video shows {} of the scenery.".format(self.format_shot_size(data.cam_setup.shot_size_info['start']))
                
            if is_subject_height_applicable:
                raise ValueError("Height relative to subject is not applicable when there is no subject.")
        elif subject_status == None:
            # Shot size does not apply to complex shots
            policy += "\n\nShot Size Information: The video features a complex scenario with ambiguous subjects or it is an abstract shot. Please try your best to describe the spatial positions and movements of the main subjects or objects in the video. Do not use shot size to describe the spatial framing."
            if is_subject_height_applicable:
                raise ValueError("Height relative to subject is not applicable when there is unknown subject.")
        
        return policy


class CameraPolicy(PromptGenerator):
    def __init__(self):
        name = "Vanilla Camera Framing and Dynamics Description"
        info = "A policy that use existing labels to prompt a human or model to provide structured captions for Camera Framing and Dynamics."
        caption_fields = ["camera_framing_dynamics"]
        super().__init__(name, info, caption_fields)

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "camera_framing_dynamics": self.get_prompt(data)
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
            return "The video features mild barrel distortion where lines near the frame edges bow slightly outward."
        elif lens_distortion == "fisheye":
            return "The video shows extreme fisheye distortion where most lines curve strongly outward."
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
            "static": "The camera is stationary",
            "very_smooth": "The camera movement is very smooth with no shaking",
            "smooth": "The camera movement is smooth with minimal shaking",
            "unsteady": "The camera movement is slightly unsteady with some shaking",
            "very_unsteady": "The camera movement is unsteady with noticeable shaking"
        }
        return steadiness_info[steadiness]

    def format_camera_motion_speed(self, speed: str) -> str:
        # Options: "slow", "regular", "fast"
        speed_info = {
            "slow": "moving slowly.",
            "regular": "moving at a regular speed (no need to mention).",
            "fast": "moving quickly."
        }
        return speed_info[speed]

    def get_movement_description_simple(self, data: VideoData) -> str:
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
            "crane_up": "craning up in an arc",
            "crane_down": "craning down in an arc",
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
                return "The camera is {}, and {}.".format(
                    ", ".join([movement_info[m] for m in true_movement[:-1]]),
                    movement_info[true_movement[-1]]
                )

    def get_movement_description_minor(self, data: VideoData) -> str:
        # #Camera direction movement options
        movement_info = {
            "camera_forward_backward": {
                "forward": "moving forward",
                "backward": "moving backward"
            },
            "camera_zoom": {
                "in": "zooming in",
                "out": "zooming out"
            },
            "camera_left_right": {
                "left_to_right": "moving left to right",
                "right_to_left": "moving right to left"
            },
            "camera_pan": {
                "left_to_right": "panning left to right",
                "right_to_left": "panning right to left"
            },
            "camera_up_down": {
                "up": "moving up",
                "down": "moving down"
            },
            "camera_tilt": {
                "up": "tilting up",
                "down": "tilting down"
            },
            "camera_arc": {
                "clockwise": "arcing clockwise",
                "counter_clockwise": "arcing counterclockwise"
            },
            "camera_crane": {
                "crane_up": "craning up in an arc",
                "crane_down": "craning down in an arc"
            },
            "camera_roll": {
                "clockwise": "rolling clockwise",
                "counter_clockwise": "rolling counterclockwise"
            }
        }
        true_movement = [key for key in movement_info.keys() if getattr(data.cam_motion, key) != "no"]
        if len(true_movement) == 0:
            return "The camera shows no clear or intentional movement."
        else:
            # For one movement: The caption should be like "The camera is **moving forward**."
            # For two movements: The caption should be like "The camera is **moving forward** and **panning right**."
            # if more than three: The caption should be like "The camera is **moving forward**, **panning right**, and **tilting up**."
            if len(true_movement) == 1:
                return "The camera is {}.".format(movement_info[true_movement[0]][getattr(data.cam_motion, true_movement[0])])
            elif len(true_movement) == 2:
                return "The camera is {} and {}.".format(
                    movement_info[true_movement[0]][getattr(data.cam_motion, true_movement[0])],
                    movement_info[true_movement[1]][getattr(data.cam_motion, true_movement[1])]
                )
            else:
                return "The camera is {}, and {}.".format(
                    ", ".join([movement_info[m][getattr(data.cam_motion, m)] for m in true_movement[:-1]]),
                    movement_info[true_movement[-1]][getattr(data.cam_motion, true_movement[-1])]
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

    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")

        policy = ""
        policy += read_text_file("caption_policy/policy/camera_framing_dynamics/policy.txt")

        policy += "\n\nCrucially, instead of inferring these attributes from the video, we have already provided human-labeled ground truth for some of the elements specified above. You should directly use this information in your description and should not infer any details that are not already provided. Your description should be brief, and if anything is normal or unremarkable, you do not need to include it (e.g., if the video is at regular playback speed, there is no need to mention it)."

        # Add playback speed information
        policy += "\n\n**Playback Speed:** {}".format(self.format_playback_speed(data.cam_setup.video_speed))

        # Add lens distortion information
        policy += "\n\n**Lens Distortion:** {}".format(self.format_lens_distortion(data.cam_setup.lens_distortion))

        # Add camera height information
        if data.cam_setup.is_height_wrt_ground_applicable:
            if data.cam_setup.height_wrt_ground_change:
                policy += "\n\n**Camera Height:** The camera starts {} and then moves {}.".format(
                    self.format_camera_height_start(data.cam_setup.height_wrt_ground_info['start']),
                    self.format_camera_height_end(data.cam_setup.height_wrt_ground_info['end'])
                )
            else:
                try:
                    policy += "\n\n**Camera Height:** The camera is {}.".format(
                        self.format_camera_height_start((data.cam_setup.height_wrt_ground_info['start']))
                    )
                except:
                    import pdb; pdb.set_trace()
        elif data.cam_setup.overall_height_description != "":
            policy += "\n\n**Camera Height:** {}".format(data.cam_setup.overall_height_description)
        else:
            policy += "\n\n**Camera Height:** The camera height is unclear or not significant enough to mention (no need to mention)."

        # Add camera angle information
        if data.cam_setup.is_camera_angle_applicable:
            if data.cam_setup.camera_angle_change:
                policy += "\n\n**Camera Angle:** The camera angle is initially at {} and then changes to {} due to camera motion.".format(
                    self.format_camera_angle(data.cam_setup.camera_angle_info['start']),
                    self.format_camera_angle(data.cam_setup.camera_angle_info['end'])
                )
            else:
                policy += "\n\n**Camera Angle:** The camera angle is at {}.".format(
                    self.format_camera_angle(data.cam_setup.camera_angle_info['start'])
                )

            # check if dutch angle is applicable
            if data.cam_setup.is_dutch_angle_varying:
                policy += " The camera is also at a dutch angle that varies due to camera rolling."
            elif data.cam_setup.is_dutch_angle_fixed:
                policy += " The camera is also at a fixed dutch angle during the video."
        elif data.cam_setup.camera_angle_description != "":
            policy += "\n\n**Camera Angle:** {}".format(data.cam_setup.camera_angle_description)
        else:
            policy += "\n\n**Camera Angle:** The camera angle is unclear or not significant enough to mention (no need to mention)."

        # Add focus information
        if data.cam_setup.is_focus_applicable:
            if data.cam_setup.is_deep_focus:
                policy += "\n\n**Camera Focus:** The camera uses a deep focus with a large depth of field."
            else:
                if data.cam_setup.is_ultra_shallow_focus:
                    policy += "\n\n**Camera Focus:** The camera uses an extremely shallow depth of field, focusing on a very narrow plane."
                else:
                    policy += "\n\n**Camera Focus:** The camera uses a shallow depth of field, keeping a limited range in focus."

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
            policy += "\n\n**Camera Focus:** {}".format(data.cam_setup.camera_focus_description)
        else:
            policy += "\n\n**Camera Focus:** The camera focus is unclear or not significant enough to mention (no need to mention)."

        # Add camera motion information
        if data.cam_motion.camera_movement == "no":
            if data.cam_motion.steadiness == "static":
                policy += "\n\n**Camera Motion:** The camera is completely static, with no movement or shaking."
            elif data.cam_motion.steadiness in ['smooth', 'unsteady']:
                policy += "\n\n**Camera Motion:** The camera is fixed but slightly unsteady, with no intentional movement."
            elif data.cam_motion.steadiness in ['very_unsteady']:
                policy += "\n\n**Camera Motion:** The camera is quite unsteady, but its motion lacks a clear pattern."
        else:

            if data.cam_motion.camera_movement == "major_complex":
                policy += "\n\n**Camera Motion:** {}".format(data.cam_motion.complex_motion_description)
            else:
                if data.cam_motion.camera_movement == "minor":
                    complex_motion_description = self.get_movement_description_minor(data)
                    policy += "\n\n**Camera Motion:** The camera shows some minor movement."
                elif data.cam_motion.camera_movement == "major_simple":
                    complex_motion_description = self.get_movement_description_simple(data)
                    policy += "\n\n**Camera Motion:** The camera shows a clear movement pattern."
                else:
                    raise ValueError("Invalid camera movement type.")
                policy += " " + complex_motion_description

            # if tracking
            if data.cam_motion.is_tracking:
                policy += "\n\n**Subject Tracking:** {}".format(
                    self.get_tracking_description(data)
                )

            policy += "\n\n**Camera Steadiness:** {}.".format(
                self.format_camera_steadiness(data.cam_motion.steadiness)
            )

            if data.cam_motion.camera_motion_speed != "regular":
                policy += " \n\n**Camera Motion Speed**: The camera is {}".format(
                    self.format_camera_motion_speed(data.cam_motion.camera_motion_speed)
                )

        policy += "\n\nIf possible, specify the subject that the camera focuses on when describing camera work. For instance, use 'focus on the man in the foreground' rather than 'focus on the foreground.' Likewise, if the camera follows a subject, avoid the generic phrase 'tracking the subject(s).' Instead, identify the subject and describe the specific type of tracking."
        return policy   

    def get_prompt_without_video_info(self) -> str:
        policy = read_text_file("caption_policy/policy/camera_framing_dynamics/policy.txt")

        policy += "\n\nTry to make the description as concise as possible. For example, if the video is at regular playback speed, has no lens distortion, and no Dutch angle, there is no need to mention these."
        policy += "\n\nWhen shot transitions occur, describe the camera framing and movement in each segment separately, note the type of transition (e.g., hard cut, soft transition), and explain how the framing and movement change between segments."
        return policy


class VanillaCameraMotionPolicy(CameraPolicy):
    def __init__(self):
        super().__init__()
        self.name = "Vanilla Camera Motion Description"
        self.info = "A policy that use existing labels to prompt a human or model to provide structured captions for Camera Motion."
        self.caption_fields = ["camera_motion"]
    
    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "camera_motion": self.get_prompt(data)
        }
            
     
    def get_prompt(self, data: VideoData) -> str:
        if data.cam_motion.shot_transition or data.cam_motion.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")
        
        policy = ""
        policy += read_text_file("caption_policy/policy/camera_motion/policy.txt")
        
        policy += "\n\nUse the provided human-labeled ground truth directly in your description without inferring any additional details. Include all given information."

        # Add camera motion information
        if data.cam_motion.camera_movement == "no":
            if data.cam_motion.steadiness == "static":
                policy += "\n\n**Camera Motion:** The camera is completely static, with no movement or shaking."
            elif data.cam_motion.steadiness in ['smooth', 'unsteady']:
                policy += "\n\n**Camera Motion:** The camera is fixed but slightly unsteady, with no intentional movement."
            elif data.cam_motion.steadiness in ['very_unsteady']:
                policy += "\n\n**Camera Motion:** The camera is quite shaky but doesn’t move in a clear pattern."
        else:
            
            if data.cam_motion.camera_movement == "major_complex":
                policy += "\n\n**Camera Motion:** {}".format(data.cam_motion.complex_motion_description)
            else:
                if data.cam_motion.camera_movement == "minor":
                    complex_motion_description = self.get_movement_description_minor(data)
                    policy += "\n\n**Camera Motion:** The camera shows some minor movement."
                elif data.cam_motion.camera_movement == "major_simple":
                    complex_motion_description = self.get_movement_description_simple(data)
                    policy += "\n\n**Camera Motion:** The camera shows a clear movement pattern."
                else:
                    raise ValueError("Invalid camera movement type.")
                policy += " " + complex_motion_description
            
            # if tracking
            if data.cam_motion.is_tracking:
                policy += "\n\n**Subject Tracking:** {}".format(
                    self.get_tracking_description(data)
                )
                
            policy += "\n\n**Camera Steadiness:** {}.".format(
                self.format_camera_steadiness(data.cam_motion.steadiness)
            )
            
            if data.cam_motion.camera_motion_speed != "regular":
                policy += " \n\n**Camera Motion Speed**: The camera is {}".format(
                    self.format_camera_motion_speed(data.cam_motion.camera_motion_speed)
                )
        return policy    

class ColorPolicy(PromptGenerator):
    def __init__(self):
        name = "Raw Color Composition and Dynamics Description"
        info = "A policy that uses existing labels to prompt a human or model to provide structured captions for Color Composition and Dynamics without subject/scene descriptions."
        caption_fields = ["raw_color_composition_dynamics"]
        super().__init__(name, info, caption_fields)

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "raw_color_composition_dynamics": self.get_prompt(data)
        }

    def format_color_temperature(self, color_temperature: str, color_temperature_dir="labels/lighting_setup/color_grading/temperature/") -> str:
        # Options: "warm", "cool", "neutral", "complex_changing", "complex_contrasting", "complex_others", "black_white"
        color_temperature_info = {
            "neutral": "color_temperature_is_neutral",
            "warm": "color_temperature_is_warm",
            "cool": "color_temperature_is_cool",
            "complex_changing": "color_temperature_is_changing",
            "complex_contrasting": "color_temperature_is_contrasting",
            "complex_others": "color_temperature_is_complex_others",
            # "black_white": "color_temperature_is_black_and_white",
        }
        if color_temperature == "black_white":
            return "The video is in black and white."
        else:
            color_temperature = color_temperature_info[color_temperature]
            color_temperature_str = read_json_file(os.path.join(color_temperature_dir, f"{color_temperature}.json"))['def_prompt'][0]
            if color_temperature == "color_temperature_is_neutral":
                color_temperature_str += " (no need to mention)."
            return color_temperature_str

    def format_colorfulness(self, colorfulness: str, colorfulness_dir="labels/lighting_setup/color_grading/colorfulness/") -> str:
        # Options: "high_colorfulness", "neutral", "low_colorfulness", "black_white", "complex_changing", "complex_contrasting", "complex_others"
        colorfulness_info = {
            "high_colorfulness": "colorfulness_is_high",
            "neutral": "colorfulness_is_neutral",
            "low_colorfulness": "colorfulness_is_low",
            "complex_changing": "colorfulness_is_changing",
            "complex_contrasting": "colorfulness_is_contrasting",
            "complex_others": "colorfulness_is_complex_others",
        }
        if colorfulness == "black_white":
            return "The video is in black and white."
        else:
            colorfulness = colorfulness_info[colorfulness]
            colorfulness_str = read_json_file(os.path.join(colorfulness_dir, f"{colorfulness}.json"))['def_prompt'][0]
            if colorfulness == "colorfulness_is_neutral":
                colorfulness_str += " (no need to mention)."
            return colorfulness_str

    def format_brightness_exposure(self, brightness: str, brightness_dir="labels/lighting_setup/color_grading/brightness/") -> str:
        # Options: "very_bright", "bright", "neutral", "dark", "very_dark", "complex_changing", "complex_contrasting", "complex_others"
        brightness_info = {
            "very_bright": "brightness_is_very_bright",
            "bright": "brightness_is_bright",
            "neutral": "brightness_is_neutral",
            "dark": "brightness_is_dark",
            "very_dark": "brightness_is_very_dark",
            "complex_changing": "brightness_is_changing",
            "complex_contrasting": "brightness_is_contrasting",
            "complex_others": "brightness_is_complex_others",
        }
        brightness = brightness_info[brightness]
        brightness_str = read_json_file(os.path.join(brightness_dir, f"{brightness}.json"))['def_prompt'][0]
        if brightness == "brightness_is_neutral":
            brightness_str += " (no need to mention)."
        return brightness_str

    def get_prompt(self, data: VideoData) -> str:
        if data.lighting_setup.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")

        policy = ""
        # policy += read_text_file("caption_policy/policy/color_composition_dynamics/policy.txt")
        policy += read_text_file("caption_policy/policy/color_composition_dynamics/policy_new.txt")

        policy += "\n\nWe have already provided some guidance on describing the aforementioned aspects of color composition. Please use these as references to expand your description."

        policy += "\n\n**Color Tone:** {}".format(self.format_color_temperature(data.lighting_setup.color_temperature))
        policy += "\n\n**Colorfulness:** {}".format(self.format_colorfulness(data.lighting_setup.colorfulness))
        policy += "\n\n**Brightness and Exposure:** {}".format(self.format_brightness_exposure(data.lighting_setup.brightness))
        policy += "\n\n" + read_text_file("caption_policy/policy/color_composition_dynamics/format_instruction.txt")
        return policy


class LightingSetupPolicy(PromptGenerator):
    def __init__(self):
        name = "Raw Lighting Setup and Dynamics Description"
        info = "A policy that uses existing labels to prompt a human or model to provide structured captions for Lighting Setup and Dynamics without subject/scene descriptions."
        caption_fields = ["raw_lighting_setup_dynamics"]
        super().__init__(name, info, caption_fields)

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {
            "raw_lighting_setup_dynamics": self.get_prompt(data)
        }

    def format_scene_type(self, scene_type: str, scene_type_dir="labels/lighting_setup/scene/") -> str:
        # Options: "interior", "exterior", "unrealistic_synthetic", "complex_others"
        scene_type_info = {
            "interior": "scene_type_is_interior",
            "exterior": "scene_type_is_exterior",
            "unrealistic_synthetic": "scene_type_is_synthetic",
            "complex_others": "scene_type_is_unclear_or_changing"
        }
        scene_type = scene_type_info[scene_type]
        scene_type_str = read_json_file(os.path.join(scene_type_dir, f"{scene_type}.json"))['def_prompt'][0]
        return scene_type_str

    def format_lighting_sources(self, lighting_setup, lighting_sources_dir="labels/lighting_setup/light_source/") -> str:
        # Major light sources
        # self.sunlight_source = lighting_setup.sunlight_source
        # self.moonlight_starlight_source = lighting_setup.moonlight_starlight_source
        # self.firelight_source = lighting_setup.firelight_source
        # self.artificial_light_source = lighting_setup.artificial_light_source
        # self.non_visible_light_source = lighting_setup.non_visible_light_source
        # self.abstract_light_source = lighting_setup.abstract_light_source
        # self.unclear_or_changing_light_source = lighting_setup.unclear_or_changing_light_source
        # if abstract_light_source is True, then the other sources are not considered
        light_source_strs = []
        # if lighting_setup.abstract_light_source:
        #     light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "is_abstract.json"))['def_prompt'][0])
        # else:
        if lighting_setup.sunlight_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_sunlight.json"))['def_prompt'][0])
        if lighting_setup.moonlight_starlight_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_moonlight_starlight.json"))['def_prompt'][0])
        if lighting_setup.firelight_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_firelight.json"))['def_prompt'][0])
        if lighting_setup.artificial_light_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_artificial_practical_light.json"))['def_prompt'][0])
        if lighting_setup.non_visible_light_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_non_visible_light_source.json"))['def_prompt'][0])
        if lighting_setup.unclear_or_changing_light_source:
            light_source_strs.append(read_json_file(os.path.join(lighting_sources_dir, "has_unclear_or_changing_light_source.json"))['def_prompt'][0])
        return " ".join(light_source_strs)

    def format_sunlight_level(self, sunlight_level: str, sunlight_level_dir="labels/lighting_setup/light_quality/sunlight_quality") -> str:
        # Options: "normal", "sunny", "overcast", "sunset_sunrise", "unknown"
        sunlight_level_info = {
            "normal": "sunlight_quality_is_normal",
            "sunny": "sunlight_quality_is_hard",
            "overcast": "sunlight_quality_is_soft",
            "sunset_sunrise": "sunlight_quality_is_sunset_sunrise",
        }
        sunlight_level = sunlight_level_info[sunlight_level]
        sunlight_level_str = read_json_file(os.path.join(sunlight_level_dir, f"{sunlight_level}.json"))['def_prompt'][0]
        return sunlight_level_str

    def format_light_quality(self, light_quality: str, light_quality_dir="labels/lighting_setup/light_quality/") -> str:
        # Options: "hard_light", "soft_light", "complex_changing", "complex_contrasting", "complex_others", "complex_ambiguous"
        light_quality_info = {
            "hard_light": "light_quality_is_hard",
            "soft_light": "light_quality_is_soft",
            "complex_changing": "light_quality_is_changing",
            "complex_contrasting": "light_quality_is_contrasting",
            "complex_others": "light_quality_is_complex_others",
            "complex_ambiguous": "light_quality_is_complex_ambiguous",
        }
        light_quality = light_quality_info[light_quality]
        light_quality_str = read_json_file(os.path.join(light_quality_dir, f"{light_quality}.json"))['def_prompt'][0]
        return light_quality_str

    def format_subject_lighting_contrast(self, lighting_setup, subject_lighting_dir="labels/lighting_setup/subject_lighting/light_contrast") -> str:
        # assert lighting_setup.is_subject_lighting_applicable, "Subject lighting must be applicable to format the subject lighting."
        subject_light_contrast_str = ""
        if lighting_setup.low_key_lighting is True:
            subject_light_contrast_str += read_json_file(os.path.join(subject_lighting_dir, "low_key_lighting.json"))['def_prompt'][0]
        if lighting_setup.high_key_lighting is True:
            subject_light_contrast_str += read_json_file(os.path.join(subject_lighting_dir, "high_key_lighting.json"))['def_prompt'][0]

        # self.subject_contrast_ratio = "unknown"  # Options: "high_contrast", "normal_contrast", "minimal_contrast", "complex", "unknown"
        subject_light_contrast_info = {
            "high_contrast": "subject_light_contrast_is_high",
            "normal_contrast": "subject_light_contrast_is_normal",
            "minimal_contrast": "subject_light_contrast_is_minimal",
            "complex_changing": "subject_light_contrast_is_changing",
            "complex_contrasting": "subject_light_contrast_is_contrasting",
            "complex_others": "subject_light_contrast_is_complex_others",
        }
        subject_light_contrast = subject_light_contrast_info[lighting_setup.subject_contrast_ratio]
        subject_light_contrast_str += " " + read_json_file(os.path.join(subject_lighting_dir, f"{subject_light_contrast}.json"))['def_prompt'][0]
        return subject_light_contrast_str

    def format_subject_lighting_direction(self, lighting_setup, subject_lighting_dir="labels/lighting_setup/subject_lighting/light_direction") -> str:
        # assert lighting_setup.is_subject_lighting_applicable, "Subject lighting must be applicable to format the subject lighting direction."
        if lighting_setup.direction_is_consistent is True:
            subject_light_direction_strs = []
            directions = [
                "direction_is_back_light",
                "direction_is_front_light",
                "direction_is_top_light",
                "direction_is_bottom_light",
                "direction_is_right_side_light",
                "direction_is_left_side_light",
                "direction_is_ambient_light"
            ]
            for direction in directions:
                if getattr(lighting_setup, direction) is True:
                    subject_light_direction_strs.append(read_json_file(os.path.join(subject_lighting_dir, f"{direction}.json"))['def_prompt'][0])
            assert len(subject_light_direction_strs) != 0, "Subject light direction must be specified if subject lighting is present."
            return " ".join(subject_light_direction_strs)
        else:
            complex_directions = [
                "direction_is_unknown",
                "direction_is_complex_others", # Must put before the below two because this includes the below two
                "direction_is_complex_changing",
                "direction_is_complex_contrasting",
            ]
            for direction in complex_directions:
                if getattr(lighting_setup, direction) is True:
                    return read_json_file(os.path.join(subject_lighting_dir, f"{direction}.json"))['def_prompt'][0]


    def format_subject_lighting_special_effects(self, lighting_setup, lighting_dir="labels/lighting_setup/") -> str:
        # Special lighting effects on subject
        # self.professional_lighting = False
        # self.rembrandt_lighting = False
        # # below two are actually not dependent on whether the subject is present or not
        # self.silhouette = False
        # self.rim_light = False
        special_light_effects_strs = []
        if lighting_setup.professional_lighting is True:
            special_light_effects_strs.append(read_json_file(os.path.join(lighting_dir, "subject_lighting", "professional_lighting.json"))['def_prompt'][0])
        if lighting_setup.rembrandt_lighting is True:
            special_light_effects_strs.append(read_json_file(os.path.join(lighting_dir, "subject_lighting", "rembrandt_lighting.json"))['def_prompt'][0])
        if lighting_setup.silhouette is True:
            special_light_effects_strs.append(read_json_file(os.path.join(lighting_dir, "special_effect", "silhouette.json"))['def_prompt'][0])
        if lighting_setup.rim_light is True:
            special_light_effects_strs.append(read_json_file(os.path.join(lighting_dir, "special_effect", "rim_light.json"))['def_prompt'][0])
        if len(special_light_effects_strs) == 0:
            return "No special lighting effects are observed on the subject. (no need to mention)."
        return " ".join(special_light_effects_strs)

    def get_prompt(self, data: VideoData) -> str:
        if data.lighting_setup.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")

        policy = ""
        policy += read_text_file("caption_policy/policy/lighting_setup_dynamics/policy.txt")

        policy += "\n\nWe have already provided some guidance on describing the aforementioned aspects of lighting setup. Please use these as references to expand your description. Keep your description a natural and brief paragraph without any formatting."

        policy += "\n\n**Scene Type:** {}".format(self.format_scene_type(data.lighting_setup.scene_type))
        policy += "\n\n**Light Source(s):** {}".format(self.format_lighting_sources(data.lighting_setup))
        # If sunlight, then ask about sunlight level
        if data.lighting_setup.sunlight_quality_is_unknown is False:
            policy += "\n\n**Sunlight Condition:** {}".format(self.format_sunlight_level(data.lighting_setup.sunlight_quality))
        policy += "\n\n**Light Quality:** {}".format(self.format_light_quality(data.lighting_setup.light_quality))

        # if data.lighting_setup.is_subject_lighting_applicable:
        policy += "\n\n**Light Contrast on Subject(s):** {}".format(self.format_subject_lighting_contrast(data.lighting_setup))
        policy += "\n\n**Light Direction(s) on Subject(s):** {}".format(self.format_subject_lighting_direction(data.lighting_setup))
        policy += "\n\n**Lighting Effects on Subject(s):** {}".format(self.format_subject_lighting_special_effects(data.lighting_setup))
        policy += "\n\n" + read_text_file("caption_policy/policy/lighting_setup_dynamics/format_instruction.txt")
        return policy


class LightingEffectsPolicy(PromptGenerator):
    def __init__(self):
        name = "Raw Lighting Effects and Dynamics Description"
        info = "A policy that uses existing labels to prompt a human or model to provide structured captions for Lighting Effects and Dynamics without subject/scene descriptions."
        caption_fields = ["raw_lighting_effects_dynamics"]
        super().__init__(name, info, caption_fields)

    def __call__(self, data: VideoData) -> Dict[str, str]:
        """Given a VideoData instance, return a dictionary of prompts for structured captions."""
        return {"raw_lighting_effects_dynamics": self.get_prompt(data)}

    
    def format_lens_effects(self, lighting_setup, lens_effects_dir="labels/lighting_setup/lens_effect/") -> str:
        lens_effect_strs = []
        lens_effects = [
            "lens_flares",
            "lens_flares_anamorphic",
            "mist_diffusion",
            "bokeh",
        ]
        for lens_effect in lens_effects:
            if getattr(lighting_setup, lens_effect) is True:
                lens_effect_strs.append(read_json_file(os.path.join(lens_effects_dir, f"{lens_effect}.json"))['def_prompt'][0])
        if len(lens_effect_strs) == 0:
            return False, "No significant lens or optical effects in this video. (no need to mention)."
        return True, " ".join(lens_effect_strs) + " (please include and explain these effects.)"

    def format_light_reflections(self, lighting_setup, light_reflections_dir="labels/lighting_setup/reflection/") -> str:
        light_reflections_strs = []
        light_reflections = [
            "reflection_from_water",
            "reflection_from_glossy_surface",
            "reflection_from_mirror",
        ]
        for light_reflection in light_reflections:
            if getattr(lighting_setup, light_reflection) is True:
                light_reflections_strs.append(read_json_file(os.path.join(light_reflections_dir, f"{light_reflection}.json"))['def_prompt'][0])
        if len(light_reflections_strs) == 0:
            return False, "No significant light reflections in this video. (no need to mention)."
        return True, " ".join(light_reflections_strs) + " (please include and explain these effects.)"

    def format_natural_lighting_effects(self, lighting_setup, natural_lighting_dir="labels/lighting_setup/natural_effect/") -> str:
        natural_lighting_strs = []
        natural_lightings = [
            "aerial_perspective",
            "rainbow",
            "aurora",
            "heat_haze",
            "lightning",
        ]
        for natural_lighting in natural_lightings:
            if getattr(lighting_setup, natural_lighting) is True:
                natural_lighting_strs.append(read_json_file(os.path.join(natural_lighting_dir, f"{natural_lighting}.json"))['def_prompt'][0])
        if len(natural_lighting_strs) == 0:
            return False, "No significant natural lighting effects in this video. (no need to mention)."
        return True, " ".join(natural_lighting_strs) + " (please include and explain these effects.)"

    def format_artificial_lighting_effects(self, lighting_setup, artificial_lighting_dir="labels/lighting_setup/special_effect/") -> str:
        # # Special lighting effects on the scene
        special_light_effects_strs = []
        special_light_effects = [
            "colored_neon_lighting",
            "headlight_flashlight",
            "vignette",
            "water_caustics",
            "city_light",
            "street_light",
        ]
        for special_light_effect in special_light_effects:
            if getattr(lighting_setup, special_light_effect) is True:
                special_light_effects_strs.append(read_json_file(os.path.join(artificial_lighting_dir, f"{special_light_effect}.json"))['def_prompt'][0])
        special_light_effects_without_subject = [
            "silhouette",
            "rim_light",
        ]
        # if lighting_setup.is_subject_lighting_applicable is False:
        for special_light_effect in special_light_effects_without_subject:
            if getattr(lighting_setup, special_light_effect) is True:
                special_light_effects_strs.append(read_json_file(os.path.join(artificial_lighting_dir, f"{special_light_effect}.json"))['def_prompt'][0])
        if len(special_light_effects_strs) == 0:
            return False, "No significant artificial or artistic lighting effects in this video. (no need to mention)."
        return True, " ".join(special_light_effects_strs) + " (please include and explain these effects.)"

    def format_volumetric_lighting(self, lighting_setup, volumetric_lighting_dir="labels/lighting_setup/volumetric_lighting/") -> str:
        volumetric_light_effects_strs = []
        volumetric_light_effects = [
            "volumetric_beam_light",
            "volumetric_spot_light",
            "god_rays",
            "light_through_medium",
            "volumetric_light_others"
        ]
        for volumetric_light_effect in volumetric_light_effects:
            if getattr(lighting_setup, volumetric_light_effect) is True:
                volumetric_light_effects_strs.append(read_json_file(os.path.join(volumetric_lighting_dir, f"{volumetric_light_effect}.json"))['def_prompt'][0])
        if len(volumetric_light_effects_strs) == 0:
            return False, "No significant volumetric lighting effects in this video. (no need to mention)."
        return True, " ".join(volumetric_light_effects_strs) + " (please include and explain these effects.)"

    def format_shadow_patterns(self, lighting_setup, shadow_patterns_dir="labels/lighting_setup/shadow_pattern/") -> str:
        # self.venetian_blinds or self.subject_shape or self.window_frames or self.foliage or self.shadow_patterns_gobo_others
        shadow_patterns_strs = []
        shadow_patterns = [
            "venetian_blinds",
            "subject_shape",
            "window_frames",
            "foliage",
            "shadow_patterns_gobo_others"
        ]
        for shadow_pattern in shadow_patterns:
            if getattr(lighting_setup, shadow_pattern) is True:
                shadow_patterns_strs.append(read_json_file(os.path.join(shadow_patterns_dir, f"{shadow_pattern}.json"))['def_prompt'][0])
        if len(shadow_patterns_strs) == 0:
            return False, "No distinct or noteworthy shadow patterns or Gobo lighting effects in this video. (no need to mention)."
        return True, " ".join(shadow_patterns_strs) + " (please include and explain these effects.)"

    def format_light_dynamics(self, lighting_setup, light_dynamics_dir="labels/lighting_setup/dynamic_light/") -> str:
        # Lighting dynamics
        # self.color_shifting_smooth = False
        # self.color_shifting_sudden = False
        # self.pulsing_flickering = False
        # self.flashing = False
        # self.moving_light = False
        light_dynamics_strs = []
        light_dynamics = [
            "color_shifting_smooth",
            "color_shifting_sudden",
            "pulsing_flickering",
            "flashing",
            "moving_light"
        ]
        for light_dynamic in light_dynamics:
            if getattr(lighting_setup, light_dynamic) is True:
                light_dynamics_strs.append(read_json_file(os.path.join(light_dynamics_dir, f"{light_dynamic}.json"))['def_prompt'][0])
        if len(light_dynamics_strs) == 0:
            return False, "No significant lighting dynamics in this video. (no need to mention)."
        return True, " ".join(light_dynamics_strs) + " (please include and explain these effects.)"

    def format_dynamics(self, lighting_setup, dynamics_dir="labels/lighting_setup/dynamic_effect/") -> str:
        other_dynamics_strs = []
        other_dynamics = [
            "revealing_shot",
            "transformation_morphing",
            "levitation_floating",
            "explosion",
            "shattering_breaking",
            "diffusion",
            "splashing_waves"
        ]
        for other_dynamic in other_dynamics:
            if getattr(lighting_setup, other_dynamic) is True:
                other_dynamics_strs.append(read_json_file(os.path.join(dynamics_dir, f"{other_dynamic}.json"))['def_prompt'][0])
        if len(other_dynamics_strs) == 0:
            return False, "No other significant dynamics in this video. (no need to mention)."
        return True, " ".join(other_dynamics_strs) + " (please include and explain these effects.)"
    
    def get_prompt(self, data: VideoData) -> str:
        if data.lighting_setup.shot_transition:
            raise ValueError("Shot transitions are not supported in this policy.")

        policy = ""
        policy += read_text_file("caption_policy/policy/lighting_effects_dynamics/policy.txt")

        policy += "\n\nWe have already provided some guidance on describing the aforementioned aspects of lighting effects. Please use these as references to expand your description. Keep your description a natural and brief paragraph without any formatting."

        lens_effects_exist, lens_effects_str = self.format_lens_effects(data.lighting_setup)
        light_reflections_exist, light_reflections_str = self.format_light_reflections(data.lighting_setup)
        natural_lighting_exist, natural_lighting_str = self.format_natural_lighting_effects(data.lighting_setup)
        artificial_lighting_exist, artificial_lighting_str = self.format_artificial_lighting_effects(data.lighting_setup)
        volumetric_lighting_exist, volumetric_lighting_str = self.format_volumetric_lighting(data.lighting_setup)
        shadow_patterns_exist, shadow_patterns_str = self.format_shadow_patterns(data.lighting_setup)
        light_dynamics_exist, light_dynamics_str = self.format_light_dynamics(data.lighting_setup)
        dynamics_exist, dynamics_str = self.format_dynamics(data.lighting_setup)
        policy += "\n\n**Lens and Optical Effects:** {}".format(lens_effects_str)
        policy += "\n\n**Light Reflections:** {}".format(light_reflections_str)
        policy += "\n\n**Natural Lighting Effects:** {}".format(natural_lighting_str)
        policy += "\n\n**Artificial or Artistic Lighting Effects:** {}".format(artificial_lighting_str)
        policy += "\n\n**Volumetric Lighting:** {}".format(volumetric_lighting_str)
        policy += "\n\n**Shadow Patterns or Gobo Lighting Effects:** {}".format(shadow_patterns_str)
        policy += "\n\n**Lighting Dynamics:** {}".format(light_dynamics_str)
        policy += "\n\n**Other Dynamics: {}".format(dynamics_str)
        policy += "\n\n" + read_text_file("caption_policy/policy/lighting_effects_dynamics/format_instruction.txt")
        return policy
