# Video_speed Overview

<details>
<summary><h2>Fast-Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fast_motion</code>


<h3>📖 Definition:</h3>
Is this video played at a faster speed than real-time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene appear quicker than normal?

- Is the motion speed increased to enhance pacing?

- Does the video show an acceleration of real-time movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A fast-motion video where playback speed is faster than real-time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where actions appear slightly accelerated.

- A scene with movement that is faster than normal speed.

- A video where motion is enhanced by speed-up effects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed in ['fast_motion', 'time_lapse']</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['fast_motion', 'time_lapse', 'speed_ramp', 'time_reversed']</code>

</details>

<details>
<summary><h2>Fast-Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>fast_motion</code>


<h3>📖 Definition:</h3>
Is this video played at a slightly faster speed than real-time (e.g., 1x-3x)?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene appear quicker than normal but not as extreme as time-lapse?

- Is the motion speed subtly increased to enhance pacing?

- Does the video show a slight acceleration of real-time movement?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A fast-motion video where playback speed is slightly faster than real-time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where actions appear slightly accelerated but not time-lapsed.

- A scene with movement that is subtly faster than normal speed.

- A video where motion is enhanced by slight speed-up effects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'fast_motion'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['fast_motion', 'speed_ramp', 'time_reversed']</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>time_lapse</b>: <code>self.cam_setup.video_speed == 'time_lapse'</code>

</details>

</details>

<details>
<summary><h2>Regular Speed</h2></summary>


<h3>🔵 Label Name:</h3>
<code>regular_speed</code>


<h3>📖 Definition:</h3>
Is this video played at normal real-time speed without noticeable acceleration or slowing?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene play at a natural, unaltered speed?

- Is the video not sped up or slowed down?

- Does the movement appear to match real-world timing?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A regular-speed video where events play in real-time without acceleration or slowing.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot captured at standard playback speed.

- A video showing motion at a natural, unmodified pace.

- A scene where time progresses at a normal rate.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'regular'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['regular', 'stop_motion', 'time_reversed']</code>

</details>

<details>
<summary><h2>Slow-Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>slow_motion</code>


<h3>📖 Definition:</h3>
Is this video played at a slower speed than real-time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the motion in this shot appear dramatically slowed down?

- Is this video played at a slower speed than real-time, making actions appear 1x-3x slower?

- Is the playback speed reduced to emphasize details in movement?

- Does the video stretch time by making movements appear smooth and slow?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A slow-motion video where playback speed is reduced, making actions appear slower than real-time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where movement is slowed down for dramatic effect.

- A video where time appears stretched due to reduced playback speed.

- A scene captured in slow-motion, emphasizing small details in movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'slow_motion'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['slow_motion', 'speed_ramp', 'time_reversed']</code>

</details>

<details>
<summary><h2>Speed-Ramp</h2></summary>


<h3>🔵 Label Name:</h3>
<code>speed_ramp</code>


<h3>📖 Definition:</h3>
Does this shot feature a speed ramp effect where playback speed smoothly transitions between faster and slower speeds?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video contain gradual speed changes within a single shot?

- Is the motion dynamically adjusted between fast and slow playback?

- Does the scene include smooth speed variations instead of a single fixed speed?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video with a speed ramp effect where playback speed smoothly transitions between fast and slow.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where the motion speed dynamically increases and decreases.

- A video featuring smooth transitions between fast and slow speeds.

- A scene that changes playback speed to enhance action or pacing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'speed_ramp'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed != 'speed_ramp'</code>

</details>

<details>
<summary><h2>Stop-Motion</h2></summary>


<h3>🔵 Label Name:</h3>
<code>stop_motion</code>


<h3>📖 Definition:</h3>
Is this a stop-motion video where objects are moved frame by frame to create motion?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video use frame-by-frame animation techniques?

- Is this shot animated by moving objects between still frames?

- Does the video create the illusion of movement using manual frame adjustments?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A stop-motion video where objects are moved frame by frame to create motion.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where stop-motion animation is used for movement.

- A scene animated using a frame-by-frame capture technique.

- A video where objects shift between frames to simulate movement.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'stop_motion'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['stop_motion', 'time_reversed']</code>

</details>

<details>
<summary><h2>Time-Lapse</h2></summary>


<h3>🔵 Label Name:</h3>
<code>time_lapse</code>


<h3>📖 Definition:</h3>
Does this shot speed up time significantly to show changes over minutes or hours?

<details>
<summary><h4> Question (Definition)</h4></summary>

- Is this a time-lapse video where time appears to move rapidly over an extended period?

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is this a time-lapse video?

- Is this video played at an extremely high speed to condense long durations?

- Does the scene depict fast changes that would normally take much longer?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A time-lapse video where time appears to move rapidly over an extended period.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot showcasing accelerated time progression.

- A video where clouds, crowds, or objects move unnaturally fast due to time-lapse.

- A scene with exaggerated speed, condensing long durations into seconds.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'time_lapse'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['time_lapse', 'speed_ramp', 'time_reversed']</code>

<details>
<summary><h4>🔴 Negative (Hard)</h4></summary>

- <b>fast_motion</b>: <code>self.cam_motion.video_speed == 'fast_motion'</code>

</details>

</details>

<details>
<summary><h2>Time-Reversed</h2></summary>


<h3>🔵 Label Name:</h3>
<code>time_reversed</code>


<h3>📖 Definition:</h3>
Is this video played in reverse, with events unfolding backward in time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the motion appear unnatural, as if time is moving backward?

- Is the sequence reversed, showing actions in reverse order?

- Does the video playback events from end to start instead of start to end?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A time-reversed video where events unfold backward in time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where movement is reversed, playing from end to beginning.

- A video where all actions appear to happen in reverse.

- A scene where objects and motion follow a backward timeline.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.video_speed == 'time_reversed'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.video_speed not in ['time_reversed', 'speed_ramp', 'time_lapse']</code>

</details>
