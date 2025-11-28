#!/usr/bin/env python3
"""
Extract all primitives from the labels directory structure.
This script walks through labels/cam_motion and labels/cam_setup to find all primitives.
Outputs a single JSON file with hierarchical primitive information.
"""

import os
import json
from pathlib import Path
from collections import defaultdict

# Labels directory structure
LABELS_ROOT = Path("labels")

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_primitive_info(json_path):
    """Extract relevant information from a primitive's JSON file"""
    data = load_json(json_path)
    
    # Only keep the essential fields - no alt_question/alt_prompt
    return {
        "label_name": data.get("label_name", ""),
        "label": data.get("label", ""),
        "def_question": data.get("def_question", [""])[0] if data.get("def_question") else "",
        "def_prompt": data.get("def_prompt", [""])[0] if data.get("def_prompt") else "",
    }

def walk_label_directory(collection_name):
    """
    Walk through a label collection directory (cam_motion or cam_setup)
    and extract all primitives organized by hierarchy.
    
    Returns a nested dictionary representing the hierarchy.
    """
    collection_path = LABELS_ROOT / collection_name
    
    if not collection_path.exists():
        print(f"Warning: {collection_path} does not exist")
        return {}
    
    primitives = {}
    
    # Walk through all directories
    for root, dirs, files in os.walk(collection_path):
        for file in files:
            if file.endswith('.json'):
                json_path = Path(root) / file
                
                # Get relative path from collection root
                rel_path = json_path.relative_to(collection_path)
                
                # Build hierarchical key (e.g., "ground_centric_movement.forward.has_forward_wrt_ground")
                path_parts = list(rel_path.parts[:-1])  # All dirs
                filename = rel_path.stem  # Filename without .json
                
                # Create full hierarchical key
                if path_parts:
                    full_key = f"{collection_name}.{'.'.join(path_parts)}.{filename}"
                else:
                    full_key = f"{collection_name}.{filename}"
                
                # Extract primitive info
                primitive_info = extract_primitive_info(json_path)
                primitive_info["hierarchy_path"] = path_parts
                primitive_info["filename"] = filename
                primitive_info["full_key"] = full_key
                
                primitives[full_key] = primitive_info
    
    return primitives

def organize_by_hierarchy(primitives):
    """
    Organize primitives into a hierarchical structure for easier viewing.
    """
    hierarchy = defaultdict(lambda: defaultdict(list))
    
    for full_key, info in primitives.items():
        parts = full_key.split('.')
        collection = parts[0]  # cam_motion or cam_setup
        
        if len(parts) == 2:
            # Top-level primitive (e.g., cam_setup.has_shot_transition)
            aspect = "root"
        elif len(parts) == 3:
            # Second-level (e.g., cam_motion.tracking.general_tracking)
            aspect = parts[1]
        else:
            # Deeper levels (e.g., cam_motion.ground_centric_movement.forward.has_forward)
            aspect = '.'.join(parts[1:-1])
        
        hierarchy[collection][aspect].append({
            "full_key": full_key,
            "label_name": info["label_name"],
            "def_question": info["def_question"],
            "def_prompt": info["def_prompt"],
        })
    
    return dict(hierarchy)

def main():
    print("Extracting primitives from labels directory...")
    
    # Extract from both collections
    all_primitives = {}
    
    for collection in ["cam_motion", "cam_setup"]:
        print(f"\nProcessing {collection}...")
        primitives = walk_label_directory(collection)
        all_primitives.update(primitives)
        print(f"  Found {len(primitives)} primitives")
    
    # # Save flat list
    # output_flat = Path("primitives_flat.json")
    # with open(output_flat, 'w') as f:
    #     json.dump(all_primitives, f, indent=2, sort_keys=True)
    # print(f"\n✓ Saved flat primitives list to {output_flat}")
    # print(f"  Total primitives: {len(all_primitives)}")
    
    # Save hierarchical organization
    hierarchy = organize_by_hierarchy(all_primitives)
    output_hierarchy = Path("label_hierarchy.json")
    with open(output_hierarchy, 'w') as f:
        json.dump(hierarchy, f, indent=2, sort_keys=True)
    print(f"✓ Saved hierarchical primitives to {output_hierarchy}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for collection, aspects in sorted(hierarchy.items()):
        print(f"\n{collection.upper()}:")
        for aspect, prims in sorted(aspects.items()):
            print(f"  {aspect}: {len(prims)} primitives")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Review label_hierarchy.json to see the organization")
    print("2. Delete any primitives you don't want to include")  
    print("3. Provide the primitives_flat.json file for LaTeX table generation")
    print("="*60)

if __name__ == "__main__":
    main()