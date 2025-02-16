# Zoom_in Overview

<details>
<summary><h2>Has Zoom In (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_zoom_in</code>


<h3>📖 Definition:</h3>
Does the camera zoom in rather than physically moving forward?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the field of view narrowing without the camera physically advancing?

- Does the shot feature zooming in instead of a dolly or tracking movement?

- Is the camera increasing magnification rather than changing position?

- Does the video include a zoom-in effect where the frame tightens on the subject?

- Is there a noticeable zoom-in effect rather than actual camera movement?

- Does the framing move closer to the subject without spatial camera movement?

- Is the shot pulling in optically instead of moving physically?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video include a zoom-in effect?

- Is the camera zooming in rather than physically approaching?

- Is there a noticeable narrowing of the field of view?

- Is the shot tightening in on the subject through zoom?

- Is the camera magnifying the image without moving?

- Does the framing close in on the subject using zoom rather than movement?

- Is the subject enlarged without a physical dolly movement?

- Does the video feature an optical zoom rather than a tracking shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera zooms in rather than physically moving forward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot featuring a zoom-in effect where the frame narrows in.

- A scene where the camera optically magnifies the subject.

- A video where the camera zooms in to close in on the subject.

- A shot where the field of view decreases as the camera zooms.

- A video where the framing tightens using zoom rather than movement.

- A shot that enhances magnification without moving forward.

- A scene where the image becomes larger due to zoom-in rather than dolly movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.zoom_in is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.zoom_in is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.zoom_out is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>forward_movement_not_zoom</b>: <code>self.cam_motion.forward is True and self.cam_motion.zoom_in is False</code>

</details>

</details>

<details>
<summary><h2>Only Zoom In (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_zoom_in</code>


<h3>📖 Definition:</h3>
Is zooming in the only motion in this shot, without other camera movement?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera zoom in without any dolly, pan, or tilt movement?

- Is zooming the sole method of changing the frame composition?

- Does the shot only use zoom in without additional spatial movement?

- Is zooming in the exclusive way the shot alters framing?

- Does the video contain only a zoom-in effect without physical movement?

- Is the framing tightening only due to zoom, with no tracking or panning?

- Does the shot feature only a zoom-in adjustment without other motions?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the shot only zooming in without additional movement?

- Does the shot focus on zooming in and nothing else?

- Is zooming in the only framing change in this scene?

- Is there no other camera motion besides zooming in?

- Does the video use zoom in as the only method of focus adjustment?

- Is the camera magnifying the image without any tracking motion?

- Is zoom in the only framing adjustment in the scene?

- Does the camera adjust focus using only zoom rather than movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where zooming in is the only motion, with no additional camera movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot featuring only a zoom-in effect with no dolly or tracking.

- A scene where zoom-in is the only framing adjustment.

- A video where the camera uses only zoom to tighten the framing.

- A shot where no other camera motion is present except zoom-in.

- A scene where zoom-in is the exclusive framing change.

- A video featuring zoom-in as the only adjustment, without panning or tilting.

- A shot where magnification increases solely due to zoom without movement.

- A scene where the only framing adjustment is a zoom-in.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.zoom_in is True and self.cam_motion.check_if_no_motion(exclude=['zoom_in'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.zoom_in is False or not self.cam_motion.check_if_no_motion(exclude=['zoom_in'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>zooming_out</b>: <code>self.cam_motion.zoom_out is True</code>

- <b>only_zooming_out</b>: <code>self.cam_motion.zoom_out is True and self.cam_motion.check_if_no_motion(exclude=['zoom_out'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>forward_movement_with_zoom</b>: <code>self.cam_motion.forward is True and self.cam_motion.zoom_in is True</code>

- <b>compound_motion_with_zoom</b>: <code>self.cam_motion.zoom_in is True and not self.cam_motion.check_if_no_motion(exclude=['zoom_in'])</code>

</details>

</details>
