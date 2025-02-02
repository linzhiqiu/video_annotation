# Down Overview

<details>
<summary><h2>Has Downward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_down_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera move downward (not tilting down) in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving downward in the scene?

- Is the camera moving downward?

- Is the camera moving downward, creating a noticeable vertical parallax effect?

- Is the camera moving downward (not tilting down) in the scene, creating a noticeable vertical parallax effect?

- Does the camera move in the downward direction relative to the ground?

- Is the camera lowering through the space?

- Is the camera performing a pedestal down?

- Is the camera descending downward?

- Is the camera moving vertically downward?

- Does the shot feature a clear downward motion of the camera?

- Is the camera's movement progressing downward rather than upward?

- Is the downward motion of the camera clear in this shot?

- Does the camera travel downward in space, rather than tilting down?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera descending in the scene?

- Does the perspective shift downward rather than relying on tilt?

- Is the camera physically traveling downward instead of rotating?

- Is the camera lowering, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera lowers downward, rather than tilting down.

- A video where the camera travels downward, creating noticeable vertical parallax.

- A scene where the camera moves physically downward instead of tilting.

- A tracking shot where the camera moves downward relative to the ground plane.

- A shot where the camera moves straight down, maintaining a sense of vertical motion.

- A video where the camera moves downward (not tilting down) in the scene.

- A shot where the camera is moving downward within the scene.

- A video where the camera moves downward, creating a noticeable vertical parallax effect.

- A shot where the camera moves in the downward direction relative to the ground.

- A video where the camera lowers through space.

- A scene where the camera performs a pedestal down.

- A video where the camera descends vertically.

- A shot where the camera moves vertically downward.

- The camera descends downward, moving vertically in the scene.

- A video where the camera progresses downward rather than upward.

- A shot where the downward motion of the camera is clearly visible.

- A video where the camera travels downward in space rather than tilting down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the shot features a clear downward motion of the camera.

- A shot where the camera pedestal moves straight down.

- A video where the camera moves in a downward direction within the scene.

- A shot where the camera lowers rather than tilting down.

- A video where the camera progresses downward, creating depth.

- A scene where the camera moves down rather than up.

- A shot where the perspective shifts downward dynamically.

- A video where the camera maintains a continuous downward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.down is True and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.down is False and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.down is False and self.cam_motion.tilt_down is True and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

</details>

<details>
<summary><h2>Has Downward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_down_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move downward (not tilting down) in the scene, or move west if it's a bird's eye view, or move east if it's a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move downward (not tilting down) in the scene, or move left if it's a bird's eye view, or move right if it's a worm's eye view?

- Is the camera moving downward in the scene (west in a bird's eye view or east in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving downward in the scene?

- Is the camera moving downward?

- Is the camera moving downward (not tilting down) in the scene, creating a noticeable vertical parallax effect?

- Is the downward motion of the camera clear in this shot?

- Does the camera travel downward in space, rather than tilting down?

- Is the camera descending in the scene?

- Does the camera move in the downward direction relative to the ground?

- Is the camera's movement progressing downward rather than upward?

- Is the camera lowering through the space?

- Does the shot feature a clear downward motion of the camera?

- Does the perspective shift downward rather than relying on tilt?

- Is the camera physically traveling downward instead of rotating?

- Is the camera lowering, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves downward (not tilting down) in the scene or moves west in a bird's eye view or east in a worm's eye view.

- A video where the camera moves downward (not tilting down) in the scene or moves west in a bird's eye view or east in a worm's eye view, creating a noticeable vertical parallax effect.

- A shot where the camera moves downward (not tilting down) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves downward, not tilting down.

- A shot where the camera lowers downward, rather than tilting down.

- A video where the camera travels downward, creating noticeable vertical parallax.

- A scene where the camera moves physically downward instead of tilting.

- A video where the camera moves in a downward direction within the scene.

- A shot where the camera lowers rather than tilting down.

- A video where the camera progresses downward, creating depth.

- A scene where the camera moves down rather than up.

- A shot where the perspective shifts downward dynamically.

- A video where the camera maintains a continuous downward movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.down is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.down is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.down is False and self.cam_motion.tilt_down is True</code>

</details>

</details>

<details>
<summary><h2>Only Downward Movement (Relative to Ground, Bird's/Worm's Eye Views Not Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_down_wrt_ground</code>


<h3>📖 Definition:</h3>
Does the camera only move downward (not tilting down) with respect to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera only moving downward with respect to the ground?

- Is the camera only moving downward without tilting down relative to the ground?

- Is the camera only lowering with respect to the ground?

- Is the camera only performing a pedestal down (not tilting down) relative to the ground?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving downward in the scene?

- Is the camera only moving downward (not tilting down) in the scene, creating a noticeable vertical parallax effect?

- Relative to ground, is downward motion the only camera movement in this shot?

- Does the camera travel only downward in space, rather than tilting down?

- Is the camera exclusively moving downward in the scene?

- Does the camera move straight down without any other motion?

- Is the camera's motion restricted to only downward movement?

- Does the tracking movement involve only a downward drop?

- Is the camera moving down without any horizontal or rotational adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves downward (not tilting down) relative to the ground.

- A shot where the camera moves straight down with respect to the ground without any other motion.

- A video where the camera exclusively moves downward relative to the ground plane, creating a noticeable vertical parallax effect.

- A scene where the camera moves only downward relative to the ground, avoiding tilting or other motions.

- The camera is only performing a pedestal down with respect to the ground.

- The camera is only lowering with respect to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves downward without incorporating other movement types.

- A shot where the downward motion is the only movement present in the scene.

- A shot where the camera moves strictly downward without horizontal or rotational movement.

- A video where the camera lowers in a single direction without any other adjustments.

- A scene where the camera moves down without shifting horizontally.

- A video where the camera strictly maintains downward movement with no deviation.

- A shot where the tracking movement is purely downward with no other motion.

- A scene where the only movement present is the camera lowering vertically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.down is True and self.cam_motion.check_if_no_motion(exclude=['down']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<h4>🔴 Negative:</h4>
<code>(self.cam_motion.down is False or not self.cam_motion.check_if_no_motion(exclude=['down']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

- <b>only_moving_up</b>: <code>self.cam_motion.up is True and self.cam_motion.check_if_no_motion(exclude=['up']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.down is False and self.cam_motion.tilt_down is True and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

- <b>compound_motion_with_down</b>: <code>self.cam_motion.down is True and not self.cam_motion.check_if_no_motion(exclude=['down']) and self.cam_setup.camera_angle_start not in ['bird_eye_angle', 'worm_eye_angle', 'unknown']</code>

</details>

</details>

<details>
<summary><h2>Only Downward Movement (Relative to Ground, Bird's/Worm's Eye Views Included)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_down_wrt_ground_birds_worms_included</code>


<h3>📖 Definition:</h3>
Does the camera move only downward (not tilting down) in the scene, or only westward in a bird's eye view, or only eastward in a worm's eye view?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move only downward (not tilting down) in the scene, or only leftward in a bird's eye view, or only rightward in a worm's eye view?

- Does the camera move only downward (not tilting down) in the scene, or only move west if it's a bird's eye view, or only move east if it's a worm's eye view?

- Is the camera only moving downward in the scene (west in a bird's eye view or east in a worm's eye view)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving downward in the scene?

- Is the camera only moving downward?

- Is the camera only moving downward (not tilting down) in the scene, creating a noticeable vertical parallax effect?

- Is downward motion the only camera movement in this shot?

- Does the camera travel only downward in space, rather than tilting down?

- Is the camera moving exclusively downward in the scene?

- Does the camera lower in a straight downward direction without other motions?

- Is the only movement in this shot a downward motion?

- Does the scene feature a camera that only moves downward without horizontal or rotational movement?

- Is the camera's motion restricted to a single downward direction?

- Does the tracking movement solely involve lowering downward?

- Is the camera free from horizontal or rotational movement while going downward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves only downward (not tilting down) in the scene, or only west in a bird's eye view or east in a worm's eye view.

- A video where the camera only moves downward (not tilting down) in the scene or moves west in a bird's eye view or east in a worm's eye view.

- A video where the camera only moves downward (not tilting down) in the scene or moves west in a bird's eye view or east in a worm's eye view, creating a noticeable vertical parallax effect.

- A shot where the camera only moves downward (not tilting down) relative to the ground plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera lowers downward without shifting horizontally.

- A video where the camera moves down with no other directional changes.

- A scene where the camera descends while maintaining a strict vertical trajectory.

- A video where the camera strictly maintains downward movement without deviation.

- A shot where the downward motion is the only movement present in the scene.

- A video where the camera only moves downward in the scene.

- A shot where the camera moves exclusively downward without any other motion.

- A video where the camera moves only downward (not tilting down), creating a noticeable vertical parallax effect.

- A scene where downward motion is the only camera movement present.

- A shot where the camera travels only downward in space, rather than tilting down.

- A video where the camera lowers in a straight downward direction without horizontal or rotational movement.

- A scene where the camera moves downward without any additional motion.

- A tracking shot where the camera's movement is restricted to a single downward direction.

- A shot where the tracking movement solely involves lowering downward.

- A video where the camera is free from horizontal or rotational movement while going downward.

- A scene where the only movement present is the downward motion of the camera.

- A video where the camera maintains strict downward motion with no deviation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.down is True and self.cam_motion.check_if_no_motion(exclude=['down'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.down is False or not self.cam_motion.check_if_no_motion(exclude=['down'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True</code>

- <b>only_moving_up</b>: <code>self.cam_motion.up is True and self.cam_motion.check_if_no_motion(exclude=['up'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.down is False and self.cam_motion.tilt_down is True</code>

- <b>compound_motion_with_down</b>: <code>self.cam_motion.down is True and not self.cam_motion.check_if_no_motion(exclude=['down'])</code>

</details>

</details>
