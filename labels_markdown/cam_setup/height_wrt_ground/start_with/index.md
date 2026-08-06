# Start_with Overview

<details>
<summary><h2>Height Wrt Ground Start With Aerial Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_aerial_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned high at an aerial level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at an aerial level?

- Is the starting frame taken from an aerial perspective?

- Does the video begin with a high-altitude shot?

- Is the initial shot captured from an aerial view?

- Does the sequence open with an aerial perspective?

- Is the first shot positioned at an aerial level?

- Does the video open with a bird’s-eye view?

- Is the starting frame recorded from a high altitude?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned high at an aerial level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at an aerial level, taken from a high altitude.

- A video beginning with an aerial shot, capturing a wide perspective.

- A sequence that starts with a high-elevation view.

- A shot showing the environment from an elevated aerial position.

- A video opening with a bird’s-eye perspective.

- A shot where the camera is positioned high above the ground.

- A video that starts with a top-down or high-altitude framing.

- A scene that opens with a drone-like aerial viewpoint.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'aerial_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['aerial_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Eye Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_eye_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at eye level (roughly at a person’s eye height, above the waist)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at eye level?

- Is the starting frame taken from an eye-level perspective?

- Does the video begin with a camera height typical of a standing person’s eyes?

- Is the initial shot captured at a height similar to a person's eye level?

- Does the sequence open with an eye-level perspective?

- Is the first shot positioned at an eye-level height?

- Does the video open with a camera positioned above waist level but below overhead level?

- Is the starting frame aligned with a natural human viewpoint?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned at eye level (roughly at a person's eye height, above the waist).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at eye level, captured at a natural viewing height.

- A video beginning with an eye-level perspective, maintaining a familiar human viewpoint.

- A sequence that starts with a camera positioned at typical standing eye height.

- A shot showing the environment from a natural eye-level angle.

- A video opening with a straight-on view at eye level.

- A shot where the camera is positioned at a height similar to a person's eyes.

- A video that starts with a perspective slightly above waist height but below overhead.

- A scene that opens with a balanced, eye-level framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'eye_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['eye_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Ground Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_ground_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at ground level, positioned close to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at ground level?

- Is the starting frame taken from a ground-level perspective?

- Does the video begin with a camera height very close to the ground?

- Is the initial shot captured from a low viewpoint near the ground surface?

- Does the sequence open with a ground-level perspective?

- Is the first shot positioned at a ground-level height?

- Does the video open with a view where the ground is prominently visible?

- Is the starting frame recorded with the camera positioned right above the ground?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at ground level, positioned close to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at ground level, taken from a very low height.

- A video beginning with a ground-level perspective, where the surface is dominant.

- A sequence that starts with a camera positioned just above the ground.

- A shot showing the environment from a low, near-ground viewpoint.

- A video opening with a perspective that emphasizes the ground surface.

- A shot where the camera is positioned directly above the ground level.

- A video that starts with a ground-skimming camera angle.

- A scene that opens with a close-to-the-ground framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'ground_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['ground_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Hip Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_hip_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at hip level?

- Is the starting frame taken from a hip-level perspective?

- Does the video begin with a camera height aligned with a subject's hips or knees?

- Is the initial shot captured from a mid-body height viewpoint?

- Does the sequence open with a hip-level perspective?

- Is the first shot positioned at a hip-level height?

- Does the video open with a perspective from around waist to knee level?

- Is the starting frame recorded from a height typical of a hip-level view?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at hip level, captured from a mid-body viewpoint.

- A video beginning with a hip-level perspective, aligning with a subject’s lower torso.

- A sequence that starts with the camera positioned between waist and knee height.

- A shot showing the environment from a hip-level camera angle.

- A video opening with a viewpoint around a subject's hips or knees.

- A shot where the camera is positioned lower than eye level but above ground level.

- A video that starts with a perspective noticeably below eye level but not at ground level.

- A scene that opens with a balanced framing from a mid-body height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'hip_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['hip_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Overhead Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_overhead_level</code>


<h3>📖 Definition:</h3>
Does the video begin with the camera at an overhead level, above eye level but below aerial (around second-floor height)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at an overhead level?

- Is the starting frame taken from an overhead perspective?

- Does the video begin with a high vantage point but lower than aerial level?

- Is the initial shot captured from a second-floor height or similar?

- Does the sequence open with an overhead view?

- Is the first shot positioned at an overhead level?

- Does the video open with a perspective from above regular human height?

- Is the starting frame recorded from a height between 1.5 to 3 person-heights?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video begins with the camera at an overhead level, above eye level but below aerial (around second-floor height).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video starts with the camera at an overhead level.

- A video beginning with an overhead perspective, from a second-floor height.

- A sequence that starts with a vantage point between eye level and aerial level.

- A video opening with a high view but not an extreme aerial perspective.

- A shot where the camera is positioned at 1.5 to 3 person-heights above ground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'overhead_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['overhead_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Underwater Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_underwater_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera fully submerged underwater?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with an underwater perspective?

- Is the starting frame taken from below the water’s surface?

- Does the video begin with the camera positioned underwater?

- Is the initial shot captured entirely beneath the waterline?

- Does the sequence open with an underwater viewpoint?

- Is the first shot filmed below the water’s surface?

- Does the video open with the camera fully submerged underwater?

- Is the starting frame positioned entirely beneath the water level?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera fully submerged underwater.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting completely underwater, beneath the surface.

- A video beginning with an underwater perspective, showing submerged scenery.

- A sequence that starts with a camera fully below the waterline.

- A shot showing the underwater environment, taken from beneath the surface.

- A video opening with a scene where the camera is entirely underwater.

- A shot where the camera is submerged and filming below water.

- A video that starts with an underwater perspective without breaking the surface.

- A scene that opens with the camera completely beneath the water’s surface.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'underwater_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['underwater_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground Start With Water Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_start_with_water_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera near water level, showing the waterline clearly and not from an aerial view?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start at water level?

- Is the starting frame taken from a water-level perspective?

- Does the video begin with the camera positioned just above the waterline?

- Is the initial shot captured at the surface of the water?

- Does the sequence open with a perspective where the waterline is visible?

- Is the first shot positioned at water level, showing the surrounding water?

- Does the video open with the camera floating just above water?

- Is the starting frame aligned with a perspective just above the water surface?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera positioned near water level, showing the waterline clearly and not from an aerial view.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting at water level, taken from just above the waterline.

- A video beginning with a perspective where the water surface is prominent.

- A sequence that starts with a camera positioned at the water’s edge.

- A shot showing the environment from a viewpoint just above the water.

- A video opening with a scene where the waterline is clearly visible.

- A shot where the camera is placed at water level without submerging.

- A video that starts with a floating camera angle, capturing the water surface.

- A scene that opens with a near-waterline framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'water_level'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] not in ['water_level', 'unknown']</code>

</details>
