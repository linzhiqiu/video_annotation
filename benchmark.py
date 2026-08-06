# benchmark.py
from label import Label, extract_labels_dict

import torch
from torch.utils.data import Dataset
from pathlib import Path

from download import get_labels
from label import extract_labels_dict, Label

from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve
import numpy as np
import matplotlib.pyplot as plt

# ROOT = Path("/data3/zhiqiul/video_annotation")
# VIDEO_ROOT = Path("/data3/zhiqiul/video_annotation/videos")
# VIDEO_LABELS_DIR = Path("/data3/zhiqiul/video_annotation/video_labels")
ROOT = Path("./")
VIDEO_ROOT = Path("./videos")
VIDEO_LABELS_DIR = Path("./video_labels")
VIDEO_LABEL_FILE = "video_labels/cam_motion-20250223_2308/label_names_selected.json"

def labels_as_dict(root=ROOT, video_root=VIDEO_ROOT, video_label_file=VIDEO_LABEL_FILE):
    if not isinstance(root, Path) or not isinstance(video_root, Path):
        root = Path(root)
        video_root = Path(video_root)
    all_labels = get_labels(root / video_label_file)
    label_collection = extract_labels_dict(Label.load_all_labels(labels_dir=root / "labels"))
    for label_name in all_labels:
        assert label_name in label_collection, f"Label {label_name} not found in label collection"
        # Add def_question, alt_question, def_prompt, alt_prompt to all_labels
        for key in ['def_question', 'alt_question', 'def_prompt', 'alt_prompt']:
            all_labels[label_name][key] = getattr(label_collection[label_name], key)
        # Add the Label object to all_labels
        all_labels[label_name]['label_obj'] = label_collection[label_name]
        # Prepend video_root to all video paths
        all_labels[label_name]['pos'] = [str(video_root / video_path) for video_path in all_labels[label_name]['pos']]
        all_labels[label_name]['neg'] = [str(video_root / video_path) for video_path in all_labels[label_name]['neg']]
    return all_labels

# all_labels = labels_as_dict(root=ROOT, video_label_file=VIDEO_LABEL_FILE)

class BinaryTask(Dataset):

    def __init__(
        self,
        label_dict,
        mode="vqa",
        def_index=0, # default to take the first def_question or first def_prompt
    ):
        assert mode in ["vqa", "retrieval"]
        self.pos = label_dict['pos']
        self.neg = label_dict['neg']
        self.labels = [1] * len(self.pos) + [0] * len(self.neg)
        self.videos = self.pos + self.neg
        self.def_prompt = label_dict['def_prompt']
        self.alt_prompt = label_dict['alt_prompt']
        self.def_question = label_dict['def_question']
        self.alt_question = label_dict['alt_question']
        
        if mode == "retrieval":
            self.prompt = self.def_prompt[def_index]
        else:
            self.prompt = self.def_question[def_index]
        self.label_name = label_dict['label_name']
        self.label = label_dict['label']
        self.label_obj = label_dict['label_obj']

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, idx):
        video_path = self.videos[idx]
        item = {"images": [str(video_path)], "texts": [self.prompt]}
        return item
    
    def evaluate_scores_subset(self, scores, subset_videos, score_name, print_name, save_path=None):
        # First assert all subset_videos are in self.videos
        for video in subset_videos:
            if video not in self.videos:
                print(f"Video {video} not found in the dataset")
                import pdb; pdb.set_trace()
        
        # print(f"Evaluating for task {self.label_name}")
        assert type(scores) == np.ndarray, "Scores must be a numpy array"
        assert len(scores.shape) == 1, "Scores must be a 1D array"
        assert scores.shape[0] == len(self.videos), f"Scores shape {scores.shape} does not match number of videos {len(self.videos)}"
        
        # Get the indices of the subset_videos
        subset_indices = [self.videos.index(video) for video in subset_videos]
        y_true = np.array(self.labels)[subset_indices]
        # random chance AP is the same as the fraction of positive labels
        random_ap = np.mean(y_true)
        
        y_scores = scores[subset_indices]
        results = {}
        # Replace NaNs with -inf
        y_scores = np.where(np.isfinite(y_scores), y_scores, -1e10)
        
        ap = average_precision_score(y_true, y_scores)
        roc_auc = roc_auc_score(y_true, y_scores)
        
        # Compute Precision-Recall curve
        precision, recall, thresholds = precision_recall_curve(y_true, y_scores)

        # Compute F1 scores for all thresholds
        f1_scores = np.where((precision + recall) > 0, 
                             2 * (precision * recall) / (precision + recall), 
                             0)  # Set F1 to 0 when precision and recall are both 0
        if len(f1_scores) > 0:
            best_idx = np.argmax(f1_scores)
            optimal_f1 = f1_scores[best_idx]
            optimal_threshold = thresholds[best_idx]
        else:
            best_idx = 0
            optimal_f1 = 0
            optimal_threshold = np.mean(y_scores)

        results = {
            "prompt": self.prompt,
            "ap": float(ap),
            "random_ap": float(random_ap),
            "roc_auc": float(roc_auc),
            "optimal_f1": float(optimal_f1),
            "optimal_threshold": float(optimal_threshold)
        }
        header = f"{score_name:80s} {'AP':>10} {'AP (Random)':>10} {'ROC AUC':>10} {'F1':>10} {'Threshold':>12}\n"
        separator = "-" * len(header) + "\n"
        result_str = f"{print_name:80s} {ap:>10.4f} {random_ap:>10.4f} {roc_auc:>10.4f} {optimal_f1:>10.4f} {optimal_threshold:>12.4f}\n"
        
        # print(f"AP: {ap:.4f}, ROC-AUC: {roc_auc:.4f}, Optimal F1: {optimal_f1:.4f} @ Threshold: {optimal_threshold:.2f}")
        print_str = header + separator + result_str
        print(print_str)
        if save_path:
            # write print_str to save_path
            with open(save_path, "a") as f:
                f.write(print_str)
        return results

    def evaluate_scores(self, scores, plot_path=None):
        # Calculate the Average Precision for each prompt
        print(f"Evaluating for task {self.label_name}")
        assert type(scores) == np.ndarray, "Scores must be a numpy array"
        assert len(scores.shape) == 1, "Scores must be a 1D array"
        assert scores.shape[0] == len(self.videos), f"Scores shape {scores.shape} does not match number of videos {len(self.videos)}"
        y_true = self.labels
        results = {}
        # Replace NaNs with -inf
        y_scores = np.where(np.isfinite(scores), scores, -1e10)
        
        ap = average_precision_score(y_true, y_scores)
        roc_auc = roc_auc_score(y_true, y_scores)
        
        # Compute Precision-Recall curve
        precision, recall, thresholds = precision_recall_curve(y_true, y_scores)

        # Compute F1 scores for all thresholds
        f1_scores = np.where((precision + recall) > 0, 
                             2 * (precision * recall) / (precision + recall), 
                             0)  # Set F1 to 0 when precision and recall are both 0
        if len(f1_scores) > 0:
            best_idx = np.argmax(f1_scores)
            optimal_f1 = f1_scores[best_idx]
            optimal_threshold = thresholds[best_idx]
        else:
            best_idx = 0
            optimal_f1 = 0
            optimal_threshold = np.mean(y_scores)

        results = {
            "prompt": self.prompt,
            "ap": float(ap),
            "roc_auc": float(roc_auc),
            "optimal_f1": float(optimal_f1),
            "optimal_threshold": float(optimal_threshold)
        }
        print(f"AP: {ap:.4f}, ROC-AUC: {roc_auc:.4f}, Optimal F1: {optimal_f1:.4f} @ Threshold: {optimal_threshold:.2f}")
        if plot_path:
            print(f"Plotting to {plot_path}")
            best_idx = np.argmax(f1_scores)
            best_precision, best_recall = precision[best_idx], recall[best_idx]
            plt.figure(figsize=(8, 6))

            # Plot Precision-Recall Curve
            plt.plot(recall, precision, label=f'Precision-Recall Curve (AP={results["ap"]:.4f})', color='blue', linewidth=2)

            # Highlight the best threshold point
            plt.scatter(best_recall, best_precision, color='red', zorder=3, label=f'Optimal F1={optimal_f1:.4f} @ Threshold={optimal_threshold:.2f}', s=100)

            # Labels and Title
            plt.xlabel("Recall", fontsize=12)
            plt.ylabel("Precision", fontsize=12)
            plt.title(f"Precision-Recall Curve\n{self.prompt}", fontsize=14)
            plt.legend(loc="lower left", fontsize=10)
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.ylim([0, 1])
            # Save the plot
            plt.savefig(plot_path, bbox_inches="tight", dpi=300)
            plt.close()
        return results
