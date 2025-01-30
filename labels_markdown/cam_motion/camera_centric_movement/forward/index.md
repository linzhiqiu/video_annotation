# Forward Overview

<details>
<summary><h2>Has Forward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_forward_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move forward (not zooming in) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move forward in space based on its starting position?

- Is the camera moving forward (not zooming in) with respect to itself, creating a noticeable parallax effect?

- Is the forward motion of the camera clear in this shot by comparing the start and end of the shot?

- Is the camera dollying in with respect to itself?

- Is the camera dollying forward with respect to itself?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move forward (not zooming in)?

- Is the camera moving forward?

- Is there clear forward movement when comparing the start and end of the shot?

- Does the camera travel forward in space, rather than zooming in?

- Is the camera pushing forward through the space?

- Does the shot feature a clear forward motion of the camera?

- Is the camera’s movement progressing forward rather than backward?

- Is the forward motion of the camera clear in this shot?

- Does the camera travel forward in space, rather than zooming in?

- Is the camera advancing in the scene?

- Does the perspective shift forward rather than relying on zoom?

- Is the camera physically traveling forward instead of adjusting focal length?

- Is the camera advancing, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves forward (not zooming in) with respect to the initial frame.

- A shot where the camera moves forward in space based on its starting position.

- A video where the camera moves forward (not zooming in) with respect to itself, creating a noticeable parallax effect.

- A scene where the forward motion of the camera is clear by comparing the start and end of the shot.

- The camera pushes in with respect to itself.

- The camera dollies forward with respect to itself.

- A video where the camera dolly moves forward with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves forward (not zooming in).

- A video where the camera is moving forward.

- The camera moves forward in space based on its starting position.

- The camera pushes forward through the space.

- The camera moves forward.

- Camera advances forward.

- A scene where there is clear forward movement when comparing the start and end of the shot.

- A video where the camera travels forward in space, rather than zooming in.

- A shot where the camera pushes forward through the space.

- A video where the shot features a clear forward motion of the camera.

- A scene where the camera’s movement progresses forward rather than backward.

- A video where the forward motion of the camera is clear.

- A shot where the camera travels forward in space rather than zooming in.

- A scene where the camera is advancing in the shot.

- A video where the perspective shifts forward rather than relying on zoom.

- A shot where the camera physically travels forward instead of adjusting focal length.

- A video where the camera advances, creating a strong sense of depth.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.camera_forward_backward_cam_frame != 'forward') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward')) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame != 'forward' and self.cam_motion.camera_zoom == 'in' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Forward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_forward_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move only forward (not zooming in) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is forward motion the only camera movement from the initial frame?

- Is there no other camera motion except forward movement relative to the initial frame?

- Does the camera move forward with respect to itself without any other movement or zooming?

- Is the camera only moving forward relative to the first frame?

- Is the camera only dollying in with respect to itself?

- Is the camera only dollying forward with respect to itself?

- Is the camera only pushing forward without zooming in relative to the first frame?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving forward?

- Is the camera only moving forward (not zooming in) in the scene, creating a noticeable parallax effect?

- Is forward motion the only camera movement in this shot?

- Does the camera travel only forward in space, rather than zooming in?

- Is the camera exclusively moving forward relative to its initial position?

- Does the camera advance in a straight forward direction without any other motions?

- Is the only movement in this shot a forward motion?

- Is there no side, tilt, or zoom adjustments while moving forward?

- Does the camera progress ahead without any vertical or lateral changes?

- Does the tracking movement consist only of a forward push?

- Is the camera strictly advancing forward with no other motion applied?

- Does the shot feature only a single directional forward movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only forward (not zooming in) with respect to the initial frame.

- A shot where the camera advances in space relative to its starting position without any additional motion.

- A video where the camera exclusively moves forward with respect to the initial frame, creating a noticeable parallax effect.

- A scene where the camera progresses forward with respect to itself without any lateral or vertical movement.

- The camera only dollying forward with respect to itself.

- The camera only pushes forward with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves forward with no additional movement type.

- The camera moves forward without incorporating other movement types.

- The camera dollies forward.

- The camera advances forward.

- Camera moves forward.

- A shot where the forward motion is the only movement present in the scene.

- A shot where the camera moves strictly forward without side-to-side or vertical adjustments.

- A video where the camera advances in a single direction without any motion complexity.

- A scene where the camera moves straight ahead without tilting or panning.

- A video where the camera strictly maintains forward movement with no deviation.

- A shot where the tracking movement is purely forward without other motions.

- A scene where the only motion is the camera pushing ahead in a single direction.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward' and self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_forward_backward_cam_frame != 'forward' or not self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward_cam_frame == 'backward'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame != 'forward' and self.cam_motion.camera_zoom == 'in'</code>

- <b>compound_motion_with_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward_cam_frame == 'forward' and not self.cam_motion.check_if_no_motion_cam_frame(exclude=['forward_backward'])</code>

</details>

</details>
