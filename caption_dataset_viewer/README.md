# Caption Annotation Viewer - Quick Start

## Setup

```bash
cd caption_dataset_viewer/

# Download videos first
python download_videos.py --all

# Start viewer
python viewer.py

# Open http://localhost:8081
```

## Access

Open browser to: **http://localhost:8081/viewer.html**

## Features

- ✅ View only completed annotations
- 📊 All scores displayed directly (no interaction needed)
- 🎯 Highlighted text segments preserved
- 📹 Video playback with download option
- 🔍 Supports all caption types (single, structured, temporal, multiple_annotators)

## Notes

- Port 8081 (different from annotation server on 8080)
- Read-only interface
- Automatically filters incomplete annotations