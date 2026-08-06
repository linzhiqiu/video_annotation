"""
Build a JSON mapping: skill name -> list of task names.

Reads sampled_tasks.json (e.g. from CameraBench-Pro sampling), and outputs a
dictionary where each key is a "skill" and each value is the list of individual
task names under that skill. Edit SKILL_TO_CATEGORIES below to change grouping
(e.g. merge depth_of_field + focus_* into a single "camera_focus" skill).
"""

import argparse
import json
import os
from typing import List, Optional

# Import test_skip_tasks for the chosen benchmark (e.g. camerabench_pro)
from benchmark_config import get_test_skip_tasks

DEFAULT_SAMPLED_TASKS_PATH = (
    "./video_labels/camerabench_pro/test_ratio_0.20_2026_03_11_num_20_sampling_random_seed_0_train_posneg_max_ratio_3.0/sampled_tasks.json"
)

# -----------------------------------------------------------------------------
# Skill -> data categories mapping. Keys are readable display names; values are
# category names from sampled_tasks.json "raw". Merge by listing multiple categories.
# -----------------------------------------------------------------------------
SKILL_TO_CATEGORIES = {
    # Motion
    "Motion & Steadiness": ["movement_and_steadiness"],
    "Movement Speed": ["camera_movement_speed"],
    "Movement Direction": [
        "translation_direction",
        "rotation_direction",
        "object_centric_direction",
        "intrinsic_direction",
    ],
    "Confusable Motion": ["rotation_vs_translation", "reference_frame"],
    "Has Motion": [
        "has_intrinsic_change",
        "has_translation",
        "has_rotation",
        "has_arc_crane",
    ],
    "Tracking Shot": ["special_tracking", "general_tracking"],
    "Only Motion": [
        "only_intrinsic_change",
        "only_translation",
        "only_rotation",
    ],
    # Setup
    "Shot Transition": ["shot_transition"],
    "Overlays": ["overlays"],
    "Lens Distortion": ["lens_distortion"],
    "Playback Speed": ["playback_speed"],
    "Point of View": ["point_of_view"],
    "Subject Framing": ["subject_framing"],
    "Shot Type": ["shot_type"],
    "Shot Size": [
        "shot_size_change",
        "shot_size_start",
        "shot_size_end",
        "shot_size_is",
    ],
    "Height wrt Subject": [
        "height_wrt_subject_change",
        "height_wrt_subject_start",
        "height_wrt_subject_end",
        "height_wrt_subject_is",
        "height_wrt_subject_transition",
    ],
    "Height wrt Ground": [
        "height_wrt_ground_change",
        "height_wrt_ground_start",
        "height_wrt_ground_end",
        "height_wrt_ground_is",
    ],
    "Camera Angle": [
        "camera_angle_change",
        "camera_angle_start",
        "camera_angle_end",
        "camera_angle_is",
        "camera_angle_transition",
    ],
    "Dutch Angle": ["dutch_angle"],
    "Depth of Field": ["depth_of_field"],
    "Focal Plane": [
        "focus_is_always",
        "focus_start_with",
        "focus_end_with",
        "focus_from_to",
    ],
}


def load_category_to_tasks(sampled_tasks_path: str, split: str = "test") -> dict:
    """Load sampled_tasks.json and return category -> list of task names.

    Uses the given split: 'test' (default) for test-set tasks only, 'train', or 'raw'.
    """
    with open(sampled_tasks_path, "r") as f:
        data = json.load(f)
    source = data.get(split, data)
    return {
        category: sorted(labels.keys())
        for category, labels in source.items()
        if isinstance(labels, dict)
    }


def build_skill_to_tasks(
    category_to_tasks: dict,
    skill_to_categories: dict,
    test_skip_tasks: Optional[List[str]] = None,
) -> dict:
    """Build skill -> list of task names from category->tasks and skill->categories.

    If test_skip_tasks is provided, tasks in that list are excluded from every skill.
    """
    skip = set(test_skip_tasks or [])
    result = {}
    for skill, categories in skill_to_categories.items():
        tasks = []
        for cat in categories:
            tasks.extend(category_to_tasks.get(cat, []))
        result[skill] = sorted(set(tasks) - skip)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build skill -> task names JSON from sampled_tasks.json"
    )
    parser.add_argument(
        "--json_path",
        type=str,
        default=DEFAULT_SAMPLED_TASKS_PATH,
        help="Path to sampled_tasks.json",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON path (default: skill_to_tasks.json next to input)",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="test",
        choices=("test", "train", "raw"),
        help="Which split to use for task names: test (default), train, or raw",
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        default="camerabench_pro",
        help="Benchmark folder name in benchmark_config (used for test_skip_tasks)",
    )
    args = parser.parse_args()

    json_path = os.path.abspath(args.json_path)
    if not os.path.isfile(json_path):
        raise SystemExit(f"File not found: {json_path}")

    if args.output:
        out_path = os.path.abspath(args.output)
    else:
        out_dir = os.path.dirname(json_path)
        out_path = os.path.join(out_dir, "skill_to_tasks.json")

    category_to_tasks = load_category_to_tasks(json_path, split=args.split)
    test_skip_tasks = get_test_skip_tasks(args.benchmark)
    skill_to_tasks = build_skill_to_tasks(
        category_to_tasks, SKILL_TO_CATEGORIES, test_skip_tasks=test_skip_tasks
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(skill_to_tasks, f, indent=2)

    print(f"Wrote {len(skill_to_tasks)} skills -> tasks to {out_path}")


if __name__ == "__main__":
    main()
