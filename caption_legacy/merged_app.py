import streamlit as st
import os
import json
import argparse
import time
from datetime import datetime
from pathlib import Path

# Import everything from both original apps
import feedback_app
import feedback_diff_app

# Import specific functions we need for the unified login
from feedback_app import (
    ANNOTATORS, FOLDER, load_json, load_config, check_video_completion_status,
    get_annotator_videos, get_video_id
)

def create_unified_args(args, portal_type):
    """Create a copy of args with portal-specific modifications if needed"""
    # For now, both portals use the same args, but this allows future customization
    return args

def unified_login_page(args):
    """Unified login page for both portals - reuses login logic from both original apps"""
    st.title("🎥 Video Caption and Review System")
    st.markdown("### Welcome to the Video Caption and Review System")
    
    # Create tabs for different login methods - combining both apps' login approaches
    tab1, tab2, tab3 = st.tabs(["📋 Login by Sheet", "👤 Login by Annotator", "📋 Job Assignment"])

    with tab1:
        # Reuse the login logic from feedback_app.py (tab1 from both apps is identical)
        with st.form("login_form_sheet"):
            st.markdown("#### Login to access video sheets")
            
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
            
            # File selection dropdown with completion status - reuse from feedback_app
            try:
                configs = load_config(FOLDER / args.configs)
                configs = [load_config(FOLDER / config) for config in configs]
                
                # Reuse the completion status check from feedback_app
                start_time = time.time()
                file_status = {}
                for video_urls_file in args.video_urls_files:
                    status_dict, annotators_dict, reviewers_dict = check_video_completion_status(
                        video_urls_file, 
                        configs,
                        args.output
                    )
                    # Count completed and reviewed videos
                    completed = sum(1 for _, (is_completed, _) in status_dict.items() if is_completed)
                    reviewed = sum(1 for _, (_, is_reviewed) in status_dict.items() if is_reviewed)
                    total = len(status_dict)
                    annotators = len(annotators_dict)
                    reviewers = len(reviewers_dict)
                    annotator_str = ", ".join([f"{annotator} ({count})" for annotator, count in annotators_dict.items()])
                    reviewer_str = ", ".join([f"{reviewer} ({count})" for reviewer, count in reviewers_dict.items()])
                    
                    # Create status string
                    if completed == total and reviewed == total:
                        status = "✅✅"
                    elif completed == total:
                        status = "✅"
                    else:
                        status = ""
                    
                    file_status[video_urls_file] = f"{status} {os.path.basename(video_urls_file)} ({completed}/{total} completed, {reviewed}/{total} reviewed) (Annotators: {annotator_str}, Reviewers: {reviewer_str})"
                
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

            submit_button = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit_button:
                if selected_annotator and password == ANNOTATORS[selected_annotator]["password"]:
                    # Store the video URLs and annotator in session state
                    st.session_state.video_urls = load_json(FOLDER / selected_file)
                    st.session_state.logged_in = True
                    st.session_state.logged_in_user = selected_annotator
                    st.session_state.login_method = "sheet"
                    st.success(f"Login successful! Welcome, {selected_annotator}!")
                    st.rerun()
                else:
                    st.error("Incorrect password or missing name. Please try again.")

    with tab2:
        # Reuse login logic from feedback_diff_app.py (modified for both caption and review)
        with st.form("login_form_annotator"):
            st.markdown("#### Search for specific annotator's videos")
            
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
                key="target_annotator_select",
                index=None,
                placeholder="Type or select annotator name...",
            )
            
            # Options for filtering - combining options from both apps
            col1, col2 = st.columns(2)
            with col1:
                not_yet_reviewed = st.checkbox(
                    "Show only videos not yet reviewed",
                    value=True,
                    key="not_yet_reviewed"
                )
            with col2:
                show_only_rejected = st.checkbox(
                    "Show only rejected videos",
                    value=False,
                    key="show_only_rejected"
                )

            submit_button = st.form_submit_button("🔍 Search & Login", use_container_width=True)

            if submit_button:
                if selected_annotator and password == ANNOTATORS[selected_annotator]["password"]:
                    try:
                        configs = load_config(FOLDER / args.configs)
                        configs = [load_config(FOLDER / config) for config in configs]
                        
                        # Reuse get_annotator_videos from feedback_app
                        start_time = time.time()
                        matching_videos = get_annotator_videos(
                            target_annotator,
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
                            st.session_state.video_urls = matching_videos
                            st.session_state.logged_in = True
                            st.session_state.logged_in_user = selected_annotator
                            st.session_state.login_method = "annotator"
                            st.session_state.target_annotator = target_annotator
                            st.success(f"Login successful! Welcome, {selected_annotator}! Found {len(matching_videos)} matching videos for {target_annotator}.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error getting annotator videos: {e}")
                else:
                    st.error("Incorrect password or missing name. Please try again.")
    with tab3:
        st.markdown("#### Job Assignment Spreadsheet")
        st.markdown("Access the master job assignment spreadsheet to view task allocations and progress.")
        
        st.link_button(
            "📋 **Open Job Assignment Spreadsheet**", 
            "https://docs.google.com/spreadsheets/d/10g-ynle9VCDrCcDCxEfBafVRdbOAckzl0y6S-J22kDY/edit?gid=0#gid=0",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("---")
        st.info("💡 This spreadsheet contains task assignments, deadlines, and progress tracking for all team members.")

def portal_selection_page():
    """Portal selection page after login"""
    st.title("🎯 Select Portal")
    st.markdown(f"### Welcome back, **{st.session_state.logged_in_user}**!")
    
    # Display login info
    if st.session_state.get('login_method') == 'annotator':
        st.info(f"📊 You're viewing videos by: **{st.session_state.get('target_annotator', 'Unknown')}**")
    
    st.markdown("---")
    
    # Create two columns for portal selection
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📝 Caption Portal")
        st.markdown("""
        **Create and Edit Captions**
        - Generate AI-powered pre-captions
        - Provide feedback to refine captions
        - Approve or reject captions (reviewer only)
        """)
        if st.button("🚀 Enter Caption Portal", key="caption_portal", use_container_width=True):
            st.session_state.selected_portal = "caption"
            # Clear any portal-specific state to ensure clean start
            clear_portal_state()
            st.rerun()
    
    with col2:
        st.markdown("### 🔍 Review Portal")
        st.markdown("""
        **Review and Compare Captions**
        - View caption differences
        - Compare feedback for each video
        - Review accuracy statistics
        """)
        if st.button("🔍 Enter Review Portal", key="review_portal", use_container_width=True):
            st.session_state.selected_portal = "review"
            # Clear any portal-specific state to ensure clean start
            clear_portal_state()
            st.rerun()
    
    st.markdown("---")
    
    # Logout and portal switching options
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def clear_portal_state():
    """Clear portal-specific state while preserving login and navigation state"""
    # Keys to preserve across portal switches
    preserve_keys = {
        'logged_in', 'logged_in_user', 'video_urls', 'login_method', 'target_annotator',
        'selected_portal', 'file_check_passed', 'personalized_output'
    }
    
    # Clear all other keys
    keys_to_clear = [k for k in st.session_state.keys() if k not in preserve_keys]
    for key in keys_to_clear:
        del st.session_state[key]

def add_portal_navigation_sidebar(current_portal, args):
    """Add consistent portal navigation to sidebar"""
    with st.sidebar:
        if current_portal == "caption":
            st.title("📝 Caption Portal")
        else:
            st.title("🔍 Review Portal")
            
        st.write(f"**User:** {st.session_state.logged_in_user}")
        
        if hasattr(args, 'output') and args.personalize_output:
            st.write(f"**Output Directory:** {args.output}")
        
        st.markdown("---")
        
        # Portal switching
        if current_portal == "caption":
            if st.button("🔄 Switch to Review Portal"):
                st.session_state.selected_portal = "review"
                clear_portal_state()
                st.rerun()
        else:
            if st.button("🔄 Switch to Caption Portal"):
                st.session_state.selected_portal = "caption"
                clear_portal_state()
                st.rerun()
        
        if st.button("🏠 Back to Portal Selection"):
            if 'selected_portal' in st.session_state:
                del st.session_state.selected_portal
            clear_portal_state()
            st.rerun()
        
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def caption_portal_wrapper(args):
    """Wrapper for caption portal - calls original feedback_app main with modifications"""
    # Add portal navigation
    add_portal_navigation_sidebar("caption", args)
    
    # Prepare args for the original caption app
    caption_args = create_unified_args(args, "caption")
    
    # # Modify the original main function call to work in portal mode
    # # We need to patch the page config call since it's already set
    # original_set_page_config = st.set_page_config
    # st.set_page_config = lambda **kwargs: None  # Disable page config in subprocess
    
    # try:
    #     # Call the original main function from feedback_app
    feedback_app.main(caption_args, feedback_app.caption_programs)
    # finally:
    #     # Restore original page config function
    #     st.set_page_config = original_set_page_config

def review_portal_wrapper(args):
    """Wrapper for review portal - calls original feedback_diff_app main with modifications"""
    # Add portal navigation
    add_portal_navigation_sidebar("review", args)
    
    # Prepare args for the original review app
    review_args = create_unified_args(args, "review")
    
    # # Modify the original main function call to work in portal mode
    # # We need to patch the page config call since it's already set
    # original_set_page_config = st.set_page_config
    # st.set_page_config = lambda **kwargs: None  # Disable page config in subprocess
    
    # try:
    #     # Call the original main function from feedback_diff_app
    feedback_diff_app.main(review_args)
    # finally:
    #     # Restore original page config function
    #     st.set_page_config = original_set_page_config

def main():
    """Main application entry point"""
    # Set page config once at the top level
    st.set_page_config(
        page_title="Video Caption System",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Parse arguments - reuse from feedback_app
    args = feedback_app.parse_args()
    
    # Check login status
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        unified_login_page(args)
        return
    
    # Check portal selection
    if "selected_portal" not in st.session_state:
        portal_selection_page()
        return
    
    # Route to appropriate portal using the original main functions
    if st.session_state.selected_portal == "caption":
        caption_portal_wrapper(args)
    elif st.session_state.selected_portal == "review":
        review_portal_wrapper(args)
    else:
        st.error("Invalid portal selection")
        if 'selected_portal' in st.session_state:
            del st.session_state.selected_portal
        st.rerun()

if __name__ == "__main__":
    main()