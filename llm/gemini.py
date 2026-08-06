from google import genai
import google.genai.types as types
from google.genai.types import Part
import google.auth
from google.oauth2 import service_account
from llm.base import LLM
from typing import List
import os
import json
import PIL.Image
from llm.utils import extract_frames_to_pil

PROJECT_ID = "gen-lang-client-0141537462"
# SERVICE_ACCOUNT_FILE = "llm/gemini_key.json"

class Gemini(LLM):
    def __init__(self, model="gemini-2.0-flash-001", api_key=None):
        # If extracted_frames is [], then use the entire video
        assert model in ["gemini-2.0-flash-001", "gemini-2.5-pro", "gemini-3-pro-preview",
            # "gemini-2.5-pro-preview-03-25", "gemini-2.5-pro-preview-05-06", 
            # "gemini-2.0-flash-lite-preview-02-05", "gemini-1.5-flash-001", "gemini-1.5-flash-8b-001", "gemini-1.5-pro-001"
        ]
        os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
        # self.client = genai.Client(api_key=self.api_key, http_options=HttpOptions(api_version="v1"))
        # self.client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        # Define the required OAuth scopes for Vertex AI
        SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

        # Load credentials with explicit scopes
        credentials = service_account.Credentials.from_service_account_info(
            api_key, scopes=SCOPES
        )
        self.client = genai.Client(vertexai=True, credentials=credentials, project=PROJECT_ID, 
                                   location="global")
        self.model = model
    
    def generate(self,
                 prompt: str,
                 images: List[str] = [],
                 video: str = "",
                 extracted_frames: List[int] = [],
                 temperature: float = 0.0,
                 **kwargs) -> str:
        """Generate text from a prompt. Optionally provide images or video."""
        if len(images) > 0 and len(video) > 0:
            raise ValueError("Error: Cannot provide both images and video")
        
        if len(images) > 0:
            imagery = [PIL.Image.open(image) for image in images]
        elif len(video) > 0:
            if len(extracted_frames) == 0:
                # Since extracted_frames is [], use the entire video
                imagery = [Part.from_uri(
                    file_uri=video,
                    mime_type=f"video/{video.split('.')[-1]}",
                )]
            else:
                # Extract specific frames from the video
                imagery = extract_frames_to_pil(video, extracted_frames)
        else:
            imagery = []
        
        contents = imagery
        contents.append(prompt)
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=temperature,
                **kwargs
            )
        )
        return response.text.strip()
            
if __name__ == "__main__":
    from streamlit import secrets
    gemini = Gemini(
        # model="gemini-2.0-flash-001",
        # model="gemini-2.5-pro-preview-03-25",
        # model="gemini-2.5-pro-preview-05-06",
        # model="gemini-2.5-pro",
        model="gemini-3-pro-preview",
        api_key=secrets["gemini_key"]
    )
    
    if not gemini.client._api_client.vertexai:
        print(f"Using Gemini Developer API.")
    elif gemini.client._api_client.project:
        print(
            f"Using Vertex AI with project: {gemini.client._api_client.project} in location: {gemini.client._api_client.location}"
        )
    elif gemini.client._api_client.api_key:
        print(
            f"Using Vertex AI in express mode with API key: {gemini.client._api_client.api_key[:5]}...{gemini.client._api_client.api_key[-5:]}"
        )
    print(gemini.generate(
        prompt="Describe this video in a single, concise, and fluent paragraph.",
        video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/OCBYMQzG44U.30.11.mp4",
        extracted_frames=[],
        temperature=0.0,
    ))
    