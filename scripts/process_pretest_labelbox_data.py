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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

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

def generate_pdf(html_content: str, output_path: str):
    """Generate PDF from HTML content using Selenium and Chrome."""
    driver = None
    temp_dir = None
    try:
        driver, temp_dir = setup_chrome_driver()
        
        # Convert HTML content to a data URL
        html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        data_url = f'data:text/html;base64,{html_base64}'
        
        # Load the HTML content directly using the data URL
        driver.get(data_url)
        
        # Wait for page to load completely
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        
        # Additional wait for any dynamic content
        time.sleep(2)
        
        # Print to PDF
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "marginTop": 0.4,
            "marginBottom": 0.4,
            "marginLeft": 0.4,
            "marginRight": 0.4,
            "paperWidth": 8.27,  # A4 width in inches
            "paperHeight": 11.7,  # A4 height in inches
        })
        
        # Save the PDF using proper base64 decoding
        pdf_data = base64.b64decode(pdf['data'])
        with open(output_path, 'wb') as f:
            f.write(pdf_data)
            
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise
    finally:
        if driver:
            driver.quit()
        # Clean up the temporary directory
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)

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

def prepare_visualization_data(ndjson_data: List[dict], ground_truth_source: dict, target_annotator: str) -> dict:
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
        'questions_metrics': metrics['questions_metrics']
    }

def should_process_ground_truth(ground_truth_path: str, config: dict) -> bool:
    """Check if we should process this ground truth file based on config."""
    target_ground_truth = config.get('pdf_generation', {}).get('target_ground_truth')
    if target_ground_truth is None:
        return True
    return os.path.basename(ground_truth_path) == os.path.basename(target_ground_truth)

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

def main():
    """Main entry point for the script."""
    # Setup Flask templates
    setup_templates()
    
    config = load_config()
    project_ground_truth = get_project_id_to_ground_truth(config)
    
    # Process each test type directory
    base_dir = config['output_dir']
    pdfs_dir = config['pdfs_dir']
    
    # Track new PDFs for the "new" folder
    new_pdfs = []  # List to track all new PDFs generated
    
    # Cache for ground truth data
    ground_truth_cache = {}
    
    # If skip_existing is true, clean up old "new" folder
    if config.get('pdf_generation', {}).get('skip_existing', False):
        new_pdfs_dir = os.path.join(pdfs_dir, 'new')
        if os.path.exists(new_pdfs_dir):
            shutil.rmtree(new_pdfs_dir)
    
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
                    
                    # Create PDF directory structure
                    test_pdf_dir = os.path.join(pdfs_dir, test_type, f"test{test_number}")
                    os.makedirs(test_pdf_dir, exist_ok=True)
                    
                    # Generate PDF filename
                    pdf_filename = f"{labeler.replace('@', '_at_')}_{project_id}.pdf"
                    pdf_path = os.path.join(test_pdf_dir, pdf_filename)
                    
                    # Check if we should generate this PDF
                    if not should_generate_pdf(pdf_path, config):
                        continue
                    
                    try:
                        # Prepare data for this labeler using cached ground truth
                        ground_truth_source['cached_ground_truth'] = ground_truth_cache[project_id]
                        labeler_data = prepare_visualization_data(ndjson_data, ground_truth_source, labeler)
                        
                        logger.info(f"Generating PDF at {pdf_path}")
                        
                        # Generate HTML content
                        html_content = render_template('pretest_report.html', **labeler_data)
                        
                        # Generate PDF directly from HTML content
                        generate_pdf(html_content, pdf_path)
                        logger.info(f"PDF generated at {pdf_path}")
                        
                        # Only track as new if generation was successful
                        if config.get('pdf_generation', {}).get('skip_existing', False):
                            new_pdfs.append({
                                'test_type': test_type,
                                'test_number': test_number,
                                'project_id': project_id,
                                'labeler': labeler,
                                'pdf_path': pdf_path
                            })
                            logger.info(f"New PDF generated - Project: {project_id}, Test: {test_number}, Email: {labeler}")
                    except Exception as e:
                        logger.error(f"Error generating PDF for {labeler} in project {project_id}: {str(e)}")
                        logger.error(f"Full error: {str(e.__class__.__name__)}: {str(e)}")
                        # If PDF generation fails, remove the file if it was partially created
                        if os.path.exists(pdf_path):
                            try:
                                os.remove(pdf_path)
                            except Exception as remove_error:
                                logger.error(f"Error removing failed PDF {pdf_path}: {str(remove_error)}")
                        continue
        
        # After all PDFs are generated, create the "new" folder structure if needed
        if new_pdfs and config.get('pdf_generation', {}).get('skip_existing', False):
            new_pdfs_dir = os.path.join(pdfs_dir, 'new')
            os.makedirs(new_pdfs_dir, exist_ok=True)
            
            # Copy new PDFs to mirrored structure
            for pdf_info in new_pdfs:
                # Create the same folder structure in "new" directory
                new_test_pdf_dir = os.path.join(new_pdfs_dir, pdf_info['test_type'], f"test{pdf_info['test_number']}")
                os.makedirs(new_test_pdf_dir, exist_ok=True)
                
                # Copy the PDF
                pdf_filename = os.path.basename(pdf_info['pdf_path'])
                new_pdf_path = os.path.join(new_test_pdf_dir, pdf_filename)
                shutil.copy2(pdf_info['pdf_path'], new_pdf_path)
            
            # Log summary of new PDFs
            logger.info("\nSummary of new PDFs generated:")
            for pdf_info in new_pdfs:
                logger.info(f"Test Type: {pdf_info['test_type']}, Test Number: {pdf_info['test_number']}, "
                          f"Project: {pdf_info['project_id']}, Email: {pdf_info['labeler']}")

if __name__ == "__main__":
    main() 