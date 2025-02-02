# Motion_complexity Overview

<details>
<summary><h2>Is Complex Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_complex_motion</code>


<h3>📖 Definition:</h3>
Does the camera show complex motion, such as moving in conflicting directions, or showing different motions at different times, or having multiple movements at different speeds, or is its motion unclear?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera show complex motion that is hard to classify?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera performing conflicting or multi-step movements?

- Does the shot contain a combination of different camera motions?

- Is there sequential, conflicting, or speed-varying motion in the scene?

- Does the camera motion change direction, sequence, or speed in a complex way?

- Does the camera move in multiple directions within the shot?

- Is there an advanced or unpredictable camera movement?

- Does the camera motion shift unexpectedly or in distinct phases?

- Is the shot difficult to describe with a single camera movement label?

- Does the camera perform a complex maneuver with multiple changes?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera executes a complex movement that is hard to classify.

- The camera moves in a complex way that doesn't fit standard motion categories.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene featuring complex camera motion with multiple phases or directions.

- A shot where the camera performs sequential or conflicting movements.

- A video where different camera motions occur at varying speeds.

- A video with intricate or multi-step camera movement.

- A shot where the camera shifts direction or sequence unpredictably.

- A scene where multiple camera motions occur with different speeds.

- A cinematic movement that combines conflicting, sequential, or varied-speed motions.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement == 'major_complex'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_movement != 'major_complex'</code>

</details>

<details>
<summary><h2>Has Minor Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_minor_motion</code>


<h3>📖 Definition:</h3>
Is the camera motion minimal, hard to discern, or very subtle?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the shot feature only slight or barely noticeable movement?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera movement too small to classify clearly?

- Does the scene contain only minor or insignificant camera motion?

- Is the motion so subtle that it is difficult to detect?

- Does the camera exhibit slight drifting or shaking with no clear direction?

- Is there barely any noticeable movement in the shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A scene where the camera movement is minimal or difficult to perceive.

- A shot with barely noticeable or insignificant camera motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera motion is too minor to classify.

- A scene featuring subtle, low-magnitude camera movement.

- A shot where the camera drifts slightly without clear motion.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement == 'minor'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_movement != 'minor' and self.cam_motion.steadiness not in ['unsteady', 'very_unsteady']</code>

</details>

<details>
<summary><h2>Is Simple Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_simple_motion</code>


<h3>📖 Definition:</h3>
Does the camera show simple motion, such as moving in a single direction, maintaining a consistent speed, or following a clear and predictable path?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera show motion that is easy to classify?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera performing a straightforward, single-direction movement?

- Does the shot contain a simple and consistent camera motion?

- Is there a smooth, predictable motion in the scene?

- Does the camera move in a steady and controlled manner?

- Does the shot feature a single, clearly defined camera movement?

- Is the camera motion easy to describe with a single label?

- Does the camera follow a clear and intentional movement path?

- Is there a stable and natural camera motion in the shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera moves in a simple, straightforward way that is easy to classify.

- The camera follows a single, clear motion without complex changes.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene featuring a smooth, predictable camera movement.

- A shot where the camera moves in a clear and steady direction.

- A video where the camera motion remains simple and controlled.

- A shot demonstrating a basic and easily understandable camera movement.

- A scene where the camera follows a linear or predictable motion path.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.camera_movement == 'major_simple'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.camera_movement != 'major_simple'</code>

</details>
