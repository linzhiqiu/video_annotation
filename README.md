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

### **🔹 TODO**
- Implement a Label class for binary labelling + VQA generation + CLIP-prompt generation.
- Implement a test function to make sure: (1) Pos and Neg are non-overlapping, (2) Easy/Hard negs are strict subset of Neg.

---

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
└── README.md             # This file
```

---

### **📜 License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
