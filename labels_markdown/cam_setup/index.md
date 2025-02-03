# Cam_setup Overview

<details>
<summary><h2>Has Overlays</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_overlays</code>


<h3>📖 Definition:</h3>
Does the shot contain on-screen overlays, such as watermarks, or titles, or subtitles, or icons, or heads-up displays, or framing elements?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video have any added text or graphics on the screen?

- Are there watermarks, titles, or subtitles visible in the shot?

- Does this shot contain icons, labels, or other graphical elements?

- Is there a heads-up display or interface overlay present?

- Are there any framing elements like borders or guide markers?

- Does the video include non-diegetic text or symbols on-screen?

- Are any subtitles or captions displayed in the scene?

- Does this shot contain on-screen information not naturally part of the scene?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot containing on-screen overlays, such as watermarks, titles, subtitles, icons, HUDs, or framing elements.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene containing on-screen overlays such as text, graphics, or icons.

- A shot with visible watermarks, titles, or subtitles.

- A video where a heads-up display or user interface is present.

- A frame that includes added graphical elements like icons or labels.

- A shot where on-screen elements are visible, such as subtitles or branding.

- A shot featuring non-diegetic overlays like game HUDs or captions.

- A video containing persistent watermarks or text elements.

- A scene with embedded UI components or informational graphics.

- A shot displaying subtitles or interactive elements.

</details>

<h4>🟢 Positive:</h4>
<code>self.has_overlays is True</code>

<h4>🔴 Negative:</h4>
<code>self.has_overlays is False</code>

</details>

<details>
<summary><h2>Shot transition</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_shot_transition_cam_setup</code>


<h3>📖 Definition:</h3>
Does the video include one or more shot transitions?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the video contain hard cuts or soft transitions, or a combination of both?

- Are there any shot transitions in the video?

- Does this footage feature one or more cuts or soft transitions?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a transition between shots?

- Does the video include a shot transition?

- Does the video include a hard cut or a soft transition?

- Is there a shot transition?

- Is a cut or soft transition used in this footage?

- Does the video include any shot transitions?

- Does the video include a hard cut or a soft transition?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video showing one or more shot transitions.

- The video features hard cuts, soft transitions, or a combination of both.

- The video contains one or more cuts or soft transitions between shots.

- A video that includes at least one shot transition.

- A video with at least one shot transition.

- A video featuring one or more shot transitions.

- A video with one or more shot transitions.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video includes either a hard cut or a soft transition.

- The video shows a hard cut or a soft transition between shots.

- A video where there is a transition between shots.

- The video contains a cut or a soft transition between scenes.

- A video that includes shot transitions between scenes.

- A video with a hard cut or soft transition.

- A video that includes a shot transition.

- A video with a cut or soft transition.

- A video featuring shot transitions.

- A video with either a hard cut or soft transition.

- A video with at least one transition.

- A video with shot transitions.

- A video with cuts or soft transitions.

- A video with hard cuts, soft transitions, or both.

- A video where shots change with a transition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_transition</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_setup.shot_transition</code>

</details>


## Subcategories

- [Lens_distortion](./lens_distortion/index.md)
- [Point_of_view](./point_of_view/index.md)
- [Shot_type](./shot_type/index.md)
- [Video_speed](./video_speed/index.md)