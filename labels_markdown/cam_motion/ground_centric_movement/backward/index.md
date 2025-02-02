# Backward Overview

<details>
<summary><h2>Has Backward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_backward_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera move backward (not zooming out) in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving backward in the scene?

- Is the camera moving backward?

- Is the camera moving backward, creating a noticeable parallax effect?

- Is the camera moving backward (not zooming out) in the scene, creating a noticeable parallax effect?

- Does the camera move in the backward direction relative to the ground?

- Is the camera pulling back through the space?

- Is the camera pulling out?

- Is the camera dollying out?

- Is the camera dollying backward?

- Does the shot feature a clear backward motion of the camera?

- Is the camera's movement progressing backward rather than forward?

- Is the backward motion of the camera clear in this shot?

- Does the camera travel backward in space, rather than zooming out?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera retreating in the scene?

- Does the perspective shift backward rather than relying on zoom?

- Is the camera physically traveling backward instead of adjusting focal length?

- Is the camera retreating, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera moves backward, rather than zooming out.

- A video where the camera travels backward, creating noticeable parallax.

- A scene where the camera moves physically backward instead of zooming.

- A tracking shot where the camera moves backward relative to the ground plane.

- A shot where the camera moves straight back, maintaining a sense of backward motion.

- A video where the camera moves backward (not zooming out) in the scene.

- A shot where the camera is moving backward within the scene.

- A video where the camera moves backward, creating a noticeable parallax effect.

- A shot where the camera moves in the backward direction relative to the ground.

- A video where the camera pulls back through space.

- A scene where the camera pulls out.

- A video where the camera performs a dolly-out motion.

- A shot where the camera dollies backward.

- The camera dollies out, moving backward in the scene.

- A video where the camera progresses backward rather than forward.

- A shot where the backward motion of the camera is clearly visible.

- A video where the camera travels backward in space rather than zooming out.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the shot features a clear backward motion of the camera.

- A shot where the camera dolly moves straight back.

- A video where the camera moves in a backward direction within the scene.

- A shot where the camera retreats rather than zooming out.

- A video where the camera progresses backward, creating depth.

- A scene where the camera moves back rather than pushing forward.

- A shot where the perspective shifts backward dynamically.

- A video where the camera maintains a continuous backward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.backward and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.backward and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'forward' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward != 'backward' and self.cam_motion.camera_zoom == 'out' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Has Backward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_backward_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move backward (not zooming out) in the scene, or move south if it's a bird's eye view, or move north if it's a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move backward (not zooming out) in the scene, or move downward if it's a bird's eye view, or move upward if it's a worm's eye view?

- Is the camera moving backward in the scene (south in a bird's eye view or north in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving backward in the scene?

- Is the camera moving backward?

- Is the camera moving backward (not zooming out) in the scene, creating a noticeable parallax effect?

- Is the backward motion of the camera clear in this shot?

- Does the camera travel backward in space, rather than zooming out?

- Is the camera retreating in the scene?

- Does the camera move in the backward direction relative to the ground?

- Is the camera's movement progressing backward rather than forward?

- Is the camera pulling back through the space?

- Does the shot feature a clear backward motion of the camera?

- Does the perspective shift backward rather than relying on zoom?

- Is the camera physically traveling backward instead of adjusting focal length?

- Is the camera retreating, creating a strong sense of depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves backward (not zooming out) in the scene or moves south in a bird's eye view or north in a worm's eye view.

- A video where the camera moves backward (not zooming out) in the scene or moves south in a bird's eye view or north in a worm's eye view, creating a noticeable parallax effect.

- A tracking shot where the camera moves backward (not zooming out) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward, not zooming out.

- A shot where the camera moves backward, rather than zooming out.

- A video where the camera travels backward, creating noticeable parallax.

- A scene where the camera moves physically backward instead of zooming.

- A video where the camera moves in a backward direction within the scene.

- A shot where the camera retreats rather than zooming out.

- A video where the camera progresses backward, creating depth.

- A scene where the camera moves back rather than pushing forward.

- A shot where the perspective shifts backward dynamically.

- A video where the camera maintains a continuous backward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.backward</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.backward</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'forward' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward != 'backward' and self.cam_motion.camera_zoom == 'out' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Backward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_backward_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera only move backward (not zooming out) with respect to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera only moving backward with respect to the ground?

- Is the camera only moving backward without zooming out relative to the ground?

- Is the camera only pulling back with respect to the ground?

- Is the camera only dollying backward (not zooming out) relative to the ground?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving backward in the scene?

- Is the camera only moving backward (not zooming out) in the scene, creating a noticeable parallax effect?

- Relative to ground, is backward motion the only camera movement in this shot?

- Does the camera travel only backward in space, rather than zooming out?

- Is the camera exclusively moving backward in the scene?

- Does the camera move straight back without any other motion?

- Is the camera's motion restricted to only backward movement?

- Does the tracking movement involve only a backward pull?

- Is the camera moving back without any vertical or lateral adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves backward (not zooming out) relative to the ground.

- A shot where the camera moves straight back with respect to the ground without any other motion.

- A video where the camera exclusively moves backward relative to the ground plane, creating a noticeable parallax effect.

- A scene where the camera moves only backward relative to the ground, avoiding zooming or other motions.

- The camera is only dollying backward with respect to the ground.

- The camera is only pulling back with respect to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves backward without incorporating other movement types.

- A shot where the backward motion is the only movement present in the scene.

- A shot where the camera moves strictly backward without lateral or vertical movement.

- A video where the camera retreats in a single direction without any other adjustments.

- A scene where the camera moves back without shifting side to side.

- A video where the camera strictly maintains backward movement with no deviation.

- A shot where the tracking movement is purely backward with no other motion.

- A scene where the only movement present is the camera pulling back.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.backward and self.cam_motion.check_if_no_motion(exclude=['backward']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.backward and self.cam_motion.check_if_no_motion(exclude=['backward']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'forward' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward != 'backward' and self.cam_motion.camera_zoom == 'out' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

- <b>compound_motion_with_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward == 'backward' and not self.cam_motion.check_if_no_motion(exclude=['forward_backward']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

</details>

<details>
<summary><h2>Only Backward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_backward_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move only backward (not zooming out) in the scene, or only southward in a bird's eye view, or only northward in a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move only backward (not zooming out) in the scene, or only downward in a bird's eye view, or only upward in a worm's eye view?

- Does the camera move only backward (not zooming out) in the scene, or only move south if it's a bird's eye view, or only move north if it's a worm's eye view?

- Is the camera only moving backward in the scene (south in a bird's eye view or north in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving backward in the scene?

- Is the camera only moving backward?

- Is the camera only moving backward (not zooming out) in the scene, creating a noticeable parallax effect?

- Is backward motion the only camera movement in this shot?

- Does the camera travel only backward in space, rather than zooming out?

- Is the camera moving exclusively backward in the scene?

- Does the camera retreat in a straight backward direction without other motions?

- Is the only movement in this shot a backward motion?

- Does the scene feature a camera that only moves backward without lateral or vertical movement?

- Is the camera's motion restricted to a single backward direction?

- Does the tracking movement solely involve pulling back?

- Is the camera free from side-to-side or up-and-down movement while going backward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only backward (not zooming out) in the scene, or only south in a bird's eye view or north in a worm's eye view.

- A video where the camera only moves backward (not zooming out) in the scene or moves south in a bird's eye view or north in a worm's eye view.

- A video where the camera only moves backward (not zooming out) in the scene or moves south in a bird's eye view or north in a worm's eye view, creating a noticeable parallax effect.

- A tracking shot where the camera only moves backward (not zooming out) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward without shifting side-to-side.

- A video where the camera moves back with no other directional changes.

- A scene where the camera pulls back while maintaining a strict backward trajectory.

- A video where the camera strictly maintains backward movement without deviation.

- A shot where the backward motion is the only movement present in the scene.

- A video where the camera only moves backward in the scene.

- A shot where the camera moves exclusively backward without any other motion.

- A video where the camera moves only backward (not zooming out), creating a noticeable parallax effect.

- A scene where backward motion is the only camera movement present.

- A shot where the camera travels only backward in space, rather than zooming out.

- A video where the camera retreats in a straight backward direction without lateral or vertical movement.

- A scene where the camera moves backward without any additional motion.

- A tracking shot where the camera's movement is restricted to a single backward direction.

- A shot where the tracking movement solely involves pulling back.

- A video where the camera is free from side-to-side or up-and-down movement while going backward.

- A scene where the only movement present is the backward motion of the camera.

- A video where the camera maintains strict backward motion with no deviation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.backward and self.cam_motion.check_if_no_motion(exclude=['backward'])</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.backward and self.cam_motion.check_if_no_motion(exclude=['backward'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_forward</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward == 'forward'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_forward_backward != 'backward' and self.cam_motion.camera_zoom == 'out'</code>

- <b>compound_motion_with_backward</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_forward_backward == 'backward' and not self.cam_motion.check_if_no_motion(exclude=['forward_backward'])</code>

</details>

</details>
