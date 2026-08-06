# prepare_train_json.py - COMPLETE REPLACEMENT
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


# DRY: Caption question formats
CAPTION_QUESTION_FORMATS = [
    "Please describe how the camera moves in this video.",
    "Describe how the camera moves in this video.",
    "How does the camera move in this video?",
    "What is the camera movement in this video?",
    "Describe the camera movement in this video.",
    "Can you describe how the camera moves in this video?",
    "Please describe the camera movement in this video.",
    "Explain the camera movement in this video.",
    "Provide an overview of the camera movement in this video.",
    "How is the camera moving in this video?",
    "What type of camera movement is used in this video?",
    "Can you explain the camera movement in this video?",
    "What kind of camera motion is present in this video?",
    "Tell me about the camera movement in this video.",
    "Identify the camera movement in this video.",
    "Break down the camera movement in this video.",
    "Summarize the camera movement in this video.",
    "Give details about the camera movement in this video.",
    "Describe the motion of the camera in this video.",
    "How does the camera move throughout this video?",
    "Explain the dynamics of the camera movement in this video.",
    "What camera techniques are used in this video?",
    "Analyze the camera motion in this video.",
    "Break down the camera dynamics in this video.",
    "What are the key camera movements in this video?",
]


def generate_motion_caption_vqa(caption_retrieval_samples):
    """Generate VQA samples from motion caption data"""
    trainset = []
    for item in caption_retrieval_samples:
        trainset.extend(convert_to_list_vqa(item, question_format="{}"))
        trainset.extend(convert_to_list_vqa(item, question_format="{} Please only answer Yes or No."))
    return trainset


def generate_label_vqa(skill_retrieval_samples):
    """Generate VQA samples from label-based tasks"""
    trainset = []
    for item in skill_retrieval_samples:
        trainset.extend(convert_to_list_vqa(item, question_format="{}"))
        trainset.extend(convert_to_list_vqa(item, question_format="{} Please only answer Yes or No."))
    return trainset


def generate_motion_caption_generation(caption_generation_samples, question_formats=None):
    """Generate caption generation samples"""
    if question_formats is None:
        question_formats = CAPTION_QUESTION_FORMATS
    
    captionset = []
    for item in caption_generation_samples:
        for question_format in question_formats:
            captionset.extend(convert_to_list_caption(item, question_format=question_format))
    return captionset


if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate training JSON with flexible output options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Types:
  full: Label VQA + Motion caption VQA + Motion caption generation (original behavior)
  label_vqa_only: Only VQA tasks from labels (no captions needed)
  motion_caption_vqa_only: Only VQA derived from motion captions (no label-based VQA)
  motion_caption_gen_only: Only motion caption generation tasks (no VQA)
  
Examples:
  # Full training set (original behavior)
  python prepare_train_json.py --output_type full

  # Only VQA from labels (skip captions - no caption files needed!)
  python prepare_train_json.py --output_type label_vqa_only

  # Only motion caption VQA
  python prepare_train_json.py --output_type motion_caption_vqa_only
  
  # Custom save path
  python prepare_train_json.py --output_type label_vqa_only --save_path my_trainset.json
        """
    )
    
    parser.add_argument(
        "--caption_save_dir", type=str, 
        default="cam_motion-20250227_0324ground_only",
        help="Directory containing caption data (required for caption-based outputs)"
    )
    
    parser.add_argument(
        "--max_samples", type=int, default=MAX_SAMPLES,
        help=f"Maximum number of samples per task (default: {MAX_SAMPLES})"
    )
    
    parser.add_argument(
        "--max_neg_samples", type=int, default=MAX_NEG_SAMPLES,
        help=f"Maximum number of negative caption samples (default: {MAX_NEG_SAMPLES})"
    )
    
    parser.add_argument(
        "--split", type=str, default="train",
        choices=["train", "test"],
        help="Split to use (default: train)"
    )
    
    # NEW: Output type control
    parser.add_argument(
        "--output_type", type=str, default="full",
        choices=["full", "label_vqa_only", "motion_caption_vqa_only", "motion_caption_gen_only"],
        help="Type of training data to generate (default: full)"
    )
    
    parser.add_argument(
        "--save_path", type=str, default=None,
        help="Path to save the JSON file (default: auto-generated based on output_type)"
    )
    
    args = parser.parse_args()
    
    # Determine save path based on output type if not specified
    if args.save_path is None:
        save_path_map = {
            "full": "trainset.json",
            "label_vqa_only": "trainset_label_vqa_only.json",
            "motion_caption_vqa_only": "trainset_motion_caption_vqa_only.json",
            "motion_caption_gen_only": "trainset_motion_caption_gen_only.json"
        }
        args.save_path = save_path_map[args.output_type]
    
    print("\n" + "="*60)
    print("Configuration Summary")
    print("="*60)
    print(f"Output type: {args.output_type}")
    print(f"Split: {args.split}")
    print(f"Max samples: {args.max_samples}")
    print(f"Save path: {args.save_path}")
    print("="*60 + "\n")
    
    # Initialize dataset components
    trainset = []
    captionset = []
    
    # ============================================
    # LOAD MOTION CAPTION DATA (if needed)
    # ============================================
    if args.output_type in ["full", "motion_caption_vqa_only", "motion_caption_gen_only"]:
        print("📝 Loading motion caption data...")
        raw_caption_retrieval = generate_pairwise_caption_dataset(
            caption_save_dir=args.caption_save_dir,
            max_samples=args.max_samples,
            max_neg_samples=args.max_neg_samples,
            split=args.split,
            video_root=VIDEO_ROOT,
            video_labels_dir=VIDEO_LABELS_DIR,
        )
        
        # For VQA mode (caption matching)
        caption_retrieval = PairwiseCaptionBenchmark(raw_caption_retrieval, mode="vqa")
        print(f"   ✅ Loaded {len(caption_retrieval.samples)} caption VQA samples")
        
        # For generation mode (caption generation)
        caption_generation = PairwiseCaptionBenchmark(raw_caption_retrieval, mode="retrieval")
        print(f"   ✅ Loaded {len(caption_generation.samples)} caption generation samples\n")
        print(f"   First caption sample: {caption_generation.samples[0]}\n")
    
    # ============================================
    # LOAD LABEL VQA DATA (if needed)
    # ============================================
    if args.output_type in ["full", "label_vqa_only"]:
        print("🎯 Loading label VQA data...")
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
        
        # CRITICAL: Use original_tasks for imbalanced train data!
        skill_retrieval = PairwiseBenchmark(
            raw_skill_retrieval['original_tasks'][args.split],  # Use original (imbalanced)!
            mode="vqa"
        )
        print(f"   ✅ Loaded {len(skill_retrieval.samples)} label VQA samples")
        print(f"   First label VQA sample: {skill_retrieval.samples[0]}\n")
    
    # ============================================
    # GENERATE DATASETS BASED ON OUTPUT TYPE
    # ============================================
    
    print(f"🔨 Generating {args.output_type} dataset...\n")
    
    if args.output_type == "full":
        # Original behavior: all three types
        # 1. VQA from motion captions
        trainset.extend(generate_motion_caption_vqa(caption_retrieval.samples))
        
        # 2. VQA from labels
        trainset.extend(generate_label_vqa(skill_retrieval.samples))
        
        # 3. Caption generation
        captionset.extend(generate_motion_caption_generation(caption_generation.samples))
        
        # Combine and shuffle
        random.shuffle(trainset)
        print(f"   First VQA sample: {trainset[0]}")
        
        random.shuffle(captionset)
        print(f"   First caption sample: {captionset[0]}")
        
        print(f"\n   📊 VQA samples: {len(trainset)}")
        print(f"   📊 Caption generation samples: {len(captionset)}")
        
        finalset = trainset + captionset
        random.shuffle(finalset)
        
    elif args.output_type == "label_vqa_only":
        # Only VQA from labels
        trainset.extend(generate_label_vqa(skill_retrieval.samples))
        random.shuffle(trainset)
        
        finalset = trainset
        print(f"   First sample: {finalset[0]}")
        print(f"   📊 Label VQA samples: {len(finalset)}")
        
    elif args.output_type == "motion_caption_vqa_only":
        # Only VQA from motion captions
        trainset.extend(generate_motion_caption_vqa(caption_retrieval.samples))
        random.shuffle(trainset)
        
        finalset = trainset
        print(f"   First sample: {finalset[0]}")
        print(f"   📊 Motion caption VQA samples: {len(finalset)}")
        
    elif args.output_type == "motion_caption_gen_only":
        # Only caption generation
        captionset.extend(generate_motion_caption_generation(caption_generation.samples))
        random.shuffle(captionset)
        
        finalset = captionset
        print(f"   First sample: {finalset[0]}")
        print(f"   📊 Motion caption generation samples: {len(finalset)}")
    
    # ============================================
    # SAVE OUTPUT
    # ============================================
    
    from pairwise_benchmark import VIDEO_LABELS_DIR, SAMPLING
    sampling_str = "top" if SAMPLING == "top" else f"random_seed_{SEED}"
    sampled_dir = Path(VIDEO_LABELS_DIR) / "motion_dataset" / \
        f"test_ratio_{1 - TRAIN_RATIO:.2f}_num_{args.max_samples}_sampling_{sampling_str}_train_imbalanced"
    
    # Create directory if it doesn't exist
    sampled_dir.mkdir(parents=True, exist_ok=True)
    
    filename = sampled_dir / args.save_path
    
    print(f"\n" + "="*60)
    print("Save Summary")
    print("="*60)
    print(f"Total samples: {len(finalset)}")
    print(f"Saving to: {filename}")
    print("="*60 + "\n")
    
    with open(filename, "w") as f:
        json.dump(finalset, f, indent=4)
    
    # PRESERVED: Save separate files like original
    if args.output_type == "full":
        # Save captionset separately
        caption_filename = sampled_dir / "captionset.json"
        with open(caption_filename, "w") as f:
            json.dump(captionset, f, indent=4)
        print(f"✅ Also saved caption generation to {caption_filename}")
        
        # Save balanced VQA separately
        balanced_vqa_filename = sampled_dir / "balanced_vqa.json"
        with open(balanced_vqa_filename, "w") as f:
            json.dump(trainset, f, indent=4)
        print(f"✅ Also saved VQA tasks to {balanced_vqa_filename}")
    
    print(f"\n✅ Successfully saved {len(finalset)} samples to {filename}!")