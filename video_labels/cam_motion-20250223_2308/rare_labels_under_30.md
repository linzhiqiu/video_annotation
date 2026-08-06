# Rare Labels
Labels with less than 30 positive examples
| Definition | Positive Examples | Negative Examples | Label Name |
| --- | --- | --- | --- |
| Is it a side-tracking shot where the camera moves left to follow the subject? | 27 | 2160 | cam_motion.object_centric_movement.side_tracking_shot_leftward |
| Does the camera roll clockwise in the scene? | 26 | 1010 | cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise |
| Is zooming in the only motion in this shot, without other camera movement? | 25 | 2162 | cam_motion.camera_centric_movement.zoom_in.only_zoom_in |
| Does the camera move only backward (not zooming out) with respect to the initial frame? | 25 | 2162 | cam_motion.camera_centric_movement.backward.only_backward_wrt_camera |
| Does the camera move in a counterclockwise arc? | 25 | 2152 | cam_motion.arc_crane_movement.arc_counterclockwise.has_arc_counterclockwise |
| Is it a tracking shot with the camera following behind the subject? | 24 | 2149 | cam_motion.object_centric_movement.tail_tracking_shot |
| Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view? | 24 | 2163 | cam_motion.ground_centric_movement.backward.only_backward_wrt_ground_birds_worms_included |
| Does the camera only pan from right to left? | 23 | 2164 | cam_motion.camera_centric_movement.pan_left.only_pan_left |
| Does the camera only pan from left to right? | 21 | 2166 | cam_motion.camera_centric_movement.pan_right.only_pan_right |
| Does the subject look smaller during the tracking shot? | 20 | 2167 | cam_motion.object_centric_movement.tracking_subject_smaller_size |
| Does the camera only move left in the scene? | 20 | 2167 | cam_motion.camera_centric_movement.leftward.only_leftward |
| Does the camera tilt to track the subjects? | 17 | 2156 | cam_motion.object_centric_movement.tilt_tracking_shot |
| Does the camera move in a clockwise arc? | 15 | 2162 | cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise |
| Is zooming out the only motion in this shot, without other camera movement? | 14 | 2173 | cam_motion.camera_centric_movement.zoom_out.only_zoom_out |
| Does the camera only tilt up in the scene? | 13 | 2174 | cam_motion.camera_centric_movement.tilt_up.only_tilt_up |
| Does the camera follow the subject while moving in an arc? | 11 | 2176 | cam_motion.object_centric_movement.arc_tracking_shot |
| Does the camera only move upward (not tilting up) with respect to the initial frame? | 10 | 2177 | cam_motion.camera_centric_movement.upward.only_upward_wrt_camera |
| Does the video contain a frame freeze effect at any point? | 8 | 2179 | cam_motion.has_frame_freezing |
| Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view? | 8 | 2179 | cam_motion.ground_centric_movement.upward.only_upward_wrt_ground_birds_worms_included |
| Does the camera only tilt down in the scene? | 8 | 2179 | cam_motion.camera_centric_movement.tilt_down.only_tilt_down |
| Is the camera performing a crane up movement? | 8 | 2139 | cam_motion.arc_crane_movement.crane_up.has_crane_up |
| Does the shot feature a dolly zoom effect with the camera moving backward and zooming in? | 7 | 2180 | cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in |
| Does the shot feature a dolly zoom effect with the camera moving forward and zooming out? | 6 | 2181 | cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out |
| Is it a tracking shot with the camera leading from the front and to the side of the subject? | 6 | 2181 | cam_motion.object_centric_movement.front_side_tracking_shot |
| Is it a tracking shot with the camera following behind and to the side of the subject? | 5 | 2182 | cam_motion.object_centric_movement.rear_side_tracking_shot |
| Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view? | 3 | 2184 | cam_motion.ground_centric_movement.downward.only_downward_wrt_ground_birds_worms_included |
| Does the camera only roll counterclockwise in the scene? | 2 | 2185 | cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise |
| Does the camera only roll clockwise in the scene? | 2 | 2185 | cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise |
| Is the camera performing a crane down movement? | 2 | 2145 | cam_motion.arc_crane_movement.crane_down.has_crane_down |
| Does the video include shot transitions? | 0 | 2187 | cam_motion.has_shot_transition_cam_motion |
| Does the camera only move downward (not tilting down) with respect to the initial frame? | 0 | 2187 | cam_motion.camera_centric_movement.downward.only_downward_wrt_camera |
