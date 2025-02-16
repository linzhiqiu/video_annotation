# End_with Overview

<details>
<summary><h2>Focus End With Background</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_end_with_background</code>


<h3>📖 Definition:</h3>
Does the video end with the background in focus, using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the background as the focal point?

- Is the final frame focused on the background while the foreground is blurred?

- Does the video conclude with the background in sharp focus?

- Is the last shot emphasizing the background through shallow depth of field?

- Does the sequence close with a sharp background and blurred foreground?

- Is the final shot highlighting the background while other elements are softened?

- Does the video close with a clear background focus while the foreground is defocused?

- Is the ending frame framed with a strong background emphasis?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the background in focus, using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with the background in sharp focus.

- A video concluding with the background as the focal plane.

- A sequence that ends with a blurred foreground, keeping the background clear.

- A shot emphasizing the background through selective focus.

- A video closing with a well-defined background while the rest is out of focus.

- A shot where depth of field isolates the background at the end.

- A video ending with the background standing out as the main point of focus.

- A scene that concludes with a sharp background while foreground elements are blurred.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['end'] == 'background'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['end'] not in ['background', 'unknown']</code>

</details>

<details>
<summary><h2>Focus End With Foreground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_end_with_foreground</code>


<h3>📖 Definition:</h3>
Does the video end with the foreground in focus, using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with a sharp focus on the foreground?

- Is the final frame focused on the foreground while the rest is blurred?

- Does the video conclude with only the foreground in clear focus?

- Is the last shot emphasizing the foreground through shallow depth of field?

- Does the sequence close with a blurred background and a focused foreground?

- Is the final shot composed with the foreground in sharp focus?

- Does the video close with a subject in the foreground while the rest is out of focus?

- Is the ending frame framed with a distinct foreground focus?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the foreground in focus, using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with a sharp focus on the foreground.

- A video concluding with the foreground clearly in focus.

- A sequence that ends with a blurred background but sharp foreground.

- A shot emphasizing the foreground while the rest is out of focus.

- A video that closes with a focused foreground and a soft background.

- A shot with shallow depth of field highlighting the foreground at the end.

- A video ending with a strong foreground focus while the background fades.

- A scene that concludes with the subject in the foreground in sharp focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['end'] == 'foreground'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['end'] not in ['foreground', 'unknown']</code>

</details>

<details>
<summary><h2>Focus End With Middle Ground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_end_with_middle_ground</code>


<h3>📖 Definition:</h3>
Does the video end with the middle ground in focus while the foreground and background are blurred?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the middle ground as the focal point?

- Is the final frame focused on the middle ground while the foreground and background are out of focus?

- Does the video conclude with the middle ground in sharp focus?

- Is the last shot emphasizing the middle ground using depth of field?

- Does the sequence close with a sharp middle ground and blurred surroundings?

- Is the final shot highlighting the middle ground while other elements are softened?

- Does the video close with a clear middle-ground focus while the foreground and background are defocused?

- Is the ending frame framed with a strong middle ground emphasis?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with the middle ground in focus, with the foreground and background blurred.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with the middle ground in sharp focus.

- A video concluding with the middle ground as the focal plane.

- A sequence that ends with a blurred foreground and background, keeping the middle ground clear.

- A shot emphasizing the middle ground through selective focus.

- A video closing with a well-defined middle ground while the rest is out of focus.

- A shot where depth of field isolates the middle ground at the end.

- A video ending with the middle ground standing out as the main point of focus.

- A scene that concludes with a sharp middle ground while surroundings are blurred.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['end'] == 'middle_ground'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['end'] not in ['middle_ground', 'unknown']</code>

</details>

<details>
<summary><h2>Focus End With Out of Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_end_with_out_of_focus</code>


<h3>📖 Definition:</h3>
Does the video end completely out of focus?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with a blurred or unfocused frame?

- Is the final frame entirely out of focus?

- Does the video conclude with an indistinct, blurry image?

- Is the last shot lacking a clear focal point due to blur?

- Does the sequence close with no sharp focus?

- Is the final shot completely blurred or unfocused?

- Does the video close with an entirely out-of-focus frame?

- Is the ending frame hazy with no clear subject in focus?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends completely out of focus.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with a blurred, unfocused frame.

- A video concluding with no clear focal point due to blur.

- A sequence ending with an indistinct, out-of-focus image.

- A shot where the entire frame lacks clarity and focus.

- A video that ends with an intentionally unfocused view.

- A shot with no sharpness at the end of the video.

- A video ending with a hazy, unclear frame.

- A scene that closes with a completely blurred composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['end'] == 'out_of_focus'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['end'] not in ['out_of_focus', 'unknown']</code>

</details>
