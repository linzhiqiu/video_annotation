#!/usr/bin/env python3
"""
Simple script to output a dictionary mapping label_name to label.
Includes ALL labels from label collections, even those without video examples.

Usage:
    python label_name_to_label.py --label_collections cam_motion cam_setup
    python label_name_to_label.py --label_collections cam_motion cam_setup --output label_mapping.json
    python label_name_to_label.py --label_collections cam_motion cam_setup --only_with_examples --input video_data/20251021_ground_and_setup_folder/videos.json
"""

import argparse
import json
import os

# Import from existing modules
from label import Label, extract_labels_dict
from download import get_label_video_mapping, get_video_labels_dir, load_from_json


def get_all_label_name_to_label_mapping(label_collections):
    """
    Get a dictionary mapping label_name (human-readable) to label (hierarchical key)
    for ALL labels in the specified collections, regardless of video examples.
    
    Returns:
        dict: {label_name: label} e.g., {"Pan Left": "cam_motion.pan.pan_left"}
    """
    labels = Label.load_all_labels()
    
    label_name_to_label = {}
    
    for label_collection in label_collections:
        # Get all labels from this collection
        labels_dict = extract_labels_dict(getattr(labels, label_collection), label_collection)
        
        for label_key, label_obj in labels_dict.items():
            label_name = label_obj.label  # Human-readable name
            
            # Handle potential duplicates
            if label_name in label_name_to_label:
                print(f"Warning: Duplicate label_name '{label_name}' found!")
                print(f"  Existing: {label_name_to_label[label_name]}")
                print(f"  New: {label_key}")
            
            label_name_to_label[label_name] = label_key
    
    return label_name_to_label


def get_filtered_label_name_to_label_mapping(json_path, label_collections, force_regenerate_labels=False):
    """
    Get a dictionary mapping label_name to label, but only for labels
    that have both positive and negative video examples.
    
    Returns:
        dict: {label_name: label} for labels with video examples
    """
    # This will generate/load the labels (filtered by video examples)
    label_to_videos = get_label_video_mapping(
        json_path,
        label_collections=label_collections,
        skip_download=True,
        force_regenerate_labels=force_regenerate_labels
    )
    
    label_name_to_label = {}
    for label_key, label_data in label_to_videos.items():
        label_name = label_data["label_name"]
        label = label_data["label"]
        
        if label_name in label_name_to_label:
            print(f"Warning: Duplicate label_name '{label_name}' found!")
            print(f"  Existing: {label_name_to_label[label_name]}")
            print(f"  New: {label}")
        
        label_name_to_label[label_name] = label
    
    return label_name_to_label


def main():
    parser = argparse.ArgumentParser(
        description="Output a dictionary mapping label_name to label."
    )
    parser.add_argument(
        "--input", 
        type=str,
        default=None,
        help="Path to the JSON file containing video data (required if --only_with_examples is used)."
    )
    parser.add_argument(
        "--label_collections", 
        nargs="+", 
        type=str,
        default=["cam_motion", "cam_setup"],
        help="List of label collections to use."
    )
    parser.add_argument(
        "--force_regenerate_labels", 
        action="store_true", 
        default=False,
        help="Force regeneration of label files even if they already exist."
    )
    parser.add_argument(
        "--output", 
        type=str,
        default=None,
        help="Output JSON file path. If not specified, prints to stdout."
    )
    parser.add_argument(
        "--only_with_examples",
        action="store_true",
        default=False,
        help="Only include labels that have both positive and negative video examples."
    )
    
    args = parser.parse_args()
    
    # Determine which mode to use
    if args.only_with_examples:
        if not args.input:
            parser.error("--input is required when using --only_with_examples")
        print("Getting labels WITH video examples only...")
        mapping = get_filtered_label_name_to_label_mapping(
            args.input,
            args.label_collections,
            force_regenerate_labels=args.force_regenerate_labels
        )
    else:
        print("Getting ALL labels (including those without video examples)...")
        mapping = get_all_label_name_to_label_mapping(args.label_collections)
    
    # Output
    if args.output:
        with open(args.output, "w") as f:
            json.dump(mapping, f, indent=2)
        print(f"Saved mapping to {args.output}")
    else:
        print("\n" + "="*60)
        print("Label Name to Label Mapping:")
        print("="*60)
        print(json.dumps(mapping, indent=2))
    
    print(f"\nTotal labels: {len(mapping)}")
    
    return mapping


if __name__ == "__main__":
    main()