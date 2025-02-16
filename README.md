## **VideoData: A Structured Representation for Video Metadata**

This repository contains `video_data.py`, which provides a structured way to handle video-related metadata, including **camera motion**, **camera setup**, and **lighting setup**. It ensures proper initialization, verification, and prevents direct instantiation of dependent objects.

---

### **🚀 Quick Start**
```python
from video_data import VideoData
from camera_motion_data import camera_motion_params_demo
import json

# Create a VideoData object
video_sample = VideoData()

# 🔹 Initializing cam_motion
# You can initialize cam_motion with a dictionary of parameters or a CameraMotionData instance
# However, you should never create a CameraMotionData instance directly without using its create() function.

video_sample.cam_motion = camera_motion_params_demo  # Correct way to set

# 🔹 Displaying camera_motion_params_demo dictionary
print("camera_motion_params_demo:")
print(json.dumps(camera_motion_params_demo, indent=4))

# 🔹 Trying to access an uninitialized attribute (this will raise an error)
print(f"If you try to access cam_setup before setting it, it will raise an Error.")
try:
    print(video_sample.cam_setup)
except AttributeError as e:
    print(f"AttributeError: {e}")
```

---

### **🔹 Rules for Initialization**
✅ You **must use** the `.create()` function for `CameraMotionData`, `CameraSetupData`, and `LightingSetupData`.  
✅ You **should not** create instances of these classes manually.  
✅ Uninitialized attributes will **raise an `AttributeError`** when accessed.  

---

### **📂 File Structure**
```
├── video_data.py         # Main VideoData class
├── camera_motion_data.py # CameraMotionData with create() function
├── camera_setup_data.py  # CameraSetupData with create() function
├── lighting_setup_data.py# LightingSetupData with create() function
├── visualize_labels.py   # Script to generate Markdown visualization
├── labels/               # Directory containing label definitions
│   ├── cam_motion/       # Camera motion-related labels
│   │   ├── steadiness/   # Steadiness-related labels
│   │   │   ├── fixed_camera.json  # Example label file
│   │   ├── cam_setup/        # Camera setup-related labels
│   ├── lighting_setup/   # Lighting-related labels
└── README.md             # This file
```

---

### **🆕 How to Add a New Label JSON File**
To add a new label, create a JSON file in the appropriate subdirectory under `labels/`. Each label should follow a structured format. 

#### **Example: `labels/cam_motion/steadiness/fixed_camera.json`**
```json
{
  "label": "Fixed Camera (Stable)",
  "label_name": "fixed_camera",
  "def_question": [
    "Is the camera completely still without any motion or shaking?",
    "Is the camera locked off without any instability?"
  ],
  "alt_question": [
    "Is the camera still?",
    "Is the camera fixed?"
  ],
  "def_prompt": [
    "A video where the camera remains completely still with no motion or shaking."
  ],
  "alt_prompt": [
    "A video with a still camera."
  ],
  "pos_rule_str": "self.cam_motion.steadiness in ['static'] and self.cam_motion.camera_movement in ['no']",
  "neg_rule_str": "self.cam_motion.steadiness not in ['static']"
}
```
- Place the file under its corresponding category in `labels/`.
- Ensure the file follows the **same structure** as the example.

---
### Download real-time data from labelbox

#### Pre-requisite:

##### Under the video_annotation folder:
```
Video_annotation
├── scripts
│   ├── export_labelbox_data.py
├── configs
│   ├── label_box_export.yaml
```

#### Run

`python scripts/export_labelbox_data.py`

#### Output

The output contains 2 folder `ndjson`  and `issues_ndjson`. They are stored at the param `output_folder` in the file `label_box_export.yaml`.



### Filter out ndjson file

#### Pre-requisite

##### Under the video_annotation folder:

```
Video_annotation
├── scripts
│   ├── export_labelbox_data.py
├── configs
│   ├── label_box_export.yaml
├── exports
│   ├── ndjson
│   │   ├── project1.ndjson (contains video_names and labels from that project)
│   │   ├── project2.ndjson
│   │   ├── ...
│   ├── issues_ndjson 
│   │   ├── project1_issues.ndjson (contains video_names that have issue)
│   │   ├── project2_issues.ndjson
│   │   ├── ...
│   ├── sheets (contains info like approver and double_check status)
```

The number of projects is defined in your `label_box_export.yaml`.

#### Run

`python test_batch.py`

##### Important params:

1. `yaml_paths:`  List, specify the yaml files that used for filtering.

2. ` ndjson_dir:`  str, dir of the ndjson, here it should be ` exports/ndjson` 

3. ` issues_dir:` str, dir of the ndjson, here it should be ` exports/issues_ndjson` 

4. `preloaded_sheet_path`: str, path to provide double check status and approver's name.

   ```
   batch = Batch.from_configs(
       yaml_paths, 
       ndjson_dir, 
       issues_dir,
       preloaded_sheet_path=preloaded_sheet_path,
       save_sheet_data=True,
       save_batch=True,
       batch_name="enter_the_output_folder_name_here"
   )
   ```



### Trans ndjson file to VideoData List

 #### Run

`python scripts/process_ndjson.py`

The output will be a list, each item in it is a VideoData object.



### Pretest Scoring and PDF Generation

This section explains how to export Labelbox data, score pretests, and generate PDF reports.

#### 1. Export Labelbox Data for Scoring

First, you need to export the data from Labelbox using `export_pretests_labelbox_data.py`:

```bash
python scripts/export_pretests_labelbox_data.py
```

Configuration is controlled through `configs/scoring_config.yaml`:

```yaml
# Key configuration options:
api_key: "your_labelbox_api_key"
output_dir: "exports_pretests"  # Directory for NDJSON exports
pdfs_dir: "pretest_pdfs"       # Directory for generated PDFs
overwrite_exports: true        # Whether to overwrite existing exports

# Export parameters (all optional):
export_params:
  attachments: false
  metadata_fields: false
  data_row_details: true
  project_details: true
  label_details: true
  performance_details: true
  interpolated_frames: false
  embeddings: false
```

#### 2. Generate PDF Reports

After exporting the data, use `process_pretest_labelbox_data.py` to generate PDF reports:

```bash
python scripts/process_pretest_labelbox_data.py
```

##### PDF Generation Options

The `scoring_config.yaml` supports several PDF generation options under the `pdf_generation` section:

```yaml
pdf_generation:
  skip_existing: true           # Skip PDFs that already exist
  target_annotator: null        # Generate PDFs for specific annotator only
  target_ground_truth: null     # Use specific ground truth file only
```

##### Project Configuration

Projects are configured in `scoring_config.yaml` under the `projects` section:

```yaml
projects:
  test_type:                    # e.g., shotcomp, motion, lighting
    test0:                      # Test number
      ground_truth_annotator:   # Ground truth configuration
        project_id: "project_id"
        email: "annotator@email.com"
      ids:                      # Project IDs to process
        - "project_id1"
        - "project_id2"
```

#### 3. Output Structure

The script creates the following directory structure:

```
workspace/
├── exports_pretests/          # Raw exports from Labelbox
│   ├── test_type/
│   │   └── ndjson/           # NDJSON files from each project
├── pretest_pdfs/             # Generated PDF reports
│   ├── test_type/
│   │   ├── test0/           # PDFs organized by test number
│   │   └── test1/
│   └── new/                  # Only contains newly generated PDFs
```

