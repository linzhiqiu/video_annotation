#!/usr/bin/env python3
"""
Extract Merged Caption Configuration

Extracts the prompt template from the Streamlit app and saves to JSON.

Usage:
    python extract_merged_caption_config.py
    python extract_merged_caption_config.py --output custom_config.json
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def extract_config(output_path: str = "summary_caption_config.json"):
    """Extract config from Streamlit app and save to JSON."""
    
    # Import from Streamlit app (required)
    from caption.json_and_summary_caption_streamlit import MultiCaptionLLMApp
    app = MultiCaptionLLMApp("main")
    
    config = {
        "prompt_template": app.TASKS["summary_generation"]["default_instruction"],
        "required_keys": ["subject", "scene", "motion", "spatial", "camera"],
        "default_model": "gpt-5.2",
        "_metadata": {
            "generated_at": datetime.now().isoformat(),
            "description": "Configuration for merged caption generation API"
        }
    }
    
    # Save
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted prompt from Streamlit app")
    print(f"💾 Saved to: {output_file}")
    return config


def main():
    parser = argparse.ArgumentParser(description="Extract merged caption config")
    parser.add_argument("--output", "-o", default="summary_caption_config.json", help="Output path")
    args = parser.parse_args()
    extract_config(args.output)


if __name__ == "__main__":
    main()