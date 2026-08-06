# Direct Caption Edit Detection Report

## Overview

This report identifies cases where **Jiaxi Li** manually edited the GPT-generated caption 
instead of using the feedback refinement workflow (re-polish feedback + re-generate caption).

**Why this matters**: Direct edits bypass the intended workflow where users should:
1. Provide feedback on the pre-caption
2. Let GPT polish the feedback and generate a refined caption
3. If unhappy, re-polish feedback and regenerate (not directly edit)

Direct edits may indicate:
- User found it faster to edit directly than iterate through feedback
- Potential quality issues if edits are substantial
- Workflow friction that should be addressed

## Dataset Information

- **Source Export File**: `caption_export/export_20260112_1158/all_videos_with_captions_20260112_1158.json`
- **Target User**: Jiaxi Li
- **Analysis Timestamp**: 20260113_1222

## Detection Criteria

A caption is flagged as "Direct Edit" if:
1. `initial_caption_rating_score` != 5 (went through feedback workflow)
2. `gpt_caption` exists (GPT generated a caption)
3. `final_caption` != `gpt_caption` (user modified the GPT output)

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Direct Edits** (final != gpt) | 70 | 5.9% |
| No Edits (final == gpt) | 494 | 41.8% |
| Perfect Pre-caption (rating=5) | 617 | 52.2% |
| **Total by Jiaxi Li** | 1181 | 100.0% |

## ⚠️ Direct Edit Cases (70 total)

These are cases where the user manually edited the GPT-generated caption.
Sorted by timestamp (latest first).

### Case 1/70

| Field | Value |
|-------|-------|
| Video ID | `Q94h0nVnPR0.0.0.mp4` |
| Batch File | `2100_to_2110.json` |
| Batch Index | 6 |
| Caption Type | scene |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-11T12:55:09.948411 |

**Pre-Caption:**

> The scene is set outdoors in a vast, pastoral landscape during the day. A slow camera pullback begins on a couple in a green meadow, gradually revealing the expansive surroundings. The setting features rolling green hills, dense clusters of trees, and a wide body of water in the distance under a partly cloudy sky. A large tree with gnarled branches is visible on the left. As the view widens, a second couple dressed in similar period attire appears further back in the meadow, which is situated on a gentle slope. The continuous zoom-out transforms the composition from an intimate shot to a wide scenic vista.

**Initial Feedback:**

> Many trees with gnarled branches is visible on the left.

**Final Feedback:**

> Many trees with gnarled branches is visible on the left.

**GPT Caption (before edit):**

> The scene is set outdoors in a vast, pastoral landscape during the day. A slow camera pullback begins on a couple in a green meadow, gradually revealing the expansive surroundings. The setting features rolling green hills, dense clusters of trees, and a wide body of water in the distance under a partly cloudy sky. As the view widens, a large tree with gnarled branches becomes prominent on the left. A second couple dressed in similar period attire appears further back in the meadow, which is situated on a gentle slope. The continuous zoom-out transforms the composition from an intimate shot to a wide scenic vista.

**Final Caption (after manual edit):**

> The scene is set outdoors in a vast, pastoral landscape during the day. A slow camera pullback begins on a couple in a green meadow, gradually revealing the expansive surroundings. The setting features rolling green hills, dense clusters of trees, and a wide body of water in the distance under a partly cloudy sky. As the view widens, many trees with gnarled branches becomes prominent on the left. A second couple dressed in similar period attire appears further back in the meadow, which is situated on a gentle slope. The continuous zoom-out transforms the composition from an intimate shot to a wide scenic vista.

**Diff:**

```diff
- As the view widens, a large tree with gnarled branches becomes prominent on the left.
+ As the view widens, many trees with gnarled branches becomes prominent on the left.
```

**Change Summary:** Added: many, trees; Removed: tree, large

---

### Case 2/70

| Field | Value |
|-------|-------|
| Video ID | `NJm86fzxG8s.6.3.mp4` |
| Batch File | `2100_to_2110.json` |
| Batch Index | 4 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-11T12:39:39.579991 |

**Pre-Caption:**

> In a static full shot, a reddish-brown skullcap on a stand is positioned in the center of the frame and in the middle ground. A wooden structure occupies the left foreground. In the out-of-focus background, other bone-like artifacts are visible behind the central skullcap, and modern shelving with soft lights is located on the right side of the frame. The camera is positioned at the subject's level.

**Initial Feedback:**

> This is not a static shot, the camera is moving left to right.

**Final Feedback:**

> The video caption inaccurately describes the shot as static.A wooden structure occupies the left foreground and middle ground. In reality, the camera is moving from left to right.The skullcap is in the foreground.

**GPT Caption (before edit):**

> In a full shot, a reddish-brown skullcap on a stand is positioned in the center of the frame and in the middle ground. A wooden structure occupies the left foreground. The camera moves from left to right, revealing other bone-like artifacts in the out-of-focus background behind the central skullcap, and modern shelving with soft lights on the right side of the frame. The camera is positioned at the subject's level.

**Final Caption (after manual edit):**

> In a full shot, a reddish-brown skullcap on a stand is positioned in the center of the frame and in the foreground. A wooden structure occupies the left foreground and middle ground. The camera moves from left to right, revealing other bone-like artifacts in the out-of-focus background behind the central skullcap, and modern shelving with soft lights on the right side of the frame. The camera is positioned at the subject's level.

**Diff:**

```diff
- In a full shot, a reddish-brown skullcap on a stand is positioned in the center of the frame and in the middle ground.
- A wooden structure occupies the left foreground.
+ In a full shot, a reddish-brown skullcap on a stand is positioned in the center of the frame and in the foreground.
+ A wooden structure occupies the left foreground and middle ground.
```

**Change Summary:** Added: foreground

---

### Case 3/70

| Field | Value |
|-------|-------|
| Video ID | `8T1ZTYtfhI0_0643_0649.mp4` |
| Batch File | `2100_to_2110.json` |
| Batch Index | 3 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-11T12:31:34.803010 |

**Pre-Caption:**

> The video begins with a full shot from a low-angle perspective, capturing a person holding a large lobster in the center of the frame, submerged in the middle ground of the underwater scene. The camera then moves vertically upwards, breaking the surface of the water. The shot transitions to a medium shot at the subject's level, where the person is now in the center-middle ground, partially above the water. They hold the lobster up, positioning it in the foreground so its underside fills the bottom of the frame. The surrounding sea occupies the middle ground, and a distant coastline stretches across the horizon in the background.

**Initial Feedback:**

> This is a level-angle shot.

**Final Feedback:**

> The video features a leve-angle shot, not a low-angle shot.

**GPT Caption (before edit):**

> The video begins with a full shot from a low-angle perspective, capturing a person holding a large lobster in the center of the frame, submerged in the middle ground of the underwater scene. The camera then moves vertically upwards, breaking the surface of the water. The shot transitions to a medium shot from a low-angle perspective, where the person is now in the center-middle ground, partially above the water. They hold the lobster up, positioning it in the foreground so its underside fills the bottom of the frame. The surrounding sea occupies the middle ground, and a distant coastline stretches across the horizon in the background.

**Final Caption (after manual edit):**

> The video begins with a full shot from a level-angle perspective, capturing a person holding a large lobster in the center of the frame, submerged in the middle ground of the underwater scene. The camera then moves vertically upwards, breaking the surface of the water. The shot transitions to a medium shot from a low-angle perspective, where the person is now in the center-middle ground, partially above the water. They hold the lobster up, positioning it in the foreground so its underside fills the bottom of the frame. The surrounding sea occupies the middle ground, and a distant coastline stretches across the horizon in the background.

**Diff:**

```diff
- The video begins with a full shot from a low-angle perspective, capturing a person holding a large lobster in the center of the frame, submerged in the middle ground of the underwater scene.
+ The video begins with a full shot from a level-angle perspective, capturing a person holding a large lobster in the center of the frame, submerged in the middle ground of the underwater scene.
```

**Change Summary:** Added: level-angle

---

### Case 4/70

| Field | Value |
|-------|-------|
| Video ID | `uZudawXgnZ8_3018_3028.mp4` |
| Batch File | `2100_to_2110.json` |
| Batch Index | 1 |
| Caption Type | camera |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-11T12:04:24.580166 |

**Pre-Caption:**

> This is a completely static shot from a high-angle, bird's-eye perspective. As it is a 2D video, traditional camera height and angle are difficult to determine.

**Initial Feedback:**

> It is a 2D video, making it hard to determine the camera angle.

**Final Feedback:**

> The video is presented in 2D, which makes it challenging to accurately assess the camera's height and angle.

**GPT Caption (before edit):**

> The video is shown from a high-angle, bird's-eye perspective, and being in 2D, it makes it challenging to accurately determine the camera's height and angle.

**Final Caption (after manual edit):**

> Being in 2D, it is challenging to accurately determine the camera's height and angle.

**Diff:**

```diff
- The video is shown from a high-angle
- bird's-eye perspective
- and being in 2D
- it makes it challenging to accurately determine the camera's height and angle.
+ Being in 2D
+ it is challenging to accurately determine the camera's height and angle.
```

**Change Summary:** Removed: makes, a, from, bird's-eye, perspective,, high-angle,, video, shown

---

### Case 5/70

| Field | Value |
|-------|-------|
| Video ID | `ocLJWCnMhTo.1.8.mp4` |
| Batch File | `2100_to_2110.json` |
| Batch Index | 0 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 2 |
| Timestamp | 2026-01-11T11:57:00.364628 |

**Pre-Caption:**

> The video begins with a medium shot from a high, bird's-eye angle, looking down at a group of people positioned in the center of the frame on a black and white checkered floor that occupies the background. A person with blonde hair is in the bottom left quadrant, while another person in blue is in the center, both in the middle ground, as confetti falls from above them, filling the foreground. The entire scene then rotates 180 degrees, inverting the perspective. The shot transitions to a low-angle view looking up at the subjects, who are now upside down at the top of the frame against the checkered surface, which now functions as the ceiling. The confetti continues to fall from the top of the frame toward the camera's position at the bottom, and green tiled walls become visible in the background at the sides and bottom of the frame.

**Initial Feedback:**

> This is not a high angle perspective.
The shot transitions to an upside-down level angle, not a low angle view.The group is not positioned at the center of the frame. One of the two main figures is located in the center, while the other is in the bottom-left corner, with the remaining people scattered around the frame. The confetti is not falling, and the entire scene remains static throughout the video.

**Final Feedback:**

> The initial description inaccurately identifies the perspective as a high angle; it is not. Additionally, the transition is to an upside-down level angle, not a low-angle view. The group is not centrally positioned in the frame; one of the main figures is indeed in the center, but the other is in the bottom-left corner, with other individuals dispersed around the frame. Furthermore, the confetti is not actively falling, and the scene remains static throughout the video.

**GPT Caption (before edit):**

> The video starts with a medium shot from a level angle, looking at a group of people dispersed around the frame on a black and white checkered floor. A person with blonde hair is in the bottom left corner, while another person in blue is centrally positioned. Confetti is suspended in the air, filling the foreground, as the entire scene rotates 180 degrees, inverting the perspective. The shot transitions to an upside-down level view, with the subjects now at the top of the frame against the checkered surface, which acts as the ceiling. The confetti remains static, and green tiled walls are visible in the background at the sides and bottom of the frame.

**Final Caption (after manual edit):**

> The video starts with a medium shot from a level angle, looking at a group of people dispersed around the frame on a black and white checkered floor. A person with blonde hair is in the bottom left corner, while another person in blue is centrally positioned. Confetti is suspended in the air, filling the foreground, as the entire scene rotates 180 degrees, inverting the perspective. The shot transitions to an upside-down level view, with the subjects now at the top and middle of the frame against the checkered surface, which acts as the ceiling. The confetti remains static, and green tiled walls are visible in the background at the sides and bottom of the frame.

**Diff:**

```diff
- The shot transitions to an upside-down level view, with the subjects now at the top of the frame against the checkered surface, which acts as the ceiling.
+ The shot transitions to an upside-down level view, with the subjects now at the top and middle of the frame against the checkered surface, which acts as the ceiling.
```

**Change Summary:** Added: middle

---

### Case 6/70

| Field | Value |
|-------|-------|
| Video ID | `SsbNOKn2cOs.3.2.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 9 |
| Caption Type | scene |
| Status | completed_not_reviewed |
| Rating Score | 3 |
| Timestamp | 2026-01-11T08:16:22.488699 |

**Pre-Caption:**

> From a high-angle, top-down perspective, the scene looks directly down into a vast, green valley during the daytime. The landscape below is a mix of green and brown vegetation covering rolling hills, with some exposed rocky ground. A narrow, winding path or dry riverbed meanders across the valley floor. A thick black rope descends through the center of the view, with a person in dark clothing suspended from it, positioned high above the ground. The overall color palette is muted under what appears to be an overcast sky.

**Initial Feedback:**

> This is not a high persppective, but a bird's-eye perspective.
A dummy is holding the man.

**Final Feedback:**

> The perspective shown is more accurately described as a bird's-eye view rather than a high-angle perspective. Additionally, it appears that a dummy is supporting the person suspended from the rope.

**GPT Caption (before edit):**

> From a bird's-eye view, the scene looks directly down into a vast, green valley during the daytime. The landscape below is a mix of green and brown vegetation covering rolling hills, with some exposed rocky ground. A narrow, winding path or dry riverbed meanders across the valley floor. A thick black rope descends through the center of the view, with a person in dark clothing, supported by a dummy, suspended from it, positioned high above the ground. The overall color palette is muted under what appears to be an overcast sky.

**Final Caption (after manual edit):**

> From a bird's-eye view, the scene looks directly down into a vast, green valley during the daytime. The landscape below is a mix of green and brown vegetation covering rolling hills, with some exposed rocky ground. A narrow, winding path or dry riverbed meanders across the valley floor. A thick black rope descends through the center of the view, with a person in dark clothing, holding by a dummy,  positioned high above the ground. The overall color palette is muted under what appears to be an overcast sky.

**Diff:**

```diff
- A thick black rope descends through the center of the view, with a person in dark clothing, supported by a dummy, suspended from it, positioned high above the ground.
+ A thick black rope descends through the center of the view, with a person in dark clothing, holding by a dummy,  positioned high above the ground.
```

**Change Summary:** Added: holding; Removed: it,, supported, suspended

---

### Case 7/70

| Field | Value |
|-------|-------|
| Video ID | `SsbNOKn2cOs.3.2.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 9 |
| Caption Type | motion |
| Status | completed_not_reviewed |
| Rating Score | 3 |
| Timestamp | 2026-01-11T08:14:09.803502 |

**Pre-Caption:**

> From a high, top-down perspective, a person hangs from a rope, remaining mostly stationary in a curled-forward position while suspended over a green, hilly landscape. They exhibit a very slight, subtle swaying motion as they hold onto the rope.

**Initial Feedback:**

> This is not a high perspective, but a bird's-eye perspective.There is a dummy holding the man.

**Final Feedback:**

> The perspective shown in the video is more accurately described as a bird's-eye view rather than a high perspective. Additionally, a dummy is holding him.

**GPT Caption (before edit):**

> From a bird's-eye view, a person hangs from a rope, remaining mostly stationary in a curled-forward position while suspended over a green, hilly landscape. They exhibit a very slight, subtle swaying motion, seemingly supported by a dummy as they hold onto the rope.

**Final Caption (after manual edit):**

> From a bird's-eye view, a person hangs from a rope, remaining mostly stationary in a curled-forward position while suspended over a green, hilly landscape. Additionally, a dummy is holding the man.

**Diff:**

```diff
- They exhibit a very slight, subtle swaying motion, seemingly supported by a dummy as they hold onto the rope.
+ Additionally, a dummy is holding the man.
```

**Change Summary:** Added: man., is, holding, additionally,; Removed: seemingly, very, motion,, they, hold, by, rope., swaying, supported, slight,

---

### Case 8/70

| Field | Value |
|-------|-------|
| Video ID | `32883a58-f203-40e6-8f7e-e162d631cd9d.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 7 |
| Caption Type | motion |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-11T07:56:43.449253 |

**Pre-Caption:**

> The woman remains stationary, holding a pose where she leans backward on a circular rug with her arms outstretched.

**Initial Feedback:**

> The woman is not stationary; she starts standing upright on the rug, then lifts one leg and leans backward.

**Final Feedback:**

> The woman is not stationary as described. She initially stands upright on the circular rug, then proceeds to lift one leg and lean backward.

**GPT Caption (before edit):**

> The woman stands upright on a circular rug, lifts one leg, and leans backward with her arms outstretched.

**Final Caption (after manual edit):**

> The woman stands upright on a circular rug, the she lifts one leg, and leans backward with her arms outstretched.

**Diff:**

```diff
- lifts one leg
+ the she lifts one leg
```

**Change Summary:** Added: she

---

### Case 9/70

| Field | Value |
|-------|-------|
| Video ID | `i82xURPkLWo.0.8.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 5 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 3 |
| Timestamp | 2026-01-11T07:39:58.129649 |

**Pre-Caption:**

> In an extreme close-up shot, the right side of a man's face is positioned in the foreground on the right side of the frame, with his cheek pressed against a rifle stock that occupies the bottom and center foreground. A portion of the rifle's scope is visible in the top-left foreground, with his hand on the stock in the center-left foreground. The background is filled with out-of-focus green foliage. The camera then pans down along the rifle, settling on the man's hand in the center foreground, with his index finger on the trigger. In this final framing, the rifle stock occupies the top and left portions of the frame in the foreground, while the blurred green background is visible on the right and bottom. The camera remains at the subject's level throughout the shot.

**Initial Feedback:**

> The left side of the man's face is positioned in the foreground on the right side of the frame, not the left. In the final framing, the rifle stock occupies the entire upper half of the foreground, while the green background appears in the bottom left and left-center of the frame.

**Final Feedback:**

> The left side of the man's face is positioned in the foreground on the right side of the frame, not the left. In the final framing, the rifle stock occupies the entire upper half of the foreground, while the green background appears in the bottom left and left-center of the frame.

**GPT Caption (before edit):**

> In an extreme close-up shot, the right side of a man's face is positioned in the foreground on the right side of the frame, with his cheek pressed against a rifle stock that occupies the bottom and center foreground. A portion of the rifle's scope is visible in the top-left foreground, with his hand on the stock in the center-left foreground. The background is filled with out-of-focus green foliage. The camera then pans down along the rifle, settling on the man's hand in the center foreground, with his index finger on the trigger. In this final framing, the rifle stock occupies the entire upper half of the foreground, while the blurred green background is visible in the bottom left and left-center of the frame. The camera remains at the subject's level throughout the shot.

**Final Caption (after manual edit):**

> In an extreme close-up shot, the left side of a man's face is positioned in the foreground on the right side of the frame, with his cheek pressed against a rifle stock that occupies the bottom and center foreground. A portion of the rifle's scope is visible in the top-left foreground, with his hand on the stock in the center-left foreground. The background is filled with out-of-focus green foliage. The camera then pans down along the rifle, settling on the man's hand in the center foreground, with his index finger on the trigger. In this final framing, the rifle stock occupies the entire upper half of the foreground, while the blurred green background is visible in the bottom left and left-center of the frame. The camera remains at the subject's level throughout the shot.

**Diff:**

```diff
- In an extreme close-up shot, the right side of a man's face is positioned in the foreground on the right side of the frame, with his cheek pressed against a rifle stock that occupies the bottom and center foreground.
+ In an extreme close-up shot, the left side of a man's face is positioned in the foreground on the right side of the frame, with his cheek pressed against a rifle stock that occupies the bottom and center foreground.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

### Case 10/70

| Field | Value |
|-------|-------|
| Video ID | `0sMUF4ULb14_20250_20490.0.0.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 4 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 2 |
| Timestamp | 2026-01-11T07:22:53.273108 |

**Pre-Caption:**

> The video is presented in a full shot, with the camera positioned at the subjects' level. A model stands in the middle ground, slightly left of the frame's center, against a white cyclorama wall. In the foreground on the right, a photographer is initially bent over. The background on the right side of the frame contains dark walls and studio lighting equipment. As the clip progresses, the photographer stands up and takes a small step to his left, moving slightly closer to the center of the frame while remaining in the foreground. He then raises his hand to gesture at the model, who remains stationary in the middle ground. The "AdoramaTV" logo is a static overlay in the bottom right corner of the foreground.

**Initial Feedback:**

> The model initially stands at the center of the frame and moves to the left side of the frame as the camera pans. The photographer starts in an upright position, then bends down to pick up the camera, and straightens up again. The "AdoramaTV" overlay appears in the bottom left corner of the frame.

**Final Feedback:**

> The model initially stands at the center of the frame and moves to the left side of the frame as the camera pans. The photographer starts in an upright position, then bends down to pick up the camera, and straightens up again. The "AdoramaTV" overlay appears in the bottom left corner of the frame.

**GPT Caption (before edit):**

> The video features a full shot with the camera at the subjects' level. A model is positioned slightly left of the center against a white cyclorama wall and remains stationary throughout the clip. In the foreground on the right, a photographer starts bent over, then stands upright and takes a small step to his left, moving closer to the center of the frame. The background on the right includes dark walls and studio lighting equipment. The "AdoramaTV" logo is consistently displayed in the bottom right corner of the frame.

**Final Caption (after manual edit):**

> The video features a full shot with the camera at the subjects' level. he model initially stands at the center of the frame and moves to the left side of the frame as the camera pans, against a white cyclorama wall and remains stationary throughout the clip. In the foreground, a photographer starts in an upright position, then bends down to pick up the camera, and straightens up again.a photographer starts bent over, then stands upright and takes a small step to his left. The background on the right includes dark walls and studio lighting equipment. The "AdoramaTV" logo is consistently displayed in the bottom right corner of the frame.

**Diff:**

```diff
- A model is positioned slightly left of the center against a white cyclorama wall and remains stationary throughout the clip.
- In the foreground on the right, a photographer starts bent over, then stands upright and takes a small step to his left, moving closer to the center of the frame.
+ he model initially stands at the center of the frame and moves to the left side of the frame as the camera pans, against a white cyclorama wall and remains stationary throughout the clip.
+ In the foreground, a photographer starts in an upright position, then bends down to pick up the camera, and straightens up again.a photographer starts bent over, then stands upright and takes a small step to his left.
```

**Change Summary:** Added: position,, bends, camera,, frame, moves, left., foreground,, he, up, pans,; Removed: foreground, moving, closer, left,, right,, positioned, slightly

---

### Case 11/70

| Field | Value |
|-------|-------|
| Video ID | `dd28a5c8-e891-4647-8f2f-03bb4a2dab6a.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 3 |
| Caption Type | motion |
| Status | completed_not_reviewed |
| Rating Score | 4 |
| Timestamp | 2026-01-10T10:26:23.216726 |

**Pre-Caption:**

> The stationary vintage car is viewed from a shifting perspective as the frame rotates. The view begins at a tilted angle, moves to a level position, and then continues to rotate into an opposing tilted angle.

**Initial Feedback:**

> The car is not stationary; it is moving backward.

**Final Feedback:**

> The car  is moving backward, contradicting the description of it being stationary.

**GPT Caption (before edit):**

> The vintage car is seen from a rotating perspective, creating the illusion of movement. The view starts at a tilted angle, shifts to a level position, and then rotates to an opposite tilted angle.

**Final Caption (after manual edit):**

> The vintage car is seen from a rotating perspective, and moving backward. The view starts at a tilted angle, shifts to a level position, and then rotates to an opposite tilted angle.

**Diff:**

```diff
- The vintage car is seen from a rotating perspective, creating the illusion of movement.
+ The vintage car is seen from a rotating perspective, and moving backward.
```

**Change Summary:** Added: moving, backward.; Removed: of, illusion, movement., creating

---

### Case 12/70

| Field | Value |
|-------|-------|
| Video ID | `XPPcA1hAfp4_4112_4122.mp4` |
| Batch File | `1990_to_2000.json` |
| Batch Index | 0 |
| Caption Type | subject |
| Status | completed_not_reviewed |
| Rating Score | 3 |
| Timestamp | 2025-12-25T21:43:45.731846 |

**Pre-Caption:**

> A pixelated character with red hair, a blue top, and brown pants stands on a wooden platform surrounded by an organized collection of objects. Along the top edge of the platform are two rows of identical green chests. In the center, there are several other containers, including a red chest, a blue chest, a wooden chest, a stone-like chest, and a metallic chest. Next to the character are various crafting stations, such as a grey anvil, a furnace, and several workbenches. The platform is illuminated by numerous lit torches placed on posts around its perimeter.

**Initial Feedback:**

> The character wears a red top, blue pants, and a brown hat. In the center of the platform, there is no blue chest or red chest; instead, there is a blue bed.

**Final Feedback:**

> The character is actually wearing a red top, blue pants, and a brown hat. Additionally, in the center of the platform, there is no blue chest or red chest; instead, there is a blue bed.

**GPT Caption (before edit):**

> A pixelated character with red hair, a red top, blue pants, and a brown hat stands on a wooden platform surrounded by an organized collection of objects. Along the top edge of the platform are two rows of identical green chests. In the center, there are several other containers, including a wooden chest, a stone-like chest, and a metallic chest, as well as a blue bed. Next to the character are various crafting stations, such as a grey anvil, a furnace, and several workbenches. The platform is illuminated by numerous lit torches placed on posts around its perimeter.

**Final Caption (after manual edit):**

> A pixelated character with a red top, blue pants, and a brown hat stands on a wooden platform surrounded by an organized collection of objects. Along the top edge of the platform are two rows of identical green chests. In the center,there is a blue bed. There is a grey chest in the lower-left corner of the platform.
Next to the character are various crafting stations, such as a grey anvil, a furnace, and several workbenches. The platform is illuminated by numerous lit torches placed on posts around its perimeter.

**Diff:**

```diff
- A pixelated character with red hair, a red top, blue pants, and a brown hat stands on a wooden platform surrounded by an organized collection of objects.
+ A pixelated character with a red top, blue pants, and a brown hat stands on a wooden platform surrounded by an organized collection of objects.
- In the center, there are several other containers, including a wooden chest, a stone-like chest, and a metallic chest, as well as a blue bed.
+ In the center,there is a blue bed.
+ There is a grey chest in the lower-left corner of the platform.
```

**Change Summary:** Added: center,there, platform., lower-left, corner, chest; Removed: metallic, well, including, stone-like, center,, other, chest,, containers,, hair,

---

### Case 13/70

| Field | Value |
|-------|-------|
| Video ID | `00ZNvOMUe0o_0243_0240.mp4` |
| Batch File | `1970_to_1980.json` |
| Batch Index | 6 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-25T10:35:08.514126 |

**Pre-Caption:**

> From a high-angle perspective, a red off-road vehicle drives forward along a dirt path, moving away from the camera across a vast, arid plain. In the lower-left corner, the front of a second vehicle is partially visible and remains stationary.

**Initial Feedback:**

> The video inaccurately describes the movement of the vehicles. Both vehicles are actually reversing, not moving forward. Additionally, the vehicle in the lower-left corner eventually exits the frame.

**Final Feedback:**

> The video caption inaccurately describes the movement of the vehicles. Both vehicles are reversing, not moving forward. Furthermore, the vehicle in the lower-left corner eventually exits the frame.

**GPT Caption (before edit):**

> From a high-angle perspective, a red off-road vehicle reverses along a dirt path, moving away from the camera across a vast, arid plain. In the lower-left corner, the front of a second vehicle is partially visible and also reversing, eventually exiting the frame.

**Final Caption (after manual edit):**

> From a high-angle perspective, a red off-road vehicle reverses along a dirt path, moving towards the camera across a vast, arid plain. In the lower-left corner, the front of a second vehicle is partially visible and also reversing, eventually exiting the frame.

**Diff:**

```diff
- From a high-angle perspective, a red off-road vehicle reverses along a dirt path, moving away from the camera across a vast, arid plain.
+ From a high-angle perspective, a red off-road vehicle reverses along a dirt path, moving towards the camera across a vast, arid plain.
```

**Change Summary:** Added: towards; Removed: away

---

### Case 14/70

| Field | Value |
|-------|-------|
| Video ID | `1497.1.17.mp4` |
| Batch File | `1970_to_1980.json` |
| Batch Index | 7 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-25T09:21:54.577791 |

**Pre-Caption:**

> A large, turbulent burst of white, foamy water erupts and moves rapidly across the view, almost completely obscuring the scene. Through the spray, indistinct, dark, and reddish shapes are barely visible in the background.

**Initial Feedback:**

> At the beginning of the scene, a man dressed in black is visible, with another man in red standing behind him.The video concludes with both men bent over, with only their upper bodies visible in the frame. Soon after, a large burst of water erupts in front of them, almost completely obscuring the view, then the video ends.

**Final Feedback:**

> At the start of the scene, a man dressed in black is visible, with another man in red standing behind him. As the video progresses, both men are seen bent over, with only their upper bodies in the frame. Shortly thereafter, a large burst of water erupts in front of them, nearly obscuring the entire view, and then the video concludes.

**GPT Caption (before edit):**

> At the start of the scene, a man dressed in black is visible, with another man in red standing behind him. As the video progresses, both men are seen bent over, with only their upper bodies in the frame. Shortly thereafter, a large, turbulent burst of white, foamy water erupts in front of them, nearly obscuring the entire view, and then the video concludes. Through the spray, indistinct, dark, and reddish shapes are barely visible in the background.

**Final Caption (after manual edit):**

> At the start of the scene, a man dressed in black is visible, with another man in red behind him, both men are seen bent over, with only their upper bodies in the frame. Shortly thereafter, a large, turbulent burst of white, foamy water erupts in front of them, nearly obscuring the entire view, and then the video concludes. Through the spray, indistinct, dark, and reddish shapes are barely visible in the background.

**Diff:**

```diff
- At the start of the scene, a man dressed in black is visible, with another man in red standing behind him.
- As the video progresses, both men are seen bent over, with only their upper bodies in the frame.
+ At the start of the scene, a man dressed in black is visible, with another man in red behind him, both men are seen bent over, with only their upper bodies in the frame.
```

**Change Summary:** Added: him,; Removed: standing, progresses,, as, him.

---

### Case 15/70

| Field | Value |
|-------|-------|
| Video ID | `i82xURPkLWo.2.4.mp4` |
| Batch File | `1970_to_1980.json` |
| Batch Index | 0 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-25T05:45:45.780937 |

**Pre-Caption:**

> The video uses a close-up shot, framing the man’s torso and hands as the main subject, with his arms and the objects he holds occupying the center and lower center of the frame in the foreground. The man’s hands, holding a photograph and a lighter, are positioned just above a round metallic bowl filled with ash, which sits on a wooden railing at the bottom center of the frame in the foreground. The photograph, initially held above the bowl, is set on fire with the lighter, and then dropped directly downward into the bowl, remaining in the foreground and center of the frame throughout the action. The camera remains at the same height as the man’s hands and the bowl, maintaining a level perspective. The background, which is softly blurred, occupies the upper part of the frame and remains in the background, showing indistinct outdoor scenery with no major elements drawing focus away from the central action. There are no significant changes in shot size or camera angle, and the spatial dynamics are defined by the downward movement of the photograph from the man’s hand into the bowl.

**Initial Feedback:**

> The camera angle is at a high angle (looking down from above).

**Final Feedback:**

> The camera angle is actually at eye level, maintaining a level perspective with the man's hands and the bowl, rather than a high angle looking down from above.

**GPT Caption (before edit):**

> The video uses a close-up shot, framing the man’s torso and hands as the main subject, with his arms and the objects he holds occupying the center and lower center of the frame in the foreground. The man’s hands, holding a photograph and a lighter, are positioned just above a round metallic bowl filled with ash, which sits on a wooden railing at the bottom center of the frame in the foreground. The photograph, initially held above the bowl, is set on fire with the lighter, and then dropped directly downward into the bowl, remaining in the foreground and center of the frame throughout the action. The camera is positioned at eye level, maintaining a level perspective with the man's hands and the bowl. The background, which is softly blurred, occupies the upper part of the frame and remains in the background, showing indistinct outdoor scenery with no major elements drawing focus away from the central action. There are no significant changes in shot size or camera angle, and the spatial dynamics are defined by the downward movement of the photograph from the man’s hand into the bowl.

**Final Caption (after manual edit):**

> The video uses a close-up shot, framing the man’s torso and hands as the main subject, with his arms and the objects he holds occupying the center and lower center of the frame in the foreground. The man’s hands, holding a photograph and a lighter, are positioned just above a round metallic bowl filled with ash, which sits on a wooden railing at the bottom center of the frame in the foreground. The photograph, initially held above the bowl, is set on fire with the lighter, and then dropped directly downward into the bowl, remaining in the foreground and center of the frame throughout the action. The camera is positioned at eye level, maintaining a high-angle perspective relative to the man's hands and the bowl. The background, which is softly blurred, occupies the upper part of the frame and remains in the background, showing indistinct outdoor scenery with no major elements drawing focus away from the central action. There are no significant changes in shot size or camera angle, and the spatial dynamics are defined by the downward movement of the photograph from the man’s hand into the bowl.

**Diff:**

```diff
- The camera is positioned at eye level, maintaining a level perspective with the man's hands and the bowl.
+ The camera is positioned at eye level, maintaining a high-angle perspective relative to the man's hands and the bowl.
```

**Change Summary:** Added: relative, high-angle, to; Removed: level

---

### Case 16/70

| Field | Value |
|-------|-------|
| Video ID | `6dc8cef6-e02f-4b5b-9487-6850402e806e.mp4` |
| Batch File | `1950_to_1960.json` |
| Batch Index | 7 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-24T11:15:43.354812 |

**Pre-Caption:**

> From a high-angle, top-down perspective, a woman with multiple arms moves rapidly and simultaneously at a kitchen counter. One arm stirs a substance in a green bowl, another mixes ingredients in a different container, and a third wipes the counter surface. As she works, the camera subtly rotates around her. At the bottom of the frame, a separate pair of hands continuously assembles small, round food items.

**Initial Feedback:**

> The woman has a total of six arms: one stirs ingredients in a green bowl, one pulls a small piece from a large lump of white substance and, together with another hand, kneads it. Another arm rolls a gray, rolling-pin-shaped object back and forth. The remaining two arms are reaching for various items.

**Final Feedback:**

> The woman in the video is depicted with six arms. One arm is stirring ingredients in a green bowl, while another pulls a small piece from a large lump of white substance and kneads it with the help of a third arm. A fourth arm is rolling a gray, rolling-pin-shaped object back and forth. The remaining two arms are reaching for various items, showcasing a dynamic and multitasking scene.

**GPT Caption (before edit):**

> From a high-angle, top-down perspective, a woman with six arms moves rapidly and simultaneously at a kitchen counter. One arm stirs ingredients in a green bowl, while another pulls a small piece from a large lump of white substance and kneads it with the help of a third arm. A fourth arm rolls a gray, rolling-pin-shaped object back and forth. The remaining two arms reach for various items, showcasing a dynamic and multitasking scene. As she works, the camera subtly rotates around her. At the bottom of the frame, a separate pair of hands continuously assembles small, round food items.

**Final Caption (after manual edit):**

> From a bird's-eye view angle, top-down perspective, a woman with six arms moves rapidly and simultaneously at a kitchen counter. One arm stirs ingredients in a green bowl, while another pulls a small piece from a large lump of white substance and kneads it with the help of a third arm. A fourth arm rolls a gray, rolling-pin-shaped object back and forth. The remaining two arms reach for various items, showcasing a dynamic and multitasking scene. As she works, the camera subtly rotates around her. At the bottom of the frame, a separate pair of hands continuously assembles small, round food items.

**Diff:**

```diff
- From a high-angle, top-down perspective, a woman with six arms moves rapidly and simultaneously at a kitchen counter.
+ From a bird's-eye view angle, top-down perspective, a woman with six arms moves rapidly and simultaneously at a kitchen counter.
```

**Change Summary:** Added: bird's-eye, view, angle,; Removed: high-angle,

---

### Case 17/70

| Field | Value |
|-------|-------|
| Video ID | `hCr1JvdvBqs.0.6.mp4` |
| Batch File | `1930_to_1940.json` |
| Batch Index | 8 |
| Caption Type | spatial |
| Status | completed_not_reviewed |
| Rating Score | 3 |
| Timestamp | 2025-12-24T03:22:48.490530 |

**Pre-Caption:**

> In a close-up shot, a man is positioned in the center-right of the frame, occupying the middle ground. On the far left, the back of another person's head is visible in the foreground. A window is located in the background to the left of the man. The camera remains static at the subjects' eye level throughout the clip. The man slightly lifts his head from a downward-looking position to face forward.

**Initial Feedback:**

> In the middle ground to the man’s left, there is a window. The camera moves forward while also moving to the right. The man initially looks straight ahead, then lowers his gaze, and afterward returns to looking straight ahead, focusing on a person off-screen.

**Final Feedback:**

> In the middle ground to the man's left, there is a window. The camera moves forward and to the right. Initially, the man looks straight ahead, then lowers his gaze, and finally returns to looking straight ahead, focusing on a person off-screen.

**GPT Caption (before edit):**

> In a close-up shot, a man is positioned in the center-right of the frame, occupying the middle ground. To the man's left, there is a window in the background. The back of another person's head is visible in the foreground on the far left. The camera moves forward and to the right, maintaining eye level with the subjects. Initially, the man looks straight ahead, then lowers his gaze, and finally returns to looking straight ahead, focusing on a person off-screen.

**Final Caption (after manual edit):**

> In a close-up shot, a man is positioned in the center-right of the frame, occupying the middle ground. To the man's left, there is a window in the middle ground. The back of another person's head is visible in the foreground on the far left. The camera moves forward and to the right, maintaining eye level with the subjects. Initially, the man looks straight ahead, then lowers his gaze, and finally returns to looking straight ahead, focusing on a person off-screen.

**Diff:**

```diff
- To the man's left, there is a window in the background.
+ To the man's left, there is a window in the middle ground.
```

**Change Summary:** Removed: background.

---

### Case 18/70

| Field | Value |
|-------|-------|
| Video ID | `uZudawXgnZ8_2605_2615.mp4` |
| Batch File | `1930_to_1940.json` |
| Batch Index | 2 |
| Caption Type | camera |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-24T02:15:20.871580 |

**Pre-Caption:**

> From a bird's-eye perspective in a 2D video game, the camera smoothly tracks the player character. The camera follows the character's movement, initially shifting slightly upward, then moving right and downward, and finally, after a brief upward motion, continuing its downward path.

**Initial Feedback:**

> It is a 2D video, making it hard to determine the camera angle.

**Final Feedback:**

> The 2D perspective of the video makes it challenging to discern the specific camera angle being used.

**GPT Caption (before edit):**

> In a 2D video game, the camera smoothly follows the player character from a top-down perspective. It tracks the character's movement by initially shifting slightly upward, then moving right and downward, and finally, after a brief upward motion, continuing its downward path.

**Final Caption (after manual edit):**

> In a 2D video game, the camera smoothly follows the player character. It tracks the character's movement by initially shifting slightly upward, then moving right and downward, and finally, after a brief upward motion, continuing its downward path.

**Diff:**

```diff
- In a 2D video game, the camera smoothly follows the player character from a top-down perspective.
+ In a 2D video game, the camera smoothly follows the player character.
```

**Change Summary:** Added: character.; Removed: character, perspective., from, top-down

---

### Case 19/70

| Field | Value |
|-------|-------|
| Video ID | `KoJ0Pih0Ssc.0.1.mp4` |
| Batch File | `1900_to_1910.json` |
| Batch Index | 9 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-24T00:55:35.448947 |

**Pre-Caption:**

> This video presents a static or very slowly moving aerial scenery shot of London. The view looks down on the River Thames and Tower Bridge, with the words "EAST - WEST" superimposed over the water. The scene is captured during what appears to be sunrise or sunset, casting a warm, hazy light over the city.

**Initial Feedback:**

> This is not a static shot,  The camera is arcing counterclockwise.
The words "EAST" and "WEST" are superimposed over the water, with a white dashed line also superimposed between the two terms.

**Final Feedback:**

> The video is not a static shot; the camera is actually arcing counterclockwise. Additionally, the words "EAST" and "WEST" are superimposed over the water, accompanied by a white dashed line between them.

**GPT Caption (before edit):**

> This video features an aerial shot of London with the camera arcing counterclockwise. The view looks down on the River Thames and Tower Bridge, with the words "EAST" and "WEST" superimposed over the water, connected by a white dashed line. The scene is captured during what appears to be sunrise or sunset, casting a warm, hazy light over the city.

**Final Caption (after manual edit):**

> This video features an aerial shot of London with the camera arcing counterclockwise. The view looks down on the River Thames and Tower Bridge, with the words "EAST" and "WEST" superimposed over the water, and a white dashed line between them. The scene is captured during what appears to be sunrise or sunset, casting a warm, hazy light over the city.

**Diff:**

```diff
- The view looks down on the River Thames and Tower Bridge, with the words "EAST" and "WEST" superimposed over the water, connected by a white dashed line.
+ The view looks down on the River Thames and Tower Bridge, with the words "EAST" and "WEST" superimposed over the water, and a white dashed line between them.
```

**Change Summary:** Added: them., line, between; Removed: line., connected, by

---

### Case 20/70

| Field | Value |
|-------|-------|
| Video ID | `5ZMi2aq_TR8_4410_4710.0.mp4` |
| Batch File | `1900_to_1910.json` |
| Batch Index | 7 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-12-23T23:48:58.888220 |

**Pre-Caption:**

> A group of people, dressed in rustic, historical-style clothing, are seated in a large wooden cart. In the center, a young man with dark, curly hair and a darker complexion wears a grey tunic, his mouth open and hands raised. To his left, a person with long, light-colored braids, wearing a grey bonnet and tunic, also looks forward with raised hands. Behind them, a woman in a brown head covering is visible. To the right of the central young man, another man in a dark green tunic has a focused expression, his hands also up. On the far left, a man in a tan, wide-brimmed hat is seen from the back with his arm raised. At the very back of the cart on the right, a young man in a straw hat and a reddish-brown tunic sits looking towards the others, his hands also raised. All the individuals in the cart have their hands up and open mouths, as if in reaction to an event.

**Initial Feedback:**

> The man is not with his mouth wide open, but grimacing. His hands are not held high, but slightly raised. The person to his right is not standing, but seated. The one in the brown head covering is between the two mentioned earlier, not behind them. The man in the dark green tunic is to the left of the central man, not his right, and he raises his hands to maintain balance.

**Final Feedback:**

> The man in the center is not with his mouth wide open, but rather grimacing. His hands are slightly raised, not held high. The person to his right is seated, not standing. The individual in the brown head covering is positioned between the two previously mentioned, not behind them. Additionally, the man in the dark green tunic is to the left of the central man, not his right, and he raises his hands to maintain balance.

**GPT Caption (before edit):**

> A group of people, dressed in rustic, historical-style clothing, are seated in a large wooden cart. In the center, a young man with dark, curly hair and a darker complexion wears a grey tunic, grimacing with his hands slightly raised. To his left, a person with long, light-colored braids, wearing a grey bonnet and tunic, also looks forward with raised hands. Positioned between them is a woman in a brown head covering. To the left of the central young man, another man in a dark green tunic has a focused expression, raising his hands to maintain balance. On the far left, a man in a tan, wide-brimmed hat is seen from the back with his arm raised. At the very back of the cart on the right, a young man in a straw hat and a reddish-brown tunic sits looking towards the others, his hands also raised. All the individuals in the cart have their hands up and open mouths, as if in reaction to an event.

**Final Caption (after manual edit):**

> A group of people, dressed in rustic, historical-style clothing, are seated in a large wooden cart. In the center, a young man with dark, curly hair and a darker complexion wears a grey tunic, grimacing with his hands slightly raised. To his right, a person with long, light-colored braids, wearing a grey bonnet and tunic, also looks forward with raised hands. Positioned between them is a woman in a brown head covering. To the right of the central young man, another man in a dark green tunic has a focused expression, raising his hands to maintain balance. On the far left, a man in a tan, wide-brimmed hat is seen from the back with his arm raised. At the very back of the cart on the right, a young man in a straw hat and a reddish-brown tunic sits looking towards the others, his hands also raised. All the individuals in the cart have their hands up and open mouths, as if in reaction to an event.

**Diff:**

```diff
- To his left, a person with long, light-colored braids, wearing a grey bonnet and tunic, also looks forward with raised hands.
+ To his right, a person with long, light-colored braids, wearing a grey bonnet and tunic, also looks forward with raised hands.
- To the left of the central young man, another man in a dark green tunic has a focused expression, raising his hands to maintain balance.
+ To the right of the central young man, another man in a dark green tunic has a focused expression, raising his hands to maintain balance.
```

**Change Summary:** Added: right; Removed: left

---

### Case 21/70

| Field | Value |
|-------|-------|
| Video ID | `VaSlqE0Nx2Q.5.1.mp4` |
| Batch File | `1900_to_1910.json` |
| Batch Index | 4 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-23T09:02:49.536168 |

**Pre-Caption:**

> In this black-and-white video, two figures are seen running across a sandy landscape. The person on the left wears a dark, flowing cloak or large piece of fabric that billows out behind them. The second person, running slightly ahead and to the right, is of a slimmer build and is dressed in dark shorts, a dark top, and a dark hat. Both individuals are running away from the viewer, casting long shadows on the sand in front of them.

**Initial Feedback:**

> The person on the right lags slightly behind, with their shadow falling to their left.

**Final Feedback:**

> The person on the right appears to be slightly behind the other, with their shadow extending to the left.

**GPT Caption (before edit):**

> In this black-and-white video, two figures are seen running across a sandy landscape. The person on the left wears a dark, flowing cloak or large piece of fabric that billows out behind them. The second person, running slightly behind and to the right, is of a slimmer build and is dressed in dark shorts, a dark top, and a dark hat. Both individuals are running away from the viewer, casting long shadows on the sand, with the second person's shadow extending to the left.

**Final Caption (after manual edit):**

> In this black-and-white video, two figures are seen running across a sandy landscape. The person on the left wears a dark, flowing cloak or large piece of fabric that billows out behind them. The second person, running slightly behind and to the right, is of a slimmer build and is dressed in dark shorts, a dark top, and a dark hat. Both individuals are running away from the viewer, casting long shadows on the sand, with the shadows extending to the left.

**Diff:**

```diff
- Both individuals are running away from the viewer, casting long shadows on the sand, with the second person's shadow extending to the left.
+ Both individuals are running away from the viewer, casting long shadows on the sand, with the shadows extending to the left.
```

**Change Summary:** Removed: person's, shadow

---

### Case 22/70

| Field | Value |
|-------|-------|
| Video ID | `aVA7aXOH1pk.0.1.mp4` |
| Batch File | `1870_to_1880.json` |
| Batch Index | 8 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-22T23:32:23.691207 |

**Pre-Caption:**

> In a static wide shot, a man in a suit stands on a stage positioned in the center of the frame and in the middle ground. A dense crowd, seen from behind, occupies the foreground and the bottom of the frame, holding up smartphones that create a layer in front of the stage. The stage itself extends horizontally across the middle ground. In the background, another large crowd fills the top portion of the frame, positioned behind the man on stage. The camera is positioned at the subject's level, maintaining a fixed perspective on the scene.

**Initial Feedback:**

> This is not a static shot, The camera is zooming in.

**Final Feedback:**

> The description inaccurately refers to the shot as static. The camera is actually zooming in, which contradicts the claim of a fixed perspective.

**GPT Caption (before edit):**

> In a wide shot, a man in a suit stands on a stage positioned in the center of the frame and in the middle ground. A dense crowd, seen from behind, occupies the foreground and the bottom of the frame, holding up smartphones that create a layer in front of the stage. The stage itself extends horizontally across the middle ground. In the background, another large crowd fills the top portion of the frame, positioned behind the man on stage. The camera gradually zooms in, altering the perspective on the scene.

**Final Caption (after manual edit):**

> In a wide shot, a man in a suit stands on a stage positioned in the center of the frame and in the middle ground. A dense crowd, seen from behind, occupies the foreground and the bottom of the frame, holding up smartphones that create a layer in front of the stage. The stage itself extends horizontally across the middle ground. In the background, another large crowd fills the top portion of the frame, positioned behind the man on stage. The camera is gradually zooming in.

**Diff:**

```diff
- The camera gradually zooms in, altering the perspective on the scene.
+ The camera is gradually zooming in.
```

**Change Summary:** Added: is, in., zooming; Removed: scene., altering, zooms, in,, perspective

---

### Case 23/70

| Field | Value |
|-------|-------|
| Video ID | `8cd277fe-7907-4159-bc44-7988cfb7ecf7.mp4` |
| Batch File | `1870_to_1880.json` |
| Batch Index | 1 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-12-22T11:16:20.108749 |

**Pre-Caption:**

> In a full shot captured from a high-angle, overhead perspective, a woman is positioned in the center of the frame and the middle ground. She is encircled by several other figures in dark clothing who are arranged around her, also in the middle ground, on a floor made of glowing square panels. The entire scene, including all subjects, rotates clockwise as a single unit due to the camera's movement.

**Initial Feedback:**

> This is a bird's-eye angle, not high angle.
The figures are in the background, not middle ground.
The camera is rolling clockwise.

**Final Feedback:**

> The video features a bird's-eye view, rather than a high-angle perspective. The figures surrounding the woman are positioned in the background, not the middle ground. Additionally, the camera is rotating clockwise.

**GPT Caption (before edit):**

> In a full shot captured from a bird's-eye view, a woman is positioned in the center of the frame. She is encircled by several other figures in dark clothing who are arranged around her in the background on a floor made of glowing square panels. The entire scene, including all subjects, rotates clockwise due to the camera's movement.

**Final Caption (after manual edit):**

> In a full shot captured from a bird's-eye view, a woman is positioned in the center of the frame. She is encircled by several other figures in dark clothing who are arranged around her in the background on a floor made of glowing square panels. The entire scene, including all subjects, rotates counter-clockwise due to the camera's movement.

**Diff:**

```diff
- The entire scene, including all subjects, rotates clockwise due to the camera's movement.
+ The entire scene, including all subjects, rotates counter-clockwise due to the camera's movement.
```

**Change Summary:** Added: counter-clockwise; Removed: clockwise

---

### Case 24/70

| Field | Value |
|-------|-------|
| Video ID | `8cd277fe-7907-4159-bc44-7988cfb7ecf7.mp4` |
| Batch File | `1870_to_1880.json` |
| Batch Index | 1 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-22T11:13:02.405130 |

**Pre-Caption:**

> From a high-angle, bird's-eye perspective, the scene is set in a dark, indoor environment where the floor consists of a grid of large, square, white panels illuminated from within. The gaps between these glowing squares are dark. A central figure in a white pinstriped outfit is surrounded by several figures dressed in black, who are positioned in the dark spaces. The entire scene, including the figures, rotates slowly, and small, bright, circular light flares are visible across the composition.

**Initial Feedback:**

> This is not a high-angle perspective.The floor has a white, tile-like appearance, with square panels embedded in it that glow from within. The figures dressed in black are standing on the white tiles. All the figures remain in their respective positions. The camera is rotating clockwise.

**Final Feedback:**

> The perspective in the video is not high-angle. The floor appears to have a white, tile-like design with square panels that glow from within. The figures dressed in black are actually standing on these white tiles. All figures maintain their positions while the camera rotates clockwise.

**GPT Caption (before edit):**

> The scene is set in a dark, indoor environment where the floor features a white, tile-like design with square panels that glow from within. Figures dressed in black are standing on these illuminated tiles, while a central figure in a white pinstriped outfit is also present. The camera rotates clockwise around the scene, and small, bright, circular light flares are visible across the composition.

**Final Caption (after manual edit):**

> The scene is set in a dark, indoor environment where the floor features a white, tile-like design with square panels that glow from within. Figures dressed in black are standing on the floor, while a central figure in a white pinstriped outfit is also present. The camera rotates clockwise around the scene, and small, bright, circular light flares are visible across the composition.

**Diff:**

```diff
- Figures dressed in black are standing on these illuminated tiles, while a central figure in a white pinstriped outfit is also present.
+ Figures dressed in black are standing on the floor, while a central figure in a white pinstriped outfit is also present.
```

**Change Summary:** Added: floor,; Removed: tiles,, illuminated, these

---

### Case 25/70

| Field | Value |
|-------|-------|
| Video ID | `uZudawXgnZ8_2337_2347.mp4` |
| Batch File | `1790_to_1800.json` |
| Batch Index | 8 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-20T02:24:31.659396 |

**Pre-Caption:**

> A pixel-art character stands in a tilled plot of soil, repeatedly moving a watering can up and down. The character then stops this motion, and a black "X" icon containing a white skull and crossbones briefly flashes above their head. Following this, the character remains stationary.

**Initial Feedback:**

> At the beginning of the video, the camera slightly shifts downward and then subtly moves upward towards the end, following the character's movements. Contrary to the description, the character continues watering and does not remain stationary. Additionally, the icon does not feature a white skull and crossbones.The character holds a watering can and moves it up and down, continuously repeating the watering action.

**Final Feedback:**

> At the beginning of the video, the camera slightly shifts downward and then subtly moves upward towards the end, following the character's movements. Contrary to the description, the character continues watering and does not remain stationary. Additionally, the icon does not feature a white skull and crossbones. The character holds a watering can and moves it up and down, continuously repeating the watering action.

**GPT Caption (before edit):**

> A pixel-art character stands in a tilled plot of soil, holding a watering can and continuously moving it up and down in a watering motion. The camera slightly shifts downward at the beginning and subtly moves upward towards the end, following the character's movements. A black "X" icon briefly flashes above the character's head, but it does not feature a white skull and crossbones.

**Final Caption (after manual edit):**

> A pixel-art character stands in a tilled plot of soil, holding a watering can and continuously moving it up and down in a watering motion. The camera slightly shifts downward at the beginning and subtly moves upward towards the end, following the character's movements. A black "X" icon briefly flashes above the character's head.

**Diff:**

```diff
- A black "X" icon briefly flashes above the character's head, but it does not feature a white skull and crossbones.
+ A black "X" icon briefly flashes above the character's head.
```

**Change Summary:** Added: head.; Removed: skull, feature, head,, not, but, crossbones., does, white

---

### Case 26/70

| Field | Value |
|-------|-------|
| Video ID | `ky5uvjPVhk8.3.0.mp4` |
| Batch File | `1790_to_1800.json` |
| Batch Index | 4 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-19T22:38:03.287255 |

**Pre-Caption:**

> A first-person POV shot, filmed as if seen directly through the character’s eyes, moves along a stone-paved path in an outdoor Japanese garden during daylight. The setting features a traditional wooden building with yellow walls and large windows on the right, supported by dark brown beams and surrounded by a low stone border filled with small blue-gray pebbles. To the left, the path curves gently past manicured shrubs, a large rock, and a pond partially visible through the trees. The garden is lush with green foliage, interspersed with trees displaying red and orange autumn leaves. A person pushing a stroller is seen ahead on the path, and the overall environment is calm and well-maintained, with no overlays or additional visual elements present.

**Initial Feedback:**

> The video inaccurately portrays the path as straight, whereas it should be depicted as curving. Furthermore, there are numerous large rocks lining the sides of the path, particularly on the left side, with none on the right.The path is straight, not curved.

**Final Feedback:**

> The video inaccurately represents the path as straight, while it should be shown as curving. Additionally, there are several large rocks lining the sides of the path, especially on the left side, with none on the right.

**GPT Caption (before edit):**

> A first-person POV shot, filmed as if seen directly through the character’s eyes, moves along a gently curving stone-paved path in an outdoor Japanese garden during daylight. The setting features a traditional wooden building with yellow walls and large windows on the right, supported by dark brown beams and surrounded by a low stone border filled with small blue-gray pebbles. To the left, the path curves past manicured shrubs, several large rocks, and a pond partially visible through the trees. The garden is lush with green foliage, interspersed with trees displaying red and orange autumn leaves. A person pushing a stroller is seen ahead on the path, and the overall environment is calm and well-maintained, with no overlays or additional visual elements present.

**Final Caption (after manual edit):**

> A first-person POV shot, filmed as if seen directly through the character’s eyes, moves along a gently curving stone-paved path in an outdoor Japanese garden during daylight. The setting features a traditional wooden building with yellow walls and large windows on the right, supported by dark brown beams and surrounded by a low stone border filled with small blue-gray pebbles. To the left, the path  passed manicured shrubs, several large rocks, and a pond partially visible through the trees. The garden is lush with green foliage, interspersed with trees displaying red and orange autumn leaves. A person pushing a stroller is seen ahead on the path, and the overall environment is calm and well-maintained, with no overlays or additional visual elements present.

**Diff:**

```diff
- To the left, the path curves past manicured shrubs, several large rocks, and a pond partially visible through the trees.
+ To the left, the path  passed manicured shrubs, several large rocks, and a pond partially visible through the trees.
```

**Change Summary:** Added: passed; Removed: curves, past

---

### Case 27/70

| Field | Value |
|-------|-------|
| Video ID | `cdBmwv8-ZBM_1713_1723.mp4` |
| Batch File | `1790_to_1800.json` |
| Batch Index | 3 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-19T11:27:59.523530 |

**Pre-Caption:**

> The man in the leather jacket raises a handgun and shoots another man, who then falls to his knees. The man in the jacket walks forward and kicks the fallen man. As he continues toward a large bonfire, several other men begin to converge on his position from the surrounding area. The man in the jacket then turns and runs in a circular path around the bonfire to evade the approaching men.

**Initial Feedback:**

> The man proceeds toward the large bonfire, shoots an individual holding an axe, and kicks him. This action causes the individual to collide with two others, resulting in their fall. Subsequently, the man runs around the bonfire, but not with the intention of evading the others.The man first shoots a person who has his back to the camera with a handgun and kicks him once, and only afterward does he shoot the man holding the axe.

**Final Feedback:**

> The man approaches the large bonfire, shoots an individual holding an axe, and kicks him, causing the individual to collide with two others, resulting in their fall. Subsequently, the man runs around the bonfire, but not with the intention of evading the others. Initially, he shoots a person who has his back to the camera with a handgun and kicks him once, and only afterward does he shoot the man holding the axe.

**GPT Caption (before edit):**

> The man in the leather jacket approaches a large bonfire and initially shoots a person who has their back to the camera with a handgun, then kicks them once. He then shoots another individual holding an axe, causing them to collide with two others, resulting in their fall. Afterward, the man in the jacket walks forward and kicks the fallen man. He continues toward the bonfire and runs in a circular path around it, not with the intention of evading the approaching men.

**Final Caption (after manual edit):**

> The man in the leather jacket approaches a large bonfire and initially shoots a person who has their back to the camera with a handgun, then kicks them once. He then shoots another individual holding an axe and kicks it, causing them to collide with two others, resulting in their fall. He continues toward the bonfire and runs in a circular path around it, not with the intention of evading the approaching men.

**Diff:**

```diff
- He then shoots another individual holding an axe, causing them to collide with two others, resulting in their fall.
- Afterward, the man in the jacket walks forward and kicks the fallen man.
+ He then shoots another individual holding an axe and kicks it, causing them to collide with two others, resulting in their fall.
```

**Change Summary:** Added: axe; Removed: afterward,, forward, axe,, walks, man., fallen

---

### Case 28/70

| Field | Value |
|-------|-------|
| Video ID | `0Pzq0URbL2M.7.3.mp4` |
| Batch File | `1790_to_1800.json` |
| Batch Index | 0 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-12-11T12:09:40.418278 |

**Pre-Caption:**

> The scene is set within a laboratory, characterized by a cool, desaturated color palette. The focus is on a worn, white workbench cluttered with scientific equipment. Several glass petri dishes are scattered across the surface, some open and others with lids askew, containing various cultures, including one with greenish, lumpy growths and others with dark liquids or streaked patterns. In the background, racks hold test tubes filled with red and blue liquids, alongside an Erlenmeyer flask and other glassware. A figure in a white lab coat stands on the right side of the scene, with their back partially toward the camera.

**Initial Feedback:**

> All of the petri dishes have no lids on them. In the background, a rack of test tubes containing blue liquid and another rack with test tubes capped with red lids can be seen.

**Final Feedback:**

> The petri dishes in the scene are all without lids. In the background, there is a rack of test tubes filled with blue liquid and another rack with test tubes that have red lids.

**GPT Caption (before edit):**

> The scene is set within a laboratory, characterized by a cool, desaturated color palette. The focus is on a worn, white workbench cluttered with scientific equipment. Several glass petri dishes are scattered across the surface, all without lids, containing various cultures, including one with greenish, lumpy growths and others with dark liquids or streaked patterns. In the background, a rack holds test tubes filled with blue liquid, alongside another rack with test tubes that have red lids, as well as an Erlenmeyer flask and other glassware. A figure in a white lab coat stands on the right side of the scene, with their back partially toward the camera.

**Final Caption (after manual edit):**

> The scene is set within a laboratory, characterized by a cool, desaturated color palette. The focus is on a worn, white workbench cluttered with scientific equipment. Several glass petri dishes are scattered across the surface, all without lids, containing various cultures, including one with greenish, lumpy growths and others with dark liquids or streaked patterns. In the background, a rack holds test tubes,one of which filled with blue liquid, alongside another rack with test tubes that have red lids, as well as an Erlenmeyer flask and other glassware. A figure in a white lab coat stands on the right side of the scene, with their back partially toward the camera.

**Diff:**

```diff
- In the background, a rack holds test tubes filled with blue liquid, alongside another rack with test tubes that have red lids, as well as an Erlenmeyer flask and other glassware.
+ In the background, a rack holds test tubes,one of which filled with blue liquid, alongside another rack with test tubes that have red lids, as well as an Erlenmeyer flask and other glassware.
```

**Change Summary:** Added: which, tubes,one

---

### Case 29/70

| Field | Value |
|-------|-------|
| Video ID | `XPPcA1hAfp4_3302_3312.mp4` |
| Batch File | `1750_to_1760.json` |
| Batch Index | 9 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-10T00:36:03.047873 |

**Pre-Caption:**

> The player character places a wooden bridge tile to connect a dirt ledge to a large wooden platform. The character then walks forward across the newly placed bridge and onto the platform, where it comes to a stop. After a brief pause, the character turns to the right and then immediately turns back to face forward.

**Initial Feedback:**

> The character places four wooden bridge tiles, then walks along the bridge onto the dirt ledge.

**Final Feedback:**

> The character places four wooden bridge tiles, creating a path to the dirt ledge, and then walks across the bridge onto the ledge.

**GPT Caption (before edit):**

> The player character places four wooden bridge tiles, creating a path to the dirt ledge. The character then walks across the bridge onto the ledge, where it comes to a stop. After a brief pause, the character turns to the right and then immediately turns back to face forward.

**Final Caption (after manual edit):**

> The player character places four wooden bridge tiles, creating a path to the dirt ledge. The character then walks across the bridge onto the ledge, where it comes to a stop.

**Diff:**

```diff
- After a brief pause, the character turns to the right and then immediately turns back to face forward.
```

**Change Summary:** Removed: face, right, turns, brief, after, forward., immediately, and, back, pause,

---

### Case 30/70

| Field | Value |
|-------|-------|
| Video ID | `Tb03_fw4VmI_1408_1413.mp4` |
| Batch File | `1750_to_1760.json` |
| Batch Index | 7 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-12-10T00:19:15.735772 |

**Pre-Caption:**

> This wide scenery shot initially frames a range of snow-covered mountains in the background, positioned across the horizontal center. The sky occupies the top half of the frame, while dark, undulating water fills the bottom half, extending from the foreground to the middle ground. The camera, positioned at water level, then submerges, moving downwards. The perspective shifts to a fully underwater view, where the dark water fills the entire frame. The water's surface is now visible as a bright, blurry line at the top of the frame, with small, out-of-focus bubbles floating in the foreground and middle ground. The camera's final position is at a low angle, looking up from below the surface.

**Initial Feedback:**

> The camera is at level angle.

**Final Feedback:**

> The camera maintains a level angle throughout the transition from above water to below, providing a consistent and immersive perspective.

**GPT Caption (before edit):**

> This wide scenery shot begins with a range of snow-covered mountains in the background, positioned across the horizontal center. The sky occupies the top half of the frame, while dark, undulating water fills the bottom half, extending from the foreground to the middle ground. The camera, maintaining a level angle, smoothly transitions from above water to below, offering a consistent and immersive perspective. As it submerges, the view shifts to a fully underwater scene, where the dark water fills the entire frame. The water's surface is now visible as a bright, blurry line at the top, with small, out-of-focus bubbles floating in the foreground and middle ground. The camera's final position is at a low angle, looking up from below the surface.

**Final Caption (after manual edit):**

> This wide scenery shot begins with a range of snow-covered mountains in the background, positioned across the horizontal center. The sky occupies the top half of the frame, while dark, undulating water fills the bottom half, extending from the foreground to the middle ground. The camera, maintaining a level angle, smoothly transitions from above water to below, offering a consistent and immersive perspective. As it submerges, the view shifts to a fully underwater scene, where the dark water fills the entire frame. The water's surface is now visible as a bright, blurry line at the top, with small, out-of-focus bubbles floating in the foreground and middle ground.

**Diff:**

```diff
- The camera's final position is at a low angle, looking up from below the surface.
```

**Change Summary:** Removed: camera's, low, looking, up, final, surface., position, below

---

### Case 31/70

| Field | Value |
|-------|-------|
| Video ID | `urgDBUXShos.0.8.mp4` |
| Batch File | `1530_to_1540.json` |
| Batch Index | 1 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-21T23:41:53.403161 |

**Pre-Caption:**

> A man, seen from over his right shoulder, confronts a woman in a close-up shot. The man has messy, wavy, blondish-green hair and is wearing a purple jacket. His face, partially visible, is covered in white makeup with dark coloration around his mouth. His left hand, clad in a purple leather glove, cups the right cheek of the light-skinned woman. The woman has brown hair pulled back, a dark sleeveless top, and a small earring in her right ear; her expression is tense. The man holds a metallic knife, positioning the blade near the corner of the woman's mouth.

**Initial Feedback:**

> The man is wearing a purple leather glove on his right hand. The woman is wearing a small earring in her left ear.

**Final Feedback:**

> The man is wearing a purple leather glove on his right hand, not his right. Additionally, the woman is wearing a small earring in her left ear, not her left.

**GPT Caption (before edit):**

> A man, seen from over his right shoulder, confronts a woman in a close-up shot. The man has messy, wavy, blondish-green hair and is wearing a purple jacket. His face, partially visible, is covered in white makeup with dark coloration around his mouth. His left hand, clad in a purple leather glove, cups the right cheek of the light-skinned woman. The woman has brown hair pulled back, a dark sleeveless top, and a small earring in her right ear; her expression is tense. The man holds a metallic knife, positioning the blade near the corner of the woman's mouth.

**Final Caption (after manual edit):**

> A man, seen from over his right shoulder, confronts a woman in a close-up shot. The man has messy, wavy, blondish-green hair and is wearing a purple jacket. His face, partially visible, is covered in white makeup with dark coloration around his mouth. His right hand, clad in a purple leather glove, cups the right cheek of the light-skinned woman. The woman has brown hair pulled back, a dark sleeveless top, and a small earring in her left ear; her expression is tense. The man holds a metallic knife, positioning the blade near the corner of the woman's mouth.

**Diff:**

```diff
- His left hand, clad in a purple leather glove, cups the right cheek of the light-skinned woman.
- The woman has brown hair pulled back, a dark sleeveless top, and a small earring in her right ear; her expression is tense.
+ His right hand, clad in a purple leather glove, cups the right cheek of the light-skinned woman.
+ The woman has brown hair pulled back, a dark sleeveless top, and a small earring in her left ear; her expression is tense.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

### Case 32/70

| Field | Value |
|-------|-------|
| Video ID | `JpEfHcVrtXI.5.4.mp4` |
| Batch File | `overlap_1300_to_1310.json` |
| Batch Index | 9 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-19T16:23:32.133799 |

**Pre-Caption:**

> In an extreme wide shot, a small, glowing creature is initially positioned on a rock ledge on the right side of the frame, in the middle ground. A large, spiky log bridge spans the center of the frame, also in the middle ground, connecting rock formations on the left and right. The creature jumps from the right ledge, moving left across the center of the frame and under the spiky bridge. It then performs a mid-air dash, propelling itself further left to land on the vertical face of the left-side rock formation. The camera, positioned at the subject's height to capture the scene in profile, pans slightly to the left to follow the creature's movement. A bright blue crystal is visible in the upper right background, and HUD elements are overlaid in the top-left and bottom-center foreground.

**Initial Feedback:**

> The video is a 2D shot, which means the concepts of foreground, middle ground, and background do not apply. The camera follows the character as it moves downward, briefly pausing when the character stops or jumps upward. It also moves left and right as the character leaps sideways.The creature leaps to the left, landing on the left rock wall, then bounces off from there to the right.

**Final Feedback:**

> The video is a 2D shot, so the terms foreground, middle ground, and background are not applicable. The camera tracks the character's movement as it descends, pausing momentarily when the character stops or jumps upward. It also shifts left and right as the character leaps sideways. The creature jumps to the left, lands on the left rock wall, and then bounces back to the right.

**GPT Caption (before edit):**

> In a 2D shot, a small, glowing creature starts on a rock ledge on the right side of the frame. A large, spiky log bridge spans the center, connecting rock formations on both sides. The creature jumps left across the frame, moving under the spiky bridge, and performs a mid-air dash to land on the vertical face of the left rock formation. The camera tracks the creature's movement, shifting left and right as it leaps sideways and pausing when the creature stops or jumps upward. After landing on the left rock wall, the creature bounces back to the right. A bright blue crystal is visible in the upper right, and HUD elements are overlaid in the top-left and bottom-center of the frame.

**Final Caption (after manual edit):**

> In a 2D shot, a small, glowing creature starts on a rock ledge on the right side of the frame. A large, spiky log bridge spans the center, connecting rock formations on both sides. The creature jumps left across the frame, moving under the spiky bridge, and lands on the vertical face of the left rock formation. The camera tracks the creature's movement, shifting left and right as it leaps sideways and pausing when the creature stops or jumps upward. After landing on the left rock wall, the creature bounces back to the right. A bright blue crystal is visible in the upper right, and HUD elements are overlaid in the top-left and bottom-center of the frame.

**Diff:**

```diff
- The creature jumps left across the frame, moving under the spiky bridge, and performs a mid-air dash to land on the vertical face of the left rock formation.
+ The creature jumps left across the frame, moving under the spiky bridge, and lands on the vertical face of the left rock formation.
```

**Change Summary:** Added: lands; Removed: land, mid-air, dash, performs

---

### Case 33/70

| Field | Value |
|-------|-------|
| Video ID | `0OFBj7EjZ-g.1.1.mp4` |
| Batch File | `overlap_1300_to_1310.json` |
| Batch Index | 2 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-19T10:01:23.345899 |

**Pre-Caption:**

> A central, pillar-like structure features a smooth, translucent, light blue cylinder positioned vertically between two circular, light gray platforms at its top and bottom. The two platforms shatter into numerous sharp, angular, light gray fragments that fly outwards, while the central blue cylinder remains intact. Two thin diagonal lines, one pink and one light green, are also visible.

**Initial Feedback:**

> The cylinder stands vertically between two light-blue circular platforms above and below it. Then several transparent fragments gather around the cylinder.

**Final Feedback:**

> The cylinder is positioned vertically between two light blue circular platforms, one above and one below. Subsequently, numerous transparent fragments appear to gather around the cylinder.

**GPT Caption (before edit):**

> A central, pillar-like structure features a smooth, translucent, light blue cylinder positioned vertically between two circular, light gray platforms, one above and one below. Numerous transparent fragments appear to gather around the cylinder, while two thin diagonal lines, one pink and one light green, are also visible.

**Final Caption (after manual edit):**

> A central, pillar-like structure features a smooth, translucent, light blue cylinder positioned vertically between two circular, light blue platforms, one above and one below. Numerous transparent fragments appear to gather around the cylinder, while two thin diagonal lines, one pink and one light green, are also visible.

**Diff:**

```diff
- A central, pillar-like structure features a smooth, translucent, light blue cylinder positioned vertically between two circular, light gray platforms, one above and one below.
+ A central, pillar-like structure features a smooth, translucent, light blue cylinder positioned vertically between two circular, light blue platforms, one above and one below.
```

**Change Summary:** Removed: gray

---

### Case 34/70

| Field | Value |
|-------|-------|
| Video ID | `Hv_DRJZZ2qI.2.0.mp4` |
| Batch File | `overlap_1220_to_1230.json` |
| Batch Index | 7 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-19T06:53:22.986898 |

**Pre-Caption:**

> Two women are sitting next to each other, looking toward the right. The woman on the left has light skin, long blonde hair, and is wearing a black tank top. On her head is a white and grey knit beanie with a pom-pom. She wears a black wristband and a colorful patterned wristband on her left wrist. She initially has her hand near her mouth and then brings her hands together. The woman to her right has light skin and long brown hair. She is wearing black sunglasses, a black hooded jacket over a t-shirt with a pink and white graphic, a ring on her right hand, and a pink wristband. She keeps her hand near her mouth.

**Initial Feedback:**

> The woman on the left also has a black wristband and a colorful patterned wristband on her right wrist. The woman on the right wears a ring on her left hand.

**Final Feedback:**

> The woman on the left is wearing a black wristband and a colorful patterned wristband on her right wrist, not her left. Additionally, the woman on the right is wearing a ring on her left hand, not her right.

**GPT Caption (before edit):**

> Two women are sitting next to each other, looking toward the right. The woman on the left has light skin, long blonde hair, and is wearing a black tank top. On her head is a white and grey knit beanie with a pom-pom. She wears a black wristband and a colorful patterned wristband on her right wrist. She initially has her hand near her mouth and then brings her hands together. The woman to her right has light skin and long brown hair. She is wearing black sunglasses, a black hooded jacket over a t-shirt with a pink and white graphic, a ring on her left hand, and a pink wristband. She keeps her hand near her mouth.

**Final Caption (after manual edit):**

> Two women are sitting next to each other, looking toward the right. The woman on the left has light skin, long blonde hair, and is wearing a black tank top. On her head is a white and grey knit beanie with a pom-pom. She wears a black wristband and a colorful patterned wristband on her left wrist. She wears a black wristband and a colorful patterned wristband on her right wrist. She initially has her hand near her mouth and then brings her hands together. The woman to her right has light skin and long brown hair. She is wearing black sunglasses, a black hooded jacket over a t-shirt with a pink and white graphic, a ring on her left hand, and a pink wristband. She keeps her hand near her mouth.

**Diff:**

```diff
+ She wears a black wristband and a colorful patterned wristband on her left wrist.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

### Case 35/70

| Field | Value |
|-------|-------|
| Video ID | `y0aS2n1WmMg.1.0.mp4` |
| Batch File | `overlap_1220_to_1230.json` |
| Batch Index | 4 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-19T04:31:15.163154 |

**Pre-Caption:**

> The scene is framed as a revealing shot through a narrow vertical opening, with large, dark, out-of-focus shapes occupying the foreground on the left and right. Initially, the view shows a bed in the middle ground, positioned in the center of the frame, with a nightstand and lamp to its right. A silhouetted figure then enters from the left, moving into the middle ground and walking towards the right, transitioning the view into a full shot. The figure comes to a stop and sits on the edge of the bed, now located in the center-right of the frame. The camera remains static and positioned at the subject's level throughout the action.

**Initial Feedback:**

> The bed is in the middle ground and background, not the background.
The camera shows some minor movement. The camera is panning right to left.

**Final Feedback:**

> The bed is positioned in the middle ground and the background. Additionally, there is slight camera movement, as it pans from right to left.

**GPT Caption (before edit):**

> The scene is framed as a revealing shot through a narrow vertical opening, with large, dark, out-of-focus shapes occupying the foreground on the left and right. Initially, the view shows a bed in the middle ground, positioned in the center of the frame, with a nightstand and lamp to its right. A silhouetted figure then enters from the left, moving into the middle ground and walking towards the right, transitioning the view into a full shot. The figure comes to a stop and sits on the edge of the bed, now located in the center-right of the frame. The camera slightly pans from right to left, remaining at the subject's level throughout the action.

**Final Caption (after manual edit):**

> The scene is framed as a revealing shot through a narrow vertical opening, with large, dark, out-of-focus shapes occupying the foreground on the left and right. Initially, the view shows a bed in the middle ground and background, positioned in the center of the frame, with a nightstand and lamp to its right. A silhouetted figure then enters from the left, moving into the middle ground and walking towards the right, transitioning the view into a full shot. The figure comes to a stop and sits on the edge of the bed, now located in the center-right of the frame. The camera slightly pans from right to left, remaining at the subject's level throughout the action.

**Diff:**

```diff
- Initially, the view shows a bed in the middle ground, positioned in the center of the frame, with a nightstand and lamp to its right.
+ Initially, the view shows a bed in the middle ground and background, positioned in the center of the frame, with a nightstand and lamp to its right.
```

**Change Summary:** Added: background,; Removed: ground,

---

### Case 36/70

| Field | Value |
|-------|-------|
| Video ID | `0OFBj7EjZ-g.3.2.mp4` |
| Batch File | `overlap_1220_to_1230.json` |
| Batch Index | 0 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-11-11T12:40:29.734765 |

**Pre-Caption:**

> From a high-angle perspective, a multi-tiered wooden cabinet is lifted vertically, revealing a stylized, low-polygon figure lying motionless on its back on the floor below. The figure and all other surrounding objects remain stationary throughout the video.

**Initial Feedback:**

> The video inaccurately depicts only one multi-tiered wooden cabinet being lifted, when in fact, two cabinets are raised. Additionally, while the cabinets are being elevated, all other objects, including the stylized figure, remain entirely motionless.

**Final Feedback:**

> The video inaccurately shows only one multi-tiered wooden cabinet being lifted, whereas, in reality, two cabinets are raised. Furthermore, during the elevation of the cabinets, all other objects, including the stylized figure, remain completely motionless.

**GPT Caption (before edit):**

> From a high-angle perspective, two multi-tiered wooden cabinets are lifted vertically, revealing a stylized, low-polygon figure lying motionless on its back on the floor below. The figure and all other surrounding objects remain completely stationary throughout the video.

**Final Caption (after manual edit):**

> From a high-angle perspective, two multi-tiered wooden cabinets are lifted vertically, revealing a stylized, low-polygon figure lying motionless on its back on the floor below. All surrounding objects remain completely stationary throughout the video, except for the two cabinets that are lifted.

**Diff:**

```diff
- The figure and all other surrounding objects remain completely stationary throughout the video.
+ All surrounding objects remain completely stationary throughout the video, except for the two cabinets that are lifted.
```

**Change Summary:** Added: video,, for, that, lifted., except; Removed: video., other, and

---

### Case 37/70

| Field | Value |
|-------|-------|
| Video ID | `H4AZhS5WqKk.0.15.mp4` |
| Batch File | `overlap_1180_to_1190.json` |
| Batch Index | 2 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-11-06T11:46:08.464261 |

**Pre-Caption:**

> The video begins with a close-up of a large, gray-blue cat occupying the left foreground. A smaller, red cat, visible in a full shot, materializes in the middle ground on the right side of the frame, standing on a white cloud and surrounded by swirling red trails. In the background, a dark wall is punctuated by out-of-focus white lights. The red cat, its cloud, and the red trails then disappear from the right side of the frame. Subsequently, the gray-blue cat moves from the left towards the right, partially exiting the frame until only the right side of its head and ear remain visible on the far left. The camera is positioned at the subjects' level throughout the sequence.

**Initial Feedback:**

> The red cat is also in the foreground. Part of the background is a dark wall, and part is a window. The gray-blue cat partially exits the frame, until only the left side of its head and ear remain visible on the far right.

**Final Feedback:**

> The red cat is also positioned in the foreground. The background consists of a dark wall and a window. The gray-blue cat moves partially out of the frame, leaving only the left side of its head and ear visible on the far right.

**GPT Caption (before edit):**

> The video begins with a close-up of a large, gray-blue cat occupying the left foreground. A smaller, red cat, also positioned in the foreground, materializes in the middle ground on the right side of the frame, standing on a white cloud and surrounded by swirling red trails. In the background, a dark wall and a window are visible, punctuated by out-of-focus white lights. The red cat, its cloud, and the red trails then disappear from the right side of the frame. Subsequently, the gray-blue cat moves from the left towards the right, partially exiting the frame until only the left side of its head and ear remain visible on the far right. The camera is positioned at the subjects' level throughout the sequence.

**Final Caption (after manual edit):**

> The video begins with a close-up of a large, gray-blue cat occupying the left foreground. A smaller, red cat, also positioned in the foreground, on the right side of the frame, standing on a white cloud and surrounded by swirling red trails. In the background, a dark wall and a window are visible, punctuated by out-of-focus white lights. The red cat, its cloud, and the red trails then disappear from the right side of the frame. Subsequently, the gray-blue cat moves from the left towards the right, partially exiting the frame until only the left side of its head and ear remain visible on the far right. The camera is positioned at the subjects' level throughout the sequence.

**Diff:**

```diff
- A smaller, red cat, also positioned in the foreground, materializes in the middle ground on the right side of the frame, standing on a white cloud and surrounded by swirling red trails.
+ A smaller, red cat, also positioned in the foreground, on the right side of the frame, standing on a white cloud and surrounded by swirling red trails.
```

**Change Summary:** Removed: middle, materializes, ground

---

### Case 38/70

| Field | Value |
|-------|-------|
| Video ID | `5eDQ2SSsmEk.3.0.mp4` |
| Batch File | `overlap_1120_to_1130.json` |
| Batch Index | 6 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-29T06:52:36.497347 |

**Pre-Caption:**

> The camera slowly pans down and to the right, moving across the surface of a static, creased poster. The view begins focused on the upper portion of the artwork and the word "Island," then moves to reveal the text "TICKETS STARTING FROM 100.000€" at the bottom.

**Initial Feedback:**

> The camera shows a clear movement pattern. The camera is tilting down.
The word is not "Island", but "Islands".

**Final Feedback:**

> The camera demonstrates a clear movement pattern, tilting downwards. Additionally, the word displayed is "Islands," not "Island."

**GPT Caption (before edit):**

> The camera tilts downwards and to the right, moving across the surface of a static, creased poster. The view begins focused on the upper portion of the artwork and the word "Islands," then moves to reveal the text "TICKETS STARTING FROM 100.000€" at the bottom.

**Final Caption (after manual edit):**

> The camera tilts downwards, moving across the surface of a static, creased poster. The view begins focused on the upper portion of the artwork and the word "Islands," then moves to reveal the text "TICKETS STARTING FROM 100.000€" at the bottom.

**Diff:**

```diff
- The camera tilts downwards and to the right, moving across the surface of a static, creased poster.
+ The camera tilts downwards, moving across the surface of a static, creased poster.
```

**Change Summary:** Added: downwards,; Removed: right,, downwards

---

### Case 39/70

| Field | Value |
|-------|-------|
| Video ID | `ORHIVufNfRM.13.6.mp4` |
| Batch File | `overlap_1090_to_1100.json` |
| Batch Index | 9 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-10-27T08:20:55.666728 |

**Pre-Caption:**

> From a first-person perspective, the scene moves forward through a dense underwater environment. A pair of gloved hands remains stationary in the foreground at the bottom of the frame. The view is populated by tall, stalk-like structures that occupy the foreground, middle ground, and background, extending from the bottom to the top of the frame. The camera is positioned below the large, flat caps of these structures. Initially, a school of small, glowing creatures is positioned in the left-center middle ground. As the camera glides forward and slightly to the right, the school of creatures shifts toward the left side of the frame. A single, thin, glowing creature enters from the right middle ground and swims horizontally to the left, passing behind a large stalk in the center. The forward movement causes the foreground stalks to move past the viewer, revealing more of the middle and background elements.

**Initial Feedback:**

> The gloved hands are not stationary; they are in motion, intermittently appearing and disappearing from the screen. The small glowing creatures move from the middle ground on the left toward the foreground on the left before disappearing from the frame. The slender glowing creature is positioned in the right middle ground, swimming away from the camera.

**Final Feedback:**

> The gloved hands are not stationary; they move intermittently, appearing and disappearing from the screen. The small glowing creatures transition from the middle ground on the left to the foreground on the left before disappearing from view. The slender glowing creature is located in the right middle ground and swims away from the camera.

**GPT Caption (before edit):**

> From a first-person perspective, the scene moves forward through a dense underwater environment. A pair of gloved hands intermittently appears and disappears at the bottom of the frame. The view is populated by tall, stalk-like structures that occupy the foreground, middle ground, and background, extending from the bottom to the top of the frame. The camera is positioned below the large, flat caps of these structures. Initially, a school of small, glowing creatures is positioned in the left-center middle ground. As the camera glides forward and slightly to the right, the school of creatures transitions to the foreground on the left before disappearing from view. A single, thin, glowing creature is located in the right middle ground and swims away from the camera, passing behind a large stalk in the center. The forward movement causes the foreground stalks to move past the viewer, revealing more of the middle and background elements.

**Final Caption (after manual edit):**

> From a first-person perspective, the scene moves forward through a dense underwater environment. A pair of gloved hands intermittently appears and disappears at the bottom of the frame. The view is populated by tall, stalk-like structures that occupy the foreground, middle ground, and background, extending from the bottom to the top of the frame. The camera is positioned below the large, flat caps of these structures. Initially, a school of small, glowing creatures is positioned in the left-center middle ground. As the camera glides forward andpans slightly to the right, the school of creatures transitions to the foreground on the left before disappearing from view. A single, thin, glowing creature is located in the right middle ground and swims away from the camera, passing behind a large stalk in the center. The forward movement causes the foreground stalks to move past the viewer, revealing more of the middle and background elements.

**Diff:**

```diff
- As the camera glides forward and slightly to the right, the school of creatures transitions to the foreground on the left before disappearing from view.
+ As the camera glides forward andpans slightly to the right, the school of creatures transitions to the foreground on the left before disappearing from view.
```

**Change Summary:** Added: andpans

---

### Case 40/70

| Field | Value |
|-------|-------|
| Video ID | `KF5p8VIbt0Y.3.2.mp4` |
| Batch File | `overlap_1080_to_1090.json` |
| Batch Index | 8 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-26T08:12:16.527910 |

**Pre-Caption:**

> In a black-and-white video, a man with dark hair, wearing a dark suit jacket and trousers, is suspended horizontally in mid-air. He is holding onto the back of a dark, old-fashioned trolley with his outstretched arms. His body is parallel to the ground, and his legs are bent at the knees and kicked up behind him as if he has just jumped from the moving vehicle.

**Initial Feedback:**

> The man holds a bag in his left hand and grips the back of the trolley with his right hand. He first runs alongside the trolley, and then his body floats horizontally in the air. He does not jump from the moving vehicle.

**Final Feedback:**

> The man is holding a bag in his left hand while gripping the back of the trolley with his right hand. Initially, he runs alongside the trolley before his body is seen floating horizontally in the air. Contrary to the caption, he does not jump from the moving vehicle.

**GPT Caption (before edit):**

> In a black-and-white video, a man with dark hair, wearing a dark suit jacket and trousers, is seen running alongside an old-fashioned trolley. He grips the back of the trolley with his right hand while holding a bag in his left hand. As he runs, his body becomes suspended horizontally in mid-air, parallel to the ground, with his legs bent at the knees and kicked up behind him. Contrary to initial impressions, he does not jump from the moving vehicle.

**Final Caption (after manual edit):**

> In a black-and-white video, a man with dark hair, wearing a dark suit jacket and trousers, is seen running alongside an old-fashioned trolley. He grips the back of the trolley with his right hand while holding a bag in his left hand. As he runs, his body becomes suspended horizontally in mid-air, parallel to the ground, with his legs bent at the knees and kicked up behind him.

**Diff:**

```diff
- Contrary to initial impressions, he does not jump from the moving vehicle.
```

**Change Summary:** Removed: from, impressions,, jump, moving, initial, not, contrary, does, vehicle.

---

### Case 41/70

| Field | Value |
|-------|-------|
| Video ID | `3epU697sU9E.7.5.mp4` |
| Batch File | `overlap_1070_to_1080.json` |
| Batch Index | 3 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-23T08:44:11.323271 |

**Pre-Caption:**

> In an indoor setting at Barksdale Air Force Base, a man in a dark suit and red tie stands behind a wooden podium. The room has light gray walls, and behind the man, four framed portraits are arranged in a grid. An American flag is positioned to his right. An overlay in the bottom left corner displays white text reading "10:22 am" and "Barksdale Air Force Base."

**Initial Feedback:**

> Behind the man, numerous framed portraits are arranged in a square pattern. The American flag is positioned directly in front of him.

**Final Feedback:**

> The feedback contains inaccuracies. Eight portraits are arranged in a grid behind the man, and the American flag is positioned to his back.

**GPT Caption (before edit):**

> In an indoor setting at Barksdale Air Force Base, a man in a dark suit and red tie stands behind a wooden podium. The room has light gray walls, and behind the man, four framed portraits are arranged in a grid. An American flag is positioned to his right. An overlay in the bottom left corner displays white text reading "10:22 am" and "Barksdale Air Force Base."

**Final Caption (after manual edit):**

> In an indoor setting at Barksdale Air Force Base, a man in a dark suit and red tie stands behind a wooden podium. The room has light gray walls, and behind the man, eight framed portraits are arranged in a grid. An American flag is positioned to his back. An overlay in the bottom left corner displays white text reading "10:22 am" and "Barksdale Air Force Base."

**Diff:**

```diff
- The room has light gray walls, and behind the man, four framed portraits are arranged in a grid.
- An American flag is positioned to his right.
+ The room has light gray walls, and behind the man, eight framed portraits are arranged in a grid.
+ An American flag is positioned to his back.
```

**Change Summary:** Added: eight, back.; Removed: four, right.

---

### Case 42/70

| Field | Value |
|-------|-------|
| Video ID | `pY50Mu04Fjs_0000_0005.mp4` |
| Batch File | `1510_to_1520.json` |
| Batch Index | 6 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-22T08:58:32.570853 |

**Pre-Caption:**

> An indoor scene features a light gray, rounded planter designed to look like a face with closed eyes and a nose. A pair of black, round-framed glasses sits on the planter's face, and vibrant green, grass-like artificial foliage sprouts from the top. The planter is placed on a glossy surface with a gray and black swirled pattern. In the blurred background, a white curtain and a red object are visible. The camera slowly pushes in toward the planter.

**Initial Feedback:**

> This is not a rounded planter, but a cylindrical one. The camera is moving backward while zooming in.

**Final Feedback:**

> The planter is cylindrical rather than rounded. Additionally, the camera is moving backward while zooming in.

**GPT Caption (before edit):**

> An indoor scene features a light gray, cylindrical planter designed to look like a face with closed eyes and a nose. A pair of black, round-framed glasses sits on the planter's face, and vibrant green, grass-like artificial foliage sprouts from the top. The planter is placed on a glossy surface with a gray and black swirled pattern. In the blurred background, a white curtain and a red object are visible. The camera slowly pulls back while zooming in on the planter.

**Final Caption (after manual edit):**

> An indoor scene features a light gray, cylindrical planter designed to look like a face with closed eyes and a nose. A pair of black, round-framed glasses sits on the planter's face, and vibrant green, grass-like artificial foliage sprouts from the top. The planter is placed on a glossy surface with a gray and black swirled pattern. In the blurred background, a white curtain and a red object are visible. The camera slowly moves backward while zooming in on the planter.

**Diff:**

```diff
- The camera slowly pulls back while zooming in on the planter.
+ The camera slowly moves backward while zooming in on the planter.
```

**Change Summary:** Added: moves, backward; Removed: pulls, back

---

### Case 43/70

| Field | Value |
|-------|-------|
| Video ID | `ti231UvSvfQ.7.2.mp4` |
| Batch File | `1490_to_1500.json` |
| Batch Index | 9 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-10-17T03:16:05.278028 |

**Pre-Caption:**

> This scene takes place in a dimly lit, sterile-looking room with plain, light-gray walls. An elderly person is lying in a bed with white sheets, positioned on the left side of the scene. A white, articulated desk lamp is attached to the wall, its light directed towards the bed. To the right, a young man in a blue sweatshirt stands holding an open blue folder. In the background, a door is visible with a green sign above it. Next to the bed, a small table holds an orange sharps container. The overall color palette is cool and desaturated, consisting mainly of grays and blues.

**Initial Feedback:**

> The desk lamp is not lit and is turned off. The only man wearing blue is sitting. The green sign is on the wall, not above the door.

**Final Feedback:**

> The desk lamp is not illuminated and is turned off. The only man wearing blue is seated, not standing. Additionally, the green sign is located on the wall, not above the door.

**GPT Caption (before edit):**

> This scene takes place in a dimly lit, sterile-looking room with plain, light-gray walls. An elderly person is lying in a bed with white sheets, positioned on the left side of the scene. A white, articulated desk lamp is attached to the wall, but it is turned off. To the right, a young man in a blue sweatshirt is seated, holding an open blue folder. In the background, a door is visible, and a green sign is located on the wall. Next to the bed, a small table holds an orange sharps container. The overall color palette is cool and desaturated, consisting mainly of grays and blues.

**Final Caption (after manual edit):**

> This scene takes place in a dimly lit, sterile-looking room with plain, light-gray walls. An elderly person is lying in a bed with white sheets, positioned on the left side of the scene. A white, articulated desk lamp is on the table, but it is turned off. To the right, a young man in a blue sweatshirt is seated, holding an open blue folder. In the background, a door is visible, and a green sign is located on the wall. Next to the bed, a small table holds an orange sharps container. The overall color palette is cool and desaturated, consisting mainly of grays and blues.

**Diff:**

```diff
- A white, articulated desk lamp is attached to the wall, but it is turned off.
+ A white, articulated desk lamp is on the table, but it is turned off.
```

**Change Summary:** Added: table,; Removed: wall,, attached

---

### Case 44/70

| Field | Value |
|-------|-------|
| Video ID | `BNzc6hG3yN4.0.3.mp4` |
| Batch File | `1490_to_1500.json` |
| Batch Index | 8 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-17T02:58:02.372212 |

**Pre-Caption:**

> From a high, top-down perspective, the scene remains completely static. A man lies motionless on his back on the pavement, and another person sits still on a bicycle. Two other bicycles are also stationary on the ground. There is no movement from any of the subjects or objects in the frame.

**Initial Feedback:**

> The scene is not static.The camera is craning up in an arc.
The man lying on the ground is not still; his hands and face are in motion. The bicycles are stationary, and on one of the bicycles sits a Black man who remains still.

**Final Feedback:**

> The scene is not entirely static, as the camera is moving upward in an arc. The man lying on the ground is not completely motionless; his hands and face show some movement. While the bicycles are stationary, a Black man is sitting still on one of them.

**GPT Caption (before edit):**

> From a high, top-down perspective, the camera moves upward in an arc. A man lies on his back on the pavement, with slight movements in his hands and face. Another person, a Black man, sits still on a bicycle, while two other bicycles remain stationary on the ground.

**Final Caption (after manual edit):**

> From a high, top-down perspective, the camera moves upward in an arc. A man lies on his back on the pavement, with slight movements in his hands and face. Another person, a Black man, sits still on a bicycle, while another bicycles remain stationary on the ground.

**Diff:**

```diff
- Another person, a Black man, sits still on a bicycle, while two other bicycles remain stationary on the ground.
+ Another person, a Black man, sits still on a bicycle, while another bicycles remain stationary on the ground.
```

**Change Summary:** Removed: two, other

---

### Case 45/70

| Field | Value |
|-------|-------|
| Video ID | `BNzc6hG3yN4.0.3.mp4` |
| Batch File | `1490_to_1500.json` |
| Batch Index | 8 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-10-17T02:44:29.003851 |

**Pre-Caption:**

> From a high, top-down perspective, a Black man with short hair lies on his back on a paved surface. He is wearing a black jacket over a blue and white patterned shirt, dark pants, and white sneakers with green accents. Near his head, a dark-colored bicycle with a black bag attached to the back lies on its side. Near his feet, a second bicycle, a BMX-style bike with a white frame and blue accents on the rims and handlebars, also lies on its side on the pavement.

**Initial Feedback:**

> To the left of the Black man, there is a black-and-red bicycle with another Black man sitting on it, and next to him is a black tire. To the right of the Black man, there is a blue-and-white bicycle placed upside down on the ground, with an orange-and-white traffic barrier beside it.

**Final Feedback:**

> To the left of the Black man, there is a black-and-red bicycle with another Black man seated on it, and next to him is a black tire. To the right of the Black man, there is a blue-and-white bicycle positioned upside down on the ground, accompanied by an orange-and-white traffic barrier.

**GPT Caption (before edit):**

> From a high, top-down perspective, a Black man with short hair lies on his back on a paved surface. He is wearing a black jacket over a blue and white patterned shirt, dark pants, and white sneakers with green accents. To his left, another Black man is seated on a black-and-red bicycle, with a black tire next to him. Near the first man's head, a dark-colored bicycle with a black bag attached to the back lies on its side. To his right, a blue-and-white bicycle is positioned upside down on the ground, accompanied by an orange-and-white traffic barrier. Near his feet, a BMX-style bike with a white frame and blue accents on the rims and handlebars also lies on its side on the pavement.

**Final Caption (after manual edit):**

> From a high, top-down perspective, a Black man with short hair lies on his back on a paved surface. He is wearing a black jacket over a blue and white patterned shirt, dark pants, and white sneakers with green accents. To his left, another Black man is seated on a black-and-red bicycle, with a black tire next to him. To the first man's right, a blue-and-white bicycle is positioned upside down on the ground, accompanied by an orange-and-white traffic barrier. Near his feet, a BMX-style bike with a white frame and blue accents on the rims and handlebars also lies on its side on the pavement.

**Diff:**

```diff
- Near the first man's head, a dark-colored bicycle with a black bag attached to the back lies on its side.
- To his right, a blue-and-white bicycle is positioned upside down on the ground, accompanied by an orange-and-white traffic barrier.
+ To the first man's right, a blue-and-white bicycle is positioned upside down on the ground, accompanied by an orange-and-white traffic barrier.
```

**Change Summary:** Removed: side., dark-colored, bag, attached, head,

---

### Case 46/70

| Field | Value |
|-------|-------|
| Video ID | `pGtjz4v0EE8.0.19.mp4` |
| Batch File | `1490_to_1500.json` |
| Batch Index | 6 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-17T02:18:47.912292 |

**Pre-Caption:**

> This is a static, top-down shot of an outdoor restaurant patio at night. A person walks past on the left side of the frame. The diners remain seated at their tables, with subtle movements as they eat, drink, and converse.

**Initial Feedback:**

> This is not a static shot, the camera is zooming out.
There are several people walking in the scene, not just one person.

**Final Feedback:**

> The shot is not static; the camera is zooming out. Additionally, there are multiple people walking in the scene, not just one.

**GPT Caption (before edit):**

> The camera is zooming out from a top-down view of an outdoor restaurant patio at night. Multiple people walk past on the left side of the frame. The diners remain seated at their tables, with subtle movements as they eat, drink, and converse.

**Final Caption (after manual edit):**

> The camera is zooming out from a top-down view of an outdoor restaurant patio at night. Multiple people walk past the frame. The diners remain seated at their tables, with subtle movements as they eat, drink, and converse.

**Diff:**

```diff
- Multiple people walk past on the left side of the frame.
+ Multiple people walk past the frame.
```

**Change Summary:** Removed: side, left, on

---

### Case 47/70

| Field | Value |
|-------|-------|
| Video ID | `HM5J6qAytJY.1.2.mp4` |
| Batch File | `1450_to_1460.json` |
| Batch Index | 7 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-10-12T02:38:39.466022 |

**Pre-Caption:**

> From a camera mounted on the hood of a moving blue sports car, a silver sports car appears from behind on the right. The silver car accelerates, overtakes the blue car, and continues to pull ahead as both vehicles drive forward on a paved surface. The two helmeted occupants inside the blue car remain seated throughout.

**Initial Feedback:**

> The silver car appears from behind on the right and is overtaken by the blue car.

**Final Feedback:**

> The silver car initially appears from behind on the right, accelerates, and overtakes the blue car.

**GPT Caption (before edit):**

> A silver sports car emerges from behind on the right of a moving blue sports car, accelerates, and overtakes it, continuing to pull ahead as both vehicles drive forward on a paved surface. The two helmeted occupants inside the blue car remain seated throughout.

**Final Caption (after manual edit):**

> A silver sports car emerges from behind on the right of a moving blue sports car, the blue car then overtakes the silver car, continuing to pull ahead as both vehicles drive forward on a paved surface. The two helmeted occupants inside the blue car remain seated throughout.

**Diff:**

```diff
- A silver sports car emerges from behind on the right of a moving blue sports car, accelerates, and overtakes it, continuing to pull ahead as both vehicles drive forward on a paved surface.
+ A silver sports car emerges from behind on the right of a moving blue sports car, the blue car then overtakes the silver car, continuing to pull ahead as both vehicles drive forward on a paved surface.
```

**Change Summary:** Added: then; Removed: accelerates,, it,, and

---

### Case 48/70

| Field | Value |
|-------|-------|
| Video ID | `IyTv_SR2uUo.2.0.mp4` |
| Batch File | `1430_to_1440.json` |
| Batch Index | 8 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-11T01:53:17.025678 |

**Pre-Caption:**

> This is a point-of-view shot from a camera mounted on a hammerhead shark, creating a wide shot of the underwater scene with a close-up of the shark's head. The dark, T-shaped head of the hammerhead is fixed in the foreground at the bottom center of the frame. The camera glides forward smoothly, showing the sandy ocean floor moving backward in the middle ground and background. In the background at the top right, another shark swims from right to left across the frame. A small, light-colored fish is also visible in the middle ground, swimming forward just above the hammerhead's head.

**Initial Feedback:**

> In the middle ground at the top right, another two  sharks swim from left to right across the frame.

In the background, several small fishes are swimming.

**Final Feedback:**

> In the middle ground at the top right, two additional sharks swim from left to right across the frame. In the background, several small fish are swimming.

**GPT Caption (before edit):**

> This is a point-of-view shot from a camera mounted on a hammerhead shark, creating a wide shot of the underwater scene with a close-up of the shark's head. The dark, T-shaped head of the hammerhead is fixed in the foreground at the bottom center of the frame. The camera glides forward smoothly, showing the sandy ocean floor moving backward in the middle ground and background. In the middle ground at the top right, two additional sharks swim from left to right across the frame. In the background, several small fish are swimming. A small, light-colored fish is also visible in the middle ground, swimming forward just above the hammerhead's head.

**Final Caption (after manual edit):**

> This is a point-of-view shot from a camera mounted on a hammerhead shark, creating a wide shot of the underwater scene with a close-up of the shark's head. The dark, T-shaped head of the hammerhead is fixed in the foreground at the bottom center of the frame. The camera glides forward smoothly, showing the sandy ocean floor moving backward in the middle ground and background. In the middle ground at the top right, two additional sharks swim from left to right across the frame. In the background, several small fish are swimming.

**Diff:**

```diff
- A small, light-colored fish is also visible in the middle ground, swimming forward just above the hammerhead's head.
```

**Change Summary:** Removed: just, also, small,, hammerhead's, visible, above, swimming, ground,, light-colored

---

### Case 49/70

| Field | Value |
|-------|-------|
| Video ID | `IyTv_SR2uUo.2.0.mp4` |
| Batch File | `1430_to_1440.json` |
| Batch Index | 8 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-11T01:48:27.263497 |

**Pre-Caption:**

> From a perspective just behind its head, a hammerhead shark swims steadily forward over a sandy ocean floor. In the background, another shark swims from the right side of the frame to the left.

**Initial Feedback:**

> In the middle ground, another two sharks swims from the right side of the frame to the right, not in the background.In the background, there are several fishes swimming.

**Final Feedback:**

> In the middle ground, two additional sharks swim from the right side of the frame to the right, not in the background. In the background, several fish can be seen swimming.

**GPT Caption (before edit):**

> From a perspective just behind its head, a hammerhead shark swims steadily forward over a sandy ocean floor. In the middle ground, two additional sharks swim from the right side of the frame to the left. In the background, several fish can be seen swimming.

**Final Caption (after manual edit):**

> From a perspective just behind its head, a hammerhead shark swims steadily forward over a sandy ocean floor. In the middle ground, two additional sharks swim from the right side of the frame to the right. In the background, several fish can be seen swimming.

**Diff:**

```diff
- In the middle ground, two additional sharks swim from the right side of the frame to the left.
+ In the middle ground, two additional sharks swim from the right side of the frame to the right.
```

**Change Summary:** Added: right.; Removed: left.

---

### Case 50/70

| Field | Value |
|-------|-------|
| Video ID | `pGtjz4v0EE8.0.11.mp4` |
| Batch File | `1430_to_1440.json` |
| Batch Index | 2 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-10-10T22:57:56.758439 |

**Pre-Caption:**

> This scenery shot begins as a high-angle wide shot, with a yellow water taxi moving from the bottom left towards the right in the middle ground. The canal's water fills the lower two-thirds of the frame, with several wooden posts also in the middle ground. A waterfront walkway and buildings occupy the background at the top of the frame. The camera then zooms out to an extreme wide shot, causing the elements to appear smaller and revealing more of the surrounding buildings and another section of the canal in the background.

**Initial Feedback:**

> The canal's water fills the lower one-seconds of the frame, while a waterfront walkway and buildings are situated in the middle ground, occupying one-fourths of the frame above the water part. The yellow water taxi moves from the bottom left towards the right in the middle ground.

**Final Feedback:**

> The canal's water fills the lower half of the frame, while a waterfront walkway and buildings are situated in the middle ground, occupying one-fourths of the frame above the water part. The yellow water taxi moves from the bottom left towards the right in the middle ground.

**GPT Caption (before edit):**

> The canal's water occupies the lower two-thirds of the frame, with several wooden posts in the middle ground. A yellow water taxi moves from the bottom left towards the right in this area. In the background at the top of the frame, a waterfront walkway and buildings are visible. The camera then zooms out to an extreme wide shot, making the elements appear smaller and revealing more of the surrounding buildings and another section of the canal in the background.

**Final Caption (after manual edit):**

> The canal's water occupies the lower half of the frame, with several wooden posts visible in the middle ground. A yellow water taxi moves from the bottom left towards the left within this area. In the middle ground, occupying the top one-fourth of the frame above the water, a waterfront walkway and buildings are visible. The camera then zooms out and slightly zoom in to an extreme wide shot, making the elements appear smaller and revealing more of the surrounding buildings and another section of the canal in the background.

**Diff:**

```diff
- The canal's water occupies the lower two-thirds of the frame, with several wooden posts in the middle ground.
- A yellow water taxi moves from the bottom left towards the right in this area.
- In the background at the top of the frame, a waterfront walkway and buildings are visible.
- The camera then zooms out to an extreme wide shot, making the elements appear smaller and revealing more of the surrounding buildings and another section of the canal in the background.
+ The canal's water occupies the lower half of the frame, with several wooden posts visible in the middle ground.
+ A yellow water taxi moves from the bottom left towards the left within this area.
+ In the middle ground, occupying the top one-fourth of the frame above the water, a waterfront walkway and buildings are visible.
+ The camera then zooms out and slightly zoom in to an extreme wide shot, making the elements appear smaller and revealing more of the surrounding buildings and another section of the canal in the background.
```

**Change Summary:** Added: frame, half, one-fourth, visible, above, ground,, zoom, occupying, water,, slightly; Removed: two-thirds, at, right, background

---

### Case 51/70

| Field | Value |
|-------|-------|
| Video ID | `pGtjz4v0EE8.0.11.mp4` |
| Batch File | `1430_to_1440.json` |
| Batch Index | 2 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-10-10T22:51:24.253314 |

**Pre-Caption:**

> From a high-angle, observational perspective, a yellow and white water taxi travels across a wide canal of blue-green water, creating a small wake. Several clusters of weathered wooden posts stand in the water. In the background, a stone waterfront lines the canal, with a light-colored building set behind it. A few people are visible walking along the waterfront during the daytime.

**Initial Feedback:**

> As the camera zooms out, a variety of buildings along the riverbank become visible in the middle ground. Behind it, there is not just one light-colored building — the riverbank is densely lined with numerous buildings.
 In the background, another section of the river and more buildings are also revealed.

**Final Feedback:**

> As the camera zooms out, a diverse array of buildings along the riverbank becomes visible in the middle ground. Contrary to the initial description, the riverbank is densely lined with numerous buildings, not just a single light-colored one. Additionally, in the background, another section of the river and more buildings are revealed.

**GPT Caption (before edit):**

> From a high-angle, observational perspective, a yellow and white water taxi travels across a wide canal of blue-green water, creating a small wake. Several clusters of weathered wooden posts stand in the water. As the camera zooms out, a diverse array of buildings densely lines the riverbank in the middle ground, contrary to the initial description of a single light-colored building. In the background, another section of the river and more buildings are revealed, with a few people visible walking along the waterfront during the daytime.

**Final Caption (after manual edit):**

> From a high-angle, observational perspective, a yellow and white water taxi travels across a wide canal of blue-green water, creating a small wake. Several clusters of weathered wooden posts stand in the water. As the camera zooms out, a diverse array of buildings densely lines the riverbank in the middle ground, with a few people visible walking along the waterfront during the daytime. In the background, another section of the river and more buildings are revealed.

**Diff:**

```diff
- As the camera zooms out, a diverse array of buildings densely lines the riverbank in the middle ground, contrary to the initial description of a single light-colored building.
- In the background, another section of the river and more buildings are revealed, with a few people visible walking along the waterfront during the daytime.
+ As the camera zooms out, a diverse array of buildings densely lines the riverbank in the middle ground, with a few people visible walking along the waterfront during the daytime.
+ In the background, another section of the river and more buildings are revealed.
```

**Change Summary:** Added: revealed.; Removed: single, light-colored, description, revealed,, building., initial, contrary, to

---

### Case 52/70

| Field | Value |
|-------|-------|
| Video ID | `BNzc6hG3yN4.0.4.mp4` |
| Batch File | `1410_to_1420.json` |
| Batch Index | 5 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-10-07T04:53:36.838208 |

**Pre-Caption:**

> The camera begins at a low angle, focused on a group of men standing together in a paved lot, and then rapidly ascends to a high, top-down perspective, revealing the men remaining largely stationary below.

**Initial Feedback:**

> The camera starts at a level angle, then smoothly cranes upward, creating a vertical arc around the group. It rises to an overhead, bird's-eye view before descending back to their height, capturing an upside-down high angle.

**Final Feedback:**

> The camera initially starts at a level angle and then smoothly moves upward, creating a vertical arc around the group. It ascends to an overhead, bird's-eye view before descending back to their level, capturing an inverted high angle.

**GPT Caption (before edit):**

> The camera starts at a low angle, smoothly moving upward in a vertical arc around a group of men standing in a paved lot. It ascends to an overhead, bird's-eye view before descending back to their level, capturing an inverted high angle.

**Final Caption (after manual edit):**

> The camera starts at a level angle, smoothly moving upward in a vertical arc around a group of men standing in a paved lot. It ascends to an overhead, bird's-eye view before descending back to their level, capturing an inverted high angle.

**Diff:**

```diff
- The camera starts at a low angle, smoothly moving upward in a vertical arc around a group of men standing in a paved lot.
+ The camera starts at a level angle, smoothly moving upward in a vertical arc around a group of men standing in a paved lot.
```

**Change Summary:** Added: level; Removed: low

---

### Case 53/70

| Field | Value |
|-------|-------|
| Video ID | `jVtnuLL2Kqs.0.16.mp4` |
| Batch File | `1370_to_1380.json` |
| Batch Index | 0 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-10-03T02:28:08.794765 |

**Pre-Caption:**

> This video is a scenery shot of a classical-style building. The scene begins with a low-angle close-up on the molded base of a large stone column, which is positioned in the foreground and center of the frame. The building's curved wall is in the middle ground, while a city street is visible in the background on the right. The camera then pulls back, pans left, and tilts up with a counter-clockwise rotation, transitioning into a wide, low-angle shot of the building's entrance. In the final composition, a broad set of stone steps occupies the foreground and bottom of the frame, leading up to the columns and building facade in the middle ground. A white logo is consistently positioned in the bottom right corner.

**Initial Feedback:**

> This is not a low-angle shot,but level angle.

This is not a close-up shot, but a wide shot.

There is no panning left and tilting up.

The stone steps are in the middle ground, not foreground.The fence is in the foreground.

**Final Feedback:**

> The video does not feature a low-angle shot; instead, it presents a level-angle perspective.

The initial shot is not a close-up but rather a wide shot.

There is no panning left or tilting up in the video.

The stone steps are situated in the middle ground, while the fence occupies the foreground.

**GPT Caption (before edit):**

> This video showcases a classical-style building. The scene begins with a level-angle wide shot of a large stone column, positioned in the foreground and center of the frame. The building's curved wall is in the middle ground, with a city street visible in the background on the right. The camera transitions into a wide shot of the building's entrance. In the final composition, a fence occupies the foreground, while a broad set of stone steps leads up to the columns and building facade in the middle ground. A white logo is consistently positioned in the bottom right corner.

**Final Caption (after manual edit):**

> This video showcases a classical-style building. The scene begins with a level-angle wide shot of a large stone column, positioned in the foreground and center of the frame. The building's curved wall is in the middle ground, with a city street visible in the background on the right. The camera transitions into a wide shot of the building's entrance. In the final composition, a fence occupies the foreground, while a broad set of stone steps leads up to the columns and building facade,they are all in the middle ground. A white logo is consistently positioned in the bottom right corner.

**Diff:**

```diff
- In the final composition, a fence occupies the foreground, while a broad set of stone steps leads up to the columns and building facade in the middle ground.
+ In the final composition, a fence occupies the foreground, while a broad set of stone steps leads up to the columns and building facade,they are all in the middle ground.
```

**Change Summary:** Added: all, facade,they, are; Removed: facade

---

### Case 54/70

| Field | Value |
|-------|-------|
| Video ID | `2WL4mIV48FA.0.3.mp4` |
| Batch File | `1340_to_1350.json` |
| Batch Index | 1 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-28T02:39:00.679479 |

**Pre-Caption:**

> From a camera mounted above the driver of a blue race car, the vehicle and driver occupy the foreground and lower half of the frame. Initially, a green race car is positioned in the middle ground on the right. The asphalt track extends from the foreground into the background, where green, rolling hills are visible across the scene. A small white building is situated in the background on the left, and a single orange cone briefly appears in the foreground on the left. As the blue car moves forward, it overtakes the green car, which shifts from the middle ground right to the background right before exiting the frame. The orange cone also quickly moves past and out of the frame on the left.

**Initial Feedback:**

> The camera is locked on the race car, not the driver. The car navigates past two sets of obstacles on the left side, each consisting of three cones.

**Final Feedback:**

> The camera is focused on the race car rather than the driver. The car maneuvers past two sets of obstacles on the left side, each consisting of three cones.

**GPT Caption (before edit):**

> From a camera mounted above the blue race car, the vehicle occupies the foreground and lower half of the frame, with the focus on the car itself rather than the driver. Initially, a green race car is positioned in the middle ground on the right. The asphalt track extends from the foreground into the background, where green, rolling hills are visible across the scene. A small white building is situated in the background on the left. As the blue car moves forward, it maneuvers past two sets of obstacles on the left side, each consisting of three orange cones, before overtaking the green car, which shifts from the middle ground right to the background right before exiting the frame.

**Final Caption (after manual edit):**

> From a camera mounted above the blue race car, the vehicle occupies the foreground and lower half of the frame, with the focus on the car itself rather than the driver. Initially, a green race car is positioned in the middle ground on the right. The asphalt track extends from the foreground into the background, where green, rolling hills are visible across the scene. A small white building is situated in the background on the left. As the blue car moves forward, it maneuvers past two sets of obstacles on the left side, each consisting of three orange cones, during which it overtakes the green car, which shifts from the middle ground right to the foreground right before exiting the frame.

**Diff:**

```diff
- As the blue car moves forward, it maneuvers past two sets of obstacles on the left side, each consisting of three orange cones, before overtaking the green car, which shifts from the middle ground right to the background right before exiting the frame.
+ As the blue car moves forward, it maneuvers past two sets of obstacles on the left side, each consisting of three orange cones, during which it overtakes the green car, which shifts from the middle ground right to the foreground right before exiting the frame.
```

**Change Summary:** Added: during, overtakes; Removed: overtaking

---

### Case 55/70

| Field | Value |
|-------|-------|
| Video ID | `2WL4mIV48FA.0.3.mp4` |
| Batch File | `1340_to_1350.json` |
| Batch Index | 1 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-28T02:29:58.354909 |

**Pre-Caption:**

> From a first-person perspective, a blue open-wheel race car accelerates on a racetrack, following a green sports prototype car through a left-hand turn. As the track straightens, the blue car pulls up on the left side of the green car and successfully overtakes it. The blue car then continues to drive straight down the track, leaving the green car behind.

**Initial Feedback:**

> This is not a first-person perspective but a locked-on perspective.
There is not a turn,the blue car overtakes the green car on a straight.

**Final Feedback:**

> The video does not depict a first-person perspective; instead, it shows a fixed or locked-on perspective. Additionally, the blue car overtakes the green car on a straight section of the track, not during a turn.

**GPT Caption (before edit):**

> From a fixed perspective, a blue open-wheel race car accelerates on a racetrack, following a green sports prototype car through a left-hand turn. As the track straightens, the blue car pulls up on the left side of the green car and successfully overtakes it on the straight section. The blue car then continues to drive straight down the track, leaving the green car behind.

**Final Caption (after manual edit):**

> From a locked-on perspective, a blue open-wheel race car accelerates on a racetrack, following a green sports prototype car through a left-hand turn. As the track straightens, the blue car pulls up on the left side of the green car and successfully overtakes it on the straight section. The blue car then continues to drive straight down the track, leaving the green car behind.

**Diff:**

```diff
- From a fixed perspective, a blue open-wheel race car accelerates on a racetrack, following a green sports prototype car through a left-hand turn.
+ From a locked-on perspective, a blue open-wheel race car accelerates on a racetrack, following a green sports prototype car through a left-hand turn.
```

**Change Summary:** Added: locked-on; Removed: fixed

---

### Case 56/70

| Field | Value |
|-------|-------|
| Video ID | `2WL4mIV48FA.0.3.mp4` |
| Batch File | `1340_to_1350.json` |
| Batch Index | 1 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-28T02:24:27.949854 |

**Pre-Caption:**

> This is a first-person view from a bright blue, open-wheel formula-style race car that occupies the lower portion of the view. The car has a white "GoPro" logo on its nose cone. Inside the cockpit, a driver is visible, wearing a white racing suit with red accents, black gloves, and a black helmet, with their hands on the steering wheel. A second race car, a lime green and black sports prototype with a large rear wing and the number "98" on its side, is seen on the right. The blue car overtakes the green car on a turn, and the green car subsequently moves out of view.

**Initial Feedback:**

> This is not a first-person view, the camera is attached to a blue racing car, so this is a locked-on point of view.There is no turn, the blue car overtakes the green car on a straight.

**Final Feedback:**

> The video does not depict a first-person view; rather, the camera is mounted on the blue racing car, providing a locked-on perspective. Additionally, the blue car overtakes the green car on a straight section of the track, not during a turn.

**GPT Caption (before edit):**

> The video shows a fixed perspective from a camera mounted on a bright blue, open-wheel formula-style race car, which occupies the lower portion of the view. The car features a white "GoPro" logo on its nose cone. Inside the cockpit, a driver is visible, wearing a white racing suit with red accents, black gloves, and a black helmet, with their hands on the steering wheel. A second race car, a lime green and black sports prototype with a large rear wing and the number "98" on its side, is seen on the right. The blue car overtakes the green car on a straight section of the track, and the green car subsequently moves out of view.

**Final Caption (after manual edit):**

> The video shows a locked-on perspective from a camera mounted on a bright blue, open-wheel formula-style race car, which occupies the lower portion of the view. The car features a white "GoPro" logo on its nose cone. Inside the cockpit, a driver is visible, wearing a white racing suit with red accents, black gloves, and a black helmet, with their hands on the steering wheel. A second race car, a lime green and black sports prototype with a large rear wing and the number "98" on its side, is seen on the right. The blue car overtakes the green car on a straight section of the track, and the green car subsequently moves out of view.

**Diff:**

```diff
- The video shows a fixed perspective from a camera mounted on a bright blue, open-wheel formula-style race car, which occupies the lower portion of the view.
+ The video shows a locked-on perspective from a camera mounted on a bright blue, open-wheel formula-style race car, which occupies the lower portion of the view.
```

**Change Summary:** Added: locked-on; Removed: fixed

---

### Case 57/70

| Field | Value |
|-------|-------|
| Video ID | `IyTv_SR2uUo.1.11.mp4` |
| Batch File | `1330_to_1340.json` |
| Batch Index | 5 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-09-27T03:03:13.533503 |

**Pre-Caption:**

> A locked-on POV shot, where the camera is mounted to an object, provides a perspective looking straight down from high in the sky during a daytime freefall. The vast, arid landscape below is a patchwork of brown and tan rolling hills and valleys, with a winding dirt path or dry riverbed visible. From the bottom of the view, the camera-wearer's legs in light-colored pants and their harness are visible. Farther below, another person in a colorful jumpsuit is also in freefall against the expansive terrain.

**Initial Feedback:**

> This is not a locked-on POV but a first-person POV.The person mounting the camera is not descending.From the bottom of the view we can also see the helmet of the camera-wearer.

**Final Feedback:**

> The video does not depict a locked-on POV shot but rather a first-person POV. The individual with the camera is not descending. Additionally, the helmet of the camera-wearer is visible at the bottom of the view.

**GPT Caption (before edit):**

> A first-person POV shot captures a perspective looking straight down from high in the sky during a daytime scene. The vast, arid landscape below is a patchwork of brown and tan rolling hills and valleys, with a winding dirt path or dry riverbed visible. From the bottom of the view, the camera-wearer's helmet and legs in light-colored pants are visible. Farther below, another person in a colorful jumpsuit is seen against the expansive terrain.

**Final Caption (after manual edit):**

> A first-person POV shot captures a perspective looking straight down from high in the sky during a daytime scene. The vast, arid landscape below is a patchwork of brown and tan rolling hills and valleys, with a winding dirt path or dry riverbed visible. From the bottom of the view, the camera-wearer's black helmet and legs in light-colored pants are visible. Farther below, another person in a colorful jumpsuit is seen against the expansive terrain.

**Diff:**

```diff
- From the bottom of the view, the camera-wearer's helmet and legs in light-colored pants are visible.
+ From the bottom of the view, the camera-wearer's black helmet and legs in light-colored pants are visible.
```

**Change Summary:** Added: black

---

### Case 58/70

| Field | Value |
|-------|-------|
| Video ID | `IyTv_SR2uUo.1.11.mp4` |
| Batch File | `1330_to_1340.json` |
| Batch Index | 5 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-27T02:54:45.762139 |

**Pre-Caption:**

> From a first-person perspective, a skydiver falls through the air while looking down at another skydiver below. The lower skydiver, initially in a stable freefall position, flips over onto their back to face the camera and raises both hands. The skydiver filming then extends their legs outward as both individuals continue their rapid descent toward the hilly terrain.

**Initial Feedback:**

> The skydiver below initially faces the camera and raises both middle fingers before turning away. The lower skydiver is decending, while the other remains the same height.

**Final Feedback:**

> The skydiver below initially faces the camera and raises both middle fingers before turning away. While the lower skydiver continues to descend, the filming skydiver maintains their altitude.

**GPT Caption (before edit):**

> From a first-person perspective, a skydiver falls through the air while looking down at another skydiver below. The lower skydiver, initially facing the camera, raises both middle fingers before turning away. As the lower skydiver continues their descent, the filming skydiver maintains their altitude, extending their legs outward as they both move toward the hilly terrain.

**Final Caption (after manual edit):**

> From a first-person perspective, a skydiver falls through the air while looking down at another skydiver below. The lower skydiver, initially facing the camera, raises both middle fingers before turning away. As the lower skydiver continues their descent, the filming skydiver maintains their altitude, extending their legs outward.

**Diff:**

```diff
- As the lower skydiver continues their descent, the filming skydiver maintains their altitude, extending their legs outward as they both move toward the hilly terrain.
+ As the lower skydiver continues their descent, the filming skydiver maintains their altitude, extending their legs outward.
```

**Change Summary:** Added: outward.; Removed: hilly, they, toward, outward, move, terrain.

---

### Case 59/70

| Field | Value |
|-------|-------|
| Video ID | `xhrAGJviQJA.1.7.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 9 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-09-25T06:39:45.007497 |

**Pre-Caption:**

> An East Asian man with short, dark hair and a broad smile wears a white t-shirt and a black shoulder carrier. He is carrying a young East Asian girl on his shoulders. The girl, who has dark, shoulder-length hair with bangs and is dressed in a light-colored sleeveless top, also smiles joyfully with her arms outstretched as she looks up.

**Initial Feedback:**

> There is no black shoulder carrier, that is the legs of the girl.

**Final Feedback:**

> The description mistakenly identifies a black shoulder carrier, which is actually the legs of the young girl being carried.

**GPT Caption (before edit):**

> An East Asian man with short, dark hair and a broad smile wears a white t-shirt. He is carrying a young East Asian girl on his shoulders. The girl, who has dark, shoulder-length hair with bangs and is dressed in a light-colored sleeveless top, also smiles joyfully with her arms outstretched as she looks up.

**Final Caption (after manual edit):**

> An East Asian man with short, dark hair and a broad smile wears a white t-shirt. He is carrying a young East Asian girl on his shoulders. The girl, who has dark, shoulder-length hair with bangs and is dressed in a light-colored sleeveless top and black trousers, also smiles joyfully with her arms outstretched as she looks up.

**Diff:**

```diff
- The girl, who has dark, shoulder-length hair with bangs and is dressed in a light-colored sleeveless top, also smiles joyfully with her arms outstretched as she looks up.
+ The girl, who has dark, shoulder-length hair with bangs and is dressed in a light-colored sleeveless top and black trousers, also smiles joyfully with her arms outstretched as she looks up.
```

**Change Summary:** Added: trousers,, black, top; Removed: top,

---

### Case 60/70

| Field | Value |
|-------|-------|
| Video ID | `2WL4mIV48FA.0.1.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 5 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-25T05:43:04.653761 |

**Pre-Caption:**

> From a high-angle, point-of-view perspective, the front half of a blue race car and its driver occupy the foreground in the bottom half of the frame. The driver's helmet is in the bottom center, with their hands on the steering wheel, and the car's nose cone extends towards the center. The front wheels are positioned on the bottom left and bottom right. The asphalt racetrack fills the middle of the frame, extending from the foreground into the middle ground as it curves to the right. In the background, a grassy landscape and rolling hills span the upper portion of the frame, with a cloudy sky positioned at the top. The entire scene moves as the car speeds forward, causing the track and scenery to rush towards the fixed camera.

**Initial Feedback:**

> The front of the car occupies the foreground and the middle ground.The wheels are positioned on the middle left and middle right,not bottom left and bottom right.

**Final Feedback:**

> The front of the car is prominently featured in both the foreground and middle ground. The wheels are actually positioned in the middle left and middle right, rather than the bottom left and bottom right as described.

**GPT Caption (before edit):**

> From a high-angle, point-of-view perspective, the front half of a blue race car and its driver occupy the foreground in the bottom half of the frame. The driver's helmet is in the bottom center, with their hands on the steering wheel, and the car's nose cone extends towards the center. The front wheels are positioned in the middle left and middle right. The asphalt racetrack fills the middle of the frame, extending from the foreground into the middle ground as it curves to the right. In the background, a grassy landscape and rolling hills span the upper portion of the frame, with a cloudy sky positioned at the top. The entire scene moves as the car speeds forward, causing the track and scenery to rush towards the fixed camera.

**Final Caption (after manual edit):**

> From a high-angle, point-of-view perspective, the front half of a blue race car and its driver occupy the foreground and middle ground in the bottom half of the frame. The driver's helmet is in the bottom center, with their hands on the steering wheel, and the car's nose cone extends towards the center. The front wheels are positioned in the middle left and middle right. The asphalt racetrack fills the middle of the frame, extending from the foreground into the middle ground as it curves to the right. In the background, a grassy landscape and rolling hills span the upper portion of the frame, with a cloudy sky positioned at the top. The entire scene moves as the car speeds forward, causing the track and scenery to rush towards the fixed camera.

**Diff:**

```diff
- From a high-angle, point-of-view perspective, the front half of a blue race car and its driver occupy the foreground in the bottom half of the frame.
+ From a high-angle, point-of-view perspective, the front half of a blue race car and its driver occupy the foreground and middle ground in the bottom half of the frame.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

### Case 61/70

| Field | Value |
|-------|-------|
| Video ID | `2WL4mIV48FA.0.1.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 5 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-09-25T05:34:19.724701 |

**Pre-Caption:**

> From an over-the-shoulder perspective, a driver is seated in the open cockpit of a bright cyan race car. The car, an open-wheel model, features the words "GoPro" and "Be a HERO." in white text on its nose cone, with its front wheels and suspension visible on either side. The driver, seen from the chest up, wears a black helmet that covers their head. Their arms are clad in a white and black patterned racing suit, and their hands are covered by black racing gloves with white and red details, including the "SPARCO" brand name.

**Initial Feedback:**

> The perspective is not over-the-shoulder; the camera is positioned slightly above the driver's head. The car is blue, not cyan. Additionally, the driver's legs, arms, and helmet are visible, not the "chest up"

**Final Feedback:**

> The perspective is not over-the-shoulder; the camera is positioned slightly above the driver's head. The car appears blue rather than cyan. Furthermore, the driver's legs, arms, and helmet are visible, not just from the chest up.

**GPT Caption (before edit):**

> From a slightly elevated perspective above the driver's head, a driver is seated in the open cockpit of a blue race car. The car, an open-wheel model, features the words "GoPro" and "Be a HERO." in white text on its nose cone, with its front wheels and suspension visible on either side. The driver, fully visible, wears a black helmet that covers their head. Their legs and arms are clad in a white and black patterned racing suit, and their hands are covered by black racing gloves with white and red details, including the "SPARCO" brand name.

**Final Caption (after manual edit):**

> From a slightly elevated perspective above the driver's head, a driver is seated in the open cockpit of a blue race car. The car, an open-wheel model, features the words "GoPro" and "Be a HERO." in white text on its nose cone, with its front wheels and suspension visible on either side. The driver wears a black helmet that covers their head. Their legs and arms are clad in a white and black patterned racing suit, and their hands are covered by black racing gloves with white and red details, including the "SPARCO" brand name.

**Diff:**

```diff
- The driver, fully visible, wears a black helmet that covers their head.
+ The driver wears a black helmet that covers their head.
```

**Change Summary:** Removed: driver,, visible,, fully

---

### Case 62/70

| Field | Value |
|-------|-------|
| Video ID | `b9-cHk-7N8k.0.3.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 3 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-25T05:03:29.907059 |

**Pre-Caption:**

> In a full shot, a surfer is positioned in the center of the frame and in the middle ground, standing on a surfboard that extends from the bottom of the frame into the foreground. The wave and its white spray are in the middle ground, flanking the surfer on the left and right. In the background, a shoreline is visible on the right side of the frame, with the sunset sky occupying the upper portion. The camera, positioned at the subject's level on the front of the board, remains fixed, causing the background shoreline to move from right to left as the surfer rides the wave.

**Initial Feedback:**

> The shoreline is moving from left to right.

The camera is not static,The camera is mounted on a surfboard, filming the surfer as they ride. It moves backward while trucking right and panning left. During this motion, it rolls slightly clockwise before rolling counterclockwise.

**Final Feedback:**

> The feedback regarding the shoreline movement is incorrect; the shoreline actually moves from left to right. The camera is not static; it is mounted on the surfboard, capturing the surfer's ride. As the camera moves backward, it simultaneously trucks right and pans left. During this motion, it also rolls slightly clockwise before rolling counterclockwise.

**GPT Caption (before edit):**

> In a full shot, a surfer is positioned in the center of the frame and in the middle ground, standing on a surfboard that extends from the bottom of the frame into the foreground. The wave and its white spray are in the middle ground, flanking the surfer on the left and right. In the background, a shoreline is visible on the right side of the frame, with the sunset sky occupying the upper portion. The camera, mounted on the surfboard, captures the surfer's ride as it moves backward, simultaneously trucking right and panning left. During this motion, the camera also rolls slightly clockwise before rolling counterclockwise, causing the background shoreline to move from right to left as the surfer rides the wave.

**Final Caption (after manual edit):**

> In a full shot, a surfer is positioned in the center of the frame and in the middle ground, standing on a surfboard that extends from the bottom of the frame into the foreground. The wave and its white spray are in the middle ground, flanking the surfer on the left and right. In the background, a shoreline is visible on the right side of the frame, with the sunset sky occupying the upper portion. The camera, mounted on the surfboard, captures the surfer's ride as it moves backward, simultaneously trucking right and panning left. During this motion, the camera also rolls slightly clockwise before rolling counterclockwise, causing the background shoreline to move from left to right as the surfer rides the wave.

**Diff:**

```diff
- During this motion, the camera also rolls slightly clockwise before rolling counterclockwise, causing the background shoreline to move from right to left as the surfer rides the wave.
+ During this motion, the camera also rolls slightly clockwise before rolling counterclockwise, causing the background shoreline to move from left to right as the surfer rides the wave.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

### Case 63/70

| Field | Value |
|-------|-------|
| Video ID | `W7S2LT1xay0.0.3.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 2 |
| Caption Type | scene |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-25T04:28:12.924133 |

**Pre-Caption:**

> A locked-on POV shot from inside a car captures the vehicle backing out of a garage at night. The camera, fixed in perspective looking out the passenger side, shows the white, paneled garage door and a brick wall moving past with motion blur. The car's black side mirror is prominent in the foreground, reflecting the dimly lit surroundings. A portion of the car's tan interior, including the dashboard and door, is visible on the right side of the view.

**Initial Feedback:**

> The video captures a stationary car with a camera mounted on the door, focusing on the side mirror,it is a locked-on point of view and is not inside the car. It shows the door being closed, providing a clear view of the car's interior and surroundings.

**Final Feedback:**

> The video effectively captures a stationary car with a camera mounted on the door. It presents a locked-on point of view. The footage clearly shows the door being closed, offering a detailed view of both the car's interior and its surroundings.

**GPT Caption (before edit):**

> A locked-on POV shot from outside a car captures the vehicle backing out of a garage at night. The camera, mounted on the door, focuses on the black side mirror, reflecting the dimly lit surroundings. The footage shows the white, paneled garage door and a brick wall moving past with motion blur. The car's tan interior, including the dashboard and door, is visible, and the video clearly shows the door being closed, offering a detailed view of both the car's interior and its surroundings.

**Final Caption (after manual edit):**

> A locked-on POV shot captures the static vehicle at night. The camera, mounted on the door, focuses on the black side mirror, reflecting the dimly lit surroundings. The footage shows the white, paneled garage door and a brick wall moving past with motion blur. The car's tan interior, including the dashboard and door, is visible, and the video clearly shows the door being closed, offering a detailed view of both the car's interior and its surroundings.

**Diff:**

```diff
- A locked-on POV shot from outside a car captures the vehicle backing out of a garage at night.
+ A locked-on POV shot captures the static vehicle at night.
```

**Change Summary:** Added: static; Removed: out, outside, from, car, backing

---

### Case 64/70

| Field | Value |
|-------|-------|
| Video ID | `vlDzYIIOYmM.0.0.mp4` |
| Batch File | `1320_to_1330.json` |
| Batch Index | 1 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-25T03:53:47.529337 |

**Pre-Caption:**

> This is a still image with no movement. A woman, a man, and a young girl are stationary in a field of tall grass.

**Initial Feedback:**

> This is not a still image.Held by a woman, the camera moves backward continuously, tracking three people walking through the grass from the front.They are not stationary, the man is holding the young girl,walking forward with the woman.

**Final Feedback:**

> The video is not a still image as described. The camera, held by a woman, moves backward continuously, capturing three people walking through the tall grass. Contrary to the caption, they are not stationary; the man is holding the young girl while walking forward alongside the woman.

**GPT Caption (before edit):**

> A woman holds a camera and moves backward, capturing a man holding a young girl as they walk forward together through a field of tall grass.

**Final Caption (after manual edit):**

> A woman holds a camera which is moving backward, capturing a man holding a young girl as they walk forward together through a field of tall grass.

**Diff:**

```diff
- A woman holds a camera and moves backward
+ A woman holds a camera which is moving backward
```

**Change Summary:** Added: is, moving, which; Removed: moves, and

---

### Case 65/70

| Field | Value |
|-------|-------|
| Video ID | `oagszCmJLpU.3.8.mp4` |
| Batch File | `1290_to_1300.json` |
| Batch Index | 6 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 4 |
| Timestamp | 2025-09-24T01:37:32.680774 |

**Pre-Caption:**

> This extreme wide shot focuses on a vast scenery, with no single main subject. A massive, dark storm cloud formation dominates the top, center, and right portions of the frame, while a smaller patch of white clouds and blue sky is visible in the top left. The foreground and middle ground consist of a flat plain occupying the bottom third of the frame. Along the horizon at the bottom, a band of golden light is visible, with shafts of light or rain descending from the cloud base in the bottom center. In this time-lapse, the dark clouds swirl and expand, moving from the top left towards the center and right, gradually obscuring the blue sky and appearing to advance towards the low-angle camera.

**Initial Feedback:**

> The movement of the clouds is irregular and difficult to describe.

**Final Feedback:**

> The cloud movement in the video appears erratic and challenging to articulate clearly.

**GPT Caption (before edit):**

> This extreme wide shot captures a dynamic and vast scenery without a single main subject. A massive, dark storm cloud formation dominates the top, center, and right portions of the frame, while a smaller patch of white clouds and blue sky is visible in the top left. The foreground and middle ground consist of a flat plain occupying the bottom third of the frame. Along the horizon at the bottom, a band of golden light is visible, with shafts of light or rain descending from the cloud base in the bottom center. In this time-lapse, the dark clouds swirl unpredictably and expand, moving erratically from the top left towards the center and right, gradually obscuring the blue sky and appearing to advance towards the low-angle camera.

**Final Caption (after manual edit):**

> This extreme wide shot captures a dynamic and vast scenery without a single main subject. A massive, dark storm cloud formation dominates the top, center, and right portions of the frame, while a smaller patch of white clouds and blue sky is visible in the top left. The foreground and middle ground consist of a flat plain occupying the bottom third of the frame. Along the horizon at the bottom, a band of golden light is visible, with shafts of light or rain descending from the cloud base in the bottom center. In this time-lapse, the dark clouds swirl unpredictably and expand, the movement is irregular and difficult to describe.

**Diff:**

```diff
- In this time-lapse, the dark clouds swirl unpredictably and expand, moving erratically from the top left towards the center and right, gradually obscuring the blue sky and appearing to advance towards the low-angle camera.
+ In this time-lapse, the dark clouds swirl unpredictably and expand, the movement is irregular and difficult to describe.
```

**Change Summary:** Added: difficult, irregular, describe., movement; Removed: advance, camera., center, moving, towards, appearing, right,, left, erratically, low-angle

---

### Case 66/70

| Field | Value |
|-------|-------|
| Video ID | `HM5J6qAytJY.0.0.mp4` |
| Batch File | `1260_to_1270.json` |
| Batch Index | 3 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-09-23T01:35:39.359066 |

**Pre-Caption:**

> In a split composition, the right half of the frame is filled by a close-up of a car in the foreground, while the left half presents a wide shot of the scenery. The car's front passenger wheel spins rapidly in the center-right foreground, with the vehicle's body extending to the top and right edges of the frame. On the left, a flat, dark ground surface occupies the foreground and middle ground, receding toward a distant mountain range in the background at the horizon. The clear sky fills the top left portion of the frame. The camera is positioned at a low angle, level with the car's wheel, and moves in unison with the vehicle, keeping the car static in the frame while the background scenery rushes past from left to right.

**Initial Feedback:**

> The car is prominently featured in the foreground, while the dark ground surface extends across the foreground, middle ground, and background. The camera is positioned at a level angle, not low angle.

**Final Feedback:**

> The car is prominently featured in the foreground, with the dark ground surface extending across the foreground, middle ground, and background. The camera is positioned at a level angle, rather than a low angle.

**GPT Caption (before edit):**

> The right half of the frame is dominated by a close-up of a car in the foreground, with its front passenger wheel spinning rapidly in the center-right. The vehicle's body extends to the top and right edges of the frame. On the left, a flat, dark ground surface stretches across the foreground, middle ground, and background, leading to a distant mountain range at the horizon. The clear sky fills the top left portion of the frame. The camera is positioned at a level angle, moving in unison with the vehicle to keep the car static in the frame while the background scenery rushes past from left to right.

**Final Caption (after manual edit):**

> The right half of the frame is dominated by a close-up of a car in the foreground, with its front passenger wheel spinning rapidly in the center-right. The vehicle's body extends to the top and right edges of the frame. On the left, a flat, dark ground surface stretches across the foreground, middle ground, and background, leading to a distant mountain range at the horizon. The clear sky fills the top left portion of the frame. The camera is positioned at a level angle, moving in unison with the vehicle to keep the car static in the frame while the scenery rushes past from left to right.

**Diff:**

```diff
- The camera is positioned at a level angle, moving in unison with the vehicle to keep the car static in the frame while the background scenery rushes past from left to right.
+ The camera is positioned at a level angle, moving in unison with the vehicle to keep the car static in the frame while the scenery rushes past from left to right.
```

**Change Summary:** Removed: background

---

### Case 67/70

| Field | Value |
|-------|-------|
| Video ID | `yIxnb1SaT14.0.3.mp4` |
| Batch File | `1260_to_1270.json` |
| Batch Index | 1 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-22T23:12:31.018164 |

**Pre-Caption:**

> This is a wide, static scenery shot. A large, golden-bronze statue occupies the foreground, positioned across the bottom half of the frame from the left towards the center. In the middle ground, the Seine River flows horizontally across the scene, with other bridges and city lights visible along its banks. The illuminated Eiffel Tower is centered in the background, rising above the cityscape. The camera is positioned at a high angle relative to the river below but at a similar height to the foreground statue. A text overlay is fixed in the bottom right corner of the frame. The shot remains stationary throughout.

**Initial Feedback:**

> This is not a static shot.The camera shows some minor movement. The camera is zooming in and rolling clockwise.

The camera is not positioned at a high angle,but a level angle.

**Final Feedback:**

> The shot is not entirely static; there is minor camera movement, including zooming in and a clockwise roll. Additionally, the camera is positioned at a level angle rather than a high angle.

**GPT Caption (before edit):**

> This is a wide scenery shot with minor camera movement, including zooming in and a slight clockwise roll. A large, golden-bronze statue occupies the foreground, positioned across the bottom half of the frame from the left towards the center. In the middle ground, the Seine River flows horizontally across the scene, with other bridges and city lights visible along its banks. The illuminated Eiffel Tower is centered in the background, rising above the cityscape. The camera is positioned at a level angle relative to the river and the foreground statue. A text overlay is fixed in the bottom right corner of the frame.

**Final Caption (after manual edit):**

> This is a wide scenery shot with minor camera movement, including zooming in and a slight clockwise roll. A large, golden-bronze statue occupies the foreground, positioned across the bottom half of the frame from the left towards the center. In the middle ground, the Seine River flows horizontally across the scene, with other bridges and city lights visible along its banks. The illuminated Eiffel Tower is centered in the background, rising above the cityscape. The camera is positioned at a level angle relative to the scene. A text overlay is fixed in the bottom right corner of the frame.

**Diff:**

```diff
- The camera is positioned at a level angle relative to the river and the foreground statue.
+ The camera is positioned at a level angle relative to the scene.
```

**Change Summary:** Added: scene.; Removed: foreground, statue.

---

### Case 68/70

| Field | Value |
|-------|-------|
| Video ID | `-2uIa-XMJC0.2.2.mp4` |
| Batch File | `1260_to_1270.json` |
| Batch Index | 2 |
| Caption Type | motion |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-22T22:59:51.002265 |

**Pre-Caption:**

> A hand reaches into the frame from the left and presses a blue button on a smart lock before retracting out of view. In response, a light at the top of the device illuminates, and a semi-transparent, holographic projection of a man materializes on the door. The projected man remains stationary in profile.

**Initial Feedback:**

> "A hand reaches into the frame from the left" change left to right.

The man is not static,He then turns his head to look at the dark rectangular object in my right hand, speaking as he does so.

**Final Feedback:**

> Please change "A hand reaches into the frame from the left" to "A hand reaches into the frame from the right."

Additionally, the man is not stationary. He turns his head to look at the dark rectangular object in my right hand and speaks as he does so.

**GPT Caption (before edit):**

> A hand reaches into the frame from the right and presses a blue button on a smart lock before retracting out of view. In response, a light at the top of the device illuminates, and a semi-transparent, holographic projection of a man materializes on the door. The projected man turns his head to look at the dark rectangular object in my right hand and speaks as he does so.

**Final Caption (after manual edit):**

> A hand reaches into the frame from the right and presses a blue button on a smart lock before retracting out of view. In response, a light at the top of the device illuminates, and a semi-transparent, holographic projection of a man materializes on the door. The projected man turns his head to look at the dark rectangular object in his right hand and speaks as he does so.

**Diff:**

```diff
- The projected man turns his head to look at the dark rectangular object in my right hand and speaks as he does so.
+ The projected man turns his head to look at the dark rectangular object in his right hand and speaks as he does so.
```

**Change Summary:** Removed: my

---

### Case 69/70

| Field | Value |
|-------|-------|
| Video ID | `hHG1wva1B0w.9.2.mp4` |
| Batch File | `1250_to_1260.json` |
| Batch Index | 8 |
| Caption Type | subject |
| Status | approved |
| Rating Score | 2 |
| Timestamp | 2025-09-22T22:10:03.544360 |

**Pre-Caption:**

> In a parking lot, a solid red, featureless human figure with a male build stands next to a row of older-model sedans. The figure is entirely monochromatic red, obscuring any clothing or facial details. It is positioned with its body slightly turned, holding its left arm with its right hand in a self-hugging gesture. To the figure's right, in the foreground, is the rear of a dark-colored sedan with its taillights illuminated, casting a bright glow. Next to the red figure is a pale green sedan, and two other dark-colored sedans are visible parked further down the row.

**Initial Feedback:**

> "holding its left arm with its right hand in a self-hugging gesture." is wrong,he is holding its right arm with its left hand in a self-hugging gesture.

Change"To the figure's right" to "To the figure's left".

In the foreground, the front of a white sedan is visible, with its headlights illuminated and shining brightly. Behind the white car is a dark black vehicle, and behind that is the pale green sedan.

**Final Feedback:**

> The description "holding its left arm with its right hand in a self-hugging gesture" is incorrect. The figure is actually holding its right arm with its left hand in a self-hugging gesture.

Additionally, the phrase "To the figure's right" should be changed to "To the figure's left."

In the foreground, the front of a white sedan is visible, with its headlights illuminated and shining brightly. Behind the white car is a dark black vehicle, and behind that is the pale green sedan.

**GPT Caption (before edit):**

> In a parking lot, a solid red, featureless human figure with a male build stands next to a row of older-model sedans. The figure is entirely monochromatic red, obscuring any clothing or facial details. It is positioned with its body slightly turned, holding its right arm with its left hand in a self-hugging gesture. To the figure's left, in the foreground, is the front of a white sedan with its headlights illuminated and shining brightly. Behind the white car is a dark black vehicle, and behind that is the pale green sedan.

**Final Caption (after manual edit):**

> In a parking lot, a solid red, featureless human figure with a male build stands next to a row of older-model sedans. The figure is entirely monochromatic red, obscuring any clothing or facial details. It is positioned with its body slightly turned, holding its right arm with its left hand in a self-hugging gesture. To the figure's left, in the foreground, is the front of a white sedan with its headlights illuminated and shining brightly. Behind the white car is a dark black vehicle, and behind that is the pale green sedan.and two other dark-colored sedans are visible parked further down the row.

**Diff:**

```diff
- Behind the white car is a dark black vehicle, and behind that is the pale green sedan.
+ Behind the white car is a dark black vehicle, and behind that is the pale green sedan.and two other dark-colored sedans are visible parked further down the row.
```

**Change Summary:** Added: parked, dark-colored, visible, row., two, are, down, further, sedans, other; Removed: sedan.

---

### Case 70/70

| Field | Value |
|-------|-------|
| Video ID | `ocLJWCnMhTo.2.3.mp4` |
| Batch File | `1250_to_1260.json` |
| Batch Index | 3 |
| Caption Type | spatial |
| Status | approved |
| Rating Score | 3 |
| Timestamp | 2025-09-22T12:18:12.799796 |

**Pre-Caption:**

> Initially, a medium shot frames the scene at the subjects' level, with a person in a white robe occupying the left-foreground, seen from behind. This person holds a child, who is positioned in the center-middle ground, while a man in a red shirt stands to the right in the middle ground. The camera then moves upward and tilts down, transitioning to a high-angle perspective. In this final composition, the person in the white robe is at the bottom of the frame in the foreground, the child is in the center-middle ground, and the man in red is at the top-right middle ground. This movement makes the black and white checkered floor a dominant element in the background, also revealing a small, clear table in the center-bottom middle ground.

**Initial Feedback:**

> “The camera then moves upward and tilts down, transitioning to a high-angle perspective.” is wrong, the camera cranes up,and finally transitioning to a bird's eye angle.

"and the man in red is at the top-right middle ground." is wrong,he is in the foreground and middle ground.

**Final Feedback:**

> The statement "The camera then moves upward and tilts down, transitioning to a high-angle perspective" is incorrect. The camera actually cranes up and transitions to a bird's eye view.

Additionally, the description "and the man in red is at the top-right middle ground" is inaccurate. He is positioned in both the foreground and middle ground.

**GPT Caption (before edit):**

> Initially, a medium shot frames the scene at the subjects' level, with a person in a white robe occupying the left-foreground, seen from behind. This person holds a child, who is positioned in the center-middle ground, while a man in a red shirt stands to the right in the middle ground. The camera then cranes upward, transitioning to a bird's eye view. In this final composition, the person in the white robe is at the bottom of the frame in the foreground, the child is in the center-middle ground, and the man in red spans both the foreground and middle ground. This movement makes the black and white checkered floor a dominant element in the background, also revealing a small, clear table in the center-bottom middle ground.

**Final Caption (after manual edit):**

> Initially, a medium shot frames the scene at the subjects' level, with a person in a white robe occupying the left-foreground, seen from behind. This person holds a child, who is positioned in the center-middle ground, while a man in a red shirt stands to the right in the middle ground. The camera then cranes upward, transitioning to a bird's eye view. In this final composition, the person in the white robe is at the bottom of the frame in the foreground, the child is in the foreground and middle ground, and the man in red spans both the foreground and middle ground. This movement makes the black and white checkered floor a dominant element in the background, also revealing a small, clear table in the center-bottom middle ground.

**Diff:**

```diff
- In this final composition, the person in the white robe is at the bottom of the frame in the foreground, the child is in the center-middle ground, and the man in red spans both the foreground and middle ground.
+ In this final composition, the person in the white robe is at the bottom of the frame in the foreground, the child is in the foreground and middle ground, and the man in red spans both the foreground and middle ground.
```

**Change Summary:** Minor changes (punctuation/formatting)

---

