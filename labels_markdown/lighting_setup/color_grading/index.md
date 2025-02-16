# Color_grading Overview

<details>
<summary><h2>Is Black & White</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_black_white</code>


<h3>📖 Definition:</h3>
Is the video entirely in black and white, with no color present?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video remain in black and white throughout?

- Is there an absence of color in the entire video?

- Does the video only contain shades of gray?

- Is the video devoid of any color from start to finish?

- Does the sequence exclusively use black-and-white tones?

- Is there no color grading applied beyond monochrome?

- Does the video avoid any colored elements entirely?

- Is the video visually limited to grayscale shades?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is entirely in black and white, with no color present.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A black-and-white video without any color.

- A sequence composed entirely in grayscale tones.

- A monochrome video with no colored elements.

- A film that remains in black and white throughout.

- A shot where all visual elements are presented in shades of gray.

- A video that avoids any use of color grading beyond grayscale.

- A cinematic sequence where no color appears at any moment.

- A video that exclusively relies on black, white, and gray tones.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_black_white is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_black_white is False</code>

</details>

<details>
<summary><h2>Color Grading Is Complex</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_color_grading_complex</code>


<h3>📖 Definition:</h3>
Does the video exhibit complex color grading, involving dynamic or contrasting variations in color temperature, saturation, or brightness?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video’s color grading shift dynamically over time?

- Is there a mix of contrasting or evolving color elements in the video?

- Does the scene contain complex color variations across temperature, saturation, or brightness?

- Is there a noticeable contrast or change in color properties throughout the video?

- Does the lighting or color scheme involve significant variations?

- Is the color design of the video intricate or shifting?

- Does the video utilize a combination of evolving and contrasting hues?

- Is there a deliberate mix of multiple color grading techniques?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video exhibits complex color grading, involving dynamic or contrasting variations in color temperature, saturation, or brightness.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with shifting and contrasting color properties.

- A shot featuring varied and dynamic color grading.

- A sequence where color temperature, saturation, or brightness change significantly.

- A video using multiple color effects to create a dynamic look.

- A scene where color elements evolve or contrast in an intricate way.

- A video that blends different lighting and color changes together.

- A shot where the color scheme undergoes complex variations.

- A video emphasizing layered and evolving color effects.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_color_grading_complex is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_color_grading_complex is False</code>

</details>


## Subcategories

- [Brightness](./brightness/index.md)
- [Saturation](./saturation/index.md)
- [Temperature](./temperature/index.md)