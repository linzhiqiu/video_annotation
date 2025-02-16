# End_with Overview

<details>
<summary><h2>Height Wrt Subject End With Above Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_end_with_above_subject</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned above the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera positioned higher than the subject?

- Is the ending frame showing the subject from an elevated position?

- Does the video finish with a high-angle perspective of the subject?

- Is the final shot framed from above the subject?

- Does the sequence conclude with the camera looking down at the subject?

- Is the last shot positioned at a noticeably higher level than the subject?

- Does the video close with an overhead or high-angle framing of the subject?

- Is the ending frame taken from a noticeably higher position than the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with the camera positioned above the subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with the camera above the subject.

- A video concluding with a high-angle perspective.

- A sequence ending with the camera looking down at the subject.

- A shot where the subject is framed from an elevated viewpoint.

- A video finishing with a downward-looking camera angle.

- A shot where the subject appears smaller due to the camera’s high position.

- A sequence concluding with the subject framed from a high perspective.

- A video closing with an overhead or high-angle framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] == 'above_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] not in ['above_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject End With At Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_end_with_at_subject</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned at the same height as the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera level with the subject?

- Is the ending frame showing the subject at eye level?

- Does the video finish with the camera at the subject’s height?

- Is the final shot taken from an eye-level perspective?

- Does the sequence conclude with the camera positioned at subject level?

- Is the last shot framed at the same height as the subject?

- Does the video close with the subject viewed from a neutral angle?

- Is the ending frame taken with the camera at the subject’s natural perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with the camera positioned at the subject’s height.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with the camera at the subject’s level.

- A video that concludes with an eye-level perspective on the subject.

- A sequence ending with the subject viewed from a neutral height.

- A shot where the subject is framed at the same height as the camera.

- A video that finishes with a straight-on perspective at the subject’s eye level.

- A shot where the subject appears naturally framed from the camera’s height.

- A sequence ending with the subject viewed from an at-subject position.

- A video closing with a neutral-height framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] == 'at_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] not in ['at_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject End With Below Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_end_with_below_subject</code>


<h3>📖 Definition:</h3>
Does the video end with the camera positioned below the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot end with the camera positioned lower than the subject?

- Is the ending frame showing the subject from a low-angle perspective?

- Does the video finish with the camera at a noticeably lower position than the subject?

- Is the final shot framed from below, looking up at the subject?

- Does the sequence conclude with the subject appearing larger due to the low camera angle?

- Is the last shot taken from a lower elevation relative to the subject?

- Does the video close with the subject viewed from a low vantage point?

- Is the ending frame captured from an upward-looking perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with the camera positioned below the subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot ending with the camera below the subject.

- A video that concludes with a low-angle perspective of the subject.

- A sequence ending with the subject viewed from a lower position.

- A shot where the subject appears larger due to the low perspective.

- A video that finishes with an upward-looking camera angle.

- A shot where the subject is framed from a noticeably lower viewpoint.

- A sequence concluding with the subject framed from a low perspective.

- A video closing with an upward-framing of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] == 'below_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['end'] not in ['below_subject', 'unknown']</code>

</details>
