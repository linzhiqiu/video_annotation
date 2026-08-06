# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (qa)
- **Total Dataset Size**: 4456 critique samples
- **Filtered Dataset Size** (qa): 1851 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 42
- **Timestamp**: 20251015_0307

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

A CONSTRUCTIVE critique must provide SPECIFIC information about what to change or add. Ask yourself: "Does this critique tell me what the answer should say or what specifically needs to be fixed?"

**CONSTRUCTIVE examples (tells you WHAT to change):**
- "This is false. She would have been 18 or 19" → You know to change the age to 18 or 19 ✅
- "The description of picking the yellow flower is incorrect" → You know that specific part is wrong ✅
- "The baby belongs to the narrator is inaccurate" → You know the baby doesn't belong to narrator ✅
- "It's omitted that the child was crushed under a roof" → You know to add this fact ✅
- "Some people are worried due to the virus" → You know what the answer should say ✅
- "Unnecessarily wordy" → You know to remove extra words ✅
- "Should be a full sentence" → You know to rewrite as complete sentence ✅
- "The last sentence is repetitive" → You know which sentence to remove/revise ✅

**NON-CONSTRUCTIVE examples (too vague, doesn't tell you what to change):**
- "The first sentence should be rewritten because it's inaccurate" → What should it say instead? ❌
- "Left out key happenings" → What happenings? What to add? ❌
- "Description is too simple" → What details to add? ❌
- "Needs more analysis" → What analysis? ❌
- "Could be more accurate" → How? What's inaccurate? ❌
- "This is wrong" → What specifically is wrong? ❌
- "Should consider correcting this" → Correct to what? ❌

**Test for constructiveness:** Can you improve the answer based ONLY on the critique, without re-reading the source material?
- If YES (critique gives you the fix or identifies the specific problematic part) → Constructive ✅
- If NO (need source to know what to add/fix) → Non-Constructive ❌

Special case:
- If the answer is already correct and the critique says "correct" or "no issues" → CONSTRUCTIVE ✅

Your rationale should conclude with ONE of these:
- "The critique specifies [what is wrong or what to change]" → Constructive
- "The critique only identifies a problem without specifying what to change" → Non-Constructive

Format your response EXACTLY as:
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

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | 33 | 66.00% |
| Non-Constructive | 17 | 34.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Write a ~6 sentence summary.

**Answer**: The author is discussing the personal war on Brett Kavanaugh and how it is representative of the larger war on conservatives. The author argues that the Kavanaugh confirmation battle is not just about Kavanaugh, but about all conservatives who are subjected to personal wars by Democrats and the Resistance.

**Critique**: The English isn't great and could be refined

**Rationale**: The critique states that "The English isn't great and could be refined," but it does not specify what aspects of the English are problematic or how it could be refined. Without specific guidance on what to change or improve, the critique does not provide actionable feedback to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Where was Carroll Snow Wales born?

**Answer**: Carroll Snow Wales was born in Boston, Massachusetts.

**Critique**: This is false, and the answer can't be found in the article.

**Rationale**: The critique states that the answer is false but does not provide any specific information about what the correct answer should be or what specifically needs to be changed. It only identifies a problem without specifying what to change.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Where is the old man headed?

**Answer**: He is headed toward a statue of a woman, who he thinks is his daughter.

**Critique**: He knows the statue of his daughter.

**Rationale**: The critique only identifies a problem without specifying what to change. It points out that the old man knows the statue is of his daughter, but it does not specify how the answer should be corrected or what specific information should be included to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Why were married couples paying more tax than couples just living together?

**Answer**: The government told voters that only 80,000 married couples were paying more tax than couples living together. The true figure was almost half a million.

**Critique**: This response is not related.

**Rationale**: The critique states that the response is not related, but it does not specify what the answer should say or what specific information is missing or incorrect. It only identifies a problem without providing guidance on how to correct it or what the correct information should be.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

Why was it transported to Boston?

**Answer**: It was probably to be re-sold.

**Critique**: The fact that the statue was installed in a Boston neighborhood is evidence against this answer.

**Rationale**: The critique points out that the statue was installed in a Boston neighborhood, which contradicts the answer's suggestion that it was transported to be re-sold. However, the critique does not specify what the correct reason for the transportation is or what the answer should say instead. It only identifies a problem without providing a specific correction or alternative information.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Answer the following question based on the above passage:

Is this story told in the first or third person?

**Answer**: Information not found.

**Critique**: The narrator clearly speaks in the first person.

**Rationale**: The critique specifies that the story is told in the first person, which directly addresses what is wrong with the answer and provides the specific information needed to correct it.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

What is the narrator's gender?

**Answer**: The narrator is female.

**Critique**: IT seems the narrator was born female, but they had procedures to be more male presenting. This would mean they are now either male or gender neutral.

**Rationale**: The critique specifies that the narrator, although born female, underwent procedures to present more male, suggesting that the narrator should be identified as either male or gender neutral. This provides specific information on what to change in the answer regarding the narrator's gender identity.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Write a ~2 sentence summary.

**Answer**: Intel has run into problems protecting its processing chips from the major Meltdown and Spectre vulnerabilities. It seems the issue effects systems running older Haswell chips.

**Critique**: "issue effects" - change "effects" to "affects"

**Rationale**: The critique specifies that the word "effects" should be changed to "affects," providing a clear and specific correction to the answer.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique specifies that the action described as drowning is incorrect and should be changed to something that resembles a baptism. This provides specific guidance on what to correct in the answer.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Write a ~6 sentence summary.

**Answer**: Eve has come up with a crowd-developed Spectrum gaming monitor with HDMI 2.1. This means that you may now be able to have an Xbox Series X and a PS5 connected simultaneously.

The monitor is 27-inches in size and comes with 100W USB-C pass-through charging and integer-ratio upscaling. The Spectrum monitor with the HDMI 2.1 configurations comes at two prices; $529 and $629.

Delivering the solid gaming monitor is certainly a challenge for a small company like Eve. But everyone is cautiously optimistic about it.

**Critique**: The answer implies HDMI 2.1 allows connecting Xbox Series X and a PS5 simultaneously. That's wrong, it's the inclusion of two HDMI 2.1 ports that allows it.

**Rationale**: The critique specifies that the issue with the answer is the implication that HDMI 2.1 itself allows for simultaneous connection of an Xbox Series X and a PS5. It clarifies that it is actually the inclusion of two HDMI 2.1 ports that enables this functionality. This provides specific information on what is incorrect and what needs to be changed in the answer.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why was it transported to Boston?

**Answer**: It was probably to be re-sold.

**Critique**: The fact that the statue was installed in a Boston neighborhood is evidence against this answer.

**Rationale**: The critique points out that the statue was installed in a Boston neighborhood, which contradicts the answer's suggestion that it was transported to be re-sold. However, the critique does not specify what the correct reason for the transportation is or what the answer should say instead. It only identifies a problem without providing a specific correction or alternative information.

**Classification**: Non-Constructive

---

### Sample 2/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to Concord Management and Consulting, LLC.

**Answer**: Concord Management and Consulting, LLC. is a Russian firm being charged by Robert Mueller in connection with an alleged online influence operation. The firm has sought to intervene in an appeal brought by an associate of Roger Stone in order to challenge Mueller's appointment as special counsel. The U.S. Court of Appeals in Washington, D.C. has denied the motion, but has allowed Concord to file an amicus brief should they choose to do so.

**Critique**: It's misleading to say that Mueller is charging Concord. It's the US Federal Court doing the charge, and Mueller is leading it. It's better to state what the charges are instead of who's doing it.

**Rationale**: The critique specifies that it is misleading to say that Mueller is charging Concord and clarifies that it is the US Federal Court doing the charge, with Mueller leading it. It also suggests stating what the charges are instead of focusing on who is doing the charging. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The Eve Spectrum is a 27-inch gaming monitor that is set to be one of the first to support HDMI 2.1. The monitor is currently on pre-sale, with models coming in the last quarter of 2020. The first real-life photos of an early model have been released, and the company says that the first measurements will be published soon. Once the Spectrum is available, we'll be sure to share our thoughts on it.

**Critique**: Two higher-end models will come in the Q4 of 2020 while the entry-level model will come out in the first quarter of 2021.

**Rationale**: The critique provides specific information about the release dates of different models of the Eve Spectrum monitor. It specifies that the higher-end models will be available in the fourth quarter of 2020, while the entry-level model will be released in the first quarter of 2021. This information tells you exactly what to change in the answer regarding the release timeline of the models.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why does the narrator suggest that they must terminate the patient's pregnancy?

**Answer**: That information is not covered in the text.

**Critique**: This is false. It is directly stated that, "...sorry, it's a boy. As you know our current sector has too many male children. When would you like to schedule the termination."

**Rationale**: The critique specifies that the answer is incorrect by providing a direct quote from the text that explains why the narrator suggests terminating the pregnancy. This allows for a clear understanding of what the answer should include, specifically the reason related to the sector having too many male children.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: The narrator is on trial, being walked by police officers in chains. He makes a crack about one of the officer's wives, whom he might have killed. The officer beats him. We flashback to the day of the murder. We learn the narrator himself is a police officer. 

**Critique**: The narrator isn't on trial. He's on his way to jail, as evidenced by Jason thinking, "It was disappointing to know that my last sight of the outside world would come from a spot-ridden plexi-glass window."

**Rationale**: The critique specifies that the narrator is not on trial but is on his way to jail, providing a specific detail from the text ("It was disappointing to know that my last sight of the outside world would come from a spot-ridden plexi-glass window") to support this correction. This allows for a clear and specific change to be made to the answer.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Why were married couples paying more tax than couples just living together?

**Answer**: The government told voters that only 80,000 married couples were paying more tax than couples living together. The true figure was almost half a million.

**Critique**: This response is not related.

**Rationale**: The critique states that the response is not related, but it does not specify what the answer should say or what specific information is missing or incorrect. It only identifies a problem without providing guidance on how to correct it or what the correct information should be.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Constructive]

**Question**: What kind of security does Bank Zero offer to its clients?

**Answer**: In November of 2019, Bank Zero has patented a debit card that used a unique system for storing card numbers. This allowed Bank Zero to control the transactions that could be done with the card -increasing its security.

**Critique**: Formatting (hyphen into dash)

**Rationale**: The critique specifies that the hyphen should be changed into a dash, which is a specific formatting change.

**Classification**: Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Explain the original art piece.

**Answer**: The original piece was spray painted on a building in East London in 2002. In 2014 it was removed and sold at auction the following year.

**Critique**: should describe the content of the image

**Rationale**: The critique only identifies a problem without specifying what to change. It suggests that the answer should describe the content of the image, but it does not provide any specific details about what the content is or what should be included in the description. Without additional information, it is not possible to improve the answer based solely on this critique.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Constructive]

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique specifies that the action described as drowning is incorrect and should be changed to something that resembles a baptism. This provides specific guidance on what to correct in the answer.

**Classification**: Constructive

---

### Sample 10/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What kind of vehicle does Alan drive?

**Answer**: The compact Optra SRV could refer to a car, though not very sporty or interesting. It also could refer to a certain type of vehicle.

**Critique**: "could refer to a car, though not very sporty or interesting. It also could refer to a certain type of vehicle." - the unnecessary information ruined a perfectly good answer. This should be deleted. Replace "The" with "A" in "compact Optra SRV"

**Rationale**: The critique specifies that the unnecessary information should be deleted and provides a specific change to make by replacing "The" with "A" in "compact Optra SRV." This gives clear guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 11/50 - [Non-Constructive]

**Question**: What is the sailor like?

**Answer**: 

**Critique**: No content.

**Rationale**: The critique only identifies a problem without specifying what to change. It points out that there is no content in the answer, but it does not provide any guidance on what the answer should include or how to address the lack of content.

**Classification**: Non-Constructive

---

### Sample 12/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is the narrator's gender?

**Answer**: The narrator is female.

**Critique**: IT seems the narrator was born female, but they had procedures to be more male presenting. This would mean they are now either male or gender neutral.

**Rationale**: The critique specifies that the narrator, although born female, underwent procedures to present more male, suggesting that the narrator should be identified as either male or gender neutral. This provides specific information on what to change in the answer regarding the narrator's gender identity.

**Classification**: Constructive

---

### Sample 13/50 - [Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: The National Climate Change Secretariat (NCCS) is a Singaporean agency that is responsible for coordinating Singapore's domestic and international policies and strategies in addressing climate change. The NCCS is part of the Strategy Group that supports the Prime Minister and his Cabinet, and it is also under the Inter-Ministerial Committee on Climate Change (IMCCC) which is chaired by Mr Teo Chee Hean, Senior Minister and Co-ordinating Minister for National Security. The NCCS has 4 main responsibilities: reducing carbon emissions throughout all sectors, assisting the nation in adapting to the short-term and long-term effects of climate change, seeking to tap on green growth opportunities brought about by climate change, and promoting climate consciousness and climate action among the general public.

**Critique**: "The NCCS is part of the Strategy Group that supports the Prime Minister and his Cabinet, and it is also under the Inter-Ministerial Committee on Climate Change (IMCCC) which is chaired by Mr Teo Chee Hean, Senior Minister and Co-ordinating Minister for National Security." can be omitted.

**Rationale**: The critique specifies that the sentence about the NCCS being part of the Strategy Group and under the IMCCC, chaired by Mr. Teo Chee Hean, can be omitted. This provides clear guidance on what part of the answer can be removed to improve the summary.

**Classification**: Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Why does the narrator suggest that they must terminate the patient's pregnancy?

**Answer**: The patient's fetus is male and, because of the current birth quotas, doctors are allowed to terminate pregnancies with male fetuses so as to make way for a more accurate representation of baby girls in the region.

**Critique**: "so as to" - use "to"

**Rationale**: The critique specifies that the phrase "so as to" should be changed to "to," providing a clear and specific instruction on what to change in the answer.

**Classification**: Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Write a ~7 sentence summary.

**Answer**: Leicester is going back into lockdown after a new spike in local coronavirus cases. This indicates that the current crisis is far from over. Nick Rushton, Leicestershire County Council leader, says that though the county rates are below the national and regional averages, the people of Leicester are asked to follow the SLR up to the extent possible. He adds that they were a bit sceptical to the move but now believe it a very sensible thing to do. The health secretary says that they are hoping that people in Leicester will stay at home as much as they can and against all travel to, from, and within Leicester. They have also been urged not to go to restaurants and pubs during the lockdown period. Sir Peter Soulsby, a city mayor, says the move is very disappointing. This is the plan that Boris Johnson will restart his premiership.

**Critique**: Why does the model shorten "strict lockdown rule" to SLR?
The summary is over seven sentences.

'He adds that they were a bit sceptical to...' 
This sentence has a wrong spelling of skeptical and inappropriate preposition use.

'He adds that they were a bit sceptical to the move but now believe it a very sensible thing to do.' 
Mayor Soulsby made this sentence, not Nick Rushton, as implied by the model.

'They have also been urged not to go to restaurants and pubs during the lockdown period.' 
This sentence was not stated in the article. Instead, the health secretary's declaration of another lockdown meant that pubs, restaurants, and salons planning to reopen would be delayed.

**Rationale**: The critique provides specific information about what needs to be changed or corrected in the answer. It points out the incorrect abbreviation of "strict lockdown rule" to "SLR," specifies the spelling and preposition errors in the sentence about skepticism, identifies the misattribution of a quote to Nick Rushton instead of Mayor Soulsby, and clarifies the inaccuracy regarding the statement about restaurants and pubs. Each point in the critique tells exactly what is wrong and what needs to be fixed or clarified in the summary.

**Classification**: Constructive

---

### Sample 16/50 - [Constructive]

**Question**: Who are the main characters of the story?

**Answer**: Maximillian Garvey, his wife Jazira, and his son the prince

**Critique**: Omits mention of the King

**Rationale**: The critique identifies that the answer is missing a specific character, the King, which needs to be added to the list of main characters. This provides clear guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who is Trina Patterson?`

**Answer**: s 5th year head coach who leads the Spartans

**Critique**: A small typo error needs to be fixed and some more specific detail needs to be added. 

**Rationale**: The critique mentions a "small typo error" and suggests adding "more specific detail," but it does not specify what the typo is or what specific details should be added. Without this information, it is not possible to improve the answer based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique specifies that the answer should include the information that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This provides specific information on what to add to the answer.

**Classification**: Constructive

---

### Sample 19/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: James Butler leads a lonely life. He is an average man in an average home. He hardly forms connections and when he is not exactly working he watches ordinary things. Despite this simplicity,James Butler has a keen sense of what could have been.

**Critique**: James Butler has a wife and two kids. He lives an ordinary life, not a lonely life.

**Rationale**: The critique specifies that James Butler has a wife and two kids, and that he lives an ordinary life rather than a lonely one. This provides specific information about what is incorrect in the answer and what needs to be changed.

**Classification**: Constructive

---

### Sample 20/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Whose statues are they?

**Answer**: They are stone statues of military people.

**Critique**: Could mention that they died defending Earth,

**Rationale**: The critique suggests adding specific information about the statues, namely that they died defending Earth. This provides clear guidance on what additional detail to include in the answer to improve it.

**Classification**: Constructive

---

### Sample 21/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Jiranová retire a race despite leading?

**Answer**: This information is not given. She tripped and her foot got caught up in the hurdle, leading her to fall.

**Critique**: The information is given. It says she stumbles. It's also contradictory to give information about her stumble after saying there is no info given.

**Rationale**: The critique points out a contradiction in the answer by stating that the information is indeed given in the passage, specifically mentioning that she stumbles. This helps to correct the answer by indicating that the reason for her retirement from the race is due to stumbling, which is information that was initially claimed to be missing. The critique specifies what is wrong with the answer and what needs to be changed to make it accurate.

**Classification**: Constructive

---

### Sample 22/50 - [Constructive]

**Question**: When was Bitossi imprisoned?

**Answer**: Bitossi was imprisoned in 1934.

**Critique**: He was imprisoned from 1927 to 1932, and then again from 1934 to 1943

**Rationale**: The critique specifies the correct imprisonment periods for Bitossi, indicating that the answer should be changed to reflect that he was imprisoned from 1927 to 1932 and then again from 1934 to 1943. This provides specific information on what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 23/50 - [Non-Constructive]

**Question**: Why do art critics think the statue is inferior?

**Answer**: The statue is described as "inferior" and "unremarkable" by art critics.

**Critique**: The response simply states information given in the question

**Rationale**: The critique points out that the answer merely repeats the information provided in the question without offering any additional insight or explanation. However, it does not specify what additional information or analysis should be included to improve the answer. Therefore, it does not provide specific guidance on how to enhance the response.

**Classification**: Non-Constructive

---

### Sample 24/50 - [Constructive]

**Question**: Write a ~1 sentence summary.

**Answer**: The RTP Awards are an annual awards ceremony for radio and television in Ghana, organized by Big Events Ghana. The 9th edition was held on October 12, 2019, and was hosted by actor James Gardiner and talk show host Cookie Tee.

**Critique**: The second sentence is unnecessary 

**Rationale**: The critique specifies that the second sentence is unnecessary, indicating that it should be removed to improve the answer.

**Classification**: Constructive

---

### Sample 25/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: Eve has come up with a crowd-developed Spectrum gaming monitor with HDMI 2.1. This means that you may now be able to have an Xbox Series X and a PS5 connected simultaneously.

The monitor is 27-inches in size and comes with 100W USB-C pass-through charging and integer-ratio upscaling. The Spectrum monitor with the HDMI 2.1 configurations comes at two prices; $529 and $629.

Delivering the solid gaming monitor is certainly a challenge for a small company like Eve. But everyone is cautiously optimistic about it.

**Critique**: The answer implies HDMI 2.1 allows connecting Xbox Series X and a PS5 simultaneously. That's wrong, it's the inclusion of two HDMI 2.1 ports that allows it.

**Rationale**: The critique specifies that the issue with the answer is the implication that HDMI 2.1 itself allows for simultaneous connection of an Xbox Series X and a PS5. It clarifies that it is actually the inclusion of two HDMI 2.1 ports that enables this functionality. This provides specific information on what is incorrect and what needs to be changed in the answer.

**Classification**: Constructive

---

### Sample 26/50 - [Constructive]

**Question**: Who is the target audience?

**Answer**: The target audience for this website is those who are interested in the St. Jacobs farmer's market and who were especially affected by the recent fire that destroyed the market building.

**Critique**: The fire and the farmers' market are only briefly mentioned; the article targets potential customers for The Fritter Co.

**Rationale**: The critique identifies that the article's target audience is not primarily those interested in the St. Jacobs farmer's market or affected by the fire, but rather potential customers for The Fritter Co. This provides specific information about what the answer should focus on, which is the correct target audience.

**Classification**: Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Where was Carroll Snow Wales born?

**Answer**: Carroll Snow Wales was born in Boston, Massachusetts.

**Critique**: This is false, and the answer can't be found in the article.

**Rationale**: The critique states that the answer is false but does not provide any specific information about what the correct answer should be or what specifically needs to be changed. It only identifies a problem without specifying what to change.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Non-Constructive]

**Question**: What was Aftab Hussain born?

**Answer**: 17 November 1997

**Critique**: I corrected for grammar.

**Rationale**: The critique mentions a correction for grammar but does not specify what the grammatical issue is or how it should be corrected. Without specific information on what to change, it is not possible to improve the answer based solely on the critique.

**Classification**: Non-Constructive

---

### Sample 29/50 - [Constructive]

**Question**: How old was Sanuth when his cricket career took off?

**Answer**: It can be implied from the article that he was 19 years old.

**Critique**: Unnecessarily wordy answer

**Rationale**: The critique specifies that the answer is unnecessarily wordy, indicating that extra words should be removed to make the answer more concise. This provides specific guidance on what to change in the answer.

**Classification**: Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What kind of restaurant is Paul in?

**Answer**: A laundromat.

**Critique**: It fails to mention that Paul is not at a restaurant.

**Rationale**: The critique identifies that the answer is incorrect by stating that Paul is not at a restaurant, but it does not specify what the correct location should be. Without knowing the correct location, the critique does not provide enough information to improve the answer.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Non-Constructive]

**Question**: How is a consensus reached?

**Answer**: The consensus is reached when only one remains.

**Critique**: This is misleading and incorrect.

**Rationale**: The critique states that the answer is "misleading and incorrect," but it does not specify what is misleading or incorrect about the answer or what the correct information should be. Without specific guidance on what to change or add, the critique does not provide enough information to improve the answer without consulting the source material.

**Classification**: Non-Constructive

---

### Sample 32/50 - [Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Helena Jiranová is a Czech runner and sprinter who has had some success in international competitions. She is currently ranked first in Czech Republic in the 400 metres, fourth in the 60 meters hurdles, and eighth in the 100 meters hurdles. Her personal bests include a 53.77 sec. time in the 400 metres and an 8.31 sec. time in the 60 meters hurdles. Jiranová has experienced some success in international competitions, placing eighth in the 4 × 400 metres relay at the European Athletics Junior Championships and sixth in the 100 meters hurdles at the European Athletics U23 Championships.

**Critique**: Jiranova is not ranked first in Czech Republic in the 400 metres, fourth in the 60 meters hurdles, and eighth in the 100 meters hurdles. This whole sentence needs to be mended, as it is entirely false.

**Rationale**: The critique specifies that the rankings mentioned in the answer are incorrect and that the entire sentence containing these rankings needs to be corrected. This provides specific guidance on what part of the answer is wrong and needs to be changed.

**Classification**: Constructive

---

### Sample 33/50 - [Non-Constructive]

**Question**: What does the train conductor give the narrator?

**Answer**: 

**Critique**: No response is given and a proper response needs to be generated. 

**Rationale**: The critique identifies that there is no response provided and specifies that a proper response needs to be generated. However, it does not specify what the response should include or what information is missing, making it unclear what the answer should say. Therefore, it does not provide specific guidance on what to change or add to the answer.

**Classification**: Non-Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: Ben is bored at home and decides to have some fun with a telemarketer. He pretends to be interested in the product, but eventually tells the telemarketer he is not interested. The next day, the telemarketer calls back and tells Ben he has quit his previous job and has got a new one, which pays much more.

**Critique**: Ben is not the narrator's real name. 

**Rationale**: The critique specifies that "Ben is not the narrator's real name," indicating that the name "Ben" should be changed to the narrator's actual name. This provides specific information about what needs to be corrected in the answer.

**Classification**: Constructive

---

### Sample 35/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Describe the relationship between the two characters.

**Answer**: The two characters have a mutual attraction and connection with one another. The protagonist is taken under the spell of the radiant smile of his companion. The two share an emotional and vibrant connection that is unbreakable.

**Critique**: There's an attraction for sure. However, it's temporary, and the answer completely makes up the unbreakable part.

**Rationale**: The critique specifies that the "unbreakable" part of the relationship is incorrect and that the attraction is temporary. This provides specific guidance on what to change in the answer regarding the nature and duration of the relationship between the characters.

**Classification**: Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: Intel has run into problems protecting its processing chips from the major Meltdown and Spectre vulnerabilities. It seems the issue effects systems running older Haswell chips.

**Critique**: "issue effects" - change "effects" to "affects"

**Rationale**: The critique specifies that the word "effects" should be changed to "affects," providing a clear and specific correction to the answer.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: President Trump says it doesn't matter if he misled the media about his son's infamous 2016 Trump Tower meeting with Russian nationals. Trump's lawyers admitted that he dictated a statement that Donald Trump Jr. released about the meeting. Trump's casual stance on telling the truth was also apparent in remarks he made about retired Army Lt. Gen. Michael Flynn, his former national security adviser who pleaded guilty to lying to the FBI.

**Critique**: "President Trump says it doesn't matter if he misled the media about his son's infamous 2016 Trump Tower meeting with Russian nationals." - while OK on its own, this statement needs a reason why the lie didn't matter. Add something about the New York Times.

**Rationale**: The critique specifies that the statement about President Trump needs additional information explaining why the lie didn't matter and suggests adding something about the New York Times. This provides specific guidance on what to change or add to the answer.

**Classification**: Constructive

---

### Sample 38/50 - [Non-Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The author is discussing the personal war on Brett Kavanaugh and how it is representative of the larger war on conservatives. The author argues that the Kavanaugh confirmation battle is not just about Kavanaugh, but about all conservatives who are subjected to personal wars by Democrats and the Resistance.

**Critique**: The English isn't great and could be refined

**Rationale**: The critique states that "The English isn't great and could be refined," but it does not specify what aspects of the English are problematic or how it could be refined. Without specific guidance on what to change or improve, the critique does not provide actionable feedback to improve the answer.

**Classification**: Non-Constructive

---

### Sample 39/50 - [Non-Constructive]

**Question**: Explain the new app update.

**Answer**: The new update is to require social security numbers for all users of the company's app. This is meant to increase security and make it harder for people to create fake accounts.

**Critique**: There is no evidence that suggests the meaning behind the app update requiring social security numbers.

**Rationale**: The critique only identifies a problem by stating there is no evidence for the meaning behind the app update, but it does not specify what to change or what the answer should say instead. It does not provide specific guidance on how to improve the answer or what information should be included to address the issue.

**Classification**: Non-Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who first reported the incident?

**Answer**: The Wall Street Journal first reported the issues with the latest Intel firmware update.

**Critique**: "first reported the issues with the latest Intel firmware update." - superfluous details that may be irrelevant given the question. Should be deleted.

**Rationale**: The critique specifies that the phrase "first reported the issues with the latest Intel firmware update" contains superfluous details that should be deleted, indicating that the answer should be more concise and directly address the question of who first reported the incident.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who is the narrator?

**Answer**: The narrator is a member of a space agency. He is stuck on a shuttle while there is a mechanical problem he cannot fix.

**Critique**: The answer should be more precise about the narrator's job.

**Rationale**: The critique only identifies a problem without specifying what to change. It suggests that the answer should be more precise about the narrator's job but does not provide specific details or guidance on what the job is or how to make it more precise.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Where did Castor begin his career?

**Answer**: He began his career as a litigator in commercial law at the low firm Blank Rome in Philadelphia and Washington D.C.

**Critique**: The word "low" in this response needs to be changed to "law".

**Rationale**: The critique specifies that the word "low" should be changed to "law," providing a clear and specific correction to the answer.

**Classification**: Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who did The Spartans lose to in the previous season?

**Answer**: The team lost in the quarter finals game to the University of Chattanooga.

**Critique**: University in this response needs to be omitted because it is not something that can be assumed. 

**Rationale**: The critique specifies that the word "University" should be omitted from the response, indicating a specific change to be made.

**Classification**: Constructive

---

### Sample 44/50 - [Non-Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Shiza Shahid is a Pakistani social entrepreneur who co-founded the Malala Fund, a non-profit organisation that promotes education for girls. She is also well-known as the mentor of Nobel Peace Prize laureate Malala Yousafzai.

**Critique**: The summary is less than 5 sentences and does not include enough information about Shiza.

**Rationale**: The critique identifies that the summary is too short and lacks sufficient information about Shiza Shahid, but it does not specify what additional information should be included or what specific details are missing. Without guidance on what to add, the critique does not provide a clear path for improvement.

**Classification**: Non-Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Is this story told in the first or third person?

**Answer**: Information not found.

**Critique**: The narrator clearly speaks in the first person.

**Rationale**: The critique specifies that the story is told in the first person, which directly addresses what is wrong with the answer and provides the specific information needed to correct it.

**Classification**: Constructive

---

### Sample 46/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How old was Jiranová when she first won a tournament?

**Answer**: Jiranová won her first tournament in 2014 when she was 17 years old.

**Critique**: This is false. She would have been 18 or 19.

**Rationale**: The critique specifies that the age mentioned in the answer is incorrect and provides the correct age range, indicating that Jiranová should be 18 or 19 years old instead of 17. This allows for a specific correction to be made to the answer.

**Classification**: Constructive

---

### Sample 47/50 - [Non-Constructive]

**Question**: What data can still be collected after this ban?

**Answer**: It is possible for data to be collected if the FBI claims there is a legitimate national security purposes.

**Critique**: This is incorrect. There are even further restrictions given, as the FBI were previously able to use "legitimate national security purpose" to justify any reason they had for collecting data.

**Rationale**: The critique identifies that the answer is incorrect but does not specify what the further restrictions are or what the answer should include. It points out a problem but does not provide specific information on what to change or add to make the answer correct.

**Classification**: Non-Constructive

---

### Sample 48/50 - [Constructive]

**Question**: Are there regional variations?

**Answer**: Yes, there are regional variations.

**Critique**: Add the regional variation mentioned - the more subdued Taiwanese version.

**Rationale**: The critique specifies what to change by indicating that the answer should include the specific regional variation, which is the more subdued Taiwanese version. This provides clear guidance on what information to add to improve the answer.

**Classification**: Constructive

---

### Sample 49/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Where is the old man headed?

**Answer**: He is headed toward a statue of a woman, who he thinks is his daughter.

**Critique**: He knows the statue of his daughter.

**Rationale**: The critique only identifies a problem without specifying what to change. It points out that the old man knows the statue is of his daughter, but it does not specify how the answer should be corrected or what specific information should be included to improve the answer.

**Classification**: Non-Constructive

---

### Sample 50/50 - [Constructive]

**Question**: Has Ralph Josselyn had children?

**Answer**: There is no mention of children in the passage, so it cannot be determined whether or not he had any.

**Critique**: The answer is wrong. The article says that "He seems to have had no surviving children, as his heir was his nephew George Josselyn, son of his elder brother Thomas."

**Rationale**: The critique specifies that the answer is wrong and provides the specific information that should be included: Ralph Josselyn seems to have had no surviving children, as his heir was his nephew George Josselyn, son of his elder brother Thomas. This gives clear guidance on what the answer should say.

**Classification**: Constructive

---

