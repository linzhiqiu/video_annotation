#!/usr/bin/env python3

import os
import yaml
import logging
from typing import Optional, Dict, Any, Tuple
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Set these variables to search for a specific video
VIDEO_NAME = "kxcw0iSn0xw.2.6.mp4"  # Name of the video to search for
PROJECT_NAME = "Video Segment Classification (Camera Movement)"  # Name of the project/sheet tab

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )

def get_google_sheets_service():
    """Get an authorized Google Sheets service instance."""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = None
    token_path = 'configs/token.json'
    credentials_path = 'configs/credentials.json'

    # Try to load token, remove if corrupted
    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            logging.warning(f"Error loading token file: {str(e)}")
            logging.info("Removing corrupted token file...")
            os.remove(token_path)
            creds = None

    # Get new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
                
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Save new token
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

def load_config(config_path: str = 'configs/labelbox_export.yaml') -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def find_video_in_sheet(service, spreadsheet_id: str, project_name: str, video_name: str) -> Optional[Tuple[str, str]]:
    """Search for a video in a specific sheet and return its meta reviewer and double check status.
    
    Args:
        service: Google Sheets service instance
        spreadsheet_id: ID of the spreadsheet to search
        project_name: Name of the project/sheet tab
        video_name: Name of the video to search for
        
    Returns:
        Tuple of (meta_reviewer, double_check_status) if found, None otherwise
    """
    try:
        # First get the sheet ID
        sheets_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_id = None
        for sheet in sheets_metadata.get('sheets', []):
            if sheet['properties']['title'] == project_name:
                sheet_id = sheet['properties']['sheetId']
                break
        
        if not sheet_id:
            logging.warning(f"Sheet '{project_name}' not found in spreadsheet")
            return None

        # Get the sheet data using sheet ID instead of name
        range_name = f"'{project_name}'!A:M"  # Still need the name for range
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
        except Exception as e:
            # Try with simplified sheet name if the full name fails
            simplified_name = project_name.replace(" ", "_").replace("(", "").replace(")", "")
            range_name = f"'{simplified_name}'!A:M"
            try:
                result = service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name
                ).execute()
            except Exception as e2:
                logging.error(f"Error accessing sheet with both original and simplified names: {str(e2)}")
                return None
        
        values = result.get('values', [])
        if not values:
            return None
            
        # Find the column indices
        headers = values[0]
        try:
            video_col = headers.index('Video Name')
            meta_col = headers.index('Meta review')
            double_check_col = headers.index('Double Check')
        except ValueError as e:
            logging.error(f"Required column not found: {str(e)}")
            return None
        
        # Search for the video
        for row in values[1:]:  # Skip header row
            if len(row) > video_col and row[video_col] == video_name:
                meta_reviewer = row[meta_col] if len(row) > meta_col else ''
                double_check = row[double_check_col] if len(row) > double_check_col else ''
                return (meta_reviewer, double_check)
                
        return None
        
    except Exception as e:
        logging.error(f"Error searching sheet: {str(e)}")
        return None

def main():
    setup_logging()
    
    # Load config
    config = load_config()
    sheets_config = config.get('google_sheets', {})
    
    # Get Google Sheets service
    service = get_google_sheets_service()
    
    # Search through all spreadsheets
    found = False
    for approver, spreadsheet_id in sheets_config.get('approver_spreadsheets', {}).items():
        result = find_video_in_sheet(service, spreadsheet_id, PROJECT_NAME, VIDEO_NAME)
        if result:
            meta_reviewer, double_check = result
            logging.info(f"\nFound video in {approver}'s spreadsheet:")
            logging.info(f"Meta Reviewer: {meta_reviewer}")
            logging.info(f"Double Check: {double_check}")
            found = True
            break
            
    # Check default spreadsheet if not found
    if not found and sheets_config.get('default_spreadsheet_id'):
        result = find_video_in_sheet(
            service, 
            sheets_config['default_spreadsheet_id'],
            PROJECT_NAME,
            VIDEO_NAME
        )
        if result:
            meta_reviewer, double_check = result
            logging.info(f"\nFound video in default spreadsheet:")
            logging.info(f"Meta Reviewer: {meta_reviewer}")
            logging.info(f"Double Check: {double_check}")
            found = True
            
    if not found:
        logging.info(f"\nVideo {VIDEO_NAME} not found in any spreadsheet for project {PROJECT_NAME}")

if __name__ == '__main__':
    main() 