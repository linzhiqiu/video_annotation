import streamlit as st
import difflib
import os
import re
from feedback_app import (
    load_video_data, get_video_id, load_json, 
    get_filename, load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    load_config, extract_frames, file_check, config_names_to_short_names, ANNOTATORS,
    convert_name_to_username, display_feedback_info,
    display_feedback_differences, display_caption_differences
)
from datetime import datetime
import argparse
from streamlit_extras.bottom_container import bottom

def parse_args():
    """Parse command line arguments for the new annotator diff app"""
    parser = argparse.ArgumentParser(description="New Annotator Comparison Viewer")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=[
            "video_urls/new_annotator_exam/exam.json",
        ],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--main_project_output", type=str, default="output_captions", help="Path to the main project output directory")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the original output directory")
    parser.add_argument("--output_new_annotator", type=str, default="output_new_annotator", help="Path to the new annotator output directory")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--personalize_output", action="store_true", default=True, help="Whether to personalize the output directory based on the logged-in user")
    parser.add_argument("--diff_prompt", type=str, default="prompts/diff_prompt.txt", help="Path to the diff prompt file")
    parser.add_argument("--diff_cap_prompt", type=str, default="prompts/diff_cap_prompt.txt", help="Path to the caption diff prompt file")
    return parser.parse_args()

def get_video_status(video_id, output_dir, new_annotator_output_dir):
    """Get the status of a video's caption completion and compare with new annotator version"""
    current_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    new_annotator_file = get_filename(video_id, new_annotator_output_dir, FEEDBACK_FILE_POSTFIX)
    
    if not os.path.exists(current_file):
        # print(f"Current file does not exist: {current_file}")
        return "not_done", None, None, None, None
    elif not os.path.exists(new_annotator_file):
        # print(f"New annotator file does not exist: {new_annotator_file}")
        return "not_done_by_new_annotator", current_file, None, None, None
    else:
        # Load both current and new annotator data to check users
        current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        new_annotator_data = load_data(video_id, output_dir=new_annotator_output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        
        current_user = current_data.get("user", "Unknown")
        new_annotator_user = new_annotator_data.get("user", "Unknown")
        
        return "done_by_new_annotator", current_file, new_annotator_file, current_user, new_annotator_user

def get_video_format_func(output_dir, new_annotator_output_dir, video_urls=None):
    """Format function for video selection dropdown with status emojis"""
    def format_func(video_url):
        if video_urls is not None:
            video_index = video_urls.index(video_url)
        else:
            video_index = ""
        
        video_id = get_video_id(video_url)
        status, _, _, _, _ = get_video_status(video_id, output_dir, new_annotator_output_dir)
        
        emoji_map = {
            "not_done": "❓",  # for not completed
            "not_done_by_new_annotator": "⏳",  # hourglass for completed but not by new annotator
            "done_by_new_annotator": "✅"  # for done by new annotator
        }
        
        emoji = emoji_map[status]
        return f"{emoji}{video_index}. {video_url.split('/')[-1]}"
    
    return format_func

def login_page(args):
    st.title("Onboarding Results Viewer Login")

    # Create a form for login
    with st.form("login_form"):
        # Annotator selection dropdown
        selected_annotator = st.selectbox(
            "Select Annotator Name:",
            list(ANNOTATORS.keys()),
            key="selected_annotator",
            index=None,
            placeholder="Type or select the annotator name...",
        )
        
        # Password input
        password = st.text_input("Enter Password:", type="password", key="password_input")
        
        # File selection dropdown
        selected_file = st.selectbox(
            "Select Video URLs File:", args.video_urls_files, key="selected_urls_file"
        )

        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Check if password matches
            if password == ANNOTATORS[selected_annotator]["password"]:
                # Load video URLs and store in session state
                video_urls = load_json(FOLDER / selected_file)
                st.session_state.video_urls = video_urls
                st.session_state.logged_in = True
                st.session_state.logged_in_user = selected_annotator
                st.success(f"Login successful! Welcome, {selected_annotator}!")
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

def format_timestamp(iso_timestamp):
    """Format ISO timestamp to a more readable format (YYYY-MM-DD HH:MM)"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return iso_timestamp  # Return original if parsing fails

def main(args):
    # Set page config first
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # Check login status
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page(args)
        return
    
    # After successful login, update the new annotator output directory based on the logged-in user if personalize_output is True
    if args.personalize_output and "logged_in_user" in st.session_state:
        # Only set the personalized output directory once in session state
        if "personalized_output" not in st.session_state:
            username = convert_name_to_username(st.session_state.logged_in_user)
            st.session_state.personalized_output = f"{args.output_new_annotator}_{username}"
        
        # Use the stored personalized output directory for new annotator
        args.output_new_annotator = st.session_state.personalized_output
        st.sidebar.write(f"**New Annotator Output Directory:** {args.output_new_annotator}")

    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    if "file_check_passed" not in st.session_state:
        file_check(st.session_state.video_urls, video_data_dict)
        st.session_state.file_check_passed = True

    # Create two columns
    page_col1, page_col2 = st.columns([1, 1])  # Left column is smaller, right column is wider

    # Add logout button
    st.sidebar.title("User Options")
    st.sidebar.write(f"Logged in as: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Logout"):
        # Clear session state and logout
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Debug information
    # st.sidebar.header("Debug Information")
    # st.sidebar.write("Full Session State:")
    # for key, value in st.session_state.items():
        # st.sidebar.write(f"{key}: {value}")
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
                if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 'video_urls', 'last_video_id', 'last_selected_video', 'logged_in_user', 'personalized_output']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_config_id = selected_config
            print(f"Config changed to: {selected_config}")
            st.rerun()  # Force a rerun to ensure clean state

        config = config_dict[selected_config]
        st.title(f"New Annotator Comparison Viewer - {config.get('name', '')}")
        video_urls = st.session_state.video_urls
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        new_annotator_output_dir = os.path.join(FOLDER, args.output_new_annotator, config["output_name"])
        
        # Select video
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=get_video_format_func(output_dir, new_annotator_output_dir, video_urls=video_urls),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video"
        )
        video_id = get_video_id(selected_video)

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
                if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 'personalized_output']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video

            st.rerun()  # Force a rerun to ensure clean state

        # Display video
        st.video(selected_video)

        # Display first and last frames
        extracted_frames = extract_frames(selected_video, [0, -1])
        # Expandable section
        with st.expander("Frames (Click to Expand/Collapse)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.image(extracted_frames[0], caption="First Frame")
            with col2:
                st.image(extracted_frames[1], caption="Last Frame")
        
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
            
            st.link_button("🔗 Report Label Errors Here", "https://docs.google.com/spreadsheets/d/1sAYL86ERcaC_vrVuloXxtPJXKzeuj8fukHtNv6nRCJ0/edit?usp=sharing")

        # Get indices
        current_index = video_urls.index(selected_video)
        current_task_index = config_names.index(selected_config)

        # Keys to keep
        preserved_keys = [
            'api_key', 'last_config_id', 'selected_config',
            'last_video_id', 'last_selected_video', 
            'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 'personalized_output'
        ]

        def reset_state_except(preserved):
            keys_to_remove = [key for key in st.session_state if key not in preserved]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()

        # Create a single horizontal row with 4 nav buttons
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            if current_index > 0:
                if st.button("Prev Video ⏪"):
                    st.session_state.last_selected_video = video_urls[current_index - 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index - 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Prev Video ⏪", disabled=True)

        with col2:
            if current_task_index > 0:
                prev_task_short_name = config_names_to_short_names[config_names[current_task_index - 1]]
                if st.button(f"{prev_task_short_name} Task ⬅️"):
                    st.session_state.last_config_id = config_names[current_task_index - 1]
                    reset_state_except(preserved_keys)
            else:
                st.button("No Prev Task ⬅️", disabled=True)
        
        with col3:
            task_short_name = config_names_to_short_names[selected_config]
            st.button(f"{task_short_name} Task 📍", disabled=True)

        with col4:
            if current_task_index < len(config_names) - 1:
                next_task_short_name = config_names_to_short_names[config_names[current_task_index + 1]]
                if st.button(f"{next_task_short_name} Task ➡️"):
                    st.session_state.last_config_id = config_names[current_task_index + 1]
                    reset_state_except(preserved_keys)
            else:
                st.button("No Next Task ➡️ ", disabled=True)

        with col5:
            if current_index < len(video_urls) - 1:
                if st.button("Next Video ⏩"):
                    st.session_state.last_selected_video = video_urls[current_index + 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index + 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Next Video ⏭️", disabled=True)
        
    with page_col2:
        with st.container(height=930, border=True):
            status, current_file, new_annotator_file, current_user, new_annotator_user = get_video_status(video_id, output_dir, new_annotator_output_dir)
            
            if status == "not_done":
                st.warning("Please complete this caption first.")
            elif status == "not_done_by_new_annotator":
                st.info("No new annotator version found.")
            else:  # done_by_new_annotator
                # Load both current and new annotator captions
                current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                new_annotator_data = load_data(video_id, output_dir=new_annotator_output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                
                st.subheader("Caption Comparison")
                
                # Display metadata information
                current_timestamp = format_timestamp(current_data.get("timestamp", "Unknown"))
                new_annotator_timestamp = format_timestamp(new_annotator_data.get("timestamp", "Unknown"))
                
                st.write(f"**Ground Truth Version:** By {current_user} on {current_timestamp}")
                st.write(f"**Your Version:** By {new_annotator_user} on {new_annotator_timestamp}")
                
                # Create tabs for viewing captions
                tab1, tab2, tab3, tab4 = st.tabs(["Feedback Differences", "Caption Differences", "Ground Truth Version", "Your Version"])
                
                with tab1:
                    st.subheader("Feedback Differences")
                    display_feedback_differences(
                        prev_feedback=new_annotator_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_prompt
                    )
                
                with tab2:
                    st.subheader("Caption Differences")
                    display_caption_differences(
                        prev_feedback=new_annotator_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_cap_prompt
                    )
                
                
                with tab3:
                    st.subheader("Ground Truth Version")
                    st.write(f"**User:** {current_user}")
                    st.write(f"**Timestamp:** {format_timestamp(current_data.get('timestamp', ''))}")
                    display_feedback_info(current_data, display_pre_caption_instead_of_final_caption=False)
                
                with tab4:
                    st.subheader("Your Version")
                    st.write(f"**User:** {new_annotator_user}")
                    st.write(f"**Timestamp:** {format_timestamp(new_annotator_data.get('timestamp', ''))}")
                    display_feedback_info(new_annotator_data, display_pre_caption_instead_of_final_caption=True)
                

if __name__ == "__main__":
    args = parse_args()
    main(args) 