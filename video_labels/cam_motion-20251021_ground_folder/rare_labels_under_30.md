# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Does the camera only tilt downward without any other camera movements? | 28 | 4421 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the camera only pan rightward without any other camera movements? | 27 | 4422 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera only roll clockwise without any other camera movements? | 27 | 4422 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Does the camera only move laterally leftward without any other camera movements? | 24 | 4425 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera only roll counterclockwise without any other camera movements? | 23 | 4426 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera move only physically upward (not tilting up) relative to the ground (even if it's a bird's or worm's eye view)? | 21 | 4428 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 20 | 4427 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 17 | 4431 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera only tilt upward without any other camera movements? | 17 | 4432 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Is it a rear-side tracking shot where the camera follows the moving subject at a rear-side angle? | 16 | 4236 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Is it a front-side tracking shot where the camera leads the moving subject from a front-side angle? | 16 | 4236 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Does the video contain a frame freeze effect at any point? | 15 | 4434 | cam_motion.has_frame_freezing |
| Is the camera craning downward in an arc relative to its own frame? | 14 | 3931 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Is the scene in the video dynamic and features movement? | 0 | 0 | cam_motion.scene_movement.dynamic_scene |
| Is the scene in the video completely static? | 0 | 0 | cam_motion.scene_movement.static_scene |
| Is the scene in the video mostly static with minimal movement? | 0 | 0 | cam_motion.scene_movement.mostly_static_scene |
| Does the camera only move physically downward (or pedestals down) without any other camera movements? | 0 | 4449 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Does the camera move physically downward (or pedestals down) with respect to the initial frame? | 0 | 1599 | cam_motion.camera_centric_movement.downward.has_downward_wrt_camera |
| Does the camera move only physically backward (not zooming out) with respect to the initial frame, without any other movement? | 0 | 4449 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move backward (not zooming out) with respect to the initial frame? | 0 | 1599 | cam_motion.camera_centric_movement.backward.has_backward_wrt_camera |
| Does the camera move only physically forward (not zooming in) with respect to the initial frame, without any other movement? | 0 | 4449 | cam_motion.camera_centric_movement.forward.only_forward_wrt_camera |
| Does the camera physically move forward (not zooming in) with respect to the initial frame? | 0 | 1599 | cam_motion.camera_centric_movement.forward.has_forward_wrt_camera |
| Does the camera only move physically upward (or pedestals up) without any other camera movements? | 0 | 4449 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the camera move physically upward (or pedestals up) with respect to the initial frame? | 0 | 1599 | cam_motion.camera_centric_movement.upward.has_upward_wrt_camera |
