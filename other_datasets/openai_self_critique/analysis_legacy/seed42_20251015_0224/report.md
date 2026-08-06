# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique
- **Total Dataset Size**: 3579 critique samples
  - Topic-based summarization: 1728 samples
  - Non-topic-based (Q&A): 1851 samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 42
- **Timestamp**: 20251015_0224

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

A CONSTRUCTIVE critique provides actionable, specific feedback that helps improve the answer. It must identify a problem AND give enough information to fix it. This includes:

1. **Providing missing information**: "Some people are worried due to the virus" or "He was caught, though" (gives the actual content that should be added)
2. **Correcting errors with the right answer**: "It should be white, not black" or "The horse is brown, not white" or "There is no evidence it was a daughter, not a son" (points out what's wrong and what's right)
3. **Specifying omitted details**: "It's omitted that the child was being crushed under a roof"
4. **Identifying specific problems**: "The last sentence is repetitive and not relevant" (tells you exactly what to fix or remove)
5. **Giving concrete improvement suggestions**: "Combine sentences that convey the same idea" or "Use X instead of Y"

A NON-CONSTRUCTIVE critique only describes a problem vaguely without providing enough information to fix it:
- "This doesn't answer the question" (doesn't say what the answer should be)
- "More details needed" (doesn't specify what details)
- "This is wrong" or "This is incomplete" (too vague, no specifics about what)
- "The story never discusses X" (doesn't tell you what X is or should be)
- "There's an error here" (doesn't say what error or where)
- "This could be better" (too vague)

Key distinction: 
- ✅ CONSTRUCTIVE: "Sentence X is repetitive" or "It was not X, it was Y" or "Missing: Z" or "Remove the last sentence"
- ❌ NON-CONSTRUCTIVE: "This is wrong" or "Something is missing" or "This could be improved" (no indication of what specifically)

Note: Even brief critiques are constructive if they clearly identify the specific issue or what needs to be changed.

Special case:
- If the answer is already correct and no critique is necessary, then an empty critique or one that says "no issues" should be treated as CONSTRUCTIVE/APPROPRIATE.

Please first provide your rationale (2-3 sentences explaining your reasoning), then output your classification.

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

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | 27 | 54.00% |
| Non-Constructive | 23 | 46.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

### Topic-based Summarization Tasks
- Samples: 24
- Constructive: 15 (62.50%)

### Non-topic-based (Q&A) Tasks
- Samples: 26
- Constructive: 12 (46.15%)

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Answer the following question based on the above passage:

What happens to the child?

**Answer**: The child drowns and the priest ignores his plea for help.

**Critique**: More background detail needs to be added to this to explain how and why the child was drowning. 

**Rationale**: The critique identifies a need for additional background detail but does not specify what specific information is missing or how to improve the answer. It vaguely suggests that more detail is needed without providing actionable guidance on what those details should be or how to incorporate them into the answer. This makes it difficult for the answerer to know exactly what to add or change.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: How is a consensus reached?

**Answer**: The consensus is reached when only one remains.

**Critique**: This is misleading and incorrect.

**Rationale**: The critique identifies that the answer is misleading and incorrect, but it does not provide any specific information on what the correct answer should be or how to improve the response. It lacks actionable feedback or specific details that would help in correcting the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Summarize everything that happened in the 1990s.

**Answer**: No answer

**Critique**: There were events mentioned in the text that took place in 1996 and 1993.

**Rationale**: The critique points out that there were events in 1996 and 1993 mentioned in the text, which implies that these events should be included in the answer. However, it does not specify what those events are or how they should be incorporated into the summary. Therefore, it lacks the specificity needed to be actionable and improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Answer the following question based on the above passage:

Summarize the most interesting facts in the text. 

**Answer**: The Mechanics Educational Society of America was founded in 1933 by disgruntled members of the International Association of Machinists. Matthew Smith, Frank McCracken, and John Anderson pushed for a full-fledged union. In June 1933, the U.S. Congress passed the National Industrial Recovery Act of 1933 which protected the collective bargaining rights of unions. A month later, MESA began an organizing drive in Detroit, Pontiac, Michigan, and Flint, Michigan.

**Critique**: The response left out key happenings in MESA's history.

**Rationale**: The critique provided is non-constructive because it vaguely states that key happenings in MESA's history are missing without specifying what those key happenings are. It does not provide any specific information or guidance on what should be included to improve the answer. For a critique to be constructive, it should identify specific missing details or provide concrete suggestions for improvement.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the text say about the parameters for an entry?

**Answer**: [rewrite]

**Critique**: The question was unconventional and the response should have been "No Answer" or "That information can't be found." 

**Rationale**: The critique identifies a problem with the answer, suggesting that the response should have been "No Answer" or "That information can't be found." However, it does not provide specific guidance on how to improve the answer or what exactly is wrong with the current response. It lacks actionable feedback that would help in revising the answer effectively.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Who is the target audience?

**Answer**: The target audience for this website is those who are interested in the St. Jacobs farmer's market and who were especially affected by the recent fire that destroyed the market building.

**Critique**: The fire and the farmers' market are only briefly mentioned; the article targets potential customers for The Fritter Co.

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the focus on the fire and the farmers' market is insufficient and that the article actually targets potential customers for The Fritter Co. This provides clear guidance on what aspect of the answer needs to be corrected or expanded upon.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

Summarize how the main character's situation changes over the story.

**Answer**: Chad's story begins with him searching through the ship for survivors. He finds the captain, who gives him command of the ship. Chad is in disbelief. He leaves the ship to escape the war.

**Critique**: He doesn't leave the ship.

**Rationale**: The critique identifies a specific error in the answer by pointing out that the statement "He leaves the ship to escape the war" is incorrect. It provides the necessary information to correct the mistake by stating that "He doesn't leave the ship." This is a clear and actionable piece of feedback that directly addresses the inaccuracy in the answer.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

What does the story say about Zofia Nehringowa's sport results?

**Answer**: Zofia Nehringowa was a Polish long track speed skater who set a world record in all four individual distances (500 m, 1000 m, 1500 m, 3000 m) in 1931 and 1935. Nehringowa competed at the 1932 European Speed Skating Championships for Men and set a women's world record in the 1500m during these race. Nehringowa represented Poland at the World Allround Speed Skating Championships for Women in 1939 where she finished 5th overall.

**Critique**: In 1931, Nehringowa set the world records in the 500m, 1000m, 1500m, 3000m and 5000m. These results were approved by the ISU's the first women's speed skating world records. In 1932, Nehringowa broke the women's world records in the 1500m and 1000m. In 1935 she improved her own world records in the 3000m, 5000m and 10 000m. Change the response to reflect these results.

**Rationale**: The critique provides specific corrections to the answer by detailing the accurate historical records set by Zofia Nehringowa. It specifies the years and distances for which she set or improved world records, correcting the inaccuracies in the original answer. Additionally, it gives clear instructions to change the response to reflect these accurate results, making it actionable and specific.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

Summarize the reveal at the end of the story.

**Answer**: Blocker is terminally ill, and the man with glasses tells him he only has a few months left. Blocker then realizes he has been fixated on the carpet, which is the color taupe. He cries.

**Critique**: This could be phrased differently to tie in better with the reveal. It should be said that Blocker only acknowledges this news and cries after he realizes what the color of the carpet is.

**Rationale**: The critique identifies a specific issue with the phrasing of the answer, suggesting that the sequence of events could be better aligned with the reveal. It provides a concrete suggestion on how to improve the answer by specifying that Blocker acknowledges the news and cries after realizing the carpet's color. This feedback is actionable and specific, making it clear what needs to be changed to improve the answer.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

Where did Castor begin his career?

**Answer**: He began his career as a litigator in commercial law at the low firm Blank Rome in Philadelphia and Washington D.C.

**Critique**: The word "low" in this response needs to be changed to "law".

**Rationale**: The critique identifies a specific error in the answer, which is the incorrect use of the word "low" instead of "law." It provides the correct word that should be used, making it clear what needs to be fixed. This is a direct and actionable piece of feedback that improves the accuracy of the answer.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Is this story told in the first or third person?

**Answer**: Information not found.

**Critique**: The narrator clearly speaks in the first person.

**Rationale**: The critique identifies a specific problem with the answer by pointing out that the narrator speaks in the first person, which directly addresses the question. This provides the necessary information to correct the answer, making it clear that the story is told in the first person. The critique is specific and actionable.

**Classification**: Constructive

---

### Sample 2/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the views of the opposing sides.

**Answer**: Republicans are counting on these judges to dismantle reproductive rights, marriage equality, and the separation of church and state and to use the courts to shred the New Deal and regulations that protect the people from corporate power. They believe the Democrats are letting Mitch McConnell and Donald Trump do this to consolidate their power and are counting on the voters to stop them. The Democratic Party, in some cases, appears to be acquiescing.

**Critique**: The Republicans are stated to believe Democrats are letting McConnell and Trump do their thing to consolidate their power, which is made up.

**Rationale**: The critique identifies a specific problem in the answer by pointing out that the statement about Republicans believing Democrats are letting McConnell and Trump consolidate power is fabricated. However, it does not provide a correction or suggest what the accurate information should be, leaving the critique incomplete in terms of providing actionable feedback.

**Classification**: Non-Constructive

---

### Sample 3/50 - [Non-Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: Ben is bored at home and decides to have some fun with a telemarketer. He pretends to be interested in the product, but eventually tells the telemarketer he is not interested. The next day, the telemarketer calls back and tells Ben he has quit his previous job and has got a new one, which pays much more.

**Critique**: Ben is not the narrator's real name. 

**Rationale**: The critique identifies a specific issue with the answer, which is the incorrect use of the name "Ben" as the narrator's real name. However, it does not provide the correct name or suggest how to address the issue, such as using a placeholder or clarifying the name. Therefore, while it points out a problem, it lacks actionable feedback to fix it.

**Classification**: Non-Constructive

---

### Sample 4/50 - [Non-Constructive]

**Question**: How is a consensus reached?

**Answer**: The consensus is reached when only one remains.

**Critique**: This is misleading and incorrect.

**Rationale**: The critique identifies that the answer is misleading and incorrect, but it does not provide any specific information on what the correct answer should be or how to improve the response. It lacks actionable feedback or specific details that would help in correcting the answer.

**Classification**: Non-Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the main character's situation changes over the story.

**Answer**: Chad's story begins with him searching through the ship for survivors. He finds the captain, who gives him command of the ship. Chad is in disbelief. He leaves the ship to escape the war.

**Critique**: He doesn't leave the ship.

**Rationale**: The critique identifies a specific error in the answer by pointing out that the statement "He leaves the ship to escape the war" is incorrect. It provides the necessary information to correct the mistake by stating that "He doesn't leave the ship." This is a clear and actionable piece of feedback that directly addresses the inaccuracy in the answer.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: What was Aftab Hussain born?

**Answer**: 17 November 1997

**Critique**: I corrected for grammar.

**Rationale**: The critique "I corrected for grammar" is non-constructive because it does not specify what grammatical errors were present or how they were corrected. It lacks the necessary details to understand what was wrong and how it was fixed, making it impossible to learn from or apply the feedback.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Non-Constructive]

**Question**: What data can still be collected after this ban?

**Answer**: It is possible for data to be collected if the FBI claims there is a legitimate national security purposes.

**Critique**: This is incorrect. There are even further restrictions given, as the FBI were previously able to use "legitimate national security purpose" to justify any reason they had for collecting data.

**Rationale**: The critique identifies a specific error in the answer by pointing out that the FBI's ability to collect data under the guise of "legitimate national security purposes" is no longer valid due to further restrictions. However, it does not provide the correct information or specify what the current restrictions are, leaving the answer incomplete without guidance on how to correct it. Therefore, the critique lacks actionable feedback to improve the answer.

**Classification**: Non-Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Where was Carroll Snow Wales born?

**Answer**: Carroll Snow Wales was born in Boston, Massachusetts.

**Critique**: This is false, and the answer can't be found in the article.

**Rationale**: The critique states that the answer is false and that the information cannot be found in the article, but it does not provide the correct information or specify what the correct answer should be. It fails to offer any actionable feedback or guidance on how to correct the answer. Therefore, it lacks the specificity required to be constructive.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything that happened in the 1990s.

**Answer**: No answer

**Critique**: There were events mentioned in the text that took place in 1996 and 1993.

**Rationale**: The critique points out that there were events in 1996 and 1993 mentioned in the text, which implies that these events should be included in the answer. However, it does not specify what those events are or how they should be incorporated into the summary. Therefore, it lacks the specificity needed to be actionable and improve the answer.

**Classification**: Non-Constructive

---

### Sample 10/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What kind of restaurant is Paul in?

**Answer**: A laundromat.

**Critique**: It fails to mention that Paul is not at a restaurant.

**Rationale**: The critique identifies a specific problem with the answer by pointing out that it incorrectly states Paul is in a laundromat instead of a restaurant. However, it does not provide the correct information or suggest how to fix the error, such as stating where Paul actually is. Therefore, it lacks the actionable feedback needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 11/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who did The Spartans lose to in the previous season?

**Answer**: The team lost in the quarter finals game to the University of Chattanooga.

**Critique**: University in this response needs to be omitted because it is not something that can be assumed. 

**Rationale**: The critique identifies a specific issue with the answer, which is the incorrect inclusion of the word "University." It provides actionable feedback by specifying that "University" should be omitted, thus giving clear guidance on how to correct the answer. This aligns with the criteria for a constructive critique as it points out exactly what is wrong and how to fix it.

**Classification**: Constructive

---

### Sample 12/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What happens to the child?

**Answer**: The child drowns and the priest ignores his plea for help.

**Critique**: More background detail needs to be added to this to explain how and why the child was drowning. 

**Rationale**: The critique identifies a need for additional background detail but does not specify what specific information is missing or how to improve the answer. It vaguely suggests that more detail is needed without providing actionable guidance on what those details should be or how to incorporate them into the answer. This makes it difficult for the answerer to know exactly what to add or change.

**Classification**: Non-Constructive

---

### Sample 13/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the tension in the story. 

**Answer**: The tension in the story seems to stem from a fallout between the two main characters. There is also the event that happened three years prior to the story.

**Critique**: The event three years ago, an accident, seems to be the point where the duo separated.

**Rationale**: The critique provides specific information about the event three years ago, identifying it as an accident and suggesting it as the pivotal moment for the separation of the duo. This adds clarity and context to the answer, making it more complete and informative. By specifying the nature of the event, the critique offers actionable feedback that can improve the answer.

**Classification**: Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about de Villa's opinion on public health?

**Answer**: She has urged for the prevention of communicable diseases and wants the brands to clamp down on misleading anti-vaccination information by minimizing the public's access to these rumors. She has also called for a ban on vaccine exemptions if an individual has certain beliefs that say they should not be vaccinated.

**Critique**: Additional detail about how De Villa's whole career is around public health issues should be stated. 

**Rationale**: The critique suggests adding specific information about De Villa's career focus on public health issues, which is a concrete suggestion for improvement. It identifies a specific omission in the answer and provides guidance on what additional detail should be included to enhance the response. This aligns with the criteria for a constructive critique by specifying what is missing and how to address it.

**Classification**: Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Rachel?

**Answer**: Rachel seems to be a very carefree and bubbly person. She is not afraid of the man that killed a group of people. She also seems to be open to new people when she meets Josh and Sana.

**Critique**: The answer should mention that Rachel is Devyn's sister

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely that Rachel is Devyn's sister. This provides clear, actionable feedback that can be used to improve the answer by adding the specified detail. The critique is specific and directly addresses what is lacking in the response.

**Classification**: Constructive

---

### Sample 16/50 - [Non-Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The author is discussing the personal war on Brett Kavanaugh and how it is representative of the larger war on conservatives. The author argues that the Kavanaugh confirmation battle is not just about Kavanaugh, but about all conservatives who are subjected to personal wars by Democrats and the Resistance.

**Critique**: The English isn't great and could be refined

**Rationale**: The critique "The English isn't great and could be refined" is non-constructive because it vaguely points out a problem with the language quality without specifying what exactly is wrong or how it could be improved. It does not provide any specific examples of poor English or suggest any concrete improvements, leaving the author without clear guidance on how to refine the answer.

**Classification**: Non-Constructive

---

### Sample 17/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What kind of vehicle does Alan drive?

**Answer**: The compact Optra SRV could refer to a car, though not very sporty or interesting. It also could refer to a certain type of vehicle.

**Critique**: "could refer to a car, though not very sporty or interesting. It also could refer to a certain type of vehicle." - the unnecessary information ruined a perfectly good answer. This should be deleted. Replace "The" with "A" in "compact Optra SRV"

**Rationale**: The critique identifies specific parts of the answer that are unnecessary and suggests their removal, which is actionable feedback. It also provides a specific correction by suggesting a change from "The" to "A" in the phrase "compact Optra SRV," which is a concrete improvement suggestion. This makes the critique constructive as it provides clear guidance on how to improve the answer.

**Classification**: Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: President Trump says it doesn't matter if he misled the media about his son's infamous 2016 Trump Tower meeting with Russian nationals. Trump's lawyers admitted that he dictated a statement that Donald Trump Jr. released about the meeting. Trump's casual stance on telling the truth was also apparent in remarks he made about retired Army Lt. Gen. Michael Flynn, his former national security adviser who pleaded guilty to lying to the FBI.

**Critique**: "President Trump says it doesn't matter if he misled the media about his son's infamous 2016 Trump Tower meeting with Russian nationals." - while OK on its own, this statement needs a reason why the lie didn't matter. Add something about the New York Times.

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the statement about President Trump needs additional context to explain why the lie didn't matter. It also provides a concrete suggestion to include information about the New York Times, which is actionable and specific feedback that can improve the answer. This aligns with the criteria for a constructive critique as it specifies what is missing and how to address it.

**Classification**: Constructive

---

### Sample 19/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: The quote from the mayor of Paris, Anne Hidalgo, suggests that the new rules would get people to exercise when the streets are generally quieter.

**Critique**: This is to stop the spread of COVID-19

**Rationale**: The critique provided is non-constructive because it does not specify what is incorrect or missing in the answer. It vaguely suggests an alternative motivation without directly addressing the content of the answer or providing specific guidance on how to improve it. The critique lacks actionable feedback that would help refine the answer.

**Classification**: Non-Constructive

---

### Sample 20/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How old was Jiranová when she first won a tournament?

**Answer**: Jiranová won her first tournament in 2014 when she was 17 years old.

**Critique**: This is false. She would have been 18 or 19.

**Rationale**: The critique identifies a specific error in the answer by stating that the age given is incorrect. It provides the correct information by suggesting that Jiranová would have been 18 or 19 years old, which directly addresses the mistake and offers a correction. This makes the feedback actionable and specific.

**Classification**: Constructive

---

### Sample 21/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Primož's strategic importance.

**Answer**: Primož is part of a ridge which separates the Pivka basin from the Reka valley. It possesses a commanding view over the entire Pivka basin, making it an important military location. During the Second World War, it was fortified with tunnels as part of the Alpine Wall, yet they were never used in combat. In total, the tunnels were more than two kilometers long, but they have since been abandoned. Today, it is made accessible by marked trails, with one specifically designated for tourists and containing numerous information signs around its peak. Primož's strategic importance stems from its commanding view and its military tunnels.

**Critique**: "which separates" - change to "that separates"

**Rationale**: The critique identifies a specific issue with the wording in the answer, suggesting a change from "which separates" to "that separates." This is a clear and actionable piece of feedback, as it specifies exactly what needs to be changed and how to change it. The critique provides a concrete suggestion for improvement, making it constructive.

**Classification**: Constructive

---

### Sample 22/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the reveal at the end of the story.

**Answer**: Blocker is terminally ill, and the man with glasses tells him he only has a few months left. Blocker then realizes he has been fixated on the carpet, which is the color taupe. He cries.

**Critique**: This could be phrased differently to tie in better with the reveal. It should be said that Blocker only acknowledges this news and cries after he realizes what the color of the carpet is.

**Rationale**: The critique identifies a specific issue with the phrasing of the answer, suggesting that the sequence of events could be better aligned with the reveal. It provides a concrete suggestion on how to improve the answer by specifying that Blocker acknowledges the news and cries after realizing the carpet's color. This feedback is actionable and specific, making it clear what needs to be changed to improve the answer.

**Classification**: Constructive

---

### Sample 23/50 - [Non-Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Helena Jiranová is a Czech runner and sprinter who has had some success in international competitions. She is currently ranked first in Czech Republic in the 400 metres, fourth in the 60 meters hurdles, and eighth in the 100 meters hurdles. Her personal bests include a 53.77 sec. time in the 400 metres and an 8.31 sec. time in the 60 meters hurdles. Jiranová has experienced some success in international competitions, placing eighth in the 4 × 400 metres relay at the European Athletics Junior Championships and sixth in the 100 meters hurdles at the European Athletics U23 Championships.

**Critique**: Jiranova is not ranked first in Czech Republic in the 400 metres, fourth in the 60 meters hurdles, and eighth in the 100 meters hurdles. This whole sentence needs to be mended, as it is entirely false.

**Rationale**: The critique identifies a specific problem with the answer by stating that the rankings mentioned for Jiranová are incorrect. However, it does not provide the correct rankings or any specific information on what the accurate details should be. Therefore, while it points out an error, it lacks the actionable information needed to correct it.

**Classification**: Non-Constructive

---

### Sample 24/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique identifies a specific problem with the answer by stating that the factors mentioned did not lead to Jerry becoming a serial killer and suggests that these should be omitted. It also provides a concrete improvement suggestion by advising that the answer should be framed in speculative terms, as the text does not explicitly state the reasons. This feedback is actionable and specific, making it constructive.

**Classification**: Constructive

---

### Sample 25/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Where did Castor begin his career?

**Answer**: He began his career as a litigator in commercial law at the low firm Blank Rome in Philadelphia and Washington D.C.

**Critique**: The word "low" in this response needs to be changed to "law".

**Rationale**: The critique identifies a specific error in the answer, which is the incorrect use of the word "low" instead of "law." It provides the correct word that should be used, making it clear what needs to be fixed. This is a direct and actionable piece of feedback that improves the accuracy of the answer.

**Classification**: Constructive

---

### Sample 26/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the military tunnels in Primož?

**Answer**: The tunnels were dug as part of the long Alpine Wall. There were two tunnels totaling 5.2 kilometers along with brick-lined access shafts. They were never used for military purposes. They were built in 1930 and secured underground with steel encased in concrete with ventilation pipes and steel plates to prevent damage from aerial bombardment. Primož's military tunnels were destroyed by German forces in 1944.

**Critique**: "totaling 5.2 kilometers" - it was never mentioned exactly how long the tunnels were in the text.

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the exact length of the tunnels, "totaling 5.2 kilometers," was not mentioned in the original text. This provides clear feedback on what part of the answer may be inaccurate or unsupported by the source material. However, it does not provide the correct information or suggest how to address the issue, such as verifying the length or removing the unsupported detail.

**Classification**: Non-Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Who is the narrator?

**Answer**: The narrator is a member of a space agency. He is stuck on a shuttle while there is a mechanical problem he cannot fix.

**Critique**: The answer should be more precise about the narrator's job.

**Rationale**: The critique identifies a need for more precision regarding the narrator's job but does not specify what information is missing or how to improve the answer. It lacks actionable feedback or specific details that would help refine the answer. Without guidance on what precise information should be included, the critique remains vague.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Non-Constructive]

**Question**: How old was Sanuth when his cricket career took off?

**Answer**: It can be implied from the article that he was 19 years old.

**Critique**: Unnecessarily wordy answer

**Rationale**: The critique "Unnecessarily wordy answer" identifies a problem with the answer but does not provide specific guidance on how to improve it. It lacks details on which parts of the answer are considered wordy or suggestions on how to make it more concise. Without this information, the critique does not offer actionable feedback to improve the answer.

**Classification**: Non-Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: What does the train conductor give the narrator?

**Answer**: 

**Critique**: No response is given and a proper response needs to be generated. 

**Rationale**: The critique identifies that there is no response provided to the question, which is a specific problem. However, it does not offer any guidance or information on what the answer should include or how to generate a proper response. It lacks actionable feedback that would help improve the answer.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the cost effectiveness of Aldi?

**Answer**: The secret to Aldi's success is that they offered a few hundred well chosen product lines at low prices and they followed a military style of organization. 

**Critique**: It is omitted that low prices are made possible by massive purchasing. This was combined with a high ratio of sales per square meter of floor space, and ferocious cost control — the latter being Theo’s special skill. Little money was wasted on marketing, and none at all on making Aldi stores look elegant: goods were simply piled up along the aisles in packing cases.


**Rationale**: The critique identifies specific missing information that would enhance the answer's completeness regarding Aldi's cost-effectiveness. It provides detailed content that should be included, such as the role of massive purchasing, high sales per square meter, and cost control, which are crucial to understanding Aldi's pricing strategy. This feedback is actionable and specific, making it a constructive critique.

**Classification**: Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who first reported the incident?

**Answer**: The Wall Street Journal first reported the issues with the latest Intel firmware update.

**Critique**: "first reported the issues with the latest Intel firmware update." - superfluous details that may be irrelevant given the question. Should be deleted.

**Rationale**: The critique identifies a specific problem with the answer, namely that it includes superfluous details that may not be relevant to the question. It also provides a concrete suggestion for improvement by advising that the unnecessary details should be deleted. This makes the critique actionable and specific, aligning with the criteria for a constructive critique.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the narrator remember about Ms. Johnson?

**Answer**: The narrator remembers Ms. Johnson being with her baby while she, Ms. Johnson, and her husband were cleaning the kitchen. She also remembers Ms. Johnson's baby bag and the scar he received after he had jumped out of a window.

**Critique**: The response inaccurately describes Ms. Johnson and her husband cleaning the kitchen. It incorrectly mentions him getting a scar.

**Rationale**: The critique identifies specific inaccuracies in the answer, pointing out that the description of Ms. Johnson and her husband cleaning the kitchen is incorrect, as well as the mention of a scar. It provides clear information on what is wrong with the answer, which is necessary for making corrections. However, it does not provide the correct information or suggest how to fix these inaccuracies, which limits its constructiveness.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Non-Constructive]

**Question**: Write a ~5 sentence summary.

**Answer**: Shiza Shahid is a Pakistani social entrepreneur who co-founded the Malala Fund, a non-profit organisation that promotes education for girls. She is also well-known as the mentor of Nobel Peace Prize laureate Malala Yousafzai.

**Critique**: The summary is less than 5 sentences and does not include enough information about Shiza.

**Rationale**: The critique identifies that the summary is shorter than requested and lacks sufficient information about Shiza Shahid. However, it does not specify what additional information should be included or how to expand the summary to meet the requirements. Without specific guidance on what details are missing or how to improve the summary, the critique remains vague.

**Classification**: Non-Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about Hitchcock as a musician?

**Answer**: Hitchcock is a singer-songwriter. He has a rich, supple voice and his songs are the real attraction of the film. He has a large personal catalog. The songs in the film are from his latest album.

**Critique**: There was no mention of Hitchcock's latest album anywhere in the text. This part should be removed. 

**Rationale**: The critique identifies a specific problem in the answer by pointing out that the mention of Hitchcock's latest album is not supported by the text. It provides a clear and actionable suggestion to remove this part of the answer, which directly addresses the issue. This makes the critique specific and actionable, fulfilling the criteria for being constructive.

**Classification**: Constructive

---

### Sample 35/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about what type of alien the creature is?

**Answer**: The narrator describes the creature as an enigma and unlike anything else. it lacks even the slightest hint of movement, yet it commands the attention of every human. Daniel thinks that it looks like melted ice cream. The voices behind the machine tell Daniel that they are messengers, that the creature is one of those who represent them. The creature is multiple creatures and they are here as messengers. It says that Daniel's emissions are a beacon to something or someone dangerous.

**Critique**: Lacking movement only applies to the beginning, so this sentence can be rephrased to reflect that it's situational.

**Rationale**: The critique identifies a specific issue with the answer, namely that the description of the creature lacking movement is only applicable at the beginning of the story. It suggests rephrasing the sentence to reflect that the lack of movement is situational, providing a clear and actionable suggestion for improvement. This aligns with the criteria for a constructive critique as it specifies the problem and offers a way to fix it.

**Classification**: Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what happened in the 1940's.

**Answer**: In 1940, Averil Demuth wrote The House in the Mountains. In 1941, she wrote The Enchanted Islands and Sea Gypsies. In 1942, she married Anthony Cockbain. In 1942, he died after only one year of marriage. In 1953, she wrote The House of the Wind.

**Critique**: The last sentence is irrelevant to what is being asked. 

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the last sentence is irrelevant to the question about the 1940s. This provides clear guidance on what part of the answer should be removed to improve its relevance and focus. The critique is actionable and specific, as it tells exactly what is wrong and what needs to be fixed.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text have to say about the traits of the rocket?

**Answer**: It's 230 feet tall, destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space. Its engines will return to Earth following lift-off. The rocket carries Elon Musk's Tesla Roadster into space.

**Critique**: It is not stated: it is destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space.


**Rationale**: The critique identifies a specific omission in the answer by pointing out that it does not state the rocket is destined to deliver more than 50 passengers and cargo, and that the company claims it will have the power to launch them into space. This provides clear guidance on what information is missing and needs to be included to improve the answer.

**Classification**: Constructive

---

### Sample 38/50 - [Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: Intel has run into problems protecting its processing chips from the major Meltdown and Spectre vulnerabilities. It seems the issue effects systems running older Haswell chips.

**Critique**: "issue effects" - change "effects" to "affects"

**Rationale**: The critique identifies a specific error in the answer, pointing out the incorrect use of the word "effects" and providing the correct word "affects" to use instead. This is a clear example of correcting an error with the right answer, which is a key aspect of a constructive critique.

**Classification**: Constructive

---

### Sample 39/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the most interesting facts in the text. 

**Answer**: The Mechanics Educational Society of America was founded in 1933 by disgruntled members of the International Association of Machinists. Matthew Smith, Frank McCracken, and John Anderson pushed for a full-fledged union. In June 1933, the U.S. Congress passed the National Industrial Recovery Act of 1933 which protected the collective bargaining rights of unions. A month later, MESA began an organizing drive in Detroit, Pontiac, Michigan, and Flint, Michigan.

**Critique**: The response left out key happenings in MESA's history.

**Rationale**: The critique provided is non-constructive because it vaguely states that key happenings in MESA's history are missing without specifying what those key happenings are. It does not provide any specific information or guidance on what should be included to improve the answer. For a critique to be constructive, it should identify specific missing details or provide concrete suggestions for improvement.

**Classification**: Non-Constructive

---

### Sample 40/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Where is the old man headed?

**Answer**: He is headed toward a statue of a woman, who he thinks is his daughter.

**Critique**: He knows the statue of his daughter.

**Rationale**: The critique "He knows the statue of his daughter" is vague and does not provide specific feedback or corrections to improve the answer. It does not clearly identify what is wrong with the original answer or how it should be corrected. The critique lacks actionable information that would help refine the answer.

**Classification**: Non-Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why is the civilian ship empty?

**Answer**: It turns out that Roger murdered Drake and then went mad killing everyone on board.

**Critique**: Although Roger killed Drake, it's not true that he went mad and killed everyone on board. The model's answer is inaccurate, insufficient, and should provide relevant and correct details from the story to answer the question.

**Rationale**: The critique identifies a specific inaccuracy in the answer by stating that it is not true that Roger went mad and killed everyone on board. However, it fails to provide the correct information or details that should replace the inaccurate part of the answer. The critique points out the problem but does not offer a solution or the correct details needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Describe the relationship between the two characters.

**Answer**: The two characters have a mutual attraction and connection with one another. The protagonist is taken under the spell of the radiant smile of his companion. The two share an emotional and vibrant connection that is unbreakable.

**Critique**: There's an attraction for sure. However, it's temporary, and the answer completely makes up the unbreakable part.

**Rationale**: The critique identifies a specific problem with the answer by pointing out that the description of the relationship as "unbreakable" is incorrect and not supported by the context. It provides the correct information by stating that the attraction is temporary, which helps in improving the accuracy of the answer. This makes the critique actionable and specific.

**Classification**: Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Why does the narrator suggest that they must terminate the patient's pregnancy?

**Answer**: The patient's fetus is male and, because of the current birth quotas, doctors are allowed to terminate pregnancies with male fetuses so as to make way for a more accurate representation of baby girls in the region.

**Critique**: "so as to" - use "to"

**Rationale**: The critique specifically identifies a language issue in the answer by pointing out the phrase "so as to" and suggests replacing it with "to." This provides a clear and actionable suggestion for improving the clarity and conciseness of the sentence. The critique is specific and directly addresses a part of the answer that can be improved.

**Classification**: Constructive

---

### Sample 44/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Summer?

**Answer**: Summer is a girl in Jeffery's school who always seems to be in his thoughts. She has a perpetual sunflower dress and dark hair.
She's beautiful, and Jeffery has a crush on her.
The author describes Summer as someone who likes to write in a journal. All of Summer's routines are scheduled around the time she waits for Jeffery's class to finish, so she can see him.

**Critique**: The last sentence of this response needs to be omitted as it is not fully accurate.

**Rationale**: The critique identifies a specific problem with the answer, namely that the last sentence is not fully accurate. It provides a clear and actionable suggestion to omit the last sentence, which is a constructive way to improve the answer by removing incorrect information. This aligns with the criteria for a constructive critique as it specifies exactly what needs to be changed.

**Classification**: Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Trump's issues with law enforcement?

**Answer**: Trump is at war with his own law enforcement officials. He has backup from his party. The day after Trump's State of the Union address was dominated by an extraordinary series of developments in which the Federal Bureau of Investigation and Department of Justice challenged Trump both on the record and through what appeared to be anonymous leaks to CNN. The Republican attacks have been encouraged by increasingly conspiratorial Fox coverage centred on what hosts have called a "Deep State" attempting to topple Trump.

**Critique**: The answer omits that Trump's allegations are due to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely the context of the FBI probe investigating Trump's ties with Russia concerning the 2016 presidential elections. This provides actionable feedback by specifying what additional detail should be included to improve the completeness of the answer.

**Classification**: Constructive

---

### Sample 46/50 - [Non-Constructive]

**Question**: Explain the new app update.

**Answer**: The new update is to require social security numbers for all users of the company's app. This is meant to increase security and make it harder for people to create fake accounts.

**Critique**: There is no evidence that suggests the meaning behind the app update requiring social security numbers.

**Rationale**: The critique points out a lack of evidence supporting the claim about the app update's purpose, but it does not provide specific information on what evidence is missing or how to address this issue. It fails to offer actionable feedback or suggest improvements to the answer.

**Classification**: Non-Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Are there regional variations?

**Answer**: Yes, there are regional variations.

**Critique**: Add the regional variation mentioned - the more subdued Taiwanese version.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely the mention of "the more subdued Taiwanese version" as a regional variation. This provides actionable feedback by specifying exactly what should be added to improve the answer.

**Classification**: Constructive

---

### Sample 48/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Zofia Nehringowa's sport results?

**Answer**: Zofia Nehringowa was a Polish long track speed skater who set a world record in all four individual distances (500 m, 1000 m, 1500 m, 3000 m) in 1931 and 1935. Nehringowa competed at the 1932 European Speed Skating Championships for Men and set a women's world record in the 1500m during these race. Nehringowa represented Poland at the World Allround Speed Skating Championships for Women in 1939 where she finished 5th overall.

**Critique**: In 1931, Nehringowa set the world records in the 500m, 1000m, 1500m, 3000m and 5000m. These results were approved by the ISU's the first women's speed skating world records. In 1932, Nehringowa broke the women's world records in the 1500m and 1000m. In 1935 she improved her own world records in the 3000m, 5000m and 10 000m. Change the response to reflect these results.

**Rationale**: The critique provides specific corrections to the answer by detailing the accurate historical records set by Zofia Nehringowa. It specifies the years and distances for which she set or improved world records, correcting the inaccuracies in the original answer. Additionally, it gives clear instructions to change the response to reflect these accurate results, making it actionable and specific.

**Classification**: Constructive

---

### Sample 49/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the parameters for an entry?

**Answer**: [rewrite]

**Critique**: The question was unconventional and the response should have been "No Answer" or "That information can't be found." 

**Rationale**: The critique identifies a problem with the answer, suggesting that the response should have been "No Answer" or "That information can't be found." However, it does not provide specific guidance on how to improve the answer or what exactly is wrong with the current response. It lacks actionable feedback that would help in revising the answer effectively.

**Classification**: Non-Constructive

---

### Sample 50/50 - [Constructive]

**Question**: Who is the target audience?

**Answer**: The target audience for this website is those who are interested in the St. Jacobs farmer's market and who were especially affected by the recent fire that destroyed the market building.

**Critique**: The fire and the farmers' market are only briefly mentioned; the article targets potential customers for The Fritter Co.

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the focus on the fire and the farmers' market is insufficient and that the article actually targets potential customers for The Fritter Co. This provides clear guidance on what aspect of the answer needs to be corrected or expanded upon.

**Classification**: Constructive

---

