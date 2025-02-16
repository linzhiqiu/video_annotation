# Temperature Overview

<details>
<summary><h2>Color Temperature Is Changing (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>color_temperature_is_changing</code>


<h3>📖 Definition:</h3>
Does the video’s color temperature shift dynamically over time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video’s color grading change significantly throughout?

- Is there a noticeable variation in the color temperature?

- Does the scene transition between warm and cool tones?

- Is there an evolving or shifting color palette in the video?

- Does the lighting and color temperature fluctuate over time?

- Does the video show deliberate color temperature changes?

- Is there a progression or transition between different color temperatures?

- Does the scene undergo a noticeable color transformation?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video’s color temperature shifts dynamically over time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the color grading changes throughout.

- A sequence featuring evolving color temperature shifts.

- A shot with transitions between warm and cool tones.

- A video with an intentional change in color temperature.

- A scene where the lighting color shifts across different moments.

- A video displaying a dynamic spectrum of color temperatures.

- A cinematic effect using changing color tones over time.

- A sequence where the color grading is deliberately inconsistent.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.color_temperature == 'complex_changing'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.color_temperature != 'complex_changing'</code>

</details>

<details>
<summary><h2>Color Temperature Is Contrasting (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>color_temperature_is_contrasting</code>


<h3>📖 Definition:</h3>
Does the video feature strongly contrasting warm and cool color temperatures within the same scene or sequence?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video exhibit a striking contrast between warm and cool tones?

- Is there a mix of warm and cool colors within the same shot or sequence?

- Does the scene use opposing color temperatures to create visual contrast?

- Is there a noticeable juxtaposition of warm and cool lighting?

- Does the color grading include a strong contrast between warm and cool hues?

- Is the video designed to emphasize the interplay of warm and cool tones?

- Does the sequence include deliberate color temperature opposition?

- Is there an intentional balance of warm and cool lighting styles?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features strongly contrasting warm and cool color temperatures within the same scene or sequence.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with a strong contrast between warm and cool tones.

- A sequence where warm and cool hues are deliberately juxtaposed.

- A shot highlighting opposing color temperatures in the same frame.

- A video with intentional warm-cool lighting contrast.

- A scene designed to emphasize a balance between warm and cool hues.

- A shot where warm and cool lights create a visually striking effect.

- A sequence where the interplay of warm and cool color grading is evident.

- A video using complementary warm and cool tones for artistic contrast.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.color_temperature == 'complex_contrasting'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.color_temperature != 'complex_contrasting'</code>

</details>

<details>
<summary><h2>Color Temperature Is Cool</h2></summary>


<h3>🔵 Label Name:</h3>
<code>color_temperature_is_cool</code>


<h3>📖 Definition:</h3>
Is the video dominated by cool tones, such as blues, greens, or cyan?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video have a noticeable cool color balance?

- Is the color grading primarily in cool hues?

- Does the video emphasize blues, greens, or teal tones?

- Is the overall scene bathed in cool lighting?

- Does the sequence consistently feature cool color grading?

- Are the dominant colors in the video within the cool spectrum?

- Does the video’s color scheme lean towards cool tones?

- Is the lighting styled to create a cool, crisp atmosphere?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is dominated by cool tones, such as blues, greens, or cyan.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video graded with cool, blue hues.

- A sequence primarily featuring teal and cyan tones.

- A shot where cool colors like blue and green are dominant.

- A cinematic look with strong cool color grading.

- A video that maintains a consistent cool color balance.

- A scene lit in soft, blue-tinted tones.

- A color scheme emphasizing coolness throughout the video.

- A video visually defined by cold, crisp color tones.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.color_temperature == 'cool'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.color_temperature != 'cool'</code>

</details>

<details>
<summary><h2>Color Temperature Is Neutral</h2></summary>


<h3>🔵 Label Name:</h3>
<code>color_temperature_is_neutral</code>


<h3>📖 Definition:</h3>
Does the video have a neutral color balance, without a strong warm or cool tint?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the video’s color temperature balanced and natural?

- Does the video lack a noticeable warm or cool shift?

- Is the overall color grading neutral and evenly toned?

- Does the sequence avoid heavy color grading shifts?

- Is the lighting in the video neither warm nor cool?

- Are the colors in the video presented in a natural balance?

- Does the color scheme avoid an artificial tint?

- Is the scene visually neutral without a strong color cast?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has a neutral color balance, without a strong warm or cool tint.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with evenly balanced color grading.

- A sequence with a neutral and natural color palette.

- A shot where no strong warm or cool tint is applied.

- A video where colors appear as naturally as possible.

- A cinematic look with minimal color grading interference.

- A scene presented in a neutral, unaltered color tone.

- A video that avoids overly warm or cool color biases.

- A shot with realistic and balanced color reproduction.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.color_temperature == 'neutral'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.color_temperature != 'neutral'</code>

</details>

<details>
<summary><h2>Color Temperature Is Warm</h2></summary>


<h3>🔵 Label Name:</h3>
<code>color_temperature_is_warm</code>


<h3>📖 Definition:</h3>
Is the video dominated by warm tones, such as reds, oranges, or yellows?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video have a noticeable warm color balance?

- Is the color grading primarily in warm hues?

- Does the video emphasize reds, oranges, or golden tones?

- Is the overall scene bathed in warm lighting?

- Does the sequence consistently feature warm color grading?

- Are the dominant colors in the video within the warm spectrum?

- Does the video’s color scheme lean towards warm tones?

- Is the lighting styled to create a warm, inviting look?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is dominated by warm tones, such as reds, oranges, or yellows.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video graded with warm, golden hues.

- A sequence primarily featuring red and orange tones.

- A shot where warm colors like yellow and amber are dominant.

- A cinematic look with strong warm color grading.

- A video that maintains a consistent warm color balance.

- A scene lit in soft, golden tones.

- A color scheme emphasizing warmth throughout the video.

- A video visually defined by warm light and hues.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.color_temperature == 'warm'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.color_temperature not in ['warm']</code>

</details>
