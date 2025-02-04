# End_with Overview

<details>
<summary><h2>Height Wrt Ground End With Aerial Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_aerial_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned high at an aerial level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at an aerial level?

- Is the final frame taken from an aerial perspective?

- Does the video conclude with a high-altitude shot?

- Is the last shot captured from an aerial view?

- Does the sequence close with an aerial perspective?

- Is the final shot positioned at an aerial level?

- Does the video close with a bird’s-eye view?

- Is the ending frame recorded from a high altitude?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned high at an aerial level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at an aerial level, taken from a high altitude.

- A video concluding with an aerial shot, capturing a wide perspective.

- A sequence that ends with a high-elevation view.

- A shot showing the environment from an elevated aerial position.

- A video closing with a bird’s-eye perspective.

- A shot where the camera is positioned high above the ground.

- A video that ends with a top-down or high-altitude framing.

- A scene that concludes with a drone-like aerial viewpoint.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'aerial_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['aerial_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Eye Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_eye_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera at eye level, roughly at a person's eye height, above the waist but below overhead level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at eye level?

- Is the final frame taken from an eye-level perspective?

- Does the video conclude with a camera height typical of a standing person’s eyes?

- Is the last shot captured at a height similar to a person's eye level?

- Does the sequence close with an eye-level perspective?

- Is the final shot positioned at an eye-level height?

- Does the video close with a camera positioned above waist level but below overhead level?

- Is the ending frame aligned with a natural human viewpoint?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at eye level, approximately at a person's eye height, including any height above waist but below overhead level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at eye level, captured at a natural viewing height.

- A video concluding with an eye-level perspective, maintaining a familiar human viewpoint.

- A sequence that ends with a camera positioned at typical standing eye height.

- A shot showing the environment from a natural eye-level angle.

- A video closing with a straight-on view at eye level.

- A shot where the camera is positioned at a height similar to a person's eyes.

- A video that ends with a perspective slightly above waist height but below overhead.

- A scene that concludes with a balanced, eye-level framing of the environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'eye_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['eye_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Ground Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_ground_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera at ground level, positioned close to the ground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at ground level?

- Is the final frame taken from a ground-level perspective?

- Does the video conclude with a camera height very close to the ground?

- Is the last shot captured from a low viewpoint near the ground surface?

- Does the sequence close with a ground-level perspective?

- Is the final shot positioned at a ground-level height?

- Does the video close with a view where the ground is prominently visible?

- Is the ending frame recorded with the camera positioned right above the ground?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at ground level, positioned close to the ground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at ground level, taken from a very low height.

- A video concluding with a ground-level perspective, where the surface is dominant.

- A sequence that ends with a camera positioned just above the ground.

- A shot showing the environment from a low, near-ground viewpoint.

- A video closing with a perspective that emphasizes the ground surface.

- A shot where the camera is positioned directly above the ground level.

- A video that ends with a ground-skimming camera angle.

- A scene that closes with a close-to-the-ground framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'ground_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['ground_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Hip Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_hip_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at hip level?

- Is the final frame taken from a hip-level perspective?

- Does the video conclude with a camera positioned between waist and knees?

- Is the last shot captured from mid-body height?

- Does the sequence close with a hip-level perspective?

- Is the final shot positioned at a hip-level height?

- Does the video close with a shot slightly lower than eye level?

- Is the ending frame aligned with a mid-body viewpoint?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video end with the camera at hip level, roughly between knee and waist height, whether or not a human subject is present.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at hip level, taken from a mid-body viewpoint.

- A video concluding with a hip-level perspective.

- A sequence that ends with a camera positioned at mid-body height.

- A shot showing the environment from a lower but not ground-level viewpoint.

- A video closing with a perspective positioned between waist and knees.

- A shot where the camera is slightly above ground but lower than eye level.

- A video that ends with a framing that emphasizes mid-body perspective.

- A scene that closes with a hip-level camera position.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'hip_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['hip_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Overhead Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_overhead_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera at an overhead level, above human height but below an aerial view, roughly at second-floor level?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at an overhead level?

- Is the final frame taken from an overhead perspective?

- Does the video conclude with a high vantage point but lower than aerial level?

- Is the last shot captured from a second-floor height or similar?

- Does the sequence close with an overhead view?

- Is the final shot positioned at an overhead level?

- Does the video close with a perspective from above regular human height?

- Is the ending frame recorded from a height between 1.5 to 3 person-heights?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera at an overhead level, above human height but below an aerial view, roughly at second-floor level.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at an overhead level, taken from a high vantage point.

- A video concluding with an overhead perspective, from a second-floor height.

- A sequence that ends with a view between eye level and aerial level.

- A shot showing the environment from a high but not extreme aerial position.

- A video closing with a balanced overhead view.

- A shot where the camera is positioned at 1.5 to 3 person-heights above ground.

- A video that ends with a high but not extreme aerial perspective.

- A scene that closes with an elevated, overhead framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'overhead_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['overhead_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Underwater Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_underwater_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera fully submerged underwater, capturing scenes beneath the water’s surface?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with an underwater perspective?

- Is the final frame taken from below the water’s surface?

- Does the video conclude with the camera positioned underwater?

- Is the last shot captured entirely beneath the waterline?

- Does the sequence close with an underwater viewpoint?

- Is the final shot filmed below the water’s surface?

- Does the video close with the camera fully submerged underwater?

- Is the ending frame positioned entirely beneath the water level?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera fully submerged underwater.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending completely underwater, beneath the surface.

- A video concluding with an underwater perspective, showing submerged scenery.

- A sequence that ends with a camera fully below the waterline.

- A shot showing the underwater environment, taken from beneath the surface.

- A video closing with a scene where the camera is entirely underwater.

- A shot where the camera is submerged and filming below water.

- A video that ends with an underwater perspective without breaking the surface.

- A scene that closes with the camera completely beneath the water’s surface.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'underwater_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['underwater_level', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Ground End With Water Level</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_ground_end_with_water_level</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at water level, where the waterline is clearly visible?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end at water level?

- Is the final frame taken from a water-level perspective?

- Does the video conclude with the camera positioned at the water surface?

- Is the last shot framed with the waterline clearly visible?

- Does the sequence close with a water-level perspective?

- Is the final shot positioned just above the water surface?

- Does the video close with a floating perspective at water level?

- Is the ending frame aligned with the surface of the water?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the camera positioned at water level, where the waterline is clearly visible.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending at water level, where the surface is prominent.

- A video concluding with a perspective positioned just above the water.

- A sequence that ends with a camera floating at the waterline.

- A shot capturing the water surface as a dominant element.

- A video closing with a framing that includes both water and sky.

- A shot where the camera is positioned at the boundary between air and water.

- A video that ends with a steady, water-level viewpoint.

- A scene that concludes with a perspective where the water surface remains clearly visible.

</details>

<h4>🟢 Positive:</h4>
<code>self.height_wrt_ground_info['end'] == 'water_level'</code>

<h4>🔴 Negative:</h4>
<code>self.height_wrt_ground_info['end'] not in ['water_level', 'unknown']</code>

</details>
