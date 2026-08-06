# Roll_counterclockwise Overview

<details>
<summary><h2>Has Counterclockwise Roll Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_roll_counterclockwise</code>


<h3>📖 Definition:</h3>
Does the camera roll counterclockwise?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera roll counterclockwise in the scene?

- Is there a counterclockwise roll motion in the scene?

- Is the camera rolling in a counterclockwise direction?

- Is the camera rotating around its optical axis in a counterclockwise manner?

- Is there a counterclockwise roll in the shot?

- Is the camera rolling counterclockwise?

- Does the camera rotate counterclockwise around its optical axis?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a counterclockwise Dutch roll in the shot?

- Does the camera perform a counterclockwise barrel roll?

- Is the camera rolling counterclockwise relative to the horizon?

- Does the horizon rotate counterclockwise in the shot?

- Is there a counterclockwise Dutch angle movement?

- Does the camera spin counterclockwise along its forward axis?

- Is there a counterclockwise canted angle movement?

- Does the frame rotate counterclockwise while keeping the subject centered?

- Is the camera executing a counterclockwise roll motion?

- Does the shot feature a counterclockwise rotational movement around the lens axis?

- Is there a counterclockwise spinning motion of the frame?

- Does the camera twist counterclockwise in the scene?

- Is this a counterclockwise Dutch roll shot?

- Does the camera create a counterclockwise rotating horizon effect?

- Is there a counterclockwise angular rotation of the frame?

- Does the shot employ a counterclockwise rolling technique?

- Is the camera performing a counterclockwise rotational movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera rolls counterclockwise.

- A shot where the camera rolls counterclockwise.

- A scene with counterclockwise camera rotation around its optical axis.

- The camera executes a counterclockwise roll motion.

- A shot with a counterclockwise camera roll.

- A scene featuring a counterclockwise roll motion.

- The camera rolls counterclockwise in the shot.

- The camera rolls in a counterclockwise direction.

- A camera roll movement in a counterclockwise direction.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot featuring a counterclockwise Dutch roll.

- The camera performs a counterclockwise barrel roll.

- A video showing counterclockwise rotation relative to the horizon.

- A shot with counterclockwise Dutch angle movement.

- The camera executes a counterclockwise roll motion.

- A scene where the camera spins counterclockwise along its forward axis.

- A shot demonstrating counterclockwise canted angle movement.

- A video where the frame rotates counterclockwise around the center.

- A scene featuring counterclockwise Dutch roll technique.

- A shot where the horizon rotates counterclockwise.

- A video showing counterclockwise angular rotation of the frame.

- A scene with counterclockwise barrel roll movement.

- A shot employing counterclockwise Dutch angle technique.

- A video demonstrating counterclockwise rotational movement around the lens axis.

- A scene where the camera twists counterclockwise.

- A shot with counterclockwise spinning motion of the frame.

- A video featuring counterclockwise roll movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.roll_ccw is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.roll_ccw is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>rolling_clockwise</b>: <code>self.cam_motion.roll_cw is True</code>

</details>

</details>

<details>
<summary><h2>Only Counterclockwise Roll Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_roll_counterclockwise</code>


<h3>📖 Definition:</h3>
Does the camera only roll counterclockwise without any other camera movements?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only roll counterclockwise in the scene?

- Does the camera only rotate counterclockwise around its optical axis?

- Is there only a counterclockwise Dutch roll in the shot?

- Does the camera perform only a counterclockwise barrel roll?

- Is the camera only rolling counterclockwise relative to the horizon?

- Does the horizon only rotate counterclockwise in the shot?

- Is there exclusively a counterclockwise Dutch angle movement?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only spinning counterclockwise along its forward axis?

- Is there only a counterclockwise canted angle movement?

- Does the frame only rotate counterclockwise while keeping the subject centered?

- Is the camera executing only a counterclockwise roll motion?

- Does the shot feature exclusively counterclockwise rotational movement around the lens axis?

- Is there only a counterclockwise spinning motion of the frame?

- Does the camera only twist counterclockwise in the scene?

- Is this purely a counterclockwise Dutch roll shot?

- Does the camera create only a counterclockwise rotating horizon effect?

- Is there exclusively a counterclockwise angular rotation of the frame?

- Does the shot employ only a counterclockwise rolling technique?

- Is the camera performing exclusively counterclockwise rotational movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera only rolls counterclockwise without any other camera movements.

- A shot where the camera only rolls counterclockwise.

- A shot featuring only a counterclockwise Dutch roll.

- A scene with only counterclockwise camera rotation around its optical axis.

- The camera performs only a counterclockwise barrel roll.

- A video showing only counterclockwise rotation relative to the horizon.

- A shot with exclusively counterclockwise Dutch angle movement.

- The camera executes only a counterclockwise roll motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera only spins counterclockwise along its forward axis.

- A shot demonstrating purely counterclockwise canted angle movement.

- A video where the frame only rotates counterclockwise around the center.

- A scene featuring exclusively counterclockwise Dutch roll technique.

- A shot where the horizon only rotates counterclockwise.

- A video showing purely counterclockwise angular rotation of the frame.

- A scene with only counterclockwise barrel roll movement.

- A shot employing exclusively counterclockwise Dutch angle technique.

- A video demonstrating only counterclockwise rotational movement around the lens axis.

- A scene where the camera only twists counterclockwise.

- A shot with purely counterclockwise spinning motion of the frame.

- A video featuring exclusively counterclockwise roll movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.roll_ccw is True and self.cam_motion.check_if_no_motion(exclude=['roll_ccw'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.roll_ccw is False or not self.cam_motion.check_if_no_motion(exclude=['roll_ccw'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>rolling_clockwise</b>: <code>self.cam_motion.roll_cw is True</code>

- <b>only_rolling_clockwise</b>: <code>self.cam_motion.roll_cw is True and self.cam_motion.check_if_no_motion(exclude=['roll_cw'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_rotation</b>: <code>self.cam_motion.pan_right is True or self.cam_motion.pan_left is True</code>

- <b>compound_motion_with_roll_ccw</b>: <code>self.cam_motion.roll_ccw is True and not self.cam_motion.check_if_no_motion(exclude=['roll_ccw'])</code>

</details>

</details>
