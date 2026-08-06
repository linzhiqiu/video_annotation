# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is the camera consistently focused on the background using a shallow depth of field? | 29 | 1368 | cam_setup.focus.is_always.focus_is_background |
| Does the video start with the camera at a low angle and transition to a high angle? | 29 | 4006 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (about 1.5×–3×), but not a time-lapse where the speed is greatly accelerated over a long duration? | 28 | 4455 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does the video show a broadcast-style viewpoint used in television production? | 26 | 4562 | cam_setup.point_of_view.broadcast_pov |
| Does the camera use focus tracking to keep a subject in focus in the video? | 25 | 3796 | cam_setup.focus.is_focus_tracking |
| Does the video start with the camera at a high angle and transition to a low angle? | 25 | 4010 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Is this a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead? | 25 | 4563 | cam_setup.point_of_view.dashcam_pov |
| Does the video have a clear subject with back-and-forth changes in shot size? | 24 | 4564 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the video end with the camera completely out of focus? | 21 | 1373 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Does the camera start in sharp focus and then shift out of focus? | 20 | 4568 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 20 | 1338 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Is this a screen recording of a software or system interface (e.g., menus, windows, toolbars)? | 20 | 4568 | cam_setup.point_of_view.screen_recording_pov |
| Does the camera’s height relative to the subject start below and end at the subject’s height? | 20 | 3027 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the video start with the camera focused on the foreground and then shift the focus to the background? | 19 | 1372 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing both the top and side planes of the environment in a three-quarters perspective, with minimal perspective distortion? | 18 | 4570 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the camera’s height relative to the subject start at the subject’s height and end below? | 18 | 3029 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Does the camera’s height relative to the subject start below and end above? | 18 | 3029 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 17 | 1380 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the camera transition from above water to underwater? | 17 | 3306 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the camera transition from underwater to above water? | 17 | 3306 | cam_setup.height_wrt_ground.underwater_to_above_water |
| Does the camera’s height relative to the subject start above and end below? | 9 | 3038 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 7 | 1390 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 6 | 1391 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Is this video played in reverse, with events playing backward in time? | 4 | 4239 | cam_setup.video_speed.time_reversed |
| Is the camera consistently out of focus throughout? | 1 | 1395 | cam_setup.focus.is_always.focus_is_out_of_focus |
