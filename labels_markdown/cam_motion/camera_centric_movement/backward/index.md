# Backward Overview

<details>
<summary><h2>Has Backward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_backward_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move backward (not zooming out) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move backward in space based on its starting position?

- Is the camera moving backward (not zooming out) with respect to itself, creating a noticeable parallax effect?

- Is the backward motion of the camera clear in this shot by comparing the start and end of the shot?

- Is the camera dollying out with respect to itself?

- Is the camera pulling back with respect to itself?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move backward (not zooming out)?

- Is the camera moving backward?

- Is there clear backward movement when comparing the start and end of the shot?

- Does the camera travel backward in space, rather than zooming out?

- Is the camera pulling back through the space?

- Does the shot feature a clear backward motion of the camera?

- Is the camera's movement progressing backward rather than forward?

- Is the backward motion of the camera clear in this shot?

- Does the camera travel backward in space, rather than zooming out?

- Is the camera retreating in the scene?

- Does the perspective shift backward rather than relying on zoom?

- Is the camera physically traveling backward instead of adjusting focal length?

- Is the camera pulling back, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves backward (not zooming out) with respect to the initial frame.

- A shot where the camera moves backward in space based on its starting position.

- A video where the camera moves backward (not zooming out) with respect to itself, creating a noticeable parallax effect.

- A scene where the backward motion of the camera is clear by comparing the start and end of the shot.

- The camera pulls back with respect to itself.

- The camera dollies backward with respect to itself.

- A video where the camera dolly moves backward with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward (not zooming out).

- A video where the camera is moving backward.

- The camera moves backward in space based on its starting position.

- The camera pulls back through the space.

- The camera moves backward.

- Camera retreats backward.

- A scene where there is clear backward movement when comparing the start and end of the shot.

- A video where the camera travels backward in space, rather than zooming out.

- A shot where the camera pulls back through the space.

- A video where the shot features a clear backward motion of the camera.

- A scene where the camera's movement progresses backward rather than forward.

- A video where the backward motion of the camera is clear.

- A shot where the camera travels backward in space rather than zooming out.

- A scene where the camera is retreating in the shot.

- A video where the perspective shifts backward rather than relying on zoom.

- A shot where the camera physically travels backward instead of adjusting focal length.

- A video where the camera pulls back, creating a strong sense of depth.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and self.cam_motion.camera_forward_backward_cam_frame != 'backward') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward'))</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame != 'backward' and self.cam_motion.camera_zoom == 'out' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Backward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_backward_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move only backward (not zooming out) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is backward motion the only camera movement from the initial frame?

- Is there no other camera motion except backward movement relative to the initial frame?

- Does the camera move backward with respect to itself without any other movement or zooming?

- Is the camera only moving backward relative to the first frame?

- Is the camera only dollying out with respect to itself?

- Is the camera only pulling back with respect to itself?

- Is the camera only moving backward without zooming out relative to the first frame?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving backward?

- Is the camera only moving backward (not zooming out) in the scene, creating a noticeable parallax effect?

- Is backward motion the only camera movement in this shot?

- Does the camera travel only backward in space, rather than zooming out?

- Is the camera exclusively moving backward relative to its initial position?

- Does the camera retreat in a straight backward direction without any other motions?

- Is the only movement in this shot a backward motion?

- Is there no side, tilt, or zoom adjustments while moving backward?

- Does the camera pull back without any vertical or lateral changes?

- Does the tracking movement consist only of a backward pull?

- Is the camera strictly retreating backward with no other motion applied?

- Does the shot feature only a single directional backward movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only backward (not zooming out) with respect to the initial frame.

- A shot where the camera retreats in space relative to its starting position without any additional motion.

- A video where the camera exclusively moves backward with respect to the initial frame, creating a noticeable parallax effect.

- A scene where the camera pulls back with respect to itself without any lateral or vertical movement.

- The camera only dollying backward with respect to itself.

- The camera only pulls back with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward with no additional movement type.

- The camera moves backward without incorporating other movement types.

- The camera dollies backward.

- The camera retreats backward.

- Camera moves backward.

- A shot where the backward motion is the only movement present in the scene.

- A shot where the camera moves strictly backward without side-to-side or vertical adjustments.

- A video where the camera retreats in a single direction without any motion complexity.

- A scene where the camera moves straight back without tilting or panning.

- A video where the camera strictly maintains backward movement with no deviation.

- A shot where the tracking movement is purely backward without other motions.

- A scene where the only motion is the camera pulling back in a single direction.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward' and self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_forward_backward_cam_frame != 'backward' or not self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame != 'backward' and self.cam_motion.camera_zoom == 'out'</code>

- <b>compound_motion_with_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward' and not self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward'])</code>

</details>

</details>
