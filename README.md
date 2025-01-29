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
│   ├── cam_setup/        # Camera setup-related labels
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

### **📖 How to Visualize Labels in Markdown**
Use `visualize_labels.py` to convert all JSON label definitions into a Markdown visualization.

#### **🔹 Running the Script**
```bash
python visualize_labels.py
```
- This will process all JSON files under `labels/` and generate a **structured Markdown output** in `labels_markdown/`.
- Each folder will have an `index.md` containing **collapsible sections** for easy browsing.

#### **🔗 View the Generated Labels**
After running the script, open:
- **[`labels.md`](./labels.md)** for a structured overview.
- **Individual category pages** in `labels_markdown/` for specific topics.

---

### **📜 License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.