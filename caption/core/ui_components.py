# caption/core/ui_components.py
import streamlit as st
import difflib
import re
import html
from datetime import datetime
from typing import Dict, Any, List, Optional
from diff_match_patch import diff_match_patch

from llm import get_llm, get_all_llms
from caption.core.data_manager import DataManager
from caption.session_state_manager import SessionStateKeyManager

class UIComponents:
    """Reusable UI components for the caption system"""
    
    # Constants
    CONTAINER_HEIGHT = 1100
    PROMPT_HEIGHT = 225
    
    config_names_to_short_names = {
        "Subject Description Caption": "🧍‍♂️Subject",
        "Scene Composition and Dynamics Caption": "🏞️Scene",
        "Subject Motion and Dynamics Caption": "🏃‍♂️Motion",
        "Spatial Framing and Dynamics Caption": "🗺️Spatial",
        "Camera Framing and Dynamics Caption": "📷Camera",
        "Color Composition and Dynamics Caption (Raw)": "🎨Color",
        "Lighting Setup and Dynamics Caption (Raw)": "💡Lighting",
        "Lighting Effects and Dynamics Caption (Raw)": "🌟Effects",
    }
    
    @staticmethod
    def display_status_indicators():
        """Display an expander explaining the status indicators used in the video selection dropdown"""
        with st.expander("📝 Status Indicators Explanation", expanded=False):
            st.markdown("""
            | Emoji | Status | Description |
            |-------|--------|-------------|
            |  | Not Completed | Video has not been captioned yet |
            | ✅ | Completed | Video has been captioned but not reviewed |
            | ✅✅ | Approved | Video has been reviewed and double-checked |
            | ❌ | Rejected | Video needs revision (different users in current and previous feedback) |
            """)
    
    @staticmethod
    def display_portal_selection():
        """Display portal selection page after login"""
        st.title("🎯 Select Portal")
        st.markdown(f"### Welcome back, **{st.session_state.logged_in_user}**!")
        
        # Display login info
        if st.session_state.get('login_method') == 'annotator':
            st.info(f"📊 You're viewing videos by: **{st.session_state.get('target_annotator', 'Unknown')}**")
        
        st.markdown("---")
        
        # Create two columns for portal selection
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### 📝 Caption Portal")
            st.markdown("""
            **Create and Edit Captions**
            - Generate AI-powered pre-captions
            - Provide feedback to refine captions
            - Approve or reject captions (reviewer only)
            """)
            if st.button("🚀 Enter Caption Portal", key="caption_portal", use_container_width=True):
                st.session_state.selected_portal = "caption"
                # Clear any portal-specific state to ensure clean start
                UIComponents.clear_portal_state()
                st.rerun()
        
        with col2:
            st.markdown("### 🔍 Review Portal")
            st.markdown("""
            **Review and Compare Captions**
            - View caption differences
            - Compare feedback for each video
            - Review accuracy statistics
            """)
            if st.button("🔍 Enter Review Portal", key="review_portal", use_container_width=True):
                st.session_state.selected_portal = "review"
                # Clear any portal-specific state to ensure clean start
                UIComponents.clear_portal_state()
                st.rerun()
        
        st.markdown("---")
        
        # Logout and portal switching options
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    @staticmethod
    def clear_portal_state():
        """Clear portal-specific state while preserving login and navigation state"""
        # Keys to preserve across portal switches - must match original logic exactly
        # preserve_keys = {
        #     'logged_in', 'logged_in_user', 'video_urls', 'login_method', 'target_annotator',
        #     'selected_portal', 'file_check_passed', 'personalized_output',
        #     # Preserve these core navigation keys to maintain consistency
        #     'api_key', 'last_config_id', 'last_video_id', 'last_selected_video'
        # }
        from caption.session_state_manager import SessionStateKeyManager
    
        preserve_keys = SessionStateKeyManager.get_base_preserved_keys()
        preserve_keys.update({'selected_portal'})  # Add portal-specific keys
    
        
        # Clear all other keys
        keys_to_clear = [k for k in st.session_state.keys() if k not in preserve_keys]
        for key in keys_to_clear:
            del st.session_state[key]
    
    @staticmethod
    def add_portal_navigation_sidebar(current_portal: str, app_config):
        """Add consistent portal navigation to sidebar"""
        with st.sidebar:
            if current_portal == "caption":
                st.title("📝 Caption Portal")
            else:
                st.title("🔍 Review Portal")
                
            st.write(f"**User:** {st.session_state.logged_in_user}")
            from caption.core.auth import AuthManager
            user_email = AuthManager.get_user_email(st.session_state.logged_in_user)
            if user_email:
                st.write(f"**Email:** {user_email}")
            
            if hasattr(app_config, 'output_dir') and app_config.personalize_output:
                st.write(f"**Output Directory:** {app_config.output_dir}")
            
            if hasattr(app_config, 'output_dir') and app_config.personalize_output:
                st.write(f"**Output Directory:** {app_config.output_dir}")
            
            st.markdown("---")
            
            # Portal switching
            if current_portal == "caption":
                if st.button("🔄 Switch to Review Portal"):
                    st.session_state.selected_portal = "review"
                    UIComponents.clear_portal_state()
                    st.rerun()
            else:
                if st.button("🔄 Switch to Caption Portal"):
                    st.session_state.selected_portal = "caption"
                    UIComponents.clear_portal_state()
                    st.rerun()
            
            if st.button("🏠 Back to Portal Selection"):
                if 'selected_portal' in st.session_state:
                    del st.session_state.selected_portal
                UIComponents.clear_portal_state()
                st.rerun()
            
            if st.button("🚪 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    @staticmethod
    def display_navigation_buttons(video_urls: List[str], config_names: List[str], 
                                 selected_video: str, selected_config: str, 
                                 preserved_keys: List[str], data_manager: DataManager):
        """Display navigation buttons for video and task switching"""
        # Get indices
        current_index = video_urls.index(selected_video)
        current_task_index = config_names.index(selected_config)

        # def reset_state_except(preserved):
        #     """Reset state while preserving specific keys - must match original logic"""
        #     keys_to_remove = [key for key in st.session_state if key not in preserved]
        #     for key in keys_to_remove:
        #         del st.session_state[key]
        #     st.rerun()
        def reset_state_except(preserved):
            SessionStateKeyManager.reset_state_except_preserved(preserved)

        # Create a single horizontal row with 5 nav buttons
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            if current_index > 0:
                if st.button("Prev Video ⏪"):
                    # Update video selection state consistently
                    prev_video = video_urls[current_index - 1]
                    st.session_state.last_selected_video = prev_video
                    st.session_state.last_video_id = data_manager.get_video_id(prev_video)
                    reset_state_except(preserved_keys)
            else:
                st.button("Prev Video ⏪", disabled=True)

        with col2:
            if current_task_index > 0:
                prev_task_index = current_task_index - 1
            else:
                prev_task_index = len(config_names) - 1
            prev_task_short_name = UIComponents.config_names_to_short_names.get(
                config_names[prev_task_index], config_names[prev_task_index]
            )
            if st.button(f"{prev_task_short_name} Task ⬅️"):
                st.session_state.last_config_id = config_names[prev_task_index]
                reset_state_except(preserved_keys)
        
        with col3:
            task_short_name = UIComponents.config_names_to_short_names.get(
                selected_config, selected_config
            )
            st.button(f"{task_short_name} Task ⬇️", disabled=True)

        with col4:
            if current_task_index < len(config_names) - 1:
                next_task_index = current_task_index + 1
            else:
                next_task_index = 0
            next_task_short_name = UIComponents.config_names_to_short_names.get(
                config_names[next_task_index], config_names[next_task_index]
            )
            if st.button(f"{next_task_short_name} Task ➡️"):
                st.session_state.last_config_id = config_names[next_task_index]
                reset_state_except(preserved_keys)

        with col5:
            if current_index < len(video_urls) - 1:
                if st.button("Next Video ⏩"):
                    # Update video selection state consistently
                    next_video = video_urls[current_index + 1]
                    st.session_state.last_selected_video = next_video
                    st.session_state.last_video_id = data_manager.get_video_id(next_video)
                    reset_state_except(preserved_keys)
            else:
                st.button("Next Video ⏭️", disabled=True)
    
    @staticmethod
    def display_feedback_info(feedback_data: Dict[str, Any], display_pre_caption_instead_of_final_caption: bool = False):
        """Display feedback information including scores, GPT feedback, and caption differences"""
        # ALWAYS show Final Caption at the top (matching original exactly)
        st.write("##### Final Caption")
        st.text(feedback_data.get("final_caption", "No caption available"))
        
        st.write("##### Pre-caption Score")
        st.write(f"**{feedback_data.get('initial_caption_rating_score', 'N/A')}/5**")

        st.write("##### Initial Feedback")
        st.text(feedback_data.get("initial_feedback", "No initial feedback available"))
        
        # st.write("##### GPT Polished Feedback")
        # st.text(feedback_data.get("gpt_feedback", "No GPT feedback available"))

        st.write("##### Final Feedback")
        st.text(feedback_data.get("final_feedback", "No final feedback available"))
        
        st.write("##### Final Caption Score")
        final_score = feedback_data.get("caption_rating_score")
        if final_score is None:
            st.write("**N/A** -- the initial caption already received a score of 5/5")
        elif final_score < 4:
            st.error(f"**{final_score}/5** - Low score indicates potential issues")
        else:
            st.write(f"**{final_score}/5**")
        
        # Calculate word changes
        gpt_caption = feedback_data.get("gpt_caption", "")
        final_caption = feedback_data.get("final_caption", "")
        if gpt_caption and final_caption:
            gpt_words = len(gpt_caption.split())
            final_words = len(final_caption.split())
            word_diff = abs(gpt_words - final_words)
            st.write("##### Word Changes from GPT to Final")
            if word_diff > 5:
                st.error(f"**{word_diff}** words changed - Large changes may indicate issues")
            else:
                st.write(f"**{word_diff}** words changed")
        
        # The parameter only affects what's shown at the bottom
        if display_pre_caption_instead_of_final_caption:
            st.write("##### Pre-Caption (For Reference Only)")
            st.text(feedback_data.get("pre_caption", "No pre-caption available"))
        else:
            st.write("##### Final Caption")
            st.text(feedback_data.get("final_caption", "No final caption available"))
    
    @staticmethod
    def emoji_to_score(emoji: str) -> int:
        """Convert emoji rating to 1-5 Likert scale"""
        emoji_map = {
            "😞": 1,  # Very unhappy
            "🙁": 2,  # Unhappy
            "😐": 3,  # Neutral
            "🙂": 4,  # Happy
            "😀": 5   # Very happy
        }
        if emoji not in emoji_map:
            raise ValueError("Invalid emoji rating provided.")
        return emoji_map[emoji]
    
    @staticmethod
    def load_txt(txt_file: str) -> str:
        """Load text from file"""
        with open(txt_file, "r") as f:
            return f.read()
    
    @staticmethod
    def highlight_differences(text1: str, text2: str, run_length: int = 5) -> str:
        """Highlight differences between two texts using HTML with word-level granularity"""
        text1 = "" if text1 is None else text1
        text2 = "" if text2 is None else text2
        
        if UIComponents._is_large_diff(text1, text2, run_length=run_length):
            return UIComponents._html_word_diff(text1, text2)
        else:
            # Split texts into words
            words1 = UIComponents._split_into_words(text1)
            words2 = UIComponents._split_into_words(text2)
            
            # Use difflib to find differences
            differ = difflib.Differ()
            diff = list(differ.compare(words1, words2))
            
            # Process the diff to create HTML with highlighting
            result = []
            for word in diff:
                if word.startswith('  '):  # unchanged
                    result.append(word[2:])
                elif word.startswith('- '):  # deleted
                    result.append(f'<span style="color: red; text-decoration: line-through;">{word[2:]}</span>')
                elif word.startswith('+ '):  # added
                    result.append(f'<span style="color: green; font-weight: bold;">{word[2:]}</span>')
            
            return ''.join(result)
    
    @staticmethod
    def highlight_differences_gpt(text1: str, text2: str, diff_prompt: str = None, 
                                diff_key: str = "diff_feedback", 
                                llm_key: str = "selected_diff_compare_llm", 
                                prompt_key: str = "cur_diff_compare_prompt", 
                                **kwargs):
        """Generate and display GPT-powered difference summary"""
        # First generate the initial diff feedback
        text1 = "" if text1 is None else text1
        text2 = "" if text2 is None else text2
        
        if diff_key not in st.session_state:
            llm_names = get_all_llms()
            selected_diff_compare_llm = llm_names[llm_names.index("gpt-4o-2024-08-06")]
            diff_compare_prompt = UIComponents.load_txt(diff_prompt)
            st.session_state[diff_key] = get_llm(
                model=selected_diff_compare_llm,
                secrets=st.secrets,
            ).generate(
                diff_compare_prompt.format(**kwargs),
            )
        
        # Display the current diff feedback
        st.markdown(st.session_state[diff_key], unsafe_allow_html=True)
        st.info("If the summary is not helpful, you can re-generate it by changing the prompt and clicking the button below.")
        
        # Then show controls for regeneration
        llm_names = get_all_llms()
        selected_diff_compare_llm = st.selectbox(
            "Select a Model:",
            llm_names,
            key=llm_key,
            index=llm_names.index("gpt-4o-2024-08-06"),
        )
        
        if prompt_key in st.session_state:
            diff_compare_prompt = st.session_state[prompt_key]
        else:
            diff_compare_prompt = UIComponents.load_txt(diff_prompt)

        diff_compare_prompt = st.text_area(
            "Prompt for comparing feedback:",
            value=diff_compare_prompt,
            key=prompt_key,
            height=UIComponents.PROMPT_HEIGHT,
        )
        if st.button("Re-generate Summary", key=f"{llm_key}_re_generate_button"):
            # Generate new diff feedback
            st.session_state[diff_key] = get_llm(
                model=selected_diff_compare_llm,
                secrets=st.secrets,
            ).generate(
                diff_compare_prompt.format(**kwargs),
            )
            st.rerun()  # Rerun to show the new feedback
    
    @staticmethod
    def _split_into_words(text: str) -> List[str]:
        """Split text into words for better diff visualization"""
        # Split by whitespace and punctuation
        words = re.findall(r"\w+|\W+", text)
        return words
    
    @staticmethod
    def _is_large_diff(text1: str, text2: str, run_length: int = 5) -> bool:
        """Return True if there is at least one consecutive run of insertions/deletions ≥ run_length tokens"""
        differ = difflib.Differ()
        w1, w2 = text1.split(), text2.split()
        diff = differ.compare(w1, w2)

        run = 0
        for tok in diff:
            if tok.startswith(('- ', '+ ')):          # a changed token
                run += 1
                if run >= run_length:
                    return True
            else:
                run = 0
        return False
    
    @staticmethod
    def _html_word_diff(text1: str, text2: str) -> str:
        """Return word-level diff between text1 and text2 using custom HTML formatting"""
        # Step 1: Word-to-char encoding
        def words_to_chars(text, word_map):
            words = text.split()
            encoded = []
            for word in words:
                if word not in word_map:
                    word_map[word] = chr(len(word_map) + 1)  # Unicode chars
                encoded.append(word_map[word])
            return ''.join(encoded), words

        word_map = {}
        text1_encoded, words1 = words_to_chars(text1, word_map)
        text2_encoded, words2 = words_to_chars(text2, word_map)

        # Step 2: Diff and cleanup
        dmp = diff_match_patch()
        diffs = dmp.diff_main(text1_encoded, text2_encoded)
        dmp.diff_cleanupSemantic(diffs)

        reverse_map = {v: k for k, v in word_map.items()}
        html_chunks = []

        # Step 3: Build HTML diff with styling
        for op, data in diffs:
            words = [reverse_map[c] for c in data]
            if op == dmp.DIFF_EQUAL:
                html_chunks.append(" ".join(map(html.escape, words)))
            elif op == dmp.DIFF_DELETE:
                html_chunks.append(
                    " ".join(f'<span style="color: red; text-decoration: line-through;">{html.escape(w)}</span>' for w in words)
                )
            elif op == dmp.DIFF_INSERT:
                html_chunks.append(
                    " ".join(f'<span style="color: green; font-weight: bold;">{html.escape(w)}</span>' for w in words)
                )
        return " ".join(html_chunks)