"""
Remove labels whose total positive cases (test + train) are <= 10,
then overwrite the original sampled_tasks.json with the filtered result.
"""

import json
import argparse

parser = argparse.ArgumentParser(description="Remove labels with <= N total positive cases from sampled_tasks.json")
parser.add_argument("--json_path", required=True, help="Path to sampled_tasks.json")
parser.add_argument("--min_total_pos", type=int, default=10, help="Remove labels with total (test+train) positive cases <= this (default: 10)")
args = parser.parse_args()

json_path = args.json_path
min_total_pos = args.min_total_pos

with open(json_path, 'r') as f:
    sampled_tasks = json.load(f)

test_tasks = sampled_tasks['test']
train_tasks = sampled_tasks['train']

removed = []

for category, labels in list(test_tasks.items()):
    for label in list(labels.keys()):
        total_pos = len(test_tasks[category][label]['pos']) + len(train_tasks[category][label]['pos'])
        if total_pos <= min_total_pos:
            removed.append((category, label, total_pos))
            del test_tasks[category][label]

# Report what was removed
print(f"Removed {len(removed)} labels with <= {min_total_pos} total positive cases:")
for category, label, count in removed:
    print(f"  {category} / {label} ({count} pos)")

with open(json_path, 'w') as f:
    json.dump(sampled_tasks, f, indent=2)

print(f"\nUpdated file saved to {json_path}")