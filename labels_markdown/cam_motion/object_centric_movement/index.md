# Object_centric_movement Overview

<details>
<summary><h2>Aerial Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>aerial_tracking_shot</code>


<h3>📖 Definition:</h3>
Does the camera track the subject from above?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is this an aerial tracking shot?

- Does the camera follow the subject from overhead?

- Is the subject tracked with the camera positioned above?

- Does the shot involve the camera moving from a high vantage point to follow the subject?

- Is the tracking done from an aerial perspective?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move above the subject to maintain tracking?

- Is the camera positioned at a high angle while following the subject?

- Is the subject followed from an overhead perspective?

- Does the camera track the subject while maintaining a bird’s-eye view?

- Is the tracking movement executed from an elevated position?

- Does the shot provide a top-down tracking perspective?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera follows the subject from above.

- A shot where the camera moves overhead while tracking the subject.

- A video where the camera maintains an aerial perspective while tracking.

- A scene where the camera follows the subject from a high vantage point.

- A tracking shot executed from an elevated position.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera moves from above to track the subject.

- A shot where the subject is tracked from a bird’s-eye view.

- A shot where the camera maintains an overhead view while following the subject.

- A scene where the tracking is performed from a high position.

- A shot where the subject is framed from an aerial tracking perspective.

- A video where the tracking movement keeps the camera above the action.

- A scene where the camera moves at an elevated position while following motion.

</details>

<h4>🟢 Positive:</h4>
<code>'aerial' in self.cam_motion.tracking_shot_types</code>

<h4>🔴 Negative:</h4>
<code>'aerial' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

</details>

<details>
<summary><h2>Arc Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>arc_tracking_shot</code>


<h3>📖 Definition:</h3>
Does the camera follow the subject while moving in an arc?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is this an arc tracking shot?

- Is the camera tracking the subject while arcing clockwise or counterclockwise around them?

- Does the camera follow the subject while moving in an orbit?

- Is the subject tracked with the camera circling around them?

- Does the shot involve the camera arcing around the subject while tracking?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving in a circular path around the subject while tracking?

- Does the camera track the subject while rotating around them?

- Is the subject framed dynamically as the camera moves in an arc?

- Does the camera move in a semi-circle or full orbit while following the subject?

- Is the tracking movement executed in a curved path?

- Does the shot provide a sense of rotation by following the subject in an arc?

- Is the camera moving along a circular trajectory while tracking the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera follows the subject while moving in an arc.

- An arc-tracking shot.

- A shot where the camera moves in an arc around the subject while tracking.

- A video where the camera tracks the subject while arcing clockwise or counterclockwise around them.

- A scene where the camera moves in an orbit around the subject while tracking.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera follows the subject by rotating in an arc.

- A shot where the subject remains centered while the camera moves in a semi-circle.

- A tracking shot where the camera circles around the subject in a smooth motion.

- A shot where the camera moves in a curved motion around the subject while tracking.

- A video where the camera tracks the subject while arcing around them.

- A shot where the camera moves in a curved trajectory while following the subject.

- A scene where the subject remains in frame while the camera orbits.

- A shot where the camera movement forms a circular motion around the subject.

- A video where the tracking movement follows a curved path.

- A scene where the subject is followed while the camera moves in a circular pattern.

</details>

<h4>🟢 Positive:</h4>
<code>'arc' in self.cam_motion.tracking_shot_types</code>

<h4>🔴 Negative:</h4>
<code>'arc' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

</details>

<details>
<summary><h2>Front-Side Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>front_side_tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot with the camera leading from the front and to the side of the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is it a front-side tracking shot?

- Does the tracking shot lead from the front and slightly to the side of the subject?

- Is the camera positioned ahead and to the side of the subject while tracking?

- Does the shot show the camera leading from a front-side angle?

- Is it a tracking shot filmed from in front and to the side of the subjects?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera track the subject from a diagonal front position?

- Is the camera slightly ahead and off to the side while tracking?

- Does the camera follow the subject while remaining in front and angled?

- Is the perspective framed slightly to the front and side of the subject?

- Does the shot create a leading effect while maintaining a side view?

- Is the camera positioned in a way that guides the subject while staying angled?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera leads from the front and to the side of the subject.

- A shot where the camera moves diagonally ahead of the subject while tracking.

- A video where the camera leads the subject from a front-side perspective.

- A scene where the camera maintains a leading position at an angle.

- A tracking shot filmed with the camera positioned slightly ahead and to the side.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera leads from a diagonal front position.

- A video where the subject moves behind while the camera tracks slightly ahead and to the side.

- A scene where the camera leads the movement from an angled front perspective.

- A video where the camera is not directly in front but slightly off to the side.

- A shot where the subject is framed from a leading diagonal view.

- A scene where the camera leads in a front-side direction while maintaining subject visibility.

- A shot where the perspective is positioned slightly off-center ahead of the subject.

</details>

<h4>🟢 Positive:</h4>
<code>set(self.cam_motion.tracking_shot_types) == set(['lead','side'])</code>

<h4>🔴 Negative:</h4>
<code>set(self.cam_motion.tracking_shot_types) != set(['lead','side'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and not ('lead' in self.cam_motion.tracking_shot_types and 'side' in self.cam_motion.tracking_shot_types)</code>

- <b>lead_tracking_shot</b>: <code>'lead' in self.cam_motion.tracking_shot_types and 'side' not in self.cam_motion.tracking_shot_types</code>

- <b>side_tracking_shot</b>: <code>'side' in self.cam_motion.tracking_shot_types and 'lead' not in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Lead Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>lead_tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot with the camera moving ahead of the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the tracking shot show the camera moving ahead of the subjects?

- Does the shot show the camera leading the subject by moving backward?

- Does the camera track the subjects by leading from the front?

- Is it a leading shot?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving back as the subjects approach?

- Is the camera moving backward while the subject moves toward it?

- Does the camera pull back while the subject moves forward?

- Does the tracking shot involve the camera moving forward ahead of the subject?

- Is the tracking shot filmed with the camera moving in front of the subjects?

- Is the camera positioned ahead of the moving subject?

- Is the subject following the camera's movement?

- Does the camera guide the viewer by leading the subject?

- Is the perspective framed with the camera in front of the action?

- Is the scene composed with the camera tracking ahead rather than behind?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera moves ahead of the subject.

- A tracking shot where the camera moves ahead of the subjects as they move.

- A shot where the camera leads the subject by moving backward.

- A scene where the camera tracks the subject while staying in front.

- A leading tracking shot where the camera moves ahead of the subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves backward as the subjects approach.

- A video where the camera moves in reverse while tracking a moving subject.

- A scene where the camera pulls back as the subject moves forward.

- A tracking shot where the perspective is set ahead of the subject.

- A shot where the camera stays ahead of the subject as they move.

- A video where the subject moves toward the camera as it leads them.

- A tracking shot where the camera maintains a position in front of the subject.

- A video where the camera guides the movement by staying ahead of the subject.

- A scene where the camera continuously pulls away as the subject moves forward.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tracking_shot_types == ['lead']</code>

<h4>🔴 Negative:</h4>
<code>'lead' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and 'lead' not in self.cam_motion.tracking_shot_types</code>

- <b>tail_tracking_shot</b>: <code>self.cam_motion.is_tracking and 'tail' in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Pan Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>pan_tracking_shot</code>


<h3>📖 Definition:</h3>
Does the camera pan to track the subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera pan to follow the subjects?

- Is this a pan-tracking shot?

- Does the camera pan horizontally to follow the subjects?

- Does the camera pan left or right to track the subjects?

- Is the camera panning to keep the subjects in frame?

- Does the shot involve the camera panning to track the motion of the subjects?

- Is this a tracking shot achieved through camera panning?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera rotate left or right to follow the subjects?

- Is the camera panning rather than physically moving to track motion?

- Is the camera swiveling in place to track a subject’s movement?

- Does the camera maintain the subject in frame through horizontal rotation?

- Is the motion of the subject followed solely through panning?

- Is the camera fixed in position while rotating to follow the action?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera pans to follow the subjects.

- A pan-tracking shot.

- A shot where the camera pans left or right to track subject's motion.

- A video where the camera maintains the subject in frame through panning.

- A scene where the camera pans horizontally to follow the subjects.

- A shot where the camera pans left or right while keeping the subject centered.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera rotates to track the subject’s movement.

- A video where the camera follows the motion using horizontal panning.

- A scene where the camera remains stationary while panning to follow action.

- A video where the camera keeps the subject in view through controlled panning.

- A shot where the camera does not move forward but instead pivots left or right.

- A scene where subject tracking is achieved purely through camera rotation.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tracking_shot_types == ['pan']</code>

<h4>🔴 Negative:</h4>
<code>'pan' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and not 'pan' in self.cam_motion.tracking_shot_types</code>

- <b>side_tracking_shot</b>: <code>'side' in self.cam_motion.tracking_shot_types and not 'pan' in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Rear-Side Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>rear_side_tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot with the camera following behind and to the side of the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is it a rear-side tracking shot?

- Does the tracking shot follow behind and to the side of the subject?

- Is the camera positioned behind and to the side of the subject while tracking?

- Does the shot show the camera following from a rear-side angle?

- Is it a tracking shot filmed from behind and to the side of the subjects?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera tracking the subject from a diagonal rear position?

- Does the camera follow the subject from a slight offset behind?

- Is the tracking shot composed with the camera positioned at a rear-side perspective?

- Does the camera follow the movement from behind at an angled view?

- Is the subject moving forward while the camera tracks diagonally behind?

- Does the tracking shot maintain a view from both behind and slightly to the side?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera follows behind and to the side of the subject.

- a rear-side tracking shot.

- A video where the camera follows the subject from a rear-side perspective.

- A tracking shot filmed with the camera positioned slightly behind and to the side.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera maintains a trailing position at an angle.

- A shot where the camera moves diagonally behind the subject while tracking.

- A tracking shot where the camera follows from a diagonal rear position.

- A video where the subject moves ahead while the camera tracks slightly behind and to the side.

- A scene where the camera follows the movement from an angled rear perspective.

- A shot where the subject is framed from a trailing diagonal view.

- A scene where the camera follows in a rear-side direction while maintaining subject visibility.

- A shot where the perspective is positioned slightly off-center behind the subject.

</details>

<h4>🟢 Positive:</h4>
<code>set(self.cam_motion.tracking_shot_types) == set(['tail','side'])</code>

<h4>🔴 Negative:</h4>
<code>set(self.cam_motion.tracking_shot_types) != set(['tail','side'])</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and not ('tail' in self.cam_motion.tracking_shot_types and 'side' in self.cam_motion.tracking_shot_types)</code>

- <b>tail_tracking_shot</b>: <code>'tail' in self.cam_motion.tracking_shot_types and 'side' not in self.cam_motion.tracking_shot_types</code>

- <b>side_tracking_shot</b>: <code>'side' in self.cam_motion.tracking_shot_types and 'tail' not in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Side Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>side_tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot with the camera moving from the side to follow the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is this a side-tracking shot?

- Does the camera move left or right to follow the subject?

- Does the camera truck left or right to follow the subject?

- Is the subject tracked with the camera moving sideways?

- Does the shot involve the camera trucking from the side to follow the motion?

- Is the camera moving along the side of the subject in this tracking shot?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move parallel to the subject?

- Is the subject followed with a lateral camera movement?

- Does the camera track the subjects from the side without leading or trailing?

- Is the perspective framed from a direct side angle?

- Is the camera movement strictly horizontal along the subject’s motion?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera moves from the side to follow the subject.

- A side-tracking shot.

- A side-tracking shot where the camera moves parallel to the subject.

- A shot where the camera trucks left or right to track the subject’s movement.

- A video where the camera follows the subject’s motion from the side.

- A shot where the camera moves along the side of the subject while tracking.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera follows the subject from a lateral position.

- A scene where the camera moves strictly sideways to maintain framing.

- A shot where the camera moves laterally to track the subject’s movement.

- A scene where the camera remains at the side while tracking the subject.

- A video where the camera keeps a constant distance while trucking left or right.

- A shot where the camera moves alongside the subject’s movement.

- A scene where the tracking shot is achieved purely through lateral movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tracking_shot_types == ['side']</code>

<h4>🔴 Negative:</h4>
<code>'side' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and not 'side' in self.cam_motion.tracking_shot_types</code>

- <b>pan_tracking_shot</b>: <code>'pan' in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Tail Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>tail_tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot with the camera following behind the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is it a following shot?

- Does the tracking shot show the camera moving behind the subjects?

- Is it a tracking shot from behind?

- Does the camera track the subjects by following from behind?

- Is the camera moving forward while the subject moves ahead of it?

- Is the tracking shot filmed with the camera moving behind the subjects?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera moving forward as the subjects move away?

- Is the subject leading while the camera follows?

- Is the camera positioned behind the moving subject?

- Does the camera follow the movement rather than leading it?

- Is the perspective framed from behind the subject?

- Is the scene composed with the camera tracking behind rather than ahead?

- Does the shot create a sense of movement by following the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera follows behind the subject.

- A tracking shot where the camera moves behind the subjects as they move.

- A shot where the camera follows the subject by moving forward.

- A scene where the camera tracks the subject while staying behind.

- A following tracking shot.

- A following shot.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves forward as the subject moves away.

- A video where the camera follows a moving subject from behind.

- A scene where the camera moves forward while tracking a subject ahead.

- A tracking shot where the perspective is set behind the subject.

- A shot where the camera stays behind the subject as they move.

- A video where the subject moves ahead while the camera follows.

- A tracking shot where the camera maintains a position behind the subject.

- A video where the camera follows the movement instead of leading it.

- A scene where the camera continuously follows behind the subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tracking_shot_types == ['tail']</code>

<h4>🔴 Negative:</h4>
<code>'tail' not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and 'tail' not in self.cam_motion.tracking_shot_types</code>

- <b>front_tracking_shot</b>: <code>self.cam_motion.is_tracking and 'lead' in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Tilt Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>tilt_tracking_shot</code>


<h3>📖 Definition:</h3>
Does the camera tilt to track the subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is this a tilt-tracking shot?

- Does the camera tilt to follow the subjects?

- Does the camera tilt vertically to follow the subjects?

- Does the camera tilt up or down to track the subjects?

- Does the shot involve the camera tilting to keep the subject in frame?

- Is the subject tracked with a vertical camera tilt?

- Does the camera angle shift up or down to follow the subjects?

- Does the camera maintain the subject in frame by tilting up or down?

- Is this a tracking shot achieved through camera tilting?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera tilting instead of panning to track motion?

- Is the camera adjusting its vertical angle to follow a subject’s movement?

- Is the motion of the subject followed solely through tilting?

- Is the camera fixed in position while tilting to follow the action?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the camera tilts to follow the subjects.

- A tilt-tracking shot.

- A shot where the camera tilts up or down to track the subject’s motion.

- A video where the camera maintains the subject in frame through vertical tilting.

- A scene where the camera tilts vertically to follow the subjects.

- A shot where the camera tilts to track the subject’s movement.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera tilts up or down while keeping the subject centered.

- A video where the camera follows the motion using vertical tilting.

- A scene where the camera remains stationary while tilting to follow action.

- A video where the camera keeps the subject in view through controlled tilting.

- A scene where subject tracking is achieved purely through camera tilting.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.tracking_shot_types == ['tilt']</code>

<h4>🔴 Negative:</h4>
<code>tilt not in self.cam_motion.tracking_shot_types</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>other_tracking_shots</b>: <code>self.cam_motion.is_tracking and not 'tilt' in self.cam_motion.tracking_shot_types</code>

- <b>aerial_tracking_shot</b>: <code>'aerial' in self.cam_motion.tracking_shot_types and not 'tilt' in self.cam_motion.tracking_shot_types</code>

- <b>side_tracking_shot</b>: <code>'side' in self.cam_motion.tracking_shot_types and not 'tilt' in self.cam_motion.tracking_shot_types</code>

</details>

</details>

<details>
<summary><h2>Tracking Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>tracking_shot</code>


<h3>📖 Definition:</h3>
Is it a tracking shot?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move to follow the subjects in the scene?

- Is this a shot where the camera follows the movement of subjects?

- Does the camera track the subjects as they move?

- Does the camera follow one or more subjects in this scene?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera tracking a moving subject?

- Does the camera maintain focus on a subject while moving?

- Is the camera following an object or person throughout the scene?

- Does the camera stay locked onto a subject while in motion?

- Is this a shot where the camera dynamically follows an actor or object?

- Does the shot involve a moving camera that follows the scene's action?

- Is the perspective shifting to maintain framing of a moving subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves to follow the subjects in the scene.

- A shot where the camera tracks a moving subject throughout the frame.

- The camera tracks the subjects as they move in the scene.

- A video where the camera follows the movement of subjects.

- A shot where the camera follows the subjects as they move.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera continuously moves to maintain focus on a subject.

- A shot that follows an actor, object, or scene movement in a continuous motion.

- A video where the camera stays locked onto a moving subject.

- A shot where the perspective follows a subject dynamically.

- A video where the camera adjusts its movement to match a moving character.

- A scene where the camera is tracking a person or object.

- A shot where the camera movement is synchronized with the subject’s motion.

- A video where the camera follows a character through the environment.

- A scene where the camera moves continuously to follow a subject.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.is_tracking</code>

<h4>🔴 Negative:</h4>
<code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h2>Tracking Shot: Subject Larger</h2></summary>


<h3>🔵 Label Name:</h3>
<code>tracking_subject_larger_size</code>


<h3>📖 Definition:</h3>
Does the subject look larger during the tracking shot?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the subject appear to grow larger in the frame during the tracking shot?

- Does the subject take up more of the frame during the tracking shot?

- Is the camera moving closer to the subject or zooming in during the tracking motion?

- Does the subject take up more of the frame as the tracking progresses?

- Does the camera reduce the distance to the subject or zoom in during the shot?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera making the subject look larger by moving closer or zooming in?

- Does the subject’s size appear to increase as the camera tracks?

- Is the camera emphasizing the subject by making it appear larger?

- Does the tracking movement result in the subject filling more of the frame?

- Is the camera’s movement reducing the background space while enlarging the subject?

- Does the tracking shot make the subject appear more dominant by increasing its size?

- Is the shot designed to gradually bring the subject closer to the viewer?

- Does the tracking result in a magnified appearance of the subject?

- Is the subject framed to increase in size as the camera moves?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the subject looks larger as the camera moves.

- A shot where the subject grows in size within the frame while tracking.

- A video where the camera moves closer to the subject or zooms in during the tracking motion.

- A scene where the subject fills more of the frame as tracking progresses.

- A tracking shot where the subject appears more dominant due to size increase.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is emphasized by appearing larger as the camera tracks.

- A shot where the camera movement results in the subject filling more of the frame.

- A scene where the camera reduces background space to enlarge the subject.

- A video where the tracking makes the subject appear progressively bigger.

- A shot where the camera adjusts its movement to frame the subject larger.

- A scene where the subject’s presence in the frame grows as the shot continues.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.is_tracking and self.cam_motion.subject_size_change == 'larger'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.is_tracking and self.cam_motion.subject_size_change == 'larger')</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>subject_gets_smaller_or_same</b>: <code>self.cam_motion.is_tracking and self.cam_motion.subject_size_change != 'larger'</code>

</details>

</details>

<details>
<summary><h2>Tracking Shot: Subject Smaller</h2></summary>


<h3>🔵 Label Name:</h3>
<code>tracking_subject_smaller_size</code>


<h3>📖 Definition:</h3>
Does the subject look smaller during the tracking shot?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the subject appear to shrink in the frame during the tracking shot?

- Does the subject take up less of the frame as the tracking progresses?

- Does the subject’s size appear to decrease as the camera tracks?

- Is the camera making the subject look smaller by moving away or zooming out?

- Does the tracking movement result in the subject occupying less of the frame?

- Is the camera moving further away from the subject or zooming out during the tracking motion?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera increase the distance to the subject or zoom out?

- Is the camera emphasizing distance by making the subject appear smaller?

- Is the camera’s movement increasing background space while shrinking the subject?

- Does the tracking shot make the subject appear less dominant by decreasing its size?

- Is the shot designed to gradually distance the subject from the viewer?

- Does the tracking result in a minimized appearance of the subject?

- Is the subject framed to reduce in size as the camera moves?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A tracking shot where the subject looks smaller as the camera moves.

- A shot where the subject shrinks in size within the frame while tracking.

- A video where the camera moves away from the subject or zooms out during the tracking motion.

- A scene where the subject occupies less of the frame as tracking progresses.

- A tracking shot where the subject appears less dominant due to size decrease.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the subject is de-emphasized by appearing smaller as the camera tracks.

- A shot where the camera movement results in the subject occupying less of the frame.

- A scene where the camera increases background space to reduce the subject’s size.

- A video where the tracking makes the subject appear progressively smaller.

- A shot where the camera adjusts its movement to frame the subject smaller.

- A scene where the subject’s presence in the frame diminishes as the shot continues.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.is_tracking and self.cam_motion.subject_size_change == 'smaller'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_motion.is_tracking and self.cam_motion.subject_size_change == 'smaller')</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_a_tracking_shot</b>: <code>not self.cam_motion.is_tracking</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>subject_gets_larger_or_same</b>: <code>self.cam_motion.is_tracking and self.cam_motion.subject_size_change != 'smaller'</code>

</details>

</details>
