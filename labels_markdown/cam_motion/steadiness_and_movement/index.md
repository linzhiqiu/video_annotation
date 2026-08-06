# Steadiness_and_movement Overview

<details>
<summary><h2>Clearly Moving Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>clear_moving_camera</code>


<h3>📖 Definition:</h3>
Does the camera have noticeable motion beyond minor shake or wobble?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is there a distinct camera movement beyond slight shaking or wobbling?

- Is there a clear and significant camera motion?

- Is the camera’s movement clear and intentional?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera clearly moving, with noticeable motion?

- Does the camera exhibit noticeable movement?

- Is the camera actively moving, rather than being mostly static?

- Does the camera have a noticeable motion?

- Is the camera clearly moving in the shot?

- Does the camera motion stand out?

- Is the camera movement easy to perceive?

- Is the camera moving in a way that is obvious?

- Does the camera display clear directional movement?

- Is the camera moving beyond subtle adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera has noticeable motion beyond minor shake or wobble.

- A video where the camera exhibits distinct movement beyond slight shaking or wobbling.

- A shot where the camera’s movement is clear and intentional.

- A video featuring a clear and significant camera motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera clearly moves with noticeable motion.

- A scene where the camera displays noticeable movement.

- A scene where the camera is actively moving rather than being mostly static.

- A video where the camera has a noticeable motion.

- A shot where the camera is clearly moving.

- A video where the camera’s motion stands out.

- A scene where the camera movement is easy to perceive.

- A video where the camera is moving in an obvious way.

- A shot where the camera displays clear directional movement.

- A video where the camera moves beyond subtle adjustments.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.clear_moving_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.clear_moving_camera is False</code>

</details>

<details>
<summary><h2>Fast Moving Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fast_moving_camera</code>


<h3>📖 Definition:</h3>
Does the camera have noticeable motion at a fast speed?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving rapidly in the shot?

- Is the camera moving at a noticeably high speed?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera's movement quick?

- Does the camera motion feel fast and dynamic?

- Is the camera shifting positions rapidly?

- Does the camera travel across the scene at high speed?

- Is the camera movement sudden and energetic?

- Is the camera capturing motion in a fast-paced manner?

- Does the camera exhibit noticeable movement at a fast speed?

- Is the camera moving quickly?

- Is the camera shifting directions rapidly?

- Does the camera move at an accelerated pace?

- Is the camera motion fast and engaging?

- Is the camera capturing motion dynamically?

- Is the camera's movement swift and noticeable?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera has noticeable motion at a fast speed.

- A video where the camera moves rapidly within the shot.

- A shot where the camera moves at a noticeably high speed.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera motion feels fast and dynamic.

- A video where the camera's movement is quick and energetic.

- A shot where the camera shifts positions rapidly.

- A scene where the camera travels across the frame at high speed.

- A video where the camera movement is sudden and engaging.

- A shot where the camera captures motion in a fast-paced manner.

- A shot where the camera exhibits noticeable movement at a fast speed.

- A video where the camera moves quickly.

- A scene where the camera shifts directions rapidly.

- A shot where the camera moves at an accelerated pace.

- A video where the camera motion is fast and engaging.

- A shot where the camera captures motion dynamically.

- A video where the camera's movement is swift and noticeable.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.fast_moving_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.fast_moving_camera is False</code>

</details>

<details>
<summary><h2>Fixed Camera (Stable)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fixed_camera</code>


<h3>📖 Definition:</h3>
Is the camera completely still without any motion or shaking?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera completely still without any movement?

- Does the camera remain perfectly stationary throughout?

- Does the camera remain perfectly still throughout the shot?

- Is the camera entirely stationary with no visible vibrations?

- Is the camera locked off without any instability?

- Is there absolutely no shake or motion in the camera?

- Is the camera entirely stable with no visible shaking?

- Is this a fixed camera shot without any shaking?

- Is the camera locked and stationary with no signs of movement?

- Is the camera locked in place without any motion or shaking?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera still?

- Is the camera stable?

- Is the camera fixed?

- Is the camera locked?

- Is the camera motionless?

- Is the camera staionary?

- Is the camera not moving?

- Is the camera not shaking?

- Is the camera not vibrating?

- Is the camera not swaying?

- Is the camera not wobbling?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera remains completely still with no motion or shaking.

- A video where the camera is completely still without any movement.

- A video where the camera remains perfectly stationary throughout.

- A video where the camera remains perfectly still throughout the shot.

- A video where the camera is entirely stationary with no visible vibrations.

- A video where the camera is locked off without any instability.

- A video where there is absolutely no shake or motion in the camera.

- A video where the camera is entirely stable with no visible shaking.

- A video that features a fixed camera shot without any shaking.

- A video where the camera is locked and stationary with no signs of movement.

- A video where the camera is locked in place without any motion or shaking.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with a still camera.

- A video where the camera is stable.

- A video with a fixed camera.

- A video where the camera is locked.

- A video with a motionless camera.

- A video where the camera is stationary.

- A video where the camera is not moving.

- A video where the camera is not shaking.

- A video where the camera is not vibrating.

- A video where the camera is not swaying.

- A video where the camera is not wobbling.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.fixed_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.fixed_camera is False</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>fixed_but_slightly_shaky</b>: <code>self.cam_motion.fixed_but_slightly_shaky is True</code>

</details>

</details>

<details>
<summary><h2>Fixed Camera (Somewhat Shaky)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fixed_camera_with_shake</code>


<h3>📖 Definition:</h3>
Is the camera stationary with minor vibrations or shaking?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera stationary with some shaking?

- Is the camera stable with minor vibrations?

- Is the camera primarily stationary but not entirely stable?

- Is the camera locked off but shows signs of slight instability?

- Does the camera remain mostly stationary but with slight shaking?

- Does the camera stay still but show some minor vibrations throughout the shot?

- Is this a fixed camera shot with minor shaking?

- Is the camera locked in place but with visible shaking or vibrations?

- Is the camera locked but not perfectly stable?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera fixed but slightly shaky?

- Is the camera stationary but not perfectly steady?

- Is the camera fixed with slight movement?

- Is the camera mostly still?

- Is the camera not entirely steady?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera is mostly stationary but has minor vibrations or shaking.

- A video where the camera is stationary but experiences some shaking.

- A video where the camera is stable but has minor vibrations.

- A video where the camera is primarily stationary but not entirely stable.

- A video where the camera is locked off but shows signs of slight instability.

- A video where the camera remains mostly stationary but with slight shaking.

- A video where the camera stays still but shows some minor vibrations.

- A video featuring a fixed camera shot with minor shaking.

- A video where the camera is locked in place but has visible shaking or vibrations.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with a fixed camera that shows slight shaking.

- A video where the camera is stationary but not perfectly steady.

- A video where the camera is fixed but has slight movement.

- A video where the camera is mostly still.

- A video where the camera is not entirely steady.

- A video where the camera is locked but not perfectly stable.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.fixed_camera_with_shake is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.fixed_camera_with_shake is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_fixed_camera</b>: <code>self.cam_motion.not_fixed_camera is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>fixed_without_shaking</b>: <code>self.cam_motion.fixed_without_shaking is True</code>

- <b>shaky_camera_that_moves</b>: <code>self.cam_motion.shaky_camera_that_moves is True</code>

</details>

</details>

<details>
<summary><h2>Moving Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>moving_camera</code>


<h3>📖 Definition:</h3>
Is there any camera movement?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move at all?

- Does the camera exhibit motion at any point?

- Is the camera moving instead of remaining still?

- Is there any motion in the camera?

- Does the shot include any camera motion?

- Is there any motion in the camera?

- Is the shot recorded with a non-stationary camera?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera shifting, panning, tilting, or zooming?

- Does the camera’s position change during the scene?

- Does the shot involve a dynamic camera?

- Is the camera actively changing position during the shot?

- Is there movement in the camera during the shot?

- Does the camera shift its position while capturing the scene?

- Is the camera moving, panning, tilting, or zooming?

- Does the camera’s perspective shift dynamically?

- Is the camera following the action instead of staying in place?

- Does the camera move in any way?

- Does the camera track a subject or change viewpoints?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera moves.

- A scene where the camera exhibits movement.

- A shot featuring a moving camera.

- The camera moves.

- A video recorded with a non-stationary camera.

- A video with camera motion.

- A video with a moving camera.

- A video where the camera exhibits motion.

- A video featuring any kind of camera movement.

- A shot where the camera moves during filming.

- A video where the camera does not remain still.

- A video where the camera is not static.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera’s position changes instead of staying fixed.

- A video where the camera is not static and moves throughout the shot.

- A scene where the camera shifts, tilts, pans, or zooms dynamically.

- A video capturing movement through an actively moving camera.

- A shot where the camera actively changes position.

- A scene where the camera follows movement dynamically.

- A video with a handheld or tracking camera.

- A shot where the camera’s framing changes through motion.

- A video with a camera that does not stay fixed in one spot.

- A video where the camera moves to capture action dynamically.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.moving_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.moving_camera is False</code>

</details>

<details>
<summary><h2>Shaky Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shaky_camera</code>


<h3>📖 Definition:</h3>
Does the camera show any vibrations, shaking, or wobbling?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is there any shaking or vibration in the camera?

- Is the camera visibly vibrating or shaking?

- Is the camera showing unintended vibrations or shaking?

- Does the camera appear unsteady, as if it’s handheld?

- Is the footage shaky or vibrating?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera show vibrations typical of handheld operation?

- Is there handheld-like shaking or wobbling in the camera?

- Does the camera have a handheld-like shake or wobble?

- Does the shot feel shaky, like it was filmed handheld?

- Is the camera unsteady?

- Does the shot feel unstable?

- Does the camera have a noticeable wobble?

- Is there movement causing an unsteady frame?

- Does the video have a handheld-like feel?

- Does the camera lack stability?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera shows vibrations, shaking, or wobbling.

- A video where the camera is visibly shaking or vibrating.

- A shot where the camera exhibits unintended shaking or wobbling.

- A scene where the camera shows handheld-like vibrations.

- A video where the camera demonstrates a handheld-like shake or wobble.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera appears unsteady, resembling handheld footage.

- A video where the camera lacks stability and shakes during the shot.

- A shot where the camera is unsteady.

- A video where the camera movement feels unstable.

- A scene where the camera has noticeable wobble.

- A video where movement causes an unsteady frame.

- A shot with a handheld-like feel due to camera motion.

- A video where the footage appears shaky or vibrating.

- A shot where the camera lacks stability.

- A scene where the camera motion is erratic or unbalanced.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.shaky_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.shaky_camera is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_shaky_camera_excluding_smooth</b>: <code>self.cam_motion.not_shaky_camera_excluding_smooth is True</code>

</details>

</details>

<details>
<summary><h2>Slowly Moving Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>slow_moving_camera</code>


<h3>📖 Definition:</h3>
Does the camera have noticeable motion but at a slow motion speed?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is the camera moving slowly in the shot?

- Is the camera’s movement slow?

- Is the camera moving at a noticeably slow rate?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the camera shifting position at a slow and steady pace?

- Does the camera pan, tilt, or move smoothly at a slow speed?

- Does the camera’s movement appear slow and deliberate?

- Is the camera’s motion smooth and gradual rather than fast or abrupt?

- Is the camera moving at a controlled and slow speed?

- Does the camera have a noticeable motion at a slow speed?

- Is the camera shifting position at a slow speed?

- Does the camera move smoothly and at a slow pace?

- Is the camera tracking or following the subject at a slow speed?

- Is the camera movement gentle and unhurried?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera has noticeable motion but at a slow motion speed.

- A shot where the camera is moving slowly.

- A video where the camera moves at a slow speed.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where the camera moves at a controlled and slow speed.

- A shot where the camera’s motion is smooth and gradual rather than fast or abrupt.

- A scene where the camera’s movement appears slow and deliberate.

- A video where the camera shifts position at a slow and steady pace.

- A shot where the camera pans, tilts, or moves smoothly at a slow speed.

- A video where the camera tracks or moves at a noticeably slow rate.

- A scene where the camera’s movement is gradual.

- A video where the camera shifts position slowly.

- A shot where the camera moves smoothly at a slow pace.

- A video where the camera tracks or follows the subject at a slow speed.

- A video where the camera movement is gentle and unhurried.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.slow_moving_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.slow_moving_camera is False</code>

</details>

<details>
<summary><h2>Stable Camera Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>stable_camera_motion</code>


<h3>📖 Definition:</h3>
Is the camera movement smooth and stable?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move in a steady, controlled manner?

- Is the camera motion stable, like a steadicam shot?

- Does the camera move without unintended vibrations or shaking?

- Is the camera motion free of shakiness?

- Does the camera show smooth, steadicam-like movement?

- Does the camera move smoothly without any wobble?

- Does the shot feel smooth, like it was filmed using a steadicam?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move fluidly?

- Is the camera motion free of sudden jerks?

- Does the camera exhibit controlled movement?

- Is the camera free from excessive vibrations?

- Does the camera glide through the scene without shaking?

- Is the footage stabilized and smooth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera movement is smooth and stable.

- A video where the camera moves in a steady, controlled manner.

- A shot where the camera exhibits stable motion like a steadicam.

- A scene where the camera moves without unintended vibrations or shaking.

- A video where the camera motion is free of shakiness.

- A shot where the camera shows smooth, steadicam-like movement.

- A scene where the camera moves smoothly without any wobble.

- A video where the shot feels smooth, like it was filmed using a steadicam.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera moves fluidly.

- A video where the camera motion is free of sudden jerks.

- A scene where the camera exhibits controlled movement.

- A shot where the camera is free from excessive vibrations.

- A shot where the camera glides through the scene without shaking.

- A video where the footage is stabilized and smooth.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.stable_camera_motion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.stable_camera_motion is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>quite_shaky_camera</b>: <code>self.cam_motion.quite_shaky_camera is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>fixed_camera_without_motion</b>: <code>self.cam_motion.fixed_camera_without_motion is True</code>

</details>

</details>

<details>
<summary><h2>Very Shaky Camera</h2></summary>


<h3>🔵 Label Name:</h3>
<code>very_shaky_camera</code>


<h3>📖 Definition:</h3>
Does the camera show noticable vibrations, shaking, or wobbling?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera appear highly unsteady, as if it’s handheld and unstable?

- Is there significant shaking or vibration in the camera?

- Is the camera heavily vibrating or shaking?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the footage extremely shaky or vibrating?

- Does the camera show strong vibrations typical of unstable handheld operation?

- Is there extreme handheld-like shaking or wobbling in the camera?

- Does the camera have an excessive handheld-like shake or wobble?

- Does the shot feel extremely shaky, as if it was filmed with unstable hands?

- Is the camera highly unsteady?

- Does the shot feel extremely unstable?

- Does the camera have an intense and noticeable wobble?

- Is there excessive movement causing an extremely unsteady frame?

- Does the video have a highly unstable, handheld-like feel?

- Does the camera lack stability and control?

- Is the camera motion erratic, uncontrolled, or excessively unbalanced?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera shows noticable vibrations, shaking, or wobbling.

- A video where the camera is obviously shaking or vibrating.

- A shot where the camera exhibits significant unintended shaking or wobbling.

- A scene where the camera shows highly unstable, handheld-like vibrations.

- A video where the camera demonstrates excessive handheld-like shake or wobble.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the camera appears extremely unsteady, resembling uncontrolled handheld footage.

- A video where the camera lacks stability and shakes intensely during the shot.

- A shot where the camera is highly unsteady.

- A video where the camera movement feels completely unstable.

- A scene where the camera has intense and extreme wobble.

- A video where excessive movement causes an extremely unsteady frame.

- A shot with an extreme handheld-like feel due to erratic camera motion.

- A video where the footage appears highly shaky or vibrating.

- A shot where the camera completely lacks stability.

- A scene where the camera motion is erratic, uncontrolled, or excessively unbalanced.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.very_shaky_camera is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.very_shaky_camera is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>not_very_shaky_camera_excluding_smooth</b>: <code>self.cam_motion.not_very_shaky_camera_excluding_smooth is True</code>

</details>

</details>

<details>
<summary><h2>Very Stable Camera Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>very_stable_camera_motion</code>


<h3>📖 Definition:</h3>
Is the camera movement exceptionally smooth and highly stable?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Does the camera move in an ultra-steady, controlled manner?

- Is the camera motion perfectly stable, like a professional steadicam or gimbal shot?

- Is the camera motion completely free of shakiness?

- Does the camera show perfectly smooth, gimbal-like movement?

- Does the camera move seamlessly without any wobble or instability?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the camera move flawlessly without any unintended vibrations or shaking?

- Does the shot feel extremely smooth, like it was filmed using high-end stabilization?

- Does the camera move effortlessly and fluidly?

- Is the camera motion completely free of sudden jerks?

- Does the camera exhibit precision-controlled movement?

- Is the camera absolutely free from any noticeable vibrations?

- Does the camera glide through the scene with flawless stability?

- Is the footage perfectly stabilized and smooth?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video where the camera movement is exceptionally smooth and highly stable.

- A video where the camera moves in an ultra-steady, controlled manner.

- A shot where the camera exhibits perfectly stable motion like a professional steadicam or gimbal.

- A video where the camera motion is completely free of shakiness.

- A shot where the camera shows perfectly smooth, gimbal-like movement.

- A scene where the camera moves seamlessly without any wobble or instability.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene where the camera moves flawlessly without any unintended vibrations or shaking.

- A video where the shot feels extremely smooth, like it was filmed using high-end stabilization.

- A shot where the camera moves effortlessly and fluidly.

- A video where the camera motion is completely free of sudden jerks.

- A scene where the camera exhibits precision-controlled movement.

- A shot where the camera is absolutely free from any noticeable vibrations.

- A shot where the camera glides through the scene with flawless stability.

- A video where the footage is perfectly stabilized and smooth.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_motion.very_stable_camera_motion is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_motion.very_stable_camera_motion is False</code>

<details>
<summary><h4>🔴 Negative (Easy)</h4></summary>

- <b>somewhat_shaky_camera</b>: <code>self.cam_motion.somewhat_shaky_camera is True</code>

</details>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>fixed_camera_without_motion</b>: <code>self.cam_motion.fixed_camera_without_motion is True</code>

</details>

</details>
