# Subject_lighting Overview

<details>
<summary><h2>Is Subject Lighting Applicable</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_subject_lighting_applicable</code>


<h3>📖 Definition:</h3>
Does the video have a clearly defined subject suitable for lighting analysis?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the contrast ratio on the subject applicable in this video?

- Does the video feature a subject where lighting contrast can be determined?

- Is there a distinguishable subject with visible lighting contrast?

- Can the contrast ratio of the subject be meaningfully classified?

- Does the video include a well-defined subject for contrast evaluation?

- Is the subject lighting clear enough to assess contrast levels?

- Does the scene provide sufficient detail to classify lighting contrast on the subject?

- Can the contrast ratio on the subject be confidently labeled?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has a clearly defined subject suitable for lighting analysis.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the contrast ratio on the subject is applicable and classifiable.

- A scene featuring a well-lit subject with distinguishable contrast levels.

- A shot where the lighting contrast on the subject can be meaningfully categorized.

- A video where the subject’s visibility allows for contrast ratio evaluation.

- A sequence where the subject’s lighting provides enough clarity for contrast classification.

- A scene in which the contrast ratio on the subject is clearly identifiable.

- A shot where subject contrast is distinct and measurable.

- A video where lighting on the subject is applicable for contrast assessment.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_subject_lighting_applicable is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_subject_lighting_applicable is False</code>

</details>

<details>
<summary><h2>Portrait Lighting</h2></summary>


<h3>🔵 Label Name:</h3>
<code>portrait_lighting</code>


<h3>📖 Definition:</h3>
Is the lighting setup designed to create a polished, professional appearance, commonly used in portrait photography or videography?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video use controlled lighting to enhance the subject’s appearance?

- Is the lighting arranged to create a professional studio look?

- Does the scene feature portrait-style lighting with soft, flattering illumination?

- Is the subject lit in a way that is typical for professional photography?

- Does the shot use specialized portrait lighting techniques?

- Is the lighting setup aimed at achieving a professional or cinematic appearance?

- Does the subject benefit from a carefully arranged lighting setup?

- Is the lighting used to highlight the subject’s features in a controlled manner?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The lighting setup is designed to create a polished, professional appearance, commonly used in portrait photography or videography.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring controlled lighting that enhances the subject’s appearance.

- A scene where the subject is illuminated with professional studio lighting.

- A shot using carefully arranged portrait lighting techniques.

- A video where the lighting is designed for a professional, polished look.

- A sequence with a cinematic and controlled lighting setup.

- A scene where portrait lighting enhances the subject’s facial details.

- A shot that applies high-quality lighting for a refined visual effect.

- A composition that follows standard portrait lighting practices.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.portrait_lighting is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.portrait_lighting is False</code>

</details>

<details>
<summary><h2>Rembrandt Lighting</h2></summary>


<h3>🔵 Label Name:</h3>
<code>rembrandt_lighting</code>


<h3>📖 Definition:</h3>
Does the video use Rembrandt lighting, where one side of the subject’s face is illuminated, creating a distinct triangle of light on the opposite cheek?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the subject lit with a classic Rembrandt lighting technique?

- Does the lighting create a triangle of light on the subject’s shaded cheek?

- Is the video using a lighting style that combines side and front illumination?

- Does the subject’s lighting emphasize dramatic contrast with controlled highlights?

- Is the lighting setup focused on one side while allowing some light to spill onto the other?

- Does the scene feature traditional portrait lighting with strong directional contrast?

- Is the video using a cinematic lighting setup inspired by Rembrandt’s style?

- Does the lighting create a balanced but moody effect on the subject’s face?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video uses Rembrandt lighting, where one side of the subject’s face is illuminated, creating a distinct triangle of light on the opposite cheek.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring classic Rembrandt lighting with side and front illumination.

- A shot where a triangle of light appears on the subject’s shaded cheek.

- A sequence using a lighting setup that creates dramatic contrast on the subject’s face.

- A scene where the subject’s lighting follows a traditional portrait photography style.

- A shot applying controlled directional lighting for a cinematic look.

- A video where the lighting creates a moody yet balanced effect.

- A composition emphasizing shadows and highlights in a portrait setup.

- A video utilizing a professional portrait lighting technique.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.rembrandt_lighting is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.rembrandt_lighting is False</code>

</details>


## Subcategories

- [Light_contrast](./light_contrast/index.md)
- [Light_direction](./light_direction/index.md)