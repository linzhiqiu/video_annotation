# Is_always Overview

<details>
<summary><h2>Camera Angle Is Bird's Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_bird_eye_angle</code>


<h3>📖 Definition:</h3>
Does the camera maintain a bird's eye angle throughout, consistently looking straight down from above?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain a bird's eye perspective throughout?

- Is the camera consistently positioned at a top-down viewpoint?

- Does the video keep the camera looking straight down at the ground?

- Is the shot captured from an overhead, bird's eye perspective throughout?

- Does the sequence maintain a camera position directly above the scene?

- Is the camera consistently positioned in a strict top-down orientation?

- Does the video keep an aerial viewpoint looking directly downward?

- Is the shot recorded from a high, perpendicular angle throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera maintains a bird's eye angle throughout, consistently looking straight down from above.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a strict top-down perspective.

- A video keeping a bird's eye view, directly above the scene.

- A sequence with a consistent overhead camera looking straight down.

- A shot where the environment is viewed from a top-down orientation.

- A video maintaining a high, perpendicular perspective.

- A shot where the camera stays positioned vertically above the ground.

- A video that maintains a fully downward-facing angle.

- A scene that keeps a bird's eye framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'bird_eye_angle' and self.cam_setup.camera_angle_info['end'] == 'bird_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['bird_eye_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['bird_eye_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_high_angle</code>


<h3>📖 Definition:</h3>
Does the camera maintain a high angle throughout, consistently looking downward compared to a level angle but not directly top-down?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain a downward-facing high angle throughout?

- Is the camera consistently positioned at a higher viewpoint, looking down compared to a level angle?

- Does the video keep the camera angled downward but not entirely overhead?

- Is the shot captured from an elevated position throughout, looking slightly down?

- Does the sequence maintain a perspective higher than a level angle but lower than a bird's-eye view?

- Is the camera consistently positioned with a noticeable downward tilt compared to a straight-on view?

- Does the camera keep a view looking downward, but not completely top-down?

- Is the shot recorded from a higher elevation than a neutral level angle throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera maintains a high angle throughout, consistently looking downward compared to a level angle but not directly top-down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a high-angle perspective, looking downward compared to a neutral angle.

- A video keeping an elevated viewpoint, angled downward but not extreme.

- A sequence with a consistent high-angle framing, positioned above level angle.

- A shot where the camera stays higher than a level angle, tilting downward.

- A video maintaining a perspective slightly above normal eye level, looking down.

- A shot where the camera remains positioned at a high angle, but not completely top-down.

- A video that keeps an elevated framing, angled slightly downward.

- A scene that maintains the camera positioned higher than a neutral level shot, tilting downward.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'high_angle' and self.cam_setup.camera_angle_info['end'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['high_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['high_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_level_angle</code>


<h3>📖 Definition:</h3>
Does the camera maintain a level angle parallel to the ground regardless of Dutch angle throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain the camera aligned parallel to the ground?

- Is the camera consistently positioned at a neutral level angle?

- Does the video keep a shot that is neither tilted upward nor downward?

- Is the shot captured from a level perspective throughout, without an angled tilt?

- Does the sequence maintain a camera angle parallel to the ground?

- Is the camera consistently framed at a natural, level viewing angle?

- Does the video keep a shot that has no vertical inclination?

- Is the shot recorded with the camera at a neutral level position throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera maintains a level angle parallel to the ground regardless of Dutch angle throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a neutral level angle, parallel to the ground.

- A video keeping a level perspective, without tilt.

- A sequence with a consistent camera position at a straight-on angle.

- A shot showing a level camera position with no upward or downward tilt.

- A video maintaining a natural, eye-level viewpoint, parallel to the ground.

- A shot where the camera stays level without angling up or down.

- A video that keeps a neutral, parallel-to-ground perspective.

- A scene that maintains the camera set at a balanced level angle.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'level_angle' and self.cam_setup.camera_angle_info['end'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['level_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['level_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_low_angle</code>


<h3>📖 Definition:</h3>
Does the camera maintain a low angle throughout, consistently looking upward compared to a level angle but not directly bottom-up?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain an upward-tilted camera angle?

- Is the camera consistently positioned below a level viewpoint?

- Does the video keep the camera angled upward from a low position?

- Is the shot captured from a perspective looking up throughout?

- Does the sequence maintain a camera angle lower than a level view?

- Is the camera consistently framed from a low vantage point looking up?

- Does the video keep the camera positioned below the main subject or scene?

- Is the shot recorded from a lower-than-normal camera height throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera maintains a low angle throughout, consistently looking upward compared to a level angle but not directly bottom-up.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a low angle, looking upward.

- A video keeping a low-angle perspective.

- A sequence with a consistent camera position below eye level.

- A shot showing the environment from a low vantage point.

- A video maintaining an upward-tilted view.

- A shot where the camera stays positioned at a low height, pointing up.

- A video that keeps an angle looking up at the subject or scene.

- A scene that maintains a low-positioned, upward-facing camera.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'low_angle' and self.cam_setup.camera_angle_info['end'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['low_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['low_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Is Worm Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_is_worm_eye_angle</code>


<h3>📖 Definition:</h3>
Does the camera maintain a worm's eye angle throughout, consistently looking straight up from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain the camera looking straight up?

- Is the camera consistently positioned at a worm's eye perspective?

- Does the video keep an extreme low-angle shot looking upward?

- Is the shot captured from below throughout, with the camera pointing skyward?

- Does the sequence maintain a worm's eye view, looking vertically up?

- Is the camera consistently positioned at the lowest perspective, directed upward?

- Does the video keep an angle opposite to a bird's eye view?

- Is the shot recorded with the camera tilted steeply upwards throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera maintains a worm's eye angle throughout, consistently looking straight up from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a worm's eye angle, looking steeply upward.

- A video keeping a worm's eye view, capturing the sky or ceiling.

- A sequence with a consistent camera position extremely low and pointing up.

- A shot showing the environment from a worm's eye perspective.

- A video maintaining a dramatically low-angle upward tilt.

- A shot where the camera stays positioned at ground level and directed upward.

- A video that keeps the camera framing subjects from an extreme low viewpoint.

- A scene that maintains the camera tilted strongly upwards, emphasizing height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'worm_eye_angle' and self.cam_setup.camera_angle_info['end'] == 'worm_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['worm_eye_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['worm_eye_angle', 'unknown'])</code>

</details>
