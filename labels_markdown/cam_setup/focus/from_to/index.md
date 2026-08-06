# From_to Overview

<details>
<summary><h2>Focus Shifts from Background to Foreground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_background_to_foreground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the background and then shift the focus to the foreground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from the background to the foreground?

- Is there a focus shift where the background starts sharp and then the foreground becomes clear?

- Does the camera begin with a sharp background before adjusting to the foreground?

- Is the initial shot focused on the background before refocusing on the foreground?

- Does the sequence open with a clear background but then shift focus to the foreground?

- Is the focus deliberately moved from the background to the foreground?

- Does the shot gradually shift from the background to bring the foreground into focus?

- Is there a clear transition where the background blurs while the foreground sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the background and then shifts the focus to the foreground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The camera's focus moves from the background to the foreground.

- A scene that begins with a sharp background and then transitions to the foreground.

- A shot where the background is in focus first, but the foreground becomes clearer.

- The camera's depth of field shifts from the background to the foreground.

- A sequence where the focus transitions from a distant subject to the foreground.

- A shot where the background starts in focus but gradually fades out while the foreground sharpens.

- The camera showing a deliberate shift in focus from background to foreground.

- A scene where the focus transitions smoothly from background to foreground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'background' and self.cam_setup.focus_info['end'] == 'foreground' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['background', 'unknown'] and self.cam_setup.focus_info['end'] in ['foreground', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Shifts from Background to Middle Ground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_background_to_middle_ground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the background and then shift the focus to the middleground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from the background to the middle ground?

- Is there a focus shift where the background starts sharp and then the middle ground becomes clear?

- Does the video begin with a sharp background before adjusting to the middle ground?

- Is the initial shot focused on the background before refocusing on the middle ground?

- Does the sequence open with a clear background but then shift focus to the middle ground?

- Is the focus deliberately moved from the background to the middle ground?

- Does the shot gradually shift from the background to bring the middle ground into focus?

- Is there a clear transition where the background blurs while the middle ground sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the background and then shifts the focus to the middleground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the focus moves from the background to the middle ground.

- A scene that begins with a sharp background and then transitions to the middle ground.

- A shot where the background is in focus first, but the middle ground becomes clearer.

- A video where the depth of field shifts from the background to the middle ground.

- A sequence where the focus transitions from a distant subject to the middle ground.

- A shot where the background starts in focus but gradually fades out while the middle ground sharpens.

- A video showing a deliberate shift in focus from background to middle ground.

- A scene where the focus transitions smoothly from background to middle ground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'background' and self.cam_setup.focus_info['end'] == 'middle_ground' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['background', 'unknown'] and self.cam_setup.focus_info['end'] in ['middle_ground', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Shifts from Foreground to Background</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_foreground_to_background</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the foreground and then shift the focus to the background?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from a sharp foreground to a sharp background?

- Is there a shift in focus from the foreground to the background over time?

- Does the video begin with the foreground in focus before changing to the background?

- Is the initial shot focusing on the foreground before transitioning to the background?

- Does the sequence open with a foreground subject in focus before shifting to the background?

- Is the focus deliberately moved from the foreground to the background?

- Does the shot gradually refocus from a nearby subject to a distant background?

- Is there a clear depth transition where the foreground blurs while the background sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the foreground and then shifts the focus to the background.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the focus moves from the foreground to the background.

- A scene that begins with the foreground in sharp focus and transitions to the background.

- A shot that starts with a foreground subject in focus before shifting to the background.

- A video where the depth of field gradually changes from the foreground to the background.

- A sequence where the focus transitions from a near subject to a distant background.

- A shot where the foreground starts in focus and later becomes blurred while the background sharpens.

- A video demonstrating a clear shift in focus from foreground to background.

- A scene where the depth transitions as the focus moves from foreground to background.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'foreground' and self.cam_setup.focus_info['end'] == 'background' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['foreground', 'unknown'] and self.cam_setup.focus_info['end'] in ['background', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Shifts from Foreground to Middle Ground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_foreground_to_middle_ground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the foreground and then shift the focus to the middleground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from a sharp foreground to a sharp middle ground?

- Is there a shift in focus from the foreground to the middle ground over time?

- Does the video begin with the foreground in focus before changing to the middle ground?

- Is the initial shot focusing on the foreground before transitioning to the middle ground?

- Does the sequence open with a foreground subject in focus before shifting to the middle ground?

- Is the focus deliberately moved from the foreground to the middle ground?

- Does the shot gradually refocus from a nearby subject to a middle ground position?

- Is there a clear depth transition where the foreground blurs while the middle ground sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the foreground and then shifts the focus to the middleground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the focus moves from the foreground to the middle ground.

- A scene that begins with the foreground in sharp focus and transitions to the middle ground.

- A shot that starts with a foreground subject in focus before shifting to the middle ground.

- A video where the depth of field gradually changes from the foreground to the middle ground.

- A sequence where the focus transitions from a near subject to a middle ground.

- A shot where the foreground starts in focus and later becomes blurred while the middle ground sharpens.

- A video demonstrating a clear shift in focus from foreground to middle ground.

- A scene where the depth transitions as the focus moves from foreground to middle ground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'foreground' and self.cam_setup.focus_info['end'] == 'middle_ground' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['foreground', 'unknown'] and self.cam_setup.focus_info['end'] in ['middle_ground', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Shifts from Middle Ground to Background</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_middle_ground_to_background</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the middle ground and then shift the focus to the background?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from the middle ground to the background?

- Is there a focus shift where the middle ground starts sharp and then the background becomes clear?

- Does the video begin with a sharp middle ground before adjusting to the background?

- Is the initial shot focused on the middle ground before refocusing on the background?

- Does the sequence open with a clear middle ground but then shift focus to the background?

- Is the focus deliberately moved from the middle ground to the background?

- Does the shot gradually shift from the middle ground to bring the background into focus?

- Is there a clear transition where the middle ground blurs while the background sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the middle ground and then shifts the focus to the background.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the focus moves from the middle ground to the background.

- A scene that begins with a sharp middle ground and then transitions to the background.

- A shot where the middle ground is in focus first, but the background becomes clearer.

- A video where the depth of field shifts from the middle ground to the background.

- A sequence where the focus transitions from a mid-range subject to the background.

- A shot where the middle ground starts in focus but gradually fades out while the background sharpens.

- A video showing a deliberate shift in focus from middle ground to background.

- A scene where the focus transitions smoothly from middle ground to background.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'middle_ground' and self.cam_setup.focus_info['end'] == 'background' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['middle_ground', 'unknown'] and self.cam_setup.focus_info['end'] in ['background', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Shifts from Middle Ground to Foreground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_from_middle_ground_to_foreground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focused on the middle ground and then shift the focus to the foreground?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the focus transition from the middle ground to the foreground?

- Is there a focus shift where the middle ground starts sharp and then the foreground becomes clear?

- Does the video begin with a sharp middle ground before adjusting to the foreground?

- Is the initial shot focused on the middle ground before refocusing on the foreground?

- Does the sequence open with a clear middle ground but then shift focus to the foreground?

- Is the focus deliberately moved from the middle ground to the foreground?

- Does the shot gradually shift from the middle ground to bring the foreground into focus?

- Is there a clear transition where the middle ground blurs while the foreground sharpens?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focused on the middle ground and then shifts the focus to the foreground.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the focus moves from the middle ground to the foreground.

- A scene that begins with a sharp middle ground and then transitions to the foreground.

- A shot where the middle ground is in focus first, but the foreground becomes clearer.

- A video where the depth of field shifts from the middle ground to the foreground.

- A sequence where the focus transitions from the middle ground to the foreground.

- A shot where the middle ground starts in focus but gradually fades out while the foreground sharpens.

- A video showing a deliberate shift in focus from middle ground to foreground.

- A scene where the focus transitions smoothly from middle ground to foreground.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'middle_ground' and self.cam_setup.focus_info['end'] == 'foreground' and self.cam_setup.is_rack_pull_focus is True</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.focus_info['start'] in ['middle_ground', 'unknown'] and self.cam_setup.focus_info['end'] in ['foreground', 'unknown'])</code>

</details>
