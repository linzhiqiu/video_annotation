# Scene_movement Overview

<details>
<summary><h2>Dynamic Scene</h2></summary>


<h3>🔵 Label Name:</h3>
<code>dynamic_scene</code>


<h3>📖 Definition:</h3>
Is the scene in the video dynamic?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the video feature a dynamic, moving scene?

- Are there objects moving in the scene?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there moving objects in the scene?

- Is the environment in the video changing dynamically?

- Does the frame contain moving elements?

- Are people, vehicles, or objects in motion?

- Is there a lot of movement happening in the scene?

- Does the shot contain visible object motion?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the scene is dynamic and features movement.

- A video where multiple objects in the scene move independently.

- A shot where the environment does not remain static.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where motion occurs naturally within the frame.

- A video where the scene contains multiple moving objects.

- A video where the scene is not static and contains movement.

- A shot where various objects in the frame are moving.

- A scene where the environment appears active.

- A video where there are moving people, vehicles, or objects.

- A shot that features a lively and dynamic setting.

- A video where the objects in the scene continuously move.

- A scene where movement is apparent in the composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.dynamic_scene is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.dynamic_scene is False</code>

</details>

<details>
<summary><h2>Mostly Static Scene</h2></summary>


<h3>🔵 Label Name:</h3>
<code>mostly_static_scene</code>


<h3>📖 Definition:</h3>
Is the scene in the video mostly static with minimal movement?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the video feature a primarily still scene with minor motion?

- Is the scene mostly still without motion?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there small, infrequent movements in an otherwise static scene?

- Is the scene almost completely still but not entirely?

- Does the scene contain occasional minor movement?

- Are there small, subtle movements in the frame?

- Is the environment largely static with only slight motion?

- Does the shot contain minimal but noticeable object motion?

- Is the movement in the scene limited and infrequent?

- Are only a few objects moving slightly while the rest remain still?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the scene is mostly static with minimal movement.

- A shot where the scene is primarily motionless.

- A video where the scene is mostly still without motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where most of the frame remains still with some minor movement.

- A video where movement is minimal but present.

- A shot where a mostly static environment contains occasional motion.

- A scene where objects are largely still but not entirely motionless.

- A video where only a few elements shift while the rest remain still.

- A shot where subtle movements exist in an otherwise still scene.

- A video where minor object motion is present in a mostly static setting.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.mostly_static_scene is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.mostly_static_scene is False</code>

</details>

<details>
<summary><h2>Static Scene</h2></summary>


<h3>🔵 Label Name:</h3>
<code>static_scene</code>


<h3>📖 Definition:</h3>
Is the scene in the video completely static?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the scene in the video completely static, aside from potential camera movement?

- Does the video feature a static, unmoving scene?

- Is everything in the scene still, aside from potential camera motion?

- Are there no objects moving in the scene, despite any camera motion?

- Is the scene static, with no movement apart from the camera?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there no movement in the scene itself?

- Does the scene contain no dynamic motion?

- Is everything in the frame motionless?

- Is the environment completely still?

- Does nothing move within the scene, aside from the camera?

- Is the scene entirely devoid of moving elements?

- Is the content of the scene static while the camera moves?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the scene is completely static.

- A video where the scene remains still, with no movement except for possible camera motion.

- A shot where everything in the scene remains motionless.

- A scene where no objects move, despite any camera motion.

- A video where the environment is entirely still.

- A video with a completely still scene.

- A shot where the scene stays fixed while the camera may move.

- A video where the environment stays motionless.

- A scene where nothing moves apart from the potential camera's motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where nothing within the frame moves.

- A scene where no elements exhibit motion.

- A video where the content remains static.

- A shot where the objects in the scene do not move.

- A scene where there is no dynamic motion within the frame.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.static_scene is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.static_scene is False</code>

</details>
