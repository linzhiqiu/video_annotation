# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (summarization)
- **Total Dataset Size**: 4505 critique samples
- **Filtered Dataset Size** (summarization): 1728 critique samples
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
| Constructive | 24 | 48.00% |
| Non-Constructive | 26 | 52.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Answer the following question based on the above passage:

Summarize how the queen changes over the story.

**Answer**: At the beginning of the story, the queen has a fatal accident while helping the crew get everyone to safety. The king is upset that she was a distraction and almost died because of it. However, later the king and the crew are impressed by her bravery in rescuing their daughter. She underwent a complete character change over the course of the story.

**Critique**: All the key events mentioned in the response are wrong.

**Rationale**: The critique states that "all the key events mentioned in the response are wrong," but it does not specify what the correct events are or what specific information should replace the incorrect details. Without knowing what the correct events are, it is impossible to improve the answer based solely on this critique. Therefore, the critique does not provide specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Answer the following question based on the above passage:

What parts of the book does the reviewer David Mumford call out as exceeding the abilities of a novice?

**Answer**: The first seven chapters.

**Critique**: The first seven chapters of the book are suitable for an undergraduate, but as a whole the book is best suited for graduate students. 

**Rationale**: The critique does not specify what to change or add to the answer. It provides additional information about the suitability of the book for different audiences but does not directly address or correct the original answer regarding which parts of the book exceed the abilities of a novice. Without specific guidance on what to change in the answer, it is not possible to improve it based solely on the critique.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Summarize resources for Australians to call up when their animals friends are in distress. 

**Answer**: The article recommends calling your local vet as well as your local wildlife group for help. It also recommends saving a few local wildlife rescue contacts in your phone so that you can ring for advice if you need it.

**Critique**: The second sentence is irrelevant.

**Rationale**: The critique states that the second sentence is irrelevant, but it does not specify what should be changed or removed from the sentence. It does not provide specific guidance on how to improve the answer or what specific information is incorrect or unnecessary. Therefore, the critique does not provide enough information to make a specific change to the answer without referring back to the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Answer the following question based on the above passage:

Discuss Pederson's role in the Eagle's comeback.

**Answer**: Eric Karabils mentions that Pederson was able to reel in the passing game thanks to Wentz. This was done to improve Wentz's time-to-throw. Wentz worked a short, quicker game with a heavy dose of RPOs that require high-speed decision-making.

**Critique**: It is not stated that Eric Karabils mentions that Pederson was able to reel in the passing game thanks to Wentz.


**Rationale**: The critique points out that the answer incorrectly attributes a statement to Eric Karabils, specifically that he mentions Pederson's ability to reel in the passing game thanks to Wentz. However, the critique does not provide the correct information or specify what should be stated instead. It only indicates that the current attribution is incorrect without suggesting what the accurate statement should be. Therefore, the critique does not provide enough information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the text say about the difference in the competence of peer reviewers?


**Answer**: The text states that there is a "sweet spot" where the average peer review competency must be greater than a certain threshold to ensure high quality content. The text also states that the Peer Review System will more intelligently match peer reviewers in order to ensure that they collectively have a higher average peer review competency. Therefore, the text says that peer reviewers need to be more competent in order to create better quality content.

**Critique**: In this response, it is important to note that not all writers and peer reviewers are equally competent. 

**Rationale**: The critique mentions that it is important to note that not all writers and peer reviewers are equally competent. However, it does not specify what specific information should be added or changed in the answer to address this point. It lacks guidance on how to incorporate the idea of varying competence levels among writers and peer reviewers into the existing answer.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Answer the following question based on the above passage:

Why did Beverly Duan donate to charity in China during the COVID-19 pandemic?

**Answer**: It is possible that she was born in China and moved to America.

**Critique**: There is no evidence that Duan might have been born in China. The passage mentions she was born in California.

**Rationale**: The critique specifies that the statement "she was born in China" is incorrect and provides the correct information that "she was born in California." This allows for a specific correction to be made to the answer.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique specifies that the factors mentioned in the answer should be omitted because they did not lead to Jerry becoming a serial killer. Additionally, it provides guidance on how the answer should be framed, suggesting that it should be in speculative terms since the information is not explicitly stated in the text. This gives clear direction on what to change and how to approach the revision.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

What does the text say about Faccio's early career?

**Answer**: Mara Faccio started her early career as Assistant Professor of Finance at the UniversitŠ Cattolica del Sacro Cuore in Milan in 1999. In 2001, she moved to the Mendoza College of Business at the University of Notre Dame and the Owen Graduate School of Management at Vanderbilt University in 2003. In 2007, she became a full professor at Purdue University.

**Critique**: "UniversitŠ" should be "Università".

**Rationale**: The critique specifies that the word "UniversitŠ" should be changed to "Università," providing a clear and specific correction to the text. This allows for the improvement of the answer without needing to refer back to the source material.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

Summarize the controversy surrounding Shanahan.

**Answer**: Patrick Shanahan and his second wife had a domestic dispute in 2010. UTM disputes established that the wife had assaulted Shanahan. He also sought legal assistance in repairing his son's reputation after his son had been associated with domestic violence regarding his mother.

**Critique**: It is omitted that after the 2010 incident, Shanahan and then-wife Kimberley both told police the other punched them. Shanahan denied the allegations.

**Rationale**: The critique specifies that the answer should include the information that after the 2010 incident, both Shanahan and his then-wife Kimberley told police that the other punched them, and that Shanahan denied the allegations. This provides specific details that need to be added to the answer to make it more complete and accurate.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the text say about Kirkland's amateur career?

**Answer**: Kirkland played golf from the age of seven. She was semi-finalist in the Girls Amateur Championship in 2001. She was a member of the Arizona Wildcats women's golf team at the University of Arizona, winning the UNLV Invitational and was a member of the NGCA All American Team in 2005.

**Critique**: Add that she was All-PAC 10 Team and won the Golfstat award for par-five scoring leader in 2004 and 2005

**Rationale**: The critique specifies that the answer should include that Kirkland was part of the All-PAC 10 Team and that she won the Golfstat award for par-five scoring leader in 2004 and 2005. This provides specific information on what to add to the answer to make it more complete.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the narrator have to say about single parenthood? 

**Answer**: The narrator's mother raised her alone. She admits that the hardest part of being a single mother is the lack of support but she proudly mentions her daughter's strength and tenacity that she got from seeing her mother excel in life despite not having a father as a support.

**Critique**: The response should be reworded for clarity on who is the mother.

**Rationale**: The critique suggests that the response should be reworded for clarity regarding the identity of the mother. However, it does not specify how to reword it or what specific information is unclear about who the mother is. Without specific guidance on what to change or how to improve clarity, the critique does not provide enough information to make the necessary adjustments to the answer. Therefore, the critique does not meet the criteria for being constructive.

**Classification**: Non-Constructive

---

### Sample 2/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about some of the issues SČH faced during its time?

**Answer**: The members began operating more or less on their own because they were initially untied to any trade union centre. The union bound themselves closer to the Czechoslovak Socialist Party as it faced police repression. As many miners were arrested and the union was increasingly dependent on the Czechoslovak Socialist Party.

**Critique**: It is omitted that its members struggled with economic hardship.

**Rationale**: The critique specifies that the answer should include information about the members struggling with economic hardship. This provides a specific detail that needs to be added to improve the answer.

**Classification**: Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything related to Samoa. 

**Answer**: Arthur Whistler was an ethnobotanist, academic and writer who focused on the flora of Samoa and Tonga. He had first lived in Samoa during the 1970s and trained Samoans on the country's flora and its uses. He authored more than a dozen books on the botany and ethnobotany of Samoa and the Pacific Islands. Whistler died in April 2020 at the age of 75 due to COVID-19. His death was Hawaii's third fatality related to the COVID-19 pandemic. His most famous work is the definitive guide to Samoa's native plants, "Flora of Samoa."

**Critique**: Whistler's death is irrelevant.

**Rationale**: The critique specifies that the information about Whistler's death is irrelevant to the summary of everything related to Samoa. This suggests that the mention of his death should be removed from the answer to focus solely on the relevant aspects of Samoa, such as his contributions to the study of its flora.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Trump's issues with law enforcement?

**Answer**: Trump is at war with his own law enforcement officials. He has backup from his party. The day after Trump's State of the Union address was dominated by an extraordinary series of developments in which the Federal Bureau of Investigation and Department of Justice challenged Trump both on the record and through what appeared to be anonymous leaks to CNN. The Republican attacks have been encouraged by increasingly conspiratorial Fox coverage centred on what hosts have called a "Deep State" attempting to topple Trump.

**Critique**: The answer omits that Trump's allegations are due to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections.

**Rationale**: The critique specifies that the answer should include information about Trump's allegations being related to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections. This provides a specific detail that is missing from the original answer, allowing for a clear improvement without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 5/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What other organizations can be inspired or learn from the Mechanics Educational Society of America?

**Answer**: The Mechanics did not affiliate with any major union for many years. Another independence was beneficial for the survival of the young union and its members. However, by the end of WWII, the Mechanics found a need to affiliate with a larger organization. It was necessary to be affiliated with an international union rather than national one. It was also wise to be a part of a larger labor movement.

**Critique**: The response seems to be critiquing the MESA and not answering the question.

**Rationale**: The critique states that the response is critiquing the Mechanics Educational Society of America (MESA) instead of answering the question about what other organizations can be inspired or learn from MESA. However, it does not specify what the answer should include or what specific information is missing to address the question properly. It lacks guidance on how to redirect the focus of the answer to meet the question's requirements. Therefore, the critique does not provide specific information on what to change or add to improve the answer.

**Classification**: Non-Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What occupation must the president's lawyer have in today's time?

**Answer**: It must be someone who is well versed in legal matters and can handle the president's case in court.

**Critique**: This isn't an occupation. It would just be better to point out that the question is confusing, as the president's lawyer is already a lawyer.

**Rationale**: The critique points out that the answer does not directly address the question about the occupation of the president's lawyer, as it simply describes the qualities of a lawyer rather than naming an occupation. However, the critique does not specify what the answer should say or what specific change should be made to improve it. It suggests that the question is confusing but does not provide a clear direction for how to correct the answer. Therefore, the critique does not provide specific information on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the successes of the Chickasha baseball teams.

**Answer**: The Chickasha Chicks were successful in 1921 winning the Western Association. They were also successful the following year winning the Oklahoma State League. They qualified twice for the playoffs and won both times. Chickasha also was successful again in 1966 playing in the Southwestern League beating the Duncan Oilers.

**Critique**: The response inaccurately mentions Chickasha qualified twice for the playoffs, however they actually qualified multiple times, but only winning twice.

**Rationale**: The critique specifies that the answer inaccurately states Chickasha qualified twice for the playoffs, and it should be corrected to indicate that they qualified multiple times but only won twice. This provides specific information on what needs to be changed in the answer.

**Classification**: Constructive

---

### Sample 8/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Sabrina's relationship with the man that enters her hotel room?

**Answer**: Sabrina is a drug addict who uses the razor blade to cut her arm. The man that enters her hotel room is her drug dealer. He tells her that he woke up and found all his drugs and money gone. He asks her what she did with them. Sabrina does not know what he is talking about but she remembers the razor blade on her bed.

**Critique**: Remove the references to Sabrina's self-harming behavior and the razor blade used to accomplish this. It does not have bearing on the question.

**Rationale**: The critique specifies that the references to Sabrina's self-harming behavior and the razor blade should be removed because they do not pertain to the question about her relationship with the man who enters her hotel room. This provides specific guidance on what content to eliminate to improve the answer's relevance to the question.

**Classification**: Constructive

---

### Sample 9/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

How did the writer compose the structure of this informative article's narrative?

**Answer**: [rewrite]

**Critique**: "No answer" would be more appropriate

**Rationale**: The critique suggests that "No answer" would be more appropriate, but it does not provide specific information on what the answer should say or what specifically needs to be fixed. It does not guide how to rewrite the answer or what elements of the structure should be addressed or omitted. Therefore, it does not meet the criteria for being constructive, as it lacks specific guidance for improvement.

**Classification**: Non-Constructive

---

### Sample 10/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Kirkland's amateur career?

**Answer**: Kirkland played golf from the age of seven. She was semi-finalist in the Girls Amateur Championship in 2001. She was a member of the Arizona Wildcats women's golf team at the University of Arizona, winning the UNLV Invitational and was a member of the NGCA All American Team in 2005.

**Critique**: Add that she was All-PAC 10 Team and won the Golfstat award for par-five scoring leader in 2004 and 2005

**Rationale**: The critique specifies that the answer should include that Kirkland was part of the All-PAC 10 Team and that she won the Golfstat award for par-five scoring leader in 2004 and 2005. This provides specific information on what to add to the answer to make it more complete.

**Classification**: Constructive

---

### Sample 11/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Gary's job?

**Answer**: Gary works in an office. He is stressed out by his job and daydreams about quitting it. He wants to be a bartender.

**Critique**: It is omitted that his job is well-paid. 

**Rationale**: The critique specifies that the answer should include the information that Gary's job is well-paid. This provides specific information about what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 12/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What specific part of the performing arts did Fott gravitate towards?

**Answer**: When Fott was young, he was fascinated with The Muppets on Sesame Street and his. He has pursued theatre, puppeteering, and directing. He is also an actor.

**Critique**: The answer should state that Fott was drawn toward the performing arts.

**Rationale**: The critique does not specify what to change or add to the answer. It merely suggests that the answer should state that Fott was drawn toward the performing arts, which is already implied by the mention of theatre, puppeteering, directing, and acting. The critique does not provide specific information on what to change or add to improve the answer.

**Classification**: Non-Constructive

---

### Sample 13/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about making the documentary The Secret Policeman?

**Answer**: It was a documentary about an undercover reporter that reveals racism among police recruits in Manchester, England. 

**Critique**: The response should be much more specific and include more details. 

**Rationale**: The critique states that the response should be "much more specific and include more details," but it does not specify which details are missing or what specific information should be added to improve the answer. Without guidance on what specific details to include, the critique does not provide enough information to make the necessary improvements to the answer. Therefore, the critique does not meet the criteria for being constructive.

**Classification**: Non-Constructive

---

### Sample 14/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What parts of the book does the reviewer David Mumford call out as exceeding the abilities of a novice?

**Answer**: The first seven chapters.

**Critique**: The first seven chapters of the book are suitable for an undergraduate, but as a whole the book is best suited for graduate students. 

**Rationale**: The critique does not specify what to change or add to the answer. It provides additional information about the suitability of the book for different audiences but does not directly address or correct the original answer regarding which parts of the book exceed the abilities of a novice. Without specific guidance on what to change in the answer, it is not possible to improve it based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Primož in the present day.

**Answer**: Primoš is located in a highly populated urban area. There are a number of tourist trails leading to the peak, and there is a Pivka Park of Military History.

**Critique**: "Primoš is located in a highly populated urban area." - this statement cannot be confirmed because it is not in the text. The spelling of Primož is also incorrect.

**Rationale**: The critique specifies that the statement "Primoš is located in a highly populated urban area" cannot be confirmed because it is not in the text, indicating that this part of the answer should be revised or removed. Additionally, the critique points out the incorrect spelling of "Primož," which should be corrected. These specific changes provide clear guidance on what needs to be fixed in the answer.

**Classification**: Constructive

---

### Sample 16/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about Curzon's grandchildren?

**Answer**: He had four daughters, but no sons. His eldest daughter Anne Mildred Curzon married Major W. J. L. Willson, and had two sons and a daughter. His second daughter Gloria Mary Curzon married J. G. Bearman, and had two sons. His third daughter Juliana Eveline Curzon married firstly G. D. S. Smith, and had two daughters and a son. She was later married to Frederick Nettleford, Sir Dudley Cunliffe-Owen, and John Roberts. His youngest daughter Diana Geraldine Curzon married firstly Frederick Nettleford, and later married John Roberts.

**Critique**: The last sentence is inaccurate. It repeats the names of Juliana Curzon's spouses. The article also did not mention Diana Curzon's spouse or child. This error should be corrected.

**Rationale**: The critique specifies that the last sentence of the answer is inaccurate because it repeats the names of Juliana Curzon's spouses instead of providing information about Diana Curzon's spouse or child. It also indicates that the article did not mention Diana Curzon's spouse or child, suggesting that this information should be added. This provides specific guidance on what needs to be corrected and added to the answer.

**Classification**: Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the story ends.

**Answer**: The narrator has a loaded gun placed to their head by their former brother. He is killed with the former brother backing out of shooting him. The war had political implications and because of it, the narrator survived, leaving the battlefield. However, even at home, music and media isn't as kind as it would be to a law-abiding citizen. The conflict ended but the past lingers in the minds of those who fought in it.

**Critique**: Everything beyond the first sentence is inaccurate..

**Rationale**: The critique states that "everything beyond the first sentence is inaccurate," but it does not specify what the correct information should be or what specifically needs to be changed in the answer. Without details on what is inaccurate or what the correct information is, the critique does not provide enough guidance to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize all the information relating to the mountainous Austrian Tyrol.

**Answer**: Averil Demuth's first story was set in the Austrian Tyrol. The girl Trudi, the boy Hansel, the cow Lotti, the dog Berni, the hen Griselda and the raven Kraak all go up the mountain to see Riese the giant, and then all come down again. Eleanor Farjeon gave the book a positive review. The House in the Mountains was also set in the Austrian Tyrol.

**Critique**: The sentence is unnecessary.

**Rationale**: The critique states that "The sentence is unnecessary," but it does not specify which sentence is unnecessary or why it should be removed. Without knowing which part of the answer is considered unnecessary, it is impossible to make a specific change or improvement based on the critique alone. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 19/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about damage types?

**Answer**: There are three physical damage types: Impact, Puncture, and Slash. Physical damage come in ten elemental damage types: four base elements and the six combinations formed by modding two elements together. Elemental damage types are stronger or weaker versus certain enemy types. The physical damage types also have "status effects" that can be applied via a "procedural random chance" percentage, often known as procs. Impact procs make enemies suffer a dramatic stagger, Puncture procs reduce enemies' damage output by a flat 30%, and Slash procs inflict "bleed" damage over time. Slash is considered the most powerful procs from all of the physical damage types.

**Critique**: The response contains inaccurate information.

**Rationale**: The critique states that the response contains inaccurate information but does not specify what information is inaccurate or what the correct information should be. Without specific details on what to change or correct, the critique does not provide actionable guidance for improving the answer. Therefore, it is not possible to improve the answer based solely on this critique without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 20/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique specifies that the factors mentioned in the answer should be omitted because they did not lead to Jerry becoming a serial killer. Additionally, it provides guidance on how the answer should be framed, suggesting that it should be in speculative terms since the information is not explicitly stated in the text. This gives clear direction on what to change and how to approach the revision.

**Classification**: Constructive

---

### Sample 21/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about de Villa's qualifications?

**Answer**: She received her medical degree at the University of Toronto in 1998. She also has a Master of Health Science degree in Health Promotion at the University of Toronto. She has a Master of Business Administration from Schulich School of Business at York University. She is an adjunct professor at the Dalla Lana School of Public Health of the University of Toronto.

**Critique**: It is omitted that she attended Havergal College then McGill University, where she received her Bachelor of Science degree in psychology and women's studies in 1991.

**Rationale**: The critique specifies that the answer should include the information that de Villa attended Havergal College and McGill University, where she received her Bachelor of Science degree in psychology and women's studies in 1991. This provides specific details that need to be added to the answer to make it more complete regarding de Villa's qualifications.

**Classification**: Constructive

---

### Sample 22/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about damage-scaling procs?

**Answer**: In an update coming soon, the developers will be making changes to IPS status effects and proc damage calculation. The primary goal is to improve Impact and Puncture. Both of these procs will now scale in effectiveness, based on the damage dealt. An Impact proc with a small damage output will still only cause a short stagger, while an Impact proc with high damage output can scale all the way up to a ragdoll. Puncture procs will now scale in effectiveness from 10% to 75% damage reduction, based on the damage dealt at the time of proc. Slash will continue working as it does now, stacking multiple status effects on top of one another.

**Critique**: The last line is not relevant.

**Rationale**: The critique states that "The last line is not relevant," but it does not specify what should be done with the last line. It does not indicate whether the line should be removed, revised, or replaced with different information. Without specific guidance on what to change or add, the critique does not provide enough information to improve the answer based solely on the critique itself.

**Classification**: Non-Constructive

---

### Sample 23/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the role of Kristine Lucius in the news.

**Answer**: Kristine Lucius is the executive vice president for policy and government affairs at the Leadership Conference. According to the passage, she criticized Senate Republicans for getting through young, unqualified conservative judges too quickly. She also said the judges are likely to dismantle reproductive rights, marriage equality, and the separation of church and state.

**Critique**: The answer omits Lucius' criticism that two of the judges wouldn't state that they agreed with the Brown v. Board of Education 1954 Supreme Court decision that ruled racial segregation of public schools unconstitutional.

**Rationale**: The critique specifies that the answer should include Lucius' criticism regarding two judges who wouldn't state their agreement with the Brown v. Board of Education 1954 Supreme Court decision. This provides specific information about what to add to the answer.

**Classification**: Constructive

---

### Sample 24/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the woman the narrator loves?

**Answer**: The narrator refers to the woman he loves as mac. Mac is someone that almost seems like a mythological figure. She progressed in their relationship, which was followed by ups and downs. Inadvertently, the narrator realized that each day with her was the best day of his life. He enjoyed stockpiling a million glances of her beautiful eyes. Initially, he accepted that they would live happily aware. However, over time they had less microscopic moments. They drifted apart but the narrator wished that things went better in the end.

**Critique**: This is inaccurate

**Rationale**: The critique states that the answer is "inaccurate," but it does not specify what part of the answer is incorrect or what specific information should be changed or added. Without details on what is inaccurate, it is not possible to improve the answer based solely on the critique. Therefore, the critique does not provide the necessary guidance to make a specific correction or addition to the answer.

**Classification**: Non-Constructive

---

### Sample 25/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what the article has to say about voter fraud. 

**Answer**: The author submits and maintains that voter fraud is a possibility in many states for reasons that the author largely attributes to Democrat policies. Factors like allowing immigrants who don't yet have a legal status in this country to obtain driver's licenses contribute to voter fraud, according to the author. This is because one can vote online in a whopping 38 states. 

**Critique**: 38 states allow or will allow soon for registering to vote, not online voting.

**Rationale**: The critique specifies that the statement about "38 states" should refer to registering to vote, not online voting. This provides a specific correction to the information presented in the answer.

**Classification**: Constructive

---

### Sample 26/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What there any personal vendetta involved in the investigation of the Trump campaign and its links with Russia?

**Answer**: The FBI agent and lawyer who exchanged private text messages during the campaign that were disparaging of Trump were on Mueller's special counsel team at one point before being reassigned.

**Critique**: It would be better to use speculative terms in this answer, since it's not concrete that there was a personal vendetta.

**Rationale**: The critique suggests using speculative terms in the answer but does not specify which terms to use or how to rephrase the answer to incorporate speculation. It lacks specific guidance on what to change or add to make the answer more speculative. Therefore, it does not provide enough information to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Discuss Pederson's role in the Eagle's comeback.

**Answer**: Eric Karabils mentions that Pederson was able to reel in the passing game thanks to Wentz. This was done to improve Wentz's time-to-throw. Wentz worked a short, quicker game with a heavy dose of RPOs that require high-speed decision-making.

**Critique**: It is not stated that Eric Karabils mentions that Pederson was able to reel in the passing game thanks to Wentz.


**Rationale**: The critique points out that the answer incorrectly attributes a statement to Eric Karabils, specifically that he mentions Pederson's ability to reel in the passing game thanks to Wentz. However, the critique does not provide the correct information or specify what should be stated instead. It only indicates that the current attribution is incorrect without suggesting what the accurate statement should be. Therefore, the critique does not provide enough information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about Asaddor Ali's accomplishments?

**Answer**: Ali was awarded the Bangla Academy Literary Award in 2004. He was also awarded the Ragib-Rabeya Literary Award in 2001. On December 20, 2004, he was awarded the KEMUSAS Literary Award.

**Critique**: The answer could also touch on some of the organizations he helped found.

**Rationale**: The critique suggests adding information about the organizations that Asaddor Ali helped found. However, it does not specify which organizations these are or provide any details about them. Without this specific information, it is not possible to improve the answer based solely on the critique. Therefore, the critique does not provide enough detail to be considered constructive.

**Classification**: Non-Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize resources for Australians to call up when their animals friends are in distress. 

**Answer**: The article recommends calling your local vet as well as your local wildlife group for help. It also recommends saving a few local wildlife rescue contacts in your phone so that you can ring for advice if you need it.

**Critique**: The second sentence is irrelevant.

**Rationale**: The critique states that the second sentence is irrelevant, but it does not specify what should be changed or removed from the sentence. It does not provide specific guidance on how to improve the answer or what specific information is incorrect or unnecessary. Therefore, the critique does not provide enough information to make a specific change to the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the difference in the competence of peer reviewers?


**Answer**: The text states that there is a "sweet spot" where the average peer review competency must be greater than a certain threshold to ensure high quality content. The text also states that the Peer Review System will more intelligently match peer reviewers in order to ensure that they collectively have a higher average peer review competency. Therefore, the text says that peer reviewers need to be more competent in order to create better quality content.

**Critique**: In this response, it is important to note that not all writers and peer reviewers are equally competent. 

**Rationale**: The critique mentions that it is important to note that not all writers and peer reviewers are equally competent. However, it does not specify what specific information should be added or changed in the answer to address this point. It lacks guidance on how to incorporate the idea of varying competence levels among writers and peer reviewers into the existing answer.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what happens when the narrator steps out of his house.

**Answer**: He sees a man in a postal uniform waiting for a few signatures.

**Critique**: Doesn't mention receiving the parcel full of memories from their friend. 

**Rationale**: The critique specifies that the answer should include the detail about receiving a parcel full of memories from their friend. This provides specific information on what to add to the answer to make it more complete and accurate.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about internet research?

**Answer**: The narrator was keen to learn about dentistry, so he decided to look it up on the internet. He watched a few videos, which were not for the faint of heart. The narrator was horrified by what he saw. He now goes to the dentist regularly. He decided to look up dentistry after learning that there was a void in the at-home orthodontist video market.

**Critique**: There is no answer to the question. The text does not focus on "internet search" as a subject matter. 

**Rationale**: The critique states that the answer does not address the question about "internet research" and that the text does not focus on this subject matter. However, it does not specify what the answer should include or how it should be changed to address the question correctly. It lacks specific guidance on what information related to "internet research" should be included or corrected in the answer. Therefore, the critique does not provide enough information to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the controversy surrounding Shanahan.

**Answer**: Patrick Shanahan and his second wife had a domestic dispute in 2010. UTM disputes established that the wife had assaulted Shanahan. He also sought legal assistance in repairing his son's reputation after his son had been associated with domestic violence regarding his mother.

**Critique**: It is omitted that after the 2010 incident, Shanahan and then-wife Kimberley both told police the other punched them. Shanahan denied the allegations.

**Rationale**: The critique specifies that the answer should include the information that after the 2010 incident, both Shanahan and his then-wife Kimberley told police that the other punched them, and that Shanahan denied the allegations. This provides specific details that need to be added to the answer to make it more complete and accurate.

**Classification**: Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How does the story reflect its genre?

**Answer**: It is the story of a typical day for a fry cook. The story has supernatural elements, such as the mysterious man who gives the protagonist a large sum of money.

**Critique**: Include that the gifts come at a price, which is the main driving point of the story.

**Rationale**: The critique specifies that the answer should include the information that the gifts come at a price, which is the main driving point of the story. This provides specific guidance on what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 35/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Beverly Duan donate to charity in China during the COVID-19 pandemic?

**Answer**: It is possible that she was born in China and moved to America.

**Critique**: There is no evidence that Duan might have been born in China. The passage mentions she was born in California.

**Rationale**: The critique specifies that the statement "she was born in China" is incorrect and provides the correct information that "she was born in California." This allows for a specific correction to be made to the answer.

**Classification**: Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator's thoughts on their King?

**Answer**: The village the narrator lives in doesn't have the best facilities, with their castle appearing to be in disrepair at best and there is no way to trade with the outside world. The narrator is an inquisitive type, always trying to learn more about their King and why they live so differently to the rest of the people of the kingdom. The narrator respects their King but is dissatisfied with how things are. When the narrator finally gets their chance, they ask simple questions, but the King speaks at length to the player, excusing his manner as slightly eccentric but his character and behaviors are as normal as any other human. That changes when the narrator goes adventuring with their King and come to realise the other side of things - this isn't "real", this is a game, and human lives are just tracks of existence which vanish when the person in the game is permanently killed or feels the need to leave. The narration is a first-person viewpoint shot from the person playing the game (their character), speaking from their perspective in the game.

**Critique**: Remove the first sentence because it contains false information.

**Rationale**: The critique specifies that the first sentence of the answer contains false information and should be removed. This provides a specific action to take, which is to delete the first sentence of the answer. The critique clearly identifies what needs to be changed, making it possible to improve the answer based solely on the critique without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about vaporizers?

**Answer**: The text talks about how the protagonist uses a vaporizer to calm nerves and fill a hole in their life. It mentions that the protagonist initially feels nothing but more placid and lethargic after using the vaporizer. The text also talks about how the protagonist wishes they could transcend their body and live amongst the stars. The text implies that the protagonist believes that vaporizers could be a helpful tool to make this happen.

**Critique**: The last two sentences are unnecessary. There is no evidence in the text that the narrator believes that the vaporizer will help him transcend their body.

**Rationale**: The critique specifies that the last two sentences of the answer are unnecessary because there is no evidence in the text to support the claim that the narrator believes the vaporizer will help them transcend their body. This provides specific guidance on what to remove from the answer.

**Classification**: Constructive

---

### Sample 38/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the queen changes over the story.

**Answer**: At the beginning of the story, the queen has a fatal accident while helping the crew get everyone to safety. The king is upset that she was a distraction and almost died because of it. However, later the king and the crew are impressed by her bravery in rescuing their daughter. She underwent a complete character change over the course of the story.

**Critique**: All the key events mentioned in the response are wrong.

**Rationale**: The critique states that "all the key events mentioned in the response are wrong," but it does not specify what the correct events are or what specific information should replace the incorrect details. Without knowing what the correct events are, it is impossible to improve the answer based solely on this critique. Therefore, the critique does not provide specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 39/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the possible messages hidden in the narrator's dreams about the girl?

**Answer**: The narrator's first dream where the girl spoke to him was probably meant to show him that she was already spoken for and happy with her life. The girl appeared to have a husband and two kids. They all looked so happy, with no troubles in the world. The narrator's second dream was probably meant to tell him "that's life" and he should move on with his.

**Critique**: This is confusing. It sounds as though he had dreamt that the girl had a husband. 

**Rationale**: The critique points out that the answer is confusing because it seems to suggest that the narrator dreamt the girl had a husband. However, it does not specify what exactly should be changed or how to clarify the confusion. It does not provide specific guidance on what the answer should say to improve clarity. Therefore, the critique does not provide enough information to make a specific change to the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What are some related fields to circle packing?

**Answer**: Some related fields are sphere packing, which considers higher dimensions (here, everything is two dimensional) and is more focused on packing density than on combinatorial patterns of tangency.

**Critique**: This answer could also mention the theory of conformal maps and conformal geometry.

**Rationale**: The critique specifies that the answer should mention the theory of conformal maps and conformal geometry as related fields to circle packing. This provides specific information about what to add to the answer to improve it.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything related to Arthur Whistler's homes.

**Answer**: Arthur Whistler was born in San Bernardino County, California and earned a bachelor's degree in Biology from UC Riverside. He went on to serve in the Peace Corps and then move to Hawaii where he completed a doctorate in botany focusing on Samoan plant life. Whistler was an adjunct professor at the Department of Botany at the University of Hawaii and owned a consulting company. His death in April 2020 was the third fatality related to COVID-19 in Hawaii. At the time of his death, he had nearly completed another book called Flora of Samoa which focused on Samoa's native plants.

**Critique**: The article doesn't mention anything about Whistler's homes.

**Rationale**: The critique points out that the answer does not address the specific topic of Arthur Whistler's homes, which is what the question asked for. However, it does not provide any specific information about what should be included regarding his homes or what details are missing. Therefore, it does not guide how to correct or improve the answer to address the question properly.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What are some related fields to circle packing?

**Answer**: The theory of conformal maps and conformal geometry are related. It has similarities to the analytical functions of classical mathematical analysis. These similarities can be applied to number theory and the visualizations of the brain's structure.

**Critique**: The later part of the response cannot be verified from the original article.

**Rationale**: The critique states that the later part of the response cannot be verified from the original article, but it does not specify what exactly is incorrect or what should be changed or added. It lacks specific guidance on how to improve the answer or what information is missing or incorrect. Therefore, it does not provide enough detail to make improvements without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 43/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the theme of moving on?

**Answer**: The narrator is moving out of her apartment and thinks about what she'll take and what she'll leave. She thinks about her relationship with her boyfriend and wonders if she's been a good partner. She wonders if she's been a good friend and if she's been a good daughter. She's moving on, but she's not sure what's next for her.

**Critique**: The first sentence is irrelevant to the theme of moving on. 

**Rationale**: The critique points out that the first sentence of the answer is irrelevant to the theme of moving on. However, it does not specify what should be changed or added to make the answer more relevant to the theme. It does not provide specific guidance on how to improve the answer in relation to the theme of moving on. Therefore, the critique does not provide enough information to improve the answer without re-reading the source material.

**Classification**: Non-Constructive

---

### Sample 44/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what happened to Alexa, and why she sent the narrator the packages.

**Answer**: The narrator has woken up after a sweet dream. He kisses his father, takes his camera with him on his way, and goes to school. When he comes back home, he finds a man on the door delivering packages. He decides to open one and finds memories of his childhood friend, a box, and a letter. He's shocked that she sent him her diary, but realizes the letter is for him to read first. She tells him about her journey battling cancer, the flashes of messages that he inspired, and how she loves him. The narrator realizes how fleeting life is, and how life might have been different if he were her or she were him.

**Critique**: The narrator's day before he gets the box is fake.

**Rationale**: The critique states that "The narrator's day before he gets the box is fake," but it does not specify what specifically needs to be changed or what the correct information should be. It lacks details on what part of the narrator's day is inaccurate or how it should be corrected. Therefore, the critique does not provide enough information to improve the answer without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Qonqurtai's early life? 

**Answer**: Qonqurtai was born to Hulagu Khan and Ajuja Aguchi, his Khitan concubine wife. He was Hulagu's ninth son and was the senior commander during the reign of his brother Abaqa.

**Critique**: Being senior commander is not part of his early life and should be omitted.

**Rationale**: The critique specifies that the information about Qonqurtai being a senior commander is not relevant to his early life and should be omitted from the answer. This provides a clear and specific instruction on what to change in the answer.

**Classification**: Constructive

---

### Sample 46/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Kirkland's professional career?

**Answer**: Kirkland was a golfer who played on the Ladies European Tour and won the Sanya Ladies Open in 2012. She also had success in college, winning the UNLV Invitational, being on the NGCA All American Team and being named All-PAC 10 Team. Following her diagnosis with cancer in 2015, she fought a two-year battle before dying at the age of 32.

**Critique**: The response includes mostly extraneous information that is not useful for the task.

**Rationale**: The critique states that the response includes mostly extraneous information but does not specify which parts of the information are extraneous or what should be included instead. It lacks specific guidance on what to change or remove from the answer. Without knowing which details are considered extraneous, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the origins of the Mechanics Educational Society of America. 

**Answer**: The Mechanics Educational Society of America is founded by disgruntled members of the International Association of Machinists as an educational society. However, radical transplants from the United Kingdom like Smith, Frank McCracken, and John Anderson recognized the potential of the group and pushed for a full-fledged union.

**Critique**: This should be past tense.

**Rationale**: The critique specifies that the answer should be in past tense, indicating that the verbs in the answer need to be changed to reflect past tense. This provides specific guidance on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 48/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Faccio's early career?

**Answer**: Mara Faccio started her early career as Assistant Professor of Finance at the UniversitŠ Cattolica del Sacro Cuore in Milan in 1999. In 2001, she moved to the Mendoza College of Business at the University of Notre Dame and the Owen Graduate School of Management at Vanderbilt University in 2003. In 2007, she became a full professor at Purdue University.

**Critique**: "UniversitŠ" should be "Università".

**Rationale**: The critique specifies that the word "UniversitŠ" should be changed to "Università," providing a clear and specific correction to the text. This allows for the improvement of the answer without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 49/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Celeste's relationship with the drugs and alcohol she took?

**Answer**: She is a teenage girl who used to be quiet when she was younger. She was very responsible, worked hard in school and was expected to be a responsible human being. One day, she goes to Darcy's party and on her way to drunkenness, an insult to her life. She was having a good time with her friends but then ate too much and saw she sick.

**Critique**: The response is incorrect and fails to answer the question. 

**Rationale**: The critique states that the response is incorrect and fails to answer the question, but it does not provide any specific information about what is incorrect or what the answer should include. It does not specify what aspects of Celeste's relationship with drugs and alcohol need to be addressed or corrected in the answer. Without specific guidance on what to change or add, the critique does not enable improvement of the answer based solely on the critique itself.

**Classification**: Non-Constructive

---

### Sample 50/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the habitat and ecology of Bienertia cycloptera. 

**Answer**: Bienertia cycloptera is located in warm climates. It grows in warm temperatures with little rainfall. It grows in saline and moist clay soils. It is located alongside Climacoptera turcomanica. Bienertia cycloptera is an endangered species.

**Critique**: The answer could include the soils being rich in sodium ions and sulfate ions.

**Rationale**: The critique specifies that the answer should include information about the soils being rich in sodium ions and sulfate ions. This provides specific details that can be added to improve the answer.

**Classification**: Constructive

---

