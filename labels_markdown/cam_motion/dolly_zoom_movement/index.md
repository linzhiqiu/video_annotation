# Dolly_zoom_movement Overview

<details>
<summary><h2>Has Dolly In and Zoom Out Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_dolly_in_zoom_out</code>


<h3>📖 Definition:</h3>
Does the shot feature a dolly zoom effect with the camera moving forward and zooming out?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera performing a dolly-in while zooming out?

- Does the shot create a dolly zoom effect by advancing while zooming out?

- Is the camera moving forward while simultaneously zooming out?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a perspective distortion due to dolly-in and zoom-out?

- Does the scene demonstrate a classic dolly zoom effect?

- Does the background appear to stretch as the camera moves forward?

- Is the subject staying the same size while the background changes due to zooming out?

- Does the depth of field shift dramatically as the camera moves inward?

- Is the frame expanding outward while the camera advances?

- Does the background appear to recede while the foreground remains steady?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A scene featuring a dolly zoom effect with a forward camera movement and zoom-out.

- A dolly zoom shot with the camera moving forward and zooming out.

- A dolly in and zoom out shot.

- The camera advances while the field of view expands due to zooming out.

- A video where the subject remains the same size, but the background stretches due to dollying in and zooming out.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves forward while optically pulling back.

- A dolly zoom shot.

- The camera moves inward while zooming out to create a perspective distortion effect.

- A shot demonstrating a dramatic warping effect caused by dolly-in and zoom-out.

- A shot where the camera tracks forward while zooming out.

- A scene demonstrating the Vertigo Effect with forward movement and zoom-out.

- A video where the subject stays fixed while the background appears to stretch.

- The camera moves inward while maintaining focus, creating a shifting depth effect.

- A cinematic perspective shift caused by simultaneous dolly-in and zoom-out.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.forward is True and self.cam_motion.zoom_out is True and self.cam_motion.dolly_zoom</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.dolly_zoom or self.cam_motion.forward is False or self.cam_motion.zoom_out is False</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>dolly_out_zoom_in</b>: <code>self.cam_motion.backward is True and self.cam_motion.zoom_in is True and self.cam_motion.dolly_zoom</code>

</details>

</details>

<details>
<summary><h2>Has Dolly Out and Zoom In Movement</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_dolly_out_zoom_in</code>


<h3>📖 Definition:</h3>
Does the shot feature a dolly zoom effect with the camera moving backward and zooming in?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera performing a dolly-out while zooming in?

- Does the shot create a dolly zoom effect by retreating while zooming in?

- Is the camera moving backward while simultaneously zooming in?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a perspective distortion due to dolly-out and zoom-in?

- Does the scene demonstrate a classic reverse dolly zoom effect?

- Does the background appear to shrink as the camera moves backward?

- Is the subject staying the same size while the background changes due to zooming in?

- Does the depth of field shift dramatically as the camera moves outward?

- Is the frame compressing inward while the camera retreats?

- Does the background appear to move closer while the foreground remains steady?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A scene featuring a dolly zoom effect with a backward camera movement and zoom-in.

- A dolly zoom shot with the camera moving backward and zooming in.

- A dolly out and zoom in shot.

- The camera retreats while the field of view narrows due to zooming in.

- A video where the subject remains the same size, but the background compresses due to dollying out and zooming in.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward while optically pushing in.

- A dolly zoom shot.

- The camera moves outward while zooming in to create a perspective distortion effect.

- A shot demonstrating a dramatic warping effect caused by dolly-out and zoom-in.

- A shot where the camera tracks backward while zooming in.

- A scene demonstrating the reverse Vertigo Effect with backward movement and zoom-in.

- A video where the subject stays fixed while the background appears to compress.

- The camera moves outward while maintaining focus, creating a shifting depth effect.

- A cinematic perspective shift caused by simultaneous dolly-out and zoom-in.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.backward is True and self.cam_motion.zoom_in is True and self.cam_motion.dolly_zoom</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.dolly_zoom or self.cam_motion.backward is False or self.cam_motion.zoom_in is False</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>dolly_in_zoom_out</b>: <code>self.cam_motion.forward is True and self.cam_motion.zoom_out is True and self.cam_motion.dolly_zoom</code>

</details>

</details>
