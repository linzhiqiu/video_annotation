# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (summarization)
- **Total Dataset Size**: 4505 critique samples
- **Filtered Dataset Size** (summarization): 1728 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 42
- **Timestamp**: 20251015_0236

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

A CONSTRUCTIVE critique provides actionable, specific feedback that helps improve the answer. It must identify a problem AND give enough information to fix it. This includes:

1. **Providing missing information**: "Some people are worried due to the virus" or "He was caught, though" (gives the actual content that should be added)
2. **Correcting errors with the right answer**: "It should be white, not black" or "The horse is brown, not white" or "There is no evidence it was a daughter, not a son" (points out what's wrong and what's right)
3. **Specifying omitted details**: "It's omitted that the child was being crushed under a roof"
4. **Identifying specific problems in the text**: "The last sentence is repetitive and not wholly relevant" (tells you exactly what part needs fixing)
5. **Giving concrete improvement suggestions**: "Combine sentences that convey the same idea" or "Use X instead of Y"

A NON-CONSTRUCTIVE critique only describes a problem without providing the information or guidance needed to fix it:
- "This doesn't answer the question" (doesn't say what the answer should be)
- "More details needed" (doesn't specify what details)
- "This is wrong" or "This is incomplete" (too vague, doesn't say what specifically)
- "The story never discusses X" (doesn't tell you what X is or should be)
- "There's an error here" (doesn't identify which part or what the error is)
- "This could be better" (no specifics on what or how)

Key distinction: 
- ✅ CONSTRUCTIVE: Points to a specific issue you can act on ("sentence X is repetitive", "missing Y", "should be Z not W")
- ❌ NON-CONSTRUCTIVE: Vague problem statement with no specifics ("something is wrong", "needs improvement")

Note: A critique that says "no evidence for X" or "not X" is constructive if it clearly indicates what the correct information is or should be (e.g., "no evidence it was a daughter, not a son" tells you it was a son).

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
| Constructive | 26 | 52.00% |
| Non-Constructive | 24 | 48.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Answer the following question based on the above passage:

Describe the ways in which the woman fights off her assailant.

**Answer**: The woman first kicks the assailant in the groin and uses the remaining piece of a broken vase to stab the assailant's eye. She is then able to escape from the house and its occupants to save herself and her baby. The altercation on the ground makes the woman realize she has to fight her way out in order to save herself and her baby. She must be proactive and use any means necessary in order to escape her attackers. Although it seems like an uphill battle, she does not give up. She uses her strength and ingenuity to subdue the assailants. She uses whatever is at her disposal to create a way to get out of the situation alive.

**Critique**: The response implies that the baby belongs to the narrator, which is inaccurate.

**Rationale**: The critique identifies a specific issue in the answer, which is the incorrect implication that the baby belongs to the narrator. However, it does not provide the correct information or guidance on how to fix this error, such as clarifying who the baby actually belongs to or suggesting a rephrasing to avoid the implication. Therefore, it lacks the actionable feedback needed to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Answer the following question based on the above passage:

Summarize the reveal at the end of the story.

**Answer**: Blocker is terminally ill, and the man with glasses tells him he only has a few months left. Blocker then realizes he has been fixated on the carpet, which is the color taupe. He cries.

**Critique**: This could be phrased differently to tie in better with the reveal. It should be said that Blocker only acknowledges this news and cries after he realizes what the color of the carpet is.

**Rationale**: The critique identifies a problem with the phrasing of the answer, suggesting that it could be improved to better align with the reveal. However, it does not provide specific guidance on how to rephrase the answer or what specific changes should be made to improve the connection between the realization of the carpet's color and Blocker's reaction. The critique lacks actionable feedback that would help improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Answer the following question based on the above passage:

Why does Devyn think that the girls are weird?

**Answer**: Because they don't text a guy who gave Sana his number in the ice cream shop. The girls do not believe in the soulmate idea.

**Critique**: The response should be written as a full sentence. 

**Rationale**: The critique points out that the response should be written as a full sentence, but it does not provide specific guidance on how to rewrite the answer into a full sentence. It identifies a problem but lacks actionable feedback or a suggestion for improvement.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: No answer

**Critique**: A response  is possible and necessary

**Rationale**: The critique "A response is possible and necessary" is non-constructive because it only states that an answer is needed without providing any guidance or specifics on what the answer should include. It does not identify any specific issues with the current lack of an answer or suggest what information should be provided to address the question.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator can be described as a keen and careful sergeant in the army with a caring family, who sacrifices his wellbeing as well as that of his men for the greater good. He is valiant and resourceful, and he is committed to his men for the time being, commanding their lives in the shells of their rifles. He is conflicted by the fact that he unwillingly leads the men, who stand shoulder by shoulder to the slaughter with camaraderie, pride, fear, and anger. He also admires his foe, the Germans, for their bravery and tenacity. The narrator is also confident that he will not die with the Germans because he is a lucky man. His spirit dwindles as the Germans begin unleashing massive weaponry and his fellows are being killed left and right. In the end, he falls into the water, where he is saved by the British soldiers.

**Critique**: The listing of these emotions does not make sense given context

**Rationale**: The critique provided is non-constructive because it vaguely states that the listing of emotions does not make sense without specifying which emotions are problematic or why they are inappropriate in the context. It does not offer any guidance on how to correct or improve the answer, such as suggesting which emotions should be included or how to better convey the narrator's emotional state.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Answer the following question based on the above passage:

What are the consequences of the increase in Ebike activity for the company?

**Answer**: The company is having a hard time catching up with the increase in orders. They are also having a hard time with the backlog of emails and phone calls. The increase in ebikes has also led to a backlog in new product development.

**Critique**: The information is not accurate and should reflect that the company is able to keep up with the demand. 

**Rationale**: The critique identifies a specific inaccuracy in the answer by stating that the company is actually able to keep up with the demand, which directly contradicts the information provided in the answer. This provides clear guidance on what needs to be corrected in the answer, making it actionable and specific.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator is a sergeant in the army. He has a caring family and a spouse. He has medals to his name and a desire to live. He is a leader of men. He is a survivor of the war.

**Critique**: It is omitted he was rescued by the British.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely that the narrator was rescued by the British. This provides clear guidance on what needs to be added to improve the answer, making it actionable and specific.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique identifies that the factors listed in the answer are not relevant to Jerry becoming a serial killer and suggests that they should be omitted. It also provides guidance on how the answer should be framed, indicating that it should be in speculative terms since the text does not explicitly state the reasons. This provides specific, actionable feedback to improve the answer.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

Summarize what happened in the 1940's.

**Answer**: In 1940, Averil Demuth wrote The House in the Mountains. In 1941, she wrote The Enchanted Islands and Sea Gypsies. In 1942, she married Anthony Cockbain. In 1942, he died after only one year of marriage. In 1953, she wrote The House of the Wind.

**Critique**: The last sentence is irrelevant to what is being asked. 

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the last sentence is irrelevant to the question about the 1940s. This provides clear guidance on what part of the answer needs to be addressed or removed to improve its relevance to the question. By specifying the irrelevance of the last sentence, the critique offers actionable feedback.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

What does the article say about Hitchcock as a musician?

**Answer**: Hitchcock is a singer-songwriter. He has a rich, supple voice and his songs are the real attraction of the film. He has a large personal catalog. The songs in the film are from his latest album.

**Critique**: There was no mention of Hitchcock's latest album anywhere in the text. This part should be removed. 

**Rationale**: The critique identifies a specific problem in the answer, which is the incorrect mention of Hitchcock's latest album. It provides clear guidance on how to fix the issue by suggesting the removal of this incorrect information. This makes the critique actionable and specific, as it points out exactly what part of the answer is incorrect and what should be done to correct it.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the views of the opposing sides.

**Answer**: Republicans are counting on these judges to dismantle reproductive rights, marriage equality, and the separation of church and state and to use the courts to shred the New Deal and regulations that protect the people from corporate power. They believe the Democrats are letting Mitch McConnell and Donald Trump do this to consolidate their power and are counting on the voters to stop them. The Democratic Party, in some cases, appears to be acquiescing.

**Critique**: The Republicans are stated to believe Democrats are letting McConnell and Trump do their thing to consolidate their power, which is made up.

**Rationale**: The critique identifies a specific issue in the answer by pointing out that the statement about Republicans believing Democrats are letting McConnell and Trump consolidate power is incorrect. However, it does not provide the correct information or suggest how to fix the error, making it non-constructive. It lacks actionable feedback or a clear correction to improve the answer.

**Classification**: Non-Constructive

---

### Sample 2/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What happens to the child?

**Answer**: The child drowns and the priest ignores his plea for help.

**Critique**: More background detail needs to be added to this to explain how and why the child was drowning. 

**Rationale**: The critique identifies a need for additional background detail but does not specify what specific information is missing or how to improve the answer. It points out a problem but lacks actionable guidance or specific suggestions on what details should be included to enhance the answer. Therefore, it does not meet the criteria for a constructive critique.

**Classification**: Non-Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Summer?

**Answer**: Summer is a girl in Jeffery's school who always seems to be in his thoughts. She has a perpetual sunflower dress and dark hair.
She's beautiful, and Jeffery has a crush on her.
The author describes Summer as someone who likes to write in a journal. All of Summer's routines are scheduled around the time she waits for Jeffery's class to finish, so she can see him.

**Critique**: The last sentence of this response needs to be omitted as it is not fully accurate.

**Rationale**: The critique identifies a specific issue with the answer, namely that the last sentence is not fully accurate and should be omitted. This provides clear guidance on how to improve the answer by removing the problematic part, which aligns with the criteria for a constructive critique. The critique specifies exactly which part of the text needs to be addressed and offers a concrete suggestion for improvement.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the military tunnels in Primož?

**Answer**: The tunnels were dug as part of the long Alpine Wall. There were two tunnels totaling 5.2 kilometers along with brick-lined access shafts. They were never used for military purposes. They were built in 1930 and secured underground with steel encased in concrete with ventilation pipes and steel plates to prevent damage from aerial bombardment. Primož's military tunnels were destroyed by German forces in 1944.

**Critique**: "totaling 5.2 kilometers" - it was never mentioned exactly how long the tunnels were in the text.

**Rationale**: The critique identifies a specific issue with the answer, pointing out that the exact length of the tunnels ("totaling 5.2 kilometers") was not mentioned in the original text. This is a constructive critique because it highlights a specific inaccuracy in the answer, allowing the responder to correct the information by either verifying the length or removing the unsupported detail.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about Hitchcock as a musician?

**Answer**: Hitchcock is a singer-songwriter. He has a rich, supple voice and his songs are the real attraction of the film. He has a large personal catalog. The songs in the film are from his latest album.

**Critique**: There was no mention of Hitchcock's latest album anywhere in the text. This part should be removed. 

**Rationale**: The critique identifies a specific problem in the answer, which is the incorrect mention of Hitchcock's latest album. It provides clear guidance on how to fix the issue by suggesting the removal of this incorrect information. This makes the critique actionable and specific, as it points out exactly what part of the answer is incorrect and what should be done to correct it.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the most interesting facts in the text. 

**Answer**: The Mechanics Educational Society of America was founded in 1933 by disgruntled members of the International Association of Machinists. Matthew Smith, Frank McCracken, and John Anderson pushed for a full-fledged union. In June 1933, the U.S. Congress passed the National Industrial Recovery Act of 1933 which protected the collective bargaining rights of unions. A month later, MESA began an organizing drive in Detroit, Pontiac, Michigan, and Flint, Michigan.

**Critique**: The response left out key happenings in MESA's history.

**Rationale**: The critique identifies a problem by stating that key happenings in MESA's history were left out, but it does not specify which events or details are missing. Without this information, the critique does not provide actionable feedback that can be used to improve the answer. It lacks the specificity needed to be constructive, as it does not guide the responder on what specific content should be added or corrected.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the parameters for an entry?

**Answer**: [rewrite]

**Critique**: The question was unconventional and the response should have been "No Answer" or "That information can't be found." 

**Rationale**: The critique identifies a problem with the answer, suggesting that the response should have been "No Answer" or "That information can't be found." However, it does not provide specific guidance on how to rewrite the answer or what specific information is missing or incorrect. It lacks actionable feedback that would help improve the answer beyond suggesting a different type of response.

**Classification**: Non-Constructive

---

### Sample 8/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why is the civilian ship empty?

**Answer**: It turns out that Roger murdered Drake and then went mad killing everyone on board.

**Critique**: Although Roger killed Drake, it's not true that he went mad and killed everyone on board. The model's answer is inaccurate, insufficient, and should provide relevant and correct details from the story to answer the question.

**Rationale**: The critique identifies that the answer is inaccurate by stating that Roger did not go mad and kill everyone on board, but it fails to provide the correct information or details from the story that would accurately answer the question. It points out the problem but does not offer a solution or specific guidance on how to correct the answer.

**Classification**: Non-Constructive

---

### Sample 9/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique identifies that the factors listed in the answer are not relevant to Jerry becoming a serial killer and suggests that they should be omitted. It also provides guidance on how the answer should be framed, indicating that it should be in speculative terms since the text does not explicitly state the reasons. This provides specific, actionable feedback to improve the answer.

**Classification**: Constructive

---

### Sample 10/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the cost effectiveness of Aldi?

**Answer**: The secret to Aldi's success is that they offered a few hundred well chosen product lines at low prices and they followed a military style of organization. 

**Critique**: It is omitted that low prices are made possible by massive purchasing. This was combined with a high ratio of sales per square meter of floor space, and ferocious cost control — the latter being Theo’s special skill. Little money was wasted on marketing, and none at all on making Aldi stores look elegant: goods were simply piled up along the aisles in packing cases.


**Rationale**: The critique identifies specific information that is missing from the answer regarding Aldi's cost-effectiveness. It provides detailed content that should be included to enhance the answer, such as the role of massive purchasing, high sales per square meter, and cost control. This feedback is actionable and specific, as it clearly outlines what additional details should be incorporated to improve the answer's completeness and accuracy.

**Classification**: Constructive

---

### Sample 11/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about de Villa's opinion on public health?

**Answer**: She has urged for the prevention of communicable diseases and wants the brands to clamp down on misleading anti-vaccination information by minimizing the public's access to these rumors. She has also called for a ban on vaccine exemptions if an individual has certain beliefs that say they should not be vaccinated.

**Critique**: Additional detail about how De Villa's whole career is around public health issues should be stated. 

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely, the detail about De Villa's career focus on public health issues. This provides actionable feedback by specifying what additional content should be included to improve the answer.

**Classification**: Constructive

---

### Sample 12/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Primož's strategic importance.

**Answer**: Primož is part of a ridge which separates the Pivka basin from the Reka valley. It possesses a commanding view over the entire Pivka basin, making it an important military location. During the Second World War, it was fortified with tunnels as part of the Alpine Wall, yet they were never used in combat. In total, the tunnels were more than two kilometers long, but they have since been abandoned. Today, it is made accessible by marked trails, with one specifically designated for tourists and containing numerous information signs around its peak. Primož's strategic importance stems from its commanding view and its military tunnels.

**Critique**: "which separates" - change to "that separates"

**Rationale**: The critique identifies a specific issue with the wording in the answer, suggesting a change from "which separates" to "that separates." This is a concrete suggestion that provides clear guidance on how to improve the sentence structure, making it a constructive critique. The critique directly addresses a grammatical choice, offering a specific correction that can be implemented to enhance the clarity or correctness of the text.

**Classification**: Constructive

---

### Sample 13/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about what type of alien the creature is?

**Answer**: The narrator describes the creature as an enigma and unlike anything else. it lacks even the slightest hint of movement, yet it commands the attention of every human. Daniel thinks that it looks like melted ice cream. The voices behind the machine tell Daniel that they are messengers, that the creature is one of those who represent them. The creature is multiple creatures and they are here as messengers. It says that Daniel's emissions are a beacon to something or someone dangerous.

**Critique**: Lacking movement only applies to the beginning, so this sentence can be rephrased to reflect that it's situational.

**Rationale**: The critique identifies a specific issue with the answer, which is the description of the creature's lack of movement. It suggests that the sentence should be rephrased to indicate that the lack of movement is only applicable at the beginning, providing clear guidance on how to improve the answer. This makes the critique actionable and specific, as it points out exactly what needs to be adjusted and how.

**Classification**: Constructive

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the tension in the story. 

**Answer**: The tension in the story seems to stem from a fallout between the two main characters. There is also the event that happened three years prior to the story.

**Critique**: The event three years ago, an accident, seems to be the point where the duo separated.

**Rationale**: The critique provides specific information about the event that occurred three years ago, identifying it as an accident and suggesting it as the pivotal moment for the separation of the two main characters. This adds clarity and context to the answer, which previously only vaguely mentioned an event without specifying its nature or significance. By doing so, the critique offers actionable feedback that can improve the answer's completeness and accuracy.

**Classification**: Constructive

---

### Sample 15/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the narrator remember about Ms. Johnson?

**Answer**: The narrator remembers Ms. Johnson being with her baby while she, Ms. Johnson, and her husband were cleaning the kitchen. She also remembers Ms. Johnson's baby bag and the scar he received after he had jumped out of a window.

**Critique**: The response inaccurately describes Ms. Johnson and her husband cleaning the kitchen. It incorrectly mentions him getting a scar.

**Rationale**: The critique identifies specific inaccuracies in the answer, pointing out that the description of Ms. Johnson and her husband cleaning the kitchen is incorrect, as well as the mention of a scar. However, it does not provide the correct information or guidance on how to fix these inaccuracies, such as what the narrator actually remembers about Ms. Johnson. Therefore, it lacks the actionable feedback needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 16/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything that happened in the 1990s.

**Answer**: No answer

**Critique**: There were events mentioned in the text that took place in 1996 and 1993.

**Rationale**: The critique identifies that there are events from 1996 and 1993 mentioned in the text, but it does not provide any specific guidance or information on how to incorporate these events into the answer. It merely points out that events from those years exist without detailing what those events are or how they should be summarized in the answer. Therefore, it lacks the actionable feedback necessary to improve the answer.

**Classification**: Non-Constructive

---

### Sample 17/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Trump's issues with law enforcement?

**Answer**: Trump is at war with his own law enforcement officials. He has backup from his party. The day after Trump's State of the Union address was dominated by an extraordinary series of developments in which the Federal Bureau of Investigation and Department of Justice challenged Trump both on the record and through what appeared to be anonymous leaks to CNN. The Republican attacks have been encouraged by increasingly conspiratorial Fox coverage centred on what hosts have called a "Deep State" attempting to topple Trump.

**Critique**: The answer omits that Trump's allegations are due to the FBI probe investigating his ties with Russia regarding the 2016 presidential elections.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely the context of the FBI probe investigating Trump's ties with Russia concerning the 2016 presidential elections. This provides actionable feedback by specifying what additional detail should be included to improve the completeness of the answer. By pointing out this omission, the critique gives clear guidance on how to enhance the response.

**Classification**: Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Rachel?

**Answer**: Rachel seems to be a very carefree and bubbly person. She is not afraid of the man that killed a group of people. She also seems to be open to new people when she meets Josh and Sana.

**Critique**: The answer should mention that Rachel is Devyn's sister

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely that Rachel is Devyn's sister. This provides clear, actionable feedback that can be used to improve the answer by adding this detail. The critique specifies exactly what is missing, making it constructive.

**Classification**: Constructive

---

### Sample 19/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text have to say about the traits of the rocket?

**Answer**: It's 230 feet tall, destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space. Its engines will return to Earth following lift-off. The rocket carries Elon Musk's Tesla Roadster into space.

**Critique**: It is not stated: it is destined to deliver more than 50 passengers and cargo. The company says it will have the power to launch them into space.


**Rationale**: The critique identifies a specific issue by pointing out that the text does not state that the rocket is destined to deliver more than 50 passengers and cargo, and that the company claims it will have the power to launch them into space. However, it does not provide any guidance or information on how to address this issue or what the correct information should be. It merely repeats part of the answer without offering a solution or improvement.

**Classification**: Non-Constructive

---

### Sample 20/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the main character's situation changes over the story.

**Answer**: Chad's story begins with him searching through the ship for survivors. He finds the captain, who gives him command of the ship. Chad is in disbelief. He leaves the ship to escape the war.

**Critique**: He doesn't leave the ship.

**Rationale**: The critique identifies a specific error in the answer by stating that the main character, Chad, does not leave the ship. However, it does not provide the correct information or suggest how to fix the error, such as what actually happens instead of leaving the ship. Therefore, it lacks the actionable guidance needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 21/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the reveal at the end of the story.

**Answer**: Blocker is terminally ill, and the man with glasses tells him he only has a few months left. Blocker then realizes he has been fixated on the carpet, which is the color taupe. He cries.

**Critique**: This could be phrased differently to tie in better with the reveal. It should be said that Blocker only acknowledges this news and cries after he realizes what the color of the carpet is.

**Rationale**: The critique identifies a problem with the phrasing of the answer, suggesting that it could be improved to better align with the reveal. However, it does not provide specific guidance on how to rephrase the answer or what specific changes should be made to improve the connection between the realization of the carpet's color and Blocker's reaction. The critique lacks actionable feedback that would help improve the answer.

**Classification**: Non-Constructive

---

### Sample 22/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: The quote from the mayor of Paris, Anne Hidalgo, suggests that the new rules would get people to exercise when the streets are generally quieter.

**Critique**: This is to stop the spread of COVID-19

**Rationale**: The critique provided is non-constructive because it only states a reason for the exercise ban without specifying how the answer should be improved or what specific information should be included. It does not provide actionable feedback or suggest how to incorporate the information about stopping the spread of COVID-19 into the answer.

**Classification**: Non-Constructive

---

### Sample 23/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about Zofia Nehringowa's sport results?

**Answer**: Zofia Nehringowa was a Polish long track speed skater who set a world record in all four individual distances (500 m, 1000 m, 1500 m, 3000 m) in 1931 and 1935. Nehringowa competed at the 1932 European Speed Skating Championships for Men and set a women's world record in the 1500m during these race. Nehringowa represented Poland at the World Allround Speed Skating Championships for Women in 1939 where she finished 5th overall.

**Critique**: In 1931, Nehringowa set the world records in the 500m, 1000m, 1500m, 3000m and 5000m. These results were approved by the ISU's the first women's speed skating world records. In 1932, Nehringowa broke the women's world records in the 1500m and 1000m. In 1935 she improved her own world records in the 3000m, 5000m and 10 000m. Change the response to reflect these results.

**Rationale**: The critique provides specific corrections to the information given in the answer. It details the exact years and events where Zofia Nehringowa set or broke world records, including the distances and the fact that these were recognized by the ISU as the first women's speed skating world records. This gives clear guidance on how to amend the original answer to accurately reflect Nehringowa's achievements.

**Classification**: Constructive

---

### Sample 24/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what happened in the 1940's.

**Answer**: In 1940, Averil Demuth wrote The House in the Mountains. In 1941, she wrote The Enchanted Islands and Sea Gypsies. In 1942, she married Anthony Cockbain. In 1942, he died after only one year of marriage. In 1953, she wrote The House of the Wind.

**Critique**: The last sentence is irrelevant to what is being asked. 

**Rationale**: The critique identifies a specific issue with the answer by pointing out that the last sentence is irrelevant to the question about the 1940s. This provides clear guidance on what part of the answer needs to be addressed or removed to improve its relevance to the question. By specifying the irrelevance of the last sentence, the critique offers actionable feedback.

**Classification**: Constructive

---

### Sample 25/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator can be described as a keen and careful sergeant in the army with a caring family, who sacrifices his wellbeing as well as that of his men for the greater good. He is valiant and resourceful, and he is committed to his men for the time being, commanding their lives in the shells of their rifles. He is conflicted by the fact that he unwillingly leads the men, who stand shoulder by shoulder to the slaughter with camaraderie, pride, fear, and anger. He also admires his foe, the Germans, for their bravery and tenacity. The narrator is also confident that he will not die with the Germans because he is a lucky man. His spirit dwindles as the Germans begin unleashing massive weaponry and his fellows are being killed left and right. In the end, he falls into the water, where he is saved by the British soldiers.

**Critique**: The listing of these emotions does not make sense given context

**Rationale**: The critique provided is non-constructive because it vaguely states that the listing of emotions does not make sense without specifying which emotions are problematic or why they are inappropriate in the context. It does not offer any guidance on how to correct or improve the answer, such as suggesting which emotions should be included or how to better convey the narrator's emotional state.

**Classification**: Non-Constructive

---

### Sample 26/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why do the police keep almost summoning "Pee Man"?

**Answer**: [rewrite]

**Critique**: No response.

**Rationale**: The critique provided is essentially an empty critique, which is appropriate if the answer is already correct and requires no changes. Since the critique does not identify any issues or suggest improvements, it implies that the answer is satisfactory as it stands. Therefore, in this context, the lack of critique is considered constructive because it indicates that no changes are necessary.

**Classification**: Constructive

---

### Sample 27/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about why Thompson wants to fight Lawler?

**Answer**: Thompson wants to fight Lawler because he believes it would show that he is still in the game and deserves another shot at the title. Thompson believes Lawler is one of the best strikers in the welterweight division.

**Critique**: This is not just a belief. 

**Rationale**: The critique provided is non-constructive because it only states that the answer is not just a belief without specifying what the correct information should be or how to improve the answer. It fails to provide actionable feedback or specific details that would help in correcting or enhancing the response.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about mental illness?

**Answer**: The man seems to suffer from schizophrenia. He cannot stop staring at the floor, at the time where the story takes place, the carpet. He is found in an institution after a mental breakdown from not being in control of his own life. He isn't able to distinguish what is a hallucination and what isn't. He seems to get lost in it and feels a sense of panic.

**Critique**: The story does not say anything specific about mental illness and the answer's suggestion the main character suffers from schizophrenia is completely unfounded. At best, the main character appears to be a little obsessive in his attempts to identify the color of the carpet, but much of the answer is untrue.

**Rationale**: The critique identifies a specific issue with the answer, stating that the suggestion of schizophrenia is unfounded and that the story does not specifically address mental illness. However, it does not provide any guidance on how to correct the answer or what the correct interpretation should be. It points out the problem but lacks actionable feedback or specific corrections.

**Classification**: Non-Constructive

---

### Sample 29/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What are the three possible approaches that music directors need to make choices about the instrumental accompaniment?

**Answer**: a capella, instruments doubling the vocal lines, or a basso continuo

**Critique**: A little explanation of the approaches would have made the response much better.

**Rationale**: The critique identifies a potential area for improvement by suggesting that the answer could be enhanced with additional explanation. However, it does not specify what kind of explanation is needed or provide any guidance on what information should be included to improve the answer. It lacks actionable specifics that would help the answerer know exactly how to enhance their response.

**Classification**: Non-Constructive

---

### Sample 30/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about education?

**Answer**: Elizabeth Benedict is an American author who lives in New York City. She works as a college admissions consultant. She is the founder and president of Don't Sweat the Essay, Inc., which focuses on coaching students for college and graduate school application essays. She attended Barnard College. She has been on the fiction faculty of the New York State Summer Writers Institute, at Skidmore College, since 1997.

**Critique**: The text does not talk about education in general as a subject matter. The question does not specify if it is referring to Benedict's background education.

**Rationale**: The critique identifies that the answer does not address the question about education in general, but it fails to provide specific guidance on how to correct the answer. It points out a potential misunderstanding of the question but does not offer a solution or suggest what information should be included to properly address the question about education. Therefore, it lacks actionable feedback.

**Classification**: Non-Constructive

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What are the consequences of the increase in Ebike activity for the company?

**Answer**: The company is having a hard time catching up with the increase in orders. They are also having a hard time with the backlog of emails and phone calls. The increase in ebikes has also led to a backlog in new product development.

**Critique**: The information is not accurate and should reflect that the company is able to keep up with the demand. 

**Rationale**: The critique identifies a specific inaccuracy in the answer by stating that the company is actually able to keep up with the demand, which directly contradicts the information provided in the answer. This provides clear guidance on what needs to be corrected in the answer, making it actionable and specific.

**Classification**: Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how the queen changes over the story.

**Answer**: The queen is the wife of the king. She is on a ship with her baby when the ship is struck by lightning, and she and the baby are sent overboard. The dragon, who is one of the humans, saves the baby from the sea, taking it to its home on the island. The dragon takes the queen to save her life, but the king hates her for abandoning the baby. She is a mother who has lost her child, and the king of a country that hates her.

**Critique**: The information relayed in the summary lack coherence as the details are incorrect,

**Rationale**: The critique provided is non-constructive because it only states that the summary lacks coherence and contains incorrect details without specifying what those incorrect details are or how the coherence can be improved. It does not offer any specific guidance or corrections to improve the answer, leaving the reader without actionable feedback.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Describe the ways in which the woman fights off her assailant.

**Answer**: The woman first kicks the assailant in the groin and uses the remaining piece of a broken vase to stab the assailant's eye. She is then able to escape from the house and its occupants to save herself and her baby. The altercation on the ground makes the woman realize she has to fight her way out in order to save herself and her baby. She must be proactive and use any means necessary in order to escape her attackers. Although it seems like an uphill battle, she does not give up. She uses her strength and ingenuity to subdue the assailants. She uses whatever is at her disposal to create a way to get out of the situation alive.

**Critique**: The response implies that the baby belongs to the narrator, which is inaccurate.

**Rationale**: The critique identifies a specific issue in the answer, which is the incorrect implication that the baby belongs to the narrator. However, it does not provide the correct information or guidance on how to fix this error, such as clarifying who the baby actually belongs to or suggesting a rephrasing to avoid the implication. Therefore, it lacks the actionable feedback needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is this an unusual case?

**Answer**: The timing of the incidents suggests premeditation. Arson attacks in the aftermath of domestic terror attacks are usually carried out when there's backlash against minority communities. The attack occurred in the early morning, which is unusual.

**Critique**: The answer omits that one of the biggest surprises about the attack was that Gurdwara Sahib had a good relationship with the local community.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely the surprising aspect of the attack given the good relationship between Gurdwara Sahib and the local community. This provides actionable feedback by specifying what additional detail should be included to improve the answer.

**Classification**: Constructive

---

### Sample 35/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what the narrator has to say about opportunities. 

**Answer**: The narrator has a metaphor where cards represents opportunities in life.

**Critique**: This neglects the rest of what the narrator says about opportunities.

**Rationale**: The critique identifies that the answer is incomplete by stating that it "neglects the rest of what the narrator says about opportunities." However, it does not specify what additional information is missing or provide guidance on how to improve the answer. It lacks actionable feedback that would help the answerer understand what specific content should be added to make the answer more complete.

**Classification**: Non-Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What happens between Lucy and the Stag?

**Answer**: Lucy removed some the stags fur with a piece of his horn while he is asleep. She wraps it over herself. This condemns her to become a doe for a year until she must die. After a year he finds her again, and he lies with her one last time.

**Critique**: "the" - add "of" (of the)

**Rationale**: The critique identifies a specific grammatical error in the answer by pointing out the missing word "of" in the phrase "some the stags fur." This provides clear, actionable feedback that can be directly applied to improve the answer by correcting the grammatical mistake.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the story say about the narrator?

**Answer**: The narrator is a sergeant in the army. He has a caring family and a spouse. He has medals to his name and a desire to live. He is a leader of men. He is a survivor of the war.

**Critique**: It is omitted he was rescued by the British.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely that the narrator was rescued by the British. This provides clear guidance on what needs to be added to improve the answer, making it actionable and specific.

**Classification**: Constructive

---

### Sample 38/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Explain how the card turned from blank to displaying the numbers "76".

**Answer**: It probably wasn't him described in the story, but the events taking place could have been the back-story for who Pete met in the end.

**Critique**: This answer doesn't make sense. Additionally, it should say the answer can't be found.

**Rationale**: The critique identifies that the answer does not make sense, which is a vague statement without specific guidance on how to improve it. However, it does provide a suggestion that the answer should state that the answer cannot be found, which is a specific and actionable piece of feedback. This makes the critique constructive because it offers a clear direction for improving the answer by suggesting what it should say instead.

**Classification**: Constructive

---

### Sample 39/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is it hard for critics to accept that Mikhail Lesin killed himself?

**Answer**: He was the founder of Russia Today, so people wonder if a politics death was being covered up.

**Critique**: "politics" - replace with "political"

**Rationale**: The critique identifies a specific issue in the answer, which is the incorrect use of the word "politics." It provides a clear and actionable suggestion to replace "politics" with "political," thereby correcting the grammatical error. This guidance is specific and directly helps improve the quality of the answer.

**Classification**: Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the weather and the number of deaths in Chicago?

**Answer**: In Chicago, a historic and deadly cold snap gripped a wide swath of the nation on Wednesday, fueled by the polar vortex, with temperatures plunging far below zero and wind chill numbers as extraordinary as they are dangerous. The temperature in Chicago tumbled to 21 below Wednesday morning, a record for the date, and closing in on the city's all-time record of minus-27 set in 1985. That record could fall on Thursday.

**Critique**: The highlighted text is a description of the extreme weather affecting a wide swath of the nation, not just "in Chicago", which makes this part of the response contradictory. It should be revised to reflect the fact that Chicago is affected. 

**Rationale**: The critique identifies a specific issue with the answer, pointing out that the description of the weather is not limited to Chicago, which contradicts the question's focus on Chicago. It suggests revising the response to accurately reflect that Chicago is affected, providing clear guidance on how to address the problem. This makes the critique actionable and specific.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the article say about the motivation behind the exercise ban?

**Answer**: No answer

**Critique**: A response  is possible and necessary

**Rationale**: The critique "A response is possible and necessary" is non-constructive because it only states that an answer is needed without providing any guidance or specifics on what the answer should include. It does not identify any specific issues with the current lack of an answer or suggest what information should be provided to address the question.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Why does Devyn think that the girls are weird?

**Answer**: Because they don't text a guy who gave Sana his number in the ice cream shop. The girls do not believe in the soulmate idea.

**Critique**: The response should be written as a full sentence. 

**Rationale**: The critique points out that the response should be written as a full sentence, but it does not provide specific guidance on how to rewrite the answer into a full sentence. It identifies a problem but lacks actionable feedback or a suggestion for improvement.

**Classification**: Non-Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to non-American countries.

**Answer**: France's air accident investigation agency BEA will analyze black-box cockpit voice and data recorders from the crashed plane. France's announcement resolved uncertainty over the fate of the two recorders after Germany's BFU said it had declined a request to handle them because it could not process the new type of recorder used on the 737 MAX jets. Brazil, Mexico, and Panama are the first Latin American nations to suspend the Boeing 737 MAX. Panama's Copa Airlines had suspended operations of its six Boeing 737 MAX 9 aircraft until the findings are published of an investigation into the Sunday's crash.

**Critique**: The question's wording, "non-American countries", should be interpreted as "countries that aren't on a continent named America". Thus, Latin American countries shouldn't be mentioned.

**Rationale**: The critique identifies a specific issue with the interpretation of the term "non-American countries" and provides guidance on how to address it by suggesting that Latin American countries should not be included in the summary. This feedback is actionable and specific, as it clarifies the scope of the question and indicates which parts of the answer are incorrect.

**Classification**: Constructive

---

### Sample 44/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Discuss LaFleur's play calls.

**Answer**: LaFleur made several questionable decisions. He had 4th & 2 from the Eagles 13-yard line, with his team leading 10-7. The Packers had been moving up and down the field. LaFleur took a page straight from the Sean McVay playbook and kicked the FG. That gave the Packers a whopping 13-7 lead. Where is the aggression? Why wouldn’t you trust Aaron Rodgers to make a play there? If you fail, you’re still up 10-7. LaFleur made some questionable play-calls.

**Critique**: A lot of the response is lifted from the passage.

**Rationale**: The critique "A lot of the response is lifted from the passage" identifies a potential issue of originality or reliance on the source material, but it does not provide specific guidance on how to address or fix this issue. It lacks actionable feedback, such as suggesting how to rephrase or add original analysis to the answer. Therefore, it does not meet the criteria for a constructive critique.

**Classification**: Non-Constructive

---

### Sample 45/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize how depression has impacted the narrator's life. 

**Answer**: The narrator has been struggling with depression since the age of 16. They have had suicidal thoughts and have attempted to commit suicide. They have also been diagnosed with psychosis.

**Critique**: He struggles with recovery going through cycles of depression and psychosis. 

**Rationale**: The critique identifies a specific issue by pointing out that the answer omits the narrator's struggle with recovery and the cyclical nature of their depression and psychosis. However, it does not provide guidance on how to incorporate this information into the answer or suggest how to improve the existing content. It merely adds additional information without integrating it into the context of the answer.

**Classification**: Non-Constructive

---

### Sample 46/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the opinions of the students of Marjory Stoneman Douglas High School?

**Answer**: The students at Marjory Stoneman Douglas High School, where the Parkland shooting occurred, do not agree with the movie and video game industry, placing the blame on the inaction of inactive politicians and the National Rifle Association, demanding gun-control reform.

**Critique**: The first sentence of the answer should be rewritten because it says the students disagree with the movie and video game industry; meanwhile, the text does not indicate such. The model's answer changes the meaning from the text and is inaccurate and should consider correcting this.

**Rationale**: The critique identifies a specific issue with the answer, namely that it inaccurately states the students disagree with the movie and video game industry, which is not supported by the text. It provides guidance on what needs to be corrected by indicating that the meaning has been changed and is inaccurate, suggesting that the answer should be revised to align with the text. This feedback is actionable and specific, as it points out the exact part of the answer that is incorrect and needs revision.

**Classification**: Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the main news event.

**Answer**: SpaceX is preparing to launch its new rocket, the Falcon Heavy - a rocket which is more powerful than Saturn V. The rocket consists of three Falcon 9 cores and is designed to return to Earth much like the company's solo Falcon 9 flights. It will launch Elon Musk's Tesla Roadster into a helocentric orbit. The KSCVC are predicting this will lead to a new kind of history being made.

**Critique**: It is not stated that the rocket is more powerful than Saturn V, but that it is the most powerful rocket since NASA's Saturn V moon rocket.

**Rationale**: The critique identifies a specific error in the answer by pointing out that the Falcon Heavy is not more powerful than the Saturn V, but rather the most powerful rocket since the Saturn V. This correction provides the necessary information to fix the inaccuracy in the original answer, making it actionable and specific.

**Classification**: Constructive

---

### Sample 48/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the issues that are making the narrator depressed.

**Answer**: The narrator's grandmother passed away, and the narrator lost his mother at a young age. He lost his contact with his mother's family. He also lost a dear loved one on January 1st, 2018. The loss of his grandmother and mother caused him to go into depression. He also moved 200 miles away from his hometown of Snoqualmie, Washington, and he lost all his friends and family.

**Critique**: Remove the third sentence, it only confuses the timeline.

**Rationale**: The critique identifies a specific issue with the answer, namely that the third sentence confuses the timeline. It provides actionable feedback by suggesting the removal of this sentence to improve clarity. This guidance is specific and directly addresses how to fix the problem, making it a constructive critique.

**Classification**: Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to Ardalent.

**Answer**: Mrs. Cardicole has claimed Lester and Sable. She had also murdered their child. She takes the child back to her apartment and later kills him because she needed to feed her own son.

**Critique**: The response should make it clear that her 'son' is Ardalent.

**Rationale**: The critique identifies a specific piece of missing information in the answer, which is the need to clarify that Mrs. Cardicole's 'son' is Ardalent. This provides actionable feedback by specifying exactly what detail should be added to improve the answer's clarity and completeness.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the skills needed to become a Russian pop star?

**Answer**: There are no clear indications of the required skills to be a good Russian pop star. However, talent in theater, cinema, TV and music seem to be shown in Napoli's case.

**Critique**: There's no specific answer, so it would be better to leave it at that.

**Rationale**: The critique points out that the answer lacks specificity but does not provide any guidance or suggestions on how to improve it. It merely states that there is no specific answer without indicating what could be added or changed to make the answer more precise or informative. This makes the critique non-constructive, as it fails to offer actionable feedback.

**Classification**: Non-Constructive

---

