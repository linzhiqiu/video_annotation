# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the video exhibit complex color grading, composition, or dynamics, involving dynamic or contrasting variations in color temperature, saturation, or brightness? | 27 | 47 | lighting_setup.color_grading.is_color_grading_complex |
| Does the video end with a wide shot of scenery, or a wide shot that frames the subject while keeping enough background context? | 26 | 33 | cam_setup.shot_size.end_with.shot_size_end_with_wide |
| Does the camera show any vibrations, shaking, or wobbling? | 25 | 49 | cam_motion.steadiness_and_movement.shaky_camera |
| Does the light quality in the video vary across the scene, making it difficult to categorize? | 25 | 49 | lighting_setup.light_quality.light_quality_is_complex |
| Does the video start with a wide shot of scenery, or a wide shot that frames the subject while keeping enough background context? | 22 | 33 | cam_setup.shot_size.start_with.shot_size_start_with_wide |
| Does the video show a wide shot of scenery, or a wide shot that frames the subject while keeping enough background context? | 21 | 36 | cam_setup.shot_size.is_always.shot_size_is_wide |
| Does the camera show simple motion, such as moving in a single direction, maintaining a consistent speed, or following a clear and predictable path? | 20 | 54 | cam_motion.motion_complexity.is_simple_motion |
| Is the video lit by unclear light sources (neither clear sunlight nor firelight) that are unseen in the frame? | 20 | 0 | lighting_setup.light_source.has_non_visible_light_source |
| Is the camera movement exceptionally smooth and highly stable? | 19 | 41 | cam_motion.steadiness_and_movement.very_stable_camera |
| Is the camera using a shallow depth of field with limited focus range? | 19 | 44 | cam_setup.focus.is_shallow_focus |
| Is the subject illuminated with soft, ambient light? | 19 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_ambient_light |
| Is the video set in an indoor environment? | 18 | 56 | lighting_setup.scene.scene_type_is_interior |
| Is the lighting on the subject complex (e.g., 2D/2.5D videos) or varying due to changes in lighting, camera motion, subject transitions, or multiple subjects with different lighting conditions? | 16 | 29 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex |
| Does the camera move forward (not zooming in) in the scene, or move north if it's a bird's eye view, or move south if it's a worm's eye view? | 15 | 33 | cam_motion.ground_centric_movement.forward.has_forward_wrt_ground_birds_worms_included |
| Does the lighting on the subject have a normal contrast ratio (1:2 to 1:8), providing a balanced distinction between bright and dark areas? | 15 | 30 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_normal |
| Does the video focus on scenery or environment without emphasis on any subjects? | 14 | 60 | cam_setup.shot_type.is_just_scenery_shot |
| Does the video consistently feature one dominant human subject or a single group of human subjects in the frame? | 14 | 60 | cam_setup.shot_type.is_just_human_shot |
| Is the shot focused on human subjects? | 14 | 23 | cam_setup.shot_type.is_human_shot |
| Is the camera moving forward in the scene? | 13 | 29 | cam_motion.ground_centric_movement.forward.has_forward_wrt_ground |
| Is there a noticeable light source illuminating the subject from the top (top lighting) as seen from the camera’s perspective? | 13 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_top_light |
| Is there a noticeable light source illuminating the subject from the side (side lighting) as seen from the camera’s perspective? | 13 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_side_light |
| Does the video feature regular daylight with balanced brightness, neither particularly hard nor soft? | 13 | 25 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_normal |
| Does the video feature bright, direct sunlight with strong intensity? | 13 | 25 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_sunny |
| Does the video end with the foreground in focus, using a shallow depth of field? | 12 | 7 | cam_setup.focus.end_with.focus_end_with_foreground |
| Does the video start with a focus on the foreground, using a shallow depth of field to blur other areas? | 12 | 7 | cam_setup.focus.start_with.focus_start_with_foreground |
| Does the video end with a medium shot that frames about half of the subject? | 12 | 47 | cam_setup.shot_size.end_with.shot_size_end_with_medium |
| Does the scene in this video features hard lighting with strong, directional light? | 12 | 62 | lighting_setup.light_quality.light_quality_is_hard |
| Does the video contain practical artificial light with its source(s) clearly visible in the frame? | 12 | 0 | lighting_setup.light_source.has_artificial_practical_light |
| Does the shot contain on-screen overlays, such as watermarks, or titles, or subtitles, or icons, or heads-up displays, or framing elements? | 11 | 63 | cam_setup.has_overlays |
| Does the video contain multiple subjects or multiple groups of subjects? | 11 | 44 | cam_setup.subject_framing.has_many_subjects |
| Is the video consistently focused on the foreground using a shallow depth of field? | 11 | 8 | cam_setup.focus.is_always.focus_is_foreground |
| Is the scene shown from the first-person perspective, as if through the character’s eyes? | 11 | 63 | cam_setup.point_of_view.first_person_pov |
| Does the video start with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down? | 11 | 57 | cam_setup.angle.start_with.camera_angle_start_with_high_angle |
| Does the scene in this video contain both hard and soft lighting? | 11 | 55 | lighting_setup.light_quality.light_quality_is_contrasting |
| Does the video’s brightness level change over time? | 11 | 59 | lighting_setup.color_grading.brightness.brightness_is_changing |
| Does the camera track the subject as they move? | 10 | 64 | cam_motion.object_centric_movement.track_shot |
| Does the camera pan to the right? | 10 | 31 | cam_motion.camera_centric_movement.pan_right.has_pan_right |
| Does the video start with a close-up shot that highlights a distinct part of the subject while maintaining context? | 10 | 45 | cam_setup.shot_size.start_with.shot_size_start_with_close_up |
| Does the video start with a medium shot that frames about half of the subject? | 10 | 45 | cam_setup.shot_size.start_with.shot_size_start_with_medium |
| Does the video end with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down? | 10 | 58 | cam_setup.angle.end_with.camera_angle_end_with_high_angle |
| Does the lighting on the subject have a high contrast ratio, where lit areas are significantly brighter than dark areas (1:8 or above)? | 10 | 35 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_high |
| Does the video feature soft, diffused light on an overcast day? | 10 | 28 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_overcast |
| Is the camera completely still without any motion or shaking? | 9 | 64 | cam_motion.steadiness_and_movement.fixed_camera |
| Is the camera stationary with minor vibrations or shaking? | 9 | 62 | cam_motion.steadiness_and_movement.fixed_camera_with_shake |
| Does the video show a medium shot that frames about half of the subject? | 9 | 49 | cam_setup.shot_size.is_always.shot_size_is_medium |
| Is the camera positioned at a high angle throughout the video, looking down at the scene but not completely top-down? | 9 | 59 | cam_setup.angle.is_always.camera_angle_is_high_angle |
| Does the video consistently feature one dominant non-human subject or a single group of non-human subjects in the frame? | 9 | 65 | cam_setup.shot_type.is_just_non_human_shot |
| Is the shot focused on non-human subjects? | 9 | 28 | cam_setup.shot_type.is_non_human_shot |
| Does the video feature different subjects, varying in type or size, making shot size classification difficult? | 9 | 65 | cam_setup.shot_type.is_just_different_subject_in_focus_shot |
| Is the subject lit by low-key lighting? | 9 | 36 | lighting_setup.subject_lighting.light_contrast.low_key_lighting |
| Is the scene type unclear, ambiguous, or changing throughout the video? | 9 | 65 | lighting_setup.scene.scene_type_is_complex_others |
| Does the video end with the camera positioned above the subject? | 8 | 37 | cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_above_subject |
| Does this shot contain noticeable lens distortion? | 8 | 66 | cam_setup.lens_distortion.with_lens_distortion |
| Does the video start with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present? | 8 | 51 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_hip_level |
| Is this video captured by a drone? | 8 | 66 | cam_setup.point_of_view.drone_pov |
| Does the video start with a full shot that frames the entire body of the subject? | 8 | 47 | cam_setup.shot_size.start_with.shot_size_start_with_full |
| Does the video maintain a close-up shot throughout, consistently highlighting a distinct part of the subject while maintaining context? | 8 | 51 | cam_setup.shot_size.is_always.shot_size_is_close_up |
| Does the video end with a full shot that frames the entire body of the subject? | 8 | 51 | cam_setup.shot_size.end_with.shot_size_end_with_full |
| Does the video end with a close-up shot that highlights a distinct part of the subject while maintaining context? | 8 | 51 | cam_setup.shot_size.end_with.shot_size_end_with_close_up |
| Does the camera show noticable vibrations, shaking, or wobbling? | 7 | 49 | cam_motion.steadiness_and_movement.very_shaky_camera |
| Does the video start with the camera positioned noticeably higher than the subject? | 7 | 38 | cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_above_subject |
| Is the camera positioned at hip level, roughly between knee and waist height, whether or not a human subject is present? | 7 | 52 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_hip_level |
| Does the video end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present? | 7 | 52 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_hip_level |
| Does the video end with the camera positioned high at an aerial level? | 7 | 52 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_aerial_level |
| Does the video end with the camera at ground level, positioned close to the ground? | 7 | 52 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_ground_level |
| Does the video start with the camera positioned high at an aerial level? | 7 | 52 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_aerial_level |
| Does the video end with the middle ground in focus while the foreground and background are blurred? | 7 | 12 | cam_setup.focus.end_with.focus_end_with_middle_ground |
| Does the shot size change throughout the video? | 7 | 52 | cam_setup.shot_size.shot_size_change |
| Is an obvious Dutch (Canted) angle (of more than 15 degrees) present in the video? | 7 | 61 | cam_setup.angle.is_dutch_angle |
| Does the video end with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below? | 7 | 61 | cam_setup.angle.end_with.camera_angle_end_with_low_angle |
| Is there a clear subject in the video, but its anatomy looks unnatural or exaggerated, as seen in games or CGI? | 7 | 67 | cam_setup.shot_type.is_just_clear_subject_atypical_shot |
| Does the lighting setup create a polished, professional appearance, common in portrait photography or videography? | 7 | 0 | lighting_setup.subject_lighting.protrait_lighting |
| Is there a noticeable light source illuminating the subject from the front as seen from the camera’s perspective? | 7 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_front_light |
| Does the video lacks a realistic light source, with lighting that does not follow natural physics? | 7 | 0 | lighting_setup.light_source.is_abstract |
| Does the video have strong contrast between bright and dark areas? | 7 | 63 | lighting_setup.color_grading.brightness.brightness_is_contrasting |
| Is the video set in a synthetic or 2D environment with unrealistic lighting effects? | 7 | 67 | lighting_setup.scene.scene_type_is_synthetic |
| Is the camera positioned noticeably higher than the subject throughout the video? | 6 | 39 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_above_subject |
| Is the camera positioned at ground level throughout the video? | 6 | 53 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_ground_level |
| Is the camera positioned at an aerial level throughout the video? | 6 | 53 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_aerial_level |
| Does the video start with the camera at ground level, positioned close to the ground? | 6 | 53 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_ground_level |
| Is the video consistently focused on the middle ground, keeping the foreground and background blurred? | 6 | 13 | cam_setup.focus.is_always.focus_is_middle_ground |
| Does the video start with a focus on the middle ground, using a shallow depth of field to blur both the foreground and background? | 6 | 13 | cam_setup.focus.start_with.focus_start_with_middle_ground |
| Does the video maintain a full shot that frames the entire body of the subject? | 6 | 52 | cam_setup.shot_size.is_always.shot_size_is_full |
| Does the light quality in the scene change between hard and soft over time? | 6 | 60 | lighting_setup.light_quality.light_quality_is_changing |
| Does the primary light source in the video change over time or include a rare light source that is not the sun, fire, moon and stars, or artificial light? | 6 | 0 | lighting_setup.light_source.has_complex_light_source |
| Does the video mainly feature highly saturated colors, making hues appear vivid and intense? | 6 | 68 | lighting_setup.color_grading.saturation.color_saturation_is_high |
| Does the video have noticeable shifts in color saturation between high and low over time? | 6 | 67 | lighting_setup.color_grading.saturation.color_saturation_is_changing |
| Does the camera move upward (not tilting up) in the scene, or move east if it's a bird's eye view, or move west if it's a worm's eye view? | 5 | 32 | cam_motion.ground_centric_movement.upward.has_upward_wrt_ground_birds_worms_included |
| Does the camera tilt upward? | 5 | 32 | cam_motion.camera_centric_movement.tilt_up.has_tilt_up |
| Does the camera have noticeable motion at a fast speed? | 5 | 61 | cam_motion.steadiness_and_movement.fast_moving_camera |
| Is the camera motion minimal, hard to discern, or very subtle? | 5 | 45 | cam_motion.motion_complexity.is_minor_motion |
| Does the video start with an extreme wide shot that emphasizes the setting over any subjects? | 5 | 50 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_wide |
| Does the camera angle decrease noticeably relative to the ground? | 5 | 2 | cam_setup.angle.camera_angle_change_from_high_to_low |
| Does the degree of the Dutch angle shift throughout the video? | 5 | 63 | cam_setup.angle.is_dutch_angle_varying |
| Is there a noticeable light source illuminating the subject from behind (backlighting) as seen from the camera’s perspective? | 5 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_back_light |
| Does the lighting in the video flash, creating sudden bursts of light in an on/off pattern? | 5 | 0 | lighting_setup.dynamic_light.flashing |
| Is the video noticeably bright or overexposed? | 5 | 69 | lighting_setup.color_grading.brightness.brightness_is_brighter_than_normal |
| Is the video well-lit with strong lighting, making the scene bright and clear but not overexposed? | 5 | 69 | lighting_setup.color_grading.brightness.brightness_is_bright |
| Does the video feature volumetric lighting, where light appears as a visible volume? | 5 | 0 | lighting_setup.volumetric_lighting.has_volumetric_lighting |
| Does the camera move backward (not zooming out) in the scene, or move south if it's a bird's eye view, or move north if it's a worm's eye view? | 4 | 45 | cam_motion.ground_centric_movement.backward.has_backward_wrt_ground_birds_worms_included |
| Is the camera moving backward in the scene? | 4 | 39 | cam_motion.ground_centric_movement.backward.has_backward_wrt_ground |
| Does the subject change in the video, such as in a revealing shot where a subject appears, disappears, or transitions to another subject? | 4 | 55 | cam_setup.subject_framing.has_subject_change |
| Does the video end with the camera at an overhead level, above human height but below an aerial view, roughly at second-floor level? | 4 | 55 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_overhead_level |
| Does the shot size change from small to large? | 4 | 55 | cam_setup.shot_size.shot_size_change_from_small_to_large |
| Does the video include a revealing shot where a subject appears? | 4 | 55 | cam_setup.shot_size.subject_revealing |
| Is the video an extreme wide shot that emphasizes the setting over any subjects? | 4 | 55 | cam_setup.shot_size.is_always.shot_size_is_extreme_wide |
| Does the video end with a wide shot? | 4 | 55 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_wide |
| Does the video start with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below? | 4 | 64 | cam_setup.angle.start_with.camera_angle_start_with_low_angle |
| Does the video start with the camera positioned at a bird's eye angle, offering a top-down view directly looking down at the ground? | 4 | 64 | cam_setup.angle.start_with.camera_angle_start_with_bird_eye_angle |
| Does the video end with the camera positioned at a bird’s eye angle, looking directly downward at the ground? | 4 | 64 | cam_setup.angle.end_with.camera_angle_end_with_bird_eye_angle |
| Is the camera positioned at a low angle throughout the video, looking upward from a lower perspective but not directly from below? | 4 | 64 | cam_setup.angle.is_always.camera_angle_is_low_angle |
| Is the camera positioned at a bird’s eye angle throughout the video, looking directly downward at the ground? | 4 | 64 | cam_setup.angle.is_always.camera_angle_is_bird_eye_angle |
| The video includes a subject change, where a subject appears, disappears, or transitions to another. | 4 | 70 | cam_setup.shot_type.is_just_change_of_subject_shot |
| Is the subject lit with flat lighting, with little to no contrast? | 4 | 41 | lighting_setup.subject_lighting.light_contrast.flat_lighting |
| Does the lighting on the subject have minimal contrast (1:1 to 1:2), creating a flat lighting effect? | 4 | 41 | lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_minimal |
| Is the subject illuminated by a mix of back and side lighting? | 4 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_rear_side |
| Does the video feature visible splashing or wave-like motion in water or other liquids? | 4 | 0 | lighting_setup.dynamic_effect.splashing_waves |
| Is the video entirely in black and white, with no color present? | 4 | 70 | lighting_setup.color_grading.is_black_white |
| Does the video mainly feature desaturated colors, making hues appear muted or grayish? | 4 | 70 | lighting_setup.color_grading.saturation.color_saturation_is_low |
| Does the video have noticeable shifts between warm and cool color tones? | 4 | 68 | lighting_setup.color_grading.temperature.color_temperature_is_changing |
| Does the video feature strong contrasts between warm and cool colors? | 4 | 68 | lighting_setup.color_grading.temperature.color_temperature_is_contrasting |
| Is the video noticeably dark or underexposed? | 4 | 70 | lighting_setup.color_grading.brightness.brightness_is_darker_than_normal |
| Does the video have a highly complex or unusual brightness level that is hard to classify? | 4 | 70 | lighting_setup.color_grading.brightness.brightness_is_complex_others |
| Does the video feature a vignette effect, where the edges gradually darken or fade? | 4 | 0 | lighting_setup.special_effect.vignette |
| Does the camera pan to track the subjects as they move? | 3 | 71 | cam_motion.object_centric_movement.pan_tracking_shot |
| Does the camera pan to the left? | 3 | 39 | cam_motion.camera_centric_movement.pan_left.has_pan_left |
| Does the camera move leftward in the scene? | 3 | 33 | cam_motion.camera_centric_movement.leftward.has_leftward |
| Does the camera move rightward in the scene? | 3 | 33 | cam_motion.camera_centric_movement.rightward.has_rightward |
| Does the video start with the camera positioned below the subject? | 3 | 42 | cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_below_subject |
| Does the video end with the camera positioned below the subject? | 3 | 42 | cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_below_subject |
| Is the camera positioned below the subject throughout the video? | 3 | 42 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject |
| Does the camera height decrease noticeably in relation to the ground? | 3 | 1 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_high_to_low |
| Is the camera positioned at an overhead level throughout the video, positioned above human height but below an aerial view, roughly at second-floor level? | 3 | 56 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_overhead_level |
| Does the video start with the camera at an overhead level, above human height but below an aerial view, roughly at second-floor level? | 3 | 56 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_overhead_level |
| Does the video have an extremely shallow depth of field? | 3 | 60 | cam_setup.focus.is_ultra_shallow_focus |
| Is this a 3D gaming video featuring a third-person perspective with the character’s full body visible? | 3 | 71 | cam_setup.point_of_view.third_person_full_body_game_pov |
| Does the shot size change from large to small? | 3 | 56 | cam_setup.shot_size.shot_size_change_from_large_to_small |
| Does the video start with the camera at a level angle and transition to a low angle? | 3 | 65 | cam_setup.angle.from_to.camera_angle_from_level_to_low |
| Does the video feature a noticeable reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail? | 3 | 0 | lighting_setup.reflection.reflection_from_glossy_surface |
| Does the video feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering? | 3 | 0 | lighting_setup.dynamic_light.pulsing_flickering |
| Does the video feature moving lights that shift direction or move across the scene? | 3 | 0 | lighting_setup.dynamic_light.moving_light |
| Does the video contain a revealing shot that gradually uncovers a new environment or subject? | 3 | 0 | lighting_setup.dynamic_effect.revealing_shot |
| Is the video predominantly featuring cool colors, such as blues or greens? | 3 | 71 | lighting_setup.color_grading.temperature.color_temperature_is_cool |
| Is the video predominantly dark with dim lighting but not so underexposed that most details are lost? | 3 | 71 | lighting_setup.color_grading.brightness.brightness_is_dark |
| Does the video feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights)? | 3 | 0 | lighting_setup.volumetric_lighting.volumetric_light_others |
| Does the video feature artificial colored or neon lighting? | 3 | 0 | lighting_setup.special_effect.colored_neon_lighting |
| Does the video contain noticeable motion blur? | 2 | 62 | cam_motion.has_motion_blur |
| Is it a tracking shot with the camera moving from the side to follow the subject as they move? | 2 | 72 | cam_motion.object_centric_movement.side_tracking_shot |
| Is it a tracking shot with the camera moving ahead of the subject? | 2 | 72 | cam_motion.object_centric_movement.lead_tracking_shot |
| Does the subject appear larger during the tracking shot? | 2 | 72 | cam_motion.object_centric_movement.tracking_subject_larger_size |
| Does the camera move upward relative to the ground? | 2 | 28 | cam_motion.ground_centric_movement.upward.has_upward_wrt_ground |
| Does the camera roll counterclockwise? | 2 | 32 | cam_motion.camera_centric_movement.roll_counterclockwise.has_roll_counterclockwise |
| Does the camera only pan leftward without any other camera movements? | 2 | 72 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the camera tilt downward? | 2 | 35 | cam_motion.camera_centric_movement.tilt_down.has_tilt_down |
| Does the camera move in a counterclockwise arc? | 2 | 70 | cam_motion.arc_crane_movement.arc_counterclockwise.has_arc_counterclockwise |
| Is the camera craning upward in an arc? | 2 | 70 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the camera height decrease noticeably in relation to the subject? | 2 | 1 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_high_to_low |
| Does the camera start at the subject's height and then move up to a higher position than them? | 2 | 43 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject |
| Does the video end with the camera positioned at water level, where the waterline is clearly visible? | 2 | 57 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_water_level |
| Is rack focus or pull focus used in the video? | 2 | 61 | cam_setup.focus.is_rack_pull_focus |
| Is the camera positioned directly above the subject for a top-down perspective? | 2 | 72 | cam_setup.point_of_view.overhead_pov |
| Does the camera angle increase noticeably relative to the ground? | 2 | 5 | cam_setup.angle.camera_angle_change_from_low_to_high |
| Does the Dutch angle remain the same throughout the video? | 2 | 66 | cam_setup.angle.is_dutch_angle_fixed |
| Does the video start with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 2 | 66 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the video start with the camera at a high angle and transition to a level angle? | 2 | 66 | cam_setup.angle.from_to.camera_angle_from_high_to_level |
| Is the subject illuminated by a mix of front and side lighting? | 2 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_front_side |
| Does the video show noticeable shimmering effects or bright highlights from light reflecting off water? | 2 | 0 | lighting_setup.reflection.reflection_from_water |
| Does the video feature warm, golden sunlight at sunrise or sunset? | 2 | 36 | lighting_setup.light_quality.sunlight_quality.sunlight_level_is_sunset_sunrise |
| Does the video feature an explosion with a sudden burst of flames, matter, and outward force? | 2 | 0 | lighting_setup.dynamic_effect.explosion |
| Does the video feature a complex color composition or dynamics that cannot be classified as strictly black-and-white, warm, cool, or neutral? | 2 | 72 | lighting_setup.color_grading.temperature.color_temperature_is_complex_others |
| Is the video predominantly featuring warm colors, such as reds, oranges, or yellows? | 2 | 72 | lighting_setup.color_grading.temperature.color_temperature_is_warm |
| Is there rim lighting that creates a glowing edge around the subject? | 2 | 0 | lighting_setup.special_effect.rim_light |
| Does the video feature light from street lamps? | 2 | 0 | lighting_setup.special_effect.street_light |
| Is there a silhouette lighting effect that creates a dark outline of the foreground subject against a bright background? | 2 | 0 | lighting_setup.special_effect.silhouette |
| Does the camera follow the subject while moving in an arc? | 1 | 73 | cam_motion.object_centric_movement.arc_tracking_shot |
| Is it a side-tracking shot where the camera moves left to follow the subject? | 1 | 73 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the camera track the subject from an aerial perspective? | 1 | 73 | cam_motion.object_centric_movement.aerial_tracking_shot |
| Is it a tracking shot with the camera following behind the subject? | 1 | 72 | cam_motion.object_centric_movement.tail_tracking_shot |
| Does the subject appear smaller during the tracking shot? | 1 | 73 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view? | 1 | 73 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground_birds_worms_included |
| Does the camera only move backward (not zooming out) with respect to the ground? | 1 | 61 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground |
| Does the camera move only forward (not zooming in) in the scene, or only northward in a bird's eye view, or only southward in a worm's eye view? | 1 | 73 | cam_motion.ground_centric_movement.forward.only_forward_wrt_ground_birds_worms_included |
| Does the camera only move forward (not zooming in) with respect to the ground? | 1 | 61 | cam_motion.ground_centric_movement.forward.only_forward_wrt_ground |
| Does the camera only roll counterclockwise without any other camera movements? | 1 | 73 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera zoom out? | 1 | 34 | cam_motion.camera_centric_movement.zoom_out.has_zoom_out |
| Does the camera zoom in? | 1 | 34 | cam_motion.camera_centric_movement.zoom_in.has_zoom_in |
| Does the camera only zoom in with no other movement? | 1 | 73 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera only move leftward without any other camera movements? | 1 | 73 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera only pan rightward without any other camera movements? | 1 | 73 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera only move rightward without any other camera movements? | 1 | 73 | cam_motion.camera_centric_movement.rightward.only_rightward |
| Does the camera only tilt downward without any other camera movements? | 1 | 73 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the camera have noticeable motion but at a slow motion speed? | 1 | 65 | cam_motion.steadiness_and_movement.slow_moving_camera |
| Does the camera height increase noticeably in relation to the subject? | 1 | 2 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_low_to_high |
| Does the camera start noticeably higher than the subject and then move down to their height? | 1 | 44 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject |
| Does this shot have a fisheye lens distortion? | 1 | 73 | cam_setup.lens_distortion.fisheye_distortion |
| Does the camera height increase noticeably in relation to the ground? | 1 | 3 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_low_to_high |
| Is the camera positioned at water level throughout the video, above the water surface with the waterline clearly visible? | 1 | 58 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_water_level |
| Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface? | 1 | 58 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level |
| Does the video end with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 1 | 58 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level |
| Does the video start with the camera positioned at water level, where the waterline is clearly visible above the surface? | 1 | 58 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_water_level |
| Does the video start with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 1 | 58 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level |
| Does the focal plane transition from distant to close? | 1 | 56 | cam_setup.focus.focus_change_from_far_to_near |
| Does the focal plane transition from close to distant? | 1 | 56 | cam_setup.focus.focus_change_from_near_to_far |
| Does the video start with the foreground in focus and then transition to focusing on the middle ground? | 1 | 18 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Does the video start with the background in focus and then shift to the foreground? | 1 | 18 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the video start with the background in focus, using a shallow depth of field? | 1 | 18 | cam_setup.focus.start_with.focus_start_with_background |
| Is this video played at a slower speed than real-time? | 1 | 72 | cam_setup.video_speed.slow_motion |
| Is this video played at a faster speed than real-time? | 1 | 72 | cam_setup.video_speed.fast_motion |
| Is this video played at a slightly faster speed than real-time (e.g., 1x-3x)? | 1 | 72 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does this shot feature a speed ramp effect where playback speed smoothly transitions between faster and slower speeds? | 1 | 73 | cam_setup.video_speed.speed_ramp |
| Does this video capture a screen recording with visible UI elements? | 1 | 73 | cam_setup.point_of_view.screen_recording_pov |
| Is this a professional viewpoint used in television broadcasts? | 1 | 73 | cam_setup.point_of_view.broadcast_pov |
| Is this a 2D or 3D gaming video where the camera is positioned at the side of the character? | 1 | 73 | cam_setup.point_of_view.third_person_side_view_game_pov |
| Is the camera positioned behind the character, showing their upper body and the scene ahead? | 1 | 73 | cam_setup.point_of_view.third_person_over_shoulder_pov |
| Does the video end with a medium close-up shot that frames the human subject from the chest upward? | 1 | 58 | cam_setup.shot_size.end_with.shot_size_end_with_medium_close_up |
| Does the video start with the camera at a level angle and transition to a high angle? | 1 | 67 | cam_setup.angle.from_to.camera_angle_from_level_to_high |
| Does the video end with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 1 | 67 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Is the camera positioned at a worm’s eye angle throughout the video, looking sharply upward to the sky? | 1 | 67 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the video feature multiple subjects with no clear focus on any one subject? | 1 | 73 | cam_setup.shot_type.is_just_many_subject_no_focus_shot |
| Does the video feature multiple subjects, but one clearly stands out as the main focus? | 1 | 73 | cam_setup.shot_type.is_just_many_subject_one_focus_shot |
| Is there Rembrandt lighting that illuminates one side of the subject’s face, creating a small triangle of light on the other? | 1 | 0 | lighting_setup.subject_lighting.rembrandt_lighting |
| Does the video show strong reflections from light bouncing off a mirror, clearly mirroring the scenery in detail? | 1 | 0 | lighting_setup.reflection.reflection_from_mirror |
| Does the lighting color in the video change gradually and smoothly (a smooth color shift)? | 1 | 0 | lighting_setup.dynamic_light.color_shifting_smooth |
| Does the video show objects breaking, shattering, or fragmenting into smaller pieces? | 1 | 0 | lighting_setup.dynamic_effect.shattering_breaking |
| Does the video show objects or characters floating or levitating as if unaffected by gravity? | 1 | 0 | lighting_setup.dynamic_effect.levitation_floating |
| Is the video primarily lit by firelight? | 1 | 0 | lighting_setup.light_source.has_firelight |
| Does the video feature a complex color composition or dynamics that cannot be classified as strictly high, low, or neutral color saturation? | 1 | 73 | lighting_setup.color_grading.saturation.color_saturation_is_complex_others |
| Is the video extremely dark and underexposed, with barely any visible details due to minimal lighting? | 1 | 73 | lighting_setup.color_grading.brightness.brightness_is_very_dark |
| Does the video feature intense light passing through smoke, fog, or liquid, shaping visible light volumes? | 1 | 0 | lighting_setup.volumetric_lighting.light_through_medium |
| Does the video feature striking, separated rays of light (god rays) streaming through gaps in the environment? | 1 | 0 | lighting_setup.volumetric_lighting.god_rays |
| Does the video use a mist diffusion filter to soften the image, creating a dreamy, glowing effect? | 1 | 0 | lighting_setup.lens_effect.mist_diffusion |
| Does the video feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field? | 1 | 0 | lighting_setup.lens_effect.bokeh |
| Does the video feature water caustics, where light creates dynamic rippling patterns? | 1 | 0 | lighting_setup.special_effect.water_caustics |
| Does the video feature bright and colorful city lighting from various artificial sources? | 1 | 0 | lighting_setup.special_effect.city_light |
| Does the video include shot transitions? | 0 | 74 | cam_motion.has_shot_transition_cam_motion |
| Does the video contain a frame freeze effect at any point? | 0 | 62 | cam_motion.has_frame_freezing |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 0 | 74 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 0 | 74 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Is it a side-tracking shot where the camera moves right to follow the subject? | 0 | 74 | cam_motion.object_centric_movement.side_tracking_shot_rightward |
| Does the camera tilt to track the subjects as they move? | 0 | 74 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Is it a tracking shot with the camera leading the subject from a front-side angle? | 0 | 74 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind the subject at a rear-side angle? | 0 | 74 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera only move upward (not tilting up) with respect to the ground? | 0 | 62 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 0 | 74 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera move downward relative to the ground? | 0 | 30 | cam_motion.ground_centric_movement.downward.has_downward_wrt_ground |
| Does the camera only move downward (not tilting down) with respect to the ground? | 0 | 62 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 0 | 74 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera move downward (not tilting down) in the scene, or move west if it's a bird's eye view, or move east if it's a worm's eye view? | 0 | 38 | cam_motion.ground_centric_movement.downward.has_downward_wrt_ground_birds_worms_included |
| Is the scene in the video dynamic? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Does the camera only zoom out with no other movement? | 0 | 74 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera move downward (not tilting down) with respect to the initial frame? | 0 | 33 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 0 | 74 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera only tilt upward without any other camera movements? | 0 | 74 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 33 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 0 | 74 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera only roll clockwise without any other camera movements? | 0 | 74 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Does the camera roll clockwise? | 0 | 34 | cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise |
| Does the camera move upward (not tilting up) with respect to the initial frame? | 0 | 33 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 0 | 74 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move forward (not zooming in) with respect to the initial frame? | 0 | 33 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera move only forward (not zooming in) with respect to the initial frame? | 0 | 74 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the camera move in a clockwise arc? | 0 | 72 | cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise |
| Is the camera craning downward in an arc? | 0 | 72 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the video include shot transitions? | 0 | 74 | cam_setup.has_shot_transition_cam_setup |
| Does the camera start above the subject and move down to a position below them? | 0 | 45 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the camera start below the subject and move up to their height? | 0 | 45 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the camera start below the subject and move up to a position above them? | 0 | 45 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera start at the subject's height and then move down to a lower position than them? | 0 | 45 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Does the camera transition from above water to underwater? | 0 | 54 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the camera transition from underwater to above water? | 0 | 54 | cam_setup.height_wrt_ground.underwater_to_above_water |
| Does the video start with a sharp focus on a subject or area and then become out of focus? | 0 | 19 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video start out of focus and then become in focus? | 0 | 19 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Is there focus tracking on a moving subject in the video? | 0 | 63 | cam_setup.focus.is_focus_tracking |
| Does the video start with the middle ground in focus and then shift to the foreground? | 0 | 19 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the video start with the foreground in focus and then transition to focusing on the background? | 0 | 19 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Does the video start with the middle ground in focus and then shift to the background? | 0 | 19 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the video start with the background in focus and then shift to the middle ground? | 0 | 19 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Is the video consistently focused on the background using a shallow depth of field? | 0 | 19 | cam_setup.focus.is_always.focus_is_background |
| Is the video consistently out of focus throughout? | 0 | 19 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Does the video end with the background in focus, using a shallow depth of field? | 0 | 19 | cam_setup.focus.end_with.focus_end_with_background |
| Does the video end completely out of focus? | 0 | 19 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Does the video start completely out of focus? | 0 | 19 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is this a stop-motion video where objects are moved frame by frame to create motion? | 0 | 74 | cam_setup.video_speed.stop_motion |
| Is this video played in reverse, with events unfolding backward in time? | 0 | 73 | cam_setup.video_speed.time_reversed |
| Does this shot speed up time significantly to show changes over minutes or hours? | 0 | 73 | cam_setup.video_speed.time_lapse |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective? | 0 | 74 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Is this a forward-facing view from a dash cam, capturing the road or surroundings? | 0 | 74 | cam_setup.point_of_view.dashcam_pov |
| Is the camera facing the person holding it? | 0 | 74 | cam_setup.point_of_view.selfie_pov |
| Is this a gaming video with a camera positioned directly above the character, showing a top-down or top-down oblique view? | 0 | 74 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Is the camera physically mounted on an object, keeping its perspective locked to that object? | 0 | 74 | cam_setup.point_of_view.locked_on_pov |
| Is the camera framing the character from the hip up? | 0 | 74 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the main subject change to another subject? | 0 | 59 | cam_setup.shot_size.subject_switching |
| Does the main subject disappear from the frame? | 0 | 59 | cam_setup.shot_size.subject_disappearing |
| Does the video start with a medium close-up shot that frames the human subject from the chest upward? | 0 | 55 | cam_setup.shot_size.start_with.shot_size_start_with_medium_close_up |
| Does the video start with a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 0 | 55 | cam_setup.shot_size.start_with.shot_size_start_with_medium_full |
| Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene? | 0 | 55 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up |
| Does the video maintain an extreme close-up shot throughout, focusing very tightly on specific details or features? | 0 | 59 | cam_setup.shot_size.is_always.shot_size_is_extreme_close_up |
| Does the video show a medium close-up shot that frames the human subject from the chest upward? | 0 | 59 | cam_setup.shot_size.is_always.shot_size_is_medium_close_up |
| Does the video show a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 0 | 59 | cam_setup.shot_size.is_always.shot_size_is_medium_full |
| Does the video end with a medium full shot that frames the human subject from the mid-thigh or knee upward? | 0 | 59 | cam_setup.shot_size.end_with.shot_size_end_with_medium_full |
| Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene? | 0 | 59 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up |
| Does the video start with the camera at a low angle and transition to a high angle? | 0 | 68 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video start with the camera at a high angle and transition to a low angle? | 0 | 68 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Does the video start with the camera at a low angle and transition to a level angle? | 0 | 68 | cam_setup.angle.from_to.camera_angle_from_low_to_level |
| Does the video feature a subject and scene that do not match, making it difficult to classify shot size? | 0 | 74 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the video feature a clear subject, but changes in framing make shot size classification tricky? | 0 | 74 | cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot |
| Does the video have a clear subject with back-and-forth changes in shot size? | 0 | 74 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the video include shot transitions? | 0 | 74 | lighting_setup.has_shot_transition_lighting_setup |
| Is the subject lit with high-key lighting? | 0 | 45 | lighting_setup.subject_lighting.light_contrast.high_key_lighting |
| Is there a noticeable light source illuminating the subject from below (bottom lighting) as seen from the camera’s perspective? | 0 | 0 | lighting_setup.subject_lighting.light_direction.direction_is_bottom_light |
| Does the lighting color in the video change abruptly and rapidly (a sudden color shift)? | 0 | 0 | lighting_setup.dynamic_light.color_shifting_sudden |
| Does the video feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat? | 0 | 0 | lighting_setup.natural_effect.heat_haze |
| Does the video feature an aurora, with flowing, colorful light patterns in the sky? | 0 | 0 | lighting_setup.natural_effect.aurora |
| Does the video capture a lightning effect with intense flashes and jagged, branching streaks? | 0 | 0 | lighting_setup.natural_effect.lightning |
| Does the video feature a noticeable rainbow? | 0 | 0 | lighting_setup.natural_effect.rainbow |
| Does the video feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects? | 0 | 0 | lighting_setup.natural_effect.aerial_perspective |
| Does the video feature a transformation or morphing effect where one object changes into another? | 0 | 0 | lighting_setup.dynamic_effect.transformation_morphing |
| Does the video feature a visible diffusion effect, where particles, fluids, or other materials spread and disperse over time? | 0 | 0 | lighting_setup.dynamic_effect.diffusion |
| Is the video lit by moonlight or starnight, with the moon or stars visible? | 0 | 0 | lighting_setup.light_source.has_moonlight_starlight |
| Does the video feature strong contrasts between highly saturated and desaturated hues? | 0 | 73 | lighting_setup.color_grading.saturation.color_saturation_is_contrasting |
| Is the video excessively bright and overexposed, making details hard to see? | 0 | 74 | lighting_setup.color_grading.brightness.brightness_is_very_bright |
| Does the video feature visible beams of light with well-defined edges, creating linear volumes of light? | 0 | 0 | lighting_setup.volumetric_lighting.volumetric_beam_light |
| Does the video feature concentrated, cone-shaped volumes of light? | 0 | 0 | lighting_setup.volumetric_lighting.volumetric_spot_light |
| Does the video feature shadows shaped by the subject, emphasizing form or movement? | 0 | 0 | lighting_setup.shadow_pattern.subject_shape |
| Does the video feature shadows cast by window frames? | 0 | 0 | lighting_setup.shadow_pattern.window_frames |
| Does the video contain distinct shadow patterns or gobo lighting effects that shape the visual composition? | 0 | 0 | lighting_setup.shadow_pattern.has_shadow_patterns |
| Does the video feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape? | 0 | 0 | lighting_setup.shadow_pattern.shadow_patterns_gobo_others |
| Does the video feature shadow patterns created by foliage, such as leaves or branches? | 0 | 0 | lighting_setup.shadow_pattern.foliage |
| Does the video feature distinct shadow patterns cast by venetian blinds? | 0 | 0 | lighting_setup.shadow_pattern.venetian_blinds |
| Does the video contain typical lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts? | 0 | 0 | lighting_setup.lens_effect.lens_flare_regular |
| Does the video contain obvious lens flares? | 0 | 0 | lighting_setup.lens_effect.lens_flares |
| Does the video contain anamorphic lens flares as bright, elongated streaks from light interacting with an anamorphic lens? | 0 | 0 | lighting_setup.lens_effect.lens_flares_anamorphic |
| Does the video feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings? | 0 | 0 | lighting_setup.special_effect.headlight_flashlight |
