# Shot_type Overview

<details>
<summary><h2>Is Human Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_human_shot</code>


<h3>📖 Definition:</h3>
Is the shot focused on human subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video primarily feature human subjects?

- Are people the main focus of this shot?

- Is this shot centered on human characters?

- Does the camera primarily follow human subjects?

- Are humans the principal subjects in this shot?

- Is the video's focus on human figures?

- Does this shot mainly capture human subjects?

- Are human subjects the primary focus of the camera?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that primarily focuses on human subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video centered on human subjects.

- A shot where people are the main focus.

- A video primarily featuring human figures.

- A shot focusing on human characters.

- A video where humans are the principal subjects.

- A shot emphasizing human subjects.

- A video capturing human-centered action.

- A shot predominantly featuring people.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_human_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_human_shot is False</code>

</details>

<details>
<summary><h2>Is Just Back And Forth Change Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_back_and_forth_change_shot</code>


<h3>📖 Definition:</h3>
Does the video have a clear subject with back-and-forth changes in shot size?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot size alternate between closer and farther views?

- Does the framing repeatedly shift between different sizes?

- Is there an oscillating pattern in the shot size?

- Does the framing alternate between different scales?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video has a clear subject with back-and-forth changes in shot size.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with oscillating shot sizes.

- A video featuring alternating frame scales.

- A shot with patterned size variations.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_back_and_forth_change_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_back_and_forth_change_shot is False</code>

</details>

<details>
<summary><h2>Is Just Change Of Subject Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_change_of_subject_shot</code>


<h3>📖 Definition:</h3>
The video includes a subject change, where a subject appears, disappears, or transitions to another.

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the shot show a transition between different subjects?

- Is there a clear change in the main subject during the video?

- Does the focus shift from one subject to another?

- Does the video show subjects appearing or disappearing?

- Is there a handoff between different subjects?

- Does the shot include subject transitions?

- Is there a change in what the camera focuses on?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video includes a subject change, where a subject appears in a revealing shot, disappears, or transitions to another.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing subject transitions.

- A shot with changing focal subjects.

- A video featuring subject appearances or disappearances.

- A shot demonstrating subject handoffs.

- A video with dynamic subject changes.

- A shot revealing new subjects.

- A video transitioning between subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_change_of_subject_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_change_of_subject_shot is False</code>

</details>

<details>
<summary><h2>Is Just Clear Subject Atypical Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_clear_subject_atypical_shot</code>


<h3>📖 Definition:</h3>
Is there a clear subject in the video, but its anatomy looks unnatural or exaggerated, as seen in games or CGI?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the subject have unusual or exaggerated proportions?

- Is the subject clearly visible but anatomically unrealistic?

- Does the video show a subject with non-standard features?

- Is there a distinct but anatomically unusual subject?

- Does the subject appear stylized or non-realistic?

- Is the main subject visibly different from natural anatomy?

- Does the video feature a subject with exaggerated features?

- Is there a clear but anatomically stylized subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot with a clear subject that has unnatural or exaggerated anatomy, typical in games or CGI.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video featuring an anatomically stylized subject.

- A shot showing a subject with exaggerated proportions.

- A video with a clear but unrealistic subject.

- A shot featuring subjects with non-standard anatomy.

- A video showing CGI-style subject features.

- A shot with an anatomically unusual subject.

- A video displaying stylized character proportions.

- A shot emphasizing non-realistic anatomy.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_clear_subject_atypical_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_clear_subject_atypical_shot is False</code>

</details>

<details>
<summary><h2>Is Just Clear Subject Dynamic Size Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_clear_subject_dynamic_size_shot</code>


<h3>📖 Definition:</h3>
Does the video feature a clear subject, but changes in framing make shot size classification tricky?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a distinct subject with varying frame sizes?

- Does the shot maintain a clear subject despite changing distances?

- Is the subject clear but shown at different scales?

- Does the framing change while following a clear subject?

- Is there dynamic framing of an identifiable subject?

- Does the shot size vary while tracking a clear subject?

- Is the subject consistent but shown at different sizes?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features a clear subject, but changes in framing make shot size classification tricky.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video showing a subject at varying distances.

- A shot with dynamic framing of a clear subject.

- A video maintaining subject focus despite size changes.

- A shot featuring variable distances to the subject.

- A video with changing shot sizes of a clear subject.

- A shot showing subject scale variations.

- A video with dynamic subject sizing.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_clear_subject_dynamic_size_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_clear_subject_dynamic_size_shot is False</code>

</details>

<details>
<summary><h2>Is Just Different Subject In Focus Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_different_subject_in_focus_shot</code>


<h3>📖 Definition:</h3>
Does the video feature different subjects, varying in type or size, making shot size classification difficult?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are various subjects brought into focus throughout the shot?

- Does the shot emphasize different subjects at different times?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- The video features different subjects (e.g., varying in type or size) in focus, making shot size classification difficult.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A shot alternating between different subjects.

- A video highlighting multiple subjects through focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_different_subject_in_focus_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_different_subject_in_focus_shot is False</code>

</details>

<details>
<summary><h2>Is Just Human Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_human_shot</code>


<h3>📖 Definition:</h3>
Does the video consistently feature one dominant human subject or a single group of human subjects in the frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a single human subject or group that dominates the frame?

- Does the shot maintain focus on one primary human subject?

- Is the video centered on a single human or human group?

- Does one human subject or group remain the main focus?

- Is there a consistent human subject throughout the shot?

- Does the camera stay focused on one human subject or group?

- Is there a single dominant human presence in the frame?

- Does the shot maintain emphasis on one human subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot consistently featuring either a single human subject or a single group of humans.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video focused on a single human subject.

- A shot maintaining focus on one human group.

- A video centered on a primary human subject.

- A shot emphasizing a single human presence.

- A video tracking one main human subject.

- A shot dedicated to a single human group.

- A video highlighting one human subject.

- A shot following a single human presence.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_human_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_human_shot is False</code>

</details>

<details>
<summary><h2>Is Just Many Subject No Focus Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_many_subject_no_focus_shot</code>


<h3>📖 Definition:</h3>
Does the video feature multiple subjects with no clear focus on any one subject?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there multiple subjects without a primary focus?

- Does the shot show several subjects of equal importance?

- Is there no dominant subject among multiple elements?

- Are various subjects shown without emphasizing any one?

- Does the shot maintain equal focus on multiple subjects?

- Is there an even distribution of focus among subjects?

- Does the video avoid emphasizing any particular subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot showing multiple subjects without emphasizing any single one as the main focus.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video with multiple equal-emphasis subjects.

- A video presenting multiple subjects equally.

- A shot featuring multiple subjects with no dominant focus.

- A video showing various subjects without a primary focus.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_many_subject_no_focus_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_many_subject_no_focus_shot is False</code>

</details>

<details>
<summary><h2>Is Just Many Subject One Focus Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_many_subject_one_focus_shot</code>


<h3>📖 Definition:</h3>
Does the video feature multiple subjects, but one clearly stands out as the main focus?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Are there multiple subjects with one primary focus?

- Does one subject dominate despite others being present?

- Is there a clear main subject among multiple elements?

- Does the shot highlight one subject among many?

- Is there a primary focus despite multiple subjects?

- Does one subject stand out from the group?

- Is there a dominant subject among several?

- Does the video emphasize one subject among many?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot featuring multiple subjects where one clearly dominates as the main focus.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video emphasizing one subject among many.

- A shot with a clear primary subject in a group.

- A video focusing on one dominant element.

- A shot highlighting one subject among several.

- A video with one standout subject.

- A shot emphasizing a primary subject among many.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_many_subject_one_focus_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_many_subject_one_focus_shot is False</code>

</details>

<details>
<summary><h2>Is Just Non Human Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_non_human_shot</code>


<h3>📖 Definition:</h3>
Does the video consistently feature one dominant non-human subject or a single group of non-human subjects in the frame?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is there a single non-human subject that dominates the frame?

- Does the shot maintain focus on one primary non-human subject?

- Is the video centered on a single non-human subject or group?

- Does one non-human subject remain the main focus?

- Is there a consistent non-human subject throughout?

- Does the camera stay focused on one non-human element?

- Is there a single dominant non-human presence?

- Does the shot emphasize one non-human subject?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot consistently featuring either a single non-human subject or a single group of non-human subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video focused on a single non-human subject.

- A shot maintaining focus on one non-human group.

- A video centered on a primary non-human subject.

- A shot emphasizing a single non-human presence.

- A video tracking one main non-human subject.

- A shot dedicated to a single non-human group.

- A video highlighting one non-human subject.

- A shot following a single non-human element.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_non_human_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_non_human_shot is False</code>

</details>

<details>
<summary><h2>Is Just Scenery Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_scenery_shot</code>


<h3>📖 Definition:</h3>
Does the video focus on scenery or environment without emphasis on any subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the shot purely focused on the environment or landscape?

- Does the video exclusively show scenery without subjects?

- Is the emphasis solely on the surrounding environment?

- Does the shot capture only the location or setting?

- Is the video dedicated to showing the scenery alone?

- Does the camera focus entirely on the environment?

- Is the shot purely about the landscape or setting?

- Does the video avoid emphasizing any specific subjects?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot focusing on scenery or environment without emphasis on any subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video purely showcasing scenery.

- A shot dedicated to environmental views.

- A video capturing only landscape elements.

- A shot emphasizing scenic composition.

- A video focused solely on surroundings.

- A shot showing pure environmental content.

- A video highlighting only scenery.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_scenery_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_scenery_shot is False</code>

</details>

<details>
<summary><h2>Is Just Subject Scene Mismatch Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_just_subject_scene_mismatch_shot</code>


<h3>📖 Definition:</h3>
Does the video feature a subject and scene that do not match, making it difficult to classify shot size?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Is the shot size difficult to classify due to a mismatch between the subject and the scene?

- Does the video present a subject-scene mismatch that makes shot size classification challenging?

- Is there a mismatch between subject and scene shot sizes?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot where the subject and scene scales are mismatched, complicating shot size classification.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- The video presents a subject-scene mismatch that makes shot size classification challenging.

- The video presents an inconsistency between the subject and the scene, making shot size classification challenging.

- The video shows a mismatch between the subject and the scene, making shot size classification difficult.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_just_subject_scene_mismatch_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_just_subject_scene_mismatch_shot is False</code>

</details>

<details>
<summary><h2>Is Non Human Shot</h2></summary>


<h3>🔵 Label Name:</h3>
<code>is_non_human_shot</code>


<h3>📖 Definition:</h3>
Is the shot focused on non-human subjects?

<details>
<summary><h4> Question (Definition)</h4></summary>

</details>

<details>
<summary><h4> Alternative Question</h4></summary>

- Does the video primarily feature non-human subjects?

- Is the main focus on animals, objects, or other non-human elements?

- Are non-human subjects the primary focus of this shot?

- Does the camera mainly follow non-human subjects?

- Is this shot centered on non-human elements?

- Are the main subjects in this shot non-human?

- Does this shot primarily capture non-human subjects?

- Is the focus primarily on subjects other than humans?

</details>

<details>
<summary><h4> Prompt (Definition)</h4></summary>

- A shot that primarily focuses on non-human subjects.

</details>

<details>
<summary><h4> Alternative Prompt</h4></summary>

- A video centered on non-human subjects.

- A shot where non-human elements are the main focus.

- A video primarily featuring animals or objects.

- A shot emphasizing non-human subjects.

- A video where non-human elements are central.

- A shot focusing on non-human characters or objects.

- A video capturing non-human-centered action.

- A shot predominantly featuring non-human subjects.

</details>

<h4>🟢 Positive:</h4>
<code>self.cam_setup.is_non_human_shot is True</code>

<h4>🔴 Negative:</h4>
<code>self.cam_setup.is_non_human_shot is False</code>

</details>
