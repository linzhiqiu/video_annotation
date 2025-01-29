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

# 🔹 Initializing camera_motion_data
# You can initialize camera_motion_data with a dictionary of parameters or a CameraMotionData instance
# However, you should never create a CameraMotionData instance directly without using its create() function.

video_sample.camera_motion_data = camera_motion_params_demo  # Correct way to set

# 🔹 Displaying camera_motion_params_demo dictionary
print("camera_motion_params_demo:")
print(json.dumps(camera_motion_params_demo, indent=4))

# 🔹 Trying to access an uninitialized attribute (this will raise an error)
print(f"If you try to access camera_setup_data before setting it, it will raise an Error.")
try:
    print(video_sample.camera_setup_data)
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
└── README.md             # This file
```

---

### **📜 License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
