import glob
import json
from typing import Dict, List


def map_camera_motion(camera_motion_annotations: List[Dict]) -> List[Dict]:
    
    res = {}
    
    # Set shot transition
    shot_transition = camera_motion_annotations.get("Are there any shot transitions?", "")
    shot_transition = True if shot_transition == "Yes" else False
    res['shot_transition'] = shot_transition
    
    # Set steadiness and camera movement
    steadiness = camera_motion_annotations.get("What is the camera steadiness?", "")
    camera_movement = camera_motion_annotations.get("Is there any camera movement other than shaking?", "")
    steadiness_map = {
        "Static (Fixed Camera)": 'static',
        "Very Smooth / No Shaking (e.g., Drone shot with no shaking at all)": 'very_smooth',
        "Smooth / Minimal Shaking (e.g., Steadicam shot or stabilized handheld shot)": 'smooth',
        "Unsteady (e.g., Somewhat shaky handheld shot)": 'unsteady',
        "Very Unsteady (e.g., Shaky shot)": 'very_unsteady'
    }
    camera_movement_map = {
        "Yes with major, complex motion": 'major_complex',
        "Yes with major, simple motion": 'major_simple',
        "Yes with minor motion": 'minor',
        "No": 'no'
    }
    steadiness = steadiness_map.get(steadiness, "")
    camera_movement = camera_movement_map.get(camera_movement, "")
    res['steadiness'] = steadiness
    res['camera_movement'] = camera_movement
    
    # Set camera movement speed and camera effect
    camera_movement_speed = camera_motion_annotations.get("How fast is the camera movement? (e.g., crash zoom, whip pan)?", "")
    camera_movement_speed_map = {
        "Slow": 'slow',
        "Regular": 'regular',
        "Fast": 'fast'
    }
    camera_movement_speed = camera_movement_speed_map.get(camera_movement_speed, "")
    frame_freezing = camera_motion_annotations.get("Is there a frame-freezing effect in this video?", "")
    frame_freezing = True if frame_freezing == "Yes" else False
    dolly_zoom = camera_motion_annotations.get("Is there a dolly-zoom effect in this video?", "")
    dolly_zoom = True if dolly_zoom == "Yes" else False
    motion_blur = camera_motion_annotations.get("Is there a motion blur effect in this video?", "")
    motion_blur = True if motion_blur == "Yes" else False
    cinemagraph = camera_motion_annotations.get("Is there a cinemagraph effect in this video?", "")
    cinemagraph = True if cinemagraph == "Yes" else False
    res['camera_motion_speed'] = camera_movement_speed
    res['frame_freezing'] = frame_freezing
    res['dolly_zoom'] = dolly_zoom
    res['motion_blur'] = motion_blur
    res['cinemagraph'] = cinemagraph
    
    # Set tracking shot
    is_tracking = camera_motion_annotations.get("Does the camera track the moving subject(s)?", "")
    is_tracking = True if is_tracking == "Yes" else False
    res['is_tracking'] = is_tracking
    
    tracking_type = []
    if camera_motion_annotations.get("Is the camera side-tracking (moving alongside the subject)?", "") == 'Yes':
        tracking_type.append('side')
    if camera_motion_annotations.get("Is the camera tail-tracking (following behind the subject)?", "") == 'Yes':
        tracking_type.append('tail')
    if camera_motion_annotations.get("Is the camera lead-tracking (moving ahead of the subject)?", "") == 'Yes':
        tracking_type.append('lead')
    if camera_motion_annotations.get("Is the camera aerial-tracking (from above, e.g., drone or crane)?", "") == 'Yes':
        tracking_type.append('aerial')
    if camera_motion_annotations.get("Is the camera arc-tracking (arcing around the subject)?", "") == 'Yes':
        tracking_type.append('arc')
    if camera_motion_annotations.get("Is the camera pan-tracking (panning to follow the subject)?", "") == 'Yes':
        tracking_type.append('pan')
    if camera_motion_annotations.get("Is the camera tilt-tracking (tilting to follow the subject)?", "") == 'Yes':
        tracking_type.append('tilt')
    res['tracking_shot_types'] = tracking_type
    
    subject_size_change = camera_motion_annotations.get("Does the size of the subject change during tracking?", "")
    subject_size_change_map = {
        "No": 'no',
        "Subject gets larger": 'larger',
        "Subject gets smaller": 'smaller'
    }
    subject_size_change = subject_size_change_map.get(subject_size_change, "")
    res['subject_size_change'] = subject_size_change
    
    # Set camera motion
    forward_backward = camera_motion_annotations.get("Is the camera moving forward or backward?", "")
    zooming = camera_motion_annotations.get("Is the camera zooming?", "")
    left_right = camera_motion_annotations.get("Is the camera moving (trucking) to the left or right?", "")
    panning = camera_motion_annotations.get("Is the camera panning?", "")
    up_down = camera_motion_annotations.get("Is the camera moving up or down?", "")
    tilting = camera_motion_annotations.get("Is the camera tilting?", "")
    arcing = camera_motion_annotations.get("Is the camera moving in an arc?", "")
    rolling = camera_motion_annotations.get("Is the camera rolling?", "")
    description = camera_motion_annotations.get("If the camera motion is too complex, how would you describe it?", "")
    
    forward_backward_map = {
        "No": 'no',
        "Forward (e.g., Dolly-in / Push-in)": 'forward',
        "Backward (e.g., Dolly-out / Pull-out)": 'backward'
    }
    
    zooming_map = {
        "No": 'no',
        "Zooming In": 'in',
        "Zooming Out": 'out'
    }
    
    left_right_map = {
        "No": 'no',
        "Left-to-Right (--->)": 'left_to_right',
        "Right-to-Left (<---)": 'right_to_left'
    }
    
    panning_map = {
        "No": 'no',
        "Left-to-Right (-->)": 'left_to_right',
        "Right-to-Left (<--)": 'right_to_left'
    }
    
    up_down_map = {
        "No": 'no',
        "Up (e.g., Pedestal up)": 'up',
        "Down (e.g., Pedestal down)": 'down'
    }
    
    tilting_map = {
        "No": 'no',
        "Up": 'up',
        "Down": 'down'
    }
    
    arcing_map = {
        "No": 'no',
        "Clockwise (e.g., Arc clockwise)": 'clockwise',
        "Counter-clockwise (e.g., Arc counter-clockwise)": 'counter_clockwise',
        "Crane Up": 'crane_up',
        "Crane Down": 'crane_down'
    }
    
    rolling_map = {
        "No": 'no',
        "Clockwise": 'clockwise',
        "Counter-clockwise": 'counter_clockwise'
    }
    
    forward_backward = forward_backward_map.get(forward_backward, "")
    zooming = zooming_map.get(zooming, "")
    left_right = left_right_map.get(left_right, "")
    panning = panning_map.get(panning, "")
    up_down = up_down_map.get(up_down, "")
    tilting = tilting_map.get(tilting, "")
    arcing = arcing_map.get(arcing, "")
    rolling = rolling_map.get(rolling, "")

    res['camera_forward_backward'] = forward_backward
    res['camera_zoom'] = zooming
    res['camera_left_right'] = left_right
    res['camera_pan'] = panning
    res['camera_up_down'] = up_down
    res['camera_tilt'] = tilting
    if arcing not in ['crane_up', 'crane_down']:
        res['camera_arc'] = arcing
    else:
        res['camera_crane'] = arcing
    res['camera_roll'] = rolling
    res['complex_motion_description'] = description
    
    return res

def map_shot_composition(shot_composition_annotations: List[Dict]) -> List[Dict]:
    
    res = {}
    
    # Set shot transition
    shot_transition = shot_composition_annotations.get("Are there any shot transitions?", "")
    shot_transition = True if shot_transition == "Yes" else False
    res['shot_transition'] = shot_transition

    # Set shot basics, shotsize and height
    shot_type = shot_composition_annotations.get("Shot type:", "")
    complex_shot = shot_composition_annotations.get("Complex shot:", "")
    complex_reason = shot_composition_annotations.get("Reason for text description:", "")
    init_shotsize = shot_composition_annotations.get("Initial shot size:", "")
    end_shotsize = shot_composition_annotations.get("Ending shot size:", "")
    shotsize_description = shot_composition_annotations.get("Describe complex shot size:", "")
    init_relative_height = shot_composition_annotations.get("Initial relative height:", "")
    end_relative_height = shot_composition_annotations.get("Ending relative height:", "")
    relative_height_description = shot_composition_annotations.get("Describe complex relative height:", "")
    init_overall_height = shot_composition_annotations.get("Initial overall height:", "")
    end_overall_height = shot_composition_annotations.get("Ending overall height:", "")
    overall_height_description = shot_composition_annotations.get("Describe complex overall height:", "")
    
    shot_type_map = {
        "Clear human subject(s)": 'human',
        "Clear non-human subject(s)": 'non_human',
        "Change of subject(s)": 'change_of_subject',
        "Scenery shot": 'scenery',
        "Complex shot": "complex"
    }
    res['shot_type'] = shot_type_map.get(shot_type, "")
    
    complex_shot_map = {
        "Not Complex": 'not_complex',
        "Clear Subject with Dynamic Size (subject)": 'clear_subject_dynamic_size',
        "Different Subjects in Focus (subject)": 'different_subject_in_focus',
        "Clear yet Atypical Subject (subject)": 'clear_subject_atypical',
        "Many Subject(s) with One Clear Focus (subject)": 'many_subject_one_focus',
        "Many Subject(s) with No Clear Focus (scenery)": 'many_subject_no_focus',
        "Description (text)": 'description',
        "N/A (e.g., abstract/FPS with body parts/screenshot/etc.)": 'unknown'
    }
    if shot_type_map.get(complex_shot, "") != 'not_complex':
        res['complex_shot_type'] = complex_shot_map.get(complex_shot, "")
    
    complex_reason_map = {
        "Not Complex": 'not_complex',
        "Subject-Scene Size Mismatch": 'subject_scene_mismatch',
        "Back-and-Forth Size Changes": 'back_and_forth_change',
        "Others": 'others'
    }
    if shot_type_map.get(complex_shot, "") != 'not_complex':
        res['shot_size_description_type'] = complex_reason_map.get(complex_reason, "")
    
    init_shotsize_map = {
        "N/A (no subject)": 'unknown',
        "Extreme wide/long shot": 'extreme_wide',
        "Wide/long shot": 'wide',
        "Full shot (Subject Shot Only)": 'full',
        "Medium-Full shot (Human Subject Shot Only)": 'medium_full',
        "Medium shot (Subject Shot Only)": 'medium',
        "Medium Close-up shot (Human Subject Shot Only)": 'medium_close_up',
        "Close-up shot": 'close_up',
        "Extreme Close-up shot": 'extreme_close_up'
    }
    res['shot_size_start'] = init_shotsize_map.get(init_shotsize, "")
    
    end_shotsize_map = {
        "N/A (no subject / no change)": 'unknown',
        "Extreme wide/long shot": 'extreme_wide',
        "Wide/long shot": 'wide',
        "Full shot (Subject Shot Only)": 'full',
        "Medium-Full shot (Human Subject Shot Only)": 'medium_full',
        "Medium shot (Subject Shot Only)": 'medium',
        "Medium Close-up shot (Human Subject Shot Only)": 'medium_close_up',
        "Close-up shot": 'close_up',
        "Extreme Close-up shot": 'extreme_close_up'
    }
    res['shot_size_end'] = end_shotsize_map.get(end_shotsize, "")
    res['shot_size_description'] = shotsize_description
    
    init_relative_height_map = {
        "N/A (no subject)": 'unknown',
        "Above the subject": 'above_subject',
        "At the subject": 'at_subject',
        "Below the subject": 'below_subject'
    }
    res['subject_height_start'] = init_relative_height_map.get(init_relative_height, "")
    
    end_relative_height_map = {
        "N/A (no subject / no change)": 'unknown',
        "Above the subject": 'above_subject',
        "At the subject": 'at_subject',
        "Below the subject": 'below_subject'
    }
    res['subject_height_end'] = end_relative_height_map.get(end_relative_height, "")
    res['subject_height_description'] = relative_height_description
    
    init_overall_height_map = {
        "N/A": 'unknown',
        "Aerial-level": 'aerial_level',
        "Overhead-level": 'overhead_level',
        "Eye-level": 'eye_level',
        "Hip-level": 'hip_level',
        "Ground-level": 'ground_level',
        "Water-level": 'water_level',
        "Underwater": 'underwater_level'
    }
    res['overall_height_start'] = init_overall_height_map.get(init_overall_height, "")
    
    end_overall_height_map = {
        "N/A (e.g., no changes)": 'unknown',
        "Aerial-level": 'aerial_level',
        "Overhead-level": 'overhead_level',
        "Eye-level": 'eye_level',
        "Hip-level": 'hip_level',
        "Ground-level": 'ground_level',
        "Water-level": 'water_level',
        "Underwater": 'underwater_level'
    }
    res['overall_height_end'] = end_overall_height_map.get(end_overall_height, "")
    res['overall_height_description'] = overall_height_description
    
    
    # Set video quality
    distortion = shot_composition_annotations.get("Lens distortion:", "")
    watermark = shot_composition_annotations.get("Text/watermarks present?", "")
    video_speed = shot_composition_annotations.get("Video speed:", "")
    camera_pov = shot_composition_annotations.get("Camera POV:", "")
    
    distortion_map = {
        "Regular Lens": 'regular',
        "Barrel Distortion (e.g., Wide-angle lens)": 'barrel',
        "Fisheye Distortion (e.g., Fisheye lens)": 'fisheye'
    }
    res['lens_distortion'] = distortion_map.get(distortion, "")
    
    res['has_overlays'] = True if watermark == "Yes" else False
    
    video_speed_map = {
        "Time-lapse": 'time_lapse',
        "Fast-Motion": 'fast_motion',
        "Regular": 'regular',
        "Slow-Motion": 'slow_motion',
        "Stop-Motion": 'stop_motion',
        "Speed-Ramp": 'speed_ramp',
        "Time-Reversed": 'time_reversed'
    }
    res['video_speed'] = video_speed_map.get(video_speed, "")
    
    camera_pov_map = {
        "N/A": 'unknown',
        "First-person POV": 'first_person',
        "Drone POV": 'drone_pov',
        "Third-person Full-body POV (Gaming only)": 'third_person_full_body',
        "Third-person Over-the-shoulder POV (Gaming / Film)": 'third_person_over_shoulder',
        "Third-person Over-the-hip POV (Gaming only)": 'third_person_over_hip',
        "Third-person Side view POV (Gaming only)": 'third_person_side_view',
        "Third-person Isometric POV (Gaming only)": 'third_person_isometric',
        "Third-person Top-down/Oblique POV (Gaming only)": 'third_person_top_down',
        "Broadcast POV (Television station)": 'broadcast_pov',
        "Overhead POV (Hands-on demonstration)": 'overhead_pov',
        "Selfie POV": 'selfie_pov',
        "Screen Recording (software tutorials, zoom calls)": 'screen_recording',
        "Dashcam POV": 'dashcam_pov',
        "Locked-on POV": 'locked_on_pov'
    }
    res['camera_pov'] = camera_pov_map.get(camera_pov, "")

    # Set camera angle
    init_camera_angle = shot_composition_annotations.get("Initial camera angle:", "")
    end_camera_angle = shot_composition_annotations.get("Ending camera angle:", "")
    camera_angle_description = shot_composition_annotations.get("Describe complex angle:", "")
    dutch_angle = shot_composition_annotations.get("Dutch angle (>15) present?", "")
    
    init_camera_angle_map = {
        "N/A": 'unknown',
        "Bird's eye": 'bird_eye_angle',
        "High angle (Looking down)": 'high_angle',
        "Level Angle": 'level_angle',
        "Low angle (Looking up)": 'low_angle',
        "Worm's eye": 'worm_eye_angle'
    }
    res['camera_angle_start'] = init_camera_angle_map.get(init_camera_angle, "")
    
    end_camera_angle_map = {
        "N/A (e.g., no change)": 'unknown',
        "Bird's eye": 'bird_eye_angle',
        "High angle (Looking down)": 'high_angle',
        "Level Angle": 'level_angle',
        "Low angle (Looking up)": 'low_angle',
        "Worm's eye": 'worm_eye_angle'
    }
    res['camera_angle_end'] = end_camera_angle_map.get(end_camera_angle, "")
    res['camera_angle_description'] = camera_angle_description
    
    dutch_angle_map = {
        "No": 'no',
        "Varying": 'varying',
        "Yes": 'yes'
    }
    res['dutch_angle'] = dutch_angle_map.get(dutch_angle, "")
    
    # Set camera focus
    focus_type = shot_composition_annotations.get("Focus type:", "")
    focus_depth_start = shot_composition_annotations.get("Focus depth (start):", "")
    focus_depth_end = shot_composition_annotations.get("Focus depth (end):", "")
    focus_change_reason = shot_composition_annotations.get("Reason for focus change:", "")
    focus_description = shot_composition_annotations.get("Describe complex focus:", "")
    
    focus_type_map = {
        "Deep focus": 'deep_focus',
        "Shallow focus": 'shallow_focus',
        "Ultra shallow focus": 'ultra_shallow_focus',
        "N/A": 'unknown'
    }
    res['camera_focus'] = focus_type_map.get(focus_type, "")
    
    focus_depth_start_map = {
        "Foreground": 'foreground',
        "Middleground": 'middle_ground',
        "Background": 'background',
        "Out of focus": 'out_of_focus',
        "N/A": 'unknown'
    }
    res['focus_plane_start'] = focus_depth_start_map.get(focus_depth_start, "")
    
    focus_depth_end_map = {
        "Foreground": 'foreground',
        "Middleground": 'middle_ground',
        "Background": 'background',
        "Out of focus": 'out_of_focus',
        "N/A": 'unknown'
    }
    res['focus_plane_end'] = focus_depth_end_map.get(focus_depth_end, "")
    
    focus_change_reason_map = {
        "No Change": 'no_change',
        "Camera or Subject Movement": 'camera_subject_movement',
        "Rack Focus": 'rack_focus',
        "Pull Focus": 'pull_focus',
        "Focus Tracking": 'focus_tracking',
        "Others (please specify)": 'others'
    }
    res['focus_change_reason'] = focus_change_reason_map.get(focus_change_reason, "")
    res['camera_focus_description'] = focus_description
    return res
    
    
def transform_to_caption(label_pizza_annotations: List[Dict] = None, question_type: str = 'camera_motion', output_path: str = None) -> List[Dict]:
    
    if question_type not in ['camera_motion', 'shot_composition']:
        raise ValueError(f"Invalid question type: {question_type}")
    res = []
    if question_type == 'camera_motion':
        for annotation in label_pizza_annotations:
            video_name = annotation['video_uid']
            user_name = annotation['user_name']
            annotations = annotation['answers']
            anno = map_camera_motion(annotations)
            res.append({
                'video_name': video_name,
                'user_name': user_name,
                'answers': anno
            })
            
    elif question_type == 'shot_composition':
        for annotation in label_pizza_annotations:
            video_name = annotation['video_uid']
            user_name = annotation['user_name']
            annotations = annotation['answers']
            anno = map_shot_composition(annotations)
            res.append({
                'video_name': video_name,
                'user_name': user_name,
                'answers': anno
            })
    with open(output_path, 'w') as f:
        json.dump(res, f, indent=2)





