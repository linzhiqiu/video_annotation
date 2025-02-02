# Leftward Overview

<details>
<summary><h2>Has Leftward Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_leftward</code>


<h3>📖 Definition:</h3>
Does the camera move left in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move leftward in the scene?

- Does the camera move from right to left?

- Does the camera truck left in the scene?

- Does the camera truck leftward?

- Does the camera truck from right to left?

- Is the camera moving leftward?

- Is the camera trucking left?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move left (not pan left)?

- Does the shot feature a leftward camera movement (moving, not rotating)?

- Is the camera traveling left in the scene?

- Is this a leftward tracking shot?

- Is this a left trucking motion (not panning)?

- Is the camera translating to the left?

- Does the camera physically move from right to left?

- Is the camera tracking leftward?

- Is this a lateral movement to the left?

- Does the camera dolly left?

- Is this a leftward dolly shot?

- Is the camera sliding left?

- Does the camera track from right to left?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera moves left.

- A shot where the camera moves leftward.

- A shot where the camera moves from right to left.

- A shot where the camera trucks left.

- A shot where the camera trucks leftward.

- A shot where the camera trucks from right to left.

- The camera moves leftward.

- The camera moves left.

- The camera moves from right to left.

- The camera trucks left.

- The camera trucks leftward.

- The camera trucks from right to left.

- The camera trucks left in the scene.

- A video featuring leftward camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera moves left (not panning left).

- A shot with leftward camera motion (moving sideways, not rotating).

- A video where the camera travels left.

- A scene featuring leftward tracking movement.

- A shot where the camera trucks left without rotation.

- A video demonstrating leftward camera translation.

- A scene where the camera physically moves from right to left.

- A shot with lateral leftward movement.

- A video where the camera dollies left.

- A scene with leftward tracking motion.

- A shot where the camera slides left.

- A video featuring a left trucking movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.left is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.left is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_right</b>: <code>self.cam_motion.right is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_left</b>: <code>self.cam_motion.pan_left is True and self.cam_motion.left is False</code>

</details>

</details>

<details>
<summary><h2>Only Leftward Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_leftward</code>


<h3>📖 Definition:</h3>
Does the camera only move left in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only move leftward, without any other camera movements?

- Does the camera only move from right to left?

- Does the camera only truck left in the scene?

- Does the camera only truck leftward?

- Does the camera only truck from right to left?

- Is the camera movement purely leftward?

- Is the camera only moving left (no panning or other movements)?

- Is the camera only translating to the left?

- Is this exclusively a leftward tracking shot?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot feature only leftward camera movement?

- Is the camera only traveling left in the scene?

- Is this just a leftward tracking shot?

- Is this strictly a left trucking motion?

- Does the camera only move physically from right to left?

- Is this just a lateral movement to the left?

- Does the camera only dolly left?

- Is this purely a leftward dolly shot?

- Is the camera only sliding left?

- Is this exclusively a left trucking shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera only moves left.

- A shot where the camera only moves leftward.

- A shot where the camera only moves from right to left.

- A shot where the camera only trucks left.

- A shot where the camera only trucks leftward.

- A shot where the camera only trucks from right to left.

- The camera only moves leftward.

- The camera only trucks left in the scene.

- A shot where the camera only trucks left.

- A video demonstrating pure leftward camera translation.

- A scene where the camera only moves physically from right to left.

- A shot with only lateral leftward movement.

- A scene where the camera only moves left (no panning or other movements).

- A video featuring exclusively leftward camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot with pure leftward camera motion (moving sideways only).

- A video where the camera only travels left.

- A scene featuring only leftward tracking movement.

- A video where the camera only dollies left.

- A scene with pure leftward tracking motion.

- A shot where the camera only slides left.

- A video featuring only left trucking movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.left is True and self.cam_motion.check_if_no_motion_cam(exclude=['left'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.left is False or not self.cam_motion.check_if_no_motion_cam(exclude=['left'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_right</b>: <code>self.cam_motion.right is True</code>

- <b>only_moving_right</b>: <code>self.cam_motion.right is True and self.cam_motion.check_if_no_motion_cam(exclude=['right'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_left</b>: <code>self.cam_motion.pan_left is True and self.cam_motion.left is False</code>

- <b>compound_motion_with_left</b>: <code>self.cam_motion.left is True and not self.cam_motion.check_if_no_motion_cam(exclude=['left'])</code>

</details>

</details>
