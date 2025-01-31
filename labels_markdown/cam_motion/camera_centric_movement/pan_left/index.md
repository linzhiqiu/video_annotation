# Pan_left Overview

<details>
<summary><h2>Has Pan Left Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_pan_left</code>


<h3>📖 Definition:</h3>
Does the camera pan left in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera pan leftward in the scene?

- Does the camera pan from right to left?

- Does the camera pan leftward?

- Is the camera panning left in the scene?

- Is the camera panning leftward?

- Is the camera panning from right to left?

- Does the camera execute a pan movement to the left?

- Does the camera pan left (not move/truck left)?

- Does the shot feature a camera pan to the left (rotating, not moving sideways)?

- Is the camera rotating left on its axis (not trucking left)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is this a leftward panning shot?

- Is this a left panning motion (not lateral movement)?

- Is the camera rotating to the left?

- Does the view shift from right to left?

- Is the camera turning leftward?

- Does the camera sweep to the left?

- Is the camera swiveling left?

- Is the camera pivoting left?

- Does the camera move horizontally from right to left?

- Is this a horizontal camera movement from right to left?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera pans left.

- A shot where the camera pans leftward.

- A shot where the camera pans from right to left.

- The camera pans leftward.

- The camera pans left in the scene.

- The camera pans from right to left.

- A video featuring a leftward panning movement.

- A scene where the camera pans left (not trucks/moves left).

- A shot with a left panning motion (camera rotating, not moving sideways).

- A video where the camera rotates left on its axis, not trucking left.

- A scene featuring a left panning camera movement (not lateral movement).

- A shot where the camera pans left without sideways translation.

- A video demonstrating a pure left panning motion (rotating, not trucking).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera rotates to the left.

- A shot where the view shifts from right to left.

- A video where the camera turns leftward.

- A scene where the camera sweeps to the left.

- A shot with leftward camera rotation.

- A video where the camera swivels left.

- A scene where the camera pivots left.

- A shot with horizontal camera movement from right to left.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan == 'left'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and self.cam_motion.camera_pan != 'left') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_pan == 'right')) and not self.cam_motion.check_if_any_motion(include=['arc', 'crane'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>panning_right</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan == 'right' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_left</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan != 'left' and self.cam_motion.camera_left_right == 'left' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Pan Left Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_pan_left</code>


<h3>📖 Definition:</h3>
Does the camera only pan from right to left?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only pan left in the scene, without any other camera movements?

- Does the camera only pan leftward, without any other camera movements?

- Does the camera only pan leftward?

- Is this a leftward panning shot?

- Is this a panning shot from right to left?

- Is the camera only panning leftward?

- Is the camera movement purely a leftward pan?

- Is this exclusively a left panning shot?

- Does the camera only execute a pan movement to the left?

- Is this purely a left panning motion (no trucking or other movements)?

- Does the shot feature only a camera pan to the left (rotating, not moving sideways)?

- Is the camera only rotating left on its axis (no trucking or other movements)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only rotating to the left?

- Does the camera just turn leftward?

- Is the movement limited to a left rotation?

- Is this just a leftward sweep of the camera?

- Is the camera only swiveling left?

- Is the camera just pivoting left?

- Is this strictly a horizontal movement from right to left?

- Does the camera only move horizontally from right to left?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera only pans left.

- A shot where the camera only pans leftward.

- A shot where the camera only pans from right to left.

- The camera only pans leftward.

- The camera only pans left in the scene.

- The camera only pans from right to left.

- A scene where the camera pans left only (not trucks/moves left).

- A video with pure left panning motion (rotating only, no translation).

- A shot with a left panning motion (camera rotating, not moving sideways).

- A video where the camera only rotates left on its axis.

- A shot demonstrating exclusively left panning motion (no trucking).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring exclusively leftward panning movement.

- A video featuring a leftward panning movement.

- A scene with only a left panning motion (no trucking or other movements).

- A shot containing only a leftward pan (camera rotating, not moving sideways).

- A scene with nothing but a left panning camera movement (no lateral movement).

- A scene where the camera only rotates to the left.

- A shot with just a leftward turning motion.

- A video showing only a left sweeping movement.

- A scene limited to leftward camera rotation.

- A shot where the camera just swivels left.

- A video where the camera only pivots left.

- A scene with just horizontal camera movement from right to left.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'left' and self.cam_motion.check_if_no_motion(exclude=['pan'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_pan != 'left' or not self.cam_motion.check_if_no_motion_cam_frame(exclude=['pan']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>only_panning_right</b>: <code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'right' and not self.cam_motion.check_if_any_motion(exclude=['pan']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>pan_right_with_other</b>: <code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'left' and not self.cam_motion.check_if_no_motion(exclude=['pan'])</code>

</details>

</details>
