# Light_contrast Overview

<details>
<summary><h2>Light Contrast Ratio on Subject Is Complex</h2></summary>


<h3>🔵 Label Name:</h3>
<code>contrast_is_complex</code>


<h3>📖 Definition:</h3>
Is the light contrast ratio on the subject complex, due to significant lighting changes, camera movement, or subject changes?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject’s lighting contrast vary significantly due to lighting shifts or movement?

- Is the contrast ratio inconsistent because of dynamic lighting conditions?

- Does the lighting on the subject change as the scene progresses?

- Is the contrast affected by camera motion or subject movement?

- Does the subject transition between different lighting conditions?

- Does the video feature lighting where contrast is not stable due to subject or scene changes?

- Is the subject’s visibility affected by fluctuating lighting contrast?

- Does the shot include multiple contrast conditions across different frames?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The light contrast ratio on the subject is complex, varying due to lighting changes, camera motion, or subject changes.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject’s contrast changes because of lighting adjustments or scene shifts.

- A scene where contrast fluctuates due to varying illumination conditions.

- A shot where the subject’s contrast level is affected by camera movement.

- A video where lighting contrast alters due to subject transitions.

- A sequence where different lighting setups impact the contrast ratio.

- A shot featuring changing contrast on the subject due to environmental or compositional shifts.

- A video where the contrast on the subject is inconsistent over time.

- A scene where contrast conditions change dynamically throughout the video.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio in ['complex_changing']</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['complex_changing', 'unknown']</code>

</details>

<details>
<summary><h2>Light Contrast Ratio on Subject Is High</h2></summary>


<h3>🔵 Label Name:</h3>
<code>contrast_is_high</code>


<h3>📖 Definition:</h3>
Does the lighting on the subject have a high contrast ratio, where lit areas are significantly brighter than shadowed areas (1:8 or above)?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is it a low-key lighting on the subject with a high contrast ratio?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject’s lighting feature a strong difference between highlights and shadows?

- Is the subject illuminated in a way that creates dramatic contrast?

- Does the subject’s lighting result in deep shadows and bright highlights?

- Is there strong separation between lit and shadowed areas on the subject?

- Does the lighting create bold, well-defined shadows on the subject?

- Is the subject shaped by high-contrast lighting effects?

- Does the video feature high contrast lighting on the subject?

- Is the subject’s visibility defined by stark lighting differences?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The lighting on the subject has a high contrast ratio (1:8 or above), creating strong separation between highlights and shadows.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit with high contrast, featuring strong highlights and deep shadows.

- A scene where the subject’s lighting produces dramatic visual contrast.

- A shot where the lighting on the subject results in sharply defined shadows.

- A video where the subject is illuminated with bold, high-contrast lighting.

- A sequence where the subject appears well-defined due to intense lighting contrast.

- A shot featuring a subject with bright highlights and deep, crisp shadows.

- A video where high contrast lighting enhances the subject’s form.

- A scene that emphasizes the subject through strong lighting contrast.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio == 'high_contrast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['high_contrast', 'unknown', 'complex_changing']</code>

</details>

<details>
<summary><h2>Light Contrast Ratio on Subject Is Minimal</h2></summary>


<h3>🔵 Label Name:</h3>
<code>contrast_is_minimal</code>


<h3>📖 Definition:</h3>
Is there a flat lighting on the subject with minimal contrast, where lit and shadowed areas appear nearly the same (1:1 to 1:2)?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is it a high-key lighting on the subject with minimal contrast?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject’s lighting feature little to no visible shadowing?

- Is the subject illuminated with very even lighting and no strong highlights?

- Does the lighting on the subject create a flat, uniform appearance?

- Is the separation between lit and shadowed areas on the subject barely noticeable?

- Does the lighting create a soft, nearly shadowless effect on the subject?

- Is the subject shaped by very low contrast lighting?

- Does the video feature lighting where the subject has no strong shadows?

- Is the subject’s visibility defined by flat, even lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The lighting on the subject has minimal contrast (1:1 to 1:2), creating a flat lighting effect.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit with minimal contrast, appearing evenly illuminated.

- A scene where the subject’s lighting lacks strong highlights or shadows.

- A shot where the lighting on the subject results in a flat, even look.

- A video where the subject is illuminated with almost no shadowing.

- A sequence where the subject appears with a soft, uniform brightness.

- A shot featuring a subject with little to no visible shading.

- A video where even lighting minimizes shadow depth.

- A scene that reduces contrast for a smooth, flat-lit appearance.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio == 'minimal_contrast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['minimal_contrast', 'unknown', 'complex_changing']</code>

</details>

<details>
<summary><h2>Light Contrast Ratio on Subject Is Normal</h2></summary>


<h3>🔵 Label Name:</h3>
<code>contrast_is_normal</code>


<h3>📖 Definition:</h3>
Does the lighting on the subject have a normal contrast ratio, where lit and shadowed areas differ slightly (1:2 to 1:8)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject’s lighting feature soft and natural contrast?

- Is the subject illuminated with a moderate difference between highlights and shadows?

- Does the lighting on the subject create subtle but visible shadowing?

- Is the separation between lit and shadowed areas on the subject balanced?

- Does the lighting create a natural, gentle contrast on the subject?

- Is the subject shaped by lighting that is neither too harsh nor too flat?

- Does the video feature well-balanced lighting on the subject?

- Is the subject’s visibility defined by moderate lighting differences?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The lighting on the subject has a normal contrast ratio (1:2 to 1:8), creating a balanced separation between highlights and shadows.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit with normal contrast, featuring soft and balanced highlights and shadows.

- A scene where the subject’s lighting appears natural and evenly distributed.

- A shot where the lighting on the subject results in gentle, moderate shadows.

- A video where the subject is illuminated with soft, natural contrast.

- A sequence where the subject appears well-defined without extreme contrast.

- A shot featuring a subject with visible but subtle shadowing.

- A video where balanced lighting enhances the subject’s form without harshness.

- A scene that maintains a natural, moderate contrast on the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio == 'normal_contrast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['normal_contrast', 'unknown', 'complex_changing']</code>

</details>

<details>
<summary><h2>High-Key Lighting</h2></summary>


<h3>🔵 Label Name:</h3>
<code>high_key_lighting</code>


<h3>📖 Definition:</h3>
Is the lighting on the subject high-key, featuring minimal contrast where lit and shadowed areas appear nearly the same (1:1 to 1:2)?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the subject’s lighting create a bright, evenly illuminated appearance with little to no shadow?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject’s lighting feature soft, minimal shadows?

- Is the subject evenly illuminated with a bright, balanced light?

- Does the lighting on the subject create a soft, diffused look with little contrast?

- Is the separation between lit and shadowed areas barely noticeable?

- Does the lighting minimize harsh shadows, creating a bright and airy appearance?

- Is the subject shaped by smooth, even lighting with minimal contrast?

- Does the video feature high-key lighting, reducing shadow depth?

- Is the subject’s visibility defined by soft, evenly distributed illumination?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features high-key lighting, where the subject is brightly lit with minimal contrast (1:1 to 1:2), reducing shadows and creating a soft, even illumination.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit with high-key lighting, appearing bright and evenly illuminated.

- A scene where the subject’s lighting lacks strong shadows, creating a soft effect.

- A shot where the lighting on the subject results in an even, well-distributed brightness.

- A video using high-key lighting to minimize contrast and shadow depth.

- A sequence where the subject appears clearly defined with smooth, diffused lighting.

- A shot featuring a subject with little to no noticeable shadowing.

- A video where even lighting ensures a bright and soft visual tone.

- A scene emphasizing a bright, clear aesthetic with minimal contrast.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio == 'minimal_contrast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['minimal_contrast', 'unknown', 'complex_changing']</code>

</details>

<details>
<summary><h2>Low-Key Lighting</h2></summary>


<h3>🔵 Label Name:</h3>
<code>low_key_lighting</code>


<h3>📖 Definition:</h3>
Is the lighting on the subject low-key, featuring a high contrast ratio where lit areas are significantly brighter than shadowed areas (1:8 or above)?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the subject’s lighting create a dramatic, high-contrast effect with deep shadows?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject illuminated in a way that produces a strong contrast between highlights and shadows?

- Does the lighting create deep shadows and strong highlights on the subject?

- Is the separation between lit and shadowed areas very pronounced?

- Does the subject appear shaped by intense, directional lighting with stark contrasts?

- Is the scene visually defined by dramatic lighting with bold shadows?

- Does the video feature low-key lighting, emphasizing shadow and depth?

- Does the subject’s visibility depend on strong contrast lighting effects?

- Does the scene use strong directional lighting that enhances the subject’s form with shadows?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features low-key lighting, creating a high contrast ratio (1:8 or above) with deep shadows and dramatic separation between highlights and dark areas.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is lit with low-key lighting, featuring dramatic shadows and strong highlights.

- A scene where the subject’s lighting creates high contrast with bold, directional light.

- A shot where the lighting produces deep, well-defined shadows on the subject.

- A video emphasizing the subject’s form through strong contrast lighting.

- A sequence that enhances the subject’s depth with intense shadows and directional light.

- A shot where bright highlights and dark shadows define the subject’s visual impact.

- A video utilizing low-key lighting to create a moody, dramatic effect.

- A scene that relies on stark lighting contrast for strong visual storytelling.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.subject_contrast_ratio == 'high_contrast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.subject_contrast_ratio not in ['high_contrast', 'unknown', 'complex_changing']</code>

</details>
