# Roll_clockwise Overview

<details>
<summary><h2>Has Clockwise Roll Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_roll_clockwise</code>


<h3>📖 Definition:</h3>
Does the camera roll clockwise?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera roll clockwise in the scene?

- Is there a clockwise roll motion in the scene?

- Is the camera rolling in a clockwise direction?

- Is the camera rotating around its optical axis in a clockwise manner?

- Is there a clockwise roll in the shot?

- Is the camera rolling clockwise?

- Does the camera rotate clockwise around its optical axis?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera spin clockwise along its forward axis?

- Is there a clockwise Dutch roll in the shot?

- Does the camera perform a clockwise barrel roll?

- Is the camera rolling clockwise relative to the horizon?

- Does the horizon rotate clockwise in the shot?

- Is there a clockwise Dutch angle movement?

- Is there a clockwise canted angle movement?

- Does the frame rotate clockwise while keeping the subject centered?

- Is the camera executing a clockwise roll motion?

- Does the shot feature a clockwise rotational movement around the lens axis?

- Is there a clockwise spinning motion of the frame?

- Does the camera twist clockwise in the scene?

- Is this a clockwise Dutch roll shot?

- Does the camera create a clockwise rotating horizon effect?

- Is there a clockwise angular rotation of the frame?

- Does the shot employ a clockwise rolling technique?

- Is the camera performing a clockwise rotational movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera rolls clockwise.

- A shot where the camera rolls clockwise.

- A scene with clockwise camera rotation around its optical axis.

- The camera executes a clockwise roll motion.

- A shot with a clockwise camera roll.

- A scene featuring a clockwise roll motion.

- The camera rolls clockwise in the shot.

- The camera rolls in a clockwise direction.

- A camera roll movement in a clockwise direction.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot featuring a clockwise Dutch roll.

- The camera performs a clockwise barrel roll.

- A video showing clockwise rotation relative to the horizon.

- A shot with clockwise Dutch angle movement.

- A scene where the camera spins clockwise along its forward axis.

- A shot demonstrating clockwise canted angle movement.

- A video where the frame rotates clockwise around the center.

- A scene featuring clockwise Dutch roll technique.

- A shot where the horizon rotates clockwise.

- A video showing clockwise angular rotation of the frame.

- A scene with clockwise barrel roll movement.

- A shot employing clockwise Dutch angle technique.

- A video demonstrating clockwise rotational movement around the lens axis.

- A scene where the camera twists clockwise.

- A shot with clockwise spinning motion of the frame.

- A video featuring clockwise roll movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.roll_cw is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.roll_cw is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>rolling_counterclockwise</b>: <code>self.cam_motion.roll_ccw is True</code>

</details>

</details>

<details>
<summary><h2>Only Clockwise Roll Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_roll_clockwise</code>


<h3>📖 Definition:</h3>
Does the camera only roll clockwise without any other camera movements?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera only roll clockwise in the scene?

- Does the camera only rotate clockwise around its optical axis?

- Is there only a clockwise Dutch roll in the shot?

- Does the camera perform only a clockwise barrel roll?

- Is the camera only rolling clockwise relative to the horizon?

- Does the horizon only rotate clockwise in the shot?

- Is there exclusively a clockwise Dutch angle movement?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only spinning clockwise along its forward axis?

- Is there only a clockwise canted angle movement?

- Does the frame only rotate clockwise while keeping the subject centered?

- Is the camera executing only a clockwise roll motion?

- Does the shot feature exclusively clockwise rotational movement around the lens axis?

- Is there only a clockwise spinning motion of the frame?

- Does the camera only twist clockwise in the scene?

- Is this purely a clockwise Dutch roll shot?

- Does the camera create only a clockwise rotating horizon effect?

- Is there exclusively a clockwise angular rotation of the frame?

- Does the shot employ only a clockwise rolling technique?

- Is the camera performing exclusively clockwise rotational movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera only rolls clockwise without any other camera movements.

- A shot where the camera only rolls clockwise.

- A shot featuring only a clockwise Dutch roll.

- A scene with only clockwise camera rotation around its optical axis.

- The camera performs only a clockwise barrel roll.

- A video showing only clockwise rotation relative to the horizon.

- A shot with exclusively clockwise Dutch angle movement.

- The camera executes only a clockwise roll motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera only spins clockwise along its forward axis.

- A shot demonstrating purely clockwise canted angle movement.

- A video where the frame only rotates clockwise around the center.

- A scene featuring exclusively clockwise Dutch roll technique.

- A shot where the horizon only rotates clockwise.

- A video showing purely clockwise angular rotation of the frame.

- A scene with only clockwise barrel roll movement.

- A shot employing exclusively clockwise Dutch angle technique.

- A video demonstrating only clockwise rotational movement around the lens axis.

- A scene where the camera only twists clockwise.

- A shot with purely clockwise spinning motion of the frame.

- A video featuring exclusively clockwise roll movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.roll_cw is True and self.cam_motion.check_if_no_motion(exclude=['roll_cw'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.roll_cw is False or not self.cam_motion.check_if_no_motion(exclude=['roll_cw'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>rolling_counterclockwise</b>: <code>self.cam_motion.roll_ccw is True</code>

- <b>only_rolling_counterclockwise</b>: <code>self.cam_motion.roll_ccw is True and self.cam_motion.check_if_no_motion(exclude=['roll_ccw'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>panning_rotation</b>: <code>self.cam_motion.pan_right is True or self.cam_motion.pan_left is True</code>

- <b>compound_motion_with_roll_cw</b>: <code>self.cam_motion.roll_cw is True and not self.cam_motion.check_if_no_motion(exclude=['roll_cw'])</code>

</details>

</details>
