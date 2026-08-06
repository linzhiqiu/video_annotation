# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique
- **Total Samples**: 50
- **Random Seed**: 42
- **Timestamp**: 20251015_0159

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

A CONSTRUCTIVE critique provides actionable, specific feedback that helps improve the answer. It must identify a problem AND give enough information to fix it. This includes:

1. **Providing missing information**: "Some people are worried due to the virus" or "He was caught, though" (gives the actual content that should be added)
2. **Correcting errors with the right answer**: "It should be white, not black" or "The horse is brown, not white"
3. **Specifying omitted details**: "It's omitted that the child was being crushed under a roof"
4. **Giving concrete improvement suggestions**: "Combine sentences that convey the same idea" or "Use X instead of Y"

A NON-CONSTRUCTIVE critique only describes a problem without providing the information or guidance needed to fix it:
- "This doesn't answer the question" (doesn't say what the answer should be)
- "More details needed" (doesn't specify what details)
- "This is wrong" or "This is incomplete" (too vague)
- "The story never discusses X" (doesn't tell you what X is or should be)

Key distinction: 
- ✅ CONSTRUCTIVE: "The answer is wrong. It should be Y" or "Missing information: Z"
- ❌ NON-CONSTRUCTIVE: "The answer is wrong" or "Information is missing" (no indication of what)

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
| Constructive | 23 | 46.00% |
| Non-Constructive | 27 | 54.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |

## Sample Examples

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: How did the extraordinary James Butler become ordinary?

**Answer**: He lost his zest when his wife and daughter died. 

**Critique**: There is no evidence that it was a daughter, and not a son, that passed away in the accident.

**Rationale**: The critique identifies a potential error in the answer by questioning the accuracy of the information regarding the family member who passed away. However, it does not provide the correct information or guidance on how to verify or correct the statement. It merely points out a possible issue without offering a solution or specific correction.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Answer the following question based on the above passage:

What does the text say about the school Jeffery goes to?

**Answer**: No answer

**Critique**: No response is provided for this question; a response needs to be created. 

**Rationale**: The critique identifies that there is no response provided to the question, which is a valid observation. However, it does not offer any specific guidance or information on what the answer should include regarding the school Jeffery goes to. It lacks actionable feedback or details that would help in constructing an appropriate answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: When was Olivewood established?

**Answer**: Olivewood was established in 2018.

**Critique**: The answer does not provide the full context (the area has been producing films since the 1950s).

**Rationale**: The critique identifies a problem with the answer, which is the lack of context regarding the area's history in film production. However, it does not provide specific guidance on how to incorporate this information into the answer or explain why this context is necessary for answering the question about when Olivewood was established. The critique fails to offer actionable steps or specific content to improve the answer.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Answer the following question based on the above passage:

What does the text say about Pierce?

**Answer**: Pierce is a childhood friend of Josh. He is a menacing presence, but Josh vouches for him, saying he's not that bad. Josh and Sana also seem to be interested in him.

**Critique**: Doesn't fully answer the question

**Rationale**: The critique "Doesn't fully answer the question" is non-constructive because it identifies a problem without providing specific guidance or information on how to improve the answer. It does not specify what details are missing or what additional information should be included to fully answer the question about Pierce.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Answer the following question based on the above passage:

Summarize the events of the accident.

**Answer**: The specific statment of the form 'the accident' needs to be fleshed out for the answer. The accident happens on an unnamed interstate. Both the man and the woman were in the car, but then it was the end of the story. The couple had a wedding but it ended early after a car accident.

**Critique**: The story never discusses any details regarding the accident.

**Rationale**: The critique provided is non-constructive because it only points out that the story lacks details about the accident without specifying what those details should be. It does not offer any guidance or specific information that could help improve the answer by filling in the missing details about the accident.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Answer the following question based on the above passage:

What is remarkable about the pay packages of In-N-out burgers?

**Answer**: The pay package is far more than the industry average and is triple the industry average.

**Critique**: The response leaves out the fact that these statistics are for store managers.

**Rationale**: The critique identifies a specific piece of missing information in the answer, which is that the pay statistics mentioned apply specifically to store managers. By pointing out this omission, the critique provides actionable feedback that can be used to improve the answer by adding the relevant detail. This aligns with the criteria for a constructive critique, as it specifies what information is missing and how to address the issue.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique identifies a specific piece of missing information from the answer, which is the number of people who died in the massacre. By specifying that six people died, it provides concrete information that can be added to improve the completeness and accuracy of the answer. This aligns with the criteria for a constructive critique, as it offers actionable feedback that directly addresses a gap in the provided answer.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Answer the following question based on the above passage:

Summarize everything relating to the narrator's plans for the future.

**Answer**: The narrator wants to gather and pack the things they need and leave this place behind. They think they'll walk east to escape their current life. They are planning to change their look and make a new life. They want to leave this place and hopefully find more joy on the road. The narrator wants to leave this place for its memories of their partner that may make them feel sad. The narrator is planning on taking the books and their emotions with them no matter what. The narrator wishes they could just change the way they are or start anew.

**Critique**: "They" and "The narrator" are being used too often and make the response sound clunky. Certain sentences that convey the same idea can be combined instead. 

**Rationale**: The critique identifies a stylistic issue with the overuse of "they" and "the narrator," which makes the response sound repetitive and awkward. It provides a concrete suggestion for improvement by recommending that sentences conveying the same idea be combined to enhance the flow and readability of the answer. This feedback is actionable and specific, addressing the problem and offering a way to fix it.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Which all countries were mentioned in the presentation for having restrictions on press freedom?

**Answer**: The mentioned countries were: Turkey, Mexico, and Egypt.

**Critique**: The answer doesn't mention Russia and Pakistan.

**Rationale**: The critique identifies a specific problem with the answer by pointing out that it omits two countries, Russia and Pakistan, which were mentioned in the presentation. This provides actionable feedback by specifying exactly what information is missing, allowing the answer to be corrected by including these countries.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

What is the subject of this story?

**Answer**: The narrator is a slave who famously escaped his masters.

**Critique**: He was caught, though.

**Rationale**: The critique provides specific information that is missing from the answer. It identifies a problem (the omission of a key detail about the narrator being caught) and provides the exact information needed to correct the answer. This aligns with the criteria for a constructive critique, as it offers actionable feedback that can improve the answer.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Non-Constructive]

**Question**: Will the brute ever become a man again?

**Answer**: No. Some may call him Dash the man now. However, it is not clear who calls him Dash the man. Can Dash ever become a man again?

**Critique**: Odd ending.

**Rationale**: The critique "Odd ending" is non-constructive because it merely points out a perceived issue with the answer without providing any specific guidance or suggestions for improvement. It does not identify what makes the ending odd or how it could be improved to better address the question.

**Classification**: Non-Constructive

---

### Sample 2/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Qonqurtai's early life? 

**Answer**: Qonqurtai was born to Hulagu Khan and Ajuja Aguchi, his Khitan concubine wife. He was Hulagu's ninth son and was the senior commander during the reign of his brother Abaqa.

**Critique**: Qonqurtai's time as a commander isn't his childhood.

**Rationale**: The critique identifies a problem with the answer by pointing out that the information about Qonqurtai's time as a commander is not relevant to his early life. However, it does not provide any specific information or guidance on what should be included to accurately address the question about Qonqurtai's early life. It lacks actionable feedback or suggestions for improvement.

**Classification**: Non-Constructive

---

### Sample 3/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the school Jeffery goes to?

**Answer**: No answer

**Critique**: No response is provided for this question; a response needs to be created. 

**Rationale**: The critique identifies that there is no response provided to the question, which is a valid observation. However, it does not offer any specific guidance or information on what the answer should include regarding the school Jeffery goes to. It lacks actionable feedback or details that would help in constructing an appropriate answer.

**Classification**: Non-Constructive

---

### Sample 4/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry was a loner and outcast. Kids always made fun of him for never being interested in any girls when most others had hit puberty. By all accounts, it appears Jerry was bullied by the other kids. Jerry was even shot in the leg one time when the kids were using real guns to shoot blanks at him, and one of the guns had a live bullet. 

**Critique**: Since the answer isn't specifically stated in the story it would be better to use  more speculative language.

**Rationale**: The critique identifies a problem with the answer, which is the lack of speculative language when discussing Jerry's motivations. However, it does not provide specific guidance on how to incorporate speculative language or what specific changes should be made to the answer to improve it. The critique lacks actionable advice or concrete suggestions for improvement, making it non-constructive.

**Classification**: Non-Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Peach & Lily?

**Answer**: The text says that Peach & Lily is a Korean beauty retailer that is launching its very own skin-care collection. The first product of the collection, Glass Skin Refining Serum, is already sold out but there is an option to be notified when orders will be accepted again. Alicia Yoon shares her research process on peachandlily.com.

**Critique**: The answer should mention that Yoon is the founder of the company.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, namely that Alicia Yoon is the founder of Peach & Lily. This provides clear guidance on what needs to be added to improve the answer, making it actionable and specific. By specifying the omitted detail, the critique helps enhance the completeness and accuracy of the answer.

**Classification**: Constructive

---

### Sample 6/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does Super Dan do that he should not have done?

**Answer**: Super Dan removed the roadside shrines when he was instructed not to.

**Critique**: Super Dan wasn't instructed not to remove the shrines, the shrines were not mentioned initially.

**Rationale**: The critique identifies an error in the answer by pointing out that Super Dan was not instructed not to remove the shrines, and it also highlights that the shrines were not mentioned initially. However, it does not provide the correct information or guidance on what Super Dan actually did wrong, nor does it suggest how to correct the answer. Therefore, it lacks the actionable, specific feedback needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 7/50 - [Non-Constructive]

**Question**: Why does the narrator tell the subject they look hideous?

**Answer**: The narrator is being sarcastic.

**Critique**: There is nothing to indicate sarcasm from the narrator.

**Rationale**: The critique identifies a problem with the answer by pointing out that there is no indication of sarcasm from the narrator. However, it does not provide any specific information or guidance on how to address this issue or what the correct interpretation should be. It lacks actionable feedback that would help improve the answer.

**Classification**: Non-Constructive

---

### Sample 8/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique identifies a specific piece of missing information from the answer, which is the number of people who died in the massacre. By specifying that six people died, it provides concrete information that can be added to improve the completeness and accuracy of the answer. This aligns with the criteria for a constructive critique, as it offers actionable feedback that directly addresses a gap in the provided answer.

**Classification**: Constructive

---

### Sample 9/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why does the narrator suggest that they must terminate the patient's pregnancy?

**Answer**: That information is not covered in the text.

**Critique**: This is false. It is directly stated that, "...sorry, it's a boy. As you know our current sector has too many male children. When would you like to schedule the termination."

**Rationale**: The critique identifies a specific error in the answer by pointing out that the information is indeed present in the text. It provides the exact quote from the text that supports the correct answer, thereby offering the necessary information to correct the initial response. This makes the critique actionable and specific, as it directly addresses the problem and provides the correct information.

**Classification**: Constructive

---

### Sample 10/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is the subject of this story?

**Answer**: The narrator is a slave who famously escaped his masters.

**Critique**: He was caught, though.

**Rationale**: The critique provides specific information that is missing from the answer. It identifies a problem (the omission of a key detail about the narrator being caught) and provides the exact information needed to correct the answer. This aligns with the criteria for a constructive critique, as it offers actionable feedback that can improve the answer.

**Classification**: Constructive

---

### Sample 11/50 - [Non-Constructive]

**Question**: Write a ~7 sentence summary.

**Answer**: Beatriz Morelos, a mother of four, was scheduled to be deported on Tuesday to Nuevo Laredo, Mexico, which is in an area that the U.S. Department of State warns travelers to avoid “due to violent crime, including homicide, armed robbery, carjacking, extortion and sexual assault,” according to its website. Morelos’ husband, Jose DeJesus, said he feels his family’s worst nightmare has come true. Morelos, 33, was awaiting deportation at an ICE detention center in Tiffin, Ohio, as of Monday evening, but her attorney, Elizabeth Ford, said she is working to get the U.S. to rethink its decision. Ford said she is trying to get ICE to grant Morelos a stay, which she admits is difficult because of the way the country’s new immigration laws are written. “It is absolutely impossible for people in her situation and in many other people’s situations to correct their status with how the laws are written now,” Ford told WEWS on Monday. “If she was able to correct her status, she absolutely would have, just like many of the other people would.” Ford said that Morelos does not have a criminal history and that she would be separated from her four young children, who are U.S. citizens, and her husband, who’s in the U.S. on a visa. “I can’t imagine putting a mother, who’s in her mid-30s with four U.S. citizen children, there alone,” Ford told WEWS. “She has no family in Mexico. Her entire family is in the United States. It’s absolutely horrific to think that this is where this young woman is going.”

**Critique**: The summary feels more like a re-written report and could use some editing to reflect that it is a summary.

**Rationale**: The critique identifies a problem with the answer, suggesting that it reads more like a report than a summary. However, it fails to provide specific guidance or actionable steps on how to transform the report-like content into a more concise summary. It does not specify which parts should be condensed or how the structure could be improved to better fit the format of a summary. Therefore, it lacks the necessary information to be considered constructive.

**Classification**: Non-Constructive

---

### Sample 12/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What factors drove Jerry to become a serial killer?

**Answer**: Jerry grew up a loner and had a strong hatred of guns. Unbeknownst to others around them, the victim usually revealed he had a problem that could be fixed, which led to their death. Jerry does not torture his victims, but makes their deaths quick and painless. Jerry tearfully kills his victims after bonding with them first. These factors drove Jerry to become a serial killer.

**Critique**: None of these factors led to Jerry being a serial killer. This should be omitted. Additionally, the answer should be in speculative terms as it's not stated explicitly in the text.

**Rationale**: The critique identifies that the factors mentioned in the answer are incorrect and suggests that they should be omitted. It also provides guidance on how the answer should be framed, specifically recommending that the answer should be in speculative terms since the text does not explicitly state the reasons. This provides actionable feedback to improve the answer by both removing incorrect information and adjusting the tone to reflect the speculative nature of the content.

**Classification**: Constructive

---

### Sample 13/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Whistler's activities during the 1970s.

**Answer**: He worked as a teacher at Samoa College, then served as a Peace Corps volunteer.

**Critique**: Whistler workes as a teacher at Samoa College while he was in the Peace Corps.

**Rationale**: The critique identifies a specific error in the answer by clarifying that Whistler worked as a teacher at Samoa College while he was in the Peace Corps, rather than these being separate activities. This correction provides the necessary information to improve the accuracy of the answer.

**Classification**: Constructive

---

### Sample 14/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Whose statues are they?

**Answer**: The statues are of people — some of whom the old man knows from his old letters.

**Critique**: The answer does not specify what is significant about the people that were given statues.

**Rationale**: The critique identifies a problem with the answer, specifically that it lacks information about the significance of the people who have statues. However, it does not provide any specific information or guidance on what should be included to address this issue. It merely points out the omission without suggesting what details are missing or how to improve the answer.

**Classification**: Non-Constructive

---

### Sample 15/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How long will the stadium be open?

**Answer**: The stadium will be open for at least as long as the weather permits.

**Critique**: It will be open "until at least 9am on Monday morning" and possibly longer depending on the weather

**Rationale**: The critique provides specific information that was missing from the original answer. It corrects the vague statement about the stadium's opening duration by specifying the exact time it will be open until, which is "until at least 9am on Monday morning," and then adds that it may be longer depending on the weather. This gives clear, actionable feedback to improve the answer.

**Classification**: Constructive

---

### Sample 16/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the main news event.

**Answer**: Officials down in the state are reporting Governor Cuomo has received $5.9 million in the past six months. That money was during the filing period. He's running for the governor's seat. Speaking of the Republicans, they've otherwise been losing completely by a wide margin.

**Critique**: The story is actually about the libertarian candidate.

**Rationale**: The critique identifies a problem with the answer by indicating that the main news event is incorrectly summarized. However, it does not provide the necessary information or guidance to correct the answer, such as what specific details about the libertarian candidate should be included. Therefore, it lacks the actionable feedback needed to improve the answer.

**Classification**: Non-Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Pierce?

**Answer**: Pierce is a childhood friend of Josh. He is a menacing presence, but Josh vouches for him, saying he's not that bad. Josh and Sana also seem to be interested in him.

**Critique**: Doesn't fully answer the question

**Rationale**: The critique "Doesn't fully answer the question" is non-constructive because it identifies a problem without providing specific guidance or information on how to improve the answer. It does not specify what details are missing or what additional information should be included to fully answer the question about Pierce.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Non-Constructive]

**Question**: Write a ~10 sentence summary.

**Answer**: Two boys in blue removed the narrator and their friend from their car and placed them in their backseat. They proceeded to drive the car all around for a while until they stopped and parked in who knows where. There, the narrators were told to hand over their cellphones. They were confused why the boys in blue detained them and worried they were about to go to jail. In their fear, they were scared that the boys had guns. One of the boys in blue, the one with the scarred face, behaved numb in their direction. He was big and strong. His face had a scar. He had a scandalous personality. The other one, the one who was wearing sunglasses, seemed more normal, like a typical guy. This one smarted off and was more intimidating.

**Critique**: There is no evidence that one of the cops had a scar on his face or that the wore sunglasses.

**Rationale**: The critique identifies a specific issue with the answer by pointing out that there is no evidence supporting the details about the cops having a scar or wearing sunglasses. However, it does not provide any guidance on how to correct the answer or what the correct details should be. It merely states that the information is not supported by evidence, which does not help in improving the answer.

**Classification**: Non-Constructive

---

### Sample 19/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is Alan worried at the end of the piece?

**Answer**: Alan is worried because, although the attendant is back, he heard footsteps that sounded like there was at least one other person following her. He also heard a heavy cough, indicating that whoever was approaching was possibly ill. This creates anxiety for Alan, as he doesn't know who is following the attendant and what their motives might be.

**Critique**: "Alan is worried because, although the attendant is back, he heard footsteps that sounded like there was at least one other person following her." - the attendant didn't go back and no one was following her. The footsteps he was hearing came from the trucker. Alan was worried because the trucker came back and the attendant didn't. 

**Rationale**: The critique identifies a specific error in the answer regarding the source of Alan's worry. It corrects the mistake by providing the accurate information that the footsteps were from the trucker, not someone following the attendant, and clarifies that the attendant did not return. This correction directly addresses the problem and provides the necessary information to improve the answer.

**Classification**: Constructive

---

### Sample 20/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is remarkable about the pay packages of In-N-out burgers?

**Answer**: The pay package is far more than the industry average and is triple the industry average.

**Critique**: The response leaves out the fact that these statistics are for store managers.

**Rationale**: The critique identifies a specific piece of missing information in the answer, which is that the pay statistics mentioned apply specifically to store managers. By pointing out this omission, the critique provides actionable feedback that can be used to improve the answer by adding the relevant detail. This aligns with the criteria for a constructive critique, as it specifies what information is missing and how to address the issue.

**Classification**: Constructive

---

### Sample 21/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarise the theme of death in paragraphs 7 and 8?

**Answer**: In paragraph 7, the old man arrives at the statue of a young woman. The plaque reads that she died protecting her home, but the old man is devastated because she is his only child. He remembers how it all started and how devastated he was when she died. In paragraph 8, he cries uncontrollably. He waits to die at her feet.

**Critique**: This does not happen in paragraph 8. It should be omitted

**Rationale**: The critique identifies a specific error in the answer by stating that the described event does not occur in paragraph 8. It provides actionable feedback by suggesting that the incorrect information should be omitted, which directly addresses the problem and offers a clear solution. This aligns with the criteria for a constructive critique as it specifies what needs to be corrected and how.

**Classification**: Constructive

---

### Sample 22/50 - [Constructive]

**Question**: Why are some people worried?

**Answer**: The virus is spread through respiratory contact.

**Critique**: This doesn't answer the question. Some people are worried due to the virus. 

**Rationale**: The critique initially points out that the answer does not address the question, which is a non-constructive element because it doesn't specify what the answer should be. However, it then provides the missing information by stating, "Some people are worried due to the virus," which directly addresses the question and offers a specific improvement to the answer. This makes the critique actionable and specific.

**Classification**: Constructive

---

### Sample 23/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about some of the issues SČH faced during its time?

**Answer**: The members began operating more or less on their own because they were initially untied to any trade union centre. The union bound themselves closer to the Czechoslovak Socialist Party as it faced police repression. As many miners were arrested and the union was increasingly dependent on the Czechoslovak Socialist Party.

**Critique**: It is omitted that its members struggled with economic hardship.

**Rationale**: The critique identifies a specific piece of missing information, which is that the members of SČH struggled with economic hardship. However, it does not provide the actual content or details that should be added to the answer to address this omission. It merely points out the absence of this information without offering a way to incorporate it into the answer.

**Classification**: Non-Constructive

---

### Sample 24/50 - [Non-Constructive]

**Question**: How did the extraordinary James Butler become ordinary?

**Answer**: He lost his zest when his wife and daughter died. 

**Critique**: There is no evidence that it was a daughter, and not a son, that passed away in the accident.

**Rationale**: The critique identifies a potential error in the answer by questioning the accuracy of the information regarding the family member who passed away. However, it does not provide the correct information or guidance on how to verify or correct the statement. It merely points out a possible issue without offering a solution or specific correction.

**Classification**: Non-Constructive

---

### Sample 25/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the climactic event of the story.

**Answer**: The narrator and Victor go sledding. They make a jump out of snow and go flying off of it. They soar over the snow for about ten feet.

**Critique**: This isn't the climax of the story. There is no real clear climax, but it could be seen as when the passenger asks the narrator why he thinks that is the best day he's ever had. 

**Rationale**: The critique identifies a problem with the answer by stating that it does not describe the climax of the story. However, it does not provide a clear or specific correction or suggestion for improvement. The critique mentions an alternative event that could be considered the climax but does not offer a definitive correction or guidance on how to revise the answer to accurately reflect the story's climax. Therefore, it lacks the actionable feedback needed to be constructive.

**Classification**: Non-Constructive

---

### Sample 26/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the narrator?

**Answer**: The narrator is a man who is in love with a woman. He has always wanted to have a family and a house with a white picket fence. He is a bit unorthodox, but he has always wanted to have a loving household. He has been with the woman for a while, and he feels like he has been spoiled by her. He has a million glances of her beautiful eyes staring into his soul.

**Critique**: It's omitted the narrator says he found himself to be the person you never tell your friends about let alone introduce to your parents.

**Rationale**: The critique identifies a specific detail that is missing from the answer, which is that the narrator considers himself to be the type of person you wouldn't introduce to your friends or parents. This provides actionable feedback by specifying exactly what information should be added to improve the answer. The critique is constructive because it not only points out the omission but also provides the exact content that should be included.

**Classification**: Constructive

---

### Sample 27/50 - [Constructive]

**Question**: What is your purpose, according to this text?

**Answer**: You are everywhere and in everything.

**Critique**: "You are everywhere and in everything." - change 2nd person writing (you) to 3rd person. A complete rewrite is needed for this to make sense.

**Rationale**: The critique identifies a specific issue with the answer, which is the use of second-person writing, and provides a clear suggestion for improvement by recommending a change to third-person writing. This guidance is actionable and specific, as it directs the rephrasing of the answer to make it more coherent and appropriate for the context.

**Classification**: Constructive

---

### Sample 28/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize why Democrats think their policies on voting procedures are right, according to the author.

**Answer**: The author presents evidence on double voting and voter fraud stats (8,471 cases of double voting in 21 states). The Democrats state that there is no need for an investigation of the extent of voter fraud because there is no evidence and such investigations are discriminating Americans who are trying to vote. They also state that there is a danger of disenfranchisement if DHS and other government come to check fraudulent voting. The author feels that such fears of investigations are unfounded and selective.

**Critique**: The Democrats don't claim that there's no evidence of voting fraud. They claim the final results aren't affected, that the scale of the problem is small.

**Rationale**: The critique identifies a specific error in the answer regarding the Democrats' stance on voting fraud. It corrects the misrepresentation by clarifying that Democrats argue the scale of the problem is small and does not affect final results, rather than claiming there is no evidence of voting fraud. This correction provides the necessary information to improve the accuracy of the answer.

**Classification**: Constructive

---

### Sample 29/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize everything relating to the narrator's plans for the future.

**Answer**: The narrator wants to gather and pack the things they need and leave this place behind. They think they'll walk east to escape their current life. They are planning to change their look and make a new life. They want to leave this place and hopefully find more joy on the road. The narrator wants to leave this place for its memories of their partner that may make them feel sad. The narrator is planning on taking the books and their emotions with them no matter what. The narrator wishes they could just change the way they are or start anew.

**Critique**: "They" and "The narrator" are being used too often and make the response sound clunky. Certain sentences that convey the same idea can be combined instead. 

**Rationale**: The critique identifies a stylistic issue with the overuse of "they" and "the narrator," which makes the response sound repetitive and awkward. It provides a concrete suggestion for improvement by recommending that sentences conveying the same idea be combined to enhance the flow and readability of the answer. This feedback is actionable and specific, addressing the problem and offering a way to fix it.

**Classification**: Constructive

---

### Sample 30/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Whistler's activities during the 1970s.

**Answer**: He moved to Hawaii and completed a doctorate in botany from the University of Hawaii at Manoa, focusing on Samoan plant life, in 1979. He lived in Samoa during the 1970s before the logging and tourism led to the deforestation of the country's rainforests.

**Critique**: The answer should mention Whistler's time in the Peace Corps.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, which is Whistler's involvement with the Peace Corps. By specifying this omission, the critique provides actionable feedback that can be used to improve the answer by including this detail. This aligns with the criteria for a constructive critique, as it points out a specific problem and provides the information needed to address it.

**Classification**: Constructive

---

### Sample 31/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Ajax's left-back Nicolas Tagliafico has been a major part of Ajax's remarkable journey to the quarter-finals, but they will go to Turin with the same belief.

**Critique**: Fails to mention other key details such as the big win against Real Madrid and Tagliafico's praise for the upcoming rival, Juventus.

**Rationale**: The critique identifies that the summary is missing specific details, such as the significant victory against Real Madrid and Tagliafico's comments about Juventus. However, it does not provide the actual content or guidance on how to incorporate these details into the summary, which is necessary for it to be considered constructive.

**Classification**: Non-Constructive

---

### Sample 32/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What statistic is missing in this article and why is it important?

**Answer**: The article does not mention the average salary of each country.

**Critique**: The response says the article doesn't mention the average salary of each country, however one can imply the salaries by realizing that the cost of a ticket is X% of X country salary.

**Rationale**: The critique points out that the answer identifies a missing statistic (average salary of each country) but suggests that the information can be inferred from the cost of a ticket as a percentage of the country's salary. However, it does not provide a direct solution or specify how to address the missing information in the article. It lacks actionable guidance on how to improve the answer or the article itself.

**Classification**: Non-Constructive

---

### Sample 33/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the story have to say about Theodore?

**Answer**: The story portrays Theodore as a loyal, intelligent creature with a keen understanding of human emotions and the ability to navigate a complicated world. He was a source of great joy for both Raymond and the narrator. The dog's death through accident is a huge loss for both brothers. Theodore is remembered fondly for his joyful spirit and intelligence.

**Critique**: The last sentence is somewhat repetitive and not wholly relevant.

**Rationale**: The critique identifies a problem with the answer, noting that the last sentence is repetitive and not entirely relevant. However, it does not provide specific guidance on how to address this issue, such as suggesting how to rephrase or what to include instead. Therefore, it lacks the actionable feedback necessary to be considered constructive.

**Classification**: Non-Constructive

---

### Sample 34/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why is it hard for critics to accept that Mikhail Lesin killed himself?

**Answer**: The FBI claims Lesin was so drunk that he repeatedly and violently fell on things until he killed himself. He had blunt force trauma injuries all over his body.

**Critique**: Add that this is an unlikely circumstance (thereby answering the question directly)

**Rationale**: The critique identifies a specific issue with the answer, which is that it does not directly address why critics find it hard to accept the explanation of Mikhail Lesin's death. It provides a concrete suggestion to improve the answer by adding that the circumstances described are unlikely, which directly answers the question. This guidance is actionable and specific, making it a constructive critique.

**Classification**: Constructive

---

### Sample 35/50 - [Non-Constructive]

**Question**: When was Olivewood established?

**Answer**: Olivewood was established in 2018.

**Critique**: The answer does not provide the full context (the area has been producing films since the 1950s).

**Rationale**: The critique identifies a problem with the answer, which is the lack of context regarding the area's history in film production. However, it does not provide specific guidance on how to incorporate this information into the answer or explain why this context is necessary for answering the question about when Olivewood was established. The critique fails to offer actionable steps or specific content to improve the answer.

**Classification**: Non-Constructive

---

### Sample 36/50 - [Constructive]

**Question**: Which all countries were mentioned in the presentation for having restrictions on press freedom?

**Answer**: The mentioned countries were: Turkey, Mexico, and Egypt.

**Critique**: The answer doesn't mention Russia and Pakistan.

**Rationale**: The critique identifies a specific problem with the answer by pointing out that it omits two countries, Russia and Pakistan, which were mentioned in the presentation. This provides actionable feedback by specifying exactly what information is missing, allowing the answer to be corrected by including these countries.

**Classification**: Constructive

---

### Sample 37/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the plot twist. 

**Answer**: The main character wakes up with someone they dislike and spends the time grumbling about their flaws and shortcomings. Eventually, the character walks away from their conversation and discovers that the person they were awake with is lonely.

**Critique**: Doesn't reveal that the protagonist is lonely. 

**Rationale**: The critique identifies a missing element in the answer, specifically that the protagonist is also lonely. However, it does not provide guidance on how to incorporate this information into the summary or suggest how to improve the answer. It merely points out the omission without offering a solution or specific content to add.

**Classification**: Non-Constructive

---

### Sample 38/50 - [Non-Constructive]

**Question**: Summarize the sorts of personal attacks conducted on Brett Kavanaugh.

**Answer**: He is being portrayed as a rapist and sexual predator. Students at Harvard and professors at his alma mater Yale Law School have demanded investigations into his relationship with the school.

**Critique**: Whilst everything in the answer is correct. The second sentence covers the consequence of the attack rather than the attack itself 

**Rationale**: The critique identifies a problem with the answer, specifically that the second sentence does not directly address the question about the types of personal attacks on Brett Kavanaugh. However, the critique does not provide any specific guidance or information on how to correct this issue or what the second sentence should include to better address the question. It merely points out the problem without offering a solution or additional details that should be included.

**Classification**: Non-Constructive

---

### Sample 39/50 - [Non-Constructive]

**Question**: What is the purpose of this article?

**Answer**: The purpose of this article is to inform readers about the reality of the government’s intrusion into private individuals’ life. The author believes that this Orwellian practice is highly controversial and inhumane.

**Critique**: The tone of the article seems overall to be neutral, so the line about the author's opinion on the practice seems fabricated.

**Rationale**: The critique identifies a potential issue with the answer by suggesting that the author's opinion may not be accurately represented. However, it does not provide specific guidance on how to correct the answer or what the correct interpretation of the article's tone should be. It lacks actionable feedback or specific information to improve the answer.

**Classification**: Non-Constructive

---

### Sample 40/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the development releases?


**Answer**: The article has sections on Search Upgrade, upcoming mobile release, mobile user profile, content validation, assisted writing and peer review experience, and something called Intelligent Editor 1.0 and Peer Review Guidance 1.0. To go along with these, there's a search upgrade, a mobile version of Lunyr, and a mobile user profile.

**Critique**: This response includes extra information that is not critical to development releases. Much of this response needs to be omitted and re-written. 

**Rationale**: The critique identifies that the answer contains extraneous information that is not directly related to the development releases, but it fails to specify which parts are unnecessary or how the answer should be re-written. It does not provide specific guidance or actionable steps to improve the answer, such as indicating which sections should be omitted or what the focus should be instead. Therefore, it lacks the specificity required to be constructive.

**Classification**: Non-Constructive

---

### Sample 41/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Summarize what motivates the narrator to keep going in this story.

**Answer**: The narrator seems driven by their sense of connection to the Sunspiders, and through that, connection to the world around them. They love the idea of contributing to the next generation and preserving themselves on a much grander scale through the Sunspiders. In their barren world, they have relied on the Sunspiders to be a focal point that connects them. When the Sunspiders begin to arrange themselves in a pattern above the narrator, they create a light show, and this final gift motivates the narrator to continue on their journey. The heat, the risk to their body, and the idea of the end being their funeral pyre keep the narrator going. Their goal is to find something that connects them to the world before, and the Sunspiders help them find an accessible connection.

**Critique**: The response does not mention that the narrator is convinced he is not the last man alive, and seeks civilization elsewhere. He uses this to motivate himself throughout his search.

**Rationale**: The critique identifies a specific piece of missing information in the answer: the narrator's belief that he is not the last man alive and his search for civilization. This provides a clear direction for improving the answer by including this motivational aspect, which is crucial to understanding the narrator's drive. The critique effectively points out what is missing and what should be added to enhance the completeness of the answer.

**Classification**: Constructive

---

### Sample 42/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Greta and the narrator divorce?

**Answer**: According to the narrator, Greta had ambitions to rule the world. It seems the narrator shot Greta for wanting to open a portal, and manipulate the world.

**Critique**: It is omitted that the key to the portal was Jericho.

**Rationale**: The critique identifies a specific piece of information that is missing from the answer, which is the role of Jericho as the key to the portal. By specifying this omitted detail, the critique provides actionable feedback that can help improve the completeness and accuracy of the answer. This aligns with the criteria for a constructive critique, as it gives enough information to address the identified problem.

**Classification**: Constructive

---

### Sample 43/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the main news event.

**Answer**: Brian Kolb, a Republican and a former executive of a trucking company, had fun raising $102,596 during the filing period. This was topped by Gov. Cuomo's staggering $5.9 million in contributions. Democrat Terry Gipson and Republican Joel Giambra are nowhere near to these totals. In fact, both of them have a mere $6,000 fundraising. Sharpe is the only declared Libertarian to date, 2016.

**Critique**: This does not capture the main new story, about Sharpe

**Rationale**: The critique identifies that the answer does not capture the main news story, which is about Sharpe. However, it fails to provide specific guidance or information on how to correct the answer or what details about Sharpe should be included. It merely points out the problem without offering a solution or additional context.

**Classification**: Non-Constructive

---

### Sample 44/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What informs Burning's career?

**Answer**: Burning's art is from a Haudensounee perspective. They are indigenous and queer. Their perspective grapples  with indigenous relationship to land, representation and "the gaze." Burning uses traditional materials. 

**Critique**: Specific detail about Burning's perspective and views towards indigenous relationships are missing.

**Rationale**: The critique identifies a problem by stating that specific details about Burning's perspective and views towards indigenous relationships are missing. However, it does not provide any specific information or guidance on what those details should be or how to incorporate them into the answer. Therefore, it lacks the actionable, specific feedback required to improve the answer.

**Classification**: Non-Constructive

---

### Sample 45/50 - [Non-Constructive]

**Question**: How did Olivewood get its name?

**Answer**: Olivewood got its name from being a portmanteau of "Olive" and "Hollywood" - both of which are associated with high-quality filmmaking. Incentives have been put in place to encourage more international productions to film in Cyprus, which is considered an up-and-coming film location.

**Critique**: It is incorrect to state that both words are associated with high-quality filmmaking (that is only true of Hollywood).

**Rationale**: The critique identifies a specific error in the answer by pointing out that only "Hollywood" is associated with high-quality filmmaking, not "Olive." However, it does not provide the correct information or suggest how to fix the error. It lacks the actionable guidance needed to improve the answer, such as explaining the actual origin of the name "Olivewood" or suggesting a correction to the statement.

**Classification**: Non-Constructive

---

### Sample 46/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What did big business do with the money that they received from the tax custs

**Answer**: Lowered their capex investments.

**Critique**: The response failed to answer the question of what businesses did with the money. It needs to mention that big businesses bought back their own stock and gave salary increases to CEOs and other high-ranking corporate executives. 

**Rationale**: The critique identifies a specific problem with the answer, which is that it does not fully address what businesses did with the money from tax cuts. It provides specific information that should be included to improve the answer, namely that big businesses bought back their own stock and gave salary increases to CEOs and other high-ranking corporate executives. This guidance is actionable and specific, making the critique constructive.

**Classification**: Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Who is the child in the story?

**Answer**: The child in the story is a young boy.

**Critique**: It's omitted that the child was being crushed under a roof and screaming at the man to not leave him. 

**Rationale**: The critique identifies a specific detail that is missing from the answer, which is that the child was being crushed under a roof and screaming at the man to not leave him. This provides actionable feedback by specifying exactly what information should be included to improve the answer.

**Classification**: Constructive

---

### Sample 48/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Explain the new app update.

**Answer**: That information can't be found in the text.

**Critique**: Yes, it can, at the end.

**Rationale**: The critique points out that the information is indeed present in the text, contradicting the answer's claim that it cannot be found. However, it does not specify what the information is or where exactly it can be found, nor does it provide guidance on how to correct the answer. Therefore, it lacks the actionable, specific feedback required to be constructive.

**Classification**: Non-Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who is the deluded one between Michael and Davenport?

**Answer**: It seems Davenport is the one who clings to the past.

**Critique**: It is omitted that Michael also is delusional.

**Rationale**: The critique identifies a missing detail in the answer by pointing out that Michael is also delusional. This provides specific information that can be added to improve the completeness of the answer. By specifying what is omitted, the critique offers actionable feedback that directly addresses the problem.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize the events of the accident.

**Answer**: The specific statment of the form 'the accident' needs to be fleshed out for the answer. The accident happens on an unnamed interstate. Both the man and the woman were in the car, but then it was the end of the story. The couple had a wedding but it ended early after a car accident.

**Critique**: The story never discusses any details regarding the accident.

**Rationale**: The critique provided is non-constructive because it only points out that the story lacks details about the accident without specifying what those details should be. It does not offer any guidance or specific information that could help improve the answer by filling in the missing details about the accident.

**Classification**: Non-Constructive

---

