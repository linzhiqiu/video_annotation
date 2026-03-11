# pairwise_benchmark.py
from benchmark import ROOT, VIDEO_ROOT, VIDEO_LABELS_DIR, VIDEO_LABEL_FILE, labels_as_dict
from pathlib import Path
from datetime import datetime
import random
import json
from collections import defaultdict
from torch.utils.data import Dataset
from benchmark_config import (
    get_pairwise_labels, 
    FOLDER_NAMES, 
    get_test_skip_tasks,
    get_folder_description
)

# SAMPLING = "random"
SAMPLING = "top"
# MAX_SAMPLES = 100
MAX_SAMPLES = 80
# MAX_SAMPLES = 300
# MAX_SAMPLES = 50
SEED = 0
TRAIN_RATIO = 0.5

def get_pairwise_scores(scores_matrix):
    """
    Convert a matrix of scores into a list of dictionaries with labeled scores.
    
    Args:
        scores_matrix: A 3D numpy array [num_sample, 2, 2]
        
    Returns:
        List of dictionaries, each containing labeled similarity scores
    """
    num_samples = scores_matrix.shape[0]
    pairwise_scores = []
    
    for idx in range(num_samples):
        pairwise_scores.append({
            "id": idx,
            "pos_text_pos_image": scores_matrix[idx][0][0],  # t0_i0
            "pos_text_neg_image": scores_matrix[idx][1][0],  # t0_i1
            "neg_text_pos_image": scores_matrix[idx][0][1],  # t1_i0
            "neg_text_neg_image": scores_matrix[idx][1][1]   # t1_i1
        })
    
    return pairwise_scores

def get_retrieval_scores(scores):
    """
    Calculate retrieval performance metrics.
    
    Args:
        scores: List of dictionaries with pairwise scores
        
    Returns:
        Dictionary containing text, image, and group retrieval accuracy
    """
    text_correct_count = 0 # Text Score measures video-to-text retrieval performance
    image_correct_count = 0 # Image Score measures video-to-image retrieval performance
    group_correct_count = 0 # Group Score measures overall retrieval performance
    def text_correct(result):
        """Check if text retrieval is correct for this sample."""
        return (result["pos_text_pos_image"] > result["neg_text_pos_image"] and 
                result["neg_text_neg_image"] > result["pos_text_neg_image"])

    def image_correct(result):
        """Check if image retrieval is correct for this sample."""
        return (result["pos_text_pos_image"] > result["pos_text_neg_image"] and 
                result["neg_text_neg_image"] > result["neg_text_pos_image"])

    def group_correct(result):
        """Check if both text and image retrieval are correct."""
        return image_correct(result) and text_correct(result)
    
    for result in scores:
        text_correct_count += 1 if text_correct(result) else 0
        image_correct_count += 1 if image_correct(result) else 0
        group_correct_count += 1 if group_correct(result) else 0

    denominator = max(1, len(scores))  # Avoid division by zero
    result = {
        'text': text_correct_count / denominator,
        'image': image_correct_count / denominator,
        'group': group_correct_count / denominator,
    }
    return result

def get_vqa_scores(yes_scores, no_scores):
    """
    Calculate Visual Question Answering (VQA) performance metrics.
    
    Args:
        yes_scores: List of dictionaries with pairwise scores for 'yes' answers
        no_scores: List of dictionaries with pairwise scores for 'no' answers
        
    Returns:
        Dictionary containing various VQA accuracy metrics
    """
    # Initialize counters for different metrics
    metrics = {
        'binary_acc': 0.0,              # Binary accuracy (random chance: 0.5)
        'pos_binary_acc': 0.0,          # Binary accuracy for positive questions only (random chance: 0.5)
        'neg_binary_acc': 0.0,          # Binary accuracy for negative questions only (random chance: 0.5)
        'question_acc': 0.0,            # Question accuracy (random chance: 0.25)
        'pos_question_acc': 0.0,        # Question accuracy for positive questions only (random chance: 0.25)
        'neg_question_acc': 0.0,        # Question accuracy for negative questions only (random chance: 0.25)
        'image_acc': 0.0,               # Image accuracy (random chance: 0.25)
        'group_acc': 0.0                # Group accuracy (random chance: 0.125)
    }
    
    # Helper functions to check correctness for each combination
    def pos_text_pos_image_correct(yes_result, no_result):
        """Positive Text, Positive Image: 'yes' should score higher than 'no'"""
        return yes_result["pos_text_pos_image"] > no_result["pos_text_pos_image"]
    
    def pos_text_neg_image_correct(yes_result, no_result):
        """Positive Text, Negative Image: 'no' should score higher than 'yes'"""
        return no_result["pos_text_neg_image"] > yes_result["pos_text_neg_image"]
    
    def neg_text_pos_image_correct(yes_result, no_result):
        """Negative Text, Positive Image: 'no' should score higher than 'yes'"""
        return no_result["neg_text_pos_image"] > yes_result["neg_text_pos_image"]
    
    def neg_text_neg_image_correct(yes_result, no_result):
        """Negative Text, Negative Image: 'yes' should score higher than 'no'"""
        return yes_result["neg_text_neg_image"] > no_result["neg_text_neg_image"]
    
    def pos_binary_acc_correct(yes_result, no_result):
        """Binary accuracy for positive questions"""
        count = 0.0
        count += 1.0 if pos_text_pos_image_correct(yes_result, no_result) else 0.0
        count += 1.0 if pos_text_neg_image_correct(yes_result, no_result) else 0.0
        return count
    
    def neg_binary_acc_correct(yes_result, no_result):
        """Binary accuracy for negative questions"""
        count = 0.0
        count += 1.0 if neg_text_pos_image_correct(yes_result, no_result) else 0.0
        count += 1.0 if neg_text_neg_image_correct(yes_result, no_result) else 0.0
        return count
    
    def binary_acc_correct(yes_result, no_result):
        """Overall binary accuracy"""
        return pos_binary_acc_correct(yes_result, no_result) + neg_binary_acc_correct(yes_result, no_result)
    
    def pos_question_acc_correct(yes_result, no_result):
        """Question accuracy for positive questions (both images correct)"""
        return 1.0 if (pos_text_pos_image_correct(yes_result, no_result) and 
                       pos_text_neg_image_correct(yes_result, no_result)) else 0.0
    
    def neg_question_acc_correct(yes_result, no_result):
        """Question accuracy for negative questions (both images correct)"""
        return 1.0 if (neg_text_pos_image_correct(yes_result, no_result) and 
                       neg_text_neg_image_correct(yes_result, no_result)) else 0.0
    
    def question_acc_correct(yes_result, no_result):
        """Overall question accuracy"""
        return pos_question_acc_correct(yes_result, no_result) + neg_question_acc_correct(yes_result, no_result)
    
    def image_acc_correct(yes_result, no_result):
        """Image accuracy (both questions correct for same image)"""
        count = 0.0
        count += 1.0 if (pos_text_pos_image_correct(yes_result, no_result) and 
                          neg_text_pos_image_correct(yes_result, no_result)) else 0.0
        count += 1.0 if (pos_text_neg_image_correct(yes_result, no_result) and 
                          neg_text_neg_image_correct(yes_result, no_result)) else 0.0
        return count
    
    def group_acc_correct(yes_result, no_result):
        """Group accuracy (all combinations correct)"""
        if (pos_text_pos_image_correct(yes_result, no_result) and 
            pos_text_neg_image_correct(yes_result, no_result) and 
            neg_text_pos_image_correct(yes_result, no_result) and 
            neg_text_neg_image_correct(yes_result, no_result)):
            return 1.0
        return 0.0

    # Calculate metrics for each pair of results
    for yes_result, no_result in zip(yes_scores, no_scores):
        metrics['binary_acc'] += binary_acc_correct(yes_result, no_result)
        metrics['pos_binary_acc'] += pos_binary_acc_correct(yes_result, no_result)
        metrics['neg_binary_acc'] += neg_binary_acc_correct(yes_result, no_result)
        metrics['question_acc'] += question_acc_correct(yes_result, no_result)
        metrics['pos_question_acc'] += pos_question_acc_correct(yes_result, no_result)
        metrics['neg_question_acc'] += neg_question_acc_correct(yes_result, no_result)
        metrics['image_acc'] += image_acc_correct(yes_result, no_result)
        metrics['group_acc'] += group_acc_correct(yes_result, no_result)
    
    # Define denominators for each metric
    sample_count = len(yes_scores)
    denominators = {
        'binary_acc': sample_count * 4.0,
        'pos_binary_acc': sample_count * 2.0,
        'neg_binary_acc': sample_count * 2.0,
        'question_acc': sample_count * 2.0,
        'pos_question_acc': sample_count,
        'neg_question_acc': sample_count,
        'image_acc': sample_count * 2.0,
        'group_acc': sample_count
    }
    
    # Calculate final scores
    result = {key: value / denominators[key] for key, value in metrics.items()}
    return result


class PairwiseBenchmark(Dataset):
    """
    Dataset class for pairwise comparison tasks (VQA or retrieval).
    
    Args:
        skills: List of skills, where each skill contains multiple tasks
        mode: Task mode, one of "vqa", "vqa_generation", or "retrieval"
    """
    def __init__(self, skills, mode="vqa"):
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
                
                pos_prompt = skills[skill][task]['task_dict']['pos_prompt']
                neg_prompt = skills[skill][task]['task_dict']['neg_prompt']
                pos_question = skills[skill][task]['task_dict']['pos_question']
                neg_question = skills[skill][task]['task_dict']['neg_question']
                
                self.task_to_metadata[task] = {
                    "skill": skill,
                    "pos_prompt": pos_prompt,
                    "neg_prompt": neg_prompt,
                    "pos_question": pos_question,
                    "neg_question": neg_question
                }
                
                assert len(pos_videos) == len(neg_videos), f"Number of positive and negative videos must match for task {task}"
                
                for pos_video, neg_video in zip(pos_videos, neg_videos):
                    sample_id = len(self.samples)
                    self.skill_to_sample_ids[skill].append(sample_id)
                    self.task_to_sample_ids[task].append(sample_id)
                    
                    # Important to make 0th the Positive Image and 1st the Negative Image
                    images = [pos_video, neg_video]
                    if self.mode in ["vqa", "vqa_generation"]:
                        texts = [pos_question, neg_question]
                    elif self.mode == "retrieval":
                        texts = [pos_prompt, neg_prompt]
                    
                    self.samples.append({
                        "images": images,
                        "texts": texts
                    })
    
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]
    
    def evaluate_retrieval_scores(self, scores):
        """
        Evaluate retrieval scores across all skills and tasks.
        
        Args:
            scores: Scores matrix from the model
            
        Returns:
            Dictionary with evaluation results
        """
        pairwise_scores = get_pairwise_scores(scores)
        acc = get_retrieval_scores(pairwise_scores)
        
        results = {
            'overall': acc,
            'skills': {}
        }
        
        for skill in self.skills:
            skill_pairwise_scores = [pairwise_scores[i] for i in self.skill_to_sample_ids[skill]]
            skill_acc = get_retrieval_scores(skill_pairwise_scores)
            
            results['skills'][skill] = {
                'overall': skill_acc,
                'tasks': {}
            }
            
            for task in self.skill_to_tasks[skill]:
                task_pairwise_scores = [pairwise_scores[i] for i in self.task_to_sample_ids[task]]
                task_acc = get_retrieval_scores(task_pairwise_scores)
                results['skills'][skill]['tasks'][task] = task_acc
        
        return results
    
    def evaluate_vqa_scores(self, yes_scores, no_scores):
        """
        Evaluate VQA scores across all skills and tasks.
        
        Args:
            yes_scores: Scores matrix for 'yes' answers
            no_scores: Scores matrix for 'no' answers
            
        Returns:
            Dictionary with evaluation results
        """
        yes_pairwise_scores = get_pairwise_scores(yes_scores)
        no_pairwise_scores = get_pairwise_scores(no_scores)
        
        acc = get_vqa_scores(yes_pairwise_scores, no_pairwise_scores)
        
        results = {
            'overall': acc,
            'skills': {}
        }
        
        for skill in self.skills:
            skill_yes_scores = [yes_pairwise_scores[i] for i in self.skill_to_sample_ids[skill]]
            skill_no_scores = [no_pairwise_scores[i] for i in self.skill_to_sample_ids[skill]]
            skill_acc = get_vqa_scores(skill_yes_scores, skill_no_scores)
            
            results['skills'][skill] = {
                'overall': skill_acc,
                'tasks': {}
            }
            
            for task in self.skill_to_tasks[skill]:
                task_yes_scores = [yes_pairwise_scores[i] for i in self.task_to_sample_ids[task]]
                task_no_scores = [no_pairwise_scores[i] for i in self.task_to_sample_ids[task]]
                task_acc = get_vqa_scores(task_yes_scores, task_no_scores)
                results['skills'][skill]['tasks'][task] = task_acc
        
        return results
    
    def format_retrieval_results(self, results, name_width=70):
        """
        Format retrieval evaluation results as a string.
        Shows overall and skill summaries first, followed by detailed task breakdown.
        
        Args:
            results: Results dictionary from evaluate_retrieval_scores
            name_width: Width for the dataset/skill/task name column (default: 50)
            
        Returns:
            Formatted string with evaluation results
        """
        output = []
        
        # Define column widths
        metric_width = 10
        metrics = ['text', 'image', 'group']
        total_width = name_width + (len(metrics) * (metric_width + 1))
        
        # Create header
        header = f"{'Dataset':{name_width}s}"
        for metric in metrics:
            header += f" {metric.capitalize():{metric_width}s}"
        separator = "-" * total_width
        
        # Part 1: Summary section
        output.append("\n====== Retrieval Performance Summary ======")
        output.append(header)
        output.append(separator)
        
        # Format overall results
        overall = results['overall']
        output.append(f"{'Overall':{name_width}s} {overall['text']:{metric_width}.2%} {overall['image']:{metric_width}.2%} {overall['group']:{metric_width}.2%}")
        
        # Format skill summaries
        for skill, skill_data in results['skills'].items():
            skill_acc = skill_data['overall']
            
            # Truncate skill name if too long
            skill_name = skill
            if len(skill_name) > name_width:
                skill_name = skill_name[:name_width-3] + "..."
                
            output.append(f"{skill_name:{name_width}s} {skill_acc['text']:{metric_width}.2%} {skill_acc['image']:{metric_width}.2%} {skill_acc['group']:{metric_width}.2%}")
        
        # Part 2: Detailed section
        output.append("\n====== Retrieval Performance Details by Task ======")
        output.append(header)
        output.append(separator)
        
        # Format task details grouped by skill
        for skill, skill_data in results['skills'].items():
            # Format skill header
            skill_acc = skill_data['overall']
            
            # Truncate skill name if too long
            skill_name = skill
            if len(skill_name) > name_width:
                skill_name = skill_name[:name_width-3] + "..."
                
            output.append(f"{skill_name:{name_width}s} {skill_acc['text']:{metric_width}.2%} {skill_acc['image']:{metric_width}.2%} {skill_acc['group']:{metric_width}.2%}")
            
            # Format tasks for this skill
            for task, task_acc in skill_data['tasks'].items():
                task_name = f"  - {task}"
                
                # Truncate task name if too long
                if len(task_name) > name_width:
                    task_name = task_name[:name_width-3] + "..."
                    
                output.append(f"{task_name:{name_width}s} {task_acc['text']:{metric_width}.2%} {task_acc['image']:{metric_width}.2%} {task_acc['group']:{metric_width}.2%}")
            
            output.append("")  # Add empty line between skills
        
        return "\n".join(output)


    def format_vqa_results(self, results, name_width=70):
        """
        Format VQA evaluation results as a string.
        Shows overall and skill summaries first, followed by detailed task breakdown.
        
        Args:
            results: Results dictionary from evaluate_vqa_scores
            name_width: Width for the dataset/skill/task name column (default: 70)
            
        Returns:
            Formatted string with evaluation results
        """
        output = []
        
        # All VQA metrics with short display names
        metrics = [
            'binary_acc', 'pos_binary_acc', 'neg_binary_acc', 
            'question_acc', 'pos_question_acc', 'neg_question_acc', 
            'image_acc', 'group_acc'
        ]
        
        # Display names for metrics (shorter for better table layout)
        display_names = {
            'binary_acc': 'acc',
            'pos_binary_acc': 'pos_a',
            'neg_binary_acc': 'neg_a',
            'question_acc': 'q_acc',
            'pos_question_acc': 'pos_q',
            'neg_question_acc': 'neg_q',
            'image_acc': 'i_acc',
            'group_acc': 'g_acc'
        }
        
        # Column width for metric values
        metric_width = 8
        total_width = name_width + (len(metrics) * (metric_width + 1))
        
        # Create header row
        header = f"{'Dataset':{name_width}s}"
        for metric in metrics:
            header += f" {display_names[metric]:{metric_width}s}"
        
        # Create separator line
        separator = "-" * total_width
        
        # PART 1: Summary of overall and skills
        output.append("\n====== VQA Performance Summary ======")
        output.append(header)
        output.append(separator)
        
        # Format overall results
        overall = results['overall']
        overall_row = f"{'Overall':{name_width}s}"
        for metric in metrics:
            overall_row += f" {overall[metric]:{metric_width}.2%}"
        output.append(overall_row)
        
        # Format skill summaries
        for skill, skill_data in results['skills'].items():
            skill_acc = skill_data['overall']
            
            # Truncate skill name if too long
            skill_name = skill
            if len(skill_name) > name_width:
                skill_name = skill_name[:name_width-3] + "..."
                
            skill_row = f"{skill_name:{name_width}s}"
            for metric in metrics:
                skill_row += f" {skill_acc[metric]:{metric_width}.2%}"
            output.append(skill_row)
        
        # PART 2: Detailed breakdown by task
        output.append("\n====== VQA Performance Details by Task ======")
        output.append(header)
        output.append(separator)
        
        # Format task details grouped by skill
        for skill, skill_data in results['skills'].items():
            # Format skill header
            skill_acc = skill_data['overall']
            
            # Truncate skill name if too long
            skill_name = skill
            if len(skill_name) > name_width:
                skill_name = skill_name[:name_width-3] + "..."
                
            skill_row = f"{skill_name:{name_width}s}"
            for metric in metrics:
                skill_row += f" {skill_acc[metric]:{metric_width}.2%}"
            output.append(skill_row)
            
            # Format tasks for this skill
            for task, task_acc in skill_data['tasks'].items():
                task_name = f"  - {task}"
                
                # Truncate task name if too long
                if len(task_name) > name_width:
                    task_name = task_name[:name_width-3] + "..."
                    
                task_row = f"{task_name:{name_width}s}"
                for metric in metrics:
                    task_row += f" {task_acc[metric]:{metric_width}.2%}"
                output.append(task_row)
            
            output.append("")  # Add empty line between skills
        
        return "\n".join(output)


    def format_vqa_generation_results(self, results, name_width=70):
        """
        Format VQA generation evaluation results as a string.
        Shows overall and skill summaries first, followed by detailed task breakdown.
        
        Args:
            results: Results dictionary from evaluate_vqa_generation_scores
            name_width: Width for the dataset/skill/task name column (default: 70)
            
        Returns:
            Formatted string with evaluation results
        """
        # This function uses the same structure as format_vqa_results
        # since the metrics structure is identical
        return self.format_vqa_results(results, name_width)


    # Wrapper functions that print the formatted results
    def print_retrieval_results(self, results, name_width=50):
        """
        Print retrieval evaluation results.
        
        Args:
            results: Results dictionary from evaluate_retrieval_scores
            name_width: Width for the dataset/skill/task name column (default: 50)
        """
        print(self.format_retrieval_results(results, name_width))


    def print_vqa_results(self, results, name_width=70):
        """
        Print VQA evaluation results.
        
        Args:
            results: Results dictionary from evaluate_vqa_scores
            name_width: Width for the dataset/skill/task name column (default: 70)
        """
        print(self.format_vqa_results(results, name_width))


    def evaluate_and_print_retrieval(self, scores, name_width=50):
        """
        Evaluate retrieval scores and print the results.
        
        Args:
            scores: Scores matrix from the model
            name_width: Width for the dataset/skill/task name column (default: 50)
            
        Returns:
            Dictionary with evaluation results
            String with formatted evaluation results
        """
        results = self.evaluate_retrieval_scores(scores)
        results_str = self.format_retrieval_results(results, name_width)
        print(results_str)
        return results, results_str


    def evaluate_and_print_vqa(self, yes_scores, no_scores, name_width=70):
        """
        Evaluate VQA scores and print the results.
        
        Args:
            yes_scores: Scores matrix for 'yes' answers
            no_scores: Scores matrix for 'no' answers
            name_width: Width for the dataset/skill/task name column (default: 70)
            
        Returns:
            Dictionary with evaluation results
            String with formatted evaluation results
        """
        results = self.evaluate_vqa_scores(yes_scores, no_scores)
        results_str = self.format_vqa_results(results, name_width)
        print(results_str)
        return results, results_str


def get_videos(label_dicts, task_spec):
    """
    Get videos based on task specifications.
    
    Args:
        label_dicts: Dictionary containing labels and their corresponding videos
        task_spec: Either a dictionary with 'label' and 'type' or a list of such dictionaries
        
    Returns:
        List of videos matching the task specification
    """
    if isinstance(task_spec, list):
        # If task_spec is a list, get the intersection of all video sets
        video_sets = []
        for task_dict in task_spec:
            _validate_task_dict(task_dict)
            videos = label_dicts[task_dict["label"]][task_dict["type"]]
            video_sets.append(set(videos))
        
        return list(set.intersection(*video_sets))
    else:
        # If task_spec is a single dictionary
        _validate_task_dict(task_spec)
        return label_dicts[task_spec["label"]][task_spec["type"]]


def _validate_task_dict(task_dict):
    """
    Validate that a task dictionary has the required keys.
    
    Args:
        task_dict: Dictionary to validate
    
    Raises:
        AssertionError: If task_dict is not a dictionary or missing required keys
    """
    assert isinstance(task_dict, dict), "Task specification must be a dictionary"
    assert "label" in task_dict and "type" in task_dict, "Task specification must have 'label' and 'type' keys"


def generate_all_to_train_tasks(
    pairwise_labels, 
    root, 
    video_root, 
    video_labels_dir, 
    labels_filename="label_names.json",
    folder_name="motion_dataset"
):
    """
    Minimal version: no Train/Test split, all positive and negative sample videos are directly stored in the train dictionary.
    """
    video_labels_dir = Path(video_labels_dir)
    raw_tasks = defaultdict(dict)
    train_tasks = defaultdict(dict)
    test_tasks = defaultdict(dict) # Kept empty
    train_videos = set()

    print(f"\n🚀 Extracting all data into Training Set (folder: {folder_name})...")

    for skill_name, tasks in pairwise_labels.items():
        for task_dict in tasks:
            task_name = task_dict["name"]
            video_label_file = video_labels_dir / task_dict["folder"] / labels_filename
            
            try:
                label_dicts = labels_as_dict(root=root, video_root=video_root, video_label_file=video_label_file)
                pos_videos = get_videos(label_dicts, task_dict["pos"])
                neg_videos = get_videos(label_dicts, task_dict["neg"])
                
                # Convert to string paths
                pos_videos = [str(v) for v in pos_videos]
                neg_videos = [str(v) for v in neg_videos]
                
                if not pos_videos or not neg_videos:
                    print(f"  ⚠️ Skipping task '{task_name}': insufficient samples (Pos:{len(pos_videos)}, Neg:{len(neg_videos)})")
                    continue

                # Store in raw for statistics
                raw_tasks[skill_name][task_name] = {
                    "task_dict": task_dict,
                    "pos": pos_videos,
                    "neg": neg_videos
                }

                # Assign everything directly to train_tasks
                train_tasks[skill_name][task_name] = {
                    "task_dict": task_dict,
                    "pos": pos_videos,
                    "neg": neg_videos
                }
                
                train_videos.update(pos_videos)
                train_videos.update(neg_videos)

            except Exception as e:
                print(f"  ❌ Failed to load task '{task_name}': {e}")
                continue

    return {
        "raw": raw_tasks,
        "train": train_tasks,
        "test": test_tasks, # Empty
        "train_videos": list(train_videos),
        "test_videos": []   # Empty
    }

from pathlib import Path
from collections import defaultdict


def compute_test_size(n, max_test_samples):
    """
    Compute the number of test samples for a task based on its total sample count.

    Tier rules:
      - n <= 10:        no test set (train only)
      - 10 < n <= 20:   even split (half test, half train)
      - 20 < n <= 40:   test gets exactly 10
      - n > 40:         test gets min(n // 2, max_test_samples)

    Args:
        n: Total number of available samples (min of pos/neg count)
        max_test_samples: Maximum allowed test samples (from --max_samples arg)

    Returns:
        Number of samples to assign to test set (0 means train-only)
    """
    if n <= 10:
        return 0
    elif n <= 20:
        return n // 2
    elif n <= 40:
        return 10
    else:
        return min(n // 2, max_test_samples)


from pathlib import Path
from collections import defaultdict


def compute_test_size(n, max_test_samples):
    """
    Compute the number of test samples for a task based on its total sample count.

    Tier rules:
      - n <= 10:        no test set (train only)
      - 10 < n <= 20:   even split (half test, half train)
      - 20 < n <= 40:   test gets exactly 10
      - n > 40:         test gets min(n // 2, max_test_samples)

    Args:
        n: Total number of available samples (min of pos/neg count)
        max_test_samples: Maximum allowed test samples (from --max_samples arg)

    Returns:
        Number of samples to assign to test set (0 means train-only)
    """
    if n <= 10:
        return 0
    elif n <= 20:
        return n // 2
    elif n <= 40:
        return 10
    else:
        return min(n // 2, max_test_samples)


from pathlib import Path
from collections import defaultdict


def compute_test_size(n, max_test_samples):
    """
    Compute the number of test samples for a task based on its total sample count.

    Tier rules:
      - n <= 10:        no test set (train only)
      - 10 < n <= 20:   even split (half test, half train)
      - 20 < n <= 40:   test gets exactly 10
      - n > 40:         test gets min(n // 2, max_test_samples)

    Args:
        n: Total number of available samples (min of pos/neg count)
        max_test_samples: Maximum allowed test samples (from --max_samples arg)

    Returns:
        Number of samples to assign to test set (0 means train-only)
    """
    if n <= 10:
        return 0
    elif n <= 20:
        return n // 2
    elif n <= 40:
        return 10
    else:
        return min(n // 2, max_test_samples)


def generate_balanced_pairwise_tasks(
    pairwise_labels,
    root,
    video_root,
    video_labels_dir,
    train_ratio=0.5,
    max_test_sample=20,
    labels_filename="label_names.json",
    folder_name="motion_dataset",
    min_samples_threshold=None,
    split_log_path='./syc_log.jsonl',
):
    """
    Generate balanced pairwise tasks with a global video-level train/test split.

    For each task, both pos and neg independently target `target_test`:
      - Count already-in-test for that side
      - If >= target_test, skip (ALREADY_SATISFIED)
      - Otherwise pick from unassigned to reach target_test

    Processing Order (smallest n first within each tier, n = min(pos, neg)):
    -----------------------------------------------------------------------
    Step 1 — 10 < n <= 20  (even split, target_test = n // 2)
    Step 2 — 20 < n <= 40  (test >= 10, target_test = 10)
    Step 3 — n <= 10       (train only, no test)
    Step 4 — n > 40        (capped test, target_test = min(max_test_sample, n // 2))
    Finalize — All videos not in test_videos → train.

    train ∩ test = ∅ guaranteed.
    """
    import json
    from collections import defaultdict
    from pathlib import Path
    from benchmark import labels_as_dict
    from benchmark_config import get_test_skip_tasks

    video_labels_dir = Path(video_labels_dir)

    # ================================================================== #
    #  Log setup                                                           #
    # ================================================================== #
    _log_file = None
    if split_log_path:
        _log_path = Path(split_log_path)
        _log_path.parent.mkdir(parents=True, exist_ok=True)
        _log_file = open(_log_path, "w")
        print(f"📝 Split log: {_log_path}")

    def log(entry):
        if _log_file:
            _log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
            _log_file.flush()

    # ================================================================== #
    #  Phase 0: Load all tasks                                             #
    # ================================================================== #
    raw_tasks = defaultdict(dict)
    task_metadata = []

    for skill_name, tasks in pairwise_labels.items():
        for task_dict in tasks:
            task_name = task_dict["name"]
            video_label_file = video_labels_dir / task_dict["folder"] / labels_filename

            try:
                label_dicts = labels_as_dict(
                    root=root,
                    video_root=video_root,
                    video_label_file=video_label_file
                )
                pos_videos = get_videos(label_dicts, task_dict["pos"])
                neg_videos = get_videos(label_dicts, task_dict["neg"])
            except Exception as e:
                print(f"  ❌ Failed to load task '{task_name}': {e}")
                continue

            pos_videos = [str(v) for v in pos_videos]
            neg_videos = [str(v) for v in neg_videos]

            if not pos_videos or not neg_videos:
                print(f"  ⚠️  Skipping '{task_name}': empty pos or neg list")
                continue

            assert set(pos_videos).isdisjoint(set(neg_videos)), \
                f"Pos/neg overlap in task '{task_name}'"

            n = min(len(pos_videos), len(neg_videos))

            raw_tasks[skill_name][task_name] = {
                "task_dict": task_dict,
                "pos": pos_videos,
                "neg": neg_videos,
            }

            task_metadata.append({
                "skill":      skill_name,
                "task":       task_name,
                "task_dict":  task_dict,
                "pos_videos": pos_videos,
                "neg_videos": neg_videos,
                "n":          n,
            })

    # ================================================================== #
    #  Tier distribution                                                   #
    # ================================================================== #
    tier_counts = {"n<=10": 0, "10<n<=20": 0, "20<n<=40": 0, "n>40": 0}
    for t in task_metadata:
        if t["n"] <= 10:     tier_counts["n<=10"] += 1
        elif t["n"] <= 20:   tier_counts["10<n<=20"] += 1
        elif t["n"] <= 40:   tier_counts["20<n<=40"] += 1
        else:                tier_counts["n>40"] += 1
    print(f"\n[Tier Distribution] {tier_counts}")
    print(f"  Total tasks: {len(task_metadata)}")
    log({"step": "TIER_DISTRIBUTION", **tier_counts, "total_tasks": len(task_metadata)})

    # ================================================================== #
    #  Global state                                                        #
    # ================================================================== #
    test_videos: set = set()

    # ================================================================== #
    #  Helper: assign one side to test                                     #
    # ================================================================== #

    def assign_side(video_list, target_test):
        """
        For one side (pos or neg), check already-in-test count.
        If < target_test, pick from unassigned to reach target_test.

        Returns: (n_already, n_new, note)
        """
        already = [v for v in video_list if v in test_videos]
        if len(already) >= target_test:
            return len(already), 0, "ALREADY_SATISFIED"

        unassigned = [v for v in video_list if v not in test_videos]
        needed = target_test - len(already)
        new = unassigned[:needed]
        test_videos.update(new)

        note = ""
        if len(new) < needed:
            note = f"SHORTFALL: needed {needed}, got {len(new)}"

        return len(already), len(new), note

    # ================================================================== #
    #  Helper: assign both sides of a task                                 #
    # ================================================================== #

    def assign_test(task, target_test, step):
        """
        Assign test videos for both pos and neg sides independently.
        Both target target_test. No cross-linking.
        """
        pos = task["pos_videos"]
        neg = task["neg_videos"]

        pos_already, pos_new, pos_note = assign_side(pos, target_test)
        neg_already, neg_new, neg_note = assign_side(neg, target_test)

        note_parts = []
        if pos_note: note_parts.append(f"pos:{pos_note}")
        if neg_note: note_parts.append(f"neg:{neg_note}")
        note = "; ".join(note_parts)

        entry = {
            "step":             step,
            "task":             task["task"],
            "n":                task["n"],
            "target_test":      target_test,
            "total_pos":        len(pos),
            "pos_already_test": pos_already,
            "pos_new_test":     pos_new,
            "total_neg":        len(neg),
            "neg_already_test": neg_already,
            "neg_new_test":     neg_new,
            "global_test_size": len(test_videos),
            "note":             note,
        }
        log(entry)

        print(f"  [{step}] '{task['task']}': n={task['n']}, target={target_test} | "
              f"pos: {pos_already}+{pos_new}={pos_already+pos_new} | "
              f"neg: {neg_already}+{neg_new}={neg_already+neg_new}"
              + (f"  [{note}]" if note else ""))

    # ================================================================== #
    #  Step 1: 10 < n <= 20 — even split                                   #
    # ================================================================== #
    print("\n[Step 1] Tasks with 10 < n <= 20 (even split) ...")
    step1_tasks = sorted(
        [t for t in task_metadata if 10 < t["n"] <= 20],
        key=lambda x: x["n"]
    )
    print(f"  ({len(step1_tasks)} tasks)")
    for task in step1_tasks:
        assign_test(task, task["n"] // 2, "Step1")

    # ================================================================== #
    #  Step 2: 20 < n <= 40 — test >= 10                                   #
    # ================================================================== #
    print("\n[Step 2] Tasks with 20 < n <= 40 (test ≥ 10) ...")
    step2_tasks = sorted(
        [t for t in task_metadata if 20 < t["n"] <= 40],
        key=lambda x: x["n"]
    )
    print(f"  ({len(step2_tasks)} tasks)")
    for task in step2_tasks:
        assign_test(task, 10, "Step2")

    # ================================================================== #
    #  Step 3: n <= 10 — train only (nothing to do)                        #
    # ================================================================== #
    print("\n[Step 3] Tasks with n <= 10 (train-only) ...")
    step3_tasks = sorted(
        [t for t in task_metadata if t["n"] <= 10],
        key=lambda x: x["n"]
    )
    print(f"  ({len(step3_tasks)} tasks)")
    for task in step3_tasks:
        pos_in_test = sum(1 for v in task["pos_videos"] if v in test_videos)
        neg_in_test = sum(1 for v in task["neg_videos"] if v in test_videos)
        log({
            "step": "Step3", "task": task["task"], "n": task["n"],
            "total_pos": len(task["pos_videos"]),
            "total_neg": len(task["neg_videos"]),
            "pos_in_test": pos_in_test, "neg_in_test": neg_in_test,
            "note": "TRAIN_ONLY",
        })
        print(f"  [Step3] '{task['task']}': n={task['n']}, "
              f"pos_in_test={pos_in_test}, neg_in_test={neg_in_test}")

    # ================================================================== #
    #  Step 4: n > 40 — capped test                                        #
    # ================================================================== #
    print(f"\n[Step 4] Tasks with n > 40 (capped test, max={max_test_sample}) ...")
    step4_tasks = sorted(
        [t for t in task_metadata if t["n"] > 40],
        key=lambda x: x["n"]
    )
    print(f"  ({len(step4_tasks)} tasks)")
    for task in step4_tasks:
        target_test = min(max_test_sample, task["n"] // 2)
        assign_test(task, target_test, "Step4")

    # ================================================================== #
    #  Finalize: everything not in test → train                            #
    # ================================================================== #
    all_videos = set()
    for task in task_metadata:
        all_videos.update(task["pos_videos"])
        all_videos.update(task["neg_videos"])

    train_videos = all_videos - test_videos

    assert len(test_videos & train_videos) == 0, "FATAL: train/test overlap!"

    print(f"\n[Finalize] Total: {len(all_videos)} | "
          f"Test: {len(test_videos)} | Train: {len(train_videos)}")

    log({
        "step": "SUMMARY",
        "total_videos": len(all_videos),
        "test_videos": len(test_videos),
        "train_videos": len(train_videos),
    })

    if _log_file:
        _log_file.close()
        print(f"📝 Split log finalized: {split_log_path}")

    # ================================================================== #
    #  Build train/test task dicts                                         #
    # ================================================================== #
    test_skip_tasks = get_test_skip_tasks(folder_name)
    if test_skip_tasks:
        print(f"\n⚠️  Test-skip tasks for '{folder_name}': {test_skip_tasks}")

    train_tasks = defaultdict(dict)
    test_tasks  = defaultdict(dict)

    for task in task_metadata:
        skill_name = task["skill"]
        task_name  = task["task"]
        pos = task["pos_videos"]
        neg = task["neg_videos"]

        train_pos = [v for v in pos if v in train_videos]
        train_neg = [v for v in neg if v in train_videos]
        test_pos  = [v for v in pos if v in test_videos]
        test_neg  = [v for v in neg if v in test_videos]

        train_tasks[skill_name][task_name] = {
            "task_dict": task["task_dict"],
            "pos": train_pos,
            "neg": train_neg,
        }

        if task_name not in test_skip_tasks:
            if test_pos and test_neg:
                test_tasks[skill_name][task_name] = {
                    "task_dict": task["task_dict"],
                    "pos": test_pos,
                    "neg": test_neg,
                }
        else:
            print(f"  ⏩ Skipping task '{task_name}' in test set (train-only)")

    # ================================================================== #
    #  Validation                                                          #
    # ================================================================== #
    train_insufficient = []
    test_insufficient  = []

    if min_samples_threshold is not None:
        print("\n" + "=" * 70)
        print("📊 Sample Count Validation")
        print("=" * 70)

        for skill_name, skill_tasks in train_tasks.items():
            for task_name, task_data in skill_tasks.items():
                mn = min(len(task_data["pos"]), len(task_data["neg"]))
                if mn < min_samples_threshold:
                    train_insufficient.append({
                        "skill": skill_name, "task": task_name,
                        "pos": len(task_data["pos"]),
                        "neg": len(task_data["neg"]), "min": mn
                    })

        for skill_name, skill_tasks in test_tasks.items():
            for task_name, task_data in skill_tasks.items():
                mn = min(len(task_data["pos"]), len(task_data["neg"]))
                if mn < min_samples_threshold:
                    test_insufficient.append({
                        "skill": skill_name, "task": task_name,
                        "pos": len(task_data["pos"]),
                        "neg": len(task_data["neg"]), "min": mn
                    })

        has_issues = train_insufficient or test_insufficient

        if has_issues:
            print(f"\n⚠️  WARNING: Tasks below threshold ({min_samples_threshold}):\n")
            for lbl, items in [("TRAIN", train_insufficient),
                               ("TEST", test_insufficient)]:
                if items:
                    print(f"🔴 {lbl} SET — {len(items)} tasks:")
                    print(f"  {'Skill/Task':<80} {'Pos':<6} {'Neg':<6} {'Min':<6}")
                    print("  " + "-" * 100)
                    for item in sorted(items, key=lambda x: x["min"]):
                        name = f"{item['skill']}/{item['task']}"
                        print(f"  {name:<80} {item['pos']:<6} {item['neg']:<6} {item['min']:<6}")
                    print()

            print("💡 Recommendations:")
            print("   1. Reduce --max_samples")
            print("   2. Add more videos for the problematic tasks")
            print("   3. Consider removing tasks with very few samples")
            print("=" * 70)

            print("\n❓ Continue and save this dataset? [y/N]: ", end="", flush=True)
            if input().strip().lower() not in ("y", "yes"):
                print("\n❌ Cancelled by user.")
                raise SystemExit(0)
            print("\n✅ Continuing ...\n")
        else:
            print(f"✅ All tasks have sufficient samples (>= {min_samples_threshold})")
            print("=" * 70 + "\n")

    validation_report = {
        "threshold":           min_samples_threshold,
        "train_insufficient":  train_insufficient,
        "test_insufficient":   test_insufficient,
        "validation_passed":   not (train_insufficient or test_insufficient),
        "total_train_tasks":   sum(len(t) for t in train_tasks.values()),
        "total_test_tasks":    sum(len(t) for t in test_tasks.values()),
    }

    return {
        "raw":              raw_tasks,
        "train":            train_tasks,
        "test":             test_tasks,
        "train_videos":     list(train_videos),
        "test_videos":      list(test_videos),
        "validation_report": validation_report,
    }

    # return {
    #     "raw": raw_tasks,
    #     "train": train_tasks,
    #     "test": test_tasks,
    #     "train_videos": list(train_videos),
    #     "test_videos": list(test_videos)
    # }



def print_detailed_task_statistics(raw_tasks, train_tasks, test_tasks):
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

    total_original_samples, total_train_samples, total_test_samples = 0, 0, 0

    for skill_name in raw_tasks:
        print(f"\n{skill_name}:")
        skill_original, skill_train, skill_test = 0, 0, 0

        for task_name in raw_tasks[skill_name]:
            orig_pos = len(raw_tasks[skill_name][task_name]["pos"])
            orig_neg = len(raw_tasks[skill_name][task_name]["neg"])

            train_pos = len(train_tasks.get(skill_name, {}).get(task_name, {}).get("pos", []))
            train_neg = len(train_tasks.get(skill_name, {}).get(task_name, {}).get("neg", []))
            test_pos = len(test_tasks.get(skill_name, {}).get(task_name, {}).get("pos", []))
            test_neg = len(test_tasks.get(skill_name, {}).get(task_name, {}).get("neg", []))

            skill_original += min(orig_pos, orig_neg)
            skill_train += min(train_pos, train_neg)
            skill_test += min(test_pos, test_neg)

            # Truncate task name if too long
            display_name = task_name if len(task_name) <= 50 else task_name[:47] + "..."

            print(f"  {display_name:<58} {orig_pos:<10} {orig_neg:<10} {train_pos:<10} {train_neg:<10} {test_pos:<10} {test_neg:<10}")

        total_original_samples += skill_original
        total_train_samples += skill_train
        total_test_samples += skill_test

        print(f"  {'Total skill samples:':<58} {skill_original:<10} {'':<10} {skill_train:<10} {'':<10} {skill_test:<10}")

    print("\n" + "-" * 110)
    print(f"{'Total benchmark samples:':<60} {total_original_samples:<10} {'':<10} {total_train_samples:<10} {'':<10} {total_test_samples:<10}")

def verify_tasks(train_tasks, test_tasks, train_videos, test_videos):
    """
    Verify that train and test tasks are correctly split and that no video appears in both sets.

    Args:
        train_tasks: Dictionary of train set pairwise tasks.
        test_tasks: Dictionary of test set pairwise tasks.
        train_videos: List of videos assigned to the train set.
        test_videos: List of videos assigned to the test set.

    Returns:
        None. Raises an assertion error if any violation is found.
    """
    train_videos_set = set(train_videos)
    test_videos_set = set(test_videos)

    assert train_videos_set.isdisjoint(test_videos_set), "Error: Some videos appear in both train and test sets!"

    def check_task_videos(tasks, allowed_videos, split_name):
        """Check that all videos in the tasks belong only to the allowed set."""
        for skill_name, skill_tasks in tasks.items():
            for task_name, task_data in skill_tasks.items():
                pos_videos = set(task_data.get("pos", []))
                neg_videos = set(task_data.get("neg", []))

                # Ensure all videos in this split belong to the correct video set
                assert pos_videos.issubset(allowed_videos), \
                    f"Error: Task {task_name} ({split_name}) has positive videos not in {split_name} set!"
                assert neg_videos.issubset(allowed_videos), \
                    f"Error: Task {task_name} ({split_name}) has negative videos not in {split_name} set!"

    # Check that all train tasks contain only train videos
    check_task_videos(train_tasks, train_videos_set, "train")

    # Check that all test tasks contain only test videos
    check_task_videos(test_tasks, test_videos_set, "test")

    print("Verification passed: No video appears in both train and test sets!")



def sample_from_tasks(
    original_tasks,
    max_samples=None,
    max_train_samples=None,
    max_test_samples=MAX_SAMPLES,
    sampling=SAMPLING,
    seed=SEED,
    max_imbalance_ratio=None,      # NEW
    balance_train=False             # NEW
):
    """
    Sample a subset of videos from pairwise tasks.
    
    NEW: Train set behavior controlled by balance_train and max_imbalance_ratio.
    
    Args:
        original_tasks: Dictionary of pairwise tasks (imbalanced from generate_balanced_pairwise_tasks)
        max_samples: Maximum number of samples for raw split (None = use all, balanced)
        max_train_samples: Maximum number of samples for train split (None = use all)
        max_test_samples: Maximum number of test samples per task
        sampling: Sampling method ("random" or "top")
        seed: Random seed for reproducibility
        max_imbalance_ratio: Max imbalance ratio for train set (e.g., 2.0 for 1:2 ratio).
                             None = no limit (fully imbalanced).
        balance_train: If True, balance train set like test set.
                       If False, use imbalanced data (respecting max_imbalance_ratio if set).
        
    Returns:
        Dictionary of sampled pairwise tasks with balancing applied per configuration
    """
    assert sampling in ["random", "top"], "Sampling method must be 'random' or 'top'"
    import copy
    sampled_tasks = copy.deepcopy(original_tasks)
    
    # Process each split with different balancing strategies
    for split_name, sample_num in [("raw", max_samples), 
                                   ("train", max_train_samples), 
                                   ("test", max_test_samples)]:
        
        for skill_name, skill_tasks in sampled_tasks[split_name].items():
            for task_name, task_data in skill_tasks.items():
                pos_videos = task_data["pos"]
                neg_videos = task_data["neg"]
                
                # ============================================
                # CRITICAL: DIFFERENT LOGIC FOR TRAIN VS TEST
                # ============================================
                
                if split_name == "train" and not balance_train:
                    # ============================================
                    # TRAIN SET: IMBALANCED or RATIO-LIMITED
                    # ============================================
                    
                    if max_imbalance_ratio is not None:
                        # Apply imbalance ratio limit
                        pos_count = len(pos_videos)
                        neg_count = len(neg_videos)
                        
                        if pos_count > 0 and neg_count > 0:
                            current_ratio = max(pos_count, neg_count) / min(pos_count, neg_count)
                            
                            if current_ratio > max_imbalance_ratio:
                                # Need to limit the excess side
                                if pos_count > neg_count:
                                    # Too many positives, limit them
                                    max_pos = int(neg_count * max_imbalance_ratio)
                                    if sampling == "random":
                                        random.seed(seed)
                                        pos_videos = random.sample(pos_videos, max_pos)
                                    else:  # "top"
                                        pos_videos = pos_videos[:max_pos]
                                else:
                                    # Too many negatives, limit them
                                    max_neg = int(pos_count * max_imbalance_ratio)
                                    if sampling == "random":
                                        random.seed(seed)
                                        neg_videos = random.sample(neg_videos, max_neg)
                                    else:  # "top"
                                        neg_videos = neg_videos[:max_neg]
                    
                    # Use all (or ratio-limited) videos without balancing
                    task_data["pos"] = pos_videos
                    task_data["neg"] = neg_videos
                    
                else:
                    # ============================================
                    # TEST SET or BALANCED TRAIN: APPLY min(pos, neg)
                    # ============================================
                    
                    if sample_num is None:
                        # Use all available, but balanced
                        sample_count = min(len(pos_videos), len(neg_videos))
                    else:
                        # Cap at max_samples, but still balanced
                        sample_count = min(sample_num, len(pos_videos), len(neg_videos))
                    
                    if sampling == "random":
                        random.seed(seed)
                        task_data["pos"] = random.sample(pos_videos, sample_count)
                        task_data["neg"] = random.sample(neg_videos, sample_count)
                    else:  # "top"
                        task_data["pos"] = pos_videos[:sample_count]
                        task_data["neg"] = neg_videos[:sample_count]
    
    # Update train_videos and test_videos to reflect actual sampled videos
    new_train_videos = set()
    new_test_videos = set()
    
    for split_name, videos in [("train", new_train_videos), ("test", new_test_videos)]:
        for skill_name, skill_tasks in sampled_tasks[split_name].items():
            for task_name, task_data in skill_tasks.items():
                videos.update(task_data["pos"])
                videos.update(task_data["neg"])
    
    sampled_tasks["train_videos"] = list(new_train_videos)
    sampled_tasks["test_videos"] = list(new_test_videos)
    
    return sampled_tasks




def generate_pairwise_datasets(
    max_samples=MAX_SAMPLES,
    sampling=SAMPLING,
    seed=SEED,
    root=ROOT,
    video_root=VIDEO_ROOT,
    video_labels_dir=VIDEO_LABELS_DIR,
    labels_filename="label_names.json",
    pairwise_labels=get_pairwise_labels(folder_name="motion_dataset"),
    train_ratio=TRAIN_RATIO,
    folder_name="motion_dataset",
    max_imbalance_ratio=None,      # NEW
    balance_train=False,           # NEW
    min_samples_threshold=None     # NEW
):
    """
    Generate a pairwise benchmark by sampling from pairwise tasks.
    
    Args:
        max_samples: Maximum number of test samples per task
        sampling: Sampling method ("random" or "top")
        seed: Random seed for reproducibility
        root: Root directory
        video_root: Video root directory
        video_labels_dir: Directory containing video labels
        labels_filename: Filename for labels (default: "label_names.json")
        pairwise_labels: Dictionary containing skill and task definitions
        train_ratio: Ratio of videos for training
        folder_name: Folder name for the dataset
        max_imbalance_ratio: Maximum imbalance ratio for train set (e.g., 2.0 for 1:2 ratio).
                             None means no limit (fully imbalanced). (NEW)
        balance_train: If True, balance train set like test set. (NEW)
        min_samples_threshold: Minimum number of pos or neg samples per train or test task. (NEW)

    Returns:
        Dictionary with original_tasks and sampled_tasks
    """
    # Get the directory for sampled tasks
    # video_labels_dir = Path(video_labels_dir)
    # sampling_str = "top" if sampling == "top" else f"random_seed_{seed}"
    # sampled_dir = video_labels_dir / folder_name / f"test_ratio_{1 - train_ratio:.2f}_num_{max_samples}_sampling_{sampling_str}"
    # video_labels_dir = Path(video_labels_dir)
    # sampling_str = "top" if sampling == "top" else f"random_seed_{seed}"
    
    # # NEW: Build train configuration string for folder name
    # if balance_train:
    #     train_config_str = "train_balanced"
    # elif max_imbalance_ratio is not None:
    #     train_config_str = f"train_posneg_max_ratio_{max_imbalance_ratio:.1f}"
    # else:
    #     train_config_str = "train_fully_imbal"
    
    # # Include train configuration in folder name
    # sampled_dir = video_labels_dir / folder_name / \
    #     f"test_ratio_{1 - train_ratio:.2f}_num_{max_samples}_sampling_{sampling_str}_{train_config_str}"
    
    video_labels_dir = Path(video_labels_dir)
    sampling_str = "top" if sampling == "top" else f"random_seed_{seed}"
    
    # 获取当前日期，格式为 YYYY_MM_DD
    date_str = datetime.now().strftime("%Y_%m_%d")
    
    # 构建训练配置字符串
    if balance_train:
        train_config_str = "train_balanced"
    elif max_imbalance_ratio is not None:
        train_config_str = f"train_posneg_max_ratio_{max_imbalance_ratio:.1f}"
    else:
        train_config_str = "train_fully_imbal"
    
    # --- 修改这里：构建新的文件夹名称 ---
    test_ratio = 1 - train_ratio
    # 使用 f-string 组合 test_ratio, 日期, 采样方式和训练配置
    folder_alias = (
        f"test_ratio_{test_ratio:.2f}_"
        f"{date_str}_"
        f"num_{max_samples}_"
        f"sampling_{sampling_str}_"
        f"{train_config_str}"
    )
    
    sampled_dir = video_labels_dir / folder_name / folder_alias
    
    current_test_skip_tasks = get_test_skip_tasks(folder_name)
    test_skip_config_file = sampled_dir / "test_skip_tasks.json"
    
    # Check if sampled tasks already exist
    if not sampled_dir.exists():
        # First time generation - create directory and save config
        print(f"📁 Creating new dataset directory: {sampled_dir.name}")
        
        if train_ratio >= 1.0:
            # If the ratio is or larger than 1.0, directly call the simplified full extraction function
            original_tasks = generate_all_to_train_tasks(
                pairwise_labels=pairwise_labels,
                root=root,
                video_root=video_root,
                video_labels_dir=video_labels_dir,
                labels_filename=labels_filename,
                folder_name=folder_name
            )
        else:
            # Generate and sample tasks
            original_tasks = generate_balanced_pairwise_tasks(
                pairwise_labels=pairwise_labels,
                root=root,
                video_root=video_root,
                video_labels_dir=video_labels_dir,
                train_ratio=train_ratio,
                labels_filename=labels_filename,
                folder_name=folder_name,  # NEW: pass folder_name for test-skip logic
                min_samples_threshold=min_samples_threshold # NEW: pass min_samples_threshold for ensuring the number of samples is greater than the threshold
            )
        
        verify_tasks(original_tasks["train"], original_tasks["test"], original_tasks["train_videos"], original_tasks["test_videos"])
        
        sampled_tasks = sample_from_tasks(
            original_tasks,
            max_samples=None,
            max_train_samples=None,
            max_test_samples=max_samples,
            sampling=sampling,
            seed=seed,
            max_imbalance_ratio=max_imbalance_ratio,  # NEW
            balance_train=balance_train                # NEW
        )
        
        verify_tasks(sampled_tasks["train"], sampled_tasks["test"], sampled_tasks["train_videos"], sampled_tasks["test_videos"])
        
        
        # Save configuration and tasks
        sampled_config = {
            "max_samples": max_samples,
            "sampling": sampling,
            "train_ratio": train_ratio,
            "seed": seed,
            "video_labels_dir": str(video_labels_dir),
            "root": str(root),
            "video_root": str(video_root),
            "pairwise_labels": pairwise_labels
        }
        
        # Create directory and save files
        sampled_dir.mkdir(parents=True, exist_ok=True)
        
        with open(sampled_dir / "sampled_config.json", "w") as f:
            json.dump(sampled_config, f, indent=4)
            
        with open(sampled_dir / "sampled_tasks.json", "w") as f:
            json.dump(sampled_tasks, f, indent=4)
            
        with open(sampled_dir / "original_tasks.json", "w") as f:
            json.dump(original_tasks, f, indent=4)

        # Save test-skip configuration
        with open(test_skip_config_file, "w") as f:
            json.dump({
                "folder_name": folder_name,
                "test_skip_tasks": current_test_skip_tasks,
                "created_at": datetime.now().isoformat()
            }, f, indent=4)
        print(f"✅ Saved test-skip configuration to {test_skip_config_file.name}")
        
    else:
        # Dataset exists - validate test-skip configuration
        print(f"📂 Loading existing dataset from: {sampled_dir.name}")
        
        # Load existing sampled tasks and config
        with open(sampled_dir / "sampled_tasks.json", "r") as f:
            sampled_tasks = json.load(f)
            
        with open(sampled_dir / "sampled_config.json", "r") as f:
            sampled_config = json.load(f)
        
        with open(sampled_dir / "original_tasks.json", "r") as f:
            original_tasks = json.load(f)
        
        if test_skip_config_file.exists():
            with open(test_skip_config_file, "r") as f:
                saved_config = json.load(f)
            
            saved_skip_tasks = set(saved_config.get("test_skip_tasks", []))
            current_skip_tasks = set(current_test_skip_tasks)
            
            if saved_skip_tasks != current_skip_tasks:
                # Configuration mismatch!
                print("\n" + "="*70)
                print("⚠️  WARNING: Test-skip configuration has changed!")
                print("="*70)
                print(f"Saved configuration: {sorted(saved_skip_tasks)}")
                print(f"Current configuration: {sorted(current_skip_tasks)}")
                print()
                print("Added tasks (now skipped):", sorted(current_skip_tasks - saved_skip_tasks))
                print("Removed tasks (no longer skipped):", sorted(saved_skip_tasks - current_skip_tasks))
                print()
                print("❌ The existing dataset was generated with different test-skip tasks.")
                print("   To regenerate with new configuration:")
                print(f"   1. Delete the directory: rm -rf {sampled_dir}")
                print(f"   2. Re-run this script")
                print("="*70)
                raise ValueError("Test-skip configuration mismatch. Please delete and regenerate.")
        else:
            print("⚠️  Warning: No test-skip configuration found in existing dataset.")
            print("   This dataset was created before test-skip validation was added.")
    
    return {
        "original_tasks": original_tasks,
        "sampled_tasks": sampled_tasks,
        "sampled_config": sampled_config,
    }



if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate pairwise benchmark datasets with flexible train/test configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fully imbalanced train, balanced test (NEW default behavior)
  python pairwise_benchmark.py --folder_name motion_dataset

  # Train with max 1:2 imbalance ratio, balanced test
  python pairwise_benchmark.py --folder_name motion_dataset --max_imbalance_ratio 2.0

  # Both train and test balanced (original behavior)
  python pairwise_benchmark.py --folder_name motion_dataset --balance_train

  # Custom sampling and seed
  python pairwise_benchmark.py --sampling random --seed 42 --train_ratio 0.7
  
  # Show folder information
  python pairwise_benchmark.py --show_folder_info
        """
    )
    
    # Dataset selection
    parser.add_argument(
        "--folder_name", type=str, default="motion_dataset",
        choices=FOLDER_NAMES,
        help=f"Folder name for the dataset. Available: {', '.join(FOLDER_NAMES)}"
    )
    
    # Test set configuration
    parser.add_argument(
        "--max_samples", type=int, default=MAX_SAMPLES,
        help=f"Maximum number of test samples per task (default: {MAX_SAMPLES})"
    )
    
    # Sampling strategy
    parser.add_argument(
        "--sampling", type=str, default=SAMPLING,
        choices=["random", "top"],
        help=f"Sampling strategy: 'top' (first N) or 'random' (default: {SAMPLING})"
    )
    
    parser.add_argument(
        "--seed", type=int, default=SEED,
        help=f"Random seed for reproducibility (default: {SEED})"
    )
    
    # Train/test split ratio
    parser.add_argument(
        "--train_ratio", type=float, default=TRAIN_RATIO,
        help=f"Ratio of videos for training (default: {TRAIN_RATIO})"
    )
    
    # NEW: Train set balancing control
    parser.add_argument(
        "--max_imbalance_ratio", type=float, default=None,
        help="Max imbalance ratio for train set (e.g., 2.0 means max 1:2 ratio). "
             "None = no limit (fully imbalanced). Default: None"
    )
    
    parser.add_argument(
        "--balance_train", action="store_true",
        help="Balance train set like test set (default: False, train uses imbalanced data)"
    )

    parser.add_argument(
        "--min_samples_threshold", type=int, default=25,
        help="Minimum samples (min of pos/neg) required per task. "
            "Tasks below this will trigger a warning (default: 25)"
    )
    
    # Utility options
    parser.add_argument(
        "--show_folder_info", action="store_true",
        help="Show information about available folders and exit"
    )
    
    args = parser.parse_args()
    
    # Handle folder info request
    if args.show_folder_info:
        print("\n" + "="*60)
        print("Available Dataset Folders")
        print("="*60)
        for fname in FOLDER_NAMES:
            desc = get_folder_description(fname)
            skip_tasks = get_test_skip_tasks(fname)
            print(f"\n📁 {fname}:")
            print(f"   Description: {desc}")
            if skip_tasks:
                print(f"   Test-skip tasks ({len(skip_tasks)}):")
                for task in skip_tasks:
                    print(f"      - {task}")
            else:
                print(f"   Test-skip tasks: None (all tasks in both train and test)")
        print("\n" + "="*60)
        exit(0)
    
    # Validate configuration
    if args.balance_train and args.max_imbalance_ratio is not None:
        parser.error(
            "❌ Cannot use both --balance_train and --max_imbalance_ratio together. "
            "Choose one: either balance completely or set a ratio limit."
        )
    
    print("\n" + "="*60)
    print("Configuration Summary")
    print("="*60)
    print(f"Folder: {args.folder_name}")
    print(f"Max test samples: {args.max_samples}")
    print(f"Sampling: {args.sampling}")
    print(f"Seed: {args.seed}")
    print(f"Train ratio: {args.train_ratio}")
    if args.balance_train:
        print(f"Train balancing: BALANCED (like test set)")
    elif args.max_imbalance_ratio:
        print(f"Train balancing: Max ratio 1:{args.max_imbalance_ratio}")
    else:
        print(f"Train balancing: FULLY IMBALANCED (no limit)")
    print("="*60 + "\n")
    
    # # Print statistics
    # print_task_statistics(sampled_tasks)
    # datasets = generate_pairwise_datasets(
    #     max_samples=args.max_samples,
    #     sampling=SAMPLING,
    #     seed=SEED,
    #     root=ROOT,
    #     video_root=VIDEO_ROOT,
    #     video_labels_dir=VIDEO_LABELS_DIR,
    #     labels_filename="label_names.json",
    #     pairwise_labels=get_pairwise_labels(args.folder_name),
    #     train_ratio=TRAIN_RATIO,
    #     folder_name=args.folder_name
    # )
    datasets = generate_pairwise_datasets(
        max_samples=args.max_samples,
        sampling=args.sampling,                        # Changed: use args
        seed=args.seed,                                # Changed: use args
        root=ROOT,
        video_root=VIDEO_ROOT,
        video_labels_dir=VIDEO_LABELS_DIR,
        labels_filename="label_names.json",
        pairwise_labels=get_pairwise_labels(args.folder_name),
        train_ratio=args.train_ratio,                  # Changed: use args
        folder_name=args.folder_name,
        max_imbalance_ratio=args.max_imbalance_ratio,  # NEW
        balance_train=args.balance_train,              # NEW
        min_samples_threshold=args.min_samples_threshold # NEW
    )
    print_detailed_task_statistics(
        datasets['original_tasks']["raw"],
        datasets['sampled_tasks']["train"],
        datasets['sampled_tasks']["test"]
    )
    print(f"Number of train videos: {len(datasets['sampled_tasks']['train_videos'])}")
    print(f"Number of test videos: {len(datasets['sampled_tasks']['test_videos'])}")
    
    # import pdb; pdb.set_trace()
    # Create benchmark
    # benchmark = PairwiseBenchmark(datasets['sampled_tasks']['test'], mode="vqa")
    
    # import numpy as np
    # retrieval_scores = np.random.rand(len(benchmark), 2, 2)
    # yes_scores = np.random.rand(len(benchmark), 2, 2)
    # no_scores = np.random.rand(len(benchmark), 2, 2)
    # benchmark.evaluate_and_print_retrieval(retrieval_scores)
    # benchmark.evaluate_and_print_vqa(yes_scores, no_scores)