# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (summarization)
- **Total Dataset Size**: 4505 critique samples
- **Filtered Dataset Size** (summarization): 1728 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 42
- **Timestamp**: 20251015_0312

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
| Constructive | 30 | 60.00% |
| Non-Constructive | 20 | 40.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Answer the following question based on the above passage:

What does the text say about the parameters for an entry?

**Answer**: [rewrite]

**Critique**: The question was unconventional and the response should have been "No Answer" or "That information can't be found." 

**Rationale**: The critique suggests that the response should have been "No Answer" or "That information can't be found," but it does not specify what specifically needs to be changed or added in the answer. It does not provide specific guidance on how to rewrite the answer or what the correct response should be based on the passage. Therefore, it lacks the specificity required to be constructive.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Answer the following question based on the above passage:

Discuss LaFleur's play calls.

**Answer**: LaFleur made several questionable decisions. He had 4th & 2 from the Eagles 13-yard line, with his team leading 10-7. The Packers had been moving up and down the field. LaFleur took a page straight from the Sean McVay playbook and kicked the FG. That gave the Packers a whopping 13-7 lead. Where is the aggression? Why wouldn’t you trust Aaron Rodgers to make a play there? If you fail, you’re still up 10-7. LaFleur made some questionable play-calls.

**Critique**: A lot of the response is lifted from the passage.

**Rationale**: The critique states that "a lot of the response is lifted from the passage," but it does not specify what needs to be changed or added to improve the answer. It does not provide guidance on how to address the issue of content being lifted or suggest any specific modifications to make the answer more original or insightful. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Why do the police keep almost summoning "Pee Man"?

**Answer**: [rewrite]

**Critique**: No response.

**Rationale**: The critique does not provide any specific information about what to change or add to the answer. It simply states "No response," which does not guide how to improve or rewrite the answer. Without specific feedback or details, it is impossible to know what needs to be corrected or added to the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Answer the following question based on the above passage:

What are the three possible approaches that music directors need to make choices about the instrumental accompaniment?

**Answer**: a capella, instruments doubling the vocal lines, or a basso continuo

**Critique**: A little explanation of the approaches would have made the response much better.

**Rationale**: The critique suggests that the answer could be improved by adding explanations of the approaches, but it does not specify what those explanations should include or how to elaborate on each approach. Without specific guidance on what to add, the critique does not provide enough information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the text have to say about the traits of the rocket?

**Answer**: It's 230 feet tall, destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space. Its engines will return to Earth following lift-off. The rocket carries Elon Musk's Tesla Roadster into space.

**Critique**: It is not stated: it is destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space.


**Rationale**: The critique points out that the statement "it is destined to deliver more than 50 passengers and cargo" and "the company says it will have the power to launch them into space" are not stated in the text. However, it does not provide specific information on what should be included instead or how to correct the answer. It merely points out what is not stated without suggesting what the correct information should be or what should be added to improve the answer.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Answer the following question based on the above passage:

What does the story say about Zofia Nehringowa's sport results?

**Answer**: Zofia Nehringowa was a Polish long track speed skater who set a world record in all four individual distances (500 m, 1000 m, 1500 m, 3000 m) in 1931 and 1935. Nehringowa competed at the 1932 European Speed Skating Championships for Men and set a women's world record in the 1500m during these race. Nehringowa represented Poland at the World Allround Speed Skating Championships for Women in 1939 where she finished 5th overall.

**Critique**: In 1931, Nehringowa set the world records in the 500m, 1000m, 1500m, 3000m and 5000m. These results were approved by the ISU's the first women's speed skating world records. In 1932, Nehringowa broke the women's world records in the 1500m and 1000m. In 1935 she improved her own world records in the 3000m, 5000m and 10 000m. Change the response to reflect these results.

**Rationale**: The critique provides specific information about the correct years and distances for which Zofia Nehringowa set world records. It specifies that in 1931, she set world records in the 500m, 1000m, 1500m, 3000m, and 5000m, and that these were the first women's speed skating world records approved by the ISU. It also specifies that in 1932, she broke the women's world records in the 1500m and 1000m, and in 1935, she improved her own world records in the 3000m, 5000m, and 10,000m. This detailed information allows for a precise correction of the original answer.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

What are the consequences of the increase in Ebike activity for the company?

**Answer**: The company is having a hard time catching up with the increase in orders. They are also having a hard time with the backlog of emails and phone calls. The increase in ebikes has also led to a backlog in new product development.

**Critique**: The information is not accurate and should reflect that the company is able to keep up with the demand. 

**Rationale**: The critique specifies that the information in the answer should be changed to reflect that the company is able to keep up with the demand, rather than having a hard time catching up. This provides a specific correction to the answer.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

What does the article say about Hitchcock as a musician?

**Answer**: Hitchcock is a singer-songwriter. He has a rich, supple voice and his songs are the real attraction of the film. He has a large personal catalog. The songs in the film are from his latest album.

**Critique**: There was no mention of Hitchcock's latest album anywhere in the text. This part should be removed. 

**Rationale**: The critique specifies that the mention of Hitchcock's latest album should be removed because it was not mentioned in the text. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

Summarize everything relating to Ardalent.

**Answer**: Mrs. Cardicole has claimed Lester and Sable. She had also murdered their child. She takes the child back to her apartment and later kills him because she needed to feed her own son.

**Critique**: The response should make it clear that her 'son' is Ardalent.

**Rationale**: The critique specifies that the answer should clarify that Mrs. Cardicole's 'son' is Ardalent. This provides specific information on what to add to the answer to improve its clarity.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

Summarize how the main character's situation changes over the story.

**Answer**: Chad's story begins with him searching through the ship for survivors. He finds the captain, who gives him command of the ship. Chad is in disbelief. He leaves the ship to escape the war.

**Critique**: He doesn't leave the ship.

**Rationale**: The critique specifies that the statement "He leaves the ship to escape the war" is incorrect and should be changed to reflect that Chad does not leave the ship. This provides specific information about what needs to be corrected in the answer.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the views of the opposing sides.

**Answer**: Republicans are counting on these judges to dismantle reproductive rights, marriage equality, and the separation of church and state and to use the courts to shred the New Deal and regulations that protect the people from corporate power. They believe the Democrats are letting Mitch McConnell and Donald Trump do this to consolidate their power and are counting on the voters to stop them. The Democratic Party, in some cases, appears to be acquiescing.

**Critique**: The Republicans are stated to believe Democrats are letting McConnell and Trump do their thing to consolidate their power, which is made up.

**Rationale**: The critique specifies that the statement about Republicans believing Democrats are letting McConnell and Trump consolidate their power is inaccurate and should be changed. This provides specific information about what part of the answer is incorrect and needs to be revised.

**Classification**: Constructive

---

### Sample 2/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What happens to the child?

**Answer**: The child drowns and the priest ignores his plea for help.

**Critique**: More background detail needs to be added to this to explain how and why the child was drowning. 

**Rationale**: The critique suggests that more background detail is needed to explain how and why the child was drowning, but it does not specify what specific details or information should be added. Without knowing the source material, it is unclear what specific background details are missing or how to improve the answer based on the critique alone.

**Classification**: Non-Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Summer?

**Answer**: Summer is a girl in Jeffery's school who always seems to be in his thoughts. She has a perpetual sunflower dress and dark hair.
She's beautiful, and Jeffery has a crush on her.
The author describes Summer as someone who likes to write in a journal. All of Summer's routines are scheduled around the time she waits for Jeffery's class to finish, so she can see him.

**Critique**: The last sentence of this response needs to be omitted as it is not fully accurate.

**Rationale**: The critique specifies that the last sentence of the response should be omitted because it is not fully accurate. This provides a specific instruction on what to change in the answer.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the military tunnels in Primož?

**Answer**: The tunnels were dug as part of the long Alpine Wall. There were two tunnels totaling 5.2 kilometers along with brick-lined access shafts. They were never used for military purposes. They were built in 1930 and secured underground with steel encased in concrete with ventilation pipes and steel plates to prevent damage from aerial bombardment. Primož's military tunnels were destroyed by German forces in 1944.

**Critique**: "totaling 5.2 kilometers" - it was never mentioned exactly how long the tunnels were in the text.

**Rationale**: The critique specifies that the phrase "totaling 5.2 kilometers" should be reconsidered because the exact length of the tunnels was not mentioned in the text. This provides specific information about what to change in the answer, namely the removal or revision of the stated length of the tunnels.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about Hitchcock as a musician?

**Answer**: Hitchcock is a singer-songwriter. He has a rich, supple voice and his songs are the real attraction of the film. He has a large personal catalog. The songs in the film are from his latest album.

**Critique**: There was no mention of Hitchcock's latest album anywhere in the text. This part should be removed. 

**Rationale**: The critique specifies that the mention of Hitchcock's latest album should be removed because it was not mentioned in the text. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the most interesting facts in the text. 

**Answer**: The Mechanics Educational Society of America was founded in 1933 by disgruntled members of the International Association of Machinists. Matthew Smith, Frank McCracken, and John Anderson pushed for a full-fledged union. In June 1933, the U.S. Congress passed the National Industrial Recovery Act of 1933 which protected the collective bargaining rights of unions. A month later, MESA began an organizing drive in Detroit, Pontiac, Michigan, and Flint, Michigan.

**Critique**: The response left out key happenings in MESA's history.

**Rationale**: The critique states that the response "left out key happenings in MESA's history," but it does not specify which events or details are missing. Without knowing what specific happenings need to be included, it is not possible to improve the answer based solely on the critique. Therefore, the critique does not provide the necessary information to make a specific change or addition to the answer.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the parameters for an entry?

**Answer**: [rewrite]

**Critique**: The question was unconventional and the response should have been "No Answer" or "That information can't be found." 

**Rationale**: The critique suggests that the response should have been "No Answer" or "That information can't be found," but it does not specify what specifically needs to be changed or added in the answer. It does not provide specific guidance on how to rewrite the answer or what the correct response should be based on the passage. Therefore, it lacks the specificity required to be constructive.

**Classification**: Non-Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why is the civilian ship empty?

**Answer**: It turns out that Roger murdered Drake and then went mad killing everyone on board.

**Critique**: Although Roger killed Drake, it's not true that he went mad and killed everyone on board. The model's answer is inaccurate, insufficient, and should provide relevant and correct details from the story to answer the question.

**Rationale**: The critique points out that the statement "Roger went mad and killed everyone on board" is inaccurate, but it does not provide specific information on what the correct details are or what should be included in the answer. It mentions that the answer should provide relevant and correct details from the story, but it does not specify what those details are. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique specifies that the factors mentioned in the answer should be omitted because they did not lead to Jerry becoming a serial killer. Additionally, it suggests that the answer should be rewritten in speculative terms since the text does not explicitly state the reasons. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 10/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the cost effectiveness of Aldi?

**Answer**: The secret to Aldi's success is that they offered a few hundred well chosen product lines at low prices and they followed a military style of organization. 

**Critique**: It is omitted that low prices are made possible by massive purchasing. This was combined with a high ratio of sales per square meter of floor space, and ferocious cost control — the latter being Theo’s special skill. Little money was wasted on marketing, and none at all on making Aldi stores look elegant: goods were simply piled up along the aisles in packing cases.


**Rationale**: The critique specifies that the answer should include information about how Aldi's low prices are achieved through massive purchasing, a high ratio of sales per square meter, and ferocious cost control. It also mentions that little money is spent on marketing and store aesthetics, which are additional details that should be added to the answer. This provides specific information on what to change or add to improve the answer.

**Classification**: Constructive

---

### Sample 11/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about de Villa's opinion on public health?

**Answer**: She has urged for the prevention of communicable diseases and wants the brands to clamp down on misleading anti-vaccination information by minimizing the public's access to these rumors. She has also called for a ban on vaccine exemptions if an individual has certain beliefs that say they should not be vaccinated.

**Critique**: Additional detail about how De Villa's whole career is around public health issues should be stated. 

**Rationale**: The critique suggests adding information about De Villa's career focus on public health issues but does not specify what specific details or statements should be included in the answer. It lacks guidance on how to incorporate this information or what specific aspects of her career should be highlighted. Therefore, the critique does not provide enough specific information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

### Sample 12/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Primož's strategic importance.

**Answer**: Primož is part of a ridge which separates the Pivka basin from the Reka valley. It possesses a commanding view over the entire Pivka basin, making it an important military location. During the Second World War, it was fortified with tunnels as part of the Alpine Wall, yet they were never used in combat. In total, the tunnels were more than two kilometers long, but they have since been abandoned. Today, it is made accessible by marked trails, with one specifically designated for tourists and containing numerous information signs around its peak. Primož's strategic importance stems from its commanding view and its military tunnels.

**Critique**: "which separates" - change to "that separates"

**Rationale**: The critique specifies that the phrase "which separates" should be changed to "that separates." This is a specific grammatical correction that can be made directly to the answer without needing additional context or information from the source material.

**Classification**: Constructive

---

### Sample 13/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about what type of alien the creature is?

**Answer**: The narrator describes the creature as an enigma and unlike anything else. it lacks even the slightest hint of movement, yet it commands the attention of every human. Daniel thinks that it looks like melted ice cream. The voices behind the machine tell Daniel that they are messengers, that the creature is one of those who represent them. The creature is multiple creatures and they are here as messengers. It says that Daniel's emissions are a beacon to something or someone dangerous.

**Critique**: Lacking movement only applies to the beginning, so this sentence can be rephrased to reflect that it's situational.

**Rationale**: The critique specifies that the sentence about the creature lacking movement should be rephrased to indicate that this characteristic is only applicable at the beginning, suggesting a situational context. This provides specific guidance on how to adjust the description of the creature's movement in the answer.

**Classification**: Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the tension in the story. 

**Answer**: The tension in the story seems to stem from a fallout between the two main characters. There is also the event that happened three years prior to the story.

**Critique**: The event three years ago, an accident, seems to be the point where the duo separated.

**Rationale**: The critique specifies that the event three years ago was an accident and that it was the point where the duo separated. This provides specific information about what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the narrator remember about Ms. Johnson?

**Answer**: The narrator remembers Ms. Johnson being with her baby while she, Ms. Johnson, and her husband were cleaning the kitchen. She also remembers Ms. Johnson's baby bag and the scar he received after he had jumped out of a window.

**Critique**: The response inaccurately describes Ms. Johnson and her husband cleaning the kitchen. It incorrectly mentions him getting a scar.

**Rationale**: The critique specifies that the description of Ms. Johnson and her husband cleaning the kitchen is inaccurate and that the mention of him getting a scar is incorrect. This provides specific information about what needs to be changed in the answer.

**Classification**: Constructive

---

### Sample 16/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything that happened in the 1990s.

**Answer**: No answer

**Critique**: There were events mentioned in the text that took place in 1996 and 1993.

**Rationale**: The critique mentions that there were events in 1996 and 1993, but it does not specify what those events are or what specifically needs to be added to the answer. Without knowing the specific events, one cannot improve the answer based solely on the critique. Therefore, the critique does not provide enough information to make a specific change or addition to the answer.

**Classification**: Non-Constructive

---

### Sample 17/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Trump's issues with law enforcement?

**Answer**: Trump is at war with his own law enforcement officials. He has backup from his party. The day after Trump's State of the Union address was dominated by an extraordinary series of developments in which the Federal Bureau of Investigation and Department of Justice challenged Trump both on the record and through what appeared to be anonymous leaks to CNN. The Republican attacks have been encouraged by increasingly conspiratorial Fox coverage centred on what hosts have called a "Deep State" attempting to topple Trump.

**Critique**: The answer omits that Trump's allegations are due to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections.

**Rationale**: The critique specifies that the answer should include information about Trump's allegations being related to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections. This provides a specific detail that is missing from the original answer, allowing for a clear improvement without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Rachel?

**Answer**: Rachel seems to be a very carefree and bubbly person. She is not afraid of the man that killed a group of people. She also seems to be open to new people when she meets Josh and Sana.

**Critique**: The answer should mention that Rachel is Devyn's sister

**Rationale**: The critique specifies that the answer should include the information that Rachel is Devyn's sister. This provides a specific detail that needs to be added to the answer, making it clear what change is necessary to improve the response.

**Classification**: Constructive

---

### Sample 19/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text have to say about the traits of the rocket?

**Answer**: It's 230 feet tall, destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space. Its engines will return to Earth following lift-off. The rocket carries Elon Musk's Tesla Roadster into space.

**Critique**: It is not stated: it is destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space.


**Rationale**: The critique points out that the statement "it is destined to deliver more than 50 passengers and cargo" and "the company says it will have the power to launch them into space" are not stated in the text. However, it does not provide specific information on what should be included instead or how to correct the answer. It merely points out what is not stated without suggesting what the correct information should be or what should be added to improve the answer.

**Classification**: Non-Constructive

---

### Sample 20/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the main character's situation changes over the story.

**Answer**: Chad's story begins with him searching through the ship for survivors. He finds the captain, who gives him command of the ship. Chad is in disbelief. He leaves the ship to escape the war.

**Critique**: He doesn't leave the ship.

**Rationale**: The critique specifies that the statement "He leaves the ship to escape the war" is incorrect and should be changed to reflect that Chad does not leave the ship. This provides specific information about what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 21/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the reveal at the end of the story.

**Answer**: Blocker is terminally ill, and the man with glasses tells him he only has a few months left. Blocker then realizes he has been fixated on the carpet, which is the color taupe. He cries.

**Critique**: This could be phrased differently to tie in better with the reveal. It should be said that Blocker only acknowledges this news and cries after he realizes what the color of the carpet is.

**Rationale**: The critique suggests that the phrasing of the answer could be improved to better align with the reveal, but it does not specify exactly how to rephrase the answer or what specific changes should be made. It mentions that Blocker acknowledges the news and cries after realizing the carpet's color, but it does not provide a clear directive on how to incorporate this into the answer. Therefore, the critique lacks specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 22/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: The quote from the mayor of Paris, Anne Hidalgo, suggests that the new rules would get people to exercise when the streets are generally quieter.

**Critique**: This is to stop the spread of COVID-19

**Rationale**: The critique specifies that the motivation behind the exercise ban is to stop the spread of COVID-19. This provides specific information about what the answer should include regarding the motivation, allowing for an improvement without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 23/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Zofia Nehringowa's sport results?

**Answer**: Zofia Nehringowa was a Polish long track speed skater who set a world record in all four individual distances (500 m, 1000 m, 1500 m, 3000 m) in 1931 and 1935. Nehringowa competed at the 1932 European Speed Skating Championships for Men and set a women's world record in the 1500m during these race. Nehringowa represented Poland at the World Allround Speed Skating Championships for Women in 1939 where she finished 5th overall.

**Critique**: In 1931, Nehringowa set the world records in the 500m, 1000m, 1500m, 3000m and 5000m. These results were approved by the ISU's the first women's speed skating world records. In 1932, Nehringowa broke the women's world records in the 1500m and 1000m. In 1935 she improved her own world records in the 3000m, 5000m and 10 000m. Change the response to reflect these results.

**Rationale**: The critique provides specific information about the correct years and distances for which Zofia Nehringowa set world records. It specifies that in 1931, she set world records in the 500m, 1000m, 1500m, 3000m, and 5000m, and that these were the first women's speed skating world records approved by the ISU. It also specifies that in 1932, she broke the women's world records in the 1500m and 1000m, and in 1935, she improved her own world records in the 3000m, 5000m, and 10,000m. This detailed information allows for a precise correction of the original answer.

**Classification**: Constructive

---

### Sample 24/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what happened in the 1940's.

**Answer**: In 1940, Averil Demuth wrote The House in the Mountains. In 1941, she wrote The Enchanted Islands and Sea Gypsies. In 1942, she married Anthony Cockbain. In 1942, he died after only one year of marriage. In 1953, she wrote The House of the Wind.

**Critique**: The last sentence is irrelevant to what is being asked. 

**Rationale**: The critique specifies that the last sentence is irrelevant to the question about the 1940s, indicating that it should be removed or revised to focus only on events from the 1940s. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 25/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator can be described as a keen and careful sergeant in the army with a caring family, who sacrifices his wellbeing as well as that of his men for the greater good. He is valiant and resourceful, and he is committed to his men for the time being, commanding their lives in the shells of their rifles. He is conflicted by the fact that he unwillingly leads the men, who stand shoulder by shoulder to the slaughter with camaraderie, pride, fear, and anger. He also admires his foe, the Germans, for their bravery and tenacity. The narrator is also confident that he will not die with the Germans because he is a lucky man. His spirit dwindles as the Germans begin unleashing massive weaponry and his fellows are being killed left and right. In the end, he falls into the water, where he is saved by the British soldiers.

**Critique**: The listing of these emotions does not make sense given context

**Rationale**: The critique states that "the listing of these emotions does not make sense given context," but it does not specify which emotions are problematic or why they do not make sense. Without specific information about which emotions are incorrect or how they should be changed, it is not possible to improve the answer based solely on this critique. Therefore, the critique does not provide the necessary details to make a specific change or addition to the answer.

**Classification**: Non-Constructive

---

### Sample 26/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why do the police keep almost summoning "Pee Man"?

**Answer**: [rewrite]

**Critique**: No response.

**Rationale**: The critique does not provide any specific information about what to change or add to the answer. It simply states "No response," which does not guide how to improve or rewrite the answer. Without specific feedback or details, it is impossible to know what needs to be corrected or added to the answer.

**Classification**: Non-Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about why Thompson wants to fight Lawler?

**Answer**: Thompson wants to fight Lawler because he believes it would show that he is still in the game and deserves another shot at the title. Thompson believes Lawler is one of the best strikers in the welterweight division.

**Critique**: This is not just a belief. 

**Rationale**: The critique states, "This is not just a belief," but it does not specify what aspect of the answer should be changed or what specific information should be added or corrected. It lacks details on how to improve the answer or what the correct information should be. Therefore, it does not provide enough guidance to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about mental illness?

**Answer**: The man seems to suffer from schizophrenia. He cannot stop staring at the floor, at the time where the story takes place, the carpet. He is found in an institution after a mental breakdown from not being in control of his own life. He isn't able to distinguish what is a hallucination and what isn't. He seems to get lost in it and feels a sense of panic.

**Critique**: The story does not say anything specific about mental illness and the answer's suggestion the main character suffers from schizophrenia is completely unfounded. At best, the main character appears to be a little obsessive in his attempts to identify the color of the carpet, but much of the answer is untrue.

**Rationale**: The critique specifies that the suggestion of schizophrenia is unfounded and that the main character may only appear a little obsessive about identifying the carpet's color. It provides specific feedback that the answer's claim about schizophrenia is incorrect and suggests a more accurate portrayal of the character's behavior. This allows for a clear direction on what to change in the answer.

**Classification**: Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What are the three possible approaches that music directors need to make choices about the instrumental accompaniment?

**Answer**: a capella, instruments doubling the vocal lines, or a basso continuo

**Critique**: A little explanation of the approaches would have made the response much better.

**Rationale**: The critique suggests that the answer could be improved by adding explanations of the approaches, but it does not specify what those explanations should include or how to elaborate on each approach. Without specific guidance on what to add, the critique does not provide enough information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about education?

**Answer**: Elizabeth Benedict is an American author who lives in New York City. She works as a college admissions consultant. She is the founder and president of Don't Sweat the Essay, Inc., which focuses on coaching students for college and graduate school application essays. She attended Barnard College. She has been on the fiction faculty of the New York State Summer Writers Institute, at Skidmore College, since 1997.

**Critique**: The text does not talk about education in general as a subject matter. The question does not specify if it is referring to Benedict's background education.

**Rationale**: The critique points out that the answer does not address the question about education in general, but it does not specify what information should be included to correct this. It highlights a potential misunderstanding of the question but does not provide specific guidance on how to adjust the answer to better address the topic of education. Therefore, it lacks the specificity needed to be constructive.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What are the consequences of the increase in Ebike activity for the company?

**Answer**: The company is having a hard time catching up with the increase in orders. They are also having a hard time with the backlog of emails and phone calls. The increase in ebikes has also led to a backlog in new product development.

**Critique**: The information is not accurate and should reflect that the company is able to keep up with the demand. 

**Rationale**: The critique specifies that the information in the answer should be changed to reflect that the company is able to keep up with the demand, rather than having a hard time catching up. This provides a specific correction to the answer.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the queen changes over the story.

**Answer**: The queen is the wife of the king. She is on a ship with her baby when the ship is struck by lightning, and she and the baby are sent overboard. The dragon, who is one of the humans, saves the baby from the sea, taking it to its home on the island. The dragon takes the queen to save her life, but the king hates her for abandoning the baby. She is a mother who has lost her child, and the king of a country that hates her.

**Critique**: The information relayed in the summary lack coherence as the details are incorrect,

**Rationale**: The critique states that the summary "lack[s] coherence as the details are incorrect," but it does not specify which details are incorrect or how they should be corrected. Without specific guidance on what to change or add, it is not possible to improve the answer based solely on this critique. Therefore, the critique does not provide the necessary information to make the answer more accurate or coherent.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Describe the ways in which the woman fights off her assailant.

**Answer**: The woman first kicks the assailant in the groin and uses the remaining piece of a broken vase to stab the assailant's eye. She is then able to escape from the house and its occupants to save herself and her baby. The altercation on the ground makes the woman realize she has to fight her way out in order to save herself and her baby. She must be proactive and use any means necessary in order to escape her attackers. Although it seems like an uphill battle, she does not give up. She uses her strength and ingenuity to subdue the assailants. She uses whatever is at her disposal to create a way to get out of the situation alive.

**Critique**: The response implies that the baby belongs to the narrator, which is inaccurate.

**Rationale**: The critique specifies that the statement "the baby belongs to the narrator" is inaccurate, indicating that this detail should be corrected in the answer. This provides specific information about what needs to be changed in the response.

**Classification**: Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is this an unusual case?

**Answer**: The timing of the incidents suggests premeditation. Arson attacks in the aftermath of domestic terror attacks are usually carried out when there's backlash against minority communities. The attack occurred in the early morning, which is unusual.

**Critique**: The answer omits that one of the biggest surprises about the attack was that Gurdwara Sahib had a good relationship with the local community.

**Rationale**: The critique specifies that the answer should include the information that one of the biggest surprises about the attack was that Gurdwara Sahib had a good relationship with the local community. This provides specific information about what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 35/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what the narrator has to say about opportunities. 

**Answer**: The narrator has a metaphor where cards represents opportunities in life.

**Critique**: This neglects the rest of what the narrator says about opportunities.

**Rationale**: The critique states that the answer neglects additional information about what the narrator says regarding opportunities, but it does not specify what that additional information is. Without knowing what specific details or aspects are missing, it is not possible to improve the answer based solely on the critique. Therefore, the critique does not provide specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What happens between Lucy and the Stag?

**Answer**: Lucy removed some the stags fur with a piece of his horn while he is asleep. She wraps it over herself. This condemns her to become a doe for a year until she must die. After a year he finds her again, and he lies with her one last time.

**Critique**: "the" - add "of" (of the)

**Rationale**: The critique specifies that the word "of" should be added to correct the phrase "some the stags fur" to "some of the stag's fur." This is a specific change that can be made to improve the answer.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator is a sergeant in the army. He has a caring family and a spouse. He has medals to his name and a desire to live. He is a leader of men. He is a survivor of the war.

**Critique**: It is omitted he was rescued by the British.

**Rationale**: The critique specifies that the answer should include the information that the narrator was rescued by the British. This provides a specific detail that needs to be added to the answer, allowing for improvement without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 38/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Explain how the card turned from blank to displaying the numbers "76".

**Answer**: It probably wasn't him described in the story, but the events taking place could have been the back-story for who Pete met in the end.

**Critique**: This answer doesn't make sense. Additionally, it should say the answer can't be found.

**Rationale**: The critique states that the answer doesn't make sense and suggests that the answer should indicate that the answer can't be found. However, it does not provide specific information on what to change or add to make the answer correct or coherent. It lacks details on how to rewrite the answer to address the question about how the card turned from blank to displaying the numbers "76". Therefore, the critique does not provide enough guidance to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 39/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is it hard for critics to accept that Mikhail Lesin killed himself?

**Answer**: He was the founder of Russia Today, so people wonder if a politics death was being covered up.

**Critique**: "politics" - replace with "political"

**Rationale**: The critique specifies that the word "politics" should be replaced with "political," providing a clear and specific change to improve the grammatical accuracy of the answer.

**Classification**: Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the weather and the number of deaths in Chicago?

**Answer**: In Chicago, a historic and deadly cold snap gripped a wide swath of the nation on Wednesday, fueled by the polar vortex, with temperatures plunging far below zero and wind chill numbers as extraordinary as they are dangerous. The temperature in Chicago tumbled to 21 below Wednesday morning, a record for the date, and closing in on the city's all-time record of minus-27 set in 1985. That record could fall on Thursday.

**Critique**: The highlighted text is a description of the extreme weather affecting a wide swath of the nation, not just "in Chicago", which makes this part of the response contradictory. It should be revised to reflect the fact that Chicago is affected. 

**Rationale**: The critique points out that the answer incorrectly implies that the extreme weather is exclusive to Chicago, whereas the text describes it as affecting a wide swath of the nation. The critique specifies that the answer should be revised to accurately reflect that Chicago is one of the affected areas, not the only one. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: No answer

**Critique**: A response  is possible and necessary

**Rationale**: The critique states that a response is possible and necessary, but it does not specify what the response should include or what specific information is missing. It does not provide any details about what the article says regarding the motivation behind the exercise ban, so it does not guide how to construct the answer. Without specific information on what to add or change, the critique is not constructive.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why does Devyn think that the girls are weird?

**Answer**: Because they don't text a guy who gave Sana his number in the ice cream shop. The girls do not believe in the soulmate idea.

**Critique**: The response should be written as a full sentence. 

**Rationale**: The critique specifies that the response should be rewritten as a full sentence, which provides clear guidance on how to improve the answer's structure.

**Classification**: Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to non-American countries.

**Answer**: France's air accident investigation agency BEA will analyze black-box cockpit voice and data recorders from the crashed plane. France's announcement resolved uncertainty over the fate of the two recorders after Germany's BFU said it had declined a request to handle them because it could not process the new type of recorder used on the 737 MAX jets. Brazil, Mexico, and Panama are the first Latin American nations to suspend the Boeing 737 MAX. Panama's Copa Airlines had suspended operations of its six Boeing 737 MAX 9 aircraft until the findings are published of an investigation into the Sunday's crash.

**Critique**: The question's wording, "non-American countries", should be interpreted as "countries that aren't on a continent named America". Thus, Latin American countries shouldn't be mentioned.

**Rationale**: The critique specifies that the mention of Latin American countries should be removed because the question asks for information about "non-American countries," which should be interpreted as excluding countries on the continents of North and South America. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 44/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Discuss LaFleur's play calls.

**Answer**: LaFleur made several questionable decisions. He had 4th & 2 from the Eagles 13-yard line, with his team leading 10-7. The Packers had been moving up and down the field. LaFleur took a page straight from the Sean McVay playbook and kicked the FG. That gave the Packers a whopping 13-7 lead. Where is the aggression? Why wouldn’t you trust Aaron Rodgers to make a play there? If you fail, you’re still up 10-7. LaFleur made some questionable play-calls.

**Critique**: A lot of the response is lifted from the passage.

**Rationale**: The critique states that "a lot of the response is lifted from the passage," but it does not specify what needs to be changed or added to improve the answer. It does not provide guidance on how to address the issue of content being lifted or suggest any specific modifications to make the answer more original or insightful. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how depression has impacted the narrator's life. 

**Answer**: The narrator has been struggling with depression since the age of 16. They have had suicidal thoughts and have attempted to commit suicide. They have also been diagnosed with psychosis.

**Critique**: He struggles with recovery going through cycles of depression and psychosis. 

**Rationale**: The critique specifies that the answer should include information about the narrator's struggle with recovery, specifically mentioning the cycles of depression and psychosis. This provides specific information on what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 46/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the opinions of the students of Marjory Stoneman Douglas High School?

**Answer**: The students at Marjory Stoneman Douglas High School, where the Parkland shooting occurred, do not agree with the movie and video game industry, placing the blame on the inaction of inactive politicians and the National Rifle Association, demanding gun-control reform.

**Critique**: The first sentence of the answer should be rewritten because it says the students disagree with the movie and video game industry; meanwhile, the text does not indicate such. The model's answer changes the meaning from the text and is inaccurate and should consider correcting this.

**Rationale**: The critique states that the first sentence of the answer is inaccurate because it incorrectly claims that the students disagree with the movie and video game industry. However, it does not provide specific information on what the correct statement should be or how to rewrite the sentence. The critique also mentions that the model's answer changes the meaning from the text and should be corrected, but it does not specify what the corrected information should be. Therefore, the critique does not provide enough specific guidance to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the main news event.

**Answer**: SpaceX is preparing to launch its new rocket, the Falcon Heavy - a rocket which is more powerful than Saturn V. The rocket consists of three Falcon 9 cores and is designed to return to Earth much like the company's solo Falcon 9 flights. It will launch Elon Musk's Tesla Roadster into a helocentric orbit. The KSCVC are predicting this will lead to a new kind of history being made.

**Critique**: It is not stated that the rocket is more powerful than Saturn V, but that it is the most powerful rocket since NASA's Saturn V moon rocket.

**Rationale**: The critique specifies that the statement "more powerful than Saturn V" should be changed to "the most powerful rocket since NASA's Saturn V moon rocket." This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 48/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the issues that are making the narrator depressed.

**Answer**: The narrator's grandmother passed away, and the narrator lost his mother at a young age. He lost his contact with his mother's family. He also lost a dear loved one on January 1st, 2018. The loss of his grandmother and mother caused him to go into depression. He also moved 200 miles away from his hometown of Snoqualmie, Washington, and he lost all his friends and family.

**Critique**: Remove the third sentence, it only confuses the timeline.

**Rationale**: The critique specifies that the third sentence should be removed because it confuses the timeline. This provides a specific action to improve the answer by eliminating a potentially misleading detail.

**Classification**: Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to Ardalent.

**Answer**: Mrs. Cardicole has claimed Lester and Sable. She had also murdered their child. She takes the child back to her apartment and later kills him because she needed to feed her own son.

**Critique**: The response should make it clear that her 'son' is Ardalent.

**Rationale**: The critique specifies that the answer should clarify that Mrs. Cardicole's 'son' is Ardalent. This provides specific information on what to add to the answer to improve its clarity.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the skills needed to become a Russian pop star?

**Answer**: There are no clear indications of the required skills to be a good Russian pop star. However, talent in theater, cinema, TV and music seem to be shown in Napoli's case.

**Critique**: There's no specific answer, so it would be better to leave it at that.

**Rationale**: The critique suggests that the answer should be left as it is because there is no specific information about the skills needed to become a Russian pop star. However, it does not provide any specific guidance on what to change or add to the answer. It merely comments on the lack of specific information without suggesting how to improve the answer or what specific content should be included or removed. Therefore, the critique does not meet the criteria for being constructive, as it does not specify what to change or add.

**Classification**: Non-Constructive

---

