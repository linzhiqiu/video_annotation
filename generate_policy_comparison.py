#!/usr/bin/env python3
"""
Policy Comparison Generator

This script generates a markdown file that compares three different versions of policies
for each of the 5 main policy classes:
1. Version from get_prompt_without_video_info() method
2. Content from the human-readable policy file  
3. First paragraph of the human-readable policy

Usage:
    python generate_policy_comparison.py [--output output.md]
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add the project root to the path so we can import from caption_policy
script_dir = Path(__file__).resolve().parent

# Try to find the correct project root by looking for the caption_policy directory
# Start from current directory and look up the tree
current_dir = Path.cwd()
project_root = None

# First try the current directory and its parents
for potential_root in [current_dir] + list(current_dir.parents):
    if (potential_root / "caption_policy").exists():
        project_root = potential_root
        break

# If not found, try looking for a caption directory in current dir or parents
if project_root is None:
    for potential_root in [current_dir] + list(current_dir.parents):
        if (potential_root / "caption" / "human").exists():
            project_root = potential_root
            break

# If still not found, try some common relative paths
if project_root is None:
    potential_paths = [
        current_dir / "..",  # parent directory
        script_dir,          # where the script is located
        script_dir / "..",   # parent of script directory
    ]
    
    for potential_root in potential_paths:
        potential_root = potential_root.resolve()
        if (potential_root / "caption_policy").exists() or (potential_root / "caption" / "human").exists():
            project_root = potential_root
            break

# Fallback to script directory
if project_root is None:
    project_root = script_dir.parent if script_dir.name == 'caption' else script_dir

print(f"Detected project root: {project_root}")
print(f"Looking for caption_policy at: {project_root / 'caption_policy'}")
print(f"Looking for human files at: {project_root / 'caption' / 'human'}")

sys.path.insert(0, str(project_root))

try:
    from caption_policy.prompt_generator import (
        SubjectPolicy, ScenePolicy, SubjectMotionPolicy, 
        SpatialPolicy, CameraPolicy
    )
except ImportError as e:
    print(f"Error importing policy classes: {e}")
    print(f"Tried to import from: {project_root}")
    print("Make sure the caption_policy directory exists and contains prompt_generator.py")
    
    # Try to provide more helpful debugging info
    caption_policy_path = project_root / "caption_policy"
    print(f"caption_policy directory exists: {caption_policy_path.exists()}")
    if caption_policy_path.exists():
        print(f"Contents: {list(caption_policy_path.iterdir())}")
    
    sys.exit(1)


def read_file_safe(file_path):
    """Safely read a file, returning None if file doesn't exist"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}")
        return None


def get_first_paragraph(text):
    """Extract the first paragraph from text"""
    if not text:
        return None
    
    # Split by double newlines to get paragraphs
    paragraphs = text.strip().split('\n\n')
    if paragraphs:
        return paragraphs[0].strip()
    return text.strip()


def add_policy_version(markdown_content, version_name, content, source_info=None):
    """Add a policy version section with proper markdown and raw text formatting"""
    if not content:
        markdown_content.append(f"### {version_name}")
        markdown_content.append("")
        markdown_content.append("**Error**: No content available")
        markdown_content.append("")
        return
    
    markdown_content.append(f"### {version_name}")
    markdown_content.append("")
    
    if source_info:
        markdown_content.append(f"*Source: {source_info}*")
        markdown_content.append("")
    
    # Rendered markdown version (shows formatted text)
    markdown_content.append("**Rendered version:**")
    markdown_content.append("")
    markdown_content.append(content)  # This will render the markdown
    markdown_content.append("")
    
    # Raw text version for copy/paste (shows markdown source)
    markdown_content.append("<details>")
    markdown_content.append("<summary>📋 Raw markdown source for copy/paste</summary>")
    markdown_content.append("")
    markdown_content.append("```text")
    markdown_content.append(content)
    markdown_content.append("```")
    markdown_content.append("")
    markdown_content.append("</details>")
    markdown_content.append("")


def get_human_short_description(task_name):
    """Get the predefined human_short description for each task"""
    human_short_descriptions = {
        "subject_description": "Describe the main subjects in the video and their most distinctive traits.",
        "scene_composition_dynamics": "Describe the setting and environment of the video.",
        "spatial_framing_dynamics": "Describe how the subjects or elements are framed and how they move within the scene.",
        "subject_motion_dynamics": "Describe the main actions of the subjects in the video.",
        "camera_framing_dynamics": "Describe the camera's perspective, lens, speed, movement, and focus."
    }
    return human_short_descriptions.get(task_name, None)


def get_first_sentence(text):
    """Extract the first sentence from text"""
    if not text:
        return None
    
    # Split by periods, exclamation marks, or question marks followed by space or end
    import re
    sentences = re.split(r'[.!?]+(?:\s|$)', text.strip())
    if sentences and sentences[0].strip():
        # Add back the punctuation if it was removed
        first_sentence = sentences[0].strip()
        if not first_sentence.endswith(('.', '!', '?')):
            first_sentence += '.'
        return first_sentence
    return text.strip()
    """Extract the first sentence from text"""
    if not text:
        return None
    
    # Split by periods, exclamation marks, or question marks followed by space or end
    import re
    sentences = re.split(r'[.!?]+(?:\s|$)', text.strip())
    if sentences and sentences[0].strip():
        # Add back the punctuation if it was removed
        first_sentence = sentences[0].strip()
        if not first_sentence.endswith(('.', '!', '?')):
            first_sentence += '.'
        return first_sentence
    return text.strip()


def get_human_readable_file_path(task_name, human_dir):
    """Get the exact human-readable file path for a given task from the config files"""
    # These are the exact mappings from the config files used in apps.py
    task_to_human_file = {
        "subject_description": "subject_description.txt",
        "scene_composition_dynamics": "scene_composition_dynamics.txt", 
        "subject_motion_dynamics": "subject_motion_dynamics.txt",
        "spatial_framing_dynamics": "spatial_framing_dynamics.txt",
        "camera_framing_dynamics": "camera_framing_dynamics.txt"
    }
    
    if task_name in task_to_human_file:
        return human_dir / task_to_human_file[task_name]
    return None


def process_single_policy(policy_instance, task_name, display_name, human_dir):
    """Process a single policy and return all its versions"""
    print(f"Processing {display_name}...")
    
    # Get human-readable file
    human_file = get_human_readable_file_path(task_name, human_dir)
    human_content = None
    
    if human_file:
        print(f"Looking for: {human_file}")
        print(f"File exists: {human_file.exists()}")
        if human_file.exists():
            human_content = read_file_safe(human_file)
            if human_content:
                print(f"Successfully read {len(human_content)} characters from {human_file.name}")
            else:
                print(f"Failed to read content from {human_file.name}")
        else:
            print(f"File does not exist: {human_file}")
    else:
        print(f"No human file mapping for task: {task_name}")
    
    # Get method output
    method_output = None
    try:
        method_output = policy_instance.get_prompt_without_video_info()
        print(f"Successfully got method output ({len(method_output)} characters)")
    except Exception as e:
        print(f"Error getting method output: {e}")
    
    # Prepare versions
    versions = {}
    
    # Use predefined human_short description
    versions['human_short'] = get_human_short_description(task_name)
    
    if human_content:
        versions['human'] = get_first_paragraph(human_content)
        versions['human_detailed'] = human_content
        versions['human_detailed_source'] = f"`{human_file.relative_to(project_root)}`"
    else:
        versions['human'] = None
        versions['human_detailed'] = None
        versions['human_detailed_source'] = f"Error: Could not read {human_file}" if human_file else f"Error: No file mapping for {task_name}"
    
    versions['model_without_label'] = method_output
    
    return versions


def generate_policy_comparison():
    """Generate markdown comparison of all policy versions"""
    
    # Define the policy classes and their corresponding task names
    policy_classes = [
        (SubjectPolicy(), "subject_description", "Subject Description"),
        (ScenePolicy(), "scene_composition_dynamics", "Scene Composition & Dynamics"),
        (SubjectMotionPolicy(), "subject_motion_dynamics", "Subject Motion & Dynamics"),
        (SpatialPolicy(), "spatial_framing_dynamics", "Spatial Framing & Dynamics"),
        (CameraPolicy(), "camera_framing_dynamics", "Camera Framing & Dynamics")
    ]
    
    # Paths
    human_dir = project_root / "caption" / "human"
    print(f"Looking for human files in: {human_dir}")
    print(f"Human dir exists: {human_dir.exists()}")
    print("")
    
    # Build header
    markdown_content = []
    markdown_content.append("# Policy Comparison Report")
    markdown_content.append("")
    markdown_content.append("This document compares four different versions of policies for each of the 5 main policy classes:")
    markdown_content.append("")
    markdown_content.append("| Version | Description |")
    markdown_content.append("|---------|-------------|")
    markdown_content.append("| **human_short** | Task-specific single-sentence prompt for human annotators, capturing the essence of the description while omitting most details. |")
    markdown_content.append("| **human** | Task-specific multi-sentence prompt for human annotators with clear detail requirements. |")
    markdown_content.append("| **human_detailed** | Expanded human prompt with explicit sub-aspects (A, B, C, D, etc.) and definitions. |")
    markdown_content.append("| **model_without_label** | Model policy (agnostic to human-labeled ground truth). |")
    markdown_content.append("")
    markdown_content.append("---")
    markdown_content.append("")
    
    # Process each policy class
    for policy_instance, task_name, display_name in policy_classes:
        markdown_content.append(f"## {display_name}")
        markdown_content.append("")
        
        # Get all versions for this policy
        versions = process_single_policy(policy_instance, task_name, display_name, human_dir)
        
        # Add each version in the specified order
        add_policy_version(
            markdown_content, 
            "1. human_short", 
            versions['human_short']
        )
        
        add_policy_version(
            markdown_content, 
            "2. human", 
            versions['human']
        )
        
        add_policy_version(
            markdown_content, 
            "3. human_detailed", 
            versions['human_detailed'],
            versions['human_detailed_source']
        )
        
        add_policy_version(
            markdown_content, 
            "4. model_without_label", 
            versions['model_without_label']
        )
        
        markdown_content.append("---")
        markdown_content.append("")
    
    # Add footer
    markdown_content.append("## Summary")
    markdown_content.append("")
    markdown_content.append("This comparison was generated automatically to help understand the different ")
    markdown_content.append("versions of policy text used throughout the system.")
    markdown_content.append("")
    markdown_content.append(f"**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    markdown_content.append("")
    
    return '\n'.join(markdown_content)


def main():
    parser = argparse.ArgumentParser(description="Generate policy comparison markdown")
    parser.add_argument(
        "--output", 
        type=str, 
        default="policy_comparison.md",
        help="Output markdown file path (default: policy_comparison.md)"
    )
    
    args = parser.parse_args()
    
    print("Generating policy comparison...")
    print(f"Project root: {project_root}")
    
    try:
        markdown_content = generate_policy_comparison()
        
        # Write to file
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Policy comparison generated successfully!")
        print(f"📄 Output saved to: {output_path.resolve()}")
        
    except Exception as e:
        print(f"❌ Error generating policy comparison: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()