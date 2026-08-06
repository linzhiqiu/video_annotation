# From_to Overview

<details>
<summary><h2>Height Wrt Subject From Above Subject To At Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_above_subject_to_at_subject</code>


<h3>📖 Definition:</h3>
Does the camera start noticeably higher than the subject and then move down to their height?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from a high-angle to an eye-level perspective?

- Does the camera descend from above the subject to their height level?

- Does the camera start above the subject and move down to their eye level?

- Does the framing change from looking down at the subject to being level with them?

- Does the camera position shift from above the subject to their height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts noticeably higher than the subject and then moves down to their height.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from a high-angle to an eye-level perspective.

- A sequence where the camera descends from above the subject to their height.

- A video showing the camera moving from a higher position to the subject's level.

- A shot that changes from looking down at the subject to being level with them.

- A camera movement descending from above the subject to their height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'above_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'at_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['above_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['at_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject From Above Subject To Below Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_above_subject_to_below_subject</code>


<h3>📖 Definition:</h3>
Does the camera start noticeably higher than the subject and then move down to a position below them?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from looking down at the subject to looking up at them?

- Does the camera descend from above the subject to a low position looking upward?

- Does the camera move from a high vantage point to below the subject's level?

- Does the framing change from a downward view to an upward view of the subject?

- Does the camera shift from an overhead position to a low angle beneath the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts noticeably higher than the subject and then moves down to a position below them.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from looking down at the subject to looking up at them.

- A sequence where the camera descends from above to below the subject.

- A video showing the camera moving from a high position to a low angle.

- A shot that changes from an overhead view to an upward view.

- A camera movement going from above the subject to beneath them.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'above_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'below_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['above_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['below_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject From At Subject To Above Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_at_subject_to_above_subject</code>


<h3>📖 Definition:</h3>
Does the camera start at the same height as the subject and then move up to a higher position than them?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from an eye-level view to looking down at the subject?

- Does the camera rise from the subject's level to a position above them?

- Does the camera move from being level with the subject to an elevated viewpoint?

- Does the framing change from a straight-on view to looking down at the subject?

- Does the camera shift from eye level to a higher vantage point?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts at the same height as the subject and then moves up to a higher position than them.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from an eye-level view to looking down at the subject.

- A sequence where the camera rises from the subject's level to above them.

- A video showing the camera elevating from eye level to a higher position.

- A shot that changes from a straight-on view to an overhead perspective.

- A camera movement ascending from the subject's height to above them.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'at_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'above_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['at_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['above_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject From At Subject To Below Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_at_subject_to_below_subject</code>


<h3>📖 Definition:</h3>
Does the camera start at the same height as the subject and then move down to a lower position than them?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from an eye-level view to looking up at the subject?

- Does the camera descend from the subject's level to a position below them?

- Does the camera move from being level with the subject to a low angle?

- Does the framing change from a straight-on view to looking up at the subject?

- Does the camera shift from eye level to a lower vantage point?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts at the same height as the subject and then moves down to a lower position than them.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from an eye-level view to looking up at the subject.

- A sequence where the camera lowers from the subject's level to below them.

- A video showing the camera moving from eye level to a low angle.

- A shot that changes from a straight-on view to an upward perspective.

- A camera movement descending from the subject's height to a lower position.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'at_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'below_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['at_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['below_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject From Below Subject To Above Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_below_subject_to_above_subject</code>


<h3>📖 Definition:</h3>
Does the camera start below the subject and move up to a position above them?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from looking up at the subject to looking down at them?

- Does the camera rise from a low angle to an elevated position?

- Does the camera move from beneath the subject to above them?

- Does the framing change from an upward view to looking down at the subject?

- Does the camera shift from a low position to a high vantage point?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts below the subject and moves up to a position above them.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from looking up at the subject to looking down at them.

- A sequence where the camera rises from below to above the subject.

- A video showing the camera moving from a low angle to a high position.

- A shot that changes from an upward view to an overhead perspective.

- A camera movement ascending from beneath the subject to above them.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'below_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'above_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['below_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['above_subject', 'unknown']</code>

</details>

<details>
<summary><h2>Height Wrt Subject From Below Subject To At Subject</h2></summary>


<h3>🔵 Label Name:</h3>
<code>height_wrt_subject_from_below_subject_to_at_subject</code>


<h3>📖 Definition:</h3>
Does the camera start below the subject and move up to their height?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot transition from looking up at the subject to a straight-on view?

- Does the camera rise from a low angle to the subject's height?

- Does the camera move from beneath the subject to being level with them?

- Does the framing change from an upward view to an eye-level perspective?

- Does the camera shift from a low position to the subject's height?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera starts below the subject and moves up to their height.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot transitioning from looking up at the subject to a straight-on view.

- A sequence where the camera rises from below to the subject's level.

- A video showing the camera moving from a low angle to eye level.

- A shot that changes from an upward view to a level perspective.

- A camera movement ascending from beneath the subject to their height.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] == 'below_subject' and self.cam_setup.height_wrt_subject_info['end'] == 'at_subject'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.height_wrt_subject_info['start'] not in ['below_subject', 'unknown'] or self.cam_setup.height_wrt_subject_info['end'] not in ['at_subject', 'unknown']</code>

</details>
