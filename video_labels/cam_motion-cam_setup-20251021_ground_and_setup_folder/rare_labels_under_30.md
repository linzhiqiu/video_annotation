# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the camera only zoom out with no other movement? | 28 | 3842 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera only zoom in with no other movement? | 28 | 3842 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below? | 28 | 3207 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the camera only roll clockwise without any other camera movements? | 27 | 3843 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is the camera positioned directly above the subject for a top-down perspective? | 27 | 3662 | cam_setup.point_of_view.overhead_pov |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (about 1.5×–3×), but not a time-lapse where the speed is greatly accelerated over a long duration? | 27 | 3572 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Is it an arc tracking shot where the camera follows the moving subject while arcing around them? | 26 | 3661 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera only pan leftward without any other camera movements? | 26 | 3844 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the video start with the camera at a low angle and transition to a high angle? | 26 | 3209 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video start with the camera focused on the foreground and then shift the focus to the middleground? | 25 | 1057 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Is this a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead? | 25 | 3664 | cam_setup.point_of_view.dashcam_pov |
| Is the camera consistently focused on the background using a shallow depth of field? | 24 | 1068 | cam_setup.focus.is_always.focus_is_background |
| Does the camera only pan rightward without any other camera movements? | 23 | 3847 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera only roll counterclockwise without any other camera movements? | 23 | 3847 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the video show a broadcast-style viewpoint used in television production? | 23 | 3666 | cam_setup.point_of_view.broadcast_pov |
| Does the video have a clear subject with back-and-forth changes in shot size? | 23 | 3666 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the video start with the camera at a high angle and transition to a low angle? | 22 | 3213 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Does the camera move only physically upward (not tilting up) relative to the ground (even if it's a bird's or worm's eye view)? | 21 | 3849 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera move only physically downward (not tilting down) relative to the ground (even if it's a bird's or worm's eye view)? | 21 | 3849 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera only tilt downward without any other camera movements? | 21 | 3849 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the camera only move laterally leftward without any other camera movements? | 21 | 3849 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 19 | 3850 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the camera only move physically downward (not tilting down) with respect to the ground? | 19 | 3077 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Is this a screen recording of a software or system interface (e.g., menus, windows, toolbars)? | 19 | 3670 | cam_setup.point_of_view.screen_recording_pov |
| Does the camera only move physically upward (not tilting up) relative to the ground? | 18 | 3078 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the video end with the camera completely out of focus? | 18 | 1073 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Does the camera start in sharp focus and then shift out of focus? | 17 | 3672 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 17 | 1075 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the camera transition from underwater to above water? | 17 | 2640 | cam_setup.height_wrt_ground.underwater_to_above_water |
| Does the camera’s height relative to the subject start below and end above? | 17 | 2400 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 16 | 3853 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera only tilt upward without any other camera movements? | 16 | 3854 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the camera transition from above water to underwater? | 16 | 2641 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the camera’s height relative to the subject start below and end at the subject’s height? | 16 | 2401 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Is it a rear-side tracking shot where the camera follows the moving subject at a rear-side angle? | 15 | 3672 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Is it a front-side tracking shot where the camera leads the moving subject from a front-side angle? | 15 | 3672 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Does the camera use focus tracking to keep a subject in focus in the video? | 15 | 3079 | cam_setup.focus.is_focus_tracking |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing both the top and side planes of the environment in a three-quarters perspective, with minimal perspective distortion? | 15 | 3674 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 14 | 1045 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the video start with the camera focused on the foreground and then shift the focus to the background? | 14 | 1074 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Does the video contain a frame freezing effect at any point? | 12 | 3858 | cam_motion.has_frame_freezing |
| Does the camera’s height relative to the subject start at the subject’s height and end below? | 12 | 2405 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Is the camera craning downward in an arc relative to its own frame? | 11 | 3454 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the camera’s height relative to the subject start above and end below? | 9 | 2408 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 6 | 1086 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 5 | 1087 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Is this video played in reverse, with events playing backward in time? | 3 | 3370 | cam_setup.video_speed.time_reversed |
| Is the camera consistently out of focus throughout? | 1 | 1091 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Is the scene in the video dynamic and features movement? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Does the camera only move physically downward (or pedestals down) without any other camera movements? | 0 | 3870 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera move physically downward (or pedestals down) with respect to the initial frame? | 0 | 1418 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera move only physically backward (not zooming out) with respect to the initial frame, without any other movement? | 0 | 3870 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 1418 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only physically forward (not zooming in) with respect to the initial frame, without any other movement? | 0 | 3870 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the camera physically move forward (not zooming in) with respect to the initial frame? | 0 | 1418 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera only move physically upward (or pedestals up) without any other camera movements? | 0 | 3870 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move physically upward (or pedestals up) with respect to the initial frame? | 0 | 1418 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
