# caption/config/__init__.py
"""
Configuration module for video annotation system.

Provides configuration management for different annotation types (main, lighting, etc.)
"""

from caption.config.base_config import AppConfig, get_config

# Expose the main public API
__all__ = [
    'AppConfig',
    'get_config',
]