# Forward Overview

<details>
<summary><h2>Has Forward Movement (Relative to Ground, Bird’s/Worm’s Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_forward_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera move forward (not zooming in) in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving forward in the scene?

- Is the camera moving forward?

- Is the camera moving forward, creating a noticeable parallax effect?

- Is the camera moving forward (not zooming in) in the scene, creating a noticeable parallax effect?

- Does the camera move in the forward direction relative to the ground?

- Is the camera pushing forward through the space?

- Is the camera pushing in?

- Is the camera dollying in?

- Is the camera dollying forward?

- Does the shot feature a clear forward motion of the camera?

- Is the camera’s movement progressing forward rather than backward?

- Is the forward motion of the camera clear in this shot?

- Does the camera travel forward in space, rather than zooming in?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera advancing in the scene?

- Does the perspective shift forward rather than relying on zoom?

- Is the camera physically traveling forward instead of adjusting focal length?

- Is the camera advancing, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera advances forward, rather than zooming in.

- A video where the camera travels forward, creating noticeable parallax.

- A scene where the camera moves physically forward instead of zooming.

- A tracking shot where the camera moves forward relative to the ground plane.

- A shot where the camera moves straight ahead, maintaining a sense of forward motion.

- A video where the camera moves forward (not zooming in) in the scene.

- A shot where the camera is moving forward within the scene.

- A video where the camera moves forward, creating a noticeable parallax effect.

- A shot where the camera moves in the forward direction relative to the ground.

- A video where the camera pushes forward through space.

- A scene where the camera pushes in.

- A video where the camera performs a dolly-in motion.

- A shot where the camera dollies forward.

- The camera dollies in, moving forward in the scene.

- A video where the camera progresses forward rather than backward.

- A shot where the forward motion of the camera is clearly visible.

- A video where the camera travels forward in space rather than zooming in.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the shot features a clear forward motion of the camera.

- A shot where the camera dolly moves straight ahead.

- A video where the camera moves in a forward direction within the scene.

- A shot where the camera advances rather than zooming in.

- A video where the camera progresses forward, creating depth.

- A scene where the camera moves ahead rather than pulling back.

- A shot where the perspective shifts forward dynamically.

- A video where the camera maintains a continuous forward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.forward and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.forward and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'backward' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward != 'forward' and self.cam_motion.camera_zoom == 'in' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Has Forward Movement (Relative to Ground, Bird’s/Worm’s Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_forward_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move forward (not zooming in) in the scene, or move north if it's a bird's eye view, or move south if it's a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move forward (not zooming in) in the scene, or move upward if it's a bird's eye view, or move downward if it's a worm's eye view?

- Is the camera moving forward in the scene (north in a bird's eye view or south in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving forward in the scene?

- Is the camera moving forward?

- Is the camera moving forward (not zooming in) in the scene, creating a noticeable parallax effect?

- Is the forward motion of the camera clear in this shot?

- Does the camera travel forward in space, rather than zooming in?

- Is the camera advancing in the scene?

- Does the camera move in the forward direction relative to the ground?

- Is the camera’s movement progressing forward rather than backward?

- Is the camera pushing forward through the space?

- Does the shot feature a clear forward motion of the camera?

- Does the perspective shift forward rather than relying on zoom?

- Is the camera physically traveling forward instead of adjusting focal length?

- Is the camera advancing, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves forward (not zooming in) in the scene or moves north in a bird's eye view or south in a worm's eye view.

- A video where the camera moves forward (not zooming in) in the scene or moves north in a bird's eye view or south in a worm's eye view, creating a noticeable parallax effect.

- A tracking shot where the camera moves forward (not zooming in) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves forward, not zooming in.

- A shot where the camera advances forward, rather than zooming in.

- A video where the camera travels forward, creating noticeable parallax.

- A scene where the camera moves physically forward instead of zooming.

- A video where the camera moves in a forward direction within the scene.

- A shot where the camera advances rather than zooming in.

- A video where the camera progresses forward, creating depth.

- A scene where the camera moves ahead rather than pulling back.

- A shot where the perspective shifts forward dynamically.

- A video where the camera maintains a continuous forward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.forward</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.forward</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'backward' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward != 'forward' and self.cam_motion.camera_zoom == 'in' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Forward Movement (Relative to Ground, Bird’s/Worm’s Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_forward_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera only move forward (not zooming in) with respect to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera only moving forward with respect to the ground?

- Is the camera only moving forward without zooming in relative to the ground?

- Is the camera only pushing in with respect to the ground?

- Is the camera only dollying forward (not zooming in) relative to the ground?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving forward in the scene?

- Is the camera only moving forward (not zooming in) in the scene, creating a noticeable parallax effect?

- Relative to ground, is forward motion the only camera movement in this shot?

- Does the camera travel only forward in space, rather than zooming in?

- Is the camera exclusively moving forward in the scene?

- Does the camera move straight ahead without any other motion?

- Is the camera's motion restricted to only forward movement?

- Does the tracking movement involve only a forward push?

- Is the camera moving ahead without any vertical or lateral adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves forward (not zooming in) relative to the ground.

- A shot where the camera moves straight ahead with respect to the ground without any other motion.

- A video where the camera exclusively moves forward relative to the ground plane, creating a noticeable parallax effect.

- A scene where the camera moves only forward relative to the ground, avoiding zooming or other motions.

- The camera is only dollying forward with respect to the ground.

- The camera is only pushing in with respect to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves forward without incorporating other movement types.

- A shot where the forward motion is the only movement present in the scene.

- A shot where the camera moves strictly forward without lateral or vertical movement.

- A video where the camera advances in a single direction without any other adjustments.

- A scene where the camera progresses forward without shifting side to side.

- A video where the camera strictly maintains forward movement with no deviation.

- A shot where the tracking movement is purely forward with no other motion.

- A scene where the only movement present is the camera pushing ahead.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.forward and self.cam_motion.check_if_no_motion(exclude=['forward']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.forward and self.cam_motion.check_if_no_motion(exclude=['forward'])) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'backward' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward != 'forward' and self.cam_motion.camera_zoom == 'in' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

- <b>compound_motion_with_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward == 'forward' and not self.cam_motion.check_if_no_motion(exclude=['forward_backward']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

</details>

<details>
<summary><h2>Only Forward Movement (Relative to Ground, Bird’s/Worm’s Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_forward_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move only forward (not zooming in) in the scene, or only northward in a bird's eye view, or only southward in a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move only forward (not zooming in) in the scene, or only upward in a bird's eye view, or only downward in a worm's eye view?

- Does the camera move only forward (not zooming in) in the scene, or only move north if it's a bird's eye view, or only move south if it's a worm's eye view?

- Is the camera only moving forward in the scene (north in a bird's eye view or south in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving forward in the scene?

- Is the camera only moving forward?

- Is the camera only moving forward (not zooming in) in the scene, creating a noticeable parallax effect?

- Is forward motion the only camera movement in this shot?

- Does the camera travel only forward in space, rather than zooming in?

- Is the camera moving exclusively forward in the scene?

- Does the camera advance in a straight forward direction without other motions?

- Is the only movement in this shot a forward motion?

- Does the scene feature a camera that only moves forward without lateral or vertical movement?

- Is the camera’s motion restricted to a single forward direction?

- Does the tracking movement solely involve pushing forward?

- Is the camera free from side-to-side or up-and-down movement while going forward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only forward (not zooming in) in the scene, or only north in a bird's eye view or south in a worm's eye view.

- A video where the camera only moves forward (not zooming in) in the scene or moves north in a bird's eye view or south in a worm's eye view.

- A video where the camera only moves forward (not zooming in) in the scene or moves north in a bird's eye view or south in a worm's eye view, creating a noticeable parallax effect.

- A tracking shot where the camera only moves forward (not zooming in) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera advances forward without shifting side-to-side.

- A video where the camera moves ahead with no other directional changes.

- A scene where the camera pushes forward while maintaining a strict forward trajectory.

- A video where the camera strictly maintains forward movement without deviation.

- A shot where the forward motion is the only movement present in the scene.

- A video where the camera only moves forward in the scene.

- A shot where the camera moves exclusively forward without any other motion.

- A video where the camera moves only forward (not zooming in), creating a noticeable parallax effect.

- A scene where forward motion is the only camera movement present.

- A shot where the camera travels only forward in space, rather than zooming in.

- A video where the camera advances in a straight forward direction without lateral or vertical movement.

- A scene where the camera moves forward without any additional motion.

- A tracking shot where the camera’s movement is restricted to a single forward direction.

- A shot where the tracking movement solely involves pushing forward.

- A video where the camera is free from side-to-side or up-and-down movement while going forward.

- A scene where the only movement present is the forward motion of the camera.

- A video where the camera maintains strict forward motion with no deviation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.forward and self.cam_motion.check_if_no_motion(exclude=['forward'])</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.forward and self.cam_motion.check_if_no_motion(exclude=['forward'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'backward'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward != 'forward' and self.cam_motion.camera_zoom == 'in'</code>

- <b>compound_motion_with_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward == 'forward' and not self.cam_motion.check_if_no_motion(exclude=['forward_backward'])</code>

</details>

</details>
