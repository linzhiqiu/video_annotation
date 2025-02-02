# Lens_distortion Overview

<details>
<summary><h2>Fisheye Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fisheye_distortion</code>


<h3>📖 Definition:</h3>
Does this shot have a fisheye lens distortion?

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

- A shot with strong fisheye distortion.

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
<code>self.cam_setup.lens_distortion == 'fisheye'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.lens_distortion != 'fisheye'</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>no_lens_distortion</b>: <code>self.cam_setup.lens_distortion == 'regular'</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>barrel_distortion</b>: <code>self.cam_setup.lens_distortion == 'barrel'</code>

</details>

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

- A shot captured without noticeable lens distortion.

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
<code>self.cam_setup.lens_distortion == 'regular'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.lens_distortion != 'regular'</code>

</details>

<details>
<summary><h2>With Lens Distortion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>with_lens_distortion</code>


<h3>📖 Definition:</h3>
Does this shot contain noticeable lens distortion?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does this shot contain noticeable barrel or fisheye distortion?

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

- A shot captured with noticeable lens distortion.

- A video with visible barrel or fisheye distortion.

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
<code>self.cam_setup.lens_distortion in ['barrel', 'fisheye']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.lens_distortion == 'regular'</code>

</details>
