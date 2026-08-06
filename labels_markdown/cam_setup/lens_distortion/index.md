# Lens_distortion Overview

<details>
<summary><h2>With Lens Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>barrel_distortion</code>


<h3>📖 Definition:</h3>
Does this shot contain noticeable yet slight barrel distortion?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does this shot contain slight barrel distortion?

- Does this shot show any slight barrel distortion?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there any slight warping or bending effect in this scene?

- Is this video captured using a lens that slightly distorts the perspective?

- Is the frame slightly bending or curving due to lens effects?

- Does the perspective appear slightly exaggerated or stretched?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot captured with noticeable yet slight barrel distortion.

- A video with visible slight barrel distortion.

- A scene with slight barrel distortion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the frame appears slightly warped due to lens effects.

- A shot where the edges appear slightly curved or stretched.

- A perspective altered by slight barrel distortion.

- A scene with an exaggerated field of view due to slight barrel distortion.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.barrel_distortion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.barrel_distortion is False</code>

</details>

<details>
<summary><h2>Fisheye Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fisheye_distortion</code>


<h3>📖 Definition:</h3>
Does this shot have a noticeable fisheye lens distortion?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the scene heavily warped due to a fisheye effect?

- Is the perspective highly curved outward in a fisheye-like manner?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot have extreme barrel distortion?

- Is the field of view significantly exaggerated?

- Does the image look highly curved, especially near the edges?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot with noticable fisheye lens distortion.

- A video where the perspective is heavily curved outward.

- A scene with extreme warping caused by a fisheye lens.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where straight lines appear curved due to fisheye distortion.

- A perspective heavily stretched near the frame edges.

- A video effect caused by an ultra-wide fisheye lens.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.fisheye_distortion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.fisheye_distortion is False</code>

</details>

<details>
<summary><h2>No Lens Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>no_lens_distortion</code>


<h3>📖 Definition:</h3>
Does this shot have no noticeable lens distortion?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does this shot have no noticeable barrel or fisheye distortion?

- Is this shot captured with a regular lens without distortion?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the lens distortion absent in this scene?

- Is there no fisheye or barrel distortion in this shot?

- Does the frame appear natural without noticeable warping?

- Is the perspective straight without lens-induced bending?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot without noticeable lens distortion.

- A video with a natural, undistorted perspective.

- A scene where the frame is clear of any fisheye or barrel distortion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot with a regular lens and no distortion.

- A perspective without bending or warping effects.

- A natural-looking shot without any lens artifacts.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.no_lens_distortion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.no_lens_distortion is False</code>

</details>

<details>
<summary><h2>With Lens Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>with_lens_distortion</code>


<h3>📖 Definition:</h3>
Does this shot contain noticeable barrel or fisheye distortion?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does this shot contain noticeable lens distortion?

- Does this shot show any fisheye or barrel distortion?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there any warping or bending effect in this scene?

- Is this video captured using a lens that distorts the perspective?

- Is the frame bending or curving due to lens effects?

- Does the perspective appear exaggerated or stretched?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video with noticeable barrel or fisheye distortion.

- A shot captured with noticeable lens distortion.

- A scene with visible fisheye or barrel distortion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the frame appears warped due to lens effects.

- A shot where the edges appear curved or stretched.

- A perspective altered by lens-induced warping.

- A scene with an exaggerated field of view due to lens distortion.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.with_lens_distortion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.with_lens_distortion is False</code>

</details>
