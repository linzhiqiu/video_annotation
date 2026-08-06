#!/usr/bin/env python3
"""
Download ShotBench and RefineShot Data

Downloads:
1. ShotBench dataset metadata from HuggingFace (Vchitect/ShotBench)
2. RefineShot refined data from GitHub (wuhang03/RefineShot)
3. All images and videos from the HuggingFace dataset repo (images.tar + videos.tar)

Usage:
    python download_data.py                    # Download everything (metadata + all media)
    python download_data.py --metadata-only    # Only download JSON metadata, skip media
    python download_data.py --modality video   # Only download videos (videos.tar)
    python download_data.py --modality image   # Only download images (images.tar)
"""

import argparse
import json
import csv
import os
import sys
import random
from pathlib import Path

DATA_DIR = Path("data")
MEDIA_DIR = Path("media")

SHOTBENCH_REPO = "Vchitect/ShotBench"
REFINESHOT_REPO_URL = "https://raw.githubusercontent.com/wuhang03/RefineShot/master"


def _unwrap_field(value):
    """
    Unwrap a field that might be a plain string, list, numpy array,
    HuggingFace Sequence, or stringified list.
    
    HuggingFace datasets can return fields in various formats:
      - Plain string: "image/ABC.jpg"
      - Python list: ["image/ABC.jpg"]
      - Stringified list: "['image/ABC.jpg']"
      - Numpy array or other sequence types
    
    This function always returns a plain string.
    """
    # Handle None
    if value is None:
        return ''
    
    # Handle any sequence-like type (list, tuple, numpy array, HF Sequence)
    # Check for __getitem__ and __len__ but NOT string (strings have those too)
    if not isinstance(value, str) and hasattr(value, '__len__') and hasattr(value, '__getitem__'):
        try:
            return str(value[0]) if len(value) > 0 else ''
        except (IndexError, KeyError):
            pass
    
    value = str(value).strip()
    
    # Handle stringified list: "['image/ABC.jpg']" or '["image/ABC.jpg"]'
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1].strip()
        # Remove quotes: 'image/ABC.jpg' or "image/ABC.jpg"
        if (inner.startswith("'") and inner.endswith("'")) or \
           (inner.startswith('"') and inner.endswith('"')):
            inner = inner[1:-1]
        return inner
    
    return value


def download_shotbench():
    """Download ShotBench dataset from HuggingFace."""
    print("📦 Downloading ShotBench from HuggingFace...")
    
    try:
        from datasets import load_dataset
        
        ds = load_dataset(SHOTBENCH_REPO, split='test')
        print(f"   ✅ Loaded {len(ds)} samples")
        
        # Debug: show raw field types from first sample
        first = ds[0]
        print(f"   🔍 Debug - raw field types from first sample:")
        print(f"      path: type={type(first['path']).__name__}, value={repr(first['path'])}")
        print(f"      type: type={type(first['type']).__name__}, value={repr(first['type'])}")
        print(f"      path unwrapped: {repr(_unwrap_field(first['path']))}")
        print(f"      type unwrapped: {repr(_unwrap_field(first['type']))}")
        
        # Convert to our format
        samples = []
        for i, item in enumerate(ds):
            # Parse options - could be string or dict
            options = item['options']
            if isinstance(options, str):
                options = json.loads(options)
            
            # Parse type field - could be string, list, or stringified list
            sample_type = item['type']
            modality = _unwrap_field(sample_type)
            
            # Parse path field - could be string, list, or stringified list
            path = item['path']
            media_path = _unwrap_field(path)
                
            samples.append({
                'index': item['index'],
                'type': modality,
                'path': media_path,
                'question': item['question'],
                'options': options,
                'answer': item['answer'],
                'category': item['category']
            })
        
        # Save as JSON
        output_path = DATA_DIR / "shotbench.json"
        with open(output_path, 'w') as f:
            json.dump(samples, f, indent=2)
        
        # Validate paths are clean
        bad_paths = [s['path'] for s in samples[:10] if s['path'].startswith('[')]
        if bad_paths:
            print(f"   ⚠️  WARNING: {len(bad_paths)} paths still have brackets!")
            print(f"      Examples: {bad_paths[:3]}")
        else:
            print(f"   ✅ All paths validated (e.g. {samples[0]['path']})")
        
        print(f"   💾 Saved to {output_path}")
        return samples
        
    except ImportError:
        print("   ⚠️  'datasets' library not available, trying CSV download...")
        return download_shotbench_csv()


def download_shotbench_csv():
    """Fallback: download ShotBench as CSV from HuggingFace."""
    try:
        from huggingface_hub import hf_hub_download
        
        # Download the parquet/csv file
        local_path = hf_hub_download(
            repo_id=SHOTBENCH_REPO,
            filename="data/test-00000-of-00001.parquet",
            repo_type="dataset",
            cache_dir="/tmp/hf_cache"
        )
        
        import pandas as pd
        df = pd.read_parquet(local_path)
        
        samples = []
        for _, row in df.iterrows():
            options = row['options']
            if isinstance(options, str):
                options = json.loads(options)
            
            sample_type = row['type']
            modality = _unwrap_field(sample_type)
                
            path = row['path']
            media_path = _unwrap_field(path)
            
            samples.append({
                'index': int(row['index']),
                'type': modality,
                'path': media_path,
                'question': row['question'],
                'options': options,
                'answer': row['answer'],
                'category': row['category']
            })
        
        output_path = DATA_DIR / "shotbench.json"
        with open(output_path, 'w') as f:
            json.dump(samples, f, indent=2)
        
        print(f"   💾 Saved {len(samples)} samples to {output_path}")
        return samples
        
    except Exception as e:
        print(f"   ❌ CSV download failed: {e}")
        return None


def download_refineshot():
    """Download RefineShot data from GitHub."""
    print("📦 Downloading RefineShot from GitHub...")
    
    # Embedded fallback — RefineShot's category.json is small and stable
    # Source: https://github.com/wuhang03/RefineShot/blob/master/category.json
    CATEGORY_JSON_FALLBACK = {
        "shot framing": {
            "all": ["Single", "Insert", "2 shot", "3 shot", "Group shot", "Establishing shot", "Over the shoulder"],
            "breakdown": {
                "subject_count": ["Single", "2 shot", "3 shot", "Group shot"],
                "detail": ["Insert"],
                "perspective": ["Over the shoulder"],
                "environment": ["Establishing shot"]
            }
        },
        "lighting type": {
            "all": ["Daylight", "Artificial light", "Mixed light", "Firelight", "Overcast", "Practical light", "Sunny", "Moonlight", "Fluorescent", "HMI", "Tungsten", "LED"],
            "breakdown": {
                "light_source": ["Daylight", "Moonlight", "Firelight", "Artificial light", "Mixed light"],
                "daylight_type": ["Overcast", "Sunny"],
                "artificial_light_type": ["Fluorescent", "HMI", "Tungsten", "LED"],
                "visible": ["Practical light"]
            }
        },
        "lighting": {
            "all": [
                "Side light", "Backlight", "Top light", "Underlight",
                "Hard light", "Soft light",
                "High contrast", "Low contrast",
                "Edge light", "Silhouette"
            ],
            "breakdown": {
                "direction": ["Side light", "Backlight", "Top light", "Underlight"],
                "quality": ["Hard light", "Soft light"],
                "contrast": ["High contrast", "Low contrast"],
                "technique": ["Edge light"],
                "effect": ["Silhouette"]
            }
        }
    }
    
    categories = None
    category_path = DATA_DIR / "refineshot_category.json"
    
    # Try downloading from GitHub first
    try:
        import urllib.request
        category_url = f"{REFINESHOT_REPO_URL}/category.json"
        print(f"   ⬇️  Downloading category.json...")
        urllib.request.urlretrieve(category_url, category_path)
        
        with open(category_path, 'r') as f:
            categories = json.load(f)
        print(f"   ✅ Category data loaded from GitHub")
    except Exception as e:
        print(f"   ⚠️  GitHub download failed ({e}), using embedded fallback")
        categories = CATEGORY_JSON_FALLBACK
        # Save fallback to disk for reference
        with open(category_path, 'w') as f:
            json.dump(categories, f, indent=2)
        print(f"   ✅ Category data loaded from embedded fallback")
    
    if categories:
        print(f"   📋 Refined categories: {list(categories.keys())}")
        for cat_key, cat_data in categories.items():
            breakdown = cat_data.get('breakdown', {})
            total_items = sum(len(items) for items in breakdown.values())
            print(f"      {cat_key}: {len(breakdown)} subcategories, {total_items} total items")
    
    return categories


def generate_refineshot_from_shotbench(shotbench_samples, categories=None):
    """
    Generate RefineShot data by applying the refinement logic to ShotBench.
    
    RefineShot (https://github.com/wuhang03/RefineShot) refines only 3 categories:
    - "shot framing": options regrouped by subcategory (subject_count, detail, etc.)
    - "lighting type": options regrouped by subcategory (light_source, daylight_type, etc.)
    - "lighting condition": options regrouped by subcategory (direction, quality, etc.)
      (Note: ShotBench calls this "lighting condition", RefineShot calls it "lighting")
    
    For each refined question:
    - Find which subcategory the correct answer belongs to
    - If subcategory has 1 item → convert to binary yes/no question
    - If subcategory has 2+ items → replace options with all items in that subcategory
    - All other categories (shot size, camera angle, etc.) are kept unchanged
    """
    print("🔧 Generating RefineShot variant...")
    
    if not categories:
        print("   ⚠️  No category.json available, cannot generate RefineShot refinements")
        return None
    
    # Map ShotBench category names to RefineShot category.json keys
    # ShotBench uses "lighting" as the category name; RefineShot's category.json
    # also uses "lighting" for this dimension (lighting condition/quality)
    CATEGORY_MAP = {
        "shot framing": "shot framing",
        "lighting type": "lighting type",
        "lighting": "lighting",  # ShotBench calls this "lighting", not "lighting condition"
    }
    
    random.seed(42)  # Match RefineShot's seed for reproducibility
    
    refineshot_samples = []
    refined_count = 0
    binary_count = 0
    kept_count = 0
    skipped_count = 0
    
    for sample in shotbench_samples:
        cat = sample['category']
        refineshot_cat_key = CATEGORY_MAP.get(cat)
        
        # Categories not in the map are kept as-is
        if not refineshot_cat_key or refineshot_cat_key not in categories:
            refined = sample.copy()
            refined['source'] = 'refineshot'
            refined['refined'] = False
            refineshot_samples.append(refined)
            kept_count += 1
            continue
        
        # Get the correct answer text from the original options
        options = sample['options']
        answer_key = sample['answer']
        
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except:
                pass
        
        if not isinstance(options, dict) or answer_key not in options:
            # Can't parse, keep as-is
            refined = sample.copy()
            refined['source'] = 'refineshot'
            refined['refined'] = False
            refineshot_samples.append(refined)
            kept_count += 1
            continue
        
        answer_text = options[answer_key]
        
        # Skip multi-answer (comma-separated) items
        if ',' in answer_text:
            refined = sample.copy()
            refined['source'] = 'refineshot'
            refined['refined'] = False
            refineshot_samples.append(refined)
            kept_count += 1
            continue
        
        # Find which subcategory this answer belongs to
        breakdown = categories[refineshot_cat_key].get('breakdown', {})
        found_subcategory = None
        subcategory_items = []
        
        for subcat_name, items in breakdown.items():
            if answer_text in items:
                found_subcategory = subcat_name
                subcategory_items = items
                break
        
        if not found_subcategory:
            # Answer not found in any subcategory, keep as-is
            refined = sample.copy()
            refined['source'] = 'refineshot'
            refined['refined'] = False
            refineshot_samples.append(refined)
            skipped_count += 1
            continue
        
        refined = sample.copy()
        refined['source'] = 'refineshot'
        refined['refined'] = True
        refined['subcategory'] = found_subcategory
        
        if len(subcategory_items) == 1:
            # Binary question: "Is the X of this shot Y?"
            refined['question'] = f"Is the {cat} of this shot {answer_text}?"
            # Shuffle yes/no
            yes_no = ["yes", "no"]
            random.shuffle(yes_no)
            new_options = {}
            new_answer = None
            for i, item in enumerate(yes_no):
                letter = chr(65 + i)  # A, B
                new_options[letter] = item
                if item == "yes":
                    new_answer = letter
            refined['options'] = new_options
            refined['answer'] = new_answer
            binary_count += 1
        else:
            # Multi-choice: create options from all subcategory items
            shuffled = subcategory_items[:]
            random.shuffle(shuffled)
            new_options = {}
            new_answer = None
            for i, item in enumerate(shuffled):
                if i >= 10:  # max 10 options (A-J)
                    break
                letter = chr(65 + i)
                new_options[letter] = item
                if item == answer_text:
                    new_answer = letter
            refined['options'] = new_options
            refined['answer'] = new_answer
            refined_count += 1
        
        refineshot_samples.append(refined)
    
    output_path = DATA_DIR / "refineshot.json"
    with open(output_path, 'w') as f:
        json.dump(refineshot_samples, f, indent=2)
    
    total_modified = refined_count + binary_count
    print(f"   💾 Saved {len(refineshot_samples)} samples to {output_path}")
    print(f"      ✏️  Modified: {total_modified} ({refined_count} multi-choice + {binary_count} binary)")
    print(f"      ➡️  Unchanged: {kept_count}")
    if skipped_count:
        print(f"      ⚠️  Answer not in taxonomy: {skipped_count}")
    
    return refineshot_samples


def download_media(shotbench_samples, modality_filter=None):
    """Download media files (images/videos) from ShotBench HuggingFace repo.
    
    The ShotBench HuggingFace repo contains images.tar and videos.tar archives.
    We download these and extract them to the media directory.
    After extraction, files are at media/image/*.jpg and media/video/*.mp4
    matching the 'path' field in the metadata (e.g. 'image/YWE9AAUK.jpg').
    """
    print("\n📥 Downloading media files from HuggingFace...")
    
    try:
        from huggingface_hub import hf_hub_download
        import shutil
        import tarfile
    except ImportError:
        print("   ❌ huggingface_hub not installed. Run: pip install huggingface_hub")
        return
    
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Determine which archives to download based on modality filter
    archives = []
    if not modality_filter or modality_filter == 'image':
        archives.append(('images.tar', 'image'))
    if not modality_filter or modality_filter == 'video':
        archives.append(('videos.tar', 'video'))
    
    for tar_name, modality in archives:
        target_dir = MEDIA_DIR / modality
        
        # Check if already extracted
        if target_dir.exists() and any(target_dir.iterdir()):
            existing = list(target_dir.iterdir())
            print(f"   ⏭  {modality}/ already exists ({len(existing)} files), skipping {tar_name}")
            continue
        
        print(f"   📦 Downloading {tar_name}...")
        try:
            tar_path = hf_hub_download(
                repo_id=SHOTBENCH_REPO,
                filename=tar_name,
                repo_type="dataset",
                cache_dir="/tmp/hf_cache"
            )
            print(f"   ✅ Downloaded {tar_name}")
            
            # Extract to media directory
            print(f"   📂 Extracting {tar_name}...")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            with tarfile.open(tar_path, 'r') as tf:
                # Get member list for progress
                members = tf.getmembers()
                print(f"      {len(members)} files in archive")
                
                # Extract all files
                for i, member in enumerate(members):
                    if member.isfile():
                        # Extract to media/ directory
                        # The tar might contain paths like "image/ABC.jpg" or just "ABC.jpg"
                        # We need to handle both cases
                        tf.extract(member, MEDIA_DIR)
                    
                    if (i + 1) % 500 == 0:
                        print(f"      [{(i+1)/len(members)*100:5.1f}%] Extracted {i+1}/{len(members)}")
            
            # Check if extraction created the expected directory structure
            # If files were extracted to media/image/ great. If to media/ directly, 
            # we may need to move them
            if not target_dir.exists() or not any(target_dir.iterdir()):
                # Files might have been extracted with a different structure
                # Look for files directly in MEDIA_DIR
                media_files = [f for f in MEDIA_DIR.iterdir() 
                              if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov')]
                if media_files:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    for f in media_files:
                        shutil.move(str(f), str(target_dir / f.name))
                    print(f"      Moved {len(media_files)} files to {target_dir}/")
            
            extracted = list(target_dir.rglob('*')) if target_dir.exists() else []
            file_count = sum(1 for f in extracted if f.is_file())
            print(f"   ✅ Extracted {file_count} {modality} files")
            
        except Exception as e:
            print(f"   ❌ Failed to download/extract {tar_name}: {e}")
            print(f"      You can manually download with:")
            print(f"      huggingface-cli download --repo-type dataset Vchitect/ShotBench {tar_name}")
            print(f"      Then extract: tar -xvf {tar_name} -C {MEDIA_DIR}")
    
    # Show disk usage
    if MEDIA_DIR.exists():
        total_size = sum(f.stat().st_size for f in MEDIA_DIR.rglob('*') if f.is_file())
        total_files = sum(1 for f in MEDIA_DIR.rglob('*') if f.is_file())
        print(f"\n   📊 Media directory:")
        print(f"      📁 Files: {total_files}")
        print(f"      💾 Total size: {total_size / (1024*1024):.1f} MB")
    
    # Verify paths match
    if shotbench_samples:
        sample_path = shotbench_samples[0]['path']
        expected = MEDIA_DIR / sample_path
        if expected.exists():
            print(f"   ✅ Path verification OK: {sample_path} found")
        else:
            print(f"   ⚠️  Path verification: {sample_path} not found at {expected}")
            print(f"      Check that tar extraction created the expected directory structure")
            # Try to diagnose
            for d in MEDIA_DIR.iterdir():
                if d.is_dir():
                    count = sum(1 for _ in d.rglob('*') if _.is_file())
                    print(f"      Found: {d.name}/ ({count} files)")


def print_stats(samples):
    """Print dataset statistics."""
    from collections import Counter
    
    type_counts = Counter(s['type'] for s in samples)
    cat_counts = Counter(s['category'] for s in samples)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(samples)}")
    print(f"\n   By modality:")
    for t, c in sorted(type_counts.items()):
        print(f"      {t}: {c}")
    print(f"\n   By category:")
    for cat, c in sorted(cat_counts.items()):
        print(f"      {cat}: {c}")
    
    # Cross-tabulation
    print(f"\n   Modality × Category:")
    cross = Counter((s['type'], s['category']) for s in samples)
    for (t, cat), c in sorted(cross.items()):
        print(f"      {t} × {cat}: {c}")


def main():
    parser = argparse.ArgumentParser(description="Download ShotBench and RefineShot data + media")
    parser.add_argument("--metadata-only", action="store_true", help="Only download metadata, skip media files")
    parser.add_argument("--modality", type=str, choices=["image", "video"], default=None,
                        help="Only download media for this modality (images.tar or videos.tar)")
    parser.add_argument("--stats-only", action="store_true", help="Only show stats from existing data")
    args = parser.parse_args()
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🎬 ShotBench & RefineShot Data Downloader")
    print("=" * 70)
    
    if args.stats_only:
        shotbench_path = DATA_DIR / "shotbench.json"
        if shotbench_path.exists():
            with open(shotbench_path) as f:
                samples = json.load(f)
            print_stats(samples)
            
            # Show media on disk
            if MEDIA_DIR.exists():
                img_count = len(list((MEDIA_DIR / "image").glob("*"))) if (MEDIA_DIR / "image").exists() else 0
                vid_count = len(list((MEDIA_DIR / "video").glob("*"))) if (MEDIA_DIR / "video").exists() else 0
                print(f"\n   Downloaded media on disk:")
                print(f"      🖼 Images: {img_count}")
                print(f"      🎬 Videos: {vid_count}")
        else:
            print("❌ No data found. Run without --stats-only first.")
        return
    
    # Step 1: Download ShotBench
    shotbench_samples = download_shotbench()
    if shotbench_samples:
        print_stats(shotbench_samples)
    else:
        print("\n❌ Failed to download ShotBench. Exiting.")
        return
    
    # Step 2: Download RefineShot
    categories = download_refineshot()
    if categories and shotbench_samples:
        generate_refineshot_from_shotbench(shotbench_samples, categories)
    
    # Step 3: Download media (default behavior!)
    if not args.metadata_only:
        download_media(shotbench_samples, modality_filter=args.modality)
    else:
        print("\n⏭  Skipping media download (--metadata-only)")
        print("   Run without --metadata-only to download images/videos")
    
    print("\n" + "=" * 70)
    print("✅ Download complete!")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"  1. Run the server:  python server.py")
    print(f"  2. Open browser:    http://localhost:8080")
    if args.metadata_only:
        print(f"\n  💡 Media not downloaded yet. Run again without --metadata-only")
        print(f"     Images will load from HuggingFace directly (slower)")


if __name__ == "__main__":
    main()