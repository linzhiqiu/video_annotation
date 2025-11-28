"""
Complete merged utility functions for video caption system.

This module contains all the utility functions, constants, and logic
merged from feedback_app.py and feedback_diff_app.py.
"""

import streamlit as st
import argparse
import os
import torch
import json
import difflib
import html
from diff_match_patch import diff_match_patch
import re
from datetime import datetime
from pathlib import Path
from streamlit_feedback import streamlit_feedback
from streamlit import fragment
import time

# External imports
from caption.utils import extract_frames, load_config, load_json, get_last_frame_index
from llm import get_llm, get_all_llms, get_supported_mode
from caption_policy.prompt_generator import (
    SubjectPolicy, ScenePolicy, SubjectMotionPolicy, 
    SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, 
    RawSpatialPolicy, RawSubjectMotionPolicy
)
from process_json import json_to_video_data

# =============================================================================
# CONSTANTS AND CONFIGURATION
# =============================================================================

# File paths and folder
FOLDER = Path(__file__).parent

# File postfixes
PRECAPTION_FILE_POSTFIX = "_precaption.json"
FEEDBACK_FILE_POSTFIX = "_feedback.json"
PREV_FEEDBACK_FILE_POSTFIX = "_feedback_prev.json"
REVIEWER_FILE_POSTFIX = "_review.json"
PREV_REVIEWER_FILE_POSTFIX = "_review_prev.json"

# UI Constants
PROMPT_HEIGHT = 225
CONTAINER_HEIGHT = 1100

# Caption names
SUBJECT_CAPTION_NAME = "Subject Description Caption"
SCENE_CAPTION_NAME = "Scene Composition and Dynamics Caption"

# Configuration mapping
config_names_to_short_names = {
    "Subject Description Caption": "🧍‍♂️Subject",
    "Scene Composition and Dynamics Caption": "🏞️Scene",
    "Subject Motion and Dynamics Caption": "🏃‍♂️Motion",
    "Spatial Framing and Dynamics Caption": "🗺️Spatial",
    "Camera Framing and Dynamics Caption": "📷Camera",
    "Color Composition and Dynamics Caption (Raw)": "🎨Color",
    "Lighting Setup and Dynamics Caption (Raw)": "💡Lighting",
    "Lighting Effects and Dynamics Caption (Raw)": "🌟Effects",
}

# =============================================================================
# ANNOTATOR MANAGEMENT
# =============================================================================

def load_annotators_from_files(input_dir="annotator"):
    """
    Load annotators from JSON files in the annotators directory.
    
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

def save_annotators_to_files(annotators, output_dir="annotators"):
    """Save annotators to JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to a single file for now
    filepath = os.path.join(output_dir, "annotators.json")
    with open(filepath, 'w') as f:
        json.dump(annotators, f, indent=4)

# Load annotators from files
ANNOTATORS = load_annotators_from_files()

APPROVED_REVIEWERS = [
    "Zhiqiu Lin", "Siyuan Cen", "Yuhan Huang", "Hewei Wang", 
    "Tiffany Ling", "Isaac Li", "Shihang Zhu"
]

# Ensure all approved reviewers are in the ANNOTATORS dictionary
assert set(APPROVED_REVIEWERS) <= set(ANNOTATORS.keys()), \
    f"All approved reviewers must be in the ANNOTATORS dictionary. {APPROVED_REVIEWERS} are not in {ANNOTATORS.keys()}"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def convert_name_to_username(full_name):
    """Convert a full name to a username format (e.g., 'Siyuan Cen' to 'siyuan_cen')"""
    return full_name.lower().replace(" ", "_")

def get_video_id(video_url):
    """Extract video ID from video URL"""
    if video_url.endswith('.mp4'):
        return video_url.split('/')[-1][:-4]  # Remove .mp4 extension
    return video_url

def get_filename(video_id, output_dir, postfix):
    """Get the filename for a video with given postfix"""
    return os.path.join(output_dir, f"{video_id}{postfix}")

def load_data(video_id, output_dir, file_postfix):
    """Load data from JSON file"""
    filename = get_filename(video_id, output_dir, file_postfix)
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def save_data(video_id, data, output_dir, file_postfix):
    """Save data to JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = get_filename(video_id, output_dir, file_postfix)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def data_is_saved(video_id, output_dir, file_postfix):
    """Check if data file exists"""
    filename = get_filename(video_id, output_dir, file_postfix)
    return os.path.exists(filename)

def load_feedback(video_id, output_dir, file_postfix):
    """Load feedback data"""
    return load_data(video_id, output_dir, file_postfix)

def file_check(video_id, output_dir):
    """Check which files exist for a video"""
    files = {}
    for postfix in [FEEDBACK_FILE_POSTFIX, PREV_FEEDBACK_FILE_POSTFIX, REVIEWER_FILE_POSTFIX]:
        files[postfix] = data_is_saved(video_id, output_dir, postfix)
    return files

def format_timestamp(iso_timestamp: str) -> str:
    """Format ISO timestamp to readable format"""
    if not iso_timestamp:
        return 'N/A'
    try:
        return datetime.fromisoformat(iso_timestamp).strftime('%Y-%m-%d')
    except ValueError:
        return 'Invalid date'

def load_video_data(video_data_path, label_collections):
    """Load video data from JSON file"""
    with open(video_data_path, 'r') as f:
        video_data = json.load(f)
    
    video_data_dict = {}
    for video_info in video_data:
        video_url = video_info["video_url"]
        video_id = get_video_id(video_url)
        video_data_dict[video_id] = json_to_video_data(video_info, label_collections)
    
    return video_data_dict

# =============================================================================
# VIDEO STATUS AND MANAGEMENT
# =============================================================================

def get_video_status(video_id, output_dir):
    """Get the status of a video's caption completion and previous iterations"""
    # Initialize all variables
    status = "not_completed"
    current_file = None
    prev_file = None
    current_user = None
    prev_user = None
    
    # Check all relevant files
    feedback_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    prev_feedback_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
    reviewer_file = get_filename(video_id, output_dir, REVIEWER_FILE_POSTFIX)
    
    # Determine status based on file existence and content
    if not os.path.exists(feedback_file):
        return status, current_file, prev_file, current_user, prev_user
        
    current_file = feedback_file
    with open(feedback_file, 'r') as f:
        current_data = json.load(f)
        current_user = current_data.get("user")
    
    if not os.path.exists(reviewer_file):
        status = "completed_not_reviewed"
        return status, current_file, prev_file, current_user, prev_user
    
    # Load reviewer data
    with open(reviewer_file, 'r') as f:
        reviewer_data = json.load(f)
        reviewer_double_check = reviewer_data.get("reviewer_double_check", False)
        
        if reviewer_double_check:
            status = "approved"
            # For approved files, load previous feedback if it exists
            if os.path.exists(prev_feedback_file):
                with open(prev_feedback_file, 'r') as pf:
                    prev_data = json.load(pf)
                    prev_user = prev_data.get("user")
        else:
            status = "rejected"
            # For rejected files, must have prev feedback with different user
            assert os.path.exists(prev_feedback_file), f"Rejected file {video_id} must have previous feedback"
            with open(prev_feedback_file, 'r') as pf:
                prev_data = json.load(pf)
                prev_user = prev_data.get("user")
                with open(feedback_file, 'r') as cf:
                    current_data = json.load(cf)
                    current_user = current_data.get("user")
                    if prev_user == current_user:
                        # This means the caption was just rejected but it has not been updated yet
                        # In this case, we should show the previous version and treat it as not reviewed
                        status = "completed_not_reviewed"
                        prev_user = None
                        prev_file = None
                        return status, current_file, prev_file, current_user, prev_user
        
        prev_file = prev_feedback_file if os.path.exists(prev_feedback_file) else None
    
    return status, current_file, prev_file, current_user, prev_user

def check_video_completion_status(video_urls_file, configs, output_dir):
    """
    Check completion status of videos in a file.
    
    Args:
        video_urls_file: Path to the video URLs file
        configs: List of configs to check
        output_dir: Output directory to check for feedback files
        
    Returns:
        Tuple of (is_completed, is_reviewed) for each video
        Dict of "annotators" and "reviewers" with the number of videos completed and reviewed by each
    """
    video_urls = load_json(FOLDER / video_urls_file)
    status_dict = {}
    annotators_dict = {}
    reviewers_dict = {}
    
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        is_completed = True
        is_reviewed = True
        
        for config in configs:
            config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
            review_file = get_filename(video_id, config_output_dir, REVIEWER_FILE_POSTFIX)
            
            if not os.path.exists(feedback_file):
                is_completed = False
                is_reviewed = False
                break
            else:
                # Check if this annotator completed this task
                with open(feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                    annotator = feedback_data.get("user")
                    if annotator not in annotators_dict:
                        annotators_dict[annotator] = 0
                    annotators_dict[annotator] += 1
                
            if not os.path.exists(review_file):
                is_reviewed = False
            else:
                with open(review_file, 'r') as rf:
                    review_data = json.load(rf)
                    reviewer = review_data.get("reviewer_name")
                    if reviewer not in reviewers_dict:
                        reviewers_dict[reviewer] = 0
                    reviewers_dict[reviewer] += 1
                
        status_dict[video_url] = (is_completed, is_reviewed)
    
    return status_dict, annotators_dict, reviewers_dict

def get_annotator_videos(video_urls_files, annotator_name, configs=None, output_dir=None, not_yet_reviewed=False, show_only_rejected=False):
    """Get all videos that have been completed by an annotator."""
    if configs is None:
        # Use a minimal config check if configs not provided
        configs = []
    
    # Get all video URLs from all files
    all_video_urls = []
    for video_urls_file in video_urls_files:
        try:
            video_urls = load_json(FOLDER / video_urls_file)
            all_video_urls.extend(video_urls)
        except Exception as e:
            print(f"Error loading {video_urls_file}: {e}")
            continue
    
    return all_video_urls  # Simplified for now

def get_video_format_func(output_dir, file_postfix=".json", video_urls=None):
    """Get video format function for display"""
    def format_func(video_url):
        video_id = get_video_id(video_url)
        if file_postfix == ".json":
            return video_url
        else:
            filename = get_filename(video_id, output_dir, file_postfix)
            status = "✅" if os.path.exists(filename) else "❌"
            return f"{status} {video_url}"
    
    return format_func

# =============================================================================
# REVIEWER FUNCTIONS
# =============================================================================

def can_reviewer_redo(video_id, output_dir, current_user):
    """Check if a reviewer can redo their review"""
    # Get video status
    status, current_file, prev_file, current_user_in_file, prev_user = get_video_status(video_id, output_dir)
    
    # If the current user is the same as the user who created the feedback, they can't review it
    if current_user == current_user_in_file:
        return False
    
    # If there's a previous file and the current user is the same as the previous user, they can't review
    if prev_user and current_user == prev_user:
        return False
    
    return True

def copy_to_prev_feedback(video_id, output_dir):
    """Copy current feedback to previous feedback file"""
    current_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    prev_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
    
    if not os.path.exists(current_file):
        print(f"Current feedback file does not exist: {current_file}")
        return
    
    # Check if they're the same to avoid unnecessary copying
    if os.path.exists(prev_file):
        with open(current_file, 'r') as cf, open(prev_file, 'r') as pf:
            current_data = json.load(cf)
            prev_data = json.load(pf)
            if current_data == prev_data:
                print("Current and previous feedback are identical. This indicates the feedback has already been redone.")
                return
    
    # Copy current to prev
    with open(current_file, 'r') as f:
        current_data = json.load(f)
    with open(prev_file, 'w') as f:
        json.dump(current_data, f, indent=4)
    print(f"Copied current feedback to previous feedback: {prev_file}")

def handle_rejection(video_id, output_dir, current_user):
    """Handle the rejection process for a caption"""
    # Copy current feedback to previous
    copy_to_prev_feedback(video_id, output_dir)
    
    # Create reviewer data
    reviewer_data = {
        "reviewer_name": current_user,
        "review_timestamp": datetime.now().isoformat(),
        "reviewer_double_check": False
    }
    save_data(video_id, reviewer_data, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
    st.rerun()

# =============================================================================
# PRECAPTION GENERATION
# =============================================================================

def generate_precaption(video_id, config, output_dir, caption_program, video_data_dict, selected_video, args):
    """Generate pre-caption for a video"""
    try:
        # Get video data
        if video_id not in video_data_dict:
            st.error(f"Video data not found for {video_id}")
            return None
        
        video_data = video_data_dict[video_id]
        
        # Generate caption using the caption program
        caption_dict = caption_program(video_data)
        
        # Get the specific caption for this config's task
        task_name = config.get("task")
        pre_caption = caption_dict.get(task_name, "")
        
        if not pre_caption:
            st.error(f"No pre-caption generated for task: {task_name}")
            return None
        
        # Save pre-caption data
        pre_caption_data = {
            "video_id": video_id,
            "pre_caption": pre_caption,
            "task": task_name,
            "timestamp": datetime.now().isoformat()
        }
        
        save_data(video_id, pre_caption_data, output_dir=output_dir, file_postfix=PRECAPTION_FILE_POSTFIX)
        print(f"Pre-caption generated for video: {video_id}")
        return pre_caption
        
    except Exception as e:
        st.error(f"Error generating pre-caption: {e}")
        return None

# =============================================================================
# FEEDBACK PROCESSING FUNCTIONS
# =============================================================================

def copy_feedback_for_precaption(configs_path, video_urls, main_project_output, personalized_output):
    """
    Copy feedback files from main project to personalized output as precaption files.
    
    Args:
        configs_path: Path to configs file
        video_urls: List of video URLs to process
        main_project_output: Path to main project output directory
        personalized_output: Path to personalized output directory
    """
    # Create personalized output directory if it doesn't exist
    os.makedirs(personalized_output, exist_ok=True)
    
    # Process each video
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        
        # For each config in the main project
        configs = load_config(FOLDER / configs_path)
        configs = [load_config(FOLDER / config) for config in configs]
        
        for config in configs:
            # Get the output directory for this config
            config_output_dir = os.path.join(FOLDER, main_project_output, config["output_name"])
            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
            
            # If feedback exists in main project, check if precaption already exists
            if os.path.exists(feedback_file):
                # Create config directory in personalized output
                personalized_config_dir = os.path.join(FOLDER, personalized_output, config["output_name"])
                os.makedirs(personalized_config_dir, exist_ok=True)
                
                # Check if precaption file already exists
                precaption_file = get_filename(video_id, personalized_config_dir, PRECAPTION_FILE_POSTFIX)
                if not os.path.exists(precaption_file):
                    # Only copy if precaption doesn't exist
                    with open(feedback_file, 'r') as src, open(precaption_file, 'w') as dst:
                        dst.write(src.read())
                    print(f"Copied {feedback_file} to {precaption_file}")
                else:
                    print(f"Skipped copying {feedback_file} as {precaption_file} already exists")
            else:
                print(f"Skipped copying {feedback_file} as it doesn't exist")

# =============================================================================
# TEXT PROCESSING AND DIFFERENCE FUNCTIONS
# =============================================================================

def split_into_words(text):
    """Split text into words while preserving spaces"""
    if not text:
        return []
    
    words = []
    current_word = ""
    
    for char in text:
        if char.isspace():
            if current_word:
                words.append(current_word)
                current_word = ""
            words.append(char)
        else:
            current_word += char
    
    if current_word:
        words.append(current_word)
    
    return words

def highlight_differences(text1, text2):
    """Highlight differences between two texts"""
    words1 = split_into_words(text1)
    words2 = split_into_words(text2)
    
    diff = difflib.SequenceMatcher(None, words1, words2)
    
    result1 = []
    result2 = []
    
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag == 'equal':
            result1.extend(words1[i1:i2])
            result2.extend(words2[j1:j2])
        elif tag == 'delete':
            for word in words1[i1:i2]:
                if word.isspace():
                    result1.append(word)
                else:
                    result1.append(f'<span style="background-color: #ffcccc">{html.escape(word)}</span>')
        elif tag == 'insert':
            for word in words2[j1:j2]:
                if word.isspace():
                    result2.append(word)
                else:
                    result2.append(f'<span style="background-color: #ccffcc">{html.escape(word)}</span>')
        elif tag == 'replace':
            for word in words1[i1:i2]:
                if word.isspace():
                    result1.append(word)
                else:
                    result1.append(f'<span style="background-color: #ffcccc">{html.escape(word)}</span>')
            for word in words2[j1:j2]:
                if word.isspace():
                    result2.append(word)
                else:
                    result2.append(f'<span style="background-color: #ccffcc">{html.escape(word)}</span>')
    
    return ''.join(result1), ''.join(result2)

# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_status_indicators():
    """Display an expander explaining the status indicators used in the video selection dropdown."""
    with st.expander("📊 Status Indicators Legend", expanded=False):
        st.markdown("""
        **Status Indicators:**
        - ✅ = Video completed (all caption tasks finished)
        - ✅✅ = Video completed and reviewed (approved)
        - ❌ = Video rejected (needs revision)
        - (blank) = Video not completed yet
        """)

def display_feedback_info(feedback_data, display_pre_caption_instead_of_final_caption=False):
    """Display feedback information including scores, GPT feedback, and caption differences."""
    if not feedback_data:
        st.write("No feedback data available.")
        return
    
    # Display pre-caption
    if "pre_caption" in feedback_data:
        st.write("##### Pre-caption")
        st.text(feedback_data["pre_caption"])
    
    # Display feedback workflow if it exists
    if feedback_data.get("feedback_is_needed", False):
        st.write("##### Feedback Workflow")
        
        # Initial feedback
        if "initial_feedback" in feedback_data:
            st.write("**Initial Feedback:**")
            st.text(feedback_data["initial_feedback"])
        
        # GPT feedback
        if "gpt_feedback" in feedback_data:
            st.write("**GPT Polished Feedback:**")
            st.text(feedback_data["gpt_feedback"])
        
        # Final feedback
        if "final_feedback" in feedback_data:
            st.write("**Final Feedback:**")
            st.text(feedback_data["final_feedback"])
        
        # Feedback rating
        if "feedback_rating_score" in feedback_data:
            st.write(f"**Feedback Rating:** {feedback_data['feedback_rating_score']}/5")
        
        # GPT caption
        if "gpt_caption" in feedback_data:
            st.write("**GPT Generated Caption:**")
            st.text(feedback_data["gpt_caption"])
        
        # Caption rating
        if "caption_rating_score" in feedback_data:
            st.write(f"**Caption Rating:** {feedback_data['caption_rating_score']}/5")
    
    # Display final caption
    caption_to_display = feedback_data.get("pre_caption" if display_pre_caption_instead_of_final_caption else "final_caption", "")
    st.write("##### Final Caption")
    st.text(caption_to_display)

def display_feedback_differences(prev_feedback, feedback_data, diff_prompt, reviewer_data):
    """Display differences between previous and current feedback"""
    
    if not prev_feedback or not feedback_data:
        st.write("Cannot display differences - missing feedback data")
        return
    
    prev_feedback_text = prev_feedback.get("final_feedback", "")
    current_feedback_text = feedback_data.get("final_feedback", "")
    
    if prev_feedback_text and current_feedback_text:
        st.write("**Feedback Differences:**")
        
        # Highlight differences
        prev_highlighted, current_highlighted = highlight_differences(prev_feedback_text, current_feedback_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Previous (Rejected):**")
            st.markdown(prev_highlighted, unsafe_allow_html=True)
        
        with col2:
            st.write("**Current (Reviewer's):**")
            st.markdown(current_highlighted, unsafe_allow_html=True)

def display_caption_differences(prev_feedback, feedback_data, diff_cap_prompt, reviewer_data):
    """Display differences between previous and current captions"""
    
    if not prev_feedback or not feedback_data:
        st.write("Cannot display differences - missing feedback data")
        return
    
    prev_caption = prev_feedback.get("final_caption", "")
    current_caption = feedback_data.get("final_caption", "")
    
    if prev_caption and current_caption:
        st.write("**Caption Differences:**")
        
        # Highlight differences
        prev_highlighted, current_highlighted = highlight_differences(prev_caption, current_caption)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Previous (Rejected):**")
            st.markdown(prev_highlighted, unsafe_allow_html=True)
        
        with col2:
            st.write("**Current (Reviewer's):**")
            st.markdown(current_highlighted, unsafe_allow_html=True)

def display_caption_expander(data, user, timestamp):
    """Helper function to display caption information in an expander"""
    st.write("##### Annotator")
    st.write(f"**Annotator:** {user}")
    st.write(f"**Timestamp:** {format_timestamp(timestamp)}")
    st.write("##### Pre-caption")
    st.text(data.get("pre_caption", "No pre-caption available"))
    
    # Use the existing display_feedback_info function
    display_feedback_info(data, display_pre_caption_instead_of_final_caption=False)

# =============================================================================
# STATISTICS AND ACCURACY FUNCTIONS
# =============================================================================

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
            continue
            
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
    
    # Calculate accuracy percentages
    for annotator in stats:
        if stats[annotator]['total_reviewed'] > 0:
            stats[annotator]['accuracy'] = (
                stats[annotator]['approved'] / stats[annotator]['total_reviewed'] * 100
            )
    
    return stats

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
            return
        
        # Display statistics
        for config_name, stats in all_stats.items():
            st.write(f"**{config_name}:**")
            
            for annotator, data in stats.items():
                accuracy_str = f"{data['accuracy']:.1f}%" if data['total_reviewed'] > 0 else "No reviews yet"
                st.write(f"  - {annotator}: {data['approved']}/{data['total_reviewed']} approved ({accuracy_str})")

# =============================================================================
# MAIN FEEDBACK INTERFACE
# =============================================================================

def feedback_interface(video_id, config, output_dir, caption_program, video_data_dict, selected_video, args, selected_config, config_dict):
    """Main feedback interface for caption annotation"""
    with st.container(height=CONTAINER_HEIGHT, border=True):
        # Step 0: Generating Pre-caption
        if st.session_state.current_step == 0:
            # If feedback already exists, load it
            if data_is_saved(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
                feedback_data = load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                current_user = st.session_state.logged_in_user
                # Display detailed feedback information in an expander
                is_approved_reviewer = current_user in APPROVED_REVIEWERS
                with st.expander("Reviewer: Please Review Caption Here", expanded=is_approved_reviewer):
                    display_feedback_info(feedback_data, display_pre_caption_instead_of_final_caption=True)
                    # Reviewer interface
                    reviewer_data = load_data(video_id, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                    current_user = st.session_state.logged_in_user
                    
                    if not is_approved_reviewer:
                        st.write("##### Reviewer Status")
                        st.write(f"You are **{current_user}**. You are not an approved reviewer.")
                    else:
                        if reviewer_data is None:
                            st.write("##### Reviewer Status")
                            st.write(f"You are **{current_user}**. You can review (double check) this caption.")
                            if not can_reviewer_redo(video_id, output_dir, current_user):
                                st.error("You cannot review this caption because you are the annotator.")
                                return
                            
                            # Reviewer actions
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Approve Caption", type="primary"):
                                    reviewer_data = {
                                        "reviewer_name": current_user,
                                        "review_timestamp": datetime.now().isoformat(),
                                        "reviewer_double_check": True
                                    }
                                    save_data(video_id, reviewer_data, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                                    st.success("Caption approved!")
                                    st.rerun()
                            
                            with col2:
                                if st.button("❌ Reject Caption", type="secondary"):
                                    handle_rejection(video_id, output_dir, current_user)
                        else:
                            # Already reviewed
                            reviewer_double_check = reviewer_data.get("reviewer_double_check", False)
                            if reviewer_double_check:
                                st.success("✅ This caption has been approved!")
                            else:
                                st.error("❌ This caption has been rejected.")
            else:
                # Generate pre-caption
                st.write("Generating pre-caption...")
                pre_caption = generate_precaption(video_id, config, output_dir, caption_program, video_data_dict, selected_video, args)
                if pre_caption:
                    st.success("Pre-caption generated successfully!")
                    st.text(pre_caption)