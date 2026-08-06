# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is it a tracking shot with the camera following behind the subject? | 29 | 1884 | cam_motion.object_centric_movement.tail_tracking_shot |
| Does the camera roll clockwise in the scene? | 28 | 811 | cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise |
| Does the camera move in a clockwise arc? | 28 | 1886 | cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise |
| Does the camera start at the subject's height and then move up to a higher position than them? | 28 | 1228 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject |
| Does the camera start noticeably higher than the subject and then move down to their height? | 27 | 1229 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject |
| Is the camera positioned below the subject throughout the video? | 26 | 1230 | cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject |
| Is this a stop-motion video where objects are moved frame by frame to create motion? | 26 | 1897 | cam_setup.video_speed.stop_motion |
| Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view? | 25 | 1901 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground_birds_worms_included |
| Does the camera only move right in the scene? | 25 | 1901 | cam_motion.camera_centric_movement.rightward.only_rightward |
| Does the video start with the background in focus, using a shallow depth of field? | 25 | 605 | cam_setup.focus.start_with.focus_start_with_background |
| Does the video end with the background in focus, using a shallow depth of field? | 24 | 604 | cam_setup.focus.end_with.focus_end_with_background |
| Does the video start with a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 24 | 1509 | cam_setup.shot_size.start_with.shot_size_start_with_medium_full |
| Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene? | 24 | 1529 | cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up |
| Does the camera only move backward (not zooming out) with respect to the ground? | 23 | 1643 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 22 | 1904 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the video start with the camera at a low angle and transition to a level angle? | 22 | 1689 | cam_setup.angle.from_to.camera_angle_from_low_to_level |
| Is it a side-tracking shot where the camera moves left to follow the subject? | 21 | 1905 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Is the camera positioned directly above the subject for a top-down perspective? | 21 | 1905 | cam_setup.point_of_view.overhead_pov |
| Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene? | 21 | 1512 | cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up |
| Does the subject look smaller during the tracking shot? | 20 | 1906 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Does the focal plane transition from distant to close? | 20 | 1301 | cam_setup.focus.focus_change_from_far_to_near |
| Does the focal plane transition from close to distant? | 19 | 1302 | cam_setup.focus.focus_change_from_near_to_far |
| Is this video played at a faster speed than real-time? | 19 | 1858 | cam_setup.video_speed.fast_motion |
| Does the main subject disappear from the frame? | 19 | 1571 | cam_setup.shot_size.subject_disappearing |
| Does the video maintain an extreme close-up shot throughout, focusing very tightly on specific details or features? | 19 | 1553 | cam_setup.shot_size.is_always.shot_size_is_extreme_close_up |
| Does the video end with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 18 | 1458 | cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level |
| Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface? | 17 | 1459 | cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level |
| Does the video start with the camera fully submerged underwater, capturing scenes beneath the water’s surface? | 17 | 1459 | cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level |
| Is the video consistently focused on the background using a shallow depth of field? | 17 | 613 | cam_setup.focus.is_always.focus_is_background |
| Does the video end with a medium full shot that frames the human subject from the mid-thigh or knee upward? | 17 | 1536 | cam_setup.shot_size.end_with.shot_size_end_with_medium_full |
| Does the video feature a clear subject, but changes in framing make shot size classification tricky? | 17 | 1909 | cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot |
| Does the camera only move left in the scene? | 16 | 1910 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Is zooming in the only motion in this shot, without other camera movement? | 15 | 1911 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera only pan from left to right? | 15 | 1911 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera only pan from right to left? | 14 | 1912 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Is this a professional viewpoint used in television broadcasts? | 14 | 1912 | cam_setup.point_of_view.broadcast_pov |
| Is this a forward-facing view from a dash cam, capturing the road or surroundings? | 14 | 1912 | cam_setup.point_of_view.dashcam_pov |
| Does the video start completely out of focus? | 13 | 617 | cam_setup.focus.start_with.focus_start_with_out_of_focus |
| Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective? | 13 | 1913 | cam_setup.point_of_view.third_person_isometric_game_pov |
| Does the camera follow the subject while moving in an arc? | 12 | 1914 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera tilt to track the subjects? | 12 | 1902 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the video start with the foreground in focus and then transition to focusing on the middle ground? | 12 | 613 | cam_setup.focus.from_to.focus_from_foreground_to_middle_ground |
| Does the video end completely out of focus? | 12 | 616 | cam_setup.focus.end_with.focus_end_with_out_of_focus |
| Is this a gaming video with a camera positioned directly above the character, showing a top-down or top-down oblique view? | 12 | 1914 | cam_setup.point_of_view.third_person_top_down_game_pov |
| Is zooming out the only motion in this shot, without other camera movement? | 11 | 1915 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Is this video played at a slightly faster speed than real-time (e.g., 1x-3x)? | 11 | 1866 | cam_setup.video_speed.fast_motion_without_time_lapse |
| Does the video show a medium-full shot that frames the human subject from mid-thigh (or knee) upward? | 11 | 1561 | cam_setup.shot_size.is_always.shot_size_is_medium_full |
| Does the video feature a subject and scene that do not match, making it difficult to classify shot size? | 11 | 1915 | cam_setup.shot_type.is_just_subject_scene_mismatch_shot |
| Is the camera performing a crane up movement? | 10 | 1848 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does this video capture a screen recording with visible UI elements? | 10 | 1916 | cam_setup.point_of_view.screen_recording_pov |
| Does the camera only tilt up in the scene? | 9 | 1917 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Is the camera physically mounted on an object, keeping its perspective locked to that object? | 9 | 1917 | cam_setup.point_of_view.locked_on_pov |
| Does the video start with the camera at a high angle and transition to a low angle? | 9 | 1702 | cam_setup.angle.from_to.camera_angle_from_high_to_low |
| Is there focus tracking on a moving subject in the video? | 8 | 1584 | cam_setup.focus.is_focus_tracking |
| Does the video start with the middle ground in focus and then shift to the foreground? | 8 | 603 | cam_setup.focus.from_to.focus_from_middle_ground_to_foreground |
| Does this shot speed up time significantly to show changes over minutes or hours? | 8 | 1869 | cam_setup.video_speed.time_lapse |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 7 | 1918 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 7 | 1918 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 7 | 1919 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 7 | 1919 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera start below the subject and move up to their height? | 7 | 1249 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject |
| Does the camera start at the subject's height and then move down to a lower position than them? | 6 | 1250 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject |
| Is it a tracking shot with the camera leading from the front and to the side of the subject? | 5 | 1921 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind and to the side of the subject? | 5 | 1921 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 5 | 1921 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera only tilt down in the scene? | 5 | 1921 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the video start with the foreground in focus and then transition to focusing on the background? | 5 | 623 | cam_setup.focus.from_to.focus_from_foreground_to_background |
| Does the video start with the camera at a low angle and transition to a high angle? | 5 | 1706 | cam_setup.angle.from_to.camera_angle_from_low_to_high |
| Does the video contain a frame freeze effect at any point? | 4 | 1922 | cam_motion.has_frame_freezing |
| Does the camera only move upward (not tilting up) with respect to the ground? | 4 | 1662 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground |
| Does the camera start above the subject and move down to a position below them? | 4 | 1252 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject |
| Does the video start out of focus and then become in focus? | 4 | 619 | cam_setup.focus.focus_change_from_out_to_in_focus |
| Does the video start with the background in focus and then shift to the foreground? | 4 | 626 | cam_setup.focus.from_to.focus_from_background_to_foreground |
| Does the video start with the background in focus and then shift to the middle ground? | 4 | 626 | cam_setup.focus.from_to.focus_from_background_to_middle_ground |
| Is the camera framing the character from the hip up? | 4 | 1922 | cam_setup.point_of_view.third_person_over_hip_pov |
| Does the video start with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 4 | 1707 | cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle |
| Does the video have a clear subject with back-and-forth changes in shot size? | 4 | 1922 | cam_setup.shot_type.is_just_back_and_forth_change_shot |
| Does the camera only move downward (not tilting down) with respect to the ground? | 3 | 1663 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground |
| Is this video played in reverse, with events unfolding backward in time? | 3 | 1869 | cam_setup.video_speed.time_reversed |
| Does the video end with the camera positioned at a worm’s eye angle, looking sharply upward to the sky? | 3 | 1708 | cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle |
| Is the camera positioned at a worm’s eye angle throughout the video, looking sharply upward to the sky? | 3 | 1708 | cam_setup.angle.is_always.camera_angle_is_worm_eye_angle |
| Does the camera only roll counterclockwise in the scene? | 2 | 1924 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 2 | 1924 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera only roll clockwise in the scene? | 2 | 1924 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is the camera performing a crane down movement? | 2 | 1856 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the video start with a sharp focus on a subject or area and then become out of focus? | 2 | 619 | cam_setup.focus.focus_change_from_in_to_out_of_focus |
| Is the video consistently out of focus throughout? | 2 | 627 | cam_setup.focus.is_always.focus_is_out_of_focus |
| Is the camera facing the person holding it? | 2 | 1924 | cam_setup.point_of_view.selfie_pov |
| Does the camera start below the subject and move up to a position above them? | 1 | 1255 | cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject |
| Does the camera transition from above water to underwater? | 1 | 1407 | cam_setup.height_wrt_ground.above_water_to_underwater |
| Does the video start with the middle ground in focus and then shift to the background? | 1 | 629 | cam_setup.focus.from_to.focus_from_middle_ground_to_background |
| Does the video include shot transitions? | 0 | 1926 | cam_motion.has_shot_transition_cam_motion |
| Does the video include shot transitions? | 0 | 1926 | cam_setup.has_shot_transition_cam_setup |
| Does the camera transition from underwater to above water? | 0 | 1408 | cam_setup.height_wrt_ground.underwater_to_above_water |
