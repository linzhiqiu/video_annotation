#!/usr/bin/env python3
"""
Caption Statistics Analyzer - analyze_caption_stats.py

Analyzes word count and token count statistics for:
- pre_caption (before feedback)
- final_caption (after feedback)
- initial_feedback
- final_feedback

Also analyzes rating scores for pre_caption and final_caption across different caption types.
"""

import json
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
import subprocess
import tempfile
import os
from urllib.parse import urlparse

# Try to import tokenizer for token counting
try:
    from transformers import AutoTokenizer
    TOKENIZER_AVAILABLE = True
    # Initialize a default tokenizer (you can change this to your preferred model)
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
except ImportError:
    TOKENIZER_AVAILABLE = False
    print("Warning: transformers library not available. Token counting will be disabled.")
    print("Install with: pip install transformers")

# Try to import pandas for Excel reading
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    # Will show error only if user tries to use Adobe Excel files


def count_words(text):
    """
    Count words/characters in a text string.
    For Chinese text, counts characters (excluding spaces and punctuation).
    For English text, counts space-separated words.
    """
    if not text or not isinstance(text, str):
        return 0
    
    # Check if text contains Chinese characters
    chinese_char_count = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    
    # If more than 30% of non-space characters are Chinese, treat as Chinese text
    non_space_chars = len([c for c in text if not c.isspace()])
    if non_space_chars > 0 and chinese_char_count / non_space_chars > 0.3:
        # Count Chinese characters (excluding spaces and common punctuation)
        return sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    else:
        # Count English words (space-separated tokens)
        return len(text.split())


def count_tokens(text):
    """
    Count tokens using a tokenizer.
    Returns 0 if tokenizer is not available or text is invalid.
    """
    if not TOKENIZER_AVAILABLE or not text or not isinstance(text, str):
        return 0
    
    try:
        tokens = tokenizer.encode(text)
        return len(tokens)
    except Exception as e:
        print(f"Warning: Error counting tokens: {e}")
        return 0


def get_video_metadata(video_url, cache_dir="/tmp/video_metadata_cache"):
    """
    Extract video metadata (duration, FPS, resolution) from video URL.
    Uses ffprobe to get metadata. Downloads video temporarily if it's a URL.
    
    Returns:
        dict: {"duration": float, "fps": float, "width": int, "height": int}
    """
    try:
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Parse URL to get video filename
        parsed_url = urlparse(video_url)
        video_filename = os.path.basename(parsed_url.path)
        
        # Check if it's a local file or URL
        if video_url.startswith('http://') or video_url.startswith('https://'):
            # Download to temp location
            temp_video_path = os.path.join(cache_dir, video_filename)
            
            # Only download if not already cached
            if not os.path.exists(temp_video_path):
                print(f"  Downloading {video_filename}...")
                import urllib.request
                urllib.request.urlretrieve(video_url, temp_video_path)
            
            video_path = temp_video_path
        else:
            video_path = video_url
        
        # Use ffprobe to get metadata
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=duration,r_frame_rate,width,height:format=duration',
            '-of', 'json',
            video_path
        ]
        
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        
        if probe_result.returncode != 0:
            print(f"Warning: ffprobe failed for {video_filename}: {probe_result.stderr}")
            return None
        
        probe_data = json.loads(probe_result.stdout)
        
        # Extract metadata
        metadata = {}
        
        # Duration (try stream first, then format)
        if 'streams' in probe_data and len(probe_data['streams']) > 0:
            stream = probe_data['streams'][0]
            
            # Duration
            if 'duration' in stream:
                metadata['duration'] = float(stream['duration'])
            elif 'format' in probe_data and 'duration' in probe_data['format']:
                metadata['duration'] = float(probe_data['format']['duration'])
            
            # FPS (from r_frame_rate like "30/1" or "30000/1001")
            if 'r_frame_rate' in stream:
                fps_str = stream['r_frame_rate']
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    metadata['fps'] = float(num) / float(den)
                else:
                    metadata['fps'] = float(fps_str)
            
            # Resolution
            if 'width' in stream and 'height' in stream:
                metadata['width'] = int(stream['width'])
                metadata['height'] = int(stream['height'])
        
        return metadata
        
    except Exception as e:
        print(f"Warning: Error extracting metadata for {video_url}: {e}")
        return None


def analyze_field_statistics(data_dict, field_name, include_tokens=True):
    """
    Analyze word count and token count statistics for a specific field across all caption types.
    
    Args:
        data_dict: Dictionary of {caption_type: [(word_count, token_count, text, video_id)]}
        field_name: Name of the field being analyzed
        include_tokens: Whether to include token count statistics
    
    Returns:
        Dictionary with statistics and examples for each caption type
    """
    stats = {}
    
    for caption_type, data_tuples in data_dict.items():
        if not data_tuples:
            stats[caption_type] = {
                "count": 0,
                "word_mean": 0,
                "word_std": 0,
                "word_min": 0,
                "word_max": 0,
                "token_mean": 0,
                "token_std": 0,
                "token_min": 0,
                "token_max": 0,
                "min_example": None
            }
            continue
        
        # Extract word counts and token counts
        word_counts = [wc for wc, _, _, _ in data_tuples]
        token_counts = [tc for _, tc, _, _ in data_tuples]
        
        # Find minimum example (by word count)
        min_tuple = min(data_tuples, key=lambda x: x[0])
        min_word_count, min_token_count, min_text, min_video_id = min_tuple
        
        stats[caption_type] = {
            "count": len(word_counts),
            "word_mean": float(np.mean(word_counts)),
            "word_std": float(np.std(word_counts)),
            "word_min": int(np.min(word_counts)),
            "word_max": int(np.max(word_counts)),
            "min_example": {
                "word_count": min_word_count,
                "token_count": min_token_count,
                "text": min_text,
                "video_id": min_video_id
            }
        }
        
        if include_tokens and TOKENIZER_AVAILABLE:
            stats[caption_type].update({
                "token_mean": float(np.mean(token_counts)),
                "token_std": float(np.std(token_counts)),
                "token_min": int(np.min(token_counts)),
                "token_max": int(np.max(token_counts)),
            })
    
    return stats


def analyze_rating_statistics(rating_dict):
    """
    Analyze rating score statistics for a specific field across all caption types.
    
    Args:
        rating_dict: Dictionary of {caption_type: [scores]}
    
    Returns:
        Dictionary with rating statistics for each caption type
    """
    stats = {}
    
    for caption_type, scores in rating_dict.items():
        if not scores:
            stats[caption_type] = {
                "count": 0,
                "mean": 0,
                "std": 0,
                "min": 0,
                "max": 0
            }
            continue
        
        stats[caption_type] = {
            "count": len(scores),
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": int(np.min(scores)),
            "max": int(np.max(scores))
        }
    
    return stats


def collect_word_counts_and_ratings(export_file, collect_video_metadata=False, adobe_excel_files=None):
    """
    Collect word counts, token counts, rating scores, video metadata, and crowd captions from an exported caption file.
    
    Args:
        export_file: Path to export JSON file
        collect_video_metadata: Whether to extract video metadata
        adobe_excel_files: List of Adobe Excel files containing crowd captions
    
    Returns:
        Tuple of:
        - Four text field dictionaries (pre_caption, final_caption, initial_feedback, final_feedback)
        - Two rating dictionaries (pre_caption_ratings, final_caption_ratings)
        - Video metadata dictionary (if collect_video_metadata=True)
        - Crowd caption data dictionary (if adobe_excel_files provided)
    """
    # Load the export file
    with open(export_file, 'r') as f:
        video_data_list = json.load(f)
    
    pre_caption_data = defaultdict(list)
    final_caption_data = defaultdict(list)
    initial_feedback_data = defaultdict(list)
    final_feedback_data = defaultdict(list)
    
    pre_caption_ratings = defaultdict(list)
    final_caption_ratings = defaultdict(list)
    
    video_metadata_dict = {}
    
    # Crowd caption data structures
    crowd_caption_data = {
        'subject_background': defaultdict(list),
        'subject_motion': defaultdict(list),
        'camera': defaultdict(list)
    }
    overlap_completed_count = 0
    total_overlap_count = 0
    
    # Load Adobe captions if provided
    adobe_captions_dict = {}
    if adobe_excel_files:
        # Check if pandas is available
        if not PANDAS_AVAILABLE:
            print("Error: pandas is required for reading Adobe Excel files.")
            print("Install with: pip install pandas openpyxl")
            return tuple([pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
                         pre_caption_ratings, final_caption_ratings])
        
        print(f"Loading crowd captions from {len(adobe_excel_files)} Adobe Excel files...")
        
        # Import pandas here (already checked availability above)
        import pandas as pd
        
        # Helper function to extract filename from URL
        def extract_filename_from_url(url):
            """Extract filename from URL or path."""
            if not url:
                return ""
            return url.split('/')[-1]
        
        # Helper function to load captions from Excel
        def load_captions_from_excel(file_path):
            """Load captions from Excel file."""
            df = pd.read_excel(file_path, engine='openpyxl')
            
            result = []
            for _, row in df.iterrows():
                caption_dict = {}
                
                # Map columns flexibly
                for col in df.columns:
                    col_lower = col.lower()
                    
                    if 'content_id' in col_lower:
                        caption_dict['content_id'] = row[col]
                    elif 'stock_url' in col_lower:
                        caption_dict['stock_url'] = row[col]
                    elif 'summary' in col_lower or 'what is the video about' in col_lower:
                        caption_dict['summary_caption'] = row[col]
                    elif ('subject' in col_lower and 'background' in col_lower) or 'who or what is in the image' in col_lower:
                        caption_dict['subject_background_caption'] = row[col]
                    elif ('subject' in col_lower and 'action' in col_lower) or 'what are they doing' in col_lower:
                        caption_dict['subject_motion_caption'] = row[col]
                    elif 'camera' in col_lower or 'how is it captured' in col_lower:
                        caption_dict['camera_caption'] = row[col]
                
                result.append(caption_dict)
            
            return result
        
        # Load all Excel files
        for excel_file in adobe_excel_files:
            captions = load_captions_from_excel(excel_file)
            for caption in captions:
                if 'stock_url' in caption:
                    filename = extract_filename_from_url(caption['stock_url'])
                    adobe_captions_dict[filename] = caption
        
        print(f"Loaded crowd captions for {len(adobe_captions_dict)} videos")
    
    # Process each video
    total_videos = len(video_data_list)
    for idx, video_data in enumerate(video_data_list, 1):
        video_id = video_data.get("video_id", "unknown")
        video_url = video_data.get("video_url", "")
        captions = video_data.get("captions", {})
        
        # Check if this video has completed captions (not "not_completed")
        has_completed_task = any(
            task_data.get("status") != "not_completed" 
            for task_data in captions.values()
        )
        
        # Extract filename from video_url for Adobe lookup
        from urllib.parse import urlparse
        video_filename = os.path.basename(urlparse(video_url).path)
        
        # Check if this video is in the overlap (has Adobe crowd captions)
        adobe_caption = adobe_captions_dict.get(video_filename)
        is_overlap = adobe_caption is not None
        
        if is_overlap:
            total_overlap_count += 1
            if has_completed_task:
                overlap_completed_count += 1
            
            # Collect crowd caption data
            if 'subject_background_caption' in adobe_caption:
                text = adobe_caption['subject_background_caption']
                if text and isinstance(text, str):
                    word_count = count_words(text)
                    token_count = count_tokens(text)
                    crowd_caption_data['subject_background']['all'].append((word_count, token_count, text, video_id))
            
            if 'subject_motion_caption' in adobe_caption:
                text = adobe_caption['subject_motion_caption']
                if text and isinstance(text, str):
                    word_count = count_words(text)
                    token_count = count_tokens(text)
                    crowd_caption_data['subject_motion']['all'].append((word_count, token_count, text, video_id))
            
            if 'camera_caption' in adobe_caption:
                text = adobe_caption['camera_caption']
                if text and isinstance(text, str):
                    word_count = count_words(text)
                    token_count = count_tokens(text)
                    crowd_caption_data['camera']['all'].append((word_count, token_count, text, video_id))
        
        # Collect video metadata if requested
        if collect_video_metadata and video_url and video_id not in video_metadata_dict:
            print(f"Processing video {idx}/{total_videos}: {video_id}")
            metadata = get_video_metadata(video_url)
            if metadata:
                video_metadata_dict[video_id] = metadata
        
        for caption_type, task_data in captions.items():
            # Skip if not completed
            if task_data.get("status") == "not_completed":
                continue
            
            # Get caption_data (main entry)
            caption_data = task_data.get("caption_data", {})
            
            # Collect pre_caption word count, token count, and text
            pre_caption = caption_data.get("pre_caption", "")
            if pre_caption:
                word_count = count_words(pre_caption)
                token_count = count_tokens(pre_caption)
                pre_caption_data[caption_type].append((word_count, token_count, pre_caption, video_id))
            
            # Collect final_caption word count, token count, and text
            final_caption = caption_data.get("final_caption", "")
            if final_caption:
                word_count = count_words(final_caption)
                token_count = count_tokens(final_caption)
                final_caption_data[caption_type].append((word_count, token_count, final_caption, video_id))
            
            # Collect initial_feedback word count, token count, and text
            initial_feedback = caption_data.get("initial_feedback", "")
            if initial_feedback:
                word_count = count_words(initial_feedback)
                token_count = count_tokens(initial_feedback)
                initial_feedback_data[caption_type].append((word_count, token_count, initial_feedback, video_id))
            
            # Collect final_feedback word count, token count, and text
            final_feedback = caption_data.get("final_feedback", "")
            if final_feedback:
                word_count = count_words(final_feedback)
                token_count = count_tokens(final_feedback)
                final_feedback_data[caption_type].append((word_count, token_count, final_feedback, video_id))
            
            # Collect rating scores
            initial_rating = caption_data.get("initial_caption_rating_score")
            if initial_rating is not None:
                pre_caption_ratings[caption_type].append(initial_rating)
            
            # For final caption rating:
            # - If initial_rating = 5 (perfect), use it as final rating
            # - Otherwise, use caption_rating_score
            if initial_rating == 5:
                final_caption_ratings[caption_type].append(initial_rating)
            else:
                caption_rating = caption_data.get("caption_rating_score")
                if caption_rating is not None:
                    final_caption_ratings[caption_type].append(caption_rating)
    
    # Print overlap statistics
    if adobe_excel_files:
        print(f"\nOverlap Statistics:")
        print(f"Total videos with crowd captions (overlap): {total_overlap_count}")
        print(f"Overlap videos with completed tasks: {overlap_completed_count}")
        print(f"Overlap completion rate: {overlap_completed_count/total_overlap_count*100:.1f}%" if total_overlap_count > 0 else "N/A")
    
    results = [
        pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
        pre_caption_ratings, final_caption_ratings
    ]
    
    if collect_video_metadata:
        results.append(video_metadata_dict)
    
    if adobe_excel_files:
        results.append({
            'crowd_data': crowd_caption_data,
            'overlap_completed': overlap_completed_count,
            'total_overlap': total_overlap_count
        })
    
    return tuple(results)


def print_statistics_table(stats_dict, field_name, include_tokens=True):
    """Print a formatted table of statistics with minimum examples."""
    print(f"\n{'='*100}")
    print(f"{field_name.upper()} - Word Count and Token Count Statistics")
    print(f"{'='*100}")
    
    if include_tokens and TOKENIZER_AVAILABLE:
        print(f"{'Caption Type':<20} {'Count':>8} {'Word Mean':>10} {'Word Std':>10} "
              f"{'Token Mean':>11} {'Token Std':>11} {'Min':>8} {'Max':>8}")
        print(f"{'-'*100}")
    else:
        print(f"{'Caption Type':<20} {'Count':>8} {'Word Mean':>10} {'Word Std':>10} {'Min':>8} {'Max':>8}")
        print(f"{'-'*100}")
    
    # Sort by caption type for consistent ordering
    caption_type_order = ["subject", "scene", "motion", "spatial", "camera", "color", "lighting", "effects"]
    
    # Calculate overall statistics by combining all caption types
    all_word_counts = []
    all_token_counts = []
    
    for caption_type in caption_type_order:
        if caption_type in stats_dict:
            stats = stats_dict[caption_type]
            if include_tokens and TOKENIZER_AVAILABLE:
                print(f"{caption_type:<20} {stats['count']:>8} {stats['word_mean']:>10.2f} "
                      f"{stats['word_std']:>10.2f} {stats['token_mean']:>11.2f} "
                      f"{stats['token_std']:>11.2f} {stats['word_min']:>8} {stats['word_max']:>8}")
            else:
                print(f"{caption_type:<20} {stats['count']:>8} {stats['word_mean']:>10.2f} "
                      f"{stats['word_std']:>10.2f} {stats['word_min']:>8} {stats['word_max']:>8}")
    
    # Print overall statistics
    print(f"{'-'*100}")
    
    # We need to recalculate from raw data stored in stats_dict
    # For now, we'll compute this in the main function and pass it separately
    # This is a placeholder line
    print(f"{'Overall':<20} (see below)")
    
    # Print minimum examples
    print(f"\n{'-'*100}")
    print(f"MINIMUM LENGTH EXAMPLES")
    print(f"{'-'*100}")
    
    for caption_type in caption_type_order:
        if caption_type in stats_dict and stats_dict[caption_type]['min_example']:
            min_ex = stats_dict[caption_type]['min_example']
            print(f"\n{caption_type.upper()} (Video: {min_ex['video_id']}, "
                  f"{min_ex['word_count']} words, {min_ex['token_count']} tokens):")
            # Wrap text at 90 characters for readability
            text = min_ex['text']
            if len(text) > 87:
                print(f"  {text[:87]}...")
            else:
                print(f"  {text}")
            # Show full text if it's longer
            if len(text) > 87:
                remaining = text[87:]
                while remaining:
                    chunk = remaining[:88]
                    print(f"  {chunk}")
                    remaining = remaining[88:]


def calculate_overall_text_stats(data_dict):
    """
    Calculate overall statistics by summing word counts across all caption types per video.
    This shows the total length when all captions for a video are combined.
    """
    # Group by video_id and sum across all caption types
    video_word_counts = defaultdict(int)
    video_token_counts = defaultdict(int)
    
    for caption_type, data_tuples in data_dict.items():
        for wc, tc, _, video_id in data_tuples:
            video_word_counts[video_id] += wc
            video_token_counts[video_id] += tc
    
    if not video_word_counts:
        return {
            "count": 0,
            "word_mean": 0,
            "word_std": 0,
            "word_min": 0,
            "word_max": 0,
            "token_mean": 0,
            "token_std": 0,
            "token_min": 0,
            "token_max": 0
        }
    
    # Convert to lists for statistics
    all_word_counts = list(video_word_counts.values())
    all_token_counts = list(video_token_counts.values())
    
    stats = {
        "count": len(all_word_counts),
        "word_mean": float(np.mean(all_word_counts)),
        "word_std": float(np.std(all_word_counts)),
        "word_min": int(np.min(all_word_counts)),
        "word_max": int(np.max(all_word_counts))
    }
    
    if TOKENIZER_AVAILABLE and all_token_counts:
        stats.update({
            "token_mean": float(np.mean(all_token_counts)),
            "token_std": float(np.std(all_token_counts)),
            "token_min": int(np.min(all_token_counts)),
            "token_max": int(np.max(all_token_counts))
        })
    
    return stats


def print_overall_text_stats(stats, field_name, include_tokens=True):
    """Print overall text statistics."""
    print(f"\n{'='*100}")
    print(f"{field_name.upper()} - Overall Statistics (All Caption Types Combined Per Video)")
    print(f"{'='*100}")
    
    if include_tokens and TOKENIZER_AVAILABLE:
        print(f"Videos with data: {stats['count']}")
        print(f"Word Count (total per video):  Mean = {stats['word_mean']:>7.2f}, Std = {stats['word_std']:>7.2f}, "
              f"Min = {stats['word_min']:>5}, Max = {stats['word_max']:>5}")
        print(f"Token Count (total per video): Mean = {stats['token_mean']:>7.2f}, Std = {stats['token_std']:>7.2f}, "
              f"Min = {stats['token_min']:>5}, Max = {stats['token_max']:>5}")
    else:
        print(f"Videos with data: {stats['count']}")
        print(f"Word Count (total per video):  Mean = {stats['word_mean']:>7.2f}, Std = {stats['word_std']:>7.2f}, "
              f"Min = {stats['word_min']:>5}, Max = {stats['word_max']:>5}")
    
    print(f"\nNote: These statistics show the total word/token count when all caption types")
    print(f"      for a single video are combined (e.g., subject + scene + motion + ...).")
    print(f"{'='*100}")


def print_rating_statistics_table(pre_caption_stats, final_caption_stats):
    """Print a formatted table of rating statistics."""
    print(f"\n{'='*100}")
    print(f"RATING SCORE STATISTICS (Per Caption Type)")
    print(f"{'='*100}")
    print(f"{'Caption Type':<20} {'Pre-Caption Mean':>18} {'Pre-Caption Std':>18} "
          f"{'Final-Caption Mean':>20} {'Final-Caption Std':>20}")
    print(f"{'-'*100}")
    
    # Sort by caption type for consistent ordering
    caption_type_order = ["subject", "scene", "motion", "spatial", "camera", "color", "lighting", "effects"]
    
    for caption_type in caption_type_order:
        if caption_type in pre_caption_stats or caption_type in final_caption_stats:
            pre_stats = pre_caption_stats.get(caption_type, {"count": 0, "mean": 0, "std": 0})
            final_stats = final_caption_stats.get(caption_type, {"count": 0, "mean": 0, "std": 0})
            
            # Format output with proper handling of missing data
            pre_mean_str = f"{pre_stats['mean']:.2f}" if pre_stats['count'] > 0 else "N/A"
            pre_std_str = f"{pre_stats['std']:.2f}" if pre_stats['count'] > 0 else "N/A"
            final_mean_str = f"{final_stats['mean']:.2f}" if final_stats['count'] > 0 else "N/A"
            final_std_str = f"{final_stats['std']:.2f}" if final_stats['count'] > 0 else "N/A"
            
            print(f"{caption_type:<20} {pre_mean_str:>18} {pre_std_str:>18} "
                  f"{final_mean_str:>20} {final_std_str:>20}")


def calculate_overall_rating_stats(pre_caption_rating_stats, final_caption_rating_stats):
    """
    Calculate overall rating statistics by averaging per-task means.
    This avoids bias from tasks with more annotations.
    """
    caption_type_order = ["subject", "scene", "motion", "spatial", "camera", "color", "lighting", "effects"]
    
    # Collect per-task means
    pre_task_means = []
    final_task_means = []
    
    for caption_type in caption_type_order:
        if caption_type in pre_caption_rating_stats:
            stats = pre_caption_rating_stats[caption_type]
            if stats['count'] > 0:
                pre_task_means.append(stats['mean'])
        
        if caption_type in final_caption_rating_stats:
            stats = final_caption_rating_stats[caption_type]
            if stats['count'] > 0:
                final_task_means.append(stats['mean'])
    
    overall_stats = {}
    
    if pre_task_means:
        overall_stats['pre_caption'] = {
            'mean': float(np.mean(pre_task_means)),
            'std': float(np.std(pre_task_means)),
            'num_tasks': len(pre_task_means)
        }
    
    if final_task_means:
        overall_stats['final_caption'] = {
            'mean': float(np.mean(final_task_means)),
            'std': float(np.std(final_task_means)),
            'num_tasks': len(final_task_means)
        }
    
    return overall_stats


def print_overall_rating_statistics(pre_caption_ratings, final_caption_ratings, 
                                    pre_caption_rating_stats, final_caption_rating_stats):
    """Print overall rating statistics across all caption types."""
    print(f"\n{'='*100}")
    print(f"OVERALL RATING STATISTICS (Averaged Across All Caption Types)")
    print(f"{'='*100}")
    
    # Calculate overall stats by averaging per-task means
    overall_stats = calculate_overall_rating_stats(pre_caption_rating_stats, final_caption_rating_stats)
    
    if 'pre_caption' in overall_stats:
        stats = overall_stats['pre_caption']
        # Also show raw counts
        total_pre_count = sum(len(scores) for scores in pre_caption_ratings.values())
        print(f"Pre-Caption Ratings:   Mean = {stats['mean']:.2f}, "
              f"Std = {stats['std']:.2f} "
              f"(averaged across {stats['num_tasks']} tasks, {total_pre_count} total annotations)")
    else:
        print(f"Pre-Caption Ratings:   No data available")
    
    if 'final_caption' in overall_stats:
        stats = overall_stats['final_caption']
        # Also show raw counts
        total_final_count = sum(len(scores) for scores in final_caption_ratings.values())
        print(f"Final-Caption Ratings: Mean = {stats['mean']:.2f}, "
              f"Std = {stats['std']:.2f} "
              f"(averaged across {stats['num_tasks']} tasks, {total_final_count} total annotations)")
    else:
        print(f"Final-Caption Ratings: No data available")
    
    print(f"\nNote: Overall statistics computed by averaging per-task means to avoid bias from")
    print(f"      tasks with more annotations. Total annotation counts shown for reference.")
    print(f"{'='*100}")


def analyze_video_metadata(video_metadata_dict):
    """
    Analyze video metadata statistics.
    
    Returns:
        dict: Statistics for duration, FPS, and resolution
    """
    if not video_metadata_dict:
        return {}
    
    durations = []
    fps_values = []
    widths = []
    heights = []
    
    for video_id, metadata in video_metadata_dict.items():
        if 'duration' in metadata:
            durations.append(metadata['duration'])
        if 'fps' in metadata:
            fps_values.append(metadata['fps'])
        if 'width' in metadata and 'height' in metadata:
            widths.append(metadata['width'])
            heights.append(metadata['height'])
    
    stats = {}
    
    if durations:
        stats['duration'] = {
            'count': len(durations),
            'mean': float(np.mean(durations)),
            'std': float(np.std(durations)),
            'min': float(np.min(durations)),
            'max': float(np.max(durations)),
            'total': float(np.sum(durations))
        }
    
    if fps_values:
        stats['fps'] = {
            'count': len(fps_values),
            'mean': float(np.mean(fps_values)),
            'std': float(np.std(fps_values)),
            'min': float(np.min(fps_values)),
            'max': float(np.max(fps_values))
        }
    
    if widths and heights:
        # Count resolution frequencies
        resolutions = [f"{w}x{h}" for w, h in zip(widths, heights)]
        resolution_counts = {}
        for res in resolutions:
            resolution_counts[res] = resolution_counts.get(res, 0) + 1
        
        stats['resolution'] = {
            'count': len(resolutions),
            'width_mean': float(np.mean(widths)),
            'height_mean': float(np.mean(heights)),
            'most_common': sorted(resolution_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    return stats


def print_video_metadata_statistics(video_metadata_stats):
    """Print video metadata statistics."""
    if not video_metadata_stats:
        print("\nNo video metadata available.")
        return
    
    print(f"\n{'='*100}")
    print(f"VIDEO METADATA STATISTICS")
    print(f"{'='*100}")
    
    if 'duration' in video_metadata_stats:
        dur_stats = video_metadata_stats['duration']
        print(f"\nDuration (seconds):")
        print(f"  Count: {dur_stats['count']}")
        print(f"  Mean:  {dur_stats['mean']:.2f}s")
        print(f"  Std:   {dur_stats['std']:.2f}s")
        print(f"  Min:   {dur_stats['min']:.2f}s")
        print(f"  Max:   {dur_stats['max']:.2f}s")
        print(f"  Total: {dur_stats['total']:.2f}s ({dur_stats['total']/3600:.2f} hours)")
    
    if 'fps' in video_metadata_stats:
        fps_stats = video_metadata_stats['fps']
        print(f"\nFrames Per Second (FPS):")
        print(f"  Count: {fps_stats['count']}")
        print(f"  Mean:  {fps_stats['mean']:.2f}")
        print(f"  Std:   {fps_stats['std']:.2f}")
        print(f"  Min:   {fps_stats['min']:.2f}")
        print(f"  Max:   {fps_stats['max']:.2f}")
    
    if 'resolution' in video_metadata_stats:
        res_stats = video_metadata_stats['resolution']
        print(f"\nResolution:")
        print(f"  Count: {res_stats['count']}")
        print(f"  Mean:  {res_stats['width_mean']:.0f}x{res_stats['height_mean']:.0f}")
        print(f"  Most common resolutions:")
        for resolution, count in res_stats['most_common']:
            percentage = (count / res_stats['count']) * 100
            print(f"    {resolution}: {count} videos ({percentage:.1f}%)")
    
    print(f"{'='*100}")


def analyze_crowd_caption_statistics(crowd_caption_info):
    """
    Analyze crowd caption statistics.
    
    Args:
        crowd_caption_info: Dictionary with crowd_data, overlap_completed, total_overlap
    
    Returns:
        Dictionary with statistics for each crowd caption type
    """
    crowd_data = crowd_caption_info['crowd_data']
    stats = {}
    
    for caption_type, data_dict in crowd_data.items():
        type_stats = {}
        for key, data_tuples in data_dict.items():
            if not data_tuples:
                type_stats[key] = {
                    'count': 0,
                    'word_mean': 0,
                    'word_std': 0,
                    'word_min': 0,
                    'word_max': 0,
                    'token_mean': 0,
                    'token_std': 0,
                    'token_min': 0,
                    'token_max': 0
                }
                continue
            
            word_counts = [wc for wc, _, _, _ in data_tuples]
            token_counts = [tc for _, tc, _, _ in data_tuples]
            
            type_stats[key] = {
                'count': len(word_counts),
                'word_mean': float(np.mean(word_counts)),
                'word_std': float(np.std(word_counts)),
                'word_min': int(np.min(word_counts)),
                'word_max': int(np.max(word_counts))
            }
            
            if TOKENIZER_AVAILABLE and token_counts:
                type_stats[key].update({
                    'token_mean': float(np.mean(token_counts)),
                    'token_std': float(np.std(token_counts)),
                    'token_min': int(np.min(token_counts)),
                    'token_max': int(np.max(token_counts))
                })
        
        stats[caption_type] = type_stats
    
    return stats


def print_crowd_caption_statistics(crowd_caption_info, crowd_stats):
    """Print crowd caption statistics."""
    print(f"\n{'='*100}")
    print(f"CROWD CAPTION STATISTICS (Overlap Videos with Crowdsourced Annotations)")
    print(f"{'='*100}")
    
    # Print overlap completion info
    overlap_completed = crowd_caption_info['overlap_completed']
    total_overlap = crowd_caption_info['total_overlap']
    completion_rate = (overlap_completed / total_overlap * 100) if total_overlap > 0 else 0
    
    print(f"\nOverlap Completion:")
    print(f"  Total videos with crowd captions: {total_overlap}")
    print(f"  Videos with completed annotations: {overlap_completed}")
    print(f"  Completion rate: {completion_rate:.1f}%")
    
    # Print statistics for each crowd caption type
    crowd_types = {
        'subject_background': 'Subject and Background',
        'subject_motion': 'Subject Motion',
        'camera': 'Camera'
    }
    
    for caption_type, display_name in crowd_types.items():
        if caption_type in crowd_stats:
            stats = crowd_stats[caption_type].get('all', {})
            
            print(f"\n{display_name} Captions:")
            if stats['count'] > 0:
                if TOKENIZER_AVAILABLE:
                    print(f"  Count:       {stats['count']}")
                    print(f"  Word Mean:   {stats['word_mean']:.2f}")
                    print(f"  Word Std:    {stats['word_std']:.2f}")
                    print(f"  Token Mean:  {stats['token_mean']:.2f}")
                    print(f"  Token Std:   {stats['token_std']:.2f}")
                    print(f"  Min:         {stats['word_min']} words, {stats['token_min']} tokens")
                    print(f"  Max:         {stats['word_max']} words, {stats['token_max']} tokens")
                else:
                    print(f"  Count:       {stats['count']}")
                    print(f"  Word Mean:   {stats['word_mean']:.2f}")
                    print(f"  Word Std:    {stats['word_std']:.2f}")
                    print(f"  Min:         {stats['word_min']} words")
                    print(f"  Max:         {stats['word_max']} words")
            else:
                print(f"  No captions found")
    
    # Calculate and print overall crowd caption statistics
    print(f"\nOverall Crowd Captions (All 3 Types Combined Per Video):")
    crowd_data = crowd_caption_info['crowd_data']
    
    # Group by video and sum across all three caption types
    video_totals = defaultdict(lambda: {'words': 0, 'tokens': 0})
    
    for caption_type in ['subject_background', 'subject_motion', 'camera']:
        if caption_type in crowd_data and 'all' in crowd_data[caption_type]:
            for wc, tc, _, video_id in crowd_data[caption_type]['all']:
                video_totals[video_id]['words'] += wc
                video_totals[video_id]['tokens'] += tc
    
    if video_totals:
        total_words = [v['words'] for v in video_totals.values()]
        total_tokens = [v['tokens'] for v in video_totals.values()]
        
        print(f"  Videos: {len(video_totals)}")
        print(f"  Word Count (total per video):  Mean = {np.mean(total_words):.2f}, "
              f"Std = {np.std(total_words):.2f}, Min = {np.min(total_words)}, Max = {np.max(total_words)}")
        if TOKENIZER_AVAILABLE and total_tokens:
            print(f"  Token Count (total per video): Mean = {np.mean(total_tokens):.2f}, "
                  f"Std = {np.std(total_tokens):.2f}, Min = {np.min(total_tokens)}, Max = {np.max(total_tokens)}")
    
    print(f"{'='*100}")


def save_statistics_json(output_file, pre_caption_stats, final_caption_stats, 
                        initial_feedback_stats, final_feedback_stats,
                        pre_caption_rating_stats, final_caption_rating_stats,
                        pre_caption_ratings, final_caption_ratings,
                        pre_caption_data, final_caption_data,
                        initial_feedback_data, final_feedback_data,
                        video_metadata_stats=None, crowd_caption_stats=None, crowd_caption_info=None):
    """Save all statistics to a JSON file."""
    # Calculate overall rating statistics using per-task averaging
    overall_rating_stats = calculate_overall_rating_stats(pre_caption_rating_stats, final_caption_rating_stats)
    
    # Add raw counts to overall stats
    if 'pre_caption' in overall_rating_stats:
        total_pre_count = sum(len(scores) for scores in pre_caption_ratings.values())
        overall_rating_stats['pre_caption']['total_annotations'] = total_pre_count
    
    if 'final_caption' in overall_rating_stats:
        total_final_count = sum(len(scores) for scores in final_caption_ratings.values())
        overall_rating_stats['final_caption']['total_annotations'] = total_final_count
    
    # Calculate overall text statistics
    overall_text_stats = {
        "pre_caption": calculate_overall_text_stats(pre_caption_data),
        "final_caption": calculate_overall_text_stats(final_caption_data),
        "initial_feedback": calculate_overall_text_stats(initial_feedback_data),
        "final_feedback": calculate_overall_text_stats(final_feedback_data)
    }
    
    results = {
        "text_statistics": {
            "by_caption_type": {
                "pre_caption": pre_caption_stats,
                "final_caption": final_caption_stats,
                "initial_feedback": initial_feedback_stats,
                "final_feedback": final_feedback_stats
            },
            "overall": overall_text_stats
        },
        "rating_statistics": {
            "by_caption_type": {
                "pre_caption": pre_caption_rating_stats,
                "final_caption": final_caption_rating_stats
            },
            "overall": overall_rating_stats
        }
    }
    
    # Add video metadata if available
    if video_metadata_stats:
        results["video_metadata"] = video_metadata_stats
    
    # Add crowd caption statistics if available
    if crowd_caption_stats and crowd_caption_info:
        results["crowd_captions"] = {
            "statistics": crowd_caption_stats,
            "overlap_completed": crowd_caption_info['overlap_completed'],
            "total_overlap": crowd_caption_info['total_overlap'],
            "completion_rate": (crowd_caption_info['overlap_completed'] / crowd_caption_info['total_overlap'] * 100) 
                               if crowd_caption_info['total_overlap'] > 0 else 0
        }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nStatistics saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze word count, token count, rating statistics, video metadata, and crowd captions for exported caption data"
    )
    
    parser.add_argument(
        "export_file",
        type=str,
        help="Path to exported JSON file (e.g., all_videos_with_captions_20251004_0625.json)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file for statistics (default: same directory as input with _stats.json suffix)"
    )
    
    parser.add_argument(
        "--tokenizer",
        type=str,
        default="gpt2",
        help="Tokenizer model to use for token counting (default: gpt2)"
    )
    
    parser.add_argument(
        "--video-metadata",
        action="store_true",
        help="Extract and analyze video metadata (duration, FPS, resolution). Requires ffprobe and will download videos."
    )
    
    parser.add_argument(
        "--adobe-excel-files",
        nargs="+",
        type=str,
        default=None,
        help="Adobe Excel files containing crowd captions (e.g., adobe_2_19.xlsx adobe_2_17.xlsx)"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    export_file = Path(args.export_file)
    if not export_file.exists():
        print(f"Error: File not found: {export_file}")
        return
    
    # Validate Adobe Excel files if provided
    if args.adobe_excel_files:
        for excel_file in args.adobe_excel_files:
            if not Path(excel_file).exists():
                print(f"Error: Adobe Excel file not found: {excel_file}")
                return
    
    # Initialize tokenizer if available
    if TOKENIZER_AVAILABLE:
        try:
            global tokenizer
            tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
            print(f"Using tokenizer: {args.tokenizer}")
        except Exception as e:
            print(f"Warning: Could not load tokenizer {args.tokenizer}: {e}")
            print("Falling back to gpt2 tokenizer")
            tokenizer = AutoTokenizer.from_pretrained("gpt2")
    
    print(f"\nAnalyzing caption statistics from: {export_file}")
    
    # Collect word counts, token counts, ratings, video metadata, and crowd captions
    print("\nCollecting data...")
    collection_result = collect_word_counts_and_ratings(
        export_file, 
        collect_video_metadata=args.video_metadata,
        adobe_excel_files=args.adobe_excel_files
    )
    
    # Unpack results based on what was collected
    if args.adobe_excel_files and args.video_metadata:
        (pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
         pre_caption_ratings, final_caption_ratings, video_metadata_dict, crowd_caption_info) = collection_result
    elif args.adobe_excel_files:
        (pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
         pre_caption_ratings, final_caption_ratings, crowd_caption_info) = collection_result
        video_metadata_dict = {}
    elif args.video_metadata:
        (pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
         pre_caption_ratings, final_caption_ratings, video_metadata_dict) = collection_result
        crowd_caption_info = None
    else:
        (pre_caption_data, final_caption_data, initial_feedback_data, final_feedback_data,
         pre_caption_ratings, final_caption_ratings) = collection_result
        video_metadata_dict = {}
        crowd_caption_info = None
    
    # Calculate statistics for text fields
    print("Calculating text statistics...")
    pre_caption_stats = analyze_field_statistics(pre_caption_data, "pre_caption")
    final_caption_stats = analyze_field_statistics(final_caption_data, "final_caption")
    initial_feedback_stats = analyze_field_statistics(initial_feedback_data, "initial_feedback")
    final_feedback_stats = analyze_field_statistics(final_feedback_data, "final_feedback")
    
    # Calculate statistics for ratings
    print("Calculating rating statistics...")
    pre_caption_rating_stats = analyze_rating_statistics(pre_caption_ratings)
    final_caption_rating_stats = analyze_rating_statistics(final_caption_ratings)
    
    # Calculate video metadata statistics if collected
    video_metadata_stats = None
    if video_metadata_dict:
        print("Calculating video metadata statistics...")
        video_metadata_stats = analyze_video_metadata(video_metadata_dict)
    
    # Calculate crowd caption statistics if collected
    crowd_caption_stats = None
    if crowd_caption_info:
        print("Calculating crowd caption statistics...")
        crowd_caption_stats = analyze_crowd_caption_statistics(crowd_caption_info)
    
    # Print results
    print_statistics_table(pre_caption_stats, "pre_caption")
    overall_pre_caption_stats = calculate_overall_text_stats(pre_caption_data)
    print_overall_text_stats(overall_pre_caption_stats, "pre_caption")
    
    print_statistics_table(final_caption_stats, "final_caption")
    overall_final_caption_stats = calculate_overall_text_stats(final_caption_data)
    print_overall_text_stats(overall_final_caption_stats, "final_caption")
    
    print_statistics_table(initial_feedback_stats, "initial_feedback")
    overall_initial_feedback_stats = calculate_overall_text_stats(initial_feedback_data)
    print_overall_text_stats(overall_initial_feedback_stats, "initial_feedback")
    
    print_statistics_table(final_feedback_stats, "final_feedback")
    overall_final_feedback_stats = calculate_overall_text_stats(final_feedback_data)
    print_overall_text_stats(overall_final_feedback_stats, "final_feedback")
    
    # Print rating statistics
    print_rating_statistics_table(pre_caption_rating_stats, final_caption_rating_stats)
    print_overall_rating_statistics(pre_caption_ratings, final_caption_ratings,
                                   pre_caption_rating_stats, final_caption_rating_stats)
    
    # Print video metadata statistics if available
    if video_metadata_stats:
        print_video_metadata_statistics(video_metadata_stats)
    
    # Print crowd caption statistics if available
    if crowd_caption_stats and crowd_caption_info:
        print_crowd_caption_statistics(crowd_caption_info, crowd_caption_stats)
    
    # Save to JSON
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = export_file.parent / f"{export_file.stem}_stats.json"
    
    save_statistics_json(output_file, pre_caption_stats, final_caption_stats,
                        initial_feedback_stats, final_feedback_stats,
                        pre_caption_rating_stats, final_caption_rating_stats,
                        pre_caption_ratings, final_caption_ratings,
                        pre_caption_data, final_caption_data,
                        initial_feedback_data, final_feedback_data,
                        video_metadata_stats, crowd_caption_stats, crowd_caption_info)
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()