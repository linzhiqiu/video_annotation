from typing import Dict, List, Any, Optional
import os
import json
import yaml
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from video_data import VideoData
from caption_data import CaptionType, CaptionMetadata

class ModelType(Enum):
    """Available models for caption generation."""
    TARSIER_7B = "Tarsier-7b"
    TARSIER_35B = "Tarsier-35b"
    GEMINI_2_FLASH = "Gemini 2.0 Flash"

@dataclass
class CaptionRule:
    """Rule for generating a specific type of caption."""
    caption_type: CaptionType
    model: ModelType
    instruction_path: str
    additional_params: Optional[Dict[str, Any]] = None

class CaptionGenerator:
    """Class for generating captions based on rules."""
    
    def __init__(self, rules: List[CaptionRule]):
        """Initialize with a list of caption rules.
        
        Args:
            rules: List of CaptionRule objects defining how to generate each caption
        """
        self.rules = rules
        self._load_instructions()
    
    def _load_instructions(self):
        """Load instruction templates for each rule."""
        self.instructions = {}
        for rule in self.rules:
            try:
                with open(rule.instruction_path, 'r') as f:
                    self.instructions[rule.caption_type] = json.load(f)
            except Exception as e:
                print(f"Error loading instructions for {rule.caption_type}: {str(e)}")
    
    def _generate_caption(self, video: VideoData, rule: CaptionRule) -> tuple[str, CaptionMetadata]:
        """Generate a caption for a video using the specified rule.
        
        Args:
            video: VideoData object containing video information
            rule: CaptionRule specifying how to generate the caption
            
        Returns:
            Tuple of (caption text, caption metadata)
        """
        # Get instruction template
        instruction_data = self.instructions.get(rule.caption_type)
        if not instruction_data:
            raise ValueError(f"No instructions found for {rule.caption_type}")
        
        # TODO: Implement actual caption generation using the specified model
        # For now, return placeholder
        caption = "Placeholder caption"
        
        # Create metadata
        metadata = CaptionMetadata(
            model=rule.model.value,
            prompt=instruction_data["instruction_template"],
            timestamp=datetime.now().isoformat(),
            additional_info=rule.additional_params
        )
        
        return caption, metadata
    
    def generate_captions(self, video: VideoData) -> None:
        """Generate all captions for a video according to the rules.
        
        Args:
            video: VideoData object to generate captions for
        """
        for rule in self.rules:
            try:
                caption, metadata = self._generate_caption(video, rule)
                video.caption_data.set_caption(rule.caption_type, caption, metadata)
            except Exception as e:
                print(f"Error generating caption for {rule.caption_type}: {str(e)}")
                continue

    @classmethod
    def from_config(cls, config_path: str) -> 'CaptionGenerator':
        """Create a CaptionGenerator from a configuration file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            New CaptionGenerator instance
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        rules = []
        for rule_config in config.get('rules', []):
            try:
                caption_type = CaptionType[rule_config['caption_type'].upper()]
                model = ModelType[rule_config['model'].upper().replace('.', '_')]
                rule = CaptionRule(
                    caption_type=caption_type,
                    model=model,
                    instruction_path=rule_config['instruction_path'],
                    additional_params=rule_config.get('additional_params')
                )
                rules.append(rule)
            except (KeyError, ValueError) as e:
                print(f"Error processing rule config: {str(e)}")
                continue
                
        return cls(rules) 