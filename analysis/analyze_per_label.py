#!/usr/bin/env python3

import os
import sys
import logging
import json
from typing import Dict, Any

# Add parent directory to Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_ndjson import process_ndjson_files
from label import Label
from labels_list import LABELS_TO_ANALYZE

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

def analyze_label(label: Label, videos: Dict[str, Any]) -> Dict[str, int]:
    """Analyze a single label and return statistics.
    
    Categories:
    - positive: Videos that satisfy the positive rule
    - negative: Videos that satisfy the negative rule
      - hard_negative: Subset of negative videos that satisfy hard negative rules
      - easy_negative: Subset of negative videos that satisfy easy negative rules
      - other_negative: Negative videos that don't satisfy hard or easy negative rules
    - uncategorized: Videos that don't satisfy either positive or negative rules
    """
    stats = {
        'positive': 0,
        'negative': 0,  # Total negative count
        'hard_negative': 0,  # Subset of negative
        'easy_negative': 0,  # Subset of negative
        'other_negative': 0,  # Negative videos not in hard or easy
        'uncategorized': 0,  # Videos that don't match any category
    }
    
    for video_name, video in videos.items():
        try:
            # First check positive rule
            if label.pos_rule(video):
                stats['positive'] += 1
                continue
                
            # Then check negative rule
            if label.neg_rule(video):
                stats['negative'] += 1
                
                # Check for hard negative subcategories
                is_hard_negative = False
                for rule_name, rule in label.hard_neg_rules.items():
                    if rule(video):
                        stats['hard_negative'] += 1
                        is_hard_negative = True
                        break
                
                # If not hard negative, check for easy negative
                if not is_hard_negative:
                    is_easy_negative = False
                    for rule_name, rule in label.easy_neg_rules.items():
                        if rule(video):
                            stats['easy_negative'] += 1
                            is_easy_negative = True
                            break
                    
                    # If neither hard nor easy negative
                    if not is_easy_negative:
                        stats['other_negative'] += 1
            else:
                # If neither positive nor negative
                stats['uncategorized'] += 1
                    
        except Exception as e:
            logging.debug(f"Error analyzing video {video_name}: {str(e)}")
            # Count errors as uncategorized
            stats['uncategorized'] += 1
    
    # Verify that subcategories sum to total negative count
    negative_subcategories_sum = stats['hard_negative'] + stats['easy_negative'] + stats['other_negative']
    if negative_subcategories_sum != stats['negative']:
        logging.error(f"Negative subcategories sum ({negative_subcategories_sum}) does not match total negative count ({stats['negative']})")
    
    return stats

def save_results(label_stats: Dict[str, Dict[str, int]], output_file: str, total_videos: int):
    """Save per-label analysis results to a text file.
    
    Args:
        label_stats: Dictionary mapping label paths to their statistics
        output_file: Path to save the results
        total_videos: Total number of videos analyzed (should be constant across all labels)
    """
    with open(output_file, 'w') as f:
        f.write("Per-Label Analysis Results\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Videos Analyzed: {total_videos}\n\n")
        f.write("Labels analyzed:\n")
        for label_path in label_stats.keys():
            f.write(f"- {label_path}\n")
        f.write("\n" + "=" * 80 + "\n")
        
        for label_path, stats in label_stats.items():
            label_name = label_path.split('/')[-2:][0]
            
            # Verify that main categories sum to total
            main_categories_sum = stats['positive'] + stats['negative'] + stats['uncategorized']
            if main_categories_sum != total_videos:
                logging.warning(f"Main categories sum mismatch for {label_path}: {main_categories_sum} != {total_videos}")
            
            # Verify that negative subcategories sum to total negative count
            negative_subcategories_sum = stats['hard_negative'] + stats['easy_negative'] + stats['other_negative']
            if negative_subcategories_sum != stats['negative']:
                logging.warning(f"Negative subcategories sum mismatch for {label_path}: {negative_subcategories_sum} != {stats['negative']}")
            
            f.write(f"\nLabel: {label_name}\n")
            f.write(f"Path: {label_path}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Videos: {total_videos}\n")
            f.write(f"Positive: {stats['positive']} ({stats['positive']/total_videos*100:.1f}%)\n")
            f.write(f"Negative: {stats['negative']} ({stats['negative']/total_videos*100:.1f}%)\n")
            f.write(f"  ├─ Hard Negative: {stats['hard_negative']} ({stats['hard_negative']/total_videos*100:.1f}%)\n")
            f.write(f"  ├─ Easy Negative: {stats['easy_negative']} ({stats['easy_negative']/total_videos*100:.1f}%)\n")
            f.write(f"  └─ Other Negative: {stats['other_negative']} ({stats['other_negative']/total_videos*100:.1f}%)\n")
            f.write(f"Uncategorized: {stats['uncategorized']} ({stats['uncategorized']/total_videos*100:.1f}%)\n")
            f.write("=" * 80 + "\n")

def save_sorted_results(label_stats: Dict[str, Dict[str, int]], output_file: str, total_videos: int):
    """Save per-label analysis results to a text file, sorted by number of positive samples.
    
    Args:
        label_stats: Dictionary mapping label paths to their statistics
        output_file: Path to save the results
        total_videos: Total number of videos analyzed
    """
    # Sort labels by positive count in descending order
    sorted_labels = sorted(
        label_stats.items(),
        key=lambda x: x[1]['positive'],
        reverse=True
    )
    
    with open(output_file, 'w') as f:
        f.write("Per-Label Analysis Results (Sorted by Positive Count)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Videos Analyzed: {total_videos}\n\n")
        f.write("Labels sorted by number of positive samples (most to least):\n")
        for label_path, stats in sorted_labels:
            f.write(f"- {label_path}: {stats['positive']} positive samples\n")
        f.write("\n" + "=" * 80 + "\n")
        
        for label_path, stats in sorted_labels:
            label_name = label_path.split('/')[-2:][0]
            
            f.write(f"\nLabel: {label_name}\n")
            f.write(f"Path: {label_path}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Videos: {total_videos}\n")
            f.write(f"Positive: {stats['positive']} ({stats['positive']/total_videos*100:.1f}%)\n")
            f.write(f"Negative: {stats['negative']} ({stats['negative']/total_videos*100:.1f}%)\n")
            f.write(f"  ├─ Hard Negative: {stats['hard_negative']} ({stats['hard_negative']/total_videos*100:.1f}%)\n")
            f.write(f"  ├─ Easy Negative: {stats['easy_negative']} ({stats['easy_negative']/total_videos*100:.1f}%)\n")
            f.write(f"  └─ Other Negative: {stats['other_negative']} ({stats['other_negative']/total_videos*100:.1f}%)\n")
            f.write(f"Uncategorized: {stats['uncategorized']} ({stats['uncategorized']/total_videos*100:.1f}%)\n")
            f.write("=" * 80 + "\n")

def main():
    """Main function to analyze per-label statistics."""
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
    
    # Analyze each label
    label_stats = {}
    total_labels = len(LABELS_TO_ANALYZE)
    
    for i, label_path in enumerate(LABELS_TO_ANALYZE, 1):
        logging.info(f"Processing label {i}/{total_labels}: {label_path}")
        try:
            json_path = get_label_file_path(label_path)
            if not os.path.exists(json_path):
                logging.error(f"Label file not found: {json_path}")
                continue
                
            label = Label.from_json(json_path)
            stats = analyze_label(label, videos)
            
            # Verify that main categories sum to total
            main_categories_sum = stats['positive'] + stats['negative'] + stats['uncategorized']
            if main_categories_sum != total_videos:
                logging.warning(f"Main categories sum mismatch for {label_path}: {main_categories_sum} != {total_videos}")
            
            # Verify that negative subcategories sum to total negative count
            negative_subcategories_sum = stats['hard_negative'] + stats['easy_negative'] + stats['other_negative']
            if negative_subcategories_sum != stats['negative']:
                logging.warning(f"Negative subcategories sum mismatch for {label_path}: {negative_subcategories_sum} != {stats['negative']}")
            
            label_stats[label_path] = stats
        except Exception as e:
            logging.error(f"Error processing label {label_path}: {str(e)}")
    
    # Create output directory if it doesn't exist
    os.makedirs('analysis/results', exist_ok=True)
    
    # Save results to files
    output_file = 'analysis/results/per_label_analysis.txt'
    sorted_output_file = 'analysis/results/per_label_analysis_sorted.txt'
    
    save_results(label_stats, output_file, total_videos)
    save_sorted_results(label_stats, sorted_output_file, total_videos)
    
    logging.info(f"Results saved to {output_file} and {sorted_output_file}")

if __name__ == '__main__':
    main() 