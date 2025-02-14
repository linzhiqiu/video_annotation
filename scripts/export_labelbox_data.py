#!/usr/bin/env python3

import os
import yaml
import json
import logging
import requests
import labelbox as lb
from datetime import datetime
from typing import Dict, Any, List
import shutil

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config(config_path: str) -> Dict[str, Any]:
    """Load export configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_export_params(config: Dict[str, Any]) -> Dict[str, bool]:
    """Get export parameters from config or use defaults."""
    defaults = {
        "attachments": False,
        "metadata_fields": False,
        "data_row_details": True,
        "project_details": False,
        "label_details": True,
        "performance_details": True,
        "interpolated_frames": False,
        "embeddings": False
    }
    
    # If export_params specified in config, use those
    if 'export_params' in config:
        return config['export_params']
    return defaults

def get_export_filters(config: Dict[str, Any]) -> Dict[str, Any]:
    """Get export filters from config."""
    filters = {}
    
    # Add any additional filters from config if they exist and are not None
    config_filters = config.get('filters', {})
    if config_filters is not None:
        filters.update(config_filters)
        
    return filters

def get_safe_filename(name: str) -> str:
    """Convert project name to a safe filename."""
    # Replace any non-alphanumeric characters with underscores
    safe_name = ''.join(c if c.isalnum() else '_' for c in name)
    # Remove multiple consecutive underscores
    safe_name = '_'.join(filter(None, safe_name.split('_')))
    return safe_name

def export_project_data(client: lb.Client, project_id: str, output_dir: str, config: Dict[str, Any]):
    """Export data from a single project."""
    try:
        # Get project
        project = client.get_project(project_id)
        project_name = project.name
        logging.info(f"Exporting project: {project_name} ({project_id})")
        
        # Create project output directory
        project_dir = os.path.join(output_dir, 'ndjson')
        issues_dir = os.path.join(output_dir, 'issues_ndjson')
        
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(issues_dir, exist_ok=True)
        
        # Export main data
        export_task = project.export(
            params=get_export_params(config),
            filters=get_export_filters(config)
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
        output_file = os.path.join(project_dir, f"{safe_project_name}_{project_id}.ndjson")
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
        
        # Export open issues only
        issues_url = project.export_issues(status="Open")
        if not issues_url:
            logging.warning(f"No issues URL returned for project {project_id}")
            return
            
        issues_response = requests.get(issues_url)
        if issues_response.status_code != 200:
            logging.error(f"Failed to fetch issues: {issues_response.status_code}")
            return
            
        issues = issues_response.json()
        if issues:  # Only save if we have issues
            issues_file = os.path.join(issues_dir, f"{safe_project_name}_{project_id}_issues.json")
            
            with open(issues_file, 'w') as f:
                json.dump(issues, f, indent=2)
                
            logging.info(f"Exported {len(issues)} open issues to {issues_file}")
        else:
            logging.info(f"No open issues found for project {project_id}")
        
    except Exception as e:
        logging.error(f"Error exporting project {project_id}: {str(e)}")
        # Log the full traceback for debugging
        import traceback
        logging.error(traceback.format_exc())

def main():
    """Main entry point for the script."""
    setup_logging()
    
    # Load config
    config = load_config('configs/labelbox_export.yaml')
    
    # Get output directory
    output_dir = config['output_dir']
    
    # If overwrite is enabled, remove existing directories at the start
    if config.get('overwrite_exports', False):
        project_dir = os.path.join(output_dir, 'ndjson')
        issues_dir = os.path.join(output_dir, 'issues_ndjson')
        
        if os.path.exists(project_dir):
            logging.info(f"Removing existing project directory: {project_dir}")
            shutil.rmtree(project_dir)
        if os.path.exists(issues_dir):
            logging.info(f"Removing existing issues directory: {issues_dir}")
            shutil.rmtree(issues_dir)
    
    # Create client
    client = lb.Client(api_key=config['api_key'])
    
    # Export each project
    for project_id in config['project_ids']:
        export_project_data(client, project_id, output_dir, config)
        
if __name__ == '__main__':
    main() 