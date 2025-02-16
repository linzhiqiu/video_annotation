# Cam_motion Overview

<details>
<summary><h2>Has Frame Freezing Effect</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_frame_freezing</code>


<h3>📖 Definition:</h3>
Does the video contain a frame freeze effect at any point?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the shot feature a frame that stays still while the video continues?

- Is there a paused frame effect within the video?

- Does the video include a sudden freeze of a specific frame?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is a single frame held for a period before resuming motion?

- Does the scene contain a sudden freeze of motion?

- Is there a moment where movement stops while the video continues playing?

- Does the video create a still frame effect in the middle of playback?

- Is the action interrupted by a frame freeze?

- Does the shot momentarily pause on a single frame before resuming?

- Is a still image effect applied to a moving video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A scene where the video includes a frame freezing effect.

- A shot where a single frame is frozen at some point.

- A video where the motion stops temporarily due to a frame freeze.

- The video pauses on a still frame before continuing.

- A sequence where a single frame is held for dramatic effect.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A moment in the video where the motion is held still before resuming.

- A video with a brief still-frame effect in the middle of an action.

- A scene where movement is interrupted by a frozen frame.

- A shot where a still image effect is applied temporarily.

- A video where a specific frame is paused momentarily.

- A cinematic freeze-frame moment within the video sequence.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.frame_freezing is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.frame_freezing is False</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>static_camera</b>: <code>self.cam_motion.steadiness in ['static'] and self.cam_motion.frame_freezing is False</code>

</details>

</details>

<details>
<summary><h2>Has Motion Blur Effect</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_motion_blur</code>


<h3>📖 Definition:</h3>
Does the video contain noticeable motion blur?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is there a motion blur effect present in the shot?

- Does fast movement in the video create a blurred effect?

- Does the shot exhibit motion blur due to rapid movement?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the motion in the scene accompanied by streaking or blurring?

- Is the video affected by motion blur when objects move quickly?

- Does the scene contain visible blurring from motion?

- Is the image smeared due to rapid movement?

- Does the camera movement create a motion blur effect?

- Is there a blurred trail behind moving objects?

- Does the shot include intentional motion blur for a cinematic effect?

- Is the video affected by a loss of clarity due to motion?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A scene where the video exhibits a motion blur effect.

- A shot where moving objects appear blurred due to rapid motion.

- A video where motion creates a smeared visual effect.

- The camera movement results in noticeable motion blur.

- A sequence where fast action introduces streaking or blurring effects.

- A moment in the video where motion blur is strongly visible.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with a blurry effect due to high-speed movement.

- A shot where fast motion causes objects to blur together.

- A scene demonstrating motion blur from rapid camera movement.

- A video where the subject appears streaked due to fast motion.

- A cinematic shot featuring intentional motion blur.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.motion_blur is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.motion_blur is False</code>

</details>

<details>
<summary><h2>Shot transition</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_shot_transition_cam_motion</code>


<h3>📖 Definition:</h3>
Does the video include shot transitions?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the video include one or more shot transitions?

- Does the video contain hard cuts or soft transitions, or a combination of both?

- Are there any shot transitions in the video?

- Does this footage feature one or more cuts or soft transitions?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a transition between shots?

- Does the video include a shot transition?

- Does the video include a hard cut or a soft transition?

- Is there a shot transition?

- Is a cut or soft transition used in this footage?

- Does the video include any shot transitions?

- Does the video include a hard cut or a soft transition?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that includes shot transitions.

- A video showing one or more shot transitions.

- The video features hard cuts, soft transitions, or a combination of both.

- The video contains one or more cuts or soft transitions between shots.

- A video that includes at least one shot transition.

- A video with at least one shot transition.

- A video featuring one or more shot transitions.

- A video with one or more shot transitions.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video includes either a hard cut or a soft transition.

- The video shows a hard cut or a soft transition between shots.

- A video where there is a transition between shots.

- The video contains a cut or a soft transition between scenes.

- A video that includes shot transitions between scenes.

- A video with a hard cut or soft transition.

- A video that includes a shot transition.

- A video with a cut or soft transition.

- A video featuring shot transitions.

- A video with either a hard cut or soft transition.

- A video with at least one transition.

- A video with shot transitions.

- A video with cuts or soft transitions.

- A video with hard cuts, soft transitions, or both.

- A video where shots change with a transition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.shot_transition</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.shot_transition</code>

</details>


## Subcategories

- [Arc_crane_movement](./arc_crane_movement/index.md)
- [Camera_centric_movement](./camera_centric_movement/index.md)
- [Dolly_zoom_movement](./dolly_zoom_movement/index.md)
- [Ground_centric_movement](./ground_centric_movement/index.md)
- [Motion_complexity](./motion_complexity/index.md)
- [Object_centric_movement](./object_centric_movement/index.md)
- [Scene_movement](./scene_movement/index.md)
- [Steadiness_and_movement](./steadiness_and_movement/index.md)