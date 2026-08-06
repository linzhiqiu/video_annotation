# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the camera only zoom in with no other movement? | 28 | 2655 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view? | 27 | 2656 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground_birds_worms_included |
| Does the camera move only physically backward (not zooming out) with respect to the initial frame, without any other movement? | 27 | 2656 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Is it an arc tracking shot where the camera follows the moving subject while arcing around them? | 24 | 2659 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the subject appear smaller during the tracking shot? | 24 | 2659 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Is it a side tracking shot where the camera moves left to follow the subject? | 23 | 2660 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the camera only pan leftward without any other camera movements? | 22 | 2661 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the camera move only physically downward (not tilting down) relative to the ground (even if it's a bird's or worm's eye view)? | 21 | 2662 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera only pan rightward without any other camera movements? | 21 | 2662 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera only move laterally leftward without any other camera movements? | 21 | 2662 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera tilt to track the moving subjects? | 18 | 2650 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the camera only tilt downward without any other camera movements? | 16 | 2667 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Is the camera craning upward in an arc relative to its own frame? | 15 | 2434 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the camera only move physically downward (or pedestals down) without any other camera movements? | 15 | 2668 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the video contain a frame freeze effect at any point? | 12 | 2671 | cam_motion.has_frame_freezing |
| Is the camera craning downward in an arc relative to its own frame? | 8 | 2441 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the camera only tilt upward without any other camera movements? | 8 | 2675 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 7 | 2676 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 7 | 2676 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Is it a front-side tracking shot where the camera leads the moving subject from a front-side angle? | 6 | 2677 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Does the camera only move physically upward (or pedestals up) without any other camera movements? | 6 | 2677 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move only physically upward (not tilting up) relative to the ground (even if it's a bird's or worm's eye view)? | 5 | 2678 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Is it a rear-side tracking shot where the camera follows the moving subject at a rear-side angle? | 4 | 2679 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera only roll clockwise without any other camera movements? | 3 | 2680 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Does the camera only roll counterclockwise without any other camera movements? | 1 | 2682 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the video include a shot transition? | 0 | 2683 | cam_motion.has_shot_transition_cam_motion |
