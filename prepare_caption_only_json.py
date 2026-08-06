# prepare_caption_only_json.py
from benchmark import ROOT, VIDEO_ROOT, VIDEO_LABELS_DIR, VIDEO_LABEL_FILE, labels_as_dict
from pathlib import Path
import random
import json
from collections import defaultdict
from torch.utils.data import Dataset

from pairwise_benchmark import PairwiseBenchmark, generate_pairwise_datasets, SAMPLING, SEED, TRAIN_RATIO, PAIRWISE_LABELS, VIDEO_LABELS_DIR
from pairwise_caption_benchmark import PairwiseCaptionBenchmark, MAX_SAMPLES, MAX_NEG_SAMPLES, generate_pairwise_caption_dataset


def convert_to_list_vqa(item, question_format="{} Please only answer Yes or No."):
    pos_video, neg_video = item['images']
    pos_prompt, neg_prompt = item['texts']
    vqa_list = []
    for video, prompt, answer in [(pos_video, pos_prompt, "Yes"), (neg_video, neg_prompt, "Yes"), (neg_video, pos_prompt, "No"), (pos_video, neg_prompt, "No")]:
        vqa_list.append({
            "video": video,
            "question": question_format.format(prompt),
            "answer": answer
        })
    return vqa_list

def convert_to_list_caption(item, question_format="Please describe how the camera moves in this video."):
    pos_video, _ = item['images']
    pos_prompt, _ = item['texts']
    caption_list = []
    caption_list.append({
        "video": pos_video,
        "question": question_format,
        "answer": pos_prompt
    })
    return caption_list

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--caption_save_dir", type=str, default="cam_motion-20250227_0324ground_only", help="Directory to save the sampled tasks")
    parser.add_argument("--max_samples", type=int, default=MAX_SAMPLES, help="A (rough) maximum number of (test) samples per task")
    parser.add_argument("--max_neg_samples", type=int, default=MAX_NEG_SAMPLES, help="A (rough) maximum number of negative samples per task")
    parser.add_argument("--split", type=str, default="train", help="Split to use for the benchmark")
    parser.add_argument("--save_path", type=str, default="trainset_caption_only.json", help="Path to save the video name to caption JSON file")
    args = parser.parse_args()
    
    # # Print statistics
    # print_task_statistics(sampled_tasks)
    raw_caption_retrieval = generate_pairwise_caption_dataset(
        caption_save_dir=args.caption_save_dir,
        max_samples=args.max_samples,
        max_neg_samples=args.max_neg_samples,
        # root=ROOT,
        split=args.split,
        video_root=VIDEO_ROOT,
        video_labels_dir=VIDEO_LABELS_DIR,
    )
    
    # import pdb; pdb.set_trace()
    # Create benchmark
    caption_retrieval = PairwiseCaptionBenchmark(raw_caption_retrieval, mode="vqa")
    
    raw_skill_retrieval = generate_pairwise_datasets(
        max_samples=args.max_samples,
        sampling=SAMPLING,
        seed=SEED,
        root=ROOT,
        video_root=VIDEO_ROOT,
        video_labels_dir=VIDEO_LABELS_DIR,
        labels_filename="label_names.json",
        pairwise_labels=PAIRWISE_LABELS,
        train_ratio=TRAIN_RATIO,
        folder_name="motion_dataset"
    )
    skill_retrieval = PairwiseBenchmark(raw_skill_retrieval['sampled_tasks']['train'], mode="vqa")
    
    # print first sample in the dataset
    # print(caption_retrieval.samples[0])
    # print(skill_retrieval.samples[0])
    
    trainset = []
    for item in caption_retrieval.samples:
        trainset.extend(convert_to_list_vqa(item, question_format="{}"))
        trainset.extend(convert_to_list_vqa(item, question_format="{} Please only answer Yes or No."))
    for item in skill_retrieval.samples:
        trainset.extend(convert_to_list_vqa(item, question_format="{}"))
        trainset.extend(convert_to_list_vqa(item, question_format="{} Please only answer Yes or No."))
    
    random.shuffle(trainset)
    print(trainset[0])
    
    caption_generation = PairwiseCaptionBenchmark(raw_caption_retrieval, mode="retrieval")
    # print first sample in the dataset
    print(caption_generation.samples[0])
    
    captionset = []
    for item in caption_generation.samples:
        captionset.extend(convert_to_list_caption(item, question_format="Please describe how the camera moves in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="Describe how the camera moves in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="How does the camera move in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="What is the camera movement in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="Describe the camera movement in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="Can you describe how the camera moves in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="Please describe the camera movement in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="Explain the camera movement in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="Provide an overview of the camera movement in this video."))
        captionset.extend(convert_to_list_caption(item, question_format="How is the camera moving in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="What type of camera movement is used in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="Can you explain the camera movement in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="What kind of camera motion is present in this video?"))
        captionset.extend(convert_to_list_caption(item, question_format="Tell me about the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Identify the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Break down the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Summarize the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Give details about the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Describe the motion of the camera in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="How does the camera move throughout this video?"))
        # captionset.extend(convert_to_list_caption(item, question_format="Explain the dynamics of the camera movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="What camera techniques are used in this video?"))
        # captionset.extend(convert_to_list_caption(item, question_format="Analyze the camera motion in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Break down the camera dynamics in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="What are the key camera movements in this video?"))
        # captionset.extend(convert_to_list_caption(item, question_format="List the camera movements in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Detail the techniques used in the camera’s movement in this video."))
        # captionset.extend(convert_to_list_caption(item, question_format="Provide insights on how the camera moves in this video."))

        
    random.shuffle(captionset)
    print(captionset[0])
    # print size of trainset and captionset
    print(f"Size of captionset: {len(captionset)}")
    
    finalset = captionset
    random.shuffle(finalset)
    print(f"Size of finalset: {len(captionset)}")
    
    from pairwise_benchmark import VIDEO_LABELS_DIR, SAMPLING
    sampling_str = "top" if SAMPLING == "top" else f"random_seed_{SEED}"
    sampled_dir = Path(VIDEO_LABELS_DIR) / "motion_dataset" / f"test_ratio_{1 - TRAIN_RATIO:.2f}_num_{args.max_samples}_sampling_{sampling_str}"
    filename = sampled_dir / args.save_path
    with open(filename, "w") as f:
        json.dump(finalset, f, indent=4)