#!/usr/bin/env python3
"""
Recovery Script: Generate Report from Existing sampled_data.jsonl

This script loads the already-classified samples from sampled_data.jsonl
and generates the report without re-running classification.

Can also complete missing classifications with --complete-missing flag.

Usage:
    # Just generate report
    python generate_report_from_jsonl.py --jsonl-file caption_export/.../sampled_data.jsonl
    
    # Complete missing classifications and generate report
    python generate_report_from_jsonl.py --jsonl-file caption_export/.../sampled_data.jsonl --complete-missing
"""

import json
import random
import argparse
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from dotenv import load_dotenv

from llm import get_llm


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


def load_samples_from_jsonl(jsonl_path: Path) -> List[Dict]:
    """Load samples from JSONL file."""
    samples = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    return samples


def calculate_statistics(samples: List[Dict]) -> Dict:
    """Calculate statistics from samples."""
    total_approved_rejected = len(samples)
    score_4_count = len([s for s in samples if s.get('initial_caption_rating_score') == 4])
    
    return {
        'total_approved_rejected': total_approved_rejected,
        'score_4_count': score_4_count
    }


def classify_nitpick(final_feedback: str, model: str = "gpt-4o-2024-08-06", secrets=None) -> Tuple[str, str, str]:
    """Classify whether a critique is a minor nitpick."""
    prompt = NITPICK_DETECTION_PROMPT.format(final_feedback=final_feedback)
    
    if secrets is None:
        secrets = {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "gemini_key": os.getenv("GEMINI_API_KEY")
        }
    
    llm = get_llm(model, secrets=secrets)
    
    try:
        response = llm.generate(prompt)
        raw_response = response.strip()
        
        lines = raw_response.split('\n')
        rationale = ""
        classification = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Rationale:"):
                rationale = line.replace("Rationale:", "").strip()
            elif line.startswith("Classification:"):
                classification = line.replace("Classification:", "").strip()
        
        if classification in ["Yes", "No"]:
            return classification, rationale, raw_response
        else:
            return "Unexpected", rationale, raw_response
            
    except Exception as e:
        return "Unexpected", f"Error: {str(e)}", str(e)


def classify_sample_worker(sample: Dict, model: str, secrets: Dict) -> Dict:
    """Worker function to classify a single sample."""
    label, rationale, raw_response = classify_nitpick(
        sample['final_feedback'],
        model=model,
        secrets=secrets
    )
    sample['label'] = label
    sample['rationale'] = rationale
    sample['raw_response'] = raw_response
    return sample


def complete_missing_classifications(samples: List[Dict], model: str = "gpt-4o-2024-08-06", 
                                     workers: int = 30) -> List[Dict]:
    """Complete classifications for samples missing labels."""
    
    # Find samples without labels
    missing_samples = [(idx, s) for idx, s in enumerate(samples) if 'label' not in s]
    
    if not missing_samples:
        print("No missing classifications found!")
        return samples
    
    print(f"\nFound {len(missing_samples)} samples missing classifications")
    print(f"Completing with {workers} workers...")
    
    # Load secrets
    secrets = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "gemini_key": os.getenv("GEMINI_API_KEY")
    }
    
    completed = 0
    progress_lock = Lock()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {}
        for idx, sample in missing_samples:
            future = executor.submit(classify_sample_worker, sample, model, secrets)
            future_to_index[future] = idx
        
        for future in as_completed(future_to_index):
            try:
                result = future.result()
                idx = future_to_index[future]
                samples[idx] = result
                
                with progress_lock:
                    completed += 1
                    if completed % 50 == 0 or completed == len(missing_samples):
                        print(f"Progress: {completed}/{len(missing_samples)} ({completed/len(missing_samples)*100:.1f}%)")
            except Exception as e:
                print(f"Error: {e}")
                idx = future_to_index[future]
                samples[idx]['label'] = 'Unexpected'
                samples[idx]['rationale'] = f'Error: {str(e)}'
                samples[idx]['raw_response'] = str(e)
    
    print(f"✅ Completed {len(missing_samples)} classifications\n")
    return samples


def save_samples_to_jsonl(samples: List[Dict], jsonl_path: Path):
    """Save samples back to JSONL file."""
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    print(f"✅ Updated sampled data saved to: {jsonl_path}")


def generate_report(samples: List[Dict], seed: int, timestamp: str, 
                   output_path: Path, export_file: str, stats: Dict):
    """Generate markdown report with statistics and examples."""
    
    # Calculate statistics
    total = len(samples)
    yes_samples = [s for s in samples if s.get('label') == 'Yes']
    no_samples = [s for s in samples if s.get('label') == 'No']
    unexpected_samples = [s for s in samples if s.get('label') == 'Unexpected']
    
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
        report += f"### Sample {i}/{total} - [{sample.get('label', 'N/A')}]\n\n"
        report += f"**Video ID**: {sample['video_id']}\n\n"
        report += f"**Caption Type**: {sample['caption_type']}\n\n"
        report += f"**Status**: {sample['status']}\n\n"
        report += f"**Rating Score**: {sample.get('initial_caption_rating_score', 'N/A')}\n\n"
        report += f"**Feedback Length**: {sample['feedback_length']} chars\n\n"
        report += f"**Final Feedback**: {sample['final_feedback']}\n\n"
        report += f"**Rationale**: {sample.get('rationale', 'N/A')}\n\n"
        report += f"**Classification**: {sample.get('label', 'N/A')}\n\n"
        if sample.get('label') == 'Unexpected':
            report += f"**Raw Response**: {sample.get('raw_response', 'N/A')}\n\n"
        report += "---\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate report from existing sampled_data.jsonl"
    )
    parser.add_argument(
        '--jsonl-file',
        type=str,
        required=True,
        help='Path to sampled_data.jsonl file'
    )
    parser.add_argument(
        '--complete-missing',
        action='store_true',
        help='Complete missing classifications before generating report'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4o-2024-08-06',
        help='Model to use for completing missing classifications'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=30,
        help='Number of parallel workers for classification'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Load samples
    jsonl_path = Path(args.jsonl_file)
    if not jsonl_path.exists():
        print(f"Error: JSONL file not found: {jsonl_path}")
        return
    
    print(f"Loading samples from: {jsonl_path}")
    samples = load_samples_from_jsonl(jsonl_path)
    print(f"✅ Loaded {len(samples)} samples")
    
    # Check for missing labels
    missing_count = sum(1 for s in samples if 'label' not in s)
    if missing_count > 0:
        print(f"⚠️  Found {missing_count} samples without labels ({missing_count/len(samples)*100:.2f}%)")
        
        if args.complete_missing:
            samples = complete_missing_classifications(samples, args.model, args.workers)
            # Save updated samples
            save_samples_to_jsonl(samples, jsonl_path)
        else:
            print("\nTo complete missing classifications, run with --complete-missing flag")
            print(f"Example: python {Path(__file__).name} --jsonl-file {args.jsonl_file} --complete-missing\n")
    
    # Calculate statistics
    stats = calculate_statistics(samples)
    
    # Generate output paths
    output_dir = jsonl_path.parent
    report_path = output_dir / 'report.md'
    
    # Extract info for report
    export_file = "Unknown"  # Can't determine from jsonl alone
    seed = 100  # Default, can't determine from jsonl
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Try to infer from directory name
    dir_name = output_dir.name
    if 'seed' in dir_name:
        try:
            seed = int(dir_name.split('seed')[1].split('_')[0])
        except:
            pass
    
    print("\nGenerating report...")
    generate_report(
        samples,
        seed,
        timestamp,
        report_path,
        export_file,
        stats
    )
    
    # Print summary
    yes_count = sum(1 for s in samples if s.get('label') == 'Yes')
    no_count = sum(1 for s in samples if s.get('label') == 'No')
    unexpected_count = sum(1 for s in samples if s.get('label') == 'Unexpected')
    missing_label_count = sum(1 for s in samples if 'label' not in s)
    
    # Debug: Check what other labels might exist
    all_labels = set(s.get('label', 'MISSING') for s in samples)
    
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Minor Nitpick Only (Yes): {yes_count} ({yes_count/len(samples)*100:.2f}%)")
    print(f"Substantial Feedback (No): {no_count} ({no_count/len(samples)*100:.2f}%)")
    print(f"Unexpected: {unexpected_count} ({unexpected_count/len(samples)*100:.2f}%)")
    if missing_label_count > 0:
        print(f"Missing label: {missing_label_count} ({missing_label_count/len(samples)*100:.2f}%)")
    print(f"Total samples: {len(samples)}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()