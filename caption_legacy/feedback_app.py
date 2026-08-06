# caption/feedback_app.py
import streamlit as st
import argparse
from streamlit_feedback import streamlit_feedback
from streamlit import fragment
import os
import torch
import json
import difflib
import html
from diff_match_patch import diff_match_patch
import re
from datetime import datetime
from pathlib import Path
from utils import extract_frames, load_config, load_json, get_last_frame_index
from llm import get_llm, get_all_llms, get_supported_mode
from caption_policy.prompt_generator import SubjectPolicy, ScenePolicy, SubjectMotionPolicy, SpatialPolicy, CameraPolicy, VanillaCameraMotionPolicy, RawSpatialPolicy, RawSubjectMotionPolicy
from process_json import json_to_video_data
import time

def feedback_interface(video_id, config, output_dir, caption_program, video_data_dict, selected_video, args, selected_config, config_dict):
    with st.container(height=CONTAINER_HEIGHT, border=True):
        # Step 0: Generating Pre-caption
        if st.session_state.current_step == 0:
            # If feedback already exists, load it
            if data_is_saved(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
                feedback_data = load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                current_user = st.session_state.logged_in_user
                # Display detailed feedback information in an expander
                is_approved_reviewer = current_user in APPROVED_REVIEWERS
                with st.expander("Reviewer: Please Review Caption Here", expanded=is_approved_reviewer):
                    display_feedback_info(feedback_data, display_pre_caption_instead_of_final_caption=True)
                    # Reviewer interface
                    reviewer_data = load_data(video_id, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                    current_user = st.session_state.logged_in_user
                    
                    if not is_approved_reviewer:
                        st.write("##### Reviewer Status")
                        st.write(f"You are **{current_user}**. You are not an approved reviewer.")
                    else:
                        if reviewer_data is None:
                            st.write("##### Reviewer Status")
                            st.write(f"You are **{current_user}**. You can review (double check) this caption.")
                            if not can_reviewer_redo(video_id, output_dir, current_user):
                                st.error("You cannot review this caption because you are the annotator.")
                            else:
                                review_col1, review_col2 = st.columns(2)
                                with review_col1:
                                    if st.button("⚠️ Reject and Redo", 
                                        help="Reject the current caption and create a new version"):
                                        handle_rejection(video_id, output_dir, current_user)
                                with review_col2:
                                    if st.button("Approve", 
                                        help="Mark the caption as correct"):
                                        reviewer_data = {
                                            "reviewer_name": current_user,
                                            "review_timestamp": datetime.now().isoformat(),
                                            "reviewer_double_check": True
                                        }
                                        save_data(video_id, reviewer_data, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
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
                                if not can_reviewer_redo(video_id, output_dir, current_user):
                                    st.error("You cannot review this caption because you are the annotator.")
                                    return
                                st.write("This caption is approved. You can still reject by clicking the button below.")
                                if st.button("⚠️ Reject and Redo", 
                                        help="Reject the current caption and create a new version",
                                        key="reject_and_redo_approved"):
                                    handle_rejection(video_id, output_dir, current_user)
                            else:
                                if not can_reviewer_redo(video_id, output_dir, current_user):
                                    st.error("You cannot review this caption because you are the annotator.")
                                    prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                                    feedback_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                                    display_feedback_differences(
                                        prev_feedback=prev_feedback,
                                        feedback_data=feedback_data,
                                        diff_prompt=args.diff_prompt,
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
                                        prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                                        if not prev_feedback:
                                            st.error("Cannot revert: Previous feedback does not exist.")
                                        else:
                                            # Update reviewer data
                                            reviewer_data = {
                                                "reviewer_name": current_user,
                                                "review_timestamp": datetime.now().isoformat(),
                                                "reviewer_double_check": True
                                            }
                                            save_data(video_id, reviewer_data, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                                            
                                            # Replace current feedback with previous
                                            save_data(video_id, prev_feedback, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                                            
                                            # Delete previous feedback file
                                            print(f"Deleting previous feedback file: {get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)}")
                                            os.remove(get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX))
                                            st.rerun()
                                # Print the previous final caption
                                prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                                st.write(f"##### Previous Final Caption")
                                st.write(prev_feedback.get("final_caption", "No previous final caption found."))
                
                annotator, reviewer = get_annotator_and_reviewer(video_id, output_dir)
                # Check if current user is a reviewer and status is approved
                reviewer_data = load_data(video_id, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
                # Check if current user is the annotator
                if annotator == current_user:
                    if not can_annotator_redo(video_id, output_dir, current_user):
                        if reviewer_data.get("reviewer_double_check", False):
                            st.success("This caption has been approved. You don't need to modify it further.")
                        else:
                            st.error("This caption has been rejected. Please see the difference between your feedback and reviewer feedback below:")
                            prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
                            feedback_data = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                            display_feedback_differences(
                                prev_feedback=prev_feedback,
                                feedback_data=feedback_data,
                                diff_prompt=args.diff_prompt,
                                reviewer_data=reviewer_data
                            )
                        return
                
                # Check if current user is a different annotator
                elif current_user not in APPROVED_REVIEWERS:
                    st.error("You are not an approved reviewer. Please reach out to Zhiqiu Lin if you want to review/redo this caption.")
                    return
                
                elif not reviewer_data:
                    st.error("This caption has not been reviewed yet. Please review it first before making modifications.")
                    return
                
                elif reviewer_data.get("reviewer_double_check", False):
                    st.success("This caption has been approved. You don't need to modify it further.")
                    return
                # If reviewer data exists but not approved, allow proceeding
                
                st.write("Feedback already exists for this video. You can choose to restart by either re-generating the pre-caption or by providing a new rating.")
            
            # if not allow_redo:
            #     st.error("You cannot redo this caption. Please contact Zhiqiu Lin if you think this is an error.")
            #     return

            # If not exist, return empty dict
            existing_precaption = load_precaption(video_id, output_dir, file_postfix=PRECAPTION_FILE_POSTFIX)
            # st.write("##### Pre-caption was generated by ")
            # st.write("Please polish the prompt and select an option to generate a caption:")
            llm_names = get_all_llms()

            # Dropdown to select a config, updating session state
            selected_llm = st.selectbox(
                "Select a Model:",
                llm_names,
                # index=llm_names.index(existing_precaption.get("pre_caption_llm", get_precaption_llm_name(config_dict, selected_config))),
                index=llm_names.index(get_precaption_llm_name(config_dict, selected_config)),
                key="selected_llm"
            )
            supported_modes = get_supported_mode(selected_llm)
            # supprted_modes_index = supported_modes.index(existing_precaption.get("pre_caption_mode", supported_modes[0])) if existing_precaption.get("pre_caption_mode", supported_modes[0]) in supported_modes else 0
            supprted_modes_index = 0
            selected_mode = st.selectbox(
                "Select a Mode:",
                supported_modes, 
                index=supprted_modes_index,
                key="selected_mode"
            )

            if "pre_caption_prompt" in st.session_state:
                pre_caption_prompt = st.session_state.pre_caption_prompt
            else:
                # pre_caption_prompt = existing_precaption.get("pre_caption_prompt", load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, args.output))
                pre_caption_prompt = load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, args.output)

            line_height = 6  # Approximate height per line in pixels
            num_lines = max(30, len(pre_caption_prompt) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height

            current_prompt = st.text_area(
                "Prompt for pre-captioning:",
                value=pre_caption_prompt,
                key="pre_caption_prompt",
                height=estimated_height,
            )

            if "pre_caption" in existing_precaption:
                pre_caption = existing_precaption["pre_caption"]
            else:
                pre_caption = generate_save_and_return_pre_caption(video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video) # TODO: Comment out this line
                # pre_caption = "**No pre-caption generated yet. Please click the button above to re-generate a pre-caption.**"

            st.session_state.pre_caption_data = {
                "video_id": video_id,
                "pre_caption_prompt": current_prompt,
                "pre_caption": pre_caption,
                "pre_caption_llm": selected_llm,
                "pre_caption_mode": selected_mode,
            }
            if st.button("Re-generate a pre-caption"):
                st.info("Be patient, this may take a while...")
                generate_save_and_return_pre_caption(video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video)
                st.rerun()  # Force a rerun to ensure clean state

            # Wait for user to confirm pre-caption by clicking on feedback
            # st.write(f"##### Pre-caption generated by {selected_llm} ({selected_mode})")
            st.write(f"##### Current pre-caption")
            st.write(pre_caption)
            st.write("#### Rate the caption (Is it accurate? Does it miss anything important?)")


            st.write("Please provide your feedback to improve this caption (if not score of 5):")
            user_feedback = st.text_area(
                "Your feedback:",
                key=f"user_feedback_{video_id}_{config['name']}",
                height=PROMPT_HEIGHT,
            )
            
            # Fetch stored initial rating if it exists
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
                feedback_is_needed = score != "😀"

                # Initialize feedback data
                st.session_state.feedback_data = {
                    "video_id": video_id,
                    "pre_caption": pre_caption,
                    "pre_caption_prompt": current_prompt,
                    "pre_caption_llm": selected_llm,
                    "pre_caption_mode": selected_mode,
                    "original_caption": pre_caption,
                    "initial_caption_rating": score,
                    "initial_caption_rating_score": emoji_to_score(score),
                    "feedback_is_needed": feedback_is_needed,
                    # "timestamp": datetime.now().isoformat(),
                    "user": st.session_state.logged_in_user,
                    # Initialize other fields as None
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
                    if args.show_feedback_prompt:
                        st.write("You can optionally change the LLM or the prompt that we used to polish your feedback. Please keep {feedback} and {pre_caption} in the prompt.")
                        llm_names = get_all_llms()
                        # Dropdown to select a config, updating session state
                        selected_feedback_llm = st.selectbox(
                            "Select a Model:",
                            llm_names,
                            key="selected_feedback_llm",
                            index=llm_names.index("gpt-4o-2024-08-06"),
                        )
                        if "cur_feedback_prompt" in st.session_state:
                            feedback_prompt = st.session_state.cur_feedback_prompt
                        else:
                            feedback_prompt = load_txt(FOLDER / args.feedback_prompt)

                        feedback_prompt = st.text_area(
                            "Prompt for polishing feedback:",
                            value=feedback_prompt,
                            key="cur_feedback_prompt",
                            height=PROMPT_HEIGHT,
                        )
                        has_user_feedback_entered_and_submitted = st.button("Submit Feedback")
                    else:
                        feedback_prompt = load_txt(FOLDER / args.feedback_prompt)
                        selected_feedback_llm = "gpt-4o-2024-08-06"
                        has_user_feedback_entered_and_submitted = True
                        
                    if has_user_feedback_entered_and_submitted:
                        st.session_state.feedback_data["initial_feedback"] = user_feedback
                        st.session_state.feedback_data["gpt_feedback_llm"] = selected_feedback_llm
                        st.session_state.feedback_data["gpt_feedback_prompt"] = feedback_prompt
                        st.session_state.current_step = 3
                        st.rerun()
                else:
                    # If happiest face, save and finish
                    st.session_state.feedback_data["final_caption"] = pre_caption
                    save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                    st.success("Caption rated as perfect! No changes needed.")
                    st.json(st.session_state.feedback_data)
                    st.session_state.current_step = 4
                    st.rerun()

        # Step 1: Rate GPT's feedback and optionally provide corrected feedback
        # if st.session_state.current_step == 1:
        #     st.session_state.current_step = 2
        #     st.rerun()

            # Comment out the below code to restore the feedback refinement prompt engineering step
            # # Wait for user to confirm pre-caption by clicking on feedback
            # st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
            # st.write(st.session_state.feedback_data["pre_caption"])
            # st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
            # st.write(f"##### Your Feedback")
            # st.write(f"{st.session_state.feedback_data['initial_feedback']}")
            # st.write(f"##### Polished Feedback from {st.session_state.feedback_data['gpt_feedback_llm']}")
            # st.write(f"{st.session_state.feedback_data['gpt_feedback']}")
            # st.subheader(f"Please Rate AI-Polished Feedback")


            # st.write("Please provide the final feedback if you are not happy with it:")

            # # Ensure final_feedback is stored persistently
            # if "final_feedback" not in st.session_state:
            #     st.session_state.final_feedback = st.session_state.feedback_data["gpt_feedback"]

            # line_height = 10  # Approximate height per line in pixels
            # num_lines = max(30, len(st.session_state.final_feedback) // 120)  # Assuming ~120 characters per line
            # estimated_height = num_lines * line_height
            # final_feedback = st.text_area(
            #     "Finalized feedback:",
            #     value=st.session_state.final_feedback,
            #     key="correct_feedback",
            #     height=estimated_height,
            # )
            # # Fetch stored feedback rating if it exists
            # if "feedback_rating" in st.session_state:
            #     score = st.session_state.feedback_rating
            # else:
            #     feedback_response = streamlit_feedback(
            #         feedback_type="faces",
            #         key="feedback_faces"
            #     )

            #     if feedback_response:
            #         st.session_state.feedback_rating = feedback_response['score']
            #         score = feedback_response['score']
            #     else:
            #         score = None  # Default to None if no response yet

            # if score:
            #     st.session_state.feedback_data["feedback_rating"] = score  # Store in feedback data
            #     st.session_state.feedback_data["feedback_rating_score"] = emoji_to_score(score)  # Store numeric rating

            #     if score != "😀":
            #         # Button Click Handling
            #         if st.button("Submit Corrected Feedback"):
            #             if final_feedback.strip():
            #                 # Persist final feedback
            #                 st.session_state.feedback_data["final_feedback"] = final_feedback
            #                 st.session_state.final_feedback = final_feedback

            #                 # Store step change in session state
            #                 st.session_state.current_step = 2
            #                 st.session_state.feedback_submitted = True  # Flag to track submission
            #             else:
            #                 st.warning("Please provide an non-empty feedback before submitting.")
            #             st.rerun()
            #     else:
            #         # If rating is happy, then directly use the GPT feedback as final feedback
            #         st.session_state.feedback_data["final_feedback"] = st.session_state.feedback_data["gpt_feedback"]
            #         st.session_state.current_step = 2
            #         st.session_state.feedback_submitted = True  # Flag to track submission

            # if st.session_state.get("feedback_submitted", False):
            #     st.session_state.current_step = 2  # Ensure next step persists
            #     st.rerun()

        # Step 2: Generate caption (intermediate step)
        # elif st.session_state.current_step == 2:
        #     ### TODO: Comment out the below code to restore the caption refinement prompt engineering step
        #     st.session_state.current_step = 3
        #     st.rerun()
            # st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
            # st.write(st.session_state.feedback_data["pre_caption"])
            # st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
            # st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
            # st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")
            # st.write("You can optionally change the LLM or the prompt that we used to polish the caption. Please keep {feedback} and {pre_caption} in the prompt.")
            # # Get the final feedback (either corrected or GPT's version)
            # final_feedback = st.session_state.feedback_data["final_feedback"]
            # pre_caption = st.session_state.feedback_data["pre_caption"]
            # # Get improved caption
            # llm_names = get_all_llms()
            # # Dropdown to select a config, updating session state
            # selected_caption_llm = st.selectbox(
            #     "Select a Model:",
            #     llm_names,
            #     key="selected_caption_llm",
            #     index=llm_names.index("gpt-4o-2024-08-06"),
            # )
            # if "cur_caption_prompt" in st.session_state:
            #     caption_prompt = st.session_state.cur_caption_prompt
            # else:
            #     caption_prompt = load_txt(FOLDER / args.caption_prompt)

            # caption_prompt = st.text_area(
            #     "Prompt for polishing caption:",
            #     value=caption_prompt,
            #     key="cur_caption_prompt",
            #     height=PROMPT_HEIGHT,
            # )
            # if st.button("Submit") and caption_prompt:
            #     st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
            #     st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
            #     # Get GPT-4 polished feedback
            #     new_caption = get_llm(
            #         model=selected_caption_llm,
            #         secrets=st.secrets,
            #     ).generate(
            #         caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
            #     )
            #     st.session_state.feedback_data["gpt_caption"] = new_caption
            #     st.session_state.current_step = 3
            #     st.rerun()

        # TODO: Old version of step 3 (updated on 2025-05-24)
        # # Step 3: Rate GPT's caption and optionally provide corrected caption (optionally to re-generate the caption)
        # elif st.session_state.current_step == 3:

        #     # Get the final feedback (either corrected or GPT's version)
        #     final_feedback = st.session_state.feedback_data["final_feedback"]
        #     pre_caption = st.session_state.feedback_data["pre_caption"]
        #     selected_caption_llm = "gpt-4o-2024-08-06"
        #     if "cur_caption_prompt" in st.session_state:
        #         caption_prompt = st.session_state.cur_caption_prompt
        #     else:
        #         caption_prompt = load_txt(FOLDER / args.caption_prompt)

        #     st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
        #     st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
        #     # Get GPT-4 polished feedback
        #     new_caption = get_llm(
        #         model=selected_caption_llm,
        #         secrets=st.secrets,
        #     ).generate(
        #         caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
        #     )
        #     st.session_state.feedback_data["gpt_caption"] = new_caption
        #     ## Done automatically to polish the caption first

        #     st.write(f"##### Final caption generated by {st.session_state.feedback_data['gpt_caption_llm']}")
        #     # Get the final feedback (either corrected or GPT's version)
        #     gpt_caption = st.session_state.feedback_data["gpt_caption"]
        #     st.write(gpt_caption)

        #     st.subheader("Rate AI-Improved Caption")

        #     st.write("Please modify the caption below (if not a perfect score of 5):")

        #     # Ensure final_caption is stored persistently
        #     if "final_caption" not in st.session_state:
        #         st.session_state.final_caption = gpt_caption

        #     line_height = 12  # Approximate height per line in pixels
        #     num_lines = max(30, len(st.session_state.final_caption) // 120)  # Assuming ~120 characters per line
        #     estimated_height = num_lines * line_height
        #     final_caption = st.text_area(
        #         "Final caption:",
        #         value=st.session_state.final_caption,
        #         key="correct_caption",
        #         height=estimated_height,
        #     )

        #     # Retrieve stored caption rating if it exists
        #     if "caption_rating" in st.session_state:
        #         score = st.session_state.caption_rating
        #     else:
        #         caption_response = streamlit_feedback(
        #             feedback_type="faces",
        #             key="caption_faces"
        #         )

        #         if caption_response:
        #             st.session_state.caption_rating = caption_response['score']
        #             score = caption_response['score']
        #         else:
        #             score = None  # Default to None if no response yet

        #     if score:
        #         st.session_state.feedback_data["caption_rating"] = score  # Persist rating
        #         st.session_state.feedback_data["caption_rating_score"] = emoji_to_score(score)  # Store numeric rating

        #         if score != "😀":
        #             # Button Click Handling
        #             if st.button("Submit Final Caption"):
        #                 if final_caption.strip():
        #                     # Persist final caption
        #                     st.session_state.feedback_data["final_caption"] = final_caption
        #                     st.session_state.final_caption = final_caption

        #                     # Save feedback data
        #                     save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        #                     st.success(f"Caption saved successfully!")
        #                     st.json(st.session_state.feedback_data)
        #                     st.session_state.caption_submitted = True
        #                     st.session_state.current_step = 4
        #                 else:
        #                     st.warning("Please provide an non-empty feedback before submitting.")
        #                 st.rerun()
        #         else:
        #             # If rating is happy, finalize caption and save
        #             st.session_state.feedback_data["final_caption"] = st.session_state.feedback_data["gpt_caption"]
        #             save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
        #             st.success(f"Caption saved successfully!")
        #             st.json(st.session_state.feedback_data)
        #             st.session_state.caption_submitted = True
        #             st.session_state.current_step = 4
        #     else:
        #         st.subheader("(Optional) Re-try a New AI-Improved Caption")
        #         st.write("If you are not happy with the current AI-improved caption, you can re-try by modifying the LLM or the prompt below.")
        #         st.write("Note: please keep {feedback} and {pre_caption} in the prompt.")
        #         # Get improved caption
        #         llm_names = get_all_llms()
        #         # Dropdown to select a config, updating session state
        #         selected_caption_llm = st.selectbox(
        #             "Select a Model:",
        #             llm_names,
        #             key="selected_caption_llm",
        #             index=llm_names.index("gpt-4o-2024-08-06"),
        #         )
        #         if "cur_caption_prompt" in st.session_state:
        #             caption_prompt = st.session_state.cur_caption_prompt
        #         else:
        #             caption_prompt = load_txt(FOLDER / args.caption_prompt)

        #         caption_prompt = st.text_area(
        #             "Prompt for polishing caption:",
        #             value=caption_prompt,
        #             key="cur_caption_prompt",
        #             height=PROMPT_HEIGHT,
        #         )
        #         if st.button("Re-generate Final Caption") and caption_prompt:
        #             st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
        #             st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
        #             # Get GPT-4 polished feedback
        #             new_caption = get_llm(
        #                 model=selected_caption_llm,
        #                 secrets=st.secrets,
        #             ).generate(
        #                 caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
        #             )
        #             st.session_state.feedback_data["gpt_caption"] = new_caption
        #             # st.session_state.current_step = 3
        #             st.rerun()
        #         st.write("Below are the original pre-caption and the final feedback for reference.")
        #         st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
        #         st.write(st.session_state.feedback_data["pre_caption"])
        #         st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
        #         st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
        #         st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")
        #     if st.session_state.get("caption_submitted", False):
        #         st.session_state.current_step = 4  # Ensure next step persists
        #         st.rerun()

        # Step 3: Rate GPT's caption and optionally provide corrected caption (optionally to re-generate the caption)
        elif st.session_state.current_step == 3:
            
            if not st.session_state.feedback_data.get("final_feedback", False):
                # Get GPT-4 polished feedback
                new_feedback = get_llm(
                    model=st.session_state.feedback_data["gpt_feedback_llm"],
                    secrets=st.secrets,
                ).generate(
                    st.session_state.feedback_data["gpt_feedback_prompt"].format(
                        feedback=st.session_state.feedback_data["initial_feedback"],
                        pre_caption=st.session_state.feedback_data["pre_caption"]),
                )
                st.session_state.feedback_data["gpt_feedback"] = new_feedback
                st.session_state.feedback_data["final_feedback"] = new_feedback

            if not st.session_state.feedback_data.get("gpt_caption", False):
                # Get the final feedback (GPT's version)
                pre_caption = st.session_state.feedback_data["pre_caption"]
                selected_caption_llm = "gpt-4o-2024-08-06"
                caption_prompt = load_txt(FOLDER / args.caption_prompt)
                st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
                st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
                # Get GPT-4 polished feedback
                new_caption = get_llm(
                    model=selected_caption_llm,
                    secrets=st.secrets,
                ).generate(
                    caption_prompt.format(feedback=st.session_state.feedback_data["final_feedback"], pre_caption=pre_caption),
                )
                st.session_state.feedback_data["gpt_caption"] = new_caption

                # TODO: By default, we assume the feedback is perfect (updated on 2025-05-24)
                perfect_score = "😀"
                st.session_state.feedback_rating = perfect_score
                st.session_state.feedback_data["feedback_rating"] = perfect_score  # Store in feedback data
                st.session_state.feedback_data["feedback_rating_score"] = emoji_to_score(perfect_score)  # Store numeric rating


            line_height = 6  # Approximate height per line in pixels
            num_lines = max(30, len(st.session_state.feedback_data["final_feedback"]) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height
            final_feedback = st.text_area(
                "Finalized feedback:",
                value=st.session_state.feedback_data["final_feedback"],
                key="correct_feedback",
                height=estimated_height,
            )

            # Create two columns
            button_col1, button_col2 = st.columns([1, 1])

            with button_col1:
                if st.button("Only Re-generate Caption"):
                    if final_feedback.strip():
                        # Persist final feedback
                        st.session_state.feedback_data["final_feedback"] = final_feedback
                        del st.session_state.feedback_data["gpt_caption"]
                    else:
                        st.warning("Please provide an non-empty feedback before submitting.")
                    st.rerun()

            with button_col2:
                if st.button("Re-polish Feedback + Re-generate Caption"):
                    if final_feedback.strip():
                        st.session_state.feedback_data["initial_feedback"] = final_feedback
                        st.session_state.feedback_data["final_feedback"] = None
                        del st.session_state.feedback_data["gpt_caption"]
                    else:
                        st.warning("Please provide an non-empty feedback before submitting.")
                    st.rerun()


            # st.write(f"##### Final caption generated by {st.session_state.feedback_data['gpt_caption_llm']}")
            # gpt_caption = st.session_state.feedback_data["gpt_caption"]
            # st.write(gpt_caption)

            # st.subheader("Rate AI-Improved Caption")

            # st.write("Please modify the caption below (if not a perfect score of 5):")

            # Ensure final_caption is stored persistently
            # if not st.session_state.feedback_data.get("final_caption", False):
            #     st.session_state.feedback_data["final_caption"] = st.session_state.feedback_data["gpt_caption"]

            line_height = 12  # Approximate height per line in pixels
            num_lines = max(30, len(st.session_state.feedback_data["gpt_caption"]) // 120)  # Assuming ~120 characters per line
            estimated_height = num_lines * line_height
            final_caption = st.text_area(
                "Final caption:",
                value=st.session_state.feedback_data["gpt_caption"],
                key="correct_caption",
                height=estimated_height,
            )

            # TODO: By default, we assume the caption is perfect (updated on 2025-05-24)
            perfect_score = "😀"
            st.session_state.feedback_data["caption_rating"] = perfect_score  # Persist rating
            st.session_state.feedback_data["caption_rating_score"] = emoji_to_score(perfect_score)  # Store numeric rating

            # Button Click Handling
            if st.button("I am happy with both feedback and caption"):
                if final_caption.strip() and final_feedback.strip():
                    # Persist final caption
                    st.session_state.feedback_data["final_caption"] = final_caption
                    st.session_state.feedback_data["final_feedback"] = final_feedback
                    # Save feedback data
                    save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                    st.success(f"Feedback and caption saved successfully!")
                    st.session_state.current_step = 4
                else:
                    st.warning("Please provide an non-empty caption and feedback before submitting.")
                st.rerun()
            else:
                st.write("Below is the original pre-caption for reference.")
                st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
                st.write(st.session_state.feedback_data["pre_caption"])
                st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
                # st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
                # st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")


        # Step 4: Print the final caption, and say if want to redo, please go to another video then come back
        elif st.session_state.current_step == 4:
            # st.write(f"##### Final Caption")
            st.write(st.session_state.feedback_data["final_caption"])
            st.success("Feedback and caption saved successfully! To redo, please go to another video then come back.")
            st.json(st.session_state.feedback_data)


def save_annotators_to_files(annotators_dict, output_dir="annotator"):
    """Save annotators dictionary to individual JSON files.
    
    Args:
        annotators_dict: Dictionary of annotators with their passwords
        output_dir: Directory to save the JSON files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each annotator to a separate file
    for name, data in annotators_dict.items():
        # Convert name to a safe filename
        safe_name = name.lower().replace(" ", "_")
        filename = os.path.join(output_dir, f"{safe_name}.json")
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump({name: data}, f, indent=4)
        print(f"Saved annotator data to {filename}")

def load_annotators_from_files(input_dir="annotator"):
    """Load annotators from individual JSON files.
    
    Args:
        input_dir: Directory containing the JSON files
        
    Returns:
        Dictionary of annotators with their passwords
    """
    annotators = {}
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        print(f"Warning: Annotator directory {input_dir} does not exist")
        return annotators
    
    # Load each JSON file
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    annotators.update(data)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
    
    return annotators

# Load annotators from files
ANNOTATORS = load_annotators_from_files()

# # If no annotators loaded, use default dictionary
# if not ANNOTATORS:
#     ANNOTATORS = {
#         "Siyuan Cen": {"password": "siyuan"},
#         "Yuhan Huang": {"password": "yuhan"},
#         "Irene Pi": {"password": "irene"},
#         "Hewei Wang": {"password": "hewei"},
#         "Yubo Wang": {"password": "yubo"},
#         "Zida Zhou": {"password": "zida"},
#         "Zhenye Luo": {"password": "zhenye"},
#         "Mingyu Wang": {"password": "mingyu"},
#         "Chancharik Mitra": {"password": "chancharik"},
#         "Tiffany Ling": {"password": "tiffany"},
#         "Sunny Guo": {"password": "sunny"},
#         "Xianya Dai": {"password": "xianya"},
#         "Kaibo Yang": {"password": "kaibo"},
#         "Tina Xu": {"password": "tina"},
#         "Shihang Zhu": {"password": "shihang"},
#         "Zhiqiu Lin": {"password": "zhiqiu"},
#         "Test User": {"password": "test"}
#     }
#     # Save default annotators to files
#     save_annotators_to_files(ANNOTATORS)

APPROVED_REVIEWERS = ["Zhiqiu Lin", "Siyuan Cen", "Yuhan Huang", "Hewei Wang", "Tiffany Ling", "Isaac Li", "Shihang Zhu"]
assert set(APPROVED_REVIEWERS) <= set(ANNOTATORS.keys()), "All approved reviewers must be in the ANNOTATORS dictionary"

caption_programs = {
    "subject_description": SubjectPolicy(),
    "scene_composition_dynamics": ScenePolicy(),
    "subject_motion_dynamics": SubjectMotionPolicy(),
    "spatial_framing_dynamics": SpatialPolicy(),
    "camera_framing_dynamics": CameraPolicy(),
    # "camera_motion": VanillaCameraMotionPolicy(),
    # "raw_spatial_framing_dynamics": RawSpatialPolicy(),
    # "raw_subject_motion_dynamics": RawSubjectMotionPolicy(),
}

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

PRECAPTION_FILE_POSTFIX = "_precaption.json"
FEEDBACK_FILE_POSTFIX = "_feedback.json"
# PREV_FEEDBACK_FILE_POSTFIX = "_feedback_prev.json"
PREV_FEEDBACK_FILE_POSTFIX = FEEDBACK_FILE_POSTFIX.replace("feedback", "feedback_prev")
REVIEWER_FILE_POSTFIX = "_review.json"
PREV_REVIEWER_FILE_POSTFIX = REVIEWER_FILE_POSTFIX.replace("review", "review_prev")
SUBJECT_CAPTION_NAME = "Subject Description Caption"
SCENE_CAPTION_NAME = "Scene Composition and Dynamics Caption"
PROMPT_HEIGHT = 225
CONTAINER_HEIGHT = 1100
# Get the directory where this script is located
FOLDER = Path(__file__).parent

DEFAULT_VIDEO_URLS_FILES = [
    "video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json",
    "video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json",
    "video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json",
    "video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json",
    "video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json",
    "video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json",
    "video_urls/20250227_0507ground_and_setup/overlap_564_to_658.json",
    "video_urls/20250227_0507ground_and_setup/overlap_658_to_752.json",
    "video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json",
    "video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json",
    "video_urls/20250406_setup_and_motion/overlap_940_to_950.json",
    "video_urls/20250406_setup_and_motion/overlap_950_to_960.json",
    "video_urls/20250406_setup_and_motion/overlap_960_to_970.json",
    "video_urls/20250406_setup_and_motion/overlap_970_to_980.json",
    "video_urls/20250406_setup_and_motion/overlap_980_to_990.json",
    "video_urls/20250406_setup_and_motion/overlap_990_to_1000.json",
    "video_urls/20250406_setup_and_motion/overlap_1000_to_1010.json",
    "video_urls/20250406_setup_and_motion/overlap_1010_to_1020.json",
    "video_urls/20250406_setup_and_motion/0_to_10.json",
    "video_urls/20250406_setup_and_motion/10_to_20.json",
    "video_urls/20250406_setup_and_motion/20_to_30.json",
    "video_urls/20250406_setup_and_motion/30_to_40.json",
    "video_urls/20250406_setup_and_motion/40_to_50.json",
    "video_urls/20250406_setup_and_motion/50_to_60.json",
    "video_urls/20250406_setup_and_motion/60_to_70.json",   
    "video_urls/20250406_setup_and_motion/70_to_80.json",
    "video_urls/20250406_setup_and_motion/80_to_90.json",
    "video_urls/20250406_setup_and_motion/90_to_100.json",
    "video_urls/20250406_setup_and_motion/100_to_110.json",
    "video_urls/20250406_setup_and_motion/110_to_120.json",
    "video_urls/20250406_setup_and_motion/120_to_130.json",
    "video_urls/20250406_setup_and_motion/130_to_140.json",
    "video_urls/20250406_setup_and_motion/140_to_150.json",
    "video_urls/20250406_setup_and_motion/150_to_160.json",
    "video_urls/20250406_setup_and_motion/160_to_170.json",
    "video_urls/20250406_setup_and_motion/170_to_180.json",
    "video_urls/20250406_setup_and_motion/180_to_190.json",
    "video_urls/20250406_setup_and_motion/190_to_200.json",
    "video_urls/20250406_setup_and_motion/200_to_210.json",
    "video_urls/20250406_setup_and_motion/210_to_220.json",
    "video_urls/20250406_setup_and_motion/220_to_230.json",
    "video_urls/20250406_setup_and_motion/230_to_240.json",
    "video_urls/20250406_setup_and_motion/240_to_250.json",
    "video_urls/20250406_setup_and_motion/250_to_260.json",
    "video_urls/20250406_setup_and_motion/260_to_270.json",
    "video_urls/20250406_setup_and_motion/270_to_280.json",
    "video_urls/20250406_setup_and_motion/280_to_290.json",
    "video_urls/20250406_setup_and_motion/290_to_300.json",
    "video_urls/20250406_setup_and_motion/300_to_310.json",
    'video_urls/20250406_setup_and_motion/310_to_320.json',
    'video_urls/20250406_setup_and_motion/320_to_330.json',
    'video_urls/20250406_setup_and_motion/330_to_340.json',
    'video_urls/20250406_setup_and_motion/340_to_350.json',
    'video_urls/20250406_setup_and_motion/350_to_360.json',
    'video_urls/20250406_setup_and_motion/360_to_370.json',
    'video_urls/20250406_setup_and_motion/370_to_380.json',
    'video_urls/20250406_setup_and_motion/380_to_390.json',
    'video_urls/20250406_setup_and_motion/390_to_400.json',
    'video_urls/20250406_setup_and_motion/400_to_410.json',
    'video_urls/20250406_setup_and_motion/410_to_420.json',
    'video_urls/20250406_setup_and_motion/420_to_430.json',
    'video_urls/20250406_setup_and_motion/430_to_440.json',
    'video_urls/20250406_setup_and_motion/440_to_450.json',
    'video_urls/20250406_setup_and_motion/450_to_460.json',
    'video_urls/20250406_setup_and_motion/460_to_470.json',
    'video_urls/20250406_setup_and_motion/470_to_480.json',
    'video_urls/20250406_setup_and_motion/480_to_490.json',
    'video_urls/20250406_setup_and_motion/490_to_500.json',
    'video_urls/20250406_setup_and_motion/500_to_510.json',
    'video_urls/20250406_setup_and_motion/510_to_520.json',
    'video_urls/20250406_setup_and_motion/520_to_530.json',
    'video_urls/20250406_setup_and_motion/530_to_540.json',
    'video_urls/20250406_setup_and_motion/540_to_550.json',
    'video_urls/20250406_setup_and_motion/550_to_560.json',
    'video_urls/20250406_setup_and_motion/560_to_570.json',
    'video_urls/20250406_setup_and_motion/570_to_580.json',
    'video_urls/20250406_setup_and_motion/580_to_590.json',
    'video_urls/20250406_setup_and_motion/590_to_600.json',
    'video_urls/20250406_setup_and_motion/600_to_610.json',
    'video_urls/20250406_setup_and_motion/610_to_620.json',
    'video_urls/20250406_setup_and_motion/620_to_630.json',
    'video_urls/20250406_setup_and_motion/630_to_640.json',
    'video_urls/20250406_setup_and_motion/640_to_650.json',
    'video_urls/20250406_setup_and_motion/650_to_660.json',
    'video_urls/20250406_setup_and_motion/660_to_670.json',
    'video_urls/20250406_setup_and_motion/670_to_680.json',
    'video_urls/20250406_setup_and_motion/680_to_690.json',
    'video_urls/20250406_setup_and_motion/690_to_700.json',
    'video_urls/20250406_setup_and_motion/700_to_710.json',
    'video_urls/20250406_setup_and_motion/710_to_720.json',
    'video_urls/20250406_setup_and_motion/720_to_730.json',
    'video_urls/20250406_setup_and_motion/730_to_740.json',
    'video_urls/20250406_setup_and_motion/740_to_750.json',
    'video_urls/20250406_setup_and_motion/750_to_760.json',
    'video_urls/20250406_setup_and_motion/760_to_770.json',
    'video_urls/20250406_setup_and_motion/770_to_780.json',
    'video_urls/20250406_setup_and_motion/780_to_790.json',
    'video_urls/20250406_setup_and_motion/790_to_800.json',
    'video_urls/20250406_setup_and_motion/800_to_810.json',
    'video_urls/20250406_setup_and_motion/810_to_820.json',
    'video_urls/20250406_setup_and_motion/820_to_830.json',
    'video_urls/20250406_setup_and_motion/830_to_840.json',
    'video_urls/20250406_setup_and_motion/840_to_850.json',
    'video_urls/20250406_setup_and_motion/850_to_860.json',
    'video_urls/20250406_setup_and_motion/860_to_870.json',
    'video_urls/20250406_setup_and_motion/870_to_880.json',
    'video_urls/20250406_setup_and_motion/880_to_890.json',
    'video_urls/20250406_setup_and_motion/890_to_900.json',
    'video_urls/20250406_setup_and_motion/900_to_910.json',
    'video_urls/20250406_setup_and_motion/910_to_920.json',
    'video_urls/20250406_setup_and_motion/920_to_930.json',
    'video_urls/20250406_setup_and_motion/930_to_940.json',
    'video_urls/20250406_setup_and_motion/940_to_950.json',
    'video_urls/20250406_setup_and_motion/950_to_960.json',
    'video_urls/20250406_setup_and_motion/960_to_970.json',
    'video_urls/20250406_setup_and_motion/970_to_980.json',
    'video_urls/20250406_setup_and_motion/980_to_990.json',
    'video_urls/20250406_setup_and_motion/990_to_1000.json',
    'video_urls/20250406_setup_and_motion/1000_to_1010.json',
    'video_urls/20250406_setup_and_motion/1010_to_1020.json',
    'video_urls/20250406_setup_and_motion/1020_to_1030.json',
    'video_urls/20250406_setup_and_motion/1030_to_1040.json',
    'video_urls/20250406_setup_and_motion/1040_to_1050.json',
    'video_urls/20250406_setup_and_motion/1050_to_1060.json',
    'video_urls/20250406_setup_and_motion/1060_to_1070.json',
    'video_urls/20250406_setup_and_motion/1070_to_1080.json',
    'video_urls/20250406_setup_and_motion/1080_to_1090.json',
    'video_urls/20250406_setup_and_motion/1090_to_1100.json',
    'video_urls/20250406_setup_and_motion/1100_to_1110.json',
    'video_urls/20250406_setup_and_motion/1110_to_1120.json',
    'video_urls/20250406_setup_and_motion/1120_to_1130.json',
    'video_urls/20250406_setup_and_motion/1130_to_1140.json',
    'video_urls/20250406_setup_and_motion/1140_to_1150.json',
    'video_urls/20250406_setup_and_motion/1150_to_1160.json',
    'video_urls/20250406_setup_and_motion/1160_to_1170.json',
    'video_urls/20250406_setup_and_motion/1170_to_1180.json',
    'video_urls/20250406_setup_and_motion/1180_to_1183.json',
    'video_urls/20250406_setup_and_motion/overlap_invalid.json',
    'video_urls/20250406_setup_and_motion/nonoverlap_invalid.json',
]

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="all_configs.json", help="Path to the JSON config file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_all.json", help="Path to the test URLs file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_selected.json", help="Path to the test URLs file")
    parser.add_argument(
        "--video_urls_files",
        nargs="+",
        type=str,
        default=DEFAULT_VIDEO_URLS_FILES,
        help="List of paths to test URLs files",
    )
    parser.add_argument("--main_project_output", type=str, default="output_captions", help="Path to the main project output directory")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--show_feedback_prompt", type=bool, default=False, help="Whether to show and allow the annotator to edit the feedback prompt")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    parser.add_argument("--diff_prompt", type=str, default="prompts/diff_prompt.txt", help="Path to the diff prompt file")
    parser.add_argument("--diff_cap_prompt", type=str, default="prompts/diff_cap_prompt.txt", help="Path to the caption diff prompt file")
    # parser.add_argument("--video_data", type=str, default="video_data/20250224_0130/videos.json", help="Path to the video data file")
    # parser.add_argument("--video_data", type=str, default="video_data/20250227_0507ground_and_setup/videos.json", help="Path to the video data file")
    parser.add_argument("--video_data", type=str, default="video_data/20250406_setup_and_motion/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion", "cam_setup"], help="List of label collections to load from the video data")
    parser.add_argument("--personalize_output", type=bool, default=False, help="Whether to personalize the output directory based on the logged-in user")
    return parser.parse_args()

# Helper function to convert a full name to a username format
def convert_name_to_username(full_name):
    """Convert a full name to a username format (e.g., 'Siyuan Cen' to 'siyuan_cen')"""
    return full_name.lower().replace(" ", "_")

def check_video_completion_status(video_urls_file, configs, output_dir):
    """Check completion status of videos in a file.
    
    Args:
        video_urls_file: Path to the video URLs file
        configs: List of configs to check
        output_dir: Output directory to check for feedback files
        
    Returns:
        Tuple of (is_completed, is_reviewed) for each video
        Dict of "annotators" and "reviewers" with the number of videos completed and reviewed by each
    """
    video_urls = load_json(FOLDER / video_urls_file)
    status_dict = {}
    annotators_dict = {}
    reviewers_dict = {}
    
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        is_completed = True
        is_reviewed = True
        
        for config in configs:
            config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
            review_file = get_filename(video_id, config_output_dir, REVIEWER_FILE_POSTFIX)
            
            if not os.path.exists(feedback_file):
                is_completed = False
                is_reviewed = False
                break
            else:
                # Check if this annotator completed this task
                with open(feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                    annotator = feedback_data.get("user")
                    if annotator not in annotators_dict:
                        annotators_dict[annotator] = 0
                    annotators_dict[annotator] += 1
                
            if not os.path.exists(review_file):
                is_reviewed = False
            else:
                with open(review_file, 'r') as rf:
                    review_data = json.load(rf)
                    reviewer = review_data.get("reviewer_name")
                    if reviewer not in reviewers_dict:
                        reviewers_dict[reviewer] = 0
                    reviewers_dict[reviewer] += 1
                
        status_dict[video_url] = (is_completed, is_reviewed)
    
    return status_dict, annotators_dict, reviewers_dict

def get_annotator_videos(annotator_name, configs, output_dir, not_yet_reviewed=False, show_only_rejected=False):
    """Get all videos that have been completed by an annotator.
    
    Args:
        annotator_name: Name of the annotator
        configs: List of configs to check
        output_dir: Output directory to check for feedback files
        not_yet_reviewed: If True, only return videos that haven't been reviewed
        show_only_rejected: If True, only return videos that have been rejected
        
    Returns:
        List of video URLs that match the criteria, sorted by:
        - If not_yet_reviewed is True: Earliest completion time across all tasks (oldest to latest)
        - If not_yet_reviewed is False: Latest review time across all tasks (latest to oldest) for reviewed videos, followed by unreviewed videos
    """
    assert not (not_yet_reviewed and show_only_rejected), "Cannot show both not yet reviewed and show only rejected videos"
    start_time = time.time()
    
    # Get all video URLs from all files
    all_video_urls = []
    for video_urls_file in DEFAULT_VIDEO_URLS_FILES:
        video_urls = load_json(FOLDER / video_urls_file)
        all_video_urls.extend(video_urls)
    
    print(f"Found {len(all_video_urls)} total videos to check")
    
    # Filter videos based on criteria
    matching_videos = []
    video_timestamps = {}  # Store timestamps for sorting
    video_reviewed = {}  # Track which videos have been reviewed
    total_videos = len(all_video_urls)
    last_progress_time = time.time()
    
    for idx, video_url in enumerate(all_video_urls):
        video_id = get_video_id(video_url)
        has_completed_task = False
        all_tasks_reviewed = True
        is_rejected = False
        earliest_completion_time = None
        latest_review_time = None
        
        # Check each task for this video
        for config in configs:
            config_output_dir = os.path.join(FOLDER, output_dir, config["output_name"])
            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
            review_file = get_filename(video_id, config_output_dir, REVIEWER_FILE_POSTFIX)
            
            # Skip if feedback file doesn't exist
            if not os.path.exists(feedback_file):
                continue
                
            try:
                # Check if this annotator completed this task
                with open(feedback_file, 'r') as f:
                    feedback_data = json.load(f)
                    if feedback_data.get("user") == annotator_name:
                        has_completed_task = True
                        # Store completion time if available
                        if "timestamp" in feedback_data:
                            completion_time = feedback_data["timestamp"]
                            if earliest_completion_time is None or completion_time < earliest_completion_time:
                                earliest_completion_time = completion_time
                        # If feedback exists but no review file, mark as not reviewed
                        if not os.path.exists(review_file):
                            all_tasks_reviewed = False
                        else:
                            # Check if the video was rejected and get review time
                            with open(review_file, 'r') as rf:
                                review_data = json.load(rf)
                                if not review_data.get("reviewer_double_check", False):
                                    is_rejected = True
                                if "review_timestamp" in review_data:
                                    review_time = review_data["review_timestamp"]
                                    if latest_review_time is None or review_time > latest_review_time:
                                        latest_review_time = review_time
            except Exception as e:
                print(f"Error reading feedback file {feedback_file}: {e}")
                continue
        
        # Add video if it matches criteria
        if has_completed_task:
            if show_only_rejected and not is_rejected:
                continue
            if not not_yet_reviewed or not all_tasks_reviewed:
                matching_videos.append(video_url)
                # Store appropriate timestamp based on sorting criteria
                if not_yet_reviewed:
                    # For not_yet_reviewed=True, sort by earliest completion time
                    video_timestamps[video_url] = earliest_completion_time if earliest_completion_time else "0000-00-00"
                else:
                    # For not_yet_reviewed=False, sort by latest review time with unreviewed at end
                    video_timestamps[video_url] = latest_review_time if latest_review_time else "0000-00-00"
                    video_reviewed[video_url] = bool(latest_review_time)
    
    # Sort videos based on criteria
    if video_timestamps:
        if not_yet_reviewed:
            # Sort by earliest completion time (oldest to latest)
            matching_videos.sort(key=lambda x: video_timestamps.get(x, "9999-99-99"))
        else:
            # Sort by latest review time (latest to oldest) with unreviewed at end
            matching_videos.sort(key=lambda x: (
                not video_reviewed.get(x, False),  # First sort by reviewed status (False comes before True)
                video_timestamps.get(x, "0000-00-00")  # Then by timestamp
            ))
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Found {len(matching_videos)} matching videos for annotator {annotator_name}")
    print(f"Total search time: {total_time:.2f} seconds ({total_time/len(all_video_urls):.3f} seconds per video)")
    return matching_videos

def login_page(args):
    st.title("Video Caption System Login")

    # Create tabs for different login methods
    tab1, tab2 = st.tabs(["Login by Sheet", "Login by Annotator"])

    with tab1:
        # Original login by sheet form
        with st.form("login_form_sheet"):
            # Annotator selection dropdown
            selected_annotator = st.selectbox(
                "Select Your Name:",
                list(ANNOTATORS.keys()),
                key="selected_annotator_sheet",
                index=None,
                placeholder="Type or select your name...",
            )
            
            # Password input
            password = st.text_input("Enter Password:", type="password", key="password_input_sheet")
            
            # File selection dropdown with completion status if enabled
            try:
                # Load configs
                configs = load_config(FOLDER / args.configs)
                configs = [load_config(FOLDER / config) for config in configs]
                
                # Check completion status for each file
                start_time = time.time()
                file_status = {}
                for video_urls_file in args.video_urls_files:
                    status_dict, annotators_dict, reviewers_dict = check_video_completion_status(
                        video_urls_file, 
                        configs,
                        args.output
                    )
                    # Count completed and reviewed videos
                    completed = sum(1 for _, (is_completed, _) in status_dict.items() if is_completed)
                    reviewed = sum(1 for _, (_, is_reviewed) in status_dict.items() if is_reviewed)
                    total = len(status_dict)
                    annotators = len(annotators_dict)
                    reviewers = len(reviewers_dict)
                    annotator_str = ", ".join([f"{annotator} ({count})" for annotator, count in annotators_dict.items()])
                    reviewer_str = ", ".join([f"{reviewer} ({count})" for reviewer, count in reviewers_dict.items()])
                    
                    # Create status string
                    if completed == total and reviewed == total:
                        status = "✅✅"
                    elif completed == total:
                        status = "✅"
                    else:
                        status = ""
                    
                    file_status[video_urls_file] = f"{status} {os.path.basename(video_urls_file)} ({completed}/{total} completed, {reviewed}/{total} reviewed) (Annotators: {annotator_str}, Reviewers: {reviewer_str})"
                
                end_time = time.time()
                print(f"Completion status check took {end_time - start_time:.2f} seconds")
                
                # Create format function for selectbox
                def format_file_with_status(file_path):
                    return file_status.get(file_path, file_path)
                
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    args.video_urls_files,
                    key="selected_urls_file_sheet",
                    format_func=format_file_with_status
                )
            except Exception as e:
                st.error(f"Error checking completion status: {e}")
                selected_file = st.selectbox(
                    "Select Video URLs File:",
                    args.video_urls_files,
                    key="selected_urls_file_sheet"
                )

            submit_button = st.form_submit_button("Login")

            if submit_button:
                # Check if password matches
                if password == ANNOTATORS[selected_annotator]["password"]:
                    # Store the video URLs and annotator in session state
                    st.session_state.video_urls = load_json(FOLDER / selected_file)
                    st.session_state.logged_in = True
                    st.session_state.logged_in_user = selected_annotator
                    st.success(f"Login successful! Welcome, {selected_annotator}!")
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")

    with tab2:
        # New login by annotator form
        with st.form("login_form_annotator"):
            # Annotator selection dropdown for login
            selected_annotator = st.selectbox(
                "Select Your Name:",
                list(ANNOTATORS.keys()),
                key="selected_annotator_annotator",
                index=None,
                placeholder="Type or select your name...",
            )
            
            # Password input
            password = st.text_input("Enter Password:", type="password", key="password_input_annotator")
            
            # Dropdown to select which annotator's videos to search for
            target_annotator = st.selectbox(
                "Search for videos completed by:",
                list(ANNOTATORS.keys()),
                key="target_annotator_select",  # Changed key name
                index=None,
                placeholder="Type or select annotator name...",
            )
            
            # Not yet reviewed checkbox
            not_yet_reviewed = st.checkbox(
                "Show only videos not yet reviewed",
                value=True,
                key="not_yet_reviewed"
            )

            submit_button = st.form_submit_button("Login")

            if submit_button:
                # Check if password matches
                if password == ANNOTATORS[selected_annotator]["password"]:
                    try:
                        # Load configs
                        configs = load_config(FOLDER / args.configs)
                        configs = [load_config(FOLDER / config) for config in configs]
                        
                        # Get videos for the target annotator
                        start_time = time.time()
                        matching_videos = get_annotator_videos(
                            target_annotator,  # Use target_annotator instead of selected_annotator
                            configs,
                            args.output,
                            not_yet_reviewed
                        )
                        end_time = time.time()
                        print(f"Getting annotator videos took {end_time - start_time:.2f} seconds")
                        
                        if not matching_videos:
                            st.error(f"No matching videos found for annotator {target_annotator}.")
                        else:
                            # Store the matching videos and annotator in session state
                            st.session_state.video_urls = matching_videos
                            st.session_state.logged_in = True
                            st.session_state.logged_in_user = selected_annotator
                            st.success(f"Login successful! Welcome, {selected_annotator}! Found {len(matching_videos)} matching videos for {target_annotator}.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error getting annotator videos: {e}")
                else:
                    st.error("Incorrect password. Please try again.")

def load_video_data(video_data_file, label_collections=["cam_motion", "cam_setup", "lighting_setup"]):
    video_data_dict = json_to_video_data(video_data_file, label_collections=label_collections)
    for video_data in video_data_dict.values():
        if hasattr(video_data, "cam_setup"):
            video_data.cam_motion.update()
        if hasattr(video_data, "cam_setup"):
            video_data.cam_setup.update()
            if getattr(video_data.cam_setup, "subject_description", None) is None:
                video_data.cam_setup.subject_description = "**{NO DESCRIPTION FOR SUBJECTS YET}**"
            if getattr(video_data.cam_setup, "scene_description", None) is None:
                video_data.cam_setup.scene_description = "**{NO DESCRIPTION FOR SCENE YET}**"
            if getattr(video_data.cam_setup, "motion_description", None) is None:
                video_data.cam_setup.motion_description = "**{NO DESCRIPTION FOR SUBJECT MOTION YET}**"
            if getattr(video_data.cam_setup, "spatial_description", None) is None:
                video_data.cam_setup.spatial_description = "**{NO DESCRIPTION FOR SPATIAL FRAMING YET}**"
            if getattr(video_data.cam_setup, "camera_description", None) is None:
                video_data.cam_setup.camera_description = "**{NO DESCRIPTION FOR CAMERA FRAMING YET}**"
            if getattr(video_data.cam_setup, "color_description", None) is None:
                video_data.cam_setup.color_description = "**{NO DESCRIPTION FOR COLOR COMPOSITION YET}**"
            if getattr(video_data.cam_setup, "lighting_description", None) is None:
                video_data.cam_setup.lighting_description = "**{NO DESCRIPTION FOR LIGHTING SETUP YET}**"
            if getattr(video_data.cam_setup, "lighting_effects_description", None) is None:
                video_data.cam_setup.lighting_effects_description = "**{NO DESCRIPTION FOR LIGHTING EFFECTS YET}**"
        if hasattr(video_data, "lighting_setup"):
            video_data.lighting_setup.update()
    return video_data_dict


def emoji_to_score(emoji):
    """Convert emoji rating to 1-5 Likert scale"""
    emoji_map = {
        "😞": 1,  # Very unhappy
        "🙁": 2,  # Unhappy
        "😐": 3,  # Neutral
        "🙂": 4,  # Happy
        "😀": 5   # Very happy
    }
    # If not found, raise an error
    if emoji not in emoji_map:
        raise ValueError("Invalid emoji rating provided.")
    return emoji_map.get(emoji, None)  # Default to neutral if emoji not found

def get_filename(video_id, output_dir="outputs", file_postfix=".json"):
    """Get the filename for saving feedback data"""
    return os.path.join(output_dir, f'{video_id}{file_postfix}')

def save_data(video_id, data, output_dir="outputs", file_postfix=".json"):
    """Save data to a JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = get_filename(video_id, output_dir, file_postfix)
    
    # Add timestamp if not already present
    if "timestamp" not in data:
        data["timestamp"] = datetime.now().isoformat()
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to: {filename}")
    return filename


def get_precaption_llm_name(config_dict, selected_config):
    config = config_dict[selected_config]
    task = config["task"]
    if task in ["subject_motion_dynamics"]:
        # return "tarsier-recap-7b"
        # return "tarsier2-7b"
        # return "gemini-2.5-pro-preview-05-06" # TODO: change back to tarsier-recap-7b
        return "gemini-2.5-pro"
    elif task in ["spatial_framing_dynamics"]:
        # return "qwen2.5-vl-72b"
        return "gemini-2.5-pro"
    elif task in ["raw_lighting_setup_dynamics", "raw_lighting_effects_dynamics"]:
        # print(f"Using qwen2.5-vl-7b for {task}")
        # return "qwen2.5-vl-7b"
        print(f"Using gemini-2.5-pro for {task}")
        return "gemini-2.5-pro"
    else:
        # return "gpt-4o-2024-08-06"
        return "gemini-2.5-pro"

def load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, output):
    """Generate a pre-caption for the video"""
    # Get the caption prompt for the video
    config = config_dict[selected_config]
    task = config["task"]
    
    if task in ["subject_motion_dynamics"]:
        # Need to update the "subject_description" if exists
        subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
        existing_subject_feedback = load_data(video_id, output_dir=FOLDER / output / subject_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        if existing_subject_feedback:
            st.success("Loading previously generated subject caption...")
            subject_caption = existing_subject_feedback["final_caption"]
            video_data_dict[video_id].cam_setup.subject_description = subject_caption
        else:
            st.error("No subject caption found. Please generate the subject caption first.")
            st.rerun()
            raise ValueError("This line will not be run because rerun will be called.")
    elif task in ["spatial_framing_dynamics", "color_composition_dynamics", "lighting_setup_dynamics", "lighting_effects_dynamics"]:
        # Need to update both "subject_description" and "scene_composition_dynamics" if exists
        subject_output_name = config_dict[SUBJECT_CAPTION_NAME]["output_name"]
        scene_output_name = config_dict[SCENE_CAPTION_NAME]["output_name"]
        existing_subject_feedback = load_data(video_id, output_dir=FOLDER / output / subject_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        existing_scene_feedback = load_data(video_id, output_dir=FOLDER / output / scene_output_name, file_postfix=FEEDBACK_FILE_POSTFIX)
        if existing_subject_feedback and existing_scene_feedback:
            st.success("Loading previously generated subject and scene captions...")
            subject_caption = existing_subject_feedback["final_caption"]
            scene_caption = existing_scene_feedback["final_caption"]
            video_data_dict[video_id].cam_setup.subject_description = subject_caption
            video_data_dict[video_id].cam_setup.scene_description = scene_caption
        else:
            st.error("No subject and scene captions found. Please generate the subject and scene captions first.")
            st.rerun()
            raise ValueError("This line will not be run because rerun will be called.")
    
    # Generate the new prompt and caption
    pre_caption_prompt = caption_program(video_data_dict[video_id])[task]
        
    return pre_caption_prompt

def load_precaption(video_id, output_dir, file_postfix=PRECAPTION_FILE_POSTFIX):
    """Load pre-caption for video. If not exist, generate a new one."""
    # Check for existing feedback and get current caption
    existing_precaption = load_data(video_id, output_dir=output_dir, file_postfix=file_postfix)
    
    # Show existing feedback if available
    if existing_precaption:
        # st.success("Loading previously generated pre-caption...")
        # print(f"Pre-caption found for video: {video_id}")
        return existing_precaption
    else:
        st.info("No pre-caption found. Generating a new pre-caption.")
        # print(f"No pre-caption found for video: {video_id}")
        return {}

def load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
    """Load feedback for video. If not exist, generate a new one."""
    # Check for existing feedback and get current caption
    existing_feedback = load_data(video_id, output_dir=output_dir, file_postfix=file_postfix)
    existing_prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)

    # Show existing feedback if available
    if existing_feedback:
        if existing_prev_feedback:
            st.success(f"This video has already been completed by {existing_prev_feedback['user']} and reviewed by {existing_feedback['user']}. The final caption is:")
        else:
            st.success(f"This video has already been completed by {existing_feedback['user']}. The final caption is:")
        st.write(existing_feedback["final_caption"])
        # Render as collapsible text
        with st.expander("Show final JSON Data", expanded=False):
            st.json(existing_feedback)
        return existing_feedback
    else:
        st.info("No pre-caption found. Generating a new pre-caption.")
        # print(f"No pre-caption found for video: {video_id}")
        return {}

def data_is_saved(video_id, output_dir="outputs", file_postfix=".json"):
    """Check if data already exists"""
    filename = os.path.join(output_dir, f'{video_id}{file_postfix}')
    return os.path.exists(filename)

def load_data(video_id, output_dir="outputs", file_postfix=".json"):
    """Load existing feedback data for a video if it exists"""
    filename = os.path.join(output_dir, f'{video_id}{file_postfix}')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


# Get video ID from URL
def get_video_id(url):
    return url.split('/')[-1]

# Load instructions from file
def load_txt(txt_file):
    with open(txt_file, "r") as f:
        return f.read()

# Load prompt template
def load_prompt(filename, **kwargs):
    with open(filename, "r") as f:
        prompt = f.read()
    return prompt.format(**kwargs)

def generate_save_and_return_pre_caption(video_id, output_dir, prompt, selected_llm, selected_mode, selected_video, file_postfix=PRECAPTION_FILE_POSTFIX):
    print(f"Generating pre-caption for video: {video_id}")
    imagery_kwargs = get_imagery_kwargs(selected_mode, selected_video)
    try:
        pre_caption = get_llm(
            model=selected_llm,
            secrets=st.secrets,
        ).generate(
            prompt,
            **imagery_kwargs
        )
    except Exception as e:
        st.error(f"Error generating pre-caption for video: {video_id}")
        st.error(f"Error: {e}")
        # If the selected_llm is gemini-2.5-pro, prompt user to try again or use gpt-4o-2024-08-06
        if selected_llm == "gemini-2.5-pro":
            st.info("Please try again or use gpt-4o-2024-08-06 as the LLM.")
        raise e
    
    pre_caption_data = {
        "video_id": video_id,
        "pre_caption_prompt": prompt,
        "pre_caption": pre_caption,
        "pre_caption_llm": selected_llm,
        "pre_caption_mode": selected_mode,
    }
    save_data(video_id, pre_caption_data, output_dir=output_dir, file_postfix=file_postfix)
    print(f"Pre-caption generated for video: {video_id}")
    return pre_caption


def get_video_status(video_id, output_dir):
    """Get the status of a video's caption completion and previous iterations"""
    # Initialize all variables
    status = "not_completed"
    current_file = None
    prev_file = None
    current_user = None
    prev_user = None
    
    # Check all relevant files
    feedback_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    prev_feedback_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
    reviewer_file = get_filename(video_id, output_dir, REVIEWER_FILE_POSTFIX)
    
    # Determine status based on file existence and content
    if not os.path.exists(feedback_file):
        return status, current_file, prev_file, current_user, prev_user
        
    current_file = feedback_file
    with open(feedback_file, 'r') as f:
        current_data = json.load(f)
        current_user = current_data.get("user")
    
    if not os.path.exists(reviewer_file):
        status = "completed_not_reviewed"
        return status, current_file, prev_file, current_user, prev_user
    
    # Load reviewer data
    with open(reviewer_file, 'r') as f:
        reviewer_data = json.load(f)
        reviewer_double_check = reviewer_data.get("reviewer_double_check", False)
        
        if reviewer_double_check:
            status = "approved"
            # For approved files, load previous feedback if it exists
            if os.path.exists(prev_feedback_file):
                with open(prev_feedback_file, 'r') as pf:
                    prev_data = json.load(pf)
                    prev_user = prev_data.get("user")
        else:
            status = "rejected"
            # For rejected files, must have prev feedback with different user
            assert os.path.exists(prev_feedback_file), f"Rejected file {video_id} must have previous feedback"
            with open(prev_feedback_file, 'r') as pf:
                prev_data = json.load(pf)
                prev_user = prev_data.get("user")
                with open(feedback_file, 'r') as cf:
                    current_data = json.load(cf)
                    current_user = current_data.get("user")
                    if prev_user == current_user:
                        # This means the caption was just rejected but it has not been updated yet
                        # In this case, we should show the previous version and treat it as not reviewed
                        status = "completed_not_reviewed"
                        prev_user = None
                        prev_file = None
                        return status, current_file, prev_file, current_user, prev_user
        
        prev_file = prev_feedback_file if os.path.exists(prev_feedback_file) else None
    
    return status, current_file, prev_file, current_user, prev_user

def get_video_format_func(output_dir, file_postfix=".json", video_urls=None):
    def video_format_func(video_url):
        if video_urls is not None:
            video_index = video_urls.index(video_url)
        else:
            video_index = ""
        video_id = get_video_id(video_url)
        video_url = video_url.split("/")[-1]
        
        # Get status and format accordingly
        status, current_file, _, _, _ = get_video_status(video_id, output_dir)
        status_emoji_map = {
            "not_completed": "",  # Not completed - no emoji
            "completed_not_reviewed": "✅",  # Completed but not reviewed - single checkmark
            "approved": "✅✅",  # Approved - double checkmark
            "rejected": "❌"  # Rejected
        }
        
        # Get timestamps if available
        timestamp_str = ""
        if status != "not_completed":
            if current_file:
                with open(current_file, 'r') as f:
                    current_data = json.load(f)
                    if status == "completed_not_reviewed":
                        timestamp_str = f" (completed at {format_timestamp(current_data.get('timestamp', 'N/A'))})"
                    elif status == "approved" or status == "rejected":
                        reviewer_file = get_filename(video_id, output_dir, REVIEWER_FILE_POSTFIX)
                        if os.path.exists(reviewer_file):
                            with open(reviewer_file, 'r') as rf:
                                reviewer_data = json.load(rf)
                                timestamp_str = f" (reviewed at {format_timestamp(reviewer_data.get('review_timestamp', 'N/A'))})"
        
        return f"{status_emoji_map[status]}{video_index}. {video_url}{timestamp_str}"
    return video_format_func

def get_imagery_kwargs(selected_mode, selected_video):
    if selected_mode == "Text Only":
        return {}
    
    imagery_kwargs = {"video": selected_video}
    if selected_mode == "Image (First-and-Last-Frame)":
        imagery_kwargs.update({"extracted_frames": [0, -1]})
    elif selected_mode == "Image (3 frames)":
        last_idx = get_last_frame_index(selected_video)
        # Uniformly sample 3 frames: first, middle, and last
        middle_idx = last_idx // 2
        imagery_kwargs.update({"extracted_frames": [0, middle_idx, last_idx]})
    elif selected_mode == "Image (4 frames)":
        last_idx = get_last_frame_index(selected_video)
        # For 4 evenly spaced frames, divide into 3 equal segments
        segment = last_idx / 3  # Using floating point division for precision
        frame_indices = [
            0,
            int(segment),
            int(2 * segment),
            last_idx
        ]
        imagery_kwargs.update({"extracted_frames": frame_indices})
    elif selected_mode == "Video":
        pass
    return imagery_kwargs

def file_check(video_urls, video_data_dict):
    """Check if all videos in the list exist in the video data dictionary.
    
    Args:
        video_urls: List of video URLs to check
        video_data_dict: Dictionary of video data
    """
    video_ids = [get_video_id(video_url) for video_url in video_urls]
    missing_video = False
    for video_id in video_ids:
        if video_id not in video_data_dict:
            st.error(f"Video ID {video_id} not found in the video data file.")
            print(f"Video ID not found: {video_id}")
            missing_video = True
    if missing_video:
        return

def get_annotator_and_reviewer(video_id, output_dir):
    """Determine who is the annotator and who is the reviewer based on feedback files"""
    current_feedback = load_data(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
    prev_feedback = load_data(video_id, output_dir=output_dir, file_postfix=PREV_FEEDBACK_FILE_POSTFIX)
    
    if not current_feedback:
        return None, None
    
    if not prev_feedback:
        # Only current feedback exists - the user in current feedback is the annotator
        return current_feedback.get("user"), None
    
    # Both files exist - prev feedback user is annotator, current feedback user is reviewer
    return prev_feedback.get("user"), current_feedback.get("user")

def can_annotator_redo(video_id, output_dir, current_user):
    """Check if the current user (as annotator) can redo the caption"""
    annotator, reviewer = get_annotator_and_reviewer(video_id, output_dir)
    
    # If no annotator yet, anyone can be the annotator
    if not annotator:
        return True
    
    # If same annotator, check if it's been reviewed
    if annotator == current_user:
        reviewer_data = load_data(video_id, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
        return not reviewer_data  # Can redo if not reviewed yet
    
    return False

def can_reviewer_redo(video_id, output_dir, current_user):
    """Check if the current user (as reviewer) can redo the caption"""
    annotator, reviewer = get_annotator_and_reviewer(video_id, output_dir)
    
    # Must be an approved reviewer
    if current_user not in APPROVED_REVIEWERS:
        return False
    
    # Cannot review if you're the annotator
    if annotator == current_user:
        return False
    
    
    return True

def copy_to_prev_feedback(video_id, output_dir):
    """Copy current feedback to previous feedback file"""
    current_file = get_filename(video_id, output_dir, FEEDBACK_FILE_POSTFIX)
    prev_file = get_filename(video_id, output_dir, PREV_FEEDBACK_FILE_POSTFIX)
    
    assert os.path.exists(current_file), f"Current feedback file does not exist: {current_file}"
    
    # If prev file exists, check if it's different from current
    if os.path.exists(prev_file):
        with open(current_file, 'r') as f:
            current_data = json.load(f)
        with open(prev_file, 'r') as f:
            prev_data = json.load(f)
        if current_data != prev_data:
            raise AssertionError(f"Current and previous feedback files are different for {video_id}. This indicates the feedback has already been redone.")
        return  # If they're the same, no need to do anything
    
    # If prev file doesn't exist, copy current to prev
    with open(current_file, 'r') as f:
        current_data = json.load(f)
    with open(prev_file, 'w') as f:
        json.dump(current_data, f, indent=4)
    print(f"Copied current feedback to previous feedback: {prev_file}")

def handle_rejection(video_id, output_dir, current_user):
    """Handle the rejection process for a caption"""
    # Copy current feedback to previous
    copy_to_prev_feedback(video_id, output_dir)
    
    # Create reviewer data
    reviewer_data = {
        "reviewer_name": current_user,
        "review_timestamp": datetime.now().isoformat(),
        "reviewer_double_check": False
    }
    save_data(video_id, reviewer_data, output_dir=output_dir, file_postfix=REVIEWER_FILE_POSTFIX)
    st.rerun()

def format_timestamp(iso_timestamp: str) -> str:
    if not iso_timestamp:
        return 'N/A'
    try:
        return datetime.fromisoformat(iso_timestamp).strftime('%Y-%m-%d')
    except ValueError:
        return 'Invalid date'

def display_feedback_info(feedback_data, display_pre_caption_instead_of_final_caption=False):
    """Display feedback information including scores, GPT feedback, and caption differences."""
    st.write("##### Final Caption")
    st.write(feedback_data.get("final_caption", "No caption available"))
    
    st.write("##### Pre-caption Score")
    st.write(f"**{feedback_data['initial_caption_rating_score']}/5**")

    st.write("##### Initial Feedback")
    st.write(feedback_data.get("initial_feedback", "No initial feedback available"))
    
    st.write("##### GPT Polished Feedback")
    st.write(feedback_data.get("gpt_feedback", "No GPT feedback available"))
    
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
    
    if display_pre_caption_instead_of_final_caption:
        st.write("##### Pre-Caption (For Reference Only)")
        st.write(feedback_data["pre_caption"])
    else:
        st.write("##### Final Caption")
        st.write(feedback_data["final_caption"])

def display_feedback_differences(prev_feedback, feedback_data, diff_prompt=None, reviewer_data=None):
    """Display differences between current and previous feedback
    
    Args:
        prev_feedback: Previous feedback data dictionary
        feedback_data: Current feedback data dictionary
        diff_prompt: Optional path to diff prompt file
        reviewer_data: Optional reviewer data dictionary
    """
    if not prev_feedback or not feedback_data:
        st.error("Previous feedback or current feedback does not exist. Please report this bug to Zhiqiu Lin.")
        return
    
    # Check if feedback is duplicated (rejected but not corrected)
    annotator_name = prev_feedback.get("user", "Unknown annotator")
    reviewer_name = reviewer_data.get("reviewer_name", feedback_data.get("user", "Unknown reviewer")) if reviewer_data else feedback_data.get("user", "Unknown reviewer")
    if prev_feedback == feedback_data:
        st.error(f"⚠️ **{annotator_name}'s** caption was rejected by **{reviewer_name}** but hasn't been corrected yet. Please ask **{reviewer_name}** to correct the caption.")
        return
    
    st.info(f"Displaying differences between **{annotator_name}'s** and **{reviewer_name}'s** feedback")
    st.write(f"##### **{annotator_name}'s** Original Feedback (GPT Polished)")
    st.write(prev_feedback.get("gpt_feedback", "No GPT feedback available"))
    st.write(f"##### **{reviewer_name}'s** Feedback (GPT Polished)")
    st.write(feedback_data.get("gpt_feedback", "No GPT feedback available"))
    st.write(f"##### Summary of Differences")
    st.markdown(highlight_differences(prev_feedback.get("gpt_feedback", ""), feedback_data.get("gpt_feedback", ""), run_length=5), unsafe_allow_html=True)
    st.write(f"##### ChatGPT summary of differences")
    highlight_differences_gpt(
        prev_feedback.get("gpt_feedback", ""),
        feedback_data.get("gpt_feedback", ""),
        diff_prompt=diff_prompt,
        diff_key="gpt_feedback_diff_feedback",
        llm_key="gpt_feedback_diff_compare_llm",
        prompt_key="gpt_feedback_diff_compare_prompt",
        old_feedback=prev_feedback.get("gpt_feedback", ""),
        new_feedback=feedback_data.get("gpt_feedback", "")
    )

def display_caption_differences(prev_feedback, feedback_data, diff_prompt=None, reviewer_data=None):
    """Display differences between current and previous captions
    
    Args:
        prev_feedback: Previous feedback data dictionary
        feedback_data: Current feedback data dictionary
        diff_prompt: Optional path to diff prompt file
        reviewer_data: Optional reviewer data dictionary
    """
    if not prev_feedback or not feedback_data:
        st.error("Previous feedback or current feedback does not exist. Please report this bug to Zhiqiu Lin.")
        return
    
    # Check if feedback is duplicated (rejected but not corrected)
    annotator_name = prev_feedback.get("user", "Unknown annotator")
    reviewer_name = reviewer_data.get("reviewer_name", feedback_data.get("user", "Unknown reviewer")) if reviewer_data else feedback_data.get("user", "Unknown reviewer")
    if prev_feedback == feedback_data:
        st.error(f"⚠️ **{annotator_name}'s** caption was rejected by **{reviewer_name}** but hasn't been corrected yet. Please ask **{reviewer_name}** to correct the caption.")
        return
    
    st.info(f"Displaying differences between **{annotator_name}'s** and **{reviewer_name}'s** captions")
    st.write(f"##### **{annotator_name}'s** Original Caption")
    st.write(prev_feedback.get("final_caption", "No caption available"))
    st.write(f"##### **{reviewer_name}'s** Revised Caption")
    st.write(feedback_data.get("final_caption", "No caption available"))
    st.write(f"##### Summary of Differences")
    st.markdown(highlight_differences(prev_feedback.get("final_caption", ""), feedback_data.get("final_caption", ""), run_length=5), unsafe_allow_html=True)
    st.write(f"##### ChatGPT summary of differences")
    highlight_differences_gpt(
        prev_feedback.get("final_caption", ""),
        feedback_data.get("final_caption", ""),
        diff_prompt=diff_prompt,
        diff_key="final_caption_diff_feedback",
        llm_key="final_caption_diff_compare_llm",
        prompt_key="final_caption_diff_compare_prompt",
        old_caption=prev_feedback.get("final_caption", ""),
        new_caption=feedback_data.get("final_caption", "")
    )

def split_into_words(text):
    """Split text into words for better diff visualization"""
    # Split by whitespace and punctuation
    words = re.findall(r"\w+|\W+", text)
    return words

def is_large_diff(text1: str, text2: str, run_length: int = 5) -> bool:
    """
    Return True if there is at least one consecutive run of insertions /
    deletions ≥ run_length tokens.
    """
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

def html_word_diff(text1: str, text2: str) -> str:
    """
    Return word-level diff between text1 and text2 using custom HTML formatting
    (✓ works well in Streamlit with st.markdown(..., unsafe_allow_html=True))
    """
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

    # Step 3: Build HTML diff with your style
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

def highlight_differences(text1, text2, run_length: int = 5):
    """Highlight differences between two texts using HTML with word-level granularity"""
    text1 = "" if text1 is None else text1
    text2 = "" if text2 is None else text2
    if is_large_diff(text1, text2, run_length=run_length):
        return html_word_diff(text1, text2)
    else:
        # Split texts into words
        words1 = split_into_words(text1)
        words2 = split_into_words(text2)
        
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

def highlight_differences_gpt(text1, text2, diff_prompt=None, diff_key="diff_feedback", llm_key="selected_diff_compare_llm", prompt_key="cur_diff_compare_prompt", **kwargs):
    # First generate the initial diff feedback
    text1 = "" if text1 is None else text1
    text2 = "" if text2 is None else text2
    if diff_key not in st.session_state:
        llm_names = get_all_llms()
        selected_diff_compare_llm = llm_names[llm_names.index("gpt-4o-2024-08-06")]
        diff_compare_prompt = load_txt(FOLDER / diff_prompt)
        st.session_state[diff_key] = get_llm(
            model=selected_diff_compare_llm,
            secrets=st.secrets,
        ).generate(
            diff_compare_prompt.format(
                **kwargs,
            ),
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
        diff_compare_prompt = load_txt(FOLDER / diff_prompt)

    diff_compare_prompt = st.text_area(
        "Prompt for comparing feedback:",
        value=diff_compare_prompt,
        key=prompt_key,
        height=PROMPT_HEIGHT,
    )
    if st.button("Re-generate Summary", key=f"{llm_key}_re_generate_button"):
        # Generate new diff feedback
        st.session_state[diff_key] = get_llm(
            model=selected_diff_compare_llm,
            secrets=st.secrets,
        ).generate(
            diff_compare_prompt.format(
                **kwargs,
            ),
        )
        st.rerun()  # Rerun to show the new feedback

def copy_feedback_for_precaption(configs_path, video_urls, main_project_output, personalized_output):
    """Copy feedback files from main project output to personalized output directory for precaption purposes.
    
    Args:
        configs_path: Path to configs file
        video_urls: List of video URLs to process
        main_project_output: Path to main project output directory
        personalized_output: Path to personalized output directory
    """
    # Create personalized output directory if it doesn't exist
    os.makedirs(personalized_output, exist_ok=True)
    
    # Process each video
    for video_url in video_urls:
        video_id = get_video_id(video_url)
        
        # For each config in the main project
        configs = load_config(FOLDER / configs_path)
        configs = [load_config(FOLDER / config) for config in configs]
        
        for config in configs:
            # Get the output directory for this config
            config_output_dir = os.path.join(FOLDER, main_project_output, config["output_name"])
            feedback_file = get_filename(video_id, config_output_dir, FEEDBACK_FILE_POSTFIX)
            
            # If feedback exists in main project, check if precaption already exists
            if os.path.exists(feedback_file):
                # Create config directory in personalized output
                personalized_config_dir = os.path.join(FOLDER, personalized_output, config["output_name"])
                os.makedirs(personalized_config_dir, exist_ok=True)
                
                # Check if precaption file already exists
                precaption_file = get_filename(video_id, personalized_config_dir, PRECAPTION_FILE_POSTFIX)
                if not os.path.exists(precaption_file):
                    # Only copy if precaption doesn't exist
                    with open(feedback_file, 'r') as src, open(precaption_file, 'w') as dst:
                        dst.write(src.read())
                    print(f"Copied {feedback_file} to {precaption_file}")
                else:
                    print(f"Skipped copying {feedback_file} as {precaption_file} already exists")
            else:
                print(f"Skipped copying {feedback_file} as it doesn't exist")

def display_status_indicators():
    """Display an expander explaining the status indicators used in the video selection dropdown."""
    with st.expander("📝 Status Indicators Explanation", expanded=False):
        st.markdown("""
        | Emoji | Status | Description |
        |-------|--------|-------------|
        |  | Not Completed | Video has not been captioned yet |
        | ✅ | Completed | Video has been captioned but not reviewed |
        | ✅✅ | Approved | Video has been reviewed and double-checked |
        | ❌ | Rejected | Video needs revision (different users in current and previous feedback) |
        """)

def main(args, caption_programs):
    # # Set page config first
    # st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # # Check login status
    # if "logged_in" not in st.session_state or not st.session_state.logged_in:
    #     login_page(args)
    #     return
    # ONLY set page config if we're running standalone (not in portal mode)
    # if not hasattr(st.session_state, 'selected_portal'):
    #     st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

    # Check login status - ONLY if not already logged in through unified system
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # ONLY show login if we're running standalone
        if not hasattr(st.session_state, 'selected_portal'):
            login_page(args)
            return
        else:
            # If we're in portal mode but not logged in, something went wrong
            st.error("Authentication error. Please logout and login again.")
            return
    
    # After successful login, update the output directory based on the logged-in user if personalize_output is True
    if args.personalize_output and "logged_in_user" in st.session_state:
        # Only set the personalized output directory once in session state
        if "personalized_output" not in st.session_state:
            username = convert_name_to_username(st.session_state.logged_in_user)
            st.session_state.personalized_output = f"{args.output}_{username}"
            print(f"Personalized output directory: {st.session_state.personalized_output}")
            # Copy feedback files from main project for precaption
            copy_feedback_for_precaption(
                args.configs,
                st.session_state.video_urls,  # Use video_urls directly
                args.main_project_output,  # Main project output
                st.session_state.personalized_output  # Personalized output
            )
        
        # Use the stored personalized output directory
        args.output = st.session_state.personalized_output
        st.sidebar.write(f"**Output Directory:** {args.output}")

    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    if "file_check_passed" not in st.session_state:
        file_check(st.session_state.video_urls, video_data_dict)  # Use video_urls directly
        st.session_state.file_check_passed = True

    # Create two columns
    page_col1, page_col2 = st.columns([1, 1])  # Left column is smaller, right column is wider

    # Add logout button
    st.sidebar.title("User Options")
    st.sidebar.write(f"Logged in as: **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Logout"):
        # Clear session state and logout
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Debug information
    st.sidebar.header("Debug Information")
    st.sidebar.write("Full Session State:")
    for key, value in st.session_state.items():
        st.sidebar.write(f"{key}: {value}")
    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        st.error(f"Config file not found: {args.configs}")
        return

    with page_col1:
    # with st.container(height=CONTAINER_HEIGHT, border=True):
        config_dict = {config["name"]: config for config in configs}
        config_names = list(config_dict.keys())
        # Dropdown to select a config, updating session state
        selected_config = st.selectbox(
            "Select a task:",
            config_names,
            index=config_names.index(st.session_state.get('last_config_id', config_names[0])),
            key="selected_task",
        )

        # Track task changes to reset state
        if 'last_config_id' not in st.session_state:
            st.session_state.last_config_id = selected_config
        elif st.session_state.last_config_id != selected_config:
            # Config changed, reset all state variables
            # First, collect all keys to remove
            keys_to_remove = []
            for key in st.session_state:
                # Keep api_key and last_config_id
                if key not in ['api_key', 'last_config_id', 'file_check_passed', 'logged_in', 'video_urls', 'last_video_id', 'last_selected_video', 'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 'target_annotator', 'selected_portal_mode', 'selected_portal_file']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_config_id = selected_config
            print(f"Config changed to: {selected_config}")
            st.rerun()  # Force a rerun to ensure clean state

        config = config_dict[selected_config]
        st.markdown(f"### {config.get('name', 'Pre-Caption System')}")
        
        # Get video URLs from session state
        video_urls = st.session_state.video_urls
            
        output_dir = os.path.join(FOLDER, args.output, config["output_name"])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Display instructions
        # st.subheader("Instructions")
        with st.expander("📜 Caption Instructions (Click to Expand/Collapse)", expanded=False):
            # Load instructions from file, otherwise throw a warning
            if "instruction_file" not in config:
                st.warning("No instruction_file found in the configuration file.")
            else:
                st.write(load_txt(FOLDER / config["instruction_file"]))

        # Display status indicators explanation
        display_status_indicators()

        # Select video
        selected_video = st.selectbox(
            "Select a video:",
            video_urls,
            format_func=get_video_format_func(output_dir, file_postfix=FEEDBACK_FILE_POSTFIX, video_urls=video_urls),
            index=video_urls.index(st.session_state.get('last_selected_video', video_urls[0])),
            key="selected_video"
        )
        video_id = get_video_id(selected_video)
        caption_program = caption_programs[config["task"]]
        current_prompt = caption_program(video_data_dict[video_id])[config["task"]]

        # Track video changes to reset state
        if 'last_video_id' not in st.session_state:
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video
        elif st.session_state.last_video_id != video_id:
            # Video changed, reset all state variables
            # First, collect all keys to remove
            keys_to_remove = []
            for key in st.session_state:
                # Keep api_key and last_video_id
                if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id', 'last_selected_video', 'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user', 'personalized_output', 'selected_portal', 'login_method', 'target_annotator', 'selected_portal_mode', 'selected_portal_file']:
                    keys_to_remove.append(key)

            # Remove all collected keys
            for key in keys_to_remove:
                del st.session_state[key]

            # Set the new video id
            st.session_state.last_video_id = video_id
            st.session_state.last_selected_video = selected_video

            # Also clear any feedback component states
            if 'feedback_submitted_initial_caption_faces' in st.session_state:
                del st.session_state['feedback_submitted_initial_caption_faces']

            st.rerun()  # Force a rerun to ensure clean state

        # Session state initialization
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'precaption_data' not in st.session_state:
            st.session_state.precaption = {}
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = {}

        from video_player import custom_video_player
        custom_video_player(selected_video)

        # Display first and last frames
        extracted_frames = extract_frames(selected_video, [0, -1])
        # Expandable section
        with st.expander("Frames (Click to Expand/Collapse)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.image(extracted_frames[0], caption="First Frame")
            with col2:
                st.image(extracted_frames[1], caption="Last Frame")
        
        with st.expander("Show Links", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            # ['cam_motion', 'cam_setup', 'lighting_setup'] check workflows['cam_motion'].editing_url
            with col1:
                st.link_button("🔗 Cam-Motion", f"https://camerapizza.a.pinggy.link/?video_uid={video_id}")
                # if 'cam_motion' in video_data_dict[video_id].workflows:
                #     st.link_button("🔗 Cam-Motion", video_data_dict[video_id].workflows['cam_motion'].editing_url)
                # else:
                #     st.link_button("🔗 Cam-Motion", "https://example.com/a", type='secondary', disabled=True)
                    
            with col2:
                st.link_button("🔗 Cam-Setup", f"https://camerapizza.a.pinggy.link/?video_uid={video_id}")
                # if 'cam_setup' in video_data_dict[video_id].workflows:
                #     st.link_button("🔗 Cam-Setup", video_data_dict[video_id].workflows['cam_setup'].editing_url)
                # else:
                #     st.link_button("🔗 Cam-Setup", "https://example.com/b", type='secondary', disabled=True)
                    
            with col3:
                st.link_button("🔗 Lighting-Setup", f"https://lightpizza.a.pinggy.link/?video_uid={video_id}")
                # if 'lighting_setup' in video_data_dict[video_id].workflows:
                #     st.link_button("🔗 Lighting-Setup", video_data_dict[video_id].workflows['lighting_setup'].editing_url)
                # else:
                #     st.link_button("🔗 Lighting-Setup", "https://example.com/c", type='secondary', disabled=True)
            
            st.link_button("🔗 Report Label Errors Here", "https://docs.google.com/spreadsheets/d/1sAYL86ERcaC_vrVuloXxtPJXKzeuj8fukHtNv6nRCJ0/edit?usp=sharing")

        # Get indices
        current_index = video_urls.index(selected_video)
        current_task_index = config_names.index(selected_config)

        # Keys to keep
        preserved_keys = [
            'api_key', 'last_config_id', 'selected_config',
            'last_video_id', 'last_selected_video', 'personalized_output',
            'file_check_passed', 'logged_in', 'video_urls', 'logged_in_user',
            'selected_portal', 'login_method', 'target_annotator', 'selected_portal_mode', 'selected_portal_file'
        ]

        def reset_state_except(preserved):
            keys_to_remove = [key for key in st.session_state if key not in preserved]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()

        # Create a single horizontal row with 4 nav buttons
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            if current_index > 0:
                if st.button("Prev Video ⏪"):
                    st.session_state.last_selected_video = video_urls[current_index - 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index - 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Prev Video ⏪", disabled=True)

        with col2:
            if current_task_index > 0:
                prev_task_index = current_task_index - 1
            else:
                prev_task_index = len(config_names) - 1
            prev_task_short_name = config_names_to_short_names[config_names[prev_task_index]]
            if st.button(f"{prev_task_short_name} Task ⬅️"):
                st.session_state.last_config_id = config_names[prev_task_index]
                reset_state_except(preserved_keys)
        
        with col3:
            task_short_name = config_names_to_short_names[selected_config]
            st.button(f"{task_short_name} Task ⬇️", disabled=True)

        with col4:
            if current_task_index < len(config_names) - 1:
                next_task_index = current_task_index + 1
            else:
                next_task_index = 0
            next_task_short_name = config_names_to_short_names[config_names[next_task_index]]
            if st.button(f"{next_task_short_name} Task ➡️"):
                st.session_state.last_config_id = config_names[next_task_index]
                reset_state_except(preserved_keys)

        with col5:
            if current_index < len(video_urls) - 1:
                if st.button("Next Video ⏩"):
                    st.session_state.last_selected_video = video_urls[current_index + 1]
                    st.session_state.last_video_id = get_video_id(video_urls[current_index + 1])
                    reset_state_except(preserved_keys)
            else:
                st.button("Next Video ⏭️", disabled=True)

    with page_col2:
        # Call the fragment function with all necessary parameters
        feedback_interface(
            video_id=video_id,
            config=config, 
            output_dir=output_dir,
            caption_program=caption_program,
            video_data_dict=video_data_dict,
            selected_video=selected_video,
            args=args,
            selected_config=selected_config,
            config_dict=config_dict
        )

if __name__ == "__main__":
    # Load configuration
    args = parse_args()
    main(args, caption_programs)
