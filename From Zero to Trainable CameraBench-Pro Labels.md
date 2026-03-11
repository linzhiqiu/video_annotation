## From Zero to Trainable CameraBench-Pro Labels

### 1. Clone Video Annotation repo

```
git clone https://github.com/linzhiqiu/video_annotation.git
cd video_annotation
```

Then build your environment following the `README.md` under this repo.

### 2. Clone LabelPizza repo

```bash
# Omit building conda environment here
# clone and set up
git clone https://github.com/linzhiqiu/label_pizza.git
cd label_pizza
```

Then build your environment following the `README.md` under this repo.

### 3. Export videos and raw annotating labels

```python
from label_pizza.db import init_database
init_database("DBURL")

from label_pizza.export_utils import export_videos
export_videos(output_path="./workspace/videos.json")

from label_pizza.export_utils import export_ground_truths
export_ground_truths(output_folder="./workspace/ground_truths")
```

### 4. Modify annotating labels to caption labels

```bash
# Go back to Video Annotation repo
cd ..
```

Run `python transfer_caption_labels.py`

It will results in 5 new folders:

```
<YYYYMMDD>_ground_folder
<YYYYMMDD>_setup_folder
<YYYYMMDD>_ground_and_setup_folder
<YYYYMMDD>_ground_and_camera_folder
<YYYYMMDD>_ground_and_camera_and_setup_folder
```

### 5. Modify caption labels to CameraBench-Pro labels

Run `download.py` with your desired configuration:

```python
# Replace <YYYYMMDD> with the date you have generated (e.g., 20260311)

# Example 1: Setup labels only
python download.py --json_path video_data/<YYYYMMDD>_setup_folder/videos.json \
                   --label_collections cam_setup \
                   --force_regenerate_labels

# Example 2: Motion and setup labels
python download.py --json_path video_data/<YYYYMMDD>_ground_and_setup_folder/videos.json \
                   --label_collections cam_motion cam_setup \
                   --force_regenerate_labels

# Example 3: Motion labels only
python download.py --json_path video_data/<YYYYMMDD>_ground_folder/videos.json \
                   --label_collections cam_motion \
                   --force_regenerate_labels

# Example 4: Motion (ground and camera) labels
python download.py --json_path video_data/<YYYYMMDD>_ground_and_camera_folder/videos.json \
                   --label_collections cam_motion \
                   --force_regenerate_labels

# Example 5: Motion (ground and camera) and setup labels
python download.py --json_path video_data/<YYYYMMDD>_ground_and_camera_and_setup_folder/videos.json \
                   --label_collections cam_motion cam_setup \
                   --force_regenerate_labels
```

### 6. Generate pairwise benchmark

#### 6.1. Update configuration

First, edit `benchmark_config.py` to add your newest folders:

```
# Update these lines in benchmark_config.py:
CAMERABENCH_PRO_FOLDER_MOTION_ONLY = "cam_motion-20260311_ground_folder"
CAMERABENCH_PRO_FOLDER_SETUP_ONLY = "cam_setup-20260311_setup_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_SETUP = "cam_motion-cam_setup-20260311_ground_and_setup_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_CAMERA = "cam_motion-20260311_ground_and_camera_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_SETUP_AND_CAMERA = "cam_motion-cam_setup-20260311_ground_and_camera_and_setup_folder"
```

#### 6.2. Run benchmark generation

Run `python pairwise_benchmark.py` to get trainable labels

| Argument                  | Default          | Description                                                  |
| ------------------------- | ---------------- | ------------------------------------------------------------ |
| `--folder_name`           | `motion_dataset` | Dataset folder (must be in `FOLDER_NAMES`)                   |
| `--max_samples`           | `20`             | Max test samples per task                                    |
| `--sampling`              | `top`            | `top` (first N) or `random`                                  |
| `--seed`                  | `0`              | Random seed (for `sampling=random`)                          |
| `--train_ratio`           | `0.5`            | Train split ratio; `1.0` = no test set                       |
| `--max_imbalance_ratio`   | `None`           | Max pos/neg ratio in train (e.g. `2.0`); mutually exclusive with `--balance_train` |
| `--balance_train`         | `False`          | Balance train like test; mutually exclusive with `--max_imbalance_ratio` |
| `--min_samples_threshold` | `25`             | Warn if any task has fewer samples                           |
| `--show_folder_info`      | `False`          | Print folder info and exit                                   |

For example:

```
python pairwise_benchmark.py \
    --folder_name camerabench_pro \
    --max_samples 20 \
    --train_ratio 0.8 \
    --max_imbalance_ratio 3.0 \
    --sampling random \
    --min_samples_threshold 20
```

### 7. Generate and check the status of splitted dataset

8:2 training set

```
python pairwise_benchmark.py \
    --folder_name camerabench_pro \
    --max_samples 20 \
    --train_ratio 0.8 \
    --max_imbalance_ratio 3.0 \
    --sampling random \
    --min_samples_threshold 20
```

10:0 training set

```
python pairwise_benchmark.py \
    --folder_name camerabench_pro \
    --max_samples 20 \
    --train_ratio 1.0 \
    --max_imbalance_ratio 3.0 \
    --sampling random \
    --min_samples_threshold 20
```

Run the following code to check the rare labels:
```python
import json

with open('./video_labels/camerabench_pro/test_ratio_0.20_<YYYY_MM_DD>_num_20_sampling_random_seed_0_train_posneg_max_ratio_3.0/sampled_tasks.json', 'r') as f:
    sampled_tasks = json.load(f)

test_tasks = sampled_tasks['test']
train_tasks = sampled_tasks['train']

for key, value in test_tasks.items():
    for k, v in value.items():
        # if k in labels:
        #     print(k, len(v['pos']), len(train_tasks[key][k]['pos']))
        pos_cases = v['pos']
        if len(pos_cases) <= 10:
            print(k, len(pos_cases), len(train_tasks[key][k]['pos']))
```

For example, it will show:
```bash
Labelname, test_cases, train_cases
has_frame_freeze_or_not 8 8
crane_up_vs_crane_down 9 24
only_pan_right_vs_only_truck_right 10 28
only_tilt_down_vs_only_pedestal_down 10 25
has_crane_down 9 8
only_pan_right_vs_has_pan_right_and_not_only 10 28
only_tilt_down_vs_has_tilt_down_and_not_only 10 28
fast_motion_without_time_lapse 10 21
broadcast_pov 10 16
dashcam_pov 10 12
overhead_pov 10 21
screen_recording_pov 10 10
is_just_clear_subject_dynamic_size_shot 10 24
is_just_back_and_forth_change_shot 10 25
height_wrt_subject_from_above_subject_to_below_subject 8 7
height_wrt_subject_from_at_subject_to_below_subject 10 18
focus_from_background_to_foreground 8 9
focus_from_background_to_middle_ground 2 7
focus_from_middle_ground_to_foreground 10 19
```

### 8. Delete the labels that have totally less than 10 cases (in total)

From `7.`, we notice that label `focus_from_background_to_middle_ground` only gets 7 + 2 = 9 cases.

Run `python remove_rare_labels_testset.py --json_path path/to/sampled_tasks.json`

For example, run `python remove_rare_labels_testset.py --json_path ./video_labels/camerabench_pro/test_ratio_0.20_2026_03_11_num_20_sampling_random_seed_0_train_posneg_max_ratio_3.0/sampled_tasks.json`

### 9. Add rack focus into 8:2 and 10:0 dataset

```bash
# Add rack focus videos (default: split across train/test)
python add_rack_focus.py --json_path path/to/sampled_tasks.json

# Add rack focus videos with custom path
python add_rack_focus.py --json_path path/to/sampled_tasks.json \
                         --rack_focus_path path/to/rack_focus_videos.json

# Add all videos to train split only
python add_rack_focus.py --json_path path/to/sampled_tasks.json --is_full_train
```

- `--rack_focus_path` already has a default in the script, so you don't need to pass it unless you want a custom path. No need to write `{with default path}` in the README.

- `--is_full_train` is a boolean flag (`action="store_true"`), so you just include it or omit it — you don't write `default false`. Present = `True`, absent = `False`.

To add this, run:
```bash
python add_rack_focus.py --json_path ./video_labels/camerabench_pro/test_ratio_0.20_2026_03_11_num_20_sampling_random_seed_0_train_posneg_max_ratio_3.0/sampled_tasks.json
```

and

```
python add_rack_focus.py --json_path ./video_labels/camerabench_pro/test_ratio_0.00_2026_03_11_num_20_sampling_random_seed_0_train_posneg_max_ratio_3.0/sampled_tasks.json --is_full_train True
```

Separately.

### 10. Generate rare labels

```bash
python generate_rare_labels.py \
    --json_path path/to/sampled_tasks.json \
    --output_path path/to/rare_labels.json \
    --threshold 0.023
```

