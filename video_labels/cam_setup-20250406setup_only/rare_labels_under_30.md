# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the camera use focus tracking to follow a moving subject in the video? | 27 | 2835 | cam_setup.focus.is_focus_tracking |
| Does the video start completely out of focus? | 26 | 1128 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is the camera positioned directly above the subject for a top-down perspective? | 26 | 3445 | cam_setup.point_of_view.overhead_pov |
| Is the camera consistently focused on the background using a shallow depth of field? | 25 | 1129 | cam_setup.focus.is_always.focus_is_background |
| Is this a professional viewpoint used in television broadcasts? | 22 | 3449 | cam_setup.point_of_view.broadcast_pov |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective? | 20 | 3451 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the video end with the camera completely out of focus? | 17 | 1133 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Does the video start with the camera focused on the middle ground and then shift the focus to the foreground? | 16 | 1103 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does the camera start below the subject and move up to their height? | 15 | 2327 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the video start with the camera at a worm’s eye angle, looking straight up from below? | 15 | 3062 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the video start with the camera at a high angle and transition to a low angle? | 15 | 3062 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Is there a mismatch between the subject and scene framing that makes it hard to classify the shot size? | 15 | 3456 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Does the camera start at the subject's height and then move down to a lower position than them? | 14 | 2328 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Does the video start with the camera focused on the foreground and then shift to the background? | 14 | 1136 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Does this video capture a screen recording with visible UI elements? | 14 | 3457 | cam_setup.point_of_view.screen_recording_pov |
| Is this a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them? | 14 | 3457 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Is this a dashcam POV shot from a forward-facing, vehicle-mounted camera, capturing the scene ahead? | 13 | 3458 | cam_setup.point_of_view.dashcam_pov |
| Is it a fast-motion video with forward playback speed slightly faster than real-time (1x–3x)? | 12 | 3389 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does the video start with the camera at a low angle and transition to a high angle? | 12 | 3065 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video have a clear subject with back-and-forth changes in shot size? | 12 | 3459 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the video end with the camera at a worm's eye angle, looking straight up from below? | 11 | 3066 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below? | 11 | 3066 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the camera start out of focus and then become in focus? | 9 | 3462 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Is the camera facing the person holding it, as in a selfie? | 9 | 3462 | cam_setup.point_of_view.selfie_pov |
| Does the video start with the camera focused on the background and then shift the focus to the foreground? | 6 | 1148 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the camera start noticeably higher than the subject and then move down to a position below them? | 5 | 2337 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start with the camera focused on the background and then shift the focus to the middleground? | 5 | 1149 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Is this video played in reverse, with events unfolding backward in time? | 5 | 3356 | cam_setup.video_speed.time_reversed |
| Does the video start with the camera focused on the middle ground and then shift the focus to the background? | 4 | 1150 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the camera start below the subject and move up to a position above them? | 3 | 2339 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera transition from above water to underwater? | 2 | 2539 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the camera start in sharp focus and then shift out of focus? | 2 | 3469 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Is the camera consistently out of focus throughout? | 2 | 1150 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Is the camera framing the character from the hip up? | 2 | 3469 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the camera transition from underwater to above water? | 0 | 2541 | cam_setup.height_wrt_ground.underwater_to_above_water |
