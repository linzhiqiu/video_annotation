#!/usr/bin/env python3

import os
import json
import yaml
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from process_ndjson import process_ndjson_files
from video_data import VideoData
from caption_generation.models.model_factory import ModelFactory
from caption_generation.models.base_model import CaptionInput, CaptionOutput
from caption_generation.utils.file_utils import find_video_files, load_video_names, filter_videos_by_constraints

def load_instruction(instruction_path: str) -> Dict[str, Any]:
    """Load instruction template and model settings."""
    if not os.path.exists(instruction_path):
        raise FileNotFoundError(f"Instruction file not found: {instruction_path}")
        
    with open(instruction_path, 'r') as f:
        return json.load(f)

def format_instruction(template: List[str], video: VideoData) -> str:
    """Format instruction template with video data.
    
    Args:
        template: List of instruction template strings
        video: VideoData object to use for formatting
        
    Returns:
        Concatenated and formatted instruction string
    """
    context = {'self': video}
    formatted_parts = []
    
    for part in template:
        try:
            formatted = eval(f"f'''{part}'''", context)
            if formatted.strip():  # Only include non-empty strings
                formatted_parts.append(formatted)
        except Exception as e:
            logging.error(f"Error formatting instruction part: {str(e)}")
            continue
            
    return " ".join(formatted_parts)

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Load configuration
    config_path = 'caption_generation/configs/generation.yaml'
    if not os.path.exists(config_path):
        logging.error(f"Config file not found: {config_path}")
        return
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Create output directory
    output_dir = config.get('settings', {}).get('output_dir', 'caption_generation/results')
    os.makedirs(output_dir, exist_ok=True)
    
    # Load videos from NDJSON files
    ndjson_dir = config.get('data', {}).get('ndjson_dir', 'exports/ndjson')
    issues_dir = config.get('data', {}).get('issues_dir', 'exports/issues_ndjson')
    
    logging.info("Processing NDJSON files...")
    all_videos = process_ndjson_files(ndjson_dir, issues_dir)
    logging.info(f"Loaded {len(all_videos)} total videos")
    
    # Filter videos based on constraints
    videos = filter_videos_by_constraints(all_videos, config)
    if not videos:
        logging.error("No videos to process after filtering")
        return
    
    # Find video files in the videos directory
    videos_dir = config.get('data', {}).get('videos_dir')
    if not videos_dir:
        logging.error("videos_dir not specified in config")
        return
        
    video_names = set(videos.keys())
    video_paths = find_video_files(videos_dir, video_names)
    if not video_paths:
        logging.error("No video files found")
        return
    
    # Process each rule
    all_results = {}
    for rule in config.get('rules', []):
        caption_type = rule['caption_type']
        instruction_path = rule['instruction_path']
        
        logging.info(f"Processing {caption_type} captions...")
        
        try:
            # Load instruction data
            instruction_data = load_instruction(instruction_path)
            model_name = instruction_data['model settings']['name']
            model_settings = instruction_data['model settings']
            instruction_template = instruction_data['instruction_template']
            
            # Get model instance
            model = ModelFactory.get_model(model_name)
            
            # Prepare inputs
            inputs = []
            for video_name, video in videos.items():
                if video_name in video_paths:  # Only process videos we found
                    final_instruction = format_instruction(instruction_template, video)
                    inputs.append(CaptionInput(
                        video_name=video_name,
                        instruction=final_instruction,
                        model_params=model_settings,
                        videos_dir=videos_dir
                    ))
            
            # Generate captions
            outputs = model.generate_captions(inputs)
            
            # Store results
            for output in outputs:
                if output.video_name not in all_results:
                    all_results[output.video_name] = {}
                    
                all_results[output.video_name][caption_type] = {
                    'model_name': model_name,
                    'instruction_template': instruction_template,
                    'final_instruction': output.instruction,
                    'output_caption': output.caption,
                    'timestamp': datetime.now().isoformat(),
                    'model_params': output.model_params
                }
                
        except Exception as e:
            logging.error(f"Error processing {caption_type}: {str(e)}")
            continue
    
    # Save results
    output_file = os.path.join(output_dir, 'captions.json')
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(videos),
            'results': all_results
        }, f, indent=2)
    
    logging.info(f"Results saved to {output_file}")

if __name__ == '__main__':
    main() 