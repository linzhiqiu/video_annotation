# caption/json_and_summary_caption_streamlit.py
import streamlit as st
import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

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
    parser = argparse.ArgumentParser(description="Multi-Caption LLM Testing Interface")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    return parser.parse_args()


@st.cache_resource
def get_token_counter():
    """Lazy load and cache the tokenizer (only loads once across all sessions)"""
    try:
        from transformers import T5TokenizerFast
        import sys
        print("Loading UMT5-XXL tokenizer (first time only, ~30 seconds)...", file=sys.stderr)
        tokenizer = T5TokenizerFast.from_pretrained("google/umt5-xxl")
        print("Tokenizer loaded successfully!", file=sys.stderr)
        return tokenizer, True, None
    except ImportError:
        return None, False, "transformers library not found. Install with: pip install transformers"
    except Exception as e:
        return None, False, f"Failed to load tokenizer: {e}"


def count_tokens(text: str, tokenizer, use_tokenizer: bool) -> int:
    """Count tokens using the tokenizer or approximate"""
    if use_tokenizer and tokenizer:
        tokens = tokenizer.encode(text, add_special_tokens=True)
        return len(tokens)
    else:
        # Approximate: assume 0.75 words per token
        return int(len(text.split()) / 0.75)


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())


class MultiCaptionLLMApp:
    """Multi-caption LLM testing application - optimized with fragments"""
    
    # Task definitions
    TASKS = {
        "summary_generation": {
            "name": "Combined Caption Generation",
            "description": "Intelligently merge all five caption types into one comprehensive, non-redundant caption",
            "default_instruction": """Please merge the following five captions into a single, comprehensive caption that describes the video completely without any redundancy.

Caption Types:
1. Subject: Describes the subjects/people in the video
2. Scene: Describes the scene composition and environment
3. Motion: Describes the movement and dynamics of subjects
4. Spatial: Describes the spatial relationships and framing
5. Camera: Describes camera movements and framing choices

Input Captions:
{captions}

Instructions:
1. Use the SPATIAL caption as your BASE structure - it provides the core visual description and framing
2. Merge MOTION and CAMERA captions into the spatial description to create a temporally coherent narrative that describes how things change over time
3. Add information from SUBJECT and SCENE captions ONLY if they contain unique details not already covered in the Spatial caption
4. Eliminate ALL redundant information - if the same detail appears in multiple captions, mention it only ONCE
5. Preserve the EXACT wording from the original captions whenever possible. You may remove duplicated phrases or clauses if they repeat the same information verbatim across captions, but you must not introduce new wording or paraphrase existing content
6. When describing temporal changes, integrate information from all five captions in chronological order. First describe the subject appearance, then narrate events as they occur over time, including subject motion and camera movement, to clearly show how the scene evolves
7. CRITICAL: Every unique non-redundant detail from all five captions must appear in the final merged caption exactly once - nothing should be omitted or repeated
8. Do NOT add any information not present in the original captions
9. Return only the merged caption without any additional text or formatting
10. Generate the output strictly based on the content provided in the five tasks, and do not add any information that is not explicitly mentioned
11. Since events across the five tasks may overlap or be repeated, consolidate them into a single coherent description without redundantly repeating the same event, while ensuring that no relevant information is omitted and the language remains fluent
12. Base subject identification strictly on the subject caption. Explicitly identify the exact number of distinct subjects and determine the corresponding appearance for each subject. Do not split descriptions that refer to the same subject into multiple subjects. Information in the spatial caption only provides spatial details for these already-identified subjects and must not be treated as introducing new subjects
13. The final caption should describe each distinct action, object, and camera movement at most once. Repetition for emphasis or rephrasing is strictly disallowed
14. The scene caption, subject caption, and spatial information may contain overlapping content. When similar descriptions appear, explicitly determine whether they refer to the same element, and do not repeat equivalent descriptions multiple times
15. Explicitly analyze the sequence of events and motions described in the spatial caption and motion caption, clearly determining the order of camera movement and subject motion. If camera movement information appears in multiple captions, prioritize and rely on the camera caption as the authoritative source. Analyze the temporal order of camera changes in relation to changes in on-screen elements, and integrate them into a single, coherent chronological description
16. Use concise language and simple sentences. Keep the description brief without losing any essential information
17. Enforce minimum expression. Before returning the caption, delete any word, phrase, or clause that can be removed without changing the viewer’s mental image of the scene. Do not repeat the same attribute, perspective, action, or UI concept in different words. If multiple descriptors refer to the same element, keep only the shortest one. Limit each sentence to a single primary visual idea; split sentences if needed to improve readability

Goal: A single, clear, and temporally coherent caption grounded in the Spatial description, with Motion and Camera information merged in chronological order. Describe each visually salient event only once, using concise, readable sentences. Add Subject and Scene details only when they introduce new, non-redundant information that affects scene understanding, and present all details in a fluent, human-readable narrative."""
        },
        "json_generation": {
            "name": "Multi-Caption JSON Generation",
            "description": "Generate a single JSON combining all five caption types",
            "default_instruction": """Please convert the following five captions into a comprehensive JSON format that combines information from all caption types.

JSON Structure (use this exact structure with these keys):
{json_policy}

Input Captions:
{captions}

Instructions:
1. Use the EXACT JSON structure shown above with all the nested keys for subject, scene, motion, spatial, and camera
2. Preserve ALL important information from each caption type - include all keywords and details mentioned in the captions
3. Organize information from each caption type under its corresponding top-level key (subject, scene, motion, spatial, camera)
4. For each field in the JSON structure, extract relevant information from the corresponding caption
5. If a caption doesn't mention information for a specific field, leave that field as an empty string ""
6. Do NOT hallucinate or add information not present in the captions
7. Do NOT add periods at the end of field values
8. Return ONLY valid JSON without any additional text or markdown formatting"""
        }
    }
    
    def __init__(self, config_type: str):
        self.app_config = get_config(config_type)
        self.folder_path = Path(__file__).parent.resolve()
        self.root_path = self.folder_path.parent
        
        # Initialize core components
        self.data_manager = DataManager(self.folder_path, self.root_path)
        self.video_utils = VideoUtils()
        self.ui = UIComponents()
        
        # Get tokenizer (lazy loaded and cached)
        self.tokenizer, self.use_tokenizer, self.tokenizer_error = get_token_counter()
        
        # Load JSON policy
        self.json_policy_path = self.root_path / "json_policy" / "json_policy.json"
        self.json_policy = self.load_json_policy()
        
        # Task name mapping
        self.task_name_map = {
            "subject_description": "Subject",
            "scene_composition_dynamics": "Scene",
            "subject_motion_dynamics": "Motion",
            "spatial_framing_dynamics": "Spatial",
            "camera_framing_dynamics": "Camera",
        }
    
    def load_json_policy(self) -> Dict[str, Any]:
        """Load the JSON policy file with proper UTF-8 encoding"""
        try:
            if self.json_policy_path.exists():
                with open(self.json_policy_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                st.warning(f"JSON policy file not found at {self.json_policy_path}")
                return {}
        except Exception as e:
            st.error(f"Error loading JSON policy: {e}")
            return {}
    
    def get_combined_json_policy(self) -> Dict[str, Any]:
        """Get the combined JSON policy structure for all 5 caption types"""
        if not self.json_policy:
            return {}
        
        combined_policy = {}
        for task_key in ["subject", "scene", "motion", "spatial", "camera"]:
            if task_key in self.json_policy:
                combined_policy[task_key] = self.json_policy[task_key]
        
        return combined_policy
    
    @st.cache_data
    def get_all_reviewed_videos(_self) -> List[Dict[str, Any]]:
        """Get all videos that have been fully reviewed across all tasks"""
        reviewed_videos = []
        
        try:
            configs = _self.data_manager.load_config(_self.app_config.configs_file)
            if isinstance(configs[0], str):
                configs = [_self.data_manager.load_config(config) for config in configs]
            
            progress_bar = st.progress(0, text="Loading reviewed videos...")
            total_files = len(_self.app_config.video_urls_files)
            
            for file_idx, video_urls_file in enumerate(_self.app_config.video_urls_files):
                progress_bar.progress((file_idx + 1) / total_files)
                
                try:
                    video_urls = _self.data_manager.load_json(video_urls_file)
                    sheet_name = Path(video_urls_file).stem
                    
                    for video_url in video_urls:
                        video_id = _self.data_manager.get_video_id(video_url)
                        
                        all_reviewed = True
                        video_captions = {}
                        
                        for config in configs:
                            config_output_dir = os.path.join(
                                str(_self.folder_path),
                                _self.app_config.output_dir, 
                                config["output_name"]
                            )
                            
                            status, _, _, _, _ = _self.data_manager.get_video_status(
                                video_id, config_output_dir
                            )
                            
                            if status not in ["approved", "rejected"]:
                                all_reviewed = False
                                break
                            
                            feedback_data = _self.data_manager.load_data(
                                video_id, config_output_dir, _self.data_manager.FEEDBACK_FILE_POSTFIX
                            )
                            
                            if feedback_data:
                                video_captions[config["task"]] = {
                                    "final_caption": feedback_data.get("final_caption", ""),
                                    "task": config["task"],
                                    "status": status
                                }
                            else:
                                all_reviewed = False
                                break
                        
                        if all_reviewed and len(video_captions) == 5:
                            reviewed_videos.append({
                                "video_id": video_id,
                                "video_url": video_url,
                                "sheet_name": sheet_name,
                                "captions": video_captions
                            })
                
                except Exception as e:
                    continue
            
            progress_bar.empty()
        
        except Exception as e:
            st.error(f"Error loading configurations: {e}")
        
        return reviewed_videos
    
    def format_captions_for_prompt(self, captions: Dict[str, str]) -> str:
        """Format captions for inclusion in prompt"""
        formatted_parts = []
        for caption_type in ["Subject", "Scene", "Motion", "Spatial", "Camera"]:
            if caption_type in captions:
                formatted_parts.append(f"{caption_type}: {captions[caption_type]}")
        return "\n\n".join(formatted_parts)
    
    @st.cache_data
    def calculate_statistics(_self, reviewed_videos: List[Dict[str, Any]]) -> Optional[Dict[str, Dict[str, float]]]:
        """Calculate token and word count statistics across all reviewed videos"""
        token_counts = []
        word_counts = []
        
        progress_bar = st.progress(0, text="Calculating statistics...")
        total = len(reviewed_videos)
        
        for idx, video_data in enumerate(reviewed_videos):
            progress_bar.progress((idx + 1) / total, 
                                 text=f"Calculating statistics... ({idx + 1}/{total})")
            
            # Get captions from video_data
            video_captions_data = video_data.get("captions", {})
            
            # Convert to the format expected by format_captions_for_prompt
            captions = {}
            for task_name, caption_info in video_captions_data.items():
                short_name = _self.task_name_map.get(task_name, task_name)
                captions[short_name] = caption_info.get("final_caption", "")
            
            # Only include videos with all 5 captions
            if len(captions) == 5:
                combined_text = _self.format_captions_for_prompt(captions)
                token_counts.append(count_tokens(combined_text, _self.tokenizer, _self.use_tokenizer))
                word_counts.append(count_words(combined_text))
        
        progress_bar.empty()
        
        if not token_counts:
            return None
        
        return {
            "tokens": {
                "mean": float(np.mean(token_counts)),
                "std": float(np.std(token_counts)),
                "min": float(np.min(token_counts)),
                "max": float(np.max(token_counts)),
                "count": len(token_counts)
            },
            "words": {
                "mean": float(np.mean(word_counts)),
                "std": float(np.std(word_counts)),
                "min": float(np.min(word_counts)),
                "max": float(np.max(word_counts)),
                "count": len(word_counts)
            }
        }
    
    def render_statistics_section(self, reviewed_videos: List[Dict[str, Any]]):
        """Render statistics section"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("📊 Dataset Statistics (Input Captions)")
        
        with col2:
            if st.button("🔄 Refresh", key="refresh_stats"):
                st.cache_data.clear()
                st.rerun()
        
        stats = self.calculate_statistics(reviewed_videos)
        
        if stats:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Token Counts (UMT5-XXL)**")
                st.metric("Mean ± Std", f"{stats['tokens']['mean']:.1f} ± {stats['tokens']['std']:.1f}")
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.metric("Min", f"{stats['tokens']['min']:.0f}")
                with subcol2:
                    st.metric("Max", f"{stats['tokens']['max']:.0f}")
                st.caption(f"Based on {stats['tokens']['count']} videos")
            
            with col2:
                st.markdown("**Word Counts**")
                st.metric("Mean ± Std", f"{stats['words']['mean']:.1f} ± {stats['words']['std']:.1f}")
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.metric("Min", f"{stats['words']['min']:.0f}")
                with subcol2:
                    st.metric("Max", f"{stats['words']['max']:.0f}")
                st.caption(f"Based on {stats['words']['count']} videos")
        else:
            st.info("No videos with all 5 caption types found")
    
    def calculate_video_token_counts(self, reviewed_videos: List[Dict[str, Any]]) -> Dict[str, int]:
        """Pre-calculate token counts for all videos (done once, outside fragment)"""
        video_token_counts = {}
        
        for video in reviewed_videos:
            video_id = video["video_id"]
            captions = {}
            for task_name, caption_info in video.get("captions", {}).items():
                short_name = self.task_name_map.get(task_name, task_name)
                captions[short_name] = caption_info.get("final_caption", "")
            
            if len(captions) == 5:
                combined_text = self.format_captions_for_prompt(captions)
                video_token_counts[video_id] = count_tokens(combined_text, self.tokenizer, self.use_tokenizer)
        
        return video_token_counts
    
    @st.fragment
    def render_video_and_generation(self, reviewed_videos: List[Dict[str, Any]], video_token_counts: Dict[str, int], selected_task: str):
        """Render video selection AND generation interface in ONE fragment"""
        st.subheader("📹 Video Selection")
        
        if not reviewed_videos:
            st.warning("No reviewed videos found")
            return
        
        # Build video data map
        video_data_map = {}
        for video in reviewed_videos:
            video_id = video["video_id"]
            if video_id not in video_data_map:
                video_data_map[video_id] = video
        
        video_ids = list(video_data_map.keys())
        
        # Sorting controls
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            sort_by = st.selectbox(
                "Sort by:",
                ["Token Count", "Video ID"],
                key="sort_by"
            )
        
        with col2:
            if sort_by == "Token Count":
                sort_order = st.selectbox(
                    "Order:",
                    ["Descending", "Ascending"],
                    key="sort_order"
                )
            else:
                sort_order = None
        
        with col3:
            st.metric("Total", len(video_ids))
        
        # Sort videos
        if sort_by == "Token Count":
            video_ids = sorted(
                video_ids,
                key=lambda vid: video_token_counts.get(vid, 0),
                reverse=(sort_order == "Descending")
            )
        
        # FAST VIDEO SELECTION: Use number_input + search instead of huge selectbox
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Search box for filtering
            search_query = st.text_input(
                "🔍 Search video ID:",
                key="video_search",
                placeholder="Type to filter videos..."
            )
        
        with col2:
            # Index-based selection (much faster than 2400-item selectbox)
            if search_query:
                # Filter videos by search query
                filtered_ids = [vid for vid in video_ids if search_query.lower() in vid.lower()]
                if filtered_ids:
                    video_index = st.number_input(
                        f"# (1-{len(filtered_ids)})",
                        min_value=1,
                        max_value=len(filtered_ids),
                        value=1,
                        step=1,
                        key="video_idx_filt"
                    )
                    selected_video_id = filtered_ids[video_index - 1]
                else:
                    st.warning("No matching videos")
                    return
            else:
                # Show all videos
                video_index = st.number_input(
                    f"Video # (1-{len(video_ids)})",
                    min_value=1,
                    max_value=len(video_ids),
                    value=1,
                    step=1,
                    key="video_idx_all"
                )
                selected_video_id = video_ids[video_index - 1]
        
        # Get video data
        selected_video_data = video_data_map.get(selected_video_id)
        selected_video_url = selected_video_data.get("video_url") if selected_video_data else None
        
        # Display current video info
        token_count = video_token_counts.get(selected_video_id, 0)
        st.info(f"**Current:** {selected_video_id} ({token_count} tokens)")
        
        # Display video
        if selected_video_id and selected_video_url:
            st.write("---")
            st.write("### 🎥 Video Preview")
            st.video(selected_video_url)
            st.caption(f"**Video ID:** {selected_video_id}")
        
        # Generation interface (same fragment, right below video)
        if not selected_video_data:
            return
        
        st.divider()
        st.subheader(f"🤖 {self.TASKS[selected_task]['name']}")
        
        # Get captions
        captions = {}
        for task_name, caption_info in selected_video_data.get("captions", {}).items():
            short_name = self.task_name_map.get(task_name, task_name)
            captions[short_name] = caption_info.get("final_caption", "")
        
        if len(captions) != 5:
            st.error(f"Video only has {len(captions)} caption types. Need all 5.")
            return
        
        # Format and display captions
        combined_text = self.format_captions_for_prompt(captions)
        
        st.write("### 📋 Input Captions")
        with st.container(border=True):
            st.code(combined_text, language="text")
        
        # Display counts
        input_tokens = count_tokens(combined_text, self.tokenizer, self.use_tokenizer)
        input_words = count_words(combined_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Input Tokens", input_tokens)
        with col2:
            st.metric("Input Words", input_words)
        
        # Instruction editing
        st.write("### ✏️ Generation Instruction")
        
        default_instruction = self.TASKS[selected_task]["default_instruction"]
        
        if selected_task == "json_generation":
            combined_json_policy = self.get_combined_json_policy()
            if combined_json_policy:
                json_policy_str = json.dumps(combined_json_policy, indent=2)
                default_instruction = default_instruction.replace("{json_policy}", json_policy_str)
        
        instruction = st.text_area(
            "Edit instruction:",
            value=default_instruction,
            height=400,
            key=f"instruction_{selected_video_id}"
        )
        
        # LLM selection
        col1, col2 = st.columns(2)
        with col1:
            available_llms = get_all_llms()
            selected_llm = st.selectbox(
                "Select LLM:",
                available_llms,
                index=available_llms.index("gpt-5.2") if "gpt-5.2" in available_llms else 0,
                key=f"llm_{selected_video_id}"
            )
        
        with col2:
            generate_clicked = st.button("🚀 Generate", type="primary", use_container_width=True, key=f"gen_{selected_video_id}")
        
        # Generation
        if generate_clicked:
            if "{captions}" not in instruction:
                st.error("Instruction must contain {captions} placeholder!")
            else:
                self.generate_output(instruction, captions, selected_llm, selected_task)
    
    def generate_output(self, instruction: str, captions: Dict[str, str], selected_llm: str, task_type: str):
        """Generate output using LLM"""
        try:
            formatted_captions = self.format_captions_for_prompt(captions)
            final_prompt = instruction.replace("{captions}", formatted_captions)
            
            with st.expander("View Full Prompt"):
                st.code(final_prompt, language="text")
            
            st.write("### 🔄 Generating...")
            with st.spinner(f"Calling {selected_llm}..."):
                try:
                    llm = get_llm(model=selected_llm, secrets=st.secrets)
                    response = llm.generate(final_prompt)
                except (TypeError, KeyError) as e:
                    st.error("❌ LLM API key not configured properly.")
                    return
            
            if not response or not response.strip():
                st.error("⚠️ LLM returned an empty response.")
                return
            
            # Clean response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            elif response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Display results
            st.write("### ✅ Generated Output")
            
            output_tokens = count_tokens(response, self.tokenizer, self.use_tokenizer)
            output_words = count_words(response)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Output Tokens", output_tokens)
            with col2:
                st.metric("Output Words", output_words)
            with col3:
                # Word limit check for combined caption
                if task_type == "summary_generation":
                    if output_words <= 320:
                        st.metric("Word Limit", "✅ PASS", delta=f"{output_words}/320")
                    else:
                        st.metric("Word Limit", "❌ FAIL", delta=f"{output_words}/320", delta_color="inverse")
            
            if task_type == "json_generation":
                try:
                    json_obj = json.loads(response)
                    st.code(json.dumps(json_obj, indent=2), language="json")
                    st.success("✅ Valid JSON!")
                except json.JSONDecodeError as e:
                    st.error(f"⚠️ Invalid JSON: {e}")
                    with st.expander("🔍 View Raw Response", expanded=True):
                        st.code(response)
            else:
                # Combined caption generation
                with st.container(border=True):
                    st.write(response)
                
                # Show warning if over 320 words
                if output_words > 320:
                    st.warning(f"⚠️ Caption exceeds 320 word limit ({output_words} words). Consider regenerating with stricter instructions.")
            
        except Exception as e:
            st.error(f"Error: {e}")
    
    def run(self):
        """Main application entry point"""
        st.title("🤖 Multi-Caption LLM Testing Interface")
        st.markdown("Generate combined captions or structured JSON from all five caption types")
        
        if self.tokenizer_error:
            st.warning(f"⚠️ {self.tokenizer_error}")
        
        # Load videos once
        if 'reviewed_videos' not in st.session_state:
            st.session_state.reviewed_videos = self.get_all_reviewed_videos()
        
        reviewed_videos = st.session_state.reviewed_videos
        
        # Sidebar: Task selection
        with st.sidebar:
            st.header("🎯 Task Selection")
            
            task_options = {
                "summary_generation": self.TASKS["summary_generation"]["name"],
                "json_generation": self.TASKS["json_generation"]["name"]
            }
            
            selected_task = st.radio(
                "Select Task:",
                list(task_options.keys()),
                format_func=lambda x: task_options[x],
                key="selected_task"
            )
            
            st.info(self.TASKS[selected_task]["description"])
        
        # Main content - SINGLE COLUMN
        if not reviewed_videos:
            st.warning("No videos found")
            return
        
        # Display statistics at the top
        self.render_statistics_section(reviewed_videos)
        st.divider()
        
        # Pre-calculate token counts ONCE (outside fragment for speed)
        if 'video_token_counts' not in st.session_state:
            st.session_state.video_token_counts = self.calculate_video_token_counts(reviewed_videos)
        
        # Video selection AND generation interface (ONE fragment - fast switching!)
        self.render_video_and_generation(reviewed_videos, st.session_state.video_token_counts, selected_task)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Multi-Caption LLM Testing",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    args = parse_args()
    app = MultiCaptionLLMApp(args.config_type)
    app.run()