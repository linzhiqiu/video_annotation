# Tilt_down Overview

<details>
<summary><h2>Has Tilt Down Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_tilt_down</code>


<h3>📖 Definition:</h3>
Does the camera tilt down in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera tilt downward in the scene?

- Does the camera tilt downward?

- Does the camera execute a tilt movement downward?

- Is the camera tilting down in the scene?

- Is the camera tilting downward?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera tilt from top to bottom?

- Is the camera tilting from top to bottom?

- Does the camera tilt down (not pedestal down)?

- Does the shot feature a camera tilt downward (not a pedestal movement)?

- Is the camera tilting downward (not pedestaling down)?

- Is this a downward tilting shot?

- Is this a down tilting motion (not moving down)?

- Is the camera rotating downward on its horizontal axis?

- Does the view shift from top to bottom?

- Is the camera angling downward?

- Does the camera sweep downward?

- Is the camera pivoting down?

- Does the camera rotate vertically downward?

- Is this a vertical rotation of the camera downward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera tilts down.

- A shot where the camera tilts downward.

- The camera tilts downward.

- The camera tilts down in the scene.

- A video where the camera angles downward.

- A video featuring a downward tilting movement.

- A scene featuring a downward tilting camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera tilts from top to bottom.

- The camera tilts from top to bottom.

- A scene where the camera tilts down (not pedestals down).

- A shot with a downward tilting motion (not a pedestal movement).

- A scene where the camera rotates downward.

- A shot where the view shifts from top to bottom.

- A scene where the camera sweeps downward.

- A shot with downward camera rotation.

- A video where the camera pivots down.

- A scene where the camera rotates vertically downward.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tilt_down is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.tilt_down is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.tilt_up is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.down is True and self.cam_motion.tilt_down is False</code>

</details>

</details>

<details>
<summary><h2>Only Tilt Down Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_tilt_down</code>


<h3>📖 Definition:</h3>
Does the camera only tilt down in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only tilt downward in the scene, without any other camera movements?

- Does the camera only tilt downward?

- Is this a downward tilting shot?

- Is the camera only tilting downward?

- Is the camera movement purely a downward tilt?

- Is this exclusively a downward tilting shot?

- Does the camera only execute a tilt movement downward?

- Is this purely a downward tilting motion (no pedestal or other movements)?

- Does the shot feature only a camera tilt downward (rotating, not moving down)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera only tilt from top to bottom?

- Is the camera only rotating downward on its horizontal axis (no pedestal or other movements)?

- Is the camera only tilting from top to bottom?

- Is the camera only rotating downward?

- Does the camera just angle downward?

- Is the movement limited to a downward rotation?

- Is this just a downward sweep of the camera?

- Is the camera only pivoting down?

- Is this strictly a vertical movement from top to bottom?

- Does the camera only move vertically from top to bottom?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera only tilts down.

- A shot where the camera only tilts downward.

- A shot where the camera only tilts from top to bottom.

- The camera only tilts downward.

- The camera only tilts down in the scene.

- The camera only tilts from top to bottom.

- A scene where the camera tilts down only (not pedestals/moves down).

- A video with pure downward tilting motion (rotating only, no translation).

- A shot with a downward tilting motion (camera rotating, not moving down).

- A shot demonstrating exclusively downward tilting motion (no pedestal movement).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring exclusively downward tilting movement.

- A video where the camera only rotates downward on its horizontal axis.

- A scene with only a downward tilting motion (no pedestal or other movements).

- A shot containing only a downward tilt (camera rotating, not moving down).

- A scene with nothing but a downward tilting camera movement (no vertical movement).

- A scene where the camera only rotates downward.

- A shot with just a downward turning motion.

- A video showing only a downward sweeping movement.

- A scene limited to downward camera rotation.

- A shot where the camera just pivots down.

- A scene with just vertical camera rotation from top to bottom.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tilt_down is True and self.cam_motion.check_if_no_motion_cam(exclude=['tilt_down'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.tilt_down is False or not self.cam_motion.check_if_no_motion_cam(exclude=['tilt_down'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.tilt_up is True</code>

- <b>only_tilting_up</b>: <code>self.cam_motion.tilt_up is True and self.cam_motion.check_if_no_motion_cam(exclude=['tilt_up'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.down is True and self.cam_motion.tilt_down is False</code>

- <b>compound_motion_with_tilt_down</b>: <code>self.cam_motion.tilt_down is True and not self.cam_motion.check_if_no_motion_cam(exclude=['tilt_down'])</code>

</details>

</details>
