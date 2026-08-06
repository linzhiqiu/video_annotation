# caption/feedback_diff_app.py
import streamlit as st
import os
import json
import argparse
from feedback_app import (
    parse_args, load_video_data, get_video_id, load_json, highlight_differences, split_into_words,
    get_filename, load_data, FOLDER, FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX, get_annotator_videos,
    load_config, extract_frames, file_check, config_names_to_short_names, ANNOTATORS, REVIEWER_FILE_POSTFIX,
    display_feedback_info, display_feedback_differences, display_caption_differences, CONTAINER_HEIGHT,
    display_status_indicators, format_timestamp,
    get_video_status, get_video_format_func
)
from datetime import datetime
import time

def calculate_accuracy_stats(video_urls, output_dir):
    """Calculate accuracy statistics for all videos in the given directory.
    
    Returns:
        dict: Dictionary containing statistics for each annotator:
            {
                'annotator_name': {
                    'total_completed': int,
                    'total_reviewed': int,
                    'approved': int,
                    'rejected': int,
                    'accuracy': float
                }
            }
    """
    stats = {}
    
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        status, _, prev_file, current_user, prev_user = get_video_status(video_id, output_dir)
        
        # Skip if not completed
        if status == "not_completed":
            continue
            
        # Determine the annotator (original caption creator)
        annotator = prev_user if prev_file else current_user
        if annotator is None:
            print(f"annotator is None for video {video_id}")
            import pdb; pdb.set_trace()
            
        # Initialize annotator stats if not exists
        if annotator not in stats:
            stats[annotator] = {
                'total_completed': 0,
                'total_reviewed': 0,
                'approved': 0,
                'rejected': 0,
                'accuracy': 0.0
            }
        
        # Update total completed
        stats[annotator]['total_completed'] += 1
        
        # Update reviewed stats if applicable
        if status in ["approved", "rejected"]:
            stats[annotator]['total_reviewed'] += 1
            if status == "approved":
                stats[annotator]['approved'] += 1
            else:  # rejected
                stats[annotator]['rejected'] += 1
    
    # Calculate accuracy for each annotator
    for annotator in stats:
        total = stats[annotator]['total_reviewed']
        if total > 0:
            stats[annotator]['accuracy'] = stats[annotator]['approved'] / total
    
    return stats

def login_page(args):
    st.title("Video Caption Difference Viewer Login")

    # Create tabs for different login methods
    tab1, tab2 = st.tabs(["Login by Sheet", "Login by Annotator"])

    with tab1:
        # Original login by sheet form
        with st.form("login_form_sheet"):
            # Annotator selection dropdown
            selected_annotator = st.selectbox(
                "Select Your Name:",
                list(ANNOTATORS.keys()),
                key="selected_annotator_sheet",
                index=None,
                placeholder="Type or select your name...",
            )
            
            # Password input
            password = st.text_input("Enter Password:", type="password", key="password_input_sheet")
            
            # File selection dropdown with completion status if enabled
            try:
                # Load configs
                configs = load_config(FOLDER / args.configs)
                configs = [load_config(FOLDER / config) for config in configs]
                
                # Check completion status for each file
                start_time = time.time()
                file_status = {}
                for video_urls_file in args.video_urls_files:
                    video_urls = load_json(FOLDER / video_urls_file)
                    total = len(video_urls)
                    completed = 0
                    reviewed = 0
                    total = len(video_urls)
                    
                    for video_url in video_urls:
                        video_id = get_video_id(video_url)
                        is_completed = True
                        is_reviewed = True
                        
                        for config in configs:
                            config_output_dir = os.path.join(FOLDER, args.output, config["output_name"])
                            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
                            review_file = get_filename(video_id, config_output_dir, REVIEWER_FILE_POSTFIX)
                            
                            if not os.path.exists(feedback_file):
                                is_completed = False
                                is_reviewed = False
                                break
                                
                            if not os.path.exists(review_file):
                                is_reviewed = False
                        
                        if is_completed:
                            completed += 1
                        if is_reviewed:
                            reviewed += 1
                    
                    # Create status string
                    if completed == total and reviewed == total:
                        status = "✅✅"
                    elif completed == total:
                        status = "✅"
                    else:
                        status = ""
                    
                    file_status[video_urls_file] = f"{status} {os.path.basename(video_urls_file)} ({completed}/{total} completed, {reviewed}/{total} reviewed)"
                
                end_time = time.time()
                print(f"Completion status check took {end_time - start_time:.2f} seconds")
                
                # Create format function for selectbox
                def format_file_with_status(file_path):
                    return file_status.get(file_path, file_path)
                
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    args.video_urls_files,
                    key="selected_urls_file_sheet",
                    format_func=format_file_with_status
                )
            except Exception as e:
                st.error(f"Error checking completion status: {e}")
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    args.video_urls_files,
                    key="selected_urls_file_sheet"
                )

            submit_button = st.form_submit_button("Login")

            if submit_button:
                # Check if password matches
                if password == ANNOTATORS[selected_annotator]["password"]:
                    # Store the video URLs and annotator in session state
                    st.session_state.video_urls = load_json(FOLDER / selected_file)
                    st.session_state.logged_in = True
                    st.session_state.logged_in_user = selected_annotator
                    st.success(f"Login successful! Welcome, {selected_annotator}!")
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")

    with tab2:
        # New login by annotator form
        with st.form("login_form_annotator"):
            # Annotator selection dropdown for login
            selected_annotator = st.selectbox(
                "Select Your Name:",
                list(ANNOTATORS.keys()),
                key="selected_annotator_annotator",
                index=None,
                placeholder="Type or select your name...",
            )
            
            # Password input
            password = st.text_input("Enter Password:", type="password", key="password_input_annotator")
            
            # Dropdown to select which annotator's videos to search for
            target_annotator = st.selectbox(
                "Search for videos completed by:",
                list(ANNOTATORS.keys()),
                key="target_annotator",
                index=None,
                placeholder="Type or select annotator name...",
            )
            
            # Not yet reviewed checkbox
            not_yet_reviewed = False
            
            # Show only rejected checkbox
            show_only_rejected = st.checkbox(
                "Show only rejected videos",
                value=False,
                key="show_only_rejected"
            )

            submit_button = st.form_submit_button("Login")

            if submit_button:
                # Check if password matches
                if password == ANNOTATORS[selected_annotator]["password"]:
                    try:
                        # Load configs
                        configs = load_config(FOLDER / args.configs)
                        configs = [load_config(FOLDER / config) for config in configs]
                        
                        # Get videos for the target annotator
                        start_time = time.time()
                        matching_videos = get_annotator_videos(
                            target_annotator,  # Use target_annotator instead of selected_annotator
                            configs,
                            args.output,
                            not_yet_reviewed,
                            show_only_rejected
                        )
                        end_time = time.time()
                        print(f"Getting annotator videos took {end_time - start_time:.2f} seconds")
                        
                        if not matching_videos:
                            st.error(f"No matching videos found for annotator {target_annotator}.")
                        else:
                            # Store the matching videos and annotator in session state
                            st.session_state.video_urls = matching_videos
                            st.session_state.logged_in = True
                            st.session_state.logged_in_user = selected_annotator
                            st.success(f"Login successful! Welcome, {selected_annotator}! Found {len(matching_videos)} matching videos for {target_annotator}.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error getting annotator videos: {e}")
                else:
                    st.error("Incorrect password. Please try again.")

def display_caption_expander(data, user, timestamp):
    """Helper function to display caption information in an expander"""
    st.write("##### Annotator")
    st.write(f"**Annotator:** {user}")
    st.write(f"**Timestamp:** {format_timestamp(timestamp)}")
    st.write("##### Pre-caption")
    st.write(data.get("pre_caption", "No pre-caption available"))
    
    # Use the existing display_feedback_info function from feedback_app.py
    display_feedback_info(data, display_pre_caption_instead_of_final_caption=False)

def display_accuracy_statistics(config_names, config_dict, video_urls, args):
    """Display accuracy statistics for all configs in an expander"""
    with st.expander("📊 Accuracy Statistics", expanded=False):
        # Calculate stats for all configs
        all_stats = {}
        for config_name in config_names:
            config = config_dict[config_name]
            output_dir = os.path.join(FOLDER, args.output, config["output_name"])
            if not os.path.exists(output_dir):
                continue
            stats = calculate_accuracy_stats(video_urls, output_dir)
            if stats:
                all_stats[config_name] = stats
        
        if not all_stats:
            st.info("No completed videos found for any task.")
        else:
            # Create tabs for each task
            task_tabs = st.tabs([config_names_to_short_names[config_name] for config_name in all_stats.keys()])
            
            # Add content to each tab
            for tab, (config_name, stats) in zip(task_tabs, all_stats.items()):
                with tab:
                    # Create markdown table string
                    table_str = "| Annotator | Total Completed | Total Reviewed | Approved | Rejected | Accuracy |\n"
                    table_str += "|-----------|----------------|----------------|----------|----------|----------|\n"
                    
                    # Add data rows for each annotator
                    for annotator, data in sorted(stats.items()):
                        if data['total_reviewed'] > 0:
                            table_str += f"| {annotator} | {data['total_completed']} | {data['total_reviewed']} | {data['approved']} | {data['rejected']} | {data['accuracy']:.1%} |\n"
                        else:
                            table_str += f"| {annotator} | {data['total_completed']} | 0 | 0 | 0 | N/A |\n"
                    # Display the table
                    st.markdown(table_str)

def main(args):
    # # Set page config first
    # st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # # Check login status
    # if "logged_in" not in st.session_state or not st.session_state.logged_in:
    #     login_page(args)
    #     return
    # ONLY set page config if we're running standalone (not in portal mode)
    # if not hasattr(st.session_state, 'selected_portal'):
    #     st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # Check login status - ONLY if not already logged in through unified system
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # ONLY show login if we're running standalone
        if not hasattr(st.session_state, 'selected_portal'):
            login_page(args)
            return
        else:
            # If we're in portal mode but not logged in, something went wrong
            st.error("Authentication error. Please logout and login again.")
            return
    
    # After successful login, update the output directory based on the logged-in user if personalize_output is True
    if args.personalize_output and "logged_in_user" in st.session_state:
        # Only set the personalized output directory once in session state
        if "personalized_output" not in st.session_state:
            username = convert_name_to_username(st.session_state.logged_in_user)
            st.session_state.personalized_output = f"{args.output}_{username}"
        
        # Use the stored personalized output directory
        args.output = st.session_state.personalized_output
        st.sidebar.write(f"**Output Directory:** {args.output}")

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
        with st.container(height=CONTAINER_HEIGHT, border=False):
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
                    if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 'video_urls', 'last_video_id', 'last_selected_video', 'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 'target_annotator']:
                        keys_to_remove.append(key)

                # Remove all collected keys
                for key in keys_to_remove:
                    del st.session_state[key]

                # Set the new video id
                st.session_state.last_config_id = selected_config
                print(f"Config changed to: {selected_config}")
                st.rerun()  # Force a rerun to ensure clean state

            config = config_dict[selected_config]
            # st.title(f"Caption Difference Viewer - {config.get('name', '')}")
            st.markdown(f"### {config.get('name', '')}")
            # Get video URLs from session state
            video_urls = st.session_state.video_urls
            
            output_dir = os.path.join(FOLDER, args.output, config["output_name"])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Display status indicators explanation
            display_status_indicators()

            # Display accuracy statistics
            display_accuracy_statistics(config_names, config_dict, video_urls, args)

            # Select video
            selected_video = st.selectbox(
                "Select a video:",
                video_urls,
                format_func=get_video_format_func(output_dir, video_urls=video_urls),
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
                    if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 'target_annotator']:
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
                'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 'personalized_output',
                'selected_portal', 'login_method', 'target_annotator'
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
        with st.container(height=CONTAINER_HEIGHT, border=True):
            status, current_file, prev_file, current_user, prev_user = get_video_status(video_id, output_dir)
            
            if status == "not_completed":
                st.warning("Please complete this caption first.")
            elif status == "completed_not_reviewed":
                st.info("The caption has been completed but not reviewed yet.")
            elif status == "approved":
                # For approved captions, only show the current version
                current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                st.success("✅ This caption has been approved! Great job!")
                st.write("**Current Version:**")
                display_caption_expander(current_data, current_user, current_data.get("timestamp", "Unknown"))
            else:  # rejected
                # Load both current and previous captions
                current_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                prev_data = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                reviewer_data = load_data(video_id, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                st.subheader("Caption Changes")
                
                # Display metadata information
                current_timestamp = format_timestamp(current_data.get("timestamp", "Unknown"))
                prev_timestamp = format_timestamp(prev_data.get("timestamp", "Unknown"))
                
                st.write(f"**Current Version:** By {current_user} on {current_timestamp}")
                st.write(f"**Previous Version:** By {prev_user} on {prev_timestamp}")
                
                # Display a message if the same user made both versions
                st.warning("❌ This caption was rejected and needs to be fixed.")
                
                # Display the differences
                current_caption = current_data["final_caption"]
                prev_caption = prev_data["final_caption"]
                
                # Create tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(["Feedback Differences", "Caption Differences", "Previous Version", "Current Version"])
                
                with tab1:
                    st.subheader("Feedback Differences")
                    display_feedback_differences(
                        prev_feedback=prev_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_prompt,
                        reviewer_data=reviewer_data
                    )
                    
                with tab2:
                    st.subheader("Caption Differences")
                    display_caption_differences(
                        prev_feedback=prev_data,
                        feedback_data=current_data,
                        diff_prompt=args.diff_cap_prompt,
                        reviewer_data=reviewer_data
                    )
                    
                with tab3:
                    st.subheader("Previous Version")
                    display_caption_expander(prev_data, prev_user, prev_data.get('timestamp', ''))
                    
                with tab4:
                    st.subheader("Current Version")
                    display_caption_expander(current_data, current_user, current_data.get('timestamp', ''))

if __name__ == "__main__":
    args = parse_args()
    main(args) 