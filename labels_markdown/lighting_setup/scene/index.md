# Scene Overview

<details>
<summary><h2>Scene Type Is Exterior</h2></summary>


<h3>🔵 Label Name:</h3>
<code>scene_type_is_exterior</code>


<h3>📖 Definition:</h3>
Is the video captured through a camera (real or simulated) and taking place outdoors with physically realistic lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene taking place outside in an open environment?

- Does the video primarily feature an outdoor setting?

- Is the background environment located in a natural or urban open space?

- Does the video take place in a landscape, street, or other outdoor area?

- Is the scene exposed to natural elements like the sky or open air?

- Does the video clearly depict an exterior environment?

- Is the location of the scene outdoors rather than indoors?

- Does the shot emphasize an outdoor setting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is captured through a camera (real or simulated) and takes place outdoors with physically realistic lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video primarily taking place in an open outdoor space.

- A sequence where the setting is clearly outside.

- A shot showing an environment exposed to open air.

- A scene depicting an exterior location such as a park or street.

- A video where the primary setting is outside in nature or urban areas.

- A sequence with all frames captured in an exterior space.

- A shot emphasizing an open outdoor environment.

- A video filmed within an exterior location.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.scene_type_is_exterior is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.scene_type_is_exterior is False</code>

</details>

<details>
<summary><h2>Scene Type Is Interior</h2></summary>


<h3>🔵 Label Name:</h3>
<code>scene_type_is_interior</code>


<h3>📖 Definition:</h3>
Is the video captured through a camera (real or simulated) and taking place indoors with physically realistic lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene taking place inside a building or enclosed space?

- Does the video primarily feature an indoor setting?

- Is the background environment confined to an enclosed structure?

- Does the video take place in a room, hallway, or other indoor space?

- Is the scene surrounded by walls, ceilings, or other enclosed elements?

- Does the video clearly depict an indoor environment?

- Is the location of the scene indoors rather than outdoors?

- Does the shot emphasize an enclosed, interior setting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is captured through a camera (real or simulated) and takes place indoors with physically realistic lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video primarily taking place in an enclosed space.

- A sequence where the setting is clearly indoors.

- A shot showing an environment surrounded by walls and ceilings.

- A scene depicting an indoor location such as a room or corridor.

- A video where the primary setting is inside a building.

- A sequence with all frames captured in an interior space.

- A shot emphasizing an enclosed indoor environment.

- A video filmed within an interior location.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.scene_type_is_interior is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.scene_type_is_interior is False</code>

</details>

<details>
<summary><h2>Scene Type Is Synthetic</h2></summary>


<h3>🔵 Label Name:</h3>
<code>scene_type_is_synthetic</code>


<h3>📖 Definition:</h3>
Is the video not a camera capture but a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene artificially generated rather than filmed in the real world?

- Does the video feature 2D animation, game graphics, or CGI environments?

- Is the background made of non-realistic or stylized elements?

- Does the video depict an environment with unrealistic lighting or physics?

- Is the scene composed of computer-generated imagery or game assets?

- Does the video show effects like exaggerated reflections or ray tracing?

- Is the scene visually distinct from real-world cinematography?

- Does the shot emphasize a synthetic, fantasy, or virtual setting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is not a camera capture but a stylized or non-photorealistic render (e.g., anime, cartoons, or low-fidelity game graphics) with non-physically realistic lighting such as flat shading, fake shadows, missing reflections, or exaggerated glow effects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video shows a synthetic environment with unnatural lighting effects that defy real-world physics.

- A video taking place in a digitally created world.

- A sequence with non-realistic, game-like visuals.

- A shot featuring exaggerated lighting and reflections.

- A video set in a stylized, animated, or computer-generated space.

- A sequence showing an environment with unrealistic physics or effects.

- A shot where the setting is clearly artificial or game-rendered.

- A video with CGI-heavy or virtual world visuals.

- A scene that exists entirely in a synthetic or animated world.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.scene_type_is_synthetic is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.scene_type_is_synthetic is False</code>

</details>

<details>
<summary><h2>Scene Type Is Unclear or Changing</h2></summary>


<h3>🔵 Label Name:</h3>
<code>scene_type_is_unclear_or_changing</code>


<h3>📖 Definition:</h3>
Is the video captured through a camera (real or simulated) with physically realistic lighting, but with an environment that is ambiguous, transitions between indoors and outdoors, or cannot be reliably determined?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene type unclear, ambiguous, or changing throughout the video (e.g., transitions between indoor and outdoor, or the setting is difficult to determine)?

- Does the video contain mixed or unclear environments?

- Is the scene type inconsistent, changing between different settings?

- Does the video transition between interior and exterior shots?

- Is it difficult to determine whether the scene is indoors or outdoors?

- Does the setting lack clear spatial context?

- Is the background too abstract or stylized to determine a concrete location?

- Does the video feature multiple environments without a dominant one?

- Is the scene composition too complex to categorize simply?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is captured through a camera (real or simulated) with physically realistic lighting, but whether it is indoors or outdoors is unclear or changes during the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The scene type is unclear, ambiguous, or changing throughout the video (e.g., transitions between indoor and outdoor, or the setting is difficult to determine).

- A video where the scene type is hard to categorize.

- A shot where the setting changes between indoor and outdoor.

- A sequence with an unclear or shifting environment.

- A video where the background lacks a clear spatial definition.

- A scene where the location is ambiguous or abstract.

- A shot with inconsistent or mixed spatial elements.

- A video where no dominant environment is clear.

- A setting that cannot be classified as purely interior, exterior, or synthetic.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.scene_type_is_unclear_or_changing is True</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.scene_type_is_unclear_or_changing is False</code>

</details>
