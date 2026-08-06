# caption/test_critique_generation.py
import streamlit as st
import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from caption.config import get_config
from caption.core.data_manager import DataManager  
from caption.core.video_utils import VideoUtils
from caption.core.ui_components import UIComponents

from llm import get_llm, get_all_llms
from caption_policy.prompt_generator import (
    SubjectPolicy, ScenePolicy, SubjectMotionPolicy, 
    SpatialPolicy, CameraPolicy
)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Critique Generation Testing Interface")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    return parser.parse_args()


class CritiqueGenerationApp:
    """Critique generation testing application"""
    
    def __init__(self, config_type: str):
        self.app_config = get_config(config_type)
        self.folder_path = Path(__file__).parent  # caption/ directory  
        self.root_path = self.folder_path.parent  # Go up to project root
        
        # Initialize core components
        self.data_manager = DataManager(self.folder_path, self.root_path)
        self.video_utils = VideoUtils()
        self.ui = UIComponents()
        
        # Initialize caption programs for getting caption instructions - MOVED UP  
        self.caption_programs = {
            "subject_description": SubjectPolicy(),
            "scene_composition_dynamics": ScenePolicy(),
            "subject_motion_dynamics": SubjectMotionPolicy(),
            "spatial_framing_dynamics": SpatialPolicy(),
            "camera_framing_dynamics": CameraPolicy(),
        }
        
        # Define critique generation tasks
        self.critique_tasks = {
            "insertion_error_critique_generation": {
                "name": "Insertion Error Critique Generation",
                "description": "Add one extra irrelevant or incorrect detail to the original critique",
                "default_llm": "gpt-4.1-2025-04-14",
                "supports_video": False
            },
            "replacement_error_critique_generation": {
                "name": "Replacement Error Critique Generation", 
                "description": "Replace one correct detail with wrong or misleading information",
                "default_llm": "gpt-4.1-2025-04-14",
                "supports_video": False
            },
            "deletion_error_critique_generation": {
                "name": "Deletion Error Critique Generation",
                "description": "Remove one important detail to make the critique incomplete",
                "default_llm": "gpt-4.1-2025-04-14",
                "supports_video": False
            },
            "nonconstructive_critique_generation": {
                "name": "Non-Constructive Critique Generation",
                "description": "Remove constructive suggestions, leaving only criticisms",
                "default_llm": "gemini-2.5-pro",
                "supports_video": False
            },
            "gemini_critique_generation": {
                "name": "Gemini Critique Generation",
                "description": "Generate critique directly using Gemini with video access",
                "default_llm": "gemini-2.5-pro",
                "supports_video": True
            },
            "blind_gemini_critique_generation": {
                "name": "Blind Gemini Critique Generation",
                "description": "Generate critique using Gemini without video access (hallucinated)",
                "default_llm": "gemini-2.5-pro",
                "supports_video": False
            },
            "worst_caption_generation": {
                "name": "Worst Caption Generation",
                "description": "Generate completely new incorrect caption (no critique/revision)",
                "default_llm": "gpt-4.1-2025-04-14",
                "supports_video": False
            }
        }
        
        # Define prompt templates
        self.prompt_templates = {
            "insertion_error_critique_generation": """Please modify the following feedback by adding one extra irrelevant or incorrect detail that was not present in the original critique.

Caption Instruction:
{caption_instruction}

Original Caption: {caption}

Original Feedback: {feedback}

Instructions:
1. Insert one additional detail at a random position in the critique that is either irrelevant to the caption task or factually incorrect about the caption
2. Make the addition feel natural and integrated with the original feedback. Inserted feedback should provide concrete details related to the caption instruction, not unrelated visual content or vague suggestions (e.g., asking to mention aspects without specifying what they are)
3. If the original feedback is empty, add one detail that is not include in the original caption and it's incorrect about what's shown.
4. Return only the modified feedback paragraph without any additional text or explanations
5. Avoid repeating any content from the original caption
6. Do not include non-visual elements (e.g., background music, narration)
7. Provide explicit information, not ambiguous details
8. Please try to use affirmative sentence rather than negative or interrogative one
9. Please do not delete the original feedback content, only insert
10. Do not use negative statement (e.g., 'there is no …' or 'avoid mentioning ...') in your inserted feedback""",

            "replacement_error_critique_generation": """Please modify the following feedback by replacing one correct detail with wrong or misleading information.

Caption Instruction:
{caption_instruction}

Original Caption: {caption}

Original Feedback: {feedback}

Instructions:
1. Identify one factual detail or suggestion in the original feedback
2. Replace this detail with an incorrect alternative that sounds plausible but is wrong
3. Keep the overall structure and tone of the original feedback
4. Return only the modified feedback paragraph without any additional text or explanations
5. Avoid repeating any content from the original caption
6. Do not include non-visual elements (e.g., background music, narration)
7. Provide explicit information, not ambiguous details
8. If the feedback includes phrases such as 'not xxx', please keep them, as they indicate errors in the original caption""",

            "deletion_error_critique_generation": """Please modify the following feedback by removing one important detail to make it incomplete.

Caption Instruction:
{caption_instruction}

Original Caption: {caption}

Original Feedback: {feedback}

Instructions:
1. Remove one key detail, suggestion, or explanation from the original feedback only if it is sufficiently long
2. If the original feedback consists of only a single sentence or item, do not simply shorten it, but replace it with 'The caption is accurate and requires no edits, so it should remain exactly the same.'
3. Return only the modified feedback paragraph without any additional text or explanations
4. If the feedback is presented as a numbered list (e.g., 1. xxxx 2. xxxx 3. xxxx …), then when deleting, remove one item at random rather than automatically deleting the last entry
5. Identify the portions of the feedback that conflict with the caption. These conflicting elements are relatively significant and can be prioritized for deletion, but delete only one full element from the original feedback""",

            "nonconstructive_critique_generation": """Please modify the following feedback to only point out problems without providing any constructive suggestions or solutions.

Caption Instruction:
{caption_instruction}

Original Caption: {caption}

Original Feedback: {feedback}

Instructions:
1. Convert all constructive suggestions in the feedback into criticism only: state only what is wrong in the caption that conflicts with the feedback, without mentioning what is correct.
2. Remove all helpful guidance or improvement suggestions. If the feedback is only guidance or suggestions, replace it with: 'The caption is accurate and requires no edits, so it should remain exactly the same.'
3. Return only the non-constructive feedback paragraph, with no extra text or explanation.
4. When feedback suggests adding something (not changing one thing to another), rephrase it to say the caption is missing that thing, stated generally without details.
5. If the feedback only provides the corrected version without explaining the issues, identify the problematic parts in the caption and state which parts are wrong.""",

            "gemini_critique_generation": """Please provide detailed feedback on how well this caption follows the given instruction. Carefully watch the video and analyze the caption against the instruction requirements.

Caption Instruction:
{caption_instruction}

Caption: {caption}

Instructions:
1. Carefully watch the video and review the caption against the specific requirements in the caption instruction
2. Identify any missing elements, inaccuracies, or areas for improvement based on what you observe in the video
3. Provide specific, actionable suggestions for how to improve the caption
4. Be thorough and constructive in your analysis
5. If the caption is already excellent, simply state 'The caption is accurate and requires no edits, so it should remain exactly the same.'
6. Return only your feedback paragraph without any additional text or explanations
7. If you discover any missing elements in the caption—details present in the video but omitted—you should point out which element has been left out
8. If you find any factual errors in the caption that conflict with the actual video, you should identify where the error occurs and explain how it should be corrected
9. If the caption is overly long and contains information unrelated to the Caption Instruction or is significantly redundant, you should point out those parts and explain that they need to be deleted
10. Do not offer feedback on things not specified in the Caption Instruction. Do not be wordy; keep suggestions concise, direct, and constructive""",

            "blind_gemini_critique_generation": """Please provide feedback on this caption by imagining you have watched the video. Generate a critique by assuming you have visual access to the content (you can imagine anything in the video).

Caption Instruction:
{caption_instruction}

Caption: {caption}

Instructions:
1. Pretend you have watched the video and generate feedback based on your imagined visual content
2. Create specific critique points about what you imagine might be missing or incorrect in the caption
3. Provide suggestions for improvement based on your imagined video content
4. Make the feedback substantial and detailed
5. You can imagine any visual elements that seem plausible for this type of content
6. Return only your feedback paragraph without any additional text or explanations""",

            "worst_caption_generation": """Please generate a completely new and incorrect caption that replaces the original caption entirely. The new caption should be plausible-sounding but factually wrong about what's shown in the video.

Caption Instruction:
{caption_instruction}

Original Caption: {caption}

Instructions:
1. Generate a completely new caption that follows the format and structure suggested by the Caption Instruction
2. The new caption should be entirely different from the original - do not reuse any specific details, objects, actions, or descriptions from the original caption
3. Replace all factual content with incorrect or irrelevant alternatives that sound plausible but are wrong
4. Maintain a similar length and level of detail as the original caption
5. The new caption should still attempt to address the Caption Instruction's requirements, but with completely incorrect information
6. Make the incorrect details specific and concrete rather than vague
7. Return only the completely new incorrect caption without any additional text or explanations
8. Do not include non-visual elements (e.g., background music, narration)
9. Ensure the new caption sounds natural and coherent, even though it's factually wrong"""
        }
    
    def debug_video_status(self, video_id: str):
        """Debug the status of a specific video across all tasks"""
        try:
            # Load configs
            configs = self.data_manager.load_config(self.app_config.configs_file)
            if isinstance(configs[0], str):
                configs = [self.data_manager.load_config(config) for config in configs]
            
            st.sidebar.write(f"**🔍 Debugging Video: {video_id}**")
            
            # Check if video exists in any URL file
            video_found_in_files = []
            for video_urls_file in self.app_config.video_urls_files:
                try:
                    video_urls = self.data_manager.load_json(video_urls_file)
                    if any(self.data_manager.get_video_id(url) == video_id for url in video_urls):
                        sheet_name = Path(video_urls_file).stem
                        video_found_in_files.append(sheet_name)
                except Exception:
                    continue
            
            if not video_found_in_files:
                st.sidebar.error(f"❌ Video {video_id} not found in any URL files")
                return
            else:
                st.sidebar.success(f"✅ Video found in sheets: {', '.join(video_found_in_files)}")
            
            # Check status for each task
            st.sidebar.write("**📋 Task Status:**")
            st.sidebar.write("*Status meanings:*")
            st.sidebar.write("- **not_completed**: No annotation yet")
            st.sidebar.write("- **completed_not_reviewed**: Annotated but not reviewed")  
            st.sidebar.write("- **approved**: Reviewed and approved (reviewer_double_check=True)")
            st.sidebar.write("- **rejected**: Reviewed and corrected by reviewer (reviewer_double_check=False)")
            st.sidebar.write("*Note: Both approved and rejected are considered 'complete' for filtering*")
            st.sidebar.write("---")
            
            all_complete = True
            task_results = []
            
            for config in configs:
                config_output_dir = os.path.join(
                    self.data_manager.folder, 
                    self.app_config.output_dir, 
                    config["output_name"]
                )
                
                # Get status using DataManager's method
                status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                    video_id, config_output_dir
                )
                
                # Load feedback data
                feedback_data = self.data_manager.load_data(
                    video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
                )
                
                # Load reviewer data  
                reviewer_data = self.data_manager.load_data(
                    video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX
                )
                
                # Extract details
                annotator = "None"
                reviewer = "None"
                reviewer_double_check = None
                
                # For rejected status, annotator is the original annotator (prev_user)
                # For approved status, annotator is current_user
                if status == "rejected" and prev_user:
                    annotator = prev_user
                elif status == "approved" and current_user:
                    annotator = current_user
                elif feedback_data:
                    # Fallback to feedback file user for other statuses
                    annotator = feedback_data.get("user", "Unknown")
                
                if reviewer_data:
                    reviewer = reviewer_data.get("reviewer_name", "Unknown")
                    reviewer_double_check = reviewer_data.get("reviewer_double_check", None)
                
                # Determine emoji based on status
                if status == "not_completed":
                    emoji = "⭕"
                elif status == "completed_not_reviewed":
                    emoji = "⏳"
                elif status == "approved":
                    emoji = "✅"
                elif status == "rejected":
                    emoji = "🔄"  # Different emoji for rejected (corrected)
                else:
                    emoji = "❓"
                
                # Both approved and rejected are considered "complete"
                if status not in ["approved", "rejected"]:
                    all_complete = False
                
                # Display task status
                task_name = config["name"]
                short_name = self.ui.config_names_to_short_names.get(task_name, task_name)
                
                st.sidebar.write(f"{emoji} **{short_name}**")
                st.sidebar.write(f"   Status: **{status}**")
                
                # Show names based on status
                if status in ["approved", "rejected"]:
                    st.sidebar.write(f"   Annotator: {annotator} {'(original)' if status == 'rejected' else ''}")
                    st.sidebar.write(f"   Reviewer: {reviewer}")
                    if reviewer_double_check is not None:
                        st.sidebar.write(f"   reviewer_double_check: {reviewer_double_check}")
                elif status in ["not_completed", "completed_not_reviewed"]:
                    if annotator != "None":
                        st.sidebar.write(f"   Annotator: {annotator}")
                    if status == "completed_not_reviewed":
                        st.sidebar.write(f"   Reviewer: Not reviewed yet")
                
                # Debug file existence
                feedback_exists = self.data_manager.data_exists(video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
                review_exists = self.data_manager.data_exists(video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
                prev_feedback_exists = self.data_manager.data_exists(video_id, config_output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                st.sidebar.write(f"   Files: feedback={feedback_exists}, review={review_exists}, prev_feedback={prev_feedback_exists}")
                st.sidebar.write("   ---")
                
                task_results.append({
                    "task": short_name,
                    "status": status,
                    "annotator": annotator,
                    "reviewer": reviewer,
                    "feedback_exists": feedback_exists,
                    "review_exists": review_exists,
                    "prev_feedback_exists": prev_feedback_exists
                })
            
            # Summary
            st.sidebar.write("**📊 Current Filter Logic:**")
            st.sidebar.write("Videos shown if ALL tasks have status='approved' OR 'rejected'")
            st.sidebar.write("(Both approved and rejected captions are considered complete)")
            
            approved_or_rejected = sum(1 for r in task_results if r["status"] in ["approved", "rejected"])
            total_tasks = len(task_results)
            
            if all_complete:
                st.sidebar.success(f"🎉 All tasks approved/rejected! Video should appear in the list.")
            else:
                incomplete_tasks = [r["task"] for r in task_results if r["status"] not in ["approved", "rejected"]]
                st.sidebar.warning(f"🚧 Not all complete. Missing: {', '.join(incomplete_tasks)}")
                
                # Detailed breakdown
                status_counts = {}
                for r in task_results:
                    status = r["status"]
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                st.sidebar.write("**Task breakdown:**")
                for status_type, count in status_counts.items():
                    st.sidebar.write(f"   {status_type}: {count}")
                
                st.sidebar.write(f"**Complete tasks:** {approved_or_rejected}/{total_tasks}")
                        
        except Exception as e:
            st.sidebar.error(f"Error debugging video {video_id}: {e}")
            import traceback
            st.sidebar.error(traceback.format_exc())
    
    @staticmethod
    @st.cache_resource
    def _load_all_reviewed_videos(configs_file, video_urls_files, output_dir, folder_path):
        """Static cached method to load all reviewed videos"""
        from caption.core.data_manager import DataManager
        from pathlib import Path
        import os
        
        # Create data manager instance
        data_manager = DataManager(Path(folder_path), Path(folder_path).parent)
        
        reviewed_videos = []
        
        try:
            # Load configs
            configs = data_manager.load_config(configs_file)
            if isinstance(configs[0], str):
                configs = [data_manager.load_config(config) for config in configs]
            
            # Check all video URL files
            for video_urls_file in video_urls_files:
                try:
                    video_urls = data_manager.load_json(video_urls_file)
                    
                    # Extract sheet name from file path
                    sheet_name = Path(video_urls_file).stem
                    
                    for video_url in video_urls:
                        video_id = data_manager.get_video_id(video_url)
                        
                        # Check if all tasks are completed and reviewed (approved OR rejected)
                        all_reviewed = True
                        video_captions = {}
                        reviewer_names = set()
                        
                        for config in configs:
                            config_output_dir = os.path.join(
                                folder_path, 
                                output_dir, 
                                config["output_name"]
                            )
                            
                            status, current_file, prev_file, current_user, prev_user = data_manager.get_video_status(
                                video_id, config_output_dir
                            )
                            
                            # Include both approved AND rejected videos (rejected = corrected by reviewer)
                            if status not in ["approved", "rejected"]:
                                all_reviewed = False
                                break
                            else:
                                # Load the final caption data
                                feedback_data = data_manager.load_data(
                                    video_id, config_output_dir, data_manager.FEEDBACK_FILE_POSTFIX
                                )
                                
                                # Load reviewer data
                                reviewer_data = data_manager.load_data(
                                    video_id, config_output_dir, data_manager.REVIEWER_FILE_POSTFIX
                                )
                                
                                reviewer_name = "Unknown"
                                if reviewer_data:
                                    reviewer_name = reviewer_data.get("reviewer_name", "Unknown")
                                    reviewer_names.add(reviewer_name)
                                
                                # For rejected status, annotator is in prev_user (original annotator)
                                # For approved status, annotator is in current_user  
                                if status == "rejected":
                                    annotator_name = prev_user if prev_user else "Unknown"
                                else:  # approved
                                    annotator_name = current_user if current_user else "Unknown"
                                
                                if feedback_data:
                                    video_captions[config["name"]] = {
                                        "final_caption": feedback_data.get("final_caption", ""),
                                        "pre_caption": feedback_data.get("pre_caption", ""),
                                        "initial_caption_rating": feedback_data.get("initial_caption_rating", ""),
                                        "final_feedback": feedback_data.get("final_feedback", ""),
                                        "annotator": annotator_name,
                                        "reviewer": reviewer_name,
                                        "timestamp": feedback_data.get("timestamp", ""),
                                        "task": config["task"],
                                        "config": config,
                                        "status": status
                                    }
                        
                        if all_reviewed and video_captions:
                            reviewed_videos.append({
                                "video_id": video_id,
                                "video_url": video_url,
                                "sheet_name": sheet_name,
                                "reviewers": list(reviewer_names),
                                "captions": video_captions
                            })
                            
                except Exception as e:
                    st.error(f"Error processing video file {video_urls_file}: {e}")
                    continue
                    
        except Exception as e:
            st.error(f"Error loading configurations: {e}")
        
        return reviewed_videos

    def get_all_reviewed_videos(self) -> List[Dict[str, Any]]:
        """Get all videos that have been fully reviewed across all tasks"""
        return self._load_all_reviewed_videos(
            self.app_config.configs_file,
            self.app_config.video_urls_files,
            self.app_config.output_dir,
            str(self.data_manager.folder)
        )
    
    def render_critique_task_selection_sidebar(self):
        """Render critique generation task selection in sidebar"""
        st.sidebar.title("🤖 Critique Generation Testing")
        st.sidebar.markdown("### Select a critique generation task")
        
        # Create task options
        task_options = {}
        for task_key, task_info in self.critique_tasks.items():
            display_name = f"{task_info['name']}"
            task_options[display_name] = {
                "key": task_key,
                "info": task_info
            }
        
        selected_task_display = st.sidebar.selectbox(
            "Select Critique Generation Task:",
            list(task_options.keys()),
            key="selected_critique_task"
        )
        
        if selected_task_display:
            selected_task = task_options[selected_task_display]
            
            # Show task description
            st.sidebar.info(f"**Description:** {selected_task['info']['description']}")
            st.sidebar.info(f"**Default LLM:** {selected_task['info']['default_llm']}")
            st.sidebar.info(f"**Video Access:** {'Yes' if selected_task['info']['supports_video'] else 'No'}")
            
            return selected_task
        return None
    
    def render_video_selection_sidebar(self, reviewed_videos: List[Dict[str, Any]]):
        """Render video selection in sidebar"""
        st.sidebar.markdown("### Select a video to test critique generation")
        
        if not reviewed_videos:
            st.sidebar.warning("No fully reviewed videos found.")
        
        # Add debugging section
        with st.sidebar.expander("🐛 Debug Video Status", expanded=False):
            debug_video_id = st.text_input(
                "Enter Video ID to debug:",
                placeholder="e.g., video_001.mp4",
                key="debug_video_id"
            )
            
            if st.button("🔍 Check Status", key="debug_button"):
                if debug_video_id:
                    self.debug_video_status(debug_video_id)
                else:
                    st.error("Please enter a video ID")
        
        if not reviewed_videos:
            return None
        
        # Add search functionality
        search_term = st.sidebar.text_input(
            "🔍 Search by Video ID:",
            placeholder="Type video ID to filter...",
            key="video_search"
        )
        
        # Create video options with sheet names
        video_options = {}
        for video_data in reviewed_videos:
            video_id = video_data["video_id"]
            sheet_name = video_data["sheet_name"]
            caption_count = len(video_data["captions"])
            display_name = f"{video_id} ({sheet_name}) - {caption_count} captions"
            video_options[display_name] = video_data
        
        # Filter videos based on search term
        if search_term:
            filtered_options = {}
            search_lower = search_term.lower()
            for display_name, video_data in video_options.items():
                video_id = video_data["video_id"].lower()
                searchable_text = f"{video_id} {sheet_name}".lower()
                if search_lower in searchable_text:
                    filtered_options[display_name] = video_data
            video_options = filtered_options
            
            # Show search results info
            if video_options:
                st.sidebar.success(f"Found {len(video_options)} video(s) matching '{search_term}'")
            else:
                st.sidebar.warning(f"No videos found matching '{search_term}'")
        
        # Show total count
        st.sidebar.info(f"Showing {len(video_options)} of {len(reviewed_videos)} total videos")
        
        if not video_options:
            return None
        
        selected_display = st.sidebar.selectbox(
            "Select Video:",
            list(video_options.keys()),
            key="selected_video"
        )
        
        if selected_display:
            return video_options[selected_display]
        return None
    
    def render_task_selection_sidebar(self, selected_video: Dict[str, Any]):
        """Render task selection in sidebar"""
        if not selected_video:
            return None
            
        captions = selected_video["captions"]
        task_options = {}
        
        for caption_name, caption_data in captions.items():
            short_name = self.ui.config_names_to_short_names.get(caption_name, caption_name)
            # Add reviewer info and status to the display
            annotator = caption_data["annotator"]
            reviewer = caption_data["reviewer"]
            status = caption_data.get("status", "unknown")
            status_emoji = "✅" if status == "approved" else "🔄" if status == "rejected" else "❓"
            
            display_with_info = f"{short_name} {status_emoji} (A:{annotator[:8]}, R:{reviewer[:8]})"
            task_options[display_with_info] = caption_data
        
        selected_task_display = st.sidebar.selectbox(
            "Select Task:",
            list(task_options.keys()),
            key="selected_task"
        )
        
        if selected_task_display:
            return task_options[selected_task_display]
        return None
    
    def render_prompt_and_generation_interface(self, selected_critique_task: Dict[str, Any], 
                                             selected_video: Dict[str, Any], selected_caption: Dict[str, Any]):
        """Render the prompt template and generation interface in the right column"""
        if not selected_critique_task or not selected_video or not selected_caption:
            st.subheader("📹 Video Preview")
            st.info("Please select a critique generation task, video, and task to begin.")
            return
            
        # Video display first
        st.subheader("📹 Video Preview")
        video_url = selected_video["video_url"]
        if video_url:
            st.video(video_url)
        else:
            st.warning("Video URL not available")
        
        # Display basic video info
        st.write(f"**Video ID:** {selected_video['video_id']}")
        st.write(f"**Sheet:** {selected_video['sheet_name']}")
        
        # Prompt input section
        st.write("### ✏️ Prompt Template")
        
        # Get task-specific prompt template
        critique_task_key = selected_critique_task['key']
        default_prompt = self.prompt_templates.get(critique_task_key, "")
        
        # Show task type info
        st.info(f"📝 Using **{selected_critique_task['info']['name']}** template")
        
        prompt_template = st.text_area(
            "Edit the prompt template (use {caption_instruction}, {caption}, {feedback} placeholders):",
            value=default_prompt,
            height=300,
            key="prompt_template"
        )
        
        # LLM selection and generate button
        col1, col2 = st.columns(2)
        with col1:
            available_llms = get_all_llms()
            default_llm = selected_critique_task['info']['default_llm']
            selected_llm = st.selectbox(
                "Select LLM:",
                available_llms,
                index=available_llms.index(default_llm) if default_llm in available_llms else 0,
                key="selected_llm"
            )
        
        with col2:
            # Change button text based on task type
            critique_task_key = selected_critique_task['key']
            button_text = "🚀 Generate Bad Caption" if critique_task_key == "worst_caption_generation" else "🚀 Generate Critique"
            generate_clicked = st.button(button_text, type="primary", use_container_width=True)
        
        # Handle generation
        if generate_clicked:
            critique_task_key = selected_critique_task['key']
            
            # Determine required placeholders based on task type
            if critique_task_key in ["gemini_critique_generation", "blind_gemini_critique_generation", "worst_caption_generation"]:
                required_placeholders = ["{caption_instruction}", "{caption}"]
            else:
                required_placeholders = ["{caption_instruction}", "{caption}", "{feedback}"]
            
            missing_placeholders = [p for p in required_placeholders if p not in prompt_template]
            
            if missing_placeholders:
                st.error(f"Prompt template must contain placeholders: {', '.join(missing_placeholders)}")
            else:
                final_caption = selected_caption["final_caption"]
                final_feedback = selected_caption.get("final_feedback", "")
                pre_caption = selected_caption["pre_caption"]
                task = selected_caption["task"]
                caption_instruction = self.get_caption_instruction_for_task(task)
                
                # Store current critique task for caption polishing logic
                st.session_state["current_critique_task"] = critique_task_key
                
                self.generate_critique(prompt_template, final_caption, final_feedback, selected_llm, 
                                     caption_instruction, selected_critique_task, selected_video["video_url"], 
                                     pre_caption)
    
    def get_caption_instruction_for_task(self, task: str) -> str:
        """Get the caption instruction for the task using PromptGenerator"""
        try:
            # Debug print to check if caption_programs exists
            if not hasattr(self, 'caption_programs'):
                st.error("DEBUG: caption_programs attribute not found!")
                return f"Please provide a detailed caption for {task.replace('_', ' ')}."
            
            if task in self.caption_programs:
                caption_program = self.caption_programs[task]
                return caption_program.get_prompt_without_video_info()
            else:
                return f"Please provide a detailed caption for {task.replace('_', ' ')}."
        except Exception as e:
            st.warning(f"Could not load caption instruction for {task}: {e}")
            return f"Please provide a detailed caption for {task.replace('_', ' ')}."
    
    def render_critique_testing_interface(self, selected_critique_task: Dict[str, Any], 
                                        selected_video: Dict[str, Any], selected_caption: Dict[str, Any]):
        """Render the critique generation testing interface in the left column"""
        if not selected_critique_task or not selected_video or not selected_caption:
            st.info("Please select a critique generation task, video, and task to begin testing.")
            return
            
        st.subheader("🤖 Critique Generation Testing")
        
        # Add instructions
        with st.expander("📖 Instructions", expanded=False):
            st.markdown(f"""
            **How to use this interface:**
            1. **Select a critique generation task** from the sidebar (currently: {selected_critique_task['info']['name']})
            2. **Select a video and task** from the sidebar
            3. **Review the final caption data** including pre_caption, rating, and feedback
            4. **Edit the prompt template** in the right column - use `{{caption_instruction}}`, `{{caption}}`, and `{{feedback}}` placeholders
            5. **Choose an LLM model** and click "Generate Critique" to test the conversion
            6. **Iterate on the prompt** to improve the critique generation
            
            **Current Task:** {selected_critique_task['info']['description']}
            """)
        
        # Display final caption information
        st.write("### 📋 Final Caption Data")
        final_caption = selected_caption["final_caption"]
        pre_caption = selected_caption.get("pre_caption", "")
        initial_caption_rating = selected_caption.get("initial_caption_rating", "")
        final_feedback = selected_caption.get("final_feedback", "")
        annotator = selected_caption["annotator"]
        reviewer = selected_caption["reviewer"]
        timestamp = self.data_manager.format_timestamp(selected_caption["timestamp"])
        status = selected_caption.get("status", "unknown")
        status_emoji = "✅" if status == "approved" else "🔄" if status == "rejected" else "❓"
        
        with st.container(border=True):
            st.write(f"**Status:** {status} {status_emoji}")
            st.write(f"**Annotator:** {annotator}")
            st.write(f"**Reviewer:** {reviewer}")
            st.write(f"**Completed:** {timestamp}")
            
            # Display all caption data
            if pre_caption:
                st.write("**Pre-Caption:**")
                st.write(pre_caption)
            
            if initial_caption_rating:
                # Convert emoji to score for display
                try:
                    score = self.ui.emoji_to_score(initial_caption_rating)
                    st.write(f"**Initial Caption Rating:** {score}/5")
                except (ValueError, AttributeError):
                    st.write(f"**Initial Caption Rating:** {initial_caption_rating}")
            
            st.write("**Final Feedback:**")
            st.write(final_feedback if final_feedback else "No feedback provided")
            
            st.write("**Final Caption:**")
            st.write(final_caption)
        
        # Get task info
        task = selected_caption["task"]
        
        # Display caption instruction
        st.write("### 📋 Caption Instruction")
        caption_instruction = self.get_caption_instruction_for_task(task)
        with st.expander("View Caption Instruction", expanded=False):
            st.write(caption_instruction)
    
    def generate_critique(self, prompt_template: str, final_caption: str, final_feedback: str, 
                         selected_llm: str, caption_instruction: str, selected_critique_task: Dict[str, Any], 
                         video_url: str, pre_caption: str = ""):
        """Generate critique using LLM"""
        try:
            critique_task_key = selected_critique_task['key']
            
            # Prepare the final prompt by substituting placeholders
            # Determine which caption to use based on task type
            if critique_task_key == "worst_caption_generation":
                # Use final_caption for worst caption generation
                caption_to_use = final_caption
                final_prompt = prompt_template.format(
                    caption_instruction=caption_instruction,
                    caption=caption_to_use
                )
            elif critique_task_key in ["gemini_critique_generation", "blind_gemini_critique_generation"]:
                # Use pre_caption for Gemini tasks without feedback
                final_prompt = prompt_template.format(
                    caption_instruction=caption_instruction,
                    caption=pre_caption
                )
            else:
                # Use pre_caption with feedback for error modification tasks
                final_prompt = prompt_template.format(
                    caption_instruction=caption_instruction,
                    caption=pre_caption,
                    feedback=final_feedback
                )
            
            with st.spinner(f"Generating critique with {selected_llm}..."):
                # Get LLM instance
                llm = get_llm(model=selected_llm, secrets=st.secrets)
                
                # Determine if we need video access
                supports_video = selected_critique_task['info']['supports_video']
                
                # Generate response
                if supports_video and video_url:
                    # For video-enabled tasks (Gemini with video)
                    response = llm.generate(
                        prompt=final_prompt,
                        video=video_url,
                        extracted_frames=[],  # Use entire video
                        temperature=0.0
                    )
                else:
                    # For text-only tasks
                    response = llm.generate(final_prompt)
                
                # Handle empty or whitespace-only responses
                if not response or not response.strip():
                    st.error("⚠️ LLM returned an empty response. Please try again or adjust the prompt.")
                    return
                
                response = response.strip()
                
                # Display results differently based on task type
                if critique_task_key == "worst_caption_generation":
                    st.write("### 🔄 Worst Caption Generation Result")
                    st.write("**📝 Original Final Caption (High Quality):**")
                    st.text(final_caption)
                    
                    st.write("**⚠️ Generated Bad Caption:**")
                    st.text(response)
                    
                    st.info("💡 This is a completely incorrect caption that replaces the original. No critique or revision step.")
                else:
                    st.write("### 📄 Generated Critique vs Original Feedback")
                    
                    # Show original feedback for all tasks for comparison purposes
                    st.write("**📝 Original Gold Feedback:**")
                    st.text(final_feedback if final_feedback else "No feedback provided")
                    
                    st.write("**⚠️ Generated Critique:**")
                    st.text(response)
                
                # Add expandable section with generation details - change title based on task type
                details_title = "🔧 Bad Caption Generation Details" if critique_task_key == "worst_caption_generation" else "🔧 Critique Generation Details"
                with st.expander(details_title, expanded=False):
                    st.write(f"**Model Used:** {selected_llm}")
                    st.write(f"**Mode:** {'Video' if supports_video else 'Text Only'}")
                    st.write("**Template Used:**")
                    st.code(prompt_template, language="text")
                    st.write("**Actual Prompt Sent to Model:**")
                    st.code(final_prompt, language="text")
                
                success_message = "✅ Bad caption generated successfully!" if critique_task_key == "worst_caption_generation" else "✅ Critique generated successfully!"
                st.success(success_message)
                
                # Only auto-generate improved caption for non-worst_caption_generation tasks
                if critique_task_key != "worst_caption_generation":
                    caption_to_polish = pre_caption
                    self.auto_generate_improved_caption(caption_to_polish, final_caption, response, selected_llm, video_url)
                
                # Store in session state for potential reuse
                if "generated_critiques" not in st.session_state:
                    st.session_state.generated_critiques = []
                
                st.session_state.generated_critiques.append({
                    "prompt": final_prompt,
                    "response": response,
                    "llm": selected_llm,
                    "task": selected_critique_task['info']['name'],
                    "supports_video": supports_video,
                    "timestamp": st.session_state.get("current_timestamp", "")
                })
                
        except Exception as e:
            st.error(f"Error generating critique with {selected_llm}: {e}")
            import traceback
            st.error(traceback.format_exc())
    
    def auto_generate_improved_caption(self, original_caption: str, final_caption: str, generated_feedback: str, selected_llm: str, video_url: str = ""):
        """Automatically generate improved caption using the generated feedback"""
        try:
            # Load the caption improvement prompt from caption/prompts/caption_prompt.txt
            caption_prompt_path = self.folder_path / "prompts" / "caption_prompt.txt"
            
            if caption_prompt_path.exists():
                with open(caption_prompt_path, 'r') as f:
                    caption_prompt_template = f.read()
            else:
                # Fallback prompt if file doesn't exist
                caption_prompt_template = """Given a video caption and user feedback, please provide an improved version of the caption that addresses the feedback. Note that the user feedback could be poorly written, so please try your best to guess what it means.

Original caption: {pre_caption}
User feedback: {feedback}

Respond with the improved caption only, without quotation marks or JSON formatting."""

            # Fill in the actual prompt with real values
            filled_caption_prompt = caption_prompt_template.format(pre_caption=original_caption, feedback=generated_feedback)

            with st.spinner("Auto-generating improved caption..."):
                # For Gemini Critique Generation, use Gemini with video
                if "gemini_critique_generation" in st.session_state.get("current_critique_task", ""):
                    caption_llm = get_llm(model="gemini-2.5-pro", secrets=st.secrets)
                    if video_url:
                        improved_caption = caption_llm.generate(
                            prompt=filled_caption_prompt,
                            video=video_url,
                            extracted_frames=[],
                            temperature=0.0
                        )
                    else:
                        improved_caption = caption_llm.generate(filled_caption_prompt)
                    caption_model_used = "gemini-2.5-pro (with video)" if video_url else "gemini-2.5-pro (text-only)"
                else:
                    # Use GPT-4 for caption improvement (consistent with the original app)
                    caption_llm = get_llm(model="gpt-4o-2024-08-06", secrets=st.secrets)
                    improved_caption = caption_llm.generate(filled_caption_prompt)
                    caption_model_used = "gpt-4o-2024-08-06"
                
                improved_caption = improved_caption.strip()
                
                # Display the caption comparison
                st.write("### 🔄 Caption Modification Using Generated Critique")
                st.write("**📝 Original Final Caption (High Quality):**")
                st.text(final_caption)
                
                st.write("**⚠️ GPT-Modified Caption (Using Generated Critique):**")
                st.text(improved_caption)
                
                # Add expandable section with prompt and model details
                with st.expander("🔧 Caption Polishing Details", expanded=False):
                    st.write(f"**Model Used:** {caption_model_used}")
                    st.write("**Template Used:**")
                    st.code(caption_prompt_template, language="text")
                    st.write("**Actual Prompt Sent to Model:**")
                    st.code(filled_caption_prompt, language="text")
                
                st.info("💡 The modified caption was generated using the generated critique as feedback, which may make it worse than the original.")
                
        except Exception as e:
            st.warning(f"Could not auto-generate improved caption: {e}")
            # Don't show error details to avoid cluttering the interface
    
    def run(self):
        """Main application entry point"""
        st.set_page_config(
            page_title="Critique Generation Testing",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🤖 Critique Generation Testing Interface")
        st.markdown("Test different prompts for converting feedback into various types of bad critiques")
        
        # Get all reviewed videos
        reviewed_videos = self.get_all_reviewed_videos()
        
        # Render sidebar - critique task selection first
        selected_critique_task = self.render_critique_task_selection_sidebar()
        selected_video = self.render_video_selection_sidebar(reviewed_videos)
        selected_caption = self.render_task_selection_sidebar(selected_video)
        
        # Main content area - split into two columns
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            self.render_critique_testing_interface(selected_critique_task, selected_video, selected_caption)
        
        with right_col:
            self.render_prompt_and_generation_interface(selected_critique_task, selected_video, selected_caption)


if __name__ == "__main__":
    args = parse_args()
    app = CritiqueGenerationApp(args.config_type)
    app.run()