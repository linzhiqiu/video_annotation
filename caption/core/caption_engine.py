# caption/core/caption_engine.py
import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path

from llm import get_llm
from caption.core.video_utils import VideoUtils
from caption.core.data_manager import DataManager


class CaptionEngine:
    """Handles caption generation and processing"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.video_utils = VideoUtils()
    
    def generate_precaption(self, video_id: str, output_dir: str, prompt: str, 
                           selected_llm: str, selected_mode: str, selected_video: str) -> str:
        """Generate and save precaption"""
        print(f"Generating pre-caption for video: {video_id}")
        imagery_kwargs = self.video_utils.get_imagery_kwargs(selected_mode, selected_video)
        
        try:
            pre_caption = get_llm(
                model=selected_llm,
                secrets=st.secrets,
            ).generate(
                prompt,
                **imagery_kwargs
            )
        except Exception as e:
            st.error(f"Error generating pre-caption for video: {video_id}")
            st.error(f"Error: {e}")
            # If the selected_llm is gemini-2.5-pro, prompt user to try again or use gpt-4.1-2025-04-14
            if selected_llm in ["gemini-2.5-pro", "gemini-3-pro-preview"]:
                st.info("Please try again or use gpt-4.1-2025-04-14 as the LLM.")
            raise e
        
        pre_caption_data = {
            "video_id": video_id,
            "pre_caption_prompt": prompt,
            "pre_caption": pre_caption,
            "pre_caption_llm": selected_llm,
            "pre_caption_mode": selected_mode,
        }
        self.data_manager.save_data(video_id, pre_caption_data, output_dir=output_dir, 
                                   file_postfix=self.data_manager.PRECAPTION_FILE_POSTFIX)
        print(f"Pre-caption generated for video: {video_id}")
        return pre_caption
    
    def get_precaption_llm_name(self, config_dict: Dict[str, Any], selected_config: str) -> str:
        """Get appropriate LLM for precaption based on task"""
        config = config_dict[selected_config]
        task = config["task"]
        
        if task in ["subject_motion_dynamics"]:
            return "gemini-2.5-pro"
        elif task in ["spatial_framing_dynamics"]:
            return "gemini-2.5-pro"
        elif task in ["raw_lighting_setup_dynamics", "raw_lighting_effects_dynamics"]:
            print(f"Using gemini-2.5-pro for {task}")
            return "gemini-2.5-pro"
        else:
            return "gemini-2.5-pro"
    
    def load_pre_caption_prompt(self, video_id: str, video_data_dict: Dict[str, Any], 
                               caption_program: Any, config_dict: Dict[str, Any], 
                               selected_config: str, output_dir: str) -> str:
        """Load and prepare precaption prompt"""
        config = config_dict[selected_config]
        task = config["task"]
        
        # Constants for subject and scene caption names
        SUBJECT_CAPTION_NAME = "Subject Description Caption"
        SCENE_CAPTION_NAME = "Scene Composition and Dynamics Caption"
        
        if task in ["subject_motion_dynamics"]:
            # Need to update the "subject_description" if exists
            subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
            existing_subject_feedback = self.data_manager.load_data(
                video_id, 
                output_dir=Path(output_dir).parent / subject_output_name, 
                file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX
            )
            if existing_subject_feedback:
                st.success("Loading previously generated subject caption...")
                subject_caption = existing_subject_feedback["final_caption"]
                video_data_dict[video_id].cam_setup.subject_description = subject_caption
            else:
                st.error("No subject caption found. Please generate the subject caption first.")
                st.rerun()
                raise ValueError("This line will not be run because rerun will be called.")
                
        elif task in ["spatial_framing_dynamics", "color_composition_dynamics", 
                     "lighting_setup_dynamics", "lighting_effects_dynamics"]:
            # Need to update both "subject_description" and "scene_composition_dynamics" if exists
            subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
            scene_output_name = config_dict[SCENE_CAPTION_NAME]["output_name"]
            
            existing_subject_feedback = self.data_manager.load_data(
                video_id,
                output_dir=Path(output_dir).parent / subject_output_name,
                file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX
            )
            existing_scene_feedback = self.data_manager.load_data(
                video_id,
                output_dir=Path(output_dir).parent / scene_output_name,
                file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX
            )
            
            if existing_subject_feedback and existing_scene_feedback:
                st.success("Loading previously generated subject and scene captions...")
                subject_caption = existing_subject_feedback["final_caption"]
                scene_caption = existing_scene_feedback["final_caption"] 
                video_data_dict[video_id].cam_setup.subject_description = subject_caption
                video_data_dict[video_id].cam_setup.scene_description = scene_caption
            else:
                st.error("No subject and scene captions found. Please generate the subject and scene captions first.")
                st.rerun()
                raise ValueError("This line will not be run because rerun will be called.")
        
        # Generate the new prompt and caption
        pre_caption_prompt = caption_program(video_data_dict[video_id])[task]
        return pre_caption_prompt
    
    def load_precaption(self, video_id: str, output_dir: str) -> Dict[str, Any]:
        """Load pre-caption for video. If not exist, return empty dict."""
        existing_precaption = self.data_manager.load_data(
            video_id, output_dir=output_dir, 
            file_postfix=self.data_manager.PRECAPTION_FILE_POSTFIX
        )
        
        if existing_precaption:
            return existing_precaption
        else:
            st.info("No pre-caption found. Generating a new pre-caption.")
            return {}
    
    def generate_feedback(self, prompt: str, llm_name: str, initial_feedback: str, pre_caption: str) -> str:
        """Generate polished feedback using GPT"""
        return get_llm(
            model=llm_name,
            secrets=st.secrets,
        ).generate(
            prompt.format(feedback=initial_feedback, pre_caption=pre_caption)
        )
    
    def generate_caption(self, prompt: str, llm_name: str, feedback: str, pre_caption: str) -> str:
        """Generate improved caption using GPT"""
        return get_llm(
            model=llm_name,
            secrets=st.secrets,
        ).generate(
            prompt.format(feedback=feedback, pre_caption=pre_caption)
        )
    
    def copy_feedback_for_precaption(self, configs_path: str, video_urls: list, 
                                   main_project_output: str, personalized_output: str):
        """Copy feedback files from main project output to personalized output directory for precaption purposes"""
        import os
        from pathlib import Path
        
        # Create personalized output directory if it doesn't exist
        os.makedirs(personalized_output, exist_ok=True)
        
        # Process each video
        for video_url in video_urls:
            video_id = self.data_manager.get_video_id(video_url)
            
            # For each config in the main project
            configs = self.data_manager.load_config(Path(configs_path))
            configs = [self.data_manager.load_config(config) for config in configs]
            
            for config in configs:
                # Get the output directory for this config
                config_output_dir = os.path.join(self.data_manager.folder, main_project_output, config["output_name"])

                feedback_file = self.data_manager.get_filename(
                    video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
                )
                
                # If feedback exists in main project, check if precaption already exists
                if os.path.exists(feedback_file):
                    # Create config directory in personalized output
                    personalized_config_dir = os.path.join(self.data_manager.folder, personalized_output, config["output_name"])
                    os.makedirs(personalized_config_dir, exist_ok=True)
                    
                    # Check if precaption file already exists
                    precaption_file = self.data_manager.get_filename(
                        video_id, personalized_config_dir, self.data_manager.PRECAPTION_FILE_POSTFIX
                    )
                    if not os.path.exists(precaption_file):
                        # Only copy if precaption doesn't exist
                        with open(feedback_file, 'r') as src, open(precaption_file, 'w') as dst:
                            dst.write(src.read())
                        print(f"Copied {feedback_file} to {precaption_file}")
                    else:
                        print(f"Skipped copying {feedback_file} as {precaption_file} already exists")
                else:
                    print(f"Skipped copying {feedback_file} as it doesn't exist")