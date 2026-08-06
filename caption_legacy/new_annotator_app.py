# caption/new_annotator_app.py
import argparse
import streamlit as st
import os
from datetime import datetime

# Import everything from feedback_app for reuse
from feedback_app import (
    main as feedback_main, caption_programs, load_video_data, get_video_id, load_json, 
    get_filename, load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX,
    load_config, extract_frames, file_check, config_names_to_short_names, ANNOTATORS,
    convert_name_to_username, display_feedback_info, copy_feedback_for_precaption,
    display_feedback_differences, display_caption_differences
)

def parse_args():
    """Parse command line arguments for the unified new annotator app"""
    parser = argparse.ArgumentParser(description="Unified New Annotator System")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=["video_urls/new_annotator_exam/exam.json"],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--main_project_output", type=str, default="output_captions", help="Path to the main project output directory")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the original/ground truth output directory")
    parser.add_argument("--output_new_annotator", type=str, default="output_onboarding/output_new_annotator", help="Path to the new annotator output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--show_feedback_prompt", type=bool, default=False, help="Whether to show and allow the annotator to edit the feedback prompt")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    parser.add_argument("--diff_prompt", type=str, default="prompts/diff_prompt.txt", help="Path to the diff prompt file")
    parser.add_argument("--diff_cap_prompt", type=str, default="prompts/diff_cap_prompt.txt", help="Path to the caption diff prompt file")
    parser.add_argument("--video_data", type=str, default="video_data/20250406_setup_and_motion/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--personalize_output", type=bool, default=True, help="Whether to personalize the output directory based on the logged-in user")
    return parser.parse_args()

def unified_login_page(args):
    """Unified login page for new annotator system"""
    st.title("🎓 New Annotator Training System")
    st.markdown("### Welcome to the New Annotator Onboarding System")
    
    # Create a form for login
    with st.form("new_annotator_login_form"):
        st.markdown("#### Login to access the training system")
        
        # Annotator selection dropdown
        selected_annotator = st.selectbox(
            "Select Your Name:",
            list(ANNOTATORS.keys()),
            key="selected_annotator",
            index=None,
            placeholder="Type or select your name...",
        )
        
        # Password input
        password = st.text_input("Enter Password:", type="password", key="password_input")
        
        # File selection dropdown
        selected_file = st.selectbox(
            "Select Training Video Set:", 
            args.video_urls_files, 
            key="selected_urls_file",
            format_func=lambda x: f"📋 {os.path.basename(x)}"
        )

        submit_button = st.form_submit_button("🚀 Login", use_container_width=True)

        if submit_button:
            if selected_annotator and password == ANNOTATORS[selected_annotator]["password"]:
                # Load video URLs and store in session state
                video_urls = load_json(FOLDER / selected_file)
                st.session_state.video_urls = video_urls
                st.session_state.logged_in = True
                st.session_state.logged_in_user = selected_annotator
                st.session_state.selected_portal_file = selected_file
                # IMPORTANT: Set portal mode flag so feedback_app knows it's running in portal mode
                st.session_state.selected_portal = True
                st.success(f"Login successful! Welcome to training, {selected_annotator}!")
                st.rerun()
            else:
                st.error("Incorrect password or missing name. Please try again.")

def mode_selection_page():
    """Mode selection page after login"""
    st.title("🎯 Select Training Mode")
    st.markdown(f"### Welcome, **{st.session_state.logged_in_user}**!")
    st.markdown("Choose your training activity:")
    
    st.markdown("---")
    
    # Create two columns for mode selection
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📝 Caption Creation Mode")
        st.markdown("""
        **Practice Creating Captions**
        - Generate AI-powered pre-captions
        - Provide feedback to refine captions
        - Submit final captions for review
        
        *Use this mode to practice and create your caption submissions.*
        """)
        if st.button("🚀 Start Caption Training", key="caption_mode", use_container_width=True):
            st.session_state.selected_portal_mode = "caption"
            # Clear any mode-specific state
            clear_mode_state()
            st.rerun()
    
    with col2:
        st.markdown("### 🔍 Comparison Mode")
        st.markdown("""
        **Compare Your Work with Ground Truth**
        - View differences between your captions and ground truth versions
        - Compare feedback and ratings
        - Learn from ground truth annotations
        
        *Use this mode to review and learn from your submissions.*
        """)
        if st.button("🔍 Compare with Ground Truth", key="comparison_mode", use_container_width=True):
            st.session_state.selected_portal_mode = "comparison"
            # Clear any mode-specific state
            clear_mode_state()
            st.rerun()
    
    st.markdown("---")
    
    # Logout option
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def clear_mode_state():
    """Clear mode-specific state while preserving login and navigation state"""
    # Keys to preserve across mode switches
    preserve_keys = {
        'logged_in', 'logged_in_user', 'video_urls', 'selected_portal_file',
        'selected_portal_mode', 'file_check_passed', 'personalized_output',
        'selected_portal', 'login_method', 'target_annotator'
    }
    
    # Clear all other keys
    keys_to_clear = [k for k in st.session_state.keys() if k not in preserve_keys]
    for key in keys_to_clear:
        del st.session_state[key]

def add_mode_navigation_sidebar(current_mode, args):
    """Add consistent mode navigation to sidebar"""
    with st.sidebar:
        if current_mode == "caption":
            st.title("📝 Caption Training")
        else:
            st.title("🔍 Comparison Mode")
            
        st.write(f"**User:** {st.session_state.logged_in_user}")
        
        if hasattr(args, 'output_new_annotator') and args.personalize_output:
            st.write(f"**Your Output:** {args.output_new_annotator}")
        
        st.markdown("---")
        
        # Mode switching
        if current_mode == "caption":
            if st.button("🔄 Switch to Comparison Mode"):
                st.session_state.selected_portal_mode = "comparison"
                clear_mode_state()
                st.rerun()
        else:
            if st.button("🔄 Switch to Caption Mode"):
                st.session_state.selected_portal_mode = "caption"
                clear_mode_state()
                st.rerun()
        
        if st.button("🏠 Back to Mode Selection"):
            if 'selected_portal_mode' in st.session_state:
                del st.session_state.selected_portal_mode
            clear_mode_state()
            st.rerun()
        
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def get_comparison_video_status(video_id, output_dir, new_annotator_output_dir):
    """Get the status of a video's caption completion and compare with new annotator version"""
    current_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    new_annotator_file = get_filename(video_id, new_annotator_output_dir, FEEDBACK_FILE_POSTFIX)
    
    if not os.path.exists(current_file):
        return "not_done", None, None, None, None
    elif not os.path.exists(new_annotator_file):
        return "not_done_by_new_annotator", current_file, None, None, None
    else:
        # Load both current and new annotator data to check users
        current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        new_annotator_data = load_data(video_id, output_dir=new_annotator_output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        
        current_user = current_data.get("user", "Unknown")
        new_annotator_user = new_annotator_data.get("user", "Unknown")
        
        return "done_by_new_annotator", current_file, new_annotator_file, current_user, new_annotator_user

def get_comparison_video_format_func(output_dir, new_annotator_output_dir, video_urls=None):
    """Format function for video selection dropdown with status emojis for comparison mode"""
    def format_func(video_url):
        if video_urls is not None:
            video_index = video_urls.index(video_url)
        else:
            video_index = ""
        
        video_id = get_video_id(video_url)
        status, _, _, _, _ = get_comparison_video_status(video_id, output_dir, new_annotator_output_dir)
        
        emoji_map = {
            "not_done": "❓",  # for not completed
            "not_done_by_new_annotator": "⏳",  # hourglass for completed but not by new annotator
            "done_by_new_annotator": "✅"  # for done by new annotator
        }
        
        emoji = emoji_map[status]
        return f"{emoji}{video_index}. {video_url.split('/')[-1]}"
    
    return format_func

def format_timestamp(iso_timestamp):
    """Format ISO timestamp to a more readable format (YYYY-MM-DD HH:MM)"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return iso_timestamp  # Return original if parsing fails

# def debug_session_state():
#     """Debug function to track session state changes"""
#     if "debug_mode" not in st.session_state:
#         st.session_state.debug_mode = True
        
    # Log current session state
    # print(f"=== DEBUG SESSION STATE ===")
    # print(f"Current time: {datetime.now()}")
    # print(f"selected_portal_mode exists: {'selected_portal_mode' in st.session_state}")
    # if 'selected_portal_mode' in st.session_state:
    #     print(f"selected_portal_mode value: {st.session_state.selected_portal_mode}")
    # print(f"logged_in: {st.session_state.get('logged_in', 'NOT SET')}")
    # print(f"selected_portal: {st.session_state.get('selected_portal', 'NOT SET')}")
    # print(f"All session state keys: {list(st.session_state.keys())}")
    # print("=" * 50)

def main():
    """Main application entry point"""
    # Set page config once at the top level
    st.set_page_config(
        page_title="New Annotator Training System",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # ADD THIS DEBUG CALL AT THE VERY START
    # debug_session_state()
    
    # Parse arguments
    args = parse_args()
    
    # Check login status
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # print("DEBUG: Not logged in, showing login page")
        unified_login_page(args)
        return
    
    # Update new annotator output directory if personalization is enabled
    if args.personalize_output and "logged_in_user" in st.session_state:
        if "personalized_output" not in st.session_state:
            username = convert_name_to_username(st.session_state.logged_in_user)
            st.session_state.personalized_output = f"{args.output_new_annotator}_{username}"
            print(f"Personalized output directory: {st.session_state.personalized_output}")
            # Copy feedback files from main project for precaption
            copy_feedback_for_precaption(
                args.configs,
                st.session_state.video_urls,  # Use video_urls directly
                args.main_project_output,  # Main project output
                st.session_state.personalized_output  # Personalized output
            )
        args.output_new_annotator = st.session_state.personalized_output
    
    # Check mode selection
    if "selected_portal_mode" not in st.session_state:
        # print("DEBUG: No mode selected, showing mode selection page")
        # print(f"DEBUG: Session state keys at this point: {list(st.session_state.keys())}")
        mode_selection_page()
        return
    
    # print(f"DEBUG: Mode selected: {st.session_state.selected_portal_mode}")
    
    # Route to appropriate mode
    if st.session_state.selected_portal_mode == "caption":
        # print("DEBUG: Entering caption mode")
        caption_mode_wrapper(args)
    elif st.session_state.selected_portal_mode == "comparison":
        # print("DEBUG: Entering comparison mode")
        comparison_mode_main(args)
    else:
        # print(f"DEBUG: Invalid mode selection: {st.session_state.selected_portal_mode}")
        if 'selected_portal_mode' in st.session_state:
            del st.session_state.selected_portal_mode
        st.rerun()

def caption_mode_wrapper(args):
    """Wrapper for caption creation mode - reuses feedback_app main function"""
    # print("DEBUG: Inside caption_mode_wrapper")
    # debug_session_state()
    
    # Add mode navigation
    add_mode_navigation_sidebar("caption", args)
    
    # Prepare args for caption creation (like new_annotator_test_app.py)
    caption_args = args  # Use the args as-is since they're already configured for new annotator
    
    # Ensure we're using the new annotator output directory
    caption_args.output = args.output_new_annotator
    
    # Store current session state before calling feedback_main
    pre_call_keys = set(st.session_state.keys())
    has_selected_portal_mode_before = 'selected_portal_mode' in st.session_state
    selected_portal_mode_value_before = st.session_state.get('selected_portal_mode', 'NOT SET')
    
    # print(f"DEBUG: Before calling feedback_main:")
    # print(f"  - selected_portal_mode exists: {has_selected_portal_mode_before}")
    # print(f"  - selected_portal_mode value: {selected_portal_mode_value_before}")
    # print(f"  - total session state keys: {len(pre_call_keys)}")
    
    # Disable page config since it's already set
    # original_set_page_config = st.set_page_config
    # st.set_page_config = lambda **kwargs: None
    
    try:
        # Call the original feedback_app main function
        feedback_main(caption_args, caption_programs)
    finally:
        # Restore original page config function
        # st.set_page_config = original_set_page_config
        
        # Check session state after the call
        post_call_keys = set(st.session_state.keys())
        has_selected_portal_mode_after = 'selected_portal_mode' in st.session_state
        selected_portal_mode_value_after = st.session_state.get('selected_portal_mode', 'NOT SET')
        
        # print(f"DEBUG: After calling feedback_main:")
        # print(f"  - selected_portal_mode exists: {has_selected_portal_mode_after}")
        # print(f"  - selected_portal_mode value: {selected_portal_mode_value_after}")
        # print(f"  - total session state keys: {len(post_call_keys)}")
        
        if has_selected_portal_mode_before and not has_selected_portal_mode_after:
            # print("DEBUG: *** SELECTED_PORTAL_MODE WAS DELETED BY feedback_main! ***")
            keys_deleted = pre_call_keys - post_call_keys
            keys_added = post_call_keys - pre_call_keys
            # print(f"DEBUG: Keys deleted: {keys_deleted}")
            # print(f"DEBUG: Keys added: {keys_added}")

def comparison_mode_main(args):
    """Main function for comparison mode - reuses logic from new_annotator_diff_app.py"""
    # Add mode navigation
    add_mode_navigation_sidebar("comparison", args)
    
    # After successful login, update the new annotator output directory based on the logged-in user
    if args.personalize_output and "logged_in_user" in st.session_state:
        if "personalized_output" not in st.session_state:
            username = convert_name_to_username(st.session_state.logged_in_user)
            st.session_state.personalized_output = f"{args.output_new_annotator}_{username}"
        args.output_new_annotator = st.session_state.personalized_output

    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    if "file_check_passed_comparison" not in st.session_state:
        file_check(st.session_state.video_urls, video_data_dict)
        st.session_state.file_check_passed_comparison = True

    # Create two columns
    page_col1, page_col2 = st.columns([1, 1])

    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        st.error(f"Config file not found: {args.configs}")
        return

    with page_col1:
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        
        # Task selection
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id_comparison', config_names[0])),
            key="selected_task_comparison",
        )

        # Handle config changes
        if 'last_config_id_comparison' not in st.session_state:
            st.session_state.last_config_id_comparison = selected_config
        elif st.session_state.last_config_id_comparison != selected_config:
            keys_to_remove = [key for key in st.session_state 
                             if key not in ['api_key', 'last_config_id_comparison', 'file_check_passed_comparison', 'logged_in', 
                                          'video_urls', 'last_video_id_comparison', 'last_selected_video_comparison', 'logged_in_user', 
                                          'selected_portal_mode', 'selected_portal_file', 'personalized_output',
                                          'selected_portal', 'login_method', 'target_annotator']]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_config_id_comparison = selected_config
            st.rerun()

        config = config_dict[selected_config]
        st.title(f"Caption Comparison - {config.get('name', '')}")
        
        video_urls = st.session_state.video_urls
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        new_annotator_output_dir = os.path.join(FOLDER, args.output_new_annotator, config["output_name"])
        
        # Video selection
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=get_comparison_video_format_func(output_dir, new_annotator_output_dir, video_urls=video_urls),
            index=video_urls.index(st.session_state.get('last_selected_video_comparison', video_urls[0])),
            key="selected_video_comparison"
        )
        
        video_id = get_video_id(selected_video)

        # Handle video changes
        if 'last_video_id_comparison' not in st.session_state:
            st.session_state.last_video_id_comparison = video_id
            st.session_state.last_selected_video_comparison = selected_video
        elif st.session_state.last_video_id_comparison != video_id:
            keys_to_remove = [key for key in st.session_state 
                             if key not in ['api_key', 'last_config_id_comparison', 'selected_config_comparison', 'last_video_id_comparison', 
                                          'last_selected_video_comparison', 'file_check_passed_comparison', 'logged_in', 'video_urls', 
                                          'logged_in_user', 'selected_portal_mode', 'selected_portal_file', 'personalized_output',
                                          'selected_portal', 'login_method', 'target_annotator']]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_video_id_comparison = video_id
            st.session_state.last_selected_video_comparison = selected_video
            st.rerun()

        # Display video
        st.video(selected_video)

        # Display frames
        extracted_frames = extract_frames(selected_video, [0, -1])
        with st.expander("Frames", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.image(extracted_frames[0], caption="First Frame")
            with col2:
                st.image(extracted_frames[1], caption="Last Frame")

        # Navigation buttons
        current_index = video_urls.index(selected_video)
        current_task_index = config_names.index(selected_config)

        # Keys to keep
        preserved_keys = [
            'api_key', 'last_config_id_comparison', 'selected_config_comparison',
            'last_video_id_comparison', 'last_selected_video_comparison', 
            'file_check_passed_comparison', 'logged_in', 'video_urls', 'logged_in_user', 
            'selected_portal_mode', 'selected_portal_file', 'personalized_output',
            'selected_portal', 'login_method', 'target_annotator'
        ]

        def reset_state_except(preserved):
            keys_to_remove = [key for key in st.session_state if key not in preserved]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()

        # Navigation buttons
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            if current_index > 0:
                if st.button("Prev Video ⏪"):
                    st.session_state.last_selected_video_comparison = video_urls[current_index - 1]
                    st.session_state.last_video_id_comparison = get_video_id(video_urls[current_index - 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Prev Video ⏪", disabled=True)

        with col2:
            if current_task_index > 0:
                prev_task_short_name = config_names_to_short_names[config_names[current_task_index - 1]]
                if st.button(f"{prev_task_short_name} Task ⬅️"):
                    st.session_state.last_config_id_comparison = config_names[current_task_index - 1]
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
                    st.session_state.last_config_id_comparison = config_names[current_task_index + 1]
                    reset_state_except(preserved_keys)
            else:
                st.button("No Next Task ➡️", disabled=True)

        with col5:
            if current_index < len(video_urls) - 1:
                if st.button("Next Video ⏩"):
                    st.session_state.last_selected_video_comparison = video_urls[current_index + 1]
                    st.session_state.last_video_id_comparison = get_video_id(video_urls[current_index + 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Next Video ⏭️", disabled=True)
        
    with page_col2:
        with st.container(height=930, border=True):
            status, current_file, new_annotator_file, current_user, new_annotator_user = get_comparison_video_status(
                video_id, output_dir, new_annotator_output_dir
            )
            
            if status == "not_done":
                st.warning("⚠️ No ground truth available for this video.")
            elif status == "not_done_by_new_annotator":
                st.info("📝 You haven't created a caption for this video yet. Switch to Caption Mode to create one!")
            else:  # done_by_new_annotator
                # Load both current and new annotator captions
                current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                new_annotator_data = load_data(video_id, output_dir=new_annotator_output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                
                st.subheader("📊 Caption Comparison Results")
                
                # Display metadata information
                current_timestamp = format_timestamp(current_data.get("timestamp", "Unknown"))
                new_annotator_timestamp = format_timestamp(new_annotator_data.get("timestamp", "Unknown"))
                
                # Create info boxes
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**📚 Ground Truth**\nBy {current_user}\n{current_timestamp}")
                with col2:
                    st.success(f"**👤 Your Version**\nBy {new_annotator_user}\n{new_annotator_timestamp}")
                
                # Create tabs for viewing captions
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🔄 Feedback Differences", 
                    "📝 Caption Differences", 
                    "📚 Ground Truth", 
                    "👤 Your Version"
                ])
                
                with tab1:
                    st.subheader("Feedback Comparison")
                    st.markdown("*Compare your feedback approach with the expert's feedback.*")
                    display_feedback_differences(
                        prev_feedback=new_annotator_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_prompt
                    )
                
                with tab2:
                    st.subheader("Caption Comparison")
                    st.markdown("*See the differences between your final caption and the expert's caption.*")
                    display_caption_differences(
                        prev_feedback=new_annotator_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_cap_prompt
                    )
                
                with tab3:
                    st.subheader("📚 Ground Truth Version")
                    st.markdown("*Expert annotation for reference and learning.*")
                    st.write(f"**Expert:** {current_user}")
                    st.write(f"**Created:** {format_timestamp(current_data.get('timestamp', ''))}")
                    display_feedback_info(current_data, display_pre_caption_instead_of_final_caption=False)
                
                with tab4:
                    st.subheader("👤 Your Version")
                    st.markdown("*Your annotation work for comparison.*")
                    st.write(f"**Annotator:** {new_annotator_user}")
                    st.write(f"**Created:** {format_timestamp(new_annotator_data.get('timestamp', ''))}")
                    display_feedback_info(new_annotator_data, display_pre_caption_instead_of_final_caption=True)

if __name__ == "__main__":
    main()