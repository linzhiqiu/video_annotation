# Up Overview

<details>
<summary><h2>Has Upward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>has_up_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera move upward (not tilting up) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving upward in space based on its starting position?

- Is the camera moving upward (not tilting up) with respect to itself, creating a noticeable vertical parallax effect?

- Is the upward motion of the camera clear in this shot by comparing the start and end of the shot?

- Is the camera performing a pedestal up movement?

- Is the camera elevating with respect to itself?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move upward (not tilting up)?

- Is the camera moving upward?

- Is there clear upward movement when comparing the start and end of the shot?

- Does the camera travel upward in space, rather than tilting up?

- Is the camera rising through the space?

- Does the shot feature a clear upward motion of the camera?

- Is the camera's movement progressing upward rather than downward?

- Is the upward motion of the camera clear in this shot?

- Does the camera travel upward in space, rather than tilting up?

- Is the camera ascending in the scene?

- Does the perspective shift upward rather than relying on tilt?

- Is the camera physically traveling upward instead of rotating?

- Is the camera rising, creating a strong sense of vertical movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves upward (not tilting up) with respect to the initial frame.

- A shot where the camera moves upward in space based on its starting position.

- A video where the camera moves upward (not tilting up) with respect to itself, creating a noticeable vertical parallax effect.

- A scene where the upward motion of the camera is clear by comparing the start and end of the shot.

- The camera performs a pedestal up movement.

- The camera elevates with respect to itself.

- A video where the camera physically rises with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves upward, not tilting up.

- A video where the camera is moving upward.

- The camera moves upward in space based on its starting position.

- The camera rises through the space.

- The camera moves upward.

- Camera ascends upward.

- A scene where there is clear upward movement when comparing the start and end of the shot.

- A video where the camera travels upward in space, rather than tilting up.

- A shot where the camera rises through the space.

- A video where the shot features a clear upward motion of the camera.

- A scene where the camera's movement progresses upward rather than downward.

- A video where the upward motion of the camera is clear.

- A shot where the camera travels upward in space rather than tilting up.

- A scene where the camera is ascending in the shot.

- A video where the perspective shifts upward rather than relying on tilt.

- A shot where the camera physically travels upward instead of rotating.

- A video where the camera rises, creating a strong sense of vertical movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.up_cam is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.up_cam is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.down_cam is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.up_cam is False and self.cam_motion.tilt_up is True</code>

</details>

</details>

<details>
<summary><h2>Only Upward Movement (Relative to Camera)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>only_up_wrt_camera</code>


<h3>📖 Definition:</h3>
Does the camera only move upward (not tilting up) with respect to the initial frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is upward motion the only camera movement from the initial frame?

- Is there no other camera motion except upward movement relative to the initial frame?

- Does the camera move upward with respect to itself without any other movement or tilting?

- Is the camera only moving upward relative to the first frame?

- Is the camera only performing a pedestal up movement?

- Is the camera only elevating with respect to itself?

- Is the camera only moving upward without tilting up relative to the first frame?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera only moving upward?

- Is the camera only moving upward (not tilting up) in the scene, creating a noticeable vertical parallax effect?

- Is upward motion the only camera movement in this shot?

- Does the camera travel only upward in space, rather than tilting up?

- Is the camera exclusively moving upward relative to its initial position?

- Does the camera rise in a straight upward direction without any other motions?

- Is the only movement in this shot an upward motion?

- Is there no forward, sideways, or tilt adjustments while moving upward?

- Does the camera ascend without any horizontal changes?

- Does the tracking movement consist only of an upward rise?

- Is the camera strictly ascending upward with no other motion applied?

- Does the shot feature only a single directional upward movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera only moves upward (not tilting up) relative to the initial frame.

- A shot where the camera rises straight up with respect to the initial frame without any other motion.

- A video where the camera exclusively moves upward relative to the initial frame, creating a noticeable vertical parallax effect.

- A scene where the camera moves only upward relative to itself, avoiding tilting or other motions.

- The camera is only performing a pedestal up movement.

- The camera is only elevating with respect to itself.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A tracking shot where the camera moves upward without incorporating other movement types.

- A shot where the upward motion is the only movement present in the scene.

- A shot where the camera moves strictly upward without forward or sideways movement.

- A video where the camera ascends in a single direction without any other adjustments.

- A scene where the camera rises without shifting horizontally.

- A video where the camera strictly maintains upward movement with no deviation.

- A shot where the tracking movement is purely upward with no other motion.

- A scene where the only movement present is the camera rising vertically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.up_cam is True and self.cam_motion.check_if_no_motion_cam(exclude=['up_cam'])</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.up_cam is False or not self.cam_motion.check_if_no_motion_cam(exclude=['up_cam']))</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>moving_down</b>: <code>self.cam_motion.down_cam is True</code>

- <b>only_moving_down</b>: <code>self.cam_motion.down_cam is True and self.cam_motion.check_if_no_motion_cam(exclude=['down_cam'])</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>tilting_up</b>: <code>self.cam_motion.up_cam is False and self.cam_motion.tilt_up is True</code>

- <b>compound_motion_with_up</b>: <code>self.cam_motion.up_cam is True and not self.cam_motion.check_if_no_motion_cam(exclude=['up_cam'])</code>

</details>

</details>
