# Focus Overview

<details>
<summary><h2>Focus Change From Far To Near</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_change_from_far_to_near</code>


<h3>📖 Definition:</h3>
Does the focal plane transition from distant to close?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus shift from far to near objects?

- Is there a focus transition to the foreground?

- Does the sharp focus move toward camera?

- Is there a focus pull from distant to close?

- Does the focus change from background to foreground?

- Is there a shift in focus to closer elements?

- Does the focal point move to nearby objects?

- Is there a focus transition toward foreground?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the focus plane transitions from distant to close.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with focus moving closer.

- A shot transitioning to near focus.

- A video pulling focus to foreground.

- A shot shifting focus inward.

- A video with approaching focus point.

- A shot changing focus to proximity.

- A video with inward focus shift.

- A shot moving focus closer.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_change_from_far_to_near is True</code>

<h4>🔴 Negative:</h4>
<code>self.focus_change_from_far_to_near is False</code>

</details>

<details>
<summary><h2>Focus Change From Near To Far</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_change_from_near_to_far</code>


<h3>📖 Definition:</h3>
Does the focal plane transition from close to distant?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus shift from near to far objects?

- Is there a focus transition to the background?

- Does the sharp focus move away from camera?

- Is there a focus pull from close to distant?

- Is there a shift in focus to farther elements?

- Does the focal point move to distant objects?

- Is there a focus transition toward background?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the focus plane transitions from close to distant.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with focus moving away.

- A shot transitioning to distant focus.

- A video pulling focus to background.

- A shot shifting focus outward.

- A video with retreating focus point.

- A shot changing focus to distance.

- A video with outward focus shift.

- A shot moving focus away.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_change_from_near_to_far is True</code>

<h4>🔴 Negative:</h4>
<code>self.focus_change_from_near_to_far is False</code>

</details>

<details>
<summary><h2>Is Deep Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_deep_focus</code>


<h3>📖 Definition:</h3>
Does the video have a deep depth of field, ensuring distant details remain sharp?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is everything in frame consistently in focus?

- Does the shot maintain sharp focus from near to far?

- Is there clear detail throughout the depth of field?

- Does the video show sharp focus at all distances?

- Is the entire scene consistently sharp?

- Does the shot keep both near and far objects in focus?

- Is there uniform sharpness throughout the frame?

- Does the video maintain focus across all depths?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has a deep depth of field, ensuring distant details remain sharp.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with everything in focus.

- A shot maintaining overall sharpness.

- A video with deep depth of field.

- A shot showing clear detail at all depths.

- A video with uniform focus.

- A shot keeping all planes sharp.

- A video with consistent focus depth.

- A shot with complete scene clarity.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_deep_focus is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_deep_focus is False</code>

</details>

<details>
<summary><h2>Is Focus Applicable</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_focus_applicable</code>


<h3>📖 Definition:</h3>
Is it possible to determine the camera focus properties?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Can the camera's focus characteristics be classified?

- Can we assess the depth of field in this shot?

- Is the focus style clear enough to classify?

- Can the focusing technique be categorized?

- Is it feasible to analyze the focus pattern?

- Can we meaningfully evaluate the focus type?

- Is the focusing method classifiable?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the camera focus characteristics can be meaningfully classified.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with classifiable focus properties.

- A shot with determinable focus style.

- A video where focus technique is apparent.

- A shot with clear focus characteristics.

- A video suitable for focus analysis.

- A shot with analyzable focus method.

- A video with measurable focus properties.

- A shot with definable focus pattern.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_focus_applicable is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_focus_applicable is False</code>

</details>

<details>
<summary><h2>Is Focus Tracking</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_focus_tracking</code>


<h3>📖 Definition:</h3>
Is there focus tracking on a moving subject in the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus follow a moving subject?

- Is there continuous focus on a mobile subject?

- Does the shot maintain focus on moving elements?

- Is there dynamic focus following movement?

- Does the focus adapt to subject motion?

- Is there automated focus following?

- Does the shot track focus with movement?

- Is there responsive focus on motion?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that maintains focus on a subject as it moves through the frame.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with moving subject focus.

- A shot tracking subject movement.

- A video maintaining mobile focus.

- A shot following subject motion.

- A video with dynamic focus tracking.

- A shot adapting to movement.

- A video with continuous focus.

- A shot following moving elements.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_focus_tracking is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_focus_tracking is False</code>

</details>

<details>
<summary><h2>Is Rack Pull Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_rack_pull_focus</code>


<h3>📖 Definition:</h3>
Is rack focus or pull focus used in the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot use deliberate focus transitions?

- Is there intentional shifting of focus planes?

- Does the video employ focus pulling technique?

- Is there controlled change in focal point?

- Does the shot use focus racking effects?

- Is there purposeful focus manipulation?

- Does the video show planned focus shifts?

- Is there deliberate refocusing in the shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot using rack focus or pull focus techniques to shift the focus plane.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with deliberate focus changes.

- A shot using focus transition effects.

- A video featuring focus manipulation.

- A shot with controlled focus shifts.

- A video employing rack focus.

- A shot showing planned refocusing.

- A video with intentional focus pulls.

- A shot using focus racking technique.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_rack_pull_focus is False</code>

</details>

<details>
<summary><h2>Is Shallow Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_shallow_focus</code>


<h3>📖 Definition:</h3>
Is the camera using a shallow depth of field with limited focus range?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot have a limited focus range?

- Is there selective focus in the frame?

- Does the video show background blur?

- Is the depth of field intentionally narrow?

- Does the shot emphasize one plane of focus?

- Is there distinct separation between sharp and soft areas?

- Does the video use selective sharpness?

- Is the focus deliberately limited in depth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot using shallow depth of field, with limited range of focus.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with selective focus.

- A shot showing background blur.

- A video with narrow depth of field.

- A shot emphasizing focal plane.

- A video with limited focus range.

- A shot using focus separation.

- A video with intentional blur.

- A shot with controlled focus depth.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_shallow_focus is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_shallow_focus is False</code>

</details>

<details>
<summary><h2>Is Ultra Shallow Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_ultra_shallow_focus</code>


<h3>📖 Definition:</h3>
Does the video have an extremely shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the focus range extremely narrow?

- Does the shot show extreme background blur?

- Is there a dramatically thin plane of focus?

- Does the video use extreme selective focus?

- Is the depth of field exceptionally shallow?

- Does the shot have minimal focus depth?

- Is there intense separation of focus planes?

- Does the video show extreme focus limitation?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot using extremely shallow depth of field, with a very narrow focus range.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with extremely selective focus.

- A shot showing intense background blur.

- A video with minimal focus depth.

- A shot emphasizing thin focal plane.

- A video with extreme focus limitation.

- A shot using dramatic focus separation.

- A video with intense selective focus.

- A shot with extremely narrow focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.is_ultra_shallow_focus is True</code>

<h4>🔴 Negative:</h4>
<code>self.is_ultra_shallow_focus is False</code>

</details>


## Subcategories

- [End_with](./end_with/index.md)
- [Is_always](./is_always/index.md)
- [Start_with](./start_with/index.md)