# From_to Overview

<details>
<summary><h2>Camera Angle Shifts from High Angle to Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_high_to_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a high angle and transition to a level angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin with a high-angle view and then shift to a level perspective?

- Is there a camera movement that lowers the angle from high to level?

- Does the video transition from a downward-tilted high angle to a neutral level angle?

- Is the initial shot angled downward before gradually aligning parallel to the ground?

- Does the sequence start with an elevated camera view and then adjust to a straight-on perspective?

- Is there a gradual framing change where the high-angle shot becomes level?

- Does the video shift from a high-angle viewpoint to a more natural, straight-on view?

- Is the starting shot looking down before the camera tilts or moves to a level angle?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a high angle and transitions to a level angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a high angle to a neutral level angle.

- A video where the camera gradually tilts from a downward-facing high angle to a level perspective.

- A sequence beginning with a high-angle shot that transitions to a straight-on view.

- A shot that starts with a downward tilt before settling into a level frame.

- A video showing a smooth transition from a high angle to a neutral viewpoint.

- A scene where the camera shifts from looking downward to a straight-on perspective.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'high_angle' and self.cam_setup.camera_angle_info['end'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['high_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['level_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Shifts from High Angle to Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_high_to_low</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a high angle and transition to a low angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin at a high angle and then tilt or move into a low-angle position?

- Is there a camera movement that lowers the angle dramatically from high to low?

- Does the video transition from a downward-tilted high angle to an upward-looking low angle?

- Is the initial shot framed at a high vantage point before moving below the subject?

- Does the sequence start with a high angle and then adjust into a low viewpoint?

- Is there a clear framing change where the high-angle shot becomes a low-angle shot?

- Does the video shift from looking down to looking up?

- Is the starting shot positioned high before tilting or moving to a lower perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a high angle and transitions to a low angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a high angle to a low angle.

- A video where the camera smoothly tilts from a downward-facing high angle to an upward-facing low angle.

- A sequence beginning with a high-angle shot that transitions to a low-angle shot.

- A shot that starts with a downward tilt before shifting into an upward-facing perspective.

- A video showing a dramatic transition from a high angle to a low-angle viewpoint.

- A scene where the camera moves from looking down to looking up.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'high_angle' and self.cam_setup.camera_angle_info['end'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['high_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['low_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Shifts from Level Angle to High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_level_to_high</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a level angle and transition to a high angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin at a neutral level angle before tilting downward into a high-angle view?

- Is there a camera movement that shifts from a straight-on angle to a high-angle perspective?

- Does the video transition from a balanced level angle to a downward-facing high angle?

- Is the initial shot framed at eye level before the camera moves higher and tilts down?

- Does the sequence start at a neutral angle and then adjust to a high vantage point?

- Is there a gradual framing change where the level angle becomes high?

- Does the video shift from a straight-on viewpoint to a downward-looking high angle?

- Is the starting shot neutral before transitioning to a high, downward-facing position?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a level angle and transitions to a high angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a level angle to a high angle.

- A video where the camera gradually tilts from a straight-on perspective to a downward-looking high angle.

- A sequence beginning with a level shot that transitions to a high vantage point.

- A shot that starts with a neutral angle before raising and tilting downward.

- A video showing a smooth transition from a level angle to a high-angle perspective.

- A scene where the camera shifts from a straight-on view to a downward-tilted framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'level_angle' and self.cam_setup.camera_angle_info['end'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['level_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['high_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Shifts from Level Angle to Low Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_level_to_low</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a level angle and transition to a low angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin at a neutral level angle before tilting upward?

- Is there a camera movement that shifts from a straight-on angle to a low-angle perspective?

- Does the video transition from a balanced level angle to an upward-facing low angle?

- Is the initial shot framed at eye level before moving lower and tilting up?

- Does the sequence start at a neutral angle and then adjust to a low vantage point?

- Is there a gradual framing change where the level angle becomes low?

- Does the video shift from a straight-on viewpoint to an upward-looking low angle?

- Is the starting shot neutral before transitioning to a low, upward-facing position?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a level angle and transitions to a low angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a level angle to a low angle.

- A video where the camera gradually tilts from a straight-on perspective to an upward-looking low angle.

- A sequence beginning with a level shot that transitions to a low vantage point.

- A shot that starts with a neutral angle before lowering and looking up.

- A video showing a smooth transition from a level angle to a low-angle perspective.

- A scene where the camera shifts from a straight-on view to an upward-tilted framing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'level_angle' and self.cam_setup.camera_angle_info['end'] == 'low_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['level_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['low_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Shifts from Low Angle to High Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_low_to_high</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a low angle and transition to a high angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin at a low angle and then tilt or move into a high-angle position?

- Is there a camera movement that raises the angle dramatically from low to high?

- Does the video transition from an upward-facing low angle to a downward-looking high angle?

- Is the initial shot framed at a low vantage point before moving above the subject?

- Does the sequence start with a low angle and then adjust into a high viewpoint?

- Is there a clear framing change where the low-angle shot becomes a high-angle shot?

- Does the video shift from looking up to looking down?

- Is the starting shot positioned low before tilting or moving to a higher perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a low angle and transitions to a high angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a low angle to a high angle.

- A video where the camera smoothly tilts from an upward-facing low angle to a downward-facing high angle.

- A sequence beginning with a low-angle shot that transitions to a high-angle shot.

- A shot that starts with an upward tilt before shifting into a downward-facing perspective.

- A video showing a dramatic transition from a low angle to a high-angle viewpoint.

- A scene where the camera moves from looking up to looking down.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'low_angle' and self.cam_setup.camera_angle_info['end'] == 'high_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['low_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['high_angle', 'unknown'])</code>

</details>

<details>
<summary><h2>Camera Angle Shifts from Low Angle to Level Angle</h2></summary>


<h3>🔵 Label Name:</h3>
<code>camera_angle_from_low_to_level</code>


<h3>📖 Definition:</h3>
Does the video start with the camera at a low angle and transition to a level angle?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot begin at a low angle before moving into a level position?

- Is there a camera movement that raises the angle from low to level?

- Does the video transition from an upward-facing low angle to a straight-on level angle?

- Is the initial shot framed below eye level before the camera adjusts to a neutral position?

- Does the sequence start at a low angle and then shift into a level perspective?

- Is there a gradual framing change where the low angle becomes level?

- Does the video shift from looking up to a neutral eye-level view?

- Is the starting shot positioned low before transitioning to a level position?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video starts with the camera at a low angle and transitions to a level angle.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves from a low angle to a neutral level angle.

- A video where the camera gradually tilts from looking up to a straight-on level angle.

- A sequence beginning with a low-angle shot that transitions to a level perspective.

- A shot that starts with an upward tilt before settling into a level frame.

- A video showing a smooth transition from a low angle to a neutral viewpoint.

- A scene where the camera moves from a low position to a balanced level angle.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.camera_angle_info['start'] == 'low_angle' and self.cam_setup.camera_angle_info['end'] == 'level_angle'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.camera_angle_info['start'] in ['low_angle', 'unknown'] and self.cam_setup.camera_angle_info['end'] in ['level_angle', 'unknown'])</code>

</details>
