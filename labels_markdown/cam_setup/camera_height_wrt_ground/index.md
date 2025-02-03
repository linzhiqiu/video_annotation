# Camera_height_wrt_ground Overview

<details>
<summary><h2>Above Water To Underwater</h2></summary>


<h3>🔵 Label Name:</h3>
<code>above_water_to_underwater</code>


<h3>📖 Definition:</h3>
Does the camera transition from above water to underwater?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot move from surface to underwater view?

- Is there a submersion of the camera into water?

- Does the perspective change from above to below water?

- Is there a transition beneath the water surface?

- Does the camera dive below water level?

- Is there a shift from air to underwater view?

- Does the shot submerge into water?

- Is there a descent into underwater perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that transitions from an above-water to an underwater perspective.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from surface to underwater.

- A shot transitioning below water.

- A video showing camera submersion.

- A shot diving beneath water surface.

- A video entering underwater view.

- A shot descending into water.

- A video transitioning to underwater.

- A shot submerging below surface.

</details>

<h4>🟢 Positive:</h4>
<code>self.above_water_to_underwater is True</code>

<h4>🔴 Negative:</h4>
<code>self.above_water_to_underwater is False</code>

</details>

<details>
<summary><h2>Height Wrt Ground Change From High To Low</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_change_from_high_to_low</code>


<h3>📖 Definition:</h3>
Does the camera height decrease noticeably in relation to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera descend closer to ground level?

- Is there a downward movement in camera elevation?

- Does the shot show decreasing camera height?

- Is there a lowering of the camera position?

- Does the camera move from high to low elevation?

- Is there a descent in camera height?

- Does the vertical position decrease relative to ground?

- Is there a downward shift in camera elevation?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera height decreases notably in relation to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing camera descent.

- A shot with decreasing elevation.

- A video moving closer to ground.

- A shot featuring downward movement.

- A video with lowering camera position.

- A shot showing height reduction.

- A video with descending perspective.

- A shot moving to lower elevation.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_change_from_high_to_low is True</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_change_from_high_to_low is False</code>

</details>

<details>
<summary><h2>Height Wrt Ground Change From Low To High</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_change_from_low_to_high</code>


<h3>📖 Definition:</h3>
Does the camera height increase noticeably in relation to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera rise from ground level?

- Is there an upward movement in camera elevation?

- Does the shot show increasing camera height?

- Is there a raising of the camera position?

- Does the camera move from low to high elevation?

- Is there an ascent in camera height?

- Does the vertical position increase relative to ground?

- Is there an upward shift in camera elevation?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera height increases notably in relation to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing camera ascent.

- A shot with increasing elevation.

- A video moving higher from ground.

- A shot featuring upward movement.

- A video with rising camera position.

- A shot showing height increase.

- A video with ascending perspective.

- A shot moving to higher elevation.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_change_from_low_to_high is True</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_change_from_low_to_high is False</code>

</details>

<details>
<summary><h2>Is Overall Height Applicable</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_overall_height_applicable</code>


<h3>📖 Definition:</h3>
Is overall height classification possible for this video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Can the camera height relative to ground be classified?

- Is it possible to determine the camera's elevation?

- Can we assess the camera's height from ground level?

- Is the camera's vertical position measurable?

- Can we classify the height of the camera view?

- Is it feasible to determine camera elevation?

- Can the camera's ground-relative height be assessed?

- Is the camera height clear enough to classify?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the overall camera height can be meaningfully classified.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with classifiable camera elevation.

- A shot with clear vertical positioning.

- A video where camera height is apparent.

- A shot showing definable camera elevation.

- A video with measurable camera height.

- A shot displaying clear elevation.

- A video with assessable camera position.

- A shot with determinable height.

</details>

<h4>🟢 Positive:</h4>
<code>any(height != 'unknown' for height in self.height_wrt_ground_info.values())</code>

<h4>🔴 Negative:</h4>
<code>not any(height != 'unknown' for height in self.height_wrt_ground_info.values())</code>

</details>

<details>
<summary><h2>Underwater To Above Water</h2></summary>


<h3>🔵 Label Name:</h3>
<code>underwater_to_above_water</code>


<h3>📖 Definition:</h3>
Does the camera transition from underwater to above water?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot move from underwater to surface view?

- Is there an emergence of the camera from water?

- Does the perspective change from below to above water?

- Is there a transition to above the water surface?

- Does the camera rise above water level?

- Is there a shift from underwater to air view?

- Does the shot emerge from water?

- Is there an ascent to above-water perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that transitions from an underwater to an above-water perspective.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from underwater to surface.

- A shot transitioning above water.

- A video showing camera emergence.

- A shot rising above water surface.

- A video exiting underwater view.

- A shot ascending from water.

- A video transitioning to surface.

- A shot emerging above water.

</details>

<h4>🟢 Positive:</h4>
<code>self.underwater_to_above_water is True</code>

<h4>🔴 Negative:</h4>
<code>self.underwater_to_above_water is False</code>

</details>
