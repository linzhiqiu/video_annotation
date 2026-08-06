# End_with Overview

<details>
<summary><h2>Camera Angle End With Bird's Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_end_with_bird_eye_angle</code>


<h3>📖 Definition:</h3>
Does the video end with the camera at a bird's eye angle, looking straight down from above?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with a bird's eye perspective?

- Is the final frame taken from a top-down viewpoint?

- Does the video finish with the camera looking straight down at the ground?

- Is the ending shot captured from an overhead, bird's eye perspective?

- Does the sequence close with a shot where the camera is directly above the scene?

- Is the last shot positioned in a strict top-down orientation?

- Does the video conclude with an aerial viewpoint looking directly downward?

- Is the ending frame recorded from a high, perpendicular angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at a bird's eye angle, looking straight down from above.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending from a strict top-down perspective.

- A video concluding with a bird's eye view, directly above the scene.

- A sequence that ends with an overhead camera looking straight down.

- A shot where the environment is captured from a top-down orientation.

- A video closing with a high, perpendicular perspective.

- A shot where the camera is positioned vertically above the ground.

- A video that ends with a fully downward-facing angle.

- A scene that closes with a bird's eye framing of the environment.

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
Does the video end with the camera at a high angle, looking downward compared to a level angle but not directly top-down?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with a downward-facing high angle?

- Is the final frame taken from a higher viewpoint, looking down compared to a level angle?

- Does the video finish with the camera angled downward but not entirely overhead?

- Is the ending shot captured from an elevated position, looking slightly down?

- Does the sequence close with a perspective higher than a level angle but lower than a bird's-eye view?

- Is the last shot positioned with a noticeable downward tilt compared to a straight-on view?

- Does the video conclude with a view looking downward, but not completely top-down?

- Is the ending frame recorded from a higher elevation than a neutral level angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at a high angle, looking downward compared to a level angle but not directly top-down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending from a high-angle perspective, looking downward compared to a neutral angle.

- A video concluding with an elevated viewpoint, angled downward but not extreme.

- A sequence that ends with a high-angle framing, positioned above level angle.

- A shot where the camera is higher than a level angle, tilting downward.

- A video closing with a perspective slightly above normal eye level, looking down.

- A shot where the camera is positioned at a high angle, but not completely top-down.

- A video that ends with an elevated framing, angled slightly downward.

- A scene that closes with the camera positioned higher than a neutral level shot, tilting downward.

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
Does the video end with the camera at a level angle, parallel to the ground regardless of Dutch angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera aligned parallel to the ground?

- Is the final frame at a neutral level angle?

- Does the video finish with a shot that is neither tilted upward nor downward?

- Is the ending shot taken from a level perspective, without an angled tilt?

- Does the sequence close with a camera angle parallel to the ground?

- Is the last shot framed at a natural, level viewing angle?

- Does the video conclude with a shot that has no vertical inclination?

- Is the ending frame recorded with the camera at a neutral level position?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at a level angle, parallel to the ground regardless of Dutch angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a neutral level angle, parallel to the ground.

- A video concluding with a level perspective, without tilt.

- A sequence that ends with a camera positioned at a straight-on angle.

- A shot showing a level camera position with no upward or downward tilt.

- A video closing with a natural, eye-level viewpoint, parallel to the ground.

- A shot where the camera remains level without angling up or down.

- A video that ends with a neutral, parallel-to-ground perspective.

- A scene that closes with the camera set at a balanced level angle.

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
Does the video end with the camera at a low angle, looking upward compared to a level angle but not directly from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with an upward-tilted camera angle?

- Is the final frame positioned below a level viewpoint?

- Does the video finish with the camera angled upward from a low position?

- Is the ending shot taken from a perspective looking up?

- Does the sequence close with the camera angled lower than a level view?

- Is the last shot framed from a low vantage point looking up?

- Does the video conclude with the camera positioned below the main subject or scene?

- Is the ending frame captured from a lower-than-normal camera height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at a low angle, looking upward compared to a level angle but not directly from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a low angle, looking upward.

- A video concluding with a low-angle perspective.

- A sequence that ends with the camera positioned below eye level.

- A shot showing the environment from a low vantage point.

- A video closing with an upward-tilted view.

- A shot where the camera is positioned at a low height, pointing up.

- A video that ends with an angle looking up at the subject or scene.

- A scene that closes with a low-positioned, upward-facing camera.

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
Does the video end with the camera at a worm's eye angle, looking straight up from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera looking straight up?

- Is the final frame positioned at a worm's eye perspective?

- Does the video finish with an extreme low-angle shot looking upward?

- Is the ending shot captured from below, with the camera pointing skyward?

- Does the sequence close with a worm's eye view, looking vertically up?

- Is the last shot taken from the lowest perspective, directed upward?

- Does the video conclude with an angle opposite to a bird's eye view?

- Is the ending frame recorded with the camera tilted steeply upwards?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at a worm's eye angle, looking straight up from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at a worm's eye angle, looking steeply upward.

- A video concluding with a worm's eye view, capturing the sky or ceiling.

- A sequence that ends with the camera positioned extremely low and pointing up.

- A shot showing the environment from a worm's eye perspective.

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
