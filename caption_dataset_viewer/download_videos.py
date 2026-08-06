#!/usr/bin/env python3
"""
Download Videos and Enrich Annotations

This script:
1. Downloads the dataset JSON from HuggingFace (source obfuscated)
2. Enriches annotation files with caption/metadata/video info
3. Downloads videos for all completed annotations

Usage:
    python download_videos.py --dataset DATASET_NAME
    python download_videos.py --all
"""

import argparse
import json
import os
from pathlib import Path
from huggingface_hub import hf_hub_download, list_repo_files
import shutil
import base64

# Configuration - obfuscated for privacy
_REPO_ENCODED = "emhpcWl1bGluL3ZpZGVvX2NhcHRpb25fZGF0YXNldHM="
HF_REPO = base64.b64decode(_REPO_ENCODED).decode('utf-8')
ANNOTATIONS_DIR = Path("annotations")
VIDEOS_DIR = Path("videos")


def is_annotation_complete(annotation):
    """Check if an annotation is complete."""
    if not annotation:
        return False
    
    required_fields = ['overall', 'camera', 'subject', 'motion', 'scene', 'spatial']
    all_ratings_complete = all(
        annotation.get(field) is not None 
        for field in required_fields
    )
    
    segments_valid = True
    if annotation.get('segments') and len(annotation['segments']) > 0:
        segments_valid = all(
            seg.get('startIndex') is not None and seg.get('endIndex') is not None
            for seg in annotation['segments']
        )
    
    return all_ratings_complete and segments_valid


def load_dataset_from_hf(dataset_name, hf_repo):
    """Load dataset JSON from HuggingFace."""
    try:
        # Find JSON files for this dataset
        files = list_repo_files(repo_id=hf_repo, repo_type="dataset")
        json_files = [f for f in files if f.startswith(dataset_name + '/') and f.endswith('.json')]
        
        if not json_files:
            print(f"❌ No JSON files found for dataset: {dataset_name}")
            return None
        
        # Download and parse the first JSON file
        json_file = json_files[0]
        print(f"📥 Downloading dataset JSON: {json_file}")
        
        local_path = hf_hub_download(
            repo_id=hf_repo,
            filename=json_file,
            repo_type="dataset",
            cache_dir="/tmp/hf_cache"
        )
        
        with open(local_path, 'r') as f:
            data = json.load(f)
        
        return data.get('samples', [])
    
    except Exception as e:
        print(f"❌ Error loading dataset from HuggingFace: {e}")
        return None


def enrich_annotation_file(ann_file, sample_data, dataset_name, force=False):
    """Enrich annotation file with sample data (captions, metadata, video info)."""
    try:
        with open(ann_file, 'r') as f:
            annotation = json.load(f)
        
        # Check if already enriched (has captions field)
        if not force and 'captions' in annotation and annotation['captions']:
            # Already enriched, skip to avoid overwriting
            return None
        
        # Get video info
        video_url = sample_data.get('video_url', '')
        if video_url:
            # Extract filename from URL
            video_filename = Path(video_url).name
            video_path = f"{dataset_name}/{video_filename}"
        else:
            video_path = ''
        
        # Add sample data to annotation (NO external URLs!)
        annotation['video_id'] = sample_data.get('video_id', '')
        annotation['video_path'] = video_path
        annotation['captions'] = sample_data.get('captions', {})
        annotation['metadata'] = sample_data.get('metadata', {})
        
        # Remove video_url if it exists (no external URLs allowed)
        if 'video_url' in annotation:
            del annotation['video_url']
        
        # Save enriched annotation
        with open(ann_file, 'w') as f:
            json.dump(annotation, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"❌ Error enriching {ann_file.name}: {e}")
        return None


def download_videos_for_dataset(dataset_name, hf_repo, annotations_dir, videos_dir, force=False):
    """Enrich annotations and download videos for completed annotations in a dataset."""
    dataset_dir = annotations_dir / dataset_name
    
    if not dataset_dir.exists():
        print(f"❌ Dataset not found: {dataset_name}")
        return 0
    
    # Load dataset from HuggingFace
    print(f"\n📦 Processing dataset: {dataset_name}")
    samples = load_dataset_from_hf(dataset_name, hf_repo)
    
    if not samples:
        print(f"❌ Could not load dataset from HuggingFace")
        return 0
    
    print(f"   Found {len(samples)} samples in HuggingFace dataset")
    
    # Create videos directory for this dataset
    dataset_videos_dir = videos_dir / dataset_name
    dataset_videos_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all completed annotations
    annotation_files = sorted(dataset_dir.glob("sample_*.json"))
    print(f"   Found {len(annotation_files)} annotation files")
    
    enriched = 0
    downloaded = 0
    skipped = 0
    
    for ann_file in annotation_files:
        # Get sample index from filename
        sample_idx = int(ann_file.stem.split('_')[1])
        
        # Load annotation
        with open(ann_file, 'r') as f:
            annotation = json.load(f)
        
        if not is_annotation_complete(annotation):
            continue
        
        # Get corresponding sample data
        if sample_idx >= len(samples):
            print(f"⚠️  Sample index {sample_idx} out of range, skipping")
            continue
        
        sample_data = samples[sample_idx]
        
        # Enrich annotation file with sample data
        enrichment_result = enrich_annotation_file(ann_file, sample_data, dataset_name, force=force)
        if enrichment_result:
            print(f"✓ Enriched: sample_{sample_idx}.json")
            enriched += 1
        elif enrichment_result is None:
            # Already enriched, skip silently
            pass
        else:
            # Error occurred
            pass
        
        # Get video path
        video_url = sample_data.get('video_url', '')
        if not video_url:
            print(f"⚠️  No video_url for sample {sample_idx}, skipping")
            continue
        
        # Determine video filename from URL
        video_filename = Path(video_url).name
        
        # Determine local video path - use dataset/filename structure
        local_video_path = dataset_videos_dir / video_filename
        
        # Skip if already downloaded
        if local_video_path.exists():
            print(f"✓ Already exists: {video_filename}")
            skipped += 1
            continue
        
        # Download from HuggingFace
        try:
            print(f"⬇️  Downloading: {video_filename}...")
            
            # Extract HF path from video_url
            # video_url format: https://huggingface.co/datasets/REPO/resolve/main/DATASET/videos/FILE
            # We need: DATASET/videos/FILE
            hf_path_parts = video_url.split('/resolve/main/')
            if len(hf_path_parts) > 1:
                hf_file_path = hf_path_parts[1]
            else:
                # Fallback: assume it's in dataset/videos/
                hf_file_path = f"{dataset_name}/videos/{video_filename}"
            
            # Download from HF
            downloaded_path = hf_hub_download(
                repo_id=hf_repo,
                filename=hf_file_path,
                repo_type="dataset",
                cache_dir="/tmp/hf_cache"
            )
            
            # Copy to local videos directory
            shutil.copy(downloaded_path, local_video_path)
            
            print(f"✅ Downloaded: {video_filename}")
            downloaded += 1
            
        except Exception as e:
            print(f"❌ Failed to download {video_filename}: {e}")
    
    print(f"\n📊 Summary for {dataset_name}:")
    print(f"   Enriched annotations: {enriched}")
    print(f"   Downloaded videos: {downloaded}")
    print(f"   Skipped (already exists): {skipped}")
    
    return downloaded


def main():
    parser = argparse.ArgumentParser(description="Download videos and enrich annotations")
    parser.add_argument("--dataset", type=str, help="Dataset name to download")
    parser.add_argument("--all", action="store_true", help="Download all datasets")
    parser.add_argument("--force", action="store_true", help="Force re-enrichment even if already enriched")
    parser.add_argument("--repo", type=str, default=HF_REPO, help="HuggingFace repo (obfuscated by default)")
    parser.add_argument("--annotations_dir", type=str, default=None, help="Annotations directory")
    parser.add_argument("--videos_dir", type=str, default=None, help="Videos output directory")
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.resolve()
    annotations_dir = Path(args.annotations_dir) if args.annotations_dir else script_dir / ANNOTATIONS_DIR
    videos_dir = Path(args.videos_dir) if args.videos_dir else script_dir / VIDEOS_DIR
    
    if not annotations_dir.exists():
        print(f"❌ Annotations directory not found: {annotations_dir}")
        return
    
    # Create videos directory
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🎬 Video Downloader for Completed Annotations")
    print("=" * 70)
    print(f"📦 Source: HuggingFace (obfuscated)")
    print(f"💾 Annotations:      {annotations_dir.resolve()}")
    print(f"🎬 Videos Output:    {videos_dir.resolve()}")
    print("=" * 70)
    
    total_downloaded = 0
    
    if args.all:
        # Download all datasets
        datasets = [d for d in annotations_dir.iterdir() if d.is_dir()]
        print(f"\n🔍 Found {len(datasets)} datasets")
        
        for dataset_dir in datasets:
            downloaded = download_videos_for_dataset(
                dataset_dir.name, 
                args.repo, 
                annotations_dir, 
                videos_dir,
                force=args.force
            )
            total_downloaded += downloaded
    
    elif args.dataset:
        # Download specific dataset
        downloaded = download_videos_for_dataset(
            args.dataset, 
            args.repo, 
            annotations_dir, 
            videos_dir,
            force=args.force
        )
        total_downloaded += downloaded
    
    else:
        print("\n❌ Please specify --dataset DATASET_NAME or --all")
        parser.print_help()
        return
    
    print("\n" + "=" * 70)
    print(f"✅ Total videos downloaded: {total_downloaded}")
    print("=" * 70)


if __name__ == "__main__":
    main()