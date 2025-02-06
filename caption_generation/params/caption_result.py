from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime
from caption_data import CaptionType

@dataclass
class CaptionResult:
    """Result of generating a single caption."""
    caption_type: CaptionType
    model_name: str
    instruction_template: str
    final_instruction: str
    output_caption: str
    timestamp: str
    model_params: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'caption_type': self.caption_type.name,
            'model_name': self.model_name,
            'instruction_template': self.instruction_template,
            'final_instruction': self.final_instruction,
            'output_caption': self.output_caption,
            'timestamp': self.timestamp,
            'model_params': self.model_params
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CaptionResult':
        """Create from dictionary format."""
        return cls(
            caption_type=CaptionType[data['caption_type']],
            model_name=data['model_name'],
            instruction_template=data['instruction_template'],
            final_instruction=data['final_instruction'],
            output_caption=data['output_caption'],
            timestamp=data['timestamp'],
            model_params=data['model_params']
        )

class VideoCaptionResults:
    """Collection of caption results for a single video."""
    
    def __init__(self, video_name: str):
        """Initialize with video name."""
        self.video_name = video_name
        self.captions: Dict[CaptionType, CaptionResult] = {}
        self.timestamp = datetime.now().isoformat()
    
    def add_caption(self, result: CaptionResult) -> None:
        """Add a caption result."""
        self.captions[result.caption_type] = result
    
    def get_caption(self, caption_type: CaptionType) -> Optional[CaptionResult]:
        """Get a specific caption result."""
        return self.captions.get(caption_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'video_name': self.video_name,
            'timestamp': self.timestamp,
            'captions': {
                caption_type.name: result.to_dict()
                for caption_type, result in self.captions.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VideoCaptionResults':
        """Create from dictionary format."""
        instance = cls(data['video_name'])
        instance.timestamp = data['timestamp']
        
        for caption_type_str, result_data in data['captions'].items():
            caption_type = CaptionType[caption_type_str]
            result = CaptionResult.from_dict(result_data)
            instance.captions[caption_type] = result
            
        return instance 