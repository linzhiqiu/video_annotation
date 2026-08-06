# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is zooming in the only motion in this shot, without other camera movement? | 29 | 3046 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 28 | 3047 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 27 | 3048 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera follow the subject while moving in an arc? | 25 | 3050 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera only pan from right to left? | 23 | 3052 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the camera only move left in the scene? | 21 | 3054 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera only pan from left to right? | 21 | 3054 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the camera tilt to track the subjects? | 18 | 3042 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 18 | 3057 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
| Is the camera performing a crane up movement? | 18 | 2815 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the camera only tilt down in the scene? | 15 | 3060 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Does the camera only tilt up in the scene? | 13 | 3062 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the video contain a frame freeze effect at any point? | 12 | 3063 | cam_motion.has_frame_freezing |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 11 | 3064 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 10 | 3064 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 10 | 3065 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 9 | 3064 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Is the camera performing a crane down movement? | 8 | 2825 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Is it a tracking shot with the camera leading from the front and to the side of the subject? | 7 | 3068 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind and to the side of the subject? | 6 | 3069 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera only roll clockwise in the scene? | 4 | 3071 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Does the camera only roll counterclockwise in the scene? | 2 | 3073 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the video include shot transitions? | 0 | 3075 | cam_motion.has_shot_transition_cam_motion |
