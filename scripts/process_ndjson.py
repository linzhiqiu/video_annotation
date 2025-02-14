import json
import os
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional, Set, Union, Tuple
import sys
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_data import VideoData, CameraMotionData, CameraSetupData, LightingSetupData
from scripts.sheet_utils import SheetService, load_all_sheet_data, load_config
import traceback

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'logs/process_ndjson_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

def normalize_question_name(name: str) -> str:
    """Normalize a question name by removing special characters and converting to lowercase."""
    return name.lower().replace(" ", "_").replace("?", "").replace("(", "").replace(")", "")

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

def extract_workflow_details(project_info):
    """Extract workflow details from project info."""
    workflow_details = {}
    
    try:
        project_name = project_info.get('name', '')
        if not project_name:
            logging.warning("No project name found in project info")
            
        workflow_details['project_name'] = project_name
        workflow_details['approver'] = None
        workflow_details['approval_time'] = None
        workflow_details['labelers'] = []
        
        # Get labelers directly from label_details
        labels = project_info.get('labels', [])
        seen_labelers = set()
        for label in labels:
            label_details = label.get('label_details', {})
            labeler = label_details.get('created_by')
            if labeler and labeler not in seen_labelers:
                seen_labelers.add(labeler)
                workflow_details['labelers'].append(labeler)
        
        # Get approval info from workflow history
        workflow_history = project_info.get('project_details', {}).get('workflow_history', [])
        for action in workflow_history:
            if action['action'] == 'Approve':
                workflow_details['approver'] = action['created_by']
                workflow_details['approval_time'] = action['created_at']
                break
                
    except Exception as e:
        logging.error(f"Error extracting workflow details: {str(e)}")
        
    return workflow_details

def extract_answers(classification: Dict[str, Any], annotations_dict: Dict[str, Any]):
    """Extract answers from a classification dictionary."""
    name = classification.get('name', '')
    
    if 'radio_answer' in classification:
        answer = classification['radio_answer'].get('name', '')
        if not answer:
            logging.error(f"Could not get name from radio_answer: {classification['radio_answer']}")
        if answer:
            annotations_dict[name] = answer
            
        # Handle nested classifications in radio answers
        if 'classifications' in classification['radio_answer']:
            for nested in classification['radio_answer']['classifications']:
                extract_answers(nested, annotations_dict)
                
    elif 'checklist_answers' in classification:
        answers = []
        for ans in classification['checklist_answers']:
            value = ans.get('name', '')
            if not value:
                logging.error(f"Could not get name from checklist answer: {ans}")
            if value:
                answers.append(value)
        
        if answers:
            annotations_dict[name] = answers
            
        # Handle nested classifications in checklist answers
        for checklist_answer in classification['checklist_answers']:
            if 'classifications' in checklist_answer:
                for nested in checklist_answer['classifications']:
                    extract_answers(nested, annotations_dict)
                    
    elif 'text_answer' in classification:
        answer = classification['text_answer'].get('content', '')
        if answer:
            annotations_dict[name] = answer
            
    elif 'number_answer' in classification:
        answer = classification['number_answer'].get('number', '')
        if answer:
            annotations_dict[name] = answer

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

        # logging.info(f"lookup_data: {lookup_data}")
        # logging.info(f"answer: {answer}")
        # logging.info(f"name: {name}")
        # logging.info(f"normalized_name: {normalized_name}")
            
        if lookup_data["type"] == "text":
            if "data_category" in lookup_data:
                category_parts = lookup_data["data_category"].split('.')
                data_class = category_parts[0]
                field = category_parts[1]
                result[data_class][field] = answer
                
        elif lookup_data["type"] == "radio":
            if "options" in lookup_data:
                # Look for matching option by value first, then by name if no value match
                option = next((opt for opt in lookup_data["options"] if opt.get("value", "") == answer), None)
                if not option:
                    option = next((opt for opt in lookup_data["options"] if opt.get("data_value", "") == answer), None)
                
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
                    # Look for matching option by value first, then by name if no value match
                    option = next((opt for opt in lookup_data["options"] if opt.get("value", "") == ans), None)
                    if not option:
                        option = next((opt for opt in lookup_data["options"] if opt.get("data_value", "") == ans), None)
                        
                    if option and "data_category" in option and "data_value" in option:
                        if "," in option["data_category"]:
                            categories = option["data_category"].split(",")
                            for category in categories:
                                category_parts = category.strip().split('.')
                                data_class = category_parts[0]
                                field = category_parts[1]
                                if isinstance(option["data_value"], bool):
                                    result[data_class][field] = option["data_value"]
                                elif isinstance(option["data_value"], list):
                                    if field not in result[data_class]:
                                        result[data_class][field] = []
                                    result[data_class][field].extend(option["data_value"])
                                else:
                                    if field not in result[data_class]:
                                        result[data_class][field] = []
                                    result[data_class][field].append(option["data_value"])
                        else:
                            category_parts = option["data_category"].split('.')
                            data_class = category_parts[0]
                            field = category_parts[1]
                            if isinstance(option["data_value"], bool):
                                result[data_class][field] = option["data_value"]
                            elif isinstance(option["data_value"], list):
                                if field not in result[data_class]:
                                    result[data_class][field] = []
                                result[data_class][field].extend(option["data_value"])
                            else:
                                if field not in result[data_class]:
                                    result[data_class][field] = []
                                result[data_class][field].append(option["data_value"])
    
    return dict(result)

def load_issues(issues_dir: str) -> set:
    """Load video IDs from issues directory."""
    issue_ids = set()
    if not os.path.exists(issues_dir):
        return issue_ids
        
    for filename in os.listdir(issues_dir):
        if filename.endswith('.json'):
            with open(os.path.join(issues_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    # Load the entire file as a JSON array
                    issues = json.load(f)
                    for issue in issues:
                        video_name = issue.get('externalDataRowId')
                        if video_name:
                            issue_ids.add(video_name)
                            # logging.info(f"Found issue for video: {video_name}")
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing JSON file {filename}: {e}")
                    continue
    
    # logging.info(f"Total issue videos found: {len(issue_ids)}")
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

def get_valid_videos_from_yaml(yaml_path: str) -> Set[str]:
    """Get set of valid video names that meet the requirements in a YAML file.
    
    Args:
        yaml_path: Path to YAML configuration file
        
    Returns:
        Set of video names that meet the requirements
    """
    # Load YAML config
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        
    # Get project name and requirements
    project_name = config.get('project_name')
    if not project_name:
        raise ValueError(f"Project name not specified in config file: {yaml_path}")
        
    # Skip if all requirements are null
    requirements = config.get('requirements', {})
    if all(val is None for val in requirements.values()):
        logging.info(f"All requirements are null for {project_name}, skipping")
        return set()
    
    return set()

def should_process_workflow(workflow_details: Dict[str, Any], yaml_configs: Dict[str, Any], video_name: str, sheet_data: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None) -> bool:
    """Check if a workflow should be processed based on YAML configurations and sheet data."""
    # If no YAML configs provided at all, accept everything
    if not yaml_configs:
        return True
        
    # Get project name from workflow details
    project_name = workflow_details.get('project_name')
    if not project_name:
        logging.warning(f"No project name in workflow details for {video_name}")
        return False
        
    # Get YAML config for this project if it exists
    yaml_config = yaml_configs.get(project_name)
    
    # If no config for this project, accept it
    if not yaml_config:
        return True
        
    # Check video name restrictions if specified
    video_names_file = yaml_config.get('video_names_file')
    if video_names_file is not None:
        try:
            with open(video_names_file, 'r') as f:
                allowed_videos = set(json.load(f))
            if video_name not in allowed_videos:
                return False
        except Exception as e:
            logging.error(f"Error reading video names file {video_names_file}: {e}")
            return False
            
    # Check time range if specified
    time_range = yaml_config.get('time_range')
    if time_range is not None:
        if workflow_details.get('approval_time'):
            try:
                approval_time = datetime.fromisoformat(workflow_details['approval_time'].replace('Z', '+00:00'))
                start_time = datetime.fromisoformat(time_range.get('start', '1970-01-01T00:00:00+00:00'))
                end_time = datetime.fromisoformat(time_range.get('end', '9999-12-31T23:59:59+00:00'))
                if not (start_time <= approval_time <= end_time):
                    return False
            except Exception as e:
                logging.error(f"Error parsing time range restriction: {e}")
                return False
            
    # Check approvers if specified
    allowed_approvers = yaml_config.get('approvers')
    if allowed_approvers is not None:
        # logging.info(f"Allowed approvers: {allowed_approvers}")
        if not allowed_approvers:  # Empty list means no approvers allowed
            return False
        workflow_approver = workflow_details.get('approver')
        # logging.info(f"Workflow approver: {workflow_approver}")
        if workflow_approver not in allowed_approvers:
            # logging.info(f"Approver {workflow_approver} not in allowed approvers {allowed_approvers}")
            return False
            
    # Check sheet data requirements if specified
    project_requirements = yaml_config.get('project_requirements')
    # If all requirements are null, accept it
    if not project_requirements or all(v is None for v in project_requirements.values()):
        return True

    if project_requirements and sheet_data:
        # Get sheet data for this video
        video_sheet_data = sheet_data.get(video_name, {})
        project_sheet_data = video_sheet_data.get(project_name)
        
        if not project_sheet_data:
            # No sheet data found for this video/project
            return False
            
        meta_reviewer = project_sheet_data.get('meta_reviewer', '')
        double_check = project_sheet_data.get('double_check', '')
        
        # Check meta reviewer requirements
        required_meta_reviewers = project_requirements.get('meta_reviewers')
        if required_meta_reviewers and meta_reviewer not in required_meta_reviewers:
            return False
            
        # Check double check status
        required_double_check = project_requirements.get('double_check_status')
        if required_double_check is not None and double_check != required_double_check:
            return False
            
    return True

def process_ndjson_files(ndjson_dir: str, issues_dir: str, yaml_paths: Optional[List[str]] = None, 
                     preloaded_sheet_path: Optional[str] = None, save_sheet_data: bool = False) -> Dict[str, VideoData]:
    """Process NDJSON files and return dictionary of VideoData objects.
    
    Args:
        ndjson_dir: Directory containing NDJSON files
        issues_dir: Directory containing issue NDJSON files
        yaml_paths: Optional list of paths to YAML configuration files
        preloaded_sheet_path: Optional path to JSON file containing preloaded sheet data
        save_sheet_data: Whether to save loaded sheet data to a JSON file
    """
    # Load sheet configuration
    config = load_config()
    sheets_config = config.get('google_sheets', {})
    
    # Load YAML configs if provided
    yaml_configs = {}
    sheet_data = None
    
    # Try loading sheet data from file if path provided
    if preloaded_sheet_path:
        try:
            with open(preloaded_sheet_path, 'r') as f:
                sheet_data = json.load(f)
                logging.info(f"Loaded sheet data from {preloaded_sheet_path}")
        except Exception as e:
            logging.error(f"Error loading sheet data from {preloaded_sheet_path}: {e}")
            sheet_data = None
    
    if yaml_paths:
        logging.info(f"Loading YAML configs from: {yaml_paths}")
        needs_sheet_data = False
        for yaml_path in yaml_paths:
            try:
                with open(yaml_path, 'r') as f:
                    config = yaml.safe_load(f)
                    project_name = config.get('project_name')
                    if project_name:
                        yaml_configs[project_name] = config
                        # Check if any project has sheet-related requirements
                        project_requirements = config.get('project_requirements', {})
                        if project_requirements.get('meta_reviewers') or project_requirements.get('double_check_status'):
                            needs_sheet_data = True
            except Exception as e:
                logging.error(f"Error loading YAML config {yaml_path}: {e}")
        
        # Only load sheet data if needed by YAML configs and not already loaded
        if needs_sheet_data and sheet_data is None:
            logging.info("Loading sheet data for YAML requirements...")
            sheet_data = load_all_sheet_data(sheets_config, yaml_configs, save_sheet_data)
    
    # Load taxonomy and collect video names
    taxonomy_lookup = load_taxonomy()
    all_videos, issue_videos = collect_valid_video_names(ndjson_dir, issues_dir)
    logging.info(f"Found {len(all_videos)} total videos ({len(issue_videos)} marked as shot transitions)")
    
    video_data_dict = {name: VideoData() for name in all_videos}
    video_annotations = defaultdict(list)
    videos_by_project = defaultdict(set)
    filtered_videos_by_project = defaultdict(set)
    
    # Process NDJSON files
    for filename in os.listdir(ndjson_dir):
        if not filename.endswith('.ndjson'):
            continue
            
        logging.info(f"Processing file: {filename}")
        filepath = os.path.join(ndjson_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    record = json.loads(line.strip())
                    video_id = record.get('data_row', {}).get('id')
                    video_name = record.get('data_row', {}).get('external_id', video_id)

                    
                    if video_name not in all_videos:
                        continue
                    
                    video_data = video_data_dict[video_name]
                    video_data.video_name = video_name
                    video_data.video_url = record.get('data_row', {}).get('row_data')
                    
                    projects = record.get('projects', {})
                    if not projects:
                        continue
                        
                    for project_id, project_info in projects.items():
                        workflow_details = extract_workflow_details(project_info)
                        if not workflow_details:
                            continue
                            
                        project_name = workflow_details.get('project_name', '')
                        videos_by_project[project_name].add(video_name)
                        
                        workflow_details.update({
                            'video_name': video_name,
                            'video_url': video_data.video_url,
                            'editing_url': f"https://app.labelbox.com/projects/{project_id}/data-rows/{video_id}"
                        })
                        
                        if not should_process_workflow(workflow_details, yaml_configs, video_name, sheet_data):
                            continue

                            
                        filtered_videos_by_project[project_name].add(video_name)
                        video_data.add_workflow(workflow_details)
                        
                        labels = project_info.get('labels', [])
                        
                        # If there's only one label, use it directly
                        if len(labels) == 1:
                            selected_label = labels[0]
                        else:
                            # Otherwise use selected_label_id to find the right one
                            selected_label_id = project_info.get('project_details', {}).get('selected_label_id')
                            if not selected_label_id:
                                continue
                            selected_label = next((label for label in labels if label.get('id') == selected_label_id), None)
                            if not selected_label:
                                continue
                        
                        annotations_dict = {}
                        classifications = selected_label.get('annotations', {}).get('classifications', [])
                        for classification in classifications:
                            extract_answers(classification, annotations_dict)

                        if annotations_dict:
                            video_annotations[video_name].append(annotations_dict)
                            
                except Exception as e:
                    logging.error(f"Error processing line {line_number} in {filepath}: {e}")
                    logging.error(traceback.format_exc())
                    continue
    
    # Process annotations and set data
    logging.info("Processing annotations and setting data...")

    # First, set shot_transition=True for all issue videos, regardless of annotations
    for video_name in issue_videos:
        if video_name in video_data_dict:
            video_data = video_data_dict[video_name]
            video_data.cam_motion = {'shot_transition': True}
            video_data.cam_setup = {'shot_transition': True}


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

        # logging.info(f"\nVideo: {video_name}")
        # logging.info("Annotations:")
        # for i, annotations in enumerate(annotations_list, 1):
        #     logging.info(f"  Annotation set {i}:")
        #     logging.info(f"    {json.dumps(annotations, indent=4)}")
        
        # logging.info("Processed Data:")
        # if all_camera_motion:
        #     logging.info("  Camera Motion:")
        #     logging.info(f"    {json.dumps(all_camera_motion, indent=4)}")
        # if all_camera_setup:
        #     logging.info("  Camera Setup:")
        #     logging.info(f"    {json.dumps(all_camera_setup, indent=4)}")
        # if all_lighting_setup:
        #     logging.info("  Lighting Setup:")
        #     logging.info(f"    {json.dumps(all_lighting_setup, indent=4)}")

        try:
            # Only set data from annotations if this is not an issue video
            if video_name not in issue_videos:
                if all_camera_motion:
                    # Merge multiple motion dictionaries if they exist
                    motion_params = {}
                    for params in all_camera_motion:
                        for key, value in params.items():
                            # Take the "lower" value if key already exists
                            if key in motion_params:
                                motion_params[key] = min(motion_params[key], value)
                            else:
                                motion_params[key] = value
                    video_data.cam_motion = motion_params
                    
                if all_camera_setup:
                    # Merge multiple setup dictionaries if they exist
                    setup_params = {}
                    for params in all_camera_setup:
                        for key, value in params.items():
                            # Take the "lower" value if key already exists
                            if key in setup_params:
                                setup_params[key] = min(setup_params[key], value)
                            else:
                                setup_params[key] = value
                    video_data.cam_setup = setup_params
                
            if all_lighting_setup:
                # Merge multiple lighting dictionaries if they exist
                lighting_params = {}
                for params in all_lighting_setup:
                    for key, value in params.items():
                        # Take the "lower" value if key already exists
                        if key in lighting_params:
                            lighting_params[key] = min(lighting_params[key], value)
                        else:
                            lighting_params[key] = value
                video_data.light_setup = lighting_params
                
        except Exception as e:
            logging.error(f"\nError processing video {video_name}:")
            logging.error("-" * 50)
            logging.error(f"Error message: {str(e)}")
            logging.error("\nTraceback:")
            logging.error(traceback.format_exc())
            
            if all_camera_setup:
                logging.error("\nCamera Setup Data:")
                logging.error(json.dumps(all_camera_setup[-1], indent=2))
            if all_camera_motion:
                logging.error("\nCamera Motion Data:")
                logging.error(json.dumps(all_camera_motion[-1], indent=2))
            if all_lighting_setup:
                logging.error("\nLighting Setup Data:")
                logging.error(json.dumps(all_lighting_setup[-1], indent=2))
            
            logging.error("-" * 50)
            continue
    
    # Filter and print statistics
    video_data_dict = {name: data for name, data in video_data_dict.items() if data.workflows}
    
    logging.info("\nPer-Project Statistics:")
    for project_name in videos_by_project:
        total = len(videos_by_project[project_name])
        filtered = len(filtered_videos_by_project[project_name])
        logging.info(f"Project: {project_name}")
        logging.info(f"  - Total unique videos: {total}")
        logging.info(f"  - After filtering: {filtered}")
        logging.info(f"  - Filtered out: {total - filtered}")
    
    logging.info(f"\nFinal Statistics:")
    logging.info(f"Total videos with data: {len(video_data_dict)}")
    
    return video_data_dict

def inspect_video(video_name: str, video_data_dict: dict):
    """Inspect a specific video by name."""
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
    """Debug a VideoData object."""
    print(f"\nDebugging video: {video_name}")
    print("=" * 50)
    
    # Check Camera Motion Data
    print("\nCamera Motion Data:")
    print("-" * 20)
    try:
        motion_data = video_data.cam_motion
        if motion_data is None:
            print("Camera motion data is None")
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
            has_data = False
            for attr in dir(setup_data):
                if not attr.startswith('_') and not callable(getattr(setup_data, attr)):
                    value = getattr(setup_data, attr)
                    if value is not None and value != '' and value != 'unknown':
                        has_data = True
                        print(f"{attr}: {value}")
            if not has_data:
                print("No camera setup data available (all values are None/empty/unknown)")
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
            has_data = False
            for attr in dir(light_data):
                if not attr.startswith('_') and not callable(getattr(light_data, attr)):
                    value = getattr(light_data, attr)
                    if value is not None and value != '' and value != 'unknown':
                        has_data = True
                        print(f"{attr}: {value}")
            if not has_data:
                print("No lighting setup data available (all values are None/empty/unknown)")
    except Exception as e:
        print(f"Error accessing lighting setup data: {e}")

def search_videos(partial_name: str, video_data_dict: dict):
    """Search for videos containing the given string in their name."""
    matching_videos = []
    for video_name in video_data_dict:
        if partial_name.lower() in video_name.lower():
            matching_videos.append(video_name)
            
    if matching_videos:
        print(f"\nFound {len(matching_videos)} matching videos:")
        for video_name in sorted(matching_videos):
            print(f"- {video_name}")
    else:
        print(f"\nNo videos found containing '{partial_name}'")
