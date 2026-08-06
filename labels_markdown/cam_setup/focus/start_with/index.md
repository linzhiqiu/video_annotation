# Start_with Overview

<details>
<summary><h2>Focus Start With Background</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_start_with_background</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focusing on the background, using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a focused background and blurred foreground?

- Is the starting frame focused on the background with a shallow depth of field?

- Does the camera begin with the background in sharp focus while other areas are blurred?

- Is the initial shot framed with the background as the focal point?

- Does the sequence open with a background focus and selective blur?

- Is the first shot emphasizing the background while softening other elements?

- Does the camera open with the background clearly in focus?

- Is the starting frame composed to highlight the background?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focusing on the background, using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with the background in focus and a shallow depth of field.

- The camera opening with the background sharp while other areas are softened.

- A sequence beginning with a focused background and blurred surroundings.

- A shot where the background is the focal point with selective focus.

- The camera starts with the background clearly in focus.

- A shot with background emphasis and softened surrounding elements.

- The camera beginning with background clarity and a shallow depth effect.

- A scene that opens with the background as the main focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'background'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['start'] not in ['background', 'unknown']</code>

</details>

<details>
<summary><h2>Focus Start With Foreground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_start_with_foreground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focusing on the foreground, using a shallow depth of field?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a clear focus on the foreground while other areas are blurred?

- Is the starting frame emphasizing foreground elements with a shallow depth of field?

- Does the video begin with a sharp foreground while the middle ground or background is out of focus?

- Is the initial shot captured with a clear foreground subject and a softened depth?

- Does the sequence open with the foreground in focus while other areas appear blurred?

- Is the first shot framed to highlight the foreground using selective focus?

- Does the video open with a foreground focus while creating depth with blur?

- Is the starting frame composed with a crisp foreground while the depth is softened?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focusing on the foreground, using a shallow depth of field.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with a sharp foreground and a blurred depth.

- A video opening with a foreground focus and a shallow depth of field.

- A sequence beginning with the foreground in focus while the background is softened.

- A shot where the foreground is emphasized while the middle or background fades out.

- A video that starts with a foreground subject in sharp focus and a shallow depth of field.

- A shot using selective focus on the foreground while the rest of the scene blurs.

- A video that begins with a crisp foreground and a gradual loss of focus behind it.

- A scene that opens with a sharp foreground and a progressively blurred depth.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'foreground'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['start'] not in ['foreground', 'unknown']</code>

</details>

<details>
<summary><h2>Focus Start With Middle Ground</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_start_with_middle_ground</code>


<h3>📖 Definition:</h3>
Does the video start with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a sharp focus on the middle ground while the foreground and background are blurred?

- Is the starting frame emphasizing the middle ground with a shallow depth of field?

- Does the video begin with a focus on the middle ground while the foreground and background fade out?

- Is the initial shot captured with the middle ground in focus while other areas are blurred?

- Does the sequence open with a balanced focus on the middle ground while surrounding areas lack sharpness?

- Is the first shot framed to highlight the middle ground while the foreground and background remain out of focus?

- Does the video open with selective focus on the middle ground, creating depth?

- Is the starting frame composed with the middle ground in sharp focus while other planes are softened?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera focusing on the middleground, using a shallow depth of field to blur both the foreground and background.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with the middle ground in sharp focus while the surrounding areas blur.

- A video opening with a middle-ground focus and a shallow depth of field.

- A sequence beginning with the middle ground in focus while both foreground and background fade out.

- A shot where the middle ground is emphasized while the other planes remain blurred.

- A video that starts with the middle ground in focus and a selective depth of field.

- A shot using selective focus on the middle ground while the foreground and background are out of focus.

- A video that begins with a sharp middle-ground focus, keeping the other areas soft.

- A scene that opens with a middle-ground subject in focus while the depth gradually blurs.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'middle_ground'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['start'] not in ['middle_ground', 'unknown']</code>

</details>

<details>
<summary><h2>Focus Start With Out of Focus</h2></summary>


<h3>🔵 Label Name:</h3>
<code>focus_start_with_out_of_focus</code>


<h3>📖 Definition:</h3>
Does the video start with the camera completely out of focus?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with a blurred or unfocused frame?

- Is the starting frame entirely out of focus?

- Does the video begin with an indistinct, blurry image?

- Is the initial shot lacking a clear focal point due to blur?

- Does the sequence open with no sharp focus?

- Is the first shot completely blurred or unfocused?

- Does the video open with an entirely out-of-focus frame?

- Is the starting frame hazy with no clear subject in focus?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera completely out of focus.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with a blurred, unfocused frame.

- A video opening with no clear focal point due to blur.

- A sequence beginning with an indistinct, out-of-focus image.

- A shot where the entire frame lacks clarity and focus.

- A video that starts with an intentionally unfocused view.

- A shot with no sharpness at the beginning of the video.

- A video beginning with a hazy, unclear frame.

- A scene that opens with a completely blurred composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.focus_info['start'] == 'out_of_focus'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.focus_info['start'] not in ['out_of_focus', 'unknown']</code>

</details>
