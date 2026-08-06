# caption/interfaces/review_interface.py
import streamlit as st
import os
import urllib.parse
from typing import Dict, Any, List, Optional
from pathlib import Path

from caption.core.auth import AuthManager
from caption.core.data_manager import DataManager
from caption.core.ui_components import UIComponents


class ReviewInterface:
    """Review and comparison interface"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ui = UIComponents()
    
    def render_review_interface(self, video_id: str, config: Dict[str, Any], 
                               output_dir: str, **kwargs):
        """Main review interface"""
        with st.container(height=self.ui.CONTAINER_HEIGHT, border=True):
            status, current_file, prev_file, current_user, prev_user = self.data_manager.get_video_status(
                video_id, output_dir
            )
            
            if status == "not_completed":
                st.warning("Please complete this caption first.")
            elif status == "completed_not_reviewed":
                st.info("The caption has been completed but not reviewed yet.")
            elif status == "approved":
                self._render_approved_caption(video_id, output_dir, current_user, current_file)
            else:  # rejected
                self._render_rejected_caption(video_id, output_dir, current_user, prev_user, 
                            current_file, prev_file, kwargs.get('args'))
    
    def _render_approved_caption(self, video_id: str, output_dir: str, current_user: str, current_file: str):
        """Render approved caption view"""
        current_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        st.success("✅ This caption has been approved! Great job!")
        st.write("**Current Version:**")
        self._display_caption_expander(current_data, current_user, current_data.get("timestamp", "Unknown"))
    
    def _render_rejected_caption(self, video_id: str, output_dir: str, current_user: str, prev_user: str,
                            current_file: str, prev_file: str, args: Any):
        """Render rejected caption view with merged comparison"""
        # Load both current and previous captions
        current_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        prev_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
        reviewer_data = self.data_manager.load_data(video_id, output_dir, self.data_manager.REVIEWER_FILE_POSTFIX)
        
        st.subheader("Caption Comparison")
        
        # Display metadata information
        current_timestamp = self.data_manager.format_timestamp(current_data.get("timestamp", "Unknown"))
        prev_timestamp = self.data_manager.format_timestamp(prev_data.get("timestamp", "Unknown"))
        
        st.write(f"**Annotator:** {prev_user} on {prev_timestamp}")
        st.write(f"**Reviewer:** {current_user} on {current_timestamp}")
        
        st.warning("❌ This caption was rejected and needs to be fixed.")
        
        # Create tabs with the merged comparison and individual versions
        tab1, tab2, tab3 = st.tabs([
            "📊 Comparison", "👤 Annotator Version", "🔍 Reviewer Version"
        ])
        
        with tab1:
            st.subheader("📊 Caption Comparison")
            
            # 1. Pre-caption (always visible)
            st.write("##### 1. Pre-caption")
            st.text(prev_data.get("pre_caption", "No pre-caption available"))
            
            # 2. Annotator's feedback and final caption (expandable)
            annotator_score = prev_data.get("initial_caption_rating_score", "N/A")
            with st.expander(f"##### 2. 👤 {prev_user}'s Feedback and Caption", expanded=True):
                st.write(f"**Final Feedback ({annotator_score}/5):**")
                st.text(prev_data.get("final_feedback", "No final feedback available"))
                
                st.write("**Final Caption:**")
                st.text(prev_data.get("final_caption", "No caption available"))
            
            # 3. Reviewer's feedback and final caption (expandable) - highlighted
            reviewer_score = current_data.get("initial_caption_rating_score", "N/A")
            with st.expander(f"🔍 {current_user}'s Feedback and Caption (Reviewer)", expanded=True):
                st.markdown(f"<span style='color: #ff6b35; font-weight: bold;'>Reviewer's Work</span>", unsafe_allow_html=True)
                st.write(f"**Final Feedback ({reviewer_score}/5):**")
                st.text(current_data.get("final_feedback", "No final feedback available"))
                
                st.write("**Final Caption:**")
                st.text(current_data.get("final_caption", "No caption available"))
            
            # 4. Regrade Request Interface (only for original annotator)
            logged_in_user = st.session_state.get('logged_in_user', '')
            if logged_in_user == prev_user:  # Only original annotator can request regrade
                st.markdown("---")
                st.info("💬 If you believe this rejection was incorrect, you can request a regrade:")
                self._render_regrade_request_interface(video_id, output_dir, prev_user, current_user, args)
            
        with tab2:
            st.subheader(f"👤 {prev_user}'s Version")
            self._display_caption_expander(prev_data, prev_user, prev_data.get('timestamp', ''))
            
        with tab3:
            st.subheader(f"🔍 {current_user}'s Version")
            self._display_caption_expander(current_data, current_user, current_data.get('timestamp', ''))

    def _render_regrade_request_interface(self, video_id: str, output_dir: str, annotator_name: str, reviewer_name: str, args: Any):
        """Render the regrade request interface"""
        
        with st.expander("📧 Request Regrade", expanded=False):
            st.write("**Explain why you believe the rejection was incorrect:**")
            st.write("This will generate an email template that you can send to the reviewer and meta-reviewer.")
            
            regrade_reason = st.text_area(
                "Your reason for requesting a regrade:",
                placeholder="Please explain why you think your original work was better than the reviewer's changes. Be specific about which aspects you disagree with and why.",
                height=150,
                key=f"regrade_reason_{video_id}"
            )
            
            # Generate button
            if st.button("📧 Generate Email Template", key=f"generate_regrade_{video_id}", use_container_width=True):
                if regrade_reason.strip():
                    email_data = self._generate_regrade_email_data(
                        video_id, output_dir, annotator_name, reviewer_name, regrade_reason, args
                    )
                    
                    st.session_state[f"email_data_{video_id}"] = email_data
                    st.success("✅ Email template generated!")
                    st.rerun()
                else:
                    st.warning("Please provide a reason for the regrade request.")
            
            # Email options (show only if template is generated)
            # Email options (show only if template is generated)
            if f"email_data_{video_id}" in st.session_state:
                email_data = st.session_state[f"email_data_{video_id}"]
                
                st.markdown("**📧 Send Regrade Request:**")
                
                # Direct links to email services
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.link_button("Gmail", "https://mail.google.com/mail/u/0/#inbox?compose=new", use_container_width=True)
                
                with col2:
                    st.link_button("Outlook", "https://outlook.live.com/mail/0/deeplink/compose", use_container_width=True)
                
                with col3:
                    st.link_button("Other Email", "https://www.google.com/search?q=email+compose", use_container_width=True)
                
                st.caption("↑ Click to open your email service, then copy the fields below ↓")

            # Show email template if generated
            if f"email_data_{video_id}" in st.session_state:
                email_data = st.session_state[f"email_data_{video_id}"]
                
                # Clean, compact template (no subheaders)
                st.text_input("To:", value=email_data['to'], key=f"email_to_{video_id}")
                st.text_input("Subject:", value=email_data['subject'], key=f"email_subject_{video_id}")
                st.text_area("Body:", value=email_data['body'], height=300, key=f"email_body_{video_id}")
                
                st.success("💡 Copy the fields above and paste into your email!")

    def _get_meta_reviewer_email(self, reviewer_name: str) -> str:
        """Get the meta-reviewer emails and avoid duplicates"""
        # Get meta-reviewer email using helper method
        meta_reviewer_names = AuthManager.get_all_meta_reviewers()
        meta_reviewer_emails = [AuthManager.get_user_email(name) for name in meta_reviewer_names if name != reviewer_name]
        meta_reviewer_email_str = "; ".join(meta_reviewer_emails)
        
        return meta_reviewer_email_str


    def _generate_regrade_email_data(self, video_id: str, output_dir: str, annotator_name: str, reviewer_name: str,
                                   regrade_reason: str, args: Any) -> Dict[str, str]:
        """Generate email data for regrade request"""
        
        # Load data
        prev_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.PREV_FEEDBACK_FILE_POSTFIX)
        current_feedback = self.data_manager.load_data(video_id, output_dir, self.data_manager.FEEDBACK_FILE_POSTFIX)
        
        # Get user info
        annotator_email = AuthManager.get_user_email(annotator_name) or "unknown@email.com"
        reviewer_email = AuthManager.get_user_email(reviewer_name) or "unknown@email.com"
        
        # Get video info
        video_urls = st.session_state.get("video_urls", [])
        selected_video = None
        video_index = "Unknown"
        
        # Find current video in the list
        for i, url in enumerate(video_urls):
            if self.data_manager.get_video_id(url) == video_id:
                selected_video = url
                video_index = str(i)
                break
        
        video_name = selected_video.split("/")[-1] if selected_video else "Unknown Video"
        
        # Convert HuggingFace download URL to viewable URL
        viewable_video_url = self._convert_to_viewable_url(selected_video)
        
        # Get sheet name using helper method
        sheet_name = self._get_sheet_name()
        
        # Get task name using helper method
        task_name = self._get_task_name()

        # Get meta-reviewer email using helper method
        meta_reviewer_email_str = self._get_meta_reviewer_email(reviewer_name)
        
        # Build email components
        to_field = f"{reviewer_email}; {meta_reviewer_email_str}"
        subject_field = f"Regrade Request - {video_name} - {task_name}"
        
        body_field = f"""Dear {reviewer_name} and Meta-Reviewer,

I am requesting a regrade for the rejected caption below. I believe my original work was incorrectly rejected.

=== VIDEO INFORMATION ===
URL: {viewable_video_url}
Sheet: {sheet_name}
Video: {video_index}. {video_name}
Task: {task_name}

=== PRE-CAPTION ===
{prev_feedback.get('pre_caption', 'No pre-caption available') if prev_feedback else 'No pre-caption available'}

=== MY ORIGINAL WORK ({annotator_name}) ===
Final Feedback ({prev_feedback.get('initial_caption_rating_score', 'N/A') if prev_feedback else 'N/A'}/5):
{prev_feedback.get('final_feedback', 'No feedback available') if prev_feedback else 'No feedback available'}

Final Caption:
{prev_feedback.get('final_caption', 'No caption available') if prev_feedback else 'No caption available'}

=== REVIEWER'S WORK ({reviewer_name}) ===
Final Feedback ({current_feedback.get('initial_caption_rating_score', 'N/A') if current_feedback else 'N/A'}/5):
{current_feedback.get('final_feedback', 'No feedback available') if current_feedback else 'No feedback available'}

Final Caption:
{current_feedback.get('final_caption', 'No caption available') if current_feedback else 'No caption available'}

=== REASON FOR REGRADE REQUEST ===
{regrade_reason}

I would appreciate your reconsideration of this rejection. Please let me know if you need any additional information.

Best regards,
{annotator_name}
{annotator_email}"""
        
        return {
            "to": to_field,
            "subject": subject_field,
            "body": body_field
        }

    def _convert_to_viewable_url(self, url: str) -> str:
        """Convert HuggingFace download URL to viewable URL"""
        if not url:
            return "Unknown URL"
        
        # Check if it's a HuggingFace dataset URL
        if "huggingface.co/datasets" in url and "/resolve/main/" in url:
            # Convert from: https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/-2uIa-XMJC0.3.0.mp4
            # To: https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/-2uIa-XMJC0.3.0.mp4?download=true
            # parts = url.split("/resolve/main/")
            # if len(parts) == 2:
            #     base_url = parts[0]
            #     filename = parts[1]
            #     return f"{base_url}/viewer/main?path={filename}"
            new_url = url + "?download=true"
            return new_url
        
        # Return original URL if not HuggingFace or different format
        return url

    def _get_sheet_name(self) -> str:
        """Get the current sheet name from session state"""
        # Debug: Print all session state keys
        # print("DEBUG: All session state keys:", list(st.session_state.keys()))
        # print("DEBUG: Login method:", st.session_state.get("login_method"))
        # print("DEBUG: Target annotator:", st.session_state.get("target_annotator"))
        # print("DEBUG: Selected sheet file:", st.session_state.get("selected_sheet_file"))
        
        # Check if we're in annotator mode
        if st.session_state.get("login_method") == "annotator":
            target_annotator = st.session_state.get("target_annotator", "")
            if target_annotator:
                return f"Videos by {target_annotator}"
        
        # Try to find stored sheet name (now properly stored from auth.py)
        if "selected_sheet_file" in st.session_state:
            sheet_file = st.session_state["selected_sheet_file"]
            filename = os.path.basename(sheet_file)
            return filename  # Get just the filename
        
        # Fallback
        print("DEBUG: Using fallback sheet name")
        return "Current Video Sheet"

    def _get_task_name(self) -> str:
        """Get the current task name from session state"""
        # Check which portal we're in and use the appropriate key
        if "selected_config_review" in st.session_state:
            # We're in review portal
            return st.session_state["selected_config_review"]
        elif "selected_config" in st.session_state:
            # We're in caption portal  
            return st.session_state["selected_config"]
        elif "last_config_id" in st.session_state:
            # Fallback to last config
            return st.session_state["last_config_id"]
        
        return "Current Task"

    def _display_caption_expander(self, data: Dict[str, Any], user: str, timestamp: str):
        """Helper function to display caption information"""
        st.write("##### Annotator")
        st.write(f"**Annotator:** {user}")
        st.write(f"**Timestamp:** {self.data_manager.format_timestamp(timestamp)}")
        st.write("##### Pre-caption")
        st.text(data.get("pre_caption", "No pre-caption available"))
        
        # Use the existing display_feedback_info function
        self.ui.display_feedback_info(data, display_pre_caption_instead_of_final_caption=False)
    
    def display_accuracy_statistics(self, config_names: List[str], config_dict: Dict[str, Any], 
                                   video_urls: List[str], output_dir: str):
        """Display accuracy statistics for all configs in an expander"""
        with st.expander("📊 Accuracy Statistics", expanded=False):
            # Calculate stats for all configs
            all_stats = {}
            for config_name in config_names:
                config = config_dict[config_name]
                config_output_dir = str(Path(output_dir) / config["output_name"])
                if not Path(config_output_dir).exists():
                    continue
                stats = self._calculate_accuracy_stats(video_urls, config_output_dir)
                if stats:
                    all_stats[config_name] = stats
            
            if not all_stats:
                st.info("No completed videos found for any task.")
            else:
                # Create tabs for each task
                task_tabs = st.tabs([self.ui.config_names_to_short_names[config_name] 
                                   for config_name in all_stats.keys()])
                
                # Add content to each tab
                for tab, (config_name, stats) in zip(task_tabs, all_stats.items()):
                    with tab:
                        self._render_accuracy_table(stats)
    
    def _calculate_accuracy_stats(self, video_urls: List[str], output_dir: str) -> Dict[str, Dict[str, Any]]:
        """Calculate accuracy statistics for all videos in the given directory"""
        stats = {}
        
        for video_url in video_urls:
            video_id = self.data_manager.get_video_id(video_url)
            status, _, prev_file, current_user, prev_user = self.data_manager.get_video_status(video_id, output_dir)
            
            # Skip if not completed
            if status == "not_completed":
                continue
                
            # Determine the annotator (original caption creator)
            annotator = prev_user if prev_file else current_user
            if annotator is None:
                print(f"annotator is None for video {video_id}")
                continue
                
            # Initialize annotator stats if not exists
            if annotator not in stats:
                stats[annotator] = {
                    'total_completed': 0,
                    'total_reviewed': 0,
                    'approved': 0,
                    'rejected': 0,
                    'accuracy': 0.0
                }
            
            # Update total completed
            stats[annotator]['total_completed'] += 1
            
            # Update reviewed stats if applicable
            if status in ["approved", "rejected"]:
                stats[annotator]['total_reviewed'] += 1
                if status == "approved":
                    stats[annotator]['approved'] += 1
                else:  # rejected
                    stats[annotator]['rejected'] += 1
        
        # Calculate accuracy for each annotator
        for annotator in stats:
            total = stats[annotator]['total_reviewed']
            if total > 0:
                stats[annotator]['accuracy'] = stats[annotator]['approved'] / total
        
        return stats
    
    def _render_accuracy_table(self, stats: Dict[str, Dict[str, Any]]):
        """Render accuracy statistics table"""
        # Create markdown table string
        table_str = "| Annotator | Total Completed | Total Reviewed | Approved | Rejected | Accuracy |\n"
        table_str += "|-----------|----------------|----------------|----------|----------|----------|\n"
        
        # Add data rows for each annotator
        for annotator, data in sorted(stats.items()):
            if data['total_reviewed'] > 0:
                table_str += (f"| {annotator} | {data['total_completed']} | {data['total_reviewed']} | "
                            f"{data['approved']} | {data['rejected']} | {data['accuracy']:.1%} |\n")
            else:
                table_str += (f"| {annotator} | {data['total_completed']} | 0 | 0 | 0 | N/A |\n")
        
        # Display the table
        st.markdown(table_str)
    
    def display_feedback_differences(self, prev_feedback: Dict[str, Any], feedback_data: Dict[str, Any], 
                                   diff_prompt: Optional[str] = None, reviewer_data: Optional[Dict[str, Any]] = None):
        """Display differences between current and previous feedback"""
        if not prev_feedback or not feedback_data:
            st.error("Previous feedback or current feedback does not exist. Please report this bug to Zhiqiu Lin.")
            return
        
        # Check if feedback is duplicated (rejected but not corrected)
        annotator_name = prev_feedback.get("user", "Unknown annotator")
        reviewer_name = (reviewer_data.get("reviewer_name", feedback_data.get("user", "Unknown reviewer")) 
                        if reviewer_data else feedback_data.get("user", "Unknown reviewer"))
        
        if prev_feedback == feedback_data:
            st.error(f"⚠️ **{annotator_name}'s** caption was rejected by **{reviewer_name}** "
                    f"but hasn't been corrected yet. Please ask **{reviewer_name}** to correct the caption.")
            return
        
        st.info(f"Displaying differences between **{annotator_name}'s** and **{reviewer_name}'s** feedback")
        
        st.write(f"##### **{annotator_name}'s** Original Feedback (GPT Polished then Finalized)")
        st.text(prev_feedback.get("final_feedback", "No final feedback available"))
        
        st.write(f"##### **{reviewer_name}'s** Feedback (GPT Polished then Finalized)")
        st.text(feedback_data.get("final_feedback", "No final feedback available"))
        
        # st.write("##### Summary of Differences")
        # st.markdown(self.ui.highlight_differences(
        #     prev_feedback.get("gpt_feedback", ""), 
        #     feedback_data.get("gpt_feedback", ""), 
        #     run_length=5
        # ), unsafe_allow_html=True)
        
        # st.write("##### ChatGPT summary of differences")
        # if diff_prompt:
        #     self.ui.highlight_differences_gpt(
        #         prev_feedback.get("gpt_feedback", ""),
        #         feedback_data.get("gpt_feedback", ""),
        #         diff_prompt=str(self.data_manager.folder / diff_prompt),
        #         diff_key="gpt_feedback_diff_feedback",
        #         llm_key="gpt_feedback_diff_compare_llm",
        #         prompt_key="gpt_feedback_diff_compare_prompt",
        #         old_feedback=prev_feedback.get("gpt_feedback", ""),
        #         new_feedback=feedback_data.get("gpt_feedback", "")
        #     )
    
    def display_caption_differences(self, prev_feedback: Dict[str, Any], feedback_data: Dict[str, Any], 
                                  diff_prompt: Optional[str] = None, reviewer_data: Optional[Dict[str, Any]] = None):
        """Display differences between current and previous captions"""
        if not prev_feedback or not feedback_data:
            st.error("Previous feedback or current feedback does not exist. Please report this bug to Zhiqiu Lin.")
            return
        
        # Check if feedback is duplicated (rejected but not corrected)
        annotator_name = prev_feedback.get("user", "Unknown annotator")
        reviewer_name = (reviewer_data.get("reviewer_name", feedback_data.get("user", "Unknown reviewer")) 
                        if reviewer_data else feedback_data.get("user", "Unknown reviewer"))
        
        if prev_feedback == feedback_data:
            st.error(f"⚠️ **{annotator_name}'s** caption was rejected by **{reviewer_name}** "
                    f"but hasn't been corrected yet. Please ask **{reviewer_name}** to correct the caption.")
            return
        
        st.info(f"Displaying differences between **{annotator_name}'s** and **{reviewer_name}'s** captions")
        
        st.write(f"##### **{annotator_name}'s** Original Caption")
        st.text(prev_feedback.get("final_caption", "No caption available"))
        
        st.write(f"##### **{reviewer_name}'s** Revised Caption")
        st.text(feedback_data.get("final_caption", "No caption available"))
        
        # st.write("##### Summary of Differences")
        # st.markdown(self.ui.highlight_differences(
        #     prev_feedback.get("final_caption", ""), 
        #     feedback_data.get("final_caption", ""), 
        #     run_length=5
        # ), unsafe_allow_html=True)
        
        # st.write("##### ChatGPT summary of differences")
        # if diff_prompt:
        #     self.ui.highlight_differences_gpt(
        #         prev_feedback.get("final_caption", ""),
        #         feedback_data.get("final_caption", ""),
        #         diff_prompt=str(self.data_manager.folder / diff_prompt),
        #         diff_key="final_caption_diff_feedback",
        #         llm_key="final_caption_diff_compare_llm",
        #         prompt_key="final_caption_diff_compare_prompt",
        #         old_caption=prev_feedback.get("final_caption", ""),
        #         new_caption=feedback_data.get("final_caption", "")
        #     )