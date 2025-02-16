import torch
import os
import json
from caption_policy.vanilla_program import VanillaSubjectPolicy, VanillaScenePolicy, VanillaSubjectMotionPolicy, VanillaSpatialPolicy, VanillaCameraPolicy

res = torch.load('temp.pt')

caption_programs = {
    "subject_policy": VanillaSubjectPolicy(),
    "scene_policy": VanillaScenePolicy(),
    "subject_motion_policy": VanillaSubjectMotionPolicy(),
    "spatial_policy": VanillaSpatialPolicy(),
    "camera_policy": VanillaCameraPolicy()
}

for video_data in res:
    # check if cam_setup is set
    try:
        cam_setup = video_data.cam_setup
    except:
        print(f"cam_setup is not set for {video_data.workflows[0].video_name}")
        pass
    
    if video_data.workflows[0].video_name == 'nb69sgB5mG0.2.2.mp4':
        video_data.cam_setup.overall_height_start = "water_level"
    
    video_data.cam_setup.update()
    video_data.cam_motion.update()
    video_data.cam_setup.subject_description = "**{NO DESCRIPTION FOR SUBJECTS YET}**"
    video_data.cam_setup.scene_description = "**{NO DESCRIPTION FOR SCENE YET}**"

if not os.path.exists('temp_captions/'):
    os.makedirs('temp_captions/')
    
for video_data in res:
    video_name = video_data.workflows[0].video_name
    video_name_no_ext = video_name.rsplit('.', 1)[0]
    if not os.path.exists(os.path.join('temp_captions/', video_name_no_ext)):
        os.makedirs(os.path.join('temp_captions/', video_name_no_ext))
    for caption_policy_name, caption_policy in caption_programs.items():
        caption = caption_policy(video_data)
        with open(os.path.join('temp_captions/', video_name_no_ext, f"{caption_policy_name}.json"), 'w') as f:
            json.dump(caption, f, indent=4)
            print(f"Saved caption for {video_name} using {caption_policy_name} policy.")