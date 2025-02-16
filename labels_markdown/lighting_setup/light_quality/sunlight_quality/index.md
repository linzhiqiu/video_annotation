# Sunlight_quality Overview

<details>
<summary><h2>Sunlight Level Is Normal</h2></summary>


<h3>🔵 Label Name:</h3>
<code>sunlight_level_is_normal</code>


<h3>📖 Definition:</h3>
Does the video feature regular daylight with balanced brightness?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene illuminated by natural daylight that is neither too intense nor too diffused?

- Does the shot depict normal outdoor lighting conditions?

- Is the sunlight soft and natural without being overly bright or cloudy?

- Is the lighting in the video evenly balanced with no strong highlights or shadows?

- Does the scene feature natural daylight without extreme contrast?

- Is the daylight in the video neutral and well-balanced?

- Is the outdoor lighting in the scene clear and natural?

- Does the video have natural daylight that does not appear too strong or weak?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features regular daylight with balanced brightness.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with natural, well-balanced daylight.

- A scene illuminated by neutral, evenly distributed daylight.

- A shot featuring clear daylight without extreme contrasts.

- A video where outdoor lighting appears natural and neutral.

- A sequence showing daylight that is neither too harsh nor too soft.

- A video with natural light that is clear and evenly lit.

- A shot where the outdoor lighting feels natural and normal.

- A scene where daylight is present without noticeable extremes.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_level == 'normal'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_level != 'normal'</code>

</details>

<details>
<summary><h2>Sunlight Level Is Overcast</h2></summary>


<h3>🔵 Label Name:</h3>
<code>sunlight_level_is_overcast</code>


<h3>📖 Definition:</h3>
Does the video feature diffused light from cloudy skies without direct sunlight?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene lit by soft, diffused light from overcast skies?

- Does the video show an absence of strong sunlight due to clouds?

- Is the lighting evenly distributed with minimal shadows and highlights?

- Does the shot appear to be taken on a cloudy or overcast day?

- Is the outdoor brightness low and lacking strong contrasts?

- Does the video have a soft, natural lighting due to an overcast sky?

- Is the scene characterized by muted, even lighting without harsh shadows?

- Does the shot have a neutral, diffused lighting due to cloud cover?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features diffused light from cloudy skies without direct sunlight.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video illuminated by soft, overcast lighting.

- A shot where cloud cover diffuses the natural light.

- A scene featuring gentle, even lighting without harsh shadows.

- A video where the lighting is consistent due to an overcast sky.

- A sequence where the absence of strong sunlight creates a muted look.

- A shot where outdoor lighting is natural but subdued.

- A video where the sky is overcast, resulting in soft lighting.

- A scene lit by cloudy, diffused light that lacks harsh brightness.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_level == 'overcast'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_level != 'overcast'</code>

</details>

<details>
<summary><h2>Sunlight Level Is Sunny</h2></summary>


<h3>🔵 Label Name:</h3>
<code>sunlight_level_is_sunny</code>


<h3>📖 Definition:</h3>
Does the video feature bright, direct sunlight with strong intensity?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene characterized by strong sunlight and high contrast?

- Does the video show harsh, bright outdoor lighting?

- Is the lighting intense with strong shadows and highlights?

- Does the shot contain direct sunlight with clear, sharp lighting?

- Is the outdoor brightness notably strong and high in contrast?

- Does the sunlight create sharp shadows and bright highlights?

- Is the lighting in the video strong and direct, typical of sunny weather?

- Does the scene have a high-exposure look due to strong sunlight?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features bright, direct sunlight with strong intensity.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video characterized by strong sunlight and deep shadows.

- A shot featuring direct sunlight with high brightness.

- A scene illuminated by intense, high-contrast sunlight.

- A video with harsh outdoor lighting conditions.

- A sequence where bright sunlight defines the lighting style.

- A shot where natural lighting is powerful and direct.

- A video where high exposure and bright highlights dominate.

- A scene showing a strong, sunlit environment with clear contrast.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_level == 'sunny'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_level != 'sunny'</code>

</details>

<details>
<summary><h2>Sunlight Level Is Sunset/Sunrise</h2></summary>


<h3>🔵 Label Name:</h3>
<code>sunlight_level_is_sunset_sunrise</code>


<h3>📖 Definition:</h3>
Does the video feature warm, golden tones from the sun at dawn or dusk?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene illuminated by soft, golden sunlight typical of sunrise or sunset?

- Does the video have a warm, orange glow from the sun?

- Is the lighting in the shot characteristic of early morning or late evening?

- Does the video feature the sun low in the sky with long shadows?

- Is the outdoor lighting rich in warm hues and soft highlights?

- Does the scene showcase dramatic, warm lighting from the rising or setting sun?

- Is the shot filled with golden-hour lighting, creating a warm atmosphere?

- Does the video emphasize the time of day with warm, directional sunlight?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features warm, golden tones from the sun at dawn or dusk.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video illuminated by the golden light of sunrise or sunset.

- A shot featuring warm, directional sunlight during golden hour.

- A sequence with the sun low in the sky, casting long shadows.

- A video where rich, warm hues define the natural lighting.

- A shot where golden tones create a soft, atmospheric look.

- A video capturing the warm, natural light of sunrise or sunset.

- A sequence where the warm, low-angle sun defines the lighting.

- A shot bathed in golden-hour lighting, emphasizing warm tones.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_level == 'sunset_sunrise'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_level != 'sunset_sunrise'</code>

</details>

<details>
<summary><h2>Sunlight Level Is Unknown</h2></summary>


<h3>🔵 Label Name:</h3>
<code>sunlight_level_is_unknown</code>


<h3>📖 Definition:</h3>
Is the sunlight condition in the video unclear or not applicable?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is it difficult to determine the sunlight level in this scene?

- Does the video take place in an environment where sunlight is irrelevant?

- Is the setting indoors or in a space where sunlight is not a factor?

- Is there no discernible sunlight influencing the scene?

- Does the lighting in the shot not match common outdoor conditions?

- Is the video’s lighting ambiguous in terms of natural sunlight?

- Does the scene lack enough visual cues to assess sunlight levels?

- Is the sunlight condition indeterminate due to the environment?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The sunlight condition in the video is unclear or not applicable.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where sunlight presence cannot be determined.

- A shot where natural lighting conditions are ambiguous.

- A scene that does not rely on direct or indirect sunlight.

- A video where sunlight exposure is not a defining factor.

- A sequence where the lighting does not indicate an outdoor setting.

- A shot where the natural light condition remains uncertain.

- A video where the sunlight level is unknown or irrelevant.

- A scene where sunlight does not visibly affect the lighting.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_level == 'unknown'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_level != 'unknown'</code>

</details>
