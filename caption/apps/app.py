# caption/apps/app.py
import streamlit as st
import argparse
from pathlib import Path

from caption.config import get_config

from caption.interfaces.review_interface import ReviewInterface
from caption.interfaces.caption_interface import CaptionInterface

from caption.core.auth import AuthManager
from caption.core.data_manager import DataManager  
from caption.core.video_utils import VideoUtils
from caption.core.ui_components import UIComponents
from caption.core.caption_engine import CaptionEngine

from caption.session_state_manager import SessionStateKeyManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Video Caption and Review System")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    return parser.parse_args()


class VideoAnnotationApp:
    """Main video annotation application"""
    
    def __init__(self, config_type: str):
        self.app_config = get_config(config_type)
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
            page_title=self.app_config.name,
            page_icon="🎥",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Check authentication
        if not self.auth_manager.is_logged_in():
            self.auth_manager.show_login_page(self.app_config)
            return
        
        # Handle personalized output if enabled
        self._setup_personalized_output()
        
        # Check portal selection
        if "selected_portal" not in st.session_state:
            self.ui.display_portal_selection()
            return
        
        # Route to appropriate portal
        if st.session_state.selected_portal == "caption":
            self._run_caption_portal()
        elif st.session_state.selected_portal == "review":
            self._run_review_portal()
        else:
            st.error("Invalid portal selection")
            if 'selected_portal' in st.session_state:
                del st.session_state.selected_portal
            st.rerun()
    
    def _setup_personalized_output(self):
        """Setup personalized output directory if enabled"""
        if self.app_config.personalize_output and "logged_in_user" in st.session_state:
            if "personalized_output" not in st.session_state:
                username = self.video_utils.convert_name_to_username(st.session_state.logged_in_user)
                st.session_state.personalized_output = f"{self.app_config.output_dir}_{username}"
                print(f"Personalized output directory: {st.session_state.personalized_output}")
                
                # Copy feedback files from main project for precaption
                self.caption_engine.copy_feedback_for_precaption(
                    self.app_config.configs_file,
                    st.session_state.video_urls,
                    self.app_config.main_project_output,
                    st.session_state.personalized_output
                )
            
            # Update the config to use personalized output
            self.app_config.output_dir = st.session_state.personalized_output
    
    def _run_caption_portal(self):
        """Run caption creation portal"""
        # Add portal navigation
        self.ui.add_portal_navigation_sidebar("caption", self.app_config)
        
        # Load video data
        video_data_dict = self.data_manager.load_video_data(
            self.app_config.video_data_file, 
            self.app_config.label_collections
        )
        
        # File check - using consistent key naming
        if "file_check_passed" not in st.session_state:
            if self.video_utils.file_check(st.session_state.video_urls, video_data_dict, self.data_manager):
                st.session_state.file_check_passed = True
            else:
                return
        
        # Create two columns
        page_col1, page_col2 = st.columns([1, 1])
        
        with page_col1:
            self._render_caption_sidebar(video_data_dict)
        
        with page_col2:
            self._render_caption_main_interface(video_data_dict)
    
    def _run_review_portal(self):
        """Run review portal"""
        # Add portal navigation
        self.ui.add_portal_navigation_sidebar("review", self.app_config)
        
        # Load video data
        video_data_dict = self.data_manager.load_video_data(
            self.app_config.video_data_file, 
            self.app_config.label_collections
        )
        
        # File check - using consistent key naming
        if "file_check_passed" not in st.session_state:
            if self.video_utils.file_check(st.session_state.video_urls, video_data_dict, self.data_manager):
                st.session_state.file_check_passed = True
            else:
                return
        
        # Create two columns
        page_col1, page_col2 = st.columns([1, 1])
        
        with page_col1:
            self._render_review_sidebar(video_data_dict)
        
        with page_col2:
            self._render_review_main_interface(video_data_dict)
    
    def _render_caption_sidebar(self, video_data_dict: dict):
        """Render caption portal sidebar"""
        # Load configs
        try:
            configs = self.data_manager.load_config(self.app_config.configs_file)
            configs = [self.data_manager.load_config(config) for config in configs]
        except FileNotFoundError:
            st.error(f"Config file not found: {self.app_config.configs_file}")
            return
        
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        
        # Task selection - using consistent key naming
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_config",  # Changed from "selected_task" to match original
        )
        
        # Handle config changes
        self._handle_config_change(selected_config, config_names)
        
        config = config_dict[selected_config]
        st.markdown(f"### {config.get('name', 'Pre-Caption System')}")
        
        # Get video URLs from session state
        video_urls = st.session_state.video_urls
        output_dir = str(self.folder_path / self.app_config.output_dir / config["output_name"])
        
        # Display instructions and status indicators
        self._display_instructions_and_status(config)
        
        # Video selection - using consistent key naming
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=self.video_utils.get_video_format_func(output_dir, video_urls, self.data_manager),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video"  # Consistent key naming
        )
        
        # Handle video changes
        video_id = self.data_manager.get_video_id(selected_video)
        self._handle_video_change(video_id, selected_video)
        
        # Display video and related info
        self.video_utils.display_video_with_frames(selected_video, use_custom_player=True)
        self.video_utils.display_video_links(video_id, video_data_dict)
        
        # Add user options and debug information to sidebar (matching original)
        with st.sidebar:
            st.title("User Options")
            st.write(f"Logged in as: **{st.session_state.logged_in_user}**")
            user_email = self.auth_manager.get_user_email(st.session_state.logged_in_user)
            if user_email:
                st.write(f"Email: **{user_email}**")
            
            if hasattr(self.app_config, 'output_dir') and self.app_config.personalize_output:
                st.write(f"**Output Directory:** {self.app_config.output_dir}")
            
            if st.button("Logout"):
                # Clear session state and logout
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            # Debug information (matching original)
            st.header("Debug Information")
            st.write("Full Session State:")
            for key, value in st.session_state.items():
                st.write(f"{key}: {value}")
        
        # Navigation buttons - consistent preserved keys
        # preserved_keys = [
        #     'api_key', 'last_config_id', 'selected_config',
        #     'last_video_id', 'last_selected_video', 'personalized_output',
        #     'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user',
        #     'selected_portal', 'login_method', 'target_annotator', 'selected_sheet_file'
        # ]
        preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
        
        self.ui.display_navigation_buttons(
            video_urls, config_names, selected_video, selected_config, 
            preserved_keys, self.data_manager
        )
        
        # Store current selections in session state
        st.session_state.current_config = config
        st.session_state.current_config_dict = config_dict
        st.session_state.current_selected_config = selected_config
        st.session_state.current_output_dir = output_dir
        st.session_state.current_video_id = video_id
        st.session_state.current_selected_video = selected_video
    
    def _render_caption_main_interface(self, video_data_dict: dict):
        """Render caption portal main interface"""
        if not hasattr(st.session_state, 'current_config'):
            return
        
        # Session state initialization - consistent with original logic
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'precaption_data' not in st.session_state:
            st.session_state.precaption_data = {}
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = {}
        
        # Call the caption interface
        self.caption_interface.render_feedback_interface(
            video_id=st.session_state.current_video_id,
            config=st.session_state.current_config,
            output_dir=st.session_state.current_output_dir,
            caption_program=self.app_config.caption_programs[st.session_state.current_config["task"]],
            video_data_dict=video_data_dict,
            selected_video=st.session_state.current_selected_video,
            args=self.app_config,
            selected_config=st.session_state.current_selected_config,
            config_dict=st.session_state.current_config_dict
        )
    
    def _render_review_sidebar(self, video_data_dict: dict):
        """Render review portal sidebar"""
        # Load configs
        try:
            configs = self.data_manager.load_config(self.app_config.configs_file)
            configs = [self.data_manager.load_config(config) for config in configs]
        except FileNotFoundError:
            st.error(f"Config file not found: {self.app_config.configs_file}")
            return
        
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        
        # Task selection - using consistent key naming for review
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_config_review",  # Different key for review to avoid conflicts
        )
        
        # Handle config changes for review
        self._handle_config_change_review(selected_config, config_names)
        
        config = config_dict[selected_config]
        st.markdown(f"### {config.get('name', '')}")
        
        # Get video URLs from session state
        video_urls = st.session_state.video_urls
        output_dir = str(self.folder_path / self.app_config.output_dir / config["output_name"])
        
        # Display status indicators and accuracy statistics
        self.ui.display_status_indicators()
        self.review_interface.display_accuracy_statistics(
            config_names, config_dict, video_urls, str(self.folder_path / self.app_config.output_dir)
        )
        
        # Video selection - using consistent key naming for review
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=self.video_utils.get_video_format_func(output_dir, video_urls, self.data_manager),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video_review"  # Different key for review to avoid conflicts
        )
        
        # Handle video changes for review
        video_id = self.data_manager.get_video_id(selected_video)
        self._handle_video_change_review(video_id, selected_video)
        
        # Display video and related info
        self.video_utils.display_video_with_frames(selected_video)
        self.video_utils.display_video_links(video_id, video_data_dict)
        
        # Navigation buttons for review - consistent preserved keys
        # preserved_keys = [
        #     'api_key', 'last_config_id', 'selected_config_review',
        #     'last_video_id', 'last_selected_video', 
        #     'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 
        #     'personalized_output', 'selected_portal', 'login_method', 'target_annotator'
        # ]
        preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
        
        self.ui.display_navigation_buttons(
            video_urls, config_names, selected_video, selected_config, 
            preserved_keys, self.data_manager
        )
        
        # Store current selections for review
        st.session_state.current_config_review = config
        st.session_state.current_output_dir_review = output_dir
        st.session_state.current_video_id_review = video_id
    
    def _render_review_main_interface(self, video_data_dict: dict):
        """Render review portal main interface"""
        if not hasattr(st.session_state, 'current_config_review'):
            return
        
        # Call the review interface
        self.review_interface.render_review_interface(
            video_id=st.session_state.current_video_id_review,
            config=st.session_state.current_config_review,
            output_dir=st.session_state.current_output_dir_review,
            args=self.app_config
        )
    
    def _handle_config_change(self, selected_config: str, config_names: list):
        """Handle configuration changes"""
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Clear state on config change - preserve more keys to maintain consistency
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
            preserved_keys.extend(['selected_config', 'selected_video'])  # Add config-specific keys
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            # keys_to_remove = [key for key in st.session_state 
            #                  if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 
            #                               'video_urls', 'last_video_id', 'last_selected_video', 'logged_in_user', 
            #                               'personalized_output', 'selected_portal', 'login_method', 'target_annotator',
            #                               'selected_config', 'selected_video']]  # Keep these consistent
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_config_id = selected_config
            print(f"Config changed to: {selected_config}")
            st.rerun()
    
    def _handle_config_change_review(self, selected_config: str, config_names: list):
        """Handle configuration changes for review"""
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Clear state on config change - use same logic as caption mode for consistency
            # keys_to_remove = [key for key in st.session_state 
            #                  if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 
            #                               'video_urls', 'last_video_id', 'last_selected_video', 'logged_in_user', 
            #                               'personalized_output', 'selected_portal', 'login_method', 'target_annotator',
            #                               'selected_config_review', 'selected_video_review']]
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
            preserved_keys.extend(['selected_config_review', 'selected_video_review'])  # Add review-specific keys
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_config_id = selected_config
            print(f"Review config changed to: {selected_config}")
            st.rerun()
    
    def _handle_video_change(self, video_id: str, selected_video: str):
        """Handle video changes"""
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_caption_portal()
            # Add video-change specific keys that should be preserved
            preserved_keys.extend(['selected_config', 'selected_video', 'last_video_id', 'last_selected_video'])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
        
            # Clear state on video change - preserve more keys for consistency
            # keys_to_remove = [key for key in st.session_state 
            #                  if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 
            #                               'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls', 
            #                               'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 
            #                               'target_annotator', 'selected_video']]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
            st.rerun()
    
    def _handle_video_change_review(self, video_id: str, selected_video: str):
        """Handle video changes for review"""
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            # Clear state on video change - use same logic as caption mode for consistency
            from caption.session_state_manager import SessionStateKeyManager
            preserved_keys = SessionStateKeyManager.get_preserved_keys_for_review_portal()
            # Add review video-change specific keys that should be preserved
            preserved_keys.extend(['selected_config_review', 'selected_video_review', 'last_video_id', 'last_selected_video'])
            
            keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
        
            # keys_to_remove = [key for key in st.session_state 
            #                  if key not in ['api_key', 'last_config_id', 'selected_config_review', 'last_video_id', 
            #                               'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls', 
            #                               'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 
            #                               'target_annotator', 'selected_video_review']]
            for key in keys_to_remove:
                del st.session_state[key]
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
            st.rerun()
    
    def _display_instructions_and_status(self, config: dict):
        """Display instructions and status indicators"""
        # Display instructions
        with st.expander("📜 Caption Instructions (Click to Expand/Collapse)", expanded=False):
            if "instruction_file" not in config:
                st.warning("No instruction_file found in the configuration file.")
            else:
                instruction_text = self.ui.load_txt(str(self.folder_path / config["instruction_file"]))
                st.write(instruction_text)
        
        # Display status indicators explanation
        self.ui.display_status_indicators()


def main():
    """Main entry point"""
    args = parse_args()
    app = VideoAnnotationApp(args.config_type)
    app.run()


if __name__ == "__main__":
    main()