# Shot_size Overview

<details>
<summary><h2>Is Shot Size Applicable</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_shot_size_applicable</code>


<h3>📖 Definition:</h3>
Is shot size classification possible for this video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Can the shot size be meaningfully categorized?

- Is it possible to determine the shot size?

- Is the shot size clear enough to classify?

- Is it feasible to determine the shot size?

- Can we meaningfully analyze the shot size?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the shot size can be meaningfully determined.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The shot size can be meaningfully categorized.

- It is possible to determine the shot size.

- The shot size is clear enough to classify.

- It is feasible to determine the shot size.

- We can meaningfully analyze the shot size.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_shot_size_applicable is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_shot_size_applicable is False</code>

</details>

<details>
<summary><h2>Shot Size Change</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_change</code>


<h3>📖 Definition:</h3>
Does the shot size change throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot size vary throughout the video?

- Are there changes in shot size during the video?

- Does the video feature shifts in shot size?

- Is the shot size inconsistent across the video?

- Does the shot size change dynamically throughout the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The shot size changes throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The shot size varies throughout the video.

- There are changes in shot size throughout the video.

- The video features shifts in shot size.

- The shot size is not consistent across the video.

- Throughout the video, the shot size changes dynamically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_change is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_change is False</code>

</details>

<details>
<summary><h2>Shot Size Change From Large To Small</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_change_from_large_to_small</code>


<h3>📖 Definition:</h3>
Does the shot size change from large to small?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move from a wide to a tighter shot?

- Does the framing become more constrained over time?

- Is there a progression from wide to tight framing?

- Does the shot narrow its field of view?

- Does the shot size transition from large to small?

- Does the shot size decrease over time?

- Is there a change in shot size from a wide view to a close-up?

- Does the framing shift from a larger to a smaller shot size?

- Does the video tighten from a wide shot to a closer composition?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The shot size transitions from large to small.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from wide to tight framing.

- A shot transitioning to a more focused view.

- A video showing a narrowing perspective.

- A shot with decreasing frame width.

- A video with a contracting frame size.

- The shot size decreases over time.

- The shot size changes from a wide view to a close-up.

- The framing shifts from a larger to a smaller shot size.

- The video tightens from a wide shot to a closer composition.

- The shot gradually or abruptly moves from a broader to a narrower perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_change_from_large_to_small is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_change_from_large_to_small is False</code>

</details>

<details>
<summary><h2>Shot Size Change From Small To Large</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_change_from_small_to_large</code>


<h3>📖 Definition:</h3>
Does the shot size change from small to large?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move from a tight to a wider shot?

- Does the framing become more expansive over time?

- Is there a progression from tight to wide framing?

- Does the shot expand its field of view?

- Does the shot size transition from small to large?

- Does the shot size increase over time?

- Is there a change in shot size from close-up to a wider view?

- Does the framing shift from a smaller to a larger shot size?

- Does the video expand from a tight shot to a wider composition?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The shot size transitions from small to large.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from tight to wide framing.

- A shot transitioning to broader view.

- A video showing expanding perspective.

- A shot with increasing frame width.

- A video with expanding frame size.

- The shot size increases over time.

- The shot size changes from a close-up to a wider view.

- The framing shifts from a smaller to a larger shot size.

- The video expands from a tight shot to a wider composition.

- The shot gradually or abruptly moves from a narrow to a broader perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_change_from_small_to_large is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_change_from_small_to_large is False</code>

</details>

<details>
<summary><h2>Is Subject Disappearing</h2></summary>


<h3>🔵 Label Name:</h3>
<code>subject_disappearing</code>


<h3>📖 Definition:</h3>
Does the main subject disappear from the frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the primary subject leave the frame?

- Is there a moment where the main subject vanishes?

- Does the subject exit from view?

- Is there a planned disappearance of the subject?

- Does the main subject fade from view?

- Is there a point where the subject leaves the shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the main subject disappears or exits from view.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The primary subject leaves the frame.

- There is a moment where the main subject vanishes.

- The subject exits from view.

- The subject disappears from the frame as planned.

- The main subject fades from view.

- There is a point where the subject leaves the shot.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.subject_disappearing is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.subject_disappearing is False</code>

</details>

<details>
<summary><h2>Is Subject Revealing</h2></summary>


<h3>🔵 Label Name:</h3>
<code>subject_revealing</code>


<h3>📖 Definition:</h3>
Does the video include a revealing shot where a subject appears?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a moment where a new subject is revealed?

- Does the video introduce a subject through a revealing shot?

- Does a subject emerge or appear in the shot?

- Does the video show a subject coming into view?

- Does the shot gradually reveal a subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A revealing shot where a subject appears.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- There is a moment where a new subject is revealed.

- The video introduces a subject through a revealing shot.

- A subject emerges or appears in the shot.

- The video shows a subject coming into view.

- The shot gradually reveals a subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.subject_revealing is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.subject_revealing is False</code>

</details>

<details>
<summary><h2>Subject Switch</h2></summary>


<h3>🔵 Label Name:</h3>
<code>subject_switching</code>


<h3>📖 Definition:</h3>
Does the main subject change to another subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a transition between main subjects?

- Does the focus shift from one subject to another?

- Does the shot switch between different subjects?

- Does the primary focus change to a new subject?

- Does the shot change its principal subject to another?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the main subject changes to a different subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- There is a transition between main subjects.

- The focus shifts from one subject to another.

- The shot switches between different subjects.

- The primary focus changes to a new subject.

- The shot changes its principal subject to another.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.subject_switching is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.subject_switching is False</code>

</details>


## Subcategories

- [End_with](./end_with/index.md)
- [Is_always](./is_always/index.md)
- [Start_with](./start_with/index.md)