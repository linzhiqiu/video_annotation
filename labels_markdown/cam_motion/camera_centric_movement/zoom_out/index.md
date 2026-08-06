# Zoom_out Overview

<details>
<summary><h2>Has Zoom Out (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_zoom_out</code>


<h3>📖 Definition:</h3>
Does the camera zoom out?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera zoom out during the shot?

- Is the camera zooming out?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera zoom out rather than physically moving backward?

- Is the field of view widening without the camera physically retreating?

- Does the shot feature zooming out instead of a dolly or tracking movement?

- Is the camera decreasing magnification rather than changing position?

- Does the video include a zoom-out effect where the frame expands?

- Is there a noticeable zoom-out effect rather than actual camera movement?

- Does the framing pull away from the subject without spatial camera movement?

- Is the shot zooming out optically instead of moving physically?

- Does the video include a zoom-out effect?

- Is the camera zooming out rather than physically retreating?

- Is there a noticeable widening of the field of view?

- Is the shot pulling away from the subject through zoom?

- Is the camera reducing magnification without moving?

- Does the framing expand to show more of the scene using zoom?

- Is the subject shrinking in frame due to zoom-out rather than a dolly?

- Does the video feature an optical zoom-out rather than a tracking shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera zooms out.

- A shot where the camera zooms out.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera zooms out rather than physically moving backward.

- A shot featuring a zoom-out effect where the frame expands.

- A scene where the camera optically widens the field of view.

- A video where the camera zooms out to reveal more of the scene.

- A shot where the field of view increases as the camera zooms out.

- A video where the framing loosens using zoom rather than movement.

- A shot that decreases magnification without moving backward.

- A scene where the image becomes smaller due to zoom-out rather than dolly movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.zoom_out is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.zoom_out is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.zoom_in is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>backward_movement_not_zoom</b>: <code>self.cam_motion.backward is True and self.cam_motion.zoom_out is False</code>

</details>

</details>

<details>
<summary><h2>Only Zoom Out (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_zoom_out</code>


<h3>📖 Definition:</h3>
Does the camera only zoom out with no other movement?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is zooming out the only motion in this shot, without other camera movement?

- Does the camera zoom out without any dolly, pan, or tilt movement?

- Is zooming the sole method of changing the frame composition?

- Does the shot only use zoom out without additional spatial movement?

- Is zooming out the exclusive way the shot alters framing?

- Does the video contain only a zoom-out effect without physical movement?

- Is the framing expanding only due to zoom, with no tracking or panning?

- Does the shot feature only a zoom-out adjustment without other motions?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the shot only zooming out without additional movement?

- Does the shot focus on zooming out and nothing else?

- Is zooming out the only framing change in this scene?

- Is there no other camera motion besides zooming out?

- Does the video use zoom out as the only method of focus adjustment?

- Is the camera reducing magnification without any tracking motion?

- Is zoom out the only framing adjustment in the scene?

- Does the camera adjust focus using only zoom rather than movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The camera only zooms out with no other movement.

- A video where zooming out is the only motion, with no additional camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot featuring only a zoom-out effect with no dolly or tracking.

- A scene where zoom-out is the only framing adjustment.

- A video where the camera uses only zoom to widen the framing.

- A shot where no other camera motion is present except zoom-out.

- A scene where zoom-out is the exclusive framing change.

- A video featuring zoom-out as the only adjustment, without panning or tilting.

- A shot where magnification decreases solely due to zoom without movement.

- A scene where the only framing adjustment is a zoom-out.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.zoom_out is True and self.cam_motion.check_if_no_motion(exclude=['zoom_out'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.zoom_out is False or not self.cam_motion.check_if_no_motion(exclude=['zoom_out'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>zooming_in</b>: <code>self.cam_motion.zoom_in is True</code>

- <b>only_zooming_in</b>: <code>self.cam_motion.zoom_in is True and self.cam_motion.check_if_no_motion(exclude=['zoom_in'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>backward_movement_with_zoom</b>: <code>self.cam_motion.backward is True and self.cam_motion.zoom_out is True</code>

- <b>compound_motion_with_zoom</b>: <code>self.cam_motion.zoom_out is True and not self.cam_motion.check_if_no_motion(exclude=['zoom_out'])</code>

</details>

</details>
