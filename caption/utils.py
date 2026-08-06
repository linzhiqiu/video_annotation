import cv2
import numpy as np
from typing import List
import json
import os
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


def extract_frames(video_path: str, frame_numbers: List[int]) -> List[np.ndarray]:
    """
    Extracts a specific frame from a video using OpenCV and converts it to RGB format.

    Parameters:
        video_path (str): Path or URL to the video file.
        frame_number (List[int]): The frame indices to extract. Supports negative indices:
                            -1 refers to the last frame, -2 to the second last, etc.

    Returns:
        List[np.ndarray]: The extracted frame in RGB format.
    
    Raises:
        ValueError: If the video cannot be opened or the frame number is out of range.
        RuntimeError: If the frame extraction fails.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        # try:
        #     local_video_path = "video.mp4"
        #     urllib.request.urlretrieve(video_path, local_video_path)
        #     cap = cv2.VideoCapture(local_video_path)
        # except:
        raise ValueError(f"Error: Unable to open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames = []
    
    for frame_number in frame_numbers:

        # Convert negative indices to positive (e.g., -1 -> last frame)
        if frame_number < 0:
            frame_number = total_frames + frame_number  # Adjust for negatives

        if frame_number < 0 or frame_number >= total_frames:
            raise ValueError(f"Error: Frame number {frame_number} is out of range (0 to {total_frames - 1})")

        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
        # Read the frame
        ret, frame = cap.read()

        if not ret:
            raise RuntimeError(f"Error: Unable to extract frame {frame_number} from {video_path}")

        # Convert BGR to RGB for easier visualization
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)

    cap.release()
    return frames

def get_middle_frame_index(video_path: str) -> int:
    """
    Get the index of middle frame of a video using OpenCV.

    Parameters:
        video_path (str): Path or URL to the video file.

    Returns:
        frame_index (int): The middle frame index.
    
    Raises:
        ValueError: If the video cannot be opened.
        RuntimeError: If the frame extraction fails.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Error: Unable to open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame_index = total_frames // 2  # Get the middle frame index

    cap.release()

    return middle_frame_index


def get_last_frame_index(video_path: str) -> int:
    """
    Get the index of the last frame of a video using OpenCV.

    Parameters:
        video_path (str): Path or URL to the video file.

    Returns:
        frame_index (int): The last frame index.

    Raises:
        ValueError: If the video cannot be opened.
        RuntimeError: If the frame extraction fails.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Error: Unable to open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    last_frame_index = total_frames - 1  # Get the last frame index

    cap.release()

    return last_frame_index


if __name__ == "__main__":
    # Example usage
    video_path = "your_video.mp4"

    # Extract first and last frames using positive and negative indices
    first_frame = extract_frame(video_path, 0)
    last_frame = extract_frame(video_path, -1)  # Using negative index for last frame
