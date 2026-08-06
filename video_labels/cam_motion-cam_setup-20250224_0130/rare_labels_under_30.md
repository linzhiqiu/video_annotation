# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the video start with the camera positioned below the subject? | 29 | 985 | cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_below_subject |
| Does the main subject change to another subject? | 29 | 2068 | cam_setup.shot_size.subject_switching |
| Does the camera only move right in the scene? | 28 | 2356 | cam_motion.camera_centric_movement.rightward.only_rightward |
| Does the camera height decrease noticeably in relation to the subject? | 28 | 24 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_high_to_low |
| Does the subject look smaller during the tracking shot? | 27 | 2357 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Is this a 3D gaming video featuring a third-person perspective with the character’s full body visible? | 27 | 2357 | cam_setup.point_of_view.third_person_full_body_game_pov |
| Does the Dutch angle remain the same throughout the video? | 26 | 1378 | cam_setup.angle.is_dutch_angle_fixed |
| Does the video end with the camera positioned at a bird’s eye angle, looking directly downward at the ground? | 26 | 1378 | cam_setup.angle.end_with.camera_angle_end_with_bird_eye_angle |
| Is the camera positioned at a bird’s eye angle throughout the video, looking directly downward at the ground? | 26 | 1378 | cam_setup.angle.is_always.camera_angle_is_bird_eye_angle |
| Does the camera height increase noticeably in relation to the ground? | 25 | 22 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_low_to_high |
| Does the camera height increase noticeably in relation to the subject? | 24 | 28 | cam_setup.height_wrt_subject.height_wrt_subject_change_from_low_to_high |
| Does the camera start at the subject's height and then move up to a higher position than them? | 24 | 990 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject |
| Does the camera only pan from right to left? | 23 | 2361 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does this shot have a fisheye lens distortion? | 23 | 2361 | cam_setup.lens_distortion.fisheye_distortion |
| Does the video start with the camera at a low angle and transition to a level angle? | 23 | 1381 | cam_setup.angle.from_to.camera_angle_from_low_to_level |
| Is zooming in the only motion in this shot, without other camera movement? | 22 | 2362 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Is the camera positioned below the subject throughout the video? | 22 | 992 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject |
| Does the camera height decrease noticeably in relation to the ground? | 22 | 25 | cam_setup.height_wrt_ground.height_wrt_ground_change_from_high_to_low |
| Is it a side-tracking shot where the camera moves left to follow the subject? | 21 | 2363 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the video end with the background in focus, using a shallow depth of field? | 21 | 503 | cam_setup.focus.end_with.focus_end_with_background |
| Does the camera only pan from left to right? | 20 | 2364 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera start noticeably higher than the subject and then move down to their height? | 20 | 994 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject |
| Does the video start with the background in focus, using a shallow depth of field? | 20 | 505 | cam_setup.focus.start_with.focus_start_with_background |
| Is this a stop-motion video where objects are moved frame by frame to create motion? | 20 | 2361 | cam_setup.video_speed.stop_motion |
| Does the camera only move backward (not zooming out) with respect to the ground? | 19 | 1352 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground |
| Does the camera only move left in the scene? | 17 | 2367 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the focal plane transition from distant to close? | 17 | 1058 | cam_setup.focus.focus_change_from_far_to_near |
| Is this video played at a faster speed than real-time? | 17 | 2322 | cam_setup.video_speed.fast_motion |
| Is the camera positioned directly above the subject for a top-down perspective? | 17 | 2367 | cam_setup.point_of_view.overhead_pov |
| Does the main subject disappear from the frame? | 17 | 2080 | cam_setup.shot_size.subject_disappearing |
| Does the video start with a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 17 | 1225 | cam_setup.shot_size.start_with.shot_size_start_with_medium_full |
| Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene? | 17 | 1239 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up |
| Does the video end with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 16 | 1185 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level |
| Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface? | 15 | 1186 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level |
| Does the video start with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 15 | 1186 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level |
| Does the focal plane transition from close to distant? | 15 | 1060 | cam_setup.focus.focus_change_from_near_to_far |
| Is the video consistently focused on the background using a shallow depth of field? | 15 | 510 | cam_setup.focus.is_always.focus_is_background |
| Does the camera follow the subject while moving in an arc? | 14 | 2370 | cam_motion.object_centric_movement.arc_tracking_shot |
| Is zooming out the only motion in this shot, without other camera movement? | 14 | 2370 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene? | 14 | 1228 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up |
| Does the video feature a clear subject, but changes in framing make shot size classification tricky? | 14 | 2370 | cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot |
| Does the camera tilt to track the subjects? | 13 | 2358 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Is the camera performing a crane up movement? | 13 | 2256 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Is this a forward-facing view from a dash cam, capturing the road or surroundings? | 13 | 2371 | cam_setup.point_of_view.dashcam_pov |
| Does the video end with a medium full shot that frames the human subject from the mid-thigh or knee upward? | 13 | 1243 | cam_setup.shot_size.end_with.shot_size_end_with_medium_full |
| Does the video contain a frame freeze effect at any point? | 12 | 2372 | cam_motion.has_frame_freezing |
| Does the camera only tilt up in the scene? | 12 | 2372 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective? | 12 | 2372 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Is this a professional viewpoint used in television broadcasts? | 12 | 2372 | cam_setup.point_of_view.broadcast_pov |
| Does the video maintain an extreme close-up shot throughout, focusing very tightly on specific details or features? | 12 | 1261 | cam_setup.shot_size.is_always.shot_size_is_extreme_close_up |
| Does the video end completely out of focus? | 11 | 513 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 10 | 2374 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the video start with the foreground in focus and then transition to focusing on the middle ground? | 10 | 511 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Does the video start completely out of focus? | 10 | 515 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is this video played at a slightly faster speed than real-time (e.g., 1x-3x)? | 10 | 2329 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Is this a gaming video with a camera positioned directly above the character, showing a top-down or top-down oblique view? | 10 | 2374 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Does the video show a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 9 | 1264 | cam_setup.shot_size.is_always.shot_size_is_medium_full |
| Does the video feature a subject and scene that do not match, making it difficult to classify shot size? | 9 | 2375 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 8 | 2374 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 8 | 2375 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the video start with the middle ground in focus and then shift to the foreground? | 8 | 501 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does this video capture a screen recording with visible UI elements? | 8 | 2376 | cam_setup.point_of_view.screen_recording_pov |
| Does the video start with the camera at a high angle and transition to a low angle? | 8 | 1396 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Does the camera only tilt down in the scene? | 7 | 2377 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does this shot speed up time significantly to show changes over minutes or hours? | 7 | 2332 | cam_setup.video_speed.time_lapse |
| Is it a tracking shot with the camera leading from the front and to the side of the subject? | 6 | 2378 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind and to the side of the subject? | 6 | 2378 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 6 | 2378 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera start below the subject and move up to their height? | 6 | 1008 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Is the camera physically mounted on an object, keeping its perspective locked to that object? | 6 | 2378 | cam_setup.point_of_view.locked_on_pov |
| Does the camera start at the subject's height and then move down to a lower position than them? | 5 | 1009 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Is there focus tracking on a moving subject in the video? | 5 | 1301 | cam_setup.focus.is_focus_tracking |
| Does the camera start above the subject and move down to a position below them? | 4 | 1010 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start out of focus and then become in focus? | 4 | 517 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Does the video start with the foreground in focus and then transition to focusing on the background? | 4 | 519 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Is the camera framing the character from the hip up? | 4 | 2380 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the camera only move upward (not tilting up) with respect to the ground? | 3 | 1368 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Is the camera performing a crane down movement? | 3 | 2266 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the video start with the background in focus and then shift to the middle ground? | 3 | 522 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Is this video played in reverse, with events unfolding backward in time? | 3 | 2332 | cam_setup.video_speed.time_reversed |
| Does the video start with the camera at a low angle and transition to a high angle? | 3 | 1401 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video have a clear subject with back-and-forth changes in shot size? | 3 | 2381 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the camera only move downward (not tilting down) with respect to the ground? | 2 | 1369 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Does the camera only roll counterclockwise in the scene? | 2 | 2382 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera only roll clockwise in the scene? | 2 | 2382 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Does the video start with a sharp focus on a subject or area and then become out of focus? | 2 | 515 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video start with the background in focus and then shift to the foreground? | 2 | 523 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Is the video consistently out of focus throughout? | 2 | 523 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Is the camera facing the person holding it? | 2 | 2382 | cam_setup.point_of_view.selfie_pov |
| Does the video start with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 2 | 1402 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the video end with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 2 | 1402 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Is the camera positioned at a worm’s eye angle throughout the video, looking sharply upward to the sky? | 2 | 1402 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the camera start below the subject and move up to a position above them? | 1 | 1013 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera transition from above water to underwater? | 1 | 1146 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the video start with the middle ground in focus and then shift to the background? | 1 | 524 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the video include shot transitions? | 0 | 2384 | cam_motion.has_shot_transition_cam_motion |
| Is the scene in the video dynamic? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Does the camera move downward (not tilting down) with respect to the initial frame? | 0 | 950 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 0 | 2384 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 950 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 0 | 2384 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move upward (not tilting up) with respect to the initial frame? | 0 | 950 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 0 | 2384 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move forward (not zooming in) with respect to the initial frame? | 0 | 950 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera move only forward (not zooming in) with respect to the initial frame? | 0 | 2384 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the video include shot transitions? | 0 | 2384 | cam_setup.has_shot_transition_cam_setup |
| Does the camera transition from underwater to above water? | 0 | 1147 | cam_setup.height_wrt_ground.underwater_to_above_water |
