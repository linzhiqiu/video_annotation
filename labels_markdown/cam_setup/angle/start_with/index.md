# Start_with Overview

<details>
<summary><h2>Camera Angle Start With Bird's Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_start_with_bird_eye_angle</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned at a bird's eye angle, offering a top-down view directly looking down at the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a bird's eye perspective?

- Is the starting frame taken from a top-down viewpoint?

- Does the video begin with the camera looking straight down at the ground?

- Is the initial shot captured from an overhead, bird's eye perspective?

- Does the sequence open with a shot where the camera is directly above the scene?

- Is the first shot positioned in a strict top-down orientation?

- Does the video open with an aerial viewpoint looking directly downward?

- Is the starting frame recorded from a high, perpendicular angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned at a bird's eye angle, looking directly downward at the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting from a strict top-down perspective.

- A video beginning with a bird's eye view, directly above the scene.

- A sequence that starts with an overhead camera looking straight down.

- A shot where the environment is captured from a top-down orientation.

- A video opening with a high, perpendicular perspective.

- A shot where the camera is positioned vertically above the ground.

- A video that starts with a fully downward-facing angle.

- A scene that opens with a bird's eye framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'bird_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.camera_angle_info['start'] not in ['bird_eye_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle Start With High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_start_with_high_angle</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a downward-facing high angle?

- Is the starting frame taken from a higher viewpoint, looking down compared to a level angle?

- Does the video begin with the camera angled downward but not entirely overhead?

- Is the initial shot captured from an elevated position, looking slightly down?

- Does the sequence open with a perspective higher than a level angle but lower than a bird’s-eye view?

- Is the first shot positioned with a noticeable downward tilt compared to a straight-on view?

- Does the video open with a view looking downward, but not completely top-down?

- Is the starting frame recorded from a higher elevation than a neutral level angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned at a high angle, tilted downward compared to a level angle but not directly top-down.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting from a high-angle perspective, looking downward compared to a neutral angle.

- A video beginning with an elevated viewpoint, angled downward but not extreme.

- A sequence that starts with a high-angle framing, positioned above level angle.

- A shot where the camera is higher than a level angle, tilting downward.

- A video opening with a perspective slightly above normal eye level, looking down.

- A shot where the camera is positioned at a high angle, but not completely top-down.

- A video that starts with an elevated framing, angled slightly downward.

- A scene that opens with the camera positioned higher than a neutral level shot, tilting downward.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.camera_angle_info['start'] not in ['high_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle Start With Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_start_with_level_angle</code>


<h3>📖 Definition:</h3>
Does the video start with level angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with level angle?

- Is the starting frame showing level angle?

- Does the video start using level angle?

- Is the initial shot at level angle?

- Does the sequence start with level angle?

- Is the first shot at level angle?

- Does the video open with level angle?

- Is the starting frame at level angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that starts with level angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with level angle.

- A video starting at level angle.

- A sequence beginning with level angle.

- A shot initially at level angle.

- A video opening with level angle.

- A shot starting at level angle.

- A video beginning with level angle.

- A sequence starting at level angle.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.camera_angle_info['start'] not in ['level_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle Start With Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_start_with_low_angle</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with an upward-tilted camera angle?

- Is the starting frame positioned below a level viewpoint?

- Does the video begin with the camera angled upward from a low position?

- Is the initial shot taken from a perspective looking up?

- Does the sequence open with the camera angled lower than a level view?

- Is the first shot framed from a low vantage point looking up?

- Does the video open with the camera positioned below the main subject or scene?

- Is the starting frame captured from a lower-than-normal camera height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned at a low angle, angled upward relative to a level perspective but not directly from below.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at a low angle, looking upward.

- A video beginning with a low-angle perspective.

- A sequence that starts with the camera positioned below eye level.

- A shot showing the environment from a low vantage point.

- A video opening with an upward-tilted view.

- A shot where the camera is positioned at a low height, pointing up.

- A video that starts with an angle looking up at the subject or scene.

- A scene that opens with a low-positioned, upward-facing camera.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.camera_angle_info['start'] not in ['low_angle', 'unknown']</code>

</details>

<details>
<summary><h2>Camera Angle Start With Worm Eye Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_start_with_worm_eye_angle</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned at a worm’s eye angle, looking sharply upward to the sky?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with the camera looking straight up?

- Is the starting frame positioned at a worm’s eye perspective?

- Does the video begin with an extreme low-angle shot looking upward?

- Is the initial shot captured from below, with the camera pointing skyward?

- Does the sequence open with a worm’s eye view, looking vertically up?

- Is the first shot taken from the lowest perspective, directed upward?

- Does the video open with an angle opposite to a bird’s eye view?

- Is the starting frame recorded with the camera tilted steeply upwards?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned at a worm’s eye angle, looking sharply upward to the sky.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at a worm’s eye angle, looking steeply upward.

- A video beginning with a worm’s eye view, capturing the sky or ceiling.

- A sequence that starts with the camera positioned extremely low and pointing up.

- A shot showing the environment from a worm’s eye perspective.

- A video opening with a dramatically low-angle upward tilt.

- A shot where the camera is positioned at ground level and directed upward.

- A video that starts with the camera framing subjects from an extreme low viewpoint.

- A scene that opens with the camera tilted strongly upwards, emphasizing height.

</details>

<h4>🟢 Positive:</h4>
<code>self.camera_angle_info['start'] == 'worm_eye_angle'</code>

<h4>🔴 Negative:</h4>
<code>self.camera_angle_info['start'] not in ['worm_eye_angle', 'unknown']</code>

</details>
