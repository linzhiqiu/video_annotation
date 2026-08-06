#!/usr/bin/env python3
"""
Analyze video_labels folders and show statistics for raw/train/test splits.

Usage:
    python analyze_video_labels.py
    python analyze_video_labels.py --video_labels_dir path/to/video_labels
    python analyze_video_labels.py --folder_name motion_dataset
"""

import json
import os
import argparse
from pathlib import Path
from collections import defaultdict
import random


def find_sampled_tasks_folders(video_labels_dir):
    """Find all folders containing sampled_tasks.json files."""
    video_labels_path = Path(video_labels_dir)
    sampled_tasks_files = []
    
    if not video_labels_path.exists():
        print(f"❌ Error: {video_labels_dir} does not exist!")
        return []
    
    # Search for sampled_tasks.json files
    for root, dirs, files in os.walk(video_labels_path):
        if "sampled_tasks.json" in files:
            sampled_tasks_files.append(Path(root))
    
    return sorted(sampled_tasks_files)


def load_sampled_tasks(folder_path):
    """Load sampled_tasks.json from a folder."""
    json_path = folder_path / "sampled_tasks.json"
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {json_path}: {e}")
        return None


def load_original_tasks(folder_path):
    """Load original_tasks.json from a folder (contains TRUE imbalanced data)."""
    json_path = folder_path / "original_tasks.json"
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load {json_path}: {e}")
        print(f"   (This file contains the true imbalanced data)")
        return None


def analyze_tasks(sampled_tasks, split_name="raw"):
    """Analyze tasks for a specific split (raw/train/test)."""
    if split_name not in sampled_tasks:
        return None
    
    split_data = sampled_tasks[split_name]
    
    # Collect statistics
    stats = []
    for skill_name, tasks in split_data.items():
        for task_name, task_data in tasks.items():
            pos_count = len(task_data.get('pos', []))
            neg_count = len(task_data.get('neg', []))
            min_count = min(pos_count, neg_count)
            imbalance = abs(pos_count - neg_count)
            
            stats.append({
                'skill': skill_name,
                'task': task_name,
                'pos': pos_count,
                'neg': neg_count,
                'min': min_count,
                'imbalance': imbalance
            })
    
    return stats


def print_split_summary(stats, split_name):
    """Print summary statistics for a split."""
    if not stats:
        print(f"  No data for {split_name}")
        return
    
    total_actual_pos = sum(s['pos'] for s in stats)
    total_actual_neg = sum(s['neg'] for s in stats)
    total_min = sum(s['min'] for s in stats)
    total_imbalance = sum(s['imbalance'] for s in stats)
    total_tasks = len(stats)
    
    # Check if this split is balanced
    is_balanced = total_actual_pos == total_actual_neg
    balance_emoji = "⚖️ BALANCED" if is_balanced else "⚠️ IMBALANCED"
    
    print(f"\n  📊 {split_name.upper()} Summary ({balance_emoji}):")
    print(f"     Total Tasks: {total_tasks}")
    
    # Show actual totals (different for imbalanced, same for balanced)
    if not is_balanced:
        print(f"     Total ACTUAL Pos Videos: {total_actual_pos:,}")
        print(f"     Total ACTUAL Neg Videos: {total_actual_neg:,}")
        print(f"     → Difference: {abs(total_actual_pos - total_actual_neg):,} videos")
        print(f"     Total Balanced Pairs Available: {total_min:,}")
    else:
        print(f"     Total Pos Samples: {total_actual_pos:,}")
        print(f"     Total Neg Samples: {total_actual_neg:,}")
        print(f"     Total Balanced Pairs: {total_min:,}")
    
    print(f"     Avg Pos per Task: {total_actual_pos/total_tasks:.1f}")
    print(f"     Avg Neg per Task: {total_actual_neg/total_tasks:.1f}")
    
    if not is_balanced:
        print(f"     Avg Imbalance per Task: {total_imbalance/total_tasks:.1f}")
        print(f"     → This means tasks have different pos/neg counts!")


def print_task_examples(stats, split_name, num_examples=3):
    """Print example tasks with most/least samples."""
    if not stats:
        return
    
    # Sort by different criteria
    by_min = sorted(stats, key=lambda x: x['min'])
    by_pos = sorted(stats, key=lambda x: x['pos'])
    by_imbalance = sorted(stats, key=lambda x: x['imbalance'], reverse=True)
    
    print(f"\n  🔝 {split_name.upper()} - Tasks with MOST balanced pairs:")
    for stat in by_min[-num_examples:]:
        print(f"     • {stat['skill']}.{stat['task'][:40]}")
        print(f"       Pos: {stat['pos']}, Neg: {stat['neg']}, Min: {stat['min']}, Imbalance: {stat['imbalance']}")
    
    print(f"\n  🔻 {split_name.upper()} - Tasks with LEAST balanced pairs:")
    for stat in by_min[:num_examples]:
        print(f"     • {stat['skill']}.{stat['task'][:40]}")
        print(f"       Pos: {stat['pos']}, Neg: {stat['neg']}, Min: {stat['min']}, Imbalance: {stat['imbalance']}")
    
    print(f"\n  ⚖️  {split_name.upper()} - Most IMBALANCED tasks (|pos-neg|):")
    for stat in by_imbalance[:num_examples]:
        print(f"     • {stat['skill']}.{stat['task'][:40]}")
        print(f"       Pos: {stat['pos']}, Neg: {stat['neg']}, Min: {stat['min']}, Imbalance: {stat['imbalance']}")
    
    # Random examples
    print(f"\n  🎲 {split_name.upper()} - Random sample tasks:")
    random_stats = random.sample(stats, min(num_examples, len(stats)))
    for stat in random_stats:
        print(f"     • {stat['skill']}.{stat['task'][:40]}")
        print(f"       Pos: {stat['pos']}, Neg: {stat['neg']}, Min: {stat['min']}, Imbalance: {stat['imbalance']}")


def compare_splits(sampled_tasks, original_tasks=None):
    """Compare raw vs train vs test splits."""
    print("\n" + "="*80)
    print("📈 COMPARING RAW vs TRAIN vs TEST SPLITS")
    print("="*80)
    
    # Get video counts
    train_videos = sampled_tasks.get('train_videos', [])
    test_videos = sampled_tasks.get('test_videos', [])
    
    print(f"\n🎬 Video Split:")
    print(f"   Train Videos: {len(train_videos)}")
    print(f"   Test Videos: {len(test_videos)}")
    print(f"   Total Videos: {len(train_videos) + len(test_videos)}")
    
    # Check for overlap (should be none)
    overlap = set(train_videos) & set(test_videos)
    if overlap:
        print(f"   ⚠️  WARNING: {len(overlap)} videos appear in BOTH train and test!")
    else:
        print(f"   ✅ No overlap between train and test (correct!)")
    
    # Analyze ORIGINAL tasks (imbalanced) if available
    if original_tasks:
        print("\n" + "="*80)
        print("📊 ORIGINAL (IMBALANCED) DATA")
        print("="*80)
        for split_name in ['raw', 'train', 'test']:
            if split_name in original_tasks:
                stats = analyze_tasks(original_tasks, split_name)
                if stats:
                    print_split_summary(stats, f"ORIGINAL-{split_name}")
    
    # Analyze SAMPLED tasks (balanced)
    print("\n" + "="*80)
    print("📊 SAMPLED (BALANCED) DATA")
    print("="*80)
    for split_name in ['raw', 'train', 'test']:
        stats = analyze_tasks(sampled_tasks, split_name)
        if stats:
            print_split_summary(stats, f"SAMPLED-{split_name}")


def analyze_skill_distribution(sampled_tasks):
    """Analyze distribution of tasks across skills."""
    print("\n" + "="*80)
    print("🎯 SKILL DISTRIBUTION ANALYSIS")
    print("="*80)
    
    for split_name in ['raw', 'train', 'test']:
        if split_name not in sampled_tasks:
            continue
        
        split_data = sampled_tasks[split_name]
        skill_counts = defaultdict(lambda: {'tasks': 0, 'pos': 0, 'neg': 0, 'min': 0})
        
        for skill_name, tasks in split_data.items():
            for task_name, task_data in tasks.items():
                pos_count = len(task_data.get('pos', []))
                neg_count = len(task_data.get('neg', []))
                
                skill_counts[skill_name]['tasks'] += 1
                skill_counts[skill_name]['pos'] += pos_count
                skill_counts[skill_name]['neg'] += neg_count
                skill_counts[skill_name]['min'] += min(pos_count, neg_count)
        
        print(f"\n📊 {split_name.upper()} - Skills Summary:")
        print(f"{'Skill':<40} {'Tasks':<8} {'Pos':<8} {'Neg':<8} {'Min':<8}")
        print("-" * 80)
        
        for skill_name in sorted(skill_counts.keys()):
            counts = skill_counts[skill_name]
            print(f"{skill_name:<40} {counts['tasks']:<8} {counts['pos']:<8} {counts['neg']:<8} {counts['min']:<8}")


def verify_train_test_split(sampled_tasks):
    """Verify that train and test splits are properly separated."""
    print("\n" + "="*80)
    print("🔍 VERIFYING TRAIN/TEST SPLIT INTEGRITY")
    print("="*80)
    
    train_videos_set = set(sampled_tasks.get('train_videos', []))
    test_videos_set = set(sampled_tasks.get('test_videos', []))
    
    # Check for overlaps
    overlap = train_videos_set & test_videos_set
    print(f"\n✓ Video-level check:")
    print(f"  Train videos: {len(train_videos_set)}")
    print(f"  Test videos: {len(test_videos_set)}")
    print(f"  Overlap: {len(overlap)}")
    
    if overlap:
        print(f"  ❌ FAIL: {len(overlap)} videos in both train and test!")
        print(f"  Example overlapping videos: {list(overlap)[:5]}")
    else:
        print(f"  ✅ PASS: No video overlap")
    
    # Check task videos
    print(f"\n✓ Task-level check:")
    train_data = sampled_tasks.get('train', {})
    test_data = sampled_tasks.get('test', {})
    
    train_violations = []
    test_violations = []
    
    # Check train tasks
    for skill_name, tasks in train_data.items():
        for task_name, task_data in tasks.items():
            pos_videos = set(task_data.get('pos', []))
            neg_videos = set(task_data.get('neg', []))
            
            # Check if any train task videos are in test set
            if pos_videos & test_videos_set:
                train_violations.append(f"{skill_name}.{task_name} (pos)")
            if neg_videos & test_videos_set:
                train_violations.append(f"{skill_name}.{task_name} (neg)")
    
    # Check test tasks
    for skill_name, tasks in test_data.items():
        for task_name, task_data in tasks.items():
            pos_videos = set(task_data.get('pos', []))
            neg_videos = set(task_data.get('neg', []))
            
            # Check if any test task videos are in train set
            if pos_videos & train_videos_set:
                test_violations.append(f"{skill_name}.{task_name} (pos)")
            if neg_videos & train_videos_set:
                test_violations.append(f"{skill_name}.{task_name} (neg)")
    
    if train_violations:
        print(f"  ❌ FAIL: {len(train_violations)} train tasks have videos in test set!")
        print(f"  Examples: {train_violations[:5]}")
    else:
        print(f"  ✅ PASS: All train task videos are in train set")
    
    if test_violations:
        print(f"  ❌ FAIL: {len(test_violations)} test tasks have videos in train set!")
        print(f"  Examples: {test_violations[:5]}")
    else:
        print(f"  ✅ PASS: All test task videos are in test set")


def analyze_folder(folder_path, num_examples=3):
    """Analyze a single sampled_tasks folder."""
    print("\n" + "="*80)
    print(f"📁 ANALYZING: {folder_path}")
    print("="*80)
    
    # Load sampled data (balanced)
    sampled_tasks = load_sampled_tasks(folder_path)
    if not sampled_tasks:
        return
    
    # Load original data (imbalanced) - THIS IS THE KEY!
    original_tasks = load_original_tasks(folder_path)
    
    # Load config if exists
    config_path = folder_path / "sampled_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            print(f"\n⚙️  Configuration:")
            print(f"   Max Samples: {config.get('max_samples', 'N/A')}")
            print(f"   Sampling: {config.get('sampling', 'N/A')}")
            print(f"   Train Ratio: {config.get('train_ratio', 'N/A')}")
            print(f"   Seed: {config.get('seed', 'N/A')}")
    
    # Compare splits (now with original tasks!)
    compare_splits(sampled_tasks, original_tasks)
    
    # Verify train/test integrity
    verify_train_test_split(sampled_tasks)
    
    # Analyze skill distribution
    analyze_skill_distribution(sampled_tasks)
    
    # Show examples for ORIGINAL (imbalanced) data
    if original_tasks:
        print("\n" + "="*80)
        print("📋 ORIGINAL (IMBALANCED) TASK EXAMPLES")
        print("="*80)
        
        for split_name in ['raw', 'train', 'test']:
            stats = analyze_tasks(original_tasks, split_name)
            if stats:
                print_task_examples(stats, f"ORIGINAL-{split_name}", num_examples)
    
    # Show examples for SAMPLED (balanced) data
    print("\n" + "="*80)
    print("📋 SAMPLED (BALANCED) TASK EXAMPLES")
    print("="*80)
    
    for split_name in ['raw', 'train', 'test']:
        stats = analyze_tasks(sampled_tasks, split_name)
        if stats:
            print_task_examples(stats, f"SAMPLED-{split_name}", num_examples)


def main():
    parser = argparse.ArgumentParser(description="Analyze video_labels folders")
    parser.add_argument("--video_labels_dir", type=str, default="video_labels",
                        help="Path to video_labels directory")
    parser.add_argument("--folder_name", type=str, default=None,
                        help="Specific folder to analyze (e.g., 'motion_dataset')")
    parser.add_argument("--num_examples", type=int, default=3,
                        help="Number of example tasks to show")
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("🎬 VIDEO LABELS ANALYZER")
    print("="*80)
    
    # Find all sampled_tasks folders
    folders = find_sampled_tasks_folders(args.video_labels_dir)
    
    if not folders:
        print(f"\n❌ No sampled_tasks.json files found in {args.video_labels_dir}")
        print(f"\nMake sure you've run: python pairwise_benchmark.py")
        return
    
    print(f"\n✅ Found {len(folders)} folders with sampled_tasks.json:")
    for folder in folders:
        relative_path = folder.relative_to(args.video_labels_dir)
        print(f"   • {relative_path}")
    
    # Filter by folder_name if specified
    if args.folder_name:
        folders = [f for f in folders if args.folder_name in str(f)]
        if not folders:
            print(f"\n❌ No folders matching '{args.folder_name}'")
            return
        print(f"\n🔍 Filtering to folders matching '{args.folder_name}':")
        for folder in folders:
            relative_path = folder.relative_to(args.video_labels_dir)
            print(f"   • {relative_path}")
    
    # Analyze each folder
    for folder in folders:
        analyze_folder(folder, args.num_examples)
    
    # Summary
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nAnalyzed {len(folders)} folder(s)")
    print("\nKey Takeaways:")
    print("  • 'raw' = Full imbalanced dataset before splitting")
    print("  • 'train' = Balanced train set (only train_videos)")
    print("  • 'test' = Balanced test set (only test_videos, capped at max_samples)")
    print("  • Min = min(pos, neg) = actual balanced pairs available")
    print("  • Imbalance = |pos - neg| = degree of imbalance")
    print("\n💡 Tip: To get imbalanced train/test data, filter 'raw' by train_videos/test_videos")


if __name__ == "__main__":
    main()