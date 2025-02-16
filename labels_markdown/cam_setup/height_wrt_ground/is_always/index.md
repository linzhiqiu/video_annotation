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

- Does the camera remain at an aerial perspective for the entire video?

- Is the camera height consistently high, capturing scenes from above?

- Does the video maintain an elevated aerial viewpoint from start to finish?

- Is the camera positioned at aerial level without transitioning to a lower height?

- Does the video continuously feature an aerial perspective?

- Is the shot composed entirely from a high-altitude viewpoint?

- Does the framing stay at an aerial level without descending?

- Is the video filmed entirely from an elevated aerial position?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains at an aerial level height throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining an aerial perspective from start to finish.

- A shot consistently captured from a high-altitude viewpoint.

- A video where the camera stays at an elevated position.

- A sequence entirely filmed from an aerial level.

- A shot maintaining an aerial perspective without height changes.

- A video where the camera remains above ground at a high altitude.

- A scene consistently framed from an aerial viewpoint.

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
Is the camera positioned at eye level throughout the video, roughly at a person's eye height, above the waist but below overhead level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at eye level for the entire video?

- Is the starting and ending frame taken from an eye-level perspective?

- Does the video maintain a height typical of a standing person’s eyes?

- Is the camera positioned at eye level from start to finish?

- Does the sequence keep an eye-level viewpoint without transitioning?

- Is the video filmed entirely at eye level?

- Does the framing remain above waist height but below overhead for the whole video?

- Is the entire shot positioned at a natural human viewpoint?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at eye level throughout the video, roughly at a person's eye height, above the waist but below overhead level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining an eye-level perspective from start to finish.

- A shot consistently captured at a natural viewing height.

- A video where the camera stays at eye level without changing.

- A sequence entirely framed from an eye-level viewpoint.

- A shot maintaining an eye-level perspective without shifting heights.

- A video where the camera remains at a natural human viewpoint.

- A scene that is consistently framed from an eye-level height.

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
Is the camera positioned at ground level throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at ground level for the entire video?

- Is the starting and ending frame taken from a ground-level perspective?

- Does the video maintain a low viewpoint near the ground surface?

- Is the camera positioned close to the ground from start to finish?

- Does the sequence keep a ground-level viewpoint without transitioning?

- Is the video filmed entirely at ground level?

- Does the framing remain at a near-ground height for the whole video?

- Is the entire shot positioned at a ground-level height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at ground level throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a ground-level perspective from start to finish.

- A shot consistently captured at ground level.

- A video where the camera stays at ground level without changing.

- A sequence entirely framed from a ground-level viewpoint.

- A shot maintaining a low perspective without shifting heights.

- A video where the camera remains just above the ground surface.

- A scene that is consistently framed from a ground-level height.

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
Is the camera positioned at hip level, roughly between knee and waist height, whether or not a human subject is present?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at hip level for the entire video?

- Is the starting and ending frame taken from a hip-level perspective?

- Does the video maintain a height between the hips and knees?

- Is the camera positioned at hip level from start to finish?

- Does the sequence keep a hip-level viewpoint without transitioning?

- Is the video filmed entirely at hip level?

- Does the framing remain at mid-body height for the whole video?

- Is the entire shot positioned at a hip-level height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at hip level throughout the video, roughly between knee and waist height, whether or not a human subject is present.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a hip-level perspective from start to finish.

- A shot consistently captured at hip level.

- A video where the camera stays at hip level without changing.

- A sequence entirely framed from a hip-level viewpoint.

- A shot maintaining a hip-level perspective without shifting heights.

- A video where the camera remains at mid-body height.

- A scene that is consistently framed from a hip-level height.

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
Is the camera positioned at an overhead level throughout the video, positioned above human height but below an aerial view, roughly at second-floor level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain at an overhead level for the entire video?

- Is the starting and ending frame taken from an overhead perspective?

- Does the video maintain a high vantage point but lower than aerial level?

- Is the camera positioned at a height between 1.5 to 3 person-heights above the ground throughout?

- Does the sequence keep an overhead viewpoint from start to finish?

- Is the video filmed entirely at an overhead level without transitioning?

- Does the framing remain above eye level but below aerial for the whole video?

- Is the entire shot positioned at an overhead perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera is positioned at an overhead level throughout the video, positioned above human height but below an aerial view, roughly at second-floor level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining an overhead perspective from start to finish.

- A shot consistently captured from an overhead height.

- A video where the camera stays at an overhead level without changing.

- A sequence entirely framed from a high vantage point but not aerial.

- A shot maintaining an overhead perspective without shifting heights.

- A video where the camera remains above human height but below aerial.

- A scene that is consistently framed from an overhead level.

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
