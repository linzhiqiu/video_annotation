import cv2
import numpy as np
from typing import List
import json
import base64
import os
from PIL import Image
import urllib.request

# Load text data from a given file
def load_text(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()

# Load configuration from a JSON file
def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

# Load JSON data from a given file
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}


def extract_frames_to_pil(video_path: str, frame_numbers: List[int]) -> List[Image.Image]:
    """
    Extracts specific frames from a video using OpenCV and converts them to PIL Image objects.

    Parameters:
        video_path (str): Path to the video file.
        frame_numbers (List[int]): List of frame indices to extract. Supports negative indices.

    Returns:
        List[Image.Image]: List of extracted frames as PIL Image objects.

    Raises:
        ValueError: If the video cannot be opened.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        try:
            local_video_path = "video.mp4"
            urllib.request.urlretrieve(video_url, local_video_path)
            cap = cv2.VideoCapture(local_video_path)
        except:
            raise ValueError(f"Error: Unable to open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pil_images = []

    for frame_number in frame_numbers:
        # Convert negative indices to positive (e.g., -1 -> last frame)
        if frame_number < 0:
            frame_number = total_frames + frame_number  # Adjust for negatives

        # Check frame number validity
        if frame_number < 0 or frame_number >= total_frames:
            print(f"Warning: Frame number {frame_number} is out of range (0 to {total_frames - 1}). Skipping...")
            continue  # Skip invalid frames instead of raising an error

        # Set the frame position and read it
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            print(f"Warning: Unable to extract frame {frame_number}. Skipping...")
            continue

        # Convert BGR (OpenCV format) to RGB (PIL format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        pil_image = Image.fromarray(frame_rgb)
        pil_images.append(pil_image)

    cap.release()
    return pil_images


def extract_frames_to_base64(video_path: str, frame_numbers: List[int]) -> List[str]:
    """
    Extracts specific frames from a video using OpenCV and converts them to base64 format.

    Parameters:
        video_path (str): Path to the video file.
        frame_numbers (List[int]): List of frame indices to extract. Supports negative indices.

    Returns:
        List[str]: List of base64-encoded JPEG images.

    Raises:
        ValueError: If the video cannot be opened.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Error: Unable to open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    base64_images = []

    for frame_number in frame_numbers:
        # Convert negative indices to positive (e.g., -1 -> last frame)
        if frame_number < 0:
            frame_number = total_frames + frame_number  # Adjust for negatives

        # Check frame number validity
        if frame_number < 0 or frame_number >= total_frames:
            print(f"Warning: Frame number {frame_number} is out of range (0 to {total_frames - 1}). Skipping...")
            continue  # Skip invalid frames instead of raising an error

        # Set the frame position and read it
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            print(f"Warning: Unable to extract frame {frame_number}. Skipping...")
            continue

        # # Convert BGR to RGB
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode as JPEG and convert to base64
        # _, buffer = cv2.imencode(".jpg", frame_rgb)
        _, buffer = cv2.imencode(".jpg", frame)
        base64_image = base64.b64encode(buffer).decode("utf-8")
        base64_images.append(base64_image)

    cap.release()
    return base64_images