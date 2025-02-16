from huggingface_hub import list_repo_files

def retrieve_all_urls(dataset_repo: str, file_extension: str) -> list:
    # Get all files in the dataset
    files = list_repo_files(repo_id=f"{dataset_repo}", repo_type="dataset")

    # Filter .mp4 files and create URLs
    mp4_urls = [
        f"https://huggingface.co/datasets/{dataset_repo}/resolve/main/{file}"
        for file in files if file.endswith(".mp4")
    ]

    return mp4_urls

if __name__ == "__main__":
    dataset_repo = "zhiqiulin/video_captioning"
    file_extension = ".mp4"

    urls = retrieve_all_urls(dataset_repo, file_extension)
    print(urls)