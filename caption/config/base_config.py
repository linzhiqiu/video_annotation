# caption/config/base_config.py
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

@dataclass
class AppConfig:
    """Base configuration class for video annotation apps"""
    name: str
    configs_file: str
    video_urls_files: List[str]
    video_data_file: str
    label_collections: List[str]
    caption_programs: Dict[str, Any]
    output_dir: str = "output_captions"
    main_project_output: str = "output_captions"
    feedback_prompt: str = "prompts/feedback_prompt.txt"
    caption_prompt: str = "prompts/caption_prompt.txt"
    diff_prompt: str = "prompts/diff_prompt.txt"
    diff_cap_prompt: str = "prompts/diff_cap_prompt.txt"
    show_feedback_prompt: bool = False
    personalize_output: bool = False

def get_config(config_type: str) -> AppConfig:
    """Factory function to get configuration based on type"""
    if config_type == "main":
        from .main_config import get_main_config
        return get_main_config()
    elif config_type == "lighting":
        from .lighting_config import get_lighting_config
        return get_lighting_config()
    else:
        raise ValueError(f"Unknown config type: {config_type}")