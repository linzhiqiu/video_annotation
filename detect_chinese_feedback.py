#!/usr/bin/env python3
"""
Detect Chinese Characters in Feedback Script

Analyzes caption export data to detect cases where:
1. Status is approved or rejected
2. Final feedback contains Chinese characters

This identifies cases where annotators wrote feedback in Chinese.

Output:
- sampled_data.jsonl: All analyzed samples with classifications
- report.md: Summary statistics and examples
"""

import json
import random
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv


def load_caption_export(export_path: Path):
    """Load caption export JSON file. Can be either list or dict format."""
    with open(export_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_json_file(file_path: str) -> List[str]:
    """Load a JSON file containing a list of video URLs."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return []


def build_batch_mapping(batch_files: List[str] = None) -> Dict[str, Tuple[str, int]]:
    """
    Build a mapping from video_url to (batch file name, index within batch).
    
    If batch_files is None or empty, tries to auto-load from main_config.py.
    
    Args:
        batch_files: Optional list of paths to batch JSON files
    
    Returns:
        Dict mapping video_url -> (batch_name, index) 
        e.g., "http://..." -> ("overlap_100_to_110.json", 3)
    """
    url_to_batch = {}
    
    # If no batch files provided, try to load from main_config.py
    if not batch_files:
        config_path = 'caption/config/main_config.py'
        print(f"No batch files provided, trying to load from {config_path}...")
        
        try:
            # Try to import directly
            import sys
            if 'caption/config' not in sys.path:
                sys.path.insert(0, 'caption/config')
            
            # Clear cached import if exists
            if 'main_config' in sys.modules:
                del sys.modules['main_config']
            
            from main_config import DEFAULT_VIDEO_URLS_FILES
            batch_files = DEFAULT_VIDEO_URLS_FILES
            print(f"Loaded {len(batch_files)} batch file paths from main_config.py")
        except ImportError as e:
            print(f"Warning: Could not import main_config.py: {e}")
            
            # Fallback: try to parse the file directly
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                
                # Extract the list using regex
                match = re.search(r'DEFAULT_VIDEO_URLS_FILES\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if match:
                    list_content = match.group(1)
                    # Extract quoted strings
                    found_files = re.findall(r"'([^']+)'|\"([^\"]+)\"", list_content)
                    batch_files = [f[0] or f[1] for f in found_files]
                    print(f"Parsed {len(batch_files)} batch file paths from main_config.py")
                else:
                    print("Warning: Could not parse DEFAULT_VIDEO_URLS_FILES")
                    return {}
            except Exception as e2:
                print(f"Warning: Could not read config file: {e2}")
                return {}
    
    # Load each batch file
    for file_path in batch_files:
        # Add caption/ prefix if not present
        if not file_path.startswith('caption/'):
            full_path = f"caption/{file_path}"
        else:
            full_path = file_path
        
        batch_path = Path(full_path)
        if not batch_path.exists():
            continue
        
        # Get just the filename for display
        batch_name = batch_path.name
        
        # Load videos from this batch file
        video_urls = load_json_file(str(batch_path))
        
        for idx, url in enumerate(video_urls):
            url_to_batch[url] = (batch_name, idx)
    
    print(f"Built mapping for {len(url_to_batch)} video URLs across {len(batch_files)} batch files")
    return url_to_batch


def contains_chinese(text: str) -> bool:
    """Check if text contains any Chinese characters."""
    if not text:
        return False
    # Match CJK Unified Ideographs and common CJK ranges
    return bool(re.search(r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002ceb0-\U0002ebef\U00030000-\U0003134f]', text))


def extract_chinese_segments(text: str) -> List[str]:
    """Extract segments containing Chinese characters with surrounding context."""
    if not text:
        return []
    segments = []
    for match in re.finditer(r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df]+', text):
        start = max(0, match.start() - 20)
        end = min(len(text), match.end() + 20)
        segment = text[start:end]
        if start > 0:
            segment = "..." + segment
        if end < len(text):
            segment = segment + "..."
        segments.append(segment)
    return segments


def analyze_export_statistics(export_data, url_to_batch: Optional[Dict[str, Tuple[str, int]]] = None) -> Dict:
    """
    Analyze export data to count feedback by status.
    
    Returns dict with:
    - total_approved_rejected: Total feedback in approved/rejected status
    - all_samples_approved_rejected: All samples with approved/rejected status
    """
    if url_to_batch is None:
        url_to_batch = {}
    
    # Handle both list and dict formats
    if isinstance(export_data, list):
        video_list = export_data
    else:
        video_list = list(export_data.values())
    
    all_samples_approved_rejected = []
    
    for video_data in video_list:
        video_id = video_data.get('video_id', '')
        video_url = video_data.get('video_url', '')
        
        # Get batch info (name and index)
        batch_info = url_to_batch.get(video_url, ('unknown', -1))
        batch_file = batch_info[0]
        batch_index = batch_info[1]
        
        captions = video_data.get('captions', {})
        
        for caption_type, caption_data in captions.items():
            # Skip if no caption_data
            if 'caption_data' not in caption_data:
                continue
            
            status = caption_data.get('status', '')
            
            # Only look at approved or rejected status
            if status not in ['approved', 'rejected']:
                continue
            
            caption_info = caption_data['caption_data']
            
            final_caption = caption_info.get('final_caption', '')
            final_feedback = caption_info.get('final_feedback', '')
            pre_caption = caption_info.get('pre_caption', '')
            
            # Safely handle None or non-string types
            if final_caption is None:
                final_caption = ''
            elif not isinstance(final_caption, str):
                final_caption = str(final_caption)
            
            if final_feedback is None:
                final_feedback = ''
            elif not isinstance(final_feedback, str):
                final_feedback = str(final_feedback)
            
            if pre_caption is None:
                pre_caption = ''
            elif not isinstance(pre_caption, str):
                pre_caption = str(pre_caption)
            
            final_caption = final_caption.strip()
            final_feedback = final_feedback.strip()
            pre_caption = pre_caption.strip()
            
            # Create sample dict
            sample = {
                'video_id': video_id,
                'video_url': video_url,
                'batch_file': batch_file,
                'batch_index': batch_index,
                'caption_type': caption_type,
                'status': status,
                'final_feedback': final_feedback,
                'pre_caption': pre_caption,
                'final_caption': final_caption,
                'user': caption_info.get('user', ''),
                'timestamp': caption_info.get('timestamp', ''),
                'caption_length': len(final_caption),
                'feedback_length': len(final_feedback),
                'initial_caption_rating_score': caption_info.get('initial_caption_rating_score'),
                'feedback_is_needed': caption_info.get('feedback_is_needed', True)
            }
            
            # Add to approved/rejected list
            all_samples_approved_rejected.append(sample)
    
    return {
        'total_approved_rejected': len(all_samples_approved_rejected),
        'all_samples_approved_rejected': all_samples_approved_rejected,
    }


def extract_samples_from_export(export_data, sample_count: int, seed: int,
                                url_to_batch: Optional[Dict[str, Tuple[str, int]]] = None) -> Tuple[List[Dict], int, Dict]:
    """
    Extract samples from export data.
    Only extracts samples from approved/rejected status.
    
    Args:
        export_data: Can be either a list of video objects or a dict keyed by video_id
        sample_count: Number of samples to select (-1 for all)
        seed: Random seed
        url_to_batch: Optional mapping from video_url to (batch_name, index)
    
    Returns:
        (samples, total_count, statistics)
    """
    random.seed(seed)
    
    # Get statistics
    stats = analyze_export_statistics(export_data, url_to_batch)
    
    # Use all approved/rejected samples
    all_samples = stats['all_samples_approved_rejected']
    total_size = len(all_samples)
    
    # Sample
    if sample_count == -1:
        print(f"Using full dataset: {total_size} samples")
        return all_samples, total_size, stats
    elif len(all_samples) < sample_count:
        print(f"Warning: Only {len(all_samples)} samples available, requested {sample_count}")
        return all_samples, total_size, stats
    
    return random.sample(all_samples, sample_count), total_size, stats


def classify_chinese_feedback(sample: Dict) -> Tuple[str, str]:
    """
    Classify whether feedback contains Chinese characters.
    
    Returns:
        (label, rationale)
        label: "Yes" or "No"
    """
    final_feedback = sample.get('final_feedback', '')
    
    if contains_chinese(final_feedback):
        segments = extract_chinese_segments(final_feedback)
        context = "; ".join(segments[:3])  # Show up to 3 segments
        return "Yes", f"Feedback contains Chinese characters. Context: \"{context}\""
    else:
        return "No", "No Chinese characters found in feedback"


def print_examples(samples: List[Dict], num_examples: int = 5):
    """Print example samples."""
    print(f"\n{'='*80}")
    print(f"Sample Examples (showing {min(num_examples, len(samples))} of {len(samples)})")
    print(f"{'='*80}\n")
    
    for i, sample in enumerate(samples[:num_examples], 1):
        print(f"Example {i}:")
        print(f"Video ID: {sample['video_id']}")
        print(f"Batch File: {sample['batch_file']}")
        print(f"Batch Index: {sample['batch_index']}")
        print(f"Caption Type: {sample['caption_type']}")
        print(f"Status: {sample['status']}")
        print(f"Rating Score: {sample.get('initial_caption_rating_score', 'N/A')}")
        print(f"Feedback Length: {sample['feedback_length']} chars")
        print(f"Final Feedback: {sample['final_feedback'][:200]}...")
        print()


def generate_report(samples: List[Dict], seed: int, timestamp: str,
                   output_path: Path, total_dataset_size: int, export_file: str, stats: Dict):
    """Generate markdown report with statistics and examples."""
    
    # Calculate statistics
    total = len(samples)
    yes_samples = [s for s in samples if s['label'] == 'Yes']
    no_samples = [s for s in samples if s['label'] == 'No']
    
    yes_count = len(yes_samples)
    no_count = len(no_samples)
    
    yes_pct = (yes_count / total * 100) if total > 0 else 0
    no_pct = (no_count / total * 100) if total > 0 else 0
    
    # Analyze feedback length statistics
    yes_lengths = [s['feedback_length'] for s in yes_samples]
    no_lengths = [s['feedback_length'] for s in no_samples]
    
    avg_yes_length = sum(yes_lengths) / len(yes_lengths) if yes_lengths else 0
    avg_no_length = sum(no_lengths) / len(no_lengths) if no_lengths else 0
    
    # Per-user breakdown for Yes samples
    user_counts = {}
    for s in yes_samples:
        user = s.get('user', 'unknown')
        user_counts[user] = user_counts.get(user, 0) + 1
    user_counts_sorted = sorted(user_counts.items(), key=lambda x: -x[1])
    
    # Start building report
    report = f"""# Chinese Characters in Feedback Detection Report

## Dataset Information

- **Source Export File**: `{export_file}`
- **Total Captions (Approved/Rejected only)**: {stats['total_approved_rejected']}
- **Sampled for Analysis**: {total} samples
- **Random Seed**: {seed}
- **Timestamp**: {timestamp}

## Detection Criteria

A sample is classified as "Yes" if:
1. Status is approved or rejected
2. Final feedback contains Chinese characters (Unicode CJK ranges)

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage | Avg Feedback Length |
|-------|-------|------------|---------------------|
| Yes (Feedback contains Chinese) | {yes_count} | {yes_pct:.2f}% | {avg_yes_length:.0f} chars |
| No (No Chinese in feedback) | {no_count} | {no_pct:.2f}% | {avg_no_length:.0f} chars |
| **Total** | {total} | 100.00% | - |

"""

    # Per-user breakdown
    if user_counts_sorted:
        report += "### Per-User Breakdown (Chinese Feedback)\n\n"
        report += "| User | Count |\n"
        report += "|------|-------|\n"
        for user, count in user_counts_sorted:
            report += f"| {user} | {count} |\n"
        report += "\n"

    # Add sample examples section - only show Yes samples
    if yes_samples:
        report += f"## All Feedback Containing Chinese Characters ({len(yes_samples)} total)\n\n"
        for i, example in enumerate(yes_samples, 1):
            report += f"### Example {i}/{len(yes_samples)}\n\n"
            report += f"| Field | Value |\n"
            report += f"|-------|-------|\n"
            report += f"| Video ID | `{example['video_id']}` |\n"
            report += f"| Batch File | `{example['batch_file']}` |\n"
            report += f"| Batch Index | {example['batch_index']} |\n"
            report += f"| Caption Type | {example['caption_type']} |\n"
            report += f"| Status | {example['status']} |\n"
            report += f"| User | {example.get('user', 'N/A')} |\n"
            report += f"| Rating Score | {example.get('initial_caption_rating_score', 'N/A')} |\n"
            report += f"| Timestamp | {example.get('timestamp', 'N/A')} |\n\n"
            report += f"**Final Feedback**:\n\n```\n{example['final_feedback']}\n```\n\n"
            report += f"**Final Caption**:\n\n```\n{example['final_caption']}\n```\n\n"
            report += f"**Detection Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += "---\n\n"
    else:
        report += "## Results\n\nNo samples found with Chinese characters in feedback.\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect Chinese characters in caption feedback"
    )
    parser.add_argument(
        '--export-file',
        type=str,
        default='caption_export/export_20260218_2254/all_videos_with_captions_20260218_2254.json',
        help='Path to caption export JSON file'
    )
    parser.add_argument(
        '--sample-count',
        type=int,
        default=-1,
        help='Number of samples to randomly select. Use -1 for full dataset (default: -1)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=100,
        help='Random seed for reproducibility (default: 100)'
    )
    parser.add_argument(
        '--batch-files',
        type=str,
        nargs='*',
        default=[],
        help='Paths to batch JSON files (each contains a list of video URLs) to map videos to batches'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Set random seed
    random.seed(args.seed)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Setup paths
    export_path = Path(args.export_file)
    if not export_path.exists():
        print(f"Error: Export file not found: {export_path}")
        return
    
    # Build batch mapping (auto-loads from main_config.py if no batch files provided)
    print(f"\nLoading batch file mappings...")
    url_to_batch = build_batch_mapping(args.batch_files if args.batch_files else None)
    
    # Generate run directory name
    if args.sample_count == -1:
        run_dir = f"chinese_feedback_analysis_full_{timestamp}"
    else:
        run_dir = f"chinese_feedback_analysis_seed{args.seed}_{timestamp}"
    
    output_dir = export_path.parent / run_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Chinese Characters in Feedback Detection")
    print(f"{'='*80}\n")
    print(f"Export file: {export_path}")
    print(f"Output directory: {output_dir}")
    print(f"Sample count: {'Full dataset' if args.sample_count == -1 else args.sample_count}")
    print(f"Random seed: {args.seed}")
    
    # Load export data
    print(f"\nLoading export data...")
    export_data = load_caption_export(export_path)
    
    # Extract samples with statistics
    print(f"\nAnalyzing export data statistics...")
    samples, total_dataset_size, stats = extract_samples_from_export(
        export_data, args.sample_count, args.seed, url_to_batch
    )
    
    print(f"\n{'='*80}")
    print("Dataset Statistics:")
    print(f"{'='*80}")
    print(f"Total captions (approved/rejected status only): {stats['total_approved_rejected']}")
    print(f"Sampled for analysis: {len(samples)}")
    print(f"{'='*80}")
    
    # Print examples
    print_examples(samples, num_examples=5)
    
    # Classify samples (no LLM needed - simple regex matching)
    print(f"\n{'='*80}")
    print(f"Detecting Chinese characters in feedback...")
    print(f"{'='*80}\n")
    
    for i, sample in enumerate(samples):
        label, rationale = classify_chinese_feedback(sample)
        sample['label'] = label
        sample['rationale'] = rationale
        
        if (i + 1) % 500 == 0 or (i + 1) == len(samples):
            print(f"Progress: {i + 1}/{len(samples)} ({(i + 1)/len(samples)*100:.1f}%)")
    
    print(f"\n✅ Classified all {len(samples)} samples\n")
    
    # Save sampled data
    sampled_data_path = output_dir / 'sampled_data.jsonl'
    with open(sampled_data_path, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"✅ Sampled data saved to: {sampled_data_path}")
    
    # Generate report
    report_path = output_dir / 'report.md'
    generate_report(
        samples,
        args.seed,
        timestamp,
        report_path,
        total_dataset_size,
        str(export_path),
        stats
    )
    
    # Print summary
    yes_count = sum(1 for s in samples if s['label'] == 'Yes')
    no_count = sum(1 for s in samples if s['label'] == 'No')
    
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Feedback contains Chinese (Yes): {yes_count} ({yes_count/len(samples)*100:.2f}%)")
    print(f"No Chinese in feedback (No): {no_count} ({no_count/len(samples)*100:.2f}%)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()