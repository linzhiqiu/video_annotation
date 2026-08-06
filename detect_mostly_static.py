#!/usr/bin/env python3
"""
Detect Mostly Static Camera Critiques Script

Analyzes caption export data to detect cases where:
1. Pre-caption rating is NOT 5 (i.e., has a critique)
2. Final caption contains "mostly static"
3. Critique/feedback contains "mostly static"
4. Pre-caption does NOT contain "mostly static"

This identifies cases where annotators added "mostly static" via their critique.

Output:
- sampled_data.jsonl: All analyzed samples with classifications
- report.md: Summary statistics and examples
"""

import os
import json
import random
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv


def load_caption_export(export_path: Path):
    """Load caption export JSON file. Can be either list or dict format."""
    with open(export_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def contains_mostly_static(text: str) -> bool:
    """Check if text contains 'mostly static' (case-insensitive)."""
    if not text:
        return False
    return 'mostly static' in text.lower()


def analyze_export_statistics(export_data) -> Dict:
    """
    Analyze export data to count feedback by status and rating.
    
    Returns dict with:
    - total_approved_rejected: Total feedback in approved/rejected status
    - non_5_score_count: Count of non-5-score pre-captions in approved/rejected
    - all_samples_approved_rejected: All samples with approved/rejected status
    - non_5_score_samples: Samples with non-5-score pre-captions (have critiques)
    """
    # Handle both list and dict formats
    if isinstance(export_data, list):
        video_list = export_data
    else:
        video_list = list(export_data.values())
    
    all_samples_approved_rejected = []
    non_5_score_samples = []
    
    for video_data in video_list:
        video_id = video_data.get('video_id', '')
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
            
            # Only include samples with non-empty final_caption
            if not final_caption:
                continue
            
            # Create sample dict
            sample = {
                'video_id': video_id,
                'caption_type': caption_type,
                'status': status,
                'final_feedback': final_feedback,
                'pre_caption': pre_caption,
                'final_caption': final_caption,
                'user': caption_info.get('user', ''),
                'timestamp': caption_info.get('timestamp', ''),
                'caption_length': len(final_caption),
                'initial_caption_rating_score': caption_info.get('initial_caption_rating_score'),
                'feedback_is_needed': caption_info.get('feedback_is_needed', True)
            }
            
            # Add to approved/rejected list
            all_samples_approved_rejected.append(sample)
            
            # Check if it's a non-5-score pre-caption (has critique)
            if sample['initial_caption_rating_score'] != 5:
                non_5_score_samples.append(sample)
    
    return {
        'total_approved_rejected': len(all_samples_approved_rejected),
        'non_5_score_count': len(non_5_score_samples),
        'all_samples_approved_rejected': all_samples_approved_rejected,
        'non_5_score_samples': non_5_score_samples
    }


def extract_samples_from_export(export_data, sample_count: int, seed: int) -> Tuple[List[Dict], int, Dict]:
    """
    Extract samples from export data.
    Only extracts non-5-score samples from approved/rejected status.
    
    Args:
        export_data: Can be either a list of video objects or a dict keyed by video_id
        sample_count: Number of samples to select (-1 for all)
        seed: Random seed
    
    Returns:
        (samples, total_count, statistics) where:
        - samples: list of sampled samples
        - total_count: total samples available
        - statistics: dict with counts by status and rating
    """
    random.seed(seed)
    
    # Get statistics
    stats = analyze_export_statistics(export_data)
    
    # Use non-5-score samples (those with critiques)
    all_samples = stats['non_5_score_samples']
    total_size = len(all_samples)
    
    # Sample
    if sample_count == -1:
        print(f"Using full dataset: {total_size} samples")
        return all_samples, total_size, stats
    elif len(all_samples) < sample_count:
        print(f"Warning: Only {len(all_samples)} samples available, requested {sample_count}")
        return all_samples, total_size, stats
    
    return random.sample(all_samples, sample_count), total_size, stats


def classify_mostly_static_critique(sample: Dict) -> Tuple[str, str]:
    """
    Classify whether a critique added 'mostly static' to a caption.
    
    Conditions for "Yes":
    1. Final caption contains "mostly static"
    2. Critique/feedback contains "mostly static"
    3. Pre-caption does NOT contain "mostly static"
    
    Returns:
        (label, rationale)
        label: "Yes" or "No"
    """
    final_caption = sample.get('final_caption', '')
    final_feedback = sample.get('final_feedback', '')
    pre_caption = sample.get('pre_caption', '')
    
    final_has_static = contains_mostly_static(final_caption)
    feedback_has_static = contains_mostly_static(final_feedback)
    pre_has_static = contains_mostly_static(pre_caption)
    
    if final_has_static and feedback_has_static and not pre_has_static:
        # Find context in feedback
        lower_feedback = final_feedback.lower()
        idx = lower_feedback.find('mostly static')
        start = max(0, idx - 30)
        end = min(len(final_feedback), idx + 50)
        context = final_feedback[start:end]
        if start > 0:
            context = "..." + context
        if end < len(final_feedback):
            context = context + "..."
        
        return "Yes", f"Critique added 'mostly static'. Feedback context: \"{context}\""
    else:
        reasons = []
        if not final_has_static:
            reasons.append("final caption missing 'mostly static'")
        if not feedback_has_static:
            reasons.append("feedback missing 'mostly static'")
        if pre_has_static:
            reasons.append("pre-caption already has 'mostly static'")
        
        return "No", f"Not a match: {'; '.join(reasons)}"


def print_examples(samples: List[Dict], num_examples: int = 5):
    """Print example samples."""
    print(f"\n{'='*80}")
    print(f"Sample Examples (showing {min(num_examples, len(samples))} of {len(samples)})")
    print(f"{'='*80}\n")
    
    for i, sample in enumerate(samples[:num_examples], 1):
        print(f"Example {i}:")
        print(f"Video ID: {sample['video_id']}")
        print(f"Caption Type: {sample['caption_type']}")
        print(f"Status: {sample['status']}")
        print(f"Rating Score: {sample.get('initial_caption_rating_score', 'N/A')}")
        print(f"Caption Length: {sample['caption_length']} chars")
        print(f"Final Caption: {sample['final_caption'][:200]}...")
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
    
    # Analyze caption length statistics
    yes_lengths = [s['caption_length'] for s in yes_samples]
    no_lengths = [s['caption_length'] for s in no_samples]
    
    avg_yes_length = sum(yes_lengths) / len(yes_lengths) if yes_lengths else 0
    avg_no_length = sum(no_lengths) / len(no_lengths) if no_lengths else 0
    
    # Start building report
    report = f"""# Mostly Static Camera Critique Detection Report

## Dataset Information

- **Source Export File**: {export_file}
- **Total Captions (Approved/Rejected only)**: {stats['total_approved_rejected']}
- **Non-5-Score Pre-Captions (have critiques)**: {stats['non_5_score_count']} ({stats['non_5_score_count']/stats['total_approved_rejected']*100:.2f}%)
- **Sampled for Analysis**: {total} samples (all from non-5-score pre-captions)
- **Random Seed**: {seed}
- **Timestamp**: {timestamp}

## Detection Criteria

A sample is classified as "Yes" if ALL of the following are true:
1. Pre-caption rating is NOT 5 (has a critique) - already filtered
2. Final caption contains "mostly static" (case-insensitive)
3. Critique/feedback contains "mostly static" (case-insensitive)
4. Pre-caption does NOT contain "mostly static"

This identifies cases where annotators added "mostly static" via their critique.

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage | Avg Caption Length |
|-------|-------|------------|---------------------|
| Yes (Critique added "mostly static") | {yes_count} | {yes_pct:.2f}% | {avg_yes_length:.0f} chars |
| No (Not matching criteria) | {no_count} | {no_pct:.2f}% | {avg_no_length:.0f} chars |
| **Total** | {total} | 100.00% | - |

"""

    # Add sample examples section - only show Yes samples
    if yes_samples:
        report += f"## All Critiques That Added 'Mostly Static' ({len(yes_samples)} total)\n\n"
        for i, example in enumerate(yes_samples, 1):
            report += f"### Example {i}/{len(yes_samples)}\n\n"
            report += f"**Video ID**: {example['video_id']}\n\n"
            report += f"**Caption Type**: {example['caption_type']}\n\n"
            report += f"**Status**: {example['status']}\n\n"
            report += f"**Rating Score**: {example.get('initial_caption_rating_score', 'N/A')}\n\n"
            report += f"**Pre-Caption**:\n\n```\n{example['pre_caption']}\n```\n\n"
            report += f"**Final Feedback (Critique)**:\n\n```\n{example['final_feedback']}\n```\n\n"
            report += f"**Final Caption**:\n\n```\n{example['final_caption']}\n```\n\n"
            report += f"**Detection Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += "---\n\n"
    else:
        report += "## Results\n\nNo samples found matching the criteria.\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect critiques that added 'mostly static' to captions"
    )
    parser.add_argument(
        '--export-file',
        type=str,
        default='caption_export/export_20260112_1158/all_videos_with_captions_20260112_1158.json',
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
    
    # Generate run directory name
    if args.sample_count == -1:
        run_dir = f"mostly_static_critique_analysis_full_{timestamp}"
    else:
        run_dir = f"mostly_static_critique_analysis_seed{args.seed}_{timestamp}"
    
    output_dir = export_path.parent / run_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Mostly Static Camera Critique Detection")
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
        export_data, args.sample_count, args.seed
    )
    
    print(f"\n{'='*80}")
    print("Dataset Statistics:")
    print(f"{'='*80}")
    print(f"Total captions (approved/rejected status only): {stats['total_approved_rejected']}")
    print(f"Non-5-score pre-captions (have critiques): {stats['non_5_score_count']} ({stats['non_5_score_count']/stats['total_approved_rejected']*100:.2f}%)")
    print(f"Sampled for analysis: {len(samples)}")
    print(f"{'='*80}")
    
    # Print examples
    print_examples(samples, num_examples=5)
    
    # Classify samples (no LLM needed - simple string matching)
    print(f"\n{'='*80}")
    print(f"Detecting critiques that added 'mostly static'...")
    print(f"{'='*80}\n")
    
    for i, sample in enumerate(samples):
        label, rationale = classify_mostly_static_critique(sample)
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
    print(f"Critique added 'mostly static' (Yes): {yes_count} ({yes_count/len(samples)*100:.2f}%)")
    print(f"Not matching criteria (No): {no_count} ({no_count/len(samples)*100:.2f}%)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()