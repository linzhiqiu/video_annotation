# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is this a stop-motion video using frame-by-frame changes to simulate motion? | 29 | 2187 | cam_setup.video_speed.stop_motion |
| Does the video end with a medium full shot that frames the human subject from the mid-thigh or knee upward? | 29 | 1748 | cam_setup.shot_size.end_with.shot_size_end_with_medium_full |
| Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene? | 29 | 1748 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up |
| Does the camera only move backward (not zooming out) with respect to the ground? | 28 | 1867 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground |
| Is the camera positioned below the subject throughout the video? | 27 | 1428 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject |
| Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene? | 27 | 1731 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up |
| Is it a side-tracking shot where the camera moves left to follow the subject? | 25 | 2183 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the focal plane shift from distant to close, moving between foreground, middleground, or background? | 25 | 1531 | cam_setup.focus.focus_change_from_far_to_near |
| Does the focal plane shift from close to distant, moving between foreground, middleground, or background? | 25 | 1531 | cam_setup.focus.focus_change_from_near_to_far |
| Does the subject appear smaller during the tracking shot? | 24 | 2184 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Is the camera physically mounted on an object, keeping its perspective locked to that object? | 24 | 2192 | cam_setup.point_of_view.locked_on_pov |
| Does the video start with the camera at a low angle and transition to a level angle? | 24 | 1935 | cam_setup.angle.from_to.camera_angle_from_low_to_level |
| Is there a clear subject, but changes in framing make it hard to classify the shot size? | 24 | 2192 | cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot |
| Is the camera positioned directly above the subject for a top-down perspective? | 23 | 2193 | cam_setup.point_of_view.overhead_pov |
| Does the video maintain an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene? | 22 | 1776 | cam_setup.shot_size.is_always.shot_size_is_extreme_close_up |
| Does the video show the main subject disappearing or leaving the frame? | 21 | 1799 | cam_setup.shot_size.subject_disappearing |
| Does the video maintain a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward? | 21 | 1777 | cam_setup.shot_size.is_always.shot_size_is_medium_full |
| Does the video end with the camera fully submerged underwater? | 20 | 1677 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level |
| Is the camera consistently focused on the background using a shallow depth of field? | 20 | 703 | cam_setup.focus.is_always.focus_is_background |
| Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface? | 19 | 1678 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level |
| Does the video start with the camera fully submerged underwater? | 19 | 1678 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level |
| Does the camera only zoom in with no other movement? | 18 | 2312 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera only move leftward without any other camera movements? | 17 | 2313 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera only pan leftward without any other camera movements? | 16 | 2314 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Is this a professional viewpoint used in television broadcasts? | 16 | 2200 | cam_setup.point_of_view.broadcast_pov |
| Does the camera only zoom out with no other movement? | 15 | 2315 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera only pan rightward without any other camera movements? | 15 | 2315 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective? | 15 | 2201 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the video start with the camera focused on the foreground and then shift to the middle ground? | 14 | 703 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Does the camera tilt to track the subjects as they move? | 13 | 2182 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Is the camera craning upward in an arc? | 13 | 2077 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the video start completely out of focus? | 13 | 710 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is this a dashcam POV shot from a forward-facing, vehicle-mounted camera, capturing the scene ahead? | 13 | 2203 | cam_setup.point_of_view.dashcam_pov |
| Does the camera use focus tracking to follow a moving subject in the video? | 12 | 1837 | cam_setup.focus.is_focus_tracking |
| Does the video end with the camera completely out of focus? | 12 | 709 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Is this a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them? | 12 | 2204 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Does the camera follow the subject while moving in an arc? | 11 | 2197 | cam_motion.object_centric_movement.arc_tracking_shot |
| Is there a mismatch between the subject and scene framing that makes it hard to classify the shot size? | 11 | 2205 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the camera only tilt upward without any other camera movements? | 10 | 2320 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (1x–3x)? | 10 | 2153 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does this video capture a screen recording with visible UI elements? | 10 | 2206 | cam_setup.point_of_view.screen_recording_pov |
| Does the camera start below the subject and move up to their height? | 9 | 1446 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 9 | 694 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the video start with the camera at a worm’s eye angle, looking straight up from below? | 9 | 1950 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the video start with the camera at a high angle and transition to a low angle? | 9 | 1950 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Does the video have a clear subject with back-and-forth changes in shot size? | 9 | 2207 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 8 | 2322 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the video start with the camera at a low angle and transition to a high angle? | 8 | 1951 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video end with the camera at a worm's eye angle, looking straight up from below? | 8 | 1951 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below? | 8 | 1951 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the video contain a frame freeze effect at any point? | 7 | 2201 | cam_motion.has_frame_freezing |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 7 | 2200 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 7 | 2200 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 7 | 2323 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera start at the subject's height and then move down to a lower position than them? | 7 | 1448 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Does the video start with the camera focused on the foreground and then shift to the background? | 7 | 714 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Is the camera facing the person holding it, as in a selfie? | 6 | 2210 | cam_setup.point_of_view.selfie_pov |
| Is it a tracking shot with the camera leading the subject from a front-side angle? | 5 | 2203 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind the subject at a rear-side angle? | 5 | 2203 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera only move upward (not tilting up) with respect to the ground? | 5 | 1890 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the camera only tilt downward without any other camera movements? | 5 | 2325 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 5 | 718 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 5 | 718 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Does the camera only move downward (not tilting down) with respect to the ground? | 4 | 1891 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Is the camera craning downward in an arc? | 4 | 2086 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the camera start noticeably higher than the subject and then move down to a position below them? | 4 | 1451 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the camera start out of focus and then become in focus? | 4 | 2212 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Does the camera only roll counterclockwise without any other camera movements? | 3 | 2327 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera only roll clockwise without any other camera movements? | 3 | 2327 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is this video played in reverse, with events unfolding backward in time? | 3 | 2125 | cam_setup.video_speed.time_reversed |
| Does the camera start below the subject and move up to a position above them? | 2 | 1453 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera start in sharp focus and then shift out of focus? | 2 | 2214 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 2 | 721 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Is the camera consistently out of focus throughout? | 2 | 720 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Is the camera framing the character from the hip up? | 2 | 2214 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the camera transition from above water to underwater? | 1 | 1616 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Is the scene in the video dynamic? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Does the camera move downward (not tilting down) with respect to the initial frame? | 0 | 888 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 0 | 2330 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 888 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 0 | 2330 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move upward (not tilting up) with respect to the initial frame? | 0 | 888 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 0 | 2330 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move forward (not zooming in) with respect to the initial frame? | 0 | 888 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera move only forward (not zooming in) with respect to the initial frame? | 0 | 2330 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the camera transition from underwater to above water? | 0 | 1617 | cam_setup.height_wrt_ground.underwater_to_above_water |
