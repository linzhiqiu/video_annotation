# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is there a mismatch between the subject and scene framing that makes it hard to classify the shot size? | 29 | 3276 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the camera only zoom out with no other movement? | 27 | 3454 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera only zoom in with no other movement? | 27 | 3454 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Is the camera positioned directly above the subject for a top-down perspective? | 27 | 3278 | cam_setup.point_of_view.overhead_pov |
| Does the camera only pan leftward without any other camera movements? | 26 | 3455 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Is it an arc tracking shot where the camera follows the moving subject while arcing around them? | 24 | 3279 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera only pan rightward without any other camera movements? | 23 | 3458 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the video show a broadcast-style viewpoint used in television production? | 23 | 3282 | cam_setup.point_of_view.broadcast_pov |
| Does the video start with the camera focused on the foreground and then shift the focus to the middleground? | 22 | 933 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Does the video end with the camera at a worm's eye angle, looking straight up from below? | 22 | 2906 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Does the camera only move laterally leftward without any other camera movements? | 21 | 3460 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Is the camera consistently focused on the background using a shallow depth of field? | 21 | 942 | cam_setup.focus.is_always.focus_is_background |
| Does the video start with the camera at a worm’s eye angle, looking straight up from below? | 20 | 2908 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the camera tilt to track the moving subjects? | 17 | 3261 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the camera start out of focus and then become in focus? | 16 | 3289 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Does the video start with the camera completely out of focus? | 16 | 947 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (about 1.5×–3×), but not a time-lapse where the speed is greatly accelerated over a long duration? | 16 | 3214 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does the video start with the camera at a low angle and transition to a high angle? | 15 | 2913 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video start with the camera at a high angle and transition to a low angle? | 15 | 2913 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Is this a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead? | 15 | 3290 | cam_setup.point_of_view.dashcam_pov |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing both the top and side planes of the environment in a three-quarters perspective, with minimal perspective distortion? | 15 | 3290 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the camera’s height relative to the subject start below and end at the subject’s height? | 15 | 2140 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the camera use focus tracking to keep a subject in focus in the video? | 14 | 2777 | cam_setup.focus.is_focus_tracking |
| Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below? | 14 | 2914 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the camera start in sharp focus and then shift out of focus? | 13 | 3292 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video end with the camera completely out of focus? | 13 | 949 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Is this a screen recording of a software or system interface (e.g., menus, windows, toolbars)? | 13 | 3292 | cam_setup.point_of_view.screen_recording_pov |
| Does the camera only tilt downward without any other camera movements? | 12 | 3469 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the video have a clear subject with back-and-forth changes in shot size? | 12 | 3293 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the video contain a frame freeze effect at any point? | 11 | 3470 | cam_motion.has_frame_freezing |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 11 | 3469 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Is this a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and environment, looking downward to show mostly the tops of objects with limited sides? | 11 | 3294 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Does the camera’s height relative to the subject start at the subject’s height and end below? | 11 | 2144 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Is the camera craning downward in an arc relative to its own frame? | 10 | 3079 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the camera move only physically upward (not tilting up) relative to the ground (even if it's a bird's or worm's eye view)? | 10 | 3471 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera only tilt upward without any other camera movements? | 10 | 3471 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 10 | 953 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 10 | 923 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 9 | 3471 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Is it a rear-side tracking shot where the camera follows the moving subject at a rear-side angle? | 9 | 3294 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Is it a front-side tracking shot where the camera leads the moving subject from a front-side angle? | 9 | 3294 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Does the camera move only physically downward (not tilting down) relative to the ground (even if it's a bird's or worm's eye view)? | 9 | 3472 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the video start with the camera focused on the foreground and then shift the focus to the background? | 9 | 950 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Does the camera only move physically downward (not tilting down) with respect to the ground? | 8 | 2819 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Does the camera only move physically upward (not tilting up) relative to the ground? | 7 | 2820 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 5 | 958 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Does the camera’s height relative to the subject start above and end below? | 5 | 2150 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 4 | 959 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Is this an over-the-hip third-person view, framing the character from the hip up? | 4 | 3301 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the camera only roll counterclockwise without any other camera movements? | 3 | 3478 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera only roll clockwise without any other camera movements? | 3 | 3478 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is this video played in reverse, with events playing backward in time? | 3 | 3006 | cam_setup.video_speed.time_reversed |
| Does the camera’s height relative to the subject start below and end above? | 3 | 2152 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera transition from above water to underwater? | 1 | 2373 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Is the scene in the video dynamic and features movement? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Does the camera only move physically downward (or pedestals down) without any other camera movements? | 0 | 3481 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera move physically downward (or pedestals down) with respect to the initial frame? | 0 | 1241 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera move only physically backward (not zooming out) with respect to the initial frame, without any other movement? | 0 | 3481 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 1241 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only physically forward (not zooming in) with respect to the initial frame, without any other movement? | 0 | 3481 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the camera physically move forward (not zooming in) with respect to the initial frame? | 0 | 1241 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera only move physically upward (or pedestals up) without any other camera movements? | 0 | 3481 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move physically upward (or pedestals up) with respect to the initial frame? | 0 | 1241 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
| Is the camera consistently out of focus throughout? | 0 | 963 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Does the camera transition from underwater to above water? | 0 | 2374 | cam_setup.height_wrt_ground.underwater_to_above_water |
