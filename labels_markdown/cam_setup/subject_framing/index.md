# Subject_framing Overview

<details>
<summary><h2>Has Many Subjects</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_many_subjects</code>


<h3>📖 Definition:</h3>
Does the video contain multiple subjects or multiple groups of subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there several distinct subjects present in the video?

- Does the shot feature multiple different subjects or groups?

- Can you identify more than one main subject in the frame?

- Does the video show various subjects or subject groups?

- Are multiple subjects visible throughout the shot?

- Does the frame contain several different subjects?

- Is there more than one subject group in the video?

- Are there multiple distinct elements or subjects to focus on?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot containing multiple subjects or multiple groups of subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring several distinct subjects.

- A shot showing multiple subject groups.

- A video with various subjects in frame.

- A shot containing multiple focal subjects.

- A video displaying several different subjects.

- A shot with multiple subject elements.

- A video presenting various subject groups.

- A shot featuring multiple distinct subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.has_many_subjects is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.has_many_subjects is False</code>

</details>

<details>
<summary><h2>Has Single Dominant Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_single_dominant_subject</code>


<h3>📖 Definition:</h3>
Is there a single dominant subject or group of subjects in the frame throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does one main subject or group dominate the frame throughout?

- Is there a primary subject that remains dominant in the video?

- Does a single subject or group stand out as the main focus?

- Is the video primarily focused on one dominant subject?

- Can you identify a single main subject throughout the shot?

- Does one subject or group clearly command more attention?

- Is there a clear primary subject maintained throughout?

- Does the video emphasize one particular subject or group?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that maintains focus on a single dominant subject or group of subjects throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video centered on one main subject or group.

- A shot where a single subject clearly dominates the frame.

- A video maintaining focus on one primary subject.

- A shot emphasizing a single dominant subject group.

- A video where one subject commands primary attention.

- A shot consistently featuring one main subject.

- A video focused on a single primary subject or group.

- A shot where one subject remains the clear focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.has_single_dominant_subject is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.has_single_dominant_subject is False</code>

</details>

<details>
<summary><h2>Has Subject Change</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_subject_change</code>


<h3>📖 Definition:</h3>
Does the subject change in the video, such as in a revealing shot where a subject appears, disappears, or transitions to another subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there any transitions between different subjects in this video?

- Does the video show any subject appearing or disappearing from view?

- Is there a shift or change in the main subject during the video?

- Does the focus transition from one subject to another?

- Are there moments where new subjects enter or existing ones leave?

- Does the video include any revealing or concealing of subjects?

- Is there a handoff or switch between different subjects?

- Does the video's subject matter change during its duration?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the subject changes, including appearances, disappearances, or transitions between subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring transitions between different subjects.

- A shot where subjects enter or leave the frame.

- A video showing clear changes in its main subject.

- A shot demonstrating subject transitions or reveals.

- A video where the focus shifts between different subjects.

- A shot containing subject appearances or disappearances.

- A video with dynamic changes in subject matter.

- A shot showing deliberate subject transitions.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.has_subject_change is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.has_subject_change is False</code>

</details>

<details>
<summary><h2>Is Framing Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_framing_subject</code>


<h3>📖 Definition:</h3>
Does the video include one or more subjects in the frame at any point, instead of just a scenery shot with no clear subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video keep its subject(s) properly framed throughout?

- Is there consistent framing of the main subject(s) in this shot?

- Are the subjects maintained within the frame's composition throughout the video?

- Does the camera maintain proper composition of the subject(s)?

- Is the framing stable and consistent for the main subject(s)?

- Are the subjects well-positioned within the frame throughout?

- Does the shot maintain its focus on the subject(s) with consistent framing?

- Is there a steady and deliberate framing of the subject(s) in this video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features at least one main subject rather than just a scenery shot.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video that keeps its subjects properly framed from start to finish.

- A shot with consistent and stable framing of its main subjects.

- A video where subjects remain well-positioned within the frame.

- A shot demonstrating deliberate and maintained subject framing.

- A video with careful attention to subject positioning and framing.

- A shot where the camera maintains proper composition of subjects.

- A video showing intentional and steady framing of its subjects.

- A shot with controlled and purposeful subject positioning.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_framing_subject is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_framing_subject is False</code>

</details>
