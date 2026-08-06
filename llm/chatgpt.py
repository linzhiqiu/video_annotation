from openai import OpenAI
from llm.base import LLM
from typing import List
import os
import base64
from llm.utils import extract_frames_to_base64, load_text


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class ChatGPT(LLM):
    def __init__(self, model="gpt-4o-2024-08-06", api_key=None):
        assert model in ["gpt-5-mini", "gpt-5.1", "gpt-5.2", "gpt-4.1-2025-04-14", "gpt-4o-2024-08-06", "gpt-4o-mini-2024-07-18", "o1-2024-12-17"]
        self.api_key = api_key
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.client = OpenAI()
        self.model = model
    
    def generate(self,
                 prompt: str,
                 images: List[str] = [],
                 video: str = "",
                 extracted_frames: List[int] = [],
                 detail: str = "low",
                 temperature: float = 0.0,
                 **kwargs) -> str:
        """Generate text from a prompt. Optionally provide images or video."""
        if len(images) > 0 and len(video) > 0:
            raise ValueError("Error: Cannot provide both images and video")
        
        if len(images) > 0:
            images = [encode_image(image) for image in images]
        elif len(video) > 0:
            images = extract_frames_to_base64(video, extracted_frames)
        else:
            images = []
        
        images = [{
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": detail
            }
        } for base64_image in images]
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        messages[0]["content"].extend(images)
        # print(f"Sending prompt to model: {prompt}")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs
        )
        print(f"Received response from model")
        return response.choices[0].message.content.strip()
            
if __name__ == "__main__":
    # chatgpt = ChatGPT(model="gpt-4o-2024-08-06")
    chatgpt = ChatGPT(model="gpt-4.1-2025-04-14")
    print(chatgpt.generate(
        prompt="Describe this video in a concise and fluent manner.",
        video="https://huggingface.co/datasets/zhiqiulin/video_captioning/resolve/main/OCBYMQzG44U.30.11.mp4",
        extracted_frames=[0, -1],
        detail="low",
        temperature=0.0,
    ))
    