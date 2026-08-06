# Is_always Overview

<details>
<summary><h2>Shot Size Is Close Up</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_close_up</code>


<h3>📖 Definition:</h3>
Does the video maintain a close-up shot throughout, consistently highlighting a distinct part of the subject or scene while still preserving some surrounding context?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in close-up, focusing on the subject's prominent features?

- Does the shot remain a close-up throughout the video where the subject fills most of the frame?

- Is the video consistently framed as a close-up, capturing key details of the subject?

- Does the video maintain a close-up perspective where the subject's face, hands, or defining features remain visible?

- Is the entire sequence shot in close-up, framing the subject closely while providing enough context?

- Does the video keep a consistent close-up that emphasizes specific portions of the subject?

- Is the subject consistently occupying 50%-100% of the frame's height or width throughout?

- Does the video maintain a close-up focus on the subject's defining features?

- Is the entire sequence shot at close range to emphasize the subject's details?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a close-up shot throughout, consistently highlighting a distinct part of the subject or scene while still preserving some surrounding context.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in close-up where the subject's defining features fill most of the frame.

- A sequence maintaining a close-up shot that emphasizes specific details of the subject.

- A video consistently framed in close-up, providing tight yet identifiable framing.

- A sequence shot entirely in close-up, focusing on the subject's key features.

- A video maintaining close-up framing while preserving essential context.

- A shot that consistently captures the subject closely with surrounding context.

- A video where the subject consistently occupies 50%-100% of the frame.

- A sequence maintaining close-up focus on the subject's defining characteristics.

- A video shot entirely in close-up to enhance the subject's presence.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'close_up' and self.cam_setup.shot_size_info['end'] == 'close_up'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['close_up', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['close_up', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Extreme Close Up</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_extreme_close_up</code>


<h3>📖 Definition:</h3>
Does the video maintain an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in extreme close-up, showing minute details?

- Does the shot remain an extreme close-up throughout, focusing on very specific features?

- Is the video consistently framed as an extreme close-up, showing intimate details?

- Does the video maintain an extreme close-up that reveals fine details or textures?

- Is the entire sequence shot in extreme close-up, emphasizing tiny details?

- Does the video keep a consistent extreme close-up that magnifies specific elements?

- Is the subject's detail consistently filling the entire frame throughout?

- Does the video maintain an extreme close-up focus that reveals intricate features?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains an extreme close-up shot throughout, consistently isolating a very small detail of the subject or scene.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in extreme close-up showing minute details.

- A sequence maintaining an extreme close-up that emphasizes specific features.

- A video consistently framed in extreme close-up, revealing intimate details.

- A sequence shot entirely in extreme close-up, focusing on fine textures.

- A video maintaining extreme close-up framing to highlight specific elements.

- A shot that consistently captures the subject's finest details.

- A video where intimate details fill the entire frame throughout.

- A sequence maintaining extreme close-up focus on intricate features.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'extreme_close_up' and self.cam_setup.shot_size_info['end'] == 'extreme_close_up'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['extreme_close_up', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['extreme_close_up', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Extreme Wide</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_extreme_wide</code>


<h3>📖 Definition:</h3>
Does the video maintain an extreme wide shot throughout, consistently emphasizing the setting over any subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in an extreme wide shot, capturing a vast expanse?

- Does the shot remain extremely wide throughout, showing the full scope of the environment?

- Is the video consistently framed as an extreme wide shot, emphasizing the grand scale?

- Does the video maintain an extreme wide perspective where subjects appear tiny in the frame?

- Is the entire sequence shot from an extreme distance, showcasing the broader context?

- Does the video keep a consistent extreme wide angle that captures the entire scene?

- Is the environment consistently shown in its entirety throughout the video?

- Does the video maintain an extreme wide focus that emphasizes the vastness of the setting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains an extreme wide shot throughout, consistently emphasizing the setting over any subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in extreme wide angle showing vast expanses.

- A sequence maintaining an extreme wide shot that emphasizes the environment's scale.

- A video consistently framed to show the maximum possible view of the scene.

- A sequence shot entirely from an extreme distance, minimizing subject size.

- A video maintaining extreme wide framing to capture the complete environment.

- A shot that consistently shows the broader context and setting.

- A video where the vast environment dominates the frame throughout.

- A sequence maintaining an extreme wide perspective on the scene.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'extreme_wide' and self.cam_setup.shot_size_info['end'] == 'extreme_wide'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['extreme_wide', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['extreme_wide', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Full</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_full</code>


<h3>📖 Definition:</h3>
Does the video maintain a full shot throughout, consistently framing the entire body of the subject without showing excessive surrounding scenery?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in a full shot, capturing the complete subject?

- Does the shot remain full-length throughout, showing subjects from head to toe?

- Is the video consistently framed to show the full height of subjects?

- Does the video maintain a full-body perspective of the subjects?

- Is the entire sequence shot to include complete figures?

- Does the video keep a consistent full shot that shows entire subjects?

- Are subjects shown in their entirety throughout the video?

- Does the video maintain a full-body framing from start to finish?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a full shot throughout, consistently framing the entire body of the subject without showing excessive surrounding scenery.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in full view showing complete subjects.

- A sequence maintaining a full shot that captures entire figures.

- A video consistently framed to show subjects from head to toe.

- A sequence shot entirely to include complete subjects.

- A video maintaining full-body framing of all subjects.

- A shot that consistently captures subjects in their entirety.

- A video where complete figures are visible throughout.

- A sequence maintaining full-body perspective of subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'full' and self.cam_setup.shot_size_info['end'] == 'full'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['full', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['full', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Medium</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_medium</code>


<h3>📖 Definition:</h3>
Does the video maintain a medium shot throughout, consistently framing about half of the human subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in medium shot, framing subjects from the waist up?

- Does the shot remain at medium distance throughout the video?

- Is the video consistently framed as a medium shot, showing upper body portions?

- Does the video maintain a medium perspective where subjects are visible from waist up?

- Is the entire sequence shot from a medium distance, focusing on the upper body?

- Does the video keep a consistent medium framing that shows subjects partially?

- Are subjects consistently shown from the waist up throughout the video?

- Does the video maintain a medium-distance focus throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a medium shot throughout, consistently framing about half of the human subject.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in medium view showing subjects from waist up.

- A sequence maintaining a medium shot that captures upper body portions.

- A video consistently framed at medium distance.

- A sequence shot entirely from medium range, focusing on upper bodies.

- A video maintaining medium framing to capture partial figures.

- A shot that consistently shows subjects from the waist up.

- A video where subjects are seen at medium distance throughout.

- A sequence maintaining medium-range perspective of subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'medium' and self.cam_setup.shot_size_info['end'] == 'medium'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['medium', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['medium', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Medium Close Up</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_medium_close_up</code>


<h3>📖 Definition:</h3>
Does the video maintain a medium close-up shot throughout, consistently framing the human subject from the chest upward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in medium close-up, framing subjects from chest up?

- Does the shot remain at medium close-up distance throughout?

- Is the video consistently framed as a medium close-up, showing upper chest and head?

- Does the video maintain a medium close-up perspective focusing on the upper torso and face?

- Is the entire sequence shot from a medium close-up distance?

- Does the video keep a consistent medium close-up framing?

- Are subjects consistently shown from chest up throughout the video?

- Does the video maintain a medium close-up focus that emphasizes facial expressions?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a medium close-up shot throughout, consistently framing the human subject from the chest upward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in medium close-up showing subjects from chest up.

- A sequence maintaining a medium close-up that captures upper torso and face.

- A video consistently framed at medium close-up distance.

- A sequence shot entirely from medium close-up range.

- A video maintaining medium close-up framing to emphasize expressions.

- A shot that consistently shows subjects from chest level up.

- A video where subjects are seen at medium close-up distance throughout.

- A sequence maintaining medium close-up perspective of subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'medium_close_up' and self.cam_setup.shot_size_info['end'] == 'medium_close_up'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['medium_close_up', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['medium_close_up', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Medium Full</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_medium_full</code>


<h3>📖 Definition:</h3>
Does the video maintain a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in medium full shot, framing subjects from knee up?

- Does the shot remain at medium full distance throughout the video?

- Is the video consistently framed as a medium full shot, showing subjects from knees to head?

- Does the video maintain a medium full perspective where most of the body is visible?

- Is the entire sequence shot from a medium full distance?

- Does the video keep a consistent medium full framing that shows subjects from knee level?

- Are subjects consistently shown from knees up throughout the video?

- Does the video maintain a medium full focus throughout?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a medium full shot throughout, consistently framing the human subject from mid-thigh (or knee) upward.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in medium full view showing subjects from knee up.

- A sequence maintaining a medium full shot that captures most of the body.

- A video consistently framed at medium full distance.

- A sequence shot entirely from medium full range.

- A video maintaining medium full framing to show subjects from knees up.

- A shot that consistently shows subjects from knee level.

- A video where subjects are seen at medium full distance throughout.

- A sequence maintaining medium full perspective of subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'medium_full' and self.cam_setup.shot_size_info['end'] == 'medium_full'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['medium_full', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['medium_full', 'unknown'])</code>

</details>

<details>
<summary><h2>Shot Size Is Wide</h2></summary>


<h3>🔵 Label Name:</h3>
<code>shot_size_is_wide</code>


<h3>📖 Definition:</h3>
Does the video maintain a wide shot throughout, consistently showing scenery or framing the entire subject while keeping ample background context?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the entire video filmed in wide shot, capturing subjects and their environment?

- Does the shot remain wide throughout, showing both subjects and surroundings?

- Is the video consistently framed as a wide shot, including contextual space?

- Does the video maintain a wide perspective where subjects and setting are visible?

- Is the entire sequence shot from a wide angle, showing the broader scene?

- Does the video keep a consistent wide framing that includes environmental context?

- Are subjects and their surroundings consistently shown throughout?

- Does the video maintain a wide focus that captures the complete setting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A video that maintains a wide shot throughout, consistently showing scenery or framing the entire subject while keeping ample background context.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video shot entirely in wide view showing subjects and environment.

- A sequence maintaining a wide shot that captures the complete scene.

- A video consistently framed to show subjects in their context.

- A sequence shot entirely from wide range, including surroundings.

- A video maintaining wide framing to capture the broader setting.

- A shot that consistently shows subjects and their environment.

- A video where subjects and surroundings are visible throughout.

- A sequence maintaining wide perspective of the entire scene.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.shot_size_info['start'] == 'wide' and self.cam_setup.shot_size_info['end'] == 'wide'</code>

<h4>🔴 Negative:</h4>
<code>not (self.cam_setup.shot_size_info['start'] in ['wide', 'unknown'] and self.cam_setup.shot_size_info['end'] in ['wide', 'unknown'])</code>

</details>
