#!/usr/bin/env python3
"""
Detect Minor Nitpick Critiques Script

Analyzes final_feedback from caption export data to detect which critiques
consist only of minor nitpicks (e.g., formatting changes, trivial wording changes).

Uses GPT-4o to classify each critique as:
- "Yes": Contains ONLY minor nitpicks
- "No": Contains substantial feedback

Output:
- sampled_data.jsonl: All analyzed samples with classifications
- report.md: Summary statistics and examples
"""

import os
import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from llm import get_llm


# GPT-4o Classification Prompt
NITPICK_DETECTION_PROMPT = """You are classifying whether a critique consists ONLY of minor nitpicks or contains substantial feedback.

**Definition of Minor Nitpick:**
A critique is a "minor nitpick" if it suggests:
- Only formatting or stylistic changes (e.g., merging paragraphs, changing line breaks) but not visual content changes
- And only overly brief feedback (e.g., the entire feedback is only 4 to 6 words)

**Instructions:**
1. Read the critique carefully
2. Determine if the critique is a minor nitpick; most of the feedback are not minor nitpicks, please only classify "Yes" if you are very confident
3. Answer ONLY "Yes" (feedback is a minor nitpick) or "No" (contains substantial feedback)
4. Provide a brief rationale explaining your classification

**Critique to classify:**
{final_feedback}

**Format your response as:**
Rationale: [Brief explanation of your reasoning]
Classification: [Yes or No]"""


def load_caption_export(export_path: Path):
    """Load caption export JSON file. Can be either list or dict format."""
    with open(export_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_export_statistics(export_data) -> Dict:
    """
    Analyze export data to count feedback by status and rating.
    
    Returns dict with:
    - total_approved_rejected: Total feedback in approved/rejected status
    - score_4_count: Count of 4-score pre-captions in approved/rejected
    - all_samples_approved_rejected: All samples with approved/rejected status
    - score_4_samples: Samples with 4-score pre-captions
    """
    # Handle both list and dict formats
    if isinstance(export_data, list):
        video_list = export_data
    else:
        video_list = list(export_data.values())
    
    all_samples_approved_rejected = []
    score_4_samples = []
    
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
            
            # Skip perfect pre-captions (no feedback needed)
            feedback_is_needed = caption_info.get('feedback_is_needed', True)
            if not feedback_is_needed:
                continue
            
            final_feedback = caption_info.get('final_feedback', '')
            
            # Safely handle None or non-string types
            if final_feedback is None:
                final_feedback = ''
            elif not isinstance(final_feedback, str):
                final_feedback = str(final_feedback)
            
            final_feedback = final_feedback.strip()
            
            # Only include samples with non-empty final_feedback
            if not final_feedback:
                continue
            
            # Create sample dict
            sample = {
                'video_id': video_id,
                'caption_type': caption_type,
                'status': status,
                'final_feedback': final_feedback,
                'pre_caption': caption_info.get('pre_caption', ''),
                'final_caption': caption_info.get('final_caption', ''),
                'user': caption_info.get('user', ''),
                'timestamp': caption_info.get('timestamp', ''),
                'feedback_length': len(final_feedback),
                'initial_caption_rating_score': caption_info.get('initial_caption_rating_score')
            }
            
            # Add to approved/rejected list
            all_samples_approved_rejected.append(sample)
            
            # Check if it's a 4-score pre-caption
            if sample['initial_caption_rating_score'] == 4:
                score_4_samples.append(sample)
    
    return {
        'total_approved_rejected': len(all_samples_approved_rejected),
        'score_4_count': len(score_4_samples),
        'all_samples_approved_rejected': all_samples_approved_rejected,
        'score_4_samples': score_4_samples
    }


def extract_samples_from_export(export_data, sample_count: int, seed: int) -> Tuple[List[Dict], int, Dict]:
    """
    Extract samples with final_feedback from export data.
    Only extracts 4-score pre-captions from approved/rejected status.
    
    Args:
        export_data: Can be either a list of video objects or a dict keyed by video_id
        sample_count: Number of samples to select (-1 for all)
        seed: Random seed
    
    Returns:
        (samples, total_count, statistics) where:
        - samples: list of sampled 4-score samples
        - total_count: total 4-score samples available
        - statistics: dict with counts by status and rating
    """
    random.seed(seed)
    
    # Get statistics
    stats = analyze_export_statistics(export_data)
    
    # Use only 4-score samples
    all_samples = stats['score_4_samples']
    total_size = len(all_samples)
    
    # Sample
    if sample_count == -1:
        print(f"Using full dataset: {total_size} samples")
        return all_samples, total_size, stats
    elif len(all_samples) < sample_count:
        print(f"Warning: Only {len(all_samples)} samples available, requested {sample_count}")
        return all_samples, total_size, stats
    
    return random.sample(all_samples, sample_count), total_size, stats


def classify_nitpick(final_feedback: str, model: str = "gpt-4o-2024-08-06", secrets=None) -> Tuple[str, str, str]:
    """
    Classify whether a critique is a minor nitpick.
    
    Returns:
        (label, rationale, raw_response)
        label: "Yes" or "No" or "Unexpected"
    """
    prompt = NITPICK_DETECTION_PROMPT.format(final_feedback=final_feedback)
    
    # Load secrets from environment if not provided
    if secrets is None:
        import os
        secrets = {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "gemini_key": os.getenv("GEMINI_API_KEY")
        }
    
    llm = get_llm(model, secrets=secrets)
    
    try:
        response = llm.generate(prompt)
        raw_response = response.strip()
        
        # Parse response
        lines = raw_response.split('\n')
        rationale = ""
        classification = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Rationale:"):
                rationale = line.replace("Rationale:", "").strip()
            elif line.startswith("Classification:"):
                classification = line.replace("Classification:", "").strip()
        
        # Validate classification
        if classification in ["Yes", "No"]:
            return classification, rationale, raw_response
        else:
            return "Unexpected", rationale, raw_response
            
    except Exception as e:
        print(f"Error classifying: {e}")
        return "Unexpected", f"Error: {str(e)}", str(e)


def classify_sample_worker(sample: Dict, model: str, secrets: Dict) -> Dict:
    """Worker function to classify a single sample (for parallel processing)"""
    label, rationale, raw_response = classify_nitpick(
        sample['final_feedback'],
        model=model,
        secrets=secrets
    )
    sample['label'] = label
    sample['rationale'] = rationale
    sample['raw_response'] = raw_response
    return sample


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
    unexpected_samples = [s for s in samples if s['label'] == 'Unexpected']
    
    yes_count = len(yes_samples)
    no_count = len(no_samples)
    unexpected_count = len(unexpected_samples)
    
    yes_pct = (yes_count / total * 100) if total > 0 else 0
    no_pct = (no_count / total * 100) if total > 0 else 0
    unexpected_pct = (unexpected_count / total * 100) if total > 0 else 0
    
    # Analyze feedback length statistics
    yes_lengths = [s['feedback_length'] for s in yes_samples]
    no_lengths = [s['feedback_length'] for s in no_samples]
    
    avg_yes_length = sum(yes_lengths) / len(yes_lengths) if yes_lengths else 0
    avg_no_length = sum(no_lengths) / len(no_lengths) if no_lengths else 0
    
    # Start building report
    report = f"""# Minor Nitpick Detection Analysis Report

## Dataset Information

- **Source Export File**: {export_file}
- **Total Feedback (Approved/Rejected only)**: {stats['total_approved_rejected']}
- **4-Score Pre-Captions**: {stats['score_4_count']} ({stats['score_4_count']/stats['total_approved_rejected']*100:.2f}% of approved/rejected)
- **Sampled for Analysis**: {total} samples (all from 4-score pre-captions)
- **Random Seed**: {seed}
- **Timestamp**: {timestamp}

## Classification Prompt

The following prompt was used to classify critiques:

```
{NITPICK_DETECTION_PROMPT}
```

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage | Avg Feedback Length |
|-------|-------|------------|---------------------|
| Yes (Minor Nitpick Only) | {yes_count} | {yes_pct:.2f}% | {avg_yes_length:.0f} chars |
| No (Substantial Feedback) | {no_count} | {no_pct:.2f}% | {avg_no_length:.0f} chars |
| Unexpected | {unexpected_count} | {unexpected_pct:.2f}% | - |
| **Total** | {total} | 100.00% | - |

"""

    if unexpected_count > 0:
        report += f"\n⚠️ **Warning**: {unexpected_count} samples received unexpected responses from the classifier.\n\n"
    
    # Add sample examples section
    report += "## Sample Examples\n\n"
    
    # Show ALL examples for each category
    yes_examples = yes_samples  # Show all nitpicks
    no_examples = random.sample(no_samples, min(20, len(no_samples))) if no_samples else []  # Still limit substantial feedback to 20
    
    if yes_examples:
        report += f"### Minor Nitpicks Only - Yes ({len(yes_examples)} shown)\n\n"
        for i, example in enumerate(yes_examples, 1):
            report += f"#### Yes Example {i}\n\n"
            report += f"**Video ID**: {example['video_id']}\n\n"
            report += f"**Caption Type**: {example['caption_type']}\n\n"
            report += f"**Status**: {example['status']}\n\n"
            report += f"**Rating Score**: {example.get('initial_caption_rating_score', 'N/A')}\n\n"
            report += f"**Feedback Length**: {example['feedback_length']} chars\n\n"
            report += f"**Final Feedback**: {example['final_feedback']}\n\n"
            report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += f"**Classification**: {example['label']}\n\n"
            report += "---\n\n"
    
    if no_examples:
        report += f"### Substantial Feedback - No ({len(no_examples)} shown)\n\n"
        for i, example in enumerate(no_examples, 1):
            report += f"#### No Example {i}\n\n"
            report += f"**Video ID**: {example['video_id']}\n\n"
            report += f"**Caption Type**: {example['caption_type']}\n\n"
            report += f"**Status**: {example['status']}\n\n"
            report += f"**Rating Score**: {example.get('initial_caption_rating_score', 'N/A')}\n\n"
            report += f"**Feedback Length**: {example['feedback_length']} chars\n\n"
            report += f"**Final Feedback**: {example['final_feedback']}\n\n"
            report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
            report += f"**Classification**: {example['label']}\n\n"
            report += "---\n\n"
    
    # All samples in sequence
    report += "## All Samples (Complete Sequence)\n\n"
    for i, sample in enumerate(samples, 1):
        report += f"### Sample {i}/{total} - [{sample['label']}]\n\n"
        report += f"**Video ID**: {sample['video_id']}\n\n"
        report += f"**Caption Type**: {sample['caption_type']}\n\n"
        report += f"**Status**: {sample['status']}\n\n"
        report += f"**Rating Score**: {sample.get('initial_caption_rating_score', 'N/A')}\n\n"
        report += f"**Feedback Length**: {sample['feedback_length']} chars\n\n"
        report += f"**Final Feedback**: {sample['final_feedback']}\n\n"
        report += f"**Rationale**: {sample.get('rationale', 'N/A')}\n\n"
        report += f"**Classification**: {sample['label']}\n\n"
        if sample['label'] == 'Unexpected':
            report += f"**Raw Response**: {sample.get('raw_response', 'N/A')}\n\n"
        report += "---\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect minor nitpick critiques in caption export data"
    )
    parser.add_argument(
        '--export-file',
        type=str,
        default='caption_export/export_20251104_0552/all_videos_with_captions_20251104_0552.json',
        help='Path to caption export JSON file (e.g., caption_export/export_20251104_0552/all_videos_with_captions_20251104_0552.json)'
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
        '--model',
        type=str,
        default='gpt-4o-2024-08-06',
        help='Model to use for classification (default: gpt-4o-2024-08-06)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=30,
        help='Number of parallel workers for classification (default: 30)'
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
    export_basename = export_path.stem
    if args.sample_count == -1:
        run_dir = f"nitpick_analysis_full_dataset_{timestamp}"
    else:
        run_dir = f"nitpick_analysis_seed{args.seed}_{timestamp}"
    
    output_dir = export_path.parent / run_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Minor Nitpick Detection Analysis")
    print(f"{'='*80}\n")
    print(f"Export file: {export_path}")
    print(f"Output directory: {output_dir}")
    print(f"Model: {args.model}")
    print(f"Sample count: {'Full dataset' if args.sample_count == -1 else args.sample_count}")
    print(f"Random seed: {args.seed}")
    print(f"Parallel workers: {args.workers}")
    
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
    print(f"Total feedback (approved/rejected status only): {stats['total_approved_rejected']}")
    print(f"4-Score pre-captions: {stats['score_4_count']} ({stats['score_4_count']/stats['total_approved_rejected']*100:.2f}%)")
    print(f"Sampled for analysis: {len(samples)} (all from 4-score pre-captions)")
    print(f"{'='*80}")
    
    # Print examples
    print_examples(samples, num_examples=5)
    
    # Load secrets for LLM
    secrets = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "gemini_key": os.getenv("GEMINI_API_KEY")
    }
    
    # Classify samples with parallel processing
    print(f"\n{'='*80}")
    print(f"Classifying critiques with {args.model} using {args.workers} workers...")
    print(f"{'='*80}\n")
    
    completed = 0
    progress_lock = Lock()
    
    # Create a mapping to track which sample corresponds to which future
    sample_to_index = {id(sample): idx for idx, sample in enumerate(samples)}
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_index = {}
        for idx, sample in enumerate(samples):
            future = executor.submit(classify_sample_worker, sample, args.model, secrets)
            future_to_index[future] = idx
        
        # Process completed tasks and update samples in place
        for future in as_completed(future_to_index):
            try:
                result = future.result()
                idx = future_to_index[future]
                # Update the original sample in the list
                samples[idx] = result
                
                with progress_lock:
                    completed += 1
                    if completed % 50 == 0 or completed == len(samples):
                        print(f"Progress: {completed}/{len(samples)} ({completed/len(samples)*100:.1f}%)")
            except Exception as e:
                print(f"Error processing sample: {e}")
                # Even on error, mark as unexpected
                idx = future_to_index[future]
                samples[idx]['label'] = 'Unexpected'
                samples[idx]['rationale'] = f'Error: {str(e)}'
                samples[idx]['raw_response'] = str(e)
    
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
    unexpected_count = sum(1 for s in samples if s['label'] == 'Unexpected')
    
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Minor Nitpick Only (Yes): {yes_count} ({yes_count/len(samples)*100:.2f}%)")
    print(f"Substantial Feedback (No): {no_count} ({no_count/len(samples)*100:.2f}%)")
    print(f"Unexpected: {unexpected_count} ({unexpected_count/len(samples)*100:.2f}%)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()