#!/usr/bin/env python3
"""
Merged Caption Generation API

Generates merged captions from five caption types using LLM.

Usage:
    from merged_caption_api import merge_captions
    
    captions = {
        "subject": "A person walking...",
        "scene": "An outdoor park...",
        "motion": "The person moves slowly...",
        "spatial": "In the center of the frame...",
        "camera": "The camera pans left..."
    }
    
    result = merge_captions(captions, secrets={"openai_key": "sk-..."})
    print(result.merged_caption)
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


# =============================================================================
# ENVIRONMENT LOADING
# =============================================================================

def load_env_file(env_path: str = ".env") -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    env_file = Path(env_path)
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
    
    return env_vars


# =============================================================================
# LLM IMPLEMENTATIONS
# =============================================================================

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.0, **kwargs) -> str:
        pass


class ChatGPT(BaseLLM):
    VALID_MODELS = [
        "gpt-5-mini", "gpt-5.1", "gpt-5.2", 
        "gpt-4.1-2025-04-14", "gpt-4o-2024-08-06", 
        "gpt-4o-mini-2024-07-18", "o1-2024-12-17"
    ]
    
    def __init__(self, model: str = "gpt-5.2", api_key: str = None):
        if model not in self.VALID_MODELS:
            raise ValueError(f"Model {model} not in {self.VALID_MODELS}")
        
        self.api_key = api_key
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        try:
            from openai import OpenAI
            self.client = OpenAI()
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")
        
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.0, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs
        )
        return response.choices[0].message.content.strip()


class Gemini(BaseLLM):
    VALID_MODELS = ["gemini-2.5-pro", "gemini-3-pro-preview"]
    
    def __init__(self, model: str = "gemini-2.5-pro", api_key: str = None):
        if model not in self.VALID_MODELS:
            raise ValueError(f"Model {model} not in {self.VALID_MODELS}")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
        except ImportError:
            raise ImportError("google-generativeai required. Install with: pip install google-generativeai")
        
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.0, **kwargs) -> str:
        response = self.client.generate_content(prompt)
        return response.text if response.text else ""


ALL_MODELS = {
    "ChatGPT": ChatGPT.VALID_MODELS,
    "Gemini": Gemini.VALID_MODELS,
}


def get_llm(model: str = "gpt-5.2", secrets: Optional[Dict[str, Any]] = None) -> BaseLLM:
    """Get LLM instance."""
    secrets = secrets or {}
    
    if not secrets:
        secrets = load_env_file()
    
    if model in ALL_MODELS["ChatGPT"]:
        api_key = secrets.get("openai_key") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("openai_key not found in secrets, .env, or environment")
        return ChatGPT(model=model, api_key=api_key)
    
    elif model in ALL_MODELS["Gemini"]:
        api_key = secrets.get("gemini_key") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("gemini_key not found in secrets or environment")
        return Gemini(model=model, api_key=api_key)
    
    else:
        raise ValueError(f"Invalid model '{model}'")


# =============================================================================
# CONSTANTS
# =============================================================================

REQUIRED_KEYS = ["subject", "scene", "motion", "spatial", "camera"]

DEFAULT_PROMPT_TEMPLATE = """Please merge the following five captions into a single, comprehensive caption that describes the video completely without any redundancy.

Caption Types:
1. Subject: Describes the subjects/people in the video
2. Scene: Describes the scene composition and environment
3. Motion: Describes the movement and dynamics of subjects
4. Spatial: Describes the spatial relationships and framing
5. Camera: Describes camera movements and framing choices

Input Captions:
{captions}

Instructions:
1. Use the SPATIAL caption as your BASE structure - it provides the core visual description and framing
2. Merge MOTION and CAMERA captions into the spatial description to create a temporally coherent narrative that describes how things change over time
3. Add information from SUBJECT and SCENE captions ONLY if they contain unique details not already covered in the Spatial caption
4. Eliminate ALL redundant information - if the same detail appears in multiple captions, mention it only ONCE
5. Preserve the EXACT wording from the original captions - do NOT paraphrase
6. When describing temporal changes, integrate motion and camera movements in chronological order to show how the scene evolves
7. CRITICAL: Every unique detail from all five captions must appear in the final merged caption - nothing should be omitted
8. Do NOT add any information not present in the original captions
9. Return only the merged caption without any additional text or formatting

Goal: A single, temporally coherent caption based on the Spatial description, with Motion and Camera information merged chronologically, and Subject/Scene details added only when they provide new information. Keep as many details as possible but limit to at most 320 words."""


# =============================================================================
# RESULT DATA CLASS
# =============================================================================

@dataclass
class MergeResult:
    """Result of merged caption generation"""
    success: bool
    merged_caption: Optional[str]
    error_message: Optional[str]
    word_count: int
    token_count: int


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def count_tokens(text: str) -> int:
    """Approximate token count (0.75 words per token)"""
    return int(len(text.split()) / 0.75)


def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())


def format_captions(captions: Dict[str, str]) -> str:
    """
    Format captions dict into string for prompt.
    
    Input: {"subject": "...", "scene": "...", ...}
    Output: "Subject: ...\n\nScene: ...\n\n..."
    """
    order = ["subject", "scene", "motion", "spatial", "camera"]
    parts = []
    for key in order:
        if key in captions:
            display_name = key.capitalize()
            parts.append(f"{display_name}: {captions[key]}")
    return "\n\n".join(parts)


def clean_response(response: str) -> str:
    """Clean LLM response (remove markdown code blocks, etc.)"""
    response = response.strip()
    
    if response.startswith('```'):
        lines = response.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        response = '\n'.join(lines).strip()
    
    return response


# =============================================================================
# MAIN API CLASS
# =============================================================================

class MergedCaptionAPI:
    """
    API for generating merged captions from five caption types.
    
    Example:
        api = MergedCaptionAPI(secrets={"openai_key": "sk-..."})
        
        captions = {
            "subject": "A person walking...",
            "scene": "An outdoor park...",
            "motion": "The person moves slowly...",
            "spatial": "In the center of the frame...",
            "camera": "The camera pans left..."
        }
        
        result = api.merge(captions)
        if result.success:
            print(result.merged_caption)
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        secrets: Optional[Dict] = None
    ):
        """
        Initialize the API.
        
        Args:
            config_path: Path to summary_caption_config.json (optional)
            secrets: Dict with API keys (openai_key, gemini_key)
        """
        self.secrets = secrets or {}
        
        if not self.secrets:
            self.secrets = load_env_file()
        
        # Load config
        self.config = self._load_config(config_path)
        self.prompt_template = self.config.get("prompt_template", DEFAULT_PROMPT_TEMPLATE)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from JSON file or use defaults."""
        paths_to_try = [config_path] if config_path else []
        paths_to_try.extend([
            "summary_caption_config.json",
            "json_policy/summary_caption_config.json",
        ])
        
        for path in paths_to_try:
            if path and Path(path).exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        return {"prompt_template": DEFAULT_PROMPT_TEMPLATE}
    
    def merge(
        self,
        captions: Dict[str, str],
        model: str = "gpt-5.2",
        temperature: float = 0.0,
        verbose: bool = False
    ) -> MergeResult:
        """
        Merge five captions into a single comprehensive caption.
        
        Args:
            captions: Dict with keys: subject, scene, motion, spatial, camera
            model: LLM model to use
            temperature: Generation temperature
            verbose: Print debug info
        
        Returns:
            MergeResult
        """
        # Normalize keys to lowercase
        captions = {k.lower(): v for k, v in captions.items()}
        
        # Validate all required keys present
        missing = [k for k in REQUIRED_KEYS if k not in captions]
        if missing:
            return MergeResult(
                success=False,
                merged_caption=None,
                error_message=f"Missing required captions: {missing}",
                word_count=0,
                token_count=0
            )
        
        # Format captions and build prompt
        formatted = format_captions(captions)
        prompt = self.prompt_template.replace("{captions}", formatted)
        
        # Get LLM
        try:
            llm = get_llm(model=model, secrets=self.secrets)
        except Exception as e:
            return MergeResult(
                success=False,
                merged_caption=None,
                error_message=f"Failed to initialize LLM: {e}",
                word_count=0,
                token_count=0
            )
        
        # Generate
        try:
            if verbose:
                print(f"Calling {model}...")
            
            response = llm.generate(prompt, temperature=temperature)
            
            if not response or not response.strip():
                return MergeResult(
                    success=False,
                    merged_caption=None,
                    error_message="LLM returned empty response",
                    word_count=0,
                    token_count=0
                )
            
            cleaned = clean_response(response)
            word_count = count_words(cleaned)
            token_count = count_tokens(cleaned)
            
            if verbose:
                print(f"  Words: {word_count}, Tokens: {token_count}")
            
            return MergeResult(
                success=True,
                merged_caption=cleaned,
                error_message=None,
                word_count=word_count,
                token_count=token_count
            )
            
        except Exception as e:
            return MergeResult(
                success=False,
                merged_caption=None,
                error_message=str(e),
                word_count=0,
                token_count=0
            )


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def merge_captions(
    captions: Dict[str, str],
    model: str = "gpt-5.2",
    temperature: float = 0.0,
    secrets: Optional[Dict] = None,
    config_path: Optional[str] = None,
    verbose: bool = False
) -> MergeResult:
    """
    Merge five captions into one.
    
    Args:
        captions: Dict with keys: subject, scene, motion, spatial, camera
        model: LLM model
        temperature: Generation temperature  
        secrets: API keys dict (openai_key, gemini_key)
        config_path: Path to config JSON
        verbose: Debug output
    
    Returns:
        MergeResult
    
    Example:
        result = merge_captions({
            "subject": "A person...",
            "scene": "A park...",
            "motion": "Walking...",
            "spatial": "Center frame...",
            "camera": "Panning..."
        })
    """
    api = MergedCaptionAPI(config_path=config_path, secrets=secrets)
    return api.merge(
        captions=captions,
        model=model,
        temperature=temperature,
        verbose=verbose
    )


# =============================================================================
# EXAMPLE
# =============================================================================

EXAMPLE_CAPTIONS = {
    "subject": """The video features a gray, angular aircraft marked with "UNSC" on its top surface, flying forward. It has two large, bright blue glowing engines at the rear, flanking a central cockpit area with two smaller, purple glowing engines. Initially, the aircraft is viewed from a rear-facing, slightly elevated perspective as it moves through a metallic, enclosed tunnel with red and white striped markings on the side walls and "UNSC INFINITY" written on an overhead arch. The tunnel also includes overhead structures with yellow markings and numbers like "3". The aircraft then exits the tunnel into a vast, open area filled with towering, dark, jagged, crystalline-like structures. In the distance, a crystalline energy sphere emits an orange energy field, partially obscured by a crystalline disc-shaped portal. A smaller, dark spherical object is positioned in front of this portal. On-screen overlay elements include a "BOOST" meter in the top left, initially at 0% and later at 100%, and text prompts like "USE [D] TO BOOST PELICAN" and "USE [D] TO TURN PELICAN." After accelerating, an overlay text "USE RS TO TURN RELICAN" appears in the upper-middle section of the frame. A small, green aircraft icon is visible in a circular radar display in the bottom left, and a "CHECKPOINT ... DONE" message appears. A targeting reticle is located in the center of the screen, along with an icon representing a weapon in the upper right.""",
    
    "scene": """A third-person 3D game video where the entire character is visible on screen shows a grey, metallic UNSC Pelican spacecraft with prominent, glowing blue back engines. The video begins with the Pelican accelerating through a narrow, grey, metallic launch tube, which has "UNSC" and "INFINITY" inscribed on an archway and features red and white striped warning markings on its interior walls, heading towards a bright light at the end. As the spacecraft exits the launch tube, the view expands to reveal a more open, outdoor aerial environment. The scene then transitions to an expansive, alien outdoor environment where the Pelican flies towards a large, dark, spherical object partially obscured by a glowing, reddish-orange, circular energy field or portal. This portal is framed by massive, dark, angular, crystalline or metallic structures scattered throughout the frame, extending vertically across the entire scene from a cloudy or gaseous surface below, under a bright, hazy sky. A disc-shaped portal or similar object is positioned at the top of the frame. Throughout the video, overlay elements are present: a "BOOST" meter with a star icon in the top left corner (showing 0% then 100%); a control prompt "USE [LT icon] TO BOOST PELICAN" (later changing to "USE [RS icon] TO TURN PELICAN") at the top center; and in the latter part, a "CHECKPOINT ... DONE" message with a small green aircraft icon in a circular reticle in the bottom left, a weapon icon in the top right, and a blue, translucent, hexagonal targeting reticle in the center.""",
    
    "motion": """The video begins with a view of a spaceship inside a large, enclosed tunnel, with the spaceship's engines glowing brightly. As the spaceship starts to move forward, the camera follows, creating the impression that the tunnel's interior is moving backward, with its metallic walls and structural elements. As the spaceship progresses, it exits the tunnel, revealing an exterior space filled with large, crystalline structures. The spaceship accelerates again, moving faster and leaving a visible trail behind, as the exterior space becomes more visible, showing a vast, open area with a large, glowing orange energy sphere in the background. The on-screen overlay elements, including a 'BOOST' meter and text prompts, remain visible throughout the transition.""",
    
    "spatial": """The video employs a consistent wide shot, with the camera positioned above and trailing a central aircraft. Initially, this aircraft is in the foreground, advancing through an enclosed tunnel whose walls and ceiling elements are visible on the left, right, and top of the frame, receding from foreground to background. The tunnel's exit, initially in the distant background center, expands as the aircraft approaches. Upon emerging, the aircraft maintains its center-foreground position, now navigating an open expanse towards a prominent energy sphere and a smaller dark orb, both located in the background center. This destination is flanked by large, dark crystalline structures positioned on the left, right, and in the further background. Throughout the sequence, various HUD elements, including a boost meter (top left), control prompts (top center), a radar display (bottom left), and a weapon icon (top right), are fixed in the foreground, with a targeting reticle also appearing in the foreground, centered on the distant objects.""",
    
    "camera": """The camera starts at an overhead level, approximately second-floor height, positioned above the spaceship relative to its height. It transitions to an aerial level as the spaceship exits the tunnel, maintaining a level angle looking straight ahead. The shot employs deep focus with a large depth of field. The camera moves forward, tracking the spaceship from above and behind, with a slightly unsteady movement that includes some shaking."""
}


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Merge five captions into one")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--model", default="gpt-5.2", help="LLM model")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.demo:
        print("=" * 60)
        print("DEMO: Merging 5 captions")
        print("=" * 60)
        
        print("\nInput captions:")
        for k, v in EXAMPLE_CAPTIONS.items():
            print(f"  {k}: {v[:60]}...")
        
        print(f"\nGenerating with {args.model}...")
        
        result = merge_captions(
            EXAMPLE_CAPTIONS,
            model=args.model,
            verbose=args.verbose
        )
        
        if result.success:
            print(f"\n✅ Success ({result.word_count} words, ~{result.token_count} tokens)")
            print("-" * 60)
            print(result.merged_caption)
        else:
            print(f"\n❌ Failed: {result.error_message}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()