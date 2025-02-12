"""Utilities for interacting with Google Sheets."""

import os
import time
import pickle
import logging
import yaml
import json
from datetime import datetime
from typing import Optional, Any, Callable, Dict, List, Tuple
from dataclasses import dataclass
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constants for sheet data storage
SHEET_DATA_DIR = "exports/sheet_data"
LATEST_SHEET_DATA_FILE = os.path.join(SHEET_DATA_DIR, "latest.json")
CONFIG_PATH = 'configs/labelbox_export.yaml'

def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_sheet_data(sheet_data: Dict[str, Any], create_timestamped: bool = True) -> str:
    """Save sheet data to the standard location.
    
    Args:
        sheet_data: The sheet data to save
        create_timestamped: Whether to also create a timestamped copy
        
    Returns:
        Path to the saved file
    """
    # Create directory if it doesn't exist
    os.makedirs(SHEET_DATA_DIR, exist_ok=True)
    
    # Always save to latest.json
    with open(LATEST_SHEET_DATA_FILE, 'w') as f:
        json.dump(sheet_data, f, indent=2)
    
    # Optionally create timestamped copy
    if create_timestamped:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_file = os.path.join(SHEET_DATA_DIR, f"sheet_data_{timestamp}.json")
        with open(timestamped_file, 'w') as f:
            json.dump(sheet_data, f, indent=2)
    
    return LATEST_SHEET_DATA_FILE

def load_latest_sheet_data() -> Dict[str, Any]:
    """Load the latest sheet data.
    
    Returns:
        The sheet data from latest.json
        
    Raises:
        FileNotFoundError: If no sheet data exists
    """
    if not os.path.exists(LATEST_SHEET_DATA_FILE):
        raise FileNotFoundError("No sheet data found. Run export_sheet_data.py first.")
        
    with open(LATEST_SHEET_DATA_FILE, 'r') as f:
        return json.load(f)

@dataclass
class SheetMetadata:
    """Metadata about a video from Google Sheets."""
    meta_reviewer: str
    double_check: str
    project_name: str
    approver: str

class SheetService:
    """Service for interacting with Google Sheets."""
    
    def __init__(self):
        self._service = None
        self.last_request_time = 0
        self._metadata_cache = {}  # Cache for video metadata
        
    def get_service(self):
        """Get an authorized Google Sheets service."""
        if self._service:
            return self._service
            
        creds = None
        token_path = 'configs/token.json'
        credentials_path = 'configs/credentials.json'
        
        # Try to load existing credentials
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/spreadsheets.readonly'])
            except Exception as e:
                logging.warning(f"Error loading token file: {str(e)}")
                logging.info("Removing corrupted token file...")
                os.remove(token_path)
                creds = None
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    ['https://www.googleapis.com/auth/spreadsheets.readonly']
                )
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                
        self._service = build('sheets', 'v4', credentials=creds)
        return self._service

    def execute_with_retry(self, api_call: Callable, api_limits: dict) -> Any:
        """Execute a Google Sheets API call with exponential backoff and rate limiting."""
        min_delay = api_limits['min_delay']
        max_delay = api_limits['max_delay']
        max_retries = api_limits['max_retries']
        delay = min_delay
        
        for attempt in range(max_retries):
            # Ensure minimum delay between requests
            time_since_last = time.time() - self.last_request_time
            if time_since_last < delay:
                time.sleep(delay - time_since_last)
            
            try:
                result = api_call().execute()
                self.last_request_time = time.time()
                return result
                
            except HttpError as e:
                if e.resp.status in [429, 503]:  # Rate limit or backend error
                    if attempt == max_retries - 1:
                        raise
                    delay = min(delay * 2, max_delay)
                    time.sleep(delay)
                else:
                    raise

    def find_sheet_id(self, spreadsheet_id: str, sheet_title: str, api_limits: dict) -> Optional[int]:
        """Find sheet ID by title."""
        try:
            service = self.get_service()
            result = self.execute_with_retry(
                lambda: service.spreadsheets().get(spreadsheetId=spreadsheet_id),
                api_limits
            )
            
            for sheet in result.get('sheets', []):
                if sheet['properties']['title'] == sheet_title:
                    return sheet['properties']['sheetId']
            return None
            
        except Exception as e:
            logging.error(f"Error finding sheet ID for {sheet_title}: {str(e)}")
            return None

    def load_all_sheet_data(self, project_requirements: dict, api_limits: dict) -> Dict[str, SheetMetadata]:
        """Load all sheet data at once and build a lookup table."""
        # Clear existing cache
        self._metadata_cache = {}
        
        # Load sheet configuration
        with open('configs/labelbox_export.yaml', 'r') as f:
            sheets_config = yaml.safe_load(f)['google_sheets']
        
        service = self.get_service()
        
        # Process each spreadsheet
        for approver, spreadsheet_id in sheets_config['approver_spreadsheets'].items():
            try:
                # Get spreadsheet metadata first
                spreadsheet_metadata = self.execute_with_retry(
                    lambda: service.spreadsheets().get(spreadsheetId=spreadsheet_id),
                    api_limits
                )
                
                # Find all project sheets and their IDs, excluding DO NOT DELETE sheets
                sheet_ids = {}
                for sheet in spreadsheet_metadata.get('sheets', []):
                    title = sheet['properties']['title']
                    if "DO NOT DELETE" in title:
                        continue
                    if title in project_requirements:
                        sheet_ids[title] = sheet['properties']['sheetId']
                
                if not sheet_ids:
                    continue
                
                # Build batch request for all sheets
                ranges = []
                for title in sheet_ids.keys():
                    # Properly escape single quotes in sheet names
                    escaped_title = title.replace("'", "\\'")
                    ranges.append(f"'{escaped_title}'!A:M")
                
                result = self.execute_with_retry(
                    lambda: service.spreadsheets().values().batchGet(
                        spreadsheetId=spreadsheet_id,
                        ranges=ranges
                    ),
                    api_limits
                )
                
                # Process each sheet's data
                for value_range in result.get('valueRanges', []):
                    range_name = value_range['range']
                    # Extract project name by removing the sheet range part
                    project_name = range_name.split('!')[0].strip("'")
                    values = value_range.get('values', [])
                    
                    if not values:
                        continue
                    
                    # Find column indices
                    headers = values[0]
                    required_columns = {'Video Name', 'Meta review', 'Double Check'}
                    missing_columns = required_columns - set(headers)
                    
                    if missing_columns:
                        logging.warning(f"Sheet '{project_name}' is missing required columns: {', '.join(missing_columns)}")
                        logging.warning(f"Available columns: {', '.join(headers)}")
                        continue
                        
                    try:
                        video_col = headers.index('Video Name')
                        meta_col = headers.index('Meta review')
                        double_check_col = headers.index('Double Check')
                    except ValueError:
                        continue
                    
                    logging.info(f"Processing sheet: {project_name}")
                    
                    # Process all rows at once
                    for row in values[1:]:
                        if len(row) <= video_col:
                            continue
                        
                        video_name = row[video_col]
                        meta_reviewer = row[meta_col] if len(row) > meta_col else ''
                        double_check = row[double_check_col] if len(row) > double_check_col else ''
                        
                        # Store in cache
                        self._metadata_cache[video_name] = SheetMetadata(
                            meta_reviewer=meta_reviewer,
                            double_check=double_check,
                            project_name=project_name,
                            approver=approver
                        )
                            
            except Exception as e:
                logging.error(f"Error querying spreadsheet for {approver}: {str(e)}")
                continue
        
        return self._metadata_cache

    def get_sheet_data(self, video_name: str, project_requirements: dict, api_limits: dict) -> Optional[SheetMetadata]:
        """Get sheet metadata for a single video from cache."""
        # If cache is empty, load all data
        if not self._metadata_cache:
            self.load_all_sheet_data(project_requirements, api_limits)
        
        return self._metadata_cache.get(video_name)

def load_all_sheet_data(sheets_config: Dict[str, Any], yaml_configs: Optional[Dict[str, Any]] = None, save_data: bool = False) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Load all sheet data at once to minimize API calls.
    
    Args:
        sheets_config: Configuration for Google Sheets
        yaml_configs: Optional YAML configurations for filtering data
        save_data: Whether to save the loaded data to a JSON file
        
    Returns:
        Dictionary mapping video names to their sheet data
    """
    video_data = {}
    
    # Create sheet service with rate limiting
    sheet_service = SheetService()
    
    # Set API limits for rate limiting
    api_limits = {
        'min_delay': 1.0,  # Minimum delay between API calls in seconds
        'max_delay': 32.0,  # Maximum delay between API calls in seconds
        'max_retries': 5  # Maximum number of retries for API calls
    }
    
    def process_spreadsheet(spreadsheet_id: str, approver: Optional[str] = None):
        try:
            # Get spreadsheet metadata with rate limiting
            spreadsheet_metadata = sheet_service.execute_with_retry(
                lambda: sheet_service.get_service().spreadsheets().get(spreadsheetId=spreadsheet_id),
                api_limits
            )
            
            # Process each sheet/project in the spreadsheet
            for sheet in spreadsheet_metadata.get('sheets', []):
                project_name = sheet['properties']['title']
                
                # Skip DO NOT DELETE sheets
                if "DO NOT DELETE" in project_name:
                    continue
                    
                # Skip if project not in yaml_configs (if provided)
                if yaml_configs and project_name not in yaml_configs:
                    continue
                    
                range_name = f"'{project_name}'!A:M"
                
                try:
                    # Get sheet data with rate limiting
                    result = sheet_service.execute_with_retry(
                        lambda: sheet_service.get_service().spreadsheets().values().get(
                            spreadsheetId=spreadsheet_id,
                            range=range_name
                        ),
                        api_limits
                    )
                except Exception:
                    # Try with simplified sheet name if the full name fails
                    simplified_name = project_name.replace(" ", "_").replace("(", "").replace(")", "")
                    range_name = f"'{simplified_name}'!A:M"
                    try:
                        result = sheet_service.execute_with_retry(
                            lambda: sheet_service.get_service().spreadsheets().values().get(
                                spreadsheetId=spreadsheet_id,
                                range=range_name
                            ),
                            api_limits
                        )
                    except Exception as e:
                        logging.warning(f"Error accessing sheet {project_name}: {str(e)}")
                        continue
                
                values = result.get('values', [])
                if not values:
                    continue
                    
                # Find column indices
                headers = values[0]
                required_columns = {'Video Name', 'Meta review', 'Double Check'}
                found_columns = set(headers)
                missing_columns = required_columns - found_columns
                
                if missing_columns:
                    if "DO NOT DELETE" not in project_name:
                        logging.warning(f"Sheet '{project_name}' is missing required columns: {', '.join(missing_columns)}")
                        logging.warning(f"Available columns: {', '.join(headers)}")
                    continue
                
                try:
                    video_col = headers.index('Video Name')
                    meta_col = headers.index('Meta review')
                    double_check_col = headers.index('Double Check')
                except ValueError as e:
                    continue
                
                logging.info(f"Processing sheet: {project_name}")
                
                # Process each row
                for row in values[1:]:
                    if len(row) <= video_col:
                        continue
                        
                    video_name = row[video_col]
                    meta_reviewer = row[meta_col] if len(row) > meta_col else ''
                    double_check = row[double_check_col] if len(row) > double_check_col else ''
                    
                    # Check requirements if yaml_configs provided
                    if yaml_configs and project_name in yaml_configs:
                        requirements = yaml_configs[project_name].get('requirements', {})
                        
                        # Check meta reviewer requirements
                        allowed_reviewers = requirements.get('allowed_meta_reviewers', [])
                        if allowed_reviewers and meta_reviewer not in allowed_reviewers:
                            continue
                            
                        # Check double check requirements
                        required_status = requirements.get('double_check_status')
                        if required_status is not None and double_check != required_status:
                            continue
                    
                    if video_name not in video_data:
                        video_data[video_name] = {}
                    if project_name not in video_data[video_name]:
                        video_data[video_name][project_name] = {
                            'meta_reviewer': meta_reviewer,
                            'double_check': double_check,
                            'approver': approver
                        }
        except Exception as e:
            logging.error(f"Error processing spreadsheet {spreadsheet_id}: {str(e)}")
            return
    
    # Process all spreadsheets
    for approver, spreadsheet_id in sheets_config.get('approver_spreadsheets', {}).items():
        logging.info(f"Processing spreadsheet for approver: {approver}")
        process_spreadsheet(spreadsheet_id, approver)
    
    # Process default spreadsheet if it exists
    if sheets_config.get('default_spreadsheet_id'):
        logging.info("Processing default spreadsheet")
        process_spreadsheet(sheets_config['default_spreadsheet_id'])
    
    # Save data if requested
    if save_data:
        os.makedirs('exports/sheets', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'exports/sheets/sheet_data_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(video_data, f, indent=2)
        logging.info(f"Saved sheet data to {output_file}")
    
    return video_data 