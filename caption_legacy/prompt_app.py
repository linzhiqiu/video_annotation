import streamlit as st
import argparse
from streamlit_feedback import streamlit_feedback
import os
import torch
import json
from datetime import datetime
from pathlib import Path
from utils import extract_frames, load_config, load_json
from llm import get_llm, get_all_llms, get_supported_mode
from caption_policy.prompt_generator import SubjectPolicy, ScenePolicy, SubjectMotionPolicy, SpatialPolicy, CameraPolicy
from process_json import json_to_video_data

caption_programs = {
    "subject_description": SubjectPolicy(),
    "scene_composition_dynamics": ScenePolicy(),
    "subject_motion_dynamics": SubjectMotionPolicy(),
    "spatial_framing_dynamics": SpatialPolicy(),
    "camera_framing_dynamics": CameraPolicy()
}

# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="test_configs.json", help="Path to the JSON config file")
    parser.add_argument("--video_urls_file", type=str, default="test_urls_2.json", help="Path to the test URLs file")
    parser.add_argument("--output", type=str, default="output_prompts", help="Path to the output directory")
    parser.add_argument("--video_data", type=str, default="video_data/20250218_1042/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    return parser.parse_args()

def load_video_data(video_data_file, label_collections=["cam_motion", "cam_setup"]):
    video_data_dict = json_to_video_data(video_data_file, label_collections)
    for video_data in video_data_dict.values():
        video_data.cam_setup.update()
        video_data.cam_motion.update()
        video_data.cam_setup.subject_description = "**{NO DESCRIPTION FOR SUBJECTS YET}**"
        video_data.cam_setup.scene_description = "**{NO DESCRIPTION FOR SCENE YET}**"
        video_data.cam_setup.motion_description = "**{NO DESCRIPTION FOR SUBJECT MOTION YET}**"
        video_data.cam_setup.spatial_description = "**{NO DESCRIPTION FOR SPATIAL FRAMING YET}**"
        video_data.cam_setup.camera_description = "**{NO DESCRIPTION FOR CAMERA FRAMING YET}**"
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

def save_feedback_data(video_id, data, output_dir="outputs"):
    """Save feedback data to a JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f'{video_id}.json')
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

def exist_feedback_data(video_id, output_dir="outputs"):
    """Check if feedback data already exists"""
    filename = os.path.join(output_dir, f'{video_id}.json')
    return os.path.exists(filename)

def load_feedback_data(video_id, output_dir="outputs"):
    """Load existing feedback data for a video if it exists"""
    filename = os.path.join(output_dir, f'{video_id}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


# Get video ID from URL
def get_video_id(url):
    return url.split('/')[-1]

# Load instructions from file
def load_instructions(instruction_file):
    with open(instruction_file, "r") as f:
        return f.read()

# Load prompt template
def load_prompt(filename, **kwargs):
    with open(filename, "r") as f:
        prompt = f.read()
    return prompt.format(**kwargs)


def get_video_format_func(output_dir):
    def video_format_func(video_url):
        # if already exists, then return f"✅ {video_url}"
        video_id = get_video_id(video_url)
        # Check for existing feedback and get current caption
        existing_feedback = load_feedback_data(video_id, output_dir=FOLDER / output_dir)
        
        # Show existing feedback if available
        if existing_feedback:
            return f"✅ {video_url}"
        return f"{video_url}"
    return video_format_func

def get_imagery_kwargs(selected_mode, selected_video):
    if selected_mode == "Text Only":
        return {}
    
    imagery_kwargs = {"video": selected_video}
    if selected_mode == "Image (First-and-Last-Frame)":
        imagery_kwargs.update({"extracted_frames": [0, -1]})
    elif selected_mode == "Video":
        pass
    return imagery_kwargs

def main():
    # Load configuration
    args = parse_args()
    
    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    
    
    # Hide sidebar by default
    st.set_page_config(initial_sidebar_state="collapsed")
    
    
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
    
    config_dict = {config["name"]: config for config in configs}
    config_names = list(config_dict.keys())
    # Dropdown to select a config, updating session state
    selected_config = st.selectbox(
        "Select a task:",
        config_names, 
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
            if key not in ['api_key', 'last_config_id']:
                keys_to_remove.append(key)
        
        # Remove all collected keys
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Set the new video id
        st.session_state.last_config_id = selected_config
        
        st.rerun()  # Force a rerun to ensure clean state


    config = config_dict[selected_config]
    st.title(config.get("name", "Pre-Caption System"))
    video_urls = load_json(FOLDER / args.video_urls_file)
    output_dir = os.path.join(FOLDER, args.output, config["output_name"])
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except:
            import pdb; pdb.set_trace()
    
    
    # Select video
    selected_video = st.selectbox("Select a video:", video_urls, format_func=get_video_format_func(output_dir), index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])))
    # selected_video = st.selectbox("Select a video:", video_urls, format_func=get_video_format_func(output_dir))
    # print(f"Selected video: {selected_video}")
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
            if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id']:
                keys_to_remove.append(key)
        
        # Remove all collected keys
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Set the new video id
        st.session_state.last_video_id = video_id
        st.session_state.last_selected_video = selected_video
        # print(f"Resetting state for new video: {video_id}")
        
        # Also clear any feedback component states
        if 'feedback_submitted_initial_caption_faces' in st.session_state:
            del st.session_state['feedback_submitted_initial_caption_faces']
        
        st.rerun()  # Force a rerun to ensure clean state
    
    # Session state initialization
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = {}

    # Display instructions
    st.subheader("Instructions")
    with st.expander("📜 Instructions (Click to Expand/Collapse)", expanded=False):
        # Load instructions from file, otherwise throw a warning
        if "instruction_file" not in config:
            st.warning("No instruction_file found in the configuration file.")
        else:
            st.write(load_instructions(FOLDER / config["instruction_file"]))

    
    # Display video
    st.video(selected_video)
    
    # Display first and last frames
    extracted_frames = extract_frames(selected_video, [0, -1])
    # Expandable section
    with st.expander("Frames (Click to Expand/Collapse)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.image(extracted_frames[0], caption="First Frame")
        with col2:
            st.image(extracted_frames[1], caption="Last Frame")

    
    st.write("##### 目前仅支持Gemini-2和ChatGPT. 可以选用（text-only) (first-last-frame) (video)的模式")
    st.write("Please polish the prompt and select an option to generate a caption:")
    llm_names = get_all_llms()
    # Dropdown to select a config, updating session state
    selected_llm = st.selectbox(
        "Select a Model:",
        llm_names, 
    )
    supported_modes = get_supported_mode(selected_llm)
    selected_mode = st.selectbox(
        "Select a Mode:",
        supported_modes, 
    )
    new_option = f"{selected_llm} ({selected_mode})"
    
    line_height = 20  # Approximate height per line in pixels
    num_lines = max(10, len(current_prompt) // 80)  # Assuming ~80 characters per line
    estimated_height = num_lines * line_height
    
    new_prompt = st.text_area(
        "Your Own Polished Prompt:",
        value=current_prompt,
        key="correct_feedback",
        height=estimated_height,
    )
    
    if st.button("Generate a Caption"):
        imagery_kwargs = get_imagery_kwargs(selected_mode, selected_video)
        st.write("Be patient, this may take a while...")
        
        new_caption = get_llm(
            model=selected_llm,
            secrets=st.secrets,
        ).generate(
            new_prompt,
            **imagery_kwargs
        )
        # Initialize feedback data
        st.session_state.feedback_data = {
            "video_id": video_id,
            "final_caption": new_caption,
            "final_prompt": new_prompt,
            "final_option": new_option
        }
        filename = save_feedback_data(video_id, st.session_state.feedback_data, output_dir=FOLDER / output_dir)
        st.rerun()  # Force a rerun to ensure clean state
    
    # Check for existing feedback and get current caption
    existing_feedback = load_feedback_data(video_id, output_dir=FOLDER / output_dir)
    
    # Show existing feedback if available
    if existing_feedback:
        st.success("Finished generating caption!")
        # st.json(st.session_state.feedback_data)
        st.write(f"**Option**: {existing_feedback['final_option']}")
        st.write(f"**Generated Caption**: {existing_feedback['final_caption']}")
        
        st.info("Previous prompt was recorded.")
        # st.subheader("Most Recent Prompt/Option/Caption")
        current_prompt = existing_feedback["final_prompt"]
        # current_caption = existing_feedback["final_caption"]
        # current_option = existing_feedback["final_option"]
        
        st.write(f"**Prompt**:")
        st.write(current_prompt.replace('\n', '\n\n'))
        
        # st.write(f"\n**Option**: {current_option}")
        # st.write(f"**Caption**: {current_caption}")


if __name__ == "__main__":
    main()