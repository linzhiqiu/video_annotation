# Light_quality Overview

<details>
<summary><h2>Light Quality Is Changing (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_changing</code>


<h3>📖 Definition:</h3>
Does the video feature dynamically shifting light quality over time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene transition between hard and soft lighting?

- Is there a noticeable variation in light sharpness throughout the video?

- Does the video include fluctuating shadow intensity and contrast?

- Is the lighting in the video inconsistent or evolving?

- Does the scene experience shifting illumination patterns?

- Is there a progression in light quality from diffused to hard or vice versa?

- Does the lighting transition multiple times in the video?

- Is the light source condition constantly changing?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features dynamically shifting light quality over time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where lighting conditions evolve throughout.

- A shot featuring transitions between soft and hard lighting.

- A scene where illumination continuously changes in intensity and texture.

- A video with a non-static lighting environment.

- A sequence where shifting light quality alters the visual effect.

- A video where lighting does not remain consistent over time.

- A shot where fluctuating brightness and contrast define the scene.

- A scene featuring multiple lighting shifts creating dynamic variation.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.light_quality == 'complex_changing'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality != 'complex_changing'</code>

</details>

<details>
<summary><h2>Light Quality Is Contrasting (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_contrasting</code>


<h3>📖 Definition:</h3>
Does the video contain both hard and soft lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene lit by a combination of hard and soft lighting?

- Does the shot contain contrasting lighting effects in different areas?

- Is there a strong interplay between sharp shadows and soft illumination?

- Does the video feature multiple lighting types coexisting?

- Is the lighting in the video diverse in terms of softness and intensity?

- Does the scene contain high-contrast lighting effects with mixed shadows?

- Is there an artistic contrast in light sources within the video?

- Does the shot showcase a balance between diffused and harsh lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features both hard and soft lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with strong contrasts between soft and hard lighting.

- A shot where diffused light coexists with harsh directional lighting.

- A scene featuring both high-contrast and smoothly illuminated areas.

- A video where shadows and highlights create a striking visual balance.

- A sequence where multiple light sources define the mood.

- A video showing an interplay between bright, harsh light and soft diffusion.

- A shot where both soft glow and hard illumination are present.

- A scene where mixed lighting styles dominate the composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.light_quality == 'complex_contrasting'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality != 'complex_contrasting'</code>

</details>

<details>
<summary><h2>Light Quality Is Hard</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_hard_light</code>


<h3>📖 Definition:</h3>
Does the video feature hard lighting with sharp, well-defined shadows and strong contrasts?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene illuminated by direct, concentrated light?

- Does the shot contain strong, crisp shadows with clear edges?

- Is the contrast between lit and shadowed areas high?

- Does the video feature lighting that accentuates textures and details?

- Is the illumination harsh with bright highlights and deep shadows?

- Does the lighting create dramatic effects with distinct shadows?

- Is the scene primarily lit by a single strong light source?

- Does the video show clear shadow lines due to hard lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features hard lighting with sharp, well-defined shadows and strong contrasts.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with high-contrast, direct lighting.

- A shot where shadows are sharp and crisp.

- A scene where light creates strong highlights and deep shadows.

- A video with dramatic lighting emphasizing textures and details.

- A sequence where hard light defines the visual structure.

- A video showing sharp shadow lines and high brightness contrast.

- A shot with focused, intense lighting creating a striking effect.

- A scene where illumination is strong and directional.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.light_quality == 'hard_light'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality != 'hard_light'</code>

</details>

<details>
<summary><h2>Light Quality Is Soft (Diffused)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_soft_light</code>


<h3>📖 Definition:</h3>
Does the video feature soft, diffused lighting with gentle illumination and minimal harsh shadows?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene lit with soft, evenly scattered light?

- Does the shot contain minimal shadows with smooth, blurred edges?

- Is the lighting low in contrast, making the scene appear evenly lit?

- Does the video feature diffused lighting with gradual shadow transitions?

- Is the illumination gentle with no strong highlights or hard shadows?

- Does the scene appear softly lit with reduced texture visibility?

- Is the lighting effect consistent with overcast skies or shaded areas?

- Does the video use soft, ambient lighting with no sharp shadow lines?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features soft, diffused lighting with gentle illumination and minimal harsh shadows.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with evenly scattered, soft lighting.

- A shot featuring smooth illumination with minimal contrast.

- A scene where lighting is diffused, reducing harsh shadows.

- A video with gentle, ambient light creating a soft glow.

- A sequence where light softly wraps around objects.

- A video showing gradual, blurred shadow transitions.

- A shot with smooth lighting that minimizes texture visibility.

- A scene where lighting is even and lacks sharp contrasts.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.light_quality == 'soft_diffused_light'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality != 'soft_diffused_light'</code>

</details>

<details>
<summary><h2>Is Lighting Quality Complex</h2></summary>


<h3>🔵 Label Name:</h3>
<code>lighting_quality_is_complex</code>


<h3>📖 Definition:</h3>
Does the video have a complex lighting quality that is changing, contrasting, or difficult to categorize?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene feature dynamic or contrasting lighting conditions?

- Is the lighting in the video inconsistent or evolving over time?

- Does the shot contain both hard and soft lighting interacting?

- Is the illumination in the video varied and difficult to classify?

- Does the video feature non-uniform lighting that shifts or blends?

- Is the scene lit with multiple sources creating a complex effect?

- Does the lighting in the video transition or contrast significantly?

- Is the overall lighting too mixed to fit a single category?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has a complex lighting quality that is changing, contrasting, or difficult to categorize.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring shifting, contrasting, or undefined lighting.

- A shot where the lighting conditions evolve or mix.

- A scene where hard and soft lighting interact dynamically.

- A video displaying complex lighting effects over time.

- A sequence with multiple light sources affecting the atmosphere.

- A video where the lighting setup is varied and undefined.

- A shot featuring an interplay of distinct lighting styles.

- A scene where light transitions, mixes, or creates contrast.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_lighting_quality_complex is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_lighting_quality_complex is False</code>

</details>


## Subcategories

- [Sunlight_quality](./sunlight_quality/index.md)