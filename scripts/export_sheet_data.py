#!/usr/bin/env python3

import json
import logging
from datetime import datetime
from scripts.sheet_utils import load_all_sheet_data, load_config, save_sheet_data

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'logs/export_sheet_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )

def main():
    """Export sheet data to JSON file."""
    setup_logging()
    
    # Load config
    config = load_config()
    sheets_config = config.get('google_sheets', {})
    
    # Load all sheet data
    logging.info("Loading sheet data...")
    sheet_data = load_all_sheet_data(sheets_config)
    
    # Save sheet data using utility function
    output_file = save_sheet_data(sheet_data)
    logging.info(f"Sheet data saved to {output_file}")
    
    # Print some statistics
    total_videos = len(sheet_data)
    total_projects = sum(len(video_data) for video_data in sheet_data.values())
    logging.info(f"\nStatistics:")
    logging.info(f"Total videos: {total_videos}")
    logging.info(f"Total project entries: {total_projects}")

if __name__ == "__main__":
    main() 