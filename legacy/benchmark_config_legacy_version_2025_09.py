CAMERABENCH_GROUND_ONLY_FOLDER = "cam_motion-20250227_0324ground_only"
CAMERABENCH_GROUND_AND_SETUP_FOLDER = "cam_motion-cam_setup-20250227_0507ground_and_setup"
CAMERABENCH_GROUND_AND_CAMERA_FOLDER = "cam_motion-20250227_0326ground_and_camera"
# New folder after ICCV
CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL_UPDATE = "cam_motion-cam_setup-20250227_0507ground_and_setup_updated_on_0406"

CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL = "cam_motion-cam_setup-20250406_setup_and_motion"
CAMERABENCH_GROUND_ONLY_FOLDER_APRIL = "cam_motion-20250406ground_only"
CAMERABENCH_SETUP_ONLY_FOLDER_APRIL = "cam_setup-20250406setup_only"
CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL = "lighting_setup-20250406lighting_only"


FOLDER_NAMES = [
    "motion_dataset", # ICCV Version
    "motion_dataset_april_update", # April Update for ICCV Version with same videos (Final version to be used?)
    "motion_dataset_april_6", # April Version of ICCV Benchmark (Final version to be used?)
    "setup_dataset_april_6",
    "lighting_dataset_april_6"
]

def get_pairwise_labels(folder_name):
    assert folder_name in FOLDER_NAMES
    if folder_name == "motion_dataset":
        return get_motion_pairwise_labels(
            ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
            ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
            ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
        )
    elif folder_name == "motion_dataset_redo":
        return get_motion_pairwise_labels(
            ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
            ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
            ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
        )
    elif folder_name == "motion_dataset_april_update":
        return get_motion_pairwise_labels(
            ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
            ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL_UPDATE,
            ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
        )
    elif folder_name == "motion_dataset_april_6":
        return get_motion_pairwise_labels(
            ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER_APRIL,
            ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL,
            ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
        )
    elif folder_name == "setup_dataset_april_6":
        return get_setup_pairwise_labels(
            setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL,
        )
    elif folder_name == "motion_and_setup_dataset_april_6":
        return get_motion_and_setup_pairwise_labels(
            ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER_APRIL,
            ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL,
            ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
            setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL,
        )
    elif folder_name == "lighting_dataset_april_6":
        return get_lighting_pairwise_labels(
            lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL,
        )
    else:
        raise ValueError(f"Invalid folder name: {folder_name}")

def get_movement_and_steadiness_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "is_the_camera_clearly_moving_or_not",
            "pos_question": "Does the camera have noticeable motion beyond minor shake or wobble?",
            "neg_question": "Is the camera free from noticeable motion beyond minor shake or wobble?",
            "pos_prompt": "A video where the camera has noticeable motion beyond minor shake or wobble.",
            "neg_prompt": "A video where the camera is free from noticeable motion beyond minor shake or wobble.",
            "pos": {
                "label": "cam_motion.steadiness_and_movement.clear_moving_camera",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.steadiness_and_movement.clear_moving_camera",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "is_the_fixed_camera_shaking_or_not",
            "pos_question": "Is the camera completely still without any motion or shaking?",
            "neg_question": "Is the camera stationary with minor vibrations or shaking?",
            "pos_prompt": "A video where the camera remains completely still with no motion or shaking.",
            "neg_prompt": "A video where the camera is mostly stationary but has minor vibrations or shaking.",
            "pos": {
                "label": "cam_motion.steadiness_and_movement.fixed_camera",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.steadiness_and_movement.fixed_camera_with_shake",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "is_the_camera_stable_or_shaky",
            "pos_question": "Is the camera movement exceptionally smooth and highly stable?",
            "neg_question": "Does the camera show noticable vibrations, shaking, or wobbling?",
            "pos_prompt": "A video where the camera movement is exceptionally smooth and highly stable.",
            "neg_prompt": "A video where the camera shows noticable vibrations, shaking, or wobbling.",
            "pos": {
                "label": "cam_motion.steadiness_and_movement.very_stable_camera",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.steadiness_and_movement.very_shaky_camera",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "is_the_camera_fixed_or_moving",
            "pos_question": "Is the camera completely still without any visible movement?",
            "neg_question": "Is the camera not completely still and shows visible movement?",
            "pos_prompt": "The camera is completely still without any visible movement.",
            "neg_prompt": "The camera is not completely still and shows visible movement.",
            "pos": {
                "label": "cam_motion.steadiness_and_movement.fixed_camera",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.steadiness_and_movement.fixed_camera",
                "type": "neg",
            },
        },
    ]

def get_scene_dynamics_tasks(
    ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
    ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER
):
    return [
        {
            "folder": ground_and_camera_folder,
            "name": "is_scene_static_or_not",
            "pos_question": "Is the scene in the video completely static?",
            "neg_question": "Is the scene in the video dynamic?",
            "pos_prompt": "A video where the scene is completely static.",
            "neg_prompt": "A video where the scene is dynamic and features movement.",
            "pos": {"label": "cam_motion.scene_movement.static_scene", "type": "pos"},
            "neg": {"label": "cam_motion.scene_movement.dynamic_scene", "type": "pos"},
        },
        {
            "folder": ground_only_folder,
            "name": "has_frame_freeze_or_not",
            "pos_question": "Does the video contain a frame freeze effect at any point?",
            "neg_question": "Is the video free from any frame freeze effect?",
            "pos_prompt": "A video that contains a frame freeze effect at some point.",
            "neg_prompt": "A video that is free from any frame freeze effect.",
            "pos": {"label": "cam_motion.has_frame_freezing", "type": "pos"},
            "neg": {"label": "cam_motion.has_frame_freezing", "type": "neg"},
        },
    ]

def get_camera_movement_speed_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "is_camera_movement_slow_or_fast",
            "pos_question": "Does the camera have noticeable motion but at a slow motion speed?",
            "neg_question": "Does the camera have noticeable motion but at a fast motion speed?",
            "pos_prompt": "A video where the camera has noticeable motion at a slow speed.",
            "neg_prompt": "A video where the camera has noticeable motion at a fast speed.",
            "pos": {
                "label": "cam_motion.steadiness_and_movement.slow_moving_camera",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.steadiness_and_movement.fast_moving_camera",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_motion_blur_or_not",
            "pos_question": "Does the video contain noticeable motion blur?",
            "neg_question": "Is the video free from any noticeable motion blur?",
            "pos_prompt": "The video exhibits a motion blur effect.",
            "neg_prompt": "The video is free from any noticeable motion blur.",
            "pos": {"label": "cam_motion.has_motion_blur", "type": "pos"},
            "neg": {"label": "cam_motion.has_motion_blur", "type": "neg"},
        },
    ]

def get_translation_direction_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
                                    ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER):
    return [
        # Translation Direction (3 tasks)
        {
            "folder": ground_and_setup_folder,
            "name": "has_forward_vs_backward_ground",
            "pos_question": "Is the camera moving forward in the scene?",
            "neg_question": "Is the camera moving backward in the scene?",
            "pos_prompt": "A shot where the camera is moving forward within the scene.",
            "neg_prompt": "A shot where the camera is moving backward within the scene.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground",
                "type": "pos",
            },
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_upward_vs_downward_ground",
            "pos_question": "Does the camera move upward relative to the ground?",
            "neg_question": "Does the camera move downward relative to the ground?",
            "pos_prompt": "The camera is moving upward relative to the ground.",
            "neg_prompt": "The camera is moving downward relative to the ground.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_leftward_vs_rightward",
            "pos_question": "Does the camera move leftward in the scene?",
            "neg_question": "Does the camera move rightward in the scene?",
            "pos_prompt": "The camera moves leftward.",
            "neg_prompt": "The camera moves rightward.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                "type": "pos",
            },
        },
    ]

def get_rotation_direction_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        # Rotation Direction (3 tasks)
        {
            "folder": ground_only_folder,
            "name": "pan_left_vs_pan_right",
            "pos_question": "Does the camera pan to the left?",
            "neg_question": "Does the camera pan to the right?",
            "pos_prompt": "The camera pans to the left.",
            "neg_prompt": "The camera pans to the right.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "tilt_up_vs_tilt_down",
            "pos_question": "Does the camera tilt upward?",
            "neg_question": "Does the camera tilt downward?",
            "pos_prompt": "The camera tilts upward.",
            "neg_prompt": "The camera tilts downward.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "roll_cc_vs_roll_ccw",
            "pos_question": "Does the camera roll clockwise?",
            "neg_question": "Does the camera roll counterclockwise?",
            "pos_prompt": "The camera rolls clockwise.",
            "neg_prompt": "The camera rolls counterclockwise.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.roll_counterclockwise.has_roll_counterclockwise",
                "type": "pos",
            },
        },
    ]

def get_object_centric_direction_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        # Object-Centric Direction (4 tasks)
        {
            "folder": ground_only_folder,
            "name": "side_tracking_leftward_vs_rightward",
            "pos_question": "Is it a side-tracking shot where the camera moves left to follow the subject?",
            "neg_question": "Is it a side-tracking shot where the camera moves right to follow the subject?",
            "pos_prompt": "A side-tracking shot where the camera moves left to follow the subject.",
            "neg_prompt": "A side-tracking shot where the camera moves right to follow the subject.",
            "pos": {
                "label": "cam_motion.object_centric_movement.side_tracking_shot_leftward",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.side_tracking_shot_rightward",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "lead_tracking_vs_tail_tracking",
            "pos_question": "Is it a tracking shot with the camera moving ahead of the subject?",
            "neg_question": "Is it a tracking shot with the camera following behind the subject?",
            "pos_prompt": "A tracking shot where the camera moves ahead of the subject.",
            "neg_prompt": "A tracking shot where the camera follows behind the subject.",
            "pos": {
                "label": "cam_motion.object_centric_movement.lead_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.tail_tracking_shot",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "arc_ccw_vs_arc_cc",
            "pos_question": "Does the camera move in a counterclockwise arc?",
            "neg_question": "Does the camera move in a clockwise arc?",
            "pos_prompt": "The camera arcs counterclockwise.",
            "neg_prompt": "The camera arcs clockwise.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.arc_counterclockwise.has_arc_counterclockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "crane_up_vs_crane_down",
            "pos_question": "Is the camera craning upward in an arc?",
            "neg_question": "Does the camera move downward in a crane shot?",
            "pos_prompt": "The camera cranes upward in an arc.",
            "neg_prompt": "The camera cranes downward in an arc.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.crane_up.has_crane_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.crane_down.has_crane_down",
                "type": "pos",
            },
        },
    ]

def get_intrinsic_direction_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        # Intrinsic Direction (2 tasks)
        {
            "folder": ground_only_folder,
            "name": "dolly_zoom_in_vs_dolly_zoom_out",
            "pos_question": "Does the shot feature a dolly zoom effect with the camera moving backward and zooming in?",
            "neg_question": "Does the shot feature a dolly zoom effect with the camera moving forward and zooming out?",
            "pos_prompt": "The camera performs a dolly zoom effect with backward movement and zoom-in.",
            "neg_prompt": "The camera performs a dolly zoom effect with forward movement and zoom-out.",
            "pos": {
                "label": "cam_motion.dolly_zoom_movement.has_dolly_out_zoom_in",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.dolly_zoom_movement.has_dolly_in_zoom_out",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "zoom_in_vs_zoom_out",
            "pos_question": "Does the camera zoom in?",
            "neg_question": "Does the camera zoom out?",
            "pos_prompt": "The camera zooms in.",
            "neg_prompt": "The camera zooms out.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                "type": "pos",
            },
        },
    ]

def get_instrinsic_vs_extrinsic_tasks(ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER):
                                      
    return [
        # Intrinsic vs. Extrinsic (4 tasks)
        {
            "folder": ground_and_camera_folder,
            "name": "has_zoom_in_not_move_vs_has_move_not_zoom_in",
            "pos_question": "Does the camera zoom in without physically moving forward?",
            "neg_question": "Does the camera physically move forward without zooming in?",
            "pos_prompt": "A video where the camera zooms in without physically moving forward.",
            "neg_prompt": "A video where the camera physically moves forward without zooming in.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.forward.has_forward_wrt_camera",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.forward.has_forward_wrt_camera",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_and_camera_folder,
            "name": "has_zoom_out_not_move_vs_has_move_not_zoom_out",
            "pos_question": "Does the camera zoom out without physically moving backward?",
            "neg_question": "Does the camera physically move backward without zooming out?",
            "pos_prompt": "A video where the camera zooms out without physically moving backward.",
            "neg_prompt": "A video where the camera physically moves backward without zooming out.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.backward.has_backward_wrt_camera",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.backward.has_backward_wrt_camera",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_and_camera_folder,
            "name": "only_zoom_in_vs_only_forward",
            "pos_question": "Does the camera only zoom in without any other camera movement?",
            "neg_question": "Does the camera only move forward without any other camera movement?",
            "pos_prompt": "A video where the camera only zooms in with no other movement.",
            "neg_prompt": "A video where the camera only moves forward with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_in.only_zoom_in",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.forward.only_forward_wrt_camera",
                "type": "pos",
            },
        },
        {
            "folder": ground_and_camera_folder,
            "name": "only_zoom_out_vs_only_backward",
            "pos_question": "Does the camera only zoom out without any other camera movement?",
            "neg_question": "Does the camera only move backward without any other camera movement?",
            "pos_prompt": "A video where the camera only zooms out with no other movement.",
            "neg_prompt": "A video where the camera only moves backward with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_out.only_zoom_out",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.backward.only_backward_wrt_camera",
                "type": "pos",
            },
        },
    ]

def get_rotation_vs_translation_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
                                  ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
                                  ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER):
    return [
        # Rotation vs. Translation (8 tasks)
        {
            "folder": ground_only_folder,
            "name": "has_pan_right_not_truck_vs_has_truck_not_pan_right",
            "pos_question": "Does the camera pan right without moving laterally to the right?",
            "neg_question": "Does the camera move laterally to the right without panning right?",
            "pos_prompt": "The camera pans right without moving laterally to the right.",
            "neg_prompt": "The camera moves laterally to the right without panning right.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "has_pan_left_not_truck_vs_has_truck_not_pan_left",
            "pos_question": "Does the camera pan left without moving laterally to the left?",
            "neg_question": "Does the camera move laterally to the left without panning left?",
            "pos_prompt": "The camera pans left without moving laterally to the left.",
            "neg_prompt": "The camera moves laterally to the left without panning left.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_pan_right_vs_only_truck_right",
            "pos_question": "Does the camera only pan right with no other movement?",
            "neg_question": "Does the camera only move laterally to the right with no other movement?",
            "pos_prompt": "A video where the camera only pans right with no other movement.",
            "neg_prompt": "A video where the camera only moves laterally to the right with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_right.only_pan_right",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.rightward.only_rightward",
                "type": "pos",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "only_pan_left_vs_only_truck_left",
            "pos_question": "Does the camera only pan left with no other movement?",
            "neg_question": "Does the camera only move laterally to the left with no other movement?",
            "pos_prompt": "A video where the camera only pans left with no other movement.",
            "neg_prompt": "A video where the camera only moves laterally to the left with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_left.only_pan_left",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.leftward.only_leftward",
                "type": "pos",
            },
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_tilt_up_not_pedestal_vs_has_pedestal_not_tilt_up",
            "pos_question": "Does the camera tilt up without moving physically upward?",
            "neg_question": "Does the camera move physically upward without tilting up?",
            "pos_prompt": "A video where the camera tilts up without physically moving upward.",
            "neg_prompt": "A video where the camera physically moves upward without tilting up.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.upward.has_upward_wrt_camera",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.upward.has_upward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_tilt_down_not_pedestal_vs_has_pedestal_not_tilt_down",
            "pos_question": "Does the camera tilt down without moving physically downward?",
            "neg_question": "Does the camera move physically downward without tilting down?",
            "pos_prompt": "A video where the camera tilts down without physically moving downward.",
            "neg_prompt": "A video where the camera physically moves downward without tilting down.",
            "pos": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.camera_centric_movement.downward.has_downward_wrt_camera",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                    "type": "neg",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.downward.has_downward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                    "type": "pos",
                },
            ],
        },
        {
            "folder": ground_and_camera_folder,
            "name": "only_tilt_up_vs_only_pedestal_up",
            "pos_question": "Does the camera only tilt up with no other movement?",
            "neg_question": "Does the camera only move physically upward (pedestal up) with no other movement?",
            "pos_prompt": "A video where the camera only tilts up with no other movement.",
            "neg_prompt": "A video where the camera only moves physically upward with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_up.only_tilt_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.upward.only_upward_wrt_camera",
                "type": "pos",
            },
        },
        {
            "folder": ground_and_camera_folder,
            "name": "only_tilt_down_vs_only_pedestal_down",
            "pos_question": "Does the camera only tilt down with no other movement?",
            "neg_question": "Does the camera only move physically downward (pedestal down) with no other movement?",
            "pos_prompt": "A video where the camera only tilts down with no other movement.",
            "neg_prompt": "A video where the camera only moves physically downward with no other movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_down.only_tilt_down",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.downward.only_downward_wrt_camera",
                "type": "pos",
            },
        },
    ]

def get_has_intrinsic_change_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "has_zoom_in",
            "pos_question": "Does the camera zoom in?",
            "neg_question": "Is the camera free from any zoom in effects?",
            "pos_prompt": "The camera zooms in.",
            "neg_prompt": "The camera is free from any zoom in effects.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_zoom_out",
            "pos_question": "Does the camera zoom out?",
            "neg_question": "Is the camera free from any zoom out effects?",
            "pos_prompt": "The camera zooms out.",
            "neg_prompt": "The camera is free from any zoom out effects.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                "type": "neg",
            },
        },
    ]

def get_has_translation_tasks(ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
                              ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_and_setup_folder,
            "name": "has_forward_motion",
            "pos_question": "Is the camera moving forward in the scene?",
            "neg_question": "Is the camera free from any forward motion?",
            "pos_prompt": "The camera is moving forward within the scene.",
            "neg_prompt": "The camera is free from any forward motion.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground",
                "type": "neg",
            },
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_backward_motion",
            "pos_question": "Is the camera moving backward in the scene?",
            "neg_question": "Is the camera free from any backward motion?",
            "pos_prompt": "The camera is moving backward within the scene.",
            "neg_prompt": "The camera is free from any backward motion.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_truck_left",
            "pos_question": "Does the camera move laterally to the left?",
            "neg_question": "Is the camera free from any leftward lateral movement?",
            "pos_prompt": "The camera moves laterally to the left.",
            "neg_prompt": "The camera is free from any leftward lateral movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_truck_right",
            "pos_question": "Does the camera move laterally to the right?",
            "neg_question": "Is the camera free from any rightward lateral movement?",
            "pos_prompt": "The camera moves laterally to the right.",
            "neg_prompt": "The camera is free from any rightward lateral movement.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                "type": "neg",
            },
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_pedestal_up",
            "pos_question": "Does the camera move upward relative to the ground?",
            "neg_question": "Is the camera free from any upward pedestal motion?",
            "pos_prompt": "The camera moves upward relative to the ground.",
            "neg_prompt": "The camera is free from any upward pedestal motion.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                "type": "neg",
            },
        },
        {
            "folder": ground_and_setup_folder,
            "name": "has_pedestal_down",
            "pos_question": "Does the camera move downward relative to the ground?",
            "neg_question": "Is the camera free from any downward pedestal motion?",
            "pos_prompt": "The camera moves downward relative to the ground.",
            "neg_prompt": "The camera is free from any downward pedestal motion.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                "type": "neg",
            },
        },
    ]

def get_has_rotation_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "has_pan_left",
            "pos_question": "Does the camera pan to the left?",
            "neg_question": "Is the camera free from any leftward panning motion?",
            "pos_prompt": "The camera pans to the left.",
            "neg_prompt": "The camera is free from any leftward panning motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_pan_right",
            "pos_question": "Does the camera pan to the right?",
            "neg_question": "Is the camera free from any rightward panning motion?",
            "pos_prompt": "The camera pans to the right.",
            "neg_prompt": "The camera is free from any rightward panning motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_tilt_up",
            "pos_question": "Does the camera tilt upward?",
            "neg_question": "Is the camera free from any upward tilting motion?",
            "pos_prompt": "The camera tilts upward.",
            "neg_prompt": "The camera is free from any upward tilting motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_tilt_down",
            "pos_question": "Does the camera tilt downward?",
            "neg_question": "Is the camera free from any downward tilting motion?",
            "pos_prompt": "The camera tilts downward.",
            "neg_prompt": "The camera is free from any downward tilting motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_roll_clockwise",
            "pos_question": "Does the camera roll clockwise?",
            "neg_question": "Is the camera free from any clockwise rolling motion?",
            "pos_prompt": "The camera rolls clockwise.",
            "neg_prompt": "The camera is free from any clockwise rolling motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_roll_counterclockwise",
            "pos_question": "Does the camera roll counterclockwise?",
            "neg_question": "Is the camera free from any counterclockwise rolling motion?",
            "pos_prompt": "The camera rolls counterclockwise.",
            "neg_prompt": "The camera is free from any counterclockwise rolling motion.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.roll_counterclockwise.has_roll_counterclockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.camera_centric_movement.roll_counterclockwise.has_roll_counterclockwise",
                "type": "neg",
            },
        },
    ]

def get_has_arc_crane_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "has_arc_clockwise",
            "pos_question": "Does the camera move in a clockwise arc?",
            "neg_question": "Is the camera free from any clockwise arc movement?",
            "pos_prompt": "The camera moves in a clockwise arc.",
            "neg_prompt": "The camera is free from any clockwise arc movement.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.arc_clockwise.has_arc_clockwise",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_arc_counterclockwise",
            "pos_question": "Does the camera move in a counterclockwise arc?",
            "neg_question": "Is the camera free from any counterclockwise arc movement?",
            "pos_prompt": "The camera moves in a counterclockwise arc.",
            "neg_prompt": "The camera is free from any counterclockwise arc movement.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.arc_counterclockwise.has_arc_counterclockwise",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.arc_counterclockwise.has_arc_counterclockwise",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_crane_up",
            "pos_question": "Does the camera crane upward in an arc?",
            "neg_question": "Is the camera not craning upward in an arc?",
            "pos_prompt": "The camera cranes upward in an arc.",
            "neg_prompt": "The camera is not craning upward in an arc.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.crane_up.has_crane_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.crane_up.has_crane_up",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_crane_down",
            "pos_question": "Does the camera crane downward in an arc?",
            "neg_question": "Is the camera not craning downward in an arc?",
            "pos_prompt": "The camera cranes downward in an arc.",
            "neg_prompt": "The camera is not craning downward in an arc.",
            "pos": {
                "label": "cam_motion.arc_crane_movement.crane_down.has_crane_down",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.arc_crane_movement.crane_down.has_crane_down",
                "type": "neg",
            },
        },
    ]

def get_special_tracking_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "has_aerial_tracking",
            "pos_question": "Does the camera track the subject from an aerial perspective?",
            "neg_question": "Is the video not a tracking shot from an aerial perspective?",
            "pos_prompt": "The camera tracks the subject from an aerial perspective.",
            "neg_prompt": "The camera is not tracking the subject from an aerial perspective.",
            "pos": {
                "label": "cam_motion.object_centric_movement.aerial_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.aerial_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_arc_tracking",
            "pos_question": "Does the camera follow the subject while moving in an arc?",
            "neg_question": "Is the video not a tracking shot with arc movement?",
            "pos_prompt": "A tracking shot where the camera follows the subject while moving in an arc.",
            "neg_prompt": "A video where the camera is not tracking the subject with arc movement.",
            "pos": {
                "label": "cam_motion.object_centric_movement.arc_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.arc_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_front_side_tracking",
            "pos_question": "Is it a tracking shot with the camera leading the subject from a front-side angle?",
            "neg_question": "Is the camera not leading the subject from a front-side angle in a tracking shot?",
            "pos_prompt": "A tracking shot where the camera leads the subject from a front-side angle.",
            "neg_prompt": "The camera is not leading the subject from a front-side angle in a tracking shot.",
            "pos": {
                "label": "cam_motion.object_centric_movement.front_side_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.front_side_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_rear_side_tracking",
            "pos_question": "Is it a tracking shot with the camera following behind the subject at a rear-side angle?",
            "neg_question": "Is the camera not following behind the subject at a rear-side angle?",
            "pos_prompt": "A tracking shot where the camera follows behind the subject at a rear-side angle.",
            "neg_prompt": "The camera is not following behind the subject at a rear-side angle.",
            "pos": {
                "label": "cam_motion.object_centric_movement.rear_side_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.rear_side_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_lead_tracking",
            "pos_question": "Is it a tracking shot with the camera moving ahead of the subject as they move?",
            "neg_question": "Is the camera not moving ahead of the subject in a tracking shot?",
            "pos_prompt": "A tracking shot where the camera moves ahead of the subjects as they move.",
            "neg_prompt": "The camera is not moving ahead of the subject in a tracking shot.",
            "pos": {
                "label": "cam_motion.object_centric_movement.lead_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.lead_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_tail_tracking",
            "pos_question": "Is it a tracking shot with the camera following behind the subject as they move?",
            "neg_question": "Is the camera not following behind the subject in a tracking shot?",
            "pos_prompt": "A tracking shot where the camera moves behind the subjects as they move.",
            "neg_prompt": "The camera is not following behind the subject in a tracking shot.",
            "pos": {
                "label": "cam_motion.object_centric_movement.tail_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.tail_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_tilt_tracking",
            "pos_question": "Does the camera tilt to track the subjects as they move?",
            "neg_question": "Is the camera not tilting to track the subjects?",
            "pos_prompt": "A tracking shot where the camera tilts to follow the subjects.",
            "neg_prompt": "The camera is not tilting to track the subjects.",
            "pos": {
                "label": "cam_motion.object_centric_movement.tilt_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.tilt_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_pan_tracking",
            "pos_question": "Does the camera pan to track the subjects as they move?",
            "neg_question": "Is the camera not panning to track the subjects?",
            "pos_prompt": "A tracking shot where the camera pans to follow the subjects as they move.",
            "neg_prompt": "The camera is not panning to track the subjects.",
            "pos": {
                "label": "cam_motion.object_centric_movement.pan_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.pan_tracking_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "has_side_tracking",
            "pos_question": "Is it a tracking shot with the camera moving from the side to follow the subject as they move?",
            "neg_question": "Is the camera not moving from the side to track the subject?",
            "pos_prompt": "A tracking shot where the camera moves from the side to follow the subject.",
            "neg_prompt": "The camera is not moving from the side to track the subject.",
            "pos": {
                "label": "cam_motion.object_centric_movement.side_tracking_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.side_tracking_shot",
                "type": "neg",
            },
        },
    ]

def get_general_tracking_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "is_tracking",
            "pos_question": "Does the camera track the subject as they move?",
            "neg_question": "Is the video not a tracking shot?",
            "pos_prompt": "The camera tracks the subject as they move.",
            "neg_prompt": "The video is not a tracking shot.",
            "pos": {
                "label": "cam_motion.object_centric_movement.track_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.track_shot",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "tracking_subject_larger",
            "pos_question": "Does the subject appear larger during the tracking shot?",
            "neg_question": "Does the subject being tracked not appear larger in size?",
            "pos_prompt": "The subject looks larger during the tracking shot.",
            "neg_prompt": "The subject being tracked does not appear larger in size.",
            "pos": {
                "label": "cam_motion.object_centric_movement.tracking_subject_larger_size",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.tracking_subject_larger_size",
                "type": "neg",
            },
        },
        {
            "folder": ground_only_folder,
            "name": "tracking_subject_smaller",
            "pos_question": "Does the subject appear smaller during the tracking shot?",
            "neg_question": "Does the subject being tracked not appear smaller in size?",
            "pos_prompt": "The subject looks smaller during the tracking shot.",
            "neg_prompt": "The subject being tracked does not appear smaller in size.",
            "pos": {
                "label": "cam_motion.object_centric_movement.tracking_subject_smaller_size",
                "type": "pos",
            },
            "neg": {
                "label": "cam_motion.object_centric_movement.tracking_subject_smaller_size",
                "type": "neg",
            },
        },
    ]

def get_only_intrinsic_change_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "only_zoom_in_vs_has_zoom_in_and_not_only",
            "pos_question": "Does the camera only zoom in with no other movement?",
            "neg_question": "Does the camera not just zoom in?",
            "pos_prompt": "The camera only zooms in without any other movement.",
            "neg_prompt": "The camera does not just zoom in.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_in.only_zoom_in",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_in.has_zoom_in",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.zoom_in.only_zoom_in",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_zoom_out_vs_has_zoom_out_and_not_only",
            "pos_question": "Does the camera only zoom out with no other movement?",
            "neg_question": "Does the camera not just zoom out?",
            "pos_prompt": "The camera only zooms out with no other movement.",
            "neg_prompt": "The camera does not just zoom out.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.zoom_out.only_zoom_out",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.zoom_out.has_zoom_out",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.zoom_out.only_zoom_out",
                    "type": "neg",
                },
            ],
        },
    ]

def get_only_translation_tasks(ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
                               ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_and_setup_folder,
            "name": "only_forward_vs_has_forward_and_not_only",
            "pos_question": "Does the camera only move forward (not zooming in) with respect to the ground?",
            "neg_question": "Does the camera not just move forward with respect to the ground?",
            "pos_prompt": "The camera only moves forward (not zooming in) relative to the ground.",
            "neg_prompt": "The camera not just moves forward relative to the ground.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.forward.only_forward_wrt_ground",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.forward.only_forward_wrt_ground",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_and_setup_folder,
            "name": "only_backward_vs_has_backward_and_not_only",
            "pos_question": "Does the camera only move backward (not zooming out) with respect to the ground?",
            "neg_question": "Does the camera not just move backward with respect to the ground?",
            "pos_prompt": "The camera only moves backward (not zooming out) relative to the ground.",
            "neg_prompt": "The camera not just moves backward relative to the ground.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.backward.only_backward_wrt_ground",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.backward.only_backward_wrt_ground",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_truck_left_vs_has_truck_left_and_not_only",
            "pos_question": "Does the camera only move leftward without any other camera movements?",
            "neg_question": "Does the camera not just move laterally to the left?",
            "pos_prompt": "The camera only moves leftward without any other camera movements.",
            "neg_prompt": "The camera not just moves laterally to the left.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.leftward.only_leftward",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.leftward.has_leftward",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.leftward.only_leftward",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_truck_right_vs_has_truck_right_and_not_only",
            "pos_question": "Does the camera only move rightward without any other camera movements?",
            "neg_question": "Does the camera not just move laterally to the right?",
            "pos_prompt": "The camera only moves rightward without any other camera movements.",
            "neg_prompt": "The camera not just moves laterally to the right.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.rightward.only_rightward",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.rightward.has_rightward",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.rightward.only_rightward",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_and_setup_folder,
            "name": "only_pedestal_up_vs_has_pedestal_up_and_not_only",
            "pos_question": "Does the camera only move upward (not tilting up) with respect to the ground?",
            "neg_question": "Does the camera not just move physically upward?",
            "pos_prompt": "The camera only moves upward (not tilting up) relative to the ground.",
            "neg_prompt": "The camera not just moves physically upward.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.upward.only_upward_wrt_ground",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.upward.only_upward_wrt_ground",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_and_setup_folder,
            "name": "only_pedestal_down_vs_has_pedestal_down_and_not_only",
            "pos_question": "Does the camera only move downward (not tilting down) with respect to the ground?",
            "neg_question": "Does the camera not just move physically downward?",
            "pos_prompt": "The camera only moves downward (not tilting down) relative to the ground.",
            "neg_prompt": "The camera not just moves physically downward.",
            "pos": {
                "label": "cam_motion.ground_centric_movement.downward.only_downward_wrt_ground",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.ground_centric_movement.downward.only_downward_wrt_ground",
                    "type": "neg",
                },
            ],
        },
    ]

def get_only_rotation_tasks(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER):
    return [
        {
            "folder": ground_only_folder,
            "name": "only_pan_left_vs_has_pan_left_and_not_only",
            "pos_question": "Does the camera only pan leftward without any other camera movements?",
            "neg_question": "Does the camera not just pan left?",
            "pos_prompt": "The camera only pans leftward without any other camera movements.",
            "neg_prompt": "The camera not just pans left.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_left.only_pan_left",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_left.has_pan_left",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.pan_left.only_pan_left",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_pan_right_vs_has_pan_right_and_not_only",
            "pos_question": "Does the camera only pan rightward without any other camera movements?",
            "neg_question": "Does the camera not just pan right?",
            "pos_prompt": "The camera only pans rightward without any other camera movements.",
            "neg_prompt": "The camera not just pans right.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.pan_right.only_pan_right",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.pan_right.has_pan_right",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.pan_right.only_pan_right",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_tilt_up_vs_has_tilt_up_and_not_only",
            "pos_question": "Does the camera only tilt upward without any other camera movements?",
            "neg_question": "Does the camera not just tilt up?",
            "pos_prompt": "The camera only tilts upward without any other camera movements.",
            "neg_prompt": "The camera not just tilts up.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_up.only_tilt_up",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_up.has_tilt_up",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.tilt_up.only_tilt_up",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_tilt_down_vs_has_tilt_down_and_not_only",
            "pos_question": "Does the camera only tilt downward without any other camera movements?",
            "neg_question": "Does the camera not just tilt down?",
            "pos_prompt": "The camera only tilts downward without any other camera movements.",
            "neg_prompt": "The camera not just tilts down.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.tilt_down.only_tilt_down",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.tilt_down.has_tilt_down",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.tilt_down.only_tilt_down",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_roll_cc_vs_has_roll_cc_and_not_only",
            "pos_question": "Does the camera only roll clockwise without any other camera movements?",
            "neg_question": "Does the camera not just roll clockwise?",
            "pos_prompt": "The camera only rolls clockwise without any other camera movements.",
            "neg_prompt": "The camera not just rolls clockwise.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.roll_clockwise.has_roll_clockwise",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.roll_clockwise.only_roll_clockwise",
                    "type": "neg",
                },
            ],
        },
        {
            "folder": ground_only_folder,
            "name": "only_roll_ccw_vs_has_roll_ccw_and_not_only",
            "pos_question": "Does the camera only roll counterclockwise without any other camera movements?",
            "neg_question": "Does the camera not just roll counterclockwise?",
            "pos_prompt": "The camera only rolls counterclockwise without any other camera movements.",
            "neg_prompt": "The camera not just rolls counterclockwise.",
            "pos": {
                "label": "cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise",
                "type": "pos",
            },
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.roll_counterclockwise.has_roll_counterclockwise",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.roll_counterclockwise.only_roll_counterclockwise",
                    "type": "neg",
                },
            ],
        },
    ]

def get_reference_frame_tasks(ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER):
    return [
        {
            # "folder": ground_and_camera_folder,
            "folder": ground_and_setup_folder,
            "name": "forward_camera_only_vs_forward_ground_and_camera",
            "pos_question": "Does the camera move forward only relative to its initial viewing direction but not relative to the ground?",
            "neg_question": "Does the camera move forward relative to both the ground and its initial viewing direction?",
            "pos_prompt": "The camera moves forward only relative to its initial viewing direction but not relative to the ground.",
            "neg_prompt": "The camera moves forward relative to both the ground and its initial viewing direction.",
            "pos": [
                {
                    "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground_birds_worms_included",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.forward.has_forward_wrt_camera",
                    "type": "pos",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.forward.has_forward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.forward.has_forward_wrt_ground_birds_worms_included",
                    "type": "pos",
                },
            ],
        },
        {
            # "folder": ground_and_camera_folder,
            "folder": ground_and_setup_folder,
            "name": "backward_camera_only_vs_backward_ground_and_camera",
            "pos_question": "Does the camera move backward only relative to its initial viewing direction but not relative to the ground?",
            "neg_question": "Does the camera move backward relative to both the ground and its initial viewing direction?",
            "pos_prompt": "The camera moves backward only relative to its initial viewing direction but not relative to the ground.",
            "neg_prompt": "The camera moves backward relative to both the ground and its initial viewing direction.",
            "pos": [
                {
                    "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground_birds_worms_included",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.backward.has_backward_wrt_camera",
                    "type": "pos",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.backward.has_backward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.backward.has_backward_wrt_ground_birds_worms_included",
                    "type": "pos",
                },
            ],
        },
        {
            # "folder": ground_and_camera_folder,
            "folder": ground_and_setup_folder,
            "name": "upward_camera_only_vs_upward_camera_and_ground",
            "pos_question": "Does the camera move upward only relative to its initial viewing direction but not relative to the ground?",
            "neg_question": "Does the camera move upward relative to both the ground and its initial viewing direction?",
            "pos_prompt": "The camera moves upward only relative to its initial viewing direction but not relative to the ground.",
            "neg_prompt": "The camera moves upward relative to both the ground and its initial viewing direction.",
            "pos": [
                {
                    "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground_birds_worms_included",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.upward.has_upward_wrt_camera",
                    "type": "pos",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.upward.has_upward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.upward.has_upward_wrt_ground_birds_worms_included",
                    "type": "pos",
                },
            ],
        },
        {
            # "folder": ground_and_camera_folder,
            "folder": ground_and_setup_folder,
            "name": "downward_camera_only_vs_downward_camera_and_ground",
            "pos_question": "Does the camera move downward only relative to its initial viewing direction but not relative to the ground?",
            "neg_question": "Does the camera move downward relative to both the ground and its initial viewing direction?",
            "pos_prompt": "The camera moves downward only relative to its initial viewing direction but not relative to the ground.",
            "neg_prompt": "The camera moves downward relative to both the ground and its initial viewing direction.",
            "pos": [
                {
                    "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground_birds_worms_included",
                    "type": "neg",
                },
                {
                    "label": "cam_motion.camera_centric_movement.downward.has_downward_wrt_camera",
                    "type": "pos",
                },
            ],
            "neg": [
                {
                    "label": "cam_motion.camera_centric_movement.downward.has_downward_wrt_camera",
                    "type": "pos",
                },
                {
                    "label": "cam_motion.ground_centric_movement.downward.has_downward_wrt_ground_birds_worms_included",
                    "type": "pos",
                },
            ],
        },
    ]

def get_shot_transition_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "has_shot_transition_cam_setup",
            "pos_question": "Does the video include shot transitions?",
            "neg_question": "Is the video free from any shot transitions?",
            "pos_prompt": "A video that includes shot transitions.",
            "neg_prompt": "A video without any shot transitions.",
            "pos": {
                "label": "cam_setup.has_shot_transition_cam_setup",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.has_shot_transition_cam_setup",
                "type": "neg",
            },
        },
    ]

def get_overlays_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "has_overlays",
            "pos_question": "Does the shot contain any on-screen overlays, such as watermarks, titles, subtitles, icons, heads-up displays (HUDs), or framing elements?",
            "neg_question": "Is the video free from any on-screen overlays like watermarks, titles, subtitles, icons, heads-up displays (HUDs), or framing elements?",
            "pos_prompt": "A shot containing on-screen overlays, such as watermarks, titles, subtitles, icons, heads-up displays (HUDs), or framing elements.",
            "neg_prompt": "A shot without any on-screen overlays like watermarks, titles, subtitles, icons, heads-up displays (HUDs), or framing elements.",
            "pos": {
                "label": "cam_setup.has_overlays",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.has_overlays",
                "type": "neg",
            },
        },
    ]

def get_lens_distortion_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "with_lens_distortion",
            "pos_question": "Does this shot contain noticeable barrel or fisheye distortion?",
            "neg_question": "Is this shot free from any noticeable barrel or fisheye distortion?",
            "pos_prompt": "A video with noticeable barrel or fisheye distortion.",
            "neg_prompt": "A video without any noticeable barrel or fisheye distortion.",
            "pos": {
                "label": "cam_setup.lens_distortion.with_lens_distortion",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.lens_distortion.with_lens_distortion",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "fisheye_distortion",
            "pos_question": "Does this shot have a noticeable fisheye lens distortion?",
            "neg_question": "Is this shot free from noticable fisheye lens distortion?",
            "pos_prompt": "A shot with noticable fisheye lens distortion.",
            "neg_prompt": "A shot without noticable fisheye lens distortion.",
            "pos": {
                "label": "cam_setup.lens_distortion.fisheye_distortion",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.lens_distortion.fisheye_distortion",
                "type": "neg",
            },
        },
    ]

def get_playback_speed_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "fast_motion",
            "pos_question": "Is it a fast-motion video with forward playback faster than real-time?",
            "neg_question": "Is it not a fast-motion video with forward playback faster than real-time?",
            "pos_prompt": "A fast-motion video where playback is forward and faster than real-time.",
            "neg_prompt": "A video that is not played at forward and faster than real-time speed.",
            "pos": {
                "label": "cam_setup.video_speed.fast_motion",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.fast_motion",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "fast_motion_without_time_lapse",
            "pos_question": "Is it a fast-motion video with forward playback speed slightly faster than real-time (1x–3x)?",
            "neg_question": "Is it not a fast-motion video with forward playback speed slightly faster than real-time (1x–3x)?",
            "pos_prompt": "A fast-motion video with forward playback speed slightly faster than real-time (1x–3x).",
            "neg_prompt": "A video that is not played at forward and slightly faster than real-time speed (1x–3x).",
            "pos": {
                "label": "cam_setup.video_speed.fast_motion_without_time_lapse",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.fast_motion_without_time_lapse",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "regular_speed",
            "pos_question": "Is the playback forward at real-time speed without noticeable speed-up or slowdown?",
            "neg_question": "Is the playback not forward at real-time speed?",
            "pos_prompt":  "The playback is forward at real-time speed without noticeable speed-up or slowdown.",
            "neg_prompt": "The playback is not forward at real-time speed.",
            "pos": {
                "label": "cam_setup.video_speed.regular_speed",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.regular_speed",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "slow_motion",
            "pos_question": "Is it a slow-motion video with forward playback slower than real-time?",
            "neg_question": "Is it not a slow-motion video with forward playback slower than real-time?",
            "pos_prompt": "A slow-motion video with forward playback speed slower than real-time.",
            "neg_prompt": "A video that is not played at forward and slower than real-time speed.",
            "pos": {
                "label": "cam_setup.video_speed.slow_motion",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.slow_motion",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "stop_motion",
            "pos_question": "Is this a stop-motion video using frame-by-frame changes to simulate motion?",
            "neg_question": "Is this not a stop-motion video using frame-by-frame changes to simulate motion?",
            "pos_prompt":  "A stop-motion video using frame-by-frame changes to simulate motion.",
            "neg_prompt": "A video that does not use stop-motion animation techniques.",
            "pos": {
                "label": "cam_setup.video_speed.stop_motion",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.stop_motion",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "time_lapse",
            "pos_question": "Is this a time-lapse video showing time passing rapidly over a long period?",
            "neg_question": "Is this not a time-lapse video showing time passing rapidly over a long period?",
            "pos_prompt":  "A time-lapse video showing time passing rapidly over a long period.",
            "neg_prompt": "A video that does not show time passing rapidly over a long period.",
            "pos": {
                "label": "cam_setup.video_speed.time_lapse",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.time_lapse",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "speed_ramp",
            "pos_question": "Is there a speed ramp effect where playback speed shifts between fast and slow?",
            "neg_question": "Is there no speed ramp effect where playback speed shifts between fast and slow?",
            "pos_prompt": "A speed ramp effect where playback speed shifts between fast and slow.",
            "neg_prompt": "A video with a constant playback speed without a speed ramp effect.",
            "pos": {
                "label": "cam_setup.video_speed.speed_ramp",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.speed_ramp",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "time_reversed",
            "pos_question": "Is this video played in reverse, with events unfolding backward in time?",
            "neg_question": "Does this video play forward in time?",
            "pos_prompt": "A time-reversed video where events unfold backward in time.",
            "neg_prompt": "A video that plays forward in time.",
            "pos": {
                "label": "cam_setup.video_speed.time_reversed",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.video_speed.time_reversed",
                "type": "neg",
            },
        },
    ]

def get_point_of_view_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "broadcast_pov",
            "pos_question": "Is this a television broadcast-style viewpoint?",
            "neg_question": "Is this not a television broadcast-style viewpoint?",
            "pos_prompt": "A television broadcast-style viewpoint.",
            "neg_prompt": "A video that does not have a television broadcast-style viewpoint.",
            "pos": {
                "label": "cam_setup.point_of_view.broadcast_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.broadcast_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "dashcam_pov",
            "pos_question": "Is this a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead?",
            "neg_question": "Is this not a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead?",
            "pos_prompt": "A forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead.",
            "neg_prompt": "A video that does not have a forward-facing dashcam view from a vehicle-mounted camera, capturing the scene ahead.",
            "pos": {
                "label": "cam_setup.point_of_view.dashcam_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.dashcam_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "drone_pov",
            "pos_question": "Is this a drone POV showing an aerial view?",
            "neg_question": "Is this not a drone POV showing an aerial view?",
            "pos_prompt": "A drone POV showing an aerial view.",
            "neg_prompt": "A video not filmed from a drone's perspective.",
            "pos": {
                "label": "cam_setup.point_of_view.drone_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.drone_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "first_person_pov",
            "pos_question": "Is the scene shown from the first-person perspective, as if through the character's eyes?",
            "neg_question": "Is the scene not shown from a first-person perspective?",
            "pos_prompt": "A first-person POV shot, as if through the character's eyes.",
            "neg_prompt": "A video not filmed from a first-person perspective.",
            "pos": {
                "label": "cam_setup.point_of_view.first_person_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.first_person_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "locked_on_pov",
            "pos_question": "Is the camera physically mounted on an object, keeping its perspective locked to that object?",
            "neg_question": "Is the camera not physically mounted to and keeping its perspective locked to an object?",
            "pos_prompt": "A locked-on POV shot where the camera is mounted to an object, keeping its perspective fixed to that object.",
            "neg_prompt": "A video where the camera is not mounted to and keeping its perspective locked to an object.",
            "pos": {
                "label": "cam_setup.point_of_view.locked_on_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.locked_on_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "overhead_pov",
            "pos_question": "Is the camera positioned directly above the subject for a top-down perspective?",
            "neg_question": "Is the camera not positioned directly above the subject for a top-down perspective?",
            "pos_prompt": "An overhead POV shot where the camera is positioned directly above the subject for a top-down perspective.",
            "neg_prompt": "A video not filmed from an overhead POV where the camera is positioned directly above the subject for a top-down perspective.",
            "pos": {
                "label": "cam_setup.point_of_view.overhead_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.overhead_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "screen_recording_pov",
            "pos_question": "Is this a screen recording of a software or system interface (e.g., menus, windows, toolbars)?",
            "neg_question": "Is this not a screen recording of a software or system interface (e.g., menus, windows, toolbars)?",
            "pos_prompt": "A screen recording of a software or system interface (e.g., menus, windows, toolbars).",
            "neg_prompt": "This is not a screen recording of a software or system interface (e.g., menus, windows, toolbars).",
            "pos": {
                "label": "cam_setup.point_of_view.screen_recording_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.screen_recording_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "selfie_pov",
            "pos_question": "Is the camera facing the person holding it, as in a selfie?",
            "neg_question": "Is the camera not facing the person holding it, as in a selfie?",
            "pos_prompt": "A selfie POV shot where the camera is facing the person holding it.",
            "neg_prompt": "A video not filmed in selfie style with the camera facing its holder.",
            "pos": {
                "label": "cam_setup.point_of_view.selfie_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.selfie_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_full_body_game_pov",
            "pos_question": "Is this a 3D gaming video featuring a third-person perspective with the character's full body visible?",
            "neg_question": "Is this not a third-person gaming video showing the full character?",
            "pos_prompt": "A third-person 3D game video where the entire character is visible on screen.",
            "neg_prompt": "A video that is not a third-person gaming perspective showing the full character.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_full_body_game_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_full_body_game_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_isometric_game_pov",
            "pos_question": "Is this a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective?",
            "neg_question": "Is this not a third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective?",
            "pos_prompt": "A third-person isometric (2.5D) gaming video with a tilted overhead angle showing the environment in a three-quarters perspective.",
            "neg_prompt": "A video that is not a third-person isometric (2.5D) gaming perspective with a tilted overhead angle showing the environment in a three-quarters perspective.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_isometric_game_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_isometric_game_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_over_hip_pov",
            "pos_question": "Is this an over-the-hip third-person view, framing the character from the hip up?",
            "neg_question": "Is this not an over-the-hip third-person view, framing the character from the hip up?",
            "pos_prompt": "A third-person over-the-hip POV shot framing the character from the hip up.",
            "neg_prompt": "A video that is not a third-person over-the-hip POV shot framing the character from the hip up.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_over_hip_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_over_hip_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_over_shoulder_pov",
            "pos_question": "Is this an over-the-shoulder POV where the camera is positioned behind the character, showing their upper body and the scene ahead?",
            "neg_question": "Is this not an over-the-shoulder POV where the camera is positioned behind the character, showing their upper body and the scene ahead?",
            "pos_prompt": "An over-the-shoulder POV where the camera is positioned behind the character, showing their upper body and the scene ahead.",
            "neg_prompt": "A video that is not an over-the-shoulder POV where the camera is positioned behind the character, showing their upper body and the scene ahead.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_over_shoulder_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_over_shoulder_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_side_view_game_pov",
            "pos_question": "Is this a side-view gaming video where the camera is placed to the side, capturing the scene or character in profile?",
            "neg_question": "Is this not a side-view gaming video where the camera is placed to the side, capturing the scene or character in profile?",
            "pos_prompt": "A side-view gaming video where the camera is placed to the side, capturing the scene or character in profile.",
            "neg_prompt": "A video that is not a side-view gaming perspective where the camera is placed to the side, capturing the scene or character in profile.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_side_view_game_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_side_view_game_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "third_person_top_down_game_pov",
            "pos_question": "Is this a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them?",
            "neg_question": "Is this not a gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them?",
            "pos_prompt": "A gaming video with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them.",
            "neg_prompt": "A video that is not a gaming perspective with a top-down or oblique top-down view, where the camera is placed directly above the character and looks down on them.",
            "pos": {
                "label": "cam_setup.point_of_view.third_person_top_down_game_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.third_person_top_down_game_pov",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "objective_pov",
            "pos_question": "Is this an objective, detached perspective where the camera does not represent any character's point of view?",
            "neg_question": "Is this video not shot from a objective, detached perspective?",
            "pos_prompt": "An objective POV shot where the camera captures the scene from a detached, observational perspective.",
            "neg_prompt": "A video that is not filmed from a objective, detached perspective.",
            "pos": {
                "label": "cam_setup.point_of_view.objective_pov",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.point_of_view.objective_pov",
                "type": "neg",
            },
        },
    ]

def get_subject_framing_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_framing_subject",
            "pos_question": "Does the video include one or more salient subjects in the frame at any point (e.g., not just scenery or abstract visuals)?",
            "neg_question": "Does the video not include one or more salient subjects in the frame at any point?",
            "pos_prompt": "The video features one or more salient subjects in the frame at any point (e.g., not just scenery or abstract visuals).",
            "neg_prompt": "A video that does not include one or more salient subjects in the frame at any point.",
            "pos": {
                "label": "cam_setup.subject_framing.is_framing_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.subject_framing.is_framing_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "has_subject_change",
            "pos_question": "Does the subject change in the video, such as appearing, disappearing, or transitioning to another subject?",
            "neg_question": "Does the subject remain the same throughout the video, or is there no subject at all?",
            "pos_prompt": "A shot where the subject changes, including appearances, disappearances, or transitions between subjects.",
            "neg_prompt": "A video where the subject remains the same throughout or there is no subject at all.",
            "pos": {
                "label": "cam_setup.subject_framing.has_subject_change",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.subject_framing.has_subject_change",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "has_single_dominant_subject",
            "pos_question": "Does the video maintain a single dominant subject or group of subjects throughout?",
            "neg_question": "Does the video not maintain a single dominant subject or group of subjects throughout?",
            "pos_prompt": "A video that maintains a single dominant subject or group of subjects throughout.",
            "neg_prompt": "A video that does not maintain a single dominant subject or group of subjects throughout.",
            "pos": {
                "label": "cam_setup.subject_framing.has_single_dominant_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.subject_framing.has_single_dominant_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "has_many_subjects",
            "pos_question": "Are there multiple distinct groups of subjects or more than two salient subjects shown in the video?",
            "neg_question": "Does the video contain no more than one group or two salient subjects?",
            "pos_prompt": "A video containing multiple distinct groups of subjects or more than two salient subjects.",
            "neg_prompt": "A video that contains no more than one group or two salient subjects.",
            "pos": {
                "label": "cam_setup.subject_framing.has_many_subjects",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.subject_framing.has_many_subjects",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "subject_revealing",
            "pos_question": "Does the video include a revealing shot where a subject appears?",
            "neg_question": "Does the video not include a revealing shot where a subject appears?",
            "pos_prompt": "A video that includes a revealing shot where a subject appears.",
            "neg_prompt": "A video that does not include a revealing shot where a subject appears.",
            "pos": {
                "label": "cam_setup.shot_size.subject_revealing",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.subject_revealing",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "subject_disappearing",
            "pos_question": "Does the video show the main subject disappearing or leaving the frame?",
            "neg_question": "Does the video not show the main subject disappearing or leaving the frame?",
            "pos_prompt": "The video shows the main subject disappearing or leaving the frame.",
            "neg_prompt": "The video does not show the main subject disappearing or leaving the frame.",
            "pos": {
                "label": "cam_setup.shot_size.subject_disappearing",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.subject_disappearing",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "subject_switching",
            "pos_question": "Does the main subject change to a different subject?",
            "neg_question": "Does the main subject not change to a different subject?",
            "pos_prompt": "The main subject changes to a different subject.",
            "neg_prompt": "The main subject does not change to a different subject.",
            "pos": {
                "label": "cam_setup.shot_size.subject_switching",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.subject_switching",
                "type": "neg",
            },
        },
    ]


def get_shot_type_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_human_shot",
            "pos_question": "Is the shot focused on human subjects?",
            "neg_question": "Is the shot not focused on human subjects?",
            "pos_prompt": "A shot that primarily focuses on human subjects.",
            "neg_prompt": "A shot that does not primarily focus on human subjects.",
            "pos": {
                "label": "cam_setup.shot_type.is_human_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_human_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_non_human_shot",
            "pos_question": "Is the shot focused on non-human subjects?",
            "neg_question": "Is the shot not focused on non-human subjects?",
            "pos_prompt": "A shot that primarily focuses on non-human subjects.",
            "neg_prompt": "A shot that does not primarily focus on non-human subjects.",
            "pos": {
                "label": "cam_setup.shot_type.is_non_human_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_non_human_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_human_shot",
            "pos_question": "Does the video consistently feature one or two salient human subjects?",
            "neg_question": "Does the video not consistently feature one or two salient human subjects?",
            "pos_prompt": "A video that consistently features one or two salient human subjects.",
            "neg_prompt": "A video that does not consistently feature one or two salient human subjects.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_human_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_human_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_non_human_shot",
            "pos_question": "Does the video consistently feature one or two salient non-human subjects?",
            "neg_question": "Does the video not consistently feature one or two salient non-human subjects?",
            "pos_prompt": "A video that consistently features one or two salient non-human subjects.",
            "neg_prompt": "A video that does not consistently feature one or two salient non-human subjects.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_non_human_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_non_human_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_change_of_subject_shot",
            "pos_question": "Does the video include a subject change, such as a revealing shot where a subject appears, disappears, or transitions to another?",
            "neg_question": "Does the video not include a subject change, such as a revealing shot where a subject appears, disappears, or transitions to another?",
            "pos_prompt": "A video that includes a subject change, such as a revealing shot where a subject appears, disappears, or transitions to another.",
            "neg_prompt": "A video that does not include a subject change, such as a revealing shot where a subject appears, disappears, or transitions to another.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_change_of_subject_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_change_of_subject_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_scenery_shot",
            "pos_question": "Does the video focus on scenery or environment without emphasis on any subjects?",
            "neg_question": "Does the video focus on some salient subjects rather than just scenery?",
            "pos_prompt": "A video that focuses on scenery or environment without emphasis on any subjects.",
            "neg_prompt": "A video that focuses on some salient subjects rather than just scenery.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_scenery_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_scenery_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_clear_subject_dynamic_size_shot",
            "pos_question": "Is there a clear subject, but changes in framing make it hard to classify the shot size?",
            "neg_question": "Does the video not have a clear subject, or does it not have changes in framing that make it hard to classify the shot size?",
            "pos_prompt": "A video with a clear subject that changes in framing, making it hard to classify the shot size.",
            "neg_prompt": "A video that does not have a clear subject, or does not have changes in framing that make it hard to classify the shot size.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_clear_subject_dynamic_size_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_different_subject_in_focus_shot",
            "pos_question": "Does the video feature different subjects, varying in type or framing, making it hard to classify the shot size?",
            "neg_question": "Does the video not feature different subjects (e.g., varying in type or framing) in focus that make it hard to classify the shot size?",
            "pos_prompt": "A video that features different subjects in focus, varying in type or framing, making it hard to classify the shot size.",
            "neg_prompt": "A video that does not feature different subjects (e.g., varying in type or framing) in focus that make it hard to classify the shot size.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_different_subject_in_focus_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_different_subject_in_focus_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_clear_subject_atypical_shot",
            "pos_question": "Does the video feature a clear subject whose anatomy looks unnatural or exaggerated?",
            "neg_question": "Does the video lack a clear subject, or does the subject appear anatomically normal?",
            "pos_prompt": "A video that features a clear subject whose anatomy looks unnatural or exaggerated.",
            "neg_prompt": "A video that lacks a clear subject, or whose subject appears anatomically normal.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_clear_subject_atypical_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_clear_subject_atypical_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_many_subject_one_focus_shot",
            "pos_question": "Does the video feature multiple subjects, but one clearly stands out as the main focus?",
            "neg_question": "Does the video not feature multiple subjects, or does it not have one clearly standing out as the main focus?",
            "pos_prompt": "A video that features multiple subjects, but one clearly stands out as the main focus.",
            "neg_prompt": "A video that does not feature multiple subjects, or does not have one clearly standing out as the main focus.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_many_subject_one_focus_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_many_subject_one_focus_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_many_subject_no_focus_shot",
            "pos_question": "Does the video feature multiple subjects with no clear focus on any one subject?",
            "neg_question": "Does the video not feature multiple subjects, or does it have a clear focus on one subject?",
            "pos_prompt": "A video that features multiple subjects with no clear focus on any one subject.",
            "neg_prompt": "A video that does not feature multiple subjects, or has a clear focus on one subject.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_many_subject_no_focus_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_many_subject_no_focus_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_subject_scene_mismatch_shot",
            "pos_question": "Is there a mismatch between the subject and scene framing that makes it hard to classify the shot size?",
            "neg_question": "Does the video not have a mismatch between the subject and scene framing that makes it hard to classify the shot size?",
            "pos_prompt": "A video that features a subject and scene that do not match in framing, making it hard to classify the shot size.",
            "neg_prompt": "A video that does not feature a subject and scene that do not match in framing, making it hard to classify the shot size.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_subject_scene_mismatch_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_subject_scene_mismatch_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_just_back_and_forth_change_shot",
            "pos_question": "Does the video have a clear subject with back-and-forth changes in shot size?",
            "neg_question": "Does the video not have a clear subject with back-and-forth changes in shot size?",
            "pos_prompt": "A video that has a clear subject with back-and-forth changes in shot size.",
            "neg_prompt": "A video that does not have a clear subject with back-and-forth changes in shot size.",
            "pos": {
                "label": "cam_setup.shot_type.is_just_back_and_forth_change_shot",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_type.is_just_back_and_forth_change_shot",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_shot_size_applicable",
            "pos_question": "Can the shot size be meaningfully determined?",
            "neg_question": "Can the shot size not be meaningfully determined?",
            "pos_prompt": "A video where the shot size can be meaningfully determined.",
            "neg_prompt": "A video where the shot size cannot be meaningfully determined.",
            "pos": {
                "label": "cam_setup.shot_size.is_shot_size_applicable",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_shot_size_applicable",
                "type": "neg",
            },
        },
    ]

def get_shot_size_change_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "shot_size_change",
            "pos_question": "Does the shot size change noticeably throughout the video?",
            "neg_question": "Does the shot size remain constant throughout the video?",
            "pos_prompt": "The shot size changes noticeably throughout the video.",
            "neg_prompt": "The shot size remains constant throughout the video.",
            "pos": {
                "label": "cam_setup.shot_size.shot_size_change",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.shot_size_change",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_change_from_large_to_small",
            "pos_question": "Does the shot size change from a wider to a tighter framing?",
            "neg_question": "Does the shot size not change from a wider to a tighter framing?",
            "pos_prompt": "The shot size changes from a wider to a tighter framing.",
            "neg_prompt": "The shot size does not change from a wider to a tighter framing.",
            "pos": {
                "label": "cam_setup.shot_size.shot_size_change_from_large_to_small",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.shot_size_change_from_large_to_small",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_change_from_small_to_large",
            "pos_question": "Does the shot size change from a tighter to a wider framing?",
            "neg_question": "Does the shot size not change from a tighter to a wider framing?",
            "pos_prompt": "The shot size changes from a tighter to a wider framing.",
            "neg_prompt": "The shot size does not change from a tighter to a wider framing.",
            "pos": {
                "label": "cam_setup.shot_size.shot_size_change_from_small_to_large",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.shot_size_change_from_small_to_large",
                "type": "neg",
            },
        },
    ]

def get_shot_size_start_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_extreme_close_up",
            "pos_question": "Does the video start with an extreme close-up shot that isolates a very small detail of the subject or scene?",
            "neg_question": "Does the video not start with an extreme close-up shot that isolates a very small detail of the subject or scene?",
            "pos_prompt": "A video that starts with an extreme close-up shot, isolating a very small detail of the subject or scene.",
            "neg_prompt": "The video does not start with an extreme close-up shot that isolates a very small detail of the subject or scene.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_extreme_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_close_up",
            "pos_question": "Does the video start with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context?",
            "neg_question": "Does the video not start with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context?",
            "pos_prompt": "A video that starts with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context.",
            "neg_prompt": "A video that does not start with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_medium_close_up",
            "pos_question": "Does the video start with a medium close-up shot that frames the human subject from the chest upward?",
            "neg_question": "Does the video not start with a medium close-up shot that frames the human subject from the chest upward?",
            "pos_prompt": "A video that starts with a medium close-up shot, framing the human subject from the chest upward.",
            "neg_prompt": "The video does not start with a medium close-up shot that frames the human subject from the chest upward.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_medium",
            "pos_question": "Does the video start with a medium shot that frames about half of the human subject?",
            "neg_question": "Does the video not start with a medium shot that frames about half of the human subject?",
            "pos_prompt": "A video that starts with a medium shot, framing about half of the human subject.",
            "neg_prompt": "The video does not start with a medium shot that frames about half of the human subject.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_medium_full",
            "pos_question": "Does the video start with a medium full shot that frames the human subject from mid-thigh (or knee) upward?",
            "neg_question": "Does the video not start with a medium full shot that frames the human subject from mid-thigh (or knee) upward?",
            "pos_prompt": "A video that starts with a medium full shot, framing the human subject from mid-thigh (or knee) upward.",
            "neg_prompt": "The video does not start with a medium full shot that frames the human subject from mid-thigh (or knee) upward.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_medium_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_full",
            "pos_question": "Does the video start with a full shot that frames the entire body of the subject without showing excessive surrounding scenery?",
            "neg_question": "Does the video not start with a full shot that frames the entire body of the subject without showing excessive surrounding scenery?",
            "pos_prompt": "A video that starts with a full shot, framing the entire body of the subject without showing excessive surrounding scenery.",
            "neg_prompt": "The video does not start with a full shot that frames the entire body of the subject without showing excessive surrounding scenery.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_wide",
            "pos_question": "Does the video start with a wide shot of scenery, or frames the entire subject while keeping ample background context?",
            "neg_question": "Does the video not start with a wide shot of scenery, or does not frame the entire subject while keeping ample background context?",
            "pos_prompt": "A video that starts with a wide shot of scenery, or frames the entire subject while keeping ample background context.",
            "neg_prompt": "The video does not start with a wide shot of scenery, or does not frame the entire subject while keeping ample background context.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_wide",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_start_with_extreme_wide",
            "pos_question": "Does the video start with an extreme wide shot that emphasizes the setting over any subjects?",
            "neg_question": "Does the video not start with an extreme wide shot that emphasizes the setting over any subjects?",
            "pos_prompt": "A video that starts with an extreme wide shot, emphasizing the setting over any subjects.",
            "neg_prompt": "The video does not start with an extreme wide shot that emphasizes the setting over any subjects.",
            "pos": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_extreme_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.start_with.shot_size_start_with_extreme_wide",
                "type": "neg",
            },
        },
    ]

def get_shot_size_end_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_extreme_close_up",
            "pos_question": "Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene?",
            "neg_question": "Does the video not end with an extreme close-up shot that isolates a very small detail of the subject or scene?",
            "pos_prompt": "A video that ends with an extreme close-up shot, isolating a very small detail of the subject or scene.",
            "neg_prompt": "The video does not end with an extreme close-up shot that isolates a very small detail of the subject or scene.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_extreme_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_close_up",
            "pos_question": "Does the video end with a close-up shot that highlights a distinct part of the subject while still preserving some surrounding context?",
            "neg_question": "Does the video not end with a close-up shot that highlights a distinct part of the subject while still preserving some surrounding context?",
            "pos_prompt": "A video that ends with a close-up shot, highlighting a distinct part of the subject while still preserving some surrounding context.",
            "neg_prompt": "A video that does not end with a close-up shot that highlights a distinct part of the subject while still preserving some surrounding context.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_medium_close_up",
            "pos_question": "Does the video end with a medium close-up shot that frames the human subject from the chest upward?",
            "neg_question": "Does the video not end with a medium close-up shot that frames the human subject from the chest upward?",
            "pos_prompt": "A video that ends with a medium close-up shot, framing the human subject from the chest upward.",
            "neg_prompt": "The video does not end with a medium close-up shot that frames the human subject from the chest upward.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_medium",
            "pos_question": "Does the video end with a medium shot that frames about half of the subject?",
            "neg_question": "Does the video not end with a medium shot that frames about half of the subject?",
            "pos_prompt": "A video that ends with a medium shot, framing about half of the subject.",
            "neg_prompt": "The video does not end with a medium shot that frames about half of the subject.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_medium_full",
            "pos_question": "Does the video end with a medium full shot that frames the human subject from mid-thigh (or knee) upward?",
            "neg_question": "Does the video not end with a medium full shot that frames the human subject from mid-thigh (or knee) upward?",
            "pos_prompt": "A video that ends with a medium full shot, framing the human subject from mid-thigh (or knee) upward.",
            "neg_prompt": "The video does not end with a medium full shot that frames the human subject from mid-thigh (or knee) upward.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_medium_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_full",
            "pos_question": "Does the video end with a full shot that frames the entire body of the subject without showing excessive surrounding scenery?",
            "neg_question": "Does the video not end with a full shot that frames the entire body of the subject without showing excessive surrounding scenery?",
            "pos_prompt": "A video that ends with a full shot, framing the entire body of the subject without showing excessive surrounding scenery.",
            "neg_prompt": "The video does not end with a full shot that frames the entire body of the subject without showing excessive surrounding scenery.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_wide",
            "pos_question": "Does the video end with a wide shot of scenery, or frames the entire subject while keeping ample background context?",
            "neg_question": "Does the video not end with a wide shot of scenery, or does not frame the entire subject while keeping ample background context?",
            "pos_prompt": "A video that ends with a wide shot of scenery, or frames the entire subject while keeping ample background context.",
            "neg_prompt": "The video does not end with a wide shot of scenery, or does not frame the entire subject while keeping ample background context.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_wide",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_end_with_extreme_wide",
            "pos_question": "Does the video end with an extreme wide shot that emphasizes the setting over any subjects?",
            "neg_question": "Does the video not end with an extreme wide shot that emphasizes the setting over any subjects?",
            "pos_prompt": "A video that ends with an extreme wide shot, emphasizing the setting over any subjects.",
            "neg_prompt": "The video does not end with an extreme wide shot that emphasizes the setting over any subjects.",
            "pos": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_extreme_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.end_with.shot_size_end_with_extreme_wide",
                "type": "neg",
            },
        },
    ]

def get_shot_size_is_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "shot_size_is_extreme_close_up",
            "pos_question": "Does the video maintain an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene?",
            "neg_question": "Does the video not maintain an extreme close-up shot throughout, or does not consistently isolate a very small detail of the subject or scene?",
            "pos_prompt": "A video that maintains an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene.",
            "neg_prompt": "A video that does not maintain an extreme close-up shot throughout, or does not consistently isolate a very small detail of the subject or scene.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_extreme_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_extreme_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_close_up",
            "pos_question": "Does the video maintain a close-up shot throughout, consistently highlighting a distinct part of the subject or scene while still preserving some surrounding context?",
            "neg_question": "Does the video not maintain a close-up shot throughout, or does not consistently highlight a distinct part of the subject or scene while preserving some surrounding context?",
            "pos_prompt": "A video that maintains a close-up shot throughout, consistently highlighting a distinct part of the subject or scene while still preserving some surrounding context.",
            "neg_prompt": "A video that does not maintain a close-up shot throughout, or does not consistently highlight a distinct part of the subject or scene while preserving some surrounding context.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_medium_close_up",
            "pos_question": "Does the video maintain a medium close-up shot throughout, consistently framing the human subject from the chest upward?",
            "neg_question": "Does the video not maintain a medium close-up shot throughout, or does not consistently frame the human subject from the chest upward?",
            "pos_prompt": "A video that maintains a medium close-up shot throughout, consistently framing the human subject from the chest upward.",
            "neg_prompt": "A video that does not maintain a medium close-up shot throughout, or does not consistently frame the human subject from the chest upward.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium_close_up",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium_close_up",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_medium",
            "pos_question": "Does the video maintain a medium shot throughout, consistently framing about half of the human subject?",
            "neg_question": "Does the video not maintain a medium shot throughout, or does not consistently frame about half of the human subject?",
            "pos_prompt": "A video that maintains a medium shot throughout, consistently framing about half of the human subject.",
            "neg_prompt": "A video that does not maintain a medium shot throughout, or does not consistently frame about half of the human subject.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_medium_full",
            "pos_question": "Does the video maintain a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward?",
            "neg_question": "Does the video not maintain a medium full shot throughout, or does not consistently frame the human subject from mid-thigh (or knee) upward?",
            "pos_prompt": "A video that maintains a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward.",
            "neg_prompt": "A video that does not maintain a medium full shot throughout, or does not consistently frame the human subject from mid-thigh (or knee) upward.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_medium_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_full",
            "pos_question": "Does the video maintain a full shot throughout, consistently framing the entire body of the subject without showing excessive surrounding scenery?",
            "neg_question": "Does the video not maintain a full shot throughout, or does not consistently frame the entire body of the subject without showing excessive surrounding scenery?",
            "pos_prompt": "A video that maintains a full shot throughout, consistently framing the entire body of the subject without showing excessive surrounding scenery.",
            "neg_prompt": "A video that does not maintain a full shot throughout, or does not consistently frame the entire body of the subject without showing excessive surrounding scenery.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_full",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_full",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_wide",
            "pos_question": "Does the video maintain a wide shot throughout, consistently showing scenery or framing the entire subject while keeping ample background context?",
            "neg_question": "Does the video not maintain a wide shot throughout, or does not consistently show scenery or frame the entire subject while keeping ample background context?",
            "pos_prompt": "A video that maintains a wide shot throughout, consistently showing scenery or framing the entire subject while keeping ample background context.",
            "neg_prompt": "A video that does not maintain a wide shot throughout, or does not consistently show scenery or frame the entire subject while keeping ample background context.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_wide",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "shot_size_is_extreme_wide",
            "pos_question": "Does the video maintain an extreme wide shot throughout, consistently emphasizing the setting over any subjects?",
            "neg_question": "Does the video not maintain an extreme wide shot throughout, or does not consistently emphasize the setting over any subjects?",
            "pos_prompt": "A video that maintains an extreme wide shot throughout, consistently emphasizing the setting over any subjects.",
            "neg_prompt": "A video that does not maintain an extreme wide shot throughout, or does not consistently emphasize the setting over any subjects.",
            "pos": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_extreme_wide",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.shot_size.is_always.shot_size_is_extreme_wide",
                "type": "neg",
            },
        },
    ]


def get_height_wrt_subject_change_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_subject_height_applicable",
            "pos_question": "Is the camera height relative to the subject clear?",
            "neg_question": "Is the camera height relative to the subject unclear?",
            "pos_prompt": "The camera height relative to the subject is clear.",
            "neg_prompt": "The camera height relative to the subject is unclear.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.is_subject_height_applicable",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.is_subject_height_applicable",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_change",
            "pos_question": "Does the camera's height relative to the subject change significantly, moving between positions above, at level with, or below the subject?",
            "neg_question": "Does the camera's height relative to the subject not change significantly, moving between positions above, at level with, or below the subject?",
            "pos_prompt": "A shot where the camera's height relative to the subject changes significantly, moving between positions above, at level with, or below the subject.",
            "neg_prompt": "A shot where the camera's height relative to the subject does not change significantly, moving between positions above, at level with, or below the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_change_from_high_to_low",
            "pos_question": "Does the camera's height decrease noticeably, transitioning from above to level with the subject or from level to below?",
            "neg_question": "Does the camera's height not decrease noticeably, or not transition from above to level with the subject or from level to below?",
            "pos_prompt": "A shot where the camera's height decreases noticeably, transitioning from above to level with the subject or from level to below.",
            "neg_prompt": "A shot where the camera's height does not decrease noticeably, or does not transition from above to level with the subject or from level to below.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change_from_high_to_low",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change_from_high_to_low",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_change_from_low_to_high",
            "pos_question": "Does the camera's height increase noticeably, transitioning from below to level with the subject or from level to above?",
            "neg_question": "Does the camera's height not increase noticeably, or not transition from below to level with the subject or from level to above?",
            "pos_prompt": "A shot where the camera's height increases noticeably, transitioning from below to level with the subject or from level to above.",
            "neg_prompt": "A shot where the camera's height does not increase noticeably, or does not transition from below to level with the subject or from level to above.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change_from_low_to_high",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.height_wrt_subject_change_from_low_to_high",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_subject_start_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_start_with_above_subject",
            "pos_question": "Does the video start with the camera positioned above the subject?",
            "neg_question": "Does the video not start with the camera positioned above the subject?",
            "pos_prompt": "A video that starts with the camera positioned above the subject.",
            "neg_prompt": "A video that does not start with the camera positioned above the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_above_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_above_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_start_with_at_subject",
            "pos_question": "Does the video start with the camera positioned at the same height as the subject?",
            "neg_question": "Does the video not start with the camera positioned at the same height as the subject?",
            "pos_prompt": "A video that starts with the camera positioned at the same height as the subject.",
            "neg_prompt": "A video that does not start with the camera positioned at the same height as the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_at_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_at_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_start_with_below_subject",
            "pos_question": "Does the video start with the camera positioned below the subject?",
            "neg_question": "Does the video not start with the camera positioned below the subject?",
            "pos_prompt": "A video that starts with the camera positioned below the subject.",
            "neg_prompt": "A video that does not start with the camera positioned below the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_below_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.start_with.height_wrt_subject_start_with_below_subject",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_subject_end_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_end_with_above_subject",
            "pos_question": "Does the video end with the camera positioned above the subject?",
            "neg_question": "Does the video not end with the camera positioned above the subject?",
            "pos_prompt": "A video that ends with the camera positioned above the subject.",
            "neg_prompt": "A video that does not end with the camera positioned above the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_above_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_above_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_end_with_at_subject",
            "pos_question": "Does the video end with the camera positioned at the same height as the subject?",
            "neg_question": "Does the video not end with the camera positioned at the same height as the subject?",
            "pos_prompt": "A video that ends with the camera positioned at the same height as the subject.",
            "neg_prompt": "A video that does not end with the camera positioned at the same height as the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_at_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_at_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_end_with_below_subject",
            "pos_question": "Does the video end with the camera positioned below the subject?",
            "neg_question": "Does the video not end with the camera positioned below the subject?",
            "pos_prompt": "A video that ends with the camera positioned below the subject.",
            "neg_prompt": "A video that does not end with the camera positioned below the subject.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_below_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.end_with.height_wrt_subject_end_with_below_subject",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_subject_is_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_is_above_subject",
            "pos_question": "Is the camera positioned above the subject throughout the video?",
            "neg_question": "Is the camera not positioned above the subject throughout the video?",
            "pos_prompt": "The camera remains positioned above the subject throughout the video.",
            "neg_prompt": "The camera does not remain positioned above the subject throughout the video.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_above_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_above_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_is_at_subject",
            "pos_question": "Is the camera positioned at the same height as the subject throughout the video?",
            "neg_question": "Is the camera not positioned at the same height as the subject throughout the video?",
            "pos_prompt": "The camera remains positioned at the same height as the subject throughout the video.",
            "neg_prompt": "The camera does not remain positioned at the same height as the subject throughout the video.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_at_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_at_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_is_below_subject",
            "pos_question": "Is the camera positioned below the subject throughout the video?",
            "neg_question": "Is the camera not positioned below the subject throughout the video?",
            "pos_prompt": "The camera remains positioned below the subject throughout the video.",
            "neg_prompt": "The camera does not remain positioned below the subject throughout the video.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.is_always.height_wrt_subject_is_below_subject",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_subject_transition_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_above_subject_to_at_subject",
            "pos_question": "Does the camera start noticeably higher than the subject and then move down to their height?",
            "neg_question": "Does the camera not start noticeably higher than the subject or not move down to their height?",
            "pos_prompt": "The camera starts noticeably higher than the subject and then moves down to their height.",
            "neg_prompt": "The camera does not start noticeably higher than the subject or does not move down to their height.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_at_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_above_subject_to_below_subject",
            "pos_question": "Does the camera start noticeably higher than the subject and then move to a position below them?",
            "neg_question": "Does the camera not start noticeably higher than the subject or not move to a position below them?",
            "pos_prompt": "The camera starts noticeably higher than the subject and then moves to a position below them.",
            "neg_prompt": "The camera does not start noticeably higher than the subject or does not move to a position below them.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_above_subject_to_below_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_at_subject_to_above_subject",
            "pos_question": "Does the camera start at the subject's height and then move up to a position above them?",
            "neg_question": "Does the camera not start at the subject's height or not move up to a position above them?",
            "pos_prompt": "The camera starts at the subject's height and then moves up to a position above them.",
            "neg_prompt": "The camera does not start at the subject's height or does not move up to a position above them.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_above_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_at_subject_to_below_subject",
            "pos_question": "Does the camera start at the subject's height and then move down to a lower position than them?",
            "neg_question": "Does the camera not start at the subject's height or not move down to a lower position than them?",
            "pos_prompt": "The camera starts at the subject's height and then moves down to a lower position than them.",
            "neg_prompt": "The camera does not start at the subject's height or does not move down to a lower position than them.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_at_subject_to_below_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_below_subject_to_at_subject",
            "pos_question": "Does the camera start below the subject and then move up to their height?",
            "neg_question": "Does the camera not start below the subject or not move up to their height?",
            "pos_prompt": "The camera starts below the subject and then moves up to their height.",
            "neg_prompt": "The camera does not start below the subject or does not move up to their height.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_at_subject",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_subject_from_below_subject_to_above_subject",
            "pos_question": "Does the camera start below the subject and then move up to a position above them?",
            "neg_question": "Does the camera not start below the subject or not move up to a position above them?",
            "pos_prompt": "The camera starts below the subject and then moves up to a position above them.",
            "neg_prompt": "The camera does not start below the subject or does not move up to a position above them.",
            "pos": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_subject.from_to.height_wrt_subject_from_below_subject_to_above_subject",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_ground_change_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_height_wrt_ground_applicable",
            "pos_question": "Is the camera height relative to the ground or water level clear?",
            "neg_question": "Is the camera height relative to the ground or water level unclear?",
            "pos_prompt": "The camera height relative to the ground or water level is clear.",
            "neg_prompt": "The camera height relative to the ground or water level is unclear.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_height_wrt_ground_applicable",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_height_wrt_ground_applicable",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_change_from_high_to_low",
            "pos_question": "Does the camera height decrease noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground?",
            "neg_question": "Does the camera height not decrease noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground?",
            "pos_prompt": "The camera height decreases noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground.",
            "neg_prompt": "The camera height does not decrease noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.height_wrt_ground_change_from_high_to_low",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.height_wrt_ground_change_from_high_to_low",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_change_from_low_to_high",
            "pos_question": "Does the camera height increase noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground?",
            "neg_question": "Does the camera height not increase noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground?",
            "pos_prompt": "The camera height increases noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground.",
            "neg_prompt": "The camera height does not increase noticeably in relation to the ground, shifting between levels like aerial, overhead, eye, hip, or ground.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.height_wrt_ground_change_from_low_to_high",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.height_wrt_ground_change_from_low_to_high",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "above_water_to_underwater",
            "pos_question": "Does the camera transition from above water to underwater?",
            "neg_question": "Does the camera not transition from above water to underwater?",
            "pos_prompt": "The camera transitions from above water to underwater.",
            "neg_prompt": "The camera does not transition from above water to underwater.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.above_water_to_underwater",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.above_water_to_underwater",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "underwater_to_above_water",
            "pos_question": "Does the camera transition from underwater to above water?",
            "neg_question": "Does the camera not transition from underwater to above water?",
            "pos_prompt": "The camera transitions from underwater to above water.",
            "neg_prompt": "The camera does not transition from underwater to above water.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.underwater_to_above_water",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.underwater_to_above_water",
                "type": "neg",
            },
        },
    ]


def get_height_wrt_ground_start_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_aerial_level",
            "pos_question": "Does the video start with the camera positioned high at an aerial level?",
            "neg_question": "Does the video not start with the camera positioned high at an aerial level?",
            "pos_prompt": "The video starts with the camera positioned high at an aerial level.",
            "neg_prompt": "The video does not start with the camera positioned high at an aerial level.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_aerial_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_aerial_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_overhead_level",
            "pos_question": "Does the video start with the camera at an overhead level, above eye level but below aerial (around second-floor height)?",
            "neg_question": "Does the video not start with the camera at an overhead level, above eye level but below aerial (around second-floor height)?",
            "pos_prompt": "The video starts with the camera at an overhead level, above eye level but below aerial (around second-floor height).",
            "neg_prompt": "The video does not start with the camera at an overhead level, above eye level but below aerial (around second-floor height).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_overhead_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_overhead_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_eye_level",
            "pos_question": "Does the video start with the camera at eye level (roughly at a person's eye height, above the waist)?",
            "neg_question": "Does the video not start with the camera at eye level (roughly at a person's eye height, above the waist)?",
            "pos_prompt": "The video starts with the camera positioned at eye level (roughly at a person's eye height, above the waist).",
            "neg_prompt": "The video does not start with the camera positioned at eye level (roughly at a person's eye height, above the waist).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_eye_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_eye_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_hip_level",
            "pos_question": "Does the video start with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?",
            "neg_question": "Does the video not start with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?",
            "pos_prompt": "The video starts with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.",
            "neg_prompt": "The video does not start with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_hip_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_hip_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_ground_level",
            "pos_question": "Does the video start with the camera at ground level, positioned close to the ground?",
            "neg_question": "Does the video not start with the camera at ground level, positioned close to the ground?",
            "pos_prompt": "The video starts with the camera at ground level, positioned close to the ground.",
            "neg_prompt": "The video does not start with the camera at ground level, positioned close to the ground.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_ground_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_ground_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_water_level",
            "pos_question": "Does the video start with the camera positioned near water level, showing the waterline clearly and not from an aerial view?",
            "neg_question": "Does the video not start with the camera positioned near water level, showing the waterline clearly and not from an aerial view?",
            "pos_prompt": "The video starts with the camera positioned near water level, showing the waterline clearly and not from an aerial view.",
            "neg_prompt": "The video does not start with the camera positioned near water level, showing the waterline clearly and not from an aerial view.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_water_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_water_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_start_with_underwater_level",
            "pos_question": "Does the video start with the camera fully submerged underwater?",
            "neg_question": "Does the video not start with the camera fully submerged underwater?",
            "pos_prompt": "The video starts with the camera fully submerged underwater.",
            "neg_prompt": "The video does not start with the camera fully submerged underwater.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.start_with.height_wrt_ground_start_with_underwater_level",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_ground_end_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_aerial_level",
            "pos_question": "Does the video end with the camera positioned high at an aerial level?",
            "neg_question": "Does the video not end with the camera positioned high at an aerial level?",
            "pos_prompt": "The video ends with the camera positioned high at an aerial level.",
            "neg_prompt": "The video does not end with the camera positioned high at an aerial level.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_aerial_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_aerial_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_overhead_level",
            "pos_question": "Does the video end with the camera at an overhead level, above eye level but below aerial (around second-floor height)?",
            "neg_question": "Does the video not end with the camera at an overhead level, above eye level but below aerial (around second-floor height)?",
            "pos_prompt": "The video ends with the camera at an overhead level, above eye level but below aerial (around second-floor height).",
            "neg_prompt": "The video does not end with the camera at an overhead level, above eye level but below aerial (around second-floor height).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_overhead_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_overhead_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_eye_level",
            "pos_question": "Does the video end with the camera at eye level (roughly at a person's eye height, above the waist)?",
            "neg_question": "Does the video not end with the camera at eye level (roughly at a person's eye height, above the waist)?",
            "pos_prompt": "The video ends with the camera positioned at eye level (roughly at a person's eye height, above the waist).",
            "neg_prompt": "The video does not end with the camera positioned at eye level (roughly at a person's eye height, above the waist).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_eye_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_eye_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_hip_level",
            "pos_question": "Does the video end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?",
            "neg_question": "Does the video not end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?",
            "pos_prompt": "The video ends with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.",
            "neg_prompt": "The video does not end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_hip_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_hip_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_ground_level",
            "pos_question": "Does the video end with the camera at ground level, positioned close to the ground?",
            "neg_question": "Does the video not end with the camera at ground level, positioned close to the ground?",
            "pos_prompt": "The video ends with the camera at ground level, positioned close to the ground.",
            "neg_prompt": "The video does not end with the camera at ground level, positioned close to the ground.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_ground_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_ground_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_water_level",
            "pos_question": "Does the video end with the camera near water level, showing the waterline clearly and not from an aerial view?",
            "neg_question": "Does the video not end with the camera near water level, showing the waterline clearly and not from an aerial view?",
            "pos_prompt": "The video ends with the camera positioned near water level, showing the waterline clearly and not from an aerial view.",
            "neg_prompt": "The video does not end with the camera positioned near water level, showing the waterline clearly and not from an aerial view.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_water_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_water_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_end_with_underwater_level",
            "pos_question": "Does the video end with the camera fully submerged underwater?",
            "neg_question": "Does the video not end with the camera fully submerged underwater?",
            "pos_prompt": "The video ends with the camera fully submerged underwater.",
            "neg_prompt": "The video does not end with the camera fully submerged underwater.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.end_with.height_wrt_ground_end_with_underwater_level",
                "type": "neg",
            },
        },
    ]

def get_height_wrt_ground_is_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_aerial_level",
            "pos_question": "Is the camera positioned at an aerial level throughout the video?",
            "neg_question": "Is the camera not positioned at an aerial level throughout the video?",
            "pos_prompt": "The camera remains at an aerial level height throughout the video.",
            "neg_prompt": "The camera does not remain at an aerial level height throughout the video.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_aerial_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_aerial_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_overhead_level",
            "pos_question": "Is the camera positioned at an overhead level throughout the video, positioned above eye level but below aerial (around second-floor height)?",
            "neg_question": "Is the camera not positioned at an overhead level throughout the video, positioned above eye level but below aerial (around second-floor height)?",
            "pos_prompt": "The camera is positioned at an overhead level throughout the video, positioned above eye level but below aerial (around second-floor height).",
            "neg_prompt": "The camera is not positioned at an overhead level throughout the video, positioned above eye level but below aerial (around second-floor height).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_overhead_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_overhead_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_eye_level",
            "pos_question": "Is the camera positioned at eye level throughout the video (roughly at a person's eye height, above the waist)?",
            "neg_question": "Is the camera not positioned at eye level throughout the video (roughly at a person's eye height, above the waist)?",
            "pos_prompt": "The camera is positioned at eye level throughout the video (roughly at a person's eye height, above the waist).",
            "neg_prompt": "The camera is not positioned at eye level throughout the video (roughly at a person's eye height, above the waist).",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_eye_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_eye_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_hip_level",
            "pos_question": "Is the camera positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present?",
            "neg_question": "Is the camera not positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present?",
            "pos_prompt": "The camera is positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present.",
            "neg_prompt": "The camera is not positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_hip_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_hip_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_ground_level",
            "pos_question": "Is the camera positioned at ground level throughout the video, positioned close to the ground?",
            "neg_question": "Is the camera not positioned at ground level throughout the video, positioned close to the ground?",
            "pos_prompt": "The camera is positioned at ground level throughout the video, positioned close to the ground.",
            "neg_prompt": "The camera is not positioned at ground level throughout the video, positioned close to the ground.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_ground_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_ground_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_water_level",
            "pos_question": "Is the camera positioned at water level throughout the video, showing the waterline clearly and not from an aerial view?",
            "neg_question": "Is the camera not positioned at water level throughout the video, showing the waterline clearly and not from an aerial view?",
            "pos_prompt": "The camera is positioned at water level throughout the video, showing the waterline clearly and not from an aerial view.",
            "neg_prompt": "The camera is not positioned at water level throughout the video, showing the waterline clearly and not from an aerial view.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_water_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_water_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "height_wrt_ground_is_underwater_level",
            "pos_question": "Is the camera fully submerged underwater throughout the video?",
            "neg_question": "Is the camera not fully submerged underwater throughout the video?",
            "pos_prompt": "The camera is fully submerged underwater throughout the video.",
            "neg_prompt": "The camera is not fully submerged underwater throughout the video.",
            "pos": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.height_wrt_ground.is_always.height_wrt_ground_is_underwater_level",
                "type": "neg",
            },
        },
    ]

def get_camera_angle_change_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_camera_angle_applicable",
            "pos_question": "Is the camera angle relative to the ground clear?",
            "neg_question": "Is the camera angle relative to the ground unclear?",
            "pos_prompt": "The camera angle relative to the ground is clear.",
            "neg_prompt": "The camera angle relative to the ground is unclear.",
            "pos": {
                "label": "cam_setup.angle.is_camera_angle_applicable",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_camera_angle_applicable",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_change",
            "pos_question": "Does the camera angle change significantly relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view?",
            "neg_question": "Does the camera angle not change significantly relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view?",
            "pos_prompt": "A shot where the camera angle changes significantly relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view.",
            "neg_prompt": "A shot where the camera angle does not change significantly relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view.",
            "pos": {
                "label": "cam_setup.angle.camera_angle_change",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.camera_angle_change",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_change_from_high_to_low",
            "pos_question": "Does the camera angle decrease noticeably relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view?",
            "neg_question": "Does the camera angle not decrease noticeably relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view?",
            "pos_prompt": "A shot where the camera angle decreases noticeably relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view.",
            "neg_prompt": "A shot where the camera angle does not decrease noticeably relative to the ground, moving between bird's eye, high angle, level, low angle, or worm's eye view.",
            "pos": {
                "label": "cam_setup.angle.camera_angle_change_from_high_to_low",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.camera_angle_change_from_high_to_low",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_change_from_low_to_high",
            "pos_question": "Does the camera angle increase noticeably relative to the ground, moving between worm's eye, low angle, level, high angle, or bird's eye view?",
            "neg_question": "Does the camera angle not increase noticeably relative to the ground, moving between worm's eye, low angle, level, high angle, or bird's eye view?",
            "pos_prompt": "A shot where the camera angle increases noticeably relative to the ground, moving between worm's eye, low angle, level, high angle, or bird's eye view.",
            "neg_prompt": "A shot where the camera angle does not increase noticeably relative to the ground, moving between worm's eye, low angle, level, high angle, or bird's eye view.",
            "pos": {
                "label": "cam_setup.angle.camera_angle_change_from_low_to_high",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.camera_angle_change_from_low_to_high",
                "type": "neg",
            },
        },
    ]

def get_dutch_angle_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_dutch_angle",
            "pos_question": "Is there a Dutch (canted) angle of more than 15 degrees present at any point in the video?",
            "neg_question": "Is there no Dutch (canted) angle of more than 15 degrees present at any point in the video?",
            "pos_prompt": "There is a Dutch (canted) angle of more than 15 degrees present at any point in the video.",
            "neg_prompt": "There is no Dutch (canted) angle of more than 15 degrees present at any point in the video.",
            "pos": {
                "label": "cam_setup.angle.is_dutch_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_dutch_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_dutch_angle_fixed",
            "pos_question": "Does the degree of the Dutch (canted) angle stay the same throughout the video?",
            "neg_question": "Does the degree of the Dutch (canted) angle not stay the same throughout the video?",
            "pos_prompt": "The degree of the Dutch (canted) angle stays the same throughout the video.",
            "neg_prompt": "There is no obvious Dutch (canted) angle of more than 15 degrees present, or the degree of the Dutch (canted) angle varies throughout the video.",
            "pos": {
                "label": "cam_setup.angle.is_dutch_angle_fixed",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_dutch_angle_fixed",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_dutch_angle_varying",
            "pos_question": "Does the degree of the Dutch (canted) angle shift throughout the video?",
            "neg_question": "Does the degree of the Dutch (canted) angle not shift throughout the video?",
            "pos_prompt": "There is a Dutch (canted) angle in the video, and its degree varies.",
            "neg_prompt": "There is no Dutch (canted) angle in the video, or the degree of the Dutch (canted) angle remains constant.",
            "pos": {
                "label": "cam_setup.angle.is_dutch_angle_varying",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_dutch_angle_varying",
                "type": "neg",
            },
        },
    ]

def get_camera_angle_start_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "camera_angle_start_with_bird_eye_angle",
            "pos_question": "Does the video start with the camera at a bird's eye angle, looking straight down from above?",
            "neg_question": "Does the video not start with the camera at a bird's eye angle, looking straight down from above?",
            "pos_prompt": "A video that starts with the camera at a bird's eye angle, looking straight down from above.",
            "neg_prompt": "A video that does not start with the camera at a bird's eye angle, looking straight down from above.",
            "pos": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_bird_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_bird_eye_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_start_with_high_angle",
            "pos_question": "Does the video start with the camera at a high angle, looking downward compared to a level angle but not directly top-down?",
            "neg_question": "Does the video not start with the camera at a high angle, looking downward compared to a level angle but not directly top-down?",
            "pos_prompt": "A video that starts with the camera at a high angle, looking downward compared to a level angle but not directly top-down.",
            "neg_prompt": "A video that does not start with the camera at a high angle, looking downward compared to a level angle but not directly top-down.",
            "pos": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_high_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_high_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_start_with_level_angle",
            "pos_question": "Does the video start with the camera at a level angle, parallel to the ground regardless of Dutch angle?",
            "neg_question": "Does the video not start with the camera at a level angle, parallel to the ground regardless of Dutch angle?",
            "pos_prompt": "A video that starts with the camera at a level angle, parallel to the ground regardless of Dutch angle.",
            "neg_prompt": "A video that does not start with the camera at a level angle, parallel to the ground regardless of Dutch angle.",
            "pos": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_level_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_level_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_start_with_low_angle",
            "pos_question": "Does the video start with the camera at a low angle, looking upward compared to a level angle but not directly from below?",
            "neg_question": "Does the video not start with the camera at a low angle, looking upward compared to a level angle but not directly from below?",
            "pos_prompt": "A video that starts with the camera at a low angle, looking upward compared to a level angle but not directly from below.",
            "neg_prompt": "A video that does not start with the camera at a low angle, looking upward compared to a level angle but not directly from below.",
            "pos": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_low_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_low_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_start_with_worm_eye_angle",
            "pos_question": "Does the video start with the camera at a worm's eye angle, looking straight up from below?",
            "neg_question": "Does the video not start with the camera at a worm's eye angle, looking straight up from below?",
            "pos_prompt": "A video that starts with the camera at a worm's eye angle, looking straight up from below.",
            "neg_prompt": "A video that does not start with the camera at a worm's eye angle, looking straight up from below.",
            "pos": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.start_with.camera_angle_start_with_worm_eye_angle",
                "type": "neg",
            },
        },
    ]

def get_camera_angle_end_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "camera_angle_end_with_bird_eye_angle",
            "pos_question": "Does the video end with the camera at a bird's eye angle, looking straight down from above?",
            "neg_question": "Does the video not end with the camera at a bird's eye angle, looking straight down from above?",
            "pos_prompt": "The video ends with the camera at a bird's eye angle, looking straight down from above.",
            "neg_prompt": "The video does not end with the camera at a bird's eye angle, looking straight down from above.",
            "pos": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_bird_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_bird_eye_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_end_with_high_angle",
            "pos_question": "Does the video end with the camera at a high angle, looking downward compared to a level angle but not directly top-down?",
            "neg_question": "Does the video not end with the camera at a high angle, looking downward compared to a level angle but not directly top-down?",
            "pos_prompt": "The video ends with the camera at a high angle, looking downward compared to a level angle but not directly top-down.",
            "neg_prompt": "The video does not end with the camera at a high angle, looking downward compared to a level angle but not directly top-down.",
            "pos": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_high_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_high_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_end_with_level_angle",
            "pos_question": "Does the video end with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle?",
            "neg_question": "Does the video not end with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle?",
            "pos_prompt": "The video ends with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle.",
            "neg_prompt": "The video does not end with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle.",
            "pos": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_level_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_level_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_end_with_low_angle",
            "pos_question": "Does the video end with the camera at a low angle, looking upward compared to a level angle but not directly from below?",
            "neg_question": "Does the video not end with the camera at a low angle, looking upward compared to a level angle but not directly from below?",
            "pos_prompt": "The video ends with the camera at a low angle, looking upward compared to a level angle but not directly from below.",
            "neg_prompt": "The video does not end with the camera at a low angle, looking upward compared to a level angle but not directly from below.",
            "pos": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_low_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_low_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_end_with_worm_eye_angle",
            "pos_question": "Does the video end with the camera at a worm's eye angle, looking straight up from below?",
            "neg_question": "Does the video not end with the camera at a worm's eye angle, looking straight up from below?",
            "pos_prompt": "The video ends with the camera at a worm's eye angle, looking straight up from below.",
            "neg_prompt": "The video does not end with the camera at a worm's eye angle, looking straight up from below.",
            "pos": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.end_with.camera_angle_end_with_worm_eye_angle",
                "type": "neg",
            },
        },
    ]

def get_camera_angle_is_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "camera_angle_is_bird_eye_angle",
            "pos_question": "Does the camera maintain a bird's eye angle throughout, consistently looking straight down from above?",
            "neg_question": "Does the camera not maintain a bird's eye angle or consistently look straight down from above throughout?",
            "pos_prompt": "The camera maintains a bird's eye angle throughout, consistently looking straight down from above.",
            "neg_prompt": "The camera does not maintain a bird's eye angle or consistently look straight down from above throughout.",
            "pos": {
                "label": "cam_setup.angle.is_always.camera_angle_is_bird_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_always.camera_angle_is_bird_eye_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_is_high_angle",
            "pos_question": "Does the camera maintain a high angle throughout, consistently looking downward compared to a level angle but not directly top-down?",
            "neg_question": "Does the camera not maintain a high angle or consistently look downward (not top-down) throughout?",
            "pos_prompt": "The camera maintains a high angle throughout, consistently looking downward compared to a level angle but not directly top-down.",
            "neg_prompt": "The camera does not stay at a high angle or consistently look downward (not top-down) throughout.",
            "pos": {
                "label": "cam_setup.angle.is_always.camera_angle_is_high_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_always.camera_angle_is_high_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_is_level_angle",
            "pos_question": "Does the camera maintain a level angle parallel to the ground regardless of Dutch angle throughout the video?",
            "neg_question": "Does the camera not maintain a level angle parallel to the ground (regardless of Dutch angle) throughout the video?",
            "pos_prompt": "The camera maintains a level angle parallel to the ground regardless of Dutch angle throughout the video.",
            "neg_prompt": "The camera does not maintain a level angle parallel to the ground (regardless of Dutch angle) throughout the video.",
            "pos": {
                "label": "cam_setup.angle.is_always.camera_angle_is_level_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_always.camera_angle_is_level_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_is_low_angle",
            "pos_question": "Does the camera maintain a low angle throughout, consistently looking upward compared to a level angle but not directly bottom-up?",
            "neg_question": "Does the camera not maintain a low angle or consistently look upward (not bottom-up) throughout?",
            "pos_prompt": "The camera maintains a low angle throughout, consistently looking upward compared to a level angle but not directly bottom-up.",
            "neg_prompt": "The camera does not maintain a low angle or consistently look upward (not bottom-up) throughout.",
            "pos": {
                "label": "cam_setup.angle.is_always.camera_angle_is_low_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_always.camera_angle_is_low_angle",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_is_worm_eye_angle",
            "pos_question": "Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below?",
            "neg_question": "Does the camera not maintain a worm's eye angle or consistently look straight up from below throughout?",
            "pos_prompt": "The camera maintains a worm's eye angle throughout, consistently looking straight up from below.",
            "neg_prompt": "The camera does not maintain a worm's eye angle or consistently look straight up from below throughout.",
            "pos": {
                "label": "cam_setup.angle.is_always.camera_angle_is_worm_eye_angle",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.is_always.camera_angle_is_worm_eye_angle",
                "type": "neg",
            },
        },
    ]

def get_camera_angle_transition_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "camera_angle_from_high_to_level",
            "pos_question": "Does the video start with the camera at a high angle and transition to a level angle?",
            "neg_question": "Does the video not start with the camera at a high angle or not transition to a level angle?",
            "pos_prompt": "The video starts with the camera at a high angle and transitions to a level angle.",
            "neg_prompt": "The video does not start with the camera at a high angle or does not transition to a level angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_high_to_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_high_to_level",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_from_high_to_low",
            "pos_question": "Does the video start with the camera at a high angle and transition to a low angle?",
            "neg_question": "Does the video not start with the camera at a high angle or not transition to a low angle?",
            "pos_prompt": "The video starts with the camera at a high angle and transitions to a low angle.",
            "neg_prompt": "The video does not start with the camera at a high angle or does not transition to a low angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_high_to_low",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_high_to_low",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_from_level_to_high",
            "pos_question": "Does the video start with the camera at a level angle and transition to a high angle?",
            "neg_question": "Does the video not start with the camera at a level angle or not transition to a high angle?",
            "pos_prompt": "The video starts with the camera at a level angle and transitions to a high angle.",
            "neg_prompt": "The video does not start with the camera at a level angle or does not transition to a high angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_level_to_high",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_level_to_high",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_from_level_to_low",
            "pos_question": "Does the video start with the camera at a level angle and transition to a low angle?",
            "neg_question": "Does the video not start with the camera at a level angle or not transition to a low angle?",
            "pos_prompt": "The video starts with the camera at a level angle and transitions to a low angle.",
            "neg_prompt": "The video does not start with the camera at a level angle or does not transition to a low angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_level_to_low",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_level_to_low",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_from_low_to_high",
            "pos_question": "Does the video start with the camera at a low angle and transition to a high angle?",
            "neg_question": "Does the video not start with the camera at a low angle or not transition to a high angle?",
            "pos_prompt": "The video starts with the camera at a low angle and transitions to a high angle.",
            "neg_prompt": "The video does not start with the camera at a low angle or does not transition to a high angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_low_to_high",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_low_to_high",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "camera_angle_from_low_to_level",
            "pos_question": "Does the video start with the camera at a low angle and transition to a level angle?",
            "neg_question": "Does the video not start with the camera at a low angle or not transition to a level angle?",
            "pos_prompt": "The video starts with the camera at a low angle and transitions to a level angle.",
            "neg_prompt": "The video does not start with the camera at a low angle or does not transition to a level angle.",
            "pos": {
                "label": "cam_setup.angle.from_to.camera_angle_from_low_to_level",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.angle.from_to.camera_angle_from_low_to_level",
                "type": "neg",
            },
        },
    ]

def get_depth_of_field_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "is_focus_applicable",
            "pos_question": "Can the camera's depth of field be perceived or inferred from the video?",
            "neg_question": "Can the camera's depth of field not be easily perceived or inferred from the video?",
            "pos_prompt": "The camera's depth of field can be perceived or inferred from the video.",
            "neg_prompt": "The camera's depth of field cannot be easily perceived or inferred from the video.",
            "pos": {
                "label": "cam_setup.depth_of_field.is_focus_applicable",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.depth_of_field.is_focus_applicable",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_deep_focus",
            "pos_question": "Does the camera use a deep depth of field with distant details remaining sharp?",
            "neg_question": "Does the camera not use a deep depth of field with distant details remaining sharp?",
            "pos_prompt": "The camera uses a deep depth of field with distant details remaining sharp.",
            "neg_prompt": "The camera does not use a deep depth of field with distant details remaining sharp.",
            "pos": {
                "label": "cam_setup.depth_of_field.is_deep_focus",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.depth_of_field.is_deep_focus",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_shallow_focus",
            "pos_question": "Is the camera using shallow depth of field, with a limited but noticeable range of space in focus?",
            "neg_question": "Is the camera not using shallow depth of field, with a limited but noticeable range of space in focus?",
            "pos_prompt": "The camera uses shallow depth of field, with a limited but noticeable range of space in focus.",
            "neg_prompt": "The camera does not use shallow depth of field, with a limited but noticeable range of space in focus.",
            "pos": {
                "label": "cam_setup.depth_of_field.is_shallow_focus",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.depth_of_field.is_shallow_focus",
                "type": "neg",
            },
        },
        {
            "folder": setup_folder,
            "name": "is_ultra_shallow_focus",
            "pos_question": "Is the camera using extremely shallow depth of field, with only a narrow plane in focus?",
            "neg_question": "Is the camera not using extremely shallow depth of field, with only a narrow plane in focus?",
            "pos_prompt": "The camera uses extremely shallow depth of field, with only a narrow plane in focus.",
            "neg_prompt": "The camera does not use extremely shallow depth of field, with only a narrow plane in focus.",
            "pos": {
                "label": "cam_setup.depth_of_field.is_ultra_shallow_focus",
                "type": "pos",
            },
            "neg": {
                "label": "cam_setup.depth_of_field.is_ultra_shallow_focus",
                "type": "neg",
            },
        },
    ]

def get_focus_is_always_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "focus_is_always_background",
            "pos_question": "Is the camera consistently focused on the background using a shallow depth of field?",
            "neg_question": "Is the camera not consistently focused on the background using a shallow depth of field?",
            "pos_prompt": "The camera remains focused on the background using a shallow depth of field.",
            "neg_prompt": "The camera does not remain focused on the background using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.is_always.focus_is_background",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.is_always.focus_is_background",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_is_always_foreground",
            "pos_question": "Is the camera consistently focused on the foreground using a shallow depth of field?",
            "neg_question": "Is the camera not consistently focused on the foreground using a shallow depth of field?",
            "pos_prompt": "The camera remains focused on the foreground using a shallow depth of field.",
            "neg_prompt": "The camera does not remain focused on the foreground using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.is_always.focus_is_foreground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.is_always.focus_is_foreground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_is_always_middle_ground",
            "pos_question": "Is the camera consistently focused on the middleground, keeping the foreground and background blurred?",
            "neg_question": "Is the camera not consistently focused on the middleground, keeping the foreground and background blurred?",
            "pos_prompt": "The camera remains focused on the middleground, keeping the foreground and background blurred.",
            "neg_prompt": "The camera does not remain focused on the middleground, keeping the foreground and background blurred.",
            "pos": {
                "label": "cam_setup.focus.is_always.focus_is_middle_ground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.is_always.focus_is_middle_ground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_is_always_out_of_focus",
            "pos_question": "Is the camera consistently out of focus throughout?",
            "neg_question": "Is the camera not consistently out of focus throughout?",
            "pos_prompt": "The camera remains out of focus throughout.",
            "neg_prompt": "The camera does not remain out of focus throughout.",
            "pos": {
                "label": "cam_setup.focus.is_always.focus_is_out_of_focus",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.is_always.focus_is_out_of_focus",
                "type": "neg"
            }
        }
    ]

def get_focus_start_with_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "focus_start_with_background",
            "pos_question": "Does the video start with the camera focusing on the background, using a shallow depth of field?",
            "neg_question": "Does the video not start with the camera focusing on the background, using a shallow depth of field?",
            "pos_prompt": "The video starts with the camera focusing on the background, using a shallow depth of field.",
            "neg_prompt": "The video does not start with the camera focusing on the background, using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.start_with.focus_start_with_background",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.start_with.focus_start_with_background",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_start_with_foreground",
            "pos_question": "Does the video start with the camera focusing on the foreground, using a shallow depth of field?",
            "neg_question": "Does the video not start with the camera focusing on the foreground, using a shallow depth of field?",
            "pos_prompt": "The video starts with the camera focusing on the foreground, using a shallow depth of field.",
            "neg_prompt": "The video does not start with the camera focusing on the foreground, using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.start_with.focus_start_with_foreground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.start_with.focus_start_with_foreground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_start_with_middle_ground",
            "pos_question": "Does the video start with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background?",
            "neg_question": "Does the video not start with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background?",
            "pos_prompt": "The video starts with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background.",
            "neg_prompt": "The video does not start with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background.",
            "pos": {
                "label": "cam_setup.focus.start_with.focus_start_with_middle_ground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.start_with.focus_start_with_middle_ground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_start_with_out_of_focus",
            "pos_question": "Does the video start with the camera completely out of focus?",
            "neg_question": "Does the video not start with the camera completely out of focus?",
            "pos_prompt": "The video starts with the camera completely out of focus.",
            "neg_prompt": "The video does not start with the camera completely out of focus.",
            "pos": {
                "label": "cam_setup.focus.start_with.focus_start_with_out_of_focus",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.start_with.focus_start_with_out_of_focus",
                "type": "neg"
            }
        }
    ]

def get_focus_end_with_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "focus_end_with_background",
            "pos_question": "Does the video end with the camera focusing on the background, using a shallow depth of field?",
            "neg_question": "Does the video not end with the camera focusing on the background, using a shallow depth of field?",
            "pos_prompt": "The video ends with the camera focusing on the background, using a shallow depth of field.",
            "neg_prompt": "The video does not end with the camera focusing on the background, using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.end_with.focus_end_with_background",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.end_with.focus_end_with_background",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_end_with_foreground",
            "pos_question": "Does the video end with the camera focusing on the foreground, using a shallow depth of field?",
            "neg_question": "Does the video not end with the camera focusing on the foreground, using a shallow depth of field?",
            "pos_prompt": "The video ends with the camera focusing on the foreground, using a shallow depth of field.",
            "neg_prompt": "The video does not end with the camera focusing on the foreground, using a shallow depth of field.",
            "pos": {
                "label": "cam_setup.focus.end_with.focus_end_with_foreground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.end_with.focus_end_with_foreground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_end_with_middle_ground",
            "pos_question": "Does the video end with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background?",
            "neg_question": "Does the video not end with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background?",
            "pos_prompt": "The video ends with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background.",
            "neg_prompt": "The video does not end with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background.",
            "pos": {
                "label": "cam_setup.focus.end_with.focus_end_with_middle_ground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.end_with.focus_end_with_middle_ground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_end_with_out_of_focus",
            "pos_question": "Does the video end with the camera completely out of focus?",
            "neg_question": "Does the video not end with the camera completely out of focus?",
            "pos_prompt": "The video ends with the camera completely out of focus.",
            "neg_prompt": "The video does not end with the camera completely out of focus.",
            "pos": {
                "label": "cam_setup.focus.end_with.focus_end_with_out_of_focus",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.end_with.focus_end_with_out_of_focus",
                "type": "neg"
            }
        }
    ]

def get_focus_from_to_tasks(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": setup_folder,
            "name": "focus_from_background_to_foreground",
            "pos_question": "Does the video start with the camera focused on the background and then shift the focus to the foreground?",
            "neg_question": "Does the video either not start with the focus on the background, or not shift the focus to the foreground?",
            "pos_prompt": "The video starts with the camera focused on the background and then shifts the focus to the foreground.",
            "neg_prompt": "The video either does not start with the focus on the background, or does not shift the focus to the foreground.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_background_to_foreground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_background_to_foreground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_from_background_to_middle_ground",
            "pos_question": "Does the video start with the camera focused on the background and then shift the focus to the middleground?",
            "neg_question": "Does the video either not start with the focus on the background, or not shift the focus to the middleground?",
            "pos_prompt": "The video starts with the camera focused on the background and then shifts the focus to the middleground.",
            "neg_prompt": "The video either does not start with the focus on the background, or does not shift the focus to the middleground.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_background_to_middle_ground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_background_to_middle_ground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_from_foreground_to_background",
            "pos_question": "Does the video start with the camera focused on the foreground and then shift the focus to the background?",
            "neg_question": "Does the video either not start with the focus on the foreground, or not shift the focus to the background?",
            "pos_prompt": "The video starts with the camera focused on the foreground and then shifts the focus to the background.",
            "neg_prompt": "The video either does not start with the focus on the foreground, or does not shift the focus to the background.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_foreground_to_background",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_foreground_to_background",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_from_foreground_to_middle_ground",
            "pos_question": "Does the video start with the camera focused on the foreground and then shift the focus to the middleground?",
            "neg_question": "Does the video either not start with the focus on the foreground, or not shift the focus to the middleground?",
            "pos_prompt": "The video starts with the camera focused on the foreground and then shifts the focus to the middleground.",
            "neg_prompt": "The video either does not start with the focus on the foreground, or does not shift the focus to the middleground.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_foreground_to_middle_ground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_foreground_to_middle_ground",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_from_middle_ground_to_background",
            "pos_question": "Does the video start with the camera focused on the middleground and then shift the focus to the background?",
            "neg_question": "Does the video either not start with the focus on the middleground, or not shift the focus to the background?",
            "pos_prompt": "The video starts with the camera focused on the middleground and then shifts the focus to the background.",
            "neg_prompt": "The video either does not start with the focus on the middleground, or does not shift the focus to the background.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_middle_ground_to_background",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_middle_ground_to_background",
                "type": "neg"
            }
        },
        {
            "folder": setup_folder,
            "name": "focus_from_middle_ground_to_foreground",
            "pos_question": "Does the video start with the camera focused on the middleground and then shift the focus to the foreground?",
            "neg_question": "Does the video either not start with the focus on the middleground, or not shift the focus to the foreground?",
            "pos_prompt": "The video starts with the camera focused on the middleground and then shifts the focus to the foreground.",
            "neg_prompt": "The video either does not start with the focus on the middleground, or does not shift the focus to the foreground.",
            "pos": {
                "label": "cam_setup.focus.from_to.focus_from_middle_ground_to_foreground",
                "type": "pos"
            },
            "neg": {
                "label": "cam_setup.focus.from_to.focus_from_middle_ground_to_foreground",
                "type": "neg"
            }
        }
    ]

def get_motion_pairwise_labels(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER,
                               ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER,
                               ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER):
    return {
        "movement_and_steadiness": get_movement_and_steadiness_tasks(ground_only_folder=ground_only_folder),
        "scene_dynamics": get_scene_dynamics_tasks(ground_and_camera_folder=ground_and_camera_folder, ground_only_folder=ground_only_folder),
        "camera_movement_speed": get_camera_movement_speed_tasks(ground_only_folder=ground_only_folder),
        "translation_direction": get_translation_direction_tasks(ground_only_folder=ground_only_folder, ground_and_setup_folder=ground_and_setup_folder),
        "rotation_direction": get_rotation_direction_tasks(ground_only_folder=ground_only_folder),
        "object_centric_direction": get_object_centric_direction_tasks(ground_only_folder=ground_only_folder),
        "intrinsic_direction": get_intrinsic_direction_tasks(ground_only_folder=ground_only_folder),
        "instrinsic_vs_extrinsic": get_instrinsic_vs_extrinsic_tasks(ground_and_camera_folder=ground_and_camera_folder),
        "rotation_vs_translation": get_rotation_vs_translation_tasks(ground_only_folder=ground_only_folder, ground_and_setup_folder=ground_and_setup_folder, ground_and_camera_folder=ground_and_camera_folder),
        "has_intrinsic_change": get_has_intrinsic_change_tasks(ground_only_folder=ground_only_folder),
        "has_translation": get_has_translation_tasks(ground_and_setup_folder=ground_and_setup_folder, ground_only_folder=ground_only_folder),
        "has_rotation": get_has_rotation_tasks(ground_only_folder=ground_only_folder),
        "has_arc_crane": get_has_arc_crane_tasks(ground_only_folder=ground_only_folder),
        "special_tracking": get_special_tracking_tasks(ground_only_folder=ground_only_folder),
        "general_tracking": get_general_tracking_tasks(ground_only_folder=ground_only_folder),
        "only_intrinsic_change": get_only_intrinsic_change_tasks(ground_only_folder=ground_only_folder),
        "only_translation": get_only_translation_tasks(ground_and_setup_folder=ground_and_setup_folder, ground_only_folder=ground_only_folder),
        "only_rotation": get_only_rotation_tasks(ground_only_folder=ground_only_folder),
        "reference_frame": get_reference_frame_tasks(ground_and_setup_folder=ground_and_setup_folder),
    }

def get_setup_pairwise_labels(setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    return {
        "shot_transition": get_shot_transition_tasks(setup_folder=setup_folder),
        "overlays": get_overlays_tasks(setup_folder=setup_folder),
        "lens_distortion": get_lens_distortion_tasks(setup_folder=setup_folder),
        "playback_speed": get_playback_speed_tasks(setup_folder=setup_folder),
        "point_of_view": get_point_of_view_tasks(setup_folder=setup_folder),
        "subject_framing": get_subject_framing_tasks(setup_folder=setup_folder),
        "shot_type": get_shot_type_tasks(setup_folder=setup_folder),
        "shot_size_change": get_shot_size_change_tasks(setup_folder=setup_folder),
        "shot_size_start": get_shot_size_start_tasks(setup_folder=setup_folder),
        "shot_size_end": get_shot_size_end_tasks(setup_folder=setup_folder),
        "shot_size_is": get_shot_size_is_tasks(setup_folder=setup_folder),
        "height_wrt_subject_change": get_height_wrt_subject_change_tasks(setup_folder=setup_folder),
        "height_wrt_subject_start": get_height_wrt_subject_start_tasks(setup_folder=setup_folder),
        "height_wrt_subject_end": get_height_wrt_subject_end_tasks(setup_folder=setup_folder),
        "height_wrt_subject_is": get_height_wrt_subject_is_tasks(setup_folder=setup_folder),
        "height_wrt_subject_transition": get_height_wrt_subject_transition_tasks(setup_folder=setup_folder),
        "height_wrt_ground_change": get_height_wrt_ground_change_tasks(setup_folder=setup_folder),
        "height_wrt_ground_start": get_height_wrt_ground_start_tasks(setup_folder=setup_folder),
        "height_wrt_ground_end": get_height_wrt_ground_end_tasks(setup_folder=setup_folder),
        "height_wrt_ground_is": get_height_wrt_ground_is_tasks(setup_folder=setup_folder),
        "camera_angle_change": get_camera_angle_change_tasks(setup_folder=setup_folder),
        "camera_angle_start": get_camera_angle_start_tasks(setup_folder=setup_folder),
        "camera_angle_end": get_camera_angle_end_tasks(setup_folder=setup_folder),
        "camera_angle_is": get_camera_angle_is_tasks(setup_folder=setup_folder),
        "camera_angle_transition": get_camera_angle_transition_tasks(setup_folder=setup_folder),
        "dutch_angle": get_dutch_angle_tasks(setup_folder=setup_folder),
        "depth_of_field": get_depth_of_field_tasks(setup_folder=setup_folder),
        "focus_is_always": get_focus_is_always_tasks(setup_folder=setup_folder),
        "focus_start_with": get_focus_start_with_tasks(setup_folder=setup_folder),
        "focus_end_with": get_focus_end_with_tasks(setup_folder=setup_folder),
        "focus_from_to": get_focus_from_to_tasks(setup_folder=setup_folder)
    }

def get_motion_and_setup_pairwise_labels(ground_only_folder=CAMERABENCH_GROUND_ONLY_FOLDER_APRIL,
                                         ground_and_setup_folder=CAMERABENCH_GROUND_AND_SETUP_FOLDER_APRIL,
                                         ground_and_camera_folder=CAMERABENCH_GROUND_AND_CAMERA_FOLDER,
                                         setup_folder=CAMERABENCH_SETUP_ONLY_FOLDER_APRIL):
    motion_dataset = get_motion_pairwise_labels(ground_only_folder=ground_only_folder,
                                                ground_and_setup_folder=ground_and_setup_folder,
                                                ground_and_camera_folder=ground_and_camera_folder)
    setup_dataset = get_setup_pairwise_labels(setup_folder=setup_folder)
    return {**motion_dataset, **setup_dataset}

def get_black_and_white_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "is_black_white",
            "pos_question": "Is the video entirely in black and white, with no chromatic colors, and only black, white, or shades of gray?",
            "neg_question": "Is the video not entirely in black and white and contains chromatic colors?",
            "pos_prompt": "The video is entirely in black and white, with no chromatic color present; only black, white, or shades of gray may appear.",
            "neg_prompt": "The video is not entirely in black and white and contains chromatic colors.",
            "pos": {
                "label": "lighting_setup.color_grading.is_black_white",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.is_black_white",
                "type": "neg",
            },
        },
    ]

def get_color_temperature_simple_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_warm",
            "pos_question": "Does the video predominantly feature warm tones such as reds, oranges, or yellows, with no obvious cool tones except possibly black, white, or gray?",
            "neg_question": "Does the video not predominantly feature warm tones such as reds, oranges, or yellows, or does it contain any obvious cool tones?",
            "pos_prompt": "The video predominantly features warm tones such as reds, oranges, or yellows, with no obvious cool tones except possibly black, white, or gray.",
            "neg_prompt": "The video does not predominantly feature warm tones such as reds, oranges, or yellows, or contains obvious cool tones.",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_warm",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_warm",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_cool",
            "pos_question": "Does the video predominantly feature cool tones such as blues or greens, with no obvious warm tones except possibly black, white, or gray?",
            "neg_question": "Does the video not predominantly feature cool tones such as blues or greens, or does it contain any obvious warm tones?",
            "pos_prompt": "The video predominantly features cool tones such as blues or greens, with no obvious warm tones except possibly black, white, or gray.",
            "neg_prompt": "The video does not predominantly feature cool tones such as blues or greens, or contains obvious warm tones.",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_cool",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_cool",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_neutral",
            "pos_question": "Does the video have a mostly neutral and stable color palette with no strong warm or cool tones standing out, and the contrasts between colors are mild (not overly intense)?",
            "neg_question": "Does the video not have a mostly neutral and stable color palette with no strong warm or cool tones standing out, and the contrasts between colors are not mild (overly intense)?",
            "pos_prompt": "The video's color palette is mostly neutral and stable, with no strong warm or cool tones standing out, and the contrasts between colors are mild (not overly intense).",
            "neg_prompt": "The video's color palette is not mostly neutral and stable with no strong warm or cool tones standing out, and the contrasts between colors are not mild (overly intense).",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_neutral",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_neutral",
                "type": "neg",
            },
        },
    ]

def get_color_temperature_complex_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_changing",
            "pos_question": "Does the video have noticeable shifts between warm, neutral, and cool color tones in large parts of the scene?",
            "neg_question": "Does the video not have noticeable shifts between warm, neutral, and cool color tones in large parts of the scene?",
            "pos_prompt": "The video has noticeable shifts between warm, neutral, and cool color tones in large parts of the scene.",
            "neg_prompt": "The video does not have noticeable shifts between warm, neutral, and cool color tones in large parts of the scene.",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_contrasting",
            "pos_question": "Does the video show intense contrasts between warm and cool colors?",
            "neg_question": "Does the video not show intense contrasts between warm and cool colors?",
            "pos_prompt": "The video shows intense contrasts between warm and cool colors.",
            "neg_prompt": "The video does not show intense contrasts between warm and cool colors.",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_contrasting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_contrasting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "color_temperature_is_complex_others",
            "pos_question": "Does the video show intense contrasts between warm and cool colors with noticeable color temperature shifts across large areas of the scene?",
            "neg_question": "Does the video not show intense contrasts between warm and cool colors with noticeable color temperature shifts across large areas of the scene?",
            "pos_prompt": "The video shows intense contrasts between warm and cool colors with noticeable color temperature shifts across large areas of the scene.",
            "neg_prompt": "The video does not show intense contrasts between warm and cool colors with noticeable color temperature shifts across large areas of the scene.",
            "pos": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_complex_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.temperature.color_temperature_is_complex_others",
                "type": "neg",
            },
        },
    ]

def get_colorfulness_simple_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_high",
            "pos_question": "Does the video predominantly feature highly vibrant and intense colors, with vivid hues dominating the scene and creating an overall impression of strong colorfulness (or saturation)?",
            "neg_question": "Does the video not predominantly feature highly vibrant and intense colors, with vivid hues dominating the scene and creating an overall impression of strong colorfulness (or saturation)?",
            "pos_prompt": "The video predominantly features highly vibrant and intense colors, with vivid hues dominating the scene and creating an overall impression of strong colorfulness (or saturation).",
            "neg_prompt": "The video does not predominantly feature highly vibrant and intense colors, with vivid hues dominating the scene and creating an overall impression of strong colorfulness (or saturation).",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_high",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_high",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_low",
            "pos_question": "Does the video feature only muted or grayish (desaturated) colors, without being entirely black and white?",
            "neg_question": "Does the video not feature only muted or grayish (desaturated) colors, without being entirely black and white?",
            "pos_prompt": "The video features only muted or grayish (desaturated) colors, without being entirely black and white.",
            "neg_prompt": "The video does not feature only muted or grayish (desaturated) colors, without being entirely black and white.",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_low",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_low",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_neutral",
            "pos_question": "Does the video feature a balanced and stable level of colorfulness, without being dominated by either overly vivid or overly grayish colors?",
            "neg_question": "Does the video not feature a balanced and stable level of colorfulness, without being dominated by either overly vivid or overly grayish colors?",
            "pos_prompt": "The video features a balanced and stable level of colorfulness, without being dominated by either overly vivid or overly grayish colors.",
            "neg_prompt": "The video does not feature a balanced and stable level of colorfulness, without being dominated by either overly vivid or overly grayish colors.",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_neutral",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_neutral",
                "type": "neg",
            },
        },
    ]

def get_colorfulness_complex_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_changing",
            "pos_question": "Does the video have noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene?",
            "neg_question": "Does the video not have noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene?",
            "pos_prompt": "The video has noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene.",
            "neg_prompt": "The video does not have noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene.",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_contrasting",
            "pos_question": "Does the video feature striking contrasts between regions of high and low colorfulness (or saturation), creating a clear visual separation?",
            "neg_question": "Does the video not feature striking contrasts between regions of high and low colorfulness (or saturation), creating a clear visual separation?",
            "pos_prompt": "The video features striking contrasts between regions of high and low colorfulness (or saturation), creating a clear visual separation.",
            "neg_prompt": "The video does not feature striking contrasts between regions of high and low colorfulness (or saturation), creating a clear visual separation.",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_contrasting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_contrasting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "colorfulness_is_complex_others",
            "pos_question": "Does the video feature striking contrasts between regions of high and low colorfulness (or saturation), with noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene?",
            "neg_question": "Does the video not feature striking contrasts between regions of high and low colorfulness (or saturation), with noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene?",
            "pos_prompt": "The video features striking contrasts between regions of high and low colorfulness (or saturation), with noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene.",
            "neg_prompt": "The video does not feature striking contrasts between regions of high and low colorfulness (or saturation), with noticeable shifts in colorfulness (or saturation) between high, neutral, and low levels across large parts of the scene.",
            "pos": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_complex_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.colorfulness.colorfulness_is_complex_others",
                "type": "neg",
            },
        },
    ]

def get_brightness_simple_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "brightness_is_very_bright",
            "pos_question": "Is the video excessively bright due to overexposure, losing details in around half or more of the frame and across most or all of the video?",
            "neg_question": "Is the video not excessively bright due to overexposure, losing details in around half or more of the frame and across most or all of the video?",
            "pos_prompt": "The video is excessively bright due to overexposure, losing details in around half or more of the frame and across most or all of the video.",
            "neg_prompt": "The video is not excessively bright due to overexposure, losing details in around half or more of the frame and across most or all of the video.",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_very_bright",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_very_bright",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "brightness_is_neutral",
            "pos_question": "Does the video show a scene with balanced and stable illumination, with no large areas that are too bright (overexposed) or too dark (underexposed)?",
            "neg_question": "Does the video not show a scene with balanced and stable illumination, with no large areas that are too bright (overexposed) or too dark (underexposed)?",
            "pos_prompt": "The video shows a scene with balanced and stable illumination, with no large areas that are too bright (overexposed) or too dark (underexposed).",
            "neg_prompt": "The video does not show a scene with balanced and stable illumination, with no large areas that are too bright (overexposed) or too dark (underexposed).",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_neutral",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_neutral",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "brightness_is_very_dark",
            "pos_question": "Does the video appear very dark due to underexposure or dim lighting, with a loss of detail in around half or more of the frame?",
            "neg_question": "Does the video not appear very dark due to underexposure or dim lighting, with a loss of detail in around half or more of the frame?",
            "pos_prompt": "The video appears very dark due to underexposure or dim lighting, with a loss of detail in around half or more of the frame.",
            "neg_prompt": "The video does not appear very dark due to underexposure or dim lighting, with a loss of detail in around half or more of the frame.",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_very_dark",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_very_dark",
                "type": "neg",
            },
        },
    ]

def get_brightness_complex_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "brightness_is_changing",
            "pos_question": "Does the overall brightness or exposure of the video change over time, with noticeable shifts between brighter and darker levels across large portions of the frame?",
            "neg_question": "Does the overall brightness or exposure of the video not change over time with noticeable shifts between brighter and darker levels across large portions of the frame?",
            "pos_prompt": "The overall brightness or exposure of the video changes over time, with noticeable shifts between brighter and darker levels across large portions of the frame.",
            "neg_prompt": "The overall brightness or exposure of the video does not change over time with noticeable shifts between brighter and darker levels across large portions of the frame.",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "brightness_is_contrasting",
            "pos_question": "Does the video shows both very bright (overexposed) and very dark (underexposed) regions within the same frame, across most or all of the video?",
            "neg_question": "Does the video not show both very bright (overexposed) and very dark (underexposed) regions within the same frame, across most or all of the video?",
            "pos_prompt": "The video shows both very bright (overexposed) and very dark (underexposed) regions within the same frame, across most or all of the video.",
            "neg_prompt": "The video does not show both very bright (overexposed) and very dark (underexposed) regions within the same frame, across most or all of the video.",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_contrasting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_contrasting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "brightness_is_complex_others",
            "pos_question": "Is the video showing both very bright (overexposed) and very dark (underexposed) regions within the same frame, and the overall brightness or exposure changes over time across large portions of the frame?",
            "neg_question": "Is the video not showing both very bright (overexposed) and very dark (underexposed) regions within the same frame, and the overall brightness or exposure not changing over time across large portions of the frame?",  
            "pos_prompt": "The video shows both very bright (overexposed) and very dark (underexposed) regions within the same frame, and the overall brightness or exposure changes over time across large portions of the frame.",
            "neg_prompt": "The video does not show both very bright (overexposed) and very dark (underexposed) regions within the same frame, and the overall brightness or exposure does not change over time across large portions of the frame.",
            "pos": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_complex_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.color_grading.brightness.brightness_is_complex_others",
                "type": "neg",
            },
        },
    ]

def get_scene_type_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "scene_type_is_exterior",
            "pos_question": "Is the video captured through a camera (real or simulated) and taking place outdoors with physically realistic lighting?",
            "neg_question": "Is the video not captured through a camera (real or simulated) and taking place outdoors with physically realistic lighting?",
            "pos_prompt": "The video is captured through a camera (real or simulated) and takes place outdoors with physically realistic lighting.",
            "neg_prompt": "The video is not captured through a camera (real or simulated) and takes place outdoors with physically realistic lighting.",
            "pos": {
                "label": "lighting_setup.scene.scene_type_is_exterior",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.scene.scene_type_is_exterior",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "scene_type_is_interior",
            "pos_question": "Is the video captured through a camera (real or simulated) and taking place indoors with physically realistic lighting?",
            "neg_question": "Is the video not captured through a camera (real or simulated) and taking place indoors with physically realistic lighting?",
            "pos_prompt": "The video is captured through a camera (real or simulated) and takes place indoors with physically realistic lighting.",
            "neg_prompt": "The video is not captured through a camera (real or simulated) and takes place indoors with physically realistic lighting.",
            "pos": {
                "label": "lighting_setup.scene.scene_type_is_interior",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.scene.scene_type_is_interior",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "scene_type_is_synthetic",
            "pos_question": "Is the video not a camera capture but a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects?",
            "neg_question": "Is the video not a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects?",
            "pos_prompt": "The video is not a camera capture but a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects.",
            "neg_prompt": "The video is not a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects.",
            "pos": {
                "label": "lighting_setup.scene.scene_type_is_synthetic",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.scene.scene_type_is_synthetic",
                "type": "neg",
            },
        },
        # {
        #     "folder": lighting_folder,
        #     "name": "scene_type_is_unclear_or_changing",
        #     "pos_question": "Is the video captured through a camera (real or simulated) with physically realistic lighting, but whether it is indoors or outdoors is unclear or changes during the video?",
        #     "neg_question": "Is the video not captured through a camera (real or simulated) with physically realistic lighting, or whether it is indoors or outdoors is clear and consistent throughout the video?",
        #     "pos_prompt": "The video is captured through a camera (real or simulated) with physically realistic lighting, but whether it is indoors or outdoors is unclear or changes during the video.",
        #     "neg_prompt": "The video is not captured through a camera (real or simulated) with physically realistic lighting, or whether it is indoors or outdoors is clear and consistent throughout the video.",
        #     "pos": {
        #         "label": "lighting_setup.scene.scene_type_is_unclear_or_changing",
        #         "type": "pos",
        #     },
        #     "neg": {
        #         "label": "lighting_setup.scene.scene_type_is_unclear_or_changing",
        #         "type": "neg",
        #     },
        # },
    ]

def get_light_source_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "has_artificial_practical_light",
            "pos_question": "Does the scene consistently feature artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video?",
            "neg_question": "Does the scene not (or at least not consistently) feature artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video?",
            "pos_prompt": "The scene consistently features artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video.",
            "neg_prompt": "The scene does not (or at least not consistently) feature artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video.",
            "pos": {
                "label": "lighting_setup.light_source.has_artificial_practical_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_artificial_practical_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_unclear_or_changing_light_source",
            "pos_question": "Does the video's primary light source change over time or comes from an uncommon source other than the sun, fire, moon, stars, or artificial light?",
            "neg_question": "Does the video's primary light source not change over time or comes from a common source including the sun, fire, moon, stars, or artificial light?",
            "pos_prompt": "The video's primary light source changes over time or comes from an uncommon source other than the sun, fire, moon, stars, or artificial light.",
            "neg_prompt": "The video's primary light source does not change over time or comes from a common source including the sun, fire, moon, stars, or artificial light.",
            "pos": {
                "label": "lighting_setup.light_source.has_unclear_or_changing_light_source",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_unclear_or_changing_light_source",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_firelight",
            "pos_question": "Is the scene consistently lit primarily by firelight, and the fire is visible in the scene?",
            "neg_question": "Is the scene not consistently lit primarily by firelight, or the fire is not visible in the scene?",
            "pos_prompt": "The scene is consistently lit primarily by firelight, and the fire is visible in the scene.",
            "neg_prompt": "The scene is not consistently lit primarily by firelight, or the fire is not visible in the scene.",
            "pos": {
                "label": "lighting_setup.light_source.has_firelight",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_firelight",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_moonlight_starlight",
            "pos_question": "Is the scene consistently lit primarily by moonlight or starlight, and the moon or stars are visible in the scene?",
            "neg_question": "Is the scene not consistently lit primarily by moonlight or starlight, or the moon or stars are not visible in the scene?",
            "pos_prompt": "The scene is consistently lit primarily by moonlight or starlight, and the moon or stars are visible in the scene.",
            "neg_prompt": "The scene is not consistently lit primarily by moonlight or starlight, or the moon or stars are not visible in the scene.",
            "pos": {
                "label": "lighting_setup.light_source.has_moonlight_starlight",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_moonlight_starlight",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_non_visible_light_source",
            "pos_question": "Does the video never show any visible light source, and the lighting cannot be clearly attributed to sunlight?",
            "neg_question": "Does the video show a visible light source at some point, or the lighting can be clearly attributed to sunlight?",
            "pos_prompt": "The video never shows any visible light source, and the lighting cannot be clearly attributed to sunlight.",
            "neg_prompt": "The video shows a visible light source at some point, or the lighting can be clearly attributed to sunlight.",
            "pos": {
                "label": "lighting_setup.light_source.has_non_visible_light_source",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_non_visible_light_source",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_sunlight",
            "pos_question": "Is the scene consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame?",
            "neg_question": "Is the scene not consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame?",
            "pos_prompt": "The scene is consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame.",
            "neg_prompt": "The scene is not consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame.",
            "pos": {
                "label": "lighting_setup.light_source.has_sunlight",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.has_sunlight",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "is_abstract",
            "pos_question": "Does the video feature an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source?",
            "neg_question": "Does the video not feature an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source?",
            "pos_prompt": "The video features an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source.",
            "neg_prompt": "The video does not feature an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source.",
            "pos": {
                "label": "lighting_setup.light_source.is_abstract",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_source.is_abstract",
                "type": "neg",
            },
        }
    ]

def get_sunlight_level_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "sunlight_quality_is_normal",
            "pos_question": "Does the scene feature regular daylight with balanced brightness, neither sunny nor overcast, nor during golden or blue hours?",
            "neg_question": "Does the scene not feature regular daylight with balanced brightness, neither sunny nor overcast, nor during golden or blue hours?",
            "pos_prompt": "The scene features regular daylight with balanced brightness, neither sunny nor overcast, nor during golden or blue hours.",
            "neg_prompt": "The scene does not feature regular daylight with balanced brightness, neither sunny nor overcast, nor during golden or blue hours.",
            "pos": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_normal",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_normal",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "sunlight_quality_is_hard",
            "pos_question": "Does the scene feature strong direct sunlight, resulting in very bright, high-contrast lighting with sharp, hard-edged shadows?",
            "neg_question": "Does the scene not feature strong direct sunlight, resulting in very bright, high-contrast lighting with sharp, hard-edged shadows?",
            "pos_prompt": "The scene features strong direct sunlight, resulting in very bright, high-contrast lighting with sharp, hard-edged shadows.",
            "neg_prompt": "The scene does not feature strong direct sunlight, resulting in very bright, high-contrast lighting with sharp, hard-edged shadows.",
            "pos": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_hard",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_hard",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "sunlight_quality_is_soft",
            "pos_question": "Is the scene illuminated by soft, diffused sunlight, such as from cloudy skies, mist, or twilight conditions, with no directional sunlight and either no visible shadows or low-contrast shadows?",
            "neg_question": "Is the scene not illuminated by soft, diffused sunlight, such as from cloudy skies, mist, or twilight conditions, with no directional sunlight and either no visible shadows or low-contrast shadows?",
            "pos_prompt": "The scene is illuminated by soft, diffused sunlight, such as from cloudy skies, mist, or twilight conditions, with no directional sunlight and either no visible shadows or low-contrast shadows.",
            "neg_prompt": "The scene is not illuminated by soft, diffused sunlight, such as from cloudy skies, mist, or twilight conditions, with no directional sunlight and either no visible shadows or low-contrast shadows.",
            "pos": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_soft",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_soft",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "sunlight_quality_is_sunset_sunrise",
            "pos_question": "Does the scene feature warm, golden sunlight at sunrise or sunset?",
            "neg_question": "Does the scene not feature warm, golden sunlight at sunrise or sunset?",
            "pos_prompt": "The scene features warm, golden sunlight at sunrise or sunset.",
            "neg_prompt": "The scene does not feature warm, golden sunlight at sunrise or sunset.",
            "pos": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_sunset_sunrise",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.sunlight_quality.sunlight_quality_is_sunset_sunrise",
                "type": "neg",
            },
        },
    ]

def get_light_quality_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "light_quality_is_soft",
            "pos_question": "Are all visible surface areas within the scene lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light?",
            "neg_question": "Are all visible surface areas within the scene not lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light?",
            "pos_prompt": "All visible surface areas within the scene are lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light.",
            "neg_prompt": "All visible surface areas within the scene are not lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light.",
            "pos": {
                "label": "lighting_setup.light_quality.light_quality_is_soft",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.light_quality_is_soft",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "light_quality_is_hard",
            "pos_question": "Are all or nearly all visible surface areas within the scene lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light?",
            "neg_question": "Are all or nearly all visible surface areas within the scene not lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light?",
            "pos_prompt": "All or nearly all visible surface areas within the scene are lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light.",
            "neg_prompt": "All or nearly all visible surface areas within the scene are not lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light.",
            "pos": {
                "label": "lighting_setup.light_quality.light_quality_is_hard",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.light_quality_is_hard",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "light_quality_is_changing",
            "pos_question": "Do some surface areas in the scene change in light quality over time, shifting between soft and hard light?",
            "neg_question": "Do some surface areas in the scene not change in light quality over time, shifting between soft and hard light?",
            "pos_prompt": "Some surface areas in the scene change in light quality over time, shifting between soft and hard light.",
            "neg_prompt": "Some surface areas in the scene do not change in light quality over time, shifting between soft and hard light.",
            "pos": {
                "label": "lighting_setup.light_quality.light_quality_is_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.light_quality_is_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "light_quality_is_complex_ambiguous",
            "pos_question": "Does the scene lack sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation?",
            "neg_question": "Does the scene not lack sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation?",
            "pos_prompt": "The scene lacks sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation.",
            "neg_prompt": "The scene does not lack sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation.",
            "pos": {
                "label": "lighting_setup.light_quality.light_quality_is_complex_ambiguous",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.light_quality.light_quality_is_complex_ambiguous",
                "type": "neg",
            },
        },
    ]

def get_light_contrast_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_high",
            "pos_question": "Is the lighting contrast on the subject's surface consistently high, with extreme brightness differences between lit and shadowed areas, and some features lost in blown-out highlights or deep shadows, roughly corresponding to a 1:16 or higher light ratio (4+ stops)?",
            "neg_question": "Is the lighting contrast on the subject's surface not consistently high, with extreme brightness differences between lit and shadowed areas, and some features lost in blown-out highlights or deep shadows, roughly corresponding to a 1:16 or higher light ratio (4+ stops)?",
            "pos_prompt": "The lighting contrast on the subject’s surface is consistently high, with extreme brightness differences between lit and shadowed areas, and some features lost in blown-out highlights or deep shadows, roughly corresponding to a 1:16 or higher light ratio (4+ stops).",
            "neg_prompt": "The lighting contrast on the subject’s surface is not consistently high, with extreme brightness differences between lit and shadowed areas, and some features lost in blown-out highlights or deep shadows, roughly corresponding to a 1:16 or higher light ratio (4+ stops).",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_high",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_high",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_normal",
            "pos_question": "Is the lighting contrast on the subject’s surface consistently moderate, with a clear but not extreme difference between lit and shadowed areas, and all surface features remaining visible, roughly within a 1:2 to 1:8 light ratio (2–3 stops)?",
            "neg_question": "Is the lighting contrast on the subject’s surface not consistently moderate, with a clear but not extreme difference between lit and shadowed areas, and all surface features remaining visible, roughly within a 1:2 to 1:8 light ratio (2–3 stops)?",
            "pos_prompt": "The lighting contrast on the subject’s surface is consistently moderate, with a clear but not extreme difference between lit and shadowed areas, and all surface features remaining visible, roughly within a 1:2 to 1:8 light ratio (2–3 stops).",
            "neg_prompt": "The lighting contrast on the subject’s surface is not consistently moderate, with a clear but not extreme difference between lit and shadowed areas, and all surface features remaining visible, roughly within a 1:2 to 1:8 light ratio (2–3 stops).",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_normal",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_normal",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_minimal",
            "pos_question": "Is the lighting contrast on the subject’s surface consistently minimal, with little or no visible difference between lit and shadowed areas, creating a flat appearance, roughly corresponding to a 1:1 to 1:2 light ratio (0–1 stop difference)?",
            "neg_question": "Is the lighting contrast on the subject’s surface not consistently minimal, with little or no visible difference between lit and shadowed areas, creating a flat appearance, roughly corresponding to a 1:1 to 1:2 light ratio (0–1 stop difference)?",
            "pos_prompt": "The lighting contrast on the subject’s surface is consistently minimal, with little or no visible difference between lit and shadowed areas, creating a flat appearance, roughly corresponding to a 1:1 to 1:2 light ratio (0–1 stop difference).",
            "neg_prompt": "The lighting contrast on the subject’s surface is not consistently minimal, with little or no visible difference between lit and shadowed areas, creating a flat appearance, roughly corresponding to a 1:1 to 1:2 light ratio (0–1 stop difference).",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_minimal",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_minimal",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_complex_changing",
            "pos_question": "Does the lighting contrast on the subject change significantly over time (e.g., due to moving light sources, changing conditions, or subject movement)?",
            "neg_question": "Does the lighting contrast on the subject remain relatively consistent over time?",
            "pos_prompt": "The lighting contrast on the subject changes significantly over time (e.g., due to moving light sources, changing conditions, or subject movement).",
            "neg_prompt": "The lighting contrast on the subject remains relatively consistent over time.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_complex_contrasting",
            "pos_question": "Does the lighting contrast on the subject vary significantly across different regions or parts of the subject simultaneously?",
            "neg_question": "Does the lighting contrast on the subject remain relatively consistent across different regions or parts?",
            "pos_prompt": "The lighting contrast on the subject varies significantly across different regions or parts of the subject simultaneously.",
            "neg_prompt": "The lighting contrast on the subject remains relatively consistent across different regions or parts.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_contrasting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_contrasting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_complex_others",
            "pos_question": "Does the lighting contrast on the subject’s surface vary both over time and across different regions, with no consistent pattern or contrast level throughout the video?",
            "neg_question": "Does the lighting contrast on the subject’s surface not vary both over time and across different regions, with no consistent pattern or contrast level throughout the video?",
            "pos_prompt": "The lighting contrast on the subject’s surface varies both over time and across different regions, with no consistent pattern or contrast level throughout the video.",
            "neg_prompt": "The lighting contrast on the subject’s surface does not vary both over time and across different regions, with no consistent pattern or contrast level throughout the video.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_complex_others",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_light_contrast_is_unknown",
            "pos_question": "Is the lighting contrast on the subject’s surface unable to be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and lighting contrast that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup?",
            "neg_question": "Is the lighting contrast on the subject’s surface able to be reliably judged?",
            "pos_prompt": "Lighting contrast on the subject’s surface cannot be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and lighting contrast that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup.",
            "neg_prompt": "Lighting contrast on the subject’s surface can be reliably judged.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_unknown",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.subject_light_contrast_is_unknown",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "flat_lighting",
            "pos_question": "Is the subject lit with flat lighting, with little to no contrast?",
            "neg_question": "Is the subject not lit with flat lighting, with little to no contrast?",
            "pos_prompt": "The subject is lit with flat lighting, with little to no contrast.",
            "neg_prompt": "The subject is not lit with flat lighting, with little to no contrast.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.flat_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.flat_lighting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "low_key_lighting",
            "pos_question": "Is the subject lit with low-key lighting?",
            "neg_question": "Is the subject not lit with low-key lighting?",
            "pos_prompt": "The subject is lit with low-key lighting.",
            "neg_prompt": "The subject is not lit with low-key lighting.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.low_key_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.low_key_lighting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "high_key_lighting",
            "pos_question": "Is the subject lit with high-key lighting?",
            "neg_question": "Is the subject not lit with high-key lighting?",
            "pos_prompt": "The subject is lit with high-key lighting.",
            "neg_prompt": "The subject is not lit with high-key lighting.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_contrast.high_key_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_contrast.high_key_lighting",
                "type": "neg",
            },
        },
    ]

def get_light_direction_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "direction_is_back_light",
            "pos_question": "Are all subjects consistently back-lit by a noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera?",
            "neg_question": "Are all subjects not consistently back-lit by a noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera?",
            "pos_prompt": "All subjects are consistently back-lit by noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera.",
            "neg_prompt": "All subjects are not consistently back-lit by noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_back_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_back_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_front_light",
            "pos_question": "Are all subjects consistently front-lit by a noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera?",
            "neg_question": "Are all subjects not consistently front-lit by a noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera?",
            "pos_prompt": "All subjects are consistently front-lit by noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera.",
            "neg_prompt": "All subjects are not consistently front-lit by noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_front_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_front_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_top_light",
            "pos_question": "Are all subjects consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward?",
            "neg_question": "Are all subjects not consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward?",
            "pos_prompt": "All subjects are consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward.",
            "neg_prompt": "All subjects are not consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_top_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_top_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_bottom_light",
            "pos_question": "Are all subjects consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward?",
            "neg_question": "Are all subjects not consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward?",
            "pos_prompt": "All subjects are consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward.",
            "neg_prompt": "All subjects are not consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_bottom_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_bottom_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_ambient_light",
            "pos_question": "Are all subjects consistently lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back?",
            "neg_question": "Are all subjects not lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back?",
            "pos_prompt": "All subjects are lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back.",
            "neg_prompt": "All subjects are not lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_ambient_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_ambient_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_right_side",
            "pos_question": "Are all subjects consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?",
            "neg_question": "Are all subjects not consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?",
            "pos_prompt": "All subjects are consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.",
            "neg_prompt": "All subjects are not consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_right_side",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_right_side",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_left_side",
            "pos_question": "Are all subjects consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?",
            "neg_question": "Are all subjects not consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?",
            "pos_prompt": "All subjects are consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.",
            "neg_prompt": "All subjects are not consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_left_side",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_left_side",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_complex_changing",
            "pos_question": "Does the dominant light direction on the subject(s) change over time, as judged from the camera's perspective?",
            "neg_question": "Does the dominant light direction on the subject(s) not change over time, as judged from the camera's perspective?",
            "pos_prompt": "The dominant light direction on the subject(s) changes over time, as judged from the camera’s perspective.",
            "neg_prompt": "The dominant light direction on the subject(s) does not change over time, as judged from the camera’s perspective.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_changing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_changing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_complex_contrasting",
            "pos_question": "Are different parts of the subject, or different subjects, lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame?",
            "neg_question": "Are different parts of the subject, or different subjects, not lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame?",
            "pos_prompt": "Different parts of the subject, or different subjects, are lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame.",
            "neg_prompt": "Different parts of the subject, or different subjects, are not lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_contrasting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_contrasting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_complex_others",
            "pos_question":  "Are different parts of the subject (or different subjects) lit by different directions simultaneously, and do these directions also change over time, so the dominant light direction varies both spatially and temporally?",
            "neg_question": "Are different parts of the subject (or different subjects) not lit by different directions simultaneously, and do these directions not also change over time, so the dominant light direction does not vary both spatially and temporally?",
            "pos_prompt": "Different parts of the subject (or different subjects) are lit by different directions simultaneously, and these directions also change over time. The dominant light direction varies both spatially and temporally.",
            "neg_prompt": "Different parts of the subject (or different subjects) are not lit by different directions simultaneously, and these directions also change over time. The dominant light direction does not vary both spatially and temporally.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_complex_others",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_unknown",
            "pos_question": "Is the lighting direction on the subject unable to be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and light direction that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup?",
            "neg_question": "Is the lighting direction on the subject clear and possible to determine?",
            "pos_prompt": "The lighting direction on the subject cannot be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and light direction that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup.",
            "neg_prompt": "The lighting direction on the subject can be reliably judged.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_unknown",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_unknown",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "direction_is_consistent",
            "pos_question": "Is the subject consistently lit with the same light direction throughout the video and uniform across the entire subject's surface?",
            "neg_question": "Is the subject not consistently lit with the same light direction throughout the video and uniform across the entire subject's surface?",
            "pos_prompt": "The subject is consistently lit with the same light direction throughout the video and uniform across the entire subject's surface.",
            "neg_prompt": "The subject is not consistently lit with the same light direction throughout the video and uniform across the entire subject's surface.",
            "pos": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_consistent",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.light_direction.direction_is_consistent",
                "type": "neg",
            },
        },
    ]

def get_subject_lighting_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "is_consistent_subject",
            "pos_question": "Are there one or more clear, salient subjects lit by external light who remain consistent in the frame throughout the shot?",
            "neg_question": "Are there not one or more clear, salient subjects lit by external light who remain consistent in the frame throughout the shot?",
            "pos_prompt": "One or more clear, salient subjects are lit by external light and remain consistent in the frame throughout the shot.",
            "neg_prompt": "There are not one or more clear, salient subjects lit by external light who remain consistent in the frame throughout the shot.",
            "pos": {
                "label": "lighting_setup.subject_lighting.is_consistent_subject",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.is_consistent_subject",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "is_inconsistent_subject",
            "pos_question": "Are one or more subjects lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced)?",
            "neg_question": "Are there not one or more subjects lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced)?",
            "pos_prompt": "One or more subjects are lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced).",
            "neg_prompt": "There are not one or more subjects lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced).",
            "pos": {
                "label": "lighting_setup.subject_lighting.is_inconsistent_subject",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.is_inconsistent_subject",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "is_unclear_or_light_emitting_subject",
            "pos_question": "Does the video lack a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge?",
            "neg_question": "Does the video not lack a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge?",
            "pos_prompt": "The video lacks a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge.",
            "neg_prompt": "The video does not lack a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge.",
            "pos": {
                "label": "lighting_setup.subject_lighting.is_unclear_or_light_emitting_subject",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.is_unclear_or_light_emitting_subject",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "is_subject_lighting_unrealistic",
            "pos_question": "Does the video contain subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction?",
            "neg_question": "Does the video not contain subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction?",
            "pos_prompt": "The video contains subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction.",
            "neg_prompt": "The video does not contain subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction.",
            "pos": {
                "label": "lighting_setup.subject_lighting.is_subject_lighting_unrealistic",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.is_subject_lighting_unrealistic",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "rembrandt_lighting",
            "pos_question": "Is there Rembrandt lighting that illuminates one side of the subject's face, creating a small triangle of light on the other side?",
            "neg_question": "Is there no Rembrandt lighting that illuminates one side of the subject's face, creating a small triangle of light on the other side?",
            "pos_prompt": "There is Rembrandt lighting that illuminates one side of the subject's face, creating a small triangle of light on the other side.",
            "neg_prompt": "There is no Rembrandt lighting that illuminates one side of the subject's face, creating a small triangle of light on the other side.",
            "pos": {
                "label": "lighting_setup.subject_lighting.rembrandt_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.subject_lighting.rembrandt_lighting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "rim_light",
            "pos_question": "Is there rim lighting that creates a glowing edge around the subject?",
            "neg_question": "Is there no rim lighting that creates a glowing edge around the subject?",
            "pos_prompt": "There is rim lighting that creates a glowing edge around the subject.",
            "neg_prompt": "There is no rim lighting that creates a glowing edge around the subject.",
            "pos": {
                "label": "lighting_setup.special_effect.rim_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.rim_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "silhouette",
            "pos_question": "Is there a silhouette lighting effect that creates a dark outline of the foreground subject against a bright background?", 
            "neg_question": "Is there no silhouette lighting effect that creates a dark outline of the foreground subject against a bright background?",
            "pos_prompt": "There is a silhouette lighting effect that creates a dark outline of the foreground subject against a bright background.",
            "neg_prompt": "There is no silhouette lighting effect that creates a dark outline of the foreground subject against a bright background.",
            "pos": {
                "label": "lighting_setup.special_effect.silhouette",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.silhouette",
                "type": "neg",
            },
        },
    ]

def get_lens_and_optical_effects_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "lens_flares_regular",
            "pos_question": "Does the video contain typical (non-anamorphic) lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts?",
            "neg_question": "Does the video not contain typical (non-anamorphic) lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts?",
            "pos_prompt": "The video contains typical (non-anamorphic) lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts.",
            "neg_prompt": "The video does not contain typical (non-anamorphic) lens flares, appearing as circular, polygonal, veiling, scattered, or streak-like artifacts.",
            "pos": {
                "label": "lighting_setup.lens_effect.lens_flares_regular",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.lens_effect.lens_flares_regular",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "lens_flares_anamorphic",
            "pos_question": "Does the video contain horizontal anamorphic lens flares from bright light sources?",
            "neg_question": "Does the video not contain horizontal anamorphic lens flares from bright light sources?",
            "pos_prompt": "The video contains horizontal anamorphic lens flares from bright light sources.",
            "neg_prompt": "The video does not contain horizontal anamorphic lens flares from bright light sources.",
            "pos": {
                "label": "lighting_setup.lens_effect.lens_flares_anamorphic",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.lens_effect.lens_flares_anamorphic",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "lens_flares",
            "pos_question": "Does the video contain obvious lens flares?",
            "neg_question": "Does the video not contain obvious lens flares?",
            "pos_prompt": "The video contains obvious lens flares.",
            "neg_prompt": "The video does not contain obvious lens flares.",
            "pos": {
                "label": "lighting_setup.lens_effect.lens_flares",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.lens_effect.lens_flares",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "mist_diffusion",
            "pos_question": "Does the video use a mist diffusion filter to soften the image, creating a dreamy, glowing effect?",
            "neg_question": "Does the video not use a mist diffusion filter to soften the image, creating a dreamy, glowing effect?",
            "pos_prompt": "The video uses a mist diffusion filter to soften the image, creating a dreamy, glowing effect.",
            "neg_prompt": "The video does not use a mist diffusion filter to soften the image, creating a dreamy, glowing effect.",
            "pos": {
                "label": "lighting_setup.lens_effect.mist_diffusion",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.lens_effect.mist_diffusion",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "bokeh",
            "pos_question": "Does the video feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field?",
            "neg_question": "Does the video not feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field?",
            "pos_prompt": "The video features soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field.",
            "neg_prompt": "The video does not feature soft, out-of-focus light orbs in the background, created by distant lights and a shallow depth of field.",
            "pos": {
                "label": "lighting_setup.lens_effect.bokeh",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.lens_effect.bokeh",
                "type": "neg",
            },
        },
    ]

def get_reflection_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "reflection_from_water",
            "pos_question": "Does the video show noticeable shimmering effects or bright highlights from light reflecting off water?",
            "neg_question": "Does the video not show noticeable shimmering effects or bright highlights from light reflecting off water?",
            "pos_prompt": "The video shows noticeable shimmering effects or bright highlights from light reflecting off water.",
            "neg_prompt": "The video does not show noticeable shimmering effects or bright highlights from light reflecting off water.",
            "pos": {
                "label": "lighting_setup.reflection.reflection_from_water",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.reflection.reflection_from_water",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "reflection_from_glossy_surface",
            "pos_question": "Does the video feature a noticeable specular reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail?",
            "neg_question": "Does the video not feature a noticeable specular reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail?",
            "pos_prompt": "The video features a noticeable specular reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail.",
            "neg_prompt": "The video does not feature a noticeable specular reflection from light bouncing off a smooth, glossy surface but does not clearly mirror the scene in detail.",
            "pos": {
                "label": "lighting_setup.reflection.reflection_from_glossy_surface",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.reflection.reflection_from_glossy_surface",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "reflection_from_mirror",
            "pos_question": "Does the video show reflections from light bouncing off a mirror, clearly mirroring the scenery in detail?",
            "neg_question": "Does the video not show reflections from light bouncing off a mirror, clearly mirroring the scenery in detail?",
            "pos_prompt": "The video shows reflections from light bouncing off a mirror, clearly mirroring the scenery in detail.",
            "neg_prompt": "The video does not show reflections from light bouncing off a mirror, clearly mirroring the scenery in detail.",
            "pos": {
                "label": "lighting_setup.reflection.reflection_from_mirror",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.reflection.reflection_from_mirror",
                "type": "neg",
            },
        },
    ]


def get_natural_atmospheric_effects_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "aerial_perspective",
            "pos_question": "Does the video feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects?",
            "neg_question": "Does the video not feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects?",
            "pos_prompt": "The video features a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects.",
            "neg_prompt": "The video does not feature a noticeable aerial perspective, where distant scenery appears less detailed, desaturated, and hazier due to atmospheric effects.",
            "pos": {
                "label": "lighting_setup.natural_effect.aerial_perspective",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.natural_effect.aerial_perspective",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "rainbow",
            "pos_question": "Does the video feature a noticeable rainbow?",
            "neg_question": "Does the video not feature a noticeable rainbow?",
            "pos_prompt": "The video features a noticeable rainbow.",
            "neg_prompt": "The video does not feature a noticeable rainbow.",
            "pos": {
                "label": "lighting_setup.natural_effect.rainbow",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.natural_effect.rainbow",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "aurora",
            "pos_question": "Does the video feature an aurora, with flowing, colorful light patterns in the sky?",
            "neg_question": "Does the video not feature an aurora, with flowing, colorful light patterns in the sky?",
            "pos_prompt": "The video features an aurora, with flowing, colorful light patterns in the sky.",
            "neg_prompt": "The video does not feature an aurora, with flowing, colorful light patterns in the sky.",
            "pos": {
                "label": "lighting_setup.natural_effect.aurora",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.natural_effect.aurora",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "heat_haze",
            "pos_question": "Does the video feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat?",
            "neg_question": "Does the video not feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat?",
            "pos_prompt": "The video features a noticeable heat haze effect, with air distortions and shimmering caused by rising heat.",
            "neg_prompt": "The video does not feature a noticeable heat haze effect, with air distortions and shimmering caused by rising heat.",
            "pos": {
                "label": "lighting_setup.natural_effect.heat_haze",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.natural_effect.heat_haze",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "lightning",
            "pos_question": "Does the video capture a lightning effect with intense flashes and jagged, branching streaks?",    
            "neg_question": "Does the video not capture a lightning effect with intense flashes and jagged, branching streaks?",
            "pos_prompt": "The video captures a lightning effect with intense flashes and jagged, branching streaks.",
            "neg_prompt": "The video does not capture a lightning effect with intense flashes and jagged, branching streaks.",
            "pos": {
                "label": "lighting_setup.natural_effect.lightning",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.natural_effect.lightning",
                "type": "neg",
            },
        },
    ]

def get_special_artistic_effects_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "colored_neon_lighting",
            "pos_question": "Does the video feature artificial colored or neon lighting?",
            "neg_question": "Does the video not feature artificial colored or neon lighting?",
            "pos_prompt": "The video features artificial colored or neon lighting.",
            "neg_prompt": "The video does not feature artificial colored or neon lighting.",
            "pos": {
                "label": "lighting_setup.special_effect.colored_neon_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.colored_neon_lighting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "professional_lighting",
            "pos_question": "Does the lighting appear professionally done (e.g., portrait, stage, or cinematic lighting)?",
            "neg_question": "Does the lighting not appear professionally done (e.g., portrait, stage, or cinematic lighting)?",
            "pos_prompt": "The lighting appears professionally done (e.g., portrait, stage, or cinematic lighting).",
            "neg_prompt": "The lighting does not appear professionally done (e.g., portrait, stage, or cinematic lighting).",
            "pos": {
                "label": "lighting_setup.special_effect.professional_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.professional_lighting",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "headlight_flashlight",
            "pos_question": "Does the video feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings?",
            "neg_question": "Does the video not feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings?",
            "pos_prompt": "The video features a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings.",
            "neg_prompt": "The video does not feature a headlight or flashlight that illuminates the scene in front with intense, focused light, creating sharp contrast against darker surroundings.",
            "pos": {
                "label": "lighting_setup.special_effect.headlight_flashlight",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.headlight_flashlight",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "vignette",
            "pos_question": "Does the video feature a vignette effect, where the edges gradually darken or fade?",
            "neg_question": "Does the video not feature a vignette effect, where the edges gradually darken or fade?",
            "pos_prompt": "The video features a vignette effect, where the edges gradually darken or fade.",
            "neg_prompt": "The video does not feature a vignette effect, where the edges gradually darken or fade.",
            "pos": {
                "label": "lighting_setup.special_effect.vignette",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.vignette",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "water_caustics",
            "pos_question": "Does the video feature water caustics, where refracted and reflected light creates dynamic, rippling patterns?",
            "neg_question": "Does the video not feature water caustics, where refracted and reflected light creates dynamic, rippling patterns?",
            "pos_prompt": "The video features water caustics, where refracted and reflected light creates dynamic, rippling patterns.",
            "neg_prompt": "The video does not feature water caustics, where refracted and reflected light creates dynamic, rippling patterns.",
            "pos": {
                "label": "lighting_setup.special_effect.water_caustics",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.water_caustics",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "city_light",
            "pos_question": "Does the video feature bright and colorful city lighting from various artificial sources?",
            "neg_question": "Does the video not feature bright and colorful city lighting from various artificial sources?",
            "pos_prompt": "The video features bright and colorful city lighting from various artificial sources.",
            "neg_prompt": "The video does not feature bright and colorful city lighting from various artificial sources.",
            "pos": {
                "label": "lighting_setup.special_effect.city_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.city_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "street_light",
            "pos_question": "Does the video feature light from street lamps?",
            "neg_question": "Does the video not feature light from street lamps?",
            "pos_prompt": "The video features light from street lamps.",
            "neg_prompt": "The video does not feature light from street lamps.",
            "pos": {
                "label": "lighting_setup.special_effect.street_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.special_effect.street_light",
                "type": "neg",
            },
        },
    ]

def get_volumetric_lighting_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "volumetric_beam_light",
            "pos_question": "Does the video feature visible beams of light with well-defined edges, creating linear volumes of light?",
            "neg_question": "Does the video not feature visible beams of light with well-defined edges, creating linear volumes of light?",
            "pos_prompt": "The video features visible beams of light with well-defined edges, creating linear volumes of light.",
            "neg_prompt": "The video does not feature visible beams of light with well-defined edges, creating linear volumes of light.",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.volumetric_beam_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.volumetric_beam_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "volumetric_spot_light",
            "pos_question": "Does the video feature concentrated, cone-shaped volumes of light?",
            "neg_question": "Does the video not feature concentrated, cone-shaped volumes of light?",
            "pos_prompt": "The video features concentrated, cone-shaped volumes of light.",
            "neg_prompt": "The video does not feature concentrated, cone-shaped volumes of light.",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.volumetric_spot_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.volumetric_spot_light",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "god_rays",
            "pos_question": "Does the video feature striking, separated rays of light (god rays) streaming from top through gaps in the environment?",
            "neg_question": "Does the video not feature striking, separated rays of light (god rays) streaming from top through gaps in the environment?",
            "pos_prompt": "The video features striking, separated rays of light (god rays) streaming from top through gaps in the environment.",
            "neg_prompt": "The video does not feature striking, separated rays of light (god rays) streaming from top through gaps in the environment.",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.god_rays",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.god_rays",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "light_through_medium",
            "pos_question": "Does the video feature intense light passing through smoke or fog, shaping visible light volumes?",
            "neg_question": "Does the video not feature intense light passing through smoke or fog, shaping visible light volumes?",
            "pos_prompt": "The video features intense light passing through smoke or fog, shaping visible light volumes.",
            "neg_prompt": "The video does not feature intense light passing through smoke or fog, shaping visible light volumes.",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.light_through_medium",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.light_through_medium",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "volumetric_light_others",
            "pos_question": "Does the video feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights)?",
            "neg_question": "Does the video not feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights)?",
            "pos_prompt": "The video features volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights).",
            "neg_prompt": "The video does not feature volumetric lighting with a well-defined, contained shape (other than beams, god rays, or spotlights).",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.volumetric_light_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.volumetric_light_others",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_volumetric_lighting",
            "pos_question": "Does the video show noticeable volumetric lighting, where light appears as a visible volume?",
            "neg_question": "Does the video not show noticeable volumetric lighting, where light appears as a visible volume?",
            "pos_prompt": "The video shows noticeable volumetric lighting, where light appears as a visible volume.",
            "neg_prompt": "The video does not show noticeable volumetric lighting, where light appears as a visible volume.",
            "pos": {
                "label": "lighting_setup.volumetric_lighting.has_volumetric_lighting",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.volumetric_lighting.has_volumetric_lighting",
                "type": "neg",
            },
        },
    ]

def get_shadow_pattern_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "venetian_blinds",
            "pos_question": "Does the video feature distinct shadow patterns cast by venetian blinds or similar slatted structures?",
            "neg_question": "Does the video not feature distinct shadow patterns cast by venetian blinds or similar slatted structures?",
            "pos_prompt": "The video features distinct shadow patterns cast by venetian blinds or similar slatted structures.",
            "neg_prompt": "The video does not feature distinct shadow patterns cast by venetian blinds or similar slatted structures.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.venetian_blinds",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.venetian_blinds",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "subject_shape",
            "pos_question": "Does the video feature shadows shaped by the subject to support the narrative, emphasizing form or movement?",
            "neg_question": "Does the video not feature shadows shaped by the subject to support the narrative, emphasizing form or movement?",
            "pos_prompt": "The video features shadows shaped by the subject to support the narrative, emphasizing form or movement.",
            "neg_prompt": "The video does not feature shadows shaped by the subject to support the narrative, emphasizing form or movement.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.subject_shape",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.subject_shape",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "window_frames",
            "pos_question": "Does the video feature shadows cast by window frames?",
            "neg_question": "Does the video not feature shadows cast by window frames?",
            "pos_prompt": "The video features shadows cast by window frames.",
            "neg_prompt": "The video does not feature shadows cast by window frames.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.window_frames",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.window_frames",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "foliage",
            "pos_question": "Does the video feature shadow patterns created by foliage, such as leaves or branches?",
            "neg_question": "Does the video not feature shadow patterns created by foliage, such as leaves or branches?",
            "pos_prompt": "The video features shadow patterns created by foliage, such as leaves or branches.",
            "neg_prompt": "The video does not feature shadow patterns created by foliage, such as leaves or branches.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.foliage",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.foliage",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "shadow_patterns_gobo_others",
            "pos_question": "Does the video feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape?",
            "neg_question": "Does the video not feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape?",
            "pos_prompt": "The video features distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape.",
            "neg_prompt": "The video does not feature distinct or dynamic shadow patterns or gobo lighting effects other than Venetian blinds, window frames, foliage, or the subject's shape.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.shadow_patterns_gobo_others",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.shadow_patterns_gobo_others",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "has_shadow_patterns",
            "pos_question": "Does the video feature distinct shadow patterns or gobo lighting effects that shape the visual composition?",
            "neg_question": "Does the video not feature distinct shadow patterns or gobo lighting effects that shape the visual composition?",
            "pos_prompt": "The video features distinct shadow patterns or gobo lighting effects that shape the visual composition.",
            "neg_prompt": "The video does not feature distinct shadow patterns or gobo lighting effects that shape the visual composition.",
            "pos": {
                "label": "lighting_setup.shadow_pattern.has_shadow_patterns",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.shadow_pattern.has_shadow_patterns",
                "type": "neg",
            },
        },
    ]

def get_dynamic_lighting_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "color_shifting_smooth",
            "pos_question": "Does the video feature a smooth color shift, with a gradual yet noticeable change in overall or lighting color?",
            "neg_question": "Does the video not feature a smooth color shift, with a gradual yet noticeable change in overall or lighting color?",
            "pos_prompt": "The video features a smooth color shift, with a gradual yet noticeable change in overall or lighting color.",
            "neg_prompt": "The video does not feature a smooth color shift, with a gradual yet noticeable change in overall or lighting color.",
            "pos": {
                "label": "lighting_setup.dynamic_light.color_shifting_smooth",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_light.color_shifting_smooth",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "color_shifting_sudden",
            "pos_question": "Does the video feature a sudden color shift, with a rapid and noticeable change in overall or lighting color?",
            "neg_question": "Does the video not feature a sudden color shift, with a rapid and noticeable change in overall or lighting color?",
            "pos_prompt": "The video features a sudden color shift, with a rapid and noticeable change in overall or lighting color.",
            "neg_prompt": "The video does not feature a sudden color shift, with a rapid and noticeable change in overall or lighting color.",
            "pos": {
                "label": "lighting_setup.dynamic_light.color_shifting_sudden",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_light.color_shifting_sudden",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "pulsing_flickering",
            "pos_question": "Does the video feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering?",
            "neg_question": "Does the video not feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering?",
            "pos_prompt": "The video features lighting that varies in brightness, either through rhythmic pulsing or irregular flickering.",
            "neg_prompt": "The video does not feature lighting that varies in brightness, either through rhythmic pulsing or irregular flickering.",
            "pos": {
                "label": "lighting_setup.dynamic_light.pulsing_flickering",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_light.pulsing_flickering",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "flashing",
            "pos_question": "Does the lighting in the video flash, creating sudden bursts of light in an on/off pattern that changes the brightness of the scene?",
            "neg_question": "Does the lighting in the video not flash, creating sudden bursts of light in an on/off pattern that changes the brightness of the scene?",
            "pos_prompt": "The lighting in the video flashes, creating sudden bursts of light in an on/off pattern that changes the brightness of the scene.",
            "neg_prompt": "The lighting in the video does not flash, creating sudden bursts of light in an on/off pattern that changes the brightness of the scene.",
            "pos": {
                "label": "lighting_setup.dynamic_light.flashing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_light.flashing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "moving_light",
            "pos_question": "Does the video feature major light source(s) that traverse the scene or change direction?",
            "neg_question": "Does the video not feature major light source(s) that traverse the scene or change direction?",
            "pos_prompt": "The video features major light source(s) that traverse the scene or change direction.",
            "neg_prompt": "The video does not feature major light source(s) that traverse the scene or change direction.",
            "pos": {
                "label": "lighting_setup.dynamic_light.moving_light",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_light.moving_light",
                "type": "neg",
            },
        },
    ]

def get_special_dynamic_effects_tasks(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return [
        {
            "folder": lighting_folder,
            "name": "revealing_shot",
            "pos_question": "Does the video feature a revealing shot that uncovers a new scene or subject?",
            "neg_question": "Does the video not feature a revealing shot that uncovers a new scene or subject?",
            "pos_prompt": "The video features a revealing shot that uncovers a new scene or subject.",
            "neg_prompt": "The video does not feature a revealing shot that uncovers a new scene or subject.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.revealing_shot",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.revealing_shot",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "transformation_morphing",
            "pos_question": "Does the video feature a transformation or morphing effect where one object changes into another?",
            "neg_question": "Does the video not feature a transformation or morphing effect where one object changes into another?",
            "pos_prompt": "The video features a transformation or morphing effect where one object changes into another.",
            "neg_prompt": "The video does not feature a transformation or morphing effect where one object changes into another.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.transformation_morphing",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.transformation_morphing",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "levitation_floating",
            "pos_question": "Does the video feature objects or characters floating or levitating as if unaffected by gravity?",
            "neg_question": "Does the video not feature objects or characters floating or levitating as if unaffected by gravity?",
            "pos_prompt": "The video features objects or characters floating or levitating as if unaffected by gravity.",
            "neg_prompt": "The video does not feature objects or characters floating or levitating as if unaffected by gravity.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.levitation_floating",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.levitation_floating",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "explosion",
            "pos_question": "Does the video show explosions with sudden bursts of flames, matter, and outward force?",
            "neg_question": "Does the video not show explosions with sudden bursts of flames, matter, and outward force?",
            "pos_prompt": "The video shows explosions with sudden bursts of flames, matter, and outward force.",
            "neg_prompt": "The video does not show explosions with sudden bursts of flames, matter, and outward force.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.explosion",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.explosion",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "shattering_breaking",
            "pos_question": "Does the video show objects breaking, shattering, or fragmenting into smaller pieces?",
            "neg_question": "Does the video not show objects breaking, shattering, or fragmenting into smaller pieces?",
            "pos_prompt": "The video shows objects breaking, shattering, or fragmenting into smaller pieces.",
            "neg_prompt": "The video does not show objects breaking, shattering, or fragmenting into smaller pieces.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.shattering_breaking",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.shattering_breaking",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "diffusion",
            "pos_question": "Does the video feature a noticable diffusion effect, where particles, fluids, or other materials spread and disperse over time?",
            "neg_question": "Does the video not feature a noticable diffusion effect, where particles, fluids, or other materials spread and disperse over time?",
            "pos_prompt": "The video features a noticable diffusion effect, where particles, fluids, or other materials spread and disperse over time.",
            "neg_prompt": "The video does not feature a noticable diffusion effect, where particles, fluids, or other materials spread and disperse over time.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.diffusion",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.diffusion",
                "type": "neg",
            },
        },
        {
            "folder": lighting_folder,
            "name": "splashing_waves",
            "pos_question": "Does the video feature noticeable splashing or wave-like motion?",
            "neg_question": "Does the video not feature noticeable splashing or wave-like motion?",
            "pos_prompt": "The video features noticeable splashing or wave-like motion.",
            "neg_prompt": "The video does not feature noticeable splashing or wave-like motion.",
            "pos": {
                "label": "lighting_setup.dynamic_effect.splashing_waves",
                "type": "pos",
            },
            "neg": {
                "label": "lighting_setup.dynamic_effect.splashing_waves",
                "type": "neg",
            },
        },
    ]

def get_lighting_pairwise_labels(lighting_folder=CAMERABENCH_LIGHTING_ONLY_FOLDER_APRIL):
    return {
        "black_white": get_black_and_white_tasks(lighting_folder=lighting_folder),
        "color_temperature_simple": get_color_temperature_simple_tasks(lighting_folder=lighting_folder),
        "color_temperature_complex": get_color_temperature_complex_tasks(lighting_folder=lighting_folder),
        "colorfulness_simple": get_colorfulness_simple_tasks(lighting_folder=lighting_folder),
        "colorfulness_complex": get_colorfulness_complex_tasks(lighting_folder=lighting_folder),
        "brightness_simple": get_brightness_simple_tasks(lighting_folder=lighting_folder),
        "brightness_complex": get_brightness_complex_tasks(lighting_folder=lighting_folder),
        "scene_type": get_scene_type_tasks(lighting_folder=lighting_folder),
        "sunlight_level": get_sunlight_level_tasks(lighting_folder=lighting_folder),
        "light_quality": get_light_quality_tasks(lighting_folder=lighting_folder),
        "light_source": get_light_source_tasks(lighting_folder=lighting_folder),
        "light_contrast": get_light_contrast_tasks(lighting_folder=lighting_folder),
        "light_direction": get_light_direction_tasks(lighting_folder=lighting_folder),
        "subject_lighting": get_subject_lighting_tasks(lighting_folder=lighting_folder),
        "lens_and_optical_effects": get_lens_and_optical_effects_tasks(lighting_folder=lighting_folder),
        "reflection": get_reflection_tasks(lighting_folder=lighting_folder),
        "natural_atmospheric_effects": get_natural_atmospheric_effects_tasks(lighting_folder=lighting_folder),
        "special_artistic_effects": get_special_artistic_effects_tasks(lighting_folder=lighting_folder),
        "volumetric_lighting": get_volumetric_lighting_tasks(lighting_folder=lighting_folder),
        "shadow_pattern": get_shadow_pattern_tasks(lighting_folder=lighting_folder),
        "dynamic_light": get_dynamic_lighting_tasks(lighting_folder=lighting_folder),
        "dynamic_effects": get_special_dynamic_effects_tasks(lighting_folder=lighting_folder),
    }