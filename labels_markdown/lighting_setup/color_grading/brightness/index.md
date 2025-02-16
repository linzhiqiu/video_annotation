# Brightness Overview

<details>
<summary><h2>Brightness Is Bright</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_bright</code>


<h3>📖 Definition:</h3>
Is the video well-lit with strong lighting, creating a bright and clear scene?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene have a well-lit, vibrant appearance?

- Is the majority of the video illuminated with strong lighting?

- Does the lighting appear bright but not overexposed?

- Are most areas of the scene clearly visible due to bright lighting?

- Does the video feature strong and direct lighting conditions?

- Is the lighting natural but notably bright?

- Does the video have high visibility due to strong lighting?

- Are the shadows minimal due to well-balanced bright lighting?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is well-lit with strong lighting, creating a bright and clear scene.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring strong and well-distributed lighting.

- A scene that appears well-lit with bright exposure.

- A shot where most areas are illuminated with good visibility.

- A video where the brightness level is high but balanced.

- A sequence where the lighting is bright, ensuring clear detail.

- A scene with strong, energetic lighting without excessive exposure.

- A video with high-key lighting, emphasizing clarity and brightness.

- A shot where the scene is illuminated brightly, enhancing visibility.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'bright'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'bright'</code>

</details>

<details>
<summary><h2>Brightness Is Brighter Than Normal</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_brighter_than_normal</code>


<h3>📖 Definition:</h3>
Is the video noticeably brighter than a standard neutral lighting setup?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video have a bright or very bright appearance?

- Is the scene well-lit with strong or intense lighting?

- Does the exposure make the video appear noticeably luminous?

- Is the lighting level above normal brightness?

- Does the scene look significantly brighter than a balanced lighting setup?

- Is the video characterized by an abundance of light?

- Does the lighting style make the visuals pop with strong brightness?

- Is the overall brightness of the video higher than average?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is noticeably brighter than a standard neutral lighting setup.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with high or very high brightness levels.

- A video featuring lighting that is more intense than neutral.

- A shot where most areas are well-lit or even overexposed.

- A video that appears noticeably bright due to strong lighting.

- A scene where bright exposure makes details highly visible.

- A video where strong lighting emphasizes a luminous atmosphere.

- A shot where brightness enhances clarity and vibrancy.

- A video with a lighting setup that is significantly brighter than normal.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness in ['very_bright', 'bright']</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness not in ['very_bright', 'bright']</code>

</details>

<details>
<summary><h2>Brightness Is Changing (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_changing</code>


<h3>📖 Definition:</h3>
Does the video’s brightness shift dynamically over time?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the lighting intensity change noticeably throughout the video?

- Is there a fluctuation in brightness levels across different scenes?

- Does the video feature transitions between bright and dark areas?

- Is the exposure level dynamically adjusted over time?

- Does the lighting environment shift continuously throughout the sequence?

- Is the brightness level inconsistent across the video?

- Does the scene transition between well-lit and low-lit moments?

- Is the video’s brightness level actively changing?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video’s brightness shifts dynamically over time.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video where brightness fluctuates across scenes.

- A sequence featuring dynamic changes in light intensity.

- A shot where lighting levels transition between bright and dark.

- A video that features varying exposure levels over time.

- A scene where brightness shifts in response to different moments.

- A video with intentional, fluctuating brightness adjustments.

- A cinematic effect using evolving light intensity.

- A sequence where brightness levels are deliberately inconsistent.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'complex_changing'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'complex_changing'</code>

</details>

<details>
<summary><h2>Brightness Is Contrasting (Complex)</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_contrasting</code>


<h3>📖 Definition:</h3>
Does the video have strong contrast between bright, dark, and neutral areas?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene mix bright highlights with deep shadows?

- Is there a stark contrast between illuminated and dark areas?

- Does the video feature both intense brightness and deep darkness?

- Are light and shadow strongly contrasted within the frame?

- Does the shot balance extreme brightness with intense darkness?

- Is there high-key and low-key lighting present simultaneously?

- Does the video emphasize strong brightness contrast?

- Are bright and dark regions equally prominent in the composition?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has strong contrast between bright, dark, and neutral areas.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with extreme light and dark contrasts in the same frame.

- A shot featuring bright highlights alongside deep shadows.

- A sequence where brightness levels are dramatically different.

- A video with simultaneous high exposure and low-lit areas.

- A scene emphasizing extreme contrast between light and shadow.

- A shot where both very bright and very dark areas coexist.

- A video with stark, dramatic lighting differences.

- A sequence designed with a strong balance of illumination and darkness.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'complex_contrasting'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'complex_contrasting'</code>

</details>

<details>
<summary><h2>Brightness Is Dark</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_dark</code>


<h3>📖 Definition:</h3>
Is the video predominantly dark, with dim lighting and prominent shadows?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene have a low-light, moody appearance?

- Is most of the video shot in dim lighting conditions?

- Does the video feature dark exposure with visible shadows?

- Are details in the video partially obscured by low lighting?

- Does the scene use darkness to create atmosphere or tension?

- Is the brightness level intentionally kept low for effect?

- Does the video rely on minimal lighting, making some elements hard to see?

- Is the lighting style in the video consistent with low-key cinematography?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is predominantly dark, with dim lighting and prominent shadows.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with low lighting, emphasizing shadows and contrast.

- A video where dim lighting dominates the frame.

- A shot featuring dark exposure, making some details less visible.

- A sequence where darkness creates a moody or mysterious atmosphere.

- A video with controlled low brightness for cinematic effect.

- A scene with minimal light, relying on shadow and contrast.

- A shot where visibility is reduced due to dark lighting conditions.

- A sequence emphasizing mood through reduced brightness.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'dark'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'dark'</code>

</details>

<details>
<summary><h2>Brightness Is Darker Than Normal</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_darker_than_normal</code>


<h3>📖 Definition:</h3>
Is the video noticeably darker than a standard neutral lighting setup?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video have a dark or very dark appearance?

- Is the scene dimly lit, with prominent shadows?

- Does the exposure make the video appear noticeably low-light?

- Is the lighting level below normal brightness?

- Does the scene look significantly darker than a balanced lighting setup?

- Is the video characterized by low visibility and deep shadows?

- Does the lighting style create a moody, dramatic effect?

- Is the overall brightness of the video lower than average?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is noticeably darker than a standard neutral lighting setup.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with low or very low brightness levels.

- A video featuring lighting that is dimmer than neutral.

- A shot where most areas are in shadow or barely visible.

- A video that appears noticeably dark due to limited lighting.

- A scene where reduced exposure creates a moody atmosphere.

- A video where low brightness makes details harder to see.

- A shot where shadows dominate the frame, reducing clarity.

- A video with a lighting setup that is significantly darker than normal.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness in ['dark', 'very_dark']</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness not in ['dark', 'very_dark']</code>

</details>

<details>
<summary><h2>Brightness Is Neutral</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_neutral</code>


<h3>📖 Definition:</h3>
Is the video’s brightness balanced, neither too bright nor too dark?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene feature an evenly lit environment?

- Is the lighting neither overly bright nor too dark?

- Does the video maintain a natural balance of brightness?

- Is the exposure level consistent without extreme highlights or shadows?

- Does the scene have a moderate brightness level, without strong contrasts?

- Is the lighting in the video soft and evenly distributed?

- Does the video avoid extremes of brightness or darkness?

- Is the brightness well-balanced for a neutral appearance?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video’s brightness is balanced, neither too bright nor too dark.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with an evenly balanced brightness level.

- A shot where lighting is neutral and well-distributed.

- A scene maintaining a natural and moderate brightness.

- A sequence where exposure remains steady without strong highlights or shadows.

- A video featuring soft, natural lighting without extremes.

- A shot with moderate brightness that does not overpower the scene.

- A video where light intensity is natural and unobtrusive.

- A sequence maintaining a consistent, neutral brightness level.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'neutral'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'neutral'</code>

</details>

<details>
<summary><h2>Brightness Is Very Bright</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_very_bright</code>


<h3>📖 Definition:</h3>
Is the video excessively bright, with overexposure that reduces detail visibility?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the scene overexposed and extremely bright?

- Does the lighting in the video appear excessively intense?

- Is most of the frame dominated by strong, overpowering brightness?

- Does the scene appear washed out due to very high exposure?

- Are darker areas appearing lighter due to strong illumination?

- Is the majority of the video affected by extreme brightness?

- Does the video have an overwhelming amount of light?

- Are most areas of the video too bright to retain clear details?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is excessively bright, with overexposure that reduces detail visibility.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A scene with extreme brightness, causing details to be washed out.

- A video where the exposure is excessively high.

- A shot dominated by bright light, reducing shadows and contrast.

- A scene appearing overwhelmingly bright due to intense illumination.

- A video where high exposure makes most details difficult to see.

- A sequence where even darker areas appear relatively bright.

- A video with overexposed lighting across the frame.

- A shot where excessive brightness dominates the composition.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'very_bright'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'very_bright'</code>

</details>

<details>
<summary><h2>Brightness Is Very Dark</h2></summary>


<h3>🔵 Label Name:</h3>
<code>brightness_is_very_dark</code>


<h3>📖 Definition:</h3>
Is the video extremely dark, with barely any visible details due to minimal lighting?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the scene have near-complete darkness?

- Is most of the video shrouded in deep shadows?

- Does the video feature extremely low visibility due to lack of light?

- Are details almost impossible to discern because of the darkness?

- Does the scene rely on extreme darkness for dramatic effect?

- Is the brightness level too low to clearly see subjects?

- Does the video contain areas that are nearly pitch black?

- Is most of the frame underexposed, making it difficult to see details?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video is extremely dark, with barely any visible details due to minimal lighting.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot where most of the frame is nearly pitch black.

- A video with extremely low lighting, making details difficult to discern.

- A scene where visibility is severely reduced due to darkness.

- A shot featuring deep shadows with very limited illumination.

- A sequence emphasizing an extremely dark atmosphere.

- A video with underexposed elements, making the scene almost unreadable.

- A shot where most of the details are lost in heavy darkness.

- A scene that is barely lit, resulting in near-total darkness.

</details>

<h4>🟢 Positive:</h4>
<code>self.lighting_setup.brightness == 'very_dark'</code>

<h4>🔴 Negative:</h4>
<code>self.lighting_setup.brightness != 'very_dark'</code>

</details>
