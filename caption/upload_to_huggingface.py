import os
import argparse
import requests
from huggingface_hub import HfApi

def upload_videos(local_folder, repo_id):
    """Uploads all .mp4 files from a given local folder to the Hugging Face dataset."""
    api = HfApi()

    # Check if the folder exists
    if not os.path.isdir(local_folder):
        print(f"Error: The folder '{local_folder}' does not exist.")
        return

    files_uploaded = 0

    for filename in os.listdir(local_folder):
        if filename.endswith(".mp4"):
            file_path = os.path.join(local_folder, filename)
            print(f"Uploading {filename}...")

            try:
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=filename,
                    repo_id=repo_id,
                    repo_type="dataset",
                )
                files_uploaded += 1
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    print("\nError: Authentication failed. Please run:")
                    print("huggingface-cli login")
                else:
                    print(f"\nHTTP error: {e}")
                return
            except Exception as e:
                print(f"\nUnexpected error uploading {filename}: {e}")
                print(f"Check if the dataset repository exists: https://huggingface.co/datasets/{repo_id}")
                return

    print(f"\nUpload complete! {files_uploaded} files uploaded.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload .mp4 files to Hugging Face dataset.")
    parser.add_argument("--local_folder", type=str, default="/Users/linzhiqiu/Downloads/captionAnythingVideos",
                        help="Path to the folder containing .mp4 files")
    parser.add_argument("--repo_id", type=str, default="zhiqiulin/video_captioning",
                        help="Hugging Face dataset repository ID")
    args = parser.parse_args()

    upload_videos(args.local_folder)
