#!/usr/bin/env python3

import os
import yaml
import json
import logging
import labelbox as lb
from pathlib import Path
from datetime import datetime
import shutil
from typing import Dict, Any

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config(config_path: str) -> Dict[str, Any]:
    """Load the scoring configuration file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_safe_filename(name: str) -> str:
    """Convert project name to a safe filename."""
    # Replace any non-alphanumeric characters with underscores
    safe_name = ''.join(c if c.isalnum() else '_' for c in name)
    # Remove multiple consecutive underscores
    safe_name = '_'.join(filter(None, safe_name.split('_')))
    return safe_name

def setup_export_directories(base_dir: str, test_types: list):
    """Create export directories for each test type if they don't exist."""
    for test_type in test_types:
        test_dir = os.path.join(base_dir, test_type, 'ndjson')
        Path(test_dir).mkdir(parents=True, exist_ok=True)

def export_project_data(client: lb.Client, project_id: str, test_type: str, output_dir: str, export_params: Dict[str, bool]):
    """Export data from a single project using the Labelbox API."""
    try:
        # Get project
        project = client.get_project(project_id)
        project_name = project.name
        logging.info(f"Exporting project: {project_name} ({project_id})")
        
        # Create project output directory
        project_dir = os.path.join(output_dir, test_type, 'ndjson')
        os.makedirs(project_dir, exist_ok=True)
        
        # Export main data
        export_task = project.export(
            params=export_params,
            filters={"workflow_status": None}  # From scoring_config.yaml
        )
        
        # Wait for export to complete
        export_task.wait_till_done()
        
        # Check for errors first
        if export_task.has_errors():
            error_stream = export_task.get_buffered_stream(stream_type=lb.StreamType.ERRORS)
            if error_stream:
                logging.error("Export errors encountered:")
                error_stream.start(stream_handler=lambda error: logging.error(f"Export error: {error}"))
            raise Exception("Export task had errors")
        
        # Check if we have results
        if not export_task.has_result():
            raise Exception("Export task completed but no results available")
        
        # Get the result stream
        stream = export_task.get_buffered_stream(stream_type=lb.StreamType.RESULT)
        if not stream:
            raise Exception("Export stream is empty")
        
        # Save exported data
        safe_project_name = get_safe_filename(project_name)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(project_dir, f"{safe_project_name}_{project_id}_{timestamp}.ndjson")
        export_count = 0
        
        def json_stream_handler(output):
            nonlocal export_count
            if output and output.json:
                with open(output_file, 'a') as f:
                    f.write(json.dumps(output.json) + '\n')
                export_count += 1
        
        # Process the stream
        stream.start(stream_handler=json_stream_handler)
        
        logging.info(f"Exported {export_count} items to {output_file}")
        logging.info(f"File size: {export_task.get_total_file_size(stream_type=lb.StreamType.RESULT)}")
        logging.info(f"Line count: {export_task.get_total_lines(stream_type=lb.StreamType.RESULT)}")
        
    except Exception as e:
        logging.error(f"Error exporting project {project_id}: {str(e)}")
        # Log the full traceback for debugging
        import traceback
        logging.error(traceback.format_exc())

def main():
    """Main entry point for the script."""
    setup_logging()
    
    # Load configuration
    config = load_config('configs/scoring_config.yaml')
    
    # Initialize Labelbox client
    client = lb.Client(api_key=config['api_key'])
    logging.info("Initialized Labelbox client")
    
    # Setup base export directory
    base_export_dir = config['output_dir']
    logging.info(f"Using export directory: {base_export_dir}")
    
    # Create directories for each test type
    test_types = config['projects'].keys()
    setup_export_directories(base_export_dir, test_types)
    
    # If overwrite is enabled, clean existing directories
    if config.get('overwrite_exports', False):
        for test_type in test_types:
            ndjson_dir = os.path.join(base_export_dir, test_type, 'ndjson')
            if os.path.exists(ndjson_dir):
                logging.info(f"Removing existing directory: {ndjson_dir}")
                shutil.rmtree(ndjson_dir)
                os.makedirs(ndjson_dir)
    
    # Export data for each test type and project
    for test_type, projects in config['projects'].items():
        logging.info(f"\nProcessing {test_type} projects...")
        
        for project in projects:
            project_id = project['id']
            # Ground truth path is optional for export
            ground_truth_path = project.get('ground_truth_path')
            # if ground_truth_path:
            #     logging.info(f"Ground truth path for project {project_id}: {ground_truth_path}")
            
            export_project_data(
                client=client,
                project_id=project_id,
                test_type=test_type,
                output_dir=base_export_dir,
                export_params=config['export_params']
            )

if __name__ == "__main__":
    main() 