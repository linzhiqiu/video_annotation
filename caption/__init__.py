"""
Video Caption System

A comprehensive system for creating, reviewing, and managing video captions
with AI assistance and human feedback.

Main components:
- config: Configuration management for different annotation types
- core: Core business logic and utilities
- interfaces: User interfaces for caption creation and review
- apps: Main application entry points
"""

__version__ = "1.0.0"
__author__ = "Video Caption Team"

# Import main components for easier access
from caption.core.auth import AuthManager
from caption.core.data_manager import DataManager
from caption.core.video_utils import VideoUtils
from caption.core.ui_components import UIComponents
from caption.core.caption_engine import CaptionEngine
from caption.interfaces.caption_interface import CaptionInterface
from caption.interfaces.review_interface import ReviewInterface

__all__ = [
    'AuthManager',
    'DataManager', 
    'VideoUtils',
    'UIComponents',
    'CaptionEngine',
    'CaptionInterface',
    'ReviewInterface'
]