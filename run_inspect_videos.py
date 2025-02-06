import os
import logging
from process_ndjson import process_ndjson_files
import sys
from io import StringIO

def get_video_names_from_directory(directory_path: str) -> set:
    """Get all video names from a directory."""
    video_names = set()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.mp4'):
                video_names.add(file)
    return video_names

def inspect_video(video_name: str, video_data_dict: dict) -> str:
    """Inspect a specific video by name and return the inspection results as a string"""
    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    
    if video_name not in video_data_dict:
        print(f"Video '{video_name}' not found!")
        sys.stdout = old_stdout
        return result.getvalue()
        
    video_data = video_data_dict[video_name]
    print(f"\nInspecting video: {video_name}")
    print("=" * 50)
    
    # Debug internal state
    print("\nInternal state:")
    print("-" * 20)
    print(f"_cam_motion exists: {hasattr(video_data, '_cam_motion')}")
    print(f"_cam_setup exists: {hasattr(video_data, '_cam_setup')}")
    print(f"_light_setup exists: {hasattr(video_data, '_light_setup')}")
    print(f"_workflow_details exists: {hasattr(video_data, '_workflow_details')}")
    
    # Check Workflow Data
    print("\nWorkflow Data:")
    print("-" * 20)
    try:
        workflow = video_data.workflow_details
        if workflow is None:
            print("Workflow data is None")
        else:
            print(f"Video Name: {workflow.get('video_name')}")
            print(f"Video URL: {workflow.get('video_url')}")
            print(f"Editing URL: {workflow.get('editing_url')}")
            print(f"Approver: {workflow.get('approver')}")
            print(f"Approval Time: {workflow.get('approval_time')}")
            print(f"Labelers: {workflow.get('labelers', [])}")
    except Exception as e:
        print(f"Error accessing workflow data: {e}")
    
    # Check Camera Motion Data
    print("\nCamera Motion Data:")
    print("-" * 20)
    try:
        motion_data = video_data.cam_motion
        if motion_data is None:
            print("Camera motion data is None")
        else:
            for attr_name in dir(motion_data):
                if not attr_name.startswith('_'):  # Skip private attributes
                    value = getattr(motion_data, attr_name)
                    if not callable(value):  # Skip methods
                        print(f"{attr_name}: {value}")
    except Exception as e:
        print(f"Error accessing camera motion data: {e}")
        
    # Check Camera Setup Data
    print("\nCamera Setup Data:")
    print("-" * 20)
    try:
        setup_data = video_data.cam_setup
        if setup_data is None:
            print("Camera setup data is None")
        else:
            for attr_name in dir(setup_data):
                if not attr_name.startswith('_'):
                    value = getattr(setup_data, attr_name)
                    if not callable(value):
                        print(f"{attr_name}: {value}")
    except Exception as e:
        print(f"Error accessing camera setup data: {e}")
        
    # Check Lighting Setup Data
    print("\nLighting Setup Data:")
    print("-" * 20)
    try:
        light_data = video_data.light_setup
        if light_data is None:
            print("Lighting setup data is None")
        else:
            for attr_name in dir(light_data):
                if not attr_name.startswith('_'):
                    value = getattr(light_data, attr_name)
                    if not callable(value):
                        print(f"{attr_name}: {value}")
    except Exception as e:
        print(f"Error accessing lighting setup data: {e}")
    
    # Restore stdout and return the captured output
    sys.stdout = old_stdout
    return result.getvalue()

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Create temp directory if it doesn't exist
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        print(f"Created directory: {temp_dir}")

    # Directory containing the videos to process
    videos_dir = "../datasets/CaptionAnythingtest/videos"
    if not os.path.exists(videos_dir):
        print(f"Error: Directory {videos_dir} does not exist")
        return

    # Get video names from directory
    video_names = get_video_names_from_directory(videos_dir)
    print(f"\nFound {len(video_names)} videos in directory")

    # Process NDJSON files
    ndjson_dir = "exports/ndjson"
    issues_dir = "exports/issues_ndjson"
    
    print("\nProcessing NDJSON files...")
    all_videos = process_ndjson_files(ndjson_dir, issues_dir)
    
    # Inspect each video from our directory and save to file
    print("\nInspecting videos and saving results...")
    for video_name in sorted(video_names):
        if video_name in all_videos:
            # Get inspection results
            inspection_results = inspect_video(video_name, all_videos)
            
            # Create output file name (replace any problematic characters in video name)
            safe_name = video_name.replace('.', '_')
            output_file = os.path.join(temp_dir, f"{safe_name}_inspection.txt")
            
            # Save results to file
            with open(output_file, 'w') as f:
                f.write(inspection_results)
            print(f"Saved inspection results for {video_name} to {output_file}")
        else:
            print(f"\nVideo {video_name} not found in NDJSON data")

if __name__ == "__main__":
    main() 