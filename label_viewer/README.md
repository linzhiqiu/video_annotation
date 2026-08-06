# Quick Start Guide

## 1. Download Videos & Generate Labels

Run `download.py` with your desired configuration:

```bash
# Example 1: Setup labels only
python download.py --json_path video_data/20251021_setup_folder/videos.json \
                   --label_collections cam_setup \
                   --force_regenerate_labels

# Example 2: Motion and setup labels
python download.py --json_path video_data/20251021_ground_and_setup_folder/videos.json \
                   --label_collections cam_motion cam_setup \
                   --force_regenerate_labels

# Example 3: Motion labels only
python download.py --json_path video_data/20251021_ground_folder/videos.json \
                   --label_collections cam_motion \
                   --force_regenerate_labels
```

## 2. Start Label Viewer Server

Navigate to the label viewer directory and run:

```bash
cd label_viewer
python server.py --port 9000
```

The server will start at `http://localhost:9000`

## 3. Setup Pinggy Tunnel

In a separate terminal, run the pinggy command to expose your local server:

```bash
while true; do 
 ssh -p 443 -R0:localhost:9000 -L4302:localhost:4300 \
     -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
     T54hZJGEimN+force@ap.pro.pinggy.io ; 
 sleep 10; 
done
```

Access your label viewer at: **https://label.a.pinggy.link/**

## 4. Generate Pairwise Benchmark

### Step 1: Update Configuration

First, edit `benchmark_config.py` to add your newest folders:

```python
# Update these lines in benchmark_config.py:
CAMERABENCH_PRO_FOLDER_MOTION_ONLY = "cam_motion-20251021_ground_folder"
CAMERABENCH_PRO_FOLDER_SETUP_ONLY = "cam_setup-20251021_setup_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_SETUP = "cam_motion-cam_setup-20251021_ground_and_setup_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_CAMERA = "cam_motion-20251021_ground_and_camera_folder"
CAMERABENCH_PRO_FOLDER_GROUND_AND_SETUP_AND_CAMERA = "cam_motion-cam_setup-20251021_ground_and_camera_and_setup_folder"
```

### Step 2: Run Benchmark Generation

```bash
python pairwise_benchmark.py \
    --folder_name camerabench_pro \
    --max_samples 50 \
    --train_ratio 0.8 \
    --max_imbalance_ratio 3.0 \
    --sampling top \
    --min_samples_threshold 20
```

**What this checks:** The script will warn you if any task has fewer than the threshold (20) samples, helping you identify tasks that need more data.

---

**Quick Tips:**
- Use `--force_regenerate_labels` to rebuild label files from scratch
- Use `--skip_download` to skip video downloads and only process labels
- The pinggy tunnel auto-reconnects if it drops (via the `while true` loop)