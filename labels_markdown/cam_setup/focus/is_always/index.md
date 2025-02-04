# Is_always Overview

<details>
<summary><h2>Focus Is Background</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_is_background</code>


<h3>📖 Definition:</h3>
Is the video consistently focused on the background using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video maintain a sharp focus on the background throughout?

- Is the background the primary focus for the entire video?

- Does the depth of field keep the background clear while blurring the foreground?

- Is the focus centered on the background without shifting?

- Does the sequence emphasize the background using selective focus?

- Is the background clearly framed as the focal area in every shot?

- Does the video consistently highlight the background while blurring the foreground?

- Is the entire video composed with a strong background focus?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video remains focused on the background using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining sharp focus on the background throughout.

- A video consistently emphasizing the background with selective focus.

- A sequence where the background is clear while the foreground is blurred.

- A shot keeping the background as the focal plane without shifting.

- A video that consistently isolates the background as the main focus.

- A scene where selective focus highlights only the background.

- A video maintaining a depth of field that prioritizes the background.

- A composition where the foreground remains blurred while the background stays in sharp focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_info['start'] == 'background' and self.focus_info['end'] == 'background'</code>

<h4>🔴 Negative:</h4>
<code>not (self.focus_info['start'] in ['background', 'unknown'] and self.focus_info['end'] in ['background', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Is Foreground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_is_foreground</code>


<h3>📖 Definition:</h3>
Is the video consistently focused on the foreground using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video maintain a sharp focus on the foreground throughout?

- Is the foreground the primary focus for the entire video?

- Does the depth of field keep the foreground clear while blurring the background?

- Is the subject in the foreground emphasized through selective focus?

- Does the focus remain on the foreground without shifting?

- Is the entire sequence framed with a strong foreground focus?

- Does the video consistently highlight the foreground as the focal area?

- Is the foreground isolated in sharp focus across the video?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video remains focused on the foreground using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining a sharp foreground focus throughout.

- A video consistently emphasizing the foreground with shallow depth of field.

- A sequence where the foreground is clear while the background is blurred.

- A shot keeping the foreground as the focal plane without shifting.

- A video that consistently isolates the foreground as the main focus.

- A scene where selective focus highlights only the foreground.

- A video maintaining a depth of field that prioritizes the foreground.

- A composition where the background remains blurred while the foreground is in sharp focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_info['start'] == 'foreground' and self.focus_info['end'] == 'foreground'</code>

<h4>🔴 Negative:</h4>
<code>not (self.focus_info['start'] in ['foreground', 'unknown'] and self.focus_info['end'] in ['foreground', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Is Middle Ground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_is_middle_ground</code>


<h3>📖 Definition:</h3>
Is the video consistently focused on the middle ground, keeping the foreground and background blurred?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video maintain a sharp focus on the middle ground throughout?

- Is the middle ground the primary focus for the entire video?

- Does the depth of field keep the middle ground clear while blurring other elements?

- Is the focus centered on the middle ground without shifting?

- Does the sequence emphasize the middle ground using selective focus?

- Is the middle ground clearly framed as the focal area in every shot?

- Does the video consistently highlight the middle ground while blurring the rest?

- Is the entire video composed with a strong middle ground focus?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video remains focused on the middle ground, with the foreground and background blurred.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining sharp focus on the middle ground throughout.

- A video consistently emphasizing the middle ground with selective focus.

- A sequence where the middle ground is clear while the foreground and background are blurred.

- A shot keeping the middle ground as the focal plane without shifting.

- A video that consistently isolates the middle ground as the main focus.

- A scene where selective focus highlights only the middle ground.

- A video maintaining a depth of field that prioritizes the middle ground.

- A composition where both the foreground and background remain blurred while the middle ground stays in sharp focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_info['start'] == 'middle_ground' and self.focus_info['end'] == 'middle_ground'</code>

<h4>🔴 Negative:</h4>
<code>not (self.focus_info['start'] in ['middle_ground', 'unknown'] and self.focus_info['end'] in ['middle_ground', 'unknown'])</code>

</details>

<details>
<summary><h2>Focus Is Out of Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_is_out_of_focus</code>


<h3>📖 Definition:</h3>
Is the video consistently out of focus throughout?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video remain entirely blurred from start to finish?

- Is the focus unclear for the entire duration of the video?

- Does the depth of field fail to establish a sharp subject throughout?

- Is there no clearly focused area in the entire sequence?

- Does the video maintain an unfocused appearance without transition?

- Is every frame lacking a distinct point of focus?

- Does the video stay blurry across the entire duration?

- Is the entire video composed without a clear focal point?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video remains out of focus throughout.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot maintaining an unfocused appearance from start to finish.

- A video where no clear subject is sharply in focus.

- A sequence that stays blurry throughout.

- A shot where depth of field does not establish a clear focal plane.

- A video that remains in soft focus or lacks a defined sharpness.

- A scene where everything remains blurred without a shift in focus.

- A video that does not provide a distinct point of sharp focus.

- A composition that is consistently out of focus across its duration.

</details>

<h4>🟢 Positive:</h4>
<code>self.focus_info['start'] == 'out_of_focus' and self.focus_info['end'] == 'out_of_focus'</code>

<h4>🔴 Negative:</h4>
<code>not (self.focus_info['start'] in ['out_of_focus', 'unknown'] and self.focus_info['end'] in ['out_of_focus', 'unknown'])</code>

</details>
