from scripts.process_labelpizza import combine_label, process_labelpizza
import json
import os
import shutil
from datetime import datetime

import argparse
from typing import Any, Dict, List


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dicts. *override* wins on conflicts.

    - Keys in both   → use *override* (recurse if both values are dicts).
    - Keys only in *override* → added.
    - Keys only in *base*     → preserved.
    """
    merged: Dict[str, Any] = {}
    for key in set(base.keys()) | set(override.keys()):
        if key in override and key in base:
            if isinstance(base[key], dict) and isinstance(override[key], dict):
                merged[key] = deep_merge(base[key], override[key])
            else:
                merged[key] = override[key]
        elif key in override:
            merged[key] = override[key]
        else:
            merged[key] = base[key]
    return merged


def build_lookup(new_data: List[dict]) -> Dict[str, dict]:
    """Index new video records by video_name for O(1) lookup.

    Returns:
        { video_name: { "cam_motion": ..., "workflow": ... } }
    """
    return {
        v["video_name"]: {
            "cam_motion": v["cam_motion"],
            "workflow": v["workflows"]["cam_motion"],
        }
        for v in new_data
    }


def merge_cam_motion(
    old_data: List[dict],
    lookup: Dict[str, dict],
) -> List[dict]:
    """Merge cam_motion from *lookup* into each matching record in *old_data*."""
    result: List[dict] = []
    updated_count = 0

    for item in old_data:
        name = item["video_name"]
        if name in lookup:
            new_info = lookup[name]

            # Merge cam_motion answers (new takes precedence).
            item["cam_motion"] = deep_merge(
                item.get("cam_motion", {}), new_info["cam_motion"]
            )

            # Merge workflows.cam_motion metadata (new takes precedence).
            item.setdefault("workflows", {})
            item["workflows"]["cam_motion"] = deep_merge(
                item["workflows"].get("cam_motion", {}), new_info["workflow"]
            )
            updated_count += 1

        result.append(item)

    print(f"  Matched & updated: {updated_count} / {len(old_data)} videos")
    return result


def run_merge(new_json: str, old_json: str, output_folder: str) -> None:
    """Load both JSON files, merge, and write the result."""
    with open(new_json, "r") as f:
        new_data = json.load(f)
    lookup = build_lookup(new_data)

    with open(old_json, "r") as f:
        old_data = json.load(f)

    merged = merge_cam_motion(old_data, lookup)

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "videos.json")
    with open(output_path, "w") as f:
        json.dump(merged, f, indent=2)

    print(f"  Wrote {len(merged)} videos to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Transfer caption labels from Label Pizza exports.")
    parser.add_argument(
        "--label_pizza_workspace",
        type=str,
        default="../label_pizza/workspace_0311/",
        help="Path to Label Pizza workspace (ground_truths and videos.json).",
    )
    args = parser.parse_args()
    workspace = args.label_pizza_workspace.rstrip("/")
    ground_truths_dir = os.path.join(workspace, "ground_truths")
    video_json_path = os.path.join(workspace, "videos.json")

    today = datetime.now().strftime("%Y%m%d")

    # ---------------------------------------------------------------------------
    # Step 1: Process raw Label Pizza exports into caption files
    # ---------------------------------------------------------------------------
    caption_folder = "./caption_folder"
    save_folder = os.path.join(caption_folder, today)
    os.makedirs(caption_folder, exist_ok=True)
    process_labelpizza(ground_truths_dir, save_folder)

    # ---------------------------------------------------------------------------
    # Step 2: Combine captions with video URLs into per-type folders
    # ---------------------------------------------------------------------------
    os.makedirs("./video_data", exist_ok=True)

    setup_path = f'./video_data/{today}_setup_folder/videos.json'
    combine_label(save_folder, setup_path, video_json_path, need_label_types=['shot_composition'])

    motion_path = f'./video_data/{today}_ground_folder/videos.json'
    combine_label(save_folder, motion_path, video_json_path, need_label_types=['camera_movement'])

    motion_setup_path = f'./video_data/{today}_ground_and_setup_folder/videos.json'
    combine_label(save_folder, motion_setup_path, video_json_path, need_label_types=["camera_movement", "shot_composition"])

    # ---------------------------------------------------------------------------
    # Step 3: Merge cam_motion into ground_and_camera using the ground folder
    # ---------------------------------------------------------------------------
    ground_and_camera_folder = f'./video_data/{today}_ground_and_camera_folder'
    print(f"\n--- Merging ground -> ground_and_camera ---")
    run_merge(
        new_json=motion_path,
        old_json=f'./video_data/{today}_ground_and_setup_folder/videos.json',
        output_folder=ground_and_camera_folder,
    )

    # ---------------------------------------------------------------------------
    # Step 4: Merge cam_motion into ground_and_camera_and_setup
    # ---------------------------------------------------------------------------
    ground_and_camera_and_setup_folder = f'./video_data/{today}_ground_and_camera_and_setup_folder'
    print(f"\n--- Merging ground_and_camera -> ground_and_camera_and_setup ---")
    run_merge(
        new_json=f'{ground_and_camera_folder}/videos.json',
        old_json=f'./video_data/{today}_ground_and_setup_folder/videos.json',
        output_folder=ground_and_camera_and_setup_folder,
    )

    shutil.rmtree(caption_folder)
    print(f"\nAll outputs written under ./video_data/{today}_*/")


if __name__ == "__main__":
    main()