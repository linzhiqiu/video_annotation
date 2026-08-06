from llm.chatgpt import ChatGPT
from llm.gemini import Gemini
from llm.open_source import OpenSource
# from llm.deepseek import DeepSeek

ALL_MODELS = {
    "ChatGPT": [
        "gpt-4.1-2025-04-14",
        "gpt-4o-2024-08-06",
        "gpt-5-mini",
        "gpt-5.1",
        "gpt-5.2",
        # "gpt-4o-mini-2024-07-18",
        # "o1-2024-12-17",
    ],
    "Gemini": [
                "gemini-2.5-pro",
                "gemini-3-pro-preview",
                #"gemini-2.5-pro-preview-05-06", 
                #"gemini-2.5-pro-preview-03-25", #"gemini-2.0-flash-001", #"gemini-2.0-flash-lite-preview-02-05", 
            #    "gemini-1.5-flash-001", "gemini-1.5-flash-8b-001", "gemini-1.5-pro-001"
               ],
    "OpenSource": [
        "tarsier2-7b",
        "tarsier-recap-7b", 
        # "llava-video-7b", 
        # "llava-video-72B", 
        # "internvl2.5-8b", 
        # "internvideo2-chat-8b-hd", 
        "qwen2.5-vl-7b", 
        "qwen2.5-vl-72b",
        ],
}

def get_llm(model="gpt-4o-2024-08-06", secrets=None):
    if model in ALL_MODELS["ChatGPT"]:
        api_key = secrets["openai_key"]
        return ChatGPT(model=model, api_key=api_key)
    elif model in ALL_MODELS["Gemini"]:
        api_key = secrets["gemini_key"]
        return Gemini(model=model, api_key=api_key)
    elif model in ALL_MODELS["OpenSource"]:
        return OpenSource(model=model)
    # elif model == "deepseek":
    #     return DeepSeek()
    else:
        raise ValueError(f"Error: Invalid LLM model '{model}'")

def get_all_llms():
    model_names = []
    for model_type, models in ALL_MODELS.items():
        model_names.extend(models)
    return model_names

def get_supported_mode(model="gpt-4o-2024-08-06"):
    if model in ALL_MODELS["ChatGPT"]:
        return [
            "Image (First-and-Last-Frame)",
            "Image (3 frames)",
            "Image (4 frames)",
            "Text Only",
        ]
    elif model in ALL_MODELS["Gemini"]:
        return [
            "Video",
            "Image (First-and-Last-Frame)",
            "Image (3 frames)",
            "Image (4 frames)",
            "Text Only"
        ]
    elif model in ALL_MODELS["OpenSource"]:
        return ["Video"]
    else:
        raise ValueError(f"Error: Invalid LLM model '{model}'")

def api_from_secrets(model="gpt-4o-2024-08-06", secrets=None):
    if model in ALL_MODELS["ChatGPT"]:
        return secrets["openai_key"]
    elif model in ALL_MODELS["Gemini"]:
        return secrets["gemini_key"]
    else:
        raise ValueError(f"Error: Invalid LLM model '{model}'")
