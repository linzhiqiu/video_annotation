# Shot_size Overview

<details>
<summary><h2>Disappearing Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>disappearing_shot</code>


<h3>📖 Definition:</h3>
Does the main subject disappear from the shot?

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

- Does the primary focus disappear from frame?

- Is there a deliberate removal of the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the main subject disappears or exits from view.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing subject disappearance.

- A shot featuring subject exit.

- A video with planned subject removal.

- A shot showing subject departure.

- A video where the subject leaves view.

- A shot with subject disappearance.

- A video featuring subject exit.

- A shot showing subject removal.

</details>

<h4>🟢 Positive:</h4>
<code>self.disappearing_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.disappearing_shot is False</code>

</details>

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

- Is it possible to determine the shot size classification?

- Can we assess the framing distance in this shot?

- Is the shot size clear enough to classify?

- Can the camera distance be effectively categorized?

- Is it feasible to determine the shot scale?

- Can we meaningfully analyze the shot size?

- Is the framing distance classifiable?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the size classification can be meaningfully determined.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with classifiable shot size.

- A shot with determinable framing distance.

- A video where shot scale can be assessed.

- A shot with clear distance categorization.

- A video suitable for size classification.

- A shot with analyzable framing.

- A video with measurable shot scale.

- A shot with definable camera distance.

</details>

<h4>🟢 Positive:</h4>
<code>self.complex_shot_type != 'unknown' or (self.complex_shot_type == 'description' and self.shot_size_description_type != 'others')</code>

<h4>🔴 Negative:</h4>
<code>not (self.complex_shot_type != 'unknown' or (self.complex_shot_type == 'description' and self.shot_size_description_type != 'others'))</code>

</details>

<details>
<summary><h2>Revealing Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>revealing_shot</code>


<h3>📖 Definition:</h3>
Does the video include a revealing shot where a subject appears?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a moment where a new subject is revealed?

- Does the shot introduce a subject through revelation?

- Is there a dramatic reveal of a subject?

- Does a subject emerge or appear in the shot?

- Is there a planned reveal of a subject?

- Does the video show a subject coming into view?

- Is there a moment where a subject is unveiled?

- Does the shot gradually reveal a subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that includes the revelation or appearance of a subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring a subject reveal.

- A shot showing a subject appearance.

- A video with a dramatic subject introduction.

- A shot containing a planned reveal.

- A video showing subject emergence.

- A shot with a calculated revelation.

- A video featuring subject unveiling.

- A shot with gradual subject appearance.

</details>

<h4>🟢 Positive:</h4>
<code>self.revealing_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.revealing_shot is False</code>

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

- Is there variation in the camera distance?

- Does the framing distance change during the shot?

- Is there a shift in how much of the subject is shown?

- Does the camera move closer or farther from the subject?

- Is there a change in the frame's coverage area?

- Does the shot scale vary throughout?

- Is there alteration in the shot's field of view?

- Does the framing size change during the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that changes in size or scale throughout its duration.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with varying shot sizes.

- A shot showing distance changes.

- A video with dynamic framing.

- A shot featuring scale changes.

- A video with varying camera distances.

- A shot showing size transitions.

- A video with changing frame coverage.

- A shot featuring distance variations.

</details>

<h4>🟢 Positive:</h4>
<code>self.shot_size_change is True</code>

<h4>🔴 Negative:</h4>
<code>self.shot_size_change is False</code>

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

- Does the camera move from a wider to a tighter shot?

- Is there a transition from a broader to a closer view?

- Does the framing become more intimate over time?

- Is there a progression from wide to tight framing?

- Does the shot narrow its field of view?

- Is there a shift from expansive to confined framing?

- Does the camera move in closer to the subject?

- Is there a change from distant to close framing?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that transitions from a larger to a smaller frame size.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from wide to tight framing.

- A shot transitioning to closer view.

- A video showing increasing intimacy.

- A shot with decreasing frame width.

- A video moving closer to subject.

- A shot narrowing its perspective.

- A video with reducing frame size.

- A shot closing in on subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.shot_size_change_from_large_to_small is True</code>

<h4>🔴 Negative:</h4>
<code>self.shot_size_change_from_large_to_small is False</code>

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

- Is there a transition from close-up to broader view?

- Does the framing become more expansive over time?

- Is there a progression from tight to wide framing?

- Does the shot expand its field of view?

- Is there a shift from confined to expansive framing?

- Does the camera pull back from the subject?

- Is there a change from close to distant framing?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that transitions from a smaller to a larger frame size.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video moving from tight to wide framing.

- A shot transitioning to broader view.

- A video showing expanding perspective.

- A shot with increasing frame width.

- A video moving away from subject.

- A shot widening its perspective.

- A video with expanding frame size.

- A shot pulling back from subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.shot_size_change_from_small_to_large is True</code>

<h4>🔴 Negative:</h4>
<code>self.shot_size_change_from_small_to_large is False</code>

</details>

<details>
<summary><h2>Subject Switch</h2></summary>


<h3>🔵 Label Name:</h3>
<code>subject_switch</code>


<h3>📖 Definition:</h3>
Does the main subject change to another subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a transition between main subjects?

- Does the focus shift from one subject to another?

- Is there a change in the primary subject?

- Does the shot switch between different subjects?

- Is there a handoff between main subjects?

- Does the primary focus change to a new subject?

- Is there a transition in the main focus?

- Does the shot change its principal subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the main subject changes to a different subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with subject transition.

- A shot showing subject change.

- A video featuring focus shift.

- A shot with subject handoff.

- A video showing main subject change.

- A shot transitioning between subjects.

- A video with focus transition.

- A shot changing primary subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.subject_switch is True</code>

<h4>🔴 Negative:</h4>
<code>self.subject_switch is False</code>

</details>
