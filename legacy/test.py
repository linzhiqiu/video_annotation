# python test.py --video_url_files video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json
import os
from tqdm import tqdm
import argparse
import json
from process_json import json_to_video_data
from caption_policy.prompt_generator import VanillaCameraMotionPolicy
from llm import get_llm, get_all_llms, get_supported_mode
from download import download_videos, get_video_labels_dir, load_from_json, save_to_json
from caption_policy.prompt_generator import SubjectPolicy, ScenePolicy, SubjectMotionPolicy, SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, RawSpatialPolicy, RawSubjectMotionPolicy
import streamlit as st

caption_programs = {
    "subject_description": SubjectPolicy(),
    "scene_composition_dynamics": ScenePolicy(),
    "subject_motion_dynamics": SubjectMotionPolicy(),
    "spatial_framing_dynamics": SpatialPolicy(),
    "camera_framing_dynamics": CameraPolicy(),
    "camera_motion": VanillaCameraMotionPolicy(),
    "raw_spatial_framing_dynamics": RawSpatialPolicy(),
    "raw_subject_motion_dynamics": RawSubjectMotionPolicy(),
}
# from caption.feedback_app import caption_programs, load_video_data, file_check, load_config, FOLDER, load_json, get_imagery_kwargs, st

def load_video_data(video_data_file, label_collections=["cam_motion", "cam_setup", "lighting_setup"]):
    video_data_dict = json_to_video_data(video_data_file, label_collections=label_collections)
    for video_data in video_data_dict.values():
        video_data.cam_motion.update()
        if hasattr(video_data, "cam_setup"):
            video_data.cam_setup.update()
            if getattr(video_data.cam_setup, "subject_description", None) is None:
                video_data.cam_setup.subject_description = "**{NO DESCRIPTION FOR SUBJECTS YET}**"
            if getattr(video_data.cam_setup, "scene_description", None) is None:
                video_data.cam_setup.scene_description = "**{NO DESCRIPTION FOR SCENE YET}**"
            if getattr(video_data.cam_setup, "motion_description", None) is None:
                video_data.cam_setup.motion_description = "**{NO DESCRIPTION FOR SUBJECT MOTION YET}**"
            if getattr(video_data.cam_setup, "spatial_description", None) is None:
                video_data.cam_setup.spatial_description = "**{NO DESCRIPTION FOR SPATIAL FRAMING YET}**"
            if getattr(video_data.cam_setup, "camera_description", None) is None:
                video_data.cam_setup.camera_description = "**{NO DESCRIPTION FOR CAMERA FRAMING YET}**"
    return video_data_dict

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument("--video_urls_file", type=str, default="video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json", help="Path to the test URLs file")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    # parser.add_argument("--video_data", type=str, default="video_data/20250224_0130/videos.json", help="Path to the video data file")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    return parser.parse_args()

args = parse_args()
# Load video data
config_dict = data = {
    'Subject Description Caption': {
        'name': 'Subject Description Caption',
        'task': 'subject_description',
        'timestamp': '2025-02-25',
        'instruction_file': 'human/subject_description.txt',
        'output_name': 'subject_description'
    },
    'Subject Motion and Dynamics Caption': {
        'name': 'Subject Motion and Dynamics Caption',
        'task': 'subject_motion_dynamics',
        'timestamp': '2025-02-25',
        'instruction_file': 'human/subject_motion_dynamics.txt',
        'output_name': 'subject_motion_dynamics'
    },
    'Scene Composition and Dynamics Caption': {
        'name': 'Scene Composition and Dynamics Caption',
        'task': 'scene_composition_dynamics',
        'timestamp': '2025-02-25',
        'instruction_file': 'human/scene_composition_dynamics.txt',
        'output_name': 'scene_composition_dynamics'
    },
    'Spatial Framing and Dynamics Caption': {
        'name': 'Spatial Framing and Dynamics Caption',
        'task': 'spatial_framing_dynamics',
        'timestamp': '2025-02-25',
        'instruction_file': 'human/spatial_framing_dynamics.txt',
        'output_name': 'spatial_framing_dynamics'
    },
    'Camera Framing and Dynamics Caption': {
        'name': 'Camera Framing and Dynamics Caption',
        'task': 'camera_framing_dynamics',
        'timestamp': '2025-02-25',
        'instruction_file': 'human/camera_framing_dynamics.txt',
        'output_name': 'camera_framing_dynamics'
    },
    '(Raw) Spatial Framing and Dynamics Caption': {
        'name': '(Raw) Spatial Framing and Dynamics Caption',
        'task': 'raw_spatial_framing_dynamics',
        'timestamp': '2025-03-13',
        'instruction_file': 'human/spatial_framing_dynamics.txt',
        'output_name': 'raw_spatial_framing_dynamics'
    },
    '(Raw) Subject Motion and Dynamics Caption': {
        'name': '(Raw) Subject Motion and Dynamics Caption',
        'task': 'raw_subject_motion_dynamics',
        'timestamp': '2025-03-12',
        'instruction_file': 'human/subject_motion_dynamics.txt',
        'output_name': 'raw_subject_motion_dynamics'
    }
}

config_names = ['Subject Description Caption', 'Subject Motion and Dynamics Caption', 'Scene Composition and Dynamics Caption', 'Spatial Framing and Dynamics Caption', 'Camera Framing and Dynamics Caption', '(Raw) Spatial Framing and Dynamics Caption', '(Raw) Subject Motion and Dynamics Caption']
# Dropdown to select a config, updating session state
video_urls = ['https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/d_T0KPYgqMA.0.2.mp4', 'https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/e_ofen9SDeM.3.0.mp4', 'https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/f4ZzHtww6Tc.2.2.mp4', 'https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/fSWFUFdV5TU.0.1.mp4']
llm_names = get_all_llms()
selected_video = 'https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/d_T0KPYgqMA.0.2.mp4'
selected_llm = 'gemini-2.0-flash-001'
# selected_llm = "gpt-4o-2024-08-06"
# selected_config = 'Scene Composition and Dynamics Caption'
selected_config = 'Subject Description Caption'
# selected_mode = "Video"
selected_mode = "Image (First-and-Last-Frame)"
# selected_mode = "Text Only"
video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)

# Get video ID from URL
def get_video_id(url):
    return url.split('/')[-1]

def get_imagery_kwargs(selected_mode, selected_video):
    if selected_mode == "Text Only":
        return {}
    
    imagery_kwargs = {"video": selected_video}
    if selected_mode == "Image (First-and-Last-Frame)":
        imagery_kwargs.update({"extracted_frames": [0, -1]})
    elif selected_mode == "Video":
        pass
    return imagery_kwargs
    
# Dropdown to select a config, updating session state
supported_modes = get_supported_mode(selected_llm)
config = config_dict[selected_config]
# video_urls = load_json(FOLDER / args.video_urls_file)
caption_program = caption_programs[config["task"]]
video_id = get_video_id(selected_video)
current_prompt = caption_program(video_data_dict[video_id])[config["task"]]
        
print(f"Generating pre-caption for video: {video_id}")
imagery_kwargs = get_imagery_kwargs(selected_mode, selected_video)
pre_caption = get_llm(
    model=selected_llm,
    secrets=st.secrets,
).generate(
    current_prompt,
    **imagery_kwargs
)
pre_caption_data = {
    "video_id": selected_video,
    "pre_caption_prompt": current_prompt,
    "pre_caption": pre_caption,
    "pre_caption_llm": selected_llm,
    "pre_caption_mode": selected_mode,
}
print(f"Pre-caption generated for video: {selected_video}")
print(json.dumps(pre_caption_data, indent=4))