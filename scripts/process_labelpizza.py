"""
Pipeline for processing Label Pizza annotation exports into structured caption data.

This module handles two annotation workflows:
  1. Camera Movement – pan, tilt, zoom, etc.
  2. Shot Composition – framing, angle, depth, etc.

Typical usage:
    1. process_labelpizza()  – deduplicate & merge raw Label Pizza JSON exports per video.
    2. combine_label()       – join the resulting caption files with video URLs and
                               produce a single unified JSON ready for downstream training.
"""

import json
import glob
import os
from typing import Dict, List, Optional

from scripts.label_pizza_to_caption import transform_to_caption

def process_labelpizza(input_folder: str, output_folder: str) -> None:
    """Read raw Label Pizza JSON exports, deduplicate by video, and write caption files.

    Each JSON file in *input_folder* is expected to contain a list of annotation
    records.  Records are routed into one of two buckets based on
    ``item['project_name']``:

    * **Camera Movement** → aggregated into ``video_motion_data``
    * **Shot Composition** → aggregated into ``video_shotcomp_data``

    Within each bucket, answers from multiple records for the same video are
    merged (later records overwrite earlier ones for duplicate keys).

    Args:
        input_folder: Directory containing one or more ``*.json`` Label Pizza
            export files.
        output_folder: Directory where the two output caption JSON files will
            be written:
            - ``camera_pizza_camera_movement_caption.json``
            - ``camera_pizza_shot_composition_caption.json``
    """
    os.makedirs(output_folder, exist_ok=True)

    # Per-video accumulators keyed by video_uid.
    video_shotcomp_data: Dict[str, dict] = {}
    video_motion_data: Dict[str, dict] = {}

    paths: List[str] = glob.glob(input_folder + "/*.json")
    print(len(paths))

    for path in paths:
        with open(path, "r") as f:
            data: List[dict] = json.load(f)

        for item in data:
            video_name: str = item["video_uid"]

            if "Camera Movement" in item["project_name"]:
                # Initialise entry on first encounter.
                if video_name not in video_motion_data:
                    video_motion_data[video_name] = {
                        "video_uid": video_name,
                        "user_name": item["user_name"],
                        "answers": {},
                    }
                # Merge answers (last-write-wins for duplicate question keys).
                video_motion_data[video_name]["answers"].update(item["answers"])

            elif "Shot Composition" in item["project_name"]:
                if video_name not in video_shotcomp_data:
                    video_shotcomp_data[video_name] = {
                        "video_uid": video_name,
                        "user_name": item["user_name"],
                        "answers": {},
                    }
                video_shotcomp_data[video_name]["answers"].update(item["answers"])

    # Convert the merged per-video dicts into human-readable caption JSON files.
    transform_to_caption(
        list(video_motion_data.values()),
        "camera_motion",
        f"{output_folder}/camera_pizza_camera_movement_caption.json",
    )
    transform_to_caption(
        list(video_shotcomp_data.values()),
        "shot_composition",
        f"{output_folder}/camera_pizza_shot_composition_caption.json",
    )


def get_video_url(json_path: str) -> Dict[str, str]:
    """Build a ``{video_uid: url}`` lookup from a video-metadata JSON file.

    Args:
        json_path: Path to a JSON file whose top-level value is a list of
            objects, each containing at least ``video_uid`` and ``url`` fields.

    Returns:
        Dictionary mapping each ``video_uid`` to its corresponding ``url``.
    """
    res: Dict[str, str] = {}
    with open(json_path, "r") as f:
        data: List[dict] = json.load(f)
    for item in data:
        res[item["video_uid"]] = item["url"]
    return res


def combine_label(
    input_folder: str,
    output_path: str,
    video_json_path: str,
    need_label_types: Optional[List[str]] = None,
) -> None:
    """Combine caption files produced by :func:`process_labelpizza` into a
    single unified JSON, enriched with video URLs.

    The function reads every ``*.json`` in *input_folder* and dispatches each
    file based on whether its filename contains ``"camera_movement"`` or
    ``"shot_composition"``.  For each video, a record is assembled with:

    * ``video_name`` – unique identifier
    * ``workflows``  – per-workflow metadata (approver, URL)
    * ``cam_motion`` / ``cam_setup`` – the raw answer dicts

    When both label types are requested (the default), only videos that have
    **both** camera-movement *and* shot-composition annotations are kept.

    Args:
        input_folder: Directory containing caption JSON files (output of
            :func:`process_labelpizza` / ``transform_to_caption``).
        output_path: Destination path for the combined JSON file.
        video_json_path: Path to the video-metadata JSON used to resolve URLs
            (passed to :func:`get_video_url`).
        need_label_types: Which label families to include. Defaults to
            ``["camera_movement", "shot_composition"]``.

    Raises:
        KeyError: If a video referenced in an annotation file has no matching
            entry in the video-metadata JSON.
    """
    if need_label_types is None:
        need_label_types = ["camera_movement", "shot_composition"]

    paths: List[str] = glob.glob(input_folder + "/*.json")
    videos_data: Dict[str, dict] = {}
    video_url: Dict[str, str] = get_video_url(video_json_path)

    for path in paths:
        with open(path, "r") as f:
            data: List[dict] = json.load(f)

        for item in data:
            video_name: str = item["video_name"]

            # --- Camera Movement branch ---
            if (
                "camera_movement" in os.path.basename(path)
                and "camera_movement" in need_label_types
            ):
                # Validate that the video exists in our URL lookup.
                if video_name not in video_url:
                    print("\n[DEBUG] Missing video_name:", repr(video_name))
                    print(
                        "[DEBUG] Available keys examples:",
                        list(video_url.keys())[:5],
                    )
                    raise KeyError(video_name)

                if video_name not in videos_data:
                    videos_data[video_name] = {
                        "video_name": video_name,
                        "workflows": {},
                    }

                videos_data[video_name]["workflows"]["cam_motion"] = {
                    "approver": item["user_name"],
                    "video_name": video_name,
                    "video_url": video_url[video_name],
                }
                videos_data[video_name]["cam_motion"] = item["answers"]

            # --- Shot Composition branch ---
            elif (
                "shot_composition" in os.path.basename(path)
                and "shot_composition" in need_label_types
            ):
                if video_name not in video_url:
                    print("\n[DEBUG] Missing video_name:", repr(video_name))
                    print(
                        "[DEBUG] Available keys examples:",
                        list(video_url.keys())[:5],
                    )
                    raise KeyError(video_name)

                if video_name not in videos_data:
                    videos_data[video_name] = {
                        "video_name": video_name,
                        "workflows": {},
                    }

                videos_data[video_name]["workflows"]["cam_setup"] = {
                    "approver": item["user_name"],
                    "video_name": video_name,
                    "video_url": video_url[video_name],
                }

                # Normalise "not_complex" sentinel to None.
                for q, a in item["answers"].items():
                    if a == "not_complex":
                        item["answers"][q] = None

                videos_data[video_name]["cam_setup"] = item["answers"]

    # Ensure the output directory exists.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if (
        "camera_movement" in need_label_types
        and "shot_composition" in need_label_types
    ):
        # Keep only videos that have BOTH annotation types.
        filter_videos_data: List[dict] = [
            video_data
            for video_data in videos_data.values()
            if "cam_motion" in video_data and "cam_setup" in video_data
        ]
        with open(output_path, "w") as f:
            json.dump(filter_videos_data, f, indent=2)
    else:
        with open(output_path, "w") as f:
            json.dump(list(videos_data.values()), f, indent=2)