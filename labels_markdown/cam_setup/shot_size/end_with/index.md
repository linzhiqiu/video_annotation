# End_with Overview

<details>
<summary><h2>Shot Size End With Close Up</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_close_up</code>


<h3>📖 Definition:</h3>
Does the video end with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a close-up shot focusing on a subject’s prominent feature?

- Is the last shot a close-up shot where the subject fills most of the frame?

- Does the video finish with a close-up shot capturing a key detail of the subject?

- Is the closing shot a close-up where a subject’s face, hands, or another defining feature is visible?

- Does the final shot show a close-up view with minimal surrounding context?

- Is the last shot a close-up that highlights intricate features?

- Does the video end with a shot where the subject takes up nearly the entire frame?

- Is the last frame a close-up that isolates a fine detail of the subject?

- Does the video conclude with a close-up framing a small portion of a subject?

- Is the final shot a tight and detailed view of an object or subject’s feature?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a close-up shot that highlights a distinct part of the subject or scene while still preserving some surrounding context.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a close-up shot where the subject's defining features fill most of the frame.

- The video closes with a close-up shot emphasizing a specific detail of the subject.

- The last shot of the video is a close-up, providing a tight yet identifiable framing.

- The closing shot includes a close-up view of a subject’s face, hands, or a recognizable object.

- The final shot of the video is a close-up, ensuring key details are in focus.

- A shot that captures a subject closely while maintaining enough surrounding information.

- A video where the subject occupies 50%-100% of the frame while keeping identifiable context.

- A shot where the subject’s defining features remain prominent within the frame.

- A video ending with a close-up shot that enhances the subject’s presence on screen.

- A cinematic close-up shot that ensures the focus remains on the subject's key details.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'close_up'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['close_up', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Extreme Close Up</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_extreme_close_up</code>


<h3>📖 Definition:</h3>
Does the video end with an extreme close-up shot that isolates a very small detail of the subject or scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with an extreme close-up shot focusing on a tiny detail?

- Is the last shot an extreme close-up shot capturing an isolated part of the subject?

- Does the video finish with an extreme close-up emphasizing texture or fine details?

- Is the closing shot an extreme close-up where only a small portion of the subject is visible?

- Does the final shot show an extreme close-up view with minimal surrounding context?

- Is the last shot an extreme close-up that highlights intricate features?

- Does the video end with a shot where the subject takes up nearly the entire frame?

- Is the last frame an extreme close-up that isolates a fine detail of the subject?

- Does the video close with an extreme close-up framing a small portion of a subject?

- Is the final shot a tight and detailed view of an object or subject’s feature?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with an extreme close-up shot, isolating a very small detail of the subject or scene.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with an extreme close-up shot capturing a tiny feature of the subject.

- The video closes with an extreme close-up shot emphasizing small details.

- The last shot of the video is an extreme close-up focusing on intricate textures.

- The closing shot is an extreme close-up, making the subject’s details highly prominent.

- The final shot of the video is an extreme close-up with minimal surrounding context.

- A shot that frames only a tiny part of the subject, emphasizing detail over broader context.

- A video where the subject takes up nearly 100% of the frame, isolating a fine feature.

- A shot where a minuscule portion of the subject is visible, creating an extreme close-up view.

- A video ending with a narrow field of view focusing intensely on a small subject detail.

- A cinematic extreme close-up shot that enhances the subject’s fine textures or intricate elements.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'extreme_close_up'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['extreme_close_up', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Extreme Wide</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_extreme_wide</code>


<h3>📖 Definition:</h3>
Does the video end with a wide shot?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a extreme wide shot?

- Is the last shot of the video a extreme wide shot?

- Does the video end with a extreme wide shot?

- Is the closing shot of the video a extreme wide shot?

- Does the video finish with a extreme wide shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a extreme wide shot.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a extreme wide shot.

- The video closes with a extreme wide shot.

- The last shot of the video is a extreme wide shot.

- The closing shot is a extreme wide shot.

- The closing shot of the video is a extreme wide shot.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'extreme_wide'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['extreme_wide', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Full (Subject Only)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_full</code>


<h3>📖 Definition:</h3>
Does the video end with a full shot that frames the entire body of the subject without showing excessive surrounding scenery?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a full shot where the subject is clearly framed?

- Is the last shot a full shot capturing the entire body of the subject?

- Does the video finish with a full shot focusing primarily on the subject?

- Is the closing shot a full shot where the subject is the main focus?

- Does the final shot provide a full-body view of the subject?

- Is the last shot a full shot with the subject occupying most of the frame?

- Does the video end with a shot where the subject takes up more than 50% of the frame?

- Is the final frame composed to fully capture the subject while maintaining a clear focus?

- Does the video conclude with a shot that ensures the entire subject is visible?

- Is the last shot taken at a distance that fully includes the subject in the frame?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a full shot, framing the entire subject while maintaining focus on it without showing excessive surrounding scenery.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a full shot where the subject is fully visible.

- The video closes with a full shot, focusing on the entire body of the subject.

- The last shot of the video is a full-body view of the subject.

- The closing shot includes the subject’s entire form with minimal background emphasis.

- The final shot of the video is a full shot, ensuring the whole subject is captured.

- A shot that fully frames the subject while keeping the focus primarily on them.

- A video where the subject takes up most of the frame, emphasizing their full form.

- A shot where the entire subject is visible, but some minor parts (e.g., foot, tail) may be cropped.

- A video ending with a full-body shot that prioritizes the subject over the background.

- A cinematic full shot that ensures the subject is the focal point of the composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'full'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['full', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Medium (Subject Only)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_medium</code>


<h3>📖 Definition:</h3>
Does the video end with a medium shot that frames about half of the subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a medium shot framing the subject from the waist or mid-torso up?

- Is the last shot a medium shot where about half of the subject is visible?

- Does the video finish with a medium shot that provides a balanced view of the subject?

- Is the closing shot a medium shot where the subject occupies around 50% of the frame?

- Does the final shot focus on the subject without being a close-up or full-body shot?

- Is the last shot a medium shot where the framing emphasizes the upper half of the subject?

- Does the video end with a shot where the subject's face and torso are visible?

- Is the final frame a medium shot that keeps the subject in clear view?

- Does the video conclude with a shot that includes the upper half of the subject while maintaining some background context?

- Is the last shot taken at a medium distance, showing about half of the subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a medium shot, framing about half of the subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a medium shot where the subject is visible from the waist or mid-torso up.

- The video closes with a medium shot capturing about half of the subject’s body.

- The last shot of the video is a medium shot, offering a balanced view of the subject.

- The closing shot includes the subject’s upper half while maintaining some scene context.

- The final shot of the video is a medium shot, ensuring the subject is well-framed.

- A shot that frames the subject from the mid-torso up, avoiding close-ups or full-body shots.

- A video where the subject occupies about 50% of the frame while still allowing background details.

- A shot where the subject's face and upper body are clearly visible.

- A video ending with a medium shot that provides a natural composition of the subject.

- A cinematic medium shot that ensures a balanced framing between the subject and background.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'medium'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['medium', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Medium Close Up (Human Only)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_medium_close_up</code>


<h3>📖 Definition:</h3>
Does the video end with a medium close-up shot that frames the human subject from the chest upward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a medium close-up shot featuring a human subject?

- Is the last shot a medium close-up shot where the subject’s face and upper body are visible?

- Does the video finish with a medium close-up shot capturing the subject’s head and shoulders?

- Is the closing shot a medium close-up shot where the subject’s upper arms are partially visible?

- Does the final shot frame the subject closely while still including some upper body?

- Is the last shot a medium close-up that avoids cutting off the head or shoulders?

- Does the video end with a shot that primarily emphasizes the subject’s facial expressions?

- Is the final frame a medium close-up shot that balances facial detail and upper body framing?

- Does the video conclude with a shot that keeps the subject’s face centered while maintaining upper body visibility?

- Is the last shot a tight but not extreme close-up of the subject’s head and chest?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a medium close-up shot, framing the human subject from the chest upward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a medium close-up shot where the subject’s head, shoulders, and upper body are visible.

- The video closes with a medium close-up shot that keeps the subject’s face and some upper body in frame.

- The last shot of the video is a medium close-up that includes the head, shoulders, and part of the arms.

- The closing shot is a medium close-up shot, ensuring the subject’s facial details are clearly visible.

- The final shot of the video is a medium close-up, balancing facial detail with upper body framing.

- A shot that focuses on the subject’s head and shoulders while maintaining a natural composition.

- A video where the subject is framed from the chest upward, avoiding excessive cropping.

- A shot where the subject’s face remains the focal point while still showing some body context.

- A video ending with a medium close-up shot that highlights the subject’s expressions.

- A cinematic medium close-up shot that ensures a clear balance between face and upper body.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'medium_close_up'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['medium_close_up', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Medium Full (Human Only)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_medium_full</code>


<h3>📖 Definition:</h3>
Does the video end with a medium full shot that frames the human subject from the mid-thigh or knee upward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a medium full shot where the subject is framed from the thighs up?

- Is the last shot a medium full shot capturing most of the subject’s body?

- Does the video finish with a medium full shot where the subject’s lower legs are cropped?

- Is the closing shot a medium full shot where the subject is visible from the knees up?

- Does the final shot frame the subject’s body from mid-thigh to head?

- Is the last shot a medium full shot where the subject remains clearly framed?

- Does the video end with a medium full shot that provides a balance between full-body and close-up?

- Is the final frame composed to show the subject’s upper body while maintaining background context?

- Does the video conclude with a medium full shot emphasizing the subject over the environment?

- Is the last shot a medium full shot with a slightly cropped lower half?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that ends with a medium full shot, framing the human subject from mid-thigh or knee upward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a medium full shot where the subject is visible from mid-thigh up.

- The video closes with a medium full shot capturing most of the subject’s body.

- The last shot of the video is a medium full shot, keeping the subject’s upper body in focus.

- The closing shot frames the subject’s body from mid-thigh while maintaining background context.

- The final shot of the video is a medium full shot ensuring the subject is well-framed.

- A shot that captures the subject’s body while avoiding a full-body composition.

- A video where the subject takes up most of the frame while keeping the scene visible.

- A shot where the subject is framed from the knees up, balancing focus and context.

- A video ending with a medium full shot that provides a natural subject framing.

- A cinematic medium full shot that ensures the subject remains the focal point.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'medium_full'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['medium_full', 'unknown']</code>

</details>

<details>
<summary><h2>Shot Size End With Wide</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_end_with_wide</code>


<h3>📖 Definition:</h3>
Does the video end with a wide shot of scenery, or frames the entire subject while keeping ample background context?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video close with a wide shot that balances the subject and surroundings?

- Is the last shot a wide shot where the subject is clearly visible but not dominant?

- Does the video finish with a wide shot that includes both the subject and its environment?

- Is the closing shot a wide shot where the surroundings remain a key part of the composition?

- Does the last shot frame the subject fully while still showing background details?

- Is the final shot a wide view where no single element dominates?

- Does the video end with a shot where the subject occupies around 15-50% of the frame?

- Is the final frame composed to show the subject in relation to its environment?

- Does the video conclude with a shot that is not too far (extreme wide) but still provides context?

- Is the last shot a wide-angle view offering more detail than an extreme wide shot?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video ends with either a wide shot of scenery or a wide shot that frames the entire subject while keeping ample background context.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video ends with a wide shot where the subject is fully visible.

- The video closes with a wide shot, balancing subject and environment.

- The last shot of the video is a wide view that emphasizes both subject and surroundings.

- The closing shot includes the entire subject but maintains scene context.

- The final shot of the video is a wide shot, offering more detail than an extreme wide shot.

- A shot that frames the subject while keeping the background visible.

- A video where the subject occupies 15-50% of the frame while the setting remains clear.

- A shot where the entire subject is visible, but surroundings are also important.

- A video ending with a balanced wide shot where no single element dominates.

- A cinematic wide shot that includes both the subject and contextual environment.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['end'] == 'wide'</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.shot_size_info['end'] not in ['wide', 'unknown']</code>

</details>
