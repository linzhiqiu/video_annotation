# process_json.py
from video_data import VideoData
import json
import argparse


def json_to_video_data(json_path, label_collections=["cam_motion", "cam_setup", "lighting_setup"]):
    """Load video data from a JSON file and return a dictionary of VideoData objects."""
    with open(json_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    video_data_dict = {}
    for video in loaded_data:
        tmp_data = VideoData()
        for label_collection in label_collections:
            if label_collection in video:
                setattr(tmp_data, label_collection, video[label_collection])
        # if 'cam_motion' in video:
        #     tmp_data.cam_motion = video['cam_motion'] # will be converted to CameraMotionData automatically using setter()
        # if 'cam_setup' in video:
        #     tmp_data.cam_setup = video['cam_setup']
        video_url = None
        for key, value in video["workflows"].items():
            
            tmp_data.add_workflow(key, value)
            videoname = value['video_name']
            if video_url is None:
                video_url = tmp_data.workflows[key].video_url
            else:
                assert video_url == tmp_data.workflows[key].video_url, f"Video URL mismatch for {videoname}. {video_url} != {tmp_data.workflows[key].video_url}"
        video_data_dict[videoname] = tmp_data
    return video_data_dict

def main():
    parser = argparse.ArgumentParser(description="Process video data from a JSON file.")
    parser.add_argument("--json_path", type=str,
                        default="video_data/20250218_1042/videos.json",
                        help="Path to the JSON file containing video data.")
    parser.add_argument("--label_collections", nargs="+", type=str,
                        default=["cam_motion", "cam_setup", "lighting_setup"],
                        help="List of labelbox project to use.")
    args = parser.parse_args()
    
    video_data_dict = json_to_video_data(args.json_path, args.label_collections)
    print(f"Loaded {len(video_data_dict)} video data entries.")

if __name__ == '__main__':
    main()
