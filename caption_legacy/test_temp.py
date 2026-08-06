import streamlit as st
import argparse
from streamlit_feedback import streamlit_feedback
import os
import torch
import json
from datetime import datetime
from pathlib import Path
from utils import extract_frames, load_config, load_json, get_last_frame_index
from llm import get_llm, get_all_llms, get_supported_mode
from caption_policy.prompt_generator import SubjectPolicy, ScenePolicy, SubjectMotionPolicy, SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, RawSpatialPolicy, RawSubjectMotionPolicy
from process_json import json_to_video_data

caption_programs = {
    "subject_description": SubjectPolicy(),
    "scene_composition_dynamics": ScenePolicy(),
    "subject_motion_dynamics": SubjectMotionPolicy(),
    "spatial_framing_dynamics": SpatialPolicy(),
    "camera_framing_dynamics": CameraPolicy(),
    # "camera_motion": VanillaCameraMotionPolicy(),
    # "raw_spatial_framing_dynamics": RawSpatialPolicy(),
    # "raw_subject_motion_dynamics": RawSubjectMotionPolicy(),
}

PRECAPTION_FILE_POSTFIX = "_precaption.json"
FEEDBACK_FILE_POSTFIX = "_feedback.json"
SUBJECT_CAPTION_NAME = "Subject Description Caption"
SCENE_CAPTION_NAME = "Scene Composition and Dynamics Caption"
PROMPT_HEIGHT = 225
# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_all.json", help="Path to the test URLs file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_selected.json", help="Path to the test URLs file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=[
            "video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json",
            "video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json",
            "video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json",
            "video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json",
            "video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json",
            "video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json",
            "video_urls/20250227_0507ground_and_setup/overlap_564_to_658.json",
            "video_urls/20250227_0507ground_and_setup/overlap_658_to_752.json",
            "video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json",
            "video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json",
        ],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    # parser.add_argument("--video_data", type=str, default="video_data/20250224_0130/videos.json", help="Path to the video data file")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    return parser.parse_args()


def login_page(args):
    st.title("Video Caption System Login")

    # Create a form for login
    with st.form("login_form"):
        # File selection dropdown
        selected_file = st.selectbox(
            "Select Video URLs File:", args.video_urls_files, key="selected_urls_file"
        )

        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Store the selected file in session state
            st.session_state.video_urls_file = selected_file
            st.session_state.logged_in = True
            st.success(f"Login successful! Selected file: {selected_file}")
            st.rerun()


def load_video_data(video_data_file, label_collections=["cam_motion", "cam_setup", "lighting_setup"]):
    video_data_dict = json_to_video_data(video_data_file, label_collections=label_collections)
    for video_data in video_data_dict.values():
        if hasattr(video_data, "cam_setup"):
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
            if getattr(video_data.cam_setup, "color_description", None) is None:
                video_data.cam_setup.color_description = "**{NO DESCRIPTION FOR COLOR COMPOSITION YET}**"
            if getattr(video_data.cam_setup, "lighting_description", None) is None:
                video_data.cam_setup.lighting_description = "**{NO DESCRIPTION FOR LIGHTING SETUP YET}**"
            if getattr(video_data.cam_setup, "lighting_effects_description", None) is None:
                video_data.cam_setup.lighting_effects_description = "**{NO DESCRIPTION FOR LIGHTING EFFECTS YET}**"
        if hasattr(video_data, "lighting_setup"):
            video_data.lighting_setup.update()
    return video_data_dict


def emoji_to_score(emoji):
    """Convert emoji rating to 1-5 Likert scale"""
    emoji_map = {
        "😞": 1,  # Very unhappy
        "🙁": 2,  # Unhappy
        "😐": 3,  # Neutral
        "🙂": 4,  # Happy
        "😀": 5   # Very happy
    }
    # If not found, raise an error
    if emoji not in emoji_map:
        raise ValueError("Invalid emoji rating provided.")
    return emoji_map.get(emoji, None)  # Default to neutral if emoji not found

def get_filename(video_id, output_dir="outputs", file_postfix=".json"):
    """Get the filename for saving feedback data"""
    return os.path.join(output_dir, f'{video_id}{file_postfix}')

def save_data(video_id, data, output_dir="outputs", file_postfix=".json"):
    """Save feedback data to a JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = get_filename(video_id, output_dir, file_postfix)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to: {filename}")
    return filename

def get_precaption_llm_name(config_dict, selected_config):
    config = config_dict[selected_config]
    task = config["task"]
    if task in ["subject_motion_dynamics"]:
        return "tarsier-recap-7b"
    elif task in ["spatial_framing_dynamics"]:
        return "qwen2.5-vl-72b"
    elif task in ["raw_lighting_setup_dynamics", "raw_lighting_effects_dynamics"]:
        print(f"Using qwen2.5-vl-7b for {task}")
        return "qwen2.5-vl-7b"
    else:
        return "gpt-4o-2024-08-06"

def load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, output):
    """Generate a pre-caption for the video"""
    # Get the caption prompt for the video
    config = config_dict[selected_config]
    task = config["task"]
    
    if task in ["subject_motion_dynamics"]:
        # Need to update the "subject_description" if exists
        subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
        existing_subject_feedback = load_data(video_id, output_dir=FOLDER / output / subject_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        if existing_subject_feedback:
            st.success("Loading previously generated subject caption...")
            subject_caption = existing_subject_feedback["final_caption"]
            video_data_dict[video_id].cam_setup.subject_description = subject_caption
        else:
            st.info("No subject caption found. Please generate the subject caption first.")
            st.rerun()
            raise ValueError("This line will not be run because rerun will be called.")
    elif task in ["spatial_framing_dynamics", "color_composition_dynamics", "lighting_setup_dynamics", "lighting_effects_dynamics"]:
        # Need to update both "subject_description" and "scene_composition_dynamics" if exists
        subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
        scene_output_name = config_dict[SCENE_CAPTION_NAME]["output_name"]
        existing_subject_feedback = load_data(video_id, output_dir=FOLDER / output / subject_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        existing_scene_feedback = load_data(video_id, output_dir=FOLDER / output / scene_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        if existing_subject_feedback and existing_scene_feedback:
            st.success("Loading previously generated subject and scene captions...")
            subject_caption = existing_subject_feedback["final_caption"]
            scene_caption = existing_scene_feedback["final_caption"]
            video_data_dict[video_id].cam_setup.subject_description = subject_caption
            video_data_dict[video_id].cam_setup.scene_description = scene_caption
        else:
            st.info("No subject and scene captions found. Please generate the subject and scene captions first.")
            st.rerun()
            raise ValueError("This line will not be run because rerun will be called.")
    
    # Generate the new prompt and caption
    pre_caption_prompt = caption_program(video_data_dict[video_id])[task]
        
    return pre_caption_prompt

def load_precaption(video_id, output_dir, file_postfix=PRECAPTION_FILE_POSTFIX):
    """Load pre-caption for video. If not exist, generate a new one."""
    # Check for existing feedback and get current caption
    existing_precaption = load_data(video_id, output_dir=output_dir, file_postfix=file_postfix)
    
    # Show existing feedback if available
    if existing_precaption:
        # st.success("Loading previously generated pre-caption...")
        # print(f"Pre-caption found for video: {video_id}")
        return existing_precaption
    else:
        st.info("No pre-caption found. Generating a new pre-caption.")
        # print(f"No pre-caption found for video: {video_id}")
        return {}

def load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
    """Load feedback for video. If not exist, generate a new one."""
    # Check for existing feedback and get current caption
    existing_feedback = load_data(video_id, output_dir=output_dir, file_postfix=file_postfix)

    # Show existing feedback if available
    if existing_feedback:
        st.success("This video has already been completed. The final caption is:")
        st.write(existing_feedback["final_caption"])
        # Render as collapsible text
        with st.expander("Show final JSON Data", expanded=False):
            st.json(existing_feedback)
        return existing_feedback
    else:
        st.info("No pre-caption found. Generating a new pre-caption.")
        # print(f"No pre-caption found for video: {video_id}")
        return {}

def data_is_saved(video_id, output_dir="outputs", file_postfix=".json"):
    """Check if data already exists"""
    filename = os.path.join(output_dir, f'{video_id}{file_postfix}')
    return os.path.exists(filename)

def load_data(video_id, output_dir="outputs", file_postfix=".json"):
    """Load existing feedback data for a video if it exists"""
    filename = os.path.join(output_dir, f'{video_id}{file_postfix}')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


# Get video ID from URL
def get_video_id(url):
    return url.split('/')[-1]

# Load instructions from file
def load_txt(txt_file):
    with open(txt_file, "r") as f:
        return f.read()

# Load prompt template
def load_prompt(filename, **kwargs):
    with open(filename, "r") as f:
        prompt = f.read()
    return prompt.format(**kwargs)

def generate_save_and_return_pre_caption(video_id, output_dir, prompt, selected_llm, selected_mode, selected_video, file_postfix=PRECAPTION_FILE_POSTFIX):
    print(f"Generating pre-caption for video: {video_id}")
    imagery_kwargs = get_imagery_kwargs(selected_mode, selected_video)
    pre_caption = get_llm(
        model=selected_llm,
        secrets=st.secrets,
    ).generate(
        prompt,
        **imagery_kwargs
    )
    pre_caption_data = {
        "video_id": video_id,
        "pre_caption_prompt": prompt,
        "pre_caption": pre_caption,
        "pre_caption_llm": selected_llm,
        "pre_caption_mode": selected_mode,
    }
    save_data(video_id, pre_caption_data, output_dir=output_dir, file_postfix=file_postfix)
    print(f"Pre-caption generated for video: {video_id}")
    return pre_caption


def get_video_format_func(output_dir, file_postfix=".json"):
    def video_format_func(video_url):
        # if already exists, then return f"✅ {video_url}"
        video_id = get_video_id(video_url)
        # Check for existing feedback and get current caption
        existing_data = load_data(video_id, output_dir=output_dir, file_postfix=file_postfix)
        video_url = video_url.split("/")[-1]
        # Show existing feedback if available
        if existing_data:
            return f"✅ {video_url}"
        return f"{video_url}"
    return video_format_func

def get_imagery_kwargs(selected_mode, selected_video):
    if selected_mode == "Text Only":
        return {}
    
    imagery_kwargs = {"video": selected_video}
    if selected_mode == "Image (First-and-Last-Frame)":
        imagery_kwargs.update({"extracted_frames": [0, -1]})
    elif selected_mode == "Image (3 frames)":
        last_idx = get_last_frame_index(selected_video)
        # Uniformly sample 3 frames: first, middle, and last
        middle_idx = last_idx // 2
        imagery_kwargs.update({"extracted_frames": [0, middle_idx, last_idx]})
    elif selected_mode == "Image (4 frames)":
        last_idx = get_last_frame_index(selected_video)
        # For 4 evenly spaced frames, divide into 3 equal segments
        segment = last_idx / 3  # Using floating point division for precision
        frame_indices = [
            0,
            int(segment),
            int(2 * segment),
            last_idx
        ]
        imagery_kwargs.update({"extracted_frames": frame_indices})
    elif selected_mode == "Video":
        pass
    return imagery_kwargs

def file_check(video_urls_file, video_data_dict):
    video_urls = load_json(FOLDER / video_urls_file)
    video_ids = [get_video_id(video_url) for video_url in video_urls]
    missing_video = False
    for video_id in video_ids:
        if video_id not in video_data_dict:
            st.error(f"Video ID {video_id} not found in the video data file.")
            print(f"Video ID not found: {video_id}")
            missing_video = True
    if missing_video:
        return

def main(args, caption_programs):
    # Set page config first
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # Check login status
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page(args)
        return

    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    if "file_check_passed" not in st.session_state:
        file_check(st.session_state.video_urls_file, video_data_dict)
        st.session_state.file_check_passed = True

    # Hide sidebar by default
    # st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    # st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    # Create two columns
    page_col1, page_col2 = st.columns([1, 1])  # Left column is smaller, right column is wider

    # Add logout button
    st.sidebar.title("User Options")
    if st.sidebar.button("Logout"):
        # Clear session state and logout
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Debug information
    st.sidebar.header("Debug Information")
    st.sidebar.write("Full Session State:")
    for key, value in st.session_state.items():
        st.sidebar.write(f"{key}: {value}")
    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        st.error(f"Config file not found: {args.configs}")
        return

    with page_col1:
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        # Dropdown to select a config, updating session state
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_task",
        )

        # Track task changes to reset state
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Config changed, reset all state variables
            # First, collect all keys to remove
            keys_to_remove = []
            for key in st.session_state:
                # Keep api_key and last_config_id
                if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 'video_urls_file']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_config_id = selected_config
            print(f"Config changed to: {selected_config}")
            st.rerun()  # Force a rerun to ensure clean state

        config = config_dict[selected_config]
        st.title(config.get("name", "Pre-Caption System"))
        video_urls = load_json(FOLDER / st.session_state.video_urls_file)
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Select video
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=get_video_format_func(output_dir, file_postfix=FEEDBACK_FILE_POSTFIX),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video"
        )
        video_id = get_video_id(selected_video)
        caption_program = caption_programs[config["task"]]
        current_prompt = caption_program(video_data_dict[video_id])[config["task"]]

        # Track video changes to reset state
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            # Video changed, reset all state variables
            # First, collect all keys to remove
            keys_to_remove = []
            for key in st.session_state:
                # Keep api_key and last_video_id
                if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'file_check_passed', 'logged_in', 'video_urls_file']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video

            # Also clear any feedback component states
            if 'feedback_submitted_initial_caption_faces' in st.session_state:
                del st.session_state['feedback_submitted_initial_caption_faces']

            st.rerun()  # Force a rerun to ensure clean state

        # Session state initialization
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'precaption_data' not in st.session_state:
            st.session_state.precaption = {}
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = {}

        # Display instructions
        st.subheader("Instructions")
        with st.expander("📜 Instructions (Click to Expand/Collapse)", expanded=False):
            # Load instructions from file, otherwise throw a warning
            if "instruction_file" not in config:
                st.warning("No instruction_file found in the configuration file.")
            else:
                st.write(load_txt(FOLDER / config["instruction_file"]))

        # Display video
        st.video(selected_video)

        # Display first and last frames
        extracted_frames = extract_frames(selected_video, [0, -1])
        # Expandable section
        with st.expander("Frames (Click to Expand/Collapse)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.image(extracted_frames[0], caption="First Frame", use_container_width=True)
            with col2:
                st.image(extracted_frames[1], caption="Last Frame", use_container_width=True)
        
        with st.expander("Show Links", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            # ['cam_motion', 'cam_setup', 'lighting_setup'] check workflows['cam_motion'].editing_url
            
            
            with col1:
                if 'cam_motion' in video_data_dict[video_id].workflows:
                    st.link_button("🔗 Cam-Motion", video_data_dict[video_id].workflows['cam_motion'].editing_url)
                else:
                    st.link_button("🔗 Cam-Motion", "https://example.com/a", type='secondary', disabled=True)
                    
            with col2:
                if 'cam_setup' in video_data_dict[video_id].workflows:
                    st.link_button("🔗 Cam-Setup", video_data_dict[video_id].workflows['cam_setup'].editing_url)
                else:
                    st.link_button("🔗 Cam-Setup", "https://example.com/b", type='secondary', disabled=True)
                    
            with col3:
                if 'lighting_setup' in video_data_dict[video_id].workflows:
                    st.link_button("🔗 Lighting-Setup", video_data_dict[video_id].workflows['lighting_setup'].editing_url)
                else:
                    st.link_button("🔗 Lighting-Setup", "https://example.com/c", type='secondary', disabled=True)
            
            st.link_button("🔗 Report Label Errors Here", "https://docs.google.com/spreadsheets/d/1sAYL86ERcaC_vrVuloXxtPJXKzeuj8fukHtNv6nRCJ0/edit?usp=sharing", use_container_width=True)

        # Add navigation buttons for previous and next videos
        nav_col1, _, nav_col2 = st.columns([1, 3, 1])
        with nav_col1:
            # Get index of current video in the list
            current_index = video_urls.index(selected_video)
            # Enable prev button only if not the first video
            if current_index > 0:
                if st.button("⬅️ Prev Video"):
                    # Set the new selected video to be the previous one in the list
                    st.session_state.last_selected_video = video_urls[current_index - 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index - 1])
                    # Reset relevant state variables
                    keys_to_remove = [key for key in st.session_state if key not in 
                                    ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls_file']]
                    for key in keys_to_remove:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            else:
                # Disabled button style if it's the first video
                st.button("⬅️ Prev Video", disabled=True)

        with nav_col2:
            # Enable next button only if not the last video
            if current_index < len(video_urls) - 1:
                if st.button("Next Video ➡️"):
                    # Set the new selected video to be the next one in the list
                    st.session_state.last_selected_video = video_urls[current_index + 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index + 1])
                    # Reset relevant state variables
                    keys_to_remove = [key for key in st.session_state if key not in 
                                    ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls_file']]
                    for key in keys_to_remove:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            else:
                # Disabled button style if it's the last video
                st.button("Next Video ➡️", disabled=True)

    with page_col2:
        # Step 0: Generating Pre-caption
        if st.session_state.current_step == 0:
            # If feedback already exists, load it
            if data_is_saved(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
                load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                st.write("Feedback already exists for this video. You can choose to restart by either re-generating the pre-caption or by providing a new rating.")

            # If not exist, return empty dict
            existing_precaption = load_precaption(video_id, output_dir, file_postfix=PRECAPTION_FILE_POSTFIX)
            # st.write("##### Pre-caption was generated by ")
            # st.write("Please polish the prompt and select an option to generate a caption:")
            llm_names = get_all_llms()

            # Dropdown to select a config, updating session state
            selected_llm = st.selectbox(
                "Select a Model:",
                llm_names,
                # index=llm_names.index(existing_precaption.get("pre_caption_llm", get_precaption_llm_name(config_dict, selected_config))),
                index=llm_names.index(get_precaption_llm_name(config_dict, selected_config)),
                key="selected_llm"
            )
            supported_modes = get_supported_mode(selected_llm)
            # supprted_modes_index = supported_modes.index(existing_precaption.get("pre_caption_mode", supported_modes[0])) if existing_precaption.get("pre_caption_mode", supported_modes[0]) in supported_modes else 0
            supprted_modes_index = 0
            selected_mode = st.selectbox(
                "Select a Mode:",
                supported_modes, 
                index=supprted_modes_index,
                key="selected_mode"
            )

            if "pre_caption_prompt" in st.session_state:
                pre_caption_prompt = st.session_state.pre_caption_prompt
            else:
                # pre_caption_prompt = existing_precaption.get("pre_caption_prompt", load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, args.output))
                pre_caption_prompt = load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, args.output)

            line_height = 6  # Approximate height per line in pixels
            num_lines = max(30, len(pre_caption_prompt) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height

            current_prompt = st.text_area(
                "Prompt for pre-captioning:",
                value=pre_caption_prompt,
                key="pre_caption_prompt",
                height=estimated_height,
            )

            if "pre_caption" in existing_precaption:
                pre_caption = existing_precaption["pre_caption"]
            else:
                pre_caption = generate_save_and_return_pre_caption(video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video) # TODO: Comment out this line
                # pre_caption = "**No pre-caption generated yet. Please click the button above to re-generate a pre-caption.**"

            st.session_state.pre_caption_data = {
                "video_id": video_id,
                "pre_caption_prompt": current_prompt,
                "pre_caption": pre_caption,
                "pre_caption_llm": selected_llm,
                "pre_caption_mode": selected_mode,
            }
            if st.button("Re-generate a pre-caption"):
                st.info("Be patient, this may take a while...")
                generate_save_and_return_pre_caption(video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video)
                st.rerun()  # Force a rerun to ensure clean state

            # Wait for user to confirm pre-caption by clicking on feedback
            # st.write(f"##### Pre-caption generated by {selected_llm} ({selected_mode})")
            st.write(f"##### Current pre-caption")
            st.write(pre_caption)
            st.write("#### Rate the caption (Is it accurate? Does it miss anything important?)")


            st.write("Please provide your feedback to improve this caption (if not score of 5):")
            user_feedback = st.text_area(
                "Your feedback:",
                key=f"user_feedback_{video_id}_{config['name']}",
                height=PROMPT_HEIGHT,
            )
            
            # Fetch stored initial rating if it exists
            if "initial_caption_rating" in st.session_state:
                score = st.session_state.initial_caption_rating
            else:
                initial_rating_response = streamlit_feedback(
                    feedback_type="faces",
                    key=f"initial_caption_faces_{video_id}_{config['name']}"
                )

                if initial_rating_response:
                    st.session_state.initial_caption_rating = initial_rating_response['score']
                    score = initial_rating_response['score']
                else:
                    score = None

            if score:
                feedback_is_needed = score != "😀"

                # Initialize feedback data
                st.session_state.feedback_data = {
                    "video_id": video_id,
                    "pre_caption": pre_caption,
                    "pre_caption_prompt": current_prompt,
                    "pre_caption_llm": selected_llm,
                    "pre_caption_mode": selected_mode,
                    "original_caption": pre_caption,
                    "initial_caption_rating": score,
                    "initial_caption_rating_score": emoji_to_score(score),
                    "feedback_is_needed": feedback_is_needed,
                    "timestamp": datetime.now().isoformat(),
                    # Initialize other fields as None
                    "initial_feedback": None,
                    "gpt_feedback_llm": None, 
                    "gpt_feedback_prompt": None, 
                    "gpt_feedback": None,
                    "feedback_rating": None,
                    "feedback_rating_score": None,
                    "final_feedback": None,
                    "gpt_caption_llm": None, 
                    "gpt_caption_prompt": None,
                    "gpt_caption": None,
                    "caption_rating": None,
                    "caption_rating_score": None,
                    "final_caption": None
                }

                if feedback_is_needed:
                    st.write("You can optionally change the LLM or the prompt that we used to polish your feedback. Please keep {feedback} and {pre_caption} in the prompt.")
                    llm_names = get_all_llms()
                    # Dropdown to select a config, updating session state
                    selected_feedback_llm = st.selectbox(
                        "Select a Model:",
                        llm_names,
                        key="selected_feedback_llm",
                        index=llm_names.index("gpt-4o-2024-08-06"),
                    )
                    if "cur_feedback_prompt" in st.session_state:
                        feedback_prompt = st.session_state.cur_feedback_prompt
                    else:
                        feedback_prompt = load_txt(FOLDER / args.feedback_prompt)

                    feedback_prompt = st.text_area(
                        "Prompt for polishing feedback:",
                        value=feedback_prompt,
                        key="cur_feedback_prompt",
                        height=PROMPT_HEIGHT,
                    )
                    if st.button("Submit Feedback") and user_feedback:
                        st.session_state.feedback_data["initial_feedback"] = user_feedback
                        st.session_state.feedback_data["gpt_feedback_llm"] = selected_feedback_llm
                        st.session_state.feedback_data["gpt_feedback_prompt"] = feedback_prompt
                        # Get GPT-4 polished feedback
                        new_feedback = get_llm(
                            model=selected_feedback_llm,
                            secrets=st.secrets,
                        ).generate(
                            feedback_prompt.format(feedback=user_feedback, pre_caption=pre_caption),
                        )
                        st.session_state.feedback_data["gpt_feedback"] = new_feedback
                        st.session_state.current_step = 1
                        st.rerun()
                else:
                    # If happiest face, save and finish
                    st.session_state.feedback_data["final_caption"] = pre_caption
                    save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                    st.success("Caption rated as perfect! No changes needed.")
                    st.json(st.session_state.feedback_data)

        # Step 1: Rate GPT's feedback and optionally provide corrected feedback
        if st.session_state.current_step == 1:
            # Wait for user to confirm pre-caption by clicking on feedback
            st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
            st.write(st.session_state.feedback_data["pre_caption"])
            st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
            st.write(f"##### Your Feedback")
            st.write(f"{st.session_state.feedback_data['initial_feedback']}")
            st.write(f"##### Polished Feedback from {st.session_state.feedback_data['gpt_feedback_llm']}")
            st.write(f"{st.session_state.feedback_data['gpt_feedback']}")
            st.subheader(f"Please Rate AI-Polished Feedback")


            st.write("Please provide the final feedback if you are not happy with it:")

            # Ensure final_feedback is stored persistently
            if "final_feedback" not in st.session_state:
                st.session_state.final_feedback = st.session_state.feedback_data["gpt_feedback"]

            line_height = 10  # Approximate height per line in pixels
            num_lines = max(30, len(st.session_state.final_feedback) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height
            final_feedback = st.text_area(
                "Finalized feedback:",
                value=st.session_state.final_feedback,
                key="correct_feedback",
                height=estimated_height,
            )
            # Fetch stored feedback rating if it exists
            if "feedback_rating" in st.session_state:
                score = st.session_state.feedback_rating
            else:
                feedback_response = streamlit_feedback(
                    feedback_type="faces",
                    key="feedback_faces"
                )

                if feedback_response:
                    st.session_state.feedback_rating = feedback_response['score']
                    score = feedback_response['score']
                else:
                    score = None  # Default to None if no response yet

            if score:
                st.session_state.feedback_data["feedback_rating"] = score  # Store in feedback data
                st.session_state.feedback_data["feedback_rating_score"] = emoji_to_score(score)  # Store numeric rating

                if score != "😀":
                    # Button Click Handling
                    if st.button("Submit Corrected Feedback"):
                        if final_feedback.strip():
                            # Persist final feedback
                            st.session_state.feedback_data["final_feedback"] = final_feedback
                            st.session_state.final_feedback = final_feedback

                            # Store step change in session state
                            st.session_state.current_step = 2
                            st.session_state.feedback_submitted = True  # Flag to track submission
                        else:
                            st.warning("Please provide an non-empty feedback before submitting.")
                        st.rerun()
                else:
                    # If rating is happy, then directly use the GPT feedback as final feedback
                    st.session_state.feedback_data["final_feedback"] = st.session_state.feedback_data["gpt_feedback"]
                    st.session_state.current_step = 2
                    st.session_state.feedback_submitted = True  # Flag to track submission

            if st.session_state.get("feedback_submitted", False):
                st.session_state.current_step = 2  # Ensure next step persists
                st.rerun()

        # Step 2: Generate caption (intermediate step)
        elif st.session_state.current_step == 2:
            ### TODO: Comment out the below code to restore the caption refinement prompt engineering step
            st.session_state.current_step = 3
            st.rerun()
            # st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
            # st.write(st.session_state.feedback_data["pre_caption"])
            # st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
            # st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
            # st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")
            # st.write("You can optionally change the LLM or the prompt that we used to polish the caption. Please keep {feedback} and {pre_caption} in the prompt.")
            # # Get the final feedback (either corrected or GPT's version)
            # final_feedback = st.session_state.feedback_data["final_feedback"]
            # pre_caption = st.session_state.feedback_data["pre_caption"]
            # # Get improved caption
            # llm_names = get_all_llms()
            # # Dropdown to select a config, updating session state
            # selected_caption_llm = st.selectbox(
            #     "Select a Model:",
            #     llm_names,
            #     key="selected_caption_llm",
            #     index=llm_names.index("gpt-4o-2024-08-06"),
            # )
            # if "cur_caption_prompt" in st.session_state:
            #     caption_prompt = st.session_state.cur_caption_prompt
            # else:
            #     caption_prompt = load_txt(FOLDER / args.caption_prompt)

            # caption_prompt = st.text_area(
            #     "Prompt for polishing caption:",
            #     value=caption_prompt,
            #     key="cur_caption_prompt",
            #     height=PROMPT_HEIGHT,
            # )
            # if st.button("Submit") and caption_prompt:
            #     st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
            #     st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
            #     # Get GPT-4 polished feedback
            #     new_caption = get_llm(
            #         model=selected_caption_llm,
            #         secrets=st.secrets,
            #     ).generate(
            #         caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
            #     )
            #     st.session_state.feedback_data["gpt_caption"] = new_caption
            #     st.session_state.current_step = 3
            #     st.rerun()

        # Step 3: Rate GPT's caption and optionally provide corrected caption (optionally to re-generate the caption)
        elif st.session_state.current_step == 3:

            # Get the final feedback (either corrected or GPT's version)
            final_feedback = st.session_state.feedback_data["final_feedback"]
            pre_caption = st.session_state.feedback_data["pre_caption"]
            selected_caption_llm = "gpt-4o-2024-08-06"
            if "cur_caption_prompt" in st.session_state:
                caption_prompt = st.session_state.cur_caption_prompt
            else:
                caption_prompt = load_txt(FOLDER / args.caption_prompt)

            st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
            st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
            # Get GPT-4 polished feedback
            new_caption = get_llm(
                model=selected_caption_llm,
                secrets=st.secrets,
            ).generate(
                caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
            )
            st.session_state.feedback_data["gpt_caption"] = new_caption
            ## Done automatically to polish the caption first

            st.write(f"##### Final caption generated by {st.session_state.feedback_data['gpt_caption_llm']}")
            # Get the final feedback (either corrected or GPT's version)
            gpt_caption = st.session_state.feedback_data["gpt_caption"]
            st.write(gpt_caption)

            st.subheader("Rate AI-Improved Caption")

            st.write("Please modify the caption below (if not a perfect score of 5):")

            # Ensure final_caption is stored persistently
            if "final_caption" not in st.session_state:
                st.session_state.final_caption = gpt_caption

            line_height = 12  # Approximate height per line in pixels
            num_lines = max(30, len(st.session_state.final_caption) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height
            final_caption = st.text_area(
                "Final caption:",
                value=st.session_state.final_caption,
                key="correct_caption",
                height=estimated_height,
            )

            # Retrieve stored caption rating if it exists
            if "caption_rating" in st.session_state:
                score = st.session_state.caption_rating
            else:
                caption_response = streamlit_feedback(
                    feedback_type="faces",
                    key="caption_faces"
                )

                if caption_response:
                    st.session_state.caption_rating = caption_response['score']
                    score = caption_response['score']
                else:
                    score = None  # Default to None if no response yet

            if score:
                st.session_state.feedback_data["caption_rating"] = score  # Persist rating
                st.session_state.feedback_data["caption_rating_score"] = emoji_to_score(score)  # Store numeric rating

                if score != "😀":
                    # Button Click Handling
                    if st.button("Submit Final Caption"):
                        if final_caption.strip():
                            # Persist final caption
                            st.session_state.feedback_data["final_caption"] = final_caption
                            st.session_state.final_caption = final_caption

                            # Save feedback data
                            save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                            st.success(f"Caption saved successfully!")
                            st.json(st.session_state.feedback_data)
                            st.session_state.caption_submitted = True
                            st.session_state.current_step = 4
                        else:
                            st.warning("Please provide an non-empty feedback before submitting.")
                        st.rerun()
                else:
                    # If rating is happy, finalize caption and save
                    st.session_state.feedback_data["final_caption"] = st.session_state.feedback_data["gpt_caption"]
                    save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                    st.success(f"Caption saved successfully!")
                    st.json(st.session_state.feedback_data)
                    st.session_state.caption_submitted = True
                    st.session_state.current_step = 4
            else:
                st.subheader("(Optional) Re-try a New AI-Improved Caption")
                st.write("If you are not happy with the current AI-improved caption, you can re-try by modifying the LLM or the prompt below.")
                st.write("Note: please keep {feedback} and {pre_caption} in the prompt.")
                # Get improved caption
                llm_names = get_all_llms()
                # Dropdown to select a config, updating session state
                selected_caption_llm = st.selectbox(
                    "Select a Model:",
                    llm_names,
                    key="selected_caption_llm",
                    index=llm_names.index("gpt-4o-2024-08-06"),
                )
                if "cur_caption_prompt" in st.session_state:
                    caption_prompt = st.session_state.cur_caption_prompt
                else:
                    caption_prompt = load_txt(FOLDER / args.caption_prompt)

                caption_prompt = st.text_area(
                    "Prompt for polishing caption:",
                    value=caption_prompt,
                    key="cur_caption_prompt",
                    height=PROMPT_HEIGHT,
                )
                if st.button("Re-generate Final Caption") and caption_prompt:
                    st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
                    st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
                    # Get GPT-4 polished feedback
                    new_caption = get_llm(
                        model=selected_caption_llm,
                        secrets=st.secrets,
                    ).generate(
                        caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
                    )
                    st.session_state.feedback_data["gpt_caption"] = new_caption
                    # st.session_state.current_step = 3
                    st.rerun()
                st.write("Below are the original pre-caption and the final feedback for reference.")
                st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
                st.write(st.session_state.feedback_data["pre_caption"])
                st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
                st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
                st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")
            if st.session_state.get("caption_submitted", False):
                st.session_state.current_step = 4  # Ensure next step persists
                st.rerun()

        # Step 4: Print the final caption, and say if want to redo, please go to another video then come back
        elif st.session_state.current_step == 4:
            # st.write(f"##### Final Caption")
            st.write(st.session_state.feedback_data["final_caption"])
            st.success("Feedback and caption saved successfully! To redo, please go to another video then come back.")
            st.json(st.session_state.feedback_data)


if __name__ == "__main__":
    # Load configuration
    args = parse_args()
    main(args, caption_programs)
