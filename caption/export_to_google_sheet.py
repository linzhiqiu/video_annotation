#!/usr/bin/env python3
"""
Google Sheets Export System for Video Caption Annotation Statistics

This script exports comprehensive statistics for video caption annotation and review work
to Google Sheets, creating a master tracking sheet with links to individual user 
performance sheets.

Bug fixes included:
- Fixed hyperlinks to show as smart chips with actual sheet URLs
- Corrected timestamp logic to properly separate annotation vs review timestamps  
- Fixed per-task statistics calculation to properly aggregate across all videos/tasks
- Fixed master sheet formatting and column widths
- Added Video Count column to master sheet
- Fixed permission management with proper Google Drive API calls
- Fixed include_payment parameter issue in _update_data_with_preservation
"""

import os
import json
import gspread
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from caption.core.data_manager import DataManager
from caption.core.auth import load_annotators_from_files, APPROVED_REVIEWERS
from caption.config import get_config


class GoogleSheetExporter:
    """Export caption statistics to Google Sheets with comprehensive tracking"""
    
    # OAuth 2.0 scopes required for Google Sheets and Drive access
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # List of emails that should have edit access to all sheets
    EDITOR_EMAILS = [
        'zhiqiulin98@gmail.com',
        'ttiffanyyllingg@gmail.com', 
        'isaacli@andrew.cmu.edu',
        'huangyuhan1130@gmail.com',
        'edzee1701@gmail.com'
    ]
    
    def __init__(self, credentials_file: str, folder_path: str, root_path: str):
        """Initialize the Google Sheets exporter"""
        self.data_manager = DataManager(folder_path, root_path)
        self._setup_google_auth(credentials_file)
        
        # Load annotators and get task names
        self.annotators = load_annotators_from_files()
        self.approved_reviewers = APPROVED_REVIEWERS
        
        # Configuration mapping for short names with emojis
        self.config_names_to_short_names = {
            "Subject Description Caption": "🧍‍♂️Subject",
            "Scene Composition and Dynamics Caption": "🏞️Scene", 
            "Subject Motion and Dynamics Caption": "🏃‍♂️Motion",
            "Spatial Framing and Dynamics Caption": "🗺️Spatial",
            "Camera Framing and Dynamics Caption": "📷Camera",
            "Color Composition and Dynamics Caption (Raw)": "🎨Color",
            "Lighting Setup and Dynamics Caption (Raw)": "💡Lighting",
            "Lighting Effects and Dynamics Caption (Raw)": "🌟Effects",
        }
        
        # Track any failures during export
        self.export_failures = []
    
    def _setup_google_auth(self, credentials_file: str):
        """Setup Google authentication using OAuth 2.0"""
        creds = None
        token_file = 'caption/token_export.json'
        old_token_file = 'caption/token.json'  # Check for old token file
        
        # Check if old token file exists and move/delete it
        if os.path.exists(old_token_file):
            try:
                old_creds = Credentials.from_authorized_user_file(old_token_file, self.SCOPES)
                if not old_creds.has_scopes(self.SCOPES):
                    print(f"🔄 Found old token file with insufficient scopes: {old_token_file}")
                    print("   Moving to backup and will create new token with full permissions...")
                    os.rename(old_token_file, f"{old_token_file}.backup")
                else:
                    print(f"✅ Using existing token with correct scopes: {old_token_file}")
                    # Copy to our export token file
                    import shutil
                    shutil.copy2(old_token_file, token_file)
                    creds = old_creds
            except Exception as e:
                print(f"🔄 Invalid old token file, backing up: {e}")
                os.rename(old_token_file, f"{old_token_file}.backup")
        
        # Load existing export token if available and not already loaded
        if os.path.exists(token_file) and creds is None:
            try:
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
                if not creds.has_scopes(self.SCOPES):
                    print("🔄 Export token has insufficient scopes, deleting...")
                    os.remove(token_file)
                    creds = None
            except:
                print("🔄 Invalid export token file, deleting...")
                os.remove(token_file)
                creds = None
        
        # If there are no (valid) credentials available, get authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"❌ Failed to refresh credentials: {e}")
                    print("🔄 Will require re-authorization...")
                    creds = None
            
            if not creds:
                # Manual OAuth flow for environments without browser
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES, redirect_uri='http://localhost:8080')
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print('='*60)
                print('GOOGLE SHEETS AUTHORIZATION REQUIRED')
                print('='*60)
                print('Required permissions:')
                print('  ✅ Google Sheets: Read, write, and manage spreadsheets')
                print('  ✅ Google Drive: Create and manage files')
                print('='*60)
                print('🔍 The script needs Drive permissions to create individual user sheets.')
                print('   Your existing token only has Sheets permissions.')
                print('='*60)
                print('1. Go to this URL in your browser:')
                print(auth_url)
                print('\n2. Click "Advanced" -> "Go to [App Name] (unsafe)"')
                print('3. Authorize the application')
                print('4. ⚠️  IMPORTANT: Grant BOTH Sheets AND Drive permissions')
                print('5. The browser will show "This site can\'t be reached" - this is expected!')
                print('6. Copy the authorization code from the failed URL')
                print('\n   Example URL: http://localhost:8080/?code=AUTHORIZATION_CODE&scope=...')
                print('   Copy only the part after "code=" and before "&"')
                print('='*60)
                
                auth_code = input('\nEnter the authorization code: ').strip()
                if not auth_code:
                    raise Exception('No authorization code provided')
                
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
                print(f"✅ New credentials with full permissions saved to {token_file}")
        
        # Verify we have the correct scopes
        if not creds.has_scopes(self.SCOPES):
            available_scopes = getattr(creds, 'scopes', ['unknown'])
            print(f"❌ Authentication missing required scopes!")
            print(f"   Required: {self.SCOPES}")
            print(f"   Available: {available_scopes}")
            raise Exception(f"Authentication missing required scopes: {self.SCOPES}")
        
        # Authorize gspread client
        self.client = gspread.authorize(creds)
        
        # Create Google Drive service for permission management
        self.drive_service = build('drive', 'v3', credentials=creds)
        
        print("✅ Google Sheets client authorized with full permissions (Sheets + Drive)")
    
    # def _api_call_with_retry(self, func, *args, max_retries=5, **kwargs):
    #     """Execute API call with rate limiting and retry logic"""
    #     operation_name = kwargs.pop('operation_name', func.__name__)
        
    #     for attempt in range(max_retries):
    #         try:
    #             # Add delay between API calls to avoid rate limits
    #             if attempt > 0:
    #                 # For rate limits, use much longer delays
    #                 delay = min(2 ** attempt * 5, 60)  # Start at 10s, max 60s
    #                 print(f"      ⏳ Waiting {delay}s before retry {attempt + 1}/{max_retries} for {operation_name}...")
    #                 time.sleep(delay)
    #             else:
    #                 # Add small delay between all API calls to prevent rate limits
    #                 time.sleep(1.5)
                
    #             result = func(*args, **kwargs)
    #             if attempt > 0:
    #                 print(f"      ✅ {operation_name} succeeded after {attempt + 1} attempts")
    #             return result
                
    #         except Exception as e:
    #             error_str = str(e).lower()
    #             if 'quota' in error_str or 'rate' in error_str or 'limit' in error_str or '429' in error_str:
    #                 if attempt == max_retries - 1:
    #                     failure_msg = f"RATE LIMIT FAILURE: {operation_name} - Data may not be synced!"
    #                     print(f"      ❌ {failure_msg}")
    #                     self.export_failures.append(failure_msg)
    #                     raise Exception(f"Rate limit failure for {operation_name} after {max_retries} attempts")
    #                 print(f"      ⚠️  Rate limit detected in {operation_name}: {e}")
    #                 continue
    #             else:
    #                 # Not a rate limit error, re-raise immediately
    #                 failure_msg = f"UNEXPECTED ERROR: {operation_name} - {str(e)}"
    #                 print(f"      ❌ {failure_msg}")
    #                 self.export_failures.append(failure_msg)
    #                 raise
        
    #     raise Exception(f"{operation_name} failed after {max_retries} attempts")
    def _api_call_with_retry(self, func, *args, max_retries=5, **kwargs):
        """Execute API call with rate limiting and retry logic"""
        operation_name = kwargs.pop('operation_name', func.__name__)
        
        for attempt in range(max_retries):
            try:
                # Add delay between API calls to avoid rate limits
                if attempt > 0:
                    # For rate limits, use much longer delays: 5, 10, 20, 40, 80 seconds
                    delay = min(5 * (2 ** attempt), 80)
                    print(f"      ⏳ Waiting {delay}s before retry {attempt + 1}/{max_retries} for {operation_name}...")
                    time.sleep(delay)
                else:
                    # Add small delay between all API calls to prevent rate limits
                    time.sleep(1.5)
                
                result = func(*args, **kwargs)
                if attempt > 0:
                    print(f"      ✅ {operation_name} succeeded after {attempt + 1} attempts")
                return result
                
            except Exception as e:
                error_str = str(e).lower()
                if 'quota' in error_str or 'rate' in error_str or 'limit' in error_str or '429' in error_str:
                    if attempt == max_retries - 1:
                        failure_msg = f"RATE LIMIT FAILURE: {operation_name} - Data may not be synced!"
                        print(f"      ❌ {failure_msg}")
                        self.export_failures.append(failure_msg)
                        raise Exception(f"Rate limit failure for {operation_name} after {max_retries} attempts")
                    print(f"      ⚠️  Rate limit detected in {operation_name}: {e}")
                    continue
                else:
                    # Not a rate limit error, re-raise immediately
                    failure_msg = f"UNEXPECTED ERROR: {operation_name} - {str(e)}"
                    print(f"      ❌ {failure_msg}")
                    self.export_failures.append(failure_msg)
                    raise
        
        raise Exception(f"{operation_name} failed after {max_retries} attempts")
    
    # def _manage_sheet_permissions(self, sheet_id: str, sheet_name: str):
    #     """Manage permissions for a sheet - give edit access to approved emails, commenter to others"""
    #     print(f"      🔐 Managing permissions for {sheet_name}...")
        
    #     try:
    #         # Get current permissions - FIXED: Use lambda to properly execute the API call
    #         current_permissions = self._api_call_with_retry(
    #             lambda: self.drive_service.permissions().list(fileId=sheet_id).execute(),
    #             operation_name=f"listing permissions for {sheet_name}"
    #         )
            
    #         # Track emails that currently have access
    #         current_editors = set()
    #         current_commenters = set()
    #         permissions_to_update = []
    #         permissions_to_delete = []
            
    #         # Analyze current permissions
    #         for permission in current_permissions.get('permissions', []):
    #             email = permission.get('emailAddress')
    #             role = permission.get('role')
    #             perm_id = permission.get('id')
    #             perm_type = permission.get('type')
                
    #             # Skip owner permissions and non-user permissions
    #             if role == 'owner' or perm_type != 'user' or not email:
    #                 continue
                
    #             if email in self.EDITOR_EMAILS:
    #                 if role != 'writer':
    #                     # Should be editor but isn't - update
    #                     permissions_to_update.append((perm_id, 'writer', email))
    #                 current_editors.add(email)
    #             else:
    #                 if role == 'writer':
    #                     # Should be commenter but is editor - update  
    #                     permissions_to_update.append((perm_id, 'commenter', email))
    #                 current_commenters.add(email)
            
    #         # Add missing editor permissions
    #         for email in self.EDITOR_EMAILS:
    #             if email not in current_editors and email not in current_commenters:
    #                 # Add new editor permission - FIXED: Use lambda to properly execute the API call
    #                 try:
    #                     self._api_call_with_retry(
    #                         lambda: self.drive_service.permissions().create(
    #                             fileId=sheet_id,
    #                             body={
    #                                 'type': 'user',
    #                                 'role': 'writer', 
    #                                 'emailAddress': email
    #                             }
    #                         ).execute(),
    #                         operation_name=f"adding editor permission for {email}"
    #                     )
    #                     print(f"        ✅ Added editor access for {email}")
    #                 except Exception as e:
    #                     print(f"        ⚠️  Could not add editor access for {email}: {e}")
            
    #         # Update existing permissions - FIXED: Use lambda to properly execute the API call
    #         for perm_id, new_role, email in permissions_to_update:
    #             try:
    #                 self._api_call_with_retry(
    #                     lambda: self.drive_service.permissions().update(
    #                         fileId=sheet_id,
    #                         permissionId=perm_id,
    #                         body={'role': new_role}
    #                     ).execute(),
    #                     operation_name=f"updating permission for {email} to {new_role}"
    #                 )
    #                 action = "editor" if new_role == 'writer' else "commenter"
    #                 print(f"        ✅ Updated {email} to {action} access")
    #             except Exception as e:
    #                 print(f"        ⚠️  Could not update permission for {email}: {e}")
            
    #         print(f"      ✅ Permissions managed for {sheet_name}")
            
    #     except Exception as e:
    #         print(f"      ⚠️  Could not manage permissions for {sheet_name}: {e}")
    
    def _manage_sheet_permissions(self, sheet_id: str, sheet_name: str):
        """Manage permissions for a sheet - give edit access to approved emails, commenter to others"""
        print(f"      🔐 Managing permissions for {sheet_name}...")
        
        try:
            # Get current permissions with email addresses - FIXED: Request email field explicitly
            current_permissions = self._api_call_with_retry(
                lambda: self.drive_service.permissions().list(
                    fileId=sheet_id,
                    fields="permissions(id,role,type,emailAddress,displayName)"
                ).execute(),
                operation_name=f"listing permissions for {sheet_name}"
            )
            
            # Track emails that currently have access
            current_editors = set()
            current_commenters = set()
            permissions_to_update = []
            permissions_to_delete = []
            
            # DEBUG: Print current permissions for troubleshooting
            print(f"      🔍 Found {len(current_permissions.get('permissions', []))} existing permissions")
            
            # Analyze current permissions
            for i, permission in enumerate(current_permissions.get('permissions', []), 1):
                email = permission.get('emailAddress')
                role = permission.get('role')
                perm_id = permission.get('id')
                perm_type = permission.get('type')
                display_name = permission.get('displayName')
                
                # If email is None, try to get it using individual permission lookup
                if not email and perm_type == 'user' and perm_id:
                    try:
                        detailed_permission = self._api_call_with_retry(
                            lambda pid=perm_id: self.drive_service.permissions().get(
                                fileId=sheet_id,
                                permissionId=pid,
                                fields="emailAddress,displayName,role,type"
                            ).execute(),
                            operation_name=f"getting detailed permission for {perm_id}"
                        )
                        email = detailed_permission.get('emailAddress')
                        if email:
                            print(f"         {i}. 🔍 Found email via lookup: {email}")
                    except Exception as e:
                        print(f"         {i}. ⚠️  Could not get email for permission {perm_id}: {e}")
                
                # DEBUG: Print ALL permission details to understand the structure
                print(f"         {i}. Type: {perm_type}, Role: {role}, Email: {email}, Display: {display_name}, ID: {perm_id}")
                
                # Skip non-user permissions or permissions without email
                if perm_type != 'user' or not email:
                    print(f"            ⏭️  Skipping (not_user={perm_type!='user'}, no_email={not email})")
                    continue

                if email in self.EDITOR_EMAILS:
                    if role == 'owner':
                        # Owner has higher permissions than writer - no need to change
                        print(f"            👑 {email} is owner (has full access, no change needed)")
                        current_editors.add(email)  # Count as having appropriate access
                    elif role != 'writer':
                        # Should be editor but isn't - update
                        permissions_to_update.append((perm_id, 'writer', email))
                        print(f"            📝 Will update {email} from {role} to writer")
                    else:
                        print(f"            ✅ {email} already has correct writer access")
                    current_editors.add(email)
                else:
                    if role == 'owner':
                        # Someone else is owner - that's fine, don't change
                        print(f"            👑 {email} is owner (external user)")
                    elif role == 'writer':
                        # Should be commenter but is editor - update  
                        permissions_to_update.append((perm_id, 'commenter', email))
                        print(f"            📝 Will update {email} from writer to commenter")
                    else:
                        print(f"            ℹ️  {email} has {role} access (will remain unchanged)")
                    current_commenters.add(email)
            
            print(f"      📊 Current status: {len(current_editors)} editors, {len(current_commenters)} others")
            print(f"         Editors found: {sorted(current_editors)}")
            print(f"         Target editors: {sorted(self.EDITOR_EMAILS)}")
            
            # Count existing writer permissions (even if we don't have emails)
            existing_writers = sum(1 for p in current_permissions.get('permissions', []) 
                                if p.get('role') == 'writer' and p.get('type') == 'user')
            target_writers = len(self.EDITOR_EMAILS)
            
            print(f"         📈 Writer permissions: {existing_writers} existing, {target_writers} target")
            
            # If we have the expected number of writers and found some emails matching, 
            # we might already be set up correctly
            if existing_writers >= target_writers and len(current_editors) > 0:
                print(f"         💡 Detected likely correct setup ({existing_writers} writers, {len(current_editors)} identified)")
            
            # Add missing editor permissions - ONLY if they don't already exist
            emails_to_add = []
            for email in self.EDITOR_EMAILS:
                if email not in current_editors and email not in current_commenters:
                    # Extra check: if we have enough writers already, be more cautious
                    if existing_writers >= target_writers:
                        print(f"         🤔 {email} not identified, but {existing_writers} writers exist (may already have access)")
                        # Still add to list but with a note
                        emails_to_add.append(email)
                    else:
                        emails_to_add.append(email)
                        print(f"         ➕ Will add writer access for {email}")
                elif email in current_editors:
                    print(f"         ⏭️  Skipping {email} - already has writer access")
                else:
                    print(f"         ⏭️  {email} has some other access level")
            
            # Actually add new permissions (with better error handling)
            successful_adds = 0
            skipped_existing = 0
            
            for email in emails_to_add:
                try:
                    self._api_call_with_retry(
                        lambda e=email: self.drive_service.permissions().create(
                            fileId=sheet_id,
                            body={
                                'type': 'user',
                                'role': 'writer', 
                                'emailAddress': e,
                            }
                        ).execute(),
                        operation_name=f"adding editor permission for {email}"
                    )
                    print(f"        ✅ Added editor access for {email}")
                    successful_adds += 1
                except Exception as e:
                    error_msg = str(e).lower()
                    # Check if error is because permission already exists
                    if any(phrase in error_msg for phrase in [
                        'already exists', 'duplicate', 'already has access', 
                        'already a collaborator', 'permission already granted',
                        'user already has access'
                    ]):
                        print(f"        ⏭️  {email} already has access (confirmed by API)")
                        skipped_existing += 1
                    else:
                        print(f"        ⚠️  Could not add editor access for {email}: {e}")
            
            # Summary of permission changes
            if successful_adds == 0 and skipped_existing > 0:
                print(f"      ✅ All {skipped_existing} target users already have access to {sheet_name}")
            elif successful_adds > 0:
                print(f"      ✅ Added {successful_adds} new permissions for {sheet_name}")
            else:
                print(f"      ✅ No permission changes needed for {sheet_name}")
            
            # Update existing permissions - FIXED: Use lambda to properly execute the API call
            for perm_id, new_role, email in permissions_to_update:
                try:
                    self._api_call_with_retry(
                        lambda pid=perm_id, role=new_role: self.drive_service.permissions().update(
                            fileId=sheet_id,
                            permissionId=pid,
                            body={'role': role}
                        ).execute(),
                        operation_name=f"updating permission for {email} to {new_role}"
                    )
                    action = "editor" if new_role == 'writer' else "commenter"
                    print(f"        ✅ Updated {email} to {action} access")
                except Exception as e:
                    print(f"        ⚠️  Could not update permission for {email}: {e}")
            
            # Summary
            total_changes = successful_adds + len(permissions_to_update)
            if total_changes == 0 and skipped_existing > 0:
                print(f"      ✅ All permissions already correct for {sheet_name} (no changes needed)")
            elif total_changes == 0:
                print(f"      ✅ All permissions already correct for {sheet_name}")
            else:
                print(f"      ✅ Updated {total_changes} permissions for {sheet_name}")
            
        except Exception as e:
            print(f"      ⚠️  Could not manage permissions for {sheet_name}: {e}")
    
    def export_all_sheets(self, configs_file: str, video_urls_files: List[str], 
                         output_dir: str, master_sheet_id: str, skip_individual: bool = False, 
                         resume_from: str = None, sheet_prefix: str = "Caption"):
        """
        Export all data to Google Sheets
        
        Args:
            configs_file: Path to configs file
            video_urls_files: List of video URL files
            output_dir: Output directory for caption data
            master_sheet_id: Google Sheet ID for the master sheet
            skip_individual: If True, only export master sheet
            resume_from: Resume from specific user (format: 'User Name Role')
            sheet_prefix: Prefix for all individual sheet names (default: 'Caption')
        """
        # Load configs to get task names
        configs = self.data_manager.load_config(configs_file)
        configs = [self.data_manager.load_config(config) for config in configs]
        task_names = [config["name"] for config in configs]
        
        # Collect all video URLs
        all_video_urls = []
        video_file_mapping = {}  # video_url -> video_file
        for video_file in video_urls_files:
            try:
                video_urls = self.data_manager.load_json(video_file)
                all_video_urls.extend(video_urls)
                for url in video_urls:
                    video_file_mapping[url] = os.path.basename(video_file)
            except FileNotFoundError:
                print(f"Warning: Video URLs file not found: {video_file}")
                continue
        
        # Calculate statistics for all users
        annotator_stats, reviewer_stats = self._calculate_all_user_stats(
            configs, all_video_urls, video_file_mapping, output_dir
        )
        
        # Export master sheet
        print("="*60)
        print("STARTING GOOGLE SHEETS EXPORT")
        print("="*60)
        self._export_master_sheet(master_sheet_id, annotator_stats, reviewer_stats, task_names)
        
        # Manage master sheet permissions
        print("Managing master sheet permissions...")
        self._manage_sheet_permissions(master_sheet_id, "Master Sheet")
        
        if skip_individual:
            print("\n✅ Master sheet export completed (individual sheets skipped)")
            return
        
        # Export individual user sheets with progress tracking and rate limiting
        total_users = sum(1 for stats in annotator_stats.values() if self._has_activity(stats)) + \
                    sum(1 for stats in reviewer_stats.values() if self._has_activity(stats))

        current_user = 0
        print(f"\nExporting individual user sheets ({total_users} total)...")
        print("⚠️  Note: Processing slowly to avoid Google Sheets rate limits...")

        # Store sheet IDs for hyperlinks
        user_sheet_ids = {}

        # Determine where to start based on resume_from parameter
        skip_until_found = resume_from is not None

        for user_name, stats in annotator_stats.items():
            if self._has_activity(stats):
                current_user += 1
                sheet_key = f"{sheet_prefix}-{user_name} Annotator"  # Add prefix to key
                
                # Skip users until we reach the resume point
                if skip_until_found:
                    if sheet_key == resume_from:
                        skip_until_found = False
                        print(f"🔄 Resuming from: {sheet_key}")
                    else:
                        print(f"⏭️  Skipping {sheet_key} (resuming from {resume_from})")
                        continue
                
                print(f"\n[{current_user}/{total_users}] Processing {user_name} Annotator...")
                
                # Add delay between users to prevent rate limits
                if current_user > 1:
                    print("    ⏳ Pausing 3 seconds between users to respect rate limits...")
                    time.sleep(3)
                
                try:
                    sheet_id = self._export_user_sheet(user_name, "Annotator", stats, task_names, master_sheet_id, sheet_prefix)
                    user_sheet_ids[sheet_key] = sheet_id
                    
                    # Manage permissions for this sheet
                    self._manage_sheet_permissions(sheet_id, f"{sheet_prefix}-{user_name} Annotator")
                    
                    print(f"    ✅ Successfully exported {sheet_prefix}-{user_name} Annotator")
                except Exception as e:
                    print(f"    ❌ Failed to export {sheet_prefix}-{user_name} Annotator: {e}")
                    self.export_failures.append(f"Failed to export {sheet_prefix}-{user_name} Annotator: {str(e)}")
                
        for user_name, stats in reviewer_stats.items():
            if self._has_activity(stats):
                current_user += 1
                sheet_key = f"{sheet_prefix}-{user_name} Reviewer"  # Add prefix to key
                
                # Skip users until we reach the resume point
                if skip_until_found:
                    if sheet_key == resume_from:
                        skip_until_found = False
                        print(f"🔄 Resuming from: {sheet_key}")
                    else:
                        print(f"⏭️  Skipping {sheet_key} (resuming from {resume_from})")
                        continue
                
                print(f"\n[{current_user}/{total_users}] Processing {user_name} Reviewer...")
                
                # Add delay between users to prevent rate limits
                print("    ⏳ Pausing 3 seconds between users to respect rate limits...")
                time.sleep(3)
                
                try:
                    sheet_id = self._export_user_sheet(user_name, "Reviewer", stats, task_names, master_sheet_id, sheet_prefix)
                    user_sheet_ids[sheet_key] = sheet_id
                    
                    # Manage permissions for this sheet
                    self._manage_sheet_permissions(sheet_id, f"{sheet_prefix}-{user_name} Reviewer")
                    
                    print(f"    ✅ Successfully exported {sheet_prefix}-{user_name} Reviewer")
                except Exception as e:
                    print(f"    ❌ Failed to export {sheet_prefix}-{user_name} Reviewer: {e}")
                    self.export_failures.append(f"Failed to export {sheet_prefix}-{user_name} Reviewer: {str(e)}")      

        # Update master sheet with correct hyperlinks
        if user_sheet_ids:
            print(f"\n⏳ Pausing 5 seconds before updating master sheet links...")
            time.sleep(5)
            print("Updating master sheet hyperlinks...")
            try:
                self._update_master_sheet_links(master_sheet_id, annotator_stats, reviewer_stats, user_sheet_ids, sheet_prefix)
            except Exception as e:
                print(f"❌ Failed to update master sheet links: {e}")
                self.export_failures.append(f"Failed to update master sheet links: {str(e)}")
        
        print("="*60)
        if self.export_failures:
            print("EXPORT COMPLETED WITH SOME FAILURES!")
            print("="*60)
            print("❌ The following operations failed:")
            for failure in self.export_failures:
                print(f"   - {failure}")
            print(f"\n⚠️  Some data may not be synced. Consider running the script again.")
            print(f"📊 Master Sheet: https://docs.google.com/spreadsheets/d/{master_sheet_id}/edit")
            print("\n💡 If you hit rate limits, you can:")
            print("   1. Wait 1 hour and run again (Google resets quotas hourly)")
            print("   2. Resume from where it failed with: --resume-from 'User Name Role'")
            print("   3. Just update master sheet with: --skip-individual")
            print("="*60)
        else:
            print("EXPORT COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"📊 Master Sheet: https://docs.google.com/spreadsheets/d/{master_sheet_id}/edit")
            print(f"   - View all annotator and reviewer statistics")
            print(f"   - Links to individual user sheets")
            print("="*60)
    
    def _has_activity(self, stats: Dict) -> bool:
        """Check if user has any activity"""
        return (stats['total_across_tasks'].get('completed', 0) > 0 or 
                stats['total_across_tasks'].get('reviewed', 0) > 0)
    
    def _calculate_all_user_stats(self, configs: List[Dict], all_video_urls: List[str], 
                                 video_file_mapping: Dict[str, str], output_dir: str) -> Tuple[Dict, Dict]:
        """Calculate statistics for all annotators and reviewers"""
        annotator_stats = {}
        reviewer_stats = {}
        
        # Initialize stats for all known users
        for user_name in self.annotators.keys():
            annotator_stats[user_name] = {
                'email': self.annotators[user_name].get('email', ''),
                'total_across_tasks': {'completed': 0, 'reviewed': 0, 'rejected': 0},
                'per_task': {},
                'per_video_file': {},
                'last_annotation_timestamp': None,
                'last_review_timestamp': None
            }
        
        for user_name in self.approved_reviewers:
            reviewer_stats[user_name] = {
                'email': self.annotators.get(user_name, {}).get('email', ''),
                'total_across_tasks': {'reviewed': 0},
                'per_task': {},
                'per_video_file': {},
                'last_annotation_timestamp': None,
                'last_review_timestamp': None
            }
        
        # Initialize per-task stats
        for config in configs:
            task_name = config["name"]
            for user_name in annotator_stats:
                annotator_stats[user_name]['per_task'][task_name] = {
                    'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': 0
                }
            for user_name in reviewer_stats:
                reviewer_stats[user_name]['per_task'][task_name] = {
                    'reviewed': 0, 'total': 0
                }
        
        # Group videos by file for calculations
        videos_by_file = {}
        for video_url in all_video_urls:
            video_file = video_file_mapping.get(video_url, 'Unknown')
            if video_file not in videos_by_file:
                videos_by_file[video_file] = []
            videos_by_file[video_file].append(video_url)
        
        # Calculate stats for each video file
        for video_file, video_urls in videos_by_file.items():
            file_stats = self._calculate_file_stats(video_urls, configs, output_dir)
            
            # Update user stats  
            for user_name in annotator_stats:
                if video_file not in annotator_stats[user_name]['per_video_file']:
                    annotator_stats[user_name]['per_video_file'][video_file] = {
                        'total_possible': len(video_urls) * len(configs),
                        'completed_all_users': 0,
                        'completed_current_user': 0,
                        'reviewed_all_users': 0,
                        'reviewed_current_user_work': 0,
                        'last_annotation_timestamp': None,
                        'last_review_timestamp': None
                    }
                
                user_file_stats = annotator_stats[user_name]['per_video_file'][video_file]
                user_file_stats.update(file_stats['annotators'].get(user_name, {
                    'completed_all_users': file_stats['global']['completed_all_users'],
                    'completed_current_user': 0,
                    'reviewed_all_users': file_stats['global']['reviewed_all_users'],
                    'reviewed_current_user_work': 0,
                    'last_annotation_timestamp': None,
                    'last_review_timestamp': None,
                    'per_task_stats': {}  # Add per-task stats for this video file
                }))
                
                # Count unique videos for this user (if they completed any task in this video file)
                # if user_file_stats['completed_current_user'] > 0:
                #     annotator_stats[user_name]['video_count'] += 1
                
                # Add per-task stats for this video file
                user_file_stats['per_task_stats'] = file_stats['per_task_annotators'].get(user_name, {})
                
                # Ensure all tasks are initialized with zero values if user didn't work on them
                for config in configs:
                    task_name = config["name"]
                    if task_name not in user_file_stats['per_task_stats']:
                        user_file_stats['per_task_stats'][task_name] = {
                            'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': len(video_urls)
                        }
                
                # Update global user stats
                annotator_stats[user_name]['total_across_tasks']['completed'] += user_file_stats['completed_current_user']
                annotator_stats[user_name]['total_across_tasks']['reviewed'] += user_file_stats['reviewed_current_user_work']
                
                # Update per-task stats for annotators
                for config in configs:
                    task_name = config["name"]
                    task_stats = file_stats['per_task_annotators'].get(user_name, {}).get(task_name, {
                        'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': len(video_urls)
                    })
                    
                    annotator_stats[user_name]['per_task'][task_name]['completed'] += task_stats['completed']
                    annotator_stats[user_name]['per_task'][task_name]['reviewed'] += task_stats['reviewed']
                    annotator_stats[user_name]['per_task'][task_name]['rejected'] += task_stats['rejected']
                    annotator_stats[user_name]['per_task'][task_name]['total'] += task_stats['total']
                
                # Update timestamps - only annotation timestamps for annotators
                if user_file_stats['last_annotation_timestamp']:
                    current_ts = annotator_stats[user_name]['last_annotation_timestamp']
                    if not current_ts or user_file_stats['last_annotation_timestamp'] > current_ts:
                        annotator_stats[user_name]['last_annotation_timestamp'] = user_file_stats['last_annotation_timestamp']
            
            # Update reviewer stats
            for user_name in reviewer_stats:
                if video_file not in reviewer_stats[user_name]['per_video_file']:
                    reviewer_stats[user_name]['per_video_file'][video_file] = {
                        'total_possible': len(video_urls) * len(configs),
                        'completed_all_users': 0,
                        'reviewed_all_users': 0,
                        'reviewed_by_current_user': 0,
                        'last_review_timestamp': None
                    }
                
                user_file_stats = reviewer_stats[user_name]['per_video_file'][video_file]
                user_file_stats.update(file_stats['reviewers'].get(user_name, {
                    'completed_all_users': file_stats['global']['completed_all_users'],
                    'reviewed_all_users': file_stats['global']['reviewed_all_users'],
                    'reviewed_by_current_user': 0,
                    'last_review_timestamp': None,
                    'per_task_stats': {}  # Add per-task stats for this video file
                }))
                
                # Count unique videos for this user (if they reviewed any task in this video file)
                # if user_file_stats['reviewed_by_current_user'] > 0:
                #     reviewer_stats[user_name]['video_count'] += 1
                
                # Add per-task stats for this video file
                user_file_stats['per_task_stats'] = file_stats['per_task_reviewers'].get(user_name, {})
                
                # Ensure all tasks are initialized with zero values if user didn't work on them
                for config in configs:
                    task_name = config["name"]
                    if task_name not in user_file_stats['per_task_stats']:
                        user_file_stats['per_task_stats'][task_name] = {
                            'reviewed': 0, 'total': len(video_urls)
                        }
                
                # Update global user stats
                reviewer_stats[user_name]['total_across_tasks']['reviewed'] += user_file_stats['reviewed_by_current_user']
                
                # Update per-task stats for reviewers
                for config in configs:
                    task_name = config["name"]
                    task_stats = file_stats['per_task_reviewers'].get(user_name, {}).get(task_name, {
                        'reviewed': 0, 'total': len(video_urls)
                    })
                    
                    reviewer_stats[user_name]['per_task'][task_name]['reviewed'] += task_stats['reviewed']
                    reviewer_stats[user_name]['per_task'][task_name]['total'] += task_stats['total']
                
                # Update timestamps - only review timestamps for reviewers
                if user_file_stats['last_review_timestamp']:
                    current_ts = reviewer_stats[user_name]['last_review_timestamp']
                    if not current_ts or user_file_stats['last_review_timestamp'] > current_ts:
                        reviewer_stats[user_name]['last_review_timestamp'] = user_file_stats['last_review_timestamp']
        
        return annotator_stats, reviewer_stats
    
    # def _calculate_file_stats(self, video_urls: List[str], configs: List[Dict], output_dir: str) -> Dict:
    #     """Calculate statistics for a single video file"""
    #     stats = {
    #         'global': {
    #             'completed_all_users': 0,
    #             'reviewed_all_users': 0
    #         },
    #         'annotators': {},
    #         'reviewers': {},
    #         'per_task_annotators': {},  # user -> task -> stats for this video file
    #         'per_task_reviewers': {}    # user -> task -> stats for this video file
    #     }
        
    #     # Initialize per-task stats with correct totals
    #     total_tasks_in_file = len(video_urls) * len(configs)
        
    #     for video_url in video_urls:
    #         video_id = self.data_manager.get_video_id(video_url)
            
    #         for config in configs:
    #             config_output_dir = os.path.join(self.data_manager.folder, output_dir, config["output_name"])
    #             task_name = config["name"]
                
    #             # Get status and users for this video/task
    #             status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
    #                 video_id, config_output_dir
    #             )
                
    #             if status == "not_completed":
    #                 continue
                
    #             # Update global stats
    #             stats['global']['completed_all_users'] += 1
    #             if status in ["approved", "rejected"]:
    #                 stats['global']['reviewed_all_users'] += 1
                
    #             # Determine annotator and reviewer
    #             annotator, reviewer = self.data_manager.get_annotator_and_reviewer(video_id, config_output_dir)
                
    #             # Update annotator stats
    #             if annotator:
    #                 if annotator not in stats['annotators']:
    #                     stats['annotators'][annotator] = {
    #                         'completed_current_user': 0,
    #                         'reviewed_current_user_work': 0,
    #                         'last_annotation_timestamp': None,
    #                         'last_review_timestamp': None
    #                     }
                    
    #                 if annotator not in stats['per_task_annotators']:
    #                     stats['per_task_annotators'][annotator] = {}
    #                 if task_name not in stats['per_task_annotators'][annotator]:
    #                     stats['per_task_annotators'][annotator][task_name] = {
    #                         'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': 0
    #                     }
                    
    #                 stats['annotators'][annotator]['completed_current_user'] += 1
    #                 stats['per_task_annotators'][annotator][task_name]['completed'] += 1
    #                 stats['per_task_annotators'][annotator][task_name]['total'] += 1  # Increment total for each task instance
                    
    #                 # Update annotation timestamp from feedback file
    #                 if current_file and os.path.exists(current_file):
    #                     try:
    #                         with open(current_file, 'r') as f:
    #                             data = json.load(f)
    #                             timestamp = data.get('timestamp')
    #                             if timestamp:
    #                                 current_ts = stats['annotators'][annotator]['last_annotation_timestamp']
    #                                 if not current_ts or timestamp > current_ts:
    #                                     stats['annotators'][annotator]['last_annotation_timestamp'] = timestamp
    #                     except:
    #                         pass
                    
    #                 # Check if this annotation was reviewed
    #                 if status in ["approved", "rejected"]:
    #                     stats['annotators'][annotator]['reviewed_current_user_work'] += 1
    #                     stats['per_task_annotators'][annotator][task_name]['reviewed'] += 1
                        
    #                     if status == "rejected":
    #                         stats['per_task_annotators'][annotator][task_name]['rejected'] += 1
    #             else:
    #                 # Even if no annotator, we need to track that this task exists in the file
    #                 # This ensures totals are correct even for tasks not completed by current user
    #                 pass
                
    #             # Update reviewer stats
    #             if reviewer and status in ["approved", "rejected"]:
    #                 if reviewer not in stats['reviewers']:
    #                     stats['reviewers'][reviewer] = {
    #                         'reviewed_by_current_user': 0,
    #                         'last_review_timestamp': None
    #                     }
                    
    #                 if reviewer not in stats['per_task_reviewers']:
    #                     stats['per_task_reviewers'][reviewer] = {}
    #                 if task_name not in stats['per_task_reviewers'][reviewer]:
    #                     stats['per_task_reviewers'][reviewer][task_name] = {
    #                         'reviewed': 0, 'total': 0
    #                     }
                    
    #                 stats['reviewers'][reviewer]['reviewed_by_current_user'] += 1
    #                 stats['per_task_reviewers'][reviewer][task_name]['reviewed'] += 1
    #                 stats['per_task_reviewers'][reviewer][task_name]['total'] += 1  # Increment total for each review instance
                    
    #                 # Update review timestamp from review file
    #                 review_file = self.data_manager.get_filename(video_id, config_output_dir, 
    #                                                            self.data_manager.REVIEWER_FILE_POSTFIX)
    #                 if os.path.exists(review_file):
    #                     try:
    #                         with open(review_file, 'r') as f:
    #                             data = json.load(f)
    #                             timestamp = data.get('review_timestamp')
    #                             if timestamp:
    #                                 current_ts = stats['reviewers'][reviewer]['last_review_timestamp']
    #                                 if not current_ts or timestamp > current_ts:
    #                                     stats['reviewers'][reviewer]['last_review_timestamp'] = timestamp
    #                     except:
    #                         pass
        
    #     # Set totals for tasks that were not completed by users (to ensure proper ratios)
    #     total_possible_per_task = len(video_urls)
    #     for annotator in stats['per_task_annotators']:
    #         for task_name in [config["name"] for config in configs]:
    #             if task_name not in stats['per_task_annotators'][annotator]:
    #                 stats['per_task_annotators'][annotator][task_name] = {
    #                     'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': total_possible_per_task
    #                 }
    #             else:
    #                 # Make sure total is at least the expected number
    #                 stats['per_task_annotators'][annotator][task_name]['total'] = max(
    #                     stats['per_task_annotators'][annotator][task_name]['total'], 
    #                     total_possible_per_task
    #                 )
        
    #     for reviewer in stats['per_task_reviewers']:
    #         for task_name in [config["name"] for config in configs]:
    #             if task_name not in stats['per_task_reviewers'][reviewer]:
    #                 stats['per_task_reviewers'][reviewer][task_name] = {
    #                     'reviewed': 0, 'total': total_possible_per_task
    #                 }
    #             else:
    #                 # Make sure total is at least the expected number
    #                 stats['per_task_reviewers'][reviewer][task_name]['total'] = max(
    #                     stats['per_task_reviewers'][reviewer][task_name]['total'], 
    #                     total_possible_per_task
    #                 )
        
    #     # Add global stats to each user's stats
    #     for annotator_stats in stats['annotators'].values():
    #         annotator_stats['completed_all_users'] = stats['global']['completed_all_users']
    #         annotator_stats['reviewed_all_users'] = stats['global']['reviewed_all_users']
        
    #     for reviewer_stats in stats['reviewers'].values():
    #         reviewer_stats['completed_all_users'] = stats['global']['completed_all_users']
    #         reviewer_stats['reviewed_all_users'] = stats['global']['reviewed_all_users']
        
    #     return stats
    
    def _calculate_file_stats(self, video_urls: List[str], configs: List[Dict], output_dir: str) -> Dict:
        """Calculate statistics for a single video file"""
        stats = {
            'global': {
                'completed_all_users': 0,
                'reviewed_all_users': 0
            },
            'annotators': {},
            'reviewers': {},
            'per_task_annotators': {},  # user -> task -> stats for this video file
            'per_task_reviewers': {}    # user -> task -> stats for this video file
        }
        
        for video_url in video_urls:
            video_id = self.data_manager.get_video_id(video_url)
            
            for config in configs:
                config_output_dir = os.path.join(self.data_manager.folder, output_dir, config["output_name"])
                task_name = config["name"]
                
                # Get status and users for this video/task - USE THE VERIFIED FUNCTION
                status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                    video_id, config_output_dir
                )
                
                if status == "not_completed":
                    continue
                
                # Count global stats based on verified status
                stats['global']['completed_all_users'] += 1
                if status in ["approved", "rejected"]:
                    stats['global']['reviewed_all_users'] += 1
                
                # Determine annotator and reviewer based on verified status logic
                annotator = None
                reviewer = None
                
                if status == "completed_not_reviewed":
                    # Only current feedback exists - current_user is the annotator
                    annotator = current_user
                    # No reviewer yet
                    
                elif status == "approved":
                    # For approved: current_user is annotator, reviewer is in reviewer file
                    annotator = current_user
                    # Get reviewer from reviewer file
                    reviewer_file = self.data_manager.get_filename(video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
                    if os.path.exists(reviewer_file):
                        try:
                            with open(reviewer_file, 'r') as f:
                                reviewer_data = json.load(f)
                                reviewer = reviewer_data.get("reviewer_name")
                        except:
                            pass
                            
                elif status == "rejected":
                    # For rejected: prev_user is annotator, current_user is reviewer (who fixed it)
                    annotator = prev_user
                    reviewer = current_user
                
                # Update annotator stats
                if annotator:
                    if annotator not in stats['annotators']:
                        stats['annotators'][annotator] = {
                            'completed_current_user': 0,
                            'reviewed_current_user_work': 0,
                            'last_annotation_timestamp': None,
                            'last_review_timestamp': None
                        }
                    
                    if annotator not in stats['per_task_annotators']:
                        stats['per_task_annotators'][annotator] = {}
                    if task_name not in stats['per_task_annotators'][annotator]:
                        stats['per_task_annotators'][annotator][task_name] = {
                            'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': 0
                        }
                    
                    stats['annotators'][annotator]['completed_current_user'] += 1
                    stats['per_task_annotators'][annotator][task_name]['completed'] += 1
                    stats['per_task_annotators'][annotator][task_name]['total'] += 1
                    
                    # Update annotation timestamp from the correct feedback file
                    annotation_file = None
                    if status == "completed_not_reviewed":
                        annotation_file = current_file
                    elif status in ["approved", "rejected"]:
                        # For approved/rejected, annotation is in prev_feedback (if exists) or current_feedback
                        annotation_file = prev_file if prev_file else current_file
                    
                    if annotation_file and os.path.exists(annotation_file):
                        try:
                            with open(annotation_file, 'r') as f:
                                data = json.load(f)
                                timestamp = data.get('timestamp')
                                if timestamp:
                                    current_ts = stats['annotators'][annotator]['last_annotation_timestamp']
                                    if not current_ts or timestamp > current_ts:
                                        stats['annotators'][annotator]['last_annotation_timestamp'] = timestamp
                        except:
                            pass
                    
                    # Check if this annotation was reviewed
                    if status in ["approved", "rejected"]:
                        stats['annotators'][annotator]['reviewed_current_user_work'] += 1
                        stats['per_task_annotators'][annotator][task_name]['reviewed'] += 1
                        
                        if status == "rejected":
                            stats['per_task_annotators'][annotator][task_name]['rejected'] += 1
                
                # Update reviewer stats
                if reviewer:
                    if reviewer not in stats['reviewers']:
                        stats['reviewers'][reviewer] = {
                            'completed_all_users': 0,
                            'reviewed_all_users': 0,
                            'reviewed_by_current_user': 0,
                            'last_review_timestamp': None
                        }
                    
                    if reviewer not in stats['per_task_reviewers']:
                        stats['per_task_reviewers'][reviewer] = {}
                    if task_name not in stats['per_task_reviewers'][reviewer]:
                        stats['per_task_reviewers'][reviewer][task_name] = {
                            'reviewed': 0, 'total': 0
                        }
                    
                    stats['reviewers'][reviewer]['reviewed_by_current_user'] += 1
                    stats['per_task_reviewers'][reviewer][task_name]['reviewed'] += 1
                    stats['per_task_reviewers'][reviewer][task_name]['total'] += 1
                    
                    # Update review timestamp from reviewer file (for both approved and rejected)
                    reviewer_file_path = self.data_manager.get_filename(video_id, config_output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
                    if os.path.exists(reviewer_file_path):
                        try:
                            with open(reviewer_file_path, 'r') as f:
                                data = json.load(f)
                                timestamp = data.get('review_timestamp')
                                if timestamp:
                                    current_ts = stats['reviewers'][reviewer]['last_review_timestamp']
                                    if not current_ts or timestamp > current_ts:
                                        stats['reviewers'][reviewer]['last_review_timestamp'] = timestamp
                        except:
                            pass
        
        # Set correct totals for all users (ensure we account for all possible tasks)
        total_possible_per_task = len(video_urls)
        
        for annotator in stats['per_task_annotators']:
            for task_name in [config["name"] for config in configs]:
                if task_name not in stats['per_task_annotators'][annotator]:
                    stats['per_task_annotators'][annotator][task_name] = {
                        'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': total_possible_per_task
                    }
                else:
                    # Make sure total is at least the expected number
                    stats['per_task_annotators'][annotator][task_name]['total'] = max(
                        stats['per_task_annotators'][annotator][task_name]['total'], 
                        total_possible_per_task
                    )
        
        for reviewer in stats['per_task_reviewers']:
            for task_name in [config["name"] for config in configs]:
                if task_name not in stats['per_task_reviewers'][reviewer]:
                    stats['per_task_reviewers'][reviewer][task_name] = {
                        'reviewed': 0, 'total': total_possible_per_task
                    }
                else:
                    # Make sure total is at least the expected number
                    stats['per_task_reviewers'][reviewer][task_name]['total'] = max(
                        stats['per_task_reviewers'][reviewer][task_name]['total'], 
                        total_possible_per_task
                    )
        
        # Add global stats to each user's stats
        for annotator_stats in stats['annotators'].values():
            annotator_stats['completed_all_users'] = stats['global']['completed_all_users']
            annotator_stats['reviewed_all_users'] = stats['global']['reviewed_all_users']
        
        for reviewer_stats in stats['reviewers'].values():
            reviewer_stats['completed_all_users'] = stats['global']['completed_all_users']
            reviewer_stats['reviewed_all_users'] = stats['global']['reviewed_all_users']
        
        return stats
        
    def _export_master_sheet(self, sheet_id: str, annotator_stats: Dict, reviewer_stats: Dict, task_names: List[str]):
        """Export the master sheet with annotator and reviewer tabs"""
        try:
            sheet = self._api_call_with_retry(self.client.open_by_key, sheet_id, 
                                            operation_name="opening master sheet")
        except Exception as e:
            print(f"❌ Error: Could not open master sheet with ID {sheet_id}")
            print(f"   Details: {str(e)}")
            print(f"\n💡 Possible solutions:")
            print(f"   1. Verify the sheet ID is correct")
            print(f"   2. Make sure you have edit access to the sheet")
            print(f"   3. Create a new Google Sheet and use its ID")
            print(f"   4. Share the sheet with your Google account")
            print(f"\n📝 To get the correct sheet ID:")
            print(f"   - Open your Google Sheet in browser")
            print(f"   - Copy the ID from URL: docs.google.com/spreadsheets/d/[SHEET_ID]/edit")
            return
        
        print("Exporting master sheet...")
        
        # Export Annotators tab
        self._export_master_tab(sheet, "Annotators", annotator_stats, task_names, "Annotator")
        
        # Export Reviewers tab  
        self._export_master_tab(sheet, "Reviewers", reviewer_stats, task_names, "Reviewer")
    
    def _export_master_tab(self, sheet, tab_name: str, user_stats: Dict, task_names: List[str], role: str):
        """Export a single tab in the master sheet"""
        print(f"  Exporting {tab_name} tab...")
        
        try:
            worksheet = sheet.worksheet(tab_name)
            print(f"    Found existing {tab_name} tab")
        except gspread.exceptions.WorksheetNotFound:
            print(f"    Creating new {tab_name} tab...")
            worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=20, 
                                                operation_name=f"creating {tab_name} tab")
        
        # Prepare headers based on role - REMOVED VIDEO COUNT
        if role == "Annotator":
            headers = [
                "User Name", "Email", "Annotation Sheet", "Last Annotated Time"
            ]
        else:  # Reviewer
            headers = [
                "User Name", "Email", "Review Sheet", "Last Review Time"
            ]
        
        # Add task headers with emoji short names
        for task_name in task_names:
            short_name = self.config_names_to_short_names.get(task_name, task_name)
            headers.append(f"{short_name} Total")
        
        # Prepare data rows
        rows = [headers]
        for user_name, stats in user_stats.items():
            if self._has_activity(stats):
                # Create placeholder links (will be updated later with actual URLs)
                sheet_link = "Link pending..."
                
                # Format timestamps based on role
                if role == "Annotator":
                    timestamp = self._format_timestamp(stats.get('last_annotation_timestamp'))
                else:  # Reviewer
                    timestamp = self._format_timestamp(stats.get('last_review_timestamp'))
                
                # Calculate totals per task
                task_totals = []
                for task_name in task_names:
                    if role == "Annotator":
                        total = stats['per_task'][task_name]['completed']
                    else:  # Reviewer
                        total = stats['per_task'][task_name]['reviewed']
                    task_totals.append(total)
                
                row = [
                    user_name, 
                    stats['email'], 
                    sheet_link, 
                    timestamp
                ] + task_totals
                rows.append(row)
        
        # Update the worksheet
        self._api_call_with_retry(worksheet.clear, operation_name="clearing master sheet")
        if rows:
            # Helper function to convert column number to Excel-style letter
            def col_num_to_letter(col_num):
                result = ""
                while col_num > 0:
                    col_num -= 1
                    result = chr(col_num % 26 + ord('A')) + result
                    col_num //= 26
                return result
            
            end_col = col_num_to_letter(len(headers))
            self._api_call_with_retry(worksheet.update, f'A1:{end_col}{len(rows)}', rows, 
                                    operation_name=f"updating {len(rows)-1} user records")
            
            # Apply master sheet formatting
            self._apply_master_sheet_formatting(worksheet, len(rows)-1, len(headers))
            
            print(f"    ✅ Successfully updated {len(rows)-1} users in {tab_name} tab")
    
    def _apply_master_sheet_formatting(self, worksheet, num_users: int, num_cols: int):
        """Apply formatting to master sheet with improved column widths"""
        try:
            # Header formatting
            header_format = {
                "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},  # Dark blue
                "textFormat": {"bold": True, "fontSize": 10, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},  # White text
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
            
            # Apply header formatting
            end_col = self._col_num_to_letter(num_cols)
            self._api_call_with_retry(
                worksheet.format, f"A1:{end_col}1", header_format,
                operation_name="formatting master sheet headers"
            )
            
            # Data row formatting (alternating colors)
            if num_users > 0:
                even_row_format = {
                    "backgroundColor": {"red": 0.95, "green": 0.98, "blue": 1.0}
                }
                
                for row in range(3, 2 + num_users + 1, 2):  # Every other row starting from 3
                    self._api_call_with_retry(
                        worksheet.format, f"A{row}:{end_col}{row}", even_row_format,
                        operation_name=f"formatting master row {row}"
                    )
            
            # Apply improved column widths for master sheet
            column_widths = [
                {"sheetId": worksheet.id, "startIndex": 0, "endIndex": 1, "pixelSize": 100},   # A: User Name
                {"sheetId": worksheet.id, "startIndex": 1, "endIndex": 2, "pixelSize": 161},   # B: Email (15% wider)
                {"sheetId": worksheet.id, "startIndex": 2, "endIndex": 3, "pixelSize": 100},   # C: Sheet Link (shorter text)
                {"sheetId": worksheet.id, "startIndex": 3, "endIndex": 4, "pixelSize": 144},   # D: Timestamp (shorter text)
            ]
            
            # Task total columns (20% wider with smaller font)
            for i in range(4, num_cols):
                column_widths.append({
                    "sheetId": worksheet.id, 
                    "startIndex": i, 
                    "endIndex": i + 1, 
                    "pixelSize": 96
                })
            
            # Apply column widths using batch update
            requests = []
            for width_spec in column_widths:
                requests.append({
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": width_spec["sheetId"],
                            "dimension": "COLUMNS",
                            "startIndex": width_spec["startIndex"],
                            "endIndex": width_spec["endIndex"]
                        },
                        "properties": {
                            "pixelSize": width_spec["pixelSize"]
                        },
                        "fields": "pixelSize"
                    }
                })
            
            if requests:
                self._api_call_with_retry(
                    worksheet.spreadsheet.batch_update,
                    {"requests": requests},
                    operation_name="updating master sheet column widths"
                )
            
            # Apply smaller font size to task total columns (columns E onwards)
            if num_cols > 4:
                task_header_format = {
                    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},  # Same blue background
                    "textFormat": {"bold": True, "fontSize": 8, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},  # Smaller font
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
                
                start_col = self._col_num_to_letter(5)  # Column E onwards
                end_col = self._col_num_to_letter(num_cols)
                self._api_call_with_retry(
                    worksheet.format, f"{start_col}1:{end_col}1", task_header_format,
                    operation_name="formatting task total headers with smaller font"
                )
            
            # Apply smaller font to main headers (columns C and D)
            main_header_small_format = {
                "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},  # Same blue background
                "textFormat": {"bold": True, "fontSize": 9, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},  # Smaller font
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
            
            self._api_call_with_retry(
                worksheet.format, "C1:D1", main_header_small_format,
                operation_name="formatting main headers with smaller font"
            )
            
            print(f"    ✅ Applied master sheet formatting with improved column widths")
            
        except Exception as e:
            print(f"    ⚠️  Master sheet formatting failed: {e}")
    
    # def _update_master_sheet_links(self, master_sheet_id: str, annotator_stats: Dict, 
    #                               reviewer_stats: Dict, user_sheet_ids: Dict):
    #     """Update master sheet with correct hyperlinks to user sheets (as smart chips)"""
    #     try:
    #         sheet = self._api_call_with_retry(self.client.open_by_key, master_sheet_id, 
    #                                         operation_name="opening master sheet for link updates")
    #     except:
    #         print(f"Error: Could not open master sheet for link updates")
    #         return

    #     # Update Annotators tab links - COLUMN C with SMART CHIPS
    #     try:
    #         worksheet = sheet.worksheet("Annotators")
    #         row_num = 2  # Start from row 2 (after headers)
            
    #         for user_name, stats in annotator_stats.items():
    #             if self._has_activity(stats):
    #                 annotation_sheet_name = f"{user_name} Annotator"
    #                 annotation_sheet_id = user_sheet_ids.get(annotation_sheet_name)
                    
    #                 if annotation_sheet_id:
    #                     annotation_url = f"https://docs.google.com/spreadsheets/d/{annotation_sheet_id}/edit"
                        
    #                     # Create smart chip using Method 1 (simple smart chip)
    #                     requests = [{
    #                         "updateCells": {
    #                             "rows": [{
    #                                 "values": [{
    #                                     "userEnteredValue": {
    #                                         "stringValue": "@"  # Single @ placeholder
    #                                     },
    #                                     "chipRuns": [{
    #                                         "startIndex": 0,  # @ is at position 0
    #                                         "chip": {
    #                                             "richLinkProperties": {
    #                                                 "uri": annotation_url
    #                                             }
    #                                         }
    #                                     }]
    #                                 }]
    #                             }],
    #                             "fields": "userEnteredValue,chipRuns",
    #                             "range": {
    #                                 "sheetId": worksheet.id,
    #                                 "startRowIndex": row_num - 1,  # Convert to 0-indexed
    #                                 "startColumnIndex": 2,  # Column C (0-indexed)
    #                                 "endRowIndex": row_num,
    #                                 "endColumnIndex": 3
    #                             }
    #                         }
    #                     }]
                        
    #                     self._api_call_with_retry(
    #                         worksheet.spreadsheet.batch_update,
    #                         {"requests": requests},
    #                         operation_name=f"updating annotation smart chip for {user_name}"
    #                     )
    #                 else:
    #                     # Fallback to text if no sheet ID
    #                     self._api_call_with_retry(worksheet.update, f'C{row_num}', [["Sheet not found"]], 
    #                                             operation_name=f"updating annotation text for {user_name}")
    #                 row_num += 1
            
    #         print("    ✅ Updated Annotators tab links (smart chips)")
    #     except Exception as e:
    #         print(f"    ❌ Failed to update Annotators tab links: {e}")
        
    #     # Update Reviewers tab links - COLUMN C with SMART CHIPS
    #     try:
    #         worksheet = sheet.worksheet("Reviewers")
    #         row_num = 2  # Start from row 2 (after headers)
            
    #         for user_name, stats in reviewer_stats.items():
    #             if self._has_activity(stats):
    #                 review_sheet_name = f"{user_name} Reviewer"
    #                 review_sheet_id = user_sheet_ids.get(review_sheet_name)
                    
    #                 if review_sheet_id:
    #                     review_url = f"https://docs.google.com/spreadsheets/d/{review_sheet_id}/edit"
                        
    #                     # Create smart chip using Method 1 (simple smart chip)
    #                     requests = [{
    #                         "updateCells": {
    #                             "rows": [{
    #                                 "values": [{
    #                                     "userEnteredValue": {
    #                                         "stringValue": "@"  # Single @ placeholder
    #                                     },
    #                                     "chipRuns": [{
    #                                         "startIndex": 0,  # @ is at position 0
    #                                         "chip": {
    #                                             "richLinkProperties": {
    #                                                 "uri": review_url
    #                                             }
    #                                         }
    #                                     }]
    #                                 }]
    #                             }],
    #                             "fields": "userEnteredValue,chipRuns",
    #                             "range": {
    #                                 "sheetId": worksheet.id,
    #                                 "startRowIndex": row_num - 1,  # Convert to 0-indexed
    #                                 "startColumnIndex": 2,  # Column C (0-indexed)
    #                                 "endRowIndex": row_num,
    #                                 "endColumnIndex": 3
    #                             }
    #                         }
    #                     }]
                        
    #                     self._api_call_with_retry(
    #                         worksheet.spreadsheet.batch_update,
    #                         {"requests": requests},
    #                         operation_name=f"updating review smart chip for {user_name}"
    #                     )
    #                 else:
    #                     # Fallback to text if no sheet ID
    #                     self._api_call_with_retry(worksheet.update, f'C{row_num}', [["Sheet not found"]], 
    #                                             operation_name=f"updating review text for {user_name}")
    #                 row_num += 1
            
    #         print("    ✅ Updated Reviewers tab links (smart chips)")
    #     except Exception as e:
    #         print(f"    ❌ Failed to update Reviewers tab links: {e}")
    
    # def _update_master_sheet_links(self, master_sheet_id: str, annotator_stats: Dict, 
    #                           reviewer_stats: Dict, user_sheet_ids: Dict, sheet_prefix: str):
    #     """Update master sheet with correct hyperlinks to user sheets (as smart chips)"""
    #     try:
    #         sheet = self._api_call_with_retry(self.client.open_by_key, master_sheet_id, 
    #                                         operation_name="opening master sheet for link updates")
    #     except:
    #         print(f"Error: Could not open master sheet for link updates")
    #         return

    #     # Update Annotators tab links - COLUMN C with SMART CHIPS
    #     try:
    #         worksheet = sheet.worksheet("Annotators")
    #         row_num = 2  # Start from row 2 (after headers)
            
    #         for user_name, stats in annotator_stats.items():
    #             if self._has_activity(stats):
    #                 annotation_sheet_name = f"{sheet_prefix}-{user_name} Annotator"
    #                 annotation_sheet_id = user_sheet_ids.get(annotation_sheet_name)
                    
    #                 if annotation_sheet_id:
    #                     annotation_url = f"https://docs.google.com/spreadsheets/d/{annotation_sheet_id}/edit"
                        
    #                     # Create smart chip using Method 1 (simple smart chip)
    #                     requests = [{
    #                         "updateCells": {
    #                             "rows": [{
    #                                 "values": [{
    #                                     "userEnteredValue": {
    #                                         "stringValue": "@"  # Single @ placeholder
    #                                     },
    #                                     "chipRuns": [{
    #                                         "startIndex": 0,  # @ is at position 0
    #                                         "chip": {
    #                                             "richLinkProperties": {
    #                                                 "uri": annotation_url
    #                                             }
    #                                         }
    #                                     }]
    #                                 }]
    #                             }],
    #                             "fields": "userEnteredValue,chipRuns",
    #                             "range": {
    #                                 "sheetId": worksheet.id,
    #                                 "startRowIndex": row_num - 1,  # Convert to 0-indexed
    #                                 "startColumnIndex": 2,  # Column C (0-indexed)
    #                                 "endRowIndex": row_num,
    #                                 "endColumnIndex": 3
    #                             }
    #                         }
    #                     }]
                        
    #                     self._api_call_with_retry(
    #                         worksheet.spreadsheet.batch_update,
    #                         {"requests": requests},
    #                         operation_name=f"updating annotation smart chip for {user_name}"
    #                     )
    #                 else:
    #                     # Fallback to text if no sheet ID
    #                     self._api_call_with_retry(worksheet.update, f'C{row_num}', [["Sheet not found"]], 
    #                                             operation_name=f"updating annotation text for {user_name}")
    #                 row_num += 1
            
    #         print("    ✅ Updated Annotators tab links (smart chips)")
    #     except Exception as e:
    #         print(f"    ❌ Failed to update Annotators tab links: {e}")
        
    #     # Update Reviewers tab links - COLUMN C with SMART CHIPS
    #     try:
    #         worksheet = sheet.worksheet("Reviewers")
    #         row_num = 2  # Start from row 2 (after headers)
            
    #         for user_name, stats in reviewer_stats.items():
    #             if self._has_activity(stats):
    #                 review_sheet_name = f"{sheet_prefix}-{user_name} Reviewer"
    #                 review_sheet_id = user_sheet_ids.get(review_sheet_name)
                    
    #                 if review_sheet_id:
    #                     review_url = f"https://docs.google.com/spreadsheets/d/{review_sheet_id}/edit"
                        
    #                     # Create smart chip using Method 1 (simple smart chip)
    #                     requests = [{
    #                         "updateCells": {
    #                             "rows": [{
    #                                 "values": [{
    #                                     "userEnteredValue": {
    #                                         "stringValue": "@"  # Single @ placeholder
    #                                     },
    #                                     "chipRuns": [{
    #                                         "startIndex": 0,  # @ is at position 0
    #                                         "chip": {
    #                                             "richLinkProperties": {
    #                                                 "uri": review_url
    #                                             }
    #                                         }
    #                                     }]
    #                                 }]
    #                             }],
    #                             "fields": "userEnteredValue,chipRuns",
    #                             "range": {
    #                                 "sheetId": worksheet.id,
    #                                 "startRowIndex": row_num - 1,  # Convert to 0-indexed
    #                                 "startColumnIndex": 2,  # Column C (0-indexed)
    #                                 "endRowIndex": row_num,
    #                                 "endColumnIndex": 3
    #                             }
    #                         }
    #                     }]
                        
    #                     self._api_call_with_retry(
    #                         worksheet.spreadsheet.batch_update,
    #                         {"requests": requests},
    #                         operation_name=f"updating review smart chip for {user_name}"
    #                     )
    #                 else:
    #                     # Fallback to text if no sheet ID
    #                     self._api_call_with_retry(worksheet.update, f'C{row_num}', [["Sheet not found"]], 
    #                                             operation_name=f"updating review text for {user_name}")
    #                 row_num += 1
            
    #         print("    ✅ Updated Reviewers tab links (smart chips)")
    #     except Exception as e:
    #         print(f"    ❌ Failed to update Reviewers tab links: {e}")

    def _update_master_sheet_links(self, master_sheet_id: str, annotator_stats: Dict, 
                          reviewer_stats: Dict, user_sheet_ids: Dict, sheet_prefix: str):
        """Update master sheet with correct hyperlinks to user sheets (as smart chips) - BATCHED VERSION"""
        try:
            sheet = self._api_call_with_retry(self.client.open_by_key, master_sheet_id, 
                                            operation_name="opening master sheet for link updates")
        except:
            print(f"Error: Could not open master sheet for link updates")
            return

        # Update Annotators tab links - COLUMN C with SMART CHIPS (BATCHED)
        try:
            worksheet = sheet.worksheet("Annotators")
            
            # Collect all smart chip requests for annotators
            smart_chip_requests = []
            row_num = 2  # Start from row 2 (after headers)
            
            for user_name, stats in annotator_stats.items():
                if self._has_activity(stats):
                    annotation_sheet_name = f"{sheet_prefix}-{user_name} Annotator"
                    annotation_sheet_id = user_sheet_ids.get(annotation_sheet_name)
                    
                    if annotation_sheet_id:
                        annotation_url = f"https://docs.google.com/spreadsheets/d/{annotation_sheet_id}/edit"
                        
                        # Add to batch request
                        smart_chip_requests.append({
                            "updateCells": {
                                "rows": [{
                                    "values": [{
                                        "userEnteredValue": {
                                            "stringValue": "@"
                                        },
                                        "chipRuns": [{
                                            "startIndex": 0,
                                            "chip": {
                                                "richLinkProperties": {
                                                    "uri": annotation_url
                                                }
                                            }
                                        }]
                                    }]
                                }],
                                "fields": "userEnteredValue,chipRuns",
                                "range": {
                                    "sheetId": worksheet.id,
                                    "startRowIndex": row_num - 1,
                                    "startColumnIndex": 2,  # Column C
                                    "endRowIndex": row_num,
                                    "endColumnIndex": 3
                                }
                            }
                        })
                    row_num += 1
            
            # Execute batch in chunks to avoid rate limits (max ~10 per batch)
            BATCH_SIZE = 10
            for i in range(0, len(smart_chip_requests), BATCH_SIZE):
                batch_chunk = smart_chip_requests[i:i + BATCH_SIZE]
                try:
                    self._api_call_with_retry(
                        worksheet.spreadsheet.batch_update,
                        {"requests": batch_chunk},
                        operation_name=f"batch updating {len(batch_chunk)} annotator smart chips"
                    )
                    print(f"        ✅ Updated {len(batch_chunk)} annotator links in batch")
                except Exception as e:
                    print(f"        ⚠️ Batch smart chip failed for annotators: {str(e)[:100]}")
                
                # Small delay between batches
                if i + BATCH_SIZE < len(smart_chip_requests):
                    time.sleep(2)
            
            print("    ✅ Updated Annotators tab links (smart chips - batched)")
        except Exception as e:
            print(f"    ❌ Failed to update Annotators tab links: {e}")
        
        # Update Reviewers tab links - COLUMN C with SMART CHIPS (BATCHED)
        try:
            worksheet = sheet.worksheet("Reviewers")
            
            # Collect all smart chip requests for reviewers
            smart_chip_requests = []
            row_num = 2  # Start from row 2 (after headers)
            
            for user_name, stats in reviewer_stats.items():
                if self._has_activity(stats):
                    review_sheet_name = f"{sheet_prefix}-{user_name} Reviewer"
                    review_sheet_id = user_sheet_ids.get(review_sheet_name)
                    
                    if review_sheet_id:
                        review_url = f"https://docs.google.com/spreadsheets/d/{review_sheet_id}/edit"
                        
                        # Add to batch request
                        smart_chip_requests.append({
                            "updateCells": {
                                "rows": [{
                                    "values": [{
                                        "userEnteredValue": {
                                            "stringValue": "@"
                                        },
                                        "chipRuns": [{
                                            "startIndex": 0,
                                            "chip": {
                                                "richLinkProperties": {
                                                    "uri": review_url
                                                }
                                            }
                                        }]
                                    }]
                                }],
                                "fields": "userEnteredValue,chipRuns",
                                "range": {
                                    "sheetId": worksheet.id,
                                    "startRowIndex": row_num - 1,
                                    "startColumnIndex": 2,  # Column C
                                    "endRowIndex": row_num,
                                    "endColumnIndex": 3
                                }
                            }
                        })
                    row_num += 1
            
            # Execute batch in chunks to avoid rate limits (max ~10 per batch)
            BATCH_SIZE = 10
            for i in range(0, len(smart_chip_requests), BATCH_SIZE):
                batch_chunk = smart_chip_requests[i:i + BATCH_SIZE]
                try:
                    self._api_call_with_retry(
                        worksheet.spreadsheet.batch_update,
                        {"requests": batch_chunk},
                        operation_name=f"batch updating {len(batch_chunk)} reviewer smart chips"
                    )
                    print(f"        ✅ Updated {len(batch_chunk)} reviewer links in batch")
                except Exception as e:
                    print(f"        ⚠️ Batch smart chip failed for reviewers: {str(e)[:100]}")
                
                # Small delay between batches
                if i + BATCH_SIZE < len(smart_chip_requests):
                    time.sleep(2)
            
            print("    ✅ Updated Reviewers tab links (smart chips - batched)")
        except Exception as e:
            print(f"    ❌ Failed to update Reviewers tab links: {e}")

    # def _export_user_sheet(self, user_name: str, role: str, stats: Dict, task_names: List[str], master_sheet_id: str, sheet_prefix: str) -> str:
    #     """Export individual user sheet and return sheet ID"""
    #     sheet_name = f"{sheet_prefix}-{user_name} {role}"  # Add prefix
    #     print(f"  Exporting {sheet_name} sheet...")
        
    #     try:
    #         # Try to open existing sheet (don't use retry logic here since failure is expected)
    #         sheet = self.client.open(sheet_name)
    #         print(f"    Found existing sheet: {sheet_name}")
    #     except (gspread.exceptions.SpreadsheetNotFound, Exception):
    #         # Create new sheet
    #         print(f"    Creating new sheet: {sheet_name}")
    #         sheet = self._api_call_with_retry(self.client.create, sheet_name, 
    #                                         operation_name=f"creating sheet '{sheet_name}'")
        
    #     # Export Payment tab
    #     self._export_user_tab(sheet, "Payment", user_name, role, stats, task_names, include_payment=True)
        
    #     # Export Feedback tab
    #     self._export_user_tab(sheet, "Feedback", user_name, role, stats, task_names, include_payment=False)
        
    #     return sheet.id

    def _export_user_sheet(self, user_name: str, role: str, stats: Dict, task_names: List[str], master_sheet_id: str, sheet_prefix: str) -> str:
        """Export individual user sheet and return sheet ID"""
        sheet_name = f"{sheet_prefix}-{user_name} {role}"  # Add prefix
        print(f"  Exporting {sheet_name} sheet...")
        
        sheet = None
        
        try:
            # First try direct open (fastest)
            sheet = self.client.open(sheet_name)
            print(f"    Found existing sheet: {sheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            # Sheet genuinely doesn't exist
            print(f"    Creating new sheet: {sheet_name}")
            sheet = self._api_call_with_retry(self.client.create, sheet_name, 
                                            operation_name=f"creating sheet '{sheet_name}'")
        except gspread.exceptions.APIError as e:
            # Rate limit or other API error - don't create new sheet!
            error_str = str(e).lower()
            if "429" in str(e) or "quota" in error_str or "rate" in error_str:
                print(f"    ⏳ Rate limit hit while searching for sheet, waiting 10s...")
                time.sleep(10)
                # Retry once
                try:
                    sheet = self.client.open(sheet_name)
                    print(f"    Found existing sheet after retry: {sheet_name}")
                except gspread.exceptions.SpreadsheetNotFound:
                    print(f"    Creating new sheet: {sheet_name}")
                    sheet = self._api_call_with_retry(self.client.create, sheet_name,
                                                    operation_name=f"creating sheet '{sheet_name}'")
            else:
                raise
        except Exception as e:
            # Log unexpected errors but don't blindly create new sheet
            print(f"    ⚠️ Unexpected error looking for sheet: {type(e).__name__}: {str(e)[:100]}")
            raise
        
        # Export Payment tab
        self._export_user_tab(sheet, "Payment", user_name, role, stats, task_names, include_payment=True)
        
        # Export Feedback tab
        self._export_user_tab(sheet, "Feedback", user_name, role, stats, task_names, include_payment=False)
        
        return sheet.id
    
    # def _export_user_tab(self, sheet, tab_name: str, user_name: str, role: str, stats: Dict, 
    #                     task_names: List[str], include_payment: bool):
    #     """Export a single tab in a user sheet with smart preservation and formatting"""
    #     print(f"    Exporting {tab_name} tab...")
        
    #     try:
    #         worksheet = sheet.worksheet(tab_name)
    #         print(f"      Found existing {tab_name} tab")
    #     except gspread.exceptions.WorksheetNotFound:
    #         print(f"      Creating new {tab_name} tab...")
    #         worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=50, 
    #                                             operation_name=f"creating {tab_name} worksheet")
    #     except Exception as e:
    #         print(f"      Error accessing {tab_name} tab: {e}")
    #         print(f"      Creating new {tab_name} tab...")
    #         worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=50, 
    #                                             operation_name=f"creating {tab_name} worksheet")
        
    #     # Step 1: Read existing data to preserve manual columns
    #     existing_data = self._read_existing_manual_data(worksheet, role, include_payment, task_names)
        
    #     # Step 1.5: Clear and unmerge header area to avoid merge conflicts
    #     self._clear_header_area(worksheet, task_names, include_payment)
        
    #     # Step 2: Create headers with proper formatting
    #     if role == "Annotator":
    #         self._create_annotator_headers(worksheet, task_names, include_payment)
    #     else:  # Reviewer
    #         self._create_reviewer_headers(worksheet, task_names, include_payment)
        
    #     # Step 3: Prepare data rows preserving manual data
    #     data_rows = []
    #     manual_col_indices = self._get_manual_column_indices(role, include_payment, task_names)
        
    #     # Add rows for each video file
    #     for video_file, file_stats in stats['per_video_file'].items():
    #         if file_stats.get('completed_current_user', 0) > 0 or file_stats.get('reviewed_by_current_user', 0) > 0:
    #             # Create automatic data row
    #             auto_row = self._create_data_row(video_file, file_stats, stats, task_names, role, include_payment)
                
    #             # Merge with preserved manual data
    #             preserved_row = self._merge_with_manual_data(auto_row, video_file, existing_data, manual_col_indices)
    #             data_rows.append(preserved_row)
        
    #     # Step 4: Update data rows with smart preservation
    #     if data_rows:
    #         self._update_data_with_preservation(worksheet, data_rows, 3, include_payment, task_names, role)  # Start from row 3
    #         print(f"      ✅ Successfully updated {len(data_rows)} rows with preserved manual data")
    #     else:
    #         print(f"      ℹ️  No data to update in {tab_name} tab")
        
    #     # Step 5: Apply beautiful formatting
    #     self._apply_worksheet_formatting(worksheet, role, include_payment, task_names, len(data_rows))
    
    def _clear_header_area(self, worksheet, task_names: List[str], include_payment: bool):
        """Clear and unmerge the header area to avoid merge conflicts"""
        print(f"      🧹 Clearing header area to avoid merge conflicts...")
        
        try:
            # Calculate the total number of columns we'll need
            base_cols = 7  # A-G: Json Sheet Name, Video Count, Completion Ratio (2), Reviewed Ratio (2), Last Submitted
            payment_cols = 3 if include_payment else 1  # Payment cols or Feedback col
            task_cols = len(task_names) * 6  # 6 columns per task for annotators, 2 for reviewers (will adjust)
            total_cols = base_cols + payment_cols + task_cols
            
            # Convert to letter
            end_col = self._col_num_to_letter(min(total_cols, 50))  # Cap at 50 columns for safety
            
            # Use batch unmerge to unmerge all cells in header area
            requests = []
            
            # Unmerge entire header area (rows 1-2)
            requests.append({
                "unmergeCells": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": 2,
                        "startColumnIndex": 0,
                        "endColumnIndex": min(total_cols, 50)
                    }
                }
            })
            
            if requests:
                try:
                    self._api_call_with_retry(
                        worksheet.spreadsheet.batch_update,
                        {"requests": requests},
                        operation_name="unmerging header area"
                    )
                except Exception as e:
                    # Ignore errors about no merged cells to unmerge
                    if "no merged cells" not in str(e).lower() and "nothing to unmerge" not in str(e).lower():
                        print(f"      ⚠️  Could not unmerge header area: {e}")
            
            # Clear the header area after unmerging
            try:
                self._api_call_with_retry(worksheet.batch_clear, [f'A1:{end_col}2'], 
                                        operation_name="clearing header area after unmerge")
                print(f"      ✅ Header area cleared successfully")
            except Exception as e:
                print(f"      ⚠️  Could not clear header area: {e}")
            
        except Exception as e:
            print(f"      ⚠️  Could not clear header area: {e}")
    
    def _read_existing_manual_data(self, worksheet, role: str, include_payment: bool, task_names: List[str]) -> Dict:
        """Read existing manual data to preserve it during updates"""
        try:
            # Get all data from worksheet
            all_data = worksheet.get_all_values()
            if len(all_data) < 3:  # No data rows
                return {}
            
            manual_col_indices = self._get_manual_column_indices(role, include_payment, task_names)
            existing_manual = {}
            
            # Skip header rows (0, 1) and start from data rows (2+)
            for row_idx, row in enumerate(all_data[2:], start=3):
                if len(row) > 0 and row[0]:  # Has Json Sheet Name
                    video_file = row[0]
                    manual_data = {}
                    
                    # Extract manual column values
                    for col_name, col_idx in manual_col_indices.items():
                        if col_idx < len(row):
                            manual_data[col_name] = row[col_idx]
                        else:
                            manual_data[col_name] = ''
                    
                    existing_manual[video_file] = manual_data
            
            print(f"      📖 Preserved manual data for {len(existing_manual)} video files")
            return existing_manual
            
        except Exception as e:
            print(f"      ⚠️  Could not read existing data (will create fresh): {e}")
            return {}
    
    def _get_manual_column_indices(self, role: str, include_payment: bool, task_names: List[str]) -> Dict[str, int]:
        """Get the column indices for manual (preserved) columns"""
        manual_cols = {}
        
        # Calculate payment/feedback start column based on role
        if role == "Annotator":
            payment_start_col = 7  # Column H for annotators
        else:  # Reviewer
            payment_start_col = 6  # Column G for reviewers
        
        if include_payment:
            # Payment columns are manual
            manual_cols["Payment Timestamp"] = payment_start_col      # Column H (annotators) / G (reviewers)
            manual_cols["Base Salary"] = payment_start_col + 1        # Column I (annotators) / H (reviewers)  
            manual_cols["Bonus Salary"] = payment_start_col + 2       # Column J (annotators) / I (reviewers)
        else:
            if role == "Annotator":
                # Feedback column is manual
                manual_cols["Feedback to Annotator"] = payment_start_col  # Column H (annotators) / G (reviewers)
            else:
                # Feedback column is manual
                manual_cols["Feedback to Reviewer"] = payment_start_col  # Column H (annotators) / G (reviewers)
        
        return manual_cols
    
    def _merge_with_manual_data(self, auto_row: List, video_file: str, existing_data: Dict, 
                               manual_col_indices: Dict[str, int]) -> List:
        """Merge automatic data with preserved manual data"""
        # Start with the automatic row
        merged_row = auto_row.copy()
        
        # Overlay preserved manual data if it exists for this video file
        if video_file in existing_data:
            preserved = existing_data[video_file]
            for col_name, col_idx in manual_col_indices.items():
                if col_idx < len(merged_row) and col_name in preserved:
                    merged_row[col_idx] = preserved[col_name]
        
        return merged_row
    
    def _update_data_with_preservation(self, worksheet, data_rows: List[List], start_row: int, 
                                     include_payment: bool, task_names: List[str], role: str):
        """Update data rows while preserving manual columns - FIXED: Added missing parameters"""
        if not data_rows:
            return
        
        # Helper function to convert column number to Excel-style letter
        def col_num_to_letter(col_num):
            result = ""
            while col_num > 0:
                col_num -= 1
                result = chr(col_num % 26 + ord('A')) + result
                col_num //= 26
            return result
        

        end_row = start_row + len(data_rows) - 1
        end_col = col_num_to_letter(len(data_rows[0]))
        
        # Update all data at once
        self._api_call_with_retry(worksheet.update, f'A{start_row}:{end_col}{end_row}', data_rows, 
                                operation_name=f"updating {len(data_rows)} data rows with preservation")
    
    # def _apply_worksheet_formatting(self, worksheet, role: str, include_payment: bool, 
    #                                task_names: List[str], num_data_rows: int):
    #     """Apply beautiful formatting to the worksheet with improved column widths"""
    #     print(f"      🎨 Applying formatting and styling...")
        
    #     try:
    #         # Apply improved column widths for individual user sheets
    #         column_widths = [
    #             {"startIndex": 0, "endIndex": 1, "pixelSize": 150},   # A: Json Sheet Name (50% wider)
    #             {"startIndex": 1, "endIndex": 2, "pixelSize": 80},    # B: Video Count
    #         ]
            
    #         if role == "Annotator":
    #             # Annotator structure: C,D = Completion Ratio, E,F = Reviewed Ratio, G = Last Submitted
    #             column_widths.extend([
    #                 {"startIndex": 2, "endIndex": 3, "pixelSize": 60},    # C: Completion Ratio - All Users
    #                 {"startIndex": 3, "endIndex": 4, "pixelSize": 60},    # D: Completion Ratio - Current User
    #                 {"startIndex": 4, "endIndex": 5, "pixelSize": 60},    # E: Reviewed Ratio - All Users
    #                 {"startIndex": 5, "endIndex": 6, "pixelSize": 60},    # F: Reviewed Ratio - Current User
    #                 {"startIndex": 6, "endIndex": 7, "pixelSize": 132},   # G: Last Submitted Timestamp
    #             ])
    #             payment_start_col = 7  # Column H
    #         else:  # Reviewer
    #             # Reviewer structure: C = Completion Ratio, D,E = Reviewed Ratio, F = Last Submitted
    #             column_widths.extend([
    #                 {"startIndex": 2, "endIndex": 3, "pixelSize": 60},    # C: Completion Ratio - All Users
    #                 {"startIndex": 3, "endIndex": 4, "pixelSize": 60},    # D: Reviewed Ratio - All Users
    #                 {"startIndex": 4, "endIndex": 5, "pixelSize": 60},    # E: Reviewed Ratio - Current User
    #                 {"startIndex": 5, "endIndex": 6, "pixelSize": 132},   # F: Last Submitted Timestamp
    #             ])
    #             payment_start_col = 6  # Column G
            
    #         # Payment/Feedback columns
    #         if include_payment:
    #             column_widths.extend([
    #                 {"startIndex": payment_start_col, "endIndex": payment_start_col + 1, "pixelSize": 120},      # Payment Timestamp
    #                 {"startIndex": payment_start_col + 1, "endIndex": payment_start_col + 2, "pixelSize": 90},   # Base Salary
    #                 {"startIndex": payment_start_col + 2, "endIndex": payment_start_col + 3, "pixelSize": 90},   # Bonus Salary
    #             ])
    #             start_task_col = payment_start_col + 3
    #         else:
    #             column_widths.append(
    #                 {"startIndex": payment_start_col, "endIndex": payment_start_col + 1, "pixelSize": 300}      # Feedback to Annotator - very wide
    #             )
    #             start_task_col = payment_start_col + 1
            
    #         # Task columns - all should be 84px for consistency
    #         task_col_widths = [84, 84, 84, 84, 84, 84] if role == "Annotator" else [84, 84]  # All 84px
    #         current_col = start_task_col
            
    #         for task_idx in range(len(task_names)):
    #             for width in task_col_widths:
    #                 column_widths.append({
    #                     "startIndex": current_col, 
    #                     "endIndex": current_col + 1, 
    #                     "pixelSize": width
    #                 })
    #                 current_col += 1
            
    #         # Apply column widths using batch update
    #         requests = []
    #         for width_spec in column_widths:
    #             requests.append({
    #                 "updateDimensionProperties": {
    #                     "range": {
    #                         "sheetId": worksheet.id,
    #                         "dimension": "COLUMNS",
    #                         "startIndex": width_spec["startIndex"],
    #                         "endIndex": width_spec["endIndex"]
    #                     },
    #                     "properties": {
    #                         "pixelSize": width_spec["pixelSize"]
    #                     },
    #                     "fields": "pixelSize"
    #                 }
    #             })
            
    #         if requests:
    #             self._api_call_with_retry(
    #                 worksheet.spreadsheet.batch_update,
    #                 {"requests": requests},
    #                 operation_name="updating user sheet column widths"
    #             )
            
    #         # Format header rows (1-2)
    #         self._apply_header_formatting(worksheet, task_names, role, include_payment)
            
    #         # Format data rows (3+) with proper heights
    #         if num_data_rows > 0:
    #             # Feedback tab needs much taller rows for 100-word feedback
    #             if not include_payment:  # This is the Feedback tab
    #                 data_height = 100  # Very tall for 100-word feedback
    #             else:  # This is the Payment tab
    #                 data_height = 35   # Normal height
                    
    #             self._apply_data_formatting(worksheet, num_data_rows, role, include_payment)
            
    #         print(f"      ✅ Applied professional formatting with improved column widths")
            
    #     except Exception as e:
    #         print(f"      ⚠️  Some formatting may not have applied: {e}")
    
    def _apply_header_formatting(self, worksheet, task_names: List[str], role: str, include_payment: bool = False):
        """Apply formatting to header rows"""
        try:
            # Header background color (light blue)
            header_format = {
                "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0},
                "textFormat": {"bold": True, "fontSize": 11},
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
            
            # Apply to header rows
            self._api_call_with_retry(
                worksheet.format, "A1:ZZ2", header_format,
                operation_name="formatting headers"
            )
            
            # Apply smaller font to task sub-headers in row 2
            # Calculate where task columns start (matches our column width calculation)
            if role == "Annotator":
                start_task_col = 11 if include_payment else 9   # Column K with payment, I without
            else:  # Reviewer
                start_task_col = 10 if include_payment else 8   # Column J with payment, H without
            
            # Apply smaller font to task sub-headers (Accuracy, Completion, etc.)
            task_subheader_format = {
                "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0},
                "textFormat": {"bold": True, "fontSize": 8},  # Much smaller font
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
            
            start_col = self._col_num_to_letter(start_task_col)
            self._api_call_with_retry(
                worksheet.format, f"{start_col}2:ZZ2", task_subheader_format,
                operation_name="formatting task sub-headers with smaller font"
            )
            
        except Exception as e:
            print(f"      ⚠️  Header formatting failed: {e}")
    
    # def _apply_data_formatting(self, worksheet, num_data_rows: int, role: str, include_payment: bool):
    #     """Apply formatting to data rows"""
    #     try:
    #         # Alternating row colors
    #         even_row_format = {
    #             "backgroundColor": {"red": 0.95, "green": 0.98, "blue": 1.0}
    #         }
            
    #         # Apply alternating colors to even rows
    #         for row in range(4, 3 + num_data_rows + 1, 2):  # Every other row starting from 4
    #             self._api_call_with_retry(
    #                 worksheet.format, f"A{row}:ZZ{row}", even_row_format,
    #                 operation_name=f"formatting row {row}"
    #             )
            
    #         # Special formatting for feedback rows (make them much taller)
    #         if not include_payment:  # Feedback tab
    #             # Make rows taller for 100-word feedback
    #             row_height_requests = []
    #             for row_index in range(2, 2 + num_data_rows):  # Start from row 3 (index 2)
    #                 row_height_requests.append({
    #                     "updateDimensionProperties": {
    #                         "range": {
    #                             "sheetId": worksheet.id,
    #                             "dimension": "ROWS",
    #                             "startIndex": row_index,
    #                             "endIndex": row_index + 1
    #                         },
    #                         "properties": {
    #                             "pixelSize": 120  # Much taller for 100-word feedback
    #                         },
    #                         "fields": "pixelSize"
    #                     }
    #                 })
                
    #             if row_height_requests:
    #                 self._api_call_with_retry(
    #                     worksheet.spreadsheet.batch_update,
    #                     {"requests": row_height_requests},
    #                     operation_name="setting feedback row heights"
    #                 )
                
    #             # Calculate feedback column based on role
    #             if role == "Annotator":
    #                 feedback_col = "H"  # Column H for annotators
    #             else:  # Reviewer  
    #                 feedback_col = "G"  # Column G for reviewers
                
    #             feedback_format = {
    #                 "wrapStrategy": "WRAP",  # Wrap text for long feedback
    #                 "verticalAlignment": "TOP",
    #                 "textFormat": {"fontSize": 9}  # Smaller font to fit more text
    #             }
    #             self._api_call_with_retry(
    #                 worksheet.format, f"{feedback_col}3:{feedback_col}{2+num_data_rows}", feedback_format,
    #                 operation_name="formatting feedback column"
    #             )
            
    #         # Format percentage columns (no decimals for accuracy)
    #         # Accuracy columns (no decimals)
    #         accuracy_format = {"numberFormat": {"type": "PERCENT", "pattern": "0%"}}
    #         # Other percentage columns (1 decimal)
    #         percent_format = {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}
            
    #         if role == "Annotator":
    #             # Apply to completion ratios (EXCLUDE column B which is Video Count)
    #             self._api_call_with_retry(
    #                 worksheet.format, f"C3:F{2+num_data_rows}", percent_format,
    #                 operation_name="formatting percentage columns"
    #             )
    #         else:  # Reviewer
    #             # For reviewers, only columns C, D, E are percentages (F is Last Submitted)
    #             self._api_call_with_retry(
    #                 worksheet.format, f"C3:E{2+num_data_rows}", percent_format,
    #                 operation_name="formatting percentage columns"
    #             )
            
    #         # Ensure Video Count column (B) is formatted as regular numbers, not percentages
    #         number_format = {"numberFormat": {"type": "NUMBER", "pattern": "0"}}
    #         self._api_call_with_retry(
    #             worksheet.format, f"B3:B{2+num_data_rows}", number_format,
    #             operation_name="formatting video count as numbers"
    #         )
            
    #         # Format Last Submitted Timestamp column to align text to bottom
    #         if role == "Annotator":
    #             timestamp_col = "G"  # Column G for annotators
    #         else:  # Reviewer
    #             timestamp_col = "F"  # Column F for reviewers
            
    #         timestamp_format = {
    #             "verticalAlignment": "BOTTOM",
    #             "horizontalAlignment": "LEFT"
    #         }
    #         self._api_call_with_retry(
    #             worksheet.format, f"{timestamp_col}3:{timestamp_col}{2+num_data_rows}", timestamp_format,
    #             operation_name="formatting timestamp column alignment"
    #         )
            
    #     except Exception as e:
    #         print(f"      ⚠️  Data formatting failed: {e}")
    
    def _apply_alternating_row_colors(self, worksheet, data_rows_count: int, header_rows: int = 2):
        """Apply alternating row colors as the FINAL formatting step to ensure they stick"""
        if data_rows_count <= 0:
            return
        
        try:
            sheet_id = worksheet.id
            
            # Define colors
            light_blue_color = {
                "red": 0.95,
                "green": 0.98, 
                "blue": 1.0
            }
            
            white_color = {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
            }
            
            # Build comprehensive alternating color requests
            alternating_requests = []
            
            # Calculate the range of data rows (after headers)
            first_data_row = header_rows  # 0-indexed (row 3 in 1-indexed becomes 2 in 0-indexed)
            
            # Apply colors to ALL data rows (both blue and white explicitly)
            for row_index in range(first_data_row, header_rows + data_rows_count):
                # Determine if this should be colored (every other row)
                is_colored_row = (row_index - first_data_row) % 2 == 1  # 0, 2, 4... = white; 1, 3, 5... = blue
                
                background_color = light_blue_color if is_colored_row else white_color
                
                alternating_requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row_index,
                            "endRowIndex": row_index + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 50  # Cover all relevant columns
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": background_color
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                })
            
            # Apply all alternating colors in one batch (HIGHER PRIORITY)
            if alternating_requests:
                alternating_batch_request = {"requests": alternating_requests}
                self._api_call_with_retry(
                    worksheet.spreadsheet.batch_update,
                    alternating_batch_request,
                    operation_name="applying robust alternating row colors"
                )
                
                print(f"      ✅ Applied alternating colors to {data_rows_count} rows (pattern agnostic)")
                
        except Exception as e:
            print(f"      ⚠️ Could not apply alternating row colors: {e}")

    # 2. MODIFY: Add sorting to _export_user_tab method
    def _export_user_tab(self, sheet, tab_name: str, user_name: str, role: str, stats: Dict, 
                        task_names: List[str], include_payment: bool):
        """Export a single tab in a user sheet with smart preservation, sorting, and formatting"""
        print(f"    Exporting {tab_name} tab...")
        
        try:
            worksheet = sheet.worksheet(tab_name)
            print(f"      Found existing {tab_name} tab")
        except gspread.exceptions.WorksheetNotFound:
            print(f"      Creating new {tab_name} tab...")
            worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=50, 
                                                operation_name=f"creating {tab_name} worksheet")

        except Exception as e:
            error_str = str(e).lower()
            if '429' in str(e) or 'quota' in error_str or 'rate' in error_str:
                print(f"      ⏳ Rate limit accessing {tab_name} tab, retrying after 10s...")
                time.sleep(10)
                worksheet = sheet.worksheet(tab_name)  # retry lookup
            else:
                print(f"      Error accessing {tab_name} tab: {e}")
                print(f"      Creating new {tab_name} tab...")
                worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=50, 
                                                    operation_name=f"creating {tab_name} worksheet")
        # except Exception as e:
        #     print(f"      Error accessing {tab_name} tab: {e}")
        #     print(f"      Creating new {tab_name} tab...")
        #     worksheet = self._api_call_with_retry(sheet.add_worksheet, title=tab_name, rows=100, cols=50, 
        #                                         operation_name=f"creating {tab_name} worksheet")
        
        # Step 1: Read existing data to preserve manual columns
        existing_data = self._read_existing_manual_data(worksheet, role, include_payment, task_names)
        
        # Step 1.5: Clear and unmerge header area to avoid merge conflicts
        self._clear_header_area(worksheet, task_names, include_payment)
        
        # Step 2: Create headers with proper formatting
        if role == "Annotator":
            self._create_annotator_headers(worksheet, task_names, include_payment)
        else:  # Reviewer
            self._create_reviewer_headers(worksheet, task_names, include_payment)
        
        # Step 3: SORT video files by last activity timestamp (MOST RECENT FIRST)
        video_files_with_stats = []
        for video_file, file_stats in stats['per_video_file'].items():
            if file_stats.get('completed_current_user', 0) > 0 or file_stats.get('reviewed_by_current_user', 0) > 0:
                # Determine the relevant timestamp for sorting
                if role == "Annotator":
                    sort_timestamp = file_stats.get('last_annotation_timestamp')
                else:  # Reviewer
                    sort_timestamp = file_stats.get('last_review_timestamp')
                
                video_files_with_stats.append((video_file, file_stats, sort_timestamp))
        
        # Sort by timestamp (most recent first) - handle None timestamps
        from datetime import datetime
        video_files_with_stats.sort(
            key=lambda x: datetime.fromisoformat(x[2]) if x[2] else datetime.min,
            reverse=True
        )
        
        print(f"      📊 Sorted {len(video_files_with_stats)} video files by most recent activity")
        
        # Step 4: Prepare data rows preserving manual data (now in sorted order)
        data_rows = []
        manual_col_indices = self._get_manual_column_indices(role, include_payment, task_names)
        
        # Add rows for each video file (now sorted)
        for video_file, file_stats, _ in video_files_with_stats:
            # Create automatic data row
            auto_row = self._create_data_row(video_file, file_stats, stats, task_names, role, include_payment)
            
            # Merge with preserved manual data (by video file name - safe because we map by name)
            preserved_row = self._merge_with_manual_data(auto_row, video_file, existing_data, manual_col_indices)
            data_rows.append(preserved_row)
        
        # Step 5: Update data rows with smart preservation
        if data_rows:
            self._update_data_with_preservation(worksheet, data_rows, 3, include_payment, task_names, role)
            print(f"      ✅ Successfully updated {len(data_rows)} sorted rows with preserved manual data")
        else:
            print(f"      ℹ️  No data to update in {tab_name} tab")
        
        # Step 6: Apply beautiful formatting with robust alternating colors
        self._apply_worksheet_formatting(worksheet, role, include_payment, task_names, len(data_rows))

    # 3. MODIFY: Update _apply_worksheet_formatting to use robust alternating colors
    def _apply_worksheet_formatting(self, worksheet, role: str, include_payment: bool, 
                                task_names: List[str], num_data_rows: int):
        """Apply beautiful formatting to the worksheet with robust alternating row colors"""
        print(f"      🎨 Applying formatting and styling...")
        
        try:
            # Apply improved column widths for individual user sheets
            column_widths = [
                {"startIndex": 0, "endIndex": 1, "pixelSize": 150},   # A: Json Sheet Name (50% wider)
                {"startIndex": 1, "endIndex": 2, "pixelSize": 80},    # B: Video Count
            ]
            
            if role == "Annotator":
                # Annotator structure: C,D = Completion Ratio, E,F = Reviewed Ratio, G = Last Submitted
                column_widths.extend([
                    {"startIndex": 2, "endIndex": 3, "pixelSize": 60},    # C: Completion Ratio - All Users
                    {"startIndex": 3, "endIndex": 4, "pixelSize": 60},    # D: Completion Ratio - Current User
                    {"startIndex": 4, "endIndex": 5, "pixelSize": 60},    # E: Reviewed Ratio - All Users
                    {"startIndex": 5, "endIndex": 6, "pixelSize": 60},    # F: Reviewed Ratio - Current User
                    {"startIndex": 6, "endIndex": 7, "pixelSize": 132},   # G: Last Submitted Timestamp
                ])
                payment_start_col = 7  # Column H
            else:  # Reviewer
                # Reviewer structure: C = Completion Ratio, D,E = Reviewed Ratio, F = Last Submitted
                column_widths.extend([
                    {"startIndex": 2, "endIndex": 3, "pixelSize": 60},    # C: Completion Ratio - All Users
                    {"startIndex": 3, "endIndex": 4, "pixelSize": 60},    # D: Reviewed Ratio - All Users
                    {"startIndex": 4, "endIndex": 5, "pixelSize": 60},    # E: Reviewed Ratio - Current User
                    {"startIndex": 5, "endIndex": 6, "pixelSize": 132},   # F: Last Submitted Timestamp
                ])
                payment_start_col = 6  # Column G
            
            # Payment/Feedback columns
            if include_payment:
                column_widths.extend([
                    {"startIndex": payment_start_col, "endIndex": payment_start_col + 1, "pixelSize": 120},      # Payment Timestamp
                    {"startIndex": payment_start_col + 1, "endIndex": payment_start_col + 2, "pixelSize": 90},   # Base Salary
                    {"startIndex": payment_start_col + 2, "endIndex": payment_start_col + 3, "pixelSize": 90},   # Bonus Salary
                ])
                start_task_col = payment_start_col + 3
            else:
                column_widths.append(
                    {"startIndex": payment_start_col, "endIndex": payment_start_col + 1, "pixelSize": 300}      # Feedback - very wide
                )
                start_task_col = payment_start_col + 1
            
            # Task columns - all should be 84px for consistency
            task_col_widths = [84, 84, 84, 84, 84, 84] if role == "Annotator" else [84, 84]  # All 84px
            current_col = start_task_col
            
            for task_idx in range(len(task_names)):
                for width in task_col_widths:
                    column_widths.append({
                        "startIndex": current_col, 
                        "endIndex": current_col + 1, 
                        "pixelSize": width
                    })
                    current_col += 1
            
            # Apply column widths using batch update
            requests = []
            for width_spec in column_widths:
                requests.append({
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": worksheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": width_spec["startIndex"],
                            "endIndex": width_spec["endIndex"]
                        },
                        "properties": {
                            "pixelSize": width_spec["pixelSize"]
                        },
                        "fields": "pixelSize"
                    }
                })
            
            if requests:
                self._api_call_with_retry(
                    worksheet.spreadsheet.batch_update,
                    {"requests": requests},
                    operation_name="updating user sheet column widths"
                )
            
            # Format header rows (1-2)
            self._apply_header_formatting(worksheet, task_names, role, include_payment)
            
            # Format data rows (3+) with proper heights - REMOVED OLD ALTERNATING COLOR CODE
            if num_data_rows > 0:
                # Set special row heights for feedback rows
                if not include_payment:  # Feedback tab
                    # Make rows taller for 100-word feedback
                    row_height_requests = []
                    for row_index in range(2, 2 + num_data_rows):  # Start from row 3 (index 2)
                        row_height_requests.append({
                            "updateDimensionProperties": {
                                "range": {
                                    "sheetId": worksheet.id,
                                    "dimension": "ROWS",
                                    "startIndex": row_index,
                                    "endIndex": row_index + 1
                                },
                                "properties": {
                                    "pixelSize": 120  # Much taller for 100-word feedback
                                },
                                "fields": "pixelSize"
                            }
                        })
                    
                    if row_height_requests:
                        self._api_call_with_retry(
                            worksheet.spreadsheet.batch_update,
                            {"requests": row_height_requests},
                            operation_name="setting feedback row heights"
                        )
                
                # Apply other data formatting (percentages, etc.) - NO background colors here
                self._apply_data_formatting_no_colors(worksheet, num_data_rows, role, include_payment)
                
                # APPLY ALTERNATING ROW COLORS LAST (robust method)
                self._apply_alternating_row_colors(worksheet, num_data_rows, header_rows=2)
            
            print(f"      ✅ Applied comprehensive formatting with robust alternating rows")
            
        except Exception as e:
            print(f"      ⚠️  Some formatting may not have applied: {e}")

    # 4. ADD: Data formatting without background colors (to avoid conflicts)
    def _apply_data_formatting_no_colors(self, worksheet, num_data_rows: int, role: str, include_payment: bool):
        """Apply data formatting without background colors (colors applied separately)"""
        try:
            # Format percentage columns (no decimals for accuracy)
            # Accuracy columns (no decimals)
            accuracy_format = {"numberFormat": {"type": "PERCENT", "pattern": "0%"}}
            # Other percentage columns (1 decimal)
            percent_format = {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}
            
            if role == "Annotator":
                # Apply to completion ratios (EXCLUDE column B which is Video Count)
                self._api_call_with_retry(
                    worksheet.format, f"C3:F{2+num_data_rows}", percent_format,
                    operation_name="formatting percentage columns"
                )
            else:  # Reviewer
                # For reviewers, only columns C, D, E are percentages (F is Last Submitted)
                self._api_call_with_retry(
                    worksheet.format, f"C3:E{2+num_data_rows}", percent_format,
                    operation_name="formatting percentage columns"
                )
            
            # Ensure Video Count column (B) is formatted as regular numbers, not percentages
            number_format = {"numberFormat": {"type": "NUMBER", "pattern": "0"}}
            self._api_call_with_retry(
                worksheet.format, f"B3:B{2+num_data_rows}", number_format,
                operation_name="formatting video count as numbers"
            )
            
            # Format Last Submitted Timestamp column alignment
            if role == "Annotator":
                timestamp_col = "G"  # Column G for annotators
            else:  # Reviewer
                timestamp_col = "F"  # Column F for reviewers
            
            timestamp_format = {
                "verticalAlignment": "BOTTOM",
                "horizontalAlignment": "LEFT"
                # NOTE: No background color here - will be set by alternating colors
            }
            self._api_call_with_retry(
                worksheet.format, f"{timestamp_col}3:{timestamp_col}{2+num_data_rows}", timestamp_format,
                operation_name="formatting timestamp column alignment"
            )
            
            # Format feedback column with text wrapping (if feedback tab)
            if not include_payment:  # Feedback tab
                # Calculate feedback column based on role
                if role == "Annotator":
                    feedback_col = "H"  # Column H for annotators
                else:  # Reviewer  
                    feedback_col = "G"  # Column G for reviewers
                
                feedback_format = {
                    "wrapStrategy": "WRAP",  # Wrap text for long feedback
                    "verticalAlignment": "TOP",
                    "textFormat": {"fontSize": 9}  # Smaller font to fit more text
                    # NOTE: No background color here - will be set by alternating colors
                }
                self._api_call_with_retry(
                    worksheet.format, f"{feedback_col}3:{feedback_col}{2+num_data_rows}", feedback_format,
                    operation_name="formatting feedback column"
                )
            
        except Exception as e:
            print(f"      ⚠️  Data formatting failed: {e}")

    def _col_num_to_letter(self, col_num):
        """Convert column number to Excel-style letter"""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + ord('A')) + result
            col_num //= 26
        return result
    
    def _create_annotator_headers(self, worksheet, task_names: List[str], include_payment: bool):
        """Create multi-row headers for annotator sheets with proper merged cells"""
        print(f"      Creating annotator headers with merged cells...")
        
        # Helper function to convert column number to Excel-style letter
        def col_num_to_letter(col_num):
            result = ""
            while col_num > 0:
                col_num -= 1
                result = chr(col_num % 26 + ord('A')) + result
                col_num //= 26
            return result
        
        # Clear only the header area (rows 1-2) to avoid clearing data
        try:
            # Calculate total columns needed
            base_cols = 7  # Json Sheet Name, Video Count, Completion Ratio (2), Reviewed Ratio (2), Last Submitted
            payment_cols = 3 if include_payment else 1  # Payment cols or Feedback col
            task_cols = len(task_names) * 6  # 6 columns per task for annotators
            total_cols = base_cols + payment_cols + task_cols
            
            end_col = self._col_num_to_letter(min(total_cols, 50))
            self._api_call_with_retry(worksheet.batch_clear, [f'A1:{end_col}2'], 
                                    operation_name="clearing header area")
        except Exception as e:
            print(f"      ⚠️  Could not clear header area: {e}")
        
        # Row 1 headers (main categories)
        row1 = ["Json Sheet Name", "Video Count", "Completion Ratio", "", "Reviewed Ratio", "", "Last Submitted Timestamp"]
        
        if include_payment:
            row1.extend(["Payment Timestamp", "Base Salary", "Bonus Salary"])
        else:
            row1.append("Feedback to Annotator")
        
        # Add task headers (each task spans 6 columns)
        for task_name in task_names:
            short_name = self.config_names_to_short_names.get(task_name, task_name)
            row1.extend([short_name, "", "", "", "", ""])
        
        # Row 2 headers (sub-categories) - FIXED ALIGNMENT
        row2 = ["", "", "All Users", "Current User", "All Users", "Current User", ""]
        
        if include_payment:
            row2.extend(["", "", ""])
        else:
            row2.append("")
        
        # Add task sub-headers (6 per task)
        for _ in task_names:
            row2.extend(["Accuracy", "Completion", "Reviewed", "Completed", "Reviewed", "Rejected"])
        
        # Update headers
        end_col = col_num_to_letter(len(row1))
        self._api_call_with_retry(worksheet.update, f'A1:{end_col}2', [row1, row2], 
                                operation_name="updating headers")
        
        # Apply merged cells for better formatting
        try:
            # Merge Json Sheet Name (A1:A2)
            self._api_call_with_retry(worksheet.merge_cells, 'A1:A2', 
                                    operation_name="merging Json Sheet Name")
            
            # Merge Video Count (B1:B2)
            self._api_call_with_retry(worksheet.merge_cells, 'B1:B2', 
                                    operation_name="merging Video Count")
            
            # Merge Completion Ratio (C1:D1)
            self._api_call_with_retry(worksheet.merge_cells, 'C1:D1', 
                                    operation_name="merging Completion Ratio")
            
            # Merge Reviewed Ratio (E1:F1)
            self._api_call_with_retry(worksheet.merge_cells, 'E1:F1', 
                                    operation_name="merging Reviewed Ratio")
            
            # Merge Last Submitted Timestamp (G1:G2)
            self._api_call_with_retry(worksheet.merge_cells, 'G1:G2', 
                                    operation_name="merging Last Submitted")
            
            # Merge payment/feedback columns
            start_col = 8  # Column H
            if include_payment:
                for i, col_name in enumerate(["Payment Timestamp", "Base Salary", "Bonus Salary"]):
                    col_letter = col_num_to_letter(start_col + i)
                    self._api_call_with_retry(worksheet.merge_cells, f'{col_letter}1:{col_letter}2', 
                                            operation_name=f"merging {col_name}")
                start_col += 3
            else:
                col_letter = col_num_to_letter(start_col)
                self._api_call_with_retry(worksheet.merge_cells, f'{col_letter}1:{col_letter}2', 
                                        operation_name="merging Feedback")
                start_col += 1
            
            # Merge task headers (each task spans 6 columns)
            for i, task_name in enumerate(task_names):
                start_task_col = start_col + (i * 6)
                end_task_col = start_task_col + 5
                start_letter = col_num_to_letter(start_task_col)
                end_letter = col_num_to_letter(end_task_col)
                short_name = self.config_names_to_short_names.get(task_name, task_name)
                self._api_call_with_retry(worksheet.merge_cells, f'{start_letter}1:{end_letter}1', 
                                        operation_name=f"merging task {short_name}")
                
                # Center the task header text
                self._api_call_with_retry(worksheet.format, f'{start_letter}1:{end_letter}1', 
                                        {"horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"},
                                        operation_name=f"centering task {short_name}")
            
            print(f"      ✅ Applied merged cells for professional header layout")
        except Exception as e:
            print(f"      ⚠️  Could not apply merged cells (formatting will be basic): {e}")
    
    def _create_reviewer_headers(self, worksheet, task_names: List[str], include_payment: bool):
        """Create multi-row headers for reviewer sheets with proper merged cells"""
        print(f"      Creating reviewer headers with merged cells...")
        
        # Helper function to convert column number to Excel-style letter
        def col_num_to_letter(col_num):
            result = ""
            while col_num > 0:
                col_num -= 1
                result = chr(col_num % 26 + ord('A')) + result
                col_num //= 26
            return result
        
        # Row 1 headers (main categories)
        row1 = ["Json Sheet Name", "Video Count", "Completion Ratio", "Reviewed Ratio", "", "Last Submitted Timestamp"]
        
        if include_payment:
            row1.extend(["Payment Timestamp", "Base Salary", "Bonus Salary"])
        else:
            row1.append("Feedback to Reviewer")
        
        # Add task headers (each task spans 2 columns for reviewers)
        for task_name in task_names:
            short_name = self.config_names_to_short_names.get(task_name, task_name)
            row1.extend([short_name, ""])
        
        # Row 2 headers (sub-categories) - FIXED ALIGNMENT FOR REVIEWERS
        row2 = ["", "", "All Users", "All Users", "Current User", ""]
        
        if include_payment:
            row2.extend(["", "", ""])
        else:
            row2.append("")
        
        # Add task sub-headers (2 per task for reviewers)
        for _ in task_names:
            row2.extend(["Completion", "Completed"])
        
        # Update headers
        end_col = col_num_to_letter(len(row1))
        self._api_call_with_retry(worksheet.update, f'A1:{end_col}2', [row1, row2], 
                                operation_name="updating headers")
        
        # Apply merged cells for better formatting
        try:
            # Merge Json Sheet Name (A1:A2)
            self._api_call_with_retry(worksheet.merge_cells, 'A1:A2', 
                                    operation_name="merging Json Sheet Name")
            
            # Merge Video Count (B1:B2)
            self._api_call_with_retry(worksheet.merge_cells, 'B1:B2', 
                                    operation_name="merging Video Count")
            
            # Merge Completion Ratio (C1:C2)
            self._api_call_with_retry(worksheet.merge_cells, 'C1:C2', 
                                    operation_name="merging Completion Ratio")
            
            # Merge Reviewed Ratio (D1:E1)
            self._api_call_with_retry(worksheet.merge_cells, 'D1:E1', 
                                    operation_name="merging Reviewed Ratio")
            
            # Merge Last Submitted Timestamp (F1:F2)
            self._api_call_with_retry(worksheet.merge_cells, 'F1:F2', 
                                    operation_name="merging Last Submitted")
            
            # Merge payment/feedback columns
            start_col = 7  # Column G
            if include_payment:
                for i, col_name in enumerate(["Payment Timestamp", "Base Salary", "Bonus Salary"]):
                    col_letter = col_num_to_letter(start_col + i)
                    self._api_call_with_retry(worksheet.merge_cells, f'{col_letter}1:{col_letter}2', 
                                            operation_name=f"merging {col_name}")
                start_col += 3
            else:
                col_letter = col_num_to_letter(start_col)
                self._api_call_with_retry(worksheet.merge_cells, f'{col_letter}1:{col_letter}2', 
                                        operation_name="merging Feedback")
                start_col += 1
            
            # Merge task headers (each task spans 2 columns for reviewers)
            for i, task_name in enumerate(task_names):
                start_task_col = start_col + (i * 2)
                end_task_col = start_task_col + 1
                start_letter = col_num_to_letter(start_task_col)
                end_letter = col_num_to_letter(end_task_col)
                short_name = self.config_names_to_short_names.get(task_name, task_name)
                self._api_call_with_retry(worksheet.merge_cells, f'{start_letter}1:{end_letter}1', 
                                        operation_name=f"merging task {short_name}")
                
                # Center the task header text
                self._api_call_with_retry(worksheet.format, f'{start_letter}1:{end_letter}1', 
                                        {"horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"},
                                        operation_name=f"centering task {short_name}")
            
            print(f"      ✅ Applied merged cells for professional header layout")
        except Exception as e:
            print(f"      ⚠️  Could not apply merged cells (formatting will be basic): {e}")
    
    def _create_data_row(self, video_file: str, file_stats: Dict, user_stats: Dict, 
                        task_names: List[str], role: str, include_payment: bool) -> List:
        """Create a data row for a video file with per-video task statistics"""
        # Calculate video count for this file - get from total_possible divided by number of tasks
        total_possible = file_stats.get('total_possible', 0)
        num_tasks = len(task_names) if task_names else 1
        video_count = total_possible // num_tasks if num_tasks > 0 else 1
        
        # Ensure video_count is stored as an integer, not a float or string
        video_count = int(video_count) if video_count else 0
        
        row = [video_file, video_count]
        
        # Add completion and reviewed ratios
        total_possible = file_stats['total_possible']
        completed_all = file_stats['completed_all_users']
        reviewed_all = file_stats['reviewed_all_users']
        
        if role == "Annotator":
            completed_current = file_stats['completed_current_user']
            reviewed_current = file_stats['reviewed_current_user_work']
            
            completion_ratio_all = completed_all / total_possible if total_possible > 0 else 0
            completion_ratio_current = completed_current / total_possible if total_possible > 0 else 0
            reviewed_ratio_all = reviewed_all / completed_all if completed_all > 0 else 0
            reviewed_ratio_current = reviewed_current / completed_current if completed_current > 0 else 0
            
            row.extend([
                f"{completion_ratio_all:.0%}",      # NO decimals
                f"{completion_ratio_current:.0%}",  # NO decimals
                f"{reviewed_ratio_all:.0%}",        # NO decimals  
                f"{reviewed_ratio_current:.0%}"     # NO decimals
            ])
            
            # Last submitted timestamp (annotation timestamp)
            timestamp = file_stats.get('last_annotation_timestamp', '')
        else:  # Reviewer
            reviewed_current = file_stats['reviewed_by_current_user']
            
            completion_ratio_all = completed_all / total_possible if total_possible > 0 else 0
            reviewed_ratio_all = reviewed_all / completed_all if completed_all > 0 else 0
            reviewed_ratio_current = reviewed_current / completed_all if completed_all > 0 else 0
            
            row.extend([
                f"{completion_ratio_all:.0%}",      # NO decimals
                f"{reviewed_ratio_all:.0%}",        # NO decimals
                f"{reviewed_ratio_current:.0%}"     # NO decimals
            ])
            
            # Last submitted timestamp (review timestamp)
            timestamp = file_stats.get('last_review_timestamp', '')
        
        # Format timestamp
        formatted_timestamp = self._format_timestamp(timestamp)
        row.append(formatted_timestamp)
        
        # Add placeholders for manual columns
        if include_payment:
            row.extend(['', '', ''])  # Payment Timestamp, Base Salary, Bonus Salary
        else:
            row.append('')  # Feedback to Annotator
        
        # Add per-task statistics - THIS IS THE KEY FIX
        # Use per-video-file task statistics instead of aggregated user statistics
        for task_name in task_names:
            # Get task stats for this specific video file, not aggregated stats
            task_stats = file_stats.get('per_task_stats', {}).get(task_name, {
                'completed': 0, 'reviewed': 0, 'rejected': 0, 'total': 0
            })
            
            if role == "Annotator":
                # Calculate task-specific ratios for this video file only
                accuracy = ((task_stats['reviewed'] - task_stats['rejected']) / task_stats['reviewed'] 
                           if task_stats['reviewed'] > 0 else 0)
                completion_ratio = task_stats['completed'] / task_stats['total'] if task_stats['total'] > 0 else 0
                reviewed_ratio = task_stats['reviewed'] / task_stats['completed'] if task_stats['completed'] > 0 else 0
                
                row.extend([
                    f"{accuracy:.0%}",           # NO decimals
                    f"{completion_ratio:.0%}",   # NO decimals  
                    f"{reviewed_ratio:.0%}",     # NO decimals
                    task_stats['completed'],
                    task_stats['reviewed'],
                    task_stats['rejected']
                ])
            else:  # Reviewer
                completion_ratio = task_stats['reviewed'] / task_stats['total'] if task_stats['total'] > 0 else 0
                row.extend([
                    f"{completion_ratio:.0%}",   # NO decimals
                    task_stats['reviewed']
                ])
        
        return row
    
    def _format_timestamp(self, timestamp: str) -> str:
        """Format timestamp to readable format"""
        if not timestamp:
            return ''
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return timestamp


def main():
    """Main function with config support"""
    parser = argparse.ArgumentParser(description="Export caption statistics to Google Sheets")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument("--master-sheet-id", type=str, required=True,
                       help="Google Sheet ID for the master sheet (from the URL)")
    parser.add_argument("--skip-individual", action="store_true",
                       help="Skip individual user sheets and only update master sheet")
    parser.add_argument("--resume-from", type=str, 
                       help="Resume from specific user (format: 'User Name Annotator' or 'User Name Reviewer')")
    parser.add_argument("--sheet-prefix", type=str, default="Caption",
                       help="Prefix for all individual sheet names (default: 'Caption')")
    
    args = parser.parse_args()
    
    print("="*60)
    print("GOOGLE SHEETS EXPORT SETUP")
    print("="*60)
    print(f"Config Type: {args.config_type}")
    print(f"Master Sheet ID: {args.master_sheet_id}")
    print(f"Master Sheet URL: https://docs.google.com/spreadsheets/d/{args.master_sheet_id}/edit")
    if args.skip_individual:
        print("Mode: Master sheet only (skipping individual user sheets)")
    elif args.resume_from:
        print(f"Mode: Resume from user '{args.resume_from}'")
    else:
        print("Mode: Full export (master sheet + individual user sheets)")
    print("="*60)
    
    # Get configuration
    app_config = get_config(args.config_type)
    
    # Setup paths
    credentials_file = Path("caption/credentials.json")
    folder_path = Path("caption")
    root_path = Path(".")
    
    # Verify credentials file exists
    if not credentials_file.exists():
        print(f"❌ Error: Credentials file not found: {credentials_file}")
        print(f"💡 Please download your Google OAuth credentials and save as 'caption/credentials.json'")
        return
    
    # Create exporter and run
    exporter = GoogleSheetExporter(str(credentials_file), folder_path, root_path)
    
    # Add resume and skip options to the export method
    exporter.export_all_sheets(
        configs_file=app_config.configs_file,
        video_urls_files=app_config.video_urls_files,
        output_dir=app_config.output_dir,
        master_sheet_id=args.master_sheet_id,
        skip_individual=args.skip_individual,
        resume_from=args.resume_from,
        sheet_prefix=args.sheet_prefix
    )
    
    print(f"Export completed for config type: {args.config_type}")
    
    print("\n" + "="*60)
    print("📋 DATA PRESERVATION SUMMARY")
    print("="*60)
    print("✅ PRESERVED (Never Overwritten):")
    print("   • Payment Timestamp")
    print("   • Base Salary") 
    print("   • Bonus Salary")
    print("   • Feedback to Annotator (100-word feedback)")
    print("\n🔄 AUTOMATICALLY UPDATED:")
    print("   • Json Sheet Name (row identifier)")
    print("   • Completion Ratios")
    print("   • Reviewed Ratios") 
    print("   • Last Submitted Timestamps")
    print("   • All task statistics (Accuracy, Completed counts, etc.)")
    print("\n🔐 PERMISSION MANAGEMENT:")
    print("   • Editor access: zhiqiulin98@gmail.com, ttiffanyyllingg@gmail.com,")
    print("     isaacli@andrew.cmu.edu, huangyuhan1130@gmail.com, edzee1701@gmail.com")
    print("   • Others: Commenter access only")
    print("   • Applied to master sheet and all individual user sheets")
    print("\n🔍 HOW IT WORKS:")
    print("   1. Read existing manual data by Json Sheet Name")
    print("   2. Calculate new automatic statistics") 
    print("   3. Merge: automatic data + preserved manual data")
    print("   4. Update sheet with combined data")
    print("   5. Apply beautiful formatting")
    print("   6. Manage sheet permissions automatically")
    print("="*60)
    
    if args.skip_individual:
        print("\n💡 Next time, remove --skip-individual to export individual user sheets")
    elif args.resume_from:
        print(f"\n💡 Resumed from: {args.resume_from}")
    else:
        print("\n💡 Usage tips:")
        print("   - If rate limited, resume with: --resume-from 'Last Failed User Role'")
        print("   - To update only master sheet: --skip-individual")
        print("   - Individual user sheet URLs are now linked in the master sheet")
        print("   - Manual data is preserved across exports!")
        print("   - Sheets now have professional formatting with colors and proper sizing")


if __name__ == "__main__":
    main()