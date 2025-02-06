"""
Caption generation package for managing video captions.

This package provides functionality for generating and managing captions for videos,
including different types of captions (shot transitions, subject descriptions, etc.)
and support for multiple caption generation models.
"""

from .core.generator import CaptionGenerator, CaptionRule, ModelType
from .core.processor import CaptionProcessor
from .params.caption_result import CaptionResult, VideoCaptionResults

__all__ = [
    'CaptionGenerator',
    'CaptionRule',
    'ModelType',
    'CaptionProcessor',
    'CaptionResult',
    'VideoCaptionResults'
] 