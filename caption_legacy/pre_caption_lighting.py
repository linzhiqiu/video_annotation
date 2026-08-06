import os
import json
from pathlib import Path
from tqdm import tqdm
import argparse
import sys
import streamlit as st

def batch_generate_precaptions(video_urls_files, config_dict, caption_programs, video_data_dict, args, redo=False):
    """
    Batch generate pre-captions for all videos across all configured tasks.
    
    Args:
        video_urls_files (list): List of paths to JSON files containing video URLs
        config_dict (dict): Dictionary of configuration objects
        caption_programs (dict): Dictionary of caption program objects
        video_data_dict (dict): Dictionary of video data objects
        args: Command line arguments containing output directory path
    """
    FOLDER = Path(__file__).parent

    # Load all video URLs from all files
    all_videos = []
    for video_urls_file in video_urls_files:
        with open(FOLDER / video_urls_file, 'r') as f:
            video_urls = json.load(f)
            all_videos.extend(video_urls)

    # Remove duplicates while preserving order
    all_videos = list(dict.fromkeys(all_videos))

    print(f"Processing {len(all_videos)} videos across {len(config_dict)} caption tasks")

    # Modified version of load_pre_caption_prompt without st.rerun()
    def load_pre_caption_prompt_batch(video_id, video_data_dict, caption_program, config_dict, selected_config, output):
        """Generate a pre-caption prompt for the video without st.rerun()"""
        config = config_dict[selected_config]
        task = config["task"]

        try:
            pre_caption_prompt = caption_program(video_data_dict[video_id])[task]
            return pre_caption_prompt
        except Exception as e:
            print(f"Error generating prompt for video {video_id}, task {task}: {str(e)}")
            return None

    # We'll import get_llm and get_supported_mode here to avoid dependencies
    from llm import get_llm, get_supported_mode

    # Loop through all configurations, but always do raw_lighting_setup_dynamics first, without removing other tasks
    for config_name in [
        # "Lighting Setup and Dynamics Caption (Raw)", # TODO: Comment out for now
        "Lighting Effects and Dynamics Caption (Raw)",
    ]:
        config = config_dict.get(config_name)
        if not config:
            print(f"Skipping {config_name}: No valid configuration found")
            continue
        # for config_name, config in tqdm(config_dict.items(), desc="Processing tasks"):
        print(f"\nProcessing task: {config_name}")

        task = config.get("task")
        if not task or task not in caption_programs:
            print(f"Skipping {config_name}: No valid task defined")
            continue

        caption_program = caption_programs[task]
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        os.makedirs(output_dir, exist_ok=True)

        # Select the appropriate LLM for this task
        selected_llm = get_precaption_llm_name(config_dict, config_name)
        try:
            selected_mode = get_supported_mode(selected_llm)[0]  # Just use the first supported mode
        except Exception as e:
            print(f"Error getting supported mode for {selected_llm}: {str(e)}")
            # Default to "Text Only" as fallback
            selected_mode = "Text Only"

        already_exists_count = 0
        not_ready_count = 0
        generated_count = 0
        error_count = 0
        # # First check all prompts are ready
        # for video_url in tqdm(all_videos, desc=f"Videos for {config_name}"):
        #     video_id = get_video_id(video_url)
            
        #     # Skip if video ID not in video_data_dict
        #     if video_id not in video_data_dict:
        #         print(f"Video ID {video_id} not found in video data, skipping")
        #         import pdb; pdb.set_trace()
            
        #     # Skip if pre-caption already exists
        #     # Generate prompt
        #     prompt = load_pre_caption_prompt_batch(video_id, video_data_dict, caption_program, config_dict, config_name, args.output)
        #     if prompt is None:
        #         print(f"Couldn't generate prompt for {video_id} in task {config_name}, skipping")
        #         import pdb; pdb.set_trace()
            
        for video_url in tqdm(all_videos, desc=f"Videos for {config_name}"):
            video_id = get_video_id(video_url)

            # Skip if video ID not in video_data_dict
            if video_id not in video_data_dict:
                print(f"Video ID {video_id} not found in video data, skipping")
                import pdb; pdb.set_trace()

            # Skip if pre-caption already exists
            if data_is_saved(video_id, output_dir=output_dir, file_postfix=PRECAPTION_FILE_POSTFIX):
                if not redo:
                    print(f"Pre-caption already exists for {video_id} in task {config_name}, skipping")
                    already_exists_count += 1
                    continue
                else:
                    print(f"Redoing pre-caption for {video_id} in task {config_name}")

            # Generate prompt
            prompt = load_pre_caption_prompt_batch(video_id, video_data_dict, caption_program, config_dict, config_name, args.output)
            if prompt is None:
                print(f"Couldn't generate prompt for {video_id} in task {config_name}, skipping")
                not_ready_count += 1
                continue

            try:
                # Set up imagery kwargs based on selected mode
                imagery_kwargs = get_imagery_kwargs(selected_mode, video_url)

                # Generate pre-caption
                # In feedback_app.py, it uses st.secrets, but for a batch script
                # you may need to handle secrets differently
                try:
                    pre_caption = get_llm(
                        model=selected_llm,
                        secrets=st.secrets
                    ).generate(
                        prompt,
                        **imagery_kwargs
                    )
                except Exception as e:
                    print(f"Error with LLM generation: {str(e)}")
                    # You might want to retry or use a different model here
                    raise

                # Save pre-caption
                pre_caption_data = {
                    "video_id": video_id,
                    "pre_caption_prompt": prompt,
                    "pre_caption": pre_caption,
                    "pre_caption_llm": selected_llm,
                    "pre_caption_mode": selected_mode,
                }

                save_data(video_id, pre_caption_data, output_dir=output_dir, file_postfix=PRECAPTION_FILE_POSTFIX)
                generated_count += 1

            except Exception as e:
                print(f"Error generating pre-caption for {video_id} in task {config_name}: {str(e)}")
                error_count += 1

    print(f"\nProcessing complete!")
    print(f"Generated: {generated_count}")
    print(f"Already exists: {already_exists_count}")
    print(f"Not ready: {not_ready_count}")
    print(f"Errors: {error_count}")


# This module can be run as a script or imported into feedback_app.py
if __name__ == "__main__":
    # Add the parent directory to sys.path if needed
    file_dir = Path(__file__).parent
    sys.path.insert(0, str(file_dir))

    # Import functions and variables from feedback_app.py
    from new_feedback_app import (
        parse_args, caption_programs,
    )
    
    from feedback_app import (
        load_video_data,
        FOLDER,
        PRECAPTION_FILE_POSTFIX,
        get_precaption_llm_name,
        get_video_id,
        save_data,
        data_is_saved,
        get_imagery_kwargs,
    )

    # Only take raw_lighting_setup_dynamics and raw_lighting_effects_dynamics from caption_programs
    caption_programs = {key: caption_programs[key] for key in ["raw_lighting_setup_dynamics", "raw_lighting_effects_dynamics"]}

    # Parse the command line arguments using the same function as the main app
    args = parse_args()

    # Load configurations
    try:
        from utils import load_config, load_json
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
        config_dict = {config["name"]: config for config in configs}
    except FileNotFoundError:
        print(f"Config file not found: {args.configs}")
        exit(1)

    # Load video data using the existing function from feedback_app.py
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)

    # Run batch generation
    batch_generate_precaptions(args.video_urls_files, config_dict, caption_programs, 
                               video_data_dict, args, redo=True) # TODO: Set redo=True to overwrite existing pre-captions, please comment out if not needed
else:
    # When imported, import from the main app since we'll be in the same context
    from feedback_app import (
        PRECAPTION_FILE_POSTFIX, FEEDBACK_FILE_POSTFIX,
        get_precaption_llm_name, get_video_id, get_filename,
        save_data, load_data, data_is_saved, get_imagery_kwargs
    )

    # Define a function to run the batch process
    def run_batch_precaption(args, config_dict, caption_programs, video_data_dict):
        """
        Run batch pre-caption generation from the main application
        
        Args:
            args: Command line arguments
            config_dict: Dictionary of configuration objects
            caption_programs: Dictionary of caption program objects
            video_data_dict: Dictionary of video data objects
        """
        batch_generate_precaptions(args.video_urls_files, config_dict, caption_programs, 
                                   video_data_dict, args)
