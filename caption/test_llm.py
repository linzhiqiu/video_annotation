# caption/test_llm.py
import time
_script_start = time.time()

import streamlit as st

# MUST be first Streamlit command
st.set_page_config(
    page_title="LLM Caption Testing",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# These imports are cached by Python after first run
from caption.config import get_config
from caption.core.data_manager import DataManager  
from caption.core.video_utils import VideoUtils
from caption.core.ui_components import UIComponents
from llm import get_llm, get_all_llms
from caption_policy.prompt_generator import (
    SubjectPolicy, ScenePolicy, SubjectMotionPolicy, 
    SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, 
    RawSpatialPolicy, RawSubjectMotionPolicy
)

print(f"[{time.time() - _script_start:.2f}s] Imports done (cached by Python after first run)")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="LLM Testing Interface for Video Captions")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    return parser.parse_args()


@st.cache_data(ttl=300)
def load_json_policy(json_policy_path: str) -> Dict[str, Any]:
    """Load the JSON policy file with caching"""
    try:
        if os.path.exists(json_policy_path):
            with open(json_policy_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}


@st.cache_resource
def get_caption_programs() -> Dict[str, Any]:
    """Cache caption programs initialization"""
    return {
        "subject_description": SubjectPolicy(),
        "scene_composition_dynamics": ScenePolicy(),
        "subject_motion_dynamics": SubjectMotionPolicy(),
        "spatial_framing_dynamics": SpatialPolicy(),
        "camera_framing_dynamics": CameraPolicy(),
    }


class LLMTestApp:
    """LLM testing application for video captions"""
    
    def __init__(self, config_type: str):
        self.app_config = get_config(config_type)
        self.folder_path = Path(__file__).parent  # caption/ directory  
        self.root_path = self.folder_path.parent  # Go up to project root
        
        # Initialize core components (fast - just object creation)
        self.data_manager = DataManager(self.folder_path, self.root_path)
        self.video_utils = VideoUtils()
        self.ui = UIComponents()
        
        # Load JSON policy with caching
        self.json_policy_path = str(self.root_path / "json_policy" / "json_policy.json")
        self.json_policy = load_json_policy(self.json_policy_path)
        
        # Use cached caption programs
        self.caption_programs = get_caption_programs()
    
    def get_configs_cached(self) -> List[Dict[str, Any]]:
        """Load configs (cached in session state)"""
        cache_key = f"configs_{self.app_config.configs_file}"
        if cache_key not in st.session_state:
            configs = self.data_manager.load_config(self.app_config.configs_file)
            if isinstance(configs[0], str):
                configs = [self.data_manager.load_config(config) for config in configs]
            st.session_state[cache_key] = configs
        return st.session_state[cache_key]
    
    def debug_video_status(self, video_id: str):
        """Debug the status of a specific video across all tasks"""
        try:
            configs = self.get_configs_cached()
            
            st.sidebar.write(f"**🔍 Debugging Video: {video_id}**")
            
            # Check if video exists in any URL file
            video_found_in_files = []
            for video_urls_file in self.app_config.video_urls_files:
                try:
                    video_urls = self.data_manager.load_json(video_urls_file)
                    if video_urls and any(self.data_manager.get_video_id(url) == video_id for url in video_urls):
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
                
                status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                    video_id, config_output_dir
                )
                
                feedback_data = self.data_manager.load_data(
                    video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
                )
                
                reviewer_data = self.data_manager.load_data(
                    video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX
                )
                
                annotator = "None"
                reviewer = "None"
                reviewer_double_check = None
                
                if status == "rejected" and prev_user:
                    annotator = prev_user
                elif status == "approved" and current_user:
                    annotator = current_user
                elif feedback_data:
                    annotator = feedback_data.get("user", "Unknown")
                
                if reviewer_data:
                    reviewer = reviewer_data.get("reviewer_name", "Unknown")
                    reviewer_double_check = reviewer_data.get("reviewer_double_check", None)
                
                if status == "not_completed":
                    emoji = "⭕"
                elif status == "completed_not_reviewed":
                    emoji = "⏳"
                elif status == "approved":
                    emoji = "✅"
                elif status == "rejected":
                    emoji = "🔄"
                else:
                    emoji = "❓"
                
                if status not in ["approved", "rejected"]:
                    all_complete = False
                
                task_name = config["name"]
                short_name = self.ui.config_names_to_short_names.get(task_name, task_name)
                
                st.sidebar.write(f"{emoji} **{short_name}**")
                st.sidebar.write(f"   Status: **{status}**")
                
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
    
    def get_all_reviewed_videos(self) -> List[Dict[str, Any]]:
        """Get all videos that have been fully reviewed across all tasks (cached in session state)"""
        cache_key = "reviewed_videos_cache"
        
        # Return cached data if available (no time expiration - use Refresh button to reload)
        if cache_key in st.session_state:
            print(f"[{time.time() - _script_start:.2f}s] Using cached video list ({len(st.session_state[cache_key])} videos)")
            return st.session_state[cache_key]
        
        print(f"[{time.time() - _script_start:.2f}s] Loading reviewed videos (first time)...")
        reviewed_videos = []
        
        try:
            configs = self.get_configs_cached()
            
            for video_urls_file in self.app_config.video_urls_files:
                try:
                    video_urls = self.data_manager.load_json(video_urls_file)
                    if not video_urls:
                        continue
                    
                    sheet_name = Path(video_urls_file).stem
                    
                    for video_url in video_urls:
                        video_id = self.data_manager.get_video_id(video_url)
                        
                        all_reviewed = True
                        video_captions = {}
                        reviewer_names = set()
                        
                        for config in configs:
                            config_output_dir = os.path.join(
                                self.data_manager.folder, 
                                self.app_config.output_dir, 
                                config["output_name"]
                            )
                            
                            status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                                video_id, config_output_dir
                            )
                            
                            if status not in ["approved", "rejected"]:
                                all_reviewed = False
                                break
                            else:
                                feedback_data = self.data_manager.load_data(
                                    video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
                                )
                                
                                reviewer_data = self.data_manager.load_data(
                                    video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX
                                )
                                
                                reviewer_name = "Unknown"
                                if reviewer_data:
                                    reviewer_name = reviewer_data.get("reviewer_name", "Unknown")
                                    reviewer_names.add(reviewer_name)
                                
                                if status == "rejected":
                                    annotator_name = prev_user if prev_user else "Unknown"
                                else:
                                    annotator_name = current_user if current_user else "Unknown"
                                
                                if feedback_data:
                                    video_captions[config["name"]] = {
                                        "final_caption": feedback_data.get("final_caption", ""),
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
                    st.error(f"Error processing {video_urls_file}: {e}")
                    continue
                    
        except Exception as e:
            st.error(f"Error loading configurations: {e}")
        
        # Cache the results permanently until refresh
        st.session_state[cache_key] = reviewed_videos
        
        print(f"[{time.time() - _script_start:.2f}s] Loaded {len(reviewed_videos)} reviewed videos (now cached)")
        return reviewed_videos
    
    def render_video_selection_sidebar(self, reviewed_videos: List[Dict[str, Any]]):
        """Render video selection in sidebar"""
        st.sidebar.title("🎥 LLM Caption Testing")
        st.sidebar.markdown("### Select a video to test LLM prompts")
        
        if not reviewed_videos:
            st.sidebar.warning("No fully reviewed videos found.")
        
        # Add refresh button to clear cache
        if st.sidebar.button("🔄 Refresh Video List"):
            if "reviewed_videos_cache" in st.session_state:
                del st.session_state["reviewed_videos_cache"]
            st.rerun()
        
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
        
        search_term = st.sidebar.text_input(
            "🔍 Search by Video ID:",
            placeholder="Type video ID to filter...",
            key="video_search"
        )
        
        video_options = {}
        for video_data in reviewed_videos:
            video_id = video_data["video_id"]
            sheet_name = video_data["sheet_name"]
            caption_count = len(video_data["captions"])
            display_name = f"{video_id} ({sheet_name}) - {caption_count} captions"
            video_options[display_name] = video_data
        
        if search_term:
            filtered_options = {}
            search_lower = search_term.lower()
            for display_name, video_data in video_options.items():
                video_id = video_data["video_id"].lower()
                if search_lower in video_id:
                    filtered_options[display_name] = video_data
            video_options = filtered_options
            
            if video_options:
                st.sidebar.success(f"Found {len(video_options)} video(s) matching '{search_term}'")
            else:
                st.sidebar.warning(f"No videos found matching '{search_term}'")
        
        st.sidebar.info(f"Showing {len(video_options)} of {len(reviewed_videos)} total videos")
        
        if not video_options:
            return None
        
        selected_display = st.sidebar.selectbox(
            "Select Video:",
            list(video_options.keys()),
            key="selected_video"
        )
        
        if selected_display:
            selected_data = video_options[selected_display]
            # Clear generated JSON if video changed
            if st.session_state.get("_last_video_id") != selected_data["video_id"]:
                if "last_generated_json" in st.session_state:
                    del st.session_state["last_generated_json"]
                st.session_state["_last_video_id"] = selected_data["video_id"]
            return selected_data
        return None
    
    def render_task_selection_sidebar(self, selected_video: Dict[str, Any]):
        """Render task selection in sidebar"""
        if not selected_video:
            return None
            
        captions = selected_video["captions"]
        task_options = {}
        
        for caption_name, caption_data in captions.items():
            short_name = self.ui.config_names_to_short_names.get(caption_name, caption_name)
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
            selected_data = task_options[selected_task_display]
            # Clear generated JSON if task changed
            if st.session_state.get("_last_task") != selected_task_display:
                if "last_generated_json" in st.session_state:
                    del st.session_state["last_generated_json"]
                st.session_state["_last_task"] = selected_task_display
            return selected_data
        return None
    
    def render_video_display(self, selected_video: Dict[str, Any]):
        """Render video display in the right column"""
        if not selected_video:
            return
            
        st.subheader("📹 Video Preview")
        
        video_url = selected_video["video_url"]
        if video_url:
            st.video(video_url)
        else:
            st.warning("Video URL not available")
        
        st.write(f"**Video ID:** {selected_video['video_id']}")
        st.write(f"**Sheet:** {selected_video['sheet_name']}")
        st.write(f"**Total Tasks Completed:** {len(selected_video['captions'])}")
        
        reviewers = selected_video.get('reviewers', [])
        if reviewers:
            if len(reviewers) == 1:
                st.write(f"**Reviewer:** {reviewers[0]}")
            else:
                st.write(f"**Reviewers:** {', '.join(reviewers)}")
        
        with st.expander("📝 All Captions Summary", expanded=False):
            for caption_name, caption_data in selected_video["captions"].items():
                status = caption_data.get("status", "unknown")
                status_emoji = "✅" if status == "approved" else "🔄" if status == "rejected" else "❓"
                
                st.write(f"**{caption_name}** {status_emoji}")
                st.write(f"- Status: {status}")
                st.write(f"- Annotator: {caption_data['annotator']}")
                st.write(f"- Reviewer: {caption_data['reviewer']}")
                st.write(f"- Timestamp: {self.data_manager.format_timestamp(caption_data['timestamp'])}")
                st.write("---")
    
    def get_caption_instruction_for_task(self, task: str) -> str:
        """Get the caption instruction for the task using PromptGenerator"""
        try:
            if task in self.caption_programs:
                caption_program = self.caption_programs[task]
                return caption_program.get_prompt_without_video_info()
            else:
                return f"Please provide a detailed caption for {task.replace('_', ' ')}."
        except Exception as e:
            return f"Please provide a detailed caption for {task.replace('_', ' ')}."
    
    def get_json_policy_for_task(self, task: str) -> Dict[str, Any]:
        """Get the JSON policy structure for the task"""
        if not self.json_policy:
            return {}
        
        task_prompts = {
            "subject_description": "subject",
            "scene_composition_dynamics": "scene", 
            "subject_motion_dynamics": "motion",
            "spatial_framing_dynamics": "spatial",
            "camera_framing_dynamics": "camera",
            "color_composition_dynamics": "color",
            "lighting_setup_dynamics": "lighting",
            "lighting_effects_dynamics": "effects"
        }
        
        prompt_key = task_prompts.get(task, task)
        
        if prompt_key in self.json_policy:
            return self.json_policy[prompt_key]
        elif task in self.json_policy:
            return self.json_policy[task]
        else:
            return {}
    
    def get_prompt_template_for_task(self, task: str, json_policy: Dict[str, Any], caption_instruction: str) -> str:
        """Get the prompt template specific to the task with actual content filled in"""
        task_prompts = {
            "subject_description": "subject",
            "scene_composition_dynamics": "scene", 
            "subject_motion_dynamics": "motion",
            "spatial_framing_dynamics": "spatial",
            "camera_framing_dynamics": "camera",
            "color_composition_dynamics": "color",
            "lighting_setup_dynamics": "lighting",
            "lighting_effects_dynamics": "effects"
        }
        
        prompt_key = task_prompts.get(task, task)
        
        # Convert json_policy to string
        if json_policy:
            json_prompt_str = json.dumps(json_policy, indent=2)
        else:
            json_prompt_str = "Please use an appropriate JSON structure for this type of caption."
        
        base_template = f"""Please convert the following caption into the JSON format shown below:

{json_prompt_str}

Caption Instruction:
{caption_instruction}

Caption: {{caption}}

Instructions:
1. Use the exact same JSON keys as shown above
2. Preserve all important information from the caption with all the keywords and details
3. Organize the information appropriately under each key
4. If the caption doesn't contain some information, please review the caption instruction above to determine what should be the input
5. It is okay to leave fields blank as "" if nothing is mentioned in the caption
6. Return only valid JSON without any additional text"""
        
        if prompt_key == "camera":
            return base_template + """
7. No period after each caption"""
            
        elif prompt_key == "subject":
            return base_template + """
7. No period after each caption
8. Don't mention any detail of "wardrobe" and "appearance" in "type". Only mention each subject in short.
9. Don't mention any detail of "wardrobe" in "appearance". Only mention each subject in short."""
            
        elif prompt_key == "motion":
            return base_template + """
7. No period after each caption
8. Mention only subject action in "subject_action". Avoid mentioning camera related details"""
            
        else:
            return f"""Please convert the following caption into the JSON format shown below:

{json_prompt_str}

Caption Instruction:
{caption_instruction}

Caption: {{caption}}

Instructions:
1. Use the exact same JSON keys as shown above
2. Preserve all important information from the caption
3. Organize the information appropriately under each key
4. If the caption doesn't contain some information, please review the caption instruction above to determine what should be the input
5. It is okay to leave fields blank as "" if nothing is mentioned in the caption
6. Return only valid JSON without any additional text"""
    
    def get_templates_dir(self, task: str) -> Path:
        """Get the templates directory for a specific task, create if not exists"""
        # Map task names to folder names
        task_folder_map = {
            "subject_description": "subject",
            "scene_composition_dynamics": "scene",
            "subject_motion_dynamics": "motion",
            "spatial_framing_dynamics": "spatial",
            "camera_framing_dynamics": "camera",
            "color_composition_dynamics": "color",
            "lighting_setup_dynamics": "lighting",
            "lighting_effects_dynamics": "effects"
        }
        folder_name = task_folder_map.get(task, task)
        templates_dir = self.root_path / "json_policy" / "templates" / folder_name
        templates_dir.mkdir(parents=True, exist_ok=True)
        return templates_dir
    
    def get_available_templates(self, task: str) -> List[str]:
        """Get list of available template names for a specific task"""
        templates_dir = self.get_templates_dir(task)
        templates = ["default"]
        for f in sorted(templates_dir.glob("*.txt")):
            templates.append(f.stem)
        return templates
    
    def load_template(self, name: str, task: str, json_policy: Dict[str, Any], caption_instruction: str) -> str:
        """Load a template by name for a specific task"""
        if name == "default":
            # First check if there's a custom default reference file
            default_ref_file = self.get_templates_dir(task) / "default.txt"
            if default_ref_file.exists():
                with open(default_ref_file, 'r') as f:
                    ref_name = f.read().strip()
                # Load the referenced template
                template_path = self.get_templates_dir(task) / f"{ref_name}.txt"
                if template_path.exists():
                    with open(template_path, 'r') as f:
                        return f.read()
            # Otherwise use code-generated default
            return self.get_prompt_template_for_task(task, json_policy, caption_instruction)
        
        template_path = self.get_templates_dir(task) / f"{name}.txt"
        if template_path.exists():
            with open(template_path, 'r') as f:
                return f.read()
        return self.get_prompt_template_for_task(task, json_policy, caption_instruction)
    
    def set_as_default(self, template_name: str, task: str) -> None:
        """Set a template as the default for this task (saves reference only)"""
        default_ref_file = self.get_templates_dir(task) / "default.txt"
        with open(default_ref_file, 'w') as f:
            f.write(template_name)
    
    def get_default_template_name(self, task: str) -> Optional[str]:
        """Get the name of the template set as default, or None if using code default"""
        default_ref_file = self.get_templates_dir(task) / "default.txt"
        if default_ref_file.exists():
            with open(default_ref_file, 'r') as f:
                return f.read().strip()
        return None
    
    def has_custom_default(self, task: str) -> bool:
        """Check if a custom default template exists for this task"""
        default_ref_file = self.get_templates_dir(task) / "default.txt"
        return default_ref_file.exists()
    
    def reset_default(self, task: str) -> None:
        """Remove custom default and revert to code-generated default"""
        default_ref_file = self.get_templates_dir(task) / "default.txt"
        if default_ref_file.exists():
            default_ref_file.unlink()
    
    def save_template(self, name: str, content: str, task: str) -> bool:
        """Save a template for a specific task. Returns False if name already exists."""
        template_path = self.get_templates_dir(task) / f"{name}.txt"
        if template_path.exists():
            return False
        with open(template_path, 'w') as f:
            f.write(content)
        return True
    
    # def render_llm_testing_interface(self, selected_video: Dict[str, Any], selected_caption: Dict[str, Any]):
    #     """Render the LLM testing interface in the left column"""
    #     if not selected_video or not selected_caption:
    #         st.info("Please select a video and task to begin testing LLM prompts.")
    #         return
            
    #     st.subheader("🤖 LLM Caption Testing")
        
    #     with st.expander("📖 Instructions", expanded=False):
    #         st.markdown("""
    #         **How to use this interface:**
    #         1. **Select a video and task** from the sidebar
    #         2. **Review the final caption** that was approved by reviewers
    #         3. **Select a prompt template** or use the default one
    #         4. **Edit the prompt template** - the JSON structure and caption instruction are already included
    #         5. **Save your template** if you want to reuse it (use a unique name)
    #         6. **Choose an LLM model** and click "Generate JSON" to test the conversion
            
    #         **Note:** The template must contain `{caption}` placeholder which will be replaced with the actual caption.
            
    #         **Task-specific default templates:**
    #         - **Camera**: Includes "No period after each caption"
    #         - **Subject**: Includes specific wardrobe/appearance restrictions
    #         - **Motion**: Includes subject action focus restrictions
    #         - **Others**: Use default template
    #         """)
        
    #     st.write("### 📋 Final Caption")
    #     final_caption = selected_caption["final_caption"]
    #     annotator = selected_caption["annotator"]
    #     reviewer = selected_caption["reviewer"]
    #     timestamp = self.data_manager.format_timestamp(selected_caption["timestamp"])
    #     status = selected_caption.get("status", "unknown")
    #     status_emoji = "✅" if status == "approved" else "🔄" if status == "rejected" else "❓"
        
    #     with st.container(border=True):
    #         st.write(f"**Status:** {status} {status_emoji}")
    #         st.write(f"**Annotator:** {annotator}")
    #         st.write(f"**Reviewer:** {reviewer}")
    #         st.write(f"**Completed:** {timestamp}")
    #         st.write("**Caption:**")
    #         st.write(final_caption)
        
    #     task = selected_caption["task"]
    #     json_policy = self.get_json_policy_for_task(task)
    #     caption_instruction = self.get_caption_instruction_for_task(task)
        
    #     # Get task short name for display
    #     task_folder_map = {
    #         "subject_description": "subject",
    #         "scene_composition_dynamics": "scene",
    #         "subject_motion_dynamics": "motion",
    #         "spatial_framing_dynamics": "spatial",
    #         "camera_framing_dynamics": "camera",
    #         "color_composition_dynamics": "color",
    #         "lighting_setup_dynamics": "lighting",
    #         "lighting_effects_dynamics": "effects"
    #     }
    #     task_short = task_folder_map.get(task, task)
        
    #     st.write("### ✏️ Prompt Template")
        
    #     # Check if custom default exists
    #     has_custom_default = self.has_custom_default(task)
    #     default_template_name = self.get_default_template_name(task)
        
    #     if has_custom_default:
    #         st.caption(f"📁 Templates for task: **{task_short}** (⭐ default → {default_template_name})")
    #     else:
    #         st.caption(f"📁 Templates for task: **{task_short}**")
        
    #     # Template selection - task-specific
    #     available_templates = self.get_available_templates(task)
        
    #     # Add indicator to default option if custom, and show which template is the default
    #     display_templates = []
    #     for t in available_templates:
    #         if t == "default" and has_custom_default:
    #             display_templates.append(f"default ⭐ (→ {default_template_name})")
    #         elif t == default_template_name:
    #             display_templates.append(f"{t} ⭐")
    #         else:
    #             display_templates.append(t)
        
    #     selected_display = st.selectbox(
    #         f"Select Template ({len(available_templates)} available):",
    #         display_templates,
    #         key="template_selector"
    #     )
        
    #     # Map back to actual template name
    #     selected_template = selected_display.split(" ⭐")[0].split(" (")[0] if selected_display else "default"
        
    #     # Load selected template
    #     # Track template changes to reload content
    #     template_cache_key = f"_template_content_{task}_{selected_template}"
    #     if template_cache_key not in st.session_state or st.session_state.get("_last_template") != selected_template or st.session_state.get("_last_task_for_template") != task:
    #         loaded_template = self.load_template(selected_template, task, json_policy, caption_instruction)
    #         st.session_state[template_cache_key] = loaded_template
    #         st.session_state["_last_template"] = selected_template
    #         st.session_state["_last_task_for_template"] = task
        
    #     prompt_template = st.text_area(
    #         "Edit the prompt template (must contain {caption} placeholder):",
    #         value=st.session_state.get(template_cache_key, ""),
    #         height=400,
    #         key="prompt_template"
    #     )
        
    #     # Update session state with current edits
    #     st.session_state[template_cache_key] = prompt_template
        
    #     # Save template section
    #     with st.expander("💾 Save as New Template", expanded=False):
    #         new_template_name = st.text_input(
    #             "Template name:",
    #             placeholder="e.g., my_custom_template",
    #             key="new_template_name"
    #         )
    #         save_clicked = st.button("💾 Save Template", type="secondary", use_container_width=True)
            
    #         if save_clicked:
    #             if not new_template_name:
    #                 st.error("Please enter a template name.")
    #             elif new_template_name == "default":
    #                 st.error("Cannot use 'default' as template name. Use 'Set as Default' button instead.")
    #             elif "{caption}" not in prompt_template:
    #                 st.error("Template must contain {caption} placeholder!")
    #             elif not new_template_name.replace("_", "").replace("-", "").isalnum():
    #                 st.error("Template name can only contain letters, numbers, underscores, and hyphens.")
    #             else:
    #                 if self.save_template(new_template_name, prompt_template, task):
    #                     st.success(f"✅ Template '{new_template_name}' saved to {task_short}/!")
    #                     st.rerun()
    #                 else:
    #                     st.error(f"❌ Template '{new_template_name}' already exists. Choose a different name.")
        
    #     # Set as default section
    #     with st.expander("⭐ Set as Default Template", expanded=False):
    #         has_custom = self.has_custom_default(task)
    #         current_default_name = self.get_default_template_name(task)
            
    #         if has_custom:
    #             st.info(f"📌 Default is set to: **{current_default_name}**")
    #         else:
    #             st.caption(f"No custom default set for {task_short} (using code-generated default)")
            
    #         # Get list of saved templates (excluding "default")
    #         saved_templates = [t for t in available_templates if t != "default"]
            
    #         if saved_templates:
    #             default_choice = st.selectbox(
    #                 "Select template to use as default:",
    #                 saved_templates,
    #                 key="default_template_choice"
    #             )
                
    #             col_set, col_reset = st.columns(2)
    #             with col_set:
    #                 set_default_clicked = st.button("⭐ Set as Default", use_container_width=True)
    #             with col_reset:
    #                 reset_default_clicked = st.button("🔄 Reset to Original", use_container_width=True, disabled=not has_custom)
                
    #             if set_default_clicked:
    #                 self.set_as_default(default_choice, task)
    #                 st.success(f"✅ '{default_choice}' set as default for {task_short}!")
    #                 # Clear cache to reload
    #                 if template_cache_key in st.session_state:
    #                     del st.session_state[template_cache_key]
    #                 st.rerun()
                
    #             if reset_default_clicked:
    #                 self.reset_default(task)
    #                 st.success(f"✅ Default reset to original for {task_short}!")
    #                 # Clear cache to reload
    #                 if template_cache_key in st.session_state:
    #                     del st.session_state[template_cache_key]
    #                 st.rerun()
    #         else:
    #             st.caption("No saved templates yet. Save a template first to set it as default.")
        
    #     # LLM selection and generate button
    #     st.write("### 🚀 Generate JSON")
        
    #     available_llms = get_all_llms()
    #     selected_llm = st.selectbox(
    #         "Select LLM:",
    #         available_llms,
    #         index=available_llms.index("gpt-5.2") if "gpt-5.2" in available_llms else 0,
    #         key="selected_llm"
    #     )
        
    #     generate_clicked = st.button("🚀 Generate JSON", type="primary", use_container_width=True)
        
    #     # Handle generation
    #     if generate_clicked:
    #         if "{caption}" not in prompt_template:
    #             st.error("Prompt template must contain {caption} placeholder!")
    #         else:
    #             self.generate_json_caption(prompt_template, final_caption, selected_llm)
        
    #     # Show previous results if available and matches current selection
    #     elif "last_generated_json" in st.session_state:
    #         last_result = st.session_state["last_generated_json"]
    #         st.write("### 📄 Last Generated JSON")
    #         st.code(last_result["formatted"], language="json")
    #         if last_result["valid"]:
    #             st.success(f"✅ Valid JSON generated with {last_result['llm']}")
    #         else:
    #             st.error(f"⚠️ Response is not valid JSON format")

    def render_llm_testing_interface(self, selected_video: Dict[str, Any], selected_caption: Dict[str, Any]):
        """Render the LLM testing interface in the left column"""
        if not selected_video or not selected_caption:
            st.info("Please select a video and task to begin testing LLM prompts.")
            return
            
        st.subheader("🤖 LLM Caption Testing")
        
        with st.expander("📖 Instructions", expanded=False):
            st.markdown("""
            **How to use this interface:**
            1. **Select a video and task** from the sidebar
            2. **Review the final caption** that was approved by reviewers
            3. **Select a prompt template** or use the default one
            4. **Edit the prompt template** - the JSON structure and caption instruction are already included
            5. **Save your template** if you want to reuse it (use a unique name)
            6. **Choose an LLM model** and click "Generate JSON" to test the conversion
            
            **Note:** The template must contain `{caption}` placeholder which will be replaced with the actual caption.
            
            **Task-specific default templates:**
            - **Camera**: Includes "No period after each caption"
            - **Subject**: Includes specific wardrobe/appearance restrictions
            - **Motion**: Includes subject action focus restrictions
            - **Others**: Use default template
            """)
        
        st.write("### 📋 Final Caption")
        final_caption = selected_caption["final_caption"]
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
            st.write("**Caption:**")
            st.write(final_caption)
        
        task = selected_caption["task"]
        json_policy = self.get_json_policy_for_task(task)
        caption_instruction = self.get_caption_instruction_for_task(task)
        
        # Get task short name for display
        task_folder_map = {
            "subject_description": "subject",
            "scene_composition_dynamics": "scene",
            "subject_motion_dynamics": "motion",
            "spatial_framing_dynamics": "spatial",
            "camera_framing_dynamics": "camera",
            "color_composition_dynamics": "color",
            "lighting_setup_dynamics": "lighting",
            "lighting_effects_dynamics": "effects"
        }
        task_short = task_folder_map.get(task, task)
        
        st.write("### ✏️ Prompt Template")
        
        # Check if custom default exists
        has_custom_default = self.has_custom_default(task)
        default_template_name = self.get_default_template_name(task)
        
        if has_custom_default:
            st.caption(f"📁 Templates for task: **{task_short}** (⭐ default → {default_template_name})")
        else:
            st.caption(f"📁 Templates for task: **{task_short}**")
        
        # Template selection - task-specific
        available_templates = self.get_available_templates(task)
        
        # Add indicator to default option if custom, and show which template is the default
        display_templates = []
        for t in available_templates:
            if t == "default" and has_custom_default:
                display_templates.append(f"default ⭐ (→ {default_template_name})")
            elif t == default_template_name:
                display_templates.append(f"{t} ⭐")
            else:
                display_templates.append(t)
        
        selected_display = st.selectbox(
            f"Select Template ({len(available_templates)} available):",
            display_templates,
            key="template_selector"
        )
        
        # Map back to actual template name
        selected_template = selected_display.split(" ⭐")[0].split(" (")[0] if selected_display else "default"
        
        # Create a unique key for tracking template/task changes
        current_template_key = f"{task}_{selected_template}"
        
        # Only reload template content when template or task actually changes
        # Use a tracking key to detect real changes vs just re-runs
        if st.session_state.get("_current_template_key") != current_template_key:
            # Template or task changed - load fresh content
            loaded_template = self.load_template(selected_template, task, json_policy, caption_instruction)
            st.session_state["_loaded_template_content"] = loaded_template
            st.session_state["_current_template_key"] = current_template_key
            # Clear the widget state to force it to use the new default
            if "prompt_template" in st.session_state:
                del st.session_state["prompt_template"]
        
        # Get the initial value - either from widget state (user edits) or loaded content
        if "prompt_template" in st.session_state:
            # Widget has state from user edits - use that
            initial_value = st.session_state["prompt_template"]
        else:
            # No widget state yet - use loaded template
            initial_value = st.session_state.get("_loaded_template_content", "")
        
        prompt_template = st.text_area(
            "Edit the prompt template (must contain {caption} placeholder):",
            value=initial_value,
            height=400,
            key="prompt_template"
        )
        
        # Save template section
        with st.expander("💾 Save as New Template", expanded=False):
            new_template_name = st.text_input(
                "Template name:",
                placeholder="e.g., my_custom_template",
                key="new_template_name"
            )
            save_clicked = st.button("💾 Save Template", type="secondary", use_container_width=True)
            
            if save_clicked:
                if not new_template_name:
                    st.error("Please enter a template name.")
                elif new_template_name == "default":
                    st.error("Cannot use 'default' as template name. Use 'Set as Default' button instead.")
                elif "{caption}" not in prompt_template:
                    st.error("Template must contain {caption} placeholder!")
                elif not new_template_name.replace("_", "").replace("-", "").isalnum():
                    st.error("Template name can only contain letters, numbers, underscores, and hyphens.")
                else:
                    if self.save_template(new_template_name, prompt_template, task):
                        st.success(f"✅ Template '{new_template_name}' saved to {task_short}/!")
                        st.rerun()
                    else:
                        st.error(f"❌ Template '{new_template_name}' already exists. Choose a different name.")
        
        # Set as default section
        with st.expander("⭐ Set as Default Template", expanded=False):
            has_custom = self.has_custom_default(task)
            current_default_name = self.get_default_template_name(task)
            
            if has_custom:
                st.info(f"📌 Default is set to: **{current_default_name}**")
            else:
                st.caption(f"No custom default set for {task_short} (using code-generated default)")
            
            # Get list of saved templates (excluding "default")
            saved_templates = [t for t in available_templates if t != "default"]
            
            if saved_templates:
                default_choice = st.selectbox(
                    "Select template to use as default:",
                    saved_templates,
                    key="default_template_choice"
                )
                
                col_set, col_reset = st.columns(2)
                with col_set:
                    set_default_clicked = st.button("⭐ Set as Default", use_container_width=True)
                with col_reset:
                    reset_default_clicked = st.button("🔄 Reset to Original", use_container_width=True, disabled=not has_custom)
                
                if set_default_clicked:
                    self.set_as_default(default_choice, task)
                    st.success(f"✅ '{default_choice}' set as default for {task_short}!")
                    # Force reload on next run
                    st.session_state["_current_template_key"] = None
                    if "prompt_template" in st.session_state:
                        del st.session_state["prompt_template"]
                    st.rerun()
                
                if reset_default_clicked:
                    self.reset_default(task)
                    st.success(f"✅ Default reset to original for {task_short}!")
                    # Force reload on next run
                    st.session_state["_current_template_key"] = None
                    if "prompt_template" in st.session_state:
                        del st.session_state["prompt_template"]
                    st.rerun()
            else:
                st.caption("No saved templates yet. Save a template first to set it as default.")
        
        # LLM selection and generate button
        st.write("### 🚀 Generate JSON")
        
        available_llms = get_all_llms()
        selected_llm = st.selectbox(
            "Select LLM:",
            available_llms,
            index=available_llms.index("gpt-5.2") if "gpt-5.2" in available_llms else 0,
            key="selected_llm"
        )
        
        generate_clicked = st.button("🚀 Generate JSON", type="primary", use_container_width=True)
        
        # Handle generation
        if generate_clicked:
            if "{caption}" not in prompt_template:
                st.error("Prompt template must contain {caption} placeholder!")
            else:
                self.generate_json_caption(prompt_template, final_caption, selected_llm)
        
        # Show previous results if available and matches current selection
        elif "last_generated_json" in st.session_state:
            last_result = st.session_state["last_generated_json"]
            st.write("### 📄 Last Generated JSON")
            st.code(last_result["formatted"], language="json")
            if last_result["valid"]:
                st.success(f"✅ Valid JSON generated with {last_result['llm']}")
            else:
                st.error(f"⚠️ Response is not valid JSON format")
                
    def generate_json_caption(self, prompt_template: str, final_caption: str, selected_llm: str):
        """Generate JSON version of caption using LLM"""
        try:
            # Use replace instead of format to avoid issues with curly braces in JSON
            final_prompt = prompt_template.replace("{caption}", final_caption)
            
            with st.spinner(f"Generating JSON with {selected_llm}..."):
                llm = get_llm(model=selected_llm, secrets=st.secrets)
                response = llm.generate(final_prompt)
                
                if not response or not response.strip():
                    st.error("⚠️ LLM returned an empty response. Please try again or adjust the prompt.")
                    return
                
                response = response.strip()
                
                if response.startswith('```json'):
                    response = response[7:]
                elif response.startswith('```'):
                    response = response[3:]
                
                if response.endswith('```'):
                    response = response[:-3]
                
                response = response.strip()
                
                st.write("### 📄 Generated JSON")
                
                try:
                    parsed_json = json.loads(response)
                    formatted_json = json.dumps(parsed_json, indent=2)
                    st.code(formatted_json, language="json")
                    st.success("✅ Valid JSON generated!")
                    
                    # Store result
                    st.session_state["last_generated_json"] = {
                        "formatted": formatted_json,
                        "valid": True,
                        "llm": selected_llm
                    }
                except json.JSONDecodeError as e:
                    st.code(response, language="json")
                    st.error(f"⚠️ Response is not valid JSON format: {e}")
                    st.info(f"Response length: {len(response)} characters")
                    if len(response) > 0:
                        st.info(f"First 50 chars: `{repr(response[:50])}`")
                    
                    st.session_state["last_generated_json"] = {
                        "formatted": response,
                        "valid": False,
                        "llm": selected_llm
                    }
                
                if "generated_results" not in st.session_state:
                    st.session_state.generated_results = []
                
                st.session_state.generated_results.append({
                    "prompt": final_prompt,
                    "response": response,
                    "llm": selected_llm,
                })
                    
        except Exception as e:
            st.error(f"Error generating JSON with {selected_llm}: {e}")
    
    def run(self):
        """Main application entry point"""
        st.title("🤖 LLM Caption Testing Interface")
        st.markdown("Test different prompts for converting final captions to JSON format")
        
        # Get all reviewed videos (cached in session state)
        reviewed_videos = self.get_all_reviewed_videos()
        
        # Render sidebar
        selected_video = self.render_video_selection_sidebar(reviewed_videos)
        selected_caption = self.render_task_selection_sidebar(selected_video)
        
        # Main content area
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            self.render_llm_testing_interface(selected_video, selected_caption)
        
        with right_col:
            self.render_video_display(selected_video)


if __name__ == "__main__":
    args = parse_args()
    app = LLMTestApp(args.config_type)
    app.run()
    print(f"[{time.time() - _script_start:.2f}s] Done")