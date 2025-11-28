import argparse
import streamlit as st
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Import from the new structure
from caption.config import get_config
from caption.core.auth import AuthManager
from caption.core.data_manager import DataManager
from caption.core.video_utils import VideoUtils
from caption.core.ui_components import UIComponents
from caption.core.caption_engine import CaptionEngine
from caption.interfaces.caption_interface import CaptionInterface
from caption.interfaces.review_interface import ReviewInterface
from caption.session_state_manager import SessionStateKeyManager


def parse_args():
    """Parse command line arguments for the new annotator onboarding system"""
    parser = argparse.ArgumentParser(description="New Annotator Onboarding System")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=["video_urls/new_annotator_exam/exam.json"],
        help="List of paths to test URLs files",
    )
    parser.add_argument("--output_new_annotator", type=str, default="output_onboarding/output_new_annotator", 
                       help="Path to the new annotator output directory")
    return parser.parse_args()


class OnboardingApp:
    """New Annotator Onboarding Application"""
    
    def __init__(self, config_type: str, video_urls_files: list, output_new_annotator: str):
        # Get base config and modify for new annotator use
        self.base_config = get_config(config_type)
        
        # Override specific settings for new annotator training
        self.base_config.video_urls_files = video_urls_files
        self.base_config.personalize_output = True
        
        self.output_new_annotator = output_new_annotator
        self.folder_path = Path(__file__).parent.parent  # Go up to caption/ directory
        self.root_path = self.folder_path.parent  # Go up to project root
        
        # Initialize core components
        self.data_manager = DataManager(self.folder_path, self.root_path)
        self.auth_manager = AuthManager(self.data_manager)
        self.video_utils = VideoUtils()
        self.caption_engine = CaptionEngine(self.data_manager)
        self.ui = UIComponents()
        
        # Initialize interfaces
        self.caption_interface = CaptionInterface(self.data_manager, self.caption_engine)
        self.review_interface = ReviewInterface(self.data_manager)
    
    def run(self):
        """Main application entry point"""
        st.set_page_config(
            page_title="New Annotator Onboarding System",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Check login status
        if not self.auth_manager.is_logged_in():
            self._show_login_page()
            return
        
        # Setup personalized output
        self._setup_personalized_output()
        
        # Check mode selection
        if "selected_portal_mode" not in st.session_state:
            self._show_mode_selection()
            return
        
        # Route to appropriate mode
        if st.session_state.selected_portal_mode == "caption":
            self._run_caption_mode()
        elif st.session_state.selected_portal_mode == "comparison":
            self._run_comparison_mode()
        else:
            if 'selected_portal_mode' in st.session_state:
                del st.session_state.selected_portal_mode
            st.rerun()
    
    def _show_login_page(self):
        """Show unified login page for new annotator system"""
        st.title("🎓 New Annotator Onboarding System")
        st.markdown(f"### Welcome to the {self.base_config.name} Onboarding")
        
        with st.form("new_annotator_login_form"):
            st.markdown("#### Login to access the onboarding system")
            
            # Import ANNOTATORS from auth module
            from caption.core.auth import ANNOTATORS
            
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
                self.base_config.video_urls_files, 
                key="selected_urls_file",
                format_func=lambda x: f"📋 {os.path.basename(x)}"
            )

            submit_button = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit_button:
                if selected_annotator and password == ANNOTATORS[selected_annotator]["password"]:
                    # Load video URLs and store in session state
                    video_urls = self.data_manager.load_json(selected_file)
                    st.session_state.video_urls = video_urls
                    st.session_state.logged_in = True
                    st.session_state.logged_in_user = selected_annotator
                    st.session_state.selected_portal_file = selected_file
                    # Set portal mode flag so other components know it's running in portal mode
                    st.session_state.selected_portal = True  # This flags it as onboarding mode
                    st.success(f"Login successful! Welcome to training, {selected_annotator}!")
                    st.rerun()
                else:
                    st.error("Incorrect password or missing name. Please try again.")
    
    def _show_mode_selection(self):
        """Show mode selection page after login"""
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
                self._clear_mode_state()
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
                self._clear_mode_state()
                st.rerun()
        
        st.markdown("---")
        
        # Additional features that might be in original new_annotator_app.py
        with st.expander("📊 Training Progress", expanded=False):
            self._display_training_progress()
        
        # Logout option
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    def _display_training_progress(self):
        """Display training progress statistics"""
        try:
            # Load configs to check progress
            configs = self.data_manager.load_config(self.base_config.configs_file)
            configs = [self.data_manager.load_config(config) for config in configs]
            
            video_urls = st.session_state.video_urls
            
            # Calculate progress for each task
            progress_data = {}
            total_completed = 0
            total_videos = len(video_urls) * len(configs)
            
            for config in configs:
                config_output_dir = str(self.folder_path / self.output_new_annotator / config["output_name"])
                completed_count = 0
                
                for video_url in video_urls:
                    video_id = self.data_manager.get_video_id(video_url)
                    if self.data_manager.data_exists(video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX):
                        completed_count += 1
                        total_completed += 1
                
                progress_data[config["name"]] = {
                    "completed": completed_count,
                    "total": len(video_urls),
                    "percentage": (completed_count / len(video_urls)) * 100 if video_urls else 0
                }
            
            # Display overall progress
            overall_percentage = (total_completed / total_videos) * 100 if total_videos > 0 else 0
            st.metric(
                label="Overall Training Progress",
                value=f"{total_completed}/{total_videos}",
                delta=f"{overall_percentage:.1f}% Complete"
            )
            
            # Display task-by-task progress
            st.markdown("##### Task Progress")
            for task_name, progress in progress_data.items():
                short_name = self.ui.config_names_to_short_names.get(task_name, task_name)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(progress["percentage"] / 100)
                    st.caption(f"{short_name}: {progress['completed']}/{progress['total']}")
                with col2:
                    st.metric("", f"{progress['percentage']:.0f}%")
                    
        except Exception as e:
            st.error(f"Error calculating training progress: {e}")
    
    def _setup_personalized_output(self):
        """Setup personalized output directory"""
        if self.base_config.personalize_output and "logged_in_user" in st.session_state:
            if "personalized_output" not in st.session_state:
                username = self.video_utils.convert_name_to_username(st.session_state.logged_in_user)
                st.session_state.personalized_output = f"{self.output_new_annotator}_{username}"
                print(f"Personalized output directory: {st.session_state.personalized_output}")
                
                # Copy feedback files from main project for precaption
                self.caption_engine.copy_feedback_for_precaption(
                    self.base_config.configs_file,
                    st.session_state.video_urls,
                    self.base_config.main_project_output,
                    st.session_state.personalized_output
                )
            
            self.output_new_annotator = st.session_state.personalized_output
    
    def _run_caption_mode(self):
        """Run caption creation mode"""
        # Add mode navigation
        self._add_mode_navigation_sidebar("caption")
        
        # Prepare config for caption creation
        caption_config = self.base_config
        caption_config.output_dir = self.output_new_annotator
        
        # Load video data
        video_data_dict = self.data_manager.load_video_data(
            self.base_config.video_data_file, 
            self.base_config.label_collections
        )
        
        # File check
        if "file_check_passed_caption" not in st.session_state:
            if self.video_utils.file_check(st.session_state.video_urls, video_data_dict, self.data_manager):
                st.session_state.file_check_passed_caption = True
            else:
                return
        
        # Create two columns
        page_col1, page_col2 = st.columns([1, 1])
        
        with page_col1:
            self._render_caption_sidebar(video_data_dict, caption_config)
        
        with page_col2:
            self._render_caption_main_interface(video_data_dict, caption_config)
    
    def _run_comparison_mode(self):
        """Run comparison mode"""
        # Add mode navigation
        self._add_mode_navigation_sidebar("comparison")
        
        # Load video data
        video_data_dict = self.data_manager.load_video_data(
            self.base_config.video_data_file, 
            self.base_config.label_collections
        )
        
        # File check
        if "file_check_passed_comparison" not in st.session_state:
            if self.video_utils.file_check(st.session_state.video_urls, video_data_dict, self.data_manager):
                st.session_state.file_check_passed_comparison = True
            else:
                return
        
        # Create two columns
        page_col1, page_col2 = st.columns([1, 1])
        
        with page_col1:
            self._render_comparison_sidebar(video_data_dict)
        
        with page_col2:
            self._render_comparison_main_interface(video_data_dict)
    
    def _render_caption_sidebar(self, video_data_dict: dict, caption_config):
        """Render caption mode sidebar"""
        # Load configs
        try:
            configs = self.data_manager.load_config(self.base_config.configs_file)
            configs = [self.data_manager.load_config(config) for config in configs]
        except FileNotFoundError:
            st.error(f"Config file not found: {self.base_config.configs_file}")
            return
        
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        
        # FIXED: Task selection - Use consistent key naming that matches navigation buttons
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_config",  # CHANGED: Use consistent key name
        )
        
        # FIXED: Handle config changes - Use standard last_config_id
        self._handle_config_change(selected_config)
        
        config = config_dict[selected_config]
        st.markdown(f"### {config.get('name', 'Caption Training')}")
        
        # Get video URLs and output directory
        video_urls = st.session_state.video_urls
        output_dir = str(self.folder_path / self.output_new_annotator / config["output_name"])
        
        # Display instructions
        self._display_instructions(config)

        self.ui.display_status_indicators()
        
        # FIXED: Video selection with training progress indicators - Use consistent key naming
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=self._get_training_video_format_func(output_dir, video_urls),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video"  # CHANGED: Use consistent key name
        )
        
        # FIXED: Handle video changes - Use standard last_video_id and last_selected_video
        video_id = self.data_manager.get_video_id(selected_video)
        self._handle_video_change(video_id, selected_video)
        
        # Display video and related info
        self.video_utils.display_video_with_frames(selected_video)
        self.video_utils.display_video_links(video_id, video_data_dict)
        
        # FIXED: Navigation buttons - Use consistent preserved keys matching main app
        preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
        # Add onboarding-specific keys that should be preserved
        preserved_keys.extend([
            'selected_portal_mode', 'selected_portal_file', 'file_check_passed_caption'
        ])
        
        self.ui.display_navigation_buttons(
            video_urls, config_names, selected_video, selected_config, 
            preserved_keys, self.data_manager
        )
        
        # Store current selections
        st.session_state.current_config_caption = config
        st.session_state.current_config_dict_caption = config_dict
        st.session_state.current_selected_config_caption = selected_config
        st.session_state.current_output_dir_caption = output_dir
        st.session_state.current_video_id_caption = video_id
        st.session_state.current_output_dir = output_dir
        st.session_state.current_selected_video_caption = selected_video
    
    def _get_training_video_format_func(self, output_dir: str, video_urls: List[str]):
        """Format function for video selection dropdown with training progress indicators"""
        def format_func(video_url: str) -> str:
            video_index = video_urls.index(video_url)
            video_id = self.data_manager.get_video_id(video_url)
            video_name = video_url.split("/")[-1]
            
            # Check if caption exists for this video
            if self.data_manager.data_exists(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX):
                emoji = "✅"  # Completed
            else:
                emoji = "📝"  # To do
            
            return f"{emoji}{video_index}. {video_name}"
        
        return format_func
    
    def _render_caption_main_interface(self, video_data_dict: dict, caption_config):
        """Render caption mode main interface"""
        if not hasattr(st.session_state, 'current_config_caption'):
            return
        
        # Session state initialization - consistent with main app
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'precaption_data' not in st.session_state:
            st.session_state.precaption_data = {}
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = {}
        
        # Call the caption interface
        self.caption_interface.render_feedback_interface(
            video_id=st.session_state.current_video_id_caption,
            config=st.session_state.current_config_caption,
            output_dir=st.session_state.current_output_dir_caption,
            caption_program=self.base_config.caption_programs[st.session_state.current_config_caption["task"]],
            video_data_dict=video_data_dict,
            selected_video=st.session_state.current_selected_video_caption,
            args=caption_config,
            selected_config=st.session_state.current_selected_config_caption,
            config_dict=st.session_state.current_config_dict_caption
        )
    
    def _render_comparison_sidebar(self, video_data_dict: dict):
        """Render comparison mode sidebar"""
        # Load configs
        try:
            configs = self.data_manager.load_config(self.base_config.configs_file)
            configs = [self.data_manager.load_config(config) for config in configs]
        except FileNotFoundError:
            st.error(f"Config file not found: {self.base_config.configs_file}")
            return
        
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        
        # FIXED: Task selection - Use consistent key naming that matches navigation buttons  
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_config_review",  # Use unique key to avoid conflicts with caption mode
        )
        
        # FIXED: Handle config changes - Use standard last_config_id
        self._handle_config_change_review(selected_config)
        
        config = config_dict[selected_config]
        st.title(f"Caption Comparison - {config.get('name', '')}")

        self.ui.display_status_indicators()
        
        # Get directories
        video_urls = st.session_state.video_urls
        output_dir = str(self.folder_path / self.base_config.output_dir / config["output_name"])
        new_annotator_output_dir = str(self.folder_path / self.output_new_annotator / config["output_name"])
        
        # FIXED: Video selection with comparison format - Use consistent key naming
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=self._get_comparison_video_format_func(output_dir, new_annotator_output_dir, video_urls),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video_review"  # Use unique key to avoid conflicts with caption mode
        )
        
        # FIXED: Handle video changes - Use standard last_video_id and last_selected_video
        video_id = self.data_manager.get_video_id(selected_video)
        self._handle_video_change_review(video_id, selected_video)
        
        # Display video and related info
        self.video_utils.display_video_with_frames(selected_video)
        self.video_utils.display_video_links(video_id, video_data_dict)
        
        # FIXED: Navigation buttons - Use consistent preserved keys
        preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
        # Add onboarding-specific keys that should be preserved
        preserved_keys.extend([
            'selected_portal_mode', 'selected_portal_file', 'file_check_passed_comparison'
        ])
        
        self.ui.display_navigation_buttons(
            video_urls, config_names, selected_video, selected_config, 
            preserved_keys, self.data_manager
        )
        
        # Store current selections
        st.session_state.current_config_comparison = config
        st.session_state.current_output_dir_comparison = output_dir
        st.session_state.current_new_annotator_output_dir_comparison = new_annotator_output_dir
        st.session_state.current_video_id_comparison = video_id
    
    def _render_comparison_main_interface(self, video_data_dict: dict):
        """Render comparison mode main interface"""
        if not hasattr(st.session_state, 'current_config_comparison'):
            return
        
        with st.container(height=930, border=True):
            video_id = st.session_state.current_video_id_comparison
            output_dir = st.session_state.current_output_dir_comparison
            new_annotator_output_dir = st.session_state.current_new_annotator_output_dir_comparison
            
            status, current_file, new_annotator_file, current_user, new_annotator_user = self._get_comparison_video_status(
                video_id, output_dir, new_annotator_output_dir
            )
            
            if status == "not_done":
                st.warning("⚠️ No ground truth available for this video.")
            elif status == "not_done_by_new_annotator":
                st.info("📝 You haven't created a caption for this video yet. Switch to Caption Mode to create one!")
            else:  # done_by_new_annotator
                self._render_comparison_results(video_id, output_dir, new_annotator_output_dir, 
                                              current_user, new_annotator_user)
    
    def _render_comparison_results(self, video_id: str, output_dir: str, new_annotator_output_dir: str,
                                current_user: str, new_annotator_user: str):
        """Render comparison results"""
        # Load both current and new annotator captions
        current_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        new_annotator_data = self.data_manager.load_data(video_id, new_annotator_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        
        st.subheader("📊 Caption Comparison Results")
        
        # Display metadata information
        current_timestamp = self._format_timestamp(current_data.get("timestamp", "Unknown"))
        new_annotator_timestamp = self._format_timestamp(new_annotator_data.get("timestamp", "Unknown"))
        
        # Create info boxes
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**📚 Ground Truth**\nBy {current_user}\n{current_timestamp}")
        with col2:
            st.success(f"**👤 Your Version**\nBy {new_annotator_user}\n{new_annotator_timestamp}")
        
        # Create tabs for viewing captions
        tab1, tab2, tab3 = st.tabs([
            "📊 Comparison", 
            "📚 Ground Truth", 
            "👤 Your Version"
        ])
        
        with tab1:
            st.subheader("📊 Caption Comparison")
            
            # 1. Pre-caption (always visible)
            st.write("##### Pre-caption")
            st.text(new_annotator_data.get("pre_caption", "No pre-caption available"))
            
            # 2. Your feedback and final caption (expandable)
            your_score = new_annotator_data.get("initial_caption_rating_score", "N/A")
            with st.expander(f"##### 👤 Your Feedback and Caption", expanded=True):
                st.write(f"**Final Feedback ({your_score}/5):**")
                st.text(new_annotator_data.get("final_feedback", "No final feedback available"))
                
                st.write("**Final Caption:**")
                st.text(new_annotator_data.get("final_caption", "No caption available"))
            
            # 3. Ground truth feedback and final caption (expandable) - highlighted
            expert_score = current_data.get("initial_caption_rating_score", "N/A")
            with st.expander(f"🔍 {current_user}'s Feedback and Caption (Expert)", expanded=True):
                st.markdown(f"<span style='color: #51cf66; font-weight: bold;'>Expert's Work</span>", unsafe_allow_html=True)
                st.write(f"**Final Feedback ({expert_score}/5):**")
                st.text(current_data.get("final_feedback", "No final feedback available"))
                
                st.write("**Final Caption:**")
                st.text(current_data.get("final_caption", "No caption available"))
        
        with tab2:
            st.subheader("📚 Ground Truth Version")
            st.markdown("*Expert annotation for reference and learning.*")
            st.write(f"**Expert:** {current_user}")
            st.write(f"**Created:** {self._format_timestamp(current_data.get('timestamp', ''))}")
            self.ui.display_feedback_info(current_data, display_pre_caption_instead_of_final_caption=True)
        
        with tab3:
            st.subheader("👤 Your Version")
            st.markdown("*Your annotation work for comparison.*")
            st.write(f"**Annotator:** {new_annotator_user}")
            st.write(f"**Created:** {self._format_timestamp(new_annotator_data.get('timestamp', ''))}")
            self.ui.display_feedback_info(new_annotator_data, display_pre_caption_instead_of_final_caption=True)

    def _get_comparison_video_status(self, video_id: str, output_dir: str, new_annotator_output_dir: str):
        """Get the status of a video's caption completion for comparison"""
        current_file = self.data_manager.get_filename(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        new_annotator_file = self.data_manager.get_filename(video_id, new_annotator_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        
        if not os.path.exists(current_file):
            return "not_done", None, None, None, None
        elif not os.path.exists(new_annotator_file):
            return "not_done_by_new_annotator", current_file, None, None, None
        else:
            # Load both current and new annotator data to check users
            current_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
            new_annotator_data = self.data_manager.load_data(video_id, new_annotator_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
            
            current_user = current_data.get("user", "Unknown") if current_data else "Unknown"
            new_annotator_user = new_annotator_data.get("user", "Unknown") if new_annotator_data else "Unknown"
            
            return "done_by_new_annotator", current_file, new_annotator_file, current_user, new_annotator_user
    
    def _get_comparison_video_format_func(self, output_dir: str, new_annotator_output_dir: str, video_urls: List[str]):
        """Format function for video selection dropdown with status emojis for comparison mode"""
        def format_func(video_url: str) -> str:
            video_index = video_urls.index(video_url)
            video_id = self.data_manager.get_video_id(video_url)
            status, _, _, _, _ = self._get_comparison_video_status(video_id, output_dir, new_annotator_output_dir)
            
            emoji_map = {
                "not_done": "❓",  # for not completed
                "not_done_by_new_annotator": "⏳",  # hourglass for completed but not by new annotator
                "done_by_new_annotator": "✅"  # for done by new annotator
            }
            
            emoji = emoji_map[status]
            return f"{emoji}{video_index}. {video_url.split('/')[-1]}"
        
        return format_func
    
    def _add_mode_navigation_sidebar(self, current_mode: str):
        """Add consistent mode navigation to sidebar"""
        with st.sidebar:
            if current_mode == "caption":
                st.title("📝 Caption Training")
            else:
                st.title("🔍 Comparison Mode")
                
            st.write(f"**User:** {st.session_state.logged_in_user}")
            user_email = self.auth_manager.get_user_email(st.session_state.logged_in_user)
            if user_email:
                st.write(f"**Email:** {user_email}")
            
            if self.base_config.personalize_output:
                st.write(f"**Your Output:** {self.output_new_annotator}")
            
            st.markdown("---")
            
            # Mode switching
            if current_mode == "caption":
                if st.button("🔄 Switch to Comparison Mode"):
                    st.session_state.selected_portal_mode = "comparison"
                    self._clear_mode_state()
                    st.rerun()
            else:
                if st.button("🔄 Switch to Caption Mode"):
                    st.session_state.selected_portal_mode = "caption"
                    self._clear_mode_state()
                    st.rerun()
            
            if st.button("🏠 Back to Mode Selection"):
                if 'selected_portal_mode' in st.session_state:
                    del st.session_state.selected_portal_mode
                self._clear_mode_state()
                st.rerun()
            
            if st.button("🚪 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    def _clear_mode_state(self):
        """Clear mode-specific state while preserving login and navigation state"""
        from caption.session_state_manager import SessionStateKeyManager
    
        # Get base preserved keys
        preserve_keys = set(SessionStateKeyManager.get_preserved_keys())
        
        # Add onboarding-specific keys that should always be preserved
        preserve_keys.update({
            'selected_portal_file', 'selected_portal_mode', 
            'file_check_passed_caption', 'file_check_passed_comparison'
        })
        
        keys_to_clear = [k for k in st.session_state.keys() if k not in preserve_keys]
        for key in keys_to_clear:
            del st.session_state[key]
    
    def _display_instructions(self, config: dict):
        """Display task instructions"""
        with st.expander("📜 Caption Instructions (Click to Expand/Collapse)", expanded=False):
            if "instruction_file" not in config:
                st.warning("No instruction_file found in the configuration file.")
            else:
                instruction_text = self.ui.load_txt(str(self.folder_path / config["instruction_file"]))
                st.write(instruction_text)
    
    def _format_timestamp(self, iso_timestamp: str) -> str:
        """Format ISO timestamp to a more readable format"""
        try:
            dt = datetime.fromisoformat(iso_timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            return iso_timestamp
    
    # FIXED: Use consistent session state key handling matching main app.py
    def _handle_config_change(self, selected_config: str):
        """Handle configuration changes - unified for both modes"""
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Clear state on config change - use same logic as main app
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
            preserved_keys.extend([
                'selected_config', 'selected_video', 'selected_portal_mode', 
                'selected_portal_file', 'file_check_passed_caption'
            ])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_config_id = selected_config
            print(f"Config changed to: {selected_config}")
            st.rerun()

    def _handle_config_change_review(self, selected_config: str):
        """Handle configuration changes for review mode"""
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Clear state on config change - use same logic as main app
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
            preserved_keys.extend([
                'selected_config_review', 'selected_video_review', 'selected_portal_mode',
                'selected_portal_file', 'file_check_passed_comparison'
            ])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_config_id = selected_config
            print(f"Review config changed to: {selected_config}")
            st.rerun()
    
    def _handle_video_change(self, video_id: str, selected_video: str):
        """Handle video changes - unified for caption mode"""
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            # Clear state on video change - use same logic as main app
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
            preserved_keys.extend([
                'selected_config', 'selected_video', 'last_video_id', 'last_selected_video',
                'selected_portal_mode', 'selected_portal_file', 'file_check_passed_caption'
            ])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
            st.rerun()

    def _handle_video_change_review(self, video_id: str, selected_video: str):
        """Handle video changes for review mode"""
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            # Clear state on video change - use same logic as main app
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
            preserved_keys.extend([
                'selected_config_review', 'selected_video_review', 'last_video_id', 'last_selected_video',
                'selected_portal_mode', 'selected_portal_file', 'file_check_passed_comparison'
            ])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
            st.rerun()


def main():
    """Main entry point"""
    args = parse_args()
    app = OnboardingApp(args.config_type, args.video_urls_files, args.output_new_annotator)
    app.run()


if __name__ == "__main__":
    main()