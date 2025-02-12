#!/usr/bin/env python3

import logging
import random
import os
from datetime import datetime
from batch import Batch

def setup_logging():
    """Set up logging configuration."""
    # Create logs directory first
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',  # Simplified format
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'logs/test_batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )

def print_video_details(video_name: str, video_data):
    """Print detailed information about a video."""
    print("\n" + "="*80)
    print(f"Video Name: {video_name}")
    print("="*80)
    
    # Print workflow data
    print("\nWorkflow Data:")
    print("-"*40)
    for workflow in video_data.workflows:
        print(f"Project: {workflow.project_name}")
        print(f"Approver: {workflow._approver}")
        print(f"Approval Time: {workflow._approval_time}")
        print(f"Video URL: {workflow._video_url}")
        print(f"Editing URL: {workflow._editing_url}")
        print(f"Labelers: {workflow._labelers}")
        print("-"*20)
    
    # Print camera motion data if available
    print("\nCamera Motion Data:")
    print("-"*40)
    try:
        motion_data = video_data.cam_motion
        if motion_data is None:
            print("No camera motion data available")
        else:
            has_data = False
            for attr in dir(motion_data):
                if not attr.startswith('_') and not callable(getattr(motion_data, attr)):
                    value = getattr(motion_data, attr)
                    if value is not None and value != '' and value != 'unknown':
                        has_data = True
                        print(f"{attr}: {value}")
            if not has_data:
                print("No camera motion data available (all values are None/empty/unknown)")
    except AttributeError:
        print("No camera motion data available")
    except Exception as e:
        print(f"Error accessing camera motion data: {e}")
    
    # Print camera setup data if available
    print("\nCamera Setup Data:")
    print("-"*40)
    try:
        cam_setup = video_data.cam_setup
        if cam_setup is None:
            print("No camera setup data available")
        else:
            has_data = False
            for attr in dir(cam_setup):
                if not attr.startswith('_') and not callable(getattr(cam_setup, attr)):
                    value = getattr(cam_setup, attr)
                    if value is not None and value != '' and value != 'unknown':
                        has_data = True
                        print(f"{attr}: {value}")
            if not has_data:
                print("No camera setup data available (all values are None/empty/unknown)")
    except AttributeError:
        print("No camera setup data available")
    except Exception as e:
        print(f"Error accessing camera setup data: {e}")
    
    # Print lighting setup data if available
    print("\nLighting Setup Data:")
    print("-"*40)
    try:
        light_data = video_data.light_setup
        if light_data is None:
            print("No lighting setup data available")
        else:
            has_data = False
            for attr in dir(light_data):
                if not attr.startswith('_') and not callable(getattr(light_data, attr)):
                    value = getattr(light_data, attr)
                    if value is not None and value != '' and value != 'unknown':
                        has_data = True
                        print(f"{attr}: {value}")
            if not has_data:
                print("No lighting setup data available (all values are None/empty/unknown)")
    except AttributeError:
        print("No lighting setup data available")
    except Exception as e:
        print(f"Error accessing lighting setup data: {e}")

def main():
    # Set up logging first, before any logging calls
    setup_logging()
    
    # Configuration
    yaml_paths = ["batch_configs/camera_setup.yaml", "batch_configs/camera_movement.yaml", "batch_configs/camera_setup2.yaml"]  # Can be a list of multiple YAML files
    ndjson_dir = "exports/ndjson"
    issues_dir = "exports/issues_ndjson"
    
    # preloaded_sheet_path = 'exports/sheets/sheet_data_20250211_193910.json'
    preloaded_sheet_path = 'exports/sheets/sheet_data_20250211_230959.json'
    
    # Create batch from YAML configs
    logging.info(f"Creating batch from {yaml_paths}")
    batch = Batch.from_configs(
        yaml_paths, 
        ndjson_dir, 
        issues_dir,
        preloaded_sheet_path=preloaded_sheet_path,
        save_sheet_data=True,
        save_batch=True,
        batch_name="donesection_motion_shotcomp"
    )
    
    # Print statistics
    logging.info(f"\nBatch Statistics:")
    logging.info(f"Total videos in batch: {len(batch)}")
    
    # # Print details for random videos from batch
    # logging.info("\nPrinting details for random videos from final batch:")
    # batch_video_names = batch.get_video_names()
    # if batch_video_names:
    #     sample_size = min(10, len(batch_video_names))
    #     random_batch_videos = random.sample(batch_video_names, sample_size)
    #     for video_name in random_batch_videos:
    #         print_video_details(video_name, batch[video_name])
    
    # # Get list of video names to inspect
    # video_names_to_inspect = ["0OFBj7EjZ-g.0.5.mp4"]  # Add video names to this list
    
    # # Print details for specified videos
    # if video_names_to_inspect:
    #     logging.info("\nPrinting details for specified videos:")
    #     for video_name in video_names_to_inspect:
    #         # Try exact match first, then try without extension
    #         video_found = False
    #         if video_name in batch:
    #             print_video_details(video_name, batch[video_name])
    #             video_found = True
    #         else:
    #             # Try searching without extension
    #             base_name = video_name.rsplit('.', 1)[0]
    #             for batch_video in batch.get_video_names():
    #                 if batch_video.startswith(base_name):
    #                     print_video_details(batch_video, batch[batch_video])
    #                     video_found = True
    #                     break
            
    #         if not video_found:
    #             logging.warning(f"Video {video_name} not found in batch (tried exact match and prefix match)")

if __name__ == "__main__":
    main() 