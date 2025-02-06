from typing import List, Dict, Any
import torch
from transformers import LlavaForConditionalGeneration
from .base_model import BaseCaptionModel, CaptionInput, CaptionOutput
from .custom_processor import TarsierProcessor
import logging
import os
from PIL import Image
import decord
import numpy as np
from ..utils.file_utils import find_video_files

def sample_frame_indices(total_frames: int, n_frames: int):
    """Sample frame indices uniformly from video."""
    if n_frames == 1:
        return [0]  # sample first frame by default
    indices = [round(i * (total_frames - 1) / (n_frames - 1)) for i in range(n_frames)]
    return indices

def sample_video_frames(video_path: str, n_frames: int = 8) -> List[Image.Image]:
    """Sample frames from video uniformly."""
    assert os.path.exists(video_path), f"Video file not found: {video_path}"
    
    # Read video
    vr = decord.VideoReader(video_path, num_threads=1, ctx=decord.cpu(0))
    total_frames = len(vr)
    
    # Sample frame indices
    frame_indices = sample_frame_indices(total_frames, n_frames)
    
    # Get frames
    frames = vr.get_batch(frame_indices).asnumpy()
    frames = [Image.fromarray(f).convert('RGB') for f in frames]
    return frames

class Tarsier7bModel(BaseCaptionModel):
    """Implementation for Tarsier-7b model."""
    
    REQUIRED_PARAMS = {'temperature', 'max_new_tokens', 'top_p'}
    DEFAULT_PARAMS = {
        'temperature': 0.2,
        'max_new_tokens': 512,
        'top_p': 1.0,
        'do_sample': True,
        'use_cache': True,
        'max_n_frames': 8,
        'top_k': 1
    }
    
    def __init__(self):
        """Initialize the model."""
        self.model = None
        self.processor = None
        
    def _ensure_model_loaded(self):
        """Load model if not already loaded."""
        if self.model is None or self.processor is None:
            logging.info("Loading Tarsier-7b model and processor...")
            try:
                self.processor = TarsierProcessor(
                    "omni-research/Tarsier-7b",
                    max_n_frames=self.DEFAULT_PARAMS['max_n_frames']
                )
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    "omni-research/Tarsier-7b",
                    device_map='auto',
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                )
                self.model.eval()
                logging.info("Model loaded successfully")
            except Exception as e:
                logging.error(f"Error loading model: {str(e)}")
                raise
    
    def validate_model_params(self, params: Dict[str, Any]) -> bool:
        """Validate Tarsier model parameters."""
        # First merge with default parameters
        full_params = self.DEFAULT_PARAMS.copy()
        full_params.update(params)
        
        # Check required parameters are present
        if not all(param in full_params for param in self.REQUIRED_PARAMS):
            logging.error(f"Missing required parameters. Required: {self.REQUIRED_PARAMS}")
            return False
            
        # Validate parameter ranges
        if not (0 <= full_params['temperature'] <= 1):
            logging.error(f"Invalid temperature: {full_params['temperature']}")
            return False
        if not (0 < full_params['max_new_tokens'] <= 2048):
            logging.error(f"Invalid max_new_tokens: {full_params['max_new_tokens']}")
            return False
        if not (0 <= full_params['top_p'] <= 1):
            logging.error(f"Invalid top_p: {full_params['top_p']}")
            return False
            
        return True
    
    def generate_captions(self, inputs: List[CaptionInput]) -> List[CaptionOutput]:
        """Generate captions using Tarsier-7b model."""
        self._ensure_model_loaded()
        outputs = []
        
        if not inputs:
            return outputs
            
        # Use videos_dir from input
        videos_dir = inputs[0].videos_dir
        logging.info(f"Looking for videos in: {videos_dir}")
        video_names = {input_data.video_name for input_data in inputs}
        video_paths = find_video_files(videos_dir, video_names)
        logging.info(f"Found video paths: {video_paths}")
        
        for input_data in inputs:
            try:
                logging.info(f"\nProcessing video: {input_data.video_name}")
                
                # Merge with default parameters
                model_params = self.DEFAULT_PARAMS.copy()
                model_params.update(input_data.model_params)
                logging.info(f"Model parameters: {model_params}")
                
                if not self.validate_model_params(model_params):
                    raise ValueError(f"Invalid model parameters for {input_data.video_name}")
                
                # Get video path
                if input_data.video_name not in video_paths:
                    raise FileNotFoundError(f"Video file not found: {input_data.video_name}")
                video_path = video_paths[input_data.video_name]
                logging.info(f"Video path: {video_path}")
                
                # Sample frames from video
                logging.info("Sampling frames from video...")
                frames = sample_video_frames(
                    video_path, 
                    n_frames=model_params.get('max_n_frames', self.DEFAULT_PARAMS['max_n_frames'])
                )
                logging.info(f"Sampled {len(frames)} frames")
                
                # Process inputs
                logging.info("Processing inputs with processor...")
                logging.info(f"Input instruction: {input_data.instruction}")
                formatted_instruction = f"USER: <video> {input_data.instruction} ASSISTANT:"
                model_inputs = self.processor(
                    text=formatted_instruction,
                    images=frames,
                    return_tensors="pt"
                )
                
                # Move input tensors to the correct device
                input_ids = model_inputs['input_ids'].to(self.model.device)
                pixel_values = model_inputs['pixel_values'].to(self.model.device)
                model_inputs = {
                    'input_ids': input_ids,
                    'pixel_values': pixel_values
                }
                
                logging.info(f"Processor output keys: {model_inputs.keys()}")
                logging.info(f"input_ids shape: {model_inputs['input_ids'].shape}")
                logging.info(f"pixel_values shape: {model_inputs['pixel_values'].shape}")
                
                # Generate caption
                logging.info("Generating caption...")
                generate_kwargs = {
                    'do_sample': model_params.get('do_sample', self.DEFAULT_PARAMS['do_sample']),
                    'max_new_tokens': model_params.get('max_new_tokens', self.DEFAULT_PARAMS['max_new_tokens']),
                    'top_p': model_params.get('top_p', self.DEFAULT_PARAMS['top_p']),
                    'temperature': model_params.get('temperature', self.DEFAULT_PARAMS['temperature']),
                    'use_cache': model_params.get('use_cache', self.DEFAULT_PARAMS['use_cache']),
                    'top_k': model_params.get('top_k', self.DEFAULT_PARAMS['top_k'])
                }
                logging.info(f"Generation parameters: {generate_kwargs}")
                
                outputs_ids = self.model.generate(
                    **model_inputs,
                    **generate_kwargs
                )
                
                # Decode output
                caption = self.processor.tokenizer.decode(
                    outputs_ids[0][model_inputs['input_ids'][0].shape[0]:],
                    skip_special_tokens=True
                )
                logging.info(f"Generated caption: {caption}")
                
                output = CaptionOutput(
                    video_name=input_data.video_name,
                    instruction=input_data.instruction,
                    caption=caption,
                    model_params=model_params
                )
                outputs.append(output)
                
            except Exception as e:
                logging.error(f"Error generating caption for {input_data.video_name}: {str(e)}")
                logging.error("Full error:", exc_info=True)  # This will print the full traceback
                # Add a failed output
                output = CaptionOutput(
                    video_name=input_data.video_name,
                    instruction=input_data.instruction,
                    caption=f"Error generating caption: {str(e)}",
                    model_params=input_data.model_params
                )
                outputs.append(output)
                continue
        
        return outputs

class Tarsier35bModel(BaseCaptionModel):
    """Implementation for Tarsier-35b model."""
    
    REQUIRED_PARAMS = {'temperature', 'max_length', 'top_k'}
    OPTIONAL_PARAMS = {'top_p', 'repetition_penalty', 'presence_penalty'}
    
    def validate_model_params(self, params: Dict[str, Any]) -> bool:
        """Validate Tarsier model parameters."""
        # Check required parameters are present
        if not all(param in params for param in self.REQUIRED_PARAMS):
            return False
            
        # Validate parameter ranges
        if not (0 <= params['temperature'] <= 1):
            return False
        if not (0 < params['max_length'] <= 2000):  # 35b allows longer outputs
            return False
        if not (0 < params['top_k'] <= 100):
            return False
            
        # Validate optional parameters if present
        if 'top_p' in params and not (0 <= params['top_p'] <= 1):
            return False
        if 'repetition_penalty' in params and not (1 <= params['repetition_penalty'] <= 2):
            return False
        if 'presence_penalty' in params and not (0 <= params['presence_penalty'] <= 1):
            return False
            
        return True
    
    def generate_captions(self, inputs: List[CaptionInput]) -> List[CaptionOutput]:
        """Generate captions using Tarsier-35b model."""
        outputs = []
        
        for input_data in inputs:
            if not self.validate_model_params(input_data.model_params):
                raise ValueError(f"Invalid model parameters for {input_data.video_name}")
            
            # TODO: Implement actual model call using transformers
            # For now, return placeholder
            output = CaptionOutput(
                video_name=input_data.video_name,
                instruction=input_data.instruction,
                caption="Placeholder caption from Tarsier-35b",
                model_params=input_data.model_params
            )
            outputs.append(output)
        
        return outputs 