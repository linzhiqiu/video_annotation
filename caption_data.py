from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum, auto

class CaptionType(Enum):
    """Enum for different types of captions."""
    SHOT_TRANSITION = auto()
    SUBJECT_DESCRIPTION = auto()
    SPATIAL_FRAMING_MOTION = auto()
    SINGLE_SUBJECT_ACTION = auto()
    SUBJECT_OBJECT_INTERACTION = auto()
    SUBJECT_SUBJECT_INTERACTION = auto()
    GROUP_ACTION = auto()
    SCENE_DESCRIPTION = auto()
    SCENE_MOTION = auto()
    CAMERA_DESCRIPTION = auto()
    CAMERA_MOTION = auto()

@dataclass
class CaptionMetadata:
    """Metadata for a caption, including the model and prompt used."""
    model: str
    prompt: str
    timestamp: Optional[str] = None
    confidence: Optional[float] = None
    additional_info: Optional[Dict[str, Any]] = None

class CaptionData:
    """Class for storing and managing video captions."""
    
    def __init__(self):
        """Initialize caption data with empty captions."""
        self._captions: Dict[CaptionType, str] = {}
        self._metadata: Dict[CaptionType, CaptionMetadata] = {}
        
        # Initialize all caption types with None
        for caption_type in CaptionType:
            self._captions[caption_type] = None
            self._metadata[caption_type] = None
    
    def set_caption(self, caption_type: CaptionType, caption: str, metadata: CaptionMetadata) -> None:
        """Set a caption and its metadata for a specific type.
        
        Args:
            caption_type: The type of caption being set
            caption: The caption text
            metadata: Metadata about how the caption was generated
        """
        self._captions[caption_type] = caption
        self._metadata[caption_type] = metadata
    
    def get_caption(self, caption_type: CaptionType) -> Optional[str]:
        """Get the caption for a specific type.
        
        Args:
            caption_type: The type of caption to retrieve
            
        Returns:
            The caption text if it exists, None otherwise
        """
        return self._captions.get(caption_type)
    
    def get_metadata(self, caption_type: CaptionType) -> Optional[CaptionMetadata]:
        """Get the metadata for a specific caption type.
        
        Args:
            caption_type: The type of caption metadata to retrieve
            
        Returns:
            The caption metadata if it exists, None otherwise
        """
        return self._metadata.get(caption_type)
    
    def get_all_captions(self) -> Dict[CaptionType, str]:
        """Get all captions.
        
        Returns:
            Dictionary mapping caption types to their text
        """
        return self._captions.copy()
    
    def get_all_metadata(self) -> Dict[CaptionType, CaptionMetadata]:
        """Get metadata for all captions.
        
        Returns:
            Dictionary mapping caption types to their metadata
        """
        return self._metadata.copy()
    
    def has_caption(self, caption_type: CaptionType) -> bool:
        """Check if a caption exists for the given type.
        
        Args:
            caption_type: The type of caption to check
            
        Returns:
            True if the caption exists and is not None
        """
        return self._captions.get(caption_type) is not None
    
    def clear_caption(self, caption_type: CaptionType) -> None:
        """Clear the caption and metadata for a specific type.
        
        Args:
            caption_type: The type of caption to clear
        """
        self._captions[caption_type] = None
        self._metadata[caption_type] = None
    
    def clear_all(self) -> None:
        """Clear all captions and metadata."""
        for caption_type in CaptionType:
            self.clear_caption(caption_type)
    
    @classmethod
    def create(cls, **kwargs) -> 'CaptionData':
        """Create a CaptionData instance from a dictionary of parameters.
        
        Args:
            **kwargs: Dictionary containing caption data
                     Each key should be a CaptionType member name
                     Each value should be a dict with 'caption' and 'metadata' keys
        
        Returns:
            A new CaptionData instance
        """
        instance = cls()
        
        for caption_type_name, data in kwargs.items():
            try:
                caption_type = CaptionType[caption_type_name.upper()]
                caption = data.get('caption')
                metadata_dict = data.get('metadata', {})
                
                if caption and metadata_dict:
                    metadata = CaptionMetadata(**metadata_dict)
                    instance.set_caption(caption_type, caption, metadata)
            except (KeyError, ValueError) as e:
                print(f"Error processing caption {caption_type_name}: {str(e)}")
                continue
        
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """Convert the caption data to a dictionary format.
        
        Returns:
            Dictionary representation of the caption data
        """
        return {
            caption_type.name.lower(): {
                'caption': self._captions[caption_type],
                'metadata': vars(self._metadata[caption_type]) if self._metadata[caption_type] else None
            }
            for caption_type in CaptionType
            if self._captions[caption_type] is not None
        }

    def __repr__(self) -> str:
        """String representation of the caption data."""
        return f"CaptionData({self.to_dict()})" 