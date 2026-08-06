# caption/core/auth.py
import streamlit as st
import os
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from caption.core.data_manager import DataManager
from caption.core.ui_components import UIComponents

def load_annotators_from_files(input_dir="annotator") -> Dict[str, Dict[str, str]]:
    """Load annotators from individual JSON files.
    
    Args:
        input_dir: Directory containing the JSON files
        
    Returns:
        Dictionary of annotators with their passwords
    """
    annotators = {}
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        print(f"Warning: Annotator directory {input_dir} does not exist")
        return annotators
    
    # Load each JSON file
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    annotators.update(data)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
    
    return annotators


# Load annotators from files
ANNOTATORS = load_annotators_from_files()
APPROVED_REVIEWERS = [
    "Zhiqiu Lin", "Siyuan Cen", "Yuhan Huang", "Hewei Wang", 
    "Tiffany Ling", "Isaac Li", "Shihang Zhu", "Caption Pizza",
    "Irene Pi", "Zhenye Luo"
]
META_REVIEWERS = [
    "Zhiqiu Lin", "Siyuan Cen", "Yuhan Huang", "Hewei Wang", 
    "Tiffany Ling", "Isaac Li", "Shihang Zhu", "Caption Pizza"
]

# Ensure all approved reviewers are in annotators dictionary
assert set(APPROVED_REVIEWERS) <= set(ANNOTATORS.keys()), \
    "All approved reviewers must be in the ANNOTATORS dictionary"


class AuthManager:
    """Handles authentication and login logic"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    @staticmethod
    def get_all_meta_reviewers() -> List[str]:
        """Get all meta-reviewers"""
        return META_REVIEWERS
    
    def show_login_page(self, app_config):
        """Unified login page for both portals"""
        st.title("🎥 Video Caption and Review System")
        st.markdown(f"### Welcome to the {app_config.name}")
        
        # Create tabs for different login methods - CHANGED: Added 4th tab, made video search 3rd tab
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Login by Sheet", "👤 Login by Annotator", "🔍 Video ID Search", "📋 Job Assignment"])

        with tab1:
            self._render_sheet_login_tab(app_config)
        
        with tab2:
            self._render_annotator_login_tab(app_config)
            
        with tab3:
            self._render_video_search_tab(app_config)
            
        with tab4:
            self._render_job_assignment_tab()

    
    def _render_video_search_tab(self, app_config):
        """Render the video ID search tab"""
        st.markdown("#### Search Video ID Across All Sheets")
        st.markdown("Search for a specific video ID across all sheets and tasks to see its completion status.")
        
        # Video ID input
        video_id_input = st.text_input(
            "Enter Video ID to search:",
            key="video_id_search_input",
            placeholder="e.g., 0001, 0045, 1234, etc.",
            help="Enter the video ID (without file extension) to search across all sheets"
        )
        
        search_button = st.button("🔍 Search Video ID", type="primary", use_container_width=True)
        
        if search_button and video_id_input.strip():
            video_id = video_id_input.strip()
            st.markdown("---")
            
            try:
                # Load all configs
                configs = self.data_manager.load_config(app_config.configs_file)
                configs = [self.data_manager.load_config(config) for config in configs]
                
                # Search across all video URLs files
                video_found = False
                search_results = []
                
                for video_urls_file in app_config.video_urls_files:
                    try:
                        video_urls = self.data_manager.load_json(video_urls_file)
                        
                        # Check if video_id exists in this file
                        for idx, video_url in enumerate(video_urls):
                            current_video_id = self.data_manager.get_video_id(video_url)
                            
                            if current_video_id == video_id:
                                video_found = True
                                
                                # Get sheet name from file path
                                sheet_name = video_urls_file.split('/')[-1].replace('.json', '')
                                
                                # Check status across all tasks/configs
                                task_statuses = []
                                for config in configs:
                                    # Fix: Use proper path construction like other parts of codebase
                                    config_output_dir = os.path.join(
                                        self.data_manager.folder, 
                                        app_config.output_dir, 
                                        config['output_name']
                                    )
                                    status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                                        video_id, config_output_dir
                                    )
                                    
                                    # Get completion details
                                    completion_info = self._get_completion_details(
                                        status, current_user, prev_user, current_file, config_output_dir, video_id
                                    )
                                    
                                    task_statuses.append({
                                        'task_name': config['name'],
                                        'status': status,
                                        'completion_info': completion_info
                                    })
                                
                                search_results.append({
                                    'video_id': video_id,
                                    'video_url': video_url,
                                    'sheet_name': sheet_name,
                                    'index': idx,
                                    'task_statuses': task_statuses
                                })
                                
                    except Exception as e:
                        st.warning(f"Error searching in {video_urls_file}: {e}")
                        continue
                
                # Display results
                if video_found:
                    st.success(f"✅ Found video ID **{video_id}** in {len(search_results)} sheet(s)")
                    
                    for result in search_results:
                        st.markdown(f"### 📄 Sheet: **{result['sheet_name']}**")
                        st.markdown(f"**Video ID:** {result['video_id']}")
                        st.markdown(f"**Index in sheet:** {result['index']}")
                        st.markdown(f"**Video URL:** `{result['video_url']}`")
                        
                        # Task completion status table
                        st.markdown("#### Task Completion Status:")
                        
                        # Create a table for task statuses
                        table_data = []
                        for task in result['task_statuses']:
                            # Get short name for display using existing mapping
                            short_name = UIComponents.config_names_to_short_names.get(
                                task['task_name'], task['task_name']
                            )
                            
                            # Get status emoji using existing pattern
                            status_emoji_map = {
                                "not_completed": "⭕",
                                "completed_not_reviewed": "✅", 
                                "approved": "✅✅",
                                "rejected": "❌"
                            }
                            status_emoji = status_emoji_map.get(task['status'], "❓")
                            
                            table_data.append({
                                'Task': short_name,
                                'Status': f"{status_emoji} {task['status'].replace('_', ' ').title()}",
                                'Details': task['completion_info']
                            })
                        
                        # Display as columns for better readability
                        for task_data in table_data:
                            col1, col2, col3 = st.columns([2, 2, 3])
                            with col1:
                                st.write(f"**{task_data['Task']}**")
                            with col2:
                                st.write(task_data['Status'])
                            with col3:
                                st.write(task_data['Details'])
                        
                        st.markdown("---")
                else:
                    st.error(f"❌ Video ID **{video_id}** not found in any sheets")
                    st.info("💡 Make sure you entered the correct video ID (usually a number like 0001, 0045, etc.)")
                    
            except Exception as e:
                st.error(f"Error during search: {e}")
        
        elif search_button and not video_id_input.strip():
            st.warning("⚠️ Please enter a video ID to search")
    
    def _get_completion_details(self, status, current_user, prev_user, current_file, config_output_dir, video_id):
        """Get human-readable completion details"""
        if status == "not_completed":
            return "Not completed"
        elif status == "completed_not_reviewed":
            return f"Completed by {current_user or 'Unknown'}"
        elif status == "approved":
            # For approved status, get reviewer name from reviewer file
            reviewer_name = self._get_reviewer_name(config_output_dir, video_id)
            annotator_name = prev_user or current_user or 'Unknown'
            return f"Completed by {annotator_name}, Approved by {reviewer_name}"
        elif status == "rejected":
            # For rejected status, get reviewer name from reviewer file  
            reviewer_name = self._get_reviewer_name(config_output_dir, video_id)
            annotator_name = prev_user or current_user or 'Unknown'
            return f"Completed by {annotator_name}, Rejected by {reviewer_name}"
        else:
            return "Unknown status"
    
    def _get_reviewer_name(self, config_output_dir, video_id):
        """Get reviewer name from reviewer file"""
        reviewer_file = self.data_manager.get_filename(
            video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX
        )
        
        if os.path.exists(reviewer_file):
            try:
                with open(reviewer_file, 'r') as f:
                    reviewer_data = json.load(f)
                    return reviewer_data.get("reviewer_name", "Unknown")
            except Exception:
                return "Unknown"
        return "Unknown"

    def _render_sheet_login_tab(self, app_config):
        """Render the sheet-based login tab"""
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
            
            # File selection dropdown with completion status
            try:
                configs = self.data_manager.load_config(app_config.configs_file)
                configs = [self.data_manager.load_config(config) for config in configs]
                
                # Check completion status for each file
                start_time = time.time()
                file_status = {}
                for video_urls_file in app_config.video_urls_files:
                    status_dict, annotators_dict, reviewers_dict = self.data_manager.check_video_completion_status(
                        video_urls_file, configs, app_config.output_dir
                    )
                    
                    # Count completed and reviewed videos
                    completed = sum(1 for _, (is_completed, _) in status_dict.items() if is_completed)
                    reviewed = sum(1 for _, (_, is_reviewed) in status_dict.items() if is_reviewed)
                    total = len(status_dict)
                    
                    # Format annotator and reviewer info
                    annotator_str = ", ".join([f"{annotator} ({count})" for annotator, count in annotators_dict.items()])
                    reviewer_str = ", ".join([f"{reviewer} ({count})" for reviewer, count in reviewers_dict.items()])
                    
                    # Create status string
                    if completed == total and reviewed == total:
                        status = "✅✅"
                    elif completed == total:
                        status = "✅"
                    else:
                        status = ""
                    
                    file_status[video_urls_file] = (
                        f"{status} {os.path.basename(video_urls_file)} "
                        f"({completed}/{total} completed, {reviewed}/{total} reviewed) "
                        f"(Annotators: {annotator_str}, Reviewers: {reviewer_str})"
                    )
                
                end_time = time.time()
                print(f"Completion status check took {end_time - start_time:.2f} seconds")
                
                # Create format function for selectbox
                def format_file_with_status(file_path):
                    return file_status.get(file_path, file_path)
                
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    app_config.video_urls_files,
                    key="selected_urls_file_sheet",
                    format_func=format_file_with_status
                )
            except Exception as e:
                st.error(f"Error checking completion status: {e}")
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    app_config.video_urls_files,
                    key="selected_urls_file_sheet"
                )

            submit_button = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit_button:
                if selected_annotator and password == ANNOTATORS[selected_annotator]["password"]:
                    # Store the video URLs and annotator in session state
                    st.session_state.video_urls = self.data_manager.load_json(selected_file)
                    st.session_state.logged_in = True
                    st.session_state.logged_in_user = selected_annotator
                    st.session_state.login_method = "sheet"
                    st.session_state.selected_sheet_file = selected_file
                    st.success(f"Login successful! Welcome, {selected_annotator}!")
                    st.rerun()
                else:
                    st.error("Incorrect password or missing name. Please try again.")
    
    def _render_annotator_login_tab(self, app_config):
        """Render the annotator-based login tab"""
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
            
            # Options for filtering
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
                        configs = self.data_manager.load_config(app_config.configs_file)
                        configs = [self.data_manager.load_config(config) for config in configs]
                        
                        # Get annotator videos
                        start_time = time.time()
                        matching_videos = self.data_manager.get_annotator_videos(
                            target_annotator, configs, app_config.output_dir,
                            not_yet_reviewed, show_only_rejected
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
                            st.success(f"Login successful! Welcome, {selected_annotator}! "
                                     f"Found {len(matching_videos)} matching videos for {target_annotator}.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error getting annotator videos: {e}")
                else:
                    st.error("Incorrect password or missing name. Please try again.")
    
    def _render_job_assignment_tab(self):
        """Render the job assignment tab"""
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
    
    @staticmethod
    def is_logged_in() -> bool:
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)

    @staticmethod
    def get_user_email(username: str) -> Optional[str]:
        """Get email for a given username"""
        if username in ANNOTATORS:
            return ANNOTATORS[username].get("email", None)
        return None
    
    @staticmethod
    def get_current_user() -> Optional[str]:
        """Get current logged in user"""
        return st.session_state.get('logged_in_user')
    
    @staticmethod
    def logout():
        """Clear all session state and logout"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    @staticmethod
    def can_annotator_redo(video_id: str, output_dir: str, current_user: str, data_manager: DataManager) -> bool:
        """Check if the current user (as annotator) can redo the caption"""
        annotator, reviewer = data_manager.get_annotator_and_reviewer(video_id, output_dir)
        
        # If no annotator yet, anyone can be the annotator
        if not annotator:
            return True
        
        # If same annotator, check if it's been reviewed
        if annotator == current_user:
            reviewer_data = data_manager.load_data(video_id, output_dir, "_review.json")
            return not reviewer_data  # Can redo if not reviewed yet
        
        return False
    
    @staticmethod
    def can_reviewer_redo(video_id: str, output_dir: str, current_user: str, data_manager: DataManager) -> bool:
        """Check if the current user (as reviewer) can redo the caption"""
        annotator, reviewer = data_manager.get_annotator_and_reviewer(video_id, output_dir)
        
        # Must be an approved reviewer
        if current_user not in APPROVED_REVIEWERS:
            return False
        
        # Cannot review if you're the annotator
        if annotator == current_user:
            return False
        
        return True