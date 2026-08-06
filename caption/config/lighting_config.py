# caption/config/lighting_config.py
from caption.config.base_config import AppConfig
from caption_policy.prompt_generator import (
    ColorPolicy,
    LightingSetupPolicy,
    LightingEffectsPolicy,
)

# Lighting project video URLs files
LIGHTING_VIDEO_URLS_FILES = [
    "video_urls/lighting_120_new/batch1.json",
    "video_urls/lighting_120_new/batch2.json",
    "video_urls/lighting_120_new/batch3.json",
    "video_urls/lighting_120_new/batch4.json",
    "video_urls/lighting_120_new/batch5.json",
    "video_urls/lighting_120_new/batch6.json",
    "video_urls/lighting_120_new/batch7.json",
    "video_urls/lighting_120_new/batch8.json",
    "video_urls/lighting_120_new/batch9.json",
    "video_urls/lighting_120_new/batch10.json",
    "video_urls/lighting_250_new/batch11.json",
    "video_urls/lighting_250_new/batch12.json",
    "video_urls/lighting_250_new/batch13.json",
    "video_urls/lighting_250_new/batch14.json",
    "video_urls/lighting_250_new/batch15.json",
    "video_urls/lighting_250_new/batch16.json",
    "video_urls/lighting_250_new/batch17.json",
    "video_urls/lighting_250_new/batch18.json",
    "video_urls/lighting_250_new/batch19.json",
    "video_urls/lighting_250_new/batch20.json",
    'video_urls/lighting_280_new/batch21.json',
    'video_urls/lighting_280_new/batch22.json',
    'video_urls/lighting_280_new/batch23.json',
    'video_urls/lighting_280_new/invalid_videos.json',
]

def get_lighting_config() -> AppConfig:
    """Get lighting annotation configuration"""
    caption_programs = {
        "raw_color_composition_dynamics": ColorPolicy(),
        "raw_lighting_setup_dynamics": LightingSetupPolicy(),
        "raw_lighting_effects_dynamics": LightingEffectsPolicy(),
    }
    
    return AppConfig(
        name="Lighting Video Annotation System",
        configs_file="lighting_configs.json",
        video_urls_files=LIGHTING_VIDEO_URLS_FILES,
        video_data_file="video_data/20250406lighting_only/videos.json",
        label_collections=["lighting_setup"],
        caption_programs=caption_programs,
    )