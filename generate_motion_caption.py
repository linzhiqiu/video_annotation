# python generate_motion_caption.py --json_path video_data/20250227_0324ground_only/videos.json --label_collections cam_motion
import os
from tqdm import tqdm
import argparse
from process_json import json_to_video_data
from caption_policy.prompt_generator import VanillaCameraMotionPolicy
from llm import get_llm, get_all_llms, get_supported_mode
from download import download_videos, get_video_labels_dir, load_from_json, save_to_json

CAPTION_TASK = "camera_motion"

def get_videos(json_path, label_collections=["cam_motion", "cam_setup"], video_labels_dir="video_labels", video_dir="videos"):
    video_labels_dir = get_video_labels_dir(json_path, label_collections, video_labels_dir)
    video_data_dict = json_to_video_data(json_path, label_collections=label_collections)
    video_data_dict = download_videos(video_data_dict, video_dir=video_dir)
    
    return video_data_dict


def main():
    parser = argparse.ArgumentParser(description="Get labels and video data.")
    parser.add_argument("--json_path", type=str,
                        default="video_data/20250227_0324ground_only/videos.json",
                        help="Path to the JSON file containing video data.")
    parser.add_argument("--label_collections", nargs="+", type=str,
                        default=["cam_motion"],
                        help="List of labelbox project to use.")
    parser.add_argument("--video_dir", type=str,
                        default="videos",
                        help="Output directory to save the downloaded videos.")
    parser.add_argument("--video_labels_dir", type=str,
                        default="video_labels",
                        help="Output directory to save the video labels JSON files.")
    parser.add_argument("--llm", type=str,
                        default="gpt-4o-2024-08-06",
                        choices=["gpt-4o-2024-08-06", "gpt-4o-mini-2024-07-18", "o1-2024-12-17"],
                        help="LLM model to use for captioning.")
    parser.add_argument("--api_key", type=str,
                        default="llm/openai_key.txt",
                        help="Path to the TXT file containing OpenAI API keys.")
    # Siyuan, please only modify the below to name your output file
    parser.add_argument("--save_path", type=str,
                        default="captions.json",
                        help="Path to save the video name to caption JSON file")
    args = parser.parse_args()
    
    video_labels_dir = get_video_labels_dir(args.json_path, args.label_collections, args.video_labels_dir)
    video_data_dict = get_videos(args.json_path, label_collections=args.label_collections, video_labels_dir=args.video_labels_dir, video_dir=args.video_dir)
    caption_program = VanillaCameraMotionPolicy()
    openai_key = open(args.api_key, "r").read().strip()
    chatgpt = get_llm(model=args.llm, secrets={"openai_key": openai_key})
    results = {}
    for video_name, video_data in tqdm(video_data_dict.items()):
        prompt = caption_program(video_data)[CAPTION_TASK]
        try:
            caption = chatgpt.generate(prompt, temperature=0.0)
        except Exception as e:
            print(f"Failed to generate caption for {video_name} because of error: {e}")
            import pdb; pdb.set_trace()
        results[video_name] = {
            "prompt": prompt,
            "caption": caption
        }
    save_path = os.path.join(video_labels_dir, args.save_path)
    save_to_json(results, save_path)
    print(f"Saved captions to {save_path}")
    
if __name__ == "__main__":
    main()
