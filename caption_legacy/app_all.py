import streamlit as st
import argparse
from openai import OpenAI
from streamlit_feedback import streamlit_feedback
import os
import json
from datetime import datetime
from pathlib import Path

# Get the directory where this script is located
FOLDER = Path(__file__).parent

# Initialize session state for API key and OpenAI client
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Video Caption Feedback System")
    parser.add_argument("--configs", type=str, default="all_test_configs.json", help="Path to the JSON config file")
    parser.add_argument("--video_urls_file", type=str, default="test_urls.json", help="Path to the test URLs file")
    parser.add_argument("--output", type=str, default="outputs", help="Path to the output directory")
    parser.add_argument("--feedback_prompt", type=str, default="prompts/feedback_prompt.txt", help="Path to the feedback prompt file")
    parser.add_argument("--caption_prompt", type=str, default="prompts/caption_prompt.txt", help="Path to the caption prompt file")
    return parser.parse_args()

# Load configuration from a JSON file
def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

# Load JSON data from a given file
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

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

def save_feedback_data(video_id, data, output_dir="outputs"):
    """Save feedback data to a JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f'{video_id}.json')
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

def load_feedback_data(video_id, output_dir="outputs"):
    """Load existing feedback data for a video if it exists"""
    filename = os.path.join(output_dir, f'{video_id}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None


# Get video ID from URL
def get_video_id(url):
    return url.split('/')[-1]

# Load instructions from file
def load_instructions(instruction_file):
    with open(instruction_file, "r") as f:
        return f.read()

# Load prompt template
def load_prompt(filename, **kwargs):
    with open(filename, "r") as f:
        prompt = f.read()
    return prompt.format(**kwargs)

def get_gpt4_feedback(feedback, original_caption, feedback_prompt='prompts/feedback_prompt.txt'):
    prompt = load_prompt(feedback_prompt, 
                        original_caption=original_caption,
                        feedback=feedback)
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def get_gpt4_caption(feedback, original_caption, caption_prompt='prompts/caption_prompt.txt'):
    prompt = load_prompt(caption_prompt,
                        original_caption=original_caption,
                        feedback=feedback)
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def get_video_format_func(output_dir):
    def video_format_func(video_url):
        # if already exists, then return f"✅ {video_url}"
        video_id = get_video_id(video_url)
        # Check for existing feedback and get current caption
        existing_feedback = load_feedback_data(video_id, output_dir=FOLDER / output_dir)
        
        # Show existing feedback if available
        if existing_feedback:
            return f"✅ {video_url}"
        return f"{video_url}"
    return video_format_func

def main():
    # Load configuration
    args = parse_args()
    
    # Hide sidebar by default
    st.set_page_config(initial_sidebar_state="collapsed")
    
    
    # Debug information
    st.sidebar.header("Debug Information")
    st.sidebar.write("Full Session State:")
    for key, value in st.session_state.items():
        st.sidebar.write(f"{key}: {value}")
    
    # API Key input
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.session_state.api_key = api_key
    
    if not st.session_state.api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        return

    try:
        configs = load_config(FOLDER / args.configs)
        configs = [load_config(FOLDER / config) for config in configs]
    except FileNotFoundError:
        st.error(f"Config file not found: {args.configs}")
        import pdb; pdb.set_trace()
        return
    
    config_dict = {config["name"]: config for config in configs}
    config_names = list(config_dict.keys())
    # Dropdown to select a config, updating session state
    selected_config = st.selectbox(
        "Select a task:",
        config_names, 
        # index=config_names.index(st.session_state.selected_config),
        # key="config_selector"
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
        
        st.rerun()  # Force a rerun to ensure clean state


    config = config_dict[selected_config]
    st.title(config.get("name", "Video Caption Feedback System"))
    captions = load_json(FOLDER / config["captions_file"]) # TODO: Bug
    video_urls = load_json(FOLDER / args.video_urls_file)
    output_dir = os.path.join(FOLDER, args.output, config["output_name"])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    
    # Select video
    selected_video = st.selectbox("Select a video:", video_urls, format_func=get_video_format_func(output_dir))
    video_id = get_video_id(selected_video)
    
    # Track video changes to reset state
    if 'last_video_id' not in st.session_state:
        st.session_state.last_video_id = video_id
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
        
        # Also clear any feedback component states
        if 'feedback_submitted_initial_caption_faces' in st.session_state:
            del st.session_state['feedback_submitted_initial_caption_faces']
        
        st.rerun()  # Force a rerun to ensure clean state
    
    # Session state initialization
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = {}

    # Display instructions
    st.subheader("Instructions")
    with st.expander("📜 Instructions (Click to Expand/Collapse)", expanded=True):
        # Load instructions from file, otherwise throw a warning
        if "instruction_file" not in config:
            st.warning("No instruction_file found in the configuration file.")
        else:
            st.write(load_instructions(FOLDER / config["instruction_file"]))

    
    # Display video
    st.video(selected_video)
    
    # Check for existing feedback and get current caption
    existing_feedback = load_feedback_data(video_id, output_dir=FOLDER / output_dir)
    
    # Show existing feedback if available
    if existing_feedback:
        st.info("Previous feedback found for this video")
        st.json(existing_feedback)
    
    # Display current caption
    st.subheader("Current Prompt")
    if existing_feedback and existing_feedback.get("final_caption"):
        current_caption = existing_feedback["final_caption"]
        st.info("Using previously approved caption")
    else:
        current_caption = captions.get(video_id, "## **No caption available**")
    st.write(current_caption)
    
    # Display conversation history
    if st.session_state.feedback_data:
        st.subheader("Conversation History")
        if "initial_feedback" in st.session_state.feedback_data:
            st.markdown("**Your Initial Feedback:**")
            st.write(st.session_state.feedback_data["initial_feedback"])
        
        if "gpt_feedback" in st.session_state.feedback_data:
            st.markdown("**AI-Polished Feedback:**")
            st.write(st.session_state.feedback_data["gpt_feedback"])
        
        if "final_feedback" in st.session_state.feedback_data:
            st.markdown("**Final Feedback:**")
            st.write(st.session_state.feedback_data["final_feedback"])
        
        if "gpt_caption" in st.session_state.feedback_data:
            st.markdown("**AI-Improved Caption:**")
            st.write(st.session_state.feedback_data["gpt_caption"])
        
        if "final_caption" in st.session_state.feedback_data:
            st.markdown("**Final Caption:**")
            st.write(st.session_state.feedback_data["final_caption"])
    
    # Step 0: Rate the initial caption
    if st.session_state.current_step == 0:
        st.write("Please rate the current caption:")
        
        # Fetch stored initial rating if it exists
        if "initial_caption_rating" in st.session_state:
            score = st.session_state.initial_caption_rating
        else:
            initial_rating_response = streamlit_feedback(
                feedback_type="faces",
                key=f"initial_caption_faces_{video_id}_{config['name']}"
            )

            if initial_rating_response and 'score' in initial_rating_response:
                st.session_state.initial_caption_rating = initial_rating_response['score']
                score = initial_rating_response['score']
            else:
                score = None

        if score:
            feedback_is_needed = score != "😀"
            
            # Initialize feedback data
            st.session_state.feedback_data = {
                "video_id": video_id,
                "original_caption": current_caption,
                "initial_caption_rating": score,
                "initial_caption_rating_score": emoji_to_score(score),
                "feedback_is_needed": feedback_is_needed,
                "timestamp": datetime.now().isoformat(),
                # Initialize other fields as None
                "initial_feedback": None,
                "gpt_feedback": None,
                "feedback_rating": None,
                "feedback_rating_score": None,
                "final_feedback": None,
                "gpt_caption": None,
                "caption_rating": None,
                "caption_rating_score": None,
                "final_caption": None
            }
            
            if feedback_is_needed:
                st.write("Please provide your feedback to improve this caption:")
                user_feedback = st.text_area("Your feedback:")
                
                if st.button("Submit Feedback") and user_feedback:
                    st.session_state.feedback_data["initial_feedback"] = user_feedback
                    # Get GPT-4 polished feedback
                    gpt_feedback = get_gpt4_feedback(user_feedback, current_caption, feedback_prompt=FOLDER / args.feedback_prompt)
                    st.session_state.feedback_data["gpt_feedback"] = gpt_feedback
                    st.session_state.current_step = 1
                    st.rerun()
            else:
                # If happiest face, save and finish
                st.session_state.feedback_data["final_caption"] = current_caption
                filename = save_feedback_data(video_id, st.session_state.feedback_data, output_dir=FOLDER / output_dir)
                st.success("Caption rated as perfect! No changes needed.")
                st.json(st.session_state.feedback_data)
    
    # Step 1: Rate GPT's feedback and optionally provide corrected feedback
    elif st.session_state.current_step == 1:
        st.subheader("Rate AI-Polished Feedback")

        # Fetch stored feedback rating if it exists
        if "feedback_rating" in st.session_state:
            score = st.session_state.feedback_rating
        else:
            feedback_response = streamlit_feedback(
                feedback_type="faces",
                key="feedback_faces"
            )

            if feedback_response and 'score' in feedback_response:
                st.session_state.feedback_rating = feedback_response['score']
                score = feedback_response['score']
            else:
                score = None  # Default to None if no response yet

        if score:
            st.session_state.feedback_data["feedback_rating"] = score  # Store in feedback data
            st.session_state.feedback_data["feedback_rating_score"] = emoji_to_score(score)  # Store numeric rating
            
            if score != "😀":
                st.write("Please modify the feedback below:")

                # Ensure final_feedback is stored persistently
                if "final_feedback" not in st.session_state:
                    st.session_state.final_feedback = st.session_state.feedback_data["gpt_feedback"]

                final_feedback = st.text_area(
                    "Correct feedback:",
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

                        st.rerun()  # Force rerun
                    else:
                        st.warning("Please provide a corrected feedback before submitting.")
                        st.rerun()
            else:
                # If rating is happy, then directly use the GPT feedback as final feedback
                st.session_state.feedback_data["final_feedback"] = st.session_state.feedback_data["gpt_feedback"]
                st.session_state.current_step = 2
                st.session_state.feedback_submitted = True  # Flag to track submission

        # Ensure we move to the next step on rerun
        if st.session_state.get("feedback_submitted", False):
            st.session_state.feedback_submitted = False  # Reset flag
            st.session_state.current_step = 2  # Ensure next step persists
            st.rerun()




    
    # Step 2: Generate caption (intermediate step)
    elif st.session_state.current_step == 2:
        # Get the final feedback (either corrected or GPT's version)
        final_feedback = st.session_state.feedback_data["final_feedback"]
        # Get improved caption
        gpt_caption = get_gpt4_caption(final_feedback, current_caption, caption_prompt=FOLDER / args.caption_prompt)
        st.session_state.feedback_data["gpt_caption"] = gpt_caption
        # Move to caption rating step
        st.session_state.current_step = 3
        st.rerun()
    
    # Step 3: Rate GPT's caption and optionally provide corrected caption
    elif st.session_state.current_step == 3:
        st.subheader("Rate AI-Improved Caption")
        st.write(st.session_state.feedback_data["gpt_caption"])

        # Retrieve stored caption rating if it exists
        if "caption_rating" in st.session_state:
            score = st.session_state.caption_rating
        else:
            caption_response = streamlit_feedback(
                feedback_type="faces",
                key="caption_faces"
            )

            if caption_response and 'score' in caption_response:
                st.session_state.caption_rating = caption_response['score']
                score = caption_response['score']
            else:
                score = None  # Default to None if no response yet

        if score:
            st.session_state.feedback_data["caption_rating"] = score  # Persist rating
            st.session_state.feedback_data["caption_rating_score"] = emoji_to_score(score)  # Store numeric rating

            if score != "😀":
                st.write("Please modify the caption below:")

                # Ensure final_caption is stored persistently
                if "final_caption" not in st.session_state:
                    st.session_state.final_caption = st.session_state.feedback_data["gpt_caption"]

                final_caption = st.text_area(
                    "Correct caption:",
                    value=st.session_state.final_caption,
                    key="correct_caption"
                )

                # Button Click Handling
                if st.button("Submit Final Caption"):
                    if final_caption.strip():
                        # Persist final caption
                        st.session_state.feedback_data["final_caption"] = final_caption
                        st.session_state.final_caption = final_caption
                        
                        # Save feedback data
                        filename = save_feedback_data(st.session_state.feedback_data["video_id"], st.session_state.feedback_data, output_dir=FOLDER / output_dir)
                        st.success(f"Feedback saved successfully!")
                        st.json(st.session_state.feedback_data)

            else:
                # If rating is happy, finalize caption and save
                st.session_state.feedback_data["final_caption"] = st.session_state.feedback_data["gpt_caption"]
                filename = save_feedback_data(st.session_state.feedback_data["video_id"], st.session_state.feedback_data, output_dir=FOLDER / output_dir)
                st.success(f"Feedback saved successfully!")
                st.json(st.session_state.feedback_data)


if __name__ == "__main__":
    main()