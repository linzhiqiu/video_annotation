import argparse
import json
import streamlit as st
from llm import get_llm
from tqdm import tqdm

# Constant prompt for video captioning
VIDEO_CAPTION_PROMPT = "Describe this video in a single, concise, and fluent paragraph."

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Generate Gemini captions for videos.")
    parser.add_argument("--input_file", type=str, default="merged_captions_camerabench.json",
                      help="Path to input JSON file (merged_captions_camerabench.json or merged_captions_camerabench_test.json)")
    parser.add_argument("--output_file", type=str, default="merged_captions_camerabench_gemini.json",
                      help="Path to save the output JSON file with Gemini captions")
    parser.add_argument("--model", type=str, default="gemini-2.5-pro-preview-05-06",
                      help="Gemini model to use")
    args = parser.parse_args()

    # Load input data
    data = load_json(args.input_file)
    print(f"Processing {len(data)} videos...")
    
    # Initialize Gemini using Streamlit secrets
    gemini = get_llm(model=args.model, secrets=st.secrets)
    
    # Process each video
    for video_data in tqdm(data, desc="Generating captions", unit="video"):
        try:
            # Generate caption using Gemini
            gemini_caption = gemini.generate(
                prompt=VIDEO_CAPTION_PROMPT,
                video=video_data.get("video_path", ""),
                temperature=0.0
            )
            
            # Add Gemini caption to the data
            video_data["gemini_caption"] = gemini_caption
            
        except Exception as e:
            print(f"Error processing video {video_data.get('video_id', 'unknown')}: {str(e)}")
            video_data["gemini_caption"] = None
    
    # Save results
    save_json(data, args.output_file)
    print(f"Saved Gemini captions to {args.output_file}")

if __name__ == "__main__":
    main() 