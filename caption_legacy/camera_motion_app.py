import streamlit as st
import argparse
from streamlit_feedback import streamlit_feedback
import os
import torch
import json
from datetime import datetime
from pathlib import Path
from utils import extract_frames, load_config, load_json
from llm import get_llm, get_all_llms, get_supported_mode
from process_json import json_to_video_data

from feedback_app import caption_programs, PRECAPTION_FILE_POSTFIX, FEEDBACK_FILE_POSTFIX, SUBJECT_CAPTION_NAME, SCENE_CAPTION_NAME, PROMPT_HEIGHT
from feedback_app import load_video_data, emoji_to_score, get_filename, save_data, load_data, load_precaption, load_feedback, data_is_saved, get_video_id, load_txt, load_prompt, generate_save_and_return_pre_caption, get_video_format_func, get_imagery_kwargs, file_check, load_pre_caption_prompt

# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="camera_motion_config.json", help="Path to the JSON config file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_all.json", help="Path to the test URLs file")
    # parser.add_argument("--video_urls_file", type=str, default="test_urls_selected.json", help="Path to the test URLs file")
    parser.add_argument("--video_urls_file", type=str, default="motion_urls_random.json", help="Path to the test URLs file")
    parser.add_argument("--output", type=str, default="output_captions", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    # parser.add_argument("--video_data", type=str, default="video_data/20250218_1042/videos.json", help="Path to the video data file")
    parser.add_argument("--video_data", type=str, default="video_data/20250227_0324ground_only/videos.json", help="Path to the video data file")
    parser.add_argument("--label_collections", nargs="+", type=str, default=["cam_motion"], help="List of label collections to load from the video data")
    return parser.parse_args()

def main():
    # Load configuration
    args = parse_args()
    
    # Load video data
    video_data_dict = load_video_data(args.video_data, label_collections=args.label_collections)
    if "file_check_passed" not in st.session_state:
        file_check(args, video_data_dict)
        st.session_state.file_check_passed = True
        
    # Hide sidebar by default
    st.set_page_config(initial_sidebar_state="collapsed")
    
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
            if key not in ['api_key', 'last_config_id']:
                keys_to_remove.append(key)
        
        # Remove all collected keys
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Set the new video id
        st.session_state.last_config_id = selected_config
        print(f"Config changed to: {selected_config}")
        st.rerun()  # Force a rerun to ensure clean state


    config = config_dict[selected_config]
    st.title(config.get("name", "Pre-Caption System"))
    video_urls = load_json(FOLDER / args.video_urls_file)
    output_dir = os.path.join(FOLDER, args.output, config["output_name"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    
    # Select video
    selected_video = st.selectbox(
        "Select a video:",
        video_urls,
        format_func=get_video_format_func(output_dir, file_postfix=FEEDBACK_FILE_POSTFIX),
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
            if key not in ['api_key', 'last_config_id', 'selected_config', 'last_video_id']:
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

    # Display instructions
    st.subheader("Instructions")
    with st.expander("📜 Instructions (Click to Expand/Collapse)", expanded=False):
        # Load instructions from file, otherwise throw a warning
        if "instruction_file" not in config:
            st.warning("No instruction_file found in the configuration file.")
        else:
            st.write(load_txt(FOLDER / config["instruction_file"]))

    
    # Display video
    st.video(selected_video)
    
    # Display first and last frames
    extracted_frames = extract_frames(selected_video, [0, -1])
    # Expandable section
    with st.expander("Frames (Click to Expand/Collapse)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.image(extracted_frames[0], caption="First Frame", use_container_width=True)
        with col2:
            st.image(extracted_frames[1], caption="Last Frame", use_container_width=True)
    
    # Step 0: Generating Pre-caption
    if st.session_state.current_step == 0:
        # If feedback already exists, load it
        if data_is_saved(video_id, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX):
            load_feedback(video_id, output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
            st.write("Feedback already exists for this video. You can choose to restart by either re-generating the pre-caption or by providing a new rating.")
    
        # If not exist, return empty dict
        existing_precaption = load_precaption(video_id, output_dir, file_postfix=PRECAPTION_FILE_POSTFIX)
        # st.write("##### Pre-caption was generated by ")
        # st.write("Please polish the prompt and select an option to generate a caption:")
        llm_names = get_all_llms()
        # Dropdown to select a config, updating session state
        selected_llm = st.selectbox(
            "Select a Model:",
            llm_names, 
            index=llm_names.index(existing_precaption.get("pre_caption_llm", llm_names[0])),
            key="selected_llm"
        )
        supported_modes = get_supported_mode(selected_llm)
        selected_mode = st.selectbox(
            "Select a Mode:",
            supported_modes, 
            index=supported_modes.index(existing_precaption.get("pre_caption_mode", "Text Only")),
            key="selected_mode"
        )
        
        if "pre_caption_prompt" in st.session_state:
            pre_caption_prompt = st.session_state.pre_caption_prompt
        else:
            pre_caption_prompt = existing_precaption.get("pre_caption_prompt", load_pre_caption_prompt(video_id, video_data_dict, caption_program, config_dict, selected_config, args.output))
        
        line_height = 12  # Approximate height per line in pixels
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
            pre_caption = generate_save_and_return_pre_caption(video_id, output_dir, current_prompt, selected_llm, selected_mode, selected_video)
        
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
        st.write(f"##### Pre-caption generated by {selected_llm} ({selected_mode})")
        st.write(pre_caption)
        st.write("#### Rate the caption (Is it accurate? Does it miss anything important?)")
    
        # Fetch stored initial rating if it exists
        if "initial_caption_rating" in st.session_state:
            score = st.session_state.initial_caption_rating
        else:
            initial_rating_response = streamlit_feedback(
                feedback_type="faces",
                key=f"initial_caption_faces_{video_id}_{config['name']}"
            )

            if initial_rating_response:
                st.session_state.initial_caption_rating = initial_rating_response['score']
                score = initial_rating_response['score']
            else:
                score = None
        
        st.write("Please provide your feedback to improve this caption (if not score of 5):")
        user_feedback = st.text_area(
            "Your feedback:",
            key=f"user_feedback_{video_id}_{config['name']}",
            height=PROMPT_HEIGHT,
        )

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
                "timestamp": datetime.now().isoformat(),
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
                st.write("You can optionally change the LLM or the prompt that we used to polish your feedback. Please keep {feedback} and {pre_caption} in the prompt.")
                llm_names = get_all_llms()
                # Dropdown to select a config, updating session state
                selected_feedback_llm = st.selectbox(
                    "Select a Model:",
                    llm_names,
                    key="selected_feedback_llm",
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
                if st.button("Submit Feedback") and user_feedback:
                    st.session_state.feedback_data["initial_feedback"] = user_feedback
                    st.session_state.feedback_data["gpt_feedback_llm"] = selected_feedback_llm
                    st.session_state.feedback_data["gpt_feedback_prompt"] = feedback_prompt
                    # Get GPT-4 polished feedback
                    new_feedback = get_llm(
                        model=selected_feedback_llm,
                        secrets=st.secrets,
                    ).generate(
                        feedback_prompt.format(feedback=user_feedback, pre_caption=pre_caption),
                    )
                    st.session_state.feedback_data["gpt_feedback"] = new_feedback
                    st.session_state.current_step = 1
                    st.rerun()
            else:
                # If happiest face, save and finish
                st.session_state.feedback_data["final_caption"] = pre_caption
                save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                st.success("Caption rated as perfect! No changes needed.")
                st.json(st.session_state.feedback_data)
    
    # Step 1: Rate GPT's feedback and optionally provide corrected feedback
    elif st.session_state.current_step == 1:
        # Wait for user to confirm pre-caption by clicking on feedback
        st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
        st.write(st.session_state.feedback_data["pre_caption"])
        st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
        st.write(f"##### Your Feedback")
        st.write(f"{st.session_state.feedback_data['initial_feedback']}")
        st.write(f"##### Polished Feedback from {st.session_state.feedback_data['gpt_feedback_llm']}")
        st.write(f"{st.session_state.feedback_data['gpt_feedback']}")
        st.subheader(f"Please Rate AI-Polished Feedback")

        # Fetch stored feedback rating if it exists
        if "feedback_rating" in st.session_state:
            score = st.session_state.feedback_rating
        else:
            feedback_response = streamlit_feedback(
                feedback_type="faces",
                key="feedback_faces"
            )

            if feedback_response:
                st.session_state.feedback_rating = feedback_response['score']
                score = feedback_response['score']
            else:
                score = None  # Default to None if no response yet

        if score:
            st.session_state.feedback_data["feedback_rating"] = score  # Store in feedback data
            st.session_state.feedback_data["feedback_rating_score"] = emoji_to_score(score)  # Store numeric rating
            
            if score != "😀":
                st.write("Please finalize the feedback:")

                # Ensure final_feedback is stored persistently
                if "final_feedback" not in st.session_state:
                    st.session_state.final_feedback = st.session_state.feedback_data["gpt_feedback"]

                final_feedback = st.text_area(
                    "Finalized feedback:",
                    value=st.session_state.final_feedback,
                    key="correct_feedback"
                )

                # Button Click Handling
                if st.button("Submit Corrected Feedback"):
                    if final_feedback.strip():
                        # Persist final feedback
                        st.session_state.feedback_data["final_feedback"] = final_feedback
                        st.session_state.final_feedback = final_feedback
                        
                        # Store step change in session state
                        st.session_state.current_step = 2
                        st.session_state.feedback_submitted = True  # Flag to track submission
                    else:
                        st.warning("Please provide an non-empty feedback before submitting.")
                    st.rerun()
            else:
                # If rating is happy, then directly use the GPT feedback as final feedback
                st.session_state.feedback_data["final_feedback"] = st.session_state.feedback_data["gpt_feedback"]
                st.session_state.current_step = 2
                st.session_state.feedback_submitted = True  # Flag to track submission

        if st.session_state.get("feedback_submitted", False):
            st.session_state.current_step = 2  # Ensure next step persists
            st.rerun()


    # Step 2: Generate caption (intermediate step)
    elif st.session_state.current_step == 2:
        st.write(f"##### Pre-caption generated by {st.session_state.feedback_data['pre_caption_llm']} ({st.session_state.feedback_data['pre_caption_mode']})")
        st.write(st.session_state.feedback_data["pre_caption"])
        st.write(f"You rate the caption as **{st.session_state.feedback_data['initial_caption_rating_score']}/5**\n\n")
        st.write(f"##### Final Feedback from you and {st.session_state.feedback_data['gpt_feedback_llm']}")
        st.write(f"{st.session_state.feedback_data['final_feedback']}\n\n")
        st.write("You can optionally change the LLM or the prompt that we used to polish the caption. Please keep {feedback} and {pre_caption} in the prompt.")
        # Get the final feedback (either corrected or GPT's version)
        final_feedback = st.session_state.feedback_data["final_feedback"]
        pre_caption = st.session_state.feedback_data["pre_caption"]
        # Get improved caption
        llm_names = get_all_llms()
        # Dropdown to select a config, updating session state
        selected_caption_llm = st.selectbox(
            "Select a Model:",
            llm_names,
            key="selected_caption_llm",
        )
        if "cur_caption_prompt" in st.session_state:
            caption_prompt = st.session_state.cur_caption_prompt
        else:
            caption_prompt = load_txt(FOLDER / args.caption_prompt)
        
        caption_prompt = st.text_area(
            "Prompt for polishing caption:",
            value=caption_prompt,
            key="cur_caption_prompt",
            height=PROMPT_HEIGHT,
        )
        if st.button("Submit") and caption_prompt:
            st.session_state.feedback_data["gpt_caption_llm"] = selected_caption_llm
            st.session_state.feedback_data["gpt_caption_prompt"] = caption_prompt
            # Get GPT-4 polished feedback
            new_caption = get_llm(
                model=selected_caption_llm,
                secrets=st.secrets,
            ).generate(
                caption_prompt.format(feedback=final_feedback, pre_caption=pre_caption),
            )
            st.session_state.feedback_data["gpt_caption"] = new_caption
            st.session_state.current_step = 3
            st.rerun()
        # gpt_caption = get_gpt4_caption(final_feedback, current_caption, caption_prompt=FOLDER / args.caption_prompt)
        # st.rerun()
    
    # Step 3: Rate GPT's caption and optionally provide corrected caption
    elif st.session_state.current_step == 3:
        st.subheader("Rate AI-Improved Caption")
        st.write(f"##### Caption generated by {st.session_state.feedback_data['gpt_caption_llm']}")
        # Get the final feedback (either corrected or GPT's version)
        gpt_caption = st.session_state.feedback_data["gpt_caption"]
        st.write(gpt_caption)

        # Retrieve stored caption rating if it exists
        if "caption_rating" in st.session_state:
            score = st.session_state.caption_rating
        else:
            caption_response = streamlit_feedback(
                feedback_type="faces",
                key="caption_faces"
            )

            if caption_response:
                st.session_state.caption_rating = caption_response['score']
                score = caption_response['score']
            else:
                score = None  # Default to None if no response yet

        st.write("Please modify the caption below (if not score of 5):")

        # Ensure final_caption is stored persistently
        if "final_caption" not in st.session_state:
            st.session_state.final_caption = gpt_caption

        line_height = 12  # Approximate height per line in pixels
        num_lines = max(30, len(st.session_state.final_caption) // 120)  # Assuming ~120 characters per line
        estimated_height = num_lines * line_height
        final_caption = st.text_area(
            "Final caption:",
            value=st.session_state.final_caption,
            key="correct_caption",
            height=estimated_height,
        )
        
        if score:
            st.session_state.feedback_data["caption_rating"] = score  # Persist rating
            st.session_state.feedback_data["caption_rating_score"] = emoji_to_score(score)  # Store numeric rating

            if score != "😀":
                # Button Click Handling
                if st.button("Submit Final Caption"):
                    if final_caption.strip():
                        # Persist final caption
                        st.session_state.feedback_data["final_caption"] = final_caption
                        st.session_state.final_caption = final_caption
                        
                        # Save feedback data
                        save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                        st.success(f"Caption saved successfully!")
                        st.json(st.session_state.feedback_data)
                        st.session_state.caption_submitted = True
                        st.session_state.current_step = 4
                    else:
                        st.warning("Please provide an non-empty feedback before submitting.")
                    st.rerun()
            else:
                # If rating is happy, finalize caption and save
                st.session_state.feedback_data["final_caption"] = st.session_state.feedback_data["gpt_caption"]
                save_data(video_id, st.session_state.feedback_data, output_dir=output_dir, file_postfix=FEEDBACK_FILE_POSTFIX)
                st.success(f"Caption saved successfully!")
                st.json(st.session_state.feedback_data)
                st.session_state.caption_submitted = True
                st.session_state.current_step = 4
        
        if st.session_state.get("caption_submitted", False):
            st.session_state.current_step = 4  # Ensure next step persists
            st.rerun()
    
    # Step 4: Print the final caption, and say if want to redo, please go to another video then come back
    elif st.session_state.current_step == 4:
        # st.write(f"##### Final Caption")
        st.write(st.session_state.feedback_data["final_caption"])
        st.success("Feedback and caption saved successfully! To redo, please go to another video then come back.")
        st.json(st.session_state.feedback_data)


if __name__ == "__main__":
    main()