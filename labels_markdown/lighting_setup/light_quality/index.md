# Light_quality Overview

<details>
<summary><h2>Light Quality Is Changing (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_changing</code>


<h3>📖 Definition:</h3>
Do some surface areas in the scene change in light quality over time, shifting between soft and hard light?

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

- Some surface area in the scene changes in light quality over time, shifting between soft and hard light.

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
<code>self.lighting_setup.light_quality_is_changing is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality_is_changing is False</code>

</details>

<details>
<summary><h2>Is Lighting Quality Complex (Ambiguous)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_complex_ambiguous</code>


<h3>📖 Definition:</h3>
Does the scene lack sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are shadows or surface cues too unclear to assess lighting?

- Is the lighting in the video stylized or non-physical?

- Are important visual cues missing, abstract, or degraded?

- Does the scene lack visible surfaces or shadows to judge from?

- Is the video too visually noisy or distorted to identify lighting type?

- Is the lighting unreadable due to low resolution or exposure issues?

- Is the shading inconsistent with real-world lighting behavior?

- Is the lighting impossible to categorize based on available cues?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The scene lacks sufficient visual information to determine light quality, due to non-physically realistic shading, absence of visible shadow-casting surface areas, or visual degradation.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where shadows are missing, abstract, or implausible.

- A shot where lighting cues are visually degraded or inconsistent.

- A scene too ambiguous or stylized to assess real-world lighting.

- A video with insufficient detail to determine shadow or highlight behavior.

- A frame where no usable shadow-casting surface is visible.

- A video with noise, blur, or compression that obscures lighting cues.

- A visually unclear or low-information scene for lighting classification.

- A sequence where light quality cannot be reliably judged.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.light_quality_is_complex_ambiguous is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality_is_complex_ambiguous is False</code>

</details>

<details>
<summary><h2>Light Quality Is Hard</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_hard</code>


<h3>📖 Definition:</h3>
Are all or nearly all visible surface areas within the scene lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Are all or nearly all visible surface areas within the scene lit by hard light?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video feature hard lighting (e.g., strong contrast, bright highlights, or sharp shadows)?

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

- All or nearly all visible surface areas within the scene are lit by hard light, indicated by sharp-edged shadows with narrow or no penumbrae, or abrupt light-to-dark transitions, or textures that are strongly emphasized, or highlights that are small and bright, and no noticeable signs of soft light.

- All or nearly all visible surface areas within the scene are lit by hard light.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video features hard lighting (e.g., strong contrast, bright highlights, or sharp shadows).

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
<code>self.lighting_setup.light_quality_is_hard is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality_is_hard is False</code>

</details>

<details>
<summary><h2>Light Quality Is Soft (Diffused)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>light_quality_is_soft</code>


<h3>📖 Definition:</h3>
Are all visible surface areas within the scene lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Are all visible surface areas within the scene lit by soft light?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video feature soft, diffused lighting with gentle illumination and minimal harsh shadows?

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

- All visible surface areas within the scene are lit by soft light, indicated by the absence of sharp-edged shadows, or the presence of wide penumbrae, or smooth light-to-dark transitions, or surface textures appearing subdued, or highlights that are soft or diffused, and no noticeable signs of hard light.

- All visible surface areas within the scene are lit by soft light.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video features soft, diffused lighting with gentle illumination and minimal harsh shadows.

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
<code>self.lighting_setup.light_quality_is_soft is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.light_quality_is_soft is False</code>

</details>


## Subcategories

- [Sunlight_quality](./sunlight_quality/index.md)