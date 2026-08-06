# core/session_state_manager.py
"""
Centralized session state key management to avoid duplication across files.
Determines which keys to preserve based on current login method, portal, and mode.
"""

import streamlit as st
from typing import List, Set


class SessionStateKeyManager:
    """Manages session state keys in a DRY way"""
    
    # Base keys that are always preserved regardless of context
    BASE_KEYS = {
        'logged_in', 'logged_in_user', 'video_urls', 'selected_portal', 
        'login_method', 'file_check_passed', 'personalized_output', 'api_key'
    }
    
    # Login method specific keys
    LOGIN_METHOD_KEYS = {
        'annotator': {'target_annotator'},
        'sheet': {'selected_sheet_file'}
    }
    
    # Portal mode keys (for onboarding app)
    PORTAL_MODE_KEYS = {'selected_portal_mode', 'selected_portal_file'}
    
    # Portal-specific navigation keys
    PORTAL_NAVIGATION_KEYS = {
        'caption': {
            'last_config_id', 'selected_config', 
            'last_video_id', 'last_selected_video'
        },
        'review': {
            'last_config_id', 'selected_config_review',
            'last_video_id', 'last_selected_video'
        },
        'comparison': {
            'last_config_id_comparison', 'selected_config_comparison',
            'last_video_id_comparison', 'last_selected_video_comparison',
            'file_check_passed_comparison'
        },
        'caption_mode': {  # For onboarding app caption mode
            'last_config_id_caption', 'last_video_id_caption', 
            'last_selected_video_caption', 'file_check_passed_caption'
        }
    }

    @classmethod
    def get_base_preserved_keys(cls) -> set:
        """Get base keys that should always be preserved regardless of context"""
        preserved_keys = set(cls.BASE_KEYS)
        
        # Add login method specific keys
        login_method = st.session_state.get('login_method')
        if login_method in cls.LOGIN_METHOD_KEYS:
            preserved_keys.update(cls.LOGIN_METHOD_KEYS[login_method])
        
        # Add portal mode keys if they exist in session state
        if any(key in st.session_state for key in cls.PORTAL_MODE_KEYS):
            preserved_keys.update(cls.PORTAL_MODE_KEYS)
        
        return preserved_keys
    
    @classmethod
    def get_preserved_keys(cls, portal: str = None, mode: str = None) -> List[str]:
        """
        Get the list of keys to preserve based on current context.
        
        Args:
            portal: Current portal ('caption', 'review', 'comparison', etc.)
            mode: Current mode (for onboarding app, e.g., 'caption_mode')
            
        Returns:
            List of session state keys to preserve
        """
        preserved_keys = set(cls.BASE_KEYS)
        
        # Add login method specific keys
        login_method = st.session_state.get('login_method')
        if login_method in cls.LOGIN_METHOD_KEYS:
            preserved_keys.update(cls.LOGIN_METHOD_KEYS[login_method])
        
        # Add portal mode keys if they exist in session state
        if any(key in st.session_state for key in cls.PORTAL_MODE_KEYS):
            preserved_keys.update(cls.PORTAL_MODE_KEYS)
        
        # Add portal-specific navigation keys
        if mode and mode in cls.PORTAL_NAVIGATION_KEYS:
            # Use mode first (for onboarding app)
            preserved_keys.update(cls.PORTAL_NAVIGATION_KEYS[mode])
        elif portal and portal in cls.PORTAL_NAVIGATION_KEYS:
            # Fall back to portal
            preserved_keys.update(cls.PORTAL_NAVIGATION_KEYS[portal])
        elif portal == 'caption':
            # Default caption portal keys
            preserved_keys.update(cls.PORTAL_NAVIGATION_KEYS['caption'])
        
        return list(preserved_keys)
    
    @classmethod
    def get_preserved_keys_for_caption_portal(cls) -> List[str]:
        """Get preserved keys for caption portal (apps/app.py)"""
        return cls.get_preserved_keys(portal='caption')
    
    @classmethod
    def get_preserved_keys_for_review_portal(cls) -> List[str]:
        """Get preserved keys for review portal (apps/app.py)"""
        return cls.get_preserved_keys(portal='review')
    
    @classmethod
    def get_preserved_keys_for_comparison_portal(cls) -> List[str]:
        """Get preserved keys for comparison portal (apps/onboard_app.py)"""
        return cls.get_preserved_keys(portal='comparison')
    
    @classmethod
    def get_preserved_keys_for_caption_mode(cls) -> List[str]:
        """Get preserved keys for caption mode in onboarding (apps/onboard_app.py)"""
        return cls.get_preserved_keys(mode='caption_mode')
    
    @classmethod
    def reset_state_except_preserved(cls, preserved_keys: List[str]) -> None:
        """
        Reset session state while preserving specific keys.
        This replaces all the scattered reset_state_except functions.
        """
        keys_to_remove = [key for key in st.session_state if key not in preserved_keys]
        for key in keys_to_remove:
            del st.session_state[key]
        st.rerun()
    
    @classmethod  
    def debug_preserved_keys(cls, context: str = "") -> None:
        """Debug helper to see what keys would be preserved in current context"""
        portal = st.session_state.get('selected_portal')
        login_method = st.session_state.get('login_method')
        
        print(f"=== DEBUG PRESERVED KEYS {context} ===")
        print(f"Portal: {portal}")
        print(f"Login method: {login_method}")
        print(f"Current session keys: {list(st.session_state.keys())}")
        
        preserved = cls.get_preserved_keys(portal=portal)
        print(f"Would preserve: {preserved}")
        print("=" * 50)