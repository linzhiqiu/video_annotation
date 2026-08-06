#!/usr/bin/env python3
"""
Cleanup Script for Individual Google Sheets

This script helps clean up individual user sheets by either:
1. Deleting all individual sheets (leaves master sheet untouched)
2. Clearing content from individual sheets but keeping the structure
3. Removing only specific sheets

Use this before running the main export to clean up any formatting issues.
"""

import os
import gspread
import argparse
import time
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from caption.core.auth import load_annotators_from_files, APPROVED_REVIEWERS


class SheetsCleanup:
    """Cleanup utility for Google Sheets"""
    
    # OAuth 2.0 scopes required for Google Sheets and Drive access
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_file: str):
        """Initialize the cleanup utility"""
        self._setup_google_auth(credentials_file)
        
        # Load annotators and reviewers
        self.annotators = load_annotators_from_files()
        self.approved_reviewers = APPROVED_REVIEWERS
    
    def _setup_google_auth(self, credentials_file: str):
        """Setup Google authentication using OAuth 2.0"""
        creds = None
        token_file = 'caption/token_export.json'
        
        # Load existing export token if available
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
                if not creds.has_scopes(self.SCOPES):
                    print("🔄 Token has insufficient scopes, deleting...")
                    os.remove(token_file)
                    creds = None
            except:
                print("🔄 Invalid token file, deleting...")
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
                    creds = None
            
            if not creds:
                # Manual OAuth flow for environments without browser
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES, redirect_uri='http://localhost:8080')
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print('='*60)
                print('GOOGLE SHEETS CLEANUP AUTHORIZATION')
                print('='*60)
                print('1. Go to this URL in your browser:')
                print(auth_url)
                print('\n2. Authorize the application')
                print('3. Copy the authorization code from the failed URL')
                print('='*60)
                
                auth_code = input('\nEnter the authorization code: ').strip()
                if not auth_code:
                    raise Exception('No authorization code provided')
                
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                
                # Save the credentials for the next run
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                    print(f"✅ Credentials saved to {token_file}")
        
        # Authorize gspread client
        self.client = gspread.authorize(creds)
        print("✅ Google Sheets client authorized")
    
    def get_all_user_sheet_names(self):
        """Get list of all potential user sheet names"""
        sheet_names = []
        
        # Add annotator sheets
        for user_name in self.annotators.keys():
            sheet_names.append(f"{user_name} Annotator")
        
        # Add reviewer sheets
        for user_name in self.approved_reviewers:
            sheet_names.append(f"{user_name} Reviewer")
        
        return sheet_names
    
    def list_existing_sheets(self):
        """List all existing individual user sheets"""
        print("🔍 Scanning for existing individual user sheets...")
        sheet_names = self.get_all_user_sheet_names()
        existing_sheets = []
        
        for sheet_name in sheet_names:
            try:
                sheet = self.client.open(sheet_name)
                existing_sheets.append((sheet_name, sheet.id))
                print(f"   ✅ Found: {sheet_name}")
            except gspread.exceptions.SpreadsheetNotFound:
                pass  # Sheet doesn't exist
            except Exception as e:
                print(f"   ⚠️  Error checking {sheet_name}: {e}")
        
        print(f"\n📊 Found {len(existing_sheets)} existing individual user sheets")
        return existing_sheets
    
    def delete_all_individual_sheets(self, confirm: bool = False):
        """Delete all individual user sheets (NOT the master sheet)"""
        existing_sheets = self.list_existing_sheets()
        
        if not existing_sheets:
            print("✅ No individual sheets found to delete")
            return
        
        if not confirm:
            print("\n⚠️  WARNING: This will permanently delete all individual user sheets!")
            print("   (Master sheet will NOT be affected)")
            print(f"   Sheets to delete: {len(existing_sheets)}")
            for sheet_name, _ in existing_sheets:
                print(f"     - {sheet_name}")
            
            response = input("\nAre you sure you want to delete these sheets? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return
        
        print(f"\n🗑️  Deleting {len(existing_sheets)} individual sheets...")
        deleted_count = 0
        
        for sheet_name, sheet_id in existing_sheets:
            try:
                # Open the sheet and delete it
                sheet = self.client.open_by_key(sheet_id)
                self.client.del_spreadsheet(sheet_id)
                print(f"   ✅ Deleted: {sheet_name}")
                deleted_count += 1
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Failed to delete {sheet_name}: {e}")
        
        print(f"\n✅ Successfully deleted {deleted_count}/{len(existing_sheets)} sheets")
    
    def clear_sheet_content(self, sheet_name: str):
        """Clear content from a specific sheet but keep structure"""
        try:
            sheet = self.client.open(sheet_name)
            print(f"   🧹 Clearing content from: {sheet_name}")
            
            # Clear all worksheets in the sheet
            for worksheet in sheet.worksheets():
                try:
                    worksheet.clear()
                    print(f"     ✅ Cleared: {worksheet.title}")
                except Exception as e:
                    print(f"     ❌ Failed to clear {worksheet.title}: {e}")
            
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"   ⚠️  Sheet not found: {sheet_name}")
        except Exception as e:
            print(f"   ❌ Error clearing {sheet_name}: {e}")
    
    def clear_all_individual_sheets(self, confirm: bool = False):
        """Clear content from all individual sheets but keep structure"""
        existing_sheets = self.list_existing_sheets()
        
        if not existing_sheets:
            print("✅ No individual sheets found to clear")
            return
        
        if not confirm:
            print("\n⚠️  WARNING: This will clear all content from individual user sheets!")
            print("   (Sheets will remain but all data will be deleted)")
            print(f"   Sheets to clear: {len(existing_sheets)}")
            for sheet_name, _ in existing_sheets:
                print(f"     - {sheet_name}")
            
            response = input("\nAre you sure you want to clear these sheets? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return
        
        print(f"\n🧹 Clearing content from {len(existing_sheets)} individual sheets...")
        cleared_count = 0
        
        for sheet_name, _ in existing_sheets:
            try:
                self.clear_sheet_content(sheet_name)
                cleared_count += 1
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Failed to clear {sheet_name}: {e}")
        
        print(f"\n✅ Successfully cleared {cleared_count}/{len(existing_sheets)} sheets")
    
    def delete_specific_sheets(self, sheet_names: list, confirm: bool = False):
        """Delete specific sheets by name"""
        existing_sheets = self.list_existing_sheets()
        existing_names = {name: sheet_id for name, sheet_id in existing_sheets}
        
        # Filter to only existing sheets
        sheets_to_delete = []
        for sheet_name in sheet_names:
            if sheet_name in existing_names:
                sheets_to_delete.append((sheet_name, existing_names[sheet_name]))
            else:
                print(f"   ⚠️  Sheet not found: {sheet_name}")
        
        if not sheets_to_delete:
            print("❌ No valid sheets found to delete")
            return
        
        if not confirm:
            print(f"\n⚠️  WARNING: This will delete {len(sheets_to_delete)} sheets:")
            for sheet_name, _ in sheets_to_delete:
                print(f"     - {sheet_name}")
            
            response = input("\nAre you sure you want to delete these sheets? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return
        
        print(f"\n🗑️  Deleting {len(sheets_to_delete)} sheets...")
        deleted_count = 0
        
        for sheet_name, sheet_id in sheets_to_delete:
            try:
                self.client.del_spreadsheet(sheet_id)
                print(f"   ✅ Deleted: {sheet_name}")
                deleted_count += 1
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Failed to delete {sheet_name}: {e}")
        
        print(f"\n✅ Successfully deleted {deleted_count}/{len(sheets_to_delete)} sheets")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Cleanup individual Google Sheets")
    parser.add_argument("--action", type=str, required=True,
                       choices=["list", "delete-all", "clear-all", "delete-specific"],
                       help="Action to perform")
    parser.add_argument("--sheets", type=str, nargs="+",
                       help="Specific sheet names to delete (for delete-specific action)")
    parser.add_argument("--yes", action="store_true",
                       help="Skip confirmation prompts")
    
    args = parser.parse_args()
    
    print("="*60)
    print("GOOGLE SHEETS CLEANUP UTILITY")
    print("="*60)
    
    # Setup paths
    credentials_file = Path("caption/credentials.json")
    
    # Verify credentials file exists
    if not credentials_file.exists():
        print(f"❌ Error: Credentials file not found: {credentials_file}")
        print(f"💡 Please download your Google OAuth credentials and save as 'caption/credentials.json'")
        return
    
    # Create cleanup utility
    cleanup = SheetsCleanup(str(credentials_file))
    
    if args.action == "list":
        cleanup.list_existing_sheets()
    
    elif args.action == "delete-all":
        cleanup.delete_all_individual_sheets(confirm=args.yes)
    
    elif args.action == "clear-all":
        cleanup.clear_all_individual_sheets(confirm=args.yes)
    
    elif args.action == "delete-specific":
        if not args.sheets:
            print("❌ Error: --sheets argument required for delete-specific action")
            return
        cleanup.delete_specific_sheets(args.sheets, confirm=args.yes)
    
    print("="*60)
    print("CLEANUP COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()