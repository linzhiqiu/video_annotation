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
