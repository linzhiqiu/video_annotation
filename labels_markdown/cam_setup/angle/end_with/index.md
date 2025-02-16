# End_with Overview

<details>
<summary><h2>Camera Angle End With Bird Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_bird_eye_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at a bird’s eye angle, looking directly downward at the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera looking straight down?

- Is the ending frame positioned at a bird’s eye perspective?

- Does the video conclude with an extreme high-angle shot looking downward?

- Is the final shot captured from above, looking down at the environment?

- Does the sequence close with a bird’s eye view, looking vertically down?

- Is the last shot taken from the highest perspective, directed downward?

- Does the video close with a top-down perspective?

- Is the final frame recorded with the camera positioned directly overhead?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at a bird’s eye angle, looking directly downward at the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a bird’s eye angle, looking directly downward.

- A video concluding with a bird’s eye perspective, capturing the ground below.

- A sequence that ends with the camera positioned directly overhead and looking down.

- A shot showing the environment from a bird’s eye perspective.

- A video closing with a top-down, overhead framing.

- A shot where the camera is positioned high above and facing downward.

- A video that ends with the camera capturing subjects from a top-down viewpoint.

- A scene that closes with the camera looking sharply downward at the ground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['end'] == 'bird_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_info['end'] not in ['bird_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle End With High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_high_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera angled slightly downward?

- Is the ending frame positioned at a high-angle perspective?

- Does the video conclude with a downward camera angle?

- Is the final shot captured from above, looking down at a subject or environment?

- Does the sequence close with a high-angle view?

- Is the last shot taken from an elevated position, angled downward?

- Does the video close with a slightly top-down perspective?

- Is the final frame recorded with the camera looking downward at an angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a high angle, looking slightly downward.

- A video concluding with a high-angle perspective, capturing the subject from above.

- A sequence that ends with the camera positioned higher than the subject.

- A shot showing the environment from an elevated, downward-facing viewpoint.

- A video closing with a subtly top-down, downward angle.

- A shot where the camera is positioned higher than eye level and facing down.

- A video that ends with the camera framing subjects from a slightly elevated perspective.

- A scene that closes with the camera tilted downward, emphasizing height differences.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['end'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_info['end'] not in ['high_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle End With Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_level_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera at a level angle?

- Is the ending frame positioned at a straight-on perspective?

- Does the video conclude with a level camera angle?

- Is the final shot captured with the camera parallel to the ground?

- Does the sequence close with a straight-on viewpoint?

- Is the last shot taken at a neutral, balanced angle?

- Does the video close with an eye-level or flat horizon perspective?

- Is the final frame recorded with no vertical tilt?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at a level angle, parallel to the ground regardless of Dutch angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a level angle, positioned parallel to the ground.

- A video concluding with a neutral camera perspective.

- A sequence that ends with the camera at a straight-on viewpoint.

- A shot showing the environment from a flat horizon level.

- A video closing with a balanced, natural perspective.

- A shot where the camera maintains a level position without tilting.

- A video that ends with an eye-level or straight-on angle.

- A scene that closes with a perfectly horizontal framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['end'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_info['end'] not in ['level_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle End With Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_low_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera angled slightly upward?

- Is the ending frame positioned at a low-angle perspective?

- Does the video conclude with an upward-facing camera angle?

- Is the final shot captured from below, looking up at a subject or environment?

- Does the sequence close with a low-angle view?

- Is the last shot taken from a lower perspective, angled upward?

- Does the video close with a subtly bottom-up perspective?

- Is the final frame recorded with the camera looking up at an angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a low angle, looking slightly upward.

- A video concluding with a low-angle perspective, capturing the subject from below.

- A sequence that ends with the camera positioned lower than the subject.

- A shot showing the environment from a lower, upward-facing viewpoint.

- A video closing with a subtly bottom-up, upward angle.

- A shot where the camera is positioned lower than eye level and facing up.

- A video that ends with the camera framing subjects from a slightly low perspective.

- A scene that closes with the camera tilted upward, emphasizing height differences.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['end'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_info['end'] not in ['low_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle End With Worm Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_worm_eye_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at a worm’s eye angle, looking sharply upward to the sky?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera looking straight up?

- Is the ending frame positioned at a worm’s eye perspective?

- Does the video conclude with an extreme low-angle shot looking upward?

- Is the final shot captured from below, with the camera pointing skyward?

- Does the sequence close with a worm’s eye view, looking vertically up?

- Is the last shot taken from the lowest perspective, directed upward?

- Does the video close with an angle opposite to a bird’s eye view?

- Is the final frame recorded with the camera tilted steeply upwards?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at a worm’s eye angle, looking sharply upward to the sky.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a worm’s eye angle, looking steeply upward.

- A video concluding with a worm’s eye view, capturing the sky or ceiling.

- A sequence that ends with the camera positioned extremely low and pointing up.

- A shot showing the environment from a worm’s eye perspective.

- A video closing with a dramatically low-angle upward tilt.

- A shot where the camera is positioned at ground level and directed upward.

- A video that ends with the camera framing subjects from an extreme low viewpoint.

- A scene that closes with the camera tilted strongly upwards, emphasizing height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['end'] == 'worm_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.camera_angle_info['end'] not in ['worm_eye_angle', 'unknown']</code>

</details>
