import json
import os
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional
from video_data import VideoData
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def normalize_question_name(name: str) -> str:
    """Normalize question name for consistent matching."""
    name = name.strip().lower()
    name = name.replace('?', '').replace(':', '')
    name = ' '.join(name.split())
    return name

def load_taxonomy() -> Dict[str, Dict[str, Any]]:
    """Load and process taxonomy.json into a lookup dictionary."""
    with open('taxonomy/taxonomy.json', 'r', encoding='utf-8') as f:
        taxonomy = json.load(f)
    
    lookup = {}
    required_fields = defaultdict(dict)
    
    for item in taxonomy:
        data = {
            "type": item["type"],
            "options": item.get("options", []),
            "data_category": item.get("data_category")
        }
        
        lookup[item["question"]] = data
        lookup[normalize_question_name(item["question"])] = data
        lookup[item["name"]] = data
        lookup[normalize_question_name(item["name"])] = data
        
        if item["type"] == "text" and "data_category" in item:
            category_parts = item["data_category"].split('.')
            data_class = category_parts[0]
            field = category_parts[1]
            required_fields[data_class][field] = ""
            
        elif "options" in item:
            for option in item["options"]:
                if "data_category" in option:
                    if "," in option["data_category"]:
                        categories = option["data_category"].split(",")
                        for category in categories:
                            category_parts = category.strip().split('.')
                            data_class = category_parts[0]
                            field = category_parts[1]
                            if option.get("data_value") in [True, False]:
                                required_fields[data_class][field] = False
                            elif isinstance(option.get("data_value"), list):
                                required_fields[data_class][field] = []
                            else:
                                required_fields[data_class][field] = "no"
                    else:
                        category_parts = option["data_category"].split('.')
                        data_class = category_parts[0]
                        field = category_parts[1]
                        if option.get("data_value") in [True, False]:
                            required_fields[data_class][field] = False
                        elif isinstance(option.get("data_value"), list):
                            required_fields[data_class][field] = []
                        else:
                            required_fields[data_class][field] = "no"
    
    lookup["__required_fields__"] = required_fields
    return lookup

def extract_answers(classification: Dict[str, Any], annotations_dict: Dict[str, Any]):
    """Extract answers from a classification dictionary."""
    name = classification.get('name', '')
    
    if 'radio_answer' in classification:
        answer = classification['radio_answer'].get('name', '')
        annotations_dict[name] = answer
    elif 'checklist_answers' in classification:
        answers = [ans.get('name', '') for ans in classification['checklist_answers']]
        annotations_dict[name] = answers
    elif 'text_answer' in classification:
        answer = classification['text_answer'].get('content', '')
        annotations_dict[name] = answer
    elif 'number_answer' in classification:
        answer = classification['number_answer'].get('number', '')
        annotations_dict[name] = answer

    if 'radio_answer' in classification and 'classifications' in classification['radio_answer']:
        for nested in classification['radio_answer']['classifications']:
            extract_answers(nested, annotations_dict)
    if 'checklist_answers' in classification:
        for checklist_answer in classification['checklist_answers']:
            if 'classifications' in checklist_answer:
                for nested in checklist_answer['classifications']:
                    extract_answers(nested, annotations_dict)

def extract_workflow_details(project_info, video_name: str, video_url: str, video_id: str, project_id: str):
    """
    Extracts essential workflow details.
    """
    workflow_history = project_info.get('project_details', {}).get('workflow_history', [])
    
    details = {
        'video_name': video_name,
        'video_url': video_url,
        'editing_url': f"https://app.labelbox.com/projects/{project_id}/data-rows/{video_id}",
        'approver': None,
        'approval_time': None,
        'labelers': []
    }
    
    # Get labelers directly from label_details
    labels = project_info.get('labels', [])
    seen_labelers = set()
    for label in labels:
        label_details = label.get('label_details', {})
        labeler = label_details.get('created_by')
        if labeler and labeler not in seen_labelers:
            seen_labelers.add(labeler)
            details['labelers'].append(labeler)
    
    # Get approval info from workflow history
    for action in workflow_history:
        if action['action'] == 'Approve':
            details['approver'] = action['created_by']
            details['approval_time'] = action['created_at']
            break
    
    return details

def convert_to_data_format(annotations_dict: Dict[str, Any], taxonomy_lookup: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Convert annotation answers to the format expected by VideoData."""
    result = defaultdict(dict)
    
    for name, answer in annotations_dict.items():
        if "(old)" in name:
            continue
            
        normalized_name = normalize_question_name(name)
        lookup_data = None
        
        for key in taxonomy_lookup:
            if key == name or key == normalized_name:
                lookup_data = taxonomy_lookup[key]
                break
            if normalize_question_name(key) == normalized_name:
                lookup_data = taxonomy_lookup[key]
                break
        
        if not lookup_data:
            continue
            
        if lookup_data["type"] == "text":
            if "data_category" in lookup_data:
                category_parts = lookup_data["data_category"].split('.')
                data_class = category_parts[0]
                field = category_parts[1]
                result[data_class][field] = answer
                
        elif lookup_data["type"] == "radio":
            if "options" in lookup_data:
                option = next((opt for opt in lookup_data["options"] if opt["value"] == answer), None)
                if option and "data_category" in option and "data_value" in option:
                    if "," in option["data_category"]:
                        categories = option["data_category"].split(",")
                        for category in categories:
                            category_parts = category.strip().split('.')
                            data_class = category_parts[0]
                            field = category_parts[1]
                            result[data_class][field] = option["data_value"]
                    else:
                        category_parts = option["data_category"].split('.')
                        data_class = category_parts[0]
                        field = category_parts[1]
                        result[data_class][field] = option["data_value"]
                    
        elif lookup_data["type"] == "checklist":
            if isinstance(answer, list):
                for ans in answer:
                    option = next((opt for opt in lookup_data["options"] if opt["value"] == ans), None)
                    if option and "data_category" in option and "data_value" in option:
                        if "," in option["data_category"]:
                            categories = option["data_category"].split(",")
                            for category in categories:
                                category_parts = category.strip().split('.')
                                data_class = category_parts[0]
                                field = category_parts[1]
                                if isinstance(option["data_value"], str):
                                    if field not in result[data_class]:
                                        result[data_class][field] = []
                                    result[data_class][field].append(option["data_value"])
                                else:
                                    result[data_class][field] = option["data_value"]
                        else:
                            category_parts = option["data_category"].split('.')
                            data_class = category_parts[0]
                            field = category_parts[1]
                            if isinstance(option["data_value"], str):
                                if field not in result[data_class]:
                                    result[data_class][field] = []
                                result[data_class][field].append(option["data_value"])
                            else:
                                result[data_class][field] = option["data_value"]
    
    return result

def load_issues(issues_dir: str) -> set:
    """Load video IDs from issues directory."""
    issue_ids = set()
    if not os.path.exists(issues_dir):
        return issue_ids
        
    for filename in os.listdir(issues_dir):
        if filename.endswith('.ndjson'):
            with open(os.path.join(issues_dir, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        video_id = record.get('data_row', {}).get('id')
                        video_name = record.get('data_row', {}).get('external_id', video_id)
                        if video_name:
                            issue_ids.add(video_name)
                    except json.JSONDecodeError:
                        continue
    return issue_ids

def collect_valid_video_names(ndjson_dir: str, issues_dir: str) -> tuple[set, set]:
    """Collect all video names and identify which ones are from issues directory."""
    all_videos = set()
    issue_videos = load_issues(issues_dir)
    
    for filename in os.listdir(ndjson_dir):
        if not filename.endswith('.ndjson'):
            continue
            
        filepath = os.path.join(ndjson_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    record = json.loads(line.strip())
                    video_id = record.get('data_row', {}).get('id')
                    video_name = record.get('data_row', {}).get('external_id', video_id)
                    
                    if video_name:
                        all_videos.add(video_name)
                except Exception as e:
                    logging.error(f"Error processing line {line_number} in {filepath}: {e}")
                    
    return all_videos, issue_videos

def process_ndjson_files(ndjson_dir: str, issues_dir: str) -> Dict[str, VideoData]:
    """Process all NDJSON files in directory and return dictionary of VideoData objects."""
    taxonomy_lookup = load_taxonomy()
    all_videos, issue_videos = collect_valid_video_names(ndjson_dir, issues_dir)
    video_data_dict = {name: VideoData() for name in all_videos}
    video_annotations = defaultdict(list)
    
    logging.info(f"Processing {len(all_videos)} videos ({len(issue_videos)} marked as shot transitions)...")
    
    # Process NDJSON files and collect annotations
    for filename in os.listdir(ndjson_dir):
        if not filename.endswith('.ndjson'):
            continue
            
        filepath = os.path.join(ndjson_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    record = json.loads(line.strip())
                    video_id = record.get('data_row', {}).get('id')
                    video_name = record.get('data_row', {}).get('external_id', video_id)
                    
                    if video_name not in all_videos:
                        continue
                    
                    # Create or get VideoData object
                    if video_name not in video_data_dict:
                        video_data_dict[video_name] = VideoData()
                    
                    video_data = video_data_dict[video_name]
                    
                    # Set basic metadata
                    video_data.video_name = video_name
                    video_data.video_url = record.get('data_row', {}).get('row_data')
                    
                    # Handle projects
                    projects = record.get('projects', {})
                    if not projects:
                        continue
                        
                    for project_id, project_info in projects.items():
                        # Set editing URL
                        video_data.editing_url = f"https://app.labelbox.com/projects/{project_id}/data-rows/{video_id}"
                        
                        # Extract and set workflow details
                        workflow_details = extract_workflow_details(project_info, video_name, video_data.video_url, video_id, project_id)
                        
                        # Only update workflow details if they're more recent
                        current_workflow = getattr(video_data, '_workflow_details', None)
                        if (not current_workflow or 
                            (workflow_details['approval_time'] and not current_workflow.approval_time) or
                            (workflow_details['approval_time'] and current_workflow.approval_time and 
                             datetime.fromisoformat(workflow_details['approval_time'].replace('Z', '+00:00')) > current_workflow.approval_time)):
                            video_data.workflow_details = workflow_details

                        # Process annotations
                        selected_label_id = project_info.get('project_details', {}).get('selected_label_id')
                        if not selected_label_id:
                            continue

                        labels = project_info.get('labels', [])
                        selected_label = next((label for label in labels if label.get('id') == selected_label_id), None)
                        if not selected_label:
                            continue

                        annotations_dict = {}
                        classifications = selected_label.get('annotations', {}).get('classifications', [])
                        for classification in classifications:
                            extract_answers(classification, annotations_dict)
                            
                        video_annotations[video_name].append(annotations_dict)
                        
                except Exception as e:
                    logging.error(f"Error processing line {line_number} in {filepath}: {e}")
                    continue
    
    # Process annotations and create video data objects
    for video_name, annotations_list in video_annotations.items():
        all_camera_motion = []
        all_camera_setup = []
        all_lighting_setup = []
        
        for annotations in annotations_list:
            data_dict = convert_to_data_format(annotations, taxonomy_lookup)
            
            if 'CameraMotionData' in data_dict:
                all_camera_motion.append(data_dict['CameraMotionData'])
            if 'CameraSetupData' in data_dict:
                all_camera_setup.append(data_dict['CameraSetupData'])
            if 'LightingSetupData' in data_dict:
                all_lighting_setup.append(data_dict['LightingSetupData'])
        
        video_data = video_data_dict[video_name]
        
        try:
            # For issue videos, set shot_transition to True and use default values
            if video_name in issue_videos:
                video_data.cam_motion = {'shot_transition': True}
                video_data.cam_setup = {'shot_transition': True}
            else:
                if all_camera_motion:
                    motion_params = all_camera_motion[-1]
                    video_data.cam_motion = motion_params
                    
                if all_camera_setup:
                    setup_params = all_camera_setup[-1]
                    video_data.cam_setup = setup_params
                
            if all_lighting_setup:
                lighting_params = all_lighting_setup[-1]
                video_data.light_setup = lighting_params
                
        except Exception as e:
            logging.error(f"Error setting data for {video_name}: {e}")
            continue
            
    logging.info(f"Successfully processed {len(video_data_dict)} videos")
    return video_data_dict

def inspect_video(video_name: str, video_data_dict: dict):
    """Inspect a specific video by name"""
    if video_name not in video_data_dict:
        print(f"Video '{video_name}' not found!")
        return
        
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
            print(f"Video Name: {workflow.video_name}")
            print(f"Video URL: {workflow.video_url}")
            print(f"Editing URL: {workflow.editing_url}")
            print(f"Approver: {workflow.approver}")
            print(f"Approval Time: {workflow.approval_time}")
            print(f"Labelers: {workflow.labelers}")
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

def debug_video_data(video_data: VideoData, video_name: str):
    """Print debug information for a video."""
    print(f"\nDEBUG INFO FOR: {video_name}")
    print("=" * 80)
    
    # Debug Camera Motion
    print("\nCamera Motion:")
    print("-" * 40)
    try:
        motion = video_data.cam_motion
        for attr in dir(motion):
            if not attr.startswith('_') and not callable(getattr(motion, attr)):
                value = getattr(motion, attr)
                print(f"{attr}: {value}")
    except AttributeError as e:
        print(f"Camera motion not set: {e}")

    # Debug Camera Setup
    print("\nCamera Setup:")
    print("-" * 40)
    try:
        setup = video_data.cam_setup
        for attr in dir(setup):
            if not attr.startswith('_') and not callable(getattr(setup, attr)):
                value = getattr(setup, attr)
                print(f"{attr}: {value}")
    except AttributeError as e:
        print(f"Camera setup not set: {e}")

    # Debug Workflow Details
    print("\nWorkflow Details:")
    print("-" * 40)
    try:
        workflow = video_data.workflow_details
        if workflow:
            print(f"Video URL: {workflow.video_url}")
            print(f"Editing URL: {workflow.editing_url}")
            print(f"Approver: {workflow.approver}")
            print(f"Approval Time: {workflow.approval_time}")
            print(f"Labelers: {workflow.labelers}")
    except AttributeError as e:
        print(f"Workflow details not set: {e}")

    print("\n" + "=" * 80) 

def search_videos(partial_name: str, video_data_dict: dict):
    """Search for videos containing the given string in their name"""
    matches = [name for name in video_data_dict.keys() if partial_name.lower() in name.lower()]
    if matches:
        print(f"Found {len(matches)} matching videos:")
        for name in sorted(matches):
            print(f"- {name}")
            try:
                workflow = video_data_dict[name].workflow_details
                print(f"  Approver: {workflow.approver}")
                print(f"  Approval Time: {workflow.approval_time}")
                print(f"  Labelers: {workflow.labelers}")
            except AttributeError:
                print("  No workflow details available")
    else:
        print(f"No videos found containing '{partial_name}'")
    return matches

if __name__ == "__main__":
    # Process the NDJSON files
    ndjson_dir = "exports/ndjson"
    issues_dir = "exports/issues_ndjson"
    
    # Process files
    video_data_dict = process_ndjson_files(ndjson_dir, issues_dir)
    
    # Show 10 random samples
    # debug_video_data(video_data_dict, num_samples=10)
    
    # Example: Inspect a specific video by name
    # inspect_video("video_name.mp4", video_data_dict)
