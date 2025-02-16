# Angle Overview

<details>
<summary><h2>Camera Angle Change From High To Low</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_change_from_high_to_low</code>


<h3>📖 Definition:</h3>
Does the camera angle decrease noticeably relative to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera tilt downward during the shot?

- Is there a transition from high to low angle?

- Does the camera perspective shift downward?

- Is there a descending camera movement?

- Does the shot angle move from high to low?

- Is there a downward tilt in camera angle?

- Does the viewing angle decrease vertically?

- Is there a lowering of camera perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera angle transitions from a higher to a lower position relative to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing downward camera tilt.

- A shot transitioning to lower angle.

- A video with descending perspective.

- A shot featuring downward movement.

- A video showing angle reduction.

- A shot with lowering camera view.

- A video transitioning downward.

- A shot with decreasing angle.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_change_from_high_to_low is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_change_from_high_to_low is False</code>

</details>

<details>
<summary><h2>Camera Angle Change From Low To High</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_change_from_low_to_high</code>


<h3>📖 Definition:</h3>
Does the camera angle increase noticeably relative to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera tilt upward during the shot?

- Is there a transition from low to high angle?

- Does the camera perspective shift upward?

- Is there an ascending camera movement?

- Does the shot angle move from low to high?

- Is there an upward tilt in camera angle?

- Does the viewing angle increase vertically?

- Is there a raising of camera perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera angle transitions from a lower to a higher position relative to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing upward camera tilt.

- A shot transitioning to higher angle.

- A video with ascending perspective.

- A shot featuring upward movement.

- A video showing angle increase.

- A shot with rising camera view.

- A video transitioning upward.

- A shot with increasing angle.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_change_from_low_to_high is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_change_from_low_to_high is False</code>

</details>

<details>
<summary><h2>Is Camera Angle Applicable</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_camera_angle_applicable</code>


<h3>📖 Definition:</h3>
Is camera angle classification possible for this video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Can the camera angle be meaningfully categorized?

- Is it possible to determine the camera's angular position?

- Can we assess the camera's rotational angle?

- Is the camera angle clear enough to classify?

- Can the camera's orientation be effectively categorized?

- Is it feasible to determine the shot angle?

- Can we meaningfully analyze the camera angle?

- Is the camera's angular position classifiable?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera angle can be meaningfully classified.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with classifiable camera angle.

- A shot with determinable angular position.

- A video where camera orientation can be assessed.

- A shot with clear angle categorization.

- A video suitable for angle classification.

- A shot with analyzable camera position.

- A video with measurable camera angle.

- A shot with definable orientation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_camera_angle_applicable is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_camera_angle_applicable is False</code>

</details>

<details>
<summary><h2>Is Dutch Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_dutch_angle</code>


<h3>📖 Definition:</h3>
Is an obvious Dutch (Canted) angle (of more than 15 degrees) present in the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot use a tilted camera angle?

- Is there an intentional diagonal tilt to the frame?

- Does the camera employ a canted angle?

- Is the horizon line intentionally tilted?

- Does the shot feature an oblique camera angle?

- Is there a deliberate tilt in the frame's orientation?

- Does the video use an angled perspective?

- Is the camera rotated off its horizontal axis?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that employs an obvious Dutch (Canted) camera angle of more than 15 degrees.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video using tilted camera perspective.

- A shot with intentional frame rotation.

- A video featuring canted angle.

- A shot with diagonal orientation.

- A video showing oblique perspective.

- A shot employing tilted framing.

- A video with angled camera position.

- A shot using rotated perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_dutch_angle is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_dutch_angle is False</code>

</details>

<details>
<summary><h2>Is Dutch Angle Fixed</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_dutch_angle_fixed</code>


<h3>📖 Definition:</h3>
Does the Dutch angle remain the same throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the tilted angle consistent throughout the shot?

- Does the camera maintain a steady Dutch angle?

- Is there a constant degree of frame tilt?

- Does the oblique angle stay fixed?

- Is the canted angle maintained steadily?

- Does the rotational tilt remain unchanged?

- Is there a consistent frame rotation?

- Does the tilted perspective stay stable?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot maintaining a consistent Dutch angle throughout its duration.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with steady tilt angle.

- A shot maintaining fixed rotation.

- A video with constant oblique angle.

- A shot showing stable Dutch angle.

- A video with unchanging frame tilt.

- A shot keeping consistent rotation.

- A video with fixed angular position.

- A shot maintaining steady tilt.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_dutch_angle_fixed is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_dutch_angle_fixed is False</code>

</details>

<details>
<summary><h2>Is Dutch Angle Varying</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_dutch_angle_varying</code>


<h3>📖 Definition:</h3>
Does the degree of the Dutch angle shift throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the tilted angle change during the shot?

- Is there variation in the camera's rotational tilt?

- Does the Dutch angle degree fluctuate?

- Is there dynamic change in the frame's tilt?

- Does the oblique angle vary throughout?

- Is there movement in the canted angle?

- Does the frame rotation change over time?

- Is there variation in the tilted perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the degree of Dutch angle changes throughout its duration.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with varying tilt angles.

- A shot showing dynamic frame rotation.

- A video with changing oblique angles.

- A shot featuring variable Dutch angles.

- A video with fluctuating frame tilt.

- A shot showing rotation changes.

- A video with dynamic angle shifts.

- A shot featuring varying tilts.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_dutch_angle_varying is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_dutch_angle_varying is False</code>

</details>


## Subcategories

- [End_with](./end_with/index.md)
- [From_to](./from_to/index.md)
- [Is_always](./is_always/index.md)
- [Start_with](./start_with/index.md)