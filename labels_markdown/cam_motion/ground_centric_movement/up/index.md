# Up Overview

<details>
<summary><h2>Has Upward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_up_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera move upward (not tilting up) in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving upward in the scene?

- Is the camera moving upward?

- Is the camera moving upward, creating a noticeable vertical parallax effect?

- Is the camera moving upward (not tilting up) in the scene, creating a noticeable vertical parallax effect?

- Does the camera move in the upward direction relative to the ground?

- Is the camera rising through the space?

- Is the camera performing a pedestal up?

- Is the camera elevating upward?

- Is the camera moving vertically upward?

- Does the shot feature a clear upward motion of the camera?

- Is the camera's movement progressing upward rather than downward?

- Is the upward motion of the camera clear in this shot?

- Does the camera travel upward in space, rather than tilting up?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera ascending in the scene?

- Does the perspective shift upward rather than relying on tilt?

- Is the camera physically traveling upward instead of rotating?

- Is the camera rising, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera rises upward, rather than tilting up.

- A video where the camera travels upward, creating noticeable vertical parallax.

- A scene where the camera moves physically upward instead of tilting.

- A tracking shot where the camera moves upward relative to the ground plane.

- A shot where the camera moves straight up, maintaining a sense of vertical motion.

- A video where the camera moves upward (not tilting up) in the scene.

- A shot where the camera is moving upward within the scene.

- A video where the camera moves upward, creating a noticeable vertical parallax effect.

- A shot where the camera moves in the upward direction relative to the ground.

- A video where the camera rises through space.

- A scene where the camera performs a pedestal up.

- A video where the camera elevates vertically.

- A shot where the camera moves vertically upward.

- The camera elevates upward, moving vertically in the scene.

- A video where the camera progresses upward rather than downward.

- A shot where the upward motion of the camera is clearly visible.

- A video where the camera travels upward in space rather than tilting up.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the shot features a clear upward motion of the camera.

- A shot where the camera pedestal moves straight up.

- A video where the camera moves in an upward direction within the scene.

- A shot where the camera rises rather than tilting up.

- A video where the camera progresses upward, creating depth.

- A scene where the camera moves up rather than down.

- A shot where the perspective shifts upward dynamically.

- A video where the camera maintains a continuous upward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'up' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.camera_up_down != 'up') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_up_down == 'down')) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and not self.cam_motion.check_if_any_motion(include=['arc', 'crane'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'down' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down != 'up' and self.cam_motion.camera_tilt == 'up' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Has Upward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_up_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move upward (not tilting up) in the scene, or move east if it's a bird's eye view, or move west if it's a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move upward (not tilting up) in the scene, or move right if it's a bird's eye view, or move left if it's a worm's eye view?

- Is the camera moving upward in the scene (east in a bird's eye view or west in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving upward in the scene?

- Is the camera moving upward?

- Is the camera moving upward (not tilting up) in the scene, creating a noticeable vertical parallax effect?

- Is the upward motion of the camera clear in this shot?

- Does the camera travel upward in space, rather than tilting up?

- Is the camera ascending in the scene?

- Does the camera move in the upward direction relative to the ground?

- Is the camera's movement progressing upward rather than downward?

- Is the camera rising through the space?

- Does the shot feature a clear upward motion of the camera?

- Does the perspective shift upward rather than relying on tilt?

- Is the camera physically traveling upward instead of rotating?

- Is the camera rising, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves upward (not tilting up) in the scene or moves east in a bird's eye view or west in a worm's eye view.

- A video where the camera moves upward (not tilting up) in the scene or moves east in a bird's eye view or west in a worm's eye view, creating a noticeable vertical parallax effect.

- A tracking shot where the camera moves upward (not tilting up) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves upward, not tilting up.

- A shot where the camera rises upward, rather than tilting up.

- A video where the camera travels upward, creating noticeable vertical parallax.

- A scene where the camera moves physically upward instead of tilting.

- A video where the camera moves in an upward direction within the scene.

- A shot where the camera rises rather than tilting up.

- A video where the camera progresses upward, creating depth.

- A scene where the camera moves up rather than down.

- A shot where the perspective shifts upward dynamically.

- A video where the camera maintains a continuous upward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'up'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and self.cam_motion.camera_up_down != 'up') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_up_down == 'down')) and not self.cam_motion.check_if_any_motion(include=['arc', 'crane'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'down' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down != 'up' and self.cam_motion.camera_tilt == 'up' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Upward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_up_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera only move upward (not tilting up) with respect to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera only moving upward with respect to the ground?

- Is the camera only moving upward without tilting up relative to the ground?

- Is the camera only rising with respect to the ground?

- Is the camera only performing a pedestal up (not tilting up) relative to the ground?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving upward in the scene?

- Is the camera only moving upward (not tilting up) in the scene, creating a noticeable vertical parallax effect?

- Relative to ground, is upward motion the only camera movement in this shot?

- Does the camera travel only upward in space, rather than tilting up?

- Is the camera exclusively moving upward in the scene?

- Does the camera move straight up without any other motion?

- Is the camera's motion restricted to only upward movement?

- Does the tracking movement involve only an upward rise?

- Is the camera moving up without any horizontal or rotational adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves upward (not tilting up) relative to the ground.

- A shot where the camera moves straight up with respect to the ground without any other motion.

- A video where the camera exclusively moves upward relative to the ground plane, creating a noticeable vertical parallax effect.

- A scene where the camera moves only upward relative to the ground, avoiding tilting or other motions.

- The camera is only performing a pedestal up with respect to the ground.

- The camera is only rising with respect to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves upward without incorporating other movement types.

- A shot where the upward motion is the only movement present in the scene.

- A shot where the camera moves strictly upward without horizontal or rotational movement.

- A video where the camera rises in a single direction without any other adjustments.

- A scene where the camera moves up without shifting horizontally.

- A video where the camera strictly maintains upward movement with no deviation.

- A shot where the tracking movement is purely upward with no other motion.

- A scene where the only movement present is the camera rising vertically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down == 'up' and self.cam_motion.check_if_no_motion(exclude=['up_down']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_up_down != 'up' or not self.cam_motion.check_if_no_motion(exclude=['up_down']) or self.cam_motion.camera_movement not in ['major_simple'] and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'down' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down != 'up' and self.cam_motion.camera_tilt == 'up' and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

- <b>compound_motion_with_up</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down == 'up' and not self.cam_motion.check_if_no_motion(exclude=['up_down']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

</details>

<details>
<summary><h2>Only Upward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_up_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move only upward (not tilting up) in the scene, or only eastward in a bird's eye view, or only westward in a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move only upward (not tilting up) in the scene, or only rightward in a bird's eye view, or only leftward in a worm's eye view?

- Does the camera move only upward (not tilting up) in the scene, or only move east if it's a bird's eye view, or only move west if it's a worm's eye view?

- Is the camera only moving upward in the scene (east in a bird's eye view or west in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving upward in the scene?

- Is the camera only moving upward?

- Is the camera only moving upward (not tilting up) in the scene, creating a noticeable vertical parallax effect?

- Is upward motion the only camera movement in this shot?

- Does the camera travel only upward in space, rather than tilting up?

- Is the camera moving exclusively upward in the scene?

- Does the camera rise in a straight upward direction without other motions?

- Is the only movement in this shot an upward motion?

- Does the scene feature a camera that only moves upward without horizontal or rotational movement?

- Is the camera's motion restricted to a single upward direction?

- Does the tracking movement solely involve rising upward?

- Is the camera free from horizontal or rotational movement while going upward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only upward (not tilting up) in the scene, or only east in a bird's eye view or west in a worm's eye view.

- A video where the camera only moves upward (not tilting up) in the scene or moves east in a bird's eye view or west in a worm's eye view.

- A video where the camera only moves upward (not tilting up) in the scene or moves east in a bird's eye view or west in a worm's eye view, creating a noticeable vertical parallax effect.

- A tracking shot where the camera only moves upward (not tilting up) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera rises upward without shifting horizontally.

- A video where the camera moves up with no other directional changes.

- A scene where the camera elevates while maintaining a strict vertical trajectory.

- A video where the camera strictly maintains upward movement without deviation.

- A shot where the upward motion is the only movement present in the scene.

- A video where the camera only moves upward in the scene.

- A shot where the camera moves exclusively upward without any other motion.

- A video where the camera moves only upward (not tilting up), creating a noticeable vertical parallax effect.

- A scene where upward motion is the only camera movement present.

- A shot where the camera travels only upward in space, rather than tilting up.

- A video where the camera rises in a straight upward direction without horizontal or rotational movement.

- A scene where the camera moves upward without any additional motion.

- A tracking shot where the camera's movement is restricted to a single upward direction.

- A shot where the tracking movement solely involves rising upward.

- A video where the camera is free from horizontal or rotational movement while going upward.

- A scene where the only movement present is the upward motion of the camera.

- A video where the camera maintains strict upward motion with no deviation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down == 'up' and self.cam_motion.check_if_no_motion(exclude=['up_down']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_up_down != 'up' or not self.cam_motion.check_if_no_motion(exclude=['up_down']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down == 'down'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_up_down != 'up' and self.cam_motion.camera_tilt == 'up'</code>

- <b>compound_motion_with_up</b>: <code>self.cam_motion.camera_movement in ['major_simple'] and self.cam_motion.camera_up_down == 'up' and not self.cam_motion.check_if_no_motion(exclude=['up_down'])</code>

</details>

</details>
