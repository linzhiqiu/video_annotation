#!/usr/bin/env python3
"""
Generate LaTeX tables from benchmark_config.py for CameraBench Pro
Outputs a static HTML file with all tables for easy viewing and copying
"""

import sys
import re
import argparse
from pathlib import Path

# ============================================================================
# PRIMITIVE GROUPING CONFIGURATION
# ============================================================================
# Three-level hierarchy: Top Level -> Second Level (Aspect) -> Primitives

# EXCLUSION CONFIGURATION
# Add aspect keys here to exclude entire aspects (and all their primitives)
EXCLUDED_ASPECTS = {
    "scene_movement",  # Excludes Scene Dynamics and all its primitives
}

# Add specific primitive names here to exclude individual primitives
EXCLUDED_PRIMITIVES = {
    # Translation Direction - Remove "only" variants, keep "has" variants
    "only_forward_wrt_ground",
    "only_backward_wrt_ground",
    "only_upward_wrt_ground",
    "only_downward_wrt_ground",
    "only_forward_wrt_camera",
    "only_backward_wrt_camera",
    "only_upward_wrt_camera",
    "only_downward_wrt_camera",
    "only_leftward",
    "only_rightward",
    "only_forward_wrt_ground_birds_worms_included",
    "only_backward_wrt_ground_birds_worms_included",
    "only_upward_wrt_ground_birds_worms_included",
    "only_downward_wrt_ground_birds_worms_included",
    
    # Rotation Direction - Remove "only" variants, keep "has" variants
    "only_pan_left",
    "only_pan_right",
    "only_tilt_up",
    "only_tilt_down",
    "only_roll_clockwise",
    "only_roll_counterclockwise",

    # Only zooming
    "only_zoom_in",
    "only_zoom_out",

    # With lens distortion
    "with_lens_distortion",

    # Video speed
    "fast_motion",

    # Shot transitions
    "has_shot_transition_cam_motion",
    
    # Additional exclusions
    "has_forward_wrt_camera",
    "has_backward_wrt_camera",
    "has_upward_wrt_camera",
    "has_downward_wrt_camera",
    "has_forward_wrt_ground",
    "has_backward_wrt_ground",
    "has_upward_wrt_ground",
    "has_downward_wrt_ground",
}

# PRIMITIVE RENAMING CONFIGURATION
# Map from original primitive name to new display name
# This only affects the display in tables, not the actual primitive name in code
PRIMITIVE_DISPLAY_NAME_OVERRIDES = {
    # Rename birds/worms included variants
    "has_forward_wrt_ground_birds_worms_included": "Forward",
    "has_backward_wrt_ground_birds_worms_included": "Backward",
    "has_upward_wrt_ground_birds_worms_included": "Upward",
    "has_downward_wrt_ground_birds_worms_included": "Downward",
    "tail_tracking_shot": "Follow Tracking Shot",
    "height_wrt_ground_end_with_aerial_level": "Height Ends With Aerial Level",
    "height_wrt_ground_end_with_eye_level": "Height Ends With Eye Level",
    "height_wrt_ground_end_with_hip_level": "Height Ends With Hip Level",
    "height_wrt_ground_end_with_overhead_level": "Height Ends With Overhead Level",
    "height_wrt_ground_end_with_water_level": "Height Ends With Water Level",
    "height_wrt_ground_end_with_underwater_level": "Height Ends With Underwater Level",
    "height_wrt_ground_end_with_ground_level": "Height Ends With Ground Level",
    "height_wrt_ground_start_with_aerial_level": "Height Starts With Aerial Level",
    "height_wrt_ground_start_with_eye_level": "Height Starts With Eye Level",
    "height_wrt_ground_start_with_hip_level": "Height Starts With Hip Level",
    "height_wrt_ground_start_with_overhead_level": "Height Starts With Overhead Level",
    "height_wrt_ground_start_with_water_level": "Height Starts With Water Level",
    "height_wrt_ground_start_with_underwater_level": "Height Starts With Underwater Level",
    "height_wrt_ground_start_with_ground_level": "Height Starts With Ground Level",
    "height_wrt_ground_change_from_low_to_high": "Height Changes From Low To High",
    "height_wrt_ground_change_from_high_to_low": "Height Changes From High To Low",
    "height_wrt_ground_change_from_water_to_underwater": "Height Changes From Above Water To Underwater",
    "height_wrt_ground_change_from_underwater_to_water": "Height Changes From Underwater To Above Water",
    "height_wrt_subject_start_with_at_subject": "Height Starts With At Subject",
    "height_wrt_subject_start_with_above_subject": "Height Starts With Above Subject",
    "height_wrt_subject_start_with_below_subject": "Height Starts With Below Subject",
    "height_wrt_subject_end_with_at_subject": "Height Ends With At Subject",
    "height_wrt_subject_end_with_above_subject": "Height Ends With Above Subject",
    "height_wrt_subject_end_with_below_subject": "Height Ends With Below Subject",
    "height_wrt_subject_from_above_subject_to_at_subject": "Height From Above Subject To At Subject",
    "height_wrt_subject_from_above_subject_to_below_subject": "Height From Above Subject To Below Subject",
    "height_wrt_subject_from_at_subject_to_above_subject": "Height From At Subject To Above Subject",
    "height_wrt_subject_from_at_subject_to_below_subject": "Height From At Subject To Below Subject",
    "height_wrt_subject_from_below_subject_to_above_subject": "Height From Below Subject To Above Subject",
    "height_wrt_subject_from_below_subject_to_at_subject": "Height From Below Subject To At Subject",
    "height_wrt_subject_is_above_subject": "Height Is Always Above Subject",
    "height_wrt_subject_is_at_subject": "Height Is Always At Subject",
    "height_wrt_subject_is_below_subject": "Height Is Always Below Subject",
    "camera_angle_change": "Camera Angle Changes",
    "camera_angle_end_with_bird_eye_angle": "Camera Ends With Bird's Eye Angle",
    "camera_angle_end_with_high_angle": "Camera Ends With High Angle",
    "camera_angle_end_with_level_angle": "Camera Ends With Level Angle",
    "camera_angle_end_with_low_angle": "Camera Ends With Low Angle",
    "camera_angle_end_with_worm_eye_angle": "Camera Ends With Worm's Eye Angle",
    "camera_angle_start_with_bird_eye_angle": "Camera Starts With Bird's Eye Angle",
    "camera_angle_start_with_high_angle": "Camera Starts With High Angle",
    "camera_angle_start_with_level_angle": "Camera Starts With Level Angle",
    "camera_angle_start_with_low_angle": "Camera Starts With Low Angle",
    "camera_angle_start_with_worm_eye_angle": "Camera Starts With Worm's Eye Angle",
    "camera_angle_change_from_high_to_low": "Camera Angle Lowers",
    "camera_angle_change_from_low_to_high": "Camera Angle Raises",
    "focus_start_with_background": "Focus Starts With Background",
    "focus_start_with_foreground": "Focus Starts With Foreground",
    "focus_start_with_middle_ground": "Focus Starts With Middle Ground",
    "focus_start_with_out_of_focus": "Focus Starts With Out of Focus",
    "focus_end_with_background": "Focus Ends With Background",
    "focus_end_with_foreground": "Focus Ends With Foreground",
    "focus_end_with_middle_ground": "Focus Ends With Middle Ground",
    "focus_end_with_out_of_focus": "Focus Ends With Out of Focus",
    "focus_change_from_far_to_near": "Focus Changes From Near To Far",
    "focus_change_from_near_to_far": "Focus Changes From Far To Near",
    "focus_change_from_in_to_out_of_focus": "Focus Changes From In To Out of Focus",
    "focus_change_from_out_to_in_focus": "Focus Changes From Out of Focus To In",
    "focus_change": "Focus Changes",
    "fast_motion_without_time_lapse": "Fast Motion",
    "has_shot_transition_cam_setup": "Has Shot Transition",
    "is_just_scenery_shot": "Scenery Shot",
    "is_just_human_shot": "Human Shot",
    "is_just_non_human_shot": "Non-Human Shot",
    "is_just_change_of_subject_shot": "Change of Subject Shot",
    "is_just_back_and_forth_change_shot": "Back and Forth Change in Shot Size",
    "is_just_clear_subject_dynamic_size_shot": "Clear Subject with Dynamic Shot Size",
    "is_just_different_subject_in_focus_shot": "Different Subjects in Focus",
    "is_just_clear_subject_atypical_shot": "Clear Subject with Atypical Shot Size",
    "is_just_many_subject_one_focus_shot": "Many Subject with One Clear Focus",
    "is_just_many_subject_no_focus_shot": "Many Subject with No Clear Focus",
    "is_just_subject_scene_mismatch_shot": "Subject and Scene Mismatch in Shot Size",
    "shot_size_end_with_wide": "Shot Size Ends With Wide",
    "shot_size_end_with_full": "Shot Size Ends With Full",
    "shot_size_end_with_medium_full": "Shot Size Ends With Medium Full (Human)",
    "shot_size_end_with_medium": "Shot Size Ends With Medium",
    "shot_size_end_with_medium_close_up": "Shot Size Ends With Medium Close Up (Human)",
    "shot_size_end_with_close_up": "Shot Size Ends With Close Up",
    "shot_size_end_with_extreme_close_up": "Shot Size Ends With Extreme Close Up",
    "shot_size_end_with_extreme_wide": "Shot Size Ends With Extreme Wide",
    "shot_size_start_with_wide": "Shot Size Starts With Wide",
    "shot_size_start_with_full": "Shot Size Starts With Full",
    "shot_size_start_with_medium_full": "Shot Size Starts With Medium Full (Human)",
    "shot_size_start_with_medium": "Shot Size Starts With Medium",
    "shot_size_start_with_medium_close_up": "Shot Size Starts With Medium Close Up (Human)",
    "shot_size_start_with_close_up": "Shot Size Starts With Close Up",
    "shot_size_start_with_extreme_close_up": "Shot Size Starts With Extreme Close Up",
    "shot_size_start_with_extreme_wide": "Shot Size Starts With Extreme Wide",
    "shot_size_change": "Shot Size Changes",
    "has_subject_change": "Subject Transitions",
    "shot_size_change_from_large_to_small": "Shot Size Changes From Large to Small",
    "shot_size_change_from_small_to_large": "Shot Size Changes From Small to Large",
    "height_wrt_subject_change": "Height Wrt Subject Changes",
    "height_wrt_subject_change_from_low_to_high": "Height Wrt Subject Changes From Low To High",
    "height_wrt_subject_change_from_high_to_low": "Height Wrt Subject Changes From High To Low",
}

# ASPECT DESCRIPTIONS
# Full-sentence descriptions for each aspect
ASPECT_DESCRIPTIONS = {
    # Camera Motion aspects
    "steadiness_and_movement": "Evaluates camera stability and motion speed, including shake detection, and the distinction between fixed and moving cameras.",
    "motion_effects": "Identifies visual effects related to camera motion, including motion blur and frame freezing effects.",
    "motion_complexity": "Classifies the complexity of camera motion, distinguishing between simple, complex, and minor movements.",
    "translation_direction": "Classifies translational camera motion directions including forward/backward, upward/downward, and leftward/rightward movements.",
    "rotation_direction": "Classifies rotational camera motion including pan left/right, tilt up/down, and roll clockwise/counterclockwise.",
    "intrinsic_direction": "Classifies intrinsic camera changes including zoom in/out.",
    "arc_crane_movement": "Identifies arc and crane camera movements, including clockwise/counterclockwise arcs and upward/downward crane shots.",
    "dolly_zoom": "Detects dolly zoom effects where the camera physically moves while zooming in the opposite direction to create a distinctive visual effect.",
    "tracking_shots": "Identifies various types of tracking shots where the camera follows moving subjects, including aerial, arc, side, lead, follow, pan, and tilt tracking.",
    
    # Camera Setup aspects
    "height_wrt_ground": "Classifies camera height relative to the ground, including ground level, hip level, eye level, overhead, aerial, water level, and underwater positions.",
    "height_wrt_subject": "Classifies camera height relative to the subject, determining whether the camera is positioned above, at, or below the subject's height.",
    "camera_angle": "Classifies camera angle relative to the ground, including bird's eye, high angle, level angle, low angle, and worm's eye perspectives.",
    "dutch_angle": "Detects the presence and characteristics of Dutch (canted) angles in the video, including whether the angle remains fixed or varies.",
    "depth_of_field": "Analyzes depth of field characteristics including deep focus, shallow focus, ultra-shallow focus, rack focus, and focus tracking.",
    "lens_distortion": "Detects lens distortion effects including barrel distortion and fisheye distortion.",
    
    # Shot Composition aspects
    "shot_transition": "Detects the presence of shot transitions within the video.",
    "overlays": "Detects on-screen overlays such as watermarks, titles, subtitles, icons, HUDs, or framing elements.",
    "point_of_view": "Classifies the camera's point of view including objective, first-person, selfie, overhead, locked-on, dashcam, drone, broadcast, screen recording, and various third-person game perspectives.",
    "playback_speed": "Classifies video playback speed including regular speed, slow motion, fast motion, time-lapse, stop motion, time reversal, and speed ramp effects.",
    "subject_framing": "Analyzes subject presence, changes, and framing characteristics in the video.",
    "shot_type": "Classifies the type of shot based on subject characteristics, including human shots, non-human shots, scenery shots, and various multi-subject configurations.",
    "shot_size_change": "Detects changes in shot size throughout the video, including transitions from wider to tighter framing or vice versa.",
    "shot_size": "Classifies the shot size throughout the video, ranging from extreme close-up to extreme wide shot, including static sizes and start/end positions.",
}

PRIMITIVE_HIERARCHY = {
    "camera_motion": {
        "display_name": "Camera Motion",
        "description": "Primitives related to camera movements",
        "aspects": {
            "steadiness_and_movement": {
                "display_name": "Motion & Steadiness",
                "primitives": [
                    "clear_moving_camera", "fixed_camera", "fixed_camera_with_shake",
                    "moving_camera", "stable_camera_motion", "very_stable_camera_motion",
                    "shaky_camera", "very_shaky_camera", "slow_moving_camera",
                    "fast_moving_camera"
                ]
            },
            "scene_movement": {
                "display_name": "Scene Dynamics",
                "primitives": [
                    "static_scene", "dynamic_scene", "mostly_static_scene"
                ]
            },
            "motion_effects": {
                "display_name": "Motion Effects",
                "primitives": [
                    "has_motion_blur", "has_frame_freezing"
                ]
            },
            "motion_complexity": {
                "display_name": "Motion Complexity",
                "primitives": [
                    "is_simple_motion", "is_complex_motion", "is_minor_motion"
                ]
            },
            "translation_direction": {
                "display_name": "Translation Direction",
                "primitives": [
                    "has_forward_wrt_ground", "has_backward_wrt_ground",
                    "has_upward_wrt_ground", "has_downward_wrt_ground",
                    "has_forward_wrt_camera", "has_backward_wrt_camera",
                    "has_upward_wrt_camera", "has_downward_wrt_camera",
                    "only_forward_wrt_ground", "only_backward_wrt_ground",
                    "only_upward_wrt_ground", "only_downward_wrt_ground",
                    "only_forward_wrt_camera", "only_backward_wrt_camera",
                    "only_upward_wrt_camera", "only_downward_wrt_camera",
                    "only_leftward", "only_rightward",
                    "has_forward_wrt_ground_birds_worms_included",
                    "has_backward_wrt_ground_birds_worms_included",
                    "has_upward_wrt_ground_birds_worms_included",
                    "has_downward_wrt_ground_birds_worms_included",
                    "has_leftward", "has_rightward",
                    "only_forward_wrt_ground_birds_worms_included",
                    "only_backward_wrt_ground_birds_worms_included",
                    "only_upward_wrt_ground_birds_worms_included",
                    "only_downward_wrt_ground_birds_worms_included"
                ]
            },
            "rotation_direction": {
                "display_name": "Rotation Direction",
                "primitives": [
                    "has_pan_left", "has_pan_right", "has_tilt_up", "has_tilt_down",
                    "has_roll_clockwise", "has_roll_counterclockwise",
                    "only_pan_left", "only_pan_right", "only_tilt_up", "only_tilt_down",
                    "only_roll_clockwise", "only_roll_counterclockwise"
                ]
            },
            "intrinsic_direction": {
                "display_name": "Intrinsic Direction",
                "primitives": [
                    "has_zoom_in", "has_zoom_out", "only_zoom_in", "only_zoom_out"
                ]
            },
            "arc_crane_movement": {
                "display_name": "Arc & Crane Movement",
                "primitives": [
                    "has_arc_clockwise", "has_arc_counterclockwise",
                    "has_crane_up", "has_crane_down"
                ]
            },
            "dolly_zoom": {
                "display_name": "Dolly Zoom",
                "primitives": [
                    "has_dolly_out_zoom_in", "has_dolly_in_zoom_out"
                ]
            },
            "tracking_shots": {
                "display_name": "Tracking Shots",
                "primitives": [
                    "tracking_shot", "aerial_tracking_shot", "arc_tracking_shot",
                    "front_side_tracking_shot", "rear_side_tracking_shot",
                    "lead_tracking_shot", "tail_tracking_shot",
                    "tilt_tracking_shot", "pan_tracking_shot", "side_tracking_shot",
                    "side_tracking_shot_leftward", "side_tracking_shot_rightward",
                    "tracking_subject_larger_size", "tracking_subject_smaller_size"
                ]
            }
        }
    },
    "camera_setup": {
        "display_name": "Camera Setup",
        "description": "Primitives related to camera configuration and positioning",
        "aspects": {
            "lens_distortion": {
                "display_name": "Lens Distortion",
                "primitives": [
                    "barrel_distortion", "fisheye_distortion",
                    "with_lens_distortion", "no_lens_distortion"
                ]
            },
            "height_wrt_ground": {
                "display_name": "Height Relative to Ground",
                "primitives": [
                    # Static height (is/start/end)
                    "height_wrt_ground_is_ground_level",
                    "height_wrt_ground_is_hip_level",
                    "height_wrt_ground_is_eye_level",
                    "height_wrt_ground_is_overhead_level",
                    "height_wrt_ground_is_aerial_level",
                    "height_wrt_ground_is_water_level",
                    "height_wrt_ground_is_underwater_level",
                    "height_wrt_ground_start_with_ground_level",
                    "height_wrt_ground_start_with_hip_level",
                    "height_wrt_ground_start_with_eye_level",
                    "height_wrt_ground_start_with_overhead_level",
                    "height_wrt_ground_start_with_aerial_level",
                    "height_wrt_ground_start_with_water_level",
                    "height_wrt_ground_start_with_underwater_level",
                    "height_wrt_ground_end_with_ground_level",
                    "height_wrt_ground_end_with_hip_level",
                    "height_wrt_ground_end_with_eye_level",
                    "height_wrt_ground_end_with_overhead_level",
                    "height_wrt_ground_end_with_aerial_level",
                    "height_wrt_ground_end_with_water_level",
                    "height_wrt_ground_end_with_underwater_level",
                    "is_height_wrt_ground_applicable"
                ]
            },
            "height_wrt_ground_changing": {
                "display_name": "Height Relative to Ground (Changing)",
                "primitives": [
                    # Height transitions
                    "height_wrt_ground_change_from_low_to_high",
                    "height_wrt_ground_change_from_high_to_low",
                    "above_water_to_underwater",
                    "underwater_to_above_water",
                ]
            },
            "height_wrt_subject": {
                "display_name": "Height Relative to Subject",
                "primitives": [
                    # Static height (is/start/end)
                    "height_wrt_subject_is_above_subject",
                    "height_wrt_subject_is_at_subject",
                    "height_wrt_subject_is_below_subject",
                    "height_wrt_subject_start_with_above_subject",
                    "height_wrt_subject_start_with_at_subject",
                    "height_wrt_subject_start_with_below_subject",
                    "height_wrt_subject_end_with_above_subject",
                    "height_wrt_subject_end_with_at_subject",
                    "height_wrt_subject_end_with_below_subject",
                    "is_subject_height_applicable"
                ]
            },
            "height_wrt_subject_changing": {
                "display_name": "Height Relative to Subject (Changing)",
                "primitives": [
                    # Height changes
                    "height_wrt_subject_change",
                    "height_wrt_subject_change_from_low_to_high",
                    "height_wrt_subject_change_from_high_to_low",
                    "height_wrt_subject_from_above_subject_to_at_subject",
                    "height_wrt_subject_from_above_subject_to_below_subject",
                    "height_wrt_subject_from_at_subject_to_above_subject",
                    "height_wrt_subject_from_at_subject_to_below_subject",
                    "height_wrt_subject_from_below_subject_to_at_subject",
                    "height_wrt_subject_from_below_subject_to_above_subject",
                ]
            },
            "camera_angle": {
                "display_name": "Camera Angle",
                "primitives": [
                    # Static angle (is/start/end)
                    "camera_angle_is_bird_eye_angle",
                    "camera_angle_is_high_angle",
                    "camera_angle_is_level_angle",
                    "camera_angle_is_low_angle",
                    "camera_angle_is_worm_eye_angle",
                    "camera_angle_start_with_bird_eye_angle",
                    "camera_angle_start_with_high_angle",
                    "camera_angle_start_with_level_angle",
                    "camera_angle_start_with_low_angle",
                    "camera_angle_start_with_worm_eye_angle",
                    "camera_angle_end_with_bird_eye_angle",
                    "camera_angle_end_with_high_angle",
                    "camera_angle_end_with_level_angle",
                    "camera_angle_end_with_low_angle",
                    "camera_angle_end_with_worm_eye_angle",
                    "is_camera_angle_applicable"
                ]
            },
            "camera_angle_changing": {
                "display_name": "Camera Angle (Changing)",
                "primitives": [
                    # Angle changes
                    "camera_angle_change",
                    "camera_angle_change_from_low_to_high",
                    "camera_angle_change_from_high_to_low",
                    "camera_angle_from_high_to_level",
                    "camera_angle_from_high_to_low",
                    "camera_angle_from_level_to_high",
                    "camera_angle_from_level_to_low",
                    "camera_angle_from_low_to_level",
                    "camera_angle_from_low_to_high",
                ]
            },
            "dutch_angle": {
                "display_name": "Dutch Angle",
                "primitives": [
                    "is_dutch_angle", "is_dutch_angle_fixed", "is_dutch_angle_varying"
                ]
            },
            "depth_of_field": {
                "display_name": "Depth of Field",
                "primitives": [
                    # Depth of field characteristics
                    "is_deep_focus", "is_shallow_focus", "is_ultra_shallow_focus",
                    "is_rack_pull_focus", "is_focus_tracking",
                    "is_focus_applicable"
                ]
            },
            "focal_plane": {
                "display_name": "Focal Plane",
                "primitives": [
                    # Static focus (is/start/end)
                    "focus_is_foreground", "focus_is_middle_ground", "focus_is_background",
                    "focus_is_out_of_focus",
                    "focus_start_with_foreground", "focus_start_with_middle_ground",
                    "focus_start_with_background", "focus_start_with_out_of_focus",
                    "focus_end_with_foreground", "focus_end_with_middle_ground",
                    "focus_end_with_background", "focus_end_with_out_of_focus",
                ]
            },
            "focal_plane_changing": {
                "display_name": "Focal Plane (Changing)",
                "primitives": [
                    # Focus changes
                    "focus_change", 
                    "focus_change_from_near_to_far",
                    "focus_change_from_far_to_near",
                    "focus_change_from_in_to_out_of_focus",
                    "focus_change_from_out_to_in_focus",
                    "focus_from_foreground_to_middle_ground",
                    "focus_from_foreground_to_background",
                    "focus_from_middle_ground_to_foreground",
                    "focus_from_middle_ground_to_background",
                    "focus_from_background_to_foreground",
                    "focus_from_background_to_middle_ground",
                ]
            }
        }
    },
    "shot_composition": {
        "display_name": "Shot Composition",
        "description": "Primitives related to shot framing, transitions, and visual composition",
        "aspects": {
            "shot_transition": {
                "display_name": "Shot Transition",
                "primitives": [
                    "has_shot_transition_cam_motion", "has_shot_transition_cam_setup"
                ]
            },
            "overlays": {
                "display_name": "Overlays",
                "primitives": [
                    "has_overlays"
                ]
            },
            "point_of_view": {
                "display_name": "Point of View",
                "primitives": [
                    "objective_pov", "first_person_pov", "selfie_pov",
                    "overhead_pov", "locked_on_pov", "dashcam_pov", "drone_pov",
                    "broadcast_pov", "screen_recording_pov",
                    "third_person_over_shoulder_pov", "third_person_over_hip_pov",
                    "third_person_full_body_game_pov", 
                    "third_person_top_down_game_pov", "third_person_side_view_game_pov",
                    "third_person_isometric_game_pov"
                ]
            },
            "playback_speed": {
                "display_name": "Playback Speed",
                "primitives": [
                    "regular_speed", "slow_motion", "fast_motion",
                    "fast_motion_without_time_lapse", "time_lapse",
                    "stop_motion", "time_reversed", "speed_ramp"
                ]
            },
            "subject_framing": {
                "display_name": "Subject Framing",
                "primitives": [
                    "is_framing_subject", "has_single_dominant_subject",
                    "has_many_subjects", "has_subject_change",
                    "subject_revealing", "subject_disappearing", "subject_switching"
                ]
            },
            "shot_type": {
                "display_name": "Shot Type",
                "primitives": [
                    "is_just_scenery_shot",
                    "is_just_human_shot", "is_just_non_human_shot",
                    "is_just_change_of_subject_shot",
                    "is_just_many_subject_one_focus_shot",
                    "is_just_many_subject_no_focus_shot",
                    "is_just_different_subject_in_focus_shot",
                    "is_just_clear_subject_dynamic_size_shot",
                    "is_just_clear_subject_atypical_shot",
                    "is_just_subject_scene_mismatch_shot",
                    "is_just_back_and_forth_change_shot"
                ]
            },
            "shot_size": {
                "display_name": "Shot Size",
                "primitives": [
                    # Static shot sizes (is/start/end)
                    "shot_size_is_extreme_close_up",
                    "shot_size_is_close_up",
                    "shot_size_is_medium_close_up",
                    "shot_size_is_medium",
                    "shot_size_is_medium_full",
                    "shot_size_is_full",
                    "shot_size_is_wide",
                    "shot_size_is_extreme_wide",
                    "shot_size_start_with_extreme_close_up",
                    "shot_size_start_with_close_up",
                    "shot_size_start_with_medium_close_up",
                    "shot_size_start_with_medium",
                    "shot_size_start_with_medium_full",
                    "shot_size_start_with_full",
                    "shot_size_start_with_wide",
                    "shot_size_start_with_extreme_wide",
                    "shot_size_end_with_extreme_close_up",
                    "shot_size_end_with_close_up",
                    "shot_size_end_with_medium_close_up",
                    "shot_size_end_with_medium",
                    "shot_size_end_with_medium_full",
                    "shot_size_end_with_full",
                    "shot_size_end_with_wide",
                    "shot_size_end_with_extreme_wide",
                    "is_shot_size_applicable"
                ]
            },
            "shot_size_changing": {
                "display_name": "Shot Size (Changing)",
                "primitives": [
                    # Shot size changes
                    "shot_size_change",
                    "shot_size_change_from_small_to_large",
                    "shot_size_change_from_large_to_small",
                ]
            }
        }
    }
}

# ============================================================================
# SKILL NAME MAPPINGS (Edit these as needed)
# ============================================================================
SKILL_DISPLAY_NAMES = {
    # Motion skills
    "movement_and_steadiness": "Motion & Steadiness",
    "camera_movement_speed": "Motion Speed",
    "translation_direction": "Translation Direction",
    "rotation_direction": "Rotation Direction",
    "object_centric_direction": "Object-Centric Direction",
    "intrinsic_direction": "Intrinsic Direction",
    "instrinsic_vs_extrinsic": "Intrinsic vs. Extrinsic",
    "rotation_vs_translation": "Rotation vs. Translation",
    "has_intrinsic_change": "Has Intrinsic Change",
    "has_translation": "Has Translation",
    "has_rotation": "Has Rotation",
    "has_arc_crane": "Has Arc/Crane",
    "special_tracking": "Special Tracking",
    "general_tracking": "General Tracking",
    "only_intrinsic_change": "Only Intrinsic Change",
    "only_translation": "Only Translation",
    "only_rotation": "Only Rotation",
    "reference_frame": "Reference Frame",
    
    # Setup skills
    "shot_transition": "Shot Transition",
    "overlays": "Overlays",
    "lens_distortion": "Lens Distortion",
    "playback_speed": "Playback Speed",
    "point_of_view": "Point of View",
    "subject_framing": "Subject Framing",
    "shot_type": "Shot Type",
    "shot_size_change": "Shot Size Change",
    "shot_size": "Shot Size",
    "height_wrt_subject_change": "Height Relative to Subject Change",
    "height_wrt_subject": "Height Relative to Subject",
    "height_wrt_ground_change": "Height Relative to Ground Change",
    "height_wrt_ground": "Height Relative to Ground",
    "camera_angle_change": "Camera Angle Change",
    "camera_angle": "Camera Angle",
    "dutch_angle": "Dutch Angle",
    "depth_of_field": "Depth of Field",
    "focal_plane": "Focal Plane",
    "focal_plane_changing": "Focal Plane (Changing)",
}

SKILL_DESCRIPTIONS = {
    # Motion skills
    "movement_and_steadiness": "Evaluates how steady the camera is and whether it moves in a controlled manner, including shake detection and fixed vs. moving camera states.",
    "camera_movement_speed": "Evaluates the speed of camera movements, distinguishing between slow-moving and fast-moving shots, and detects motion blur and frame freeze.",
    "translation_direction": "Classifies translational camera motion directions including forward/backward, upward/downward, and leftward/rightward movements.",
    "rotation_direction": "Classifies rotational camera motion including pan left/right, tilt up/down, and roll clockwise/counterclockwise.",
    "object_centric_direction": "Identifies object-centric camera movements including side tracking, lead/tail tracking, arc movements, and crane shots.",
    "intrinsic_direction": "Detects intrinsic camera changes including zoom in/out and dolly zoom effects.",
    "instrinsic_vs_extrinsic": "Distinguishes between intrinsic changes (zoom) and physical camera movement (dolly in/out).",
    "rotation_vs_translation": "Distinguishes between rotational movements (pan/tilt) and translational movements (truck/pedestal).",
    "has_intrinsic_change": "Determines whether the camera exhibits intrinsic changes such as zooming in or out.",
    "has_translation": "Determines whether the camera exhibits translational movement in various directions.",
    "has_rotation": "Determines whether the camera exhibits rotational movement including pan, tilt, and roll.",
    "has_arc_crane": "Determines whether the camera exhibits arc or crane movements.",
    "special_tracking": "Identifies specific types of tracking shots including aerial, arc, front-side, rear-side, lead, tail, tilt, pan, and side tracking.",
    "general_tracking": "Determines whether the camera is tracking a subject and whether the subject appears larger or smaller during tracking.",
    "only_intrinsic_change": "Identifies cases where the camera performs only intrinsic changes (zoom) without any other movement.",
    "only_translation": "Identifies cases where the camera performs only translational movement without any other camera motion.",
    "only_rotation": "Identifies cases where the camera performs only rotational movement without any other camera motion.",
    "reference_frame": "Determines the reference frame of camera motion, distinguishing between camera-centric and ground-centric perspectives.",
    
    # Camera Setup aspects
    "lens_distortion": "Detects lens distortion effects including barrel distortion and fisheye distortion.",
    "height_wrt_ground": "Classifies camera height relative to the ground, including ground level, hip level, eye level, overhead, aerial, water level, and underwater positions.",
    "height_wrt_ground_changing": "Detects transitions in camera height relative to the ground, including movements between different height levels and water surface transitions.",
    "height_wrt_subject": "Classifies camera height relative to the subject, determining whether the camera is positioned above, at, or below the subject's height.",
    "height_wrt_subject_changing": "Detects transitions in camera height relative to the subject, including movements from above to below or vice versa.",
    "camera_angle": "Classifies camera angle relative to the ground, including bird's eye, high angle, level angle, low angle, and worm's eye perspectives.",
    "camera_angle_changing": "Detects transitions in camera angle relative to the ground, including shifts between different angular perspectives.",
    "dutch_angle": "Detects the presence and characteristics of Dutch (canted) angles in the video, including whether the angle remains fixed or varies.",
    "depth_of_field": "Analyzes depth of field characteristics including deep focus, shallow focus, ultra-shallow focus, rack focus, and focus tracking.",
    "focal_plane": "Classifies the focal plane position in the video, including focus on foreground, middleground, background, or out-of-focus states.",
    "focal_plane_changing": "Detects transitions in focal plane position, including rack focus effects moving between different depth planes.",
    
    # Shot Composition aspects
    "shot_transition": "Detects the presence of shot transitions within the video.",
    "overlays": "Detects on-screen overlays such as watermarks, titles, subtitles, icons, HUDs, or framing elements.",
    "point_of_view": "Classifies the camera's point of view including objective, first-person, selfie, overhead, locked-on, dashcam, drone, broadcast, screen recording, and various third-person game perspectives.",
    "playback_speed": "Classifies video playback speed including regular speed, slow motion, fast motion, time-lapse, stop motion, time reversal, and speed ramp effects.",
    "subject_framing": "Analyzes subject presence, changes, and framing characteristics in the video.",
    "shot_type": "Classifies the type of shot based on subject characteristics, including human shots, non-human shots, scenery shots, and various multi-subject configurations.",
    "shot_size": "Classifies the shot size, ranging from extreme close-up to extreme wide shot.",
    "shot_size_changing": "Detects changes in shot size, including transitions from wider to tighter framing or vice versa.",
}

# ============================================================================
# LATEX TABLE GENERATION
# ============================================================================

def escape_latex(text):
    """Escape special LaTeX characters in text"""
    # Order matters! Backslash must be first
    text = text.replace('\\', r'\textbackslash{}')
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('{', r'\{')
    text = text.replace('}', r'\}')
    text = text.replace('~', r'\textasciitilde{}')
    text = text.replace('^', r'\textasciicircum{}')
    return text

def clean_task_name(name):
    """Convert task name to display format"""
    # Remove common prefixes/suffixes
    name = re.sub(r'^(is_|has_|only_)', '', name)
    name = re.sub(r'(_vs_|_or_)', ' vs. ', name)
    # Convert underscores to spaces and title case
    name = name.replace('_', ' ').title()
    return name

def count_hierarchy_stats():
    """Count top-level categories, aspects, and primitives"""
    stats = {
        'top_level': 0,
        'aspects': 0,
        'primitives': 0,
        'per_top_level': {}
    }
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        stats['top_level'] += 1
        aspect_count = 0
        primitive_count = 0
        
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            # Skip excluded aspects
            if aspect_key in EXCLUDED_ASPECTS:
                continue
            
            # Filter out excluded primitives
            primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
            
            # Skip aspect if no primitives remain
            if not primitive_list:
                continue
            
            aspect_count += 1
            primitive_count += len(primitive_list)
        
        stats['aspects'] += aspect_count
        stats['primitives'] += primitive_count
        stats['per_top_level'][top_level_key] = {
            'display_name': top_level_config['display_name'],
            'aspects': aspect_count,
            'primitives': primitive_count
        }
    
    return stats

def generate_overview_table(skills_data, folder_name="camerabench_pro"):
    """Generate the overview table listing all skills"""
    lines = []
    lines.append(r"\begin{table*}[h!]")
    lines.append(r"\centering")
    lines.append(r"\caption{\small \textbf{All tasks for each top-level skill in CameraBench Pro.} We list all tasks across all skills in CameraBench Pro.}")
    lines.append(r"\scalebox{0.7}{")
    lines.append(r"\begin{NiceTabular}{l M{0.3\linewidth} M{0.6\linewidth}}")
    lines.append(r"\CodeBefore")
    lines.append(r"    \Body")
    lines.append(r"\toprule[1.2pt]")
    lines.append(r"\textbf{Skill} & \textbf{Description} & \textbf{Tasks} \\")
    lines.append(r"\midrule")
    
    first_skill = True
    for skill_name, tasks in skills_data.items():
        if not first_skill:
            lines.append(r"\midrule")
        first_skill = False
        
        display_name = SKILL_DISPLAY_NAMES.get(skill_name, skill_name.replace('_', ' ').title())
        description = SKILL_DESCRIPTIONS.get(skill_name, "")
        
        # Count tasks
        num_tasks = len(tasks)
        
        # Create task list
        task_names = []
        for task in tasks:
            # Extract a readable task name from the question or name
            task_display = clean_task_name(task['name'])
            task_names.append(task_display)
        
        task_list = ", ".join(task_names)
        
        # Generate label reference
        label_ref = f"tab:{skill_name}"
        
        # Escape each component separately and format properly
        display_name_escaped = escape_latex(display_name)
        description_escaped = escape_latex(description)
        task_list_escaped = escape_latex(task_list)
        
        lines.append(f"\\textbf{{{display_name_escaped}}} ")
        lines.append(f"& {description_escaped} ")
        lines.append(f"& {task_list_escaped}. ({num_tasks} Tasks in \\autoref{{{label_ref}}}) \\\\")
    
    lines.append(r"\bottomrule[1.2pt]")
    lines.append(r"\end{NiceTabular}")
    lines.append(r"}")
    lines.append(r"\label{tab:overview_camera_bench_pro}")
    lines.append(r"\end{table*}")
    
    return "\n".join(lines)

def generate_primitive_overview_tables(primitives_data):
    """Generate three overview tables for Camera Motion, Camera Setup, and Shot Composition primitives"""
    tables = {}
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        lines = []
        lines.append(r"\begin{table*}[h!]")
        lines.append(r"\centering")
        
        display_name = top_level_config["display_name"]

        # Count total primitives for this top-level category
        total_primitives = 0
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            if aspect_key not in EXCLUDED_ASPECTS:
                primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
                total_primitives += len(primitive_list)

        # Escape display name for use in caption
        display_name_escaped = escape_latex(display_name)
        lines.append(f"\\caption{{\\small \\textbf{{{display_name_escaped} Primitives Overview.}} All primitive aspects in {display_name_escaped} ({total_primitives} primitives in total).}}")
        lines.append(r"\scalebox{0.7}{")
        lines.append(r"\begin{NiceTabular}{l M{0.3\linewidth} M{0.6\linewidth}}")
        lines.append(r"\CodeBefore")
        lines.append(r"    \Body")
        lines.append(r"\toprule[1.2pt]")
        lines.append(r"\textbf{Aspect} & \textbf{Description} & \textbf{Primitives} \\")
        lines.append(r"\midrule")
        
        first_aspect = True
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            # Skip excluded aspects
            if aspect_key in EXCLUDED_ASPECTS:
                continue
                
            # Filter out excluded primitives
            primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
            
            # Skip aspect if no primitives remain after filtering
            if not primitive_list:
                continue
                
            if not first_aspect:
                lines.append(r"\midrule")
            first_aspect = False
            
            aspect_display = aspect_config["display_name"]
            
            # Get descriptions and count
            num_primitives = len(primitive_list)
            
            # Get description from ASPECT_DESCRIPTIONS (preferred) or fall back to SKILL_DESCRIPTIONS or display name
            description = ASPECT_DESCRIPTIONS.get(aspect_key, SKILL_DESCRIPTIONS.get(aspect_key, aspect_display))
            
            # Create primitive list (cleaned names, with custom overrides)
            primitive_names = []
            for p in primitive_list:
                if p in PRIMITIVE_DISPLAY_NAME_OVERRIDES:
                    primitive_names.append(PRIMITIVE_DISPLAY_NAME_OVERRIDES[p])
                else:
                    primitive_names.append(clean_task_name(p))
            primitives_str = ", ".join(primitive_names)
            
            # Generate label reference
            label_ref = f"tab:primitives_{aspect_key}"
            
            # Escape each component separately
            aspect_display_escaped = escape_latex(aspect_display)
            description_escaped = escape_latex(description)
            primitives_escaped = escape_latex(primitives_str)
            
            lines.append(f"\\textbf{{{aspect_display_escaped}}} ")
            lines.append(f"& {description_escaped} ")
            lines.append(f"& {primitives_escaped}. ({num_primitives} Primitives in \\autoref{{{label_ref}}}) \\\\")
        
        lines.append(r"\bottomrule[1.2pt]")
        lines.append(r"\end{NiceTabular}")
        lines.append(r"}")
        lines.append(f"\\label{{tab:primitives_overview_{top_level_key}}}")
        lines.append(r"\end{table*}")
        
        tables[top_level_key] = "\n".join(lines)
    
    return tables

def generate_detail_table(skill_name, tasks):
    """Generate a detail table for a specific skill"""
    display_name = SKILL_DISPLAY_NAMES.get(skill_name, skill_name.replace('_', ' ').title())
    
    lines = []
    lines.append(r"\begin{table*}[h!]")
    lines.append(r"\centering")
    lines.append(f"\\caption{{\\small \\textbf{{{escape_latex(display_name)} Tasks}}}}")
    lines.append(r"\scalebox{0.7}{")
    lines.append(r"\begin{NiceTabular}{l M{0.45\linewidth} M{0.45\linewidth}}")
    lines.append(r"\CodeBefore")
    lines.append(r"    \Body")
    lines.append(r"\toprule[1.2pt]")
    lines.append(r"\textbf{Tasks} & \textbf{Questions} & \textbf{Descriptions} \\")
    lines.append(r"\midrule")
    
    for i, task in enumerate(tasks):
        if i > 0:
            lines.append(r"\midrule")
        
        task_display = clean_task_name(task['name'])
        
        pos_question = task.get('pos_question', '')
        neg_question = task.get('neg_question', '')
        pos_prompt = task.get('pos_prompt', '')
        neg_prompt = task.get('neg_prompt', '')
        
        lines.append(f"\\multirow{{2}}{{*}}{{\\textbf{{{escape_latex(task_display)}}}}} & \\textbf{{Positive:}} {escape_latex(pos_question)} & \\textbf{{Positive:}} {escape_latex(pos_prompt)} \\\\")
        lines.append(r"\cmidrule(l){2-3}")
        lines.append(f"& \\textbf{{Negative:}} {escape_latex(neg_question)} & \\textbf{{Negative:}} {escape_latex(neg_prompt)} \\\\")
    
    lines.append(r"\bottomrule[1.2pt]")
    lines.append(r"\end{NiceTabular}")
    lines.append(r"}")
    lines.append(f"\\label{{tab:{skill_name}}}")
    lines.append(r"\end{table*}")
    
    return "\n".join(lines)

def load_primitives_from_json(json_path):
    """Load primitives from the label hierarchy JSON file"""
    import json
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Create a flat dictionary mapping primitive names to their definitions
    primitives = {}
    
    for collection_name, collection_data in data.items():
        for path, primitive_list in collection_data.items():
            for primitive_info in primitive_list:
                label_name = primitive_info['label_name']
                primitives[label_name] = {
                    'question': primitive_info.get('def_question', ''),
                    'prompt': primitive_info.get('def_prompt', ''),
                    'full_key': primitive_info.get('full_key', ''),
                    'collection': collection_name
                }
    
    return primitives

def generate_primitives_detail_tables(primitives_data, use_definition_only=False):
    """Generate individual primitive tables for each aspect following the hierarchy"""
    tables = {}
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            # Skip excluded aspects
            if aspect_key in EXCLUDED_ASPECTS:
                continue
                
            aspect_display = aspect_config["display_name"]
            # Filter out excluded primitives
            primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
            
            # Skip aspect if no primitives remain after filtering
            if not primitive_list:
                continue
            
            lines = []
            lines.append(r"\begin{table*}[h!]")
            lines.append(r"\centering")
            
            # Escape aspect display name
            aspect_display_escaped = escape_latex(aspect_display)
            lines.append(f"\\caption{{\\small \\textbf{{{aspect_display_escaped} Primitives}}}}")
            lines.append(r"\scalebox{0.7}{")
            
            if use_definition_only:
                # Single column table with only definitions
                lines.append(r"\begin{NiceTabular}{l M{0.9\linewidth}}")
                lines.append(r"\CodeBefore")
                lines.append(r"    \Body")
                lines.append(r"\toprule[1.2pt]")
                lines.append(r"\textbf{Primitive} & \textbf{Description} \\")
            else:
                # Two column table with questions and descriptions
                lines.append(r"\begin{NiceTabular}{l M{0.45\linewidth} M{0.45\linewidth}}")
                lines.append(r"\CodeBefore")
                lines.append(r"    \Body")
                lines.append(r"\toprule[1.2pt]")
                lines.append(r"\textbf{Primitive} & \textbf{Question} & \textbf{Description} \\")
            
            lines.append(r"\midrule")
            
            for i, primitive_name in enumerate(primitive_list):
                if i > 0:
                    lines.append(r"\midrule")
                
                # Check if there's a custom display name override
                if primitive_name in PRIMITIVE_DISPLAY_NAME_OVERRIDES:
                    primitive_display = PRIMITIVE_DISPLAY_NAME_OVERRIDES[primitive_name]
                else:
                    primitive_display = clean_task_name(primitive_name)
                
                # Get primitive info from loaded data
                if primitive_name in primitives_data:
                    prim_info = primitives_data[primitive_name]
                    question = prim_info.get('question', '')
                    prompt = prim_info.get('prompt', '')
                else:
                    # Fallback if primitive not found
                    question = f"Does the video have {primitive_display.lower()}?"
                    prompt = f"The video has {primitive_display.lower()}."
                
                # Escape each component separately
                primitive_display_escaped = escape_latex(primitive_display)
                question_escaped = escape_latex(question)
                prompt_escaped = escape_latex(prompt)
                
                if use_definition_only:
                    lines.append(f"\\textbf{{{primitive_display_escaped}}} ")
                    lines.append(f"& {prompt_escaped} \\\\")
                else:
                    lines.append(f"\\textbf{{{primitive_display_escaped}}} ")
                    lines.append(f"& {question_escaped} ")
                    lines.append(f"& {prompt_escaped} \\\\")
            
            lines.append(r"\bottomrule[1.2pt]")
            lines.append(r"\end{NiceTabular}")
            lines.append(r"}")
            lines.append(f"\\label{{tab:primitives_{aspect_key}}}")
            lines.append(r"\end{table*}")
            
            tables[aspect_key] = "\n".join(lines)
    
    return tables

# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_html(overview_latex, primitive_overview_tables, detail_tables, primitive_detail_tables, use_definition_only=False):
    """Generate HTML page with all tables"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CameraBench Pro LaTeX Tables</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 40px;
            border-bottom: 2px solid #6c757d;
            padding-bottom: 8px;
        }
        h3 {
            color: #666;
            margin-top: 30px;
        }
        h4 {
            color: #777;
            margin-top: 20px;
        }
        .table-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .copy-button {
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 10px;
            transition: background 0.3s;
        }
        .copy-button:hover {
            background: #0056b3;
        }
        .copy-button.copied {
            background: #28a745;
        }
        pre {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
        }
        code {
            font-family: 'Courier New', Courier, monospace;
        }
        .toc {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .toc ul {
            list-style-type: none;
            padding-left: 20px;
        }
        .toc a {
            color: #007bff;
            text-decoration: none;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        .section-nav {
            position: sticky;
            top: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section-nav a {
            display: inline-block;
            margin-right: 15px;
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
        }
        .section-nav a:hover {
            text-decoration: underline;
        }
        .stats-box {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-box h3 {
            margin-top: 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>CameraBench Pro LaTeX Tables</h1>
    
    <div class="section-nav">
        <a href="#stats">Statistics</a>
        <a href="#overview">Overview Table</a>
        <a href="#binary">Binary Tables</a>
        <a href="#primitives">Primitive Tables</a>
        <button class="copy-button" onclick="copyAllPrimitives()" style="margin-left: 20px;">Copy All Primitives Tables</button>
    </div>
"""
    
    # Add statistics section
    stats = count_hierarchy_stats()
    html += """
    <div id="stats" class="stats-box">
        <h3>Hierarchy Statistics</h3>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Top-Level Categories</div>
                <div class="stat-value">""" + str(stats['top_level']) + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Aspects</div>
                <div class="stat-value">""" + str(stats['aspects']) + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Primitives</div>
                <div class="stat-value">""" + str(stats['primitives']) + """</div>
            </div>
        </div>
        
        <h4>Breakdown by Category</h4>
        <div class="stats-grid">
"""
    
    for top_level_key, top_stats in stats['per_top_level'].items():
        html += f"""
            <div class="stat-item">
                <div class="stat-label">{top_stats['display_name']}</div>
                <div class="stat-value">{top_stats['aspects']} aspects, {top_stats['primitives']} primitives</div>
            </div>
"""
    
    html += """
        </div>
    </div>
    
    <div class="toc">
        <h3>Table of Contents</h3>
        <ul>
            <li><a href="#stats">Statistics</a></li>
            <li><a href="#overview">Overview Table</a></li>
            <li><a href="#binary">Binary Task Tables</a>
                <ul>
"""
    
    for skill_name in detail_tables.keys():
        display_name = SKILL_DISPLAY_NAMES.get(skill_name, skill_name.replace('_', ' ').title())
        html += f'                    <li><a href="#binary_{skill_name}">{display_name}</a></li>\n'
    
    html += """                </ul>
            </li>
            <li><a href="#primitives">Primitive Tables</a>
                <ul>
                    <li><a href="#primitive_overview">Primitive Overview Tables</a>
                        <ul>
"""
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        html += f'                            <li><a href="#primitive_overview_{top_level_key}">{top_level_config["display_name"]}</a></li>\n'
    
    html += """                        </ul>
                    </li>
                    <li><a href="#primitive_detail">Primitive Detail Tables</a>
                        <ul>
"""
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        html += f'                            <li>{top_level_config["display_name"]}\n'
        html += '                                <ul>\n'
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            # Skip excluded aspects
            if aspect_key in EXCLUDED_ASPECTS:
                continue
            # Skip aspects with no primitives after filtering
            primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
            if not primitive_list:
                continue
            html += f'                                    <li><a href="#primitive_detail_{aspect_key}">{aspect_config["display_name"]}</a></li>\n'
        html += '                                </ul>\n'
        html += '                            </li>\n'
    
    html += """                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
    
    <h2 id="overview">Overview Table</h2>
    <div class="table-container">
        <button class="copy-button" onclick="copyToClipboard('overview-latex', this)">Copy LaTeX</button>
        <pre><code id="overview-latex" class="language-latex">""" + overview_latex.replace('<', '&lt;').replace('>', '&gt;') + """</code></pre>
    </div>
    
    <h2 id="binary">Binary Task Tables</h2>
"""
    
    for skill_name, latex in detail_tables.items():
        display_name = SKILL_DISPLAY_NAMES.get(skill_name, skill_name.replace('_', ' ').title())
        html += f"""
    <h3 id="binary_{skill_name}">{display_name}</h3>
    <div class="table-container">
        <button class="copy-button" onclick="copyToClipboard('binary-{skill_name}', this)">Copy LaTeX</button>
        <pre><code id="binary-{skill_name}" class="language-latex">""" + latex.replace('<', '&lt;').replace('>', '&gt;') + """</code></pre>
    </div>
"""
    
    html += """
    <h2 id="primitives">Primitive Tables</h2>
    
    <h3 id="primitive_overview">Primitive Overview Tables</h3>
"""
    
    for top_level_key, latex in primitive_overview_tables.items():
        top_level_config = PRIMITIVE_HIERARCHY[top_level_key]
        display_name = top_level_config["display_name"]
        html += f"""
    <h4 id="primitive_overview_{top_level_key}">{display_name}</h4>
    <div class="table-container">
        <button class="copy-button" onclick="copyToClipboard('primitive-overview-{top_level_key}', this)">Copy LaTeX</button>
        <pre><code id="primitive-overview-{top_level_key}" class="language-latex">""" + latex.replace('<', '&lt;').replace('>', '&gt;') + """</code></pre>
    </div>
"""
    
    html += """
    <h3 id="primitive_detail">Primitive Detail Tables</h3>
"""
    
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        html += f'    <h4>{top_level_config["display_name"]}</h4>\n'
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            if aspect_key in primitive_detail_tables:
                latex = primitive_detail_tables[aspect_key]
                aspect_display = aspect_config["display_name"]
                html += f"""
    <h5 id="primitive_detail_{aspect_key}">{aspect_display}</h5>
    <div class="table-container">
        <button class="copy-button" onclick="copyToClipboard('primitive-detail-{aspect_key}', this)">Copy LaTeX</button>
        <pre><code id="primitive-detail-{aspect_key}" class="language-latex">""" + latex.replace('<', '&lt;').replace('>', '&gt;') + """</code></pre>
    </div>
"""
    
    html += """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-latex.min.js"></script>
    <script>
        function copyToClipboard(elementId, button) {
            const element = document.getElementById(elementId);
            const text = element.textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy to clipboard');
            });
        }
        
        function copyAllPrimitives() {
            // Order: Camera Motion Overview, Camera Motion Details, Camera Setup Overview, Camera Setup Details, Shot Composition Overview, Shot Composition Details
            const elementIds = [
"""
    
    # Generate the list of element IDs in the correct order
    for top_level_key, top_level_config in PRIMITIVE_HIERARCHY.items():
        # Add overview table for this top-level category
        html += f"                'primitive-overview-{top_level_key}',\n"
        
        # Add all detail tables for this top-level category
        for aspect_key, aspect_config in top_level_config["aspects"].items():
            # Skip excluded aspects
            if aspect_key in EXCLUDED_ASPECTS:
                continue
            # Check if aspect has any non-excluded primitives
            primitive_list = [p for p in aspect_config["primitives"] if p not in EXCLUDED_PRIMITIVES]
            if primitive_list:
                html += f"                'primitive-detail-{aspect_key}',\n"
    
    html += """            ];
            
            let allText = '';
            for (const id of elementIds) {
                const element = document.getElementById(id);
                if (element) {
                    allText += element.textContent + '\\n\\n';
                }
            }
            
            navigator.clipboard.writeText(allText).then(() => {
                alert('All primitive tables copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy to clipboard');
            });
        }
    </script>
</body>
</html>
"""
    
    return html

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Generate LaTeX tables for CameraBench Pro')
    parser.add_argument('--definition-only', action='store_true',
                       help='Use only definitions (no questions) in primitive detail tables')
    args = parser.parse_args()
    
    # Import benchmark_config
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import benchmark_config
    except ImportError:
        print("Error: Could not import benchmark_config.py")
        print("Make sure benchmark_config.py is in the same directory as this script")
        sys.exit(1)
    
    folder_name = "camerabench_pro"
    print(f"Generating tables for: {folder_name}")
    
    if args.definition_only:
        print("Mode: Definition-only (questions will be excluded from primitive detail tables)")
    else:
        print("Mode: Full tables (questions and definitions included)")
    
    # Get task data
    skills_data = benchmark_config.get_pairwise_labels(folder_name)
    
    print(f"Found {len(skills_data)} skill categories")
    
    # Calculate and print hierarchy statistics
    print("\n" + "="*60)
    print("HIERARCHY STATISTICS")
    print("="*60)
    stats = count_hierarchy_stats()
    print(f"Top-Level Categories: {stats['top_level']}")
    print(f"Total Aspects: {stats['aspects']}")
    print(f"Total Primitives: {stats['primitives']}")
    print("\nBreakdown by Category:")
    for top_level_key, top_stats in stats['per_top_level'].items():
        print(f"  {top_stats['display_name']}: {top_stats['aspects']} aspects, {top_stats['primitives']} primitives")
    print("="*60 + "\n")
    
    # Load primitives from JSON
    json_path = Path(__file__).parent / "label_hierarchy.json"
    if not json_path.exists():
        print(f"Error: Could not find label_hierarchy.json at {json_path}")
        print("Please ensure the JSON file is in the same directory")
        sys.exit(1)
    
    print("Loading primitives from JSON...")
    primitives_data = load_primitives_from_json(json_path)
    print(f"Loaded {len(primitives_data)} primitives")
    
    # Generate overview table
    print("Generating overview table...")
    overview_latex = generate_overview_table(skills_data, folder_name)
    
    # Generate primitive overview tables (3 tables for Motion, Setup, Composition)
    print("Generating primitive overview tables...")
    primitive_overview_tables = generate_primitive_overview_tables(primitives_data)
    
    # Generate detail tables
    print("Generating binary task tables...")
    detail_tables = {}
    for skill_name, tasks in skills_data.items():
        print(f"  - {skill_name}: {len(tasks)} tasks")
        detail_tables[skill_name] = generate_detail_table(skill_name, tasks)
    
    # Generate primitive detail tables
    print("Generating primitive detail tables...")
    primitive_detail_tables = generate_primitives_detail_tables(primitives_data, args.definition_only)
    print(f"  Generated {len(primitive_detail_tables)} primitive detail tables")
    
    # Generate HTML
    print("Generating HTML output...")
    html = generate_html(overview_latex, primitive_overview_tables, detail_tables, primitive_detail_tables, args.definition_only)
    
    # Write HTML file to current directory
    output_file = Path("camerabench_pro_tables.html")
    output_file.write_text(html)
    
    print(f"\n✓ Successfully generated tables!")
    print(f"  Total skills: {len(skills_data)}")
    print(f"  Total tasks: {sum(len(tasks) for tasks in skills_data.values())}")
    print(f"  Total primitives: {len(primitives_data)}")
    print(f"  Primitive overview tables: {len(primitive_overview_tables)}")
    print(f"  Primitive detail tables: {len(primitive_detail_tables)}")
    print(f"  Output file: {output_file.absolute()}")

if __name__ == "__main__":
    main()