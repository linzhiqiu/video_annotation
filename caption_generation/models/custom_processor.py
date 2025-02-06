"""Custom processor implementation for Tarsier models."""

from PIL import Image
from typing import List
import torch
from transformers import LlavaProcessor
import re
import logging

class CustomImageProcessor:
    def __init__(self, processor) -> None:
        self.processor = processor

    def __call__(self, images: List[Image.Image], do_padding=False) -> torch.Tensor:
        if do_padding:
            images = [self.expand2square(
                img,
                tuple(int(x * 255) for x in self.processor.image_processor.image_mean)
            ) for img in images]
        else:
            images = [self.resize2square(img) for img in images]
        images_pixel = self.processor(text="", images=images, return_tensors="pt")['pixel_values']
        return images_pixel  # [num_images, 3, 336, 336]

    def expand2square(self, pil_img, background_color):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    def resize2square(self, pil_img: Image.Image):
        width, height = pil_img.size
        pil_img = pil_img.resize((max(width, height), max(width, height)))
        return pil_img

class TarsierProcessor:
    def __init__(
            self,
            model_name_or_path,
            max_n_frames=8,
            max_seq_len=None,
            add_sep=False,
            do_image_padding=False,
        ):
        self.max_n_frames = max_n_frames
        self.max_seq_len = max_seq_len
        self.add_sep = add_sep
        self.do_image_padding = do_image_padding
        
        self.setup(model_name_or_path)
    
    def setup(self, model_name_or_path):
        sub_processor = LlavaProcessor.from_pretrained(
            model_name_or_path,
            padding_side='left',
            trust_remote_code=True,
        )
        self.processor = CustomImageProcessor(sub_processor)
        self.tokenizer = sub_processor.tokenizer
        self.sep_id = self.tokenizer.sep_token_id
        self.pad_id = self.tokenizer.pad_token_id
        self.eos_id = self.tokenizer.eos_token_id

        if self.sep_id is None:
            self.add_sep = False
        if not self.max_seq_len:
            self.max_seq_len = self.tokenizer.model_max_length

    def process_prompt(self, prompt, images: List[Image.Image]=None):
        """Process the prompt to include correct number of image tokens.
        
        Args:
            prompt: Input prompt text
            images: List of images to process
            
        Returns:
            Processed prompt with correct number of image tokens
        """
        if not images:
            prompt = prompt.replace("<image>", "").replace("<video>", "")
        elif images is not None:
            # For video prompts, we want to add the correct number of image tokens
            if "<video>" in prompt:
                # Replace <video> with the correct number of <image> tokens
                prompt = prompt.replace("<video>", "<image>" * len(images))
            
            # Count existing image tokens
            image_token_num = len(re.findall('<image>', prompt, re.S))
            
            # If no image tokens or incorrect number, add them at the start of the user message
            if image_token_num != len(images):
                prompt_parts = re.findall(r'USER:(.*)ASSISTANT:(.*)', prompt, re.S)
                if prompt_parts and len(prompt_parts[0]):
                    p1, p2 = prompt_parts[0]
                else:
                    p1 = prompt
                    p2 = ''
                # Remove any existing image tokens and add the correct number
                p1 = re.sub('<image>', '', p1)
                prompt = f"USER: {'<image>' * len(images)} {p1.strip()} ASSISTANT: {p2.strip()}"
        
        if not re.findall(r'USER:(.*)ASSISTANT:(.*)', prompt, re.S):
            prompt = f'USER: {prompt} ASSISTANT: '
        return prompt

    def get_pixel_values(self, images):
        if images is not None and len(images) > 0:
            pixel_values = self.processor(images=images, do_padding=self.do_image_padding)
        else:
            pixel_values = None
        return pixel_values

    def get_text_inputs(self, text):
        prompt_ids = self.tokenizer.encode(text, add_special_tokens=True)  # will add <s>
        if self.add_sep:
            prompt_ids = prompt_ids + [self.sep_id]
        prompt_ids = torch.tensor(prompt_ids, dtype=torch.long).unsqueeze(dim=0)
        return prompt_ids

    def __call__(self, text: str, images: List[Image.Image], return_tensors: str = "pt"):
        """Process inputs for the model.
        
        Args:
            text: Input text prompt
            images: List of PIL images
            return_tensors: Return format for tensors
            
        Returns:
            Dictionary with input_ids and pixel_values
        """
        text = self.process_prompt(text, images)
        text_inputs = self.get_text_inputs(text)
        pixel_values = self.get_pixel_values(images)
        
        return {
            "input_ids": text_inputs,
            "pixel_values": pixel_values
        } 