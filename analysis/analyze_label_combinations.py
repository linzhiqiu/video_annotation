#!/usr/bin/env python3

import os
import sys
import logging
import json
from typing import List, Dict, Set, Any
from itertools import combinations

# Add parent directory to Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_ndjson import process_ndjson_files
from label import Label
from labels_list_compoundmotionspeedshakiness import LABELS_TO_ANALYZE

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_label_file_path(label_path: str) -> str:
    """Convert a label path to its corresponding JSON file path."""
    # Convert path like 'cam_setup/video_speed/time_lapse' to 'labels/cam_setup/video_speed/time_lapse.json'
    return os.path.join('labels', f"{label_path}.json")

def load_labels(label_paths: List[str]) -> Dict[str, Label]:
    """Load label objects from their paths."""
    labels = {}
    for path in label_paths:
        try:
            json_path = get_label_file_path(path)
            if not os.path.exists(json_path):
                logging.error(f"Label file not found: {json_path}")
                continue
                
            label = Label.from_json(json_path)
            labels[path] = label
            logging.info(f"Loaded label: {path}")
        except Exception as e:
            logging.error(f"Error loading label {path}: {str(e)}")
    return labels

def analyze_label_pair(label1: Label, label2: Label, videos: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a pair of labels and return statistics."""
    stats = {
        'both_positive': 0,
        'label1_positive': 0,
        'label2_positive': 0,
        'both_negative': 0,
        'uncategorized': 0
    }
    
    for video_name, video in videos.items():
        try:
            # Check label1
            is_pos1 = label1.pos_rule(video)
            is_neg1 = label1.neg_rule(video)
            
            # Check label2
            is_pos2 = label2.pos_rule(video)
            is_neg2 = label2.neg_rule(video)
            
            # Update statistics
            if is_pos1 and is_pos2:
                stats['both_positive'] += 1
            elif is_pos1:
                stats['label1_positive'] += 1
            elif is_pos2:
                stats['label2_positive'] += 1
            elif is_neg1 and is_neg2:
                stats['both_negative'] += 1
            else:
                stats['uncategorized'] += 1
                
        except Exception as e:
            logging.debug(f"Error analyzing video {video_name}: {str(e)}")
            stats['uncategorized'] += 1
    
    return stats

def analyze_combinations(videos: Dict[str, Any], labels: Dict[str, Label]) -> List[Dict[str, Any]]:
    """Analyze all possible combinations of different labels."""
    results = []
    
    # Generate all possible combinations of 2 different labels
    label_items = list(labels.items())
    total_combinations = len(label_items) * (len(label_items) - 1) // 2
    processed_combinations = 0
    
    for i, (path1, label1) in enumerate(label_items):
        for path2, label2 in label_items[i+1:]:  # Start from i+1 to avoid self-combinations
            # Analyze the label pair
            stats = analyze_label_pair(label1, label2, videos)
            
            # Store results
            result = {
                'label1': path1,
                'label2': path2,
                'stats': stats
            }
            results.append(result)
            
            # Update progress
            processed_combinations += 1
            if processed_combinations % 100 == 0:
                logging.info(f"Processed {processed_combinations}/{total_combinations} combinations")
    
    # Sort results by number of videos positive for both labels
    results.sort(key=lambda x: x['stats']['both_positive'], reverse=True)
    return results

def save_results(results: List[Dict[str, Any]], output_file: str, total_videos: int):
    """Save analysis results to a text file."""
    with open(output_file, 'w') as f:
        f.write("Label Combination Analysis Results\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Videos Analyzed: {total_videos}\n\n")
        
        for i, result in enumerate(results, 1):
            label1_name = result['label1'].split('/')[-1]
            label2_name = result['label2'].split('/')[-1]
            stats = result['stats']
            
            f.write(f"\n{i}. Label Combination:\n")
            f.write(f"   Label 1: {result['label1']}\n")
            f.write(f"   Label 2: {result['label2']}\n")
            f.write(f"   Statistics:\n")
            f.write(f"   - Both Positive: {stats['both_positive']} ({stats['both_positive']/total_videos*100:.1f}%)\n")
            f.write(f"   - Only Label 1 Positive: {stats['label1_positive']} ({stats['label1_positive']/total_videos*100:.1f}%)\n")
            f.write(f"   - Only Label 2 Positive: {stats['label2_positive']} ({stats['label2_positive']/total_videos*100:.1f}%)\n")
            f.write(f"   - Both Negative: {stats['both_negative']} ({stats['both_negative']/total_videos*100:.1f}%)\n")
            f.write(f"   - Uncategorized: {stats['uncategorized']} ({stats['uncategorized']/total_videos*100:.1f}%)\n")
            f.write("-" * 80 + "\n")

def main():
    """Main function to analyze label combinations."""
    setup_logging()
    
    # Load videos from NDJSON files
    logging.info("Processing NDJSON files...")
    all_videos = process_ndjson_files('exports/ndjson', 'exports/issues_ndjson')
    logging.info(f"Loaded {len(all_videos)} total videos")
    
    # Load video names from donesection.json
    logging.info("Loading video names from donesection.json...")
    try:
        with open('donevideos/donesection.json', 'r') as f:
            video_names = json.load(f)
        if not isinstance(video_names, list):
            raise ValueError("donesection.json must contain a JSON array of strings")
        if not all(isinstance(name, str) for name in video_names):
            raise ValueError("All entries in donesection.json must be strings")
    except Exception as e:
        logging.error(f"Error loading donesection.json: {str(e)}")
        return
        
    # Filter videos to only include those in donesection.json
    videos = {name: video for name, video in all_videos.items() if name in video_names}
    total_videos = len(videos)
    logging.info(f"Filtered to {total_videos} videos from donesection.json")
    
    # Load labels
    logging.info("Loading labels...")
    labels = load_labels(LABELS_TO_ANALYZE)
    if not labels:
        logging.error("No labels could be loaded. Exiting.")
        return
    
    # Analyze combinations
    logging.info("Analyzing label combinations...")
    results = analyze_combinations(videos, labels)
    
    # Create output directory if it doesn't exist
    os.makedirs('analysis/results', exist_ok=True)
    
    # Save results to file
    output_file = 'analysis/results/label_combinations_analysis_compoundmotionspeedshakiness.txt'
    save_results(results, output_file, total_videos)
    logging.info(f"Results saved to {output_file}")

if __name__ == '__main__':
    main()