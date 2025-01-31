# Down Overview

<details>
<summary><h2>Has Downward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_down_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move downward (not tilting down) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving downward in space based on its starting position?

- Is the camera moving downward (not tilting down) with respect to itself, creating a noticeable vertical parallax effect?

- Is the downward motion of the camera clear in this shot by comparing the start and end of the shot?

- Is the camera performing a pedestal down movement?

- Is the camera descending with respect to itself?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move downward (not tilting down)?

- Is the camera moving downward?

- Is there clear downward movement when comparing the start and end of the shot?

- Does the camera travel downward in space, rather than tilting down?

- Is the camera lowering through the space?

- Does the shot feature a clear downward motion of the camera?

- Is the camera's movement progressing downward rather than upward?

- Is the downward motion of the camera clear in this shot?

- Does the camera travel downward in space, rather than tilting down?

- Is the camera descending in the scene?

- Does the perspective shift downward rather than relying on tilt?

- Is the camera physically traveling downward instead of rotating?

- Is the camera lowering, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves downward (not tilting down) with respect to the initial frame.

- A shot where the camera moves downward in space based on its starting position.

- A video where the camera moves downward (not tilting down) with respect to itself, creating a noticeable vertical parallax effect.

- A scene where the downward motion of the camera is clear by comparing the start and end of the shot.

- The camera performs a pedestal down movement.

- The camera descends with respect to itself.

- A video where the camera physically lowers with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves downward, not tilting down.

- A video where the camera is moving downward.

- The camera moves downward in space based on its starting position.

- The camera lowers through the space.

- The camera moves downward.

- Camera descends downward.

- A scene where there is clear downward movement when comparing the start and end of the shot.

- A video where the camera travels downward in space, rather than tilting down.

- A shot where the camera lowers through the space.

- A video where the shot features a clear downward motion of the camera.

- A scene where the camera's movement progresses downward rather than upward.

- A video where the downward motion of the camera is clear.

- A shot where the camera travels downward in space rather than tilting down.

- A scene where the camera is descending in the shot.

- A video where the perspective shifts downward rather than relying on tilt.

- A shot where the camera physically travels downward instead of rotating.

- A video where the camera lowers, creating a strong sense of vertical movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down_cam_frame == 'down'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and self.cam_motion.camera_up_down_cam_frame != 'down') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_up_down_cam_frame == 'up'))</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down_cam_frame == 'up' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down_cam_frame != 'down' and self.cam_motion.camera_tilt == 'down' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Downward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_down_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera only move downward (not tilting down) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is downward motion the only camera movement from the initial frame?

- Is there no other camera motion except downward movement relative to the initial frame?

- Does the camera move downward with respect to itself without any other movement or tilting?

- Is the camera only moving downward relative to the first frame?

- Is the camera only performing a pedestal down movement?

- Is the camera only descending with respect to itself?

- Is the camera only moving downward without tilting down relative to the first frame?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving downward?

- Is the camera only moving downward (not tilting down) in the scene, creating a noticeable vertical parallax effect?

- Is downward motion the only camera movement in this shot?

- Does the camera travel only downward in space, rather than tilting down?

- Is the camera exclusively moving downward relative to its initial position?

- Does the camera lower in a straight downward direction without any other motions?

- Is the only movement in this shot a downward motion?

- Is there no forward, sideways, or tilt adjustments while moving downward?

- Does the camera descend without any horizontal changes?

- Does the tracking movement consist only of a downward drop?

- Is the camera strictly descending downward with no other motion applied?

- Does the shot feature only a single directional downward movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves downward (not tilting down) relative to the initial frame.

- A shot where the camera lowers straight down with respect to the initial frame without any other motion.

- A video where the camera exclusively moves downward relative to the initial frame, creating a noticeable vertical parallax effect.

- A scene where the camera moves only downward relative to itself, avoiding tilting or other motions.

- The camera is only performing a pedestal down movement.

- The camera is only descending with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves downward without incorporating other movement types.

- A shot where the downward motion is the only movement present in the scene.

- A shot where the camera moves strictly downward without forward or sideways movement.

- A video where the camera descends in a single direction without any other adjustments.

- A scene where the camera lowers without shifting horizontally.

- A video where the camera strictly maintains downward movement with no deviation.

- A shot where the tracking movement is purely downward with no other motion.

- A scene where the only movement present is the camera lowering vertically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down_cam_frame == 'down' and self.cam_motion.check_if_no_motion_cam_frame(exclude=['up_down']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_up_down_cam_frame != 'down' or not self.cam_motion.check_if_no_motion_cam_frame(exclude=['up_down']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down_cam_frame == 'up'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down_cam_frame != 'down' and self.cam_motion.camera_tilt == 'down'</code>

- <b>compound_motion_with_down</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down_cam_frame == 'down' and not self.cam_motion.check_if_no_motion_cam_frame(exclude=['up_down'])</code>

</details>

</details>
