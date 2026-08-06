# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (qa)
- **Total Dataset Size**: 4456 critique samples
- **Filtered Dataset Size** (qa): 1851 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 40
- **Timestamp**: 20251015_0327

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

A CONSTRUCTIVE critique must provide SPECIFIC information about what to change or add. Ask yourself: "Does this critique tell me what the answer should say or what specifically needs to be fixed?"

**CONSTRUCTIVE examples (tells you WHAT to change):**
- "This is false. She would have been 18 or 19" → Change age to 18 or 19 ✅
- "The baby belongs to the narrator is inaccurate" → Baby doesn't belong to narrator ✅
- "It's omitted that the child was crushed under a roof" → Add this fact ✅
- "The description of picking the yellow flower is incorrect" → That specific action is wrong ✅
- "Some people are worried due to the virus" → Add this as the answer ✅
- "Unnecessarily wordy" → Remove extra words ✅
- "Should be a full sentence" → Rewrite as complete sentence ✅
- "The last sentence is repetitive" → Remove/revise that sentence ✅

**NON-CONSTRUCTIVE examples (too vague, doesn't tell you what to change):**
- "Should be rewritten because X doesn't indicate such" → How to rewrite? What should it say? ❌
- "The listing of emotions doesn't make sense" → Which emotions? What's wrong? ❌
- "Left out key happenings" → What happenings? ❌
- "Description is too simple" → What details to add? ❌
- "Needs more analysis" → What analysis? ❌
- "Could be more accurate" → How? What's inaccurate specifically? ❌
- "This is wrong" (without saying what) → What specifically? ❌
- "Should consider correcting this" → Correct to what? ❌

**Test for constructiveness:** Can you improve the answer based ONLY on the critique, without re-reading the source material?
- If YES (critique provides the missing/corrected information) → Constructive ✅
- If NO (need source to know what to add/fix) → Non-Constructive ❌

Special case:
- If the answer is already correct and the critique says "correct" or "no issues" → CONSTRUCTIVE ✅

Your rationale should conclude with ONE of these patterns:
- "The critique specifies that [specific change X]" → Constructive
- "The critique does not specify what to change/add" → Non-Constructive

Format your response as:
Rationale: [Your reasoning here]
Classification: [Constructive or Non-Constructive]

Question:
{question}

Answer:
{answer}

Critique:
{critique}
```

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | 25 | 50.00% |
| Non-Constructive | 25 | 50.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Write a ~3 sentence summary.

**Answer**: Community Forest International purchased a 350-acre old-growth forest from Robena Weatherly. Robena's family has owned the land for generations, dating back to 1812. CFI plans to preserve the forest, using it as part of its carbon offsetting program. 

**Critique**: This should be in past tense and use "at the time of the article" for further accuracy.

**Rationale**: The critique suggests changing the tense of the summary to past tense and adding the phrase "at the time of the article" for increased accuracy. However, it does not specify which parts of the summary need to be changed to past tense or where exactly to insert the phrase "at the time of the article." Without these specifics, it is unclear how to implement the suggested changes.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Write a ~2 sentence summary.

**Answer**: President Trump accused Democrats who did not applaud during his State of the Union address of treason, saying they would rather see Trump do badly than do well. Trump also contrasted Democrats' reactions to his State of the Union with the enthusiastic support from Republicans. He also criticized Pelosi for calling the bonuses some companies are giving employees as a result of Trump's tax cuts "crumbs," saying she wants to give all of Americans' money away. Trump then likened Pelosi to Hillary Clinton, saying she is the Democrats' "secret weapon."

**Critique**: There are too many sentences. 

**Rationale**: The critique states that there are too many sentences in the answer, but it does not specify which sentences should be removed or how the information should be condensed. Without specific guidance on what to change, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: What is the narrator's predator?

**Answer**: The narrator's predator is another fish that got to the glowing light first and claimed it as their own.

**Critique**: It is not correct that the bigger fish got to the glowing light first and claimed it as their own

**Rationale**: The critique points out that the statement about the bigger fish getting to the glowing light first and claiming it as their own is incorrect. However, it does not provide specific information on what the correct information should be or what the answer should say instead. Without knowing what the correct scenario is, the critique does not guide how to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Explain the part about Jeanne hating being old despite the fact that she was always old for the narrator.

**Answer**: 

**Critique**: Answer missing.

**Rationale**: The critique states that the answer is missing, but it does not provide any specific information about what the answer should include or what specific details need to be addressed regarding Jeanne hating being old. Without guidance on what to add or how to construct the answer, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

Who is the producer of the Lord of the Rings series?

**Answer**: New Line Cinema

**Critique**: While New Line Cinema is involved in the production, they are not the main producers.

**Rationale**: The critique states that New Line Cinema is involved in the production but does not specify who the main producers are. It does not provide the specific information needed to correct the answer, such as naming the main producers. Therefore, the critique does not give enough detail to improve the answer without additional information from the source material.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Write a ~6 sentence summary.

**Answer**: An old man walks through the marble memorials of heroes from a bloody past. In the heart of the memorial is a statue of the daughter he lost in a global war, his grief pushing him to the ground in torment. He remembers all the hope he had for her future before he watched the live footage of her dying in battle. Despite all the pain, he resolves to keep going for her sake.

**Critique**: The ending is inaccurate. Rather than resolve to keep going, he curls up and waits to die.

**Rationale**: The critique specifies that the ending of the summary is inaccurate and provides the specific change needed: instead of the old man resolving to keep going, he actually curls up and waits to die. This gives clear guidance on what to change in the answer.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique specifies that the answer should include the information that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This provides specific information that can be added to improve the answer.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

Why did Trump aides want dirt on Rhodes and Khal?

**Answer**: They wanted to reverse the Iran Deal.

**Critique**: Trump was the one who wanted to reverse the deal. The dirt was wanted on the two former aides in connection with Trump’s goal of reversing the Iran deal.

**Rationale**: The critique specifies that the dirt was wanted on the two former aides in connection with Trump's goal of reversing the Iran deal, rather than the aides themselves wanting to reverse the deal. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

What has she achieved?

**Answer**: She was elected to the National Assembly as part of the My Step Alliance.

**Critique**: Another accomplishment in Ghazaryan's career is her membership in the Yerevan Council of Elders.

**Rationale**: The critique specifies that another accomplishment to add is Ghazaryan's membership in the Yerevan Council of Elders. This provides specific information about what to include in the answer to make it more complete.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Are there other characters in the story?

**Answer**: The boy and the men with apparently fine boots.

**Critique**: There is no mention of the man, the main character. 

**Rationale**: The critique specifies that the answer should include a mention of the man, who is identified as the main character. This provides specific information about what is missing from the answer and what needs to be added to improve it.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What role does Will Poulter play in the Lord of the Rings series?

**Answer**: Poulter and the other producers of the show are staying quiet about the specific details of Poulter's character.

**Critique**: While it is true that the specifics of the role are being kept under wraps, it is mentioned that it will be a lead role.

**Rationale**: The critique specifies that the answer should include the information that Will Poulter's role is a lead role, even though the specifics are not disclosed. This provides a specific detail to add to the answer, making it constructive.

**Classification**: Constructive

---

### Sample 2/50 - [Constructive]

**Question**: Summarize the interactions between the narrator and his client.

**Answer**: The narrator meets with his client, Mrs. Richardson, and offers to show her some pictures of her husband's affair. Mrs. Richardson agrees to go to the narrator's apartment.

**Critique**: It is implied that Mrs. Richardson is the one having an affair, not her husband. 

**Rationale**: The critique specifies that the information about who is having an affair is incorrect. It indicates that Mrs. Richardson is the one having an affair, not her husband. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They plan to use it as part of its carbon offset program, through which businesses pay them to preserve old-growth forests. 

**Critique**: It's omitted that they plan to put a "working land conservation easement" on the property.

**Rationale**: The critique specifies that the answer should include the information about the new owners' plan to put a "working land conservation easement" on the property. This provides specific information about what to add to the answer.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who are the main characters of the story?

**Answer**: Max; Nina

**Critique**: A grammar mistake needs to be fixed here, the comma needs to be deleted between Max and Nina, and replaced with an "and".

**Rationale**: The critique specifies that the comma between "Max" and "Nina" should be deleted and replaced with "and". This provides a specific grammatical change to be made to the answer.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique specifies that the answer should include the information that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This provides specific information that can be added to improve the answer.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Why were married couples paying more tax than couples just living together?

**Answer**: The proposal was rejected because married couples were paying more tax than couples who were just living together. This was due to the fact that the government had provided incomplete information to voters, which was later overturned by the supreme court.

**Critique**: This response is not related.

**Rationale**: The critique states that the response is "not related," but it does not specify what the answer should say or what specifically needs to be fixed. It does not provide any information on how to correct or improve the answer, such as what the correct relationship between married couples and tax should be or what specific information is missing or incorrect. Therefore, the critique does not provide enough guidance to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How did the two characters in the story meet?

**Answer**: The two characters met at a party.

**Critique**: The answer can venture a guess, but it must note that it's doing that.

**Rationale**: The critique suggests that the answer should indicate that it is a guess, but it does not specify how to incorporate this into the answer or what specific wording to use. It lacks specific guidance on what to change or add to the answer to make it clear that it is a guess. Therefore, the critique does not provide enough information to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two of th co-producers are working on the movie.

**Critique**: There are more than two producers working on the movie.

**Rationale**: The critique states that there are more than two producers working on the movie, but it does not specify the exact number of producers or provide any specific information about what the answer should say. Without knowing the exact number, the answer cannot be improved based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who made the Statue of Christopher Columbus in Beacon Hill, Boston?

**Answer**: Joseph Iasigi, a Greek merchant, made the statue of Christopher Columbus.

**Critique**: This is incorrect--the article does not state who made the sculpture.

**Rationale**: The critique points out that the answer is incorrect but does not provide the correct information or specify what the answer should say. It only states that the article does not mention who made the sculpture, which does not help in improving the answer without additional information from the source material. Therefore, the critique does not provide specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 10/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two: David Ellison and Dana Goldberg.

**Critique**: There are more than two producers on the film.

**Rationale**: The critique states that there are more than two producers on the film, but it does not specify who the additional producers are or how many there are in total. Without this specific information, it is not possible to correct the answer based solely on the critique. Therefore, the critique does not provide enough detail to make a specific change to the answer.

**Classification**: Non-Constructive

---

### Sample 11/50 - [Non-Constructive]

**Question**: Explain the part about Jeanne hating being old despite the fact that she was always old for the narrator.

**Answer**: 

**Critique**: Answer missing.

**Rationale**: The critique states that the answer is missing, but it does not provide any specific information about what the answer should include or what specific details need to be addressed regarding Jeanne hating being old. Without guidance on what to add or how to construct the answer, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 12/50 - [Non-Constructive]

**Question**: Why is the narrator starving?

**Answer**: It may be implied they are a fish or at least amphibious.

**Critique**: The answer is irrelevant. 

**Rationale**: The critique states that the answer is irrelevant but does not provide any specific information about what the answer should say or what specifically needs to be fixed. It does not indicate what the correct or relevant information should be regarding why the narrator is starving. Without this information, one cannot improve the answer based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 13/50 - [Non-Constructive]

**Question**: What is the purpose of this article?

**Answer**: To inform of the ban passed by Michigan on intrusive data collection practices, explain the content of the ban and its implications.

**Critique**: Doesn't mention who is being informed.

**Rationale**: The critique points out that the answer does not specify who is being informed by the article. However, it does not provide specific information on what to change or add to the answer to address this issue. It does not specify who should be mentioned as the audience or how to incorporate this information into the answer. Therefore, the critique does not provide enough detail to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What has she achieved?

**Answer**: She was elected to the National Assembly as part of the My Step Alliance.

**Critique**: Another accomplishment in Ghazaryan's career is her membership in the Yerevan Council of Elders.

**Rationale**: The critique specifies that another accomplishment to add is Ghazaryan's membership in the Yerevan Council of Elders. This provides specific information about what to include in the answer to make it more complete.

**Classification**: Constructive

---

### Sample 15/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who are the major characters in the story?

**Answer**: The narrator and a woman

**Critique**: The answer would be better if it gave a little bit more information about the woman.

**Rationale**: The critique suggests that the answer should include more information about the woman, but it does not specify what additional information should be provided. It lacks specific guidance on what details to add about the woman, making it unclear how to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 16/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Community Forest International purchased a 350-acre old-growth forest from Robena Weatherly. Robena's family has owned the land for generations, dating back to 1812. CFI plans to preserve the forest, using it as part of its carbon offsetting program. 

**Critique**: This should be in past tense and use "at the time of the article" for further accuracy.

**Rationale**: The critique suggests changing the tense of the summary to past tense and adding the phrase "at the time of the article" for increased accuracy. However, it does not specify which parts of the summary need to be changed to past tense or where exactly to insert the phrase "at the time of the article." Without these specifics, it is unclear how to implement the suggested changes.

**Classification**: Non-Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: A doctor visits a couple who want a female doctor; upon reading their gen-pref results, the doctor tells them that they're having a boy. The female starts crying, and the doctor suggests an abortion.

**Critique**: This doesn't capture the story at all and needs to be rewritten totally. 

**Rationale**: The critique states that the summary "doesn't capture the story at all and needs to be rewritten totally," but it does not provide any specific information about what is incorrect or what should be included in the rewritten summary. Without specific guidance on what to change or add, it is not possible to improve the answer based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Does the narrator experience betrayal?

**Answer**: Yes, the narrator experiences betrayal from his former brother who is now a nationalist and has defected. The brother is happy not to shoot the narrator on their final goodbye and understands that he is simply "just a soldier" and does not understand the "big picture."

**Critique**: The second sentence might not be necessary at all.

**Rationale**: The critique suggests that the second sentence in the answer might not be necessary, implying that it could be removed to improve the answer. This provides specific guidance on what to change by indicating that the second sentence could be omitted.

**Classification**: Constructive

---

### Sample 19/50 - [Constructive]

**Question**: Which all countries were mentioned in the presentation for having restrictions on press freedom?

**Answer**: The mentioned countries were: Turkey, Mexico, and Egypt.

**Critique**: The answer doesn't mention Russia and Pakistan.

**Rationale**: The critique specifies that the answer should include Russia and Pakistan as countries mentioned in the presentation for having restrictions on press freedom. This provides specific information on what to add to the answer.

**Classification**: Constructive

---

### Sample 20/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: James Butler works an ordinary job in an ordinary office, and interacts with the ordinary edition of himself through a transparent glass wall. He dedicates himself to catching glimpses of the extraordinary James Butler's smile. When the ordinary James Butler finally passes away, the extraordinary James Butler finally crosses the glass wall and dies smiling.

**Critique**: James Butler wishes his life could be extraordinary. He does not interact with this extraordinary life, merely exists knowing that the other side exists.

**Rationale**: The critique does not specify what to change or add to the original answer. It provides an interpretation of James Butler's feelings and actions but does not indicate how the summary should be altered or what specific details are missing or incorrect. Without specific guidance on what to change, the critique is too vague to be constructive.

**Classification**: Non-Constructive

---

### Sample 21/50 - [Non-Constructive]

**Question**: Write a ~7 sentence summary.

**Answer**: Max asks where the narrator was the previous night. The narrator gives evasive answers because she does not want him to get involved in her "mess". Her friend Nina invites her to the party. She enjoys the party but there are disturbing rumors of her hit her ear. She notices Nina yelling, but the worst that happens at first. She finds that Nina is on her back with Todd standing over her. Then he punches her. The narrator does not react.

**Critique**: This summary needs to be re-written as it is awkwardly phrased and has details that do not need to be included. 

**Rationale**: The critique mentions that the summary is "awkwardly phrased" and contains "details that do not need to be included," but it does not specify which parts are awkward or which details are unnecessary. Without specific guidance on what to change or remove, the critique does not provide enough information to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 22/50 - [Non-Constructive]

**Question**: Describe the narrator's encounter with the Martians.

**Answer**: The narrator's ship is attacked by Martians, who are intent on conquering Earth. The crew is killed, except for the narrator, who manages to kill one Martian before being overpowered. The remaining two are killed by other crew members. The ship returns to Earth, but the narrator is not a member of the crew, but rather a passenger on the mission.

**Critique**: The answer describes Aigstar's response, not the truth.

**Rationale**: The critique states that the answer describes "Aigstar's response" rather than the truth, but it does not specify what the truth is or what specific details need to be changed or added to correct the answer. Without knowing what the correct information is, it is impossible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 23/50 - [Constructive]

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique specifies that the action described in the answer is incorrect and clarifies that the event was more akin to a baptism rather than drowning the child. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 24/50 - [Non-Constructive]

**Question**: What is the narrator's predator?

**Answer**: The narrator's predator is another fish that got to the glowing light first and claimed it as their own.

**Critique**: It is not correct that the bigger fish got to the glowing light first and claimed it as their own

**Rationale**: The critique points out that the statement about the bigger fish getting to the glowing light first and claiming it as their own is incorrect. However, it does not provide specific information on what the correct information should be or what the answer should say instead. Without knowing what the correct scenario is, the critique does not guide how to improve the answer.

**Classification**: Non-Constructive

---

### Sample 25/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Trump aides want dirt on Rhodes and Khal?

**Answer**: They wanted to reverse the Iran Deal.

**Critique**: Trump was the one who wanted to reverse the deal. The dirt was wanted on the two former aides in connection with Trump’s goal of reversing the Iran deal.

**Rationale**: The critique specifies that the dirt was wanted on the two former aides in connection with Trump's goal of reversing the Iran deal, rather than the aides themselves wanting to reverse the deal. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 26/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why do art critics think the statue is inferior?

**Answer**: because they thought the statue was unremarkable.

**Critique**: Circular logic--does not answer the question.

**Rationale**: The critique points out that the answer uses circular logic and does not effectively answer the question. However, it does not specify what the answer should say or what specific information is missing. It fails to provide guidance on how to improve the answer or what specific details should be included to address the question properly. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Carroll Wales was an art restorer and conservator of paintings, icons, frescoes, and murals. He specialized in the conservation of early Christian Byzantine art and worked on restoration projects in the Middle East, Europe and the United States.

**Critique**: When Wales existed is omitted.

**Rationale**: The critique points out that the time period during which Carroll Wales existed is missing from the answer. However, it does not specify what specific information should be added, such as the years or time period of his activity or life. Without this specific information, the critique does not provide enough guidance to improve the answer.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What will be offered at the Stadium of Light?

**Answer**: No information.

**Critique**: No, the input explicitly says that there will be "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter"

**Rationale**: The critique specifies that the answer should include the information about "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter" being offered at the Stadium of Light. This provides specific details that need to be added to the answer.

**Classification**: Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

mistake

**Answer**: Eric CrossAgario. He can't find the right charger.

**Critique**: there is no question being asked.

**Rationale**: The critique points out that there is no question being asked, but it does not specify what to change or add to the answer. It does not provide any specific information on how to improve the answer or what the answer should address. Therefore, it does not meet the criteria for being constructive.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who is the producer of the Lord of the Rings series?

**Answer**: New Line Cinema

**Critique**: While New Line Cinema is involved in the production, they are not the main producers.

**Rationale**: The critique states that New Line Cinema is involved in the production but does not specify who the main producers are. It does not provide the specific information needed to correct the answer, such as naming the main producers. Therefore, the critique does not give enough detail to improve the answer without additional information from the source material.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How long is the Canadian Birkebeiner?

**Answer**: The Canadian Birkebeiner is a one-day cross-country marathon event with races from 2 km to 55 km in distance. The main event is 55 km.

**Critique**: It misses to mention that the main event is three races, two 55km and one 31km.

**Rationale**: The critique specifies that the answer should mention that the main event consists of three races: two 55 km races and one 31 km race. This provides specific information about what is missing from the answer and what needs to be added to improve it.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Danny Lee Fread was an American hydraulic engineer and Senior Research Hydrologist, best known for his computer-based mathematical simulation programs for rainfall and runoff to forecast the flow of flooding rivers and dam failures.

**Critique**: Not up to five sentences.

**Rationale**: The critique points out that the answer is not up to five sentences, but it does not specify what additional information should be included to expand the summary to meet the sentence requirement. It lacks guidance on what content or details should be added to reach the desired length. Therefore, the critique does not provide specific instructions on how to improve the answer.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique specifies that the answer should include the information that six people died in the massacre. This provides a specific detail that needs to be added to improve the answer.

**Classification**: Constructive

---

### Sample 34/50 - [Non-Constructive]

**Question**: What era is this narration set in?

**Answer**: A. 1700s 
B. 1800s 
C. 1900s 
D. 2007
E. 2497 

E. 2497

**Critique**: Multiple incorrect answers listed as choices.

**Rationale**: The critique mentions that there are multiple incorrect answers listed as choices, but it does not specify which choices are incorrect or what the correct answer should be. Without this specific information, it is not possible to improve the answer based solely on the critique. Therefore, the critique does not provide the necessary details to make a specific change or correction to the answer.

**Classification**: Non-Constructive

---

### Sample 35/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Jerry and Brian are a happy couple, but when Jerry's friend Janice dies, Brian starts to cry and Jerry leaves.

**Critique**: Jerry does not leave

**Rationale**: The critique specifies that the statement "Jerry leaves" is incorrect and should be changed to reflect that Jerry does not leave. This provides specific information about what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Write a ~4 sentence summary.

**Answer**: Sharon is married to Mike, a writer for a popular newspaper company in New York. She is aware that he is cheating on her with Melissa, a coworker. Sharon decides to kill Mike by poisoning his potato soup. She is shocked when he dies in her arms, and she realizes that the poison she used was tasteless and would kill him in his sleep.

**Critique**: Sharon is not aware that he is cheating on her: she simply believes that.

**Rationale**: The critique specifies that the answer incorrectly states Sharon is aware of Mike's infidelity, when in fact, she only believes he is cheating. This provides specific information on what needs to be changed in the answer, which is to adjust the wording to reflect Sharon's belief rather than certainty about the cheating.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who is steering Miller's legal fight now that it is heading to the U.S. Court of Appeals?

**Answer**: The lawyers representing Andrew Miller are steering his legal fight now that it is heading to the U.S. Court of Appeals. These lawyers are affiliated with veteran Washington legal group that has a history of taking on Democrats, as well as longstanding Republican donors.

**Critique**: The answer's wording implies the legal group challenges both Democrats and Republican donors, which is wrong. The group is backed by Republican donors.

**Rationale**: The critique specifies that the wording in the answer incorrectly implies that the legal group challenges both Democrats and Republican donors, when in fact, the group is backed by Republican donors. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 38/50 - [Constructive]

**Question**: Are there other characters in the story?

**Answer**: The boy and the men with apparently fine boots.

**Critique**: There is no mention of the man, the main character. 

**Rationale**: The critique specifies that the answer should include a mention of the man, who is identified as the main character. This provides specific information about what is missing from the answer and what needs to be added to improve it.

**Classification**: Constructive

---

### Sample 39/50 - [Constructive]

**Question**: When was Patsy's first film?

**Answer**: 1983

**Critique**: 1983 was her first television role ('In 1983 she had debut in television'), so replace with the correct answer: 1986 ('1986 _El cachas de oro_ Selena')

**Rationale**: The critique specifies that the answer should be changed from 1983 to 1986, as 1983 was her first television role, not her first film. It provides the specific information needed to correct the answer by stating the correct year and the film title, "El cachas de oro," in which she debuted in 1986.

**Classification**: Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is the story's genre?

**Answer**: Science fiction. The sudden event has a supernatural cause and the story deals with an apocalyptic event.

**Critique**: 'Supernatural' should read 'scientific'

**Rationale**: The critique specifies that the word "supernatural" should be changed to "scientific," providing a specific correction to the answer. This allows for an improvement of the answer without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Why does the narrator want to leave everything behind?

**Answer**: The narrator has a sense of apathy about the life that she has been living and the current state of her living space. She wants to rid her life of external things to make something new and worthwhile out of her life.

**Critique**: We don't know the narrator' gender.

**Rationale**: The critique points out that the gender of the narrator is not specified, but it does not provide specific information on what to change or add to the answer. It does not suggest how to address the issue or what the answer should say instead. Therefore, it does not guide how to improve the answer based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Non-Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: President Trump accused Democrats who did not applaud during his State of the Union address of treason, saying they would rather see Trump do badly than do well. Trump also contrasted Democrats' reactions to his State of the Union with the enthusiastic support from Republicans. He also criticized Pelosi for calling the bonuses some companies are giving employees as a result of Trump's tax cuts "crumbs," saying she wants to give all of Americans' money away. Trump then likened Pelosi to Hillary Clinton, saying she is the Democrats' "secret weapon."

**Critique**: There are too many sentences. 

**Rationale**: The critique states that there are too many sentences in the answer, but it does not specify which sentences should be removed or how the information should be condensed. Without specific guidance on what to change, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The narrator persuades people to be wise about recycled pizza boxes. They say that because pizza boxes are made of corrugated cardboard, they are recyclable. The reason some pizza boxes are not recyclable is that the juicy toppings and cheese stick to the pizza box. Once they are caked with oil or grease, they are difficult to recycle.

Additionally, pizza boxes usually have moisture, which could harbor mold and bacteria if composted. One way to avoid such events is to ensure the pizza box is pest free. Properly disposing them will be helpful, too.

**Critique**: The oil is what causes problems when composting too, and "properly disposing them" is the subject of the article

**Rationale**: The critique specifies that the issue with oil also affects composting, which should be included in the answer. Additionally, it points out that "properly disposing them" is the main subject of the article, suggesting that the answer should focus more on this aspect. These specific points provide clear guidance on what to change or add to the answer.

**Classification**: Constructive

---

### Sample 44/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How do the boy and the mother feel about each other?

**Answer**: The boy and his mother feel deeply connected to each other, but they also feel hurt and confusion because he left for awhile. However, both remain hopeful that he will return and their relationship can continue to grow.

**Critique**: "Slowly, quickly, coldly he spoke to his mother. "Fine," he would say. "You're not my mother," he would say." is evidence of the terms on which the son left his mother. Correct the answer to reflect that the boy denies the connection with his mother.

**Rationale**: The critique specifies that the answer should be corrected to reflect that the boy denies the connection with his mother, as evidenced by his statements "You're not my mother." This provides specific information on what aspect of the relationship needs to be changed in the answer.

**Classification**: Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: A man in a trail hears a car approaching. It's a dark blue Cobra. The man waits with a concealed weapon. A tall man pulls out and he places a said weapon beside him on the passenger seat, and then climbs out of the car and walk toward the trail. The two meet, the tall man walks up to the weathered man. Both have weapons: the weathered man a silenced Glock and the tall man a Marlin 1984 rifle; the weathered man holds it back on the trail, and the tall man resumes walking to the base of the trail. The two meet there, each clutching a gun and a knife, with a lot of tension in the air.

**Critique**: The two never meet. 

**Rationale**: The critique specifies that the statement "The two meet" in the answer is incorrect and should be changed to reflect that the two never meet. This provides specific information about what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 46/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is his academic pedigree?

**Answer**: His undergraduate degree is a BA from the University of Toronto, his master's degree is a Ph. D. from York University. He also has a postgraduate diploma from Humber College.

**Critique**: The claim that he has a postgraduate degree from Humber College is unattested.

**Rationale**: The critique specifies that the claim about having a postgraduate degree from Humber College is unattested, indicating that this part of the answer should be removed or verified. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: An old man walks through the marble memorials of heroes from a bloody past. In the heart of the memorial is a statue of the daughter he lost in a global war, his grief pushing him to the ground in torment. He remembers all the hope he had for her future before he watched the live footage of her dying in battle. Despite all the pain, he resolves to keep going for her sake.

**Critique**: The ending is inaccurate. Rather than resolve to keep going, he curls up and waits to die.

**Rationale**: The critique specifies that the ending of the summary is inaccurate and provides the specific change needed: instead of the old man resolving to keep going, he actually curls up and waits to die. This gives clear guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 48/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: The Democratic Party needs a nominee, but right now it has a train wreck instead. The front-runner seems too old for the job and is poised to lose the first two primary season contests. The woman who was supposed to become the front-runner on the basis of her policy chops is sliding in the polls after botching her health care strategy.

**Critique**: This is a copy and paste job

**Rationale**: The critique "This is a copy and paste job" does not provide any specific information about what to change or add to the answer. It does not indicate which parts of the answer are problematic or how they should be revised. Without additional details, it is impossible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They are hoping to manage it so that it will cater for some of the neighboring community.

**Critique**: This answer is wrong. They plan to  use it for their carbon offset program and preserve it by putting a "working land conservation easement" on the property. 


**Rationale**: The critique specifies that the new owners plan to use the property for their carbon offset program and preserve it by putting a "working land conservation easement" on the property. This provides specific information about what the answer should say, allowing for a clear correction to be made without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Write a ~10 sentence summary.

**Answer**: Lucius is stationed at Hadrian's Wall in Britannia, to extend Rome's reach. The native Pict tribes continually assault the Wall, and Lucius worries the Romans are losing this war. One night, an enemy fighter sneaks into the camp and slaughters Lucius. The endless cycle of violence weighs heavy on Lucius and he begins to question the purpose of his existence. Despite continuing to fight, rampant violence makes Lucius reconsider his assumed destiny in faraway Britannia.

**Critique**: Far too self-reflective

**Rationale**: The critique "Far too self-reflective" does not specify what to change or add in the answer. It is vague and does not provide any specific guidance on how to adjust the content to address the issue of being "too self-reflective." Without additional details on what aspects of the self-reflection should be reduced or altered, it is not possible to improve the answer based solely on this critique. Therefore, the critique does not meet the criteria for being constructive.

**Classification**: Non-Constructive

---

