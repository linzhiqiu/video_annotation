#!/usr/bin/env python3
"""
Extract Final Captions Script

Extracts final captions (approved or rejected) from all reviewed videos and saves them
to separate text files for each caption type.

Usage:
    python extract_final_captions.py --config-type main
    python extract_final_captions.py --output-dir caption/final_captions
"""

import argparse
import os
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
from tqdm import tqdm

# Import from caption system
from caption.config import get_config
from caption.core.data_manager import DataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Extract Final Captions")
    parser.add_argument("--config-type", type=str, default="main", 
                       choices=["main", "lighting"],
                       help="Configuration type to use")
    parser.add_argument("--output-dir", type=str, default="caption/final_captions",
                       help="Output directory for caption text files")
    return parser.parse_args()


class CaptionExtractor:
    """Extract final captions from reviewed videos"""
    
    # Task name mapping
    TASK_NAME_MAP = {
        "subject_description": "Subject",
        "scene_composition_dynamics": "Scene",
        "subject_motion_dynamics": "Motion",
        "spatial_framing_dynamics": "Spatial",
        "camera_framing_dynamics": "Camera",
    }
    
    def __init__(self, args):
        self.args = args
        self.app_config = get_config(args.config_type)
        
        # Set up paths - detect if running from root or from script location
        script_path = Path(__file__).resolve()
        
        # If script is in root directory (video_annotation/)
        if script_path.parent.name == "video_annotation" or (script_path.parent / "caption").exists():
            self.root_path = script_path.parent
        # If script is somewhere else, try to find caption directory
        else:
            # Try current working directory
            cwd = Path.cwd()
            if (cwd / "caption").exists():
                self.root_path = cwd
            else:
                raise ValueError(f"Cannot locate project root. Script at: {script_path}, CWD: {cwd}")
        
        self.folder_path = self.root_path / "caption"
        
        # Verify caption directory exists
        if not self.folder_path.exists():
            raise ValueError(f"Caption directory not found at: {self.folder_path}")
        
        print(f"Root path: {self.root_path}")
        print(f"Caption folder: {self.folder_path}")
        
        self.output_dir = self.root_path / args.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data manager
        self.data_manager = DataManager(self.folder_path, self.root_path)
        
        # Statistics
        self.stats = {
            "total_videos_scanned": 0,
            "videos_with_all_5_captions": 0,
            "captions_by_type": defaultdict(int),
            "captions_by_status": defaultdict(lambda: defaultdict(int))
        }
    
    def get_all_reviewed_videos(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all videos that have been reviewed (approved or rejected) for each task.
        Returns a dict mapping task names to lists of caption data.
        """
        captions_by_task = defaultdict(list)
        
        # Load configs
        configs = self.data_manager.load_config(self.app_config.configs_file)
        if isinstance(configs[0], str):
            configs = [self.data_manager.load_config(config) for config in configs]
        
        print("Loading reviewed videos...")
        
        # Track videos that have all 5 captions
        videos_with_all_captions = set()
        video_caption_counts = defaultdict(int)
        
        # Check all video URL files
        for video_urls_file in tqdm(self.app_config.video_urls_files, desc="Scanning video files"):
            try:
                video_urls = self.data_manager.load_json(video_urls_file)
                sheet_name = Path(video_urls_file).stem
                
                for video_url in video_urls:
                    self.stats["total_videos_scanned"] += 1
                    video_id = self.data_manager.get_video_id(video_url)
                    
                    # Check each task for this video
                    video_has_all = True
                    
                    for config in configs:
                        config_output_dir = os.path.join(
                            str(self.folder_path),
                            self.app_config.output_dir, 
                            config["output_name"]
                        )
                        
                        # Get video status
                        status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                            video_id, config_output_dir
                        )
                        
                        # Only "approved" and "rejected" count as reviewed
                        if status in ["approved", "rejected"]:
                            # Load feedback data to get final caption
                            feedback_data = self.data_manager.load_data(
                                video_id, config_output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX
                            )
                            
                            if feedback_data and feedback_data.get("final_caption"):
                                task_name = config["task"]
                                short_name = self.TASK_NAME_MAP.get(task_name, task_name)
                                
                                captions_by_task[short_name].append({
                                    "video_id": video_id,
                                    "video_url": video_url,
                                    "sheet_name": sheet_name,
                                    "caption": feedback_data["final_caption"],
                                    "status": status,
                                    "task": task_name
                                })
                                
                                self.stats["captions_by_type"][short_name] += 1
                                self.stats["captions_by_status"][short_name][status] += 1
                                video_caption_counts[video_id] += 1
                            else:
                                video_has_all = False
                        else:
                            video_has_all = False
                    
                    # Check if this video has all 5 captions
                    if video_caption_counts[video_id] == 5:
                        videos_with_all_captions.add(video_id)
            
            except Exception as e:
                print(f"Warning: Error processing {video_urls_file}: {e}")
                continue
        
        self.stats["videos_with_all_5_captions"] = len(videos_with_all_captions)
        
        return captions_by_task
    
    def save_captions_to_files(self, captions_by_task: Dict[str, List[Dict[str, Any]]]):
        """Save captions to separate text files for each task"""
        print("\nSaving captions to text files...")
        
        for task_name in ["Subject", "Scene", "Motion", "Spatial", "Camera"]:
            if task_name not in captions_by_task:
                print(f"  ⚠️  No captions found for {task_name}")
                continue
            
            captions = captions_by_task[task_name]
            output_path = self.output_dir / f"{task_name.lower()}_captions.txt"
            
            # Sort by video_id for consistency
            captions.sort(key=lambda x: x["video_id"])
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                for caption_data in captions:
                    # Write just the caption text, one per line
                    f.write(caption_data["caption"] + "\n")
            
            print(f"  ✓ Saved {len(captions)} captions to {output_path.name}")
    
    def print_statistics(self):
        """Print comprehensive statistics"""
        print("\n" + "="*80)
        print("EXTRACTION SUMMARY")
        print("="*80)
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total videos scanned: {self.stats['total_videos_scanned']}")
        print(f"  Videos with all 5 captions: {self.stats['videos_with_all_5_captions']}")
        
        print(f"\n📝 Captions by Type:")
        for task_name in ["Subject", "Scene", "Motion", "Spatial", "Camera"]:
            count = self.stats['captions_by_type'][task_name]
            print(f"  {task_name:8s}: {count:5d} captions")
        
        print(f"\n✅ Captions by Status:")
        for task_name in ["Subject", "Scene", "Motion", "Spatial", "Camera"]:
            approved = self.stats['captions_by_status'][task_name]['approved']
            rejected = self.stats['captions_by_status'][task_name]['rejected']
            total = approved + rejected
            if total > 0:
                print(f"  {task_name:8s}: {approved:4d} approved, {rejected:4d} rejected "
                      f"({approved/total*100:.1f}% approval rate)")
        
        print("\n" + "="*80 + "\n")
    
    def run(self):
        """Main execution"""
        print("\n" + "="*80)
        print("FINAL CAPTION EXTRACTION")
        print("="*80)
        print(f"Config: {self.args.config_type}")
        print(f"Output directory: {self.output_dir}")
        print("="*80 + "\n")
        
        # Get all reviewed captions
        captions_by_task = self.get_all_reviewed_videos()
        
        if not any(captions_by_task.values()):
            print("No reviewed captions found.")
            return
        
        # Save to files
        self.save_captions_to_files(captions_by_task)
        
        # Print statistics
        self.print_statistics()
        
        print(f"✓ Caption files saved to: {self.output_dir}")
        print()


if __name__ == "__main__":
    args = parse_args()
    extractor = CaptionExtractor(args)
    extractor.run()