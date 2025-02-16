# Is_always Overview

<details>
<summary><h2>Height Wrt Subject Is Above Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_is_above_subject</code>


<h3>📖 Definition:</h3>
Is the camera positioned noticeably higher than the subject throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain above the subject for the entire video?

- Is the subject consistently framed from a higher perspective?

- Does the video maintain a high camera position relative to the subject?

- Is the shot taken from above the subject throughout the sequence?

- Does the framing stay elevated in relation to the subject?

- Is the subject viewed from a noticeably higher viewpoint for the whole video?

- Does the video consistently present the subject from an overhead or high-angle perspective?

- Is the subject framed from an elevated camera position without transitioning?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains positioned above the subject throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a high-angle perspective on the subject.

- A sequence where the subject is framed from an elevated viewpoint.

- A shot that keeps the camera consistently above the subject.

- A video where the subject is viewed from a higher perspective throughout.

- A scene that remains framed from a noticeably elevated position.

- A shot with the subject appearing lower in the frame throughout the video.

- A video maintaining an overhead or high-angle framing without shifting positions.

- A sequence that keeps the camera looking down at the subject the entire time.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'above_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'above_subject'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_subject_info['start'] in ['above_subject', 'unknown'] and self.cam_setup.height_wrt_subject_info['end'] in ['above_subject', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Subject Is At Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_is_at_subject</code>


<h3>📖 Definition:</h3>
Is the camera positioned at the same height as the subject throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain level with the subject for the entire video?

- Is the subject consistently framed at eye level?

- Does the video maintain the camera at the subject’s height?

- Is the shot taken from an eye-level perspective throughout?

- Does the framing stay at subject level from start to finish?

- Is the subject viewed from a neutral angle for the whole video?

- Does the video consistently present the subject from an at-subject perspective?

- Is the subject framed at the same height as the camera without transitioning?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains positioned at the subject’s height throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining an eye-level perspective on the subject.

- A sequence where the subject is consistently framed at a neutral height.

- A shot that keeps the camera at the subject’s level.

- A video where the subject is viewed from an at-subject perspective throughout.

- A scene that remains framed from a neutral angle.

- A shot with the subject appearing at the same height as the camera throughout.

- A video maintaining a straight-on perspective at subject level.

- A sequence that keeps the camera level with the subject the entire time.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'at_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'at_subject'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_subject_info['start'] in ['at_subject', 'unknown'] and self.cam_setup.height_wrt_subject_info['end'] in ['at_subject', 'unknown'])</code>

</details>

<details>
<summary><h2>Height Wrt Subject Is Below Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_is_below_subject</code>


<h3>📖 Definition:</h3>
Is the camera positioned below the subject throughout the video?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera remain below the subject for the entire video?

- Is the subject consistently framed from a lower perspective?

- Does the video maintain a low-angle shot throughout?

- Is the subject viewed from below from start to finish?

- Does the sequence keep an upward-looking perspective?

- Is the subject presented from a noticeably lower camera height the whole time?

- Does the framing remain below the subject’s eye level?

- Is the entire shot taken from a low-angle viewpoint?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera remains positioned below the subject throughout the video.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video maintaining a low-angle perspective on the subject.

- A sequence where the subject is consistently framed from below.

- A shot that keeps the camera at a lower height than the subject.

- A video where the subject appears taller due to the low perspective throughout.

- A scene that remains framed from an upward-looking angle.

- A shot with the subject consistently appearing above the camera viewpoint.

- A video maintaining an upward-looking perspective for its entire duration.

- A sequence that keeps the camera below the subject the entire time.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'below_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'below_subject'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.height_wrt_subject_info['start'] in ['below_subject', 'unknown'] and self.cam_setup.height_wrt_subject_info['end'] in ['below_subject', 'unknown'])</code>

</details>
