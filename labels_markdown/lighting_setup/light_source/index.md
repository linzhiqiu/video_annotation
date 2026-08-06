# Light_source Overview

<details>
<summary><h2>Has Artificial Light</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_artificial_practical_light</code>


<h3>📖 Definition:</h3>
The scene is consistently lit by artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video.

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene contain clearly visible artificial light sources?

- Are artificial lights physically present and visible in the video?

- Is artificial lighting visibly included in the composition?

- Does the video feature practical artificial light sources?

- Are artificial lights seen in the frame?

- Is the environment illuminated by visible artificial lighting?

- Does the video include artificial lighting that is clearly present?

- Are artificial light sources included as part of the scene?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The scene is consistently lit by artificial practical light sources, such as lamps, streetlights, or LEDs, with the light source visible at some point in the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where artificial lights are visible in the frame.

- A scene illuminated by artificial light sources that can be seen.

- A shot where practical artificial lighting is present and visible.

- A sequence where artificial lights are included in the composition.

- A video featuring clearly visible artificial lighting fixtures.

- A setting where artificial light sources are physically present.

- A shot where artificial lights are included as part of the scene.

- A scene where visible artificial lighting contributes to the atmosphere.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.artificial_light_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.artificial_light_source is False</code>

</details>

<details>
<summary><h2>Has Firelight</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_firelight</code>


<h3>📖 Definition:</h3>
Is the scene consistently lit primarily by firelight, and the fire is visible in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is firelight the primary light source in the video, even if the fire itself is not visible?

- Is the scene primarily lit by a fire, such as a candle, torch, or campfire?

- Does the lighting suggest a warm glow from a fire source?

- Is firelight providing the dominant illumination in the video?

- Is the environment visibly affected by flickering firelight?

- Does the shot contain lighting that suggests flames as the main source?

- Is the video illuminated by a warm, fluctuating fire-based light?

- Does the lighting have an orange-red hue characteristic of fire?

- Is the scene’s lighting dynamically shifting in a way that suggests fire?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The scene is consistently lit primarily by firelight, and the fire is visible in the scene.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video is primarily lit by firelight, even if the fire itself is not visible.

- A video where firelight serves as the main source of illumination.

- A scene where the environment is lit by flames.

- A sequence where firelight provides the dominant glow.

- A shot characterized by warm, flickering fire-based lighting.

- A video where torches, candles, or campfires illuminate the scene.

- A setting bathed in a reddish-orange glow from fire.

- A shot where the light shifts dynamically, indicating a fire source.

- A video with lighting that resembles fire’s natural movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.firelight_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.firelight_source is False</code>

</details>

<details>
<summary><h2>Has Moonlight or Starlight</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_moonlight_starlight</code>


<h3>📖 Definition:</h3>
Is the scene consistently lit primarily by moonlight or starlight, and the moon or stars are visible in the scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene primarily illuminated by moonlight?

- Does the lighting suggest nighttime with the moon as the main source?

- Is the moon itself visible and providing the dominant illumination?

- Does the video rely on natural moonlight for lighting?

- Is the environment bathed in a soft, cool-toned light consistent with moonlight?

- Does the scene depict a night setting where the moon acts as the main light source?

- Is the primary source of illumination a visible moon?

- Is the video characterized by the cool, ambient glow of moonlight?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The scene is consistently lit primarily by moonlight or starlight, and the moon or stars are visible in the scene.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where moonlight serves as the dominant illumination.

- A scene where the moon visibly lights up the environment.

- A sequence where moonlight creates the primary lighting effect.

- A shot where the moon acts as the key light source.

- A night scene illuminated by visible moonlight.

- A setting where the ambient glow of the moon defines the lighting.

- A shot where the moon is prominently casting light on the environment.

- A video where moonlight provides soft, cool-toned illumination.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.moonlight_starlight_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.moonlight_starlight_source is False</code>

</details>

<details>
<summary><h2>Has Non-Visible Light Source</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_non_visible_light_source</code>


<h3>📖 Definition:</h3>
Does the video never show any visible light source, and the lighting cannot be clearly attributed to sunlight?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene illuminated by a light source that is not seen in the frame?

- Does the shot lack a clearly identifiable lighting source?

- Is the dominant light coming from an unseen origin?

- Is the lighting setup ambiguous with no apparent source?

- Does the scene appear naturally lit without a direct light source?

- Is the shot illuminated in a way that makes it hard to determine the source?

- Does the video rely on environmental or ambient lighting?

- Is the primary illumination coming from an off-screen source?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video never shows any visible light source, and the lighting cannot be clearly attributed to sunlight.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video is lit by artificial light (e.g., not sunlight or firelight), with the light source not visible in the frame.

- A video where the light source is not identifiable.

- A scene where the illumination comes from an unseen source.

- A shot where the lighting does not have a clear origin.

- A video with ambient or environmental lighting without visible fixtures.

- A setting where the source of brightness is not visible in the frame.

- A shot where light is present but the source remains off-screen.

- A video where the illumination is subtle and indirect.

- A scene with a non-visible primary light source.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.non_visible_light_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.non_visible_light_source is False</code>

</details>

<details>
<summary><h2>Has Sunlight</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_sunlight</code>


<h3>📖 Definition:</h3>
Is the scene consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is sunlight the primary light source in the video, even if the sun itself is not visible?

- Does the scene appear to be naturally illuminated by sunlight?

- Is the dominant lighting in the video coming from the sun?

- Does the video primarily rely on daylight as the main light source?

- Is the environment bright due to sunlight, even if the sun is not visible?

- Does natural outdoor lighting suggest a sunlight source?

- Is the scene illuminated in a way that strongly indicates sunlight?

- Is sunlight the key source shaping the scene’s lighting conditions?

- Does the video’s lighting behave like outdoor sunlight exposure?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The scene is consistently lit primarily by sunlight, whether or not the sun itself is visible in the frame.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The primary light source in the video is sunlight, whether or not the sun is visible.

- A video where daylight is the dominant light source.

- A shot primarily illuminated by natural sunlight.

- A scene where outdoor sunlight shapes the lighting conditions.

- A sequence where daylight provides the main illumination.

- A video with strong natural light, consistent with sunlight.

- A shot where the lighting suggests exposure to direct or indirect sunlight.

- A scene where sunlight is the defining source of illumination.

- A setting that appears naturally lit by the sun.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.sunlight_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.sunlight_source is False</code>

</details>

<details>
<summary><h2>Has Unclear or Changing Light Source</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_unclear_or_changing_light_source</code>


<h3>📖 Definition:</h3>
Does the video’s primary light source change over time or comes from an uncommon source other than the sun, fire, moon, stars, or artificial light?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the light source change dynamically across different parts of the video?

- Is the illumination shifting unpredictably between different lighting setups?

- Does the video feature inconsistent or rapidly changing light sources?

- Is the scene affected by multiple fluctuating light sources?

- Does the lighting undergo frequent transformations or significant variations?

- Is the video characterized by a mix of different lighting types over time?

- Does the light source appear complex and non-uniform throughout the sequence?

- Is the scene influenced by multiple changing or contrasting light sources?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video’s primary light source changes over time or comes from an uncommon source other than the sun, fire, moon, stars, or artificial light.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the light source is dynamic and ever-changing.

- A shot with unpredictable and shifting lighting conditions.

- A scene featuring multiple contrasting or fluctuating light sources.

- A video characterized by varying illumination setups.

- A sequence where lighting changes significantly over time.

- A shot where brightness, color, or intensity varies unpredictably.

- A video with irregular or mixed lighting across different moments.

- A scene where the light source alternates frequently.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.complex_light_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.complex_light_source is False</code>

</details>

<details>
<summary><h2>Is Abstract Light Source</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_abstract</code>


<h3>📖 Definition:</h3>
Does the video feature an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene have no identifiable physical light source?

- Is the lighting in the video artificial or detached from real-world illumination?

- Does the video appear to have lighting that is independent of any real-world sources?

- Is the scene artificially lit with no clear or natural light source?

- Does the video feature synthetic or digital lighting without a physical origin?

- Is the illumination stylized or abstract rather than derived from real-world lighting?

- Does the video rely on a simulated or non-realistic light source?

- Is the lighting setup in the video disconnected from real-world physics?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features an abstract or synthetic scene, with non-physically realistic lighting that makes it hard to identify the light source.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the lighting is artificial and detached from real-world sources.

- A shot where the illumination is abstract and does not follow physical lighting behavior.

- A scene featuring non-realistic, digitally rendered lighting.

- A video using synthetic lighting without any identifiable physical source.

- A sequence where the light is generated artificially, without sun, fire, or lamps.

- A shot with stylized lighting that does not mimic real-world conditions.

- A video where the lighting does not originate from a realistic source.

- A scene where illumination appears purely digital or graphical.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.abstract_light_source is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.abstract_light_source is False</code>

</details>
