from abc import ABC, abstractmethod
from typing import List, Dict, Any, NamedTuple
from dataclasses import dataclass

@dataclass
class CaptionInput:
    """Input for caption generation."""
    video_name: str
    instruction: str
    model_params: Dict[str, Any]
    videos_dir: str

@dataclass
class CaptionOutput:
    """Output from caption generation."""
    video_name: str
    instruction: str
    caption: str
    model_params: Dict[str, Any]

class BaseCaptionModel(ABC):
    """Base class for caption generation models."""
    
    @abstractmethod
    def generate_captions(self, inputs: List[CaptionInput]) -> List[CaptionOutput]:
        """Generate captions for multiple inputs.
        
        Args:
            inputs: List of CaptionInput objects containing video names and instructions
            
        Returns:
            List of CaptionOutput objects containing generated captions
        """
        pass
    
    @abstractmethod
    def validate_model_params(self, params: Dict[str, Any]) -> bool:
        """Validate that the model parameters are valid for this model.
        
        Args:
            params: Dictionary of model parameters
            
        Returns:
            True if parameters are valid, False otherwise
        """
        pass 