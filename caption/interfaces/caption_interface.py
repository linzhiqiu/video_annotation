# caption/interfaces/caption_interface.py
import streamlit as st
import os
from datetime import datetime
from typing import Dict, Any, List
from streamlit_feedback import streamlit_feedback

from caption.core.data_manager import DataManager
from caption.core.caption_engine import CaptionEngine
from caption.core.ui_components import UIComponents
from caption.core.auth import APPROVED_REVIEWERS
from llm import get_llm, get_all_llms, get_supported_mode


class CaptionInterface:
    """Main caption creation interface"""
    
    def __init__(self, data_manager: DataManager, caption_engine: CaptionEngine):
        self.data_manager = data_manager
        self.caption_engine = caption_engine
        self.ui = UIComponents()
    
    def render_feedback_interface(self, video_id: str, config: Dict[str, Any], 
                                 output_dir: str, caption_program: Any, 
                                 video_data_dict: Dict[str, Any], selected_video: str,
                                 args: Any, selected_config: str, config_dict: Dict[str, Any]):
        """Main feedback interface for caption creation"""
        
        with st.container(height=self.ui.CONTAINER_HEIGHT, border=True):
            # Step 0: Generating Pre-caption
            if st.session_state.current_step == 0:
                # Check if feedback already exists
                feedback_exists = self.data_manager.data_exists(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
                
                if feedback_exists:
                    self._handle_existing_feedback_and_review(video_id, output_dir, args)
                    
                    # Only check permissions if feedback already exists
                    if not self._check_permissions(video_id, output_dir, args):
                        return
                
                self._render_precaption_step(
                    video_id, output_dir, caption_program, video_data_dict, 
                    selected_video, selected_config, config_dict, args
                )
            
            # Step 3: Rate GPT's caption and optionally provide corrected caption
            elif st.session_state.current_step == 3:
                self._render_final_caption_step(video_id, output_dir, args)
            
            # Step 4: Print the final caption
            elif st.session_state.current_step == 4:
                self._render_completion_step()
    
    def _handle_existing_feedback_and_review(self, video_id: str, output_dir: str, args: Any):
        """Handle existing feedback and reviewer interface"""
        # First display the existing feedback in the original format
        feedback_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        prev_feedback_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
        
        # Show existing feedback if available (matching original load_feedback logic)
        if feedback_data:
            if prev_feedback_data:
                st.success(f"This video has already been completed by {prev_feedback_data['user']} and reviewed by {feedback_data['user']}. The final caption is:")
            else:
                st.success(f"This video has already been completed by {feedback_data['user']}. The final caption is:")
            st.text(feedback_data["final_caption"])
            # Render as collapsible text
            with st.expander("Show final JSON Data", expanded=False):
                st.json(feedback_data)
        
        # Then show the reviewer interface
        current_user = st.session_state.logged_in_user
        is_approved_reviewer = current_user in APPROVED_REVIEWERS
        
        with st.expander("Reviewer: Please Review Caption Here", expanded=is_approved_reviewer):
            self.ui.display_feedback_info(feedback_data, display_pre_caption_instead_of_final_caption=True)
            self._render_reviewer_interface(video_id, output_dir, current_user, is_approved_reviewer, args)
    
    def _render_reviewer_interface(self, video_id: str, output_dir: str, current_user: str, 
                                 is_approved_reviewer: bool, args: Any):
        """Render the reviewer interface - exact copy from original feedback_app.py"""
        reviewer_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
        
        if not is_approved_reviewer:
            st.write("##### Reviewer Status")
            st.write(f"You are **{current_user}**. You are not an approved reviewer.")
        else:
            if reviewer_data is None:
                st.write("##### Reviewer Status")
                st.write(f"You are **{current_user}**. You can review (double check) this caption.")
                if not self._can_reviewer_redo(video_id, output_dir, current_user):
                    st.error("You cannot review this caption because you are the annotator.")
                else:
                    review_col1, review_col2 = st.columns(2)
                    with review_col1:
                        if st.button("⚠️ Reject and Redo", 
                            help="Reject the current caption and create a new version"):
                            self._handle_rejection(video_id, output_dir, current_user)
                    with review_col2:
                        if st.button("Approve", 
                            help="Mark the caption as correct"):
                            reviewer_data = {
                                "reviewer_name": current_user,
                                "review_timestamp": datetime.now().isoformat(),
                                "reviewer_double_check": True
                            }
                            self.data_manager.save_data(video_id, reviewer_data, output_dir=output_dir, 
                                                       file_postfix=self.data_manager.REVIEWER_FILE_POSTFIX)
                            st.rerun()
            else:
                is_same_reviewer = reviewer_data.get("reviewer_name") == current_user
                is_approved = reviewer_data.get("reviewer_double_check", False)
                
                st.write("##### Reviewer Status")
                if is_same_reviewer:
                    status = "approved" if is_approved else "rejected"
                    st.write(f"You are **{current_user}**. You already reviewed the caption and {status} it.")
                else:
                    other_reviewer = reviewer_data.get("reviewer_name")
                    status = "approved" if is_approved else "rejected"
                    st.write(f"You are **{current_user}**. **{other_reviewer}** already reviewed the caption and {status} it.")
                
                st.write("##### Review Controls")
                if is_approved:
                    if not self._can_reviewer_redo(video_id, output_dir, current_user):
                        st.error("You cannot review this caption because you are the annotator.")
                        return
                    st.write("This caption is approved. You can still reject by clicking the button below.")
                    if st.button("⚠️ Reject and Redo", 
                            help="Reject the current caption and create a new version",
                            key="reject_and_redo_approved"):
                        self._handle_rejection(video_id, output_dir, current_user)
                else:
                    if not self._can_reviewer_redo(video_id, output_dir, current_user):
                        st.error("You cannot review this caption because you are the annotator.")
                        prev_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                        feedback_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
                        # Import here to avoid circular imports
                        from caption.interfaces.review_interface import ReviewInterface
                        review_interface = ReviewInterface(self.data_manager)
                        review_interface.display_feedback_differences(
                            prev_feedback=prev_feedback,
                            feedback_data=feedback_data,
                            diff_prompt=args.diff_prompt if args else None,
                            reviewer_data=reviewer_data
                        )
                        return
                    st.write("This caption is rejected. You can either approve it or redo it.")
                    review_col1, review_col2 = st.columns(2)
                    with review_col1:
                        if st.button("Already Rejected", 
                                disabled=True,
                                help="Current status: Rejected"):
                            pass
                    with review_col2:
                        if st.button("⚠️ Approve (revert to the annotator's caption below)", 
                                help="Mark the caption as correct"):
                            # Load previous feedback
                            prev_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                            if not prev_feedback:
                                st.error("Cannot revert: Previous feedback does not exist.")
                            else:
                                # Update reviewer data
                                reviewer_data = {
                                    "reviewer_name": current_user,
                                    "review_timestamp": datetime.now().isoformat(),
                                    "reviewer_double_check": True
                                }
                                self.data_manager.save_data(video_id, reviewer_data, output_dir=output_dir, 
                                                           file_postfix=self.data_manager.REVIEWER_FILE_POSTFIX)
                                
                                # Replace current feedback with previous
                                self.data_manager.save_data(video_id, prev_feedback, output_dir=output_dir, 
                                                           file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX)
                                
                                # Delete previous feedback file
                                prev_file = self.data_manager.get_filename(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                                print(f"Deleting previous feedback file: {prev_file}")
                                os.remove(prev_file)
                                st.rerun()
                    # Print the previous final caption
                    prev_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                    st.write(f"##### Previous Final Caption")
                    st.write(prev_feedback.get("final_caption", "No previous final caption found."))
    
    def _check_permissions(self, video_id: str, output_dir: str, args: Any) -> bool:
        """Check if user has permissions to proceed (only called when feedback already exists)"""
        annotator, reviewer = self.data_manager.get_annotator_and_reviewer(video_id, output_dir)
        reviewer_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
        current_user = st.session_state.logged_in_user
        
        # Check if current user is the annotator
        if annotator == current_user:
            if not self._can_annotator_redo(video_id, output_dir, current_user):
                if reviewer_data and reviewer_data.get("reviewer_double_check", False):
                    st.success("This caption has been approved. You don't need to modify it further.")
                else:
                    st.error("This caption has been rejected. Please see the difference between your feedback and reviewer feedback below:")
                    prev_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
                    feedback_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
                    # Import here to avoid circular imports
                    from caption.interfaces.review_interface import ReviewInterface
                    review_interface = ReviewInterface(self.data_manager)
                    review_interface.display_feedback_differences(
                        prev_feedback=prev_feedback,
                        feedback_data=feedback_data,
                        diff_prompt=str(self.data_manager.folder / getattr(args, 'diff_prompt', 'prompts/diff_prompt.txt')) if 'args' in locals() else str(self.data_manager.folder / 'prompts/diff_prompt.txt'),
                        reviewer_data=reviewer_data
                    )
                return False
        
        # Check if current user is a different user who is not an approved reviewer
        elif current_user not in APPROVED_REVIEWERS:
            st.error("You are not an approved reviewer. Please reach out to Zhiqiu Lin if you want to review/redo this caption.")
            return False
        
        # Check if current user is an approved reviewer but caption hasn't been reviewed - MATCH ORIGINAL LOGIC
        elif not reviewer_data:
            st.error("This caption has not been reviewed yet. Please review it first before making modifications.")
            return False
        
        # Check if caption has been approved
        elif reviewer_data.get("reviewer_double_check", False):
            st.success("This caption has been approved. You don't need to modify it further.")
            return False
        
        # If reviewer data exists but not approved, allow proceeding (caption was rejected)
        return True
    

    def _render_precaption_step(self, video_id: str, output_dir: str, caption_program: Any,
                               video_data_dict: Dict[str, Any], selected_video: str,
                               selected_config: str, config_dict: Dict[str, Any], args: Any):
        """Render the precaption generation step"""
        # Get the config object from config_dict and selected_config
        config = config_dict[selected_config]
        
        # Load existing precaption
        existing_precaption = self.caption_engine.load_precaption(video_id, output_dir)
        
        # LLM selection
        llm_names = get_all_llms()
        selected_llm = st.selectbox(
            "Select a Model:",
            llm_names,
            index=llm_names.index(self.caption_engine.get_precaption_llm_name(config_dict, selected_config)),
            key="selected_llm"
        )
        
        # Mode selection
        supported_modes = get_supported_mode(selected_llm)
        selected_mode = st.selectbox(
            "Select a Mode:",
            supported_modes,
            index=0,
            key="selected_mode"
        )
        
        # Prompt editing
        if "pre_caption_prompt" in st.session_state:
            pre_caption_prompt = st.session_state.pre_caption_prompt
        else:
            pre_caption_prompt = self.caption_engine.load_pre_caption_prompt(
                video_id, video_data_dict, caption_program, config_dict, selected_config, output_dir
            )
        
        # Calculate text area height
        line_height = 6
        num_lines = max(30, len(pre_caption_prompt) // 120)
        estimated_height = num_lines * line_height
        
        current_prompt = st.text_area(
            "Prompt for pre-captioning:",
            value=pre_caption_prompt,
            key="pre_caption_prompt",
            height=estimated_height,
        )
        
        # Get or generate precaption
        if "pre_caption" in existing_precaption:
            pre_caption = existing_precaption["pre_caption"]
        else:
            pre_caption = self.caption_engine.generate_precaption(
                video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video
            )
        
        # Store precaption data in session state
        st.session_state.pre_caption_data = {
            "video_id": video_id,
            "pre_caption_prompt": current_prompt,
            "pre_caption": pre_caption,
            "pre_caption_llm": selected_llm,
            "pre_caption_mode": selected_mode,
        }
        
        # Re-generation button
        if st.button("Re-generate a pre-caption"):
            st.info("Be patient, this may take a while...")
            self.caption_engine.generate_precaption(
                video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video
            )
            st.rerun()
        
        # Display current precaption
        st.write("##### Current pre-caption")
        st.write(pre_caption)
        st.write("#### Critique and then rate the pre-caption (Is it accurate based on the caption instruction?)")
        
        # Exact text from original feedback_app.py
        st.write("Please provide your feedback to improve this caption (if the score is not 5):")
        
        # Feedback collection
        user_feedback = st.text_area(
            "Your feedback:",
            key=f"user_feedback_{video_id}_{config['name']}",
            height=self.ui.PROMPT_HEIGHT,
        )
        
        # Rating collection
        self._collect_initial_rating(video_id, config, user_feedback, pre_caption, current_prompt, 
                                   selected_llm, selected_mode, args)
    
    def _collect_initial_rating(self, video_id: str, config: Dict[str, Any], user_feedback: str,
                              pre_caption: str, current_prompt: str, selected_llm: str, selected_mode: str, args: Any):
        """Collect initial rating from user"""
        if "initial_caption_rating" in st.session_state:
            score = st.session_state.initial_caption_rating
        else:
            st.warning("If unhappy with the caption, please write your feedback before rating.")
            initial_rating_response = streamlit_feedback(
                feedback_type="faces",
                key=f"initial_caption_faces_{video_id}_{config['name']}"
            )
            
            if initial_rating_response:
                st.session_state.initial_caption_rating = initial_rating_response['score']
                score = initial_rating_response['score']
            else:
                score = None
        
        if score:
            self._process_initial_rating(score, video_id, pre_caption, current_prompt, selected_llm, 
                                       selected_mode, user_feedback, args)
    
    def _process_initial_rating(self, score: str, video_id: str, pre_caption: str, current_prompt: str,
                              selected_llm: str, selected_mode: str, user_feedback: str, args: Any):
        """Process the initial rating and determine next steps"""
        feedback_is_needed = score != "😀"
        
        # Initialize feedback data - ensure all fields are present to match original logic
        st.session_state.feedback_data = {
            "video_id": video_id,
            "pre_caption": pre_caption,
            "pre_caption_prompt": current_prompt,
            "pre_caption_llm": selected_llm,
            "pre_caption_mode": selected_mode,
            "original_caption": pre_caption,
            "initial_caption_rating": score,
            "initial_caption_rating_score": self.ui.emoji_to_score(score),
            "feedback_is_needed": feedback_is_needed,
            "user": st.session_state.logged_in_user,
            "timestamp": datetime.now().isoformat(),  # Add timestamp immediately
            # Initialize other fields as None - must match original schema exactly
            "initial_feedback": None,
            "gpt_feedback_llm": None,
            "gpt_feedback_prompt": None,
            "gpt_feedback": None,
            "feedback_rating": None,
            "feedback_rating_score": None,
            "final_feedback": None,
            "gpt_caption_llm": None,
            "gpt_caption_prompt": None,
            "gpt_caption": None,
            "caption_rating": None,
            "caption_rating_score": None,
            "final_caption": None
        }
        
        if feedback_is_needed:
            self._handle_feedback_needed(user_feedback, args)
        else:
            # For perfect ratings, get the output_dir from session state or current context
            output_dir = getattr(st.session_state, 'current_output_dir', args.output_dir if hasattr(args, 'output_dir') else '')
            self._handle_perfect_rating(video_id, pre_caption, output_dir)
    
    def _handle_feedback_needed(self, user_feedback: str, args: Any):
        """Handle case where feedback is needed"""
        if args.show_feedback_prompt:
            self._render_feedback_prompt_interface(user_feedback)
        else:
            feedback_prompt = self.ui.load_txt(str(self.data_manager.folder / args.feedback_prompt))
            selected_feedback_llm = "gpt-4o-2024-08-06"
            has_user_feedback_entered_and_submitted = True
            
            if has_user_feedback_entered_and_submitted:
                st.session_state.feedback_data["initial_feedback"] = user_feedback
                st.session_state.feedback_data["gpt_feedback_llm"] = selected_feedback_llm
                st.session_state.feedback_data["gpt_feedback_prompt"] = feedback_prompt
                st.session_state.current_step = 3
                st.rerun()
    
    def _render_feedback_prompt_interface(self, user_feedback: str):
        """Render feedback prompt editing interface"""
        st.write("You can optionally change the LLM or the prompt that we used to polish your feedback. Please keep {feedback} and {pre_caption} in the prompt.")
        
        llm_names = get_all_llms()
        selected_feedback_llm = st.selectbox(
            "Select a Model:",
            llm_names,
            key="selected_feedback_llm",
            index=llm_names.index("gpt-4o-2024-08-06"),
        )
        
        if "cur_feedback_prompt" in st.session_state:
            feedback_prompt = st.session_state.cur_feedback_prompt
        else:
            feedback_prompt = self.ui.load_txt(str(self.data_manager.folder / "prompts/feedback_prompt.txt"))
        
        feedback_prompt = st.text_area(
            "Prompt for polishing feedback:",
            value=feedback_prompt,
            key="cur_feedback_prompt",
            height=self.ui.PROMPT_HEIGHT,
        )
        
        has_user_feedback_entered_and_submitted = st.button("Submit Feedback")
        
        if has_user_feedback_entered_and_submitted:
            st.session_state.feedback_data["initial_feedback"] = user_feedback
            st.session_state.feedback_data["gpt_feedback_llm"] = selected_feedback_llm
            st.session_state.feedback_data["gpt_feedback_prompt"] = feedback_prompt
            st.session_state.current_step = 3
            st.rerun()
    
    def _handle_perfect_rating(self, video_id: str, pre_caption: str, output_dir: str):
        """Handle case where rating is perfect"""
        st.session_state.feedback_data["final_caption"] = pre_caption
        # Add missing timestamp if not present
        if "timestamp" not in st.session_state.feedback_data:
            st.session_state.feedback_data["timestamp"] = datetime.now().isoformat()
        
        self.data_manager.save_data(video_id, st.session_state.feedback_data, 
                                   output_dir=output_dir, 
                                   file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX)
        st.success("Caption rated as perfect! No changes needed.")
        st.json(st.session_state.feedback_data)
        st.session_state.current_step = 4
        st.rerun()
    
    def _render_final_caption_step(self, video_id: str, output_dir: str, args: Any):
        """Render the final caption editing step"""
        # Generate polished feedback if not exists
        if not st.session_state.feedback_data.get("final_feedback", False):
            new_feedback = self.caption_engine.generate_feedback(
                st.session_state.feedback_data["gpt_feedback_prompt"],
                st.session_state.feedback_data["gpt_feedback_llm"],
                st.session_state.feedback_data["initial_feedback"],
                st.session_state.feedback_data["pre_caption"]
            )
            st.session_state.feedback_data["gpt_feedback"] = new_feedback
            st.session_state.feedback_data["final_feedback"] = new_feedback
        
        # Generate caption if not exists
        if not st.session_state.feedback_data.get("gpt_caption", False):
            pre_caption = st.session_state.feedback_data["pre_caption"]
            selected_caption_llm = "gpt-4o-2024-08-06"
            caption_prompt = self.ui.load_txt(str(self.data_manager.folder / args.caption_prompt))
            
            st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
            st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
            
            new_caption = self.caption_engine.generate_caption(
                caption_prompt, selected_caption_llm,
                st.session_state.feedback_data["final_feedback"], pre_caption
            )
            st.session_state.feedback_data["gpt_caption"] = new_caption
            
            # Set default perfect ratings
            perfect_score = "😀"
            st.session_state.feedback_rating = perfect_score
            st.session_state.feedback_data["feedback_rating"] = perfect_score
            st.session_state.feedback_data["feedback_rating_score"] = self.ui.emoji_to_score(perfect_score)
        
        self._render_final_editing_interface(video_id, output_dir, args)
    
    def _render_final_editing_interface(self, video_id: str, output_dir: str, args: Any):
        """Render final editing interface"""
        # Feedback editing
        line_height = 6
        num_lines = max(30, len(st.session_state.feedback_data["final_feedback"]) // 120)
        estimated_height = num_lines * line_height
        
        final_feedback = st.text_area(
            "Finalized feedback:",
            value=st.session_state.feedback_data["final_feedback"],
            key="correct_feedback",
            height=estimated_height,
        )
        
        # # Re-generation buttons
        # button_col1, button_col2 = st.columns([1, 1])
        
        # with button_col1:
        #     if st.button("Only Re-generate Caption (Disabled)", disabled=True):
        #         if final_feedback.strip():
        #             st.session_state.feedback_data["final_feedback"] = final_feedback
        #             del st.session_state.feedback_data["gpt_caption"]
        #         else:
        #             st.warning("Please provide an non-empty feedback before submitting.")
        #         st.rerun()
        
        # with button_col2:
        #     if st.button("✨ Polish Feedback & Regenerate Caption"):
        #         if final_feedback.strip():
        #             st.session_state.feedback_data["initial_feedback"] = final_feedback
        #             st.session_state.feedback_data["final_feedback"] = None
        #             del st.session_state.feedback_data["gpt_caption"]
        #         else:
        #             st.warning("Please provide an non-empty feedback before submitting.")
        #         st.rerun()
        # Re-generation button (full width)
        if st.button("✨ Polish Feedback & Regenerate Caption", use_container_width=True):
            if final_feedback.strip():
                st.session_state.feedback_data["initial_feedback"] = final_feedback
                st.session_state.feedback_data["final_feedback"] = None
                del st.session_state.feedback_data["gpt_caption"]
            else:
                st.warning("Please provide an non-empty feedback before submitting.")
            st.rerun()
        
        # Caption editing
        line_height = 12
        num_lines = max(30, len(st.session_state.feedback_data["gpt_caption"]) // 120)
        estimated_height = num_lines * line_height
        
        final_caption = st.text_area(
            "Final caption:",
            value=st.session_state.feedback_data["gpt_caption"],
            key="correct_caption",
            height=estimated_height,
        )
        
        # Set default perfect rating for caption
        perfect_score = "😀"
        st.session_state.feedback_data["caption_rating"] = perfect_score
        st.session_state.feedback_data["caption_rating_score"] = self.ui.emoji_to_score(perfect_score)
        
        # Submit button
        if st.button("I am happy with both feedback and caption"):
            if final_caption.strip() and final_feedback.strip():
                st.session_state.feedback_data["final_caption"] = final_caption
                st.session_state.feedback_data["final_feedback"] = final_feedback
                # Ensure timestamp and user are set for consistency with original logic
                if "timestamp" not in st.session_state.feedback_data:
                    st.session_state.feedback_data["timestamp"] = datetime.now().isoformat()
                if "user" not in st.session_state.feedback_data:
                    st.session_state.feedback_data["user"] = st.session_state.logged_in_user
                
                # Save feedback data
                self.data_manager.save_data(video_id, st.session_state.feedback_data, 
                                          output_dir=output_dir, 
                                          file_postfix=self.data_manager.FEEDBACK_FILE_POSTFIX)
                st.success("Feedback and caption saved successfully!")
                st.session_state.current_step = 4
            else:
                st.warning("Please provide an non-empty caption and feedback before submitting.")
            st.rerun()
        else:
            # Show reference pre-caption
            st.write("Below is the original pre-caption for reference.")
            st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
            st.text(st.session_state.feedback_data["pre_caption"])
            st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
    
    def _render_completion_step(self):
        """Render the completion step"""
        st.text(st.session_state.feedback_data["final_caption"])
        st.success("Feedback and caption saved successfully! To redo, please go to another video then come back.")
        st.json(st.session_state.feedback_data)
    
    def _handle_rejection(self, video_id: str, output_dir: str, current_user: str):
        """Handle caption rejection"""
        # Copy current feedback to previous
        self.data_manager.copy_to_prev_feedback(video_id, output_dir)
        
        # Create reviewer data
        reviewer_data = {
            "reviewer_name": current_user,
            "review_timestamp": datetime.now().isoformat(),
            "reviewer_double_check": False
        }
        self.data_manager.save_data(video_id, reviewer_data, output_dir=output_dir, 
                                   file_postfix=self.data_manager.REVIEWER_FILE_POSTFIX)
        st.rerun()
    
    def _can_annotator_redo(self, video_id: str, output_dir: str, current_user: str) -> bool:
        """Check if the current user (as annotator) can redo the caption"""
        from caption.core.auth import AuthManager
        return AuthManager.can_annotator_redo(video_id, output_dir, current_user, self.data_manager)
    
    def _can_reviewer_redo(self, video_id: str, output_dir: str, current_user: str) -> bool:
        """Check if the current user (as reviewer) can redo the caption"""
        from caption.core.auth import AuthManager
        return AuthManager.can_reviewer_redo(video_id, output_dir, current_user, self.data_manager)