#!/usr/bin/env python3
"""
Batch Merged Caption Generation Script

Generates merged captions from all five caption types for videos with complete annotations.
Tracks prompts and captions to avoid unnecessary regeneration.

Usage:
    python generate_merged_captions.py --config-type main
    python generate_merged_captions.py --regenerate-on-prompt-change
    python generate_merged_captions.py --regenerate-all
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np
from tqdm import tqdm

# Import from caption system
from caption.config import get_config
from caption.core.data_manager import DataManager
from llm import get_llm

# Import the prompt and app class from the streamlit app
try:
    from caption.json_and_summary_caption_streamlit import MultiCaptionLLMApp
    PROMPT_IMPORTED = True
except ImportError:
    print("Warning: Could not import from caption.json_and_summary_caption_streamlit")
    print("Make sure the file exists at caption/json_and_summary_caption_streamlit.py")
    PROMPT_IMPORTED = False
    # Fallback prompt will be set in the class


# Constants
MAX_TOKEN_LENGTH = 512  # Maximum allowed token length for merged captions


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Batch Merged Caption Generation")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument("--llm", type=str, default="gpt-4o-2024-08-06",
                       help="LLM model to use for generation")
    parser.add_argument("--output-dir", type=str, default="caption/merged_captions",
                       help="Output directory for merged captions")
    parser.add_argument("--regenerate-on-prompt-change", action="store_true", default=True,
                       help="Regenerate captions if prompt has changed (default: True)")
    parser.add_argument("--regenerate-on-caption-change", action="store_true", default=True,
                       help="Regenerate captions if any of the 5 input captions have changed (default: True)")
    parser.add_argument("--regenerate-all", action="store_true",
                       help="Regenerate all captions regardless of existing files")
    parser.add_argument("--skip-prompt-check", action="store_true",
                       help="Skip regeneration on prompt changes")
    parser.add_argument("--skip-caption-check", action="store_true",
                       help="Skip regeneration on caption changes")
    parser.add_argument("--dry-run", action="store_true",
                       help="Print statistics only, don't generate any captions")
    return parser.parse_args()


def count_tokens(text: str) -> int:
    """Approximate token count (0.75 words per token)"""
    return int(len(text.split()) / 0.75)


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())


class MergedCaptionGenerator:
    """Generate merged captions from five caption types"""
    
    # Task name mapping (same as streamlit app)
    TASK_NAME_MAP = {
        "subject_description": "Subject",
        "scene_composition_dynamics": "Scene",
        "subject_motion_dynamics": "Motion",
        "spatial_framing_dynamics": "Spatial",
        "camera_framing_dynamics": "Camera",
    }
    
    def __init__(self, args):
        self.args = args
        self.app_config = get_config(args.config_type)
        
        # Handle skip flags (override defaults)
        if args.skip_prompt_check:
            args.regenerate_on_prompt_change = False
        if args.skip_caption_check:
            args.regenerate_on_caption_change = False
        
        # Set up paths - detect if running from root or from script location
        script_path = Path(__file__).resolve()
        
        # If script is in root directory (video_annotation/)
        if script_path.parent.name == "video_annotation" or (script_path.parent / "caption").exists():
            self.root_path = script_path.parent
        # If script is somewhere else, try to find caption directory
        else:
            # Try current working directory
            cwd = Path.cwd()
            if (cwd / "caption").exists():
                self.root_path = cwd
            else:
                raise ValueError(f"Cannot locate project root. Script at: {script_path}, CWD: {cwd}")
        
        self.folder_path = self.root_path / "caption"
        
        # Verify caption directory exists
        if not self.folder_path.exists():
            raise ValueError(f"Caption directory not found at: {self.folder_path}")
        
        print(f"Root path: {self.root_path}")
        print(f"Caption folder: {self.folder_path}")
        
        self.output_dir = self.root_path / args.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data manager
        self.data_manager = DataManager(self.folder_path, self.root_path)
        
        # Get the prompt from the imported app
        if PROMPT_IMPORTED:
            # Create a temporary app instance to get the prompt
            temp_app = MultiCaptionLLMApp(args.config_type)
            self.merged_caption_prompt_template = temp_app.TASKS["summary_generation"]["default_instruction"]
            print("✓ Successfully imported prompt from caption.json_and_summary_caption_streamlit")
        else:
            # Fallback prompt (should not be used in production)
            print("⚠ Using fallback prompt - update caption/json_and_summary_caption_streamlit.py if this is incorrect")
            self.merged_caption_prompt_template = """Please merge the following five captions into a single, comprehensive caption that describes the video completely without any redundancy.

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
5. Preserve the EXACT wording from the original captions - do NOT paraphrase
6. When describing temporal changes, integrate motion and camera movements in chronological order to show how the scene evolves
7. CRITICAL: Every unique detail from all five captions must appear in the final merged caption - nothing should be omitted
8. Do NOT add any information not present in the original captions
9. Return only the merged caption without any additional text or formatting

Goal: A single, temporally coherent caption based on the Spatial description, with Motion and Camera information merged chronologically, and Subject/Scene details added only when they provide new information. Keep as many details as possible but limit to at most 320 words."""
        
        # Load secrets for LLM
        try:
            import streamlit as st
            self.secrets = st.secrets
        except:
            # Fallback to loading from .streamlit/secrets.toml
            secrets_file = self.root_path / ".streamlit" / "secrets.toml"
            if secrets_file.exists():
                import toml
                self.secrets = toml.load(secrets_file)
            else:
                raise ValueError("Cannot load secrets. Please ensure .streamlit/secrets.toml exists")
        
        # Initialize LLM
        if not args.dry_run:
            print(f"Initializing LLM: {args.llm}")
            self.llm = get_llm(model=args.llm, secrets=self.secrets)
        else:
            self.llm = None
        
        # Statistics
        self.stats = {
            "total_videos": 0,
            "already_generated": 0,
            "prompt_changed": 0,
            "caption_changed": 0,
            "needs_generation": 0,
            "successfully_generated": 0,
            "failed": 0
        }
    
    def format_captions_for_prompt(self, captions: Dict[str, str]) -> str:
        """Format captions for inclusion in prompt (same as streamlit app)"""
        formatted_parts = []
        for caption_type in ["Subject", "Scene", "Motion", "Spatial", "Camera"]:
            if caption_type in captions:
                formatted_parts.append(f"{caption_type}: {captions[caption_type]}")
        return "\n\n".join(formatted_parts)
    
    def get_all_reviewed_videos(self) -> List[Dict[str, Any]]:
        """Get all videos that have been fully reviewed across all tasks"""
        reviewed_videos = []
        
        # Load configs
        configs = self.data_manager.load_config(self.app_config.configs_file)
        if isinstance(configs[0], str):
            configs = [self.data_manager.load_config(config) for config in configs]
        
        print("Loading reviewed videos...")
        
        # Check all video URL files
        for video_urls_file in tqdm(self.app_config.video_urls_files, desc="Scanning video files"):
            try:
                video_urls = self.data_manager.load_json(video_urls_file)
                sheet_name = Path(video_urls_file).stem
                
                for video_url in video_urls:
                    video_id = self.data_manager.get_video_id(video_url)
                    
                    # Check if ALL tasks are completed and reviewed
                    all_reviewed = True
                    video_captions = {}
                    
                    for config in configs:
                        config_output_dir = os.path.join(
                            str(self.folder_path),
                            self.app_config.output_dir, 
                            config["output_name"]
                        )
                        
                        # Get video status
                        status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                            video_id, config_output_dir
                        )
                        
                        # Only "approved" and "rejected" count as reviewed
                        if status not in ["approved", "rejected"]:
                            all_reviewed = False
                            break
                        
                        # Load feedback data to get final caption
                        feedback_data = self.data_manager.load_data(
                            video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
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
                    
                    # Only add video if ALL tasks are reviewed AND we have exactly 5 captions
                    if all_reviewed and len(video_captions) == 5:
                        reviewed_videos.append({
                            "video_id": video_id,
                            "video_url": video_url,
                            "sheet_name": sheet_name,
                            "captions": video_captions
                        })
            
            except Exception as e:
                print(f"Warning: Error processing {video_urls_file}: {e}")
                continue
        
        self.stats["total_videos"] = len(reviewed_videos)
        print(f"\nFound {len(reviewed_videos)} videos with all 5 reviewed captions")
        
        return reviewed_videos
    
    def get_output_path(self, video_id: str) -> Path:
        """Get output path for merged caption"""
        return self.output_dir / f"{video_id}.json"
    
    def load_existing_output(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Load existing merged caption if it exists"""
        output_path = self.get_output_path(video_id)
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def should_regenerate(self, video_id: str, video_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Determine if caption should be regenerated
        Returns: (should_regenerate, reason)
        """
        # Load existing output
        existing = self.load_existing_output(video_id)
        
        if existing is None:
            return True, "not_yet_generated"
        
        if self.args.regenerate_all:
            return True, "regenerate_all_flag"
        
        # Check if prompt changed (default: True unless --skip-prompt-check)
        if self.args.regenerate_on_prompt_change:
            existing_prompt = existing.get("prompt", "")
            current_prompt = self.merged_caption_prompt_template
            if existing_prompt != current_prompt:
                return True, "prompt_changed"
        
        # Check if input captions changed (default: True unless --skip-caption-check)
        if self.args.regenerate_on_caption_change:
            existing_captions = existing.get("input_captions", {})
            
            # Get current captions
            current_captions = {}
            for task_name, caption_info in video_data.get("captions", {}).items():
                short_name = self.TASK_NAME_MAP.get(task_name, task_name)
                current_captions[short_name] = caption_info.get("final_caption", "")
            
            # Compare
            if existing_captions != current_captions:
                return True, "caption_changed"
        
        return False, "already_generated"
    
    def analyze_videos(self, reviewed_videos: List[Dict[str, Any]]):
        """Analyze videos and print statistics before generation"""
        print("\n" + "="*80)
        print("PRE-GENERATION ANALYSIS")
        print("="*80)
        
        for video_data in tqdm(reviewed_videos, desc="Analyzing videos"):
            video_id = video_data["video_id"]
            should_regen, reason = self.should_regenerate(video_id, video_data)
            
            if reason == "already_generated":
                self.stats["already_generated"] += 1
            elif reason == "prompt_changed":
                self.stats["prompt_changed"] += 1
                self.stats["needs_generation"] += 1
            elif reason == "caption_changed":
                self.stats["caption_changed"] += 1
                self.stats["needs_generation"] += 1
            elif reason == "not_yet_generated":
                self.stats["needs_generation"] += 1
            elif reason == "regenerate_all_flag":
                self.stats["needs_generation"] += 1
        
        # Print statistics
        print(f"\n📊 Video Status Summary:")
        print(f"  Total videos with 5 captions: {self.stats['total_videos']}")
        print(f"  Already generated (up-to-date): {self.stats['already_generated']}")
        print(f"  Prompt changed: {self.stats['prompt_changed']}")
        print(f"  Caption changed: {self.stats['caption_changed']}")
        print(f"  Not yet generated: {self.stats['needs_generation'] - self.stats['prompt_changed'] - self.stats['caption_changed']}")
        print(f"  Total needs generation: {self.stats['needs_generation']}")
        print(f"\n{'='*80}\n")
    
    def generate_merged_caption(self, video_id: str, video_data: Dict[str, Any]) -> Optional[str]:
        """Generate merged caption for a video"""
        # Get captions
        video_captions_data = video_data.get("captions", {})
        captions = {}
        for task_name, caption_info in video_captions_data.items():
            short_name = self.TASK_NAME_MAP.get(task_name, task_name)
            captions[short_name] = caption_info.get("final_caption", "")
        
        if len(captions) != 5:
            print(f"  ⚠️ Warning: {video_id} only has {len(captions)} captions")
            return None
        
        # Format captions for prompt
        formatted_captions = self.format_captions_for_prompt(captions)
        
        # Create final prompt using the imported prompt template
        final_prompt = self.merged_caption_prompt_template.replace("{captions}", formatted_captions)
        
        try:
            # Generate
            response = self.llm.generate(final_prompt)
            
            # Clean response
            if not response or not response.strip():
                print(f"  ⚠️ Warning: Empty response for {video_id}")
                return None
            
            response = response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith('```'):
                lines = response.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                response = '\n'.join(lines).strip()
            
            # Save output
            output_data = {
                "video_id": video_id,
                "merged_caption": response,
                "input_captions": captions,
                "prompt": self.merged_caption_prompt_template,
                "llm_model": self.args.llm,
                "timestamp": datetime.now().isoformat(),
                "input_token_count": count_tokens(formatted_captions),
                "input_word_count": count_words(formatted_captions),
                "output_token_count": count_tokens(response),
                "output_word_count": count_words(response)
            }
            
            output_path = self.get_output_path(video_id)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            return response
            
        except Exception as e:
            print(f"  ❌ Error generating caption for {video_id}: {e}")
            return None
    
    def run(self):
        """Main execution"""
        print("\n" + "="*80)
        print("MERGED CAPTION BATCH GENERATION")
        print("="*80)
        print(f"Config: {self.args.config_type}")
        print(f"LLM: {self.args.llm}")
        print(f"Output directory: {self.output_dir}")
        print(f"Regenerate on prompt change: {self.args.regenerate_on_prompt_change}")
        print(f"Regenerate on caption change: {self.args.regenerate_on_caption_change}")
        print(f"Regenerate all: {self.args.regenerate_all}")
        print(f"Dry run: {self.args.dry_run}")
        print("="*80 + "\n")
        
        # Get all reviewed videos
        reviewed_videos = self.get_all_reviewed_videos()
        
        if not reviewed_videos:
            print("No videos found with all 5 reviewed captions.")
            return
        
        # Analyze videos
        self.analyze_videos(reviewed_videos)
        
        if self.args.dry_run:
            print("Dry run mode - no captions generated.")
            return
        
        if self.stats["needs_generation"] == 0:
            print("All captions are up-to-date. Nothing to generate.")
        else:
            # Generate captions
            print(f"Generating {self.stats['needs_generation']} merged captions...")
            print("="*80 + "\n")
            
            for video_data in tqdm(reviewed_videos, desc="Generating captions"):
                video_id = video_data["video_id"]
                should_regen, reason = self.should_regenerate(video_id, video_data)
                
                if should_regen:
                    result = self.generate_merged_caption(video_id, video_data)
                    if result:
                        self.stats["successfully_generated"] += 1
                    else:
                        self.stats["failed"] += 1
        
        # Final statistics
        print("\n" + "="*80)
        print("GENERATION SUMMARY")
        print("="*80)
        print(f"Successfully generated: {self.stats['successfully_generated']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped (up-to-date): {self.stats['already_generated']}")
        print("="*80 + "\n")
        
        # Compute token/word statistics
        self.compute_final_statistics()
    
    def compute_final_statistics(self):
        """Compute final token and word count statistics"""
        print("\n" + "="*80)
        print("TOKEN & WORD COUNT STATISTICS")
        print("="*80)
        
        # Load all generated merged captions
        input_tokens = []
        input_words = []
        output_tokens = []
        output_words = []
        videos_exceeding_limit = []  # Track videos exceeding MAX_TOKEN_LENGTH
        
        for file_path in self.output_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                input_tokens.append(data.get("input_token_count", 0))
                input_words.append(data.get("input_word_count", 0))
                output_token_count = data.get("output_token_count", 0)
                output_tokens.append(output_token_count)
                output_words.append(data.get("output_word_count", 0))
                
                # Check if exceeds limit
                if output_token_count > MAX_TOKEN_LENGTH:
                    videos_exceeding_limit.append({
                        "video_id": data.get("video_id", file_path.stem),
                        "token_count": output_token_count,
                        "word_count": data.get("output_word_count", 0)
                    })
            except:
                continue
        
        if not input_tokens:
            print("No merged captions found for statistics.")
            return
        
        # Compute statistics
        print(f"\n📊 Statistics based on {len(input_tokens)} merged captions:")
        print("\n" + "-"*80)
        print("INPUT CAPTIONS (Combined 5 captions):")
        print("-"*80)
        print(f"  Token Count:")
        print(f"    Mean: {np.mean(input_tokens):.1f}")
        print(f"    Std:  {np.std(input_tokens):.1f}")
        print(f"    Min:  {np.min(input_tokens):.0f}")
        print(f"    Max:  {np.max(input_tokens):.0f}")
        print(f"\n  Word Count:")
        print(f"    Mean: {np.mean(input_words):.1f}")
        print(f"    Std:  {np.std(input_words):.1f}")
        print(f"    Min:  {np.min(input_words):.0f}")
        print(f"    Max:  {np.max(input_words):.0f}")
        
        print("\n" + "-"*80)
        print("MERGED CAPTIONS:")
        print("-"*80)
        print(f"  Token Count:")
        print(f"    Mean: {np.mean(output_tokens):.1f}")
        print(f"    Std:  {np.std(output_tokens):.1f}")
        print(f"    Min:  {np.min(output_tokens):.0f}")
        print(f"    Max:  {np.max(output_tokens):.0f}")
        print(f"\n  Word Count:")
        print(f"    Mean: {np.mean(output_words):.1f}")
        print(f"    Std:  {np.std(output_words):.1f}")
        print(f"    Min:  {np.min(output_words):.0f}")
        print(f"    Max:  {np.max(output_words):.0f}")
        
        # Compute reduction statistics
        token_reduction = (1 - np.array(output_tokens) / np.array(input_tokens)) * 100
        word_reduction = (1 - np.array(output_words) / np.array(input_words)) * 100
        
        print("\n" + "-"*80)
        print("REDUCTION (Input → Merged):")
        print("-"*80)
        print(f"  Token Reduction:")
        print(f"    Mean: {np.mean(token_reduction):.1f}%")
        print(f"    Std:  {np.std(token_reduction):.1f}%")
        print(f"    Min:  {np.min(token_reduction):.1f}%")
        print(f"    Max:  {np.max(token_reduction):.1f}%")
        print(f"\n  Word Reduction:")
        print(f"    Mean: {np.mean(word_reduction):.1f}%")
        print(f"    Std:  {np.std(word_reduction):.1f}%")
        print(f"    Min:  {np.min(word_reduction):.1f}%")
        print(f"    Max:  {np.max(word_reduction):.1f}%")
        
        # Report videos exceeding token limit
        print("\n" + "-"*80)
        print(f"VIDEOS EXCEEDING {MAX_TOKEN_LENGTH} TOKENS:")
        print("-"*80)
        
        if videos_exceeding_limit:
            # Sort by token count (descending)
            videos_exceeding_limit.sort(key=lambda x: x["token_count"], reverse=True)
            
            print(f"  Found {len(videos_exceeding_limit)} videos exceeding {MAX_TOKEN_LENGTH} tokens:")
            print(f"  ({len(videos_exceeding_limit) / len(input_tokens) * 100:.1f}% of total)\n")
            
            for i, video_info in enumerate(videos_exceeding_limit, 1):
                print(f"  {i:3d}. {video_info['video_id']}")
                print(f"       Tokens: {video_info['token_count']} ({video_info['token_count'] - MAX_TOKEN_LENGTH} over limit)")
                print(f"       Words:  {video_info['word_count']}")
        else:
            print(f"  ✓ All videos are within the {MAX_TOKEN_LENGTH} token limit!")
        
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    args = parse_args()
    generator = MergedCaptionGenerator(args)
    generator.run()