# pairwise_caption_benchmark.py
from benchmark import ROOT, VIDEO_ROOT, VIDEO_LABELS_DIR, VIDEO_LABEL_FILE, labels_as_dict
from pathlib import Path
import random
import json
from collections import defaultdict
from torch.utils.data import Dataset

MAX_SAMPLES = 80
MAX_NEG_SAMPLES = 4

from pairwise_benchmark import PairwiseBenchmark


class PairwiseCaptionBenchmark(PairwiseBenchmark):
    """
    Dataset class for pairwise caption tasks (VQA or retrieval).
    
    Args:
        skills: List of skills, where each skill contains multiple tasks
        mode: Task mode, one of "vqa", "vqa_generation", or "retrieval"
    """
    def __init__(self, skills, mode="vqa",
                 question_format="Does the camera movement in this video match the following description: '{}'?"):
        valid_modes = ["vqa", "vqa_generation", "retrieval"]
        if mode not in valid_modes:
            raise ValueError(f"Mode must be one of {valid_modes}, got {mode}")
        
        self.mode = mode
        self.skills = []
        self.tasks = []
        self.skill_to_sample_ids = {}
        self.skill_to_tasks = {}
        self.task_to_sample_ids = {}
        self.samples = []
        self.task_to_metadata = {}
        self.question_format = question_format
        
        for skill in skills:
            self.skills.append(skill)
            self.skill_to_tasks[skill] = []
            self.skill_to_sample_ids[skill] = []
            
            for task in skills[skill]:
                self.skill_to_tasks[skill].append(task)
                self.tasks.append(task)
                self.task_to_sample_ids[task] = []
                
                pos_videos = skills[skill][task]['pos']
                neg_videos = skills[skill][task]['neg']
                pos_captions = skills[skill][task]['pos_caption']
                neg_captions = skills[skill][task]['neg_caption']
                
                self.task_to_metadata[task] = {
                    "skill": skill,
                }
                
                assert len(pos_videos) == len(neg_videos), f"Number of positive and negative videos must match for task {task}"
                for pos_video, neg_video, pos_caption, neg_caption in zip(pos_videos, neg_videos, pos_captions, neg_captions):
                    sample_id = len(self.samples)
                    self.skill_to_sample_ids[skill].append(sample_id)
                    self.task_to_sample_ids[task].append(sample_id)
                    assert pos_video != neg_video, f"Positive and negative videos must be different for task {task}, caption {pos_caption} vs {neg_caption} at pos_video {pos_video}"
                    
                    # Important to make 0th the Positive Image and 1st the Negative Image
                    images = [pos_video, neg_video]
                    if self.mode in ["vqa", "vqa_generation"]:
                        texts = [self.question_format.format(pos_caption), self.question_format.format(neg_caption)]
                    elif self.mode == "retrieval":
                        texts = [pos_caption, neg_caption]
                    
                    self.samples.append({
                        "images": images,
                        "texts": texts
                    })


def print_detailed_caption_task_statistics(tasks):
    """
    Print statistics about the original, train, and test task distributions.

    Args:
        raw_tasks: Dictionary of original pairwise tasks.
        train_tasks: Dictionary of train set pairwise tasks.
        test_tasks: Dictionary of test set pairwise tasks.
    """
    print("\n===== Task Statistics =====")
    print(f"{'Skill/Task':<60} {'Orig Pos':<10} {'Orig Neg':<10} {'Train Pos':<10} {'Train Neg':<10} {'Test Pos':<10} {'Test Neg':<10}")
    print("-" * 110)

    pos_videos = set()
    neg_videos = set()
    video_count = defaultdict(lambda: 0)
    for skill_name in tasks:
        print(f"\n{skill_name}:")
        skill_total = 0
        for task_name in tasks[skill_name]:
            pos_videos = tasks[skill_name][task_name]["pos"]
            neg_videos = tasks[skill_name][task_name]["neg"]
            for video in pos_videos:
                video_count[video] += 1
            for video in neg_videos:
                video_count[video] += 1
            skill_total += len(pos_videos)

        print(f"  {'Total skill samples:':<58} {skill_total:<10}")
        print(f"Maximum number of samples per video: {max(video_count.values())}")
        print(f"Minimum number of samples per video: {min(video_count.values())}")
        for count in range(0, max(video_count.values()) + 1):
            print(f"Number of videos with {count} samples: {sum([1 for v in video_count.values() if v == count])}")

    print("\n" + "-" * 110)

def generate_pairwise_caption_dataset(
    caption_save_dir="cam_motion-20250227_0324ground_only",
    max_samples=MAX_SAMPLES,
    max_neg_samples=MAX_NEG_SAMPLES,
    split="testset",
    video_root=VIDEO_ROOT,
    video_labels_dir=VIDEO_LABELS_DIR,
):
    """
    Generate a pairwise benchmark by sampling from pairwise tasks.
    
    Args:
        pairwise_labels: Dictionary containing skill and task definitions
        max_samples: Maximum number of samples per task
        max_neg_samples: Maximum number of negative samples per task
        root: Root directory
        video_root: Video root directory
        video_labels_dir: Directory containing video labels
        folder_name: Folder name to save the sampled tasks
        
    Returns:
        dataset: Dictionary containing the sampled tasks
    """
    # Get the directory for sampled tasks
    video_labels_dir = Path(video_labels_dir)
    sampling_str = f"sample_{max_samples}_max_{max_neg_samples}_{split}"
    filename = video_labels_dir / caption_save_dir / f"{sampling_str}.json"
    assert filename.exists(), f"Error: File {filename} does not exist!"
    
    with open(filename, "r") as f:
        pairwise_captions = json.load(f)
    # Generate and sample tasks
    dataset = {
        "pos": [],
        "neg": [],
        "pos_caption": [],
        "neg_caption": [],
    }
    for item in pairwise_captions:
        pos_video = list(item.keys())[0]
        neg_video = list(item.keys())[1]
        pos_caption = item[pos_video]
        neg_caption = item[neg_video]
        pos_video = str(video_root / pos_video)
        neg_video = str(video_root / neg_video)
        dataset["pos"].append(pos_video)
        dataset["neg"].append(neg_video)
        dataset["pos_caption"].append(pos_caption)
        dataset["neg_caption"].append(neg_caption)
    
    return {
        "complex_description": {
            "all": dataset,
        }
    }




if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--caption_save_dir", type=str, default="cam_motion-20250227_0324ground_only", help="Directory to save the sampled tasks")
    parser.add_argument("--max_samples", type=int, default=MAX_SAMPLES, help="A (rough) maximum number of (test) samples per task")
    parser.add_argument("--max_neg_samples", type=int, default=MAX_NEG_SAMPLES, help="A (rough) maximum number of negative samples per task")
    parser.add_argument("--split", type=str, default="test", help="Split to use for the benchmark")
    args = parser.parse_args()
    
    # # Print statistics
    # print_task_statistics(sampled_tasks)
    dataset = generate_pairwise_caption_dataset(
        caption_save_dir=args.caption_save_dir,
        max_samples=args.max_samples,
        max_neg_samples=args.max_neg_samples,
        # root=ROOT,
        split=args.split,
        video_root=VIDEO_ROOT,
        video_labels_dir=VIDEO_LABELS_DIR,
    )
    print_detailed_caption_task_statistics(
        dataset,
    )
    
    # import pdb; pdb.set_trace()
    # Create benchmark
    benchmark = PairwiseCaptionBenchmark(dataset, mode="retrieval")
    # print first sample in the dataset
    print(benchmark.samples[0])
    
    import numpy as np
    retrieval_scores = np.random.rand(len(benchmark), 2, 2)
    yes_scores = np.random.rand(len(benchmark), 2, 2)
    no_scores = np.random.rand(len(benchmark), 2, 2)
    benchmark.evaluate_and_print_retrieval(retrieval_scores)
    benchmark.evaluate_and_print_vqa(yes_scores, no_scores)
    
    # print vqa version of benchmark
    benchmark = PairwiseCaptionBenchmark(dataset, mode="vqa")
    print(benchmark.samples[0])