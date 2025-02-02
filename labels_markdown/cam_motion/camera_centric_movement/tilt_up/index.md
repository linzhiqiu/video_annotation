# Tilt_up Overview

<details>
<summary><h2>Has Tilt Up Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_tilt_up</code>


<h3>📖 Definition:</h3>
Does the camera tilt up in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera tilt upward in the scene?

- Does the camera tilt upward?

- Does the camera execute a tilt movement upward?

- Is the camera tilting up in the scene?

- Is the camera tilting upward?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera tilt from bottom to top?

- Is the camera tilting from bottom to top?

- Does the camera tilt up (not pedestal up)?

- Does the shot feature a camera tilt upward (not a pedestal movement)?

- Is the camera tilting upward (not pedestaling up)?

- Is this an upward tilting shot?

- Is this an up tilting motion (not moving up)?

- Is the camera rotating upward on its horizontal axis?

- Does the view shift from bottom to top?

- Is the camera angling upward?

- Does the camera sweep upward?

- Is the camera pivoting up?

- Does the camera rotate vertically upward?

- Is this a vertical rotation of the camera upward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera tilts up.

- A shot where the camera tilts upward.

- The camera tilts upward.

- The camera tilts up in the scene.

- A video where the camera angles upward.

- A video featuring an upward tilting movement.

- A scene featuring an upward tilting camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera tilts from bottom to top.

- The camera tilts from bottom to top.

- A scene where the camera tilts up (not pedestals up).

- A shot with an upward tilting motion (not a pedestal movement).

- A scene where the camera rotates upward.

- A shot where the view shifts from bottom to top.

- A scene where the camera sweeps upward.

- A shot with upward camera rotation.

- A video where the camera pivots up.

- A scene where the camera rotates vertically upward.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tilt_up is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.tilt_up is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.tilt_down is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True and self.cam_motion.tilt_up is False</code>

</details>

</details>

<details>
<summary><h2>Only Tilt Up Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_tilt_up</code>


<h3>📖 Definition:</h3>
Does the camera only tilt up in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only tilt upward in the scene, without any other camera movements?

- Does the camera only tilt upward?

- Is this an upward tilting shot?

- Is the camera only tilting upward?

- Is the camera movement purely an upward tilt?

- Is this exclusively an upward tilting shot?

- Does the camera only execute a tilt movement upward?

- Is this purely an upward tilting motion (no pedestal or other movements)?

- Does the shot feature only a camera tilt upward (rotating, not moving up)?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera only tilt from bottom to top?

- Is the camera only rotating upward on its horizontal axis (no pedestal or other movements)?

- Is the camera only tilting from bottom to top?

- Is the camera only rotating upward?

- Does the camera just angle upward?

- Is the movement limited to an upward rotation?

- Is this just an upward sweep of the camera?

- Is the camera only pivoting up?

- Is this strictly a vertical movement from bottom to top?

- Does the camera only move vertically from bottom to top?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera only tilts up.

- A shot where the camera only tilts upward.

- A shot where the camera only tilts from bottom to top.

- The camera only tilts upward.

- The camera only tilts up in the scene.

- The camera only tilts from bottom to top.

- A scene where the camera tilts up only (not pedestals/moves up).

- A video with pure upward tilting motion (rotating only, no translation).

- A shot with an upward tilting motion (camera rotating, not moving up).

- A shot demonstrating exclusively upward tilting motion (no pedestal movement).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring exclusively upward tilting movement.

- A video where the camera only rotates upward on its horizontal axis.

- A scene with only an upward tilting motion (no pedestal or other movements).

- A shot containing only an upward tilt (camera rotating, not moving up).

- A scene with nothing but an upward tilting camera movement (no vertical movement).

- A scene where the camera only rotates upward.

- A shot with just an upward turning motion.

- A video showing only an upward sweeping movement.

- A scene limited to upward camera rotation.

- A shot where the camera just pivots up.

- A scene with just vertical camera rotation from bottom to top.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tilt_up is True and self.cam_motion.check_if_no_motion_cam(exclude=['tilt_up'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.tilt_up is False or not self.cam_motion.check_if_no_motion_cam(exclude=['tilt_up'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>tilting_down</b>: <code>self.cam_motion.tilt_down is True</code>

- <b>only_tilting_down</b>: <code>self.cam_motion.tilt_down is True and self.cam_motion.check_if_no_motion_cam(exclude=['tilt_down'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>moving_up</b>: <code>self.cam_motion.up is True and self.cam_motion.tilt_up is False</code>

- <b>compound_motion_with_tilt_up</b>: <code>self.cam_motion.tilt_up is True and not self.cam_motion.check_if_no_motion_cam(exclude=['tilt_up'])</code>

</details>

</details>
