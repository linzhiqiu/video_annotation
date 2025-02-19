#!/usr/bin/env python3

import os
import json
import yaml
import shutil
import logging
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Tuple, Any
from flask import Flask, render_template
import threading
import time
import signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import tempfile
import uuid
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from datetime import datetime
from google.oauth2 import service_account
import cv2
import numpy as np
from PIL import Image
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive']  # Simplified to just Drive scope

def find_video_file(videos_dir: str, video_name: str) -> str:
    """
    Search for a video file recursively in the videos directory.
    Returns the path to the video file if found, None otherwise.
    
    The function tries multiple search patterns:
    1. Exact match with extension
    2. Case-insensitive match
    3. Match with different path separators
    4. Match ignoring some special characters
    5. Match with or without file extension
    """
    if not os.path.exists(videos_dir):
        logger.error(f"Videos directory not found: {videos_dir}")
        return None
    
    # Common video extensions
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.MP4', '.AVI', '.MOV', '.MKV')
    
    # Clean up video name for searching
    base_name = os.path.splitext(video_name)[0]  # Remove extension if present
    
    # Different search patterns to try
    patterns = [
        f"**/{video_name}",  # Exact match with extension
        f"**/{base_name}.*",  # Exact match without extension
        f"**/*{video_name}*",  # Contains full name with extension
        f"**/*{base_name}*.*",  # Contains base name
    ]
    
    # Additional patterns with cleaned up name
    cleaned_name = re.sub(r'[_\-.]', '', base_name)  # Remove common separators
    if cleaned_name != base_name:
        patterns.append(f"**/*{cleaned_name}*.*")
    
    # Try each pattern
    for pattern in patterns:
        for ext in video_extensions:
            if not pattern.endswith('.*'):
                if not pattern.endswith(ext):
                    search_pattern = pattern + ext
                else:
                    search_pattern = pattern
            else:
                search_pattern = pattern
                
            try:
                matches = list(Path(videos_dir).glob(search_pattern))
                if matches:
                    # If multiple matches found, try to find the best match
                    if len(matches) > 1:
                        # First try exact name match
                        exact_matches = [m for m in matches if m.stem == base_name]
                        if exact_matches:
                            return str(exact_matches[0])
                        
                        # Then try closest match by length
                        matches.sort(key=lambda x: abs(len(x.stem) - len(base_name)))
                        logger.info(f"Multiple matches found for {video_name}, using closest match: {matches[0]}")
                    
                    return str(matches[0])
            except Exception as e:
                logger.warning(f"Error searching with pattern {search_pattern}: {str(e)}")
                continue
    
    # Try one final search with very loose matching
    try:
        # Get all video files recursively
        all_videos = []
        for ext in video_extensions:
            all_videos.extend(Path(videos_dir).rglob(f"*{ext}"))
        
        # Try to find the best match
        if all_videos:
            # Create a simplified version of the search name
            simple_search = re.sub(r'[^a-zA-Z0-9]', '', base_name.lower())
            
            # Find potential matches
            potential_matches = []
            for video_path in all_videos:
                simple_name = re.sub(r'[^a-zA-Z0-9]', '', video_path.stem.lower())
                if simple_search in simple_name or simple_name in simple_search:
                    potential_matches.append(video_path)
            
            if potential_matches:
                # Sort by similarity to original name
                potential_matches.sort(key=lambda x: abs(len(x.stem) - len(base_name)))
                logger.info(f"Found potential match for {video_name}: {potential_matches[0]}")
                return str(potential_matches[0])
    except Exception as e:
        logger.warning(f"Error in final search attempt for {video_name}: {str(e)}")
    
    return None

def extract_video_frames(video_path: str, num_frames: int) -> List[np.ndarray]:
    """
    Extract evenly spaced frames from a video.
    Returns a list of numpy arrays containing the frames.
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return []
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Could not open video file: {video_path}")
            return []
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        # logger.info(f"Video info - Total frames: {total_frames}, FPS: {fps}, Duration: {duration:.2f}s")
        
        if total_frames <= 0:
            logger.error(f"Could not read frames from video: {video_path}")
            return []
        
        # Calculate frame indices to extract
        indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        frames = []
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
                # logger.debug(f"Successfully extracted frame {idx} ({len(frames)}/{num_frames})")
            else:
                logger.warning(f"Failed to read frame at index {idx}")
        
        cap.release()
        # logger.info(f"Successfully extracted {len(frames)}/{num_frames} frames")
        return frames
    
    except Exception as e:
        logger.error(f"Error extracting frames from video {video_path}: {str(e)}")
        return []

def create_frame_preview(frames: List[np.ndarray], max_width: int = 800) -> Image.Image:
    """
    Create a horizontal preview image from the extracted frames.
    Resizes frames to maintain aspect ratio while fitting within max_width.
    Returns a PIL Image object.
    """
    if not frames:
        return None
    
    # Get dimensions of first frame
    height, width = frames[0].shape[:2]
    num_frames = len(frames)
    
    # Calculate new dimensions to fit within max_width
    new_width = max_width // num_frames
    scale = new_width / width
    new_height = int(height * scale)
    
    # Resize frames
    resized_frames = [cv2.resize(frame, (new_width, new_height)) for frame in frames]
    
    # Concatenate horizontally
    preview = np.concatenate(resized_frames, axis=1)
    
    # Convert to PIL Image
    return Image.fromarray(preview)

def get_video_preview_base64(videos_dir: str, video_name: str, num_frames: int) -> str:
    """
    Generate a base64-encoded preview image for a video.
    Returns the base64 string or None if the video cannot be processed.
    """
    # logger.info(f"Attempting to generate preview for video: {video_name}")
    
    video_path = find_video_file(videos_dir, video_name)
    if not video_path:
        logger.warning(f"Could not find video file for: {video_name}")
        logger.warning(f"Searched in directory: {videos_dir}")
        return None
    
    # logger.info(f"Found video file at: {video_path}")
    frames = extract_video_frames(video_path, num_frames)
    if not frames:
        logger.warning(f"Could not extract frames from video: {video_name}")
        return None
    
    # logger.info(f"Successfully extracted {len(frames)} frames from video")
    preview_image = create_frame_preview(frames)
    if not preview_image:
        logger.warning(f"Could not create preview image for video: {video_name}")
        return None
    
    # logger.info(f"Successfully created preview image for video: {video_name}")
    
    # Convert to base64
    try:
        buffer = io.BytesIO()
        preview_image.save(buffer, format='PNG')
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # logger.info(f"Successfully encoded preview image to base64")
        return base64_string
    except Exception as e:
        logger.error(f"Error encoding preview image to base64: {str(e)}")
        return None

def get_google_drive_service():
    """Sets up and returns Google Drive service."""
    # Try service account authentication first
    service_account_path = 'configs/service-account.json'
    if os.path.exists(service_account_path):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=SCOPES
            )
            logging.info("Successfully authenticated using service account")
            return build('drive', 'v3', credentials=credentials)
        except Exception as e:
            logging.warning(f"Service account authentication failed: {str(e)}")
            logging.info("Falling back to OAuth authentication")
    
    # Fall back to OAuth if service account fails or isn't configured
    creds = None
    token_path = 'configs/token.json'
    credentials_path = 'configs/credentials.json'
    
    # Try to load existing credentials
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            logging.info("Successfully loaded existing credentials")
        except Exception as e:
            logging.warning(f"Error loading token file: {str(e)}")
            logging.info("Removing corrupted token file...")
            os.remove(token_path)
            creds = None
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logging.info("Attempting to refresh expired token...")
                creds.refresh(Request())
                logging.info("Successfully refreshed token")
                
                # Save the refreshed credentials
                os.makedirs(os.path.dirname(token_path), exist_ok=True)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                logging.info("Saved refreshed token")
            except Exception as e:
                logging.error(f"Error refreshing token: {str(e)}")
                logging.info("Token refresh failed, removing token file...")
                if os.path.exists(token_path):
                    os.remove(token_path)
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            
            # Check if we're in a headless environment
            if 'DISPLAY' not in os.environ:
                raise EnvironmentError(
                    "No display available. Please generate token.json on a machine with a browser first. "
                    "Copy the generated token.json to this machine's configs directory. "
                    "If you already have a token.json and are seeing this error, the token may have expired "
                    "and failed to refresh. Please generate a new token on a machine with a browser."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES
            )
            creds = flow.run_local_server(
                port=0,
                access_type='offline',
                prompt='consent',  # Force prompt to ensure refresh token
                include_granted_scopes='true'
            )
            
            # Save the credentials for the next run
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            logging.info("Saved new token")
    
    return build('drive', 'v3', credentials=creds)

def create_drive_folder_structure(drive_service, parent_folder_id: str, test_type: str, test_number: str) -> str:
    """Create folder structure in Google Drive and return the final folder ID."""
    # Create test type folder if it doesn't exist
    test_type_folder = None
    query = f"name = '{test_type}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_folder_id}' in parents and trashed = false"
    
    try:
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            orderBy='createdTime'
        ).execute()
        
        if results['files']:
            # Use the first (oldest) folder found
            test_type_folder = results['files'][0]['id']
            logging.info(f"Found existing folder for {test_type}")
        else:
            folder_metadata = {
                'name': test_type,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            file = drive_service.files().create(
                body=folder_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            test_type_folder = file['id']
            logging.info(f"Created new folder for {test_type}")
    except Exception as e:
        logging.error(f"Error handling test type folder {test_type}: {str(e)}")
        raise
    
    # Create test number folder if it doesn't exist
    test_folder = None
    test_folder_name = f'test{test_number}'
    query = f"name = '{test_folder_name}' and mimeType = 'application/vnd.google-apps.folder' and '{test_type_folder}' in parents and trashed = false"
    
    try:
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            orderBy='createdTime'
        ).execute()
        
        if results['files']:
            # Use the first (oldest) folder found
            test_folder = results['files'][0]['id']
            logging.info(f"Found existing folder for {test_folder_name}")
        else:
            folder_metadata = {
                'name': test_folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [test_type_folder]
            }
            file = drive_service.files().create(
                body=folder_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            test_folder = file['id']
            logging.info(f"Created new folder for {test_folder_name}")
    except Exception as e:
        logging.error(f"Error handling test folder {test_folder_name}: {str(e)}")
        raise
    
    return test_folder

def upload_pdf_to_drive(drive_service, folder_id: str, pdf_data: bytes, filename: str, test_type: str = None, test_number: str = None) -> str:
    """Upload PDF to Google Drive and return the file ID."""
    try:
        # If test_type and test_number are provided, create/get folder structure
        target_folder_id = folder_id
        if test_type and test_number:
            # Create test type folder if needed
            query = f"name = '{test_type}' and mimeType = 'application/vnd.google-apps.folder' and '{folder_id}' in parents and trashed = false"
            results = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            if results['files']:
                test_type_folder = results['files'][0]['id']
                logging.info(f"Found existing folder for {test_type}")
            else:
                folder_metadata = {
                    'name': test_type,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [folder_id]
                }
                test_type_folder = drive_service.files().create(
                    body=folder_metadata,
                    fields='id',
                    supportsAllDrives=True
                ).execute()['id']
                logging.info(f"Created new folder for {test_type}")
            
            # Create test number folder if needed
            test_folder_name = f'test{test_number}'
            query = f"name = '{test_folder_name}' and mimeType = 'application/vnd.google-apps.folder' and '{test_type_folder}' in parents and trashed = false"
            results = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            if results['files']:
                target_folder_id = results['files'][0]['id']
                logging.info(f"Found existing folder for {test_folder_name}")
            else:
                folder_metadata = {
                    'name': test_folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [test_type_folder]
                }
                target_folder_id = drive_service.files().create(
                    body=folder_metadata,
                    fields='id',
                    supportsAllDrives=True
                ).execute()['id']
                logging.info(f"Created new folder for {test_folder_name}")
        
        # Check if file already exists in the target folder
        query = f"name = '{filename}' and '{target_folder_id}' in parents and trashed = false"
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        # Create media
        fh = io.BytesIO(pdf_data)
        media = MediaIoBaseUpload(fh, mimetype='application/pdf', resumable=True)
        
        if results['files']:
            # Update existing file
            existing_file = results['files'][0]
            file = drive_service.files().update(
                fileId=existing_file['id'],
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()
            logging.info(f"Updated existing file: {filename}")
            return file['id']
        else:
            # Create new file
            file_metadata = {
                'name': filename,
                'parents': [target_folder_id]
            }
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()
            logging.info(f"Created new file: {filename}")
            return file['id']
            
    except Exception as e:
        logging.error(f"Error uploading file {filename} to Drive: {str(e)}")
        raise

def load_config() -> dict:
    """Load the scoring configuration file."""
    config_path = 'configs/scoring_config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_project_id_to_ground_truth(config: dict) -> Dict[str, dict]:
    """Create mapping of project IDs to their ground truth annotator info."""
    project_mapping = {}
    for test_type, tests in config['projects'].items():
        for test_num, test_data in tests.items():
            for project_id in test_data['ids']:
                project_mapping[project_id] = {
                    'ground_truth_annotator': test_data.get('ground_truth_annotator')
                }
    return project_mapping

def get_test_number_from_config(config: dict, project_id: str) -> str:
    """Get test number from config structure based on project ID."""
    for test_type, tests in config['projects'].items():
        for test_num, test_data in tests.items():
            if project_id in test_data['ids']:
                # Extract number from test key (e.g., 'test0' -> '0')
                return test_num.replace('test', '')
    return "unknown"

def process_ndjson_file(file_path: str) -> Tuple[Dict[str, Set[str]], Set[str], int, str]:
    """
    Process a single NDJSON file and return:
    - Dict mapping labelers to their labeled video IDs
    - Set of all video IDs
    - Total number of unique videos
    - Project ID from the data
    """
    labeler_videos = defaultdict(set)
    all_videos = set()
    project_id = None
    
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            video_id = data['data_row']['external_id']
            all_videos.add(video_id)
            
            if project_id is None:
                project_id = next(iter(data['projects'].keys()))
            
            for _, project_data in data['projects'].items():
                for label in project_data['labels']:
                    labeler = label['label_details']['created_by']
                    labeler_videos[labeler].add(video_id)
    
    return labeler_videos, all_videos, len(all_videos), project_id

def setup_templates():
    """Setup Flask templates directory and ensure template is accessible."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, 'templates')
    static_dir = os.path.join(script_dir, 'static')
    
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(template_dir, exist_ok=True)
    
    app.template_folder = template_dir
    app.static_folder = static_dir
    
    template_path = os.path.join(template_dir, 'pretest_report.html')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found at {template_path}")

def setup_chrome_driver():
    """Setup Chrome driver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--print-to-pdf-no-header')
    
    # Create a unique temporary directory for user data
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f'--user-data-dir={temp_dir}')
    chrome_options.add_argument(f'--profile-directory=Profile{uuid.uuid4().hex[:8]}')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver, temp_dir
    except Exception as e:
        # Clean up the temporary directory if driver creation fails
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

def generate_pdf_in_memory(html_content: str) -> bytes:
    """Generate PDF from HTML content and return it as bytes."""
    driver = None
    temp_dir = None
    temp_html_path = None
    try:
        # logger.info("Setting up Chrome options for PDF generation")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--print-to-pdf-no-header')
        chrome_options.add_argument('--run-all-compositor-stages-before-draw')
        chrome_options.add_argument('--disable-web-security')
        
        # Create a unique temporary directory for user data
        temp_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f'--user-data-dir={temp_dir}')
        chrome_options.add_argument(f'--profile-directory=Profile{uuid.uuid4().hex[:8]}')
        
        # logger.info("Initializing Chrome driver")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Save HTML content to a temporary file
        # logger.info("Saving HTML content to temporary file")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_html_path = f.name
            # logger.info(f"Temporary HTML file created at: {temp_html_path}")
        
        try:
            # Load the HTML file using file:// protocol
            file_url = f'file://{temp_html_path}'
            # logger.info(f"Loading HTML file from: {file_url}")
            driver.get(file_url)
            
            # Wait for page to load completely
            # logger.info("Waiting for page to load completely")
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            # Additional wait for images to load
            # logger.info("Waiting for images to load")
            time.sleep(2)
            
            # Wait for all images to load
            # logger.info("Verifying all images are loaded")
            driver.execute_script("""
                return Promise.all(Array.from(document.images).map(img => {
                    if (img.complete) return Promise.resolve();
                    return new Promise(resolve => {
                        img.onload = img.onerror = resolve;
                    });
                }));
            """)
            
            # Print to PDF with images enabled
            # logger.info("Generating PDF")
            pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                "printBackground": True,
                "marginTop": 0.4,
                "marginBottom": 0.4,
                "marginLeft": 0.4,
                "marginRight": 0.4,
                "paperWidth": 8.27,  # A4 width in inches
                "paperHeight": 11.7,  # A4 height in inches
            })
            
            # Verify PDF data
            if not pdf.get('data'):
                raise Exception("No PDF data received from Chrome")
            
            # logger.info("Successfully generated PDF data")
            pdf_bytes = base64.b64decode(pdf['data'])
            # logger.info(f"PDF size: {len(pdf_bytes)} bytes")
            
            return pdf_bytes
            
        finally:
            # Clean up temporary HTML file
            if temp_html_path:
                try:
                    os.unlink(temp_html_path)
                    # logger.info("Cleaned up temporary HTML file")
                except Exception as e:
                    logger.warning(f"Failed to clean up temporary HTML file: {e}")
                
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
                # logger.info("Chrome driver closed")
            except Exception as e:
                logger.warning(f"Failed to close Chrome driver: {e}")
        if temp_dir:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
                # logger.info("Cleaned up temporary directory")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {e}")

def calculate_metrics(videos_data: List[dict]) -> dict:
    """Calculate overall metrics from the videos data."""
    total_comparisons = 0
    total_correct = 0
    total_questions = 0
    annotator_stats = defaultdict(lambda: {'correct_answers': 0, 'total_questions': 0})
    question_stats = defaultdict(lambda: {
        'total_comparisons': 0,
        'correct_answers': 0,
        'total_questions': 0,
        'annotator_performance': defaultdict(lambda: {
            'correct_answers': 0,
            'total_questions': 0,
            'ground_truth_occurrences': 0,
            'annotator_occurrences': 0
        })
    })
    
    # Collect statistics
    for video in videos_data:
        for row in video['table_data']:
            question = row['question']
            ground_truth = row['ground_truth']
            
            for username, annotator_data in row['annotators'].items():
                if annotator_data['accuracy'] is not None:
                    total_comparisons += 1
                    question_stats[question]['total_comparisons'] += 1
                    question_stats[question]['total_questions'] += 1
                    question_stats[question]['annotator_performance'][username]['total_questions'] += 1
                    question_stats[question]['annotator_performance'][username]['annotator_occurrences'] += 1
                    
                    if ground_truth:
                        question_stats[question]['annotator_performance'][username]['ground_truth_occurrences'] += 1
                    
                    if annotator_data['accuracy'] == 1.0:
                        total_correct += 1
                        annotator_stats[username]['correct_answers'] += 1
                        question_stats[question]['correct_answers'] += 1
                        question_stats[question]['annotator_performance'][username]['correct_answers'] += 1
                        
                    annotator_stats[username]['total_questions'] += 1
                    total_questions += 1
    
    # Calculate metrics
    precision = total_correct / total_comparisons if total_comparisons > 0 else 0
    recall = total_correct / total_questions if total_questions > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate per-annotator accuracy
    annotator_accuracy = {}
    for username, stats in annotator_stats.items():
        accuracy = stats['correct_answers'] / stats['total_questions'] if stats['total_questions'] > 0 else 0
        annotator_accuracy[username] = {
            'total_questions': stats['total_questions'],
            'correct_answers': stats['correct_answers'],
            'accuracy': accuracy
        }
    
    # Calculate per-question metrics
    questions_metrics = {}
    for question, stats in question_stats.items():
        q_precision = stats['correct_answers'] / stats['total_comparisons'] if stats['total_comparisons'] > 0 else 0
        q_recall = stats['correct_answers'] / stats['total_questions'] if stats['total_questions'] > 0 else 0
        q_f1 = 2 * (q_precision * q_recall) / (q_precision + q_recall) if (q_precision + q_recall) > 0 else 0
        
        annotator_metrics = {}
        for username, perf in stats['annotator_performance'].items():
            ann_precision = perf['correct_answers'] / perf['annotator_occurrences'] if perf['annotator_occurrences'] > 0 else 0
            ann_recall = perf['correct_answers'] / perf['ground_truth_occurrences'] if perf['ground_truth_occurrences'] > 0 else 0
            ann_f1 = 2 * (ann_precision * ann_recall) / (ann_precision + ann_recall) if (ann_precision + ann_recall) > 0 else 0
            
            annotator_metrics[username] = {
                'precision': ann_precision,
                'recall': ann_recall,
                'f1_score': ann_f1,
                'correct_answers': perf['correct_answers'],
                'total_questions': perf['total_questions']
            }
        
        questions_metrics[question] = {
            'overall': {
                'precision': q_precision,
                'recall': q_recall,
                'f1_score': q_f1,
                'total_comparisons': stats['total_comparisons'],
                'correct_answers': stats['correct_answers']
            },
            'annotator_performance': annotator_metrics
        }
    
    return {
        'overall_metrics': {
            'total_comparisons': total_comparisons,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        },
        'annotator_accuracy': annotator_accuracy,
        'questions_metrics': questions_metrics
    }

def load_taxonomy() -> List[str]:
    """Load taxonomy and return ordered list of questions."""
    with open('taxonomy/taxonomy.json', 'r') as f:
        taxonomy = json.load(f)
        return [item['question'] for item in taxonomy]

def process_classification_recursively(classification: dict, annotations: dict):
    """Recursively process a classification and its nested classifications."""
    question = classification['name']
    if "(old)" in question:
        return
        
    # Get answer based on the type of classification
    answer = None
    if 'radio_answer' in classification:
        answer = classification['radio_answer']['name']
        # Process nested classifications in radio answer
        for nested in classification['radio_answer'].get('classifications', []):
            process_classification_recursively(nested, annotations)
    elif 'checklist_answers' in classification:
        answer = [item['name'] for item in classification['checklist_answers']]
        # Process nested classifications in each checklist answer
        for checklist_item in classification['checklist_answers']:
            for nested in checklist_item.get('classifications', []):
                process_classification_recursively(nested, annotations)
    elif 'text_answer' in classification:
        answer = classification['text_answer']['content']
    
    if answer is not None:
        annotations[question] = answer

def extract_ground_truth_from_annotator(ndjson_data: List[dict], annotator_email: str) -> Dict[str, Dict[str, Any]]:
    """Extract ground truth from a specific annotator's annotations."""
    ground_truth_dict = {}
    
    for data in ndjson_data:
        video_name = data['data_row']['external_id']
        annotations = {}
        
        # Process each project's labels
        for project_data in data['projects'].values():
            for label in project_data['labels']:
                if label['label_details']['created_by'] != annotator_email:
                    continue
                
                # Process classifications
                for classification in label['annotations'].get('classifications', []):
                    process_classification_recursively(classification, annotations)
        
        if annotations:  # Only add if there are annotations
            ground_truth_dict[video_name] = annotations
    
    return ground_truth_dict

def prepare_visualization_data(ndjson_data: List[dict], ground_truth_source: dict, target_annotator: str, config: dict = None) -> dict:
    """Prepare data for visualization template."""
    # Load taxonomy for question ordering
    question_order = load_taxonomy()
    
    # Use cached ground truth if available, otherwise load it
    ground_truth_dict = ground_truth_source.get('cached_ground_truth', {})
    if not ground_truth_dict:
        # Get ground truth from annotator
        if ground_truth_source.get('ground_truth_annotator'):
            annotator_email = ground_truth_source['ground_truth_annotator']['email']
            ground_truth_dict = extract_ground_truth_from_annotator(ndjson_data, annotator_email)
            logger.info(f"Using ground truth from annotator: {annotator_email}")
    
    # Get video preview configuration from pdf_generation section
    video_preview_enabled = False
    videos_dir = None
    frames_per_video = 5
    if config and 'pdf_generation' in config:
        pdf_config = config['pdf_generation']
        if 'video_preview' in pdf_config:
            video_preview_enabled = pdf_config['video_preview'].get('enabled', False)
            videos_dir = pdf_config['video_preview'].get('videos_dir')
            frames_per_video = pdf_config['video_preview'].get('frames_per_video', 5)
    
    # Process videos data
    videos_data = []
    all_questions = set()  # Track all possible questions across all videos
    
    # First pass: collect all possible questions from ground truth and annotations
    for data in ndjson_data:
        video_name = data['data_row']['external_id']
        
        # Add questions from ground truth
        if video_name in ground_truth_dict:
            all_questions.update(ground_truth_dict[video_name].keys())
        
        # Add questions from annotations
        for project_id, project_data in data['projects'].items():
            for label in project_data['labels']:
                if label['label_details']['created_by'] != target_annotator:
                    continue
                    
                # Process all classifications recursively to collect questions
                temp_annotations = {}
                for classification in label['annotations'].get('classifications', []):
                    process_classification_recursively(classification, temp_annotations)
                all_questions.update(temp_annotations.keys())
    
    # Second pass: process each video
    for data in ndjson_data:
        video_name = data['data_row']['external_id']
        video_id = data['data_row']['id']
        project_id = next(iter(data['projects'].keys()))  # Get the first project ID
        
        # Create Labelbox editing URL
        video_url = f"https://app.labelbox.com/projects/{project_id}/data-rows/{video_id}"
        
        # Get video preview if enabled
        video_preview = None
        if video_preview_enabled and videos_dir:
            video_preview = get_video_preview_base64(videos_dir, video_name, frames_per_video)
            if video_preview:
                # logger.info(f"Successfully generated preview for video: {video_name}")
                pass
            else:
                logger.warning(f"Could not generate preview for video: {video_name}")
        
        # Collect questions and annotations for target annotator
        annotator_data = defaultdict(list)
        has_labels = False
        
        # Process each project's labels
        for project_id, project_data in data['projects'].items():
            for label in project_data['labels']:
                username = label['label_details']['created_by']
                if username != target_annotator:
                    continue
                    
                # Get all annotations recursively
                temp_annotations = {}
                for classification in label['annotations'].get('classifications', []):
                    process_classification_recursively(classification, temp_annotations)
                
                has_labels = has_labels or bool(temp_annotations)
                
                if temp_annotations:
                    annotator_data[username].extend([
                        {'question': q, 'answer': a} 
                        for q, a in temp_annotations.items()
                    ])
        
        # Prepare table data if either ground truth exists or annotator has labels
        has_ground_truth = video_name in ground_truth_dict
        
        # Always include the video, even if both are empty
        table_data = []
        
        # Only create table data if either has content
        if has_ground_truth or has_labels:
            # Sort questions according to taxonomy order
            sorted_questions = sorted(all_questions, key=lambda q: question_order.index(q) if q in question_order else len(question_order))
            
            # Process all collected questions
            for question in sorted_questions:
                ground_truth = ground_truth_dict.get(video_name, {}).get(question)
                
                # Get annotator's answer
                answer = None
                if target_annotator in annotator_data:
                    answer = next((ann['answer'] for ann in annotator_data[target_annotator] 
                                if ann['question'] == question), None)
                
                # Determine correctness based on the different cases
                is_correct = None
                if has_ground_truth:  # Ground truth exists
                    if answer is not None:  # Annotator provided an answer
                        if isinstance(answer, list) and isinstance(ground_truth, list):
                            is_correct = sorted(answer) == sorted(ground_truth)
                        else:
                            is_correct = str(answer).strip() == str(ground_truth).strip()
                    else:  # Annotator didn't provide an answer
                        is_correct = 0.0 if ground_truth is not None else None
                elif has_labels and ground_truth is None:  # No ground truth but annotator labeled
                    is_correct = 0.0  # Wrong by default when no ground truth exists
                
                row = {
                    'question': question,
                    'ground_truth': ground_truth if ground_truth is not None else "",
                    'annotators': {
                        target_annotator: {
                            'answer': answer,
                            'accuracy': 1.0 if is_correct else 0.0 if is_correct is not None else None
                        }
                    }
                }
                
                table_data.append(row)
        
        videos_data.append({
            'video_name': video_name,
            'video_url': video_url,
            'video_preview': video_preview,
            'table_data': table_data,
            'annotator_usernames': [target_annotator]
        })
    
    # Calculate metrics
    metrics = calculate_metrics(videos_data)
    
    return {
        'videos_data': videos_data,
        'compare_groundtruth': True if ground_truth_dict else False,
        'hide_unused_labels': False,
        'annotator': target_annotator,
        'overall_metrics': metrics['overall_metrics'],
        'annotator_accuracy': metrics['annotator_accuracy'],
        'questions_metrics': metrics['questions_metrics'],
        'video_preview_enabled': video_preview_enabled
    }

def should_process_project(project_id: str, test_num: str, config: dict) -> bool:
    """Check if we should process this project based on config."""
    target_project = config.get('pdf_generation', {}).get('target_project')
    target_test = config.get('pdf_generation', {}).get('target_test')
    
    # If neither target is set, process all projects
    if target_project is None and target_test is None:
        return True
    
    # Check project ID match if target_project is set
    if target_project is not None and project_id != target_project:
        return False
    
    # Check test number match if target_test is set
    if target_test is not None and f"test{test_num}" != target_test:
        return False
    
    return True

def should_process_annotator(annotator: str, config: dict) -> bool:
    """Check if we should process this annotator based on config."""
    target_annotator = config.get('pdf_generation', {}).get('target_annotator')
    if target_annotator is None:
        return True
    return annotator == target_annotator

def should_generate_pdf(pdf_path: str, config: dict) -> bool:
    """Check if we should generate this PDF based on config."""
    skip_existing = config.get('pdf_generation', {}).get('skip_existing', False)
    if skip_existing and os.path.exists(pdf_path):
        logger.info(f"Skipping existing PDF: {pdf_path}")
        return False
    return True

def print_drive_folder_structure(drive_service, folder_id: str, indent: str = "") -> None:
    """
    Recursively prints the folder structure in Google Drive, showing both folders and files.
    
    Args:
        drive_service: Authorized Google Drive API service instance
        folder_id: ID of the Google Drive folder to list
        indent: Current indentation string for pretty printing
    """
    try:
        # Get folder metadata to check if it's in a Shared Drive
        folder_metadata = drive_service.files().get(
            fileId=folder_id,
            fields="driveId,name",
            supportsAllDrives=True
        ).execute()
        
        drive_id = folder_metadata.get("driveId")
        folder_name = folder_metadata.get("name", "Root Folder")
        
        print(f"{indent}📁 {folder_name} (ID: {folder_id})")
        
        # List files and subfolders
        query = f"'{folder_id}' in parents and trashed=false"
        page_token = None
        
        while True:
            params = {
                'q': query,
                'fields': "nextPageToken, files(id, name, mimeType)",
                'pageSize': 100,
                'pageToken': page_token,
                'orderBy': 'name',  # Sort items alphabetically
                'includeItemsFromAllDrives': True,
                'supportsAllDrives': True
            }
            
            if drive_id:
                params['corpora'] = 'drive'
                params['driveId'] = drive_id
            else:
                params['corpora'] = 'user'
            
            response = drive_service.files().list(**params).execute()
            items = response.get('files', [])
            
            # Sort items: folders first, then files, both alphabetically
            folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
            files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']
            
            # Process folders first
            for folder in sorted(folders, key=lambda x: x['name'].lower()):
                print_drive_folder_structure(drive_service, folder['id'], indent + "  ")
            
            # Then process files
            for file in sorted(files, key=lambda x: x['name'].lower()):
                print(f"{indent}  📄 {file['name']} (ID: {file['id']})")
            
            page_token = response.get('nextPageToken')
            if not page_token:
                break
                
    except Exception as e:
        logging.error(f"Error listing folder contents: {str(e)}")
        print(f"{indent}❌ Error accessing folder: {str(e)}")

def main():
    """Main entry point for the script."""
    # Setup Flask templates
    setup_templates()
    
    config = load_config()
    project_ground_truth = get_project_id_to_ground_truth(config)
    
    # Get Google Drive folder ID from config
    drive_folder_id = config.get('pdf_generation', {}).get('drive_folder_id')
    if not drive_folder_id:
        raise ValueError("Google Drive folder ID not specified in config")
    
    # Initialize Google Drive service
    drive_service = get_google_drive_service()
    
    # # Print current Drive folder structure for debugging
    # logger.info("\nCurrent Google Drive folder structure:")
    # logger.info("-" * 50)
    # print_drive_folder_structure(drive_service, drive_folder_id)
    # logger.info("-" * 50 + "\n")
    
    # Process each test type directory
    base_dir = config['output_dir']
    pdfs_dir = config['pdfs_dir']
    
    # Check if we should create a "new" folder
    create_new_folder = config.get('pdf_generation', {}).get('create_new_folder', True)
    new_pdfs_dir = os.path.join(pdfs_dir, 'new') if create_new_folder else None
    if create_new_folder:
        os.makedirs(new_pdfs_dir, exist_ok=True)
    
    # Cache for ground truth data
    ground_truth_cache = {}
    
    # Create Flask application context
    with app.app_context():
        for test_type in config['projects'].keys():
            ndjson_dir = os.path.join(base_dir, test_type, 'ndjson')
            
            if not os.path.exists(ndjson_dir):
                logger.info(f"Skipping {test_type}: Directory not found")
                continue
                
            logger.info(f"Processing {test_type} files")
            
            # First, load and cache ground truth data for all projects in each test
            test_ground_truth_cache = {}
            for test_num, test_data in config['projects'][test_type].items():
                # Skip if we shouldn't process this test/project
                should_process = any(should_process_project(project_id, test_num.replace('test', ''), config)
                                   for project_id in test_data['ids'])
                if not should_process:
                    logger.info(f"Skipping {test_type} {test_num}: Not targeted for processing")
                    continue
                
                if not test_data.get('ground_truth_annotator'):
                    continue
                    
                ground_truth_annotator = test_data['ground_truth_annotator']
                ground_truth_project_id = ground_truth_annotator['project_id']
                ground_truth_email = ground_truth_annotator['email']
                
                # Load ground truth data from the ground truth project
                ground_truth_files = [f for f in os.listdir(ndjson_dir) 
                                    if ground_truth_project_id in f and f.endswith('.ndjson')]
                
                if ground_truth_files:
                    ground_truth_path = os.path.join(ndjson_dir, ground_truth_files[0])
                    try:
                        with open(ground_truth_path, 'r') as f:
                            ground_truth_ndjson = [json.loads(line) for line in f]
                        ground_truth_dict = extract_ground_truth_from_annotator(ground_truth_ndjson, ground_truth_email)
                        test_ground_truth_cache[test_num] = ground_truth_dict
                        
                        # Also cache for each project ID in this test
                        for project_id in test_data['ids']:
                            ground_truth_cache[project_id] = ground_truth_dict
                            
                        logger.info(f"Loaded ground truth from {ground_truth_email} for {test_type} {test_num}")
                    except Exception as e:
                        logger.error(f"Error loading ground truth for {test_type} {test_num}: {str(e)}")
                        continue
            
            # Now process each NDJSON file
            for file_name in filter(lambda x: x.endswith('.ndjson'), os.listdir(ndjson_dir)):
                file_path = os.path.join(ndjson_dir, file_name)
                try:
                    labeler_videos, all_videos, total_entries, project_id = process_ndjson_file(file_path)
                except Exception as e:
                    logger.error(f"Error processing file {file_name}: {str(e)}")
                    continue
                
                ground_truth_source = project_ground_truth.get(project_id, {})
                
                # Skip if no ground truth annotator is configured
                if not ground_truth_source.get('ground_truth_annotator'):
                    logger.info(f"Skipping project {project_id}: No ground truth annotator configured")
                    continue
                
                # Get test number from config structure
                test_number = get_test_number_from_config(config, project_id)
                if test_number == "unknown":
                    logger.error(f"Could not find test number for project {project_id}")
                    continue
                
                # Check if we should process this project/test
                if not should_process_project(project_id, test_number, config):
                    logger.info(f"Skipping project {project_id} test{test_number}: Not targeted for processing")
                    continue
                
                # Load NDJSON data once for the project
                try:
                    with open(file_path, 'r') as f:
                        ndjson_data = [json.loads(line) for line in f]
                except Exception as e:
                    logger.error(f"Error reading NDJSON data from {file_name}: {str(e)}")
                    continue
                
                # Verify we have ground truth data for this project
                if project_id not in ground_truth_cache:
                    logger.error(f"No ground truth data found for project {project_id}")
                    continue
                
                # Get consistent labelers
                consistent_labelers = {
                    labeler for labeler, videos in labeler_videos.items()
                    if len(videos) == total_entries
                }
                
                # Process each consistent labeler
                for labeler in consistent_labelers:
                    # Check if we should process this annotator
                    if not should_process_annotator(labeler, config):
                        logger.info(f"Skipping annotator: {labeler}")
                        continue
                        
                    logger.info(f"Processing labeler: {labeler}")
                    
                    # Generate PDF filename and paths
                    pdf_filename = f"{labeler.replace('@', '_at_')}_{project_id}.pdf"
                    pdf_path = os.path.join(pdfs_dir, test_type, f"test{test_number}", pdf_filename)
                    
                    # Create local directory structure
                    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                    
                    # Check if we should generate this PDF
                    if not should_generate_pdf(pdf_path, config):
                        continue
                    
                    try:
                        # Prepare data for this labeler using cached ground truth
                        ground_truth_source['cached_ground_truth'] = ground_truth_cache[project_id]
                        labeler_data = prepare_visualization_data(ndjson_data, ground_truth_source, labeler, config)
                        
                        logger.info(f"Generating PDF for {labeler}")
                        
                        # Generate PDF
                        html_content = render_template('pretest_report.html', **labeler_data)
                        pdf_data = generate_pdf_in_memory(html_content)
                        
                        # Save PDF
                        with open(pdf_path, 'wb') as f:
                            f.write(pdf_data)
                        logger.info(f"PDF saved locally: {pdf_path}")
                        
                        # Copy to new folder if enabled
                        if create_new_folder:
                            new_pdf_path = os.path.join(new_pdfs_dir, pdf_filename)
                            with open(new_pdf_path, 'wb') as f:
                                f.write(pdf_data)
                            logger.info(f"PDF copied to new folder: {new_pdf_path}")
                        
                        # Upload to Google Drive
                        file_id = upload_pdf_to_drive(drive_service, drive_folder_id, pdf_data, pdf_filename, test_type, test_number)
                        logger.info(f"PDF uploaded to Google Drive with ID: {file_id}")
                        
                    except Exception as e:
                        logger.error(f"Error generating/uploading PDF for {labeler} in project {project_id}: {str(e)}")
                        logger.error(f"Full error: {str(e.__class__.__name__)}: {str(e)}")
                        continue
        
        logger.info("\nPDF generation and upload complete")

if __name__ == "__main__":
    main() 