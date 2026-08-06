#!/usr/bin/env python3
"""
Detect Direct Caption Edits Script

Analyzes caption export data to detect cases where:
1. User is "Jiaxi Li"
2. final_caption != gpt_caption (user manually edited instead of using feedback workflow)

This identifies a potentially problematic pattern where users bypass the 
feedback+regeneration workflow and directly edit the GPT-generated caption.

Output:
- sampled_data.jsonl: All detected samples
- report.md: Summary statistics and all examples
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


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
                import re
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


def analyze_user_captions(export_data, target_user: str, url_to_batch: Optional[Dict[str, Tuple[str, int]]] = None) -> Dict:
    """
    Analyze export data to find captions by target user with direct edits.
    
    Args:
        export_data: Export JSON data
        target_user: Username to filter by
        url_to_batch: Optional mapping from video_url to (batch_name, index)
    
    Returns dict with:
    - total_by_user: Total captions by the target user
    - direct_edit_samples: Samples where final_caption != gpt_caption
    - no_edit_samples: Samples where final_caption == gpt_caption
    - perfect_precaption_samples: Samples with rating 5 (no gpt_caption generated)
    """
    if url_to_batch is None:
        url_to_batch = {}
    
    # Handle both list and dict formats
    if isinstance(export_data, list):
        video_list = export_data
    else:
        video_list = list(export_data.values())
    
    direct_edit_samples = []
    no_edit_samples = []
    perfect_precaption_samples = []
    
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
            
            caption_info = caption_data['caption_data']
            user = caption_info.get('user', '')
            
            # Only look at target user's captions
            if user != target_user:
                continue
            
            status = caption_data.get('status', '')
            final_caption = caption_info.get('final_caption', '') or ''
            gpt_caption = caption_info.get('gpt_caption', '') or ''
            pre_caption = caption_info.get('pre_caption', '') or ''
            final_feedback = caption_info.get('final_feedback', '') or ''
            initial_feedback = caption_info.get('initial_feedback', '') or ''
            initial_rating = caption_info.get('initial_caption_rating_score')
            workflow_type = caption_info.get('workflow_type', '')
            
            # Create sample dict
            sample = {
                'video_id': video_id,
                'video_url': video_url,
                'batch_file': batch_file,
                'batch_index': batch_index,
                'caption_type': caption_type,
                'status': status,
                'user': user,
                'timestamp': caption_info.get('timestamp', ''),
                'initial_caption_rating_score': initial_rating,
                'workflow_type': workflow_type,
                'pre_caption': pre_caption.strip(),
                'initial_feedback': initial_feedback.strip(),
                'final_feedback': final_feedback.strip(),
                'gpt_caption': gpt_caption.strip(),
                'final_caption': final_caption.strip(),
            }
            
            # Classify based on workflow
            if initial_rating == 5:
                # Perfect precaption - no gpt_caption generated
                sample['edit_type'] = 'perfect_precaption'
                perfect_precaption_samples.append(sample)
            elif not gpt_caption:
                # No gpt_caption but rating != 5 (unusual case)
                sample['edit_type'] = 'missing_gpt_caption'
                direct_edit_samples.append(sample)
            elif final_caption.strip() != gpt_caption.strip():
                # Direct edit detected
                sample['edit_type'] = 'direct_edit'
                direct_edit_samples.append(sample)
            else:
                # No edit - accepted gpt_caption as-is
                sample['edit_type'] = 'no_edit'
                no_edit_samples.append(sample)
    
    total_by_user = len(direct_edit_samples) + len(no_edit_samples) + len(perfect_precaption_samples)
    
    return {
        'total_by_user': total_by_user,
        'direct_edit_samples': direct_edit_samples,
        'no_edit_samples': no_edit_samples,
        'perfect_precaption_samples': perfect_precaption_samples,
    }


def compute_diff_summary(gpt_caption: str, final_caption: str) -> str:
    """Compute a simple diff summary between gpt_caption and final_caption."""
    gpt_words = set(gpt_caption.lower().split())
    final_words = set(final_caption.lower().split())
    
    added = final_words - gpt_words
    removed = gpt_words - final_words
    
    summary_parts = []
    if added:
        summary_parts.append(f"Added: {', '.join(list(added)[:10])}")
    if removed:
        summary_parts.append(f"Removed: {', '.join(list(removed)[:10])}")
    
    if not summary_parts:
        return "Minor changes (punctuation/formatting)"
    
    return "; ".join(summary_parts)


def compute_line_diff(gpt_caption: str, final_caption: str) -> str:
    """
    Compute a line-based diff using GitHub's diff code block format.
    Lines starting with - are shown in red (deletions)
    Lines starting with + are shown in green (additions)
    """
    import difflib
    
    # Split into sentences for more readable diff
    import re
    
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        # Split on period, exclamation, question mark followed by space or end
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    gpt_sentences = split_into_sentences(gpt_caption)
    final_sentences = split_into_sentences(final_caption)
    
    # If only one sentence each, split by clauses (commas) instead
    if len(gpt_sentences) <= 1 and len(final_sentences) <= 1:
        gpt_sentences = [s.strip() for s in gpt_caption.split(',') if s.strip()]
        final_sentences = [s.strip() for s in final_caption.split(',') if s.strip()]
    
    # Generate unified diff
    diff_lines = list(difflib.unified_diff(
        gpt_sentences, 
        final_sentences, 
        lineterm='',
        n=0  # No context lines
    ))
    
    # Filter out header lines and format for GitHub diff block
    result_lines = []
    for line in diff_lines:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            continue
        if line.startswith('-'):
            result_lines.append(f"- {line[1:].strip()}")
        elif line.startswith('+'):
            result_lines.append(f"+ {line[1:].strip()}")
    
    if not result_lines:
        # If no diff detected (maybe just whitespace), show simple comparison
        return f"- {gpt_caption}\n+ {final_caption}"
    
    return '\n'.join(result_lines)


def generate_report(results: Dict, target_user: str, timestamp: str, 
                   output_path: Path, export_file: str):
    """Generate markdown report with statistics and all examples."""
    
    direct_edit_samples = results['direct_edit_samples']
    no_edit_samples = results['no_edit_samples']
    perfect_precaption_samples = results['perfect_precaption_samples']
    total = results['total_by_user']
    
    direct_count = len(direct_edit_samples)
    no_edit_count = len(no_edit_samples)
    perfect_count = len(perfect_precaption_samples)
    
    direct_pct = (direct_count / total * 100) if total > 0 else 0
    no_edit_pct = (no_edit_count / total * 100) if total > 0 else 0
    perfect_pct = (perfect_count / total * 100) if total > 0 else 0
    
    # Start building report
    report = f"""# Direct Caption Edit Detection Report

## Overview

This report identifies cases where **{target_user}** manually edited the GPT-generated caption 
instead of using the feedback refinement workflow (re-polish feedback + re-generate caption).

**Why this matters**: Direct edits bypass the intended workflow where users should:
1. Provide feedback on the pre-caption
2. Let GPT polish the feedback and generate a refined caption
3. If unhappy, re-polish feedback and regenerate (not directly edit)

Direct edits may indicate:
- User found it faster to edit directly than iterate through feedback
- Potential quality issues if edits are substantial
- Workflow friction that should be addressed

## Dataset Information

- **Source Export File**: `{export_file}`
- **Target User**: {target_user}
- **Analysis Timestamp**: {timestamp}

## Detection Criteria

A caption is flagged as "Direct Edit" if:
1. `initial_caption_rating_score` != 5 (went through feedback workflow)
2. `gpt_caption` exists (GPT generated a caption)
3. `final_caption` != `gpt_caption` (user modified the GPT output)

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Direct Edits** (final != gpt) | {direct_count} | {direct_pct:.1f}% |
| No Edits (final == gpt) | {no_edit_count} | {no_edit_pct:.1f}% |
| Perfect Pre-caption (rating=5) | {perfect_count} | {perfect_pct:.1f}% |
| **Total by {target_user}** | {total} | 100.0% |

"""

    # Sort direct edit samples by timestamp (latest first)
    direct_edit_samples_sorted = sorted(
        direct_edit_samples, 
        key=lambda x: x.get('timestamp', ''), 
        reverse=True
    )
    
    # Add direct edit examples
    if direct_edit_samples_sorted:
        report += f"""## ⚠️ Direct Edit Cases ({direct_count} total)

These are cases where the user manually edited the GPT-generated caption.
Sorted by timestamp (latest first).

"""
        for i, sample in enumerate(direct_edit_samples_sorted, 1):
            diff_summary = compute_diff_summary(sample['gpt_caption'], sample['final_caption'])
            line_diff = compute_line_diff(sample['gpt_caption'], sample['final_caption'])
            
            report += f"""### Case {i}/{direct_count}

| Field | Value |
|-------|-------|
| Video ID | `{sample['video_id']}` |
| Batch File | `{sample['batch_file']}` |
| Batch Index | {sample['batch_index']} |
| Caption Type | {sample['caption_type']} |
| Status | {sample['status']} |
| Rating Score | {sample['initial_caption_rating_score']} |
| Timestamp | {sample['timestamp']} |

**Pre-Caption:**

> {sample['pre_caption']}

**Initial Feedback:**

> {sample['initial_feedback'] if sample['initial_feedback'] else '(empty)'}

**Final Feedback:**

> {sample['final_feedback'] if sample['final_feedback'] else '(empty)'}

**GPT Caption (before edit):**

> {sample['gpt_caption']}

**Final Caption (after manual edit):**

> {sample['final_caption']}

**Diff:**

```diff
{line_diff}
```

**Change Summary:** {diff_summary}

---

"""
    else:
        report += "## Results\n\nNo direct edit cases found for this user.\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect direct caption edits (final_caption != gpt_caption) by a specific user"
    )
    parser.add_argument(
        '--export-file',
        type=str,
        default='caption_export/export_20260112_1158/all_videos_with_captions_20260112_1158.json',
        help='Path to caption export JSON file'
    )
    parser.add_argument(
        '--user',
        type=str,
        default='Jiaxi Li',
        help='Target user to analyze (default: "Jiaxi Li")'
    )
    parser.add_argument(
        '--batch-files',
        type=str,
        nargs='*',
        default=[],
        help='Paths to batch JSON files (each contains a list of video URLs) to map videos to batches'
    )
    
    args = parser.parse_args()
    
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
    
    # Generate output directory
    safe_user = args.user.replace(' ', '_').lower()
    run_dir = f"direct_edit_analysis_{safe_user}_{timestamp}"
    output_dir = export_path.parent / run_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Direct Caption Edit Detection")
    print(f"{'='*80}\n")
    print(f"Export file: {export_path}")
    print(f"Target user: {args.user}")
    print(f"Output directory: {output_dir}")
    
    # Load export data
    print(f"\nLoading export data...")
    export_data = load_caption_export(export_path)
    
    # Analyze user captions
    print(f"Analyzing captions by {args.user}...")
    results = analyze_user_captions(export_data, args.user, url_to_batch)
    
    # Print summary
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Total captions by {args.user}: {results['total_by_user']}")
    print(f"Direct edits (final != gpt): {len(results['direct_edit_samples'])}")
    print(f"No edits (final == gpt): {len(results['no_edit_samples'])}")
    print(f"Perfect pre-caption (rating=5): {len(results['perfect_precaption_samples'])}")
    print(f"{'='*80}\n")
    
    # Save sampled data
    sampled_data_path = output_dir / 'direct_edit_samples.jsonl'
    with open(sampled_data_path, 'w', encoding='utf-8') as f:
        for sample in results['direct_edit_samples']:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    print(f"✅ Direct edit samples saved to: {sampled_data_path}")
    
    # Generate report
    report_path = output_dir / 'report.md'
    generate_report(
        results,
        args.user,
        timestamp,
        report_path,
        str(export_path)
    )
    
    # Final summary
    if results['direct_edit_samples']:
        print(f"\n⚠️  Found {len(results['direct_edit_samples'])} direct edit cases!")
        print(f"   Review the report for details: {report_path}")
    else:
        print(f"\n✅ No direct edit cases found for {args.user}")


if __name__ == "__main__":
    main()