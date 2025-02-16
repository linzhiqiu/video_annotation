# Start_with Overview

<details>
<summary><h2>Height Wrt Subject Start With Above Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_start_with_above_subject</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned noticeably higher than the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with the camera above the subject?

- Is the starting frame showing the subject from a higher perspective?

- Does the video start with a high camera position relative to the subject?

- Is the initial shot taken from above the subject?

- Does the sequence start with the camera looking down at the subject?

- Is the first shot framed from an elevated position above the subject?

- Does the video open with the subject framed from above?

- Is the starting frame taken from a noticeably higher position than the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that starts with the camera positioned above the subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with the camera above the subject.

- A video that opens with a high-angle perspective on the subject.

- A sequence beginning with the camera looking down at the subject.

- A shot where the subject is framed from a noticeably higher viewpoint.

- A video that starts with a downward-looking camera angle on the subject.

- A shot where the subject is viewed from an elevated position.

- A sequence beginning with the subject framed from a high perspective.

- A video opening with an overhead or high-angle framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'above_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['above_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject Start With At Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_start_with_at_subject</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned at the same height as the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with the camera level with the subject?

- Is the starting frame showing the subject at eye level?

- Does the video start with the camera at the subject’s height?

- Is the initial shot taken from an eye-level perspective?

- Does the sequence start with the camera positioned at subject level?

- Is the first shot framed at the same height as the subject?

- Does the video open with the subject viewed from a neutral angle?

- Is the starting frame taken with the camera at the subject’s natural perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that starts with the camera positioned at the subject’s height.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with the camera at the subject’s level.

- A video that opens with an eye-level perspective on the subject.

- A sequence beginning with the subject viewed from a neutral height.

- A shot where the subject is framed at the same height as the camera.

- A video that starts with a straight-on perspective at the subject’s eye level.

- A shot where the subject appears naturally framed from the camera’s height.

- A sequence beginning with the subject viewed from an at-subject position.

- A video opening with a neutral-height framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'at_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['at_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject Start With Below Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_start_with_below_subject</code>


<h3>📖 Definition:</h3>
Does the video start with the camera positioned below the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot start with the camera below the subject?

- Is the starting frame showing the subject from a lower perspective?

- Does the video start with the camera positioned lower than the subject?

- Is the initial shot taken from a low angle looking up at the subject?

- Does the sequence start with the camera at a lower position than the subject?

- Is the first shot framed from below the subject’s eye level?

- Does the video open with the subject appearing larger due to a low camera angle?

- Is the starting frame taken from a noticeably lower position than the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that starts with the camera positioned below the subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot starting with the camera below the subject.

- A video that opens with a low-angle perspective on the subject.

- A sequence beginning with the camera looking up at the subject.

- A shot where the subject is framed from a noticeably lower viewpoint.

- A video that starts with an upward-looking camera angle on the subject.

- A shot where the subject appears taller due to the low perspective.

- A sequence beginning with the subject framed from a lower vantage point.

- A video opening with an upward-framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'below_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['below_subject', 'unknown']</code>

</details>
