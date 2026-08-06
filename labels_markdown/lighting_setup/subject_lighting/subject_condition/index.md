# Subject_condition Overview

<details>
<summary><h2>Consistent Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_consistent_subject</code>


<h3>📖 Definition:</h3>
Are there one or more clear, salient subjects lit by external light who remain consistent in the frame throughout the shot?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot maintain the same subject(s) from start to finish?

- Are there clear, identifiable subjects that don't change?

- Is the subject presence stable throughout the sequence?

- Are there no subject changes, exits, or reveals?

- Is the subject clearly visible and consistent?

- Does the shot feature stable subject presence?

- Are there no subject transformations or replacements?

- Is the subject's presence uninterrupted?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- One or more clear, salient subjects are lit by external light and remain consistent in the frame throughout the shot.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with stable, consistent subject presence.

- A sequence where the subject remains unchanged.

- A shot featuring clear, identifiable subjects throughout.

- A video with uninterrupted subject presence.

- A sequence where subjects don't change or exit.

- A shot with stable, consistent subject visibility.

- A video where subject presence is maintained.

- A sequence with no subject transformations.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_consistent_subject is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_consistent_subject is False</code>

</details>

<details>
<summary><h2>Inconsistent Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_inconsistent_subject</code>


<h3>📖 Definition:</h3>
Are one or more subjects lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Do subjects change while lighting remains stable?

- Are there subject transitions with consistent lighting?

- Does the subject presence vary but lighting stays the same?

- Are there subject changes without lighting variation?

- Do subjects enter or exit with stable lighting?

- Is there subject replacement with consistent lighting?

- Do subjects change while lighting properties remain fixed?

- Are there subject variations with unchanged lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- One or more subjects are lit by external light, but change during the shot (e.g., enter the frame, exit the frame, or are replaced).

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where subjects change but lighting remains stable.

- A sequence with subject transitions and consistent lighting.

- A shot where subject presence varies but lighting stays the same.

- A video featuring subject changes without lighting variation.

- A sequence with subject entries/exits and stable lighting.

- A shot where subjects are replaced with consistent lighting.

- A video with subject variations but fixed lighting properties.

- A sequence where subjects change but lighting remains unchanged.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_inconsistent_subject is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_inconsistent_subject is False</code>

</details>

<details>
<summary><h2>Subject Lighting Is Unrealistic</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_subject_lighting_unrealistic</code>


<h3>📖 Definition:</h3>
Does the video contain subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene animated or stylized in a way that makes lighting hard to analyze?

- Does the scene lack clear lightable surfaces or shading?

- Is the lighting physically unrealistic or abstract?

- Is the scene 2D or 2.5D with unclear lighting properties?

- Are the lighting properties ambiguous or hard to interpret?

- Does the scene lack consistent shading or shadows?

- Is the lighting analysis too complex or uncertain?

- Are the lighting effects too stylized to analyze?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video contains subjects, but the lighting is non-physically realistic, including animated, stylized, synthetic, 2D, or 2.5D content, making it too visually abstract to reliably analyze contrast and lighting direction.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with stylized or abstract lighting that's hard to analyze.

- A video where lighting properties are ambiguous or unclear.

- A sequence with non-physically realistic lighting effects.

- A shot where lighting analysis is too complex or uncertain.

- A scene with 2D or 2.5D rendering and unclear lighting.

- A video where lighting effects are too stylized to analyze.

- A sequence lacking clear lightable surfaces or shading.

- A shot where lighting properties are difficult to interpret.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_subject_lighting_unrealistic is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_subject_lighting_unrealistic is False</code>

</details>

<details>
<summary><h2>Unclear or Light-Emitting Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_unclear_or_light_emitting_subject</code>


<h3>📖 Definition:</h3>
Does the video lack a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is this primarily a scenery or environmental shot without a distinct subject?

- Does the scene show only distant landscapes or minimal visible surfaces?

- Is there no clear target for assessing lighting effects?

- Are there insufficient lightable surfaces to evaluate lighting?

- Is the scene dominated by environmental elements without a clear subject?

- Are there only light sources without visible effects on surfaces?

- Is the scene too abstract or distant to identify a clear subject?

- Are there no distinct objects or elements to analyze lighting on?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video lacks a clear subject visibly illuminated by external light, either because the subject is absent, ambiguous (e.g., scenery shot), or emits light or is engulfed by a light source in a way that obscures form shadows and highlights, making contrast and direction unreliable to judge.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scenery shot without a distinct subject for lighting analysis.

- A video showing only environmental elements or landscapes.

- A sequence with insufficient lightable surfaces to evaluate.

- A shot dominated by distant or abstract elements.

- A scene with only light sources and minimal surface effects.

- A video without clear subjects to analyze lighting on.

- A sequence showing only environmental lighting effects.

- A shot where lighting cannot be evaluated on any subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.is_unclear_or_light_emitting_subject is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.is_unclear_or_light_emitting_subject is False</code>

</details>
