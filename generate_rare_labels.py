"""
Extract rare labels from the train split of sampled_tasks.json.

Labels are sorted by positive-sample count (fewest first) and accumulated
until the cumulative positive count reaches a given fraction (threshold)
of the total. Negative samples are capped at 3x the positive count per label.

Usage:
    python generate_rare_labels.py --json_path path/to/sampled_tasks.json \
                                   --output_path path/to/rare_labels.json \
                                   --threshold 0.023
"""

import json
import argparse
from typing import Any, Dict, List


def generate_rare_labels(
    input_data: Dict[str, Dict[str, dict]],
    threshold: float = 0.2,
) -> Dict[str, Dict[str, dict]]:
    """Select the rarest labels whose cumulative positives stay within *threshold*.

    Args:
        input_data: The train split, structured as
            ``{ category: { task_key: { "pos": [...], "neg": [...], "task_dict": {...} } } }``.
        threshold: Fraction of total positive samples to include (e.g. 0.023 = ~2.3%).

    Returns:
        A subset of *input_data* containing only the rare labels, with negative
        samples capped at 3× the positive count per label.
    """
    # Collect per-label stats into a flat list.
    stats: List[dict] = []
    total_pos_count = 0

    for category, tasks in input_data.items():
        for task_key, task_content in tasks.items():
            pos_list = task_content.get("pos", [])
            neg_list = task_content.get("neg", [])
            count = len(pos_list)
            total_pos_count += count
            stats.append({
                "category": category,
                "task_key": task_key,
                "pos_count": count,
                "pos_data": pos_list,
                "neg_data": neg_list,
                "task_dict": task_content.get("task_dict", {}),
            })

    # Sort by positive count ascending (rarest first).
    stats.sort(key=lambda x: x["pos_count"])

    # Cumulative target: stop once we've collected this many positives.
    target_limit = total_pos_count * threshold

    rare_labels: Dict[str, Dict[str, dict]] = {}
    current_pos_sum = 0

    for item in stats:
        if current_pos_sum >= target_limit:
            break

        cat = item["category"]
        task_key = item["task_key"]
        pos_samples = item["pos_data"]
        num_pos = len(pos_samples)

        # Cap negatives at 3× the number of positives.
        neg_samples = item["neg_data"]
        max_neg = num_pos * 3
        if len(neg_samples) > max_neg:
            neg_samples = neg_samples[:max_neg]

        if cat not in rare_labels:
            rare_labels[cat] = {}

        rare_labels[cat][task_key] = {
            "task_dict": item["task_dict"],
            "pos": pos_samples,
            "neg": neg_samples,
        }

        current_pos_sum += num_pos

    print(f"Total positives: {total_pos_count}, threshold: {threshold} -> target: {target_limit:.0f}")
    print(f"Selected {sum(len(t) for t in rare_labels.values())} rare labels with {current_pos_sum} positives")

    return rare_labels


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract rare labels from the train split of sampled_tasks.json"
    )
    parser.add_argument(
        "--json_path", required=True, help="Path to sampled_tasks.json"
    )
    parser.add_argument(
        "--output_path", required=True, help="Path to write rare_labels.json"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.023,
        help="Fraction of total positives to include (default: 0.023)",
    )
    args = parser.parse_args()

    with open(args.json_path, "r") as f:
        data = json.load(f)

    result = generate_rare_labels(data["train"], threshold=args.threshold)

    with open(args.output_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"Wrote rare labels to {args.output_path}")


if __name__ == "__main__":
    main()