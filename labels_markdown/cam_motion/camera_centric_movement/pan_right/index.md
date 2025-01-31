# Pan_right Overview

<details>
<summary><h2>Has Pan Right Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_pan_right</code>


<h3>📖 Definition:</h3>
Does the camera pan right in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera pan rightward in the scene?

- Does the camera pan from left to right?

- Does the camera pan rightward?

- Is the camera panning right in the scene?

- Is the camera panning rightward?

- Is the camera panning from left to right?

- Does the camera execute a pan movement to the right?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera pan right (not move/truck right)?

- Does the shot feature a camera pan to the right (rotating, not moving sideways)?

- Is the camera rotating right on its axis (not trucking right)?

- Is this a rightward panning shot?

- Is this a right panning motion (not lateral movement)?

- Is the camera rotating to the right?

- Does the view shift from left to right?

- Is the camera turning rightward?

- Does the camera sweep to the right?

- Is the camera swiveling right?

- Is the camera pivoting right?

- Does the camera move horizontally from left to right?

- Is this a horizontal camera movement from left to right?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera pans right.

- A shot where the camera pans rightward.

- A shot where the camera pans from left to right.

- The camera pans rightward.

- The camera pans right in the scene.

- The camera pans from left to right.

- A video featuring a rightward panning movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera pans right (not trucks/moves right).

- A shot with a right panning motion (camera rotating, not moving sideways).

- A video where the camera rotates right on its axis, not trucking right.

- A scene featuring a right panning camera movement (not lateral movement).

- A shot where the camera pans right without sideways translation.

- A video demonstrating a pure right panning motion (rotating, not trucking).

- A scene where the camera rotates to the right.

- A shot where the view shifts from left to right.

- A video where the camera turns rightward.

- A scene where the camera sweeps to the right.

- A shot with rightward camera rotation.

- A video where the camera swivels right.

- A scene where the camera pivots right.

- A shot with horizontal camera movement from left to right.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan == 'right'</code>

<h4>🔴 Negative:</h4>
<code>((self.cam_motion.camera_movement in ['major_simple','no'] and self.cam_motion.camera_pan != 'right') or (self.cam_motion.camera_movement in ['major_complex'] and self.cam_motion.camera_pan == 'left')) and self.cam_motion.steadiness not in ['unsteady','very_unsteady'] and not self.cam_motion.check_if_any_motion(include=['arc', 'crane'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>panning_left</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan == 'left' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_right</b>: <code>self.cam_motion.camera_movement in ['major_simple','major_complex'] and self.cam_motion.camera_pan != 'right' and self.cam_motion.camera_left_right == 'right' and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

</details>

<details>
<summary><h2>Only Pan Right Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_pan_right</code>


<h3>📖 Definition:</h3>
Does the camera only pan from left to right?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only pan right in the scene, without any other camera movements?

- Does the camera only pan rightward, without any other camera movements?

- Does the camera only pan rightward?

- Is this a rightward panning shot?

- Is this a panning shot from left to right?

- Is the camera only panning rightward?

- Is the camera movement purely a rightward pan?

- Is this exclusively a right panning shot?

- Does the camera only execute a pan movement to the right?

- Is this purely a right panning motion (no trucking or other movements)?

- Does the shot feature only a camera pan to the right (rotating, not moving sideways)?

- Is the camera only rotating right on its axis (no trucking or other movements)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only rotating to the right?

- Does the camera just turn rightward?

- Is the movement limited to a right rotation?

- Is this just a rightward sweep of the camera?

- Is the camera only swiveling right?

- Is the camera just pivoting right?

- Is this strictly a horizontal movement from left to right?

- Does the camera only move horizontally from left to right?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera only pans right.

- A shot where the camera only pans rightward.

- A shot where the camera only pans from left to right.

- The camera only pans rightward.

- The camera only pans right in the scene.

- The camera only pans from left to right.

- A scene where the camera pans right only (not trucks/moves right).

- A video with pure right panning motion (rotating only, no translation).

- A shot with a right panning motion (camera rotating, not moving sideways).

- A video where the camera only rotates right on its axis.

- A shot demonstrating exclusively right panning motion (no trucking).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring exclusively rightward panning movement.

- A video featuring a rightward panning movement.

- A scene with only a right panning motion (no trucking or other movements).

- A shot containing only a rightward pan (camera rotating, not moving sideways).

- A scene with nothing but a right panning camera movement (no lateral movement).

- A scene where the camera only rotates to the right.

- A shot with just a rightward turning motion.

- A video showing only a right sweeping movement.

- A scene limited to rightward camera rotation.

- A shot where the camera just swivels right.

- A video where the camera only pivots right.

- A scene with just horizontal camera movement from left to right.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'right' and self.cam_motion.check_if_no_motion(exclude=['pan'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_pan != 'right' or not self.cam_motion.check_if_no_motion_cam_frame(exclude=['pan']) or self.cam_motion.camera_movement not in ['major_simple']</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>only_panning_left</b>: <code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'left' and self.cam_motion.check_if_no_motion(exclude=['pan']) and self.cam_motion.steadiness not in ['unsteady','very_unsteady']</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>pan_right_with_other</b>: <code>self.cam_motion.camera_movement == 'major_simple' and self.cam_motion.camera_pan == 'right' and not self.cam_motion.check_if_no_motion(exclude=['pan'])</code>

</details>

</details>
