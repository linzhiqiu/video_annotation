# Policy Comparison Report

This document compares four different versions of policies for each of the 5 main policy classes:

| Version | Description |
|---------|-------------|
| **human_short** | Task-specific single-sentence prompt for human annotators, capturing the essence of the description while omitting most details. |
| **human** | Task-specific multi-sentence prompt for human annotators with clear detail requirements. |
| **human_detailed** | Expanded human prompt with explicit sub-aspects (A, B, C, D, etc.) and definitions. |
| **model_without_label** | Model policy (agnostic to human-labeled ground truth). |

---

## Subject Description

### 1. human_short

**Rendered version:**

Describe the main subjects in the video and their most distinctive traits.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Describe the main subjects in the video and their most distinctive traits.
```

</details>

### 2. human

**Rendered version:**

Provide a concise yet informative description of the subjects in this video, including their types, appearances (e.g., clothing, facial expressions, gender, ethnicity, color, shape), and poses. When multiple subjects are present, clearly distinguish them using unique traits, position, actions, or relationships, and describe them in temporal or prominence-based order to ensure clarity.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subjects in this video, including their types, appearances (e.g., clothing, facial expressions, gender, ethnicity, color, shape), and poses. When multiple subjects are present, clearly distinguish them using unique traits, position, actions, or relationships, and describe them in temporal or prominence-based order to ensure clarity.
```

</details>

### 3. human_detailed

*Source: `caption/human/subject_description.txt`*

**Rendered version:**

Provide a concise yet informative description of the subjects in this video, including their types, appearances (e.g., clothing, facial expressions, gender, ethnicity, color, shape), and poses. When multiple subjects are present, clearly distinguish them using unique traits, position, actions, or relationships, and describe them in temporal or prominence-based order to ensure clarity.

#### 1. Subject Type  
1. Identify the subject's type precisely.  
   - **Examples:**  
     1. "man," "woman," "dog," "car," "tree."  
     2. Avoid vague terms like "thing" or "item."  
2. If the subject type is ambiguous, provide your best judgment and explain your reasoning.  

#### 2. Visual Attributes  
1. Describe the subject's key visual characteristics using specific and descriptive language.  
2. Consider the following aspects where relevant:  

   - **Appearance:**  
     1. **People:** Include details like clothing (colors and style), hairstyle, facial hair, age (if discernible), gender, ethnicity (if relevant and clear), and facial expression.  
     2. **Objects:** Describe their color, material, shape, and distinguishing marks (e.g., "smooth," "rough," "furry," "metallic," "black," "red," etc.).  

   - **Pose/Orientation:**  
     1. Describe the subject's posture and orientation within the frame (e.g., "standing," "sitting," "lying down," "walking," "facing left," "arms raised," "facing the camera").  
     2. Pay particular attention to objects not in their usual state (e.g., a tilted lamp, a book lying open face down).  

#### 3. How to Refer to Multiple Subjects  
1. When there is more than one important person or object, make sure it's clear which one you are referring to.  
2. Use the following strategies for clarity:  

   - **Type:** The simplest way to refer to a subject is by its category, e.g., “the man,” “the dog,” or “the tree.”  
   - **Attributes:** If multiple subjects belong to the same category, use distinguishing features:  

     1. **Unique Appearance:** Highlight distinct traits, such as "the woman in the red dress," "the man with the beard," "the blue car," or "the largest tree."  
     2. **Location:** Specify position within the scene, e.g., "the man on the left," "the dog in the background," "the car in the midground," or "the building in the middle."  
     3. **Action:** Describe their activity, e.g., "the person walking," "the child playing with a ball," "the bird flying," or "the cat sitting on the windowsill."  
     4. **Relationship to Each Other:** For example, "the man next to the woman" (spatial relationship), “the first man that enters the frame” (temporal relationship), or "the two cars parked side by side."  

   - **Combining Descriptions:** For maximum clarity, combine multiple attributes.  
     - **Example:**  
       1. "The woman in the red dress on the left, talking on her phone."  
       2. "The dog in the background, running toward the ball."  

3. The key is to provide enough detail so that anyone reading the description can easily tell which subject you are referring to.  

#### 4. Order Matters When Describing Multiple Subjects  
1. When describing multiple subjects, the order in which you mention them matters. Prioritize elements based on their importance in the video.  
2. Follow these guidelines:  

   - **Temporal Order:** If the scene unfolds over time, describe subjects in the order they appear.  
     - **Example:** "First, the car speeds past, then the cyclist enters the frame."  
   - **Prominence-Based Order:** If temporal order isn’t relevant, start with the most visually striking or important subject before moving on to less prominent ones.  
     - **Example:** "The video shows a bright red sports car in the foreground. In the midground, a blue sedan is right behind it."  

#### 5. If the Video Contains Multiple Subjects or Complex Subject Transitions  
1. **Determine the Primary Focus:**  

   - If there is a single clear main subject:  
     1. Describe the main subject in detail, explaining why this subject is the focus while others are not.  
     2. Include relevant details such as appearance, actions, and positioning that make the subject stand out.  
     3. Provide a less detailed overview of secondary subjects, mentioning only their general presence or relationship to the main subject.  

   - If the main subject is unclear:  
     1. Describe subjects in prominence-based order (e.g., humans before objects).  

   - If there is no clear main subject:  
     1. Give a brief overview of all subjects without excessive detail.  

2. **Identify Subject Transitions:**  

   - If the focus shifts between subjects, specify the type of transition:  
     1. **Subject Revealing:** A new subject enters the frame.  
     2. **Subject Disappearing:** A subject exits or is no longer visible.  
     3. **Subject Switching:** The focus shifts from one subject to another through rack focus or other camera movements.  
     4. **Other Complex Changes:** Subjects alternate focus multiple times.  

   - Explain how the transition occurs (through subject movement or camera movement).  

Following these steps ensures a more fluent and coherent subject description. In cases of subject switching, always describe subjects in **temporal order** for clarity.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subjects in this video, including their types, appearances (e.g., clothing, facial expressions, gender, ethnicity, color, shape), and poses. When multiple subjects are present, clearly distinguish them using unique traits, position, actions, or relationships, and describe them in temporal or prominence-based order to ensure clarity.

#### 1. Subject Type  
1. Identify the subject's type precisely.  
   - **Examples:**  
     1. "man," "woman," "dog," "car," "tree."  
     2. Avoid vague terms like "thing" or "item."  
2. If the subject type is ambiguous, provide your best judgment and explain your reasoning.  

#### 2. Visual Attributes  
1. Describe the subject's key visual characteristics using specific and descriptive language.  
2. Consider the following aspects where relevant:  

   - **Appearance:**  
     1. **People:** Include details like clothing (colors and style), hairstyle, facial hair, age (if discernible), gender, ethnicity (if relevant and clear), and facial expression.  
     2. **Objects:** Describe their color, material, shape, and distinguishing marks (e.g., "smooth," "rough," "furry," "metallic," "black," "red," etc.).  

   - **Pose/Orientation:**  
     1. Describe the subject's posture and orientation within the frame (e.g., "standing," "sitting," "lying down," "walking," "facing left," "arms raised," "facing the camera").  
     2. Pay particular attention to objects not in their usual state (e.g., a tilted lamp, a book lying open face down).  

#### 3. How to Refer to Multiple Subjects  
1. When there is more than one important person or object, make sure it's clear which one you are referring to.  
2. Use the following strategies for clarity:  

   - **Type:** The simplest way to refer to a subject is by its category, e.g., “the man,” “the dog,” or “the tree.”  
   - **Attributes:** If multiple subjects belong to the same category, use distinguishing features:  

     1. **Unique Appearance:** Highlight distinct traits, such as "the woman in the red dress," "the man with the beard," "the blue car," or "the largest tree."  
     2. **Location:** Specify position within the scene, e.g., "the man on the left," "the dog in the background," "the car in the midground," or "the building in the middle."  
     3. **Action:** Describe their activity, e.g., "the person walking," "the child playing with a ball," "the bird flying," or "the cat sitting on the windowsill."  
     4. **Relationship to Each Other:** For example, "the man next to the woman" (spatial relationship), “the first man that enters the frame” (temporal relationship), or "the two cars parked side by side."  

   - **Combining Descriptions:** For maximum clarity, combine multiple attributes.  
     - **Example:**  
       1. "The woman in the red dress on the left, talking on her phone."  
       2. "The dog in the background, running toward the ball."  

3. The key is to provide enough detail so that anyone reading the description can easily tell which subject you are referring to.  

#### 4. Order Matters When Describing Multiple Subjects  
1. When describing multiple subjects, the order in which you mention them matters. Prioritize elements based on their importance in the video.  
2. Follow these guidelines:  

   - **Temporal Order:** If the scene unfolds over time, describe subjects in the order they appear.  
     - **Example:** "First, the car speeds past, then the cyclist enters the frame."  
   - **Prominence-Based Order:** If temporal order isn’t relevant, start with the most visually striking or important subject before moving on to less prominent ones.  
     - **Example:** "The video shows a bright red sports car in the foreground. In the midground, a blue sedan is right behind it."  

#### 5. If the Video Contains Multiple Subjects or Complex Subject Transitions  
1. **Determine the Primary Focus:**  

   - If there is a single clear main subject:  
     1. Describe the main subject in detail, explaining why this subject is the focus while others are not.  
     2. Include relevant details such as appearance, actions, and positioning that make the subject stand out.  
     3. Provide a less detailed overview of secondary subjects, mentioning only their general presence or relationship to the main subject.  

   - If the main subject is unclear:  
     1. Describe subjects in prominence-based order (e.g., humans before objects).  

   - If there is no clear main subject:  
     1. Give a brief overview of all subjects without excessive detail.  

2. **Identify Subject Transitions:**  

   - If the focus shifts between subjects, specify the type of transition:  
     1. **Subject Revealing:** A new subject enters the frame.  
     2. **Subject Disappearing:** A subject exits or is no longer visible.  
     3. **Subject Switching:** The focus shifts from one subject to another through rack focus or other camera movements.  
     4. **Other Complex Changes:** Subjects alternate focus multiple times.  

   - Explain how the transition occurs (through subject movement or camera movement).  

Following these steps ensures a more fluent and coherent subject description. In cases of subject switching, always describe subjects in **temporal order** for clarity.
```

</details>

### 4. model_without_label

**Rendered version:**

Provide a concise yet informative description of the subjects in this video. Keep the description concise and clear, focusing on subject types and visual attributes. You should describe the video by combining details from the frames without referring to any specific one (e.g., don’t mention things like "first frame" or "last frame"), and avoid using terms like "image" or "frame." Don't mention the background or motion unless it's necessary to distinguish subjects by location, action, or relationships. You must avoid describing what is not visible or what you are unsure about. You must use simple, natural English and ensure the description is a clear, concise, and coherent paragraph that highlights the most essential details. You must avoid subjective adjectives that convey emotions. Whenever you mention a subject, please describe its key visual attributes in detail. Return only the one-paragraph video description without Markdown formatting or introductory text.

Clearly identify each subject’s type, using precise terms such as “man,” “woman,” “dog,” “car,” or “tree,” rather than vague words like “thing” or “item.” If the subject type is ambiguous, use your best judgment and briefly explain your reasoning.

Describe key visual attributes with specific and descriptive language. For people, include details such as clothing color and style, skin tone, hairstyle, facial hair, age (if discernible), gender, ethnicity (if relevant and clear), and facial expression. For objects, describe their color, material, shape, and distinguishing features like texture or markings. Additionally, note the subject’s pose and orientation within the frame, such as standing, sitting, walking, or facing a certain direction. Pay attention to any objects that are not in their usual state, like a tilted lamp or an open book lying face down.

If there are multiple subjects to describe, ensure clarity in referring to each. The simplest way is by type, such as “the man,” “the dog,” or “the tree.” If multiple subjects belong to the same category, distinguish them using unique appearance traits (e.g., “the woman in the red dress,” “the man with the beard”), location within the scene (e.g., “the man on the left,” “the car in the midground”), actions (e.g., “the child playing with a ball,” “the bird flying”), or relationships to each other (e.g., “the man next to the woman,” “the first man that enters the frame”). Also, when describing multiple subjects, the order in which they are mentioned matters. Prioritize based on relevance, starting with the largest or most centered subject. If the scene unfolds over time, describe subjects in the order they appear. If temporal order isn’t relevant, begin with the most visually striking or important subject before moving to less prominent ones. The goal is to provide enough detail so that anyone reading the description can easily identify each subject.

When shot transitions occur, describe the subject in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subjects change from one segment to the next.

If the video is a scenery shot without salient subjects, you do not need to describe a specific subject. Instead, concisely specify the type of scenery shot (e.g., landscape, cityscape) in a single fluent paragraph. Briefly explain why there is no main subject, for example by noting that the focus is on the environment, atmosphere, or scale rather than on a particular object, using one to three sentences.

If the video features salient human or non-human subjects, focus your description on them. If the video features multiple subjects with a clear focus, you may describe the main subject in detail and briefly mention the secondary subjects. If the video features multiple subjects without a clear main focus, describe the types of subjects without going into too much detail. You may also describe the subjects collectively as a group.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subjects in this video. Keep the description concise and clear, focusing on subject types and visual attributes. You should describe the video by combining details from the frames without referring to any specific one (e.g., don’t mention things like "first frame" or "last frame"), and avoid using terms like "image" or "frame." Don't mention the background or motion unless it's necessary to distinguish subjects by location, action, or relationships. You must avoid describing what is not visible or what you are unsure about. You must use simple, natural English and ensure the description is a clear, concise, and coherent paragraph that highlights the most essential details. You must avoid subjective adjectives that convey emotions. Whenever you mention a subject, please describe its key visual attributes in detail. Return only the one-paragraph video description without Markdown formatting or introductory text.

Clearly identify each subject’s type, using precise terms such as “man,” “woman,” “dog,” “car,” or “tree,” rather than vague words like “thing” or “item.” If the subject type is ambiguous, use your best judgment and briefly explain your reasoning.

Describe key visual attributes with specific and descriptive language. For people, include details such as clothing color and style, skin tone, hairstyle, facial hair, age (if discernible), gender, ethnicity (if relevant and clear), and facial expression. For objects, describe their color, material, shape, and distinguishing features like texture or markings. Additionally, note the subject’s pose and orientation within the frame, such as standing, sitting, walking, or facing a certain direction. Pay attention to any objects that are not in their usual state, like a tilted lamp or an open book lying face down.

If there are multiple subjects to describe, ensure clarity in referring to each. The simplest way is by type, such as “the man,” “the dog,” or “the tree.” If multiple subjects belong to the same category, distinguish them using unique appearance traits (e.g., “the woman in the red dress,” “the man with the beard”), location within the scene (e.g., “the man on the left,” “the car in the midground”), actions (e.g., “the child playing with a ball,” “the bird flying”), or relationships to each other (e.g., “the man next to the woman,” “the first man that enters the frame”). Also, when describing multiple subjects, the order in which they are mentioned matters. Prioritize based on relevance, starting with the largest or most centered subject. If the scene unfolds over time, describe subjects in the order they appear. If temporal order isn’t relevant, begin with the most visually striking or important subject before moving to less prominent ones. The goal is to provide enough detail so that anyone reading the description can easily identify each subject.

When shot transitions occur, describe the subject in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subjects change from one segment to the next.

If the video is a scenery shot without salient subjects, you do not need to describe a specific subject. Instead, concisely specify the type of scenery shot (e.g., landscape, cityscape) in a single fluent paragraph. Briefly explain why there is no main subject, for example by noting that the focus is on the environment, atmosphere, or scale rather than on a particular object, using one to three sentences.

If the video features salient human or non-human subjects, focus your description on them. If the video features multiple subjects with a clear focus, you may describe the main subject in detail and briefly mention the secondary subjects. If the video features multiple subjects without a clear main focus, describe the types of subjects without going into too much detail. You may also describe the subjects collectively as a group.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail.
```

</details>

---

## Scene Composition & Dynamics

### 1. human_short

**Rendered version:**

Describe the setting and environment of the video.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Describe the setting and environment of the video.
```

</details>

### 2. human

**Rendered version:**

Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, overlays, and notable visual elements. If subjects are present, the scene description should complement their descriptions by establishing their location and possible context. Aim to give enough detail to convey the setting while avoiding unnecessary information.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, overlays, and notable visual elements. If subjects are present, the scene description should complement their descriptions by establishing their location and possible context. Aim to give enough detail to convey the setting while avoiding unnecessary information.
```

</details>

### 3. human_detailed

*Source: `caption/human/scene_composition_dynamics.txt`*

**Rendered version:**

Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, overlays, and notable visual elements. If subjects are present, the scene description should complement their descriptions by establishing their location and possible context. Aim to give enough detail to convey the setting while avoiding unnecessary information.

#### 1. Point of View (if relevant)  
1. Indicate how the scene is captured, such as first-person, dashcam, screen recording, drone shot, or an objective or detached view.  
2. Focus on how the perspective influences the viewer’s perception of the scene.  

#### 2. Setting (Where does it happen?)  
1. **Scene Type:** Specify whether the setting is indoors or outdoors using precise and descriptive terms. Avoid vague descriptions.  
   - **Good:** "A sunlit café with large windows and wooden tables."  
   - **Avoid:** "An indoor place."  

2. **Visual Attributes:** Provide relevant details about the scene.  
   - **Location:**  
     1. If the setting is a well-known place, state it explicitly (e.g., "Times Square," "Grand Canyon," "Tokyo subway station").  
     2. If the exact location is unclear, describe its defining visual elements, such as:  
        - "A narrow alley with graffiti-covered walls."  
        - "A vast desert with rolling dunes."  
        - "A dimly lit space with metal walls."  
   
   - **Time of Day:** Indicate whether the scene occurs during the day, night, or a transitional period like sunset or dawn.  
   
   - **Architectural and Natural Features:** Mention buildings, roads, vegetation, water bodies, or other landscape elements that structure the scene.  
     - **Examples:**  
       1. "A winding mountain path surrounded by tall pines."  
       2. "A bustling marketplace with food stalls and colorful banners."  
   
   - **Weather Conditions:** If outdoors, describe weather effects.  
     - **Examples:**  
       1. "A rainy street with wet pavement reflecting city lights."  
       2. "A snowy mountain pass covered in thick fog."  
   
   - **Furniture and Props (for indoor scenes):** Identify relevant furnishings that establish the setting.  
     - **Examples:**  
       1. "A wooden desk cluttered with books and a vintage lamp."  
       2. "A hospital room with a bed, medical monitors, and IV stands."  
   
   - **Style:** If notable, describe color schemes or stylistic choices.  
     - **Examples:**  
       1. "A monochromatic, grayscale environment."  
       2. "A vibrant and colorful carnival scene with neon lights."  
  
  - **Overlay:** If overlays are present, describe their apperance and location.
    - **Examples:**
      1. "White sans-serif subtitles reading ‘We should leave now’ appear at the bottom center of the frame."
      2. "A rectangular minimap HUD with roads and markers is overlaid in the bottom left corner."

#### 3. Movement and Changes in the Environment  
1. Describe any natural or human-made motion within the scene.  

2. **Natural Motion:**  
   - **Examples:**  
     1. "Leaves sway in the wind."  
     2. "Waves crash against the shore."  
     3. "As the sun sets, it casts long shadows on the trees."  

3. **Man-Made Motion:**  
   - **Examples:**  
     1. "Traffic moves steadily on the highway."  
     2. "A train passes in the distance."  
     3. "Factory workers operate machinery in the background."  

4. **Crowd & Background Activity:**  
   - **Examples:**  
     1. "Pedestrians walk along a busy street."  
     2. "A crowd cheers and waves hands."  
     3. "The office starts empty, but employees gradually arrive and take their seats."  

#### 4. Scene Transitions  
1. If the scene changes, describe how it happens in the order it appears.  

2. **Time-Based Transitions:**  
   - **Example:** "The shot begins during the day but transitions to nighttime."  

3. **Movement-Based Transitions:**  
   - **Example:** "The shot begins with a view of a quiet street. Then, the camera pans to reveal a hidden alley behind the main street."  

#### 5. How to Refer to Multiple Scene Elements  
1. Use precise and concise language when referring to different elements within the scene.  
   - **Examples:**  
     1. "In the background, a mountain range is visible."  
     2. "On the left side of the frame, there is a large tree."  
     3. "A wide river runs through the center, with a bridge arching over it."  

2. Prioritize the most prominent and important aspects of the scene.  
3. Start with the overall setting, then move on to more specific details.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, overlays, and notable visual elements. If subjects are present, the scene description should complement their descriptions by establishing their location and possible context. Aim to give enough detail to convey the setting while avoiding unnecessary information.

#### 1. Point of View (if relevant)  
1. Indicate how the scene is captured, such as first-person, dashcam, screen recording, drone shot, or an objective or detached view.  
2. Focus on how the perspective influences the viewer’s perception of the scene.  

#### 2. Setting (Where does it happen?)  
1. **Scene Type:** Specify whether the setting is indoors or outdoors using precise and descriptive terms. Avoid vague descriptions.  
   - **Good:** "A sunlit café with large windows and wooden tables."  
   - **Avoid:** "An indoor place."  

2. **Visual Attributes:** Provide relevant details about the scene.  
   - **Location:**  
     1. If the setting is a well-known place, state it explicitly (e.g., "Times Square," "Grand Canyon," "Tokyo subway station").  
     2. If the exact location is unclear, describe its defining visual elements, such as:  
        - "A narrow alley with graffiti-covered walls."  
        - "A vast desert with rolling dunes."  
        - "A dimly lit space with metal walls."  
   
   - **Time of Day:** Indicate whether the scene occurs during the day, night, or a transitional period like sunset or dawn.  
   
   - **Architectural and Natural Features:** Mention buildings, roads, vegetation, water bodies, or other landscape elements that structure the scene.  
     - **Examples:**  
       1. "A winding mountain path surrounded by tall pines."  
       2. "A bustling marketplace with food stalls and colorful banners."  
   
   - **Weather Conditions:** If outdoors, describe weather effects.  
     - **Examples:**  
       1. "A rainy street with wet pavement reflecting city lights."  
       2. "A snowy mountain pass covered in thick fog."  
   
   - **Furniture and Props (for indoor scenes):** Identify relevant furnishings that establish the setting.  
     - **Examples:**  
       1. "A wooden desk cluttered with books and a vintage lamp."  
       2. "A hospital room with a bed, medical monitors, and IV stands."  
   
   - **Style:** If notable, describe color schemes or stylistic choices.  
     - **Examples:**  
       1. "A monochromatic, grayscale environment."  
       2. "A vibrant and colorful carnival scene with neon lights."  
  
  - **Overlay:** If overlays are present, describe their apperance and location.
    - **Examples:**
      1. "White sans-serif subtitles reading ‘We should leave now’ appear at the bottom center of the frame."
      2. "A rectangular minimap HUD with roads and markers is overlaid in the bottom left corner."

#### 3. Movement and Changes in the Environment  
1. Describe any natural or human-made motion within the scene.  

2. **Natural Motion:**  
   - **Examples:**  
     1. "Leaves sway in the wind."  
     2. "Waves crash against the shore."  
     3. "As the sun sets, it casts long shadows on the trees."  

3. **Man-Made Motion:**  
   - **Examples:**  
     1. "Traffic moves steadily on the highway."  
     2. "A train passes in the distance."  
     3. "Factory workers operate machinery in the background."  

4. **Crowd & Background Activity:**  
   - **Examples:**  
     1. "Pedestrians walk along a busy street."  
     2. "A crowd cheers and waves hands."  
     3. "The office starts empty, but employees gradually arrive and take their seats."  

#### 4. Scene Transitions  
1. If the scene changes, describe how it happens in the order it appears.  

2. **Time-Based Transitions:**  
   - **Example:** "The shot begins during the day but transitions to nighttime."  

3. **Movement-Based Transitions:**  
   - **Example:** "The shot begins with a view of a quiet street. Then, the camera pans to reveal a hidden alley behind the main street."  

#### 5. How to Refer to Multiple Scene Elements  
1. Use precise and concise language when referring to different elements within the scene.  
   - **Examples:**  
     1. "In the background, a mountain range is visible."  
     2. "On the left side of the frame, there is a large tree."  
     3. "A wide river runs through the center, with a bridge arching over it."  

2. Prioritize the most prominent and important aspects of the scene.  
3. Start with the overall setting, then move on to more specific details.
```

</details>

### 4. model_without_label

**Rendered version:**

Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, and notable visual elements like overlays. For notable visual elements within the scene, describe their color, material, shape, and distinguishing features like texture or markings. If subjects are present, ensure their placement and context complement the scene without excessive detail. You should describe the video by combining details from the frames without referring to any specific one (e.g., don’t mention things like "first frame" or "last frame"), and avoid using terms like "image" or "frame." Focus on the setting and scenery rather than detailed subject descriptions. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B.' Do not infer the role of the scene setting. Do not explain what the scene emphasizes or highlights. Return only the one-paragraph video description without Markdown formatting or introductory text.

If relevant, indicate the **point of view**, such as first-person, drone shot, or dashcam, and describe how it influences the viewer’s perception. Specify the **setting** by clearly identifying whether it is indoors or outdoors, using precise language. If the location is known, state it explicitly (e.g., "Times Square" or "Tokyo subway station"). Otherwise, describe defining features such as “a narrow alley with graffiti-covered walls” or “a vast desert with rolling dunes.” Mention the **time of day** and any notable **architectural or natural features**, such as buildings, roads, forests, or bodies of water. Include relevant **weather conditions** if applicable, like “a rainy street with wet pavement reflecting city lights” or “a snowy mountain pass covered in thick fog.” For indoor settings, describe key **furniture or props** that establish the environment, such as “a wooden desk cluttered with books and a vintage lamp.” If notable, mention the **style** of the scene, such as a monochromatic color scheme or a vibrant carnival with neon lights. If the video contains **overlay elements** such as text, titles, subtitles, captions, icons, watermarks, heads-up displays (HUD), or framing elements, specify that they are overlays (not part of the scene) and describe their content and placement.

If the scene involves **motion or changes**, describe natural elements like wind blowing through trees or waves crashing against the shore, as well as human-made movements such as traffic flowing on a highway or pedestrians walking along a busy street. If **scene transitions** occur, explain how they happen, whether through changes in time (e.g., “The shot transitions from day to night”) or movement-based shifts (e.g., “The camera pans to reveal an alley behind the main street”). Use precise language to refer to different elements within the scene, prioritizing the most prominent details and organizing descriptions logically from the overall setting to more specific features.

When shot transitions occur, describe the scene in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the scene changes from one segment to the next.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the overall scene, including the point of view, environment, setting, time of day, and notable visual elements like overlays. For notable visual elements within the scene, describe their color, material, shape, and distinguishing features like texture or markings. If subjects are present, ensure their placement and context complement the scene without excessive detail. You should describe the video by combining details from the frames without referring to any specific one (e.g., don’t mention things like "first frame" or "last frame"), and avoid using terms like "image" or "frame." Focus on the setting and scenery rather than detailed subject descriptions. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B.' Do not infer the role of the scene setting. Do not explain what the scene emphasizes or highlights. Return only the one-paragraph video description without Markdown formatting or introductory text.

If relevant, indicate the **point of view**, such as first-person, drone shot, or dashcam, and describe how it influences the viewer’s perception. Specify the **setting** by clearly identifying whether it is indoors or outdoors, using precise language. If the location is known, state it explicitly (e.g., "Times Square" or "Tokyo subway station"). Otherwise, describe defining features such as “a narrow alley with graffiti-covered walls” or “a vast desert with rolling dunes.” Mention the **time of day** and any notable **architectural or natural features**, such as buildings, roads, forests, or bodies of water. Include relevant **weather conditions** if applicable, like “a rainy street with wet pavement reflecting city lights” or “a snowy mountain pass covered in thick fog.” For indoor settings, describe key **furniture or props** that establish the environment, such as “a wooden desk cluttered with books and a vintage lamp.” If notable, mention the **style** of the scene, such as a monochromatic color scheme or a vibrant carnival with neon lights. If the video contains **overlay elements** such as text, titles, subtitles, captions, icons, watermarks, heads-up displays (HUD), or framing elements, specify that they are overlays (not part of the scene) and describe their content and placement.

If the scene involves **motion or changes**, describe natural elements like wind blowing through trees or waves crashing against the shore, as well as human-made movements such as traffic flowing on a highway or pedestrians walking along a busy street. If **scene transitions** occur, explain how they happen, whether through changes in time (e.g., “The shot transitions from day to night”) or movement-based shifts (e.g., “The camera pans to reveal an alley behind the main street”). Use precise language to refer to different elements within the scene, prioritizing the most prominent details and organizing descriptions logically from the overall setting to more specific features.

When shot transitions occur, describe the scene in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the scene changes from one segment to the next.
```

</details>

---

## Subject Motion & Dynamics

### 1. human_short

**Rendered version:**

Describe the main actions of the subjects in the video.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Describe the main actions of the subjects in the video.
```

</details>

### 2. human

**Rendered version:**

Provide a concise yet informative description of the subject’s motion in this video, including individual actions, subject–object or subject–subject interactions, and group activities when a crowd is present. Please note that event order matters! If multiple actions occur, present them in chronological order (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch").

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subject’s motion in this video, including individual actions, subject–object or subject–subject interactions, and group activities when a crowd is present. Please note that event order matters! If multiple actions occur, present them in chronological order (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch").
```

</details>

### 3. human_detailed

*Source: `caption/human/subject_motion_dynamics.txt`*

**Rendered version:**

Provide a concise yet informative description of the subject’s motion in this video, including individual actions, subject–object or subject–subject interactions, and group activities when a crowd is present. Please note that event order matters! If multiple actions occur, present them in chronological order (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch").

#### 1. Individual Subject Actions  
1. Describe the actions and dynamic changes of individual subjects, ensuring clarity on the manner of movement.
2. **Examples:**  
   - **Good:** "A runner sprints across the finish line."  
     - **Instead of:** "A person is running."  
   - **Good:** "A hummingbird hovers delicately, wings beating rapidly as it sips nectar from a flower."  
     - **Instead of:** "A bird is flying."  
   - **Good:** "A caterpillar slowly inches its way along a leaf."  
     - **Instead of:** "An insect is moving."  
   - **Good:** "A time-lapse shows a sunflower turning its head to follow the sun across the sky."  
     - **Instead of:** "A plant is rotating."  
   - **Good:** "A seed sprouts, sending a root down and a sprout up."  
     - **Instead of:** "A seed is growing."  

#### 2. Subject-Object Interactions
1. Describe the interactions between subjects and objects in the video. Specify the type of interaction and the object involved. If relevant, detail the effect of the interaction.  
2. **Examples:**  
   - **Good:** "A chef flips an omelet in a pan."  
     - **Instead of:** "A person is using a pan."  
   - **Good:** "A dog fetches a tennis ball thrown by its owner."  
     - **Instead of:** "A dog is playing."  
   - **Good:** "A construction worker operates a jackhammer, breaking up the pavement."  
     - **Instead of:** "A person is working."  
   - **Good:** "A car collides with a traffic sign, bending it at a sharp angle."  
     - **Instead of:** "A car crashed."  

#### 3. Subject-Subject Interactions
1. Describe the interactions between different subjects in this video. Describe the nature of the interaction and the relative movements of the subjects.  
2. **Examples:**  
   - **Good:** "Two boxers exchange blows in the ring, circling each other cautiously."  
     - **Instead of:** "People are fighting."  
   - **Good:** "A mother bird feeds worms to her chicks in the nest."  
     - **Instead of:** "Birds are together."  
   - **Good:** "Dancers perform a complex tango, their movements synchronized and graceful."  
     - **Instead of:** "People are dancing."  
   - **Good:** "A pride of lions hunts a zebra, surrounding it and closing in for the kill."  
     - **Instead of:** "Animals are interacting."  

#### 4. Group Activities
1. **Summarize collective behaviors or actions of a group**, describing the overall movement and any coordinated actions. If relevant, specify the type of group.  
2. **Examples:**  
   - **Good:** "A flock of geese flies in a V-formation across the horizon."  
     - **Instead of:** "Birds are flying."  
   - **Good:** "A crowd of protesters marches down the street, carrying signs and banners."  
     - **Instead of:** "People are walking."  
   - **Good:** "A swarm of bees buzzes around a hive."  
     - **Instead of:** "Insects are moving."  
   - **Good:** "A school of fish swims in unison, changing direction as one unit."  
     - **Instead of:** "Fish are swimming."

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subject’s motion in this video, including individual actions, subject–object or subject–subject interactions, and group activities when a crowd is present. Please note that event order matters! If multiple actions occur, present them in chronological order (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch").

#### 1. Individual Subject Actions  
1. Describe the actions and dynamic changes of individual subjects, ensuring clarity on the manner of movement.
2. **Examples:**  
   - **Good:** "A runner sprints across the finish line."  
     - **Instead of:** "A person is running."  
   - **Good:** "A hummingbird hovers delicately, wings beating rapidly as it sips nectar from a flower."  
     - **Instead of:** "A bird is flying."  
   - **Good:** "A caterpillar slowly inches its way along a leaf."  
     - **Instead of:** "An insect is moving."  
   - **Good:** "A time-lapse shows a sunflower turning its head to follow the sun across the sky."  
     - **Instead of:** "A plant is rotating."  
   - **Good:** "A seed sprouts, sending a root down and a sprout up."  
     - **Instead of:** "A seed is growing."  

#### 2. Subject-Object Interactions
1. Describe the interactions between subjects and objects in the video. Specify the type of interaction and the object involved. If relevant, detail the effect of the interaction.  
2. **Examples:**  
   - **Good:** "A chef flips an omelet in a pan."  
     - **Instead of:** "A person is using a pan."  
   - **Good:** "A dog fetches a tennis ball thrown by its owner."  
     - **Instead of:** "A dog is playing."  
   - **Good:** "A construction worker operates a jackhammer, breaking up the pavement."  
     - **Instead of:** "A person is working."  
   - **Good:** "A car collides with a traffic sign, bending it at a sharp angle."  
     - **Instead of:** "A car crashed."  

#### 3. Subject-Subject Interactions
1. Describe the interactions between different subjects in this video. Describe the nature of the interaction and the relative movements of the subjects.  
2. **Examples:**  
   - **Good:** "Two boxers exchange blows in the ring, circling each other cautiously."  
     - **Instead of:** "People are fighting."  
   - **Good:** "A mother bird feeds worms to her chicks in the nest."  
     - **Instead of:** "Birds are together."  
   - **Good:** "Dancers perform a complex tango, their movements synchronized and graceful."  
     - **Instead of:** "People are dancing."  
   - **Good:** "A pride of lions hunts a zebra, surrounding it and closing in for the kill."  
     - **Instead of:** "Animals are interacting."  

#### 4. Group Activities
1. **Summarize collective behaviors or actions of a group**, describing the overall movement and any coordinated actions. If relevant, specify the type of group.  
2. **Examples:**  
   - **Good:** "A flock of geese flies in a V-formation across the horizon."  
     - **Instead of:** "Birds are flying."  
   - **Good:** "A crowd of protesters marches down the street, carrying signs and banners."  
     - **Instead of:** "People are walking."  
   - **Good:** "A swarm of bees buzzes around a hive."  
     - **Instead of:** "Insects are moving."  
   - **Good:** "A school of fish swims in unison, changing direction as one unit."  
     - **Instead of:** "Fish are swimming."
```

</details>

### 4. model_without_label

**Rendered version:**

Provide a concise yet informative description of the subject’s motion in this video, ensuring actions are presented in **chronological order** if multiple movements occur (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch"). Focus on the subject's motion rather than repeating details already included in the human-written subject descriptions. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B.' Return only the one-paragraph video description without Markdown formatting or introductory text.

If the subject in the video has no movement, please briefly mention that without going into too much detail.

Please only describe the content of the video. Don't mention the details of the subject's appearance unless you need to differentiate between multiple subjects by their appearance. Clearly describe the subject's motion.

Avoid abstract descriptions, such as "The car maintains a low, sleek profile as it maneuvers the bend, emphasizing its speed and agility" and "emphasizing its speed and agility as it maneuvers through the turn."

Below are detailed instructions:

Describe **individual subject actions** with clarity, specifying how they move rather than using generic descriptions. For example, instead of “a person is running,” say “a runner sprints across the finish line.”

If the subject interacts with an **object**, specify the type of interaction and its effect. Instead of “a person is working,” say “a construction worker operates a jackhammer, breaking up the pavement.”

If there are **interactions between subjects**, describe the nature of their relationship and movements relative to each other. Instead of “people are fighting,” say “two boxers exchange blows in the ring, circling each other cautiously.”

If there are collective behaviors for a group of subjects, describe **group activities** with specificity. Instead of “birds are flying,” say “a flock of geese flies in a V-formation across the horizon.” Instead of “people are walking,” say “a crowd of protesters marches down the street, carrying signs and banners.” Clearly convey the type of group, their coordinated actions, and any notable patterns in their movement.

When shot transitions occur, describe the motion of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subject’s motion changes between segments.

If the video is a scenery shot without salient subjects, you do not need to describe subject motion. Instead, briefly note this in one to three sentences.

If the video features salient human or non-human subjects, focus your description on their motion. When there are multiple subjects with a clear focus, describe the main subject’s motion in detail and briefly mention the motion of secondary subjects. If there are multiple subjects without a clear main focus, describe their motion collectively and concisely without going into excessive detail.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail along with the description of their motion.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the subject’s motion in this video, ensuring actions are presented in **chronological order** if multiple movements occur (e.g., "The bird first takes flight, then soars in a circle, and finally lands on a branch"). Focus on the subject's motion rather than repeating details already included in the human-written subject descriptions. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B.' Return only the one-paragraph video description without Markdown formatting or introductory text.

If the subject in the video has no movement, please briefly mention that without going into too much detail.

Please only describe the content of the video. Don't mention the details of the subject's appearance unless you need to differentiate between multiple subjects by their appearance. Clearly describe the subject's motion.

Avoid abstract descriptions, such as "The car maintains a low, sleek profile as it maneuvers the bend, emphasizing its speed and agility" and "emphasizing its speed and agility as it maneuvers through the turn."

Below are detailed instructions:

Describe **individual subject actions** with clarity, specifying how they move rather than using generic descriptions. For example, instead of “a person is running,” say “a runner sprints across the finish line.”

If the subject interacts with an **object**, specify the type of interaction and its effect. Instead of “a person is working,” say “a construction worker operates a jackhammer, breaking up the pavement.”

If there are **interactions between subjects**, describe the nature of their relationship and movements relative to each other. Instead of “people are fighting,” say “two boxers exchange blows in the ring, circling each other cautiously.”

If there are collective behaviors for a group of subjects, describe **group activities** with specificity. Instead of “birds are flying,” say “a flock of geese flies in a V-formation across the horizon.” Instead of “people are walking,” say “a crowd of protesters marches down the street, carrying signs and banners.” Clearly convey the type of group, their coordinated actions, and any notable patterns in their movement.

When shot transitions occur, describe the motion of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how the subject’s motion changes between segments.

If the video is a scenery shot without salient subjects, you do not need to describe subject motion. Instead, briefly note this in one to three sentences.

If the video features salient human or non-human subjects, focus your description on their motion. When there are multiple subjects with a clear focus, describe the main subject’s motion in detail and briefly mention the motion of secondary subjects. If there are multiple subjects without a clear main focus, describe their motion collectively and concisely without going into excessive detail.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail along with the description of their motion.
```

</details>

---

## Spatial Framing & Dynamics

### 1. human_short

**Rendered version:**

Describe how the subjects or elements are framed and how they move within the scene.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Describe how the subjects or elements are framed and how they move within the scene.
```

</details>

### 2. human

**Rendered version:**

Provide a concise yet informative description of how subjects and elements are spatially framed within the scene, including the shot size of the subject (or the shot size of the scenery if there is no salient subject), their 2D position within the frame, spatial depth within the scene (foreground, middle ground, background), height relative to the camera, and any notable spatial movement.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of how subjects and elements are spatially framed within the scene, including the shot size of the subject (or the shot size of the scenery if there is no salient subject), their 2D position within the frame, spatial depth within the scene (foreground, middle ground, background), height relative to the camera, and any notable spatial movement.
```

</details>

### 3. human_detailed

*Source: `caption/human/spatial_framing_dynamics.txt`*

**Rendered version:**

Provide a concise yet informative description of how subjects and elements are spatially framed within the scene, including the shot size of the subject (or the shot size of the scenery if there is no salient subject), their 2D position within the frame, spatial depth within the scene (foreground, middle ground, background), height relative to the camera, and any notable spatial movement.

#### 1. Framing of Subjects (How Are They Positioned in the Shot?)  
1. **Shot Size:** Indicate how much of the subject is visible, such as close-up, medium shot, wide shot, or a varying shot that does not follow a fixed framing. Focus on how framing affects the perception of the subject rather than forcing a specific shot type.  
   - **Examples:**  
     1. "A close-up captures the subject’s face."  
     2. "A medium shot frames the person from the waist up."  
     3. "A wide shot shows a person standing in an open field."  
     4. "The camera tracks a skateboarder in an unsteady manner, mostly capturing the skateboarder’s lower body."  

2. **Position within the Frame:** Describe the subject’s approximate location within the frame.  
   - **Examples:**  
     1. "The person is in the bottom-left corner of the frame."  
     2. "The person is on the right of the frame."  

3. **Depth within the Scene:** Describe the subject’s placement in relation to the foreground, midground, or background.  
   - **Examples:**  
     1. "In the foreground, a person is sitting in front of a computer."  

4. **Position within the Scene:** Describe the subject’s physical placement in the scene.  
   - **Examples:**  
     1. "The woman in the midground stands near a window, looking outside."  

5. **Height Relative to the Camera:** Describe the subject’s vertical positioning relative to the camera.  
   - **Examples:**  
     1. "The man is framed at eye level."  
     2. "A low-angle shot captures the person from below."  

#### 2. Framing of Scenery (How Is the Environment Captured?)  
1. **Shot Size:** Indicate how the environment is framed, such as a wide shot, close-up, or a dynamic framing that shifts within the scene.  
   - **Examples:**  
     1. "A wide shot of a mountain range stretching across the horizon."  
     2. "A close-up of raindrops hitting a window."  

2. **Spatial Composition:** Describe how elements appear within the frame.  
   - **Spatial Positioning:** Specify where key elements appear within the frame.  
     - **Examples:**  
       1. "A symmetrical shot of a hallway positioned at the center of the frame, leading toward a vanishing point."  
       2. "A large tree stands in the bottom-left corner of the frame."  
       3. "A streetlamp is visible on the right side of the frame."  

   - **Depth (Foreground, Midground, and Background Elements):** Describe relationships between elements at different depths.  
     - **Examples:**  
       1. "In the foreground, a bicycle is parked to the right against a fence, while in the background, skyscrapers rise against the sky."  
       2. "The midground features a river cutting through the landscape."  

#### 3. Spatial Motion Within the Frame (How Do Subjects or Scene Elements Move?)  
1. If shot size or spatial position changes within the frame, describe how these transitions happen clearly, specifying both the initial and final state.  

2. **Changes in Shot Size and Spatial Position for Subjects:**  
   - **Examples:**  
     1. "A medium shot of a man’s upper body near a doorway transitions into a close-up of his face as he walks toward the camera."  
     2. "A woman walking from the background to the foreground transitions from a wide shot capturing both her and the street scenery to a medium shot focusing on her lower body."  
     3. "A cyclist moves from the left to the right side of the frame, maintaining a full shot throughout."  
     4. "A full-body shot of a child at eye level shifts as the camera tilts upward, reframing them from a low angle looking up."  
     5. "A wide shot captures a person near a park bench, who then walks diagonally from the bottom-left to the top-right corner of the frame."  

3. **Changes in Shot Size and Spatial Composition for Scenery Shots:**  
   - **Examples:**  
     1. "The shot begins with an aerial view of a city skyline, then tilts downward to focus on a busy intersection."  
     2. "The camera moves forward, transitioning from a wide view of a dense forest to a close-up of a single tree trunk covered in moss."  

#### 4. If the Video Contains Multiple Subjects or Complex Subject Transitions  
1. **Determine the Primary Focus:**  
   - If there is a single clear main subject:  
     1. Follow the “Framing of Subjects” section to describe this subject in detail, including shot size and spatial position.  
     2. Follow "Spatial Motion Within the Frame" to describe any spatial motion and changes.  
     3. Provide a less detailed overview of secondary subjects.  

   - If the main subject is unclear:  
     1. Describe subjects’ spatial position and movement in prominence-based order (e.g., humans before objects).  
     2. Instead of determining the shot size based on a random subject, specify it based on the most prominent subject (e.g., a human) if one is clearly dominant.  
     3. Otherwise, if the subjects are relatively similar in size, use the average shot size.  
     4. If the shot is even more complex, directly state which (part of) subjects are visible and which are not.  

   - If there is no clear main subject:  
     1. Provide a general overview of subjects' spatial positions without excessive detail.  
     2. Do not specify shot size, as it is not meaningful in this case. You may optionally describe the shot size following "Framing of Scenery" instead.  

2. **Identify Subject Transitions:**  
   - If subjects reveal, disappear, switch focus, or undergo other complex changes, describe their shot size (if relevant), spatial position, and movement accordingly.  
   - Ensure that the description follows the temporal order in which subjects appear.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of how subjects and elements are spatially framed within the scene, including the shot size of the subject (or the shot size of the scenery if there is no salient subject), their 2D position within the frame, spatial depth within the scene (foreground, middle ground, background), height relative to the camera, and any notable spatial movement.

#### 1. Framing of Subjects (How Are They Positioned in the Shot?)  
1. **Shot Size:** Indicate how much of the subject is visible, such as close-up, medium shot, wide shot, or a varying shot that does not follow a fixed framing. Focus on how framing affects the perception of the subject rather than forcing a specific shot type.  
   - **Examples:**  
     1. "A close-up captures the subject’s face."  
     2. "A medium shot frames the person from the waist up."  
     3. "A wide shot shows a person standing in an open field."  
     4. "The camera tracks a skateboarder in an unsteady manner, mostly capturing the skateboarder’s lower body."  

2. **Position within the Frame:** Describe the subject’s approximate location within the frame.  
   - **Examples:**  
     1. "The person is in the bottom-left corner of the frame."  
     2. "The person is on the right of the frame."  

3. **Depth within the Scene:** Describe the subject’s placement in relation to the foreground, midground, or background.  
   - **Examples:**  
     1. "In the foreground, a person is sitting in front of a computer."  

4. **Position within the Scene:** Describe the subject’s physical placement in the scene.  
   - **Examples:**  
     1. "The woman in the midground stands near a window, looking outside."  

5. **Height Relative to the Camera:** Describe the subject’s vertical positioning relative to the camera.  
   - **Examples:**  
     1. "The man is framed at eye level."  
     2. "A low-angle shot captures the person from below."  

#### 2. Framing of Scenery (How Is the Environment Captured?)  
1. **Shot Size:** Indicate how the environment is framed, such as a wide shot, close-up, or a dynamic framing that shifts within the scene.  
   - **Examples:**  
     1. "A wide shot of a mountain range stretching across the horizon."  
     2. "A close-up of raindrops hitting a window."  

2. **Spatial Composition:** Describe how elements appear within the frame.  
   - **Spatial Positioning:** Specify where key elements appear within the frame.  
     - **Examples:**  
       1. "A symmetrical shot of a hallway positioned at the center of the frame, leading toward a vanishing point."  
       2. "A large tree stands in the bottom-left corner of the frame."  
       3. "A streetlamp is visible on the right side of the frame."  

   - **Depth (Foreground, Midground, and Background Elements):** Describe relationships between elements at different depths.  
     - **Examples:**  
       1. "In the foreground, a bicycle is parked to the right against a fence, while in the background, skyscrapers rise against the sky."  
       2. "The midground features a river cutting through the landscape."  

#### 3. Spatial Motion Within the Frame (How Do Subjects or Scene Elements Move?)  
1. If shot size or spatial position changes within the frame, describe how these transitions happen clearly, specifying both the initial and final state.  

2. **Changes in Shot Size and Spatial Position for Subjects:**  
   - **Examples:**  
     1. "A medium shot of a man’s upper body near a doorway transitions into a close-up of his face as he walks toward the camera."  
     2. "A woman walking from the background to the foreground transitions from a wide shot capturing both her and the street scenery to a medium shot focusing on her lower body."  
     3. "A cyclist moves from the left to the right side of the frame, maintaining a full shot throughout."  
     4. "A full-body shot of a child at eye level shifts as the camera tilts upward, reframing them from a low angle looking up."  
     5. "A wide shot captures a person near a park bench, who then walks diagonally from the bottom-left to the top-right corner of the frame."  

3. **Changes in Shot Size and Spatial Composition for Scenery Shots:**  
   - **Examples:**  
     1. "The shot begins with an aerial view of a city skyline, then tilts downward to focus on a busy intersection."  
     2. "The camera moves forward, transitioning from a wide view of a dense forest to a close-up of a single tree trunk covered in moss."  

#### 4. If the Video Contains Multiple Subjects or Complex Subject Transitions  
1. **Determine the Primary Focus:**  
   - If there is a single clear main subject:  
     1. Follow the “Framing of Subjects” section to describe this subject in detail, including shot size and spatial position.  
     2. Follow "Spatial Motion Within the Frame" to describe any spatial motion and changes.  
     3. Provide a less detailed overview of secondary subjects.  

   - If the main subject is unclear:  
     1. Describe subjects’ spatial position and movement in prominence-based order (e.g., humans before objects).  
     2. Instead of determining the shot size based on a random subject, specify it based on the most prominent subject (e.g., a human) if one is clearly dominant.  
     3. Otherwise, if the subjects are relatively similar in size, use the average shot size.  
     4. If the shot is even more complex, directly state which (part of) subjects are visible and which are not.  

   - If there is no clear main subject:  
     1. Provide a general overview of subjects' spatial positions without excessive detail.  
     2. Do not specify shot size, as it is not meaningful in this case. You may optionally describe the shot size following "Framing of Scenery" instead.  

2. **Identify Subject Transitions:**  
   - If subjects reveal, disappear, switch focus, or undergo other complex changes, describe their shot size (if relevant), spatial position, and movement accordingly.  
   - Ensure that the description follows the temporal order in which subjects appear.
```

</details>

### 4. model_without_label

**Rendered version:**

Analyze the subjects and elements in this video and provide a concise yet informative description of how they are spatially framed within the scene, including **shot size, position, depth, height relative to the camera, and any changes**. Your goal is to describe the **spatial framing and dynamics** of the subjects and elements within the shot, considering both their placement within the frame and their relative positions in the scene. Ensure the description covers any notable spatial movements. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B'. Return only the one-paragraph video description without Markdown formatting or introductory text.

First, specify the **shot size** based on the subject's size in the frame if major subjects are present. If the shot size is unclear, describe how much of the subject is visible. If no major subject exists (e.g., a scenery shot), describe the shot size in relation to the scenery.

Next, describe the **spatial position of subjects and elements in the video**, if relevant. Indicate their approximate **2D position** within the frame using terms like **left, right, bottom left, bottom right, top right, top left, bottom, top, or center**. Additionally, describe their **3D position** within the scene as **foreground, middle ground, or background**. Analyze as many elements as possible, and for each element mentioned, provide both its **2D and 3D position**.

Finally, describe the **camera’s height relative to the subject**, if relevant. Indicate whether the camera is positioned at the subject's height, above them, or below them. We already have this information provided at the end. If it’s not provided, try to describe it by yourself.

If **shot size or spatial position** changes, describe how these transitions occur clearly, specifying both the **initial and final states**.

When shot transitions occur, describe the spatial framing and movement of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how their framing, position, depth, and height relative to the camera change between segments.

If the video is a scenery shot without salient subjects, specify the shot size of the scenery (e.g., wide shot, close-up) and describe any movement within it.

If the video features salient human or non-human subjects, focus your description on their spatial framing and movement. When there are multiple subjects with a clear focus, describe the main subject’s spatial framing and movement in detail and briefly mention those of secondary subjects. If there are multiple subjects without a clear main focus, describe their spatial composition and movement collectively and concisely.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail along with their spatial framing and movement.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Analyze the subjects and elements in this video and provide a concise yet informative description of how they are spatially framed within the scene, including **shot size, position, depth, height relative to the camera, and any changes**. Your goal is to describe the **spatial framing and dynamics** of the subjects and elements within the shot, considering both their placement within the frame and their relative positions in the scene. Ensure the description covers any notable spatial movements. Avoid describing anything not visible or uncertain. Use simple, natural English to create a clear, concise, and coherent paragraph that highlights essential details. Avoid emotional or subjective adjectives. Avoid speculative statements like 'there might be,' 'it appears,' or ambiguous options like 'A or B'. Return only the one-paragraph video description without Markdown formatting or introductory text.

First, specify the **shot size** based on the subject's size in the frame if major subjects are present. If the shot size is unclear, describe how much of the subject is visible. If no major subject exists (e.g., a scenery shot), describe the shot size in relation to the scenery.

Next, describe the **spatial position of subjects and elements in the video**, if relevant. Indicate their approximate **2D position** within the frame using terms like **left, right, bottom left, bottom right, top right, top left, bottom, top, or center**. Additionally, describe their **3D position** within the scene as **foreground, middle ground, or background**. Analyze as many elements as possible, and for each element mentioned, provide both its **2D and 3D position**.

Finally, describe the **camera’s height relative to the subject**, if relevant. Indicate whether the camera is positioned at the subject's height, above them, or below them. We already have this information provided at the end. If it’s not provided, try to describe it by yourself.

If **shot size or spatial position** changes, describe how these transitions occur clearly, specifying both the **initial and final states**.

When shot transitions occur, describe the spatial framing and movement of subjects in each segment separately, noting the type of transition (e.g., hard cut, soft transition) and explaining how their framing, position, depth, and height relative to the camera change between segments.

If the video is a scenery shot without salient subjects, specify the shot size of the scenery (e.g., wide shot, close-up) and describe any movement within it.

If the video features salient human or non-human subjects, focus your description on their spatial framing and movement. When there are multiple subjects with a clear focus, describe the main subject’s spatial framing and movement in detail and briefly mention those of secondary subjects. If there are multiple subjects without a clear main focus, describe their spatial composition and movement collectively and concisely.

If the video features subjects revealing, disappearing, or switching, describe the transition in detail along with their spatial framing and movement.
```

</details>

---

## Camera Framing & Dynamics

### 1. human_short

**Rendered version:**

Describe the camera's perspective, lens, speed, movement, and focus.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Describe the camera's perspective, lens, speed, movement, and focus.
```

</details>

### 2. human

**Rendered version:**

Provide a concise yet informative description of the video and camera configuration, including playback speed, lens distortion (if present), camera angle, camera height relative to the ground plane, camera movements (translation, rotation, zooming, steadiness, speed, intensity, and complexity), and focus (depth, focus plane, and any changes in focus).

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the video and camera configuration, including playback speed, lens distortion (if present), camera angle, camera height relative to the ground plane, camera movements (translation, rotation, zooming, steadiness, speed, intensity, and complexity), and focus (depth, focus plane, and any changes in focus).
```

</details>

### 3. human_detailed

*Source: `caption/human/camera_framing_dynamics.txt`*

**Rendered version:**

Provide a concise yet informative description of the video and camera configuration, including playback speed, lens distortion (if present), camera angle, camera height relative to the ground plane, camera movements (translation, rotation, zooming, steadiness, speed, intensity, and complexity), and focus (depth, focus plane, and any changes in focus).

#### 1. Video Speed  
1. If the video speed is altered, specify the type of speed change.  
   - **Examples:**  
     1. **Time-lapse**: Events unfold significantly faster. "Clouds move rapidly across the sky."  
     2. **Fast-Motion**: Slightly faster than real-time (1x-3x speed).  
     3. **Slow-Motion**: Slower playback than real-time.  
     4. **Stop-Motion**: Frame-by-frame animation with discrete movements.  
     5. **Speed-Ramp**: A mix of fast and slow speeds within the same video.  
     6. **Time-Reversed**: The video plays in reverse.  

#### 2. Lens Distortion  
1. If lens distortion is present, describe the type and degree.  
   - **Examples:**  
     1. **Fisheye**: Extreme distortion with strong curvature, making the edges appear bent outward.  
     2. **Barrel**: Mild distortion causing straight lines near the edges to bow outward.  

#### 3. Camera Height (Relative to the Ground)  
1. If the camera height is discernible, specify one of the following:  
   - Aerial-level, Overhead-level, Eye-level, Hip-level, Ground-level, Water-level, Underwater.  
2. Mention any camera movement that causes height changes.  

#### 4. Camera Angle (Relative to the Ground)  
1. If the camera angle is discernible, specify one of the following:  
   - Bird’s Eye, High Angle, Level Angle, Low Angle, Worm’s Eye.  
2. Mention any camera movement that changes the camera angle.  

#### 5. Dutch/Canted Angle  
1. If a Dutch angle is present, describe its behavior.  
   - **Examples:**  
     1. "The Dutch angle remains fixed throughout the shot."  
     2. "The Dutch angle varies, changing due to camera rolling."  

#### 6. Camera Focus and Depth of Field  
1. If the type of camera focus is indeterminable, explain whether the video lacks a realistic depth of field effect, is too blurry, or does not appear to be filmed with a real camera.  
2. If discernible, specify whether the camera has a shallow depth of field.  
   - If the depth of field is deep, state **"Deep Focus."**  
   - If the depth of field is shallow, describe it as **shallow** or **extremely shallow**.  
   - Specify which part of the frame is in focus (**Foreground, Midground, Background, Out-of-Focus**).  
   - If the focus changes, describe both the reason for the focus plane transition (e.g., rack/pull focus, focus tracking) and how the focus plane shifts (for example, from the midground to the foreground to focus on a nearby object).

#### 7. Camera Movement  
1. If the camera is completely static, no further description is required.  
2. If the camera is shaking or wobbling, describe the degree.  
   - **Examples:** minimal, moderate, or severe shaking.  
3. If the camera follows or moves with an object, describe how it moves with the subject.  
   - **Examples:** Tracking Shot, Arcing, Craning.  
4. Describe why the camera is moving (e.g., tracking a subject, revealing a scene, creating emphasis).  
5. Use precise movement terms to describe the motion.  
   - **Examples:**  
     1. **Dolly In/Out**: Moving forward or backward toward or away from the subject.  
     2. **Zoom In/Out**: Changing focal length to create the illusion of moving closer or farther.  
     3. **Pan Left/Right**: Rotating the camera horizontally.  
     4. **Truck Left/Right**: Moving the camera laterally left or right.  
     5. **Tilt Up/Down**: Angling the camera up or down.  
     6. **Pedestal Up/Down**: Lifting or lowering the camera while keeping it level.  
     7. **Rolling Clockwise/Counterclockwise**: Rotating the camera around its lens axis.  
     8. **Arcing Clockwise/Counterclockwise**: Circling the camera around a subject or the frame center horizontally.
     9. **Craning Up/Down**: Circling the camera around a subject or the frame center vertically.  
6. Mention the speed of movement if noticeably slow or fast. If different movements occur at different speeds, clearly distinguish them.  
   - **Example:**  
     - "The camera slowly dollies forward while trucking quickly to the right."  
7. Describe motion in temporal order if multiple movements occur.  
   - **Example:**  
     - "The camera first pans right, then tilts upward to follow the subject."  
8. If the movement appears too fragmented or random, avoid excessive detail.  
   - **Excessive Detail (Too much description):**  
     - "As the player explores, the camera moves left, then quickly tilts up, followed by a rapid pan right. The player hesitates, looking down, then abruptly swings the camera left again before slightly tilting upward and making another quick turn to the right."  
   - **Better Description (Concise & clear):**  
     - "The first-person camera moves randomly as the player looks around, frequently changing direction without a clear pattern."

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the video and camera configuration, including playback speed, lens distortion (if present), camera angle, camera height relative to the ground plane, camera movements (translation, rotation, zooming, steadiness, speed, intensity, and complexity), and focus (depth, focus plane, and any changes in focus).

#### 1. Video Speed  
1. If the video speed is altered, specify the type of speed change.  
   - **Examples:**  
     1. **Time-lapse**: Events unfold significantly faster. "Clouds move rapidly across the sky."  
     2. **Fast-Motion**: Slightly faster than real-time (1x-3x speed).  
     3. **Slow-Motion**: Slower playback than real-time.  
     4. **Stop-Motion**: Frame-by-frame animation with discrete movements.  
     5. **Speed-Ramp**: A mix of fast and slow speeds within the same video.  
     6. **Time-Reversed**: The video plays in reverse.  

#### 2. Lens Distortion  
1. If lens distortion is present, describe the type and degree.  
   - **Examples:**  
     1. **Fisheye**: Extreme distortion with strong curvature, making the edges appear bent outward.  
     2. **Barrel**: Mild distortion causing straight lines near the edges to bow outward.  

#### 3. Camera Height (Relative to the Ground)  
1. If the camera height is discernible, specify one of the following:  
   - Aerial-level, Overhead-level, Eye-level, Hip-level, Ground-level, Water-level, Underwater.  
2. Mention any camera movement that causes height changes.  

#### 4. Camera Angle (Relative to the Ground)  
1. If the camera angle is discernible, specify one of the following:  
   - Bird’s Eye, High Angle, Level Angle, Low Angle, Worm’s Eye.  
2. Mention any camera movement that changes the camera angle.  

#### 5. Dutch/Canted Angle  
1. If a Dutch angle is present, describe its behavior.  
   - **Examples:**  
     1. "The Dutch angle remains fixed throughout the shot."  
     2. "The Dutch angle varies, changing due to camera rolling."  

#### 6. Camera Focus and Depth of Field  
1. If the type of camera focus is indeterminable, explain whether the video lacks a realistic depth of field effect, is too blurry, or does not appear to be filmed with a real camera.  
2. If discernible, specify whether the camera has a shallow depth of field.  
   - If the depth of field is deep, state **"Deep Focus."**  
   - If the depth of field is shallow, describe it as **shallow** or **extremely shallow**.  
   - Specify which part of the frame is in focus (**Foreground, Midground, Background, Out-of-Focus**).  
   - If the focus changes, describe both the reason for the focus plane transition (e.g., rack/pull focus, focus tracking) and how the focus plane shifts (for example, from the midground to the foreground to focus on a nearby object).

#### 7. Camera Movement  
1. If the camera is completely static, no further description is required.  
2. If the camera is shaking or wobbling, describe the degree.  
   - **Examples:** minimal, moderate, or severe shaking.  
3. If the camera follows or moves with an object, describe how it moves with the subject.  
   - **Examples:** Tracking Shot, Arcing, Craning.  
4. Describe why the camera is moving (e.g., tracking a subject, revealing a scene, creating emphasis).  
5. Use precise movement terms to describe the motion.  
   - **Examples:**  
     1. **Dolly In/Out**: Moving forward or backward toward or away from the subject.  
     2. **Zoom In/Out**: Changing focal length to create the illusion of moving closer or farther.  
     3. **Pan Left/Right**: Rotating the camera horizontally.  
     4. **Truck Left/Right**: Moving the camera laterally left or right.  
     5. **Tilt Up/Down**: Angling the camera up or down.  
     6. **Pedestal Up/Down**: Lifting or lowering the camera while keeping it level.  
     7. **Rolling Clockwise/Counterclockwise**: Rotating the camera around its lens axis.  
     8. **Arcing Clockwise/Counterclockwise**: Circling the camera around a subject or the frame center horizontally.
     9. **Craning Up/Down**: Circling the camera around a subject or the frame center vertically.  
6. Mention the speed of movement if noticeably slow or fast. If different movements occur at different speeds, clearly distinguish them.  
   - **Example:**  
     - "The camera slowly dollies forward while trucking quickly to the right."  
7. Describe motion in temporal order if multiple movements occur.  
   - **Example:**  
     - "The camera first pans right, then tilts upward to follow the subject."  
8. If the movement appears too fragmented or random, avoid excessive detail.  
   - **Excessive Detail (Too much description):**  
     - "As the player explores, the camera moves left, then quickly tilts up, followed by a rapid pan right. The player hesitates, looking down, then abruptly swings the camera left again before slightly tilting upward and making another quick turn to the right."  
   - **Better Description (Concise & clear):**  
     - "The first-person camera moves randomly as the player looks around, frequently changing direction without a clear pattern."
```

</details>

### 4. model_without_label

**Rendered version:**

Provide a concise yet informative description of the **video’s and camera’s configuration**, covering **video speed, lens distortion, camera angle, camera height, movements (translation, rotation, zooming, steadiness, arcing, craning, tracking, speed, complexity, and purpose), and focus (depth, focus plane, focus changes).**  

If **video speed** is altered, specify the type, such as *time-lapse* (“Clouds move rapidly across the sky”), *slow-motion*, *fast-motion*, or *speed ramp* (changing between fast and slow motion). If the video is *time-reversed* or *stop-motion*, note this as well.  

If **lens distortion** is present, describe the type and degree. For example, *fisheye distortion* creates extreme curvature, while *barrel distortion* causes mild outward bowing of straight lines near the edges.  

Describe the **camera height** in relation to the ground, such as *eye-level, hip-level, ground-level, overhead-level, aerial-level, above water, or underwater*. If height changes due to movement, mention how it transitions. Similarly, specify the **camera angle**, such as *bird’s eye, high angle, level angle, low angle, or worm’s eye*, noting any shifts within the video. If a **Dutch angle** (tilted horizon) is present, indicate whether it remains fixed or varies due to camera rolling.  

If discernible, describe the **camera focus and depth of field**. For example, *deep focus* keeps all elements sharp, while *shallow or ultra-shallow depth of field* blurs the background or foreground. If focus changes dynamically, note whether it’s a *rack focus* (shifting focus between subjects) or *focus tracking* (following a subject’s depth movement), and state the focus plane at each stage (foreground, midground, background, or out-of-focus). If the video lacks realistic depth of field, describe whether it appears artificial (without a physical camera) or overly blurry.

If the **camera is static**, simply state that the shot is static. If it moves, describe the **type, direction, steadiness, and speed** of movement. Specify movements such as *tracking (following a subject), arcing clockwise/counterclockwise (circling around a subject or frame center horizontally), craning up/down (circling around a subject or frame center vertically), zooming (changing focal length), dollying (moving forward/backward), trucking (moving left/right), pedestaling (moving up/down), panning (rotating the camera horizontally), tilting (rotating the camera up/down), or rolling (rotating around the lens axis).* If the camera is shaking or wobbling, indicate the degree (e.g., minimal, moderate, or severe). If different movements occur at different speeds, clearly distinguish them. If the camera performs multiple movements, describe them in temporal order (e.g., *“The camera first pans right, then tilts upward to follow the subject”*). If movement is fragmented or random, summarize it concisely instead of detailing every small change (e.g., *“The first-person camera moves erratically, frequently changing direction without a clear pattern”*). If relevant, describe the reason or purpose of the camera movement.

Try to make the description as concise as possible. For example, if the video is at regular playback speed, has no lens distortion, and no Dutch angle, there is no need to mention these.

When shot transitions occur, describe the camera framing and movement in each segment separately, note the type of transition (e.g., hard cut, soft transition), and explain how the framing and movement change between segments.

<details>
<summary>📋 Raw markdown source for copy/paste</summary>

```text
Provide a concise yet informative description of the **video’s and camera’s configuration**, covering **video speed, lens distortion, camera angle, camera height, movements (translation, rotation, zooming, steadiness, arcing, craning, tracking, speed, complexity, and purpose), and focus (depth, focus plane, focus changes).**  

If **video speed** is altered, specify the type, such as *time-lapse* (“Clouds move rapidly across the sky”), *slow-motion*, *fast-motion*, or *speed ramp* (changing between fast and slow motion). If the video is *time-reversed* or *stop-motion*, note this as well.  

If **lens distortion** is present, describe the type and degree. For example, *fisheye distortion* creates extreme curvature, while *barrel distortion* causes mild outward bowing of straight lines near the edges.  

Describe the **camera height** in relation to the ground, such as *eye-level, hip-level, ground-level, overhead-level, aerial-level, above water, or underwater*. If height changes due to movement, mention how it transitions. Similarly, specify the **camera angle**, such as *bird’s eye, high angle, level angle, low angle, or worm’s eye*, noting any shifts within the video. If a **Dutch angle** (tilted horizon) is present, indicate whether it remains fixed or varies due to camera rolling.  

If discernible, describe the **camera focus and depth of field**. For example, *deep focus* keeps all elements sharp, while *shallow or ultra-shallow depth of field* blurs the background or foreground. If focus changes dynamically, note whether it’s a *rack focus* (shifting focus between subjects) or *focus tracking* (following a subject’s depth movement), and state the focus plane at each stage (foreground, midground, background, or out-of-focus). If the video lacks realistic depth of field, describe whether it appears artificial (without a physical camera) or overly blurry.

If the **camera is static**, simply state that the shot is static. If it moves, describe the **type, direction, steadiness, and speed** of movement. Specify movements such as *tracking (following a subject), arcing clockwise/counterclockwise (circling around a subject or frame center horizontally), craning up/down (circling around a subject or frame center vertically), zooming (changing focal length), dollying (moving forward/backward), trucking (moving left/right), pedestaling (moving up/down), panning (rotating the camera horizontally), tilting (rotating the camera up/down), or rolling (rotating around the lens axis).* If the camera is shaking or wobbling, indicate the degree (e.g., minimal, moderate, or severe). If different movements occur at different speeds, clearly distinguish them. If the camera performs multiple movements, describe them in temporal order (e.g., *“The camera first pans right, then tilts upward to follow the subject”*). If movement is fragmented or random, summarize it concisely instead of detailing every small change (e.g., *“The first-person camera moves erratically, frequently changing direction without a clear pattern”*). If relevant, describe the reason or purpose of the camera movement.

Try to make the description as concise as possible. For example, if the video is at regular playback speed, has no lens distortion, and no Dutch angle, there is no need to mention these.

When shot transitions occur, describe the camera framing and movement in each segment separately, note the type of transition (e.g., hard cut, soft transition), and explain how the framing and movement change between segments.
```

</details>

---

## Summary

This comparison was generated automatically to help understand the different 
versions of policy text used throughout the system.

**Generated on**: 2025-08-10 06:31:24
