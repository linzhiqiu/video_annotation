#!/usr/bin/env python3
"""
Script to extract default prompts and JSON keys for each task.
This helps understand the structure before creating the caption-to-JSON API.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

# Import caption policy programs
from caption_policy.prompt_generator import (
    SubjectPolicy, ScenePolicy, SubjectMotionPolicy, 
    SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, 
    RawSpatialPolicy, RawSubjectMotionPolicy
)


# Task name mappings
TASK_FULL_TO_SHORT = {
    "subject_description": "subject",
    "scene_composition_dynamics": "scene",
    "subject_motion_dynamics": "motion",
    "spatial_framing_dynamics": "spatial",
    "camera_framing_dynamics": "camera",
    "color_composition_dynamics": "color",
    "lighting_setup_dynamics": "lighting",
    "lighting_effects_dynamics": "effects"
}

TASK_SHORT_TO_FULL = {v: k for k, v in TASK_FULL_TO_SHORT.items()}


def get_root_path() -> Path:
    """Get the project root path"""
    # This script should be run from project root or caption/ directory
    current = Path(__file__).parent
    if (current / "json_policy").exists():
        return current
    elif (current.parent / "json_policy").exists():
        return current.parent
    else:
        # Assume current working directory
        return Path.cwd()


def load_json_policy(root_path: Path) -> Dict[str, Any]:
    """Load the JSON policy file"""
    json_policy_path = root_path / "json_policy" / "json_policy.json"
    if json_policy_path.exists():
        with open(json_policy_path, 'r') as f:
            return json.load(f)
    return {}


def get_caption_programs() -> Dict[str, Any]:
    """Get caption policy programs for each task"""
    return {
        "subject_description": SubjectPolicy(),
        "scene_composition_dynamics": ScenePolicy(),
        "subject_motion_dynamics": SubjectMotionPolicy(),
        "spatial_framing_dynamics": SpatialPolicy(),
        "camera_framing_dynamics": CameraPolicy(),
    }


def extract_json_keys_recursive(obj: Any, prefix: str = "") -> List[str]:
    """
    Recursively extract all keys from a JSON structure.
    Returns flat list of keys with dot notation for nested keys.
    """
    keys = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.append(full_key)
            # Recursively get nested keys
            nested_keys = extract_json_keys_recursive(value, full_key)
            keys.extend(nested_keys)
    elif isinstance(obj, list) and len(obj) > 0:
        # For arrays, check the first element's structure
        nested_keys = extract_json_keys_recursive(obj[0], f"{prefix}[]")
        keys.extend(nested_keys)
    
    return keys


def extract_top_level_keys(obj: Any) -> List[str]:
    """Extract only top-level keys from JSON structure"""
    if isinstance(obj, dict):
        return list(obj.keys())
    return []


def get_json_policy_for_task(json_policy: Dict[str, Any], task: str) -> Dict[str, Any]:
    """Get the JSON policy structure for a specific task"""
    short_name = TASK_FULL_TO_SHORT.get(task, task)
    
    if short_name in json_policy:
        return json_policy[short_name]
    elif task in json_policy:
        return json_policy[task]
    return {}


def get_caption_instruction_for_task(task: str, caption_programs: Dict[str, Any]) -> str:
    """Get the caption instruction for a task"""
    if task in caption_programs:
        return caption_programs[task].get_prompt_without_video_info()
    return f"Please provide a detailed caption for {task.replace('_', ' ')}."


def get_templates_dir(root_path: Path, task: str) -> Path:
    """Get the templates directory for a task"""
    short_name = TASK_FULL_TO_SHORT.get(task, task)
    return root_path / "json_policy" / "templates" / short_name


def get_default_template(root_path: Path, task: str, json_policy: Dict[str, Any], caption_instruction: str) -> str:
    """Get the default template for a task (checks for custom default first)"""
    templates_dir = get_templates_dir(root_path, task)
    default_ref_file = templates_dir / "default.txt"
    
    # Check for custom default reference
    if default_ref_file.exists():
        with open(default_ref_file, 'r') as f:
            ref_name = f.read().strip()
        template_path = templates_dir / f"{ref_name}.txt"
        if template_path.exists():
            with open(template_path, 'r') as f:
                return f.read()
    
    # Fall back to code-generated default
    return get_code_generated_template(task, json_policy, caption_instruction)


def get_code_generated_template(task: str, json_policy: Dict[str, Any], caption_instruction: str) -> str:
    """Get the code-generated default template for a task"""
    short_name = TASK_FULL_TO_SHORT.get(task, task)
    
    if json_policy:
        json_prompt_str = json.dumps(json_policy, indent=2)
    else:
        json_prompt_str = "Please use an appropriate JSON structure for this type of caption."
    
    base_template = f"""Please convert the following caption into the JSON format shown below:

{json_prompt_str}

Caption Instruction:
{caption_instruction}

Caption: {{caption}}

Instructions:
1. Use the exact same JSON keys as shown above
2. Preserve all important information from the caption with all the keywords and details
3. Organize the information appropriately under each key
4. If the caption doesn't contain some information, please review the caption instruction above to determine what should be the input
5. It is okay to leave fields blank as "" if nothing is mentioned in the caption
6. Return only valid JSON without any additional text"""
    
    if short_name == "camera":
        return base_template + """
7. No period after each caption"""
    elif short_name == "subject":
        return base_template + """
7. No period after each caption
8. Don't mention any detail of "wardrobe" and "appearance" in "type". Only mention each subject in short.
9. Don't mention any detail of "wardrobe" in "appearance". Only mention each subject in short."""
    elif short_name == "motion":
        return base_template + """
7. No period after each caption
8. Mention only subject action in "subject_action". Avoid mentioning camera related details"""
    else:
        return base_template


def extract_json_keys_from_template(template: str) -> List[str]:
    """Extract JSON keys from the template by parsing the embedded JSON structure"""
    # Try to find a JSON object in the template
    # Look for the pattern starting with { and ending with } that forms valid JSON
    
    # First, find the first { that looks like start of JSON (has a " after it for a key)
    start_idx = -1
    for i, char in enumerate(template):
        if char == '{':
            # Check if this looks like JSON start (has a key after it)
            rest = template[i:i+50]
            if '"' in rest:
                start_idx = i
                break
    
    if start_idx == -1:
        return []
    
    # Now find the matching closing brace
    brace_count = 0
    end_idx = -1
    in_string = False
    escape_next = False
    
    for i in range(start_idx, len(template)):
        char = template[i]
        
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if in_string:
            continue
        
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i
                break
    
    if end_idx == -1:
        return []
    
    json_str = template[start_idx:end_idx + 1]
    
    try:
        parsed = json.loads(json_str)
        return extract_top_level_keys(parsed)
    except json.JSONDecodeError as e:
        # Try to clean up common issues
        # Sometimes there are trailing commas
        json_str_clean = re.sub(r',\s*}', '}', json_str)
        json_str_clean = re.sub(r',\s*]', ']', json_str_clean)
        try:
            parsed = json.loads(json_str_clean)
            return extract_top_level_keys(parsed)
        except json.JSONDecodeError:
            pass
    
    return []


def main():
    root_path = get_root_path()
    print(f"Project root: {root_path}")
    print("=" * 80)
    
    # Load JSON policy
    json_policy = load_json_policy(root_path)
    if not json_policy:
        print("WARNING: Could not load json_policy.json")
    else:
        print(f"Loaded JSON policy with keys: {list(json_policy.keys())}")
    
    # Get caption programs
    caption_programs = get_caption_programs()
    
    print("\n" + "=" * 80)
    print("TASK INFORMATION")
    print("=" * 80)
    
    all_task_info = {}
    
    for task_full, task_short in TASK_FULL_TO_SHORT.items():
        print(f"\n{'─' * 80}")
        print(f"TASK: {task_short} ({task_full})")
        print(f"{'─' * 80}")
        
        # Get JSON policy for this task
        task_json_policy = get_json_policy_for_task(json_policy, task_full)
        
        # Get caption instruction
        if task_full in caption_programs:
            caption_instruction = get_caption_instruction_for_task(task_full, caption_programs)
        else:
            caption_instruction = f"Please provide a detailed caption for {task_full.replace('_', ' ')}."
        
        # Get JSON keys from policy
        json_keys = extract_top_level_keys(task_json_policy)
        
        # Get default template
        default_template = get_default_template(root_path, task_full, task_json_policy, caption_instruction)
        
        # Check if using custom default
        templates_dir = get_templates_dir(root_path, task_full)
        default_ref_file = templates_dir / "default.txt"
        using_custom = default_ref_file.exists()
        custom_name = None
        if using_custom:
            with open(default_ref_file, 'r') as f:
                custom_name = f.read().strip()
        
        # Extract keys from template (in case they differ from json_policy)
        template_keys = extract_json_keys_from_template(default_template)
        
        print(f"\n📋 JSON Keys (from json_policy.json):")
        if json_keys:
            for key in json_keys:
                print(f"   - {key}")
        else:
            print("   (No keys found in json_policy.json for this task)")
        
        print(f"\n📋 JSON Keys (extracted from template):")
        if template_keys:
            for key in template_keys:
                print(f"   - {key}")
            # Compare with json_policy keys
            if json_keys:
                if set(json_keys) == set(template_keys):
                    print("   ✅ Keys match json_policy.json")
                else:
                    missing_in_template = set(json_keys) - set(template_keys)
                    extra_in_template = set(template_keys) - set(json_keys)
                    if missing_in_template:
                        print(f"   ⚠️ Missing from template: {missing_in_template}")
                    if extra_in_template:
                        print(f"   ⚠️ Extra in template: {extra_in_template}")
        else:
            print("   (Could not extract keys from template)")
        
        print(f"\n📄 Default Template Source:")
        if using_custom:
            print(f"   Custom default → {custom_name}")
        else:
            print(f"   Code-generated default")
        
        print(f"\n📄 Default Template Preview (first 500 chars):")
        print("   " + default_template[:500].replace('\n', '\n   ') + "...")
        
        # Store info
        all_task_info[task_short] = {
            "task_full": task_full,
            "task_short": task_short,
            "json_keys": json_keys if json_keys else template_keys,
            "json_policy": task_json_policy,
            "caption_instruction": caption_instruction[:200] + "..." if len(caption_instruction) > 200 else caption_instruction,
            "default_template": default_template,
            "using_custom_default": using_custom,
            "custom_default_name": custom_name
        }
    
    # Save summary to JSON file
    summary_path = root_path / "json_policy" / "task_info_summary.json"
    summary_data = {}
    for task_short, info in all_task_info.items():
        summary_data[task_short] = {
            "task_full": info["task_full"],
            "json_keys": info["json_keys"],
            "json_policy": info["json_policy"],
            "using_custom_default": info["using_custom_default"],
            "custom_default_name": info["custom_default_name"]
        }
    
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"\n\n{'=' * 80}")
    print(f"Summary saved to: {summary_path}")
    print("=" * 80)
    
    # Print compact summary
    print("\n\nCOMPACT SUMMARY OF JSON KEYS PER TASK:")
    print("=" * 80)
    for task_short, info in all_task_info.items():
        keys = info["json_keys"]
        print(f"\n{task_short}: {keys}")


if __name__ == "__main__":
    main()