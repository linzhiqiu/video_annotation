# Rightward Overview

<details>
<summary><h2>Has Rightward Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_rightward</code>


<h3>📖 Definition:</h3>
Does the camera move rightward in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move right in the scene?

- Does the camera move from left to right?

- Does the camera truck right in the scene?

- Does the camera truck rightward?

- Does the camera truck from left to right?

- Is the camera moving rightward?

- Is the camera trucking right?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move right (not pan right)?

- Does the shot feature a rightward camera movement (moving, not rotating)?

- Is the camera traveling right in the scene?

- Is this a rightward tracking shot?

- Is this a right trucking motion (not panning)?

- Is the camera translating to the right?

- Does the camera physically move from left to right?

- Is the camera tracking rightward?

- Is this a lateral movement to the right?

- Does the camera dolly right?

- Is this a rightward dolly shot?

- Is the camera sliding right?

- Does the camera track from left to right?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera moves rightward.

- The camera moves right.

- A shot where the camera moves right.

- A shot where the camera moves rightward.

- A shot where the camera moves from left to right.

- A shot where the camera trucks right.

- A shot where the camera trucks rightward.

- A shot where the camera trucks from left to right.

- The camera moves from left to right.

- The camera trucks right.

- The camera trucks rightward.

- The camera trucks from left to right.

- The camera trucks right in the scene.

- A video featuring rightward camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera moves right (not panning right).

- A shot with rightward camera motion (moving sideways, not rotating).

- A video where the camera travels right.

- A scene featuring rightward tracking movement.

- A shot where the camera trucks right without rotation.

- A video demonstrating rightward camera translation.

- A scene where the camera physically moves from left to right.

- A shot with lateral rightward movement.

- A video where the camera dollies right.

- A scene with rightward tracking motion.

- A shot where the camera slides right.

- A video featuring a right trucking movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.right is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.right is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_left</b>: <code>self.cam_motion.left is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_right</b>: <code>self.cam_motion.pan_right is True and self.cam_motion.right is False</code>

</details>

</details>

<details>
<summary><h2>Only Rightward Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_rightward</code>


<h3>📖 Definition:</h3>
Does the camera only move rightward without any other camera movements?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only move right in the scene?

- Does the camera only move from left to right?

- Does the camera only truck right in the scene?

- Does the camera only truck rightward?

- Does the camera only truck from left to right?

- Is the camera movement purely rightward?

- Is the camera only moving right (no panning or other movements)?

- Is the camera only translating to the right?

- Is this exclusively a rightward tracking shot?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot feature only rightward camera movement?

- Is the camera only traveling right in the scene?

- Is this just a rightward tracking shot?

- Is this strictly a right trucking motion?

- Does the camera only move physically from left to right?

- Is this just a lateral movement to the right?

- Does the camera only dolly right?

- Is this purely a rightward dolly shot?

- Is the camera only sliding right?

- Is this exclusively a right trucking shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera only moves rightward without any other camera movements.

- A shot where the camera only moves right.

- A shot where the camera only moves rightward.

- A shot where the camera only moves from left to right.

- A shot where the camera only trucks right.

- A shot where the camera only trucks rightward.

- A shot where the camera only trucks from left to right.

- The camera only moves rightward.

- The camera only trucks right in the scene.

- A scene where the camera only moves right (no panning or other movements).

- A shot where the camera only trucks right.

- A video demonstrating pure rightward camera translation.

- A scene where the camera only moves physically from left to right.

- A shot with only lateral rightward movement.

- A video featuring exclusively rightward camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot with pure rightward camera motion (moving sideways only).

- A video where the camera only travels right.

- A scene featuring only rightward tracking movement.

- A video where the camera only dollies right.

- A scene with pure rightward tracking motion.

- A shot where the camera only slides right.

- A video featuring only right trucking movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.right is True and self.cam_motion.check_if_no_motion(exclude=['right'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.right is False or not self.cam_motion.check_if_no_motion(exclude=['right'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_left</b>: <code>self.cam_motion.left is True</code>

- <b>only_moving_left</b>: <code>self.cam_motion.left is True and self.cam_motion.check_if_no_motion(exclude=['left'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_right</b>: <code>self.cam_motion.pan_right is True and self.cam_motion.right is False</code>

- <b>compound_motion_with_right</b>: <code>self.cam_motion.right is True and not self.cam_motion.check_if_no_motion(exclude=['right'])</code>

</details>

</details>
