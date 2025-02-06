import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from video_data import VideoData
from ..params.caption_result import CaptionResult, VideoCaptionResults
from .generator import CaptionGenerator, ModelType, CaptionRule
from caption_data import CaptionType

class CaptionProcessor:
    """Handles the workflow of generating and saving captions for videos."""
    
    def __init__(self, generator: CaptionGenerator, output_dir: str):
        """Initialize the processor.
        
        Args:
            generator: Configured CaptionGenerator instance
            output_dir: Directory to save caption results
        """
        self.generator = generator
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _format_instruction(self, template: str, video: VideoData) -> str:
        """Format instruction template with video data.
        
        Args:
            template: Instruction template with placeholders
            video: VideoData object to use for formatting
            
        Returns:
            Formatted instruction string
        """
        # Create a context dictionary with all video attributes
        context = {
            'self': video  # Allow direct access to video object in template
        }
        
        try:
            # Use eval to handle complex expressions in the template
            # This is safe because we control the template content
            return eval(f"f'''{template}'''", context)
        except Exception as e:
            logging.error(f"Error formatting instruction: {str(e)}")
            return template
    
    def _generate_caption(self, video: VideoData, rule: CaptionRule) -> Optional[CaptionResult]:
        """Generate a caption for a video using the specified rule.
        
        Args:
            video: VideoData object
            rule: CaptionRule to apply
            
        Returns:
            CaptionResult if successful, None otherwise
        """
        try:
            # Get instruction data
            instruction_data = self.generator.instructions.get(rule.caption_type)
            if not instruction_data:
                raise ValueError(f"No instructions found for {rule.caption_type}")
            
            # Format the instruction template
            template = instruction_data['instruction_template']
            final_instruction = self._format_instruction(template, video)
            
            # Get model settings
            model_settings = instruction_data.get('model settings', {})
            if rule.additional_params:
                model_settings.update(rule.additional_params)
            
            # TODO: Implement actual model call here
            # For now, return placeholder
            output_caption = "Placeholder caption"
            
            return CaptionResult(
                caption_type=rule.caption_type,
                model_name=rule.model.value,
                instruction_template=template,
                final_instruction=final_instruction,
                output_caption=output_caption,
                timestamp=datetime.now().isoformat(),
                model_params=model_settings
            )
            
        except Exception as e:
            logging.error(f"Error generating caption for {rule.caption_type}: {str(e)}")
            return None
    
    def process_video(self, video_name: str, video: VideoData) -> Optional[VideoCaptionResults]:
        """Process a single video and generate all configured captions.
        
        Args:
            video_name: Name/ID of the video
            video: VideoData object
            
        Returns:
            VideoCaptionResults if successful, None otherwise
        """
        try:
            results = VideoCaptionResults(video_name)
            
            for rule in self.generator.rules:
                caption_result = self._generate_caption(video, rule)
                if caption_result:
                    results.add_caption(caption_result)
                    
            return results
            
        except Exception as e:
            logging.error(f"Error processing video {video_name}: {str(e)}")
            return None
    
    def process_videos(self, videos: Dict[str, VideoData]) -> Dict[str, VideoCaptionResults]:
        """Process multiple videos and generate captions.
        
        Args:
            videos: Dictionary mapping video names to VideoData objects
            
        Returns:
            Dictionary mapping video names to their caption results
        """
        results = {}
        total = len(videos)
        
        for i, (video_name, video) in enumerate(videos.items(), 1):
            logging.info(f"Processing video {i}/{total}: {video_name}")
            
            video_results = self.process_video(video_name, video)
            if video_results:
                results[video_name] = video_results
                
        return results
    
    def save_results(self, results: Dict[str, VideoCaptionResults], output_file: str) -> None:
        """Save caption results to a JSON file.
        
        Args:
            results: Dictionary of caption results
            output_file: Path to save the results
        """
        output_path = os.path.join(self.output_dir, output_file)
        
        # Convert results to dictionary format
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(results),
            'results': {
                name: result.to_dict()
                for name, result in results.items()
            }
        }
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logging.info(f"Results saved to {output_path}")
    
    def load_results(self, input_file: str) -> Dict[str, VideoCaptionResults]:
        """Load caption results from a JSON file.
        
        Args:
            input_file: Path to the results file
            
        Returns:
            Dictionary mapping video names to their caption results
        """
        input_path = os.path.join(self.output_dir, input_file)
        
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        return {
            name: VideoCaptionResults.from_dict(result_data)
            for name, result_data in data['results'].items()
        } 