# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the camera move in a clockwise arc? | 28 | 1732 | cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise |
| Does the degree of the Dutch (canted) angle stay the same throughout the video? | 28 | 1535 | cam_setup.angle.is_dutch_angle_fixed |
| Does the subject start below and end at or above the camera’s height, or start level and end above? | 28 | 25 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_low_to_high |
| Does the camera height decrease noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground? | 27 | 24 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_high_to_low |
| Does the camera roll clockwise? | 26 | 765 | cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise |
| Is it a stop-motion video using frame-by-frame changes to simulate motion? | 26 | 1745 | cam_setup.video_speed.stop_motion |
| Does the subject start above and end at or below the camera’s height, or start level and end below? | 25 | 28 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_high_to_low |
| Is the camera positioned below the subject throughout the video? | 25 | 1126 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject |
| Does the video start with the camera focusing on the background, using a shallow depth of field? | 24 | 552 | cam_setup.focus.start_with.focus_start_with_background |
| Does the camera height increase noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground? | 24 | 27 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_low_to_high |
| Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene? | 24 | 1404 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up |
| Is it a follow tracking shot where the camera moves behind the subject, traveling in the same direction as they move away from the camera? | 23 | 1737 | cam_motion.object_centric_movement.tail_tracking_shot |
| Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view? | 23 | 1748 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground_birds_worms_included |
| Does the camera’s height relative to the subject start at the subject’s height and end above? | 23 | 1128 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject |
| Does the camera move only physically backward (not zooming out) with respect to the initial frame, without any other movement? | 22 | 1749 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the video end with the camera focusing on the background, using a shallow depth of field? | 22 | 553 | cam_setup.focus.end_with.focus_end_with_background |
| Does the camera only move physically backward (not zooming out) with respect to the ground? | 21 | 1503 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground |
| Does the video start with the camera at a low angle and transition to a level angle? | 21 | 1542 | cam_setup.angle.from_to.camera_angle_from_low_to_level |
| Is the camera positioned directly above the subject for a top-down perspective? | 21 | 1750 | cam_setup.point_of_view.overhead_pov |
| Does the video start with a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 21 | 1390 | cam_setup.shot_size.start_with.shot_size_start_with_medium_full |
| Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene? | 21 | 1390 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up |
| Does the camera’s height relative to the subject start above and end at the subject’s height? | 21 | 1130 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject |
| Does the camera only move laterally rightward with no other movement? | 20 | 1751 | cam_motion.camera_centric_movement.rightward.only_rightward |
| Does the focal plane shift from distant to close, moving between foreground, middleground, or background? | 19 | 1187 | cam_setup.focus.focus_change_from_far_to_near |
| Does the video maintain an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene? | 19 | 1427 | cam_setup.shot_size.is_always.shot_size_is_extreme_close_up |
| Does the video show the main subject disappearing or leaving the frame? | 18 | 1444 | cam_setup.shot_size.subject_disappearing |
| Is it a fast-motion video with forward playback moderately faster than real-time (about 1.5×–3×)? | 18 | 1711 | cam_setup.video_speed.fast_motion |
| Does the video end with the camera fully submerged underwater? | 17 | 1333 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level |
| Is it a side tracking shot where the camera moves left to follow the subject? | 16 | 1755 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the camera only move laterally leftward without any other camera movements? | 16 | 1755 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Is the camera consistently focused on the background using a shallow depth of field? | 16 | 560 | cam_setup.focus.is_always.focus_is_background |
| Does the video start with the camera fully submerged underwater? | 16 | 1334 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level |
| Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface? | 16 | 1334 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level |
| Is there a clear subject, but the framing is unstable, making the exact shot size difficult to classify? | 16 | 1755 | cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot |
| Does the camera only zoom in with no other movement? | 15 | 1756 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera only pan rightward without any other camera movements? | 15 | 1756 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the focal plane shift from close to distant, moving between foreground, middleground, or background? | 15 | 1191 | cam_setup.focus.focus_change_from_near_to_far |
| Does the video end with a medium full shot that frames the human subject from the mid-thigh (or knee) upward? | 15 | 1413 | cam_setup.shot_size.end_with.shot_size_end_with_medium_full |
| Does the camera only pan leftward without any other camera movements? | 14 | 1757 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the video show a broadcast-style viewpoint used in television production? | 14 | 1757 | cam_setup.point_of_view.broadcast_pov |
| Does the video start with the camera completely out of focus? | 13 | 563 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is this a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead? | 13 | 1758 | cam_setup.point_of_view.dashcam_pov |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing both the top and side planes of the environment in a three-quarters perspective, with minimal perspective distortion? | 13 | 1758 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the camera tilt to track the moving subjects? | 12 | 1747 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the subject appear smaller during the tracking shot? | 12 | 1759 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Does the video end with the camera completely out of focus? | 12 | 563 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Is this a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and environment, looking downward to show mostly the tops of objects with limited sides? | 12 | 1759 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Is it an arc tracking shot where the camera follows the moving subject while arcing around them? | 11 | 1760 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera only zoom out with no other movement? | 10 | 1761 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera start out of focus and then become in focus? | 10 | 1761 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Does the camera start in sharp focus and then shift out of focus? | 10 | 1761 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Is this a screen recording of a software or system interface (e.g., menus, windows, toolbars)? | 10 | 1761 | cam_setup.point_of_view.screen_recording_pov |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (about 1.5×–3×), but not a time-lapse where the speed is greatly accelerated over a long duration? | 10 | 1719 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Is the camera craning upward in an arc relative to its own frame? | 9 | 1697 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the video start with the camera focused on the foreground and then shift the focus to the middleground? | 9 | 563 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Is the camera physically mounted on an object, keeping its perspective locked to that object? | 9 | 1762 | cam_setup.point_of_view.locked_on_pov |
| Does the video maintain a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward? | 9 | 1437 | cam_setup.shot_size.is_always.shot_size_is_medium_full |
| Is there a mismatch between the subject and scene framing that makes it hard to classify the shot size? | 9 | 1762 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 8 | 552 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the video start with the camera at a high angle and transition to a low angle? | 8 | 1555 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Is this a time-lapse video played forward at greatly accelerated speed (more than 3× real-time), showing time passing rapidly over a long period? | 8 | 1721 | cam_setup.video_speed.time_lapse |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 7 | 1764 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera use focus tracking to keep a subject in focus in the video? | 7 | 1450 | cam_setup.focus.is_focus_tracking |
| Does the video contain a frame freeze effect at any point? | 6 | 1765 | cam_motion.has_frame_freezing |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 6 | 1765 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the camera only tilt upward without any other camera movements? | 6 | 1765 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the camera’s height relative to the subject start at the subject’s height and end below? | 6 | 1145 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Does the camera’s height relative to the subject start below and end at the subject’s height? | 6 | 1145 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Is it a front-side tracking shot where the camera leads the moving subject from a front-side angle? | 5 | 1766 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Does the camera only tilt downward without any other camera movements? | 5 | 1766 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the video start with the camera at a low angle and transition to a high angle? | 5 | 1558 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the camera move only physically upward (not tilting up) relative to the ground (even if it's a bird's or worm's eye view)? | 4 | 1767 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera only move physically downward (not tilting down) with respect to the ground? | 4 | 1520 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Does the camera move only physically downward (not tilting down) relative to the ground (even if it's a bird's or worm's eye view)? | 4 | 1767 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera only move physically upward (or pedestals up) without any other camera movements? | 4 | 1767 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 4 | 572 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 4 | 572 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Does the video start with the camera focused on the foreground and then shift the focus to the background? | 4 | 571 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Is this an over-the-hip third-person view, framing the character from the hip up? | 4 | 1767 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the video have a clear subject with back-and-forth changes in shot size? | 4 | 1767 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the camera’s height relative to the subject start above and end below? | 4 | 1147 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Is it a rear-side tracking shot where the camera follows the moving subject at a rear-side angle? | 3 | 1768 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera only move physically upward (not tilting up) relative to the ground? | 3 | 1521 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the video start with the camera at a worm’s eye angle, looking straight up from below? | 3 | 1560 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Is this video played in reverse, with events playing backward in time? | 3 | 1718 | cam_setup.video_speed.time_reversed |
| Is the camera craning downward in an arc relative to its own frame? | 2 | 1704 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the camera only roll clockwise without any other camera movements? | 2 | 1769 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is the camera consistently out of focus throughout? | 2 | 573 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below? | 2 | 1561 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the video end with the camera at a worm's eye angle, looking straight up from below? | 2 | 1561 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Is it a selfie POV shot where the camera is held by the person being filmed (e.g., by hand, selfie stick, or invisible selfie rod) and faces them? | 2 | 1769 | cam_setup.point_of_view.selfie_pov |
| Does the camera only move physically downward (or pedestals down) without any other camera movements? | 1 | 1770 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera only roll counterclockwise without any other camera movements? | 1 | 1770 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 1 | 575 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the camera transition from above water to underwater? | 1 | 1290 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the camera’s height relative to the subject start below and end above? | 1 | 1150 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the video include a shot transition? | 0 | 1771 | cam_motion.has_shot_transition_cam_motion |
| Does the video include a shot transition? | 0 | 0 | cam_setup.has_shot_transition_cam_setup |
| Does the camera transition from underwater to above water? | 0 | 1291 | cam_setup.height_wrt_ground.underwater_to_above_water |
