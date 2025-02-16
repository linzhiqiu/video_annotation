#!/usr/bin/env python3

import json
import os
import logging
import yaml
import pandas as pd
import time
from datetime import datetime
from collections import defaultdict
from typing import Dict, Any, List, Callable, Optional
from googleapiclient.errors import HttpError

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from labelbox import Client
from labelbox.data.serialization import NDJsonConverter

# Import functions from export_labelbox_data.py
from export_labelbox_data import (
    export_project_data,
    load_config,
    setup_logging
)

# Import functions from process_ndjson.py
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.process_ndjson import extract_workflow_details, extract_answers

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Rate limiting constants
MIN_DELAY = 1.0  # Minimum delay between API calls in seconds
MAX_DELAY = 32.0  # Maximum delay between API calls in seconds
MAX_RETRIES = 5  # Maximum number of retries for API calls

def execute_with_retry(api_call: Callable, *args, **kwargs) -> Any:
    """Execute a Google Sheets API call with exponential backoff and rate limiting."""
    delay = MIN_DELAY
    last_request_time = getattr(execute_with_retry, 'last_request_time', 0)
    
    for attempt in range(MAX_RETRIES):
        # Ensure minimum delay between requests
        time_since_last_request = time.time() - last_request_time
        if time_since_last_request < delay:
            time.sleep(delay - time_since_last_request)
        
        try:
            result = api_call(*args, **kwargs).execute()
            execute_with_retry.last_request_time = time.time()
            return result
            
        except HttpError as e:
            if e.resp.status in [429, 503]:  # Rate limit or backend error
                if attempt == MAX_RETRIES - 1:
                    raise  # Re-raise on last attempt
                
                delay = min(delay * 2, MAX_DELAY)
                logging.warning(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
                
            raise  # Re-raise other HTTP errors
            
        except Exception as e:
            raise

def get_google_sheets_service():
    """Sets up and returns Google Sheets service."""
    creds = None
    token_path = 'configs/token.json'
    credentials_path = 'configs/credentials.json'
    
    # Delete token.json if it exists to force new authentication
    if os.path.exists(token_path):
        os.remove(token_path)
    
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, 
        SCOPES,
        redirect_uri='http://localhost:8080/'
    )
    creds = flow.run_local_server(
        port=8080,
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # Save the credentials for the next run
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

def get_sheet_id_by_title(service, spreadsheet_id: str, sheet_title: str) -> int:
    """Gets the sheet ID for a sheet with the given title."""
    try:
        spreadsheet = execute_with_retry(
            service.spreadsheets().get,
            spreadsheetId=spreadsheet_id
        )
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == sheet_title:
                return sheet['properties']['sheetId']
        return None
    except Exception as e:
        logging.error(f'Error getting sheet ID for "{sheet_title}": {str(e)}')
        raise

def convert_iso_to_google_sheets_friendly(timestamp: str) -> str:
    """Convert a single ISO timestamp to Google Sheets friendly format."""
    if not timestamp:
        return ''
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return timestamp

def get_text_box_questions_from_taxonomy(taxonomy_path: str, project_name: str) -> Dict[str, str]:
    """Extract text box questions from the taxonomy file for a specific project."""
    with open(taxonomy_path, 'r') as f:
        taxonomy = json.load(f)
    
    text_box_questions = []
    
    def extract_text_box_questions(node):
        if isinstance(node, dict):
            if (node.get('type') == 'text' and 
                node.get('group', '') == project_name):
                name = node.get('name')
                question = node.get('question', name)
                if name and question:
                    text_box_questions.append((name, question))
            
            for value in node.values():
                extract_text_box_questions(value)
        elif isinstance(node, list):
            for item in node:
                extract_text_box_questions(item)
    
    extract_text_box_questions(taxonomy)
    return dict(text_box_questions)

def create_or_update_sheet(service, spreadsheet_id, display_name, new_df):
    """Create or update a sheet in the spreadsheet."""
    try:
        # Get existing sheets
        spreadsheet = execute_with_retry(
            service.spreadsheets().get,
            spreadsheetId=spreadsheet_id
        )
        sheets = spreadsheet.get('sheets', [])
        
        # Format sheet name for API calls
        api_sheet_name = display_name.replace("'", "\\'")
        range_name = f"'{api_sheet_name}'!A1:Z"
        
        # Find if sheet already exists
        sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == display_name:
                sheet_id = sheet['properties']['sheetId']
                break
        
        # If sheet doesn't exist, create it and add all data
        if sheet_id is None:
            request = {
                'addSheet': {
                    'properties': {
                        'title': display_name
                    }
                }
            }
            execute_with_retry(
                service.spreadsheets().batchUpdate,
                spreadsheetId=spreadsheet_id,
                body={'requests': [request]}
            )
            
            # Get the new sheet's ID
            sheet_id = None
            for sheet in execute_with_retry(
                service.spreadsheets().get,
                spreadsheetId=spreadsheet_id
            ).get('sheets', []):
                if sheet['properties']['title'] == display_name:
                    sheet_id = sheet['properties']['sheetId']
                    break
            
            # For new sheets, just add all the data
            values = [new_df.columns.tolist()]  # Header row
            for _, row in new_df.iterrows():
                values.append([str(val) if pd.notnull(val) else '' for val in row])
            
            execute_with_retry(
                service.spreadsheets().values().update,
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': values}
            )
            
            logging.info(f'Sheet "{display_name}": Created new sheet with {len(new_df)} rows')
            
        else:
            # For existing sheets, get current data
            result = execute_with_retry(
                service.spreadsheets().values().get,
                spreadsheetId=spreadsheet_id,
                range=range_name
            )
            
            if 'values' in result:
                current_values = result['values']
                headers = current_values[0]
                
                # Pad each row to match the number of columns
                padded_values = []
                for row in current_values[1:]:  # Skip header
                    padded_row = row + [''] * (len(headers) - len(row))
                    padded_values.append(padded_row)
                
                # Convert current sheet data to DataFrame
                current_df = pd.DataFrame(padded_values, columns=headers)
                existing_rows = len(current_df)
                
                # Get video names from current data
                current_videos = set(current_df['Video Name'].values)
                
                # Filter new_df to only include videos not in current data
                new_videos_df = new_df[~new_df['Video Name'].isin(current_videos)].copy()
                new_rows = len(new_videos_df)
                
                if not new_videos_df.empty:
                    # Make sure new_df has all columns from current sheet
                    for col in headers:
                        if col not in new_videos_df.columns:
                            new_videos_df[col] = ''
                    
                    # Reorder columns to match current sheet
                    new_videos_df = new_videos_df[headers]
                    
                    # Create requests to insert rows and update their values
                    requests = []
                    
                    # First, insert the new rows after the header
                    requests.append({
                        'insertDimension': {
                            'range': {
                                'sheetId': sheet_id,
                                'dimension': 'ROWS',
                                'startIndex': 1,  # After header
                                'endIndex': 1 + new_rows  # Number of new rows
                            },
                            'inheritFromBefore': False
                        }
                    })
                    
                    # Clear the newly inserted rows to ensure no data inheritance
                    requests.append({
                        'updateCells': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': 1,
                                'endRowIndex': 1 + new_rows,
                                'startColumnIndex': 0,
                                'endColumnIndex': len(headers)
                            },
                            'fields': 'userEnteredValue'
                        }
                    })
                    
                    # Execute the insert and clear requests first
                    execute_with_retry(
                        service.spreadsheets().batchUpdate,
                        spreadsheetId=spreadsheet_id,
                        body={'requests': requests}
                    )
                    
                    # Now update the values in the newly inserted rows
                    new_values = []
                    for _, row in new_videos_df.iterrows():
                        row_values = [str(val) if pd.notnull(val) else '' for val in row]
                        row_values.extend([''] * (len(headers) - len(row_values)))
                        new_values.append(row_values)
                    
                    update_range = f"'{api_sheet_name}'!A2:{chr(65 + len(headers))}{1 + new_rows}"
                    execute_with_retry(
                        service.spreadsheets().values().update,
                        spreadsheetId=spreadsheet_id,
                        range=update_range,
                        valueInputOption='RAW',
                        body={'values': new_values}
                    )
                    
                    logging.info(f'Sheet "{display_name}": Added {new_rows} new rows at the top, {existing_rows} existing rows unchanged')
                else:
                    logging.info(f'Sheet "{display_name}": No new rows to add, {existing_rows} existing rows unchanged')
            else:
                # If sheet is empty, treat it like a new sheet
                values = [new_df.columns.tolist()]  # Header row
                for _, row in new_df.iterrows():
                    values.append([str(val) if pd.notnull(val) else '' for val in row])
                
                execute_with_retry(
                    service.spreadsheets().values().update,
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='RAW',
                    body={'values': values}
                )
                
                logging.info(f'Sheet "{display_name}": Created new sheet with {len(new_df)} rows')
        
        # Apply formatting
        if sheet_id:
            apply_sheet_formatting(service, spreadsheet_id, sheet_id, headers)
            
        return True
        
    except Exception as e:
        logging.error(f'Error updating sheet "{display_name}": {str(e)}')
        return False

def apply_sheet_formatting(service, spreadsheet_id: str, sheet_id: int, headers: List[str]):
    """Apply formatting to the sheet."""
    requests = []
    
    # Set column widths
    video_name_index = headers.index('Video Name')
    editing_url_index = headers.index('Editing URL')
    
    for col_index in [video_name_index, editing_url_index]:
        requests.extend([
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": col_index,
                        "endIndex": col_index + 1
                    },
                    "properties": {
                        "pixelSize": 150
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startColumnIndex": col_index,
                        "endColumnIndex": col_index + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat.wrapStrategy"
                }
            }
        ])
    
    # Format headers
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0.8,
                        "green": 0.8,
                        "blue": 0.8
                    },
                    "textFormat": {
                        "bold": True
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }
    })
    
    execute_with_retry(
        service.spreadsheets().batchUpdate,
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    )

def process_ndjson_export(ndjson_path: str, issues_dir: str, taxonomy_path: str, include_issues: bool = True) -> List[Dict[str, Any]]:
    """Process NDJSON export file and extract relevant data."""
    logging.info(f"Starting to process NDJSON file: {ndjson_path}")
    
    video_data = defaultdict(lambda: {
        "video_name": "",
        "video_url": "",
        "editing_url": "",
        "text_answers": {},
        "has_issues": False
    })
    
    # First load any issues
    project_name = os.path.basename(ndjson_path).split('_')[0]
    issues_file = os.path.join(issues_dir, f"{project_name}_issues.json")
    issues = set()
    
    if os.path.exists(issues_file):
        try:
            with open(issues_file, 'r') as f:
                issues_data = json.load(f)
                for issue in issues_data:
                    if 'dataRow' in issue and 'id' in issue['dataRow']:
                        issues.add(issue['dataRow']['id'])
            logging.info(f"Loaded {len(issues)} issues from {issues_file}")
        except Exception as e:
            logging.error(f"Error loading issues file {issues_file}: {str(e)}")
    
    if not os.path.isfile(ndjson_path):
        logging.error(f"Input file not found: {ndjson_path}")
        return []
        
    records_processed = 0
    records_with_data = 0
    
    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            try:
                record = json.loads(line.strip())
                records_processed += 1
                
                # Extract video info
                video_id = record.get('data_row', {}).get('id', f'unknown_video_{line_number}')
                video_name = record.get('data_row', {}).get('external_id', video_id)
                video_url = record.get('data_row', {}).get('row_data', '')
                
                # Mark if this video has issues
                has_issues = video_id in issues
                if has_issues and not include_issues:
                    continue
                    
                video_entry = video_data[video_id]
                video_entry["video_name"] = video_name
                video_entry["video_url"] = video_url
                video_entry["has_issues"] = has_issues
                
                # Handle projects
                projects = record.get('projects', {})
                if not projects:
                    continue
                    
                for project_id, project_info in projects.items():
                    # Extract workflow details
                    workflow_details = extract_workflow_details(project_info)
                    if workflow_details:
                        # Add video info to workflow details
                        workflow_details.update({
                            'video_name': video_name,
                            'video_url': video_url,
                            'editing_url': f"https://app.labelbox.com/projects/{project_id}/data-rows/{video_id}"
                        })
                        
                        # Update workflow details in video entry
                        if 'workflows' not in video_entry:
                            video_entry['workflows'] = []
                            
                        # Check if we already have a workflow for this project
                        existing_workflow = None
                        for wf in video_entry['workflows']:
                            if wf['project_name'] == workflow_details['project_name']:
                                existing_workflow = wf
                                break
                                
                        if existing_workflow:
                            # Update if new workflow has more recent approval time
                            if (workflow_details['approval_time'] and 
                                (not existing_workflow['approval_time'] or 
                                 workflow_details['approval_time'] > existing_workflow['approval_time'])):
                                video_entry['workflows'].remove(existing_workflow)
                                video_entry['workflows'].append(workflow_details)
                        else:
                            video_entry['workflows'].append(workflow_details)
                            
                        records_with_data += 1
                        
                        # Extract text answers from selected label
                        selected_label_id = project_info.get('project_details', {}).get('selected_label_id')
                        if selected_label_id:
                            labels = project_info.get('labels', [])
                            selected_label = next((label for label in labels if label.get('id') == selected_label_id), None)
                            if selected_label:
                                annotations_dict = {}
                                classifications = selected_label.get('annotations', {}).get('classifications', [])
                                for classification in classifications:
                                    extract_answers(classification, annotations_dict)
                                video_entry["text_answers"].update(annotations_dict)
                                    
            except json.JSONDecodeError as e:
                logging.error(f"Error parsing JSON on line {line_number}: {e}")
                continue
    
    result = list(video_data.values())
    logging.info(f"Finished processing {ndjson_path}:")
    logging.info(f"  - Total records processed: {records_processed}")
    logging.info(f"  - Records with workflow data: {records_with_data}")
    logging.info(f"  - Unique videos extracted: {len(result)}")
    return result

def export_to_sheets(processed_data: List[Dict[str, Any]], config: Dict[str, Any], taxonomy_path: str):
    """Export processed data to Google Sheets based on approvers."""
    try:
        service = get_google_sheets_service()
        
        # Group data by project first
        project_data = defaultdict(list)
        for video in processed_data:
            # Get workflows from the video data
            workflows = video.get('workflows', [])
            for workflow in workflows:
                project_name = workflow.get('project_name', '')
                if project_name:
                    # Create a copy of the video data with this specific workflow
                    video_entry = {
                        'Video Name': str(video['video_name']),
                        'Editing URL': str(workflow['editing_url']),
                        'Approver': str(workflow.get('approver', '')),
                        'Has Issues': 'Yes' if video.get('has_issues', False) else 'No',
                        'Approval Time': convert_iso_to_google_sheets_friendly(
                            workflow.get('approval_time', '')
                        ),
                        'Labelers': ', '.join(workflow.get('labelers', []))
                    }
                    
                    # Add text answers
                    text_answers = video.get('text_answers', {})
                    
                    # Add Has Text Answers column
                    question_mapping = get_text_box_questions_from_taxonomy(taxonomy_path, project_name)
                    has_text = any(question in question_mapping.values() 
                                 for question, answer in text_answers.items() 
                                 if answer)
                    video_entry['Has Text Answers'] = 'Yes' if has_text else 'No'
                    
                    # Add text answers
                    for name, full_question in question_mapping.items():
                        video_entry[full_question] = str(text_answers.get(full_question, ''))
                    
                    project_data[project_name].append(video_entry)
        
        # Convert to DataFrames by project
        project_dfs = {}
        for project_name, videos in project_data.items():
            if videos:
                df = pd.DataFrame(videos)
                # Sort by approval time (most recent first)
                df['_sort_time'] = pd.to_datetime(df['Approval Time'], errors='coerce')
                df = df.sort_values(by='_sort_time', ascending=False, na_position='last')
                df = df.drop(columns=['_sort_time'])
                project_dfs[project_name] = df
        
        # Get sheets configuration
        sheets_config = config.get('google_sheets', {})
        approver_spreadsheets = sheets_config.get('approver_spreadsheets', {})
        default_spreadsheet_id = sheets_config.get('default_spreadsheet_id')
        
        # Update sheets for each approver
        for approver, spreadsheet_id in approver_spreadsheets.items():
            logging.info(f"Processing spreadsheet for approver: {approver}")
            
            # Filter DataFrames for this approver
            approver_dfs = {}
            for project_name, df in project_dfs.items():
                approver_df = df[df['Approver'] == approver]
                if not approver_df.empty:
                    approver_dfs[project_name] = approver_df
            
            # Update each project's sheet
            for project_name, df in approver_dfs.items():
                sheet_name = project_name[:100]  # Sheets names limited to 100 chars
                sheet_name = ''.join(c for c in sheet_name if c.isalnum() or c in ' _-()') # Keep parentheses
                sheet_name = sheet_name.strip()
                
                create_or_update_sheet(service, spreadsheet_id, sheet_name, df)
        
        # Handle videos for approvers not in the mapping
        if default_spreadsheet_id:
            default_dfs = {}
            for project_name, df in project_dfs.items():
                default_df = df[~df['Approver'].isin(approver_spreadsheets.keys())]
                if not default_df.empty:
                    default_dfs[project_name] = default_df
            
            # Update default spreadsheet
            if default_dfs:
                logging.info("Processing videos for approvers not in mapping")
                for project_name, df in default_dfs.items():
                    sheet_name = project_name[:100]
                    sheet_name = ''.join(c for c in sheet_name if c.isalnum() or c in ' _-()') # Keep parentheses
                    sheet_name = sheet_name.strip()
                    
                    create_or_update_sheet(service, default_spreadsheet_id, sheet_name, df)
        
    except Exception as e:
        logging.error(f'Error exporting to Google Sheets: {str(e)}')
        raise

def main():
    """Main function to export Labelbox data and update Google Sheets."""
    try:
        # Set up logging
        setup_logging()
        logging.info("Starting export process...")
        
        # Load configuration
        config = load_config('configs/labelbox_export.yaml')
        logging.info("Loaded configuration")
        
        # Get export configuration
        sheets_config = config.get('google_sheets', {})
        export_dir = sheets_config.get('perform_export')
        logging.info(f"Using export directory: {export_dir}")
        
        if not export_dir:
            # Only export from Labelbox if perform_export is null
            client = Client(api_key=config['api_key'])
            for project_id in config['project_ids']:
                try:
                    export_project_data(client, project_id, config['output_dir'], config)
                except Exception as e:
                    logging.error(f"Error exporting project {project_id}: {str(e)}")
                    continue
            export_dir = config['output_dir']
        
        if not os.path.exists(export_dir):
            raise FileNotFoundError(f"Export directory not found: {export_dir}")
            
        include_issues = sheets_config.get('include_issues', True)
        logging.info(f"Include issues: {include_issues}")
        
        # Process NDJSON files
        all_processed_data = []
        ndjson_dir = os.path.join(export_dir, 'ndjson')
        issues_dir = os.path.join(export_dir, 'issues_ndjson')
        
        if not os.path.exists(ndjson_dir):
            raise FileNotFoundError(f"NDJSON directory not found: {ndjson_dir}")
        
        ndjson_files = [f for f in os.listdir(ndjson_dir) if f.endswith('.ndjson')]
        logging.info(f"Found {len(ndjson_files)} NDJSON files to process")
        
        for ndjson_file in ndjson_files:
            ndjson_path = os.path.join(ndjson_dir, ndjson_file)
            processed_data = process_ndjson_export(
                ndjson_path, 
                issues_dir, 
                'taxonomy/taxonomy.json',
                include_issues=include_issues
            )
            all_processed_data.extend(processed_data)
            logging.info(f"Added {len(processed_data)} videos from {ndjson_file}")
        
        logging.info(f"Total videos processed: {len(all_processed_data)}")
        
        # Export directly to Google Sheets
        if all_processed_data:
            export_to_sheets(all_processed_data, config, 'taxonomy/taxonomy.json')
            logging.info(f"Successfully processed and exported {len(all_processed_data)} videos to Google Sheets")
        else:
            logging.warning("No data to export")
        
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main() 