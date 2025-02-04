# Is_always Overview

<details>
<summary><h2>Camera Angle Is Bird Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_bird_eye_angle</code>


<h3>📖 Definition:</h3>
Is the camera positioned at a bird’s eye angle throughout the video, looking directly downward at the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at a bird’s eye angle for the entire video?

- Is the starting and ending frame taken from a bird’s eye perspective?

- Does the video maintain an extreme high-angle, looking downward?

- Is the camera positioned directly overhead from start to finish?

- Does the sequence keep a top-down perspective throughout?

- Is the video filmed entirely at a bird’s eye angle without changing?

- Does the framing stay at an overhead viewpoint for the whole video?

- Is the entire video shot with a camera looking straight down?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at a bird’s eye angle throughout the video, looking directly downward at the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a bird’s eye perspective from start to finish.

- A shot consistently captured from a top-down angle.

- A video where the camera stays at an overhead position without changing.

- A sequence entirely framed from a high, downward perspective.

- A shot maintaining a bird’s eye view without shifting angles.

- A video where the camera remains above, looking straight down.

- A scene consistently framed from a bird’s eye perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'bird_eye_angle' and self.camera_angle_info['end'] == 'bird_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.camera_angle_info['start'] in ['bird_eye_angle', 'unknown'] and self.camera_angle_info['end'] in ['bird_eye_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_high_angle</code>


<h3>📖 Definition:</h3>
Is the camera positioned at a high angle throughout the video, looking down at the scene but not completely top-down?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at a high angle for the entire video?

- Is the starting and ending frame taken from a downward-tilted perspective?

- Does the video maintain a high vantage point from start to finish?

- Is the camera positioned slightly above level angle throughout?

- Does the sequence keep a high-angle perspective the whole time?

- Is the video filmed entirely at a high angle without changing?

- Does the framing stay at an elevated viewpoint for the whole video?

- Is the entire video shot with the camera angled downward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at a high angle throughout the video, looking down at the scene but not completely top-down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a high-angle perspective from start to finish.

- A shot consistently captured from a slightly downward-tilted angle.

- A video where the camera stays at an elevated position without changing.

- A sequence entirely framed from a high-angle viewpoint.

- A shot maintaining a high perspective without shifting angles.

- A video where the camera remains angled downward throughout.

- A scene consistently framed from a high perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'high_angle' and self.camera_angle_info['end'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.camera_angle_info['start'] in ['high_angle', 'unknown'] and self.camera_angle_info['end'] in ['high_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_level_angle</code>


<h3>📖 Definition:</h3>
Is the camera positioned at a level angle throughout the video, parallel to the ground regardless of Dutch angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at a level angle for the entire video?

- Is the starting and ending frame taken from a straight-on perspective?

- Does the video maintain a neutral camera angle throughout?

- Is the camera positioned parallel to the ground for the entire duration?

- Does the sequence keep a level viewpoint from start to finish?

- Is the video filmed entirely at a level angle without changing?

- Does the framing remain neutral and parallel to the ground?

- Is the entire video shot at a flat horizon level?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains at a level angle throughout the video, parallel to the ground regardless of Dutch angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a level perspective from start to finish.

- A shot consistently captured from a straight-on angle.

- A video where the camera stays at a neutral position without tilting.

- A sequence entirely framed at a level viewpoint.

- A shot maintaining a level angle without shifting.

- A video where the camera remains flat and parallel to the ground.

- A scene consistently framed at a level perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'level_angle' and self.camera_angle_info['end'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.camera_angle_info['start'] in ['level_angle', 'unknown'] and self.camera_angle_info['end'] in ['level_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_low_angle</code>


<h3>📖 Definition:</h3>
Is the camera positioned at a low angle throughout the video, looking upward from a lower perspective but not directly from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at a low angle for the entire video?

- Is the starting and ending frame taken from an upward-facing perspective?

- Does the video maintain a low vantage point from start to finish?

- Is the camera positioned slightly below level angle throughout?

- Does the sequence keep a low-angle perspective the whole time?

- Is the video filmed entirely at a low angle without changing?

- Does the framing stay at an upward viewpoint for the whole video?

- Is the entire video shot with the camera angled slightly upward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at a low angle throughout the video, looking upward from a lower perspective but not directly from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a low-angle perspective from start to finish.

- A shot consistently captured from a slightly upward-tilted angle.

- A video where the camera stays at a low position without changing.

- A sequence entirely framed from a low-angle viewpoint.

- A shot maintaining a low perspective without shifting angles.

- A video where the camera remains angled upward throughout.

- A scene consistently framed from a low perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'low_angle' and self.camera_angle_info['end'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.camera_angle_info['start'] in ['low_angle', 'unknown'] and self.camera_angle_info['end'] in ['low_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Worm Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_worm_eye_angle</code>


<h3>📖 Definition:</h3>
Is the camera positioned at a worm’s eye angle throughout the video, looking sharply upward to the sky?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at a worm’s eye angle for the entire video?

- Is the starting and ending frame taken from an extreme low-angle perspective?

- Does the video maintain an upward-facing camera position throughout?

- Is the camera positioned extremely low and directed sharply upward from start to finish?

- Does the sequence keep a worm’s eye viewpoint the whole time?

- Is the video filmed entirely at a worm’s eye angle without changing?

- Does the framing stay at a low-angle perspective for the whole video?

- Is the entire video shot with the camera pointed significantly upward?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains at a worm’s eye angle throughout the video, looking sharply upward to the sky.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a worm’s eye perspective from start to finish.

- A shot consistently captured from an extreme low-angle viewpoint.

- A video where the camera stays at a worm’s eye position without tilting away.

- A sequence entirely framed from a worm’s eye perspective.

- A shot maintaining an extreme low angle without shifting.

- A video where the camera remains angled steeply upward throughout.

- A scene consistently framed from a worm’s eye perspective, emphasizing height.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'worm_eye_angle' and self.camera_angle_info['end'] == 'worm_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.camera_angle_info['start'] in ['worm_eye_angle', 'unknown'] and self.camera_angle_info['end'] in ['worm_eye_angle', 'unknown'])</code>

</details>
