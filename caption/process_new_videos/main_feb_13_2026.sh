#!/bin/bash

# Process new overlapping videos from February 13 dataset
python caption/process_new_videos.py \
    --new-dir "caption/video_urls/20260213_ground_and_setup_folder" \
    --valid-filename "overlap_all_1826.json" \
    --invalid-filename-overlap "caption/video_urls/20260213_ground_and_setup_folder/overlap_invalid.json" \
    --batch-files \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_188_to_282.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_282_to_376.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_376_to_470.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_470_to_564.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_564_to_658.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_658_to_752.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_752_to_846.json" \
        "caption/video_urls/20250227_0507ground_and_setup/overlap_846_to_940.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_940_to_950.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_950_to_960.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_960_to_970.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_970_to_980.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_980_to_990.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_990_to_1000.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_1000_to_1010.json" \
        "caption/video_urls/20250406_setup_and_motion/overlap_1010_to_1020.json" \
        "caption/video_urls/20250912_setup_and_motion/overlap_1020_to_1030.json" \
        "caption/video_urls/20250912_setup_and_motion/overlap_1030_to_1040.json" \
        "caption/video_urls/20250912_setup_and_motion/overlap_1040_to_1050.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1050_to_1060.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1060_to_1070.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1070_to_1080.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1080_to_1090.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1090_to_1100.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1100_to_1110.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1110_to_1120.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1120_to_1130.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1130_to_1140.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1140_to_1150.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1150_to_1160.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1160_to_1170.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1170_to_1180.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1180_to_1190.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1190_to_1200.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1200_to_1210.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1210_to_1220.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1220_to_1230.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1230_to_1240.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1240_to_1250.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1250_to_1260.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1260_to_1270.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1270_to_1280.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1280_to_1290.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1290_to_1300.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1300_to_1310.json" \
        "caption/video_urls/20251021_ground_and_setup_folder/overlap_1310_to_1320.json" \
    --batch-size 10 \
    --naming-mode overlap

