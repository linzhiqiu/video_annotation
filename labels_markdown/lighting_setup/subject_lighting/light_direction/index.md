# Light_direction Overview

<details>
<summary><h2>Direction Is Ambient Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_ambient_light</code>


<h3>📖 Definition:</h3>
Is the subject illuminated with soft, ambient light?

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

- The subject is illuminated with soft, ambient light.

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
<code>self.lighting_setup.subject_ambient_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_ambient_light is False</code>

</details>

<details>
<summary><h2>Direction Is Back Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_back_light</code>


<h3>📖 Definition:</h3>
Is the primary light source positioned behind the subject?

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

- A shot where the primary light source is behind the subject.

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
<code>self.lighting_setup.subject_back_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_back_light is False</code>

</details>

<details>
<summary><h2>Direction Is Bottom Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_bottom_light</code>


<h3>📖 Definition:</h3>
Is the primary light source positioned below the subject?

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

- A shot where the primary light source is positioned below.

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
<code>self.lighting_setup.subject_bottom_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_bottom_light is False</code>

</details>

<details>
<summary><h2>Direction Is Front Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_front_light</code>


<h3>📖 Definition:</h3>
Is the primary light source positioned in front of the subject?

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

- A shot where the primary light source is in front of the subject.

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
<code>self.lighting_setup.subject_front_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_front_light is False</code>

</details>

<details>
<summary><h2>Direction Is Rear-Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_rear_side</code>


<h3>📖 Definition:</h3>
Is the subject illuminated from a combination of back and side lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the primary light source come from behind and slightly to the side of the subject?

- Is the subject lit from a rear-side angle, creating strong contrast?

- Does the lighting emphasize both back and side illumination on the subject?

- Is there rim lighting from behind while also partially lighting the side of the subject?

- Does the subject receive directional lighting from both the back and the side?

- Is the main illumination positioned between backlight and sidelight?

- Does the shot feature a blend of back and side lighting on the subject?

- Is the subject framed with lighting that wraps from the rear and the side?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The subject is illuminated with a combination of back and side lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit from both behind and the side.

- A shot featuring strong directional lighting from a rear-side angle.

- A sequence where backlight and sidelight work together to shape the subject.

- A video where the lighting creates rim highlights while illuminating the side.

- A scene where the primary light source is positioned between back and side.

- A subject illuminated with a mix of back and side lighting for depth.

- A shot emphasizing contrast with both rear and side illumination.

- A composition using a lighting blend between back and side sources.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_back_light is True and self.lighting_setup.subject_side_light is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.lighting_setup.subject_back_light is True and self.lighting_setup.subject_side_light is True)</code>

</details>

<details>
<summary><h2>Direction Is Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_side_light</code>


<h3>📖 Definition:</h3>
Is the primary light source positioned to the side of the subject?

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

- A shot where the primary light source is positioned to the side of the subject.

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
<code>self.lighting_setup.subject_side_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_side_light is False</code>

</details>

<details>
<summary><h2>Direction Is Top Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_top_light</code>


<h3>📖 Definition:</h3>
Is the primary light source positioned above the subject?

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

- A shot where the primary light source is positioned overhead.

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
<code>self.lighting_setup.subject_top_light is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_top_light is False</code>

</details>

<details>
<summary><h2>Direction Is Top-Side Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>direction_is_top_side</code>


<h3>📖 Definition:</h3>
Is the subject illuminated from a combination of top and side lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the primary light source come from above and slightly to the side of the subject?

- Is the subject lit from a top-side angle, creating strong directional contrast?

- Does the lighting emphasize both top and side illumination on the subject?

- Is there overhead lighting while also partially lighting the side of the subject?

- Does the subject receive directional lighting from both above and the side?

- Is the main illumination positioned between toplight and sidelight?

- Does the shot feature a blend of top and side lighting on the subject?

- Is the subject framed with lighting that wraps from the top and the side?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The subject is illuminated with a combination of top and side lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit from both above and the side.

- A shot featuring strong directional lighting from a top-side angle.

- A sequence where toplight and sidelight work together to shape the subject.

- A video where the lighting creates depth using overhead and side illumination.

- A scene where the primary light source is positioned between top and side.

- A subject illuminated with a mix of top and side lighting for a dramatic effect.

- A shot emphasizing contrast with both overhead and side illumination.

- A composition using a lighting blend between top and side sources.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_top_light is True and self.lighting_setup.subject_side_light is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.lighting_setup.subject_top_light is True and self.lighting_setup.subject_side_light is True)</code>

</details>
