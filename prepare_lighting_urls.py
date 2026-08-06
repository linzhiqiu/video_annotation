import os
import json
import argparse
from process_json import json_to_video_data
from label import Label, extract_labels_dict

# HF_PREFIX = "https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/"


def save_to_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_from_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_valid_labels_dict(
    video_data_dict, label_collections=["cam_motion", "cam_setup", "lighting_setup"]
):
    video_data_list = list(video_data_dict.values())
    labels = Label.load_all_labels()
    all_valid_labels_dict = {}
    for label_collection in label_collections:
        labels_dict = extract_labels_dict(
            getattr(labels, label_collection), label_collection
        )
        invalid_labels = []
        for label_name, label in labels_dict.items():
            # call verify()
            try:
                label.verify(video_data_list)
            except Exception as e:
                print(f"Skipping {label_name}: {e}")
                invalid_labels.append(label_name)
                continue
        if len(invalid_labels) > 0:
            print(
                f"Skipping {len(invalid_labels)} invalid labels for {label_collection}: {invalid_labels}"
            )
            for label_name in invalid_labels:
                labels_dict.pop(label_name)
        all_valid_labels_dict.update(labels_dict)

    return all_valid_labels_dict


def prepare_url_files(
    json_path,
    label_collections=["cam_motion", "cam_setup", "lighting_setup"],
    output_dir="caption/video_urls/lighting_120",
):
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load video data
    print(f"Loading video data from {json_path}")
    video_data_dict = json_to_video_data(json_path, label_collections=label_collections)
    print(f"Loaded {len(video_data_dict)} videos")

    # Get valid labels
    valid_labels_dict = get_valid_labels_dict(
        video_data_dict, label_collections=label_collections
    )

    # Check each video for shot_transition label
    video_data_list = list(video_data_dict.values())

    # Prepare URLs for all three files
    all_labels_urls = []
    invalid_videos_urls = []
    lighting_only_urls = []

    # Find shot_transition labels across all label collections
    shot_transition_labels = []
    for label_name in valid_labels_dict:
        if "shot_transition" in label_name:
            shot_transition_labels.append(valid_labels_dict[label_name])
            print(f"Found shot_transition label: {label_name}")

    if not shot_transition_labels:
        print("Warning: No shot_transition labels found!")

    # Organize labels by collection
    labels_by_collection = {"cam_motion": [], "cam_setup": [], "lighting_setup": []}

    for label_name, label in valid_labels_dict.items():
        collection = label_name.split(".")[0]
        if collection in labels_by_collection:
            labels_by_collection[collection].append(label)

    # Check each video
    for video_name, video_data in video_data_dict.items():
        video_url = video_data.get_video_url()

        # Check if video has shot_transition label
        is_invalid = False
        for label in shot_transition_labels:
            if video_data in label.pos(video_data_list):
                invalid_videos_urls.append(video_url)
                is_invalid = True
                break

        if is_invalid:
            continue

        # Check if video has labels from all three collections
        has_all_collections = True
        for collection, labels in labels_by_collection.items():
            collection_has_label = False
            for label in labels:
                if video_data in label.pos(video_data_list):
                    collection_has_label = True
                    break
            if not collection_has_label:
                has_all_collections = False
                break

        if has_all_collections:
            all_labels_urls.append(video_url)
        else:
            # Check if it has any lighting_setup label
            has_lighting = False
            for label in labels_by_collection["lighting_setup"]:
                if video_data in label.pos(video_data_list):
                    has_lighting = True
                    break

            if has_lighting:
                lighting_only_urls.append(video_url)

    # Save URL files
    all_labels_path = os.path.join(output_dir, "all_labels.json")
    invalid_videos_path = os.path.join(output_dir, "invalid_videos.json")
    lighting_only_path = os.path.join(output_dir, "lighting_only.json")

    save_to_json(all_labels_urls, all_labels_path)
    save_to_json(invalid_videos_urls, invalid_videos_path)
    save_to_json(lighting_only_urls, lighting_only_path)

    print(
        f"All labels (videos with all 3 collections): {len(all_labels_urls)} videos saved to {all_labels_path}"
    )
    print(
        f"Invalid videos (with shot_transition): {len(invalid_videos_urls)} videos saved to {invalid_videos_path}"
    )
    print(
        f"Lighting only (remaining valid videos with lighting): {len(lighting_only_urls)} videos saved to {lighting_only_path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Prepare URL files for video captioning."
    )
    parser.add_argument(
        "--json_path",
        type=str,
        # default="video_data/20250324_1616_all_labels/videos.json",
        # default="video_data/20250328_1455_lighting_120/videos.json", # Before April 14
        default="video_data/20250406lighting_only/videos.json", # After April 14 then 16
        help="Path to the JSON file containing video data.",
    )
    parser.add_argument(
        "--label_collections",
        nargs="+",
        type=str,
        # default=["cam_motion", "cam_setup", "lighting_setup"],
        default=["lighting_setup"],
        help="List of labelbox project to use.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        # default="caption/video_urls/lighting_120_new", # Before April 14
        # default="caption/video_urls/lighting_250_new", # After April 14
        default="caption/video_urls/lighting_280_new", # After April 16
        help="Output directory for URL files.",
    )
    args = parser.parse_args()

    prepare_url_files(
        args.json_path,
        label_collections=args.label_collections,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
