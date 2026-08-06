# Is_always Overview

<details>
<summary><h2>Height Wrt Ground Is Aerial Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_aerial_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at an aerial level throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera at an aerial level throughout the video?

- Is the camera positioned high at an aerial level throughout the video?

- Is the camera at a high altitude throughout the video?

- Is the camera capturing an aerial view throughout the video?

- Is the camera positioned at an aerial perspective throughout the video?

- Is the camera at an aerial level height throughout the video?

- Is the camera providing a bird's-eye view throughout the video?

- Is the camera recording from a high altitude throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains at an aerial level height throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintained at an aerial level, taken from a high altitude.

- A video with a consistent aerial shot, capturing a wide perspective.

- A sequence that maintains a high-elevation view.

- A shot showing the environment from an elevated aerial position.

- A video with a consistent bird's-eye perspective.

- A shot where the camera is positioned high above the ground.

- A video that maintains a top-down or high-altitude framing.

- A scene that keeps a drone-like aerial viewpoint.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'aerial_level' and self.cam_setup.height_wrt_ground_info['end'] == 'aerial_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['aerial_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['aerial_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Eye Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_eye_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at eye level throughout the video (roughly at a person's eye height, above the waist)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera at eye level throughout the video?

- Is the camera positioned at an eye-level perspective throughout the video?

- Is the camera at a height typical of a standing person's eyes throughout the video?

- Is the camera at a height similar to a person's eye level throughout the video?

- Is the camera maintaining an eye-level perspective throughout the video?

- Is the camera at an eye-level height throughout the video?

- Is the camera positioned above waist level but below overhead level throughout the video?

- Is the camera aligned with a natural human viewpoint throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at eye level throughout the video (roughly at a person's eye height, above the waist).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintained at eye level, captured at a natural viewing height.

- A video with a consistent eye-level perspective, maintaining a familiar human viewpoint.

- A sequence that maintains a camera position at typical standing eye height.

- A shot showing the environment from a natural eye-level angle.

- A video with a consistent straight-on view at eye level.

- A shot where the camera is positioned at a height similar to a person's eyes.

- A video that maintains a perspective slightly above waist height but below overhead.

- A scene that keeps a balanced, eye-level framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'eye_level' and self.cam_setup.height_wrt_ground_info['end'] == 'eye_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['eye_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['eye_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Ground Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_ground_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at ground level throughout the video, positioned close to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera at ground level throughout the video?

- Is the camera positioned very close to the ground throughout the video?

- Is the camera at a height just above the ground throughout the video?

- Is the camera at a height similar to ground level throughout the video?

- Is the camera maintaining a ground-level perspective throughout the video?

- Is the camera at a ground-level height throughout the video?

- Is the camera positioned almost touching the ground throughout the video?

- Is the camera aligned with the ground surface throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at ground level throughout the video, positioned close to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintained at ground level, captured very close to the ground.

- A video with a consistent ground-level perspective, maintaining a low viewpoint.

- A sequence that maintains a camera position just above the ground.

- A shot showing the environment from a ground-level angle.

- A video with a consistent view at ground level.

- A shot where the camera is positioned almost touching the ground.

- A video that maintains a perspective very close to the ground.

- A scene that keeps a balanced, ground-level framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'ground_level' and self.cam_setup.height_wrt_ground_info['end'] == 'ground_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['ground_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['ground_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Hip Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_hip_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera at hip level throughout the video?

- Is the camera positioned at a hip-level perspective throughout the video?

- Is the camera at a height typical of a person's hips throughout the video?

- Is the camera at a height similar to a person's hip level throughout the video?

- Is the camera maintaining a hip-level perspective throughout the video?

- Is the camera at a hip-level height throughout the video?

- Is the camera positioned below eye level but above ground level throughout the video?

- Is the camera aligned with a typical hip height throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintained at hip level, captured at a typical hip height.

- A video with a consistent hip-level perspective, maintaining a familiar hip-height viewpoint.

- A sequence that maintains a camera position at typical hip height.

- A shot showing the environment from a hip-level angle.

- A video with a consistent view at hip level.

- A shot where the camera is positioned at a height similar to a person's hips.

- A video that maintains a perspective below eye level but above ground.

- A scene that keeps a balanced, hip-level framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'hip_level' and self.cam_setup.height_wrt_ground_info['end'] == 'hip_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['hip_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['hip_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Overhead Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_overhead_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at an overhead level throughout the video, above eye level but below aerial (around second-floor height)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera at an overhead level throughout the video?

- Is the camera positioned at an overhead level throughout the video?

- Is the camera at a high vantage point but lower than aerial level throughout the video?

- Is the camera at a second-floor height or similar throughout the video?

- Is the camera maintaining an overhead view throughout the video?

- Is the camera at an overhead level height throughout the video?

- Is the camera positioned from above regular human height throughout the video?

- Is the camera at a height between 1.5 to 3 person-heights throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at an overhead level throughout the video, above eye level but below aerial (around second-floor height).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintained at an overhead level, taken from a second-floor height.

- A video with a consistent overhead perspective, from a second-floor height.

- A sequence that maintains a vantage point between eye level and aerial level.

- A shot showing the environment from a high but not extreme aerial position.

- A video with a consistent high view but not an extreme aerial perspective.

- A shot where the camera is positioned at 1.5 to 3 person-heights above ground.

- A video that maintains a high viewpoint without reaching aerial height.

- A scene that keeps a balanced overhead framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'overhead_level' and self.cam_setup.height_wrt_ground_info['end'] == 'overhead_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['overhead_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['overhead_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Underwater Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_underwater_level</code>


<h3>📖 Definition:</h3>
Is the camera fully submerged underwater throughout the video, capturing scenes beneath the water’s surface?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain underwater for the entire video?

- Is the starting and ending frame taken from an underwater perspective?

- Does the video maintain a fully submerged viewpoint?

- Is the camera positioned below the water surface from start to finish?

- Does the sequence keep an underwater perspective throughout?

- Is the video filmed entirely beneath the water’s surface?

- Does the framing remain completely submerged underwater for the whole video?

- Is the entire shot positioned below the water level without transitioning above?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is fully submerged underwater throughout the video, capturing scenes beneath the water’s surface.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining an underwater perspective from start to finish.

- A shot consistently captured beneath the water surface.

- A video where the camera stays underwater without surfacing.

- A sequence entirely framed from an underwater viewpoint.

- A shot maintaining a submerged perspective without shifting heights.

- A video where the camera remains below the water surface.

- A scene that is consistently framed from an underwater height.

- A shot where the camera stays beneath the water for the entire duration.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'underwater_level' and self.cam_setup.height_wrt_ground_info['end'] == 'underwater_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['underwater_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['underwater_level', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Ground Is Water Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_is_water_level</code>


<h3>📖 Definition:</h3>
Is the camera positioned at water level throughout the video, above the water surface with the waterline clearly visible?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at water level for the entire video?

- Is the starting and ending frame taken from a water-level perspective?

- Does the video maintain a height at the surface of the water?

- Is the camera positioned at water level from start to finish?

- Does the sequence keep a water-level viewpoint without transitioning?

- Is the video filmed entirely at water level?

- Does the framing remain just above the water surface for the whole video?

- Is the entire shot positioned at a water-level height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at water level throughout the video, above the water surface with the waterline clearly visible.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a water-level perspective from start to finish.

- A shot consistently captured at water level.

- A video where the camera stays at water level without changing.

- A sequence entirely framed from a water-level viewpoint.

- A shot maintaining a near-water perspective without shifting heights.

- A video where the camera remains just above the water surface.

- A scene that is consistently framed from a water-level height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_ground_info['start'] == 'water_level' and self.cam_setup.height_wrt_ground_info['end'] == 'water_level'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_ground_info['start'] in ['water_level', 'unknown'] and self.cam_setup.height_wrt_ground_info['end'] in ['water_level', 'unknown'])</code>

</details>
