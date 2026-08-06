# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (qa)
- **Total Dataset Size**: 4456 critique samples
- **Filtered Dataset Size** (qa): 1851 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 40
- **Timestamp**: 20251015_0336

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating whether a critique provides ACTIONABLE feedback for improving an answer.

**Core principle:** A critique is CONSTRUCTIVE if it gives you specific actions to take that will improve the answer. Think: "After reading this critique, do I know what to do next?"

**CONSTRUCTIVE - Examples where you know what action to take:**

1. Factual corrections that help answer the question:
   - "He was caught, though" → Action: Add this fact ✅
   - "Some people are worried due to the virus" → Action: Use this as the answer ✅
   - "It should be 18 or 19, not 17" → Action: Change the number ✅

2. Content to add/remove:
   - "It's omitted that X" → Action: Add X ✅
   - "The second sentence is irrelevant" → Action: Remove second sentence ✅
   - "The last sentence is repetitive" → Action: Remove/revise it ✅

3. Style improvements with clear direction:
   - "Unnecessarily wordy" → Action: Make it more concise ✅
   - "Should be a full sentence" → Action: Rewrite as complete sentence ✅

4. Confirmation when answer is good:
   - "Correct answer" or "Answer correctly" when answer is already good → Action: No changes needed ✅

**NON-CONSTRUCTIVE - Examples where you don't know what action to take:**

1. Corrections that don't help answer the question:
   - Question: "Why did she donate?" Answer: "She was born in China" Critique: "No, she was born in California"
   - Problem: Even with correction, still doesn't answer WHY she donated ❌

2. Vague problems without specifics:
   - "Needs more description" → What description? ❌
   - "Could be more accurate" → What's inaccurate? How to fix? ❌
   - "Left out key information" → What information? ❌
   - "The listing doesn't make sense" → Which part? What's wrong? ❌

3. Contradictory or unclear:
   - "Correct answer, no description" when answer needs improvement → Which is it? What description? ❌
   - "Should be rewritten" without saying how → Rewrite how? ❌

**Decision process:**
1. Read the critique
2. Ask: "Can I improve the answer using ONLY this critique, without re-reading the source?"
3. Ask: "Does this critique help me better answer the QUESTION that was asked?"
4. If YES to both → Constructive
5. If NO to either → Non-Constructive

**Special case:** If the answer is good and critique says "correct" / "no issues" / "accurate" → Constructive (action = keep as is)

Format your response as:
Rationale: [In 2-3 sentences, explain what action the critique suggests (if constructive) or what's missing (if non-constructive)]
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
| Constructive | 29 | 58.00% |
| Non-Constructive | 21 | 42.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Write a ~7 sentence summary.

**Answer**: Max asks where the narrator was the previous night. The narrator gives evasive answers because she does not want him to get involved in her "mess". Her friend Nina invites her to the party. She enjoys the party but there are disturbing rumors of her hit her ear. She notices Nina yelling, but the worst that happens at first. She finds that Nina is on her back with Todd standing over her. Then he punches her. The narrator does not react.

**Critique**: This summary needs to be re-written as it is awkwardly phrased and has details that do not need to be included. 

**Rationale**: The critique suggests that the summary should be re-written due to awkward phrasing and the inclusion of unnecessary details. However, it does not provide specific guidance on which parts are awkward or which details should be removed. Without specific instructions on how to improve the phrasing or which details to omit, the critique lacks actionable feedback. Therefore, it does not help in improving the answer effectively.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Write a ~10 sentence summary.

**Answer**: Lucius is stationed at Hadrian's Wall in Britannia, to extend Rome's reach. The native Pict tribes continually assault the Wall, and Lucius worries the Romans are losing this war. One night, an enemy fighter sneaks into the camp and slaughters Lucius. The endless cycle of violence weighs heavy on Lucius and he begins to question the purpose of his existence. Despite continuing to fight, rampant violence makes Lucius reconsider his assumed destiny in faraway Britannia.

**Critique**: Far too self-reflective

**Rationale**: The critique "Far too self-reflective" is vague and does not provide specific guidance on how to improve the answer. It does not specify which parts of the summary are overly self-reflective or suggest how to adjust the content to better meet the requirements of the question. Without clear direction on what to change or how to make the summary less self-reflective, the critique does not offer actionable feedback.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Who is the producer of the Lord of the Rings series?

**Answer**: New Line Cinema

**Critique**: While New Line Cinema is involved in the production, they are not the main producers.

**Rationale**: The critique points out that New Line Cinema is involved but not the main producer, suggesting that the answer is incomplete or partially incorrect. However, it does not specify who the main producers are, leaving the answer incomplete without clear guidance on how to correct it. Therefore, the critique does not provide specific actions to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Why is the narrator starving?

**Answer**: It may be implied they are a fish or at least amphibious.

**Critique**: The answer is irrelevant. 

**Rationale**: The critique states that the answer is irrelevant, but it does not provide any specific guidance on how to improve the answer or what relevant information should be included. Without knowing what makes the answer irrelevant or what the correct focus should be, there is no clear action to take to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: What is the purpose of this article?

**Answer**: To inform of the ban passed by Michigan on intrusive data collection practices, explain the content of the ban and its implications.

**Critique**: Doesn't mention who is being informed.

**Rationale**: The critique points out that the answer does not specify who the intended audience is for the article. However, it does not provide specific guidance on how to address this issue or suggest who the audience might be. Without additional information, it is unclear how to improve the answer to better address the critique. Therefore, the critique lacks actionable feedback.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Write a ~6 sentence summary.

**Answer**: The narrator persuades people to be wise about recycled pizza boxes. They say that because pizza boxes are made of corrugated cardboard, they are recyclable. The reason some pizza boxes are not recyclable is that the juicy toppings and cheese stick to the pizza box. Once they are caked with oil or grease, they are difficult to recycle.

Additionally, pizza boxes usually have moisture, which could harbor mold and bacteria if composted. One way to avoid such events is to ensure the pizza box is pest free. Properly disposing them will be helpful, too.

**Critique**: The oil is what causes problems when composting too, and "properly disposing them" is the subject of the article

**Rationale**: The critique provides specific information that can be used to improve the answer. It suggests adding the detail that oil causes problems when composting, which is a factual correction that enhances the explanation of why pizza boxes are difficult to recycle or compost. Additionally, it points out that "properly disposing them" is the main focus of the article, indicating that the answer should emphasize this aspect more. These suggestions give clear directions for revising the answer to better align with the article's content.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique provides specific information that can be added to the answer to improve it. It suggests that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This gives a clear direction to include this reasoning in the answer, making it more complete and relevant to the question asked.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Does the narrator experience betrayal?

**Answer**: Yes, the narrator experiences betrayal from his former brother who is now a nationalist and has defected. The brother is happy not to shoot the narrator on their final goodbye and understands that he is simply "just a soldier" and does not understand the "big picture."

**Critique**: The second sentence might not be necessary at all.

**Rationale**: The critique suggests that the second sentence in the answer might be unnecessary, which provides a specific action to take: consider removing the second sentence to improve the answer's conciseness and focus. This feedback is actionable as it directly addresses how to refine the content of the answer.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

How did the two characters in the story meet?

**Answer**: The two characters met at a party.

**Critique**: The answer can venture a guess, but it must note that it's doing that.

**Rationale**: The critique suggests that the answer should indicate that it is making an assumption or guess about how the two characters met. This provides a specific action to take: revise the answer to clarify that it is a speculative response. By doing so, the answer will be more transparent about the level of certainty regarding the information provided.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique provides specific information that was omitted from the original answer, namely that six people died in the massacre. The action suggested by the critique is to add this detail to the answer to provide a more complete picture of the events surrounding 'O sicco's arrest. This additional information helps to better answer the question by giving context to the severity of the massacre he was involved in.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What role does Will Poulter play in the Lord of the Rings series?

**Answer**: Poulter and the other producers of the show are staying quiet about the specific details of Poulter's character.

**Critique**: While it is true that the specifics of the role are being kept under wraps, it is mentioned that it will be a lead role.

**Rationale**: The critique provides specific information that can be added to the answer to improve it. It suggests including the fact that Will Poulter's role is a lead role, even though the specifics are not disclosed. This gives a clear action to enhance the answer by adding this detail.

**Classification**: Constructive

---

### Sample 2/50 - [Constructive]

**Question**: Summarize the interactions between the narrator and his client.

**Answer**: The narrator meets with his client, Mrs. Richardson, and offers to show her some pictures of her husband's affair. Mrs. Richardson agrees to go to the narrator's apartment.

**Critique**: It is implied that Mrs. Richardson is the one having an affair, not her husband. 

**Rationale**: The critique provides a factual correction that directly impacts the accuracy of the answer. It suggests that the affair involves Mrs. Richardson, not her husband, which changes the context of the interactions between the narrator and his client. The action to take is to revise the answer to reflect that Mrs. Richardson is the one having an affair.

**Classification**: Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They plan to use it as part of its carbon offset program, through which businesses pay them to preserve old-growth forests. 

**Critique**: It's omitted that they plan to put a "working land conservation easement" on the property.

**Rationale**: The critique provides specific information that is missing from the original answer, namely the plan to put a "working land conservation easement" on the property. This suggests a clear action: add this detail to the answer to make it more complete and accurate. By including this information, the answer will better address the question about the new owners' plans for the property.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who are the main characters of the story?

**Answer**: Max; Nina

**Critique**: A grammar mistake needs to be fixed here, the comma needs to be deleted between Max and Nina, and replaced with an "and".

**Rationale**: The critique provides a specific action to improve the answer by correcting a grammatical error. It instructs to replace the comma with "and" between "Max" and "Nina," which is a clear and actionable step to enhance the clarity and correctness of the answer.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique provides specific information that can be added to the answer to improve it. It suggests that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This gives a clear direction to include this reasoning in the answer, making it more complete and relevant to the question asked.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Why were married couples paying more tax than couples just living together?

**Answer**: The proposal was rejected because married couples were paying more tax than couples who were just living together. This was due to the fact that the government had provided incomplete information to voters, which was later overturned by the supreme court.

**Critique**: This response is not related.

**Rationale**: The critique states that the response is not related, but it does not provide any specific guidance on how to improve the answer or what the correct information should be. Without knowing what aspect of the answer is unrelated or what the correct information is, there is no clear action to take to improve the answer. The critique lacks specificity and does not help in better answering the question.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How did the two characters in the story meet?

**Answer**: The two characters met at a party.

**Critique**: The answer can venture a guess, but it must note that it's doing that.

**Rationale**: The critique suggests that the answer should indicate that it is making an assumption or guess about how the two characters met. This provides a specific action to take: revise the answer to clarify that it is a speculative response. By doing so, the answer will be more transparent about the level of certainty regarding the information provided.

**Classification**: Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two of th co-producers are working on the movie.

**Critique**: There are more than two producers working on the movie.

**Rationale**: The critique indicates that the number of co-producers mentioned in the answer is incorrect, suggesting that there are more than two. However, it does not specify the correct number of co-producers, leaving the answer incomplete and without a clear action to correct it. The critique lacks the specific information needed to improve the answer directly.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who made the Statue of Christopher Columbus in Beacon Hill, Boston?

**Answer**: Joseph Iasigi, a Greek merchant, made the statue of Christopher Columbus.

**Critique**: This is incorrect--the article does not state who made the sculpture.

**Rationale**: The critique points out that the answer is incorrect but does not provide any specific information or guidance on what the correct answer should be. It fails to offer actionable feedback that would help improve the answer, as it does not specify who actually made the statue or suggest how to find this information. Therefore, the critique does not help in better answering the question.

**Classification**: Non-Constructive

---

### Sample 10/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two: David Ellison and Dana Goldberg.

**Critique**: There are more than two producers on the film.

**Rationale**: The critique indicates that the answer is incomplete by stating that there are more than two producers on the film. However, it does not specify who the additional producers are or how many there are in total. Without this specific information, the critique does not provide a clear action to improve the answer. Therefore, it lacks the necessary details to be actionable.

**Classification**: Non-Constructive

---

### Sample 11/50 - [Non-Constructive]

**Question**: Explain the part about Jeanne hating being old despite the fact that she was always old for the narrator.

**Answer**: 

**Critique**: Answer missing.

**Rationale**: The critique points out that the answer is missing entirely. While it identifies a problem, it does not provide specific guidance on how to address the question or what content should be included. Without additional information or direction, it is unclear what specific actions should be taken to improve the answer.

**Classification**: Non-Constructive

---

### Sample 12/50 - [Non-Constructive]

**Question**: Why is the narrator starving?

**Answer**: It may be implied they are a fish or at least amphibious.

**Critique**: The answer is irrelevant. 

**Rationale**: The critique states that the answer is irrelevant, but it does not provide any specific guidance on how to improve the answer or what relevant information should be included. Without knowing what makes the answer irrelevant or what the correct focus should be, there is no clear action to take to improve the answer.

**Classification**: Non-Constructive

---

### Sample 13/50 - [Non-Constructive]

**Question**: What is the purpose of this article?

**Answer**: To inform of the ban passed by Michigan on intrusive data collection practices, explain the content of the ban and its implications.

**Critique**: Doesn't mention who is being informed.

**Rationale**: The critique points out that the answer does not specify who the intended audience is for the article. However, it does not provide specific guidance on how to address this issue or suggest who the audience might be. Without additional information, it is unclear how to improve the answer to better address the critique. Therefore, the critique lacks actionable feedback.

**Classification**: Non-Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What has she achieved?

**Answer**: She was elected to the National Assembly as part of the My Step Alliance.

**Critique**: Another accomplishment in Ghazaryan's career is her membership in the Yerevan Council of Elders.

**Rationale**: The critique provides specific information about another achievement of Ghazaryan, which is her membership in the Yerevan Council of Elders. This suggests a clear action to improve the answer by adding this additional accomplishment to provide a more comprehensive response to the question about her achievements.

**Classification**: Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who are the major characters in the story?

**Answer**: The narrator and a woman

**Critique**: The answer would be better if it gave a little bit more information about the woman.

**Rationale**: The critique suggests that the answer should include more information about the woman, which is a specific action to take. This guidance helps improve the answer by providing additional details about one of the major characters, thereby making the response more informative and complete.

**Classification**: Constructive

---

### Sample 16/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Community Forest International purchased a 350-acre old-growth forest from Robena Weatherly. Robena's family has owned the land for generations, dating back to 1812. CFI plans to preserve the forest, using it as part of its carbon offsetting program. 

**Critique**: This should be in past tense and use "at the time of the article" for further accuracy.

**Rationale**: The critique suggests specific actions to improve the answer by changing the tense to past and adding the phrase "at the time of the article" for accuracy. These are clear, actionable steps that can be taken to enhance the precision and clarity of the summary.

**Classification**: Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: A doctor visits a couple who want a female doctor; upon reading their gen-pref results, the doctor tells them that they're having a boy. The female starts crying, and the doctor suggests an abortion.

**Critique**: This doesn't capture the story at all and needs to be rewritten totally. 

**Rationale**: The critique states that the summary does not capture the story at all and suggests a complete rewrite. However, it does not provide any specific guidance on what aspects of the story are missing or how to improve the summary. Without specific details or directions, it is unclear what changes need to be made to better capture the story. Therefore, the critique does not offer actionable feedback.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Does the narrator experience betrayal?

**Answer**: Yes, the narrator experiences betrayal from his former brother who is now a nationalist and has defected. The brother is happy not to shoot the narrator on their final goodbye and understands that he is simply "just a soldier" and does not understand the "big picture."

**Critique**: The second sentence might not be necessary at all.

**Rationale**: The critique suggests that the second sentence in the answer might be unnecessary, which provides a specific action to take: consider removing the second sentence to improve the answer's conciseness and focus. This feedback is actionable as it directly addresses how to refine the content of the answer.

**Classification**: Constructive

---

### Sample 19/50 - [Constructive]

**Question**: Which all countries were mentioned in the presentation for having restrictions on press freedom?

**Answer**: The mentioned countries were: Turkey, Mexico, and Egypt.

**Critique**: The answer doesn't mention Russia and Pakistan.

**Rationale**: The critique provides specific information that is missing from the answer, namely the omission of Russia and Pakistan. This suggests a clear action to take: add Russia and Pakistan to the list of countries mentioned in the presentation for having restrictions on press freedom. This directly helps improve the accuracy and completeness of the answer. Classification: Constructive

**Classification**: Constructive

---

### Sample 20/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: James Butler works an ordinary job in an ordinary office, and interacts with the ordinary edition of himself through a transparent glass wall. He dedicates himself to catching glimpses of the extraordinary James Butler's smile. When the ordinary James Butler finally passes away, the extraordinary James Butler finally crosses the glass wall and dies smiling.

**Critique**: James Butler wishes his life could be extraordinary. He does not interact with this extraordinary life, merely exists knowing that the other side exists.

**Rationale**: The critique suggests that the answer should focus more on James Butler's desire for an extraordinary life and his awareness of its existence, rather than his interactions with it. However, it does not provide specific guidance on how to incorporate this perspective into the summary. The critique lacks actionable steps to improve the answer, such as which parts to revise or add.

**Classification**: Non-Constructive

---

### Sample 21/50 - [Non-Constructive]

**Question**: Write a ~7 sentence summary.

**Answer**: Max asks where the narrator was the previous night. The narrator gives evasive answers because she does not want him to get involved in her "mess". Her friend Nina invites her to the party. She enjoys the party but there are disturbing rumors of her hit her ear. She notices Nina yelling, but the worst that happens at first. She finds that Nina is on her back with Todd standing over her. Then he punches her. The narrator does not react.

**Critique**: This summary needs to be re-written as it is awkwardly phrased and has details that do not need to be included. 

**Rationale**: The critique suggests that the summary should be re-written due to awkward phrasing and the inclusion of unnecessary details. However, it does not provide specific guidance on which parts are awkward or which details should be removed. Without specific instructions on how to improve the phrasing or which details to omit, the critique lacks actionable feedback. Therefore, it does not help in improving the answer effectively.

**Classification**: Non-Constructive

---

### Sample 22/50 - [Non-Constructive]

**Question**: Describe the narrator's encounter with the Martians.

**Answer**: The narrator's ship is attacked by Martians, who are intent on conquering Earth. The crew is killed, except for the narrator, who manages to kill one Martian before being overpowered. The remaining two are killed by other crew members. The ship returns to Earth, but the narrator is not a member of the crew, but rather a passenger on the mission.

**Critique**: The answer describes Aigstar's response, not the truth.

**Rationale**: The critique states that the answer describes "Aigstar's response" rather than the truth, but it does not provide any specific information on what the truth is or how the answer should be corrected. Without knowing what "Aigstar's response" refers to or what the accurate details are, there is no clear action to take to improve the answer. The critique lacks specific guidance on what needs to be changed or added to make the answer accurate.

**Classification**: Non-Constructive

---

### Sample 23/50 - [Constructive]

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique provides a factual correction by clarifying that the event described is more akin to a baptism rather than an intention to drown the child. This suggests a specific action to revise the summary to reflect the correct interpretation of the event.

**Classification**: Constructive

---

### Sample 24/50 - [Non-Constructive]

**Question**: What is the narrator's predator?

**Answer**: The narrator's predator is another fish that got to the glowing light first and claimed it as their own.

**Critique**: It is not correct that the bigger fish got to the glowing light first and claimed it as their own

**Rationale**: The critique points out that the information provided in the answer is incorrect, specifically regarding the sequence of events with the bigger fish and the glowing light. However, it does not provide any specific guidance on what the correct information should be or how to improve the answer. Without knowing what the correct sequence of events is, the critique does not offer a clear action to take to improve the answer.

**Classification**: Non-Constructive

---

### Sample 25/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Trump aides want dirt on Rhodes and Khal?

**Answer**: They wanted to reverse the Iran Deal.

**Critique**: Trump was the one who wanted to reverse the deal. The dirt was wanted on the two former aides in connection with Trump’s goal of reversing the Iran deal.

**Rationale**: The critique provides a factual correction by clarifying that it was Trump who wanted to reverse the Iran Deal, and the dirt on Rhodes and Khal was sought in connection with this goal. This suggests a specific action: revise the answer to accurately reflect that the desire for dirt on the aides was linked to Trump's objective of reversing the Iran Deal.

**Classification**: Constructive

---

### Sample 26/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why do art critics think the statue is inferior?

**Answer**: because they thought the statue was unremarkable.

**Critique**: Circular logic--does not answer the question.

**Rationale**: The critique points out that the answer uses circular logic and does not effectively address the question of why art critics think the statue is inferior. However, it does not provide specific guidance on how to improve the answer or what information should be included to better address the question. Without additional details or suggestions, the critique does not offer a clear path for improvement.

**Classification**: Non-Constructive

---

### Sample 27/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Carroll Wales was an art restorer and conservator of paintings, icons, frescoes, and murals. He specialized in the conservation of early Christian Byzantine art and worked on restoration projects in the Middle East, Europe and the United States.

**Critique**: When Wales existed is omitted.

**Rationale**: The critique points out that the time period during which Carroll Wales lived or worked is missing from the summary. This suggests a specific action: add information about the time period or dates relevant to Wales's life or career. This would enhance the completeness of the summary by providing temporal context.

**Classification**: Constructive

---

### Sample 28/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What will be offered at the Stadium of Light?

**Answer**: No information.

**Critique**: No, the input explicitly says that there will be "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter"

**Rationale**: The critique provides specific information that was omitted from the original answer. It suggests adding details about what will be offered at the Stadium of Light, namely "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter." This gives clear direction on how to improve the answer by including this specific content.

**Classification**: Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

mistake

**Answer**: Eric CrossAgario. He can't find the right charger.

**Critique**: there is no question being asked.

**Rationale**: The critique points out that there is no question being asked, which is a fundamental issue that prevents any meaningful evaluation or improvement of the answer. Without a question, it's impossible to determine if the answer is relevant or correct, and thus, no specific actions can be taken to improve the answer based on this critique. The critique does not provide guidance on how to address the lack of a question or how to proceed with the given answer.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who is the producer of the Lord of the Rings series?

**Answer**: New Line Cinema

**Critique**: While New Line Cinema is involved in the production, they are not the main producers.

**Rationale**: The critique points out that New Line Cinema is involved but not the main producer, suggesting that the answer is incomplete or partially incorrect. However, it does not specify who the main producers are, leaving the answer incomplete without clear guidance on how to correct it. Therefore, the critique does not provide specific actions to improve the answer.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How long is the Canadian Birkebeiner?

**Answer**: The Canadian Birkebeiner is a one-day cross-country marathon event with races from 2 km to 55 km in distance. The main event is 55 km.

**Critique**: It misses to mention that the main event is three races, two 55km and one 31km.

**Rationale**: The critique provides specific information that can be added to improve the answer. It suggests including the detail that the main event consists of three races: two 55 km races and one 31 km race. This gives clear direction on what content to add to make the answer more accurate and complete.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Danny Lee Fread was an American hydraulic engineer and Senior Research Hydrologist, best known for his computer-based mathematical simulation programs for rainfall and runoff to forecast the flow of flooding rivers and dam failures.

**Critique**: Not up to five sentences.

**Rationale**: The critique points out that the answer does not meet the requirement of being approximately five sentences long. However, it does not provide specific guidance on what additional information or details should be included to expand the summary to the desired length. Without knowing what content to add, the critique does not offer actionable feedback to improve the answer.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique provides specific information that was omitted from the original answer, namely that six people died in the massacre. The action suggested by the critique is to add this detail to the answer to provide a more complete picture of the events surrounding 'O sicco's arrest. This additional information helps to better answer the question by giving context to the severity of the massacre he was involved in.

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

**Rationale**: The critique points out that there are multiple incorrect answers listed as choices, but it does not specify which choices are incorrect or how to correct them. Without specific guidance on which options to remove or replace, the critique does not provide actionable feedback to improve the answer. Therefore, it lacks the specificity needed to be constructive.

**Classification**: Non-Constructive

---

### Sample 35/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Jerry and Brian are a happy couple, but when Jerry's friend Janice dies, Brian starts to cry and Jerry leaves.

**Critique**: Jerry does not leave

**Rationale**: The critique provides a factual correction by stating that "Jerry does not leave," which directly addresses an inaccuracy in the original answer. This suggests a specific action to take: revise the summary to accurately reflect that Jerry does not leave. This correction helps improve the accuracy of the answer in relation to the question asked.

**Classification**: Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Write a ~4 sentence summary.

**Answer**: Sharon is married to Mike, a writer for a popular newspaper company in New York. She is aware that he is cheating on her with Melissa, a coworker. Sharon decides to kill Mike by poisoning his potato soup. She is shocked when he dies in her arms, and she realizes that the poison she used was tasteless and would kill him in his sleep.

**Critique**: Sharon is not aware that he is cheating on her: she simply believes that.

**Rationale**: The critique provides a factual correction by clarifying that Sharon is not aware of Mike's infidelity but only believes it. This suggests a specific action to improve the answer: revise the statement to reflect that Sharon believes Mike is cheating, rather than stating it as a fact. This correction directly addresses the content of the summary and helps improve its accuracy.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who is steering Miller's legal fight now that it is heading to the U.S. Court of Appeals?

**Answer**: The lawyers representing Andrew Miller are steering his legal fight now that it is heading to the U.S. Court of Appeals. These lawyers are affiliated with veteran Washington legal group that has a history of taking on Democrats, as well as longstanding Republican donors.

**Critique**: The answer's wording implies the legal group challenges both Democrats and Republican donors, which is wrong. The group is backed by Republican donors.

**Rationale**: The critique identifies a specific issue with the wording of the answer, which could lead to a misunderstanding of the legal group's affiliations. It suggests that the wording implies the group challenges both Democrats and Republican donors, which is incorrect. The critique provides a clear direction to revise the wording to accurately reflect that the group is backed by Republican donors. This gives a specific action to improve the answer by clarifying the group's affiliations.

**Classification**: Constructive

---

### Sample 38/50 - [Constructive]

**Question**: Are there other characters in the story?

**Answer**: The boy and the men with apparently fine boots.

**Critique**: There is no mention of the man, the main character. 

**Rationale**: The critique suggests that the answer is missing a mention of the main character, the man. This provides a specific action to take: add the main character, the man, to the list of characters in the story. This directly helps improve the answer by ensuring it includes all relevant characters.

**Classification**: Constructive

---

### Sample 39/50 - [Constructive]

**Question**: When was Patsy's first film?

**Answer**: 1983

**Critique**: 1983 was her first television role ('In 1983 she had debut in television'), so replace with the correct answer: 1986 ('1986 _El cachas de oro_ Selena')

**Rationale**: The critique provides specific factual corrections that directly address the question about Patsy's first film. It identifies the error in the original answer and supplies the correct information, indicating that her first film was in 1986. The action to take is clear: replace "1983" with "1986" in the answer.

**Classification**: Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is the story's genre?

**Answer**: Science fiction. The sudden event has a supernatural cause and the story deals with an apocalyptic event.

**Critique**: 'Supernatural' should read 'scientific'

**Rationale**: The critique provides a specific factual correction by suggesting that the word "supernatural" should be replaced with "scientific." This gives a clear action to take: change the word to better align with the genre of science fiction, which typically involves scientific or technological elements rather than supernatural ones. This correction helps improve the accuracy of the answer in relation to the question about the story's genre.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Why does the narrator want to leave everything behind?

**Answer**: The narrator has a sense of apathy about the life that she has been living and the current state of her living space. She wants to rid her life of external things to make something new and worthwhile out of her life.

**Critique**: We don't know the narrator' gender.

**Rationale**: The critique points out a potential factual inaccuracy regarding the narrator's gender, but it does not provide specific guidance on how to address this issue. Without additional context or information, it's unclear how to correct the answer to better address the question. The critique does not help improve the answer in a way that directly answers why the narrator wants to leave everything behind.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Non-Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: President Trump accused Democrats who did not applaud during his State of the Union address of treason, saying they would rather see Trump do badly than do well. Trump also contrasted Democrats' reactions to his State of the Union with the enthusiastic support from Republicans. He also criticized Pelosi for calling the bonuses some companies are giving employees as a result of Trump's tax cuts "crumbs," saying she wants to give all of Americans' money away. Trump then likened Pelosi to Hillary Clinton, saying she is the Democrats' "secret weapon."

**Critique**: There are too many sentences. 

**Rationale**: The critique suggests that the answer is too lengthy but does not provide specific guidance on which sentences to remove or how to condense the information. Without knowing which parts are considered excessive or how to effectively shorten the summary, the critique lacks actionable feedback.

**Classification**: Non-Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The narrator persuades people to be wise about recycled pizza boxes. They say that because pizza boxes are made of corrugated cardboard, they are recyclable. The reason some pizza boxes are not recyclable is that the juicy toppings and cheese stick to the pizza box. Once they are caked with oil or grease, they are difficult to recycle.

Additionally, pizza boxes usually have moisture, which could harbor mold and bacteria if composted. One way to avoid such events is to ensure the pizza box is pest free. Properly disposing them will be helpful, too.

**Critique**: The oil is what causes problems when composting too, and "properly disposing them" is the subject of the article

**Rationale**: The critique provides specific information that can be used to improve the answer. It suggests adding the detail that oil causes problems when composting, which is a factual correction that enhances the explanation of why pizza boxes are difficult to recycle or compost. Additionally, it points out that "properly disposing them" is the main focus of the article, indicating that the answer should emphasize this aspect more. These suggestions give clear directions for revising the answer to better align with the article's content.

**Classification**: Constructive

---

### Sample 44/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How do the boy and the mother feel about each other?

**Answer**: The boy and his mother feel deeply connected to each other, but they also feel hurt and confusion because he left for awhile. However, both remain hopeful that he will return and their relationship can continue to grow.

**Critique**: "Slowly, quickly, coldly he spoke to his mother. "Fine," he would say. "You're not my mother," he would say." is evidence of the terms on which the son left his mother. Correct the answer to reflect that the boy denies the connection with his mother.

**Rationale**: The critique provides specific evidence from the text that suggests the boy denies his connection with his mother, which contradicts the original answer's claim of a deep connection. The action suggested is to revise the answer to reflect this denial of connection, using the provided evidence to support the change. This makes the critique constructive, as it gives clear direction on how to improve the answer by incorporating specific textual evidence.

**Classification**: Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: A man in a trail hears a car approaching. It's a dark blue Cobra. The man waits with a concealed weapon. A tall man pulls out and he places a said weapon beside him on the passenger seat, and then climbs out of the car and walk toward the trail. The two meet, the tall man walks up to the weathered man. Both have weapons: the weathered man a silenced Glock and the tall man a Marlin 1984 rifle; the weathered man holds it back on the trail, and the tall man resumes walking to the base of the trail. The two meet there, each clutching a gun and a knife, with a lot of tension in the air.

**Critique**: The two never meet. 

**Rationale**: The critique provides a specific factual correction by stating that "the two never meet," which directly contradicts the events described in the answer. This suggests a clear action: revise the summary to accurately reflect that the two characters do not meet, thereby improving the accuracy of the answer. The critique is actionable because it identifies a specific inaccuracy that needs to be addressed.

**Classification**: Constructive

---

### Sample 46/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is his academic pedigree?

**Answer**: His undergraduate degree is a BA from the University of Toronto, his master's degree is a Ph. D. from York University. He also has a postgraduate diploma from Humber College.

**Critique**: The claim that he has a postgraduate degree from Humber College is unattested.

**Rationale**: The critique points out that the claim about the postgraduate degree from Humber College is unattested, suggesting that this information may not be accurate or verifiable. The action implied by this critique is to verify the claim about the postgraduate diploma and either provide a source to support it or remove it if it cannot be substantiated. This is a specific action that can improve the accuracy of the answer.

**Classification**: Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: An old man walks through the marble memorials of heroes from a bloody past. In the heart of the memorial is a statue of the daughter he lost in a global war, his grief pushing him to the ground in torment. He remembers all the hope he had for her future before he watched the live footage of her dying in battle. Despite all the pain, he resolves to keep going for her sake.

**Critique**: The ending is inaccurate. Rather than resolve to keep going, he curls up and waits to die.

**Rationale**: The critique provides a specific factual correction regarding the ending of the summary. It suggests that instead of resolving to keep going, the old man curls up and waits to die. This gives a clear action to take: revise the ending of the summary to accurately reflect the man's reaction as described in the critique.

**Classification**: Constructive

---

### Sample 48/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: The Democratic Party needs a nominee, but right now it has a train wreck instead. The front-runner seems too old for the job and is poised to lose the first two primary season contests. The woman who was supposed to become the front-runner on the basis of her policy chops is sliding in the polls after botching her health care strategy.

**Critique**: This is a copy and paste job

**Rationale**: The critique "This is a copy and paste job" does not provide specific guidance on how to improve the answer. It does not identify what aspects of the answer need to be changed or how to address the issue of it being a "copy and paste job." Without further details, it is unclear what action should be taken to enhance the summary.

**Classification**: Non-Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They are hoping to manage it so that it will cater for some of the neighboring community.

**Critique**: This answer is wrong. They plan to  use it for their carbon offset program and preserve it by putting a "working land conservation easement" on the property. 


**Rationale**: The critique provides specific factual corrections that directly address the question about the new owners' plans for the property. It suggests that the answer should include information about the carbon offset program and the conservation easement. This gives clear guidance on what content to add to improve the answer.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Write a ~10 sentence summary.

**Answer**: Lucius is stationed at Hadrian's Wall in Britannia, to extend Rome's reach. The native Pict tribes continually assault the Wall, and Lucius worries the Romans are losing this war. One night, an enemy fighter sneaks into the camp and slaughters Lucius. The endless cycle of violence weighs heavy on Lucius and he begins to question the purpose of his existence. Despite continuing to fight, rampant violence makes Lucius reconsider his assumed destiny in faraway Britannia.

**Critique**: Far too self-reflective

**Rationale**: The critique "Far too self-reflective" is vague and does not provide specific guidance on how to improve the answer. It does not specify which parts of the summary are overly self-reflective or suggest how to adjust the content to better meet the requirements of the question. Without clear direction on what to change or how to make the summary less self-reflective, the critique does not offer actionable feedback.

**Classification**: Non-Constructive

---

