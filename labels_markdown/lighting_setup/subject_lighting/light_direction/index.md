# Light_direction Overview

<details>
<summary><h2>Direction Is Ambient Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_ambient_light</code>


<h3>📖 Definition:</h3>
Are all subjects consistently lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the lighting on the subject evenly distributed without a clear direction?

- Does the video feature illumination without a strong directional source?

- Is the subject lit primarily by soft, non-directional ambient light?

- Does the shot lack a dominant light source coming from one direction?

- Is the lighting in the scene diffuse, without strong highlights or shadows?

- Does the subject appear illuminated by scattered or indirect lighting?

- Is the main illumination provided by ambient, environmental light?

- Does the video rely on a soft, uniform light source rather than directional lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently lit with no dominant light direction, as shadows and highlights do not indicate a dominant (or key) light from the side, top, bottom, front, or back.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the subject is lit with soft, ambient lighting.

- A video where the illumination is diffuse without strong highlights.

- A scene featuring non-directional light with an even glow.

- A sequence where scattered or indirect light provides illumination.

- A shot with balanced lighting, lacking a dominant light source.

- A video where no single light direction defines the subject’s appearance.

- A scene relying on ambient illumination rather than focused light.

- A shot where the subject appears naturally lit with no strong shadows.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_ambient_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_ambient_light is False</code>

</details>

<details>
<summary><h2>Direction Is Back Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_back_light</code>


<h3>📖 Definition:</h3>
Are all subjects consistently back-lit by a noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated from behind?

- Does the lighting create a silhouette effect with strong contrast?

- Is the subject primarily lit from the back?

- Does the shot feature backlighting as the dominant illumination?

- Is the subject's front side darker due to backlight emphasis?

- Does the lighting come from behind the subject rather than the front?

- Is the scene primarily defined by a strong backlight?

- Is the main source of illumination positioned behind the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently back-lit by noticeable (or key) light (not just ambient or fill light) coming from the far side, with the light source positioned within a 90-degree angle behind them, facing away from the camera.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The subject is illuminated from behind.

- A video where the subject is lit from the back, creating contrast.

- A scene featuring strong backlighting with silhouetting effects.

- A sequence where backlight defines the subject's appearance.

- A shot highlighting the subject’s edges through backlighting.

- A video where the lighting is primarily positioned behind the subject.

- A scene emphasizing backlight effects with shadowed front areas.

- A shot where the subject's front remains darker due to backlight.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_back_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_back_light is False</code>

</details>

<details>
<summary><h2>Direction Is Bottom Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_bottom_light</code>


<h3>📖 Definition:</h3>
Are all subjects consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated from below, casting shadows upward?

- Does the lighting create upward-facing shadows on the subject?

- Is the scene characterized by light coming from underneath?

- Does the shot feature bottom lighting as the main illumination?

- Is the subject’s face or body partially obscured due to under-lighting?

- Does the video emphasize shadows above the subject’s eyes or chin?

- Is the main source of illumination positioned directly below?

- Is the subject’s form shaped by a strong upward lighting effect?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently illuminated by bottom lighting, with noticeable (or key) light (not just ambient or fill light) coming from below and casting shadows upward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The subject is illuminated from below, casting shadows upward.

- A video where the subject is dramatically lit from underneath.

- A scene featuring eerie bottom lighting contrast.

- A sequence where under-lighting creates an unnatural look on the subject.

- A shot where the subject’s features are shaped by bottom-up light.

- A video where shadows form above the subject due to under-lighting.

- A scene with strong highlights on the subject’s lower face and body.

- A shot where the subject appears unsettling due to strong upward light.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_bottom_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_bottom_light is False</code>

</details>

<details>
<summary><h2>Changing (Temporal) Light Direction</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_complex_changing</code>


<h3>📖 Definition:</h3>
Does the dominant light direction on the subject(s) change over time, as judged from the camera's perspective?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the side of the subject that appears lit shift during the video?

- Does the light source move or change during the shot?

- Does the subject move into a new light zone that changes the directional effect?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The dominant light direction on the subject(s) changes over time, as judged from the camera’s perspective.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the lit side of the subject shifts during the shot.

- A scene where the light source moves or changes, altering the direction.

- A shot where the subject moves into a new light zone, changing the directional effect.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_complex_changing is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_complex_changing is False</code>

</details>

<details>
<summary><h2>Mixed (Spatial) Light Direction</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_complex_contrasting</code>


<h3>📖 Definition:</h3>
Are different parts of the subject, or different subjects, lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are multiple subjects in the same frame lit from different directions?

- Do light sources hit separate regions of the subject from distinct angles at the same time?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- Different parts of the subject, or different subjects, are lit by different dominant light directions simultaneously, with no single direction applying across the entire subject or all subjects in the frame.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with multiple subjects lit from different directions.

- A subject with different regions lit from distinct angles simultaneously.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_complex_contrasting is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_complex_contrasting is False</code>

</details>

<details>
<summary><h2>Mixed (Spatial) + Changing (Temporal) Light Direction</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_complex_others</code>


<h3>📖 Definition:</h3>
Are different parts of the subject (or different subjects) lit by different directions simultaneously, and do these directions also change over time, so the dominant light direction varies both spatially and temporally?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Do different areas get lit from different directions, and those directions change during the video?

- Are multiple subjects each lit from different directions, and their lighting direction shifts over time?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- Different parts of the subject (or different subjects) are lit by different directions simultaneously, and these directions also change over time, so the dominant light direction varies both spatially and temporally.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where different regions are lit from different directions, and those directions change during the video.

- A video with multiple subjects, each lit from different directions, and their lighting direction shifts over time.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_complex_others is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_complex_others is False</code>

</details>

<details>
<summary><h2>Consistent Light Direction</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_consistent</code>


<h3>📖 Definition:</h3>
Is the subject consistently lit with the same light direction throughout the video and uniform across the entire subject's surface?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the light direction remain the same for the entire video?

- Is the direction of light uniform across the subject at all times?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The subject is consistently lit with the same light direction throughout the video and uniform across the entire subject's surface.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the light direction does not change at any point.

- A scene where the subject is always lit from the same direction.

- A shot where the light direction is uniform across the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_consistent is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_consistent is False</code>

</details>

<details>
<summary><h2>Direction Is Front Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_front_light</code>


<h3>📖 Definition:</h3>
Are all subjects consistently front-lit by a noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated from the front?

- Does the lighting create an evenly lit appearance on the subject?

- Is the subject's face or body fully illuminated with minimal shadows?

- Does the shot feature front lighting as the dominant illumination?

- Is the scene characterized by a lack of strong shadows on the subject?

- Is the main source of illumination coming from the front?

- Is the subject’s visibility defined by direct front lighting?

- Does the video showcase the subject clearly due to front lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently front-lit by noticeable (or key) light (not just ambient or fill light) coming from the camera side, with the light source positioned within a 90-degree angle in front of them, extending toward the camera.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The subject is illuminated from the front.

- A video where the subject is evenly lit from the front.

- A scene featuring clear front lighting without harsh shadows.

- A sequence where front light highlights the subject evenly.

- A shot where the subject is fully visible due to front lighting.

- A video where front light minimizes dramatic contrasts.

- A scene where front light provides an evenly distributed glow.

- A shot with balanced illumination from a front-facing light source.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_front_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_front_light is False</code>

</details>

<details>
<summary><h2>Left-Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_left_side</code>


<h3>📖 Definition:</h3>
Are all subjects consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject have a clear left-side light source?

- Is the left side of the subject more illuminated than the right?

- Does the lighting create a visible shadow on the right side of the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the left side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A subject with the left side more brightly lit than the right.

- A scene where the left-side lighting creates a shadow on the right side of the subject.

- A shot where the key light is positioned to the left of the subject from the camera's perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_left_side is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_left_side is False</code>

</details>

<details>
<summary><h2>Right-Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_right_side</code>


<h3>📖 Definition:</h3>
Are all subjects consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject have a clear right-side light source?

- Is the right side of the subject more illuminated than the left?

- Does the lighting create a visible shadow on the left side of the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently illuminated by side lighting, with noticeable (or key) light (not just ambient or fill light) coming from the right side of each subject as seen from the camera, causing one side to appear more lit and the opposite side darker.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A subject with the right side more brightly lit than the left.

- A scene where the right-side lighting creates a shadow on the left side of the subject.

- A shot where the key light is positioned to the right of the subject from the camera's perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_right_side is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_right_side is False</code>

</details>

<details>
<summary><h2>Direction Is Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_side_light</code>


<h3>📖 Definition:</h3>
Is there a noticeable light source consistently illuminating the subject from one side (side lighting) as seen from the camera’s perspective?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated from the side?

- Does the lighting create noticeable highlights on one side of the subject?

- Is the scene characterized by strong light contrast from one direction?

- Does the shot feature a dominant sidelight as the main illumination?

- Is the subject’s face or body partially shadowed due to side lighting?

- Does the video showcase dramatic lighting contrast with sidelight emphasis?

- Is the main source of illumination positioned to the side?

- Is the subject’s form defined by a strong sidelight effect?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- There is a noticeable light source consistently illuminating the subject from one side (side lighting), as seen from the camera’s perspective.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The subject is illuminated from the side, creating strong contrast and shadows on one side.

- A video where the subject is dramatically lit from one direction.

- A scene featuring noticeable side lighting contrast.

- A sequence where side light creates depth and shadow on the subject.

- A shot where the subject’s form is emphasized by sidelight contrast.

- A video where shadows and highlights form due to side illumination.

- A scene with a strong directional light source from the side.

- A shot where the subject’s face or body has strong light-shadow separation.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_side_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_side_light is False</code>

</details>

<details>
<summary><h2>Direction Is Top Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_top_light</code>


<h3>📖 Definition:</h3>
Are all subjects consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated from above, casting shadows downward?

- Does the lighting create downward-facing shadows on the subject?

- Is the scene characterized by highlights on top and shadows below?

- Does the shot feature top lighting as the main illumination?

- Is the subject’s face or body partially obscured due to overhead light?

- Does the video emphasize shadows under the subject’s eyes or chin?

- Is the main source of illumination positioned directly above?

- Is the subject’s form shaped by a strong overhead lighting effect?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- All subjects are consistently illuminated by top lighting, with noticeable (or key) light (not just ambient or fill light) coming from above and casting shadows downward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The subject is illuminated from above, casting shadows downward.

- A video where the subject is dramatically lit from above.

- A scene featuring strong top lighting contrast.

- A sequence where top light creates directional depth on the subject.

- A shot where the subject’s features are shaped by overhead light.

- A video where shadows form beneath the subject due to top lighting.

- A scene with strong highlights on the subject’s head and shoulders.

- A shot where the subject appears sculpted due to strong top-down light.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_top_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_top_light is False</code>

</details>

<details>
<summary><h2>Unclear Light Direction</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_unknown</code>


<h3>📖 Definition:</h3>
Is the lighting direction on the subject unable to be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and light direction that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there no clear and lightable subject (e.g., scenery-only shot)?

- Does the subject change and the light direction also change?

- Is the scene 2D, stylized, or flat-rendered, making light direction uninterpretable?

- Is the light direction too ambiguous to judge?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- Lighting direction on the subject cannot be reliably judged because the video may lack a clear subject lit by external light, lack a subject altogether (e.g., scenery shot), feature both complex subject transitions and light direction that varies across regions or time, or be too stylized or abstract to physically interpret the lighting setup.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with no clear and lightable subject.

- A video where the subject and light direction both change.

- A 2D or stylized scene where light direction cannot be interpreted.

- A shot where light direction is too ambiguous to judge.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.direction_is_unknown is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.direction_is_unknown is False</code>

</details>
