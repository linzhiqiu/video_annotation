# caption/core/video_utils.py
import streamlit as st
import os
from typing import Dict, Any, List, Callable
from datetime import datetime

from caption.utils import extract_frames, get_last_frame_index
from caption.video_player import custom_video_player

class VideoUtils:
    """Utility functions for video handling and display"""
    
    @staticmethod
    def get_imagery_kwargs(selected_mode: str, selected_video: str) -> Dict[str, Any]:
        """Get imagery kwargs based on selected mode"""
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
    
    @staticmethod
    def display_video_with_frames(selected_video: str, expanded: bool = False, use_custom_player: bool = True):
        """Display video with expandable frame viewer"""
        # Display video - try custom player first, fallback to regular
        if use_custom_player:
            try:
                custom_video_player(selected_video)
            except ImportError:
                # Fallback to regular video if custom_video_player is not available
                st.video(selected_video)
        else:
            st.video(selected_video)

        # # Display first and last frames
        # extracted_frames = extract_frames(selected_video, [0, -1])
        # # Expandable section
        # with st.expander("Frames (Click to Expand/Collapse)", expanded=expanded):
        #     col1, col2 = st.columns(2)
        #     with col1:
        #         st.image(extracted_frames[0], caption="First Frame")
        #     with col2:
        #         st.image(extracted_frames[1], caption="Last Frame")
    
    @staticmethod
    def display_video_links(video_id: str, video_data_dict: Dict[str, Any]):
        """Display video-related links"""
        with st.expander("Show Links", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.link_button("🔗 Cam-Motion", f"https://camerapizza.a.pinggy.link/?video_uid={video_id}")
                    
            with col2:
                st.link_button("🔗 Cam-Setup", f"https://camerapizza.a.pinggy.link/?video_uid={video_id}")
                    
            with col3:
                st.link_button("🔗 Lighting-Setup", f"https://lightpizza.a.pinggy.link/?video_uid={video_id}")
            
            st.link_button("🔗 Report Label Errors Here", 
                          "https://docs.google.com/spreadsheets/d/1sAYL86ERcaC_vrVuloXxtPJXKzeuj8fukHtNv6nRCJ0/edit?usp=sharing")
    
    @staticmethod
    def get_video_format_func(output_dir: str, video_urls: List[str] = None, data_manager=None) -> Callable[[str], str]:
        """Create a format function for video selection dropdown with status emojis"""
        def format_func(video_url: str) -> str:
            if video_urls is not None:
                video_index = video_urls.index(video_url)
            else:
                video_index = ""
            
            video_id = data_manager.get_video_id(video_url) if data_manager else video_url.split('/')[-1]
            video_name = video_url.split("/")[-1]
            
            # Get status and format accordingly
            if data_manager:
                status, current_file, _, _, _ = data_manager.get_video_status(video_id, output_dir)
            else:
                status = "not_completed"
            
            status_emoji_map = {
                "not_completed": "",  # Not completed - no emoji
                "completed_not_reviewed": "✅",  # Completed but not reviewed - single checkmark
                "approved": "✅✅",  # Approved - double checkmark
                "rejected": "❌"  # Rejected
            }
            
            # Get timestamps if available
            timestamp_str = ""
            if status != "not_completed" and data_manager:
                if current_file:
                    with open(current_file, 'r') as f:
                        import json
                        current_data = json.load(f)
                        if status == "completed_not_reviewed":
                            timestamp_str = f" (completed at {data_manager.format_timestamp(current_data.get('timestamp', 'N/A'))})"
                        elif status == "approved" or status == "rejected":
                            reviewer_file = data_manager.get_filename(video_id, output_dir, data_manager.REVIEWER_FILE_POSTFIX)
                            if os.path.exists(reviewer_file):
                                with open(reviewer_file, 'r') as rf:
                                    reviewer_data = json.load(rf)
                                    timestamp_str = f" (reviewed at {data_manager.format_timestamp(reviewer_data.get('review_timestamp', 'N/A'))})"
            
            return f"{status_emoji_map[status]}{video_index}. {video_name}{timestamp_str}"
        
        return format_func
    
    @staticmethod
    def file_check(video_urls: List[str], video_data_dict: Dict[str, Any], data_manager):
        """Check if all videos in the list exist in the video data dictionary"""
        video_ids = [data_manager.get_video_id(video_url) for video_url in video_urls]
        missing_video = False
        for video_id in video_ids:
            if video_id not in video_data_dict:
                st.error(f"Video ID {video_id} not found in the video data file.")
                print(f"Video ID not found: {video_id}")
                missing_video = True
        if missing_video:
            return False
        return True
    
    @staticmethod
    def convert_name_to_username(full_name: str) -> str:
        """Convert a full name to a username format (e.g., 'Siyuan Cen' to 'siyuan_cen')"""
        return full_name.lower().replace(" ", "_")