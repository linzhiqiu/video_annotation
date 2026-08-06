#!/usr/bin/env python3
"""
Extract CameraBench Pro labels into classifier_label_mapping.json.

This script extracts labels from benchmark_config.py for the camerabench_pro version,
separating them into atomic (single label with pos/neg type) and composite (multiple labels) categories.

It also compares atomic labels against a previous label_mapping.json to verify coverage.

Usage:
    python extract_classifier_labels.py --output classifier_label_mapping.json
    python extract_classifier_labels.py --output classifier_label_mapping.json --compare label_mapping.json
"""

import argparse
import json
import os
from benchmark_config import (
    get_pairwise_labels,
    get_test_skip_tasks,
    FOLDERS
)


def classify_task(task):
    """
    Classify a task and determine how many atomic labels can be extracted.
    
    Returns:
        tuple: (task_type, atomic_labels_info)
        
        task_type can be:
        - "atomic_simple": pos is single dict, neg is same label with type "neg"
        - "atomic_with_complex_neg": pos is single dict, neg is a list
        - "atomic_dual": both pos and neg are single dicts with type "pos" (two different labels)
        - "composite": pos is a list
        
        atomic_labels_info is a list of dicts with keys:
        - "raw_name": the label name
        - "pos_question": the question for this label
        - "pos_prompt": the prompt for this label
        - "source": "pos" or "neg" (which field this came from)
    """
    pos = task.get("pos")
    neg = task.get("neg")
    
    # If pos is a list, it's composite
    if isinstance(pos, list):
        return ("composite", [])
    
    # pos is a single dict
    if not (isinstance(pos, dict) and "label" in pos and "type" in pos):
        return ("composite", [])
    
    atomic_labels = []
    
    # Always extract the pos label
    atomic_labels.append({
        "raw_name": pos["label"],
        "pos_question": task.get("pos_question"),
        "pos_prompt": task.get("pos_prompt"),
        "source": "pos"
    })
    
    # Check neg type
    if isinstance(neg, list):
        # pos is single, neg is list
        return ("atomic_with_complex_neg", atomic_labels)
    
    if isinstance(neg, dict) and "label" in neg and "type" in neg:
        if neg["type"] == "neg" and neg["label"] == pos["label"]:
            # Simple atomic: same label, opposite types
            return ("atomic_simple", atomic_labels)
        elif neg["type"] == "pos":
            # Dual atomic: neg is actually a positive example of a different label!
            # Extract the neg as a second atomic label
            atomic_labels.append({
                "raw_name": neg["label"],
                "pos_question": task.get("neg_question"),
                "pos_prompt": task.get("neg_prompt"),
                "source": "neg"
            })
            return ("atomic_dual", atomic_labels)
        else:
            # neg is a different label with type "neg" - unusual case
            return ("atomic_with_complex_neg", atomic_labels)
    
    return ("atomic_simple", atomic_labels)


def extract_full_info(task, source="pos"):
    """
    Extract full_info from task, excluding only 'folder'.
    
    If source="neg" (for atomic_dual), swap:
    - pos_question <-> neg_question
    - pos_prompt <-> neg_prompt
    - pos <-> neg
    """
    excluded_keys = {"folder"}
    
    if source == "pos":
        return {k: v for k, v in task.items() if k not in excluded_keys}
    else:
        # For neg-sourced atomic labels (atomic_dual), swap the fields
        result = {}
        for k, v in task.items():
            if k in excluded_keys:
                continue
            elif k == "pos_question":
                result["pos_question"] = task.get("neg_question")
            elif k == "neg_question":
                result["neg_question"] = task.get("pos_question")
            elif k == "pos_prompt":
                result["pos_prompt"] = task.get("neg_prompt")
            elif k == "neg_prompt":
                result["neg_prompt"] = task.get("pos_prompt")
            elif k == "pos":
                result["pos"] = task.get("neg")
            elif k == "neg":
                result["neg"] = task.get("pos")
            else:
                result[k] = v
        return result


def extract_labels_for_folder(folder_name):
    """
    Extract all labels for a given folder, categorized as atomic or composite.
    
    Args:
        folder_name: The folder name (e.g., "camerabench_pro")
    
    Returns:
        dict with "atomic" and "composite" sub-dicts
    """
    # Get all pairwise labels for this folder
    pairwise_labels = get_pairwise_labels(folder_name)
    
    # Get tasks to skip in test set
    skip_tasks = get_test_skip_tasks(folder_name)
    
    result = {
        "atomic": {},
        "composite": {}
    }
    
    # Track special cases for reporting
    special_cases = {
        "atomic_simple": [],
        "atomic_with_complex_neg": [],
        "atomic_dual": [],
        "composite": []
    }
    
    skipped_count = 0
    
    for category_name, tasks in pairwise_labels.items():
        for task in tasks:
            task_name = task.get("name")
            
            # Skip tasks in test_skip_tasks
            if task_name in skip_tasks:
                skipped_count += 1
                print(f"Skipping (in test_skip_tasks): {task_name}")
                continue
            
            # Classify the task
            task_type, atomic_labels_info = classify_task(task)
            special_cases[task_type].append(task_name)
            
            if task_type == "composite":
                # Composite label
                classifier_name = f"{category_name}.{task_name}"
                full_info = extract_full_info(task, source="pos")
                result["composite"][task_name] = {
                    "classifier_name": classifier_name,
                    "pos_question": full_info.get("pos_question"),
                    "pos_prompt": full_info.get("pos_prompt"),
                    "full_info": full_info
                }
            else:
                # Atomic label(s)
                for i, label_info in enumerate(atomic_labels_info):
                    source = label_info["source"]
                    raw_name = label_info["raw_name"]
                    
                    # For dual atomic, create unique task names
                    if task_type == "atomic_dual" and source == "neg":
                        # Use a modified task name to indicate this came from neg
                        actual_task_name = f"{task_name}_negated"
                        classifier_name = f"{category_name}.{actual_task_name}"
                    else:
                        actual_task_name = task_name
                        classifier_name = f"{category_name}.{task_name}"
                    
                    full_info = extract_full_info(task, source=source)
                    
                    result["atomic"][actual_task_name] = {
                        "raw_name": raw_name,
                        "classifier_name": classifier_name,
                        "pos_question": full_info.get("pos_question"),
                        "pos_prompt": full_info.get("pos_prompt"),
                        "full_info": full_info
                    }
    
    print(f"\nSkipped {skipped_count} tasks from test_skip_tasks")
    print(f"Extracted {len(result['atomic'])} atomic labels")
    print(f"Extracted {len(result['composite'])} composite labels")
    
    # Report special cases
    print("\n" + "="*60)
    print("TASK TYPE BREAKDOWN:")
    print("="*60)
    print(f"  atomic_simple (pos/neg same label, opposite types): {len(special_cases['atomic_simple'])}")
    print(f"  atomic_with_complex_neg (pos single, neg is list): {len(special_cases['atomic_with_complex_neg'])}")
    print(f"  atomic_dual (both pos and neg are type='pos'): {len(special_cases['atomic_dual'])}")
    print(f"  composite (pos is a list): {len(special_cases['composite'])}")
    
    if special_cases['atomic_dual']:
        print("\n--- ATOMIC_DUAL tasks (two labels extracted from one task) ---")
        for name in special_cases['atomic_dual']:
            print(f"  {name}")
    
    if special_cases['atomic_with_complex_neg']:
        print("\n--- ATOMIC_WITH_COMPLEX_NEG tasks (pos single, neg is list) ---")
        for name in special_cases['atomic_with_complex_neg']:
            print(f"  {name}")
    
    return result, special_cases


def compare_with_label_mapping(result, label_mapping_path):
    """
    Compare extracted atomic labels with a previous label_mapping.json.
    
    Args:
        result: The extracted labels dict with "atomic" and "composite" keys
        label_mapping_path: Path to the previous label_mapping.json
    
    Returns:
        dict with comparison results
    """
    if not os.path.exists(label_mapping_path):
        print(f"\nWarning: {label_mapping_path} not found, skipping comparison")
        return None
    
    with open(label_mapping_path, "r") as f:
        previous_mapping = json.load(f)
    
    # previous_mapping is {label_name: raw_label} e.g., {"Pan Left": "cam_motion.pan.pan_left"}
    # We need to compare raw_names in our atomic labels with values in previous_mapping
    
    # Build set of raw_names from our atomic labels
    atomic_raw_names = {data["raw_name"] for data in result["atomic"].values()}
    
    # Build set of raw_names from previous mapping (the values)
    previous_raw_names = set(previous_mapping.values())
    
    # Find matches and mismatches
    in_both = atomic_raw_names & previous_raw_names
    only_in_atomic = atomic_raw_names - previous_raw_names
    only_in_previous = previous_raw_names - atomic_raw_names
    
    print("\n" + "="*60)
    print("COMPARISON WITH PREVIOUS label_mapping.json")
    print("="*60)
    print(f"Total in previous label_mapping.json: {len(previous_raw_names)}")
    print(f"Total atomic raw_names extracted: {len(atomic_raw_names)}")
    print(f"In both: {len(in_both)}")
    print(f"Only in atomic (new): {len(only_in_atomic)}")
    print(f"Only in previous (missing from atomic): {len(only_in_previous)}")
    
    if only_in_previous:
        print("\n--- Labels in previous but NOT in atomic ---")
        # Find the label_name for each missing raw_name
        for raw_name in sorted(only_in_previous):
            label_names = [k for k, v in previous_mapping.items() if v == raw_name]
            for label_name in label_names:
                print(f"  {label_name}: {raw_name}")
    
    if only_in_atomic:
        print("\n--- Labels in atomic but NOT in previous ---")
        for raw_name in sorted(only_in_atomic):
            # Find task_name for this raw_name
            task_names = [k for k, v in result["atomic"].items() if v["raw_name"] == raw_name]
            for task_name in task_names:
                print(f"  {task_name}: {raw_name}")
    
    # Check if all previous labels are covered
    if len(only_in_previous) == 0:
        print("\n✓ All labels from previous label_mapping.json are covered by atomic labels!")
    else:
        print(f"\n✗ {len(only_in_previous)} labels from previous label_mapping.json are NOT covered by atomic labels")
    
    return {
        "in_both": list(in_both),
        "only_in_atomic": list(only_in_atomic),
        "only_in_previous": list(only_in_previous),
        "previous_total": len(previous_raw_names),
        "atomic_total": len(atomic_raw_names)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract CameraBench Pro labels into classifier_label_mapping.json"
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="camerabench_pro",
        choices=list(FOLDERS.keys()),
        help="Folder name to extract labels from (default: camerabench_pro)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="classifier_label_mapping.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--compare",
        type=str,
        default="label_mapping.json",
        help="Path to previous label_mapping.json for comparison (default: label_mapping.json)"
    )
    parser.add_argument(
        "--no-compare",
        action="store_true",
        help="Skip comparison with previous label_mapping.json"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about each label"
    )
    
    args = parser.parse_args()
    
    print(f"Extracting labels for folder: {args.folder}")
    print(f"Description: {FOLDERS[args.folder]['description']}")
    print(f"Test skip tasks: {get_test_skip_tasks(args.folder)}")
    print()
    
    # Extract labels
    result, special_cases = extract_labels_for_folder(args.folder)
    
    # Compare with previous label_mapping.json
    comparison = None
    if not args.no_compare:
        comparison = compare_with_label_mapping(result, args.compare)
    
    if args.verbose:
        print("\n" + "="*60)
        print("ATOMIC LABELS:")
        print("="*60)
        for name, data in result["atomic"].items():
            print(f"  {name}:")
            print(f"    raw_name: {data['raw_name']}")
            print(f"    classifier_name: {data['classifier_name']}")
        
        print("\n" + "="*60)
        print("COMPOSITE LABELS:")
        print("="*60)
        for name, data in result["composite"].items():
            print(f"  {name}:")
            print(f"    classifier_name: {data['classifier_name']}")
    
    # Save to JSON
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nSaved to {args.output}")
    
    # Print final statistics
    print("\n" + "="*60)
    print("FINAL STATISTICS:")
    print("="*60)
    print(f"  atomic_simple:           {len(special_cases['atomic_simple']):4d}")
    print(f"  atomic_with_complex_neg: {len(special_cases['atomic_with_complex_neg']):4d}")
    print(f"  atomic_dual:             {len(special_cases['atomic_dual']):4d} (x2 = {len(special_cases['atomic_dual']) * 2} labels)")
    print(f"  composite:               {len(special_cases['composite']):4d}")
    print("-" * 40)
    print(f"  Total atomic labels:     {len(result['atomic']):4d}")
    print(f"  Total composite labels:  {len(result['composite']):4d}")
    print(f"  TOTAL LABELS:            {len(result['atomic']) + len(result['composite']):4d}")
    
    return result, special_cases, comparison


if __name__ == "__main__":
    main()