# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique (qa)
- **Total Dataset Size**: 4456 critique samples
- **Filtered Dataset Size** (qa): 1851 critique samples
- **Sampled for Analysis**: 50 samples
- **Random Seed**: 40
- **Timestamp**: 20251015_0342

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating whether a critique is CONSTRUCTIVE or NON-CONSTRUCTIVE.

**Definition from first principles:**

A critique is CONSTRUCTIVE if and only if it provides ENOUGH INFORMATION to improve the answer WITHOUT needing to go back to the source material.

**The test (apply this literally):**
Imagine you are an editor who CANNOT see the original source text. You only have:
1. The question
2. The current answer  
3. The critique

Can you make a CONCRETE improvement to the answer using just these three things?

- If YES (you can write a better answer) → CONSTRUCTIVE
- If NO (you need to read the source to know what to write) → NON-CONSTRUCTIVE

**Examples to illustrate the principle:**

Example 1:
Question: "What did she accomplish?"
Answer: "She won awards in 2001 and 2004."
Critique: "Could also mention the organizations she founded."
→ NON-CONSTRUCTIVE (Which organizations? What are their names? You need the source)

Example 2:
Question: "What did she accomplish?"
Answer: "She won awards in 2001 and 2004."
Critique: "Should mention she founded UNESCO and WHO."
→ CONSTRUCTIVE (Now you can add those specific organizations)

Example 3:
Question: "Why did she donate?"
Answer: "She was born in China."
Critique: "She was born in California, not China."
→ NON-CONSTRUCTIVE (Fixing this doesn't help answer WHY she donated)

Example 4:
Answer: "The narrator is a keen sergeant. He admires the Germans. He is confident he will survive."
Critique: "The second sentence is irrelevant."
→ CONSTRUCTIVE (Remove the second sentence - you can do this without the source)

Example 5:
Answer: "The answer is good."
Critique: "Correct answer."
→ CONSTRUCTIVE (Action: keep it as is - no changes needed)

Example 6:
Answer: "Brief description."
Critique: "Correct answer, needs more description."
→ NON-CONSTRUCTIVE (What description? Need source to know what to add)

**Your task:**
Apply the test literally. Can you write a better answer using ONLY the question, current answer, and critique?

Format your response as:
Rationale: [Explain whether you can or cannot improve the answer without the source, and why]
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
| Non-Constructive | 9 | 18.00% |
| Unexpected | 17 | 34.00% |
| **Total** | 50 | 100.00% |


⚠️ **Warning**: 17 samples received unexpected responses from the classifier.

## Sample Examples

### Unexpected Samples (5 shown)

#### Unexpected Example 1

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two: David Ellison and Dana Goldberg.

**Critique**: There are more than two producers on the film.

**Rationale**: The critique indicates that there are more than two producers, but it does not specify who the additional producers are. Without knowing the names or number of the additional producers, I cannot improve the answer. I would need to refer to the source material to identify the other producers involved in the movie.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that there are more than two producers, but it does not specify who the additional producers are. Without knowing the names or number of the additional producers, I cannot improve the answer. I would need to refer to the source material to identify the other producers involved in the movie.

Classification: NON-CONSTRUCTIVE

---

#### Unexpected Example 2

**Question**: Describe the narrator's encounter with the Martians.

**Answer**: The narrator's ship is attacked by Martians, who are intent on conquering Earth. The crew is killed, except for the narrator, who manages to kill one Martian before being overpowered. The remaining two are killed by other crew members. The ship returns to Earth, but the narrator is not a member of the crew, but rather a passenger on the mission.

**Critique**: The answer describes Aigstar's response, not the truth.

**Rationale**: The critique indicates that the answer provided is incorrect because it describes "Aigstar's response" rather than the truth. However, the critique does not provide any specific information or details about what the correct encounter with the Martians should be. Without additional information or specific corrections, it is impossible to improve the answer based solely on the critique. The editor would need to refer back to the source material to understand what the true encounter was and how to accurately describe it.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that the answer provided is incorrect because it describes "Aigstar's response" rather than the truth. However, the critique does not provide any specific information or details about what the correct encounter with the Martians should be. Without additional information or specific corrections, it is impossible to improve the answer based solely on the critique. The editor would need to refer back to the source material to understand what the true encounter was and how to accurately describe it.

Classification: NON-CONSTRUCTIVE

---

#### Unexpected Example 3

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two of th co-producers are working on the movie.

**Critique**: There are more than two producers working on the movie.

**Rationale**: The critique indicates that the number of co-producers mentioned in the answer is incorrect, but it does not provide the correct number. Without knowing the exact number of co-producers, I cannot improve the answer. I would need to refer back to the source material to find out how many co-producers are actually working on the movie.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that the number of co-producers mentioned in the answer is incorrect, but it does not provide the correct number. Without knowing the exact number of co-producers, I cannot improve the answer. I would need to refer back to the source material to find out how many co-producers are actually working on the movie.

Classification: NON-CONSTRUCTIVE

---

#### Unexpected Example 4

**Question**: Answer the following question based on the above passage:

Who are the major characters in the story?

**Answer**: The narrator and a woman

**Critique**: The answer would be better if it gave a little bit more information about the woman.

**Rationale**: The critique suggests adding more information about the woman, but it does not provide any specific details or information that can be added to the answer. Without knowing what additional information to include about the woman, it is not possible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique suggests adding more information about the woman, but it does not provide any specific details or information that can be added to the answer. Without knowing what additional information to include about the woman, it is not possible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

Classification: NON-CONSTRUCTIVE

---

#### Unexpected Example 5

**Question**: Write a ~3 sentence summary.

**Answer**: Jerry and Brian are a happy couple, but when Jerry's friend Janice dies, Brian starts to cry and Jerry leaves.

**Critique**: Jerry does not leave

**Rationale**: The critique provides specific information that directly contradicts a part of the current answer. By stating that "Jerry does not leave," it allows for a concrete improvement to the answer by removing or correcting the part about Jerry leaving. This can be done without needing to refer back to the source material, as the critique gives clear guidance on what is incorrect.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique provides specific information that directly contradicts a part of the current answer. By stating that "Jerry does not leave," it allows for a concrete improvement to the answer by removing or correcting the part about Jerry leaving. This can be done without needing to refer back to the source material, as the critique gives clear guidance on what is incorrect.

Classification: CONSTRUCTIVE

---

### Non-Constructive Samples (5 shown)

#### Non-Constructive Example 1

**Question**: Write a ~3 sentence summary.

**Answer**: Carroll Wales was an art restorer and conservator of paintings, icons, frescoes, and murals. He specialized in the conservation of early Christian Byzantine art and worked on restoration projects in the Middle East, Europe and the United States.

**Critique**: When Wales existed is omitted.

**Rationale**: The critique points out that the time period during which Carroll Wales existed is missing from the answer. However, it does not provide specific information about the dates or time period that should be included. Without knowing the specific years or time frame, I cannot improve the answer to include this information. Therefore, I would need to refer back to the source material to find the relevant dates or time period to add to the summary.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 2

**Question**: Write a ~3 sentence summary.

**Answer**: The Democratic Party needs a nominee, but right now it has a train wreck instead. The front-runner seems too old for the job and is poised to lose the first two primary season contests. The woman who was supposed to become the front-runner on the basis of her policy chops is sliding in the polls after botching her health care strategy.

**Critique**: This is a copy and paste job

**Rationale**: The critique states that the answer is a "copy and paste job," but it does not provide any specific information or guidance on how to improve the answer. Without additional details or suggestions, such as what aspects of the summary need to be changed or what specific information should be included, it is impossible to make a concrete improvement to the answer. The critique does not offer enough information to revise the summary without referring back to the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 3

**Question**: Write a ~10 sentence summary.

**Answer**: Lucius is stationed at Hadrian's Wall in Britannia, to extend Rome's reach. The native Pict tribes continually assault the Wall, and Lucius worries the Romans are losing this war. One night, an enemy fighter sneaks into the camp and slaughters Lucius. The endless cycle of violence weighs heavy on Lucius and he begins to question the purpose of his existence. Despite continuing to fight, rampant violence makes Lucius reconsider his assumed destiny in faraway Britannia.

**Critique**: Far too self-reflective

**Rationale**: The critique "Far too self-reflective" indicates that the current answer is overly focused on Lucius's internal thoughts and feelings. However, it does not provide specific guidance on what to change or add to make the summary less self-reflective. Without additional information or specific suggestions, it is not possible to concretely improve the answer. The critique lacks the necessary details to make a specific revision without referring back to the source material to understand what other aspects should be included or emphasized instead.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 4

**Question**: Why does the narrator want to leave everything behind?

**Answer**: The narrator has a sense of apathy about the life that she has been living and the current state of her living space. She wants to rid her life of external things to make something new and worthwhile out of her life.

**Critique**: We don't know the narrator' gender.

**Rationale**: The critique points out an issue with the assumption of the narrator's gender in the answer. However, it does not provide any specific information to correct or improve the answer regarding the narrator's gender. Without knowing the correct gender from the source material, I cannot make a concrete improvement to the answer. The critique does not provide enough information to address the issue without referring back to the source material.

**Classification**: Non-Constructive

---

#### Non-Constructive Example 5

**Question**: Write a ~3 sentence summary.

**Answer**: A doctor visits a couple who want a female doctor; upon reading their gen-pref results, the doctor tells them that they're having a boy. The female starts crying, and the doctor suggests an abortion.

**Critique**: This doesn't capture the story at all and needs to be rewritten totally. 

**Rationale**: The critique states that the current answer does not capture the story at all and needs to be completely rewritten. However, it does not provide any specific information or details about what the correct story should include. Without additional information or guidance on what the correct content should be, it is impossible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

**Classification**: Non-Constructive

---

### Constructive Samples (5 shown)

#### Constructive Example 1

**Question**: Write a ~6 sentence summary.

**Answer**: An old man walks through the marble memorials of heroes from a bloody past. In the heart of the memorial is a statue of the daughter he lost in a global war, his grief pushing him to the ground in torment. He remembers all the hope he had for her future before he watched the live footage of her dying in battle. Despite all the pain, he resolves to keep going for her sake.

**Critique**: The ending is inaccurate. Rather than resolve to keep going, he curls up and waits to die.

**Rationale**: The critique provides specific information about the ending of the summary, stating that instead of resolving to keep going, the old man curls up and waits to die. This allows for a concrete change to be made to the current answer by altering the last sentence to reflect the accurate ending. The editor can revise the summary to match the critique without needing to refer back to the source material.

**Classification**: Constructive

---

#### Constructive Example 2

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique provides specific information that the event described in the answer is not an actual drowning but rather resembles a baptism. This allows for a concrete improvement to the answer by changing the description of the event from "drown a child" to something more accurate, like "perform a baptism." Therefore, the critique gives enough information to revise the answer without needing to refer back to the source material.

**Classification**: Constructive

---

#### Constructive Example 3

**Question**: Write a ~4 sentence summary.

**Answer**: Sharon is married to Mike, a writer for a popular newspaper company in New York. She is aware that he is cheating on her with Melissa, a coworker. Sharon decides to kill Mike by poisoning his potato soup. She is shocked when he dies in her arms, and she realizes that the poison she used was tasteless and would kill him in his sleep.

**Critique**: Sharon is not aware that he is cheating on her: she simply believes that.

**Rationale**: The critique provides specific information that Sharon is not aware of Mike's infidelity but only believes it. This allows for a concrete improvement to the answer by changing the wording to reflect that Sharon believes Mike is cheating, rather than stating it as a fact. This change can be made without needing to refer back to the source material.

**Classification**: Constructive

---

#### Constructive Example 4

**Question**: Answer the following question based on the above passage:

What has she achieved?

**Answer**: She was elected to the National Assembly as part of the My Step Alliance.

**Critique**: Another accomplishment in Ghazaryan's career is her membership in the Yerevan Council of Elders.

**Rationale**: The critique provides specific information about another accomplishment, namely Ghazaryan's membership in the Yerevan Council of Elders. This allows for a concrete improvement to the answer by adding this specific detail without needing to refer back to the source material.

**Classification**: Constructive

---

#### Constructive Example 5

**Question**: Answer the following question based on the above passage:

What is the story's genre?

**Answer**: Science fiction. The sudden event has a supernatural cause and the story deals with an apocalyptic event.

**Critique**: 'Supernatural' should read 'scientific'

**Rationale**: The critique provides specific information that allows for a concrete improvement to the answer. By changing the word 'supernatural' to 'scientific,' the answer can be corrected to better reflect the genre of science fiction. This change can be made without needing to refer back to the source material.

**Classification**: Constructive

---

## All Samples (Complete Sequence)

### Sample 1/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What role does Will Poulter play in the Lord of the Rings series?

**Answer**: Poulter and the other producers of the show are staying quiet about the specific details of Poulter's character.

**Critique**: While it is true that the specifics of the role are being kept under wraps, it is mentioned that it will be a lead role.

**Rationale**: The critique provides specific information that can be directly added to the answer, namely that Will Poulter's role is a lead role. This allows for a concrete improvement to the answer without needing to refer back to the source material. The revised answer can now include the information that Poulter's role is a lead role, even if the specifics are not disclosed.

**Classification**: Constructive

---

### Sample 2/50 - [Constructive]

**Question**: Summarize the interactions between the narrator and his client.

**Answer**: The narrator meets with his client, Mrs. Richardson, and offers to show her some pictures of her husband's affair. Mrs. Richardson agrees to go to the narrator's apartment.

**Critique**: It is implied that Mrs. Richardson is the one having an affair, not her husband. 

**Rationale**: The critique provides specific information that contradicts the current answer, indicating that Mrs. Richardson is the one having an affair, not her husband. With this information, I can revise the answer to accurately reflect the interactions between the narrator and Mrs. Richardson without needing to refer back to the source material. I can change the answer to: "The narrator meets with his client, Mrs. Richardson, and offers to show her some pictures related to her affair. Mrs. Richardson agrees to go to the narrator's apartment." This correction directly addresses the critique and improves the accuracy of the answer.

**Classification**: Constructive

---

### Sample 3/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They plan to use it as part of its carbon offset program, through which businesses pay them to preserve old-growth forests. 

**Critique**: It's omitted that they plan to put a "working land conservation easement" on the property.

**Rationale**: The critique provides specific information about the new owners' plans that can be directly added to the current answer. The term "working land conservation easement" is specific enough to be included without needing to refer back to the source material. Therefore, the critique allows for a concrete improvement to the answer by adding this detail.

**Classification**: Constructive

---

### Sample 4/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who are the main characters of the story?

**Answer**: Max; Nina

**Critique**: A grammar mistake needs to be fixed here, the comma needs to be deleted between Max and Nina, and replaced with an "and".

**Rationale**: The critique provides specific guidance on how to improve the answer by correcting a grammatical error. It instructs to replace the comma with "and" between "Max" and "Nina." This is a concrete improvement that can be made without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 5/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why do they describe the bad cop as having a scandalous personality?

**Answer**: That information can't be found.

**Critique**: It is omitted that it seems so because they weren't sure if he was going to take them to prison or shoot them.

**Rationale**: The critique provides specific information that can be added to the answer to improve it. It suggests that the bad cop is described as having a scandalous personality because there was uncertainty about whether he would take them to prison or shoot them. This information allows for a concrete improvement to the answer without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 6/50 - [Unexpected]

**Question**: Why were married couples paying more tax than couples just living together?

**Answer**: The proposal was rejected because married couples were paying more tax than couples who were just living together. This was due to the fact that the government had provided incomplete information to voters, which was later overturned by the supreme court.

**Critique**: This response is not related.

**Rationale**: The critique states that the response is not related, but it does not provide any specific information or guidance on how to correct or improve the answer. Without additional details or context, it is impossible to determine what the correct or relevant information should be. Therefore, I cannot make a concrete improvement to the answer using only the question, current answer, and critique.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique states that the response is not related, but it does not provide any specific information or guidance on how to correct or improve the answer. Without additional details or context, it is impossible to determine what the correct or relevant information should be. Therefore, I cannot make a concrete improvement to the answer using only the question, current answer, and critique.

Classification: NON-CONSTRUCTIVE

---

### Sample 7/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

How did the two characters in the story meet?

**Answer**: The two characters met at a party.

**Critique**: The answer can venture a guess, but it must note that it's doing that.

**Rationale**: The critique suggests that the answer should indicate that it is a guess. However, it does not provide specific information on how to improve the answer beyond adding a note that it is a guess. Without additional details or context from the source material, it is not possible to make a concrete improvement to the answer. The critique does not provide enough information to enhance the answer meaningfully without referring back to the source material.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique suggests that the answer should indicate that it is a guess. However, it does not provide specific information on how to improve the answer beyond adding a note that it is a guess. Without additional details or context from the source material, it is not possible to make a concrete improvement to the answer. The critique does not provide enough information to enhance the answer meaningfully without referring back to the source material.

Classification: NON-CONSTRUCTIVE

---

### Sample 8/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two of th co-producers are working on the movie.

**Critique**: There are more than two producers working on the movie.

**Rationale**: The critique indicates that the number of co-producers mentioned in the answer is incorrect, but it does not provide the correct number. Without knowing the exact number of co-producers, I cannot improve the answer. I would need to refer back to the source material to find out how many co-producers are actually working on the movie.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that the number of co-producers mentioned in the answer is incorrect, but it does not provide the correct number. Without knowing the exact number of co-producers, I cannot improve the answer. I would need to refer back to the source material to find out how many co-producers are actually working on the movie.

Classification: NON-CONSTRUCTIVE

---

### Sample 9/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

Who made the Statue of Christopher Columbus in Beacon Hill, Boston?

**Answer**: Joseph Iasigi, a Greek merchant, made the statue of Christopher Columbus.

**Critique**: This is incorrect--the article does not state who made the sculpture.

**Rationale**: The critique points out that the current answer is incorrect but does not provide the correct information or any details that would allow for a concrete improvement to the answer. Without knowing who actually made the statue, I cannot correct the answer. Therefore, I would need to refer back to the source material to find the correct information.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the current answer is incorrect but does not provide the correct information or any details that would allow for a concrete improvement to the answer. Without knowing who actually made the statue, I cannot correct the answer. Therefore, I would need to refer back to the source material to find the correct information.

Classification: NON-CONSTRUCTIVE

---

### Sample 10/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

How many co-producers are working on the movie?

**Answer**: Two: David Ellison and Dana Goldberg.

**Critique**: There are more than two producers on the film.

**Rationale**: The critique indicates that there are more than two producers, but it does not specify who the additional producers are. Without knowing the names or number of the additional producers, I cannot improve the answer. I would need to refer to the source material to identify the other producers involved in the movie.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that there are more than two producers, but it does not specify who the additional producers are. Without knowing the names or number of the additional producers, I cannot improve the answer. I would need to refer to the source material to identify the other producers involved in the movie.

Classification: NON-CONSTRUCTIVE

---

### Sample 11/50 - [Unexpected]

**Question**: Explain the part about Jeanne hating being old despite the fact that she was always old for the narrator.

**Answer**: 

**Critique**: Answer missing.

**Rationale**: The critique points out that the answer is missing entirely. Without any content in the answer, there is no information to improve upon or modify. The critique does not provide any specific details or information that could be used to construct an answer. Therefore, I cannot write a better answer without referring to the source material to understand the context of Jeanne hating being old and how she was perceived by the narrator.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the answer is missing entirely. Without any content in the answer, there is no information to improve upon or modify. The critique does not provide any specific details or information that could be used to construct an answer. Therefore, I cannot write a better answer without referring to the source material to understand the context of Jeanne hating being old and how she was perceived by the narrator.

Classification: NON-CONSTRUCTIVE

---

### Sample 12/50 - [Unexpected]

**Question**: Why is the narrator starving?

**Answer**: It may be implied they are a fish or at least amphibious.

**Critique**: The answer is irrelevant. 

**Rationale**: The critique states that the answer is irrelevant, but it does not provide any specific information or guidance on what the correct or relevant answer should be. Without additional details or context, I cannot improve the answer to address why the narrator is starving. I would need to refer back to the source material to understand the correct context or reason for the narrator's starvation.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique states that the answer is irrelevant, but it does not provide any specific information or guidance on what the correct or relevant answer should be. Without additional details or context, I cannot improve the answer to address why the narrator is starving. I would need to refer back to the source material to understand the correct context or reason for the narrator's starvation.

Classification: NON-CONSTRUCTIVE

---

### Sample 13/50 - [Unexpected]

**Question**: What is the purpose of this article?

**Answer**: To inform of the ban passed by Michigan on intrusive data collection practices, explain the content of the ban and its implications.

**Critique**: Doesn't mention who is being informed.

**Rationale**: The critique points out that the answer does not specify who is being informed by the article. However, it does not provide any specific information about the intended audience or who is being informed. Without knowing who the article is targeting (e.g., Michigan residents, data companies, policymakers), it is not possible to improve the answer. Therefore, additional information from the source material would be needed to address this critique.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the answer does not specify who is being informed by the article. However, it does not provide any specific information about the intended audience or who is being informed. Without knowing who the article is targeting (e.g., Michigan residents, data companies, policymakers), it is not possible to improve the answer. Therefore, additional information from the source material would be needed to address this critique.

Classification: NON-CONSTRUCTIVE

---

### Sample 14/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What has she achieved?

**Answer**: She was elected to the National Assembly as part of the My Step Alliance.

**Critique**: Another accomplishment in Ghazaryan's career is her membership in the Yerevan Council of Elders.

**Rationale**: The critique provides specific information about another accomplishment, namely Ghazaryan's membership in the Yerevan Council of Elders. This allows for a concrete improvement to the answer by adding this specific detail without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 15/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

Who are the major characters in the story?

**Answer**: The narrator and a woman

**Critique**: The answer would be better if it gave a little bit more information about the woman.

**Rationale**: The critique suggests adding more information about the woman, but it does not provide any specific details or information that can be added to the answer. Without knowing what additional information to include about the woman, it is not possible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique suggests adding more information about the woman, but it does not provide any specific details or information that can be added to the answer. Without knowing what additional information to include about the woman, it is not possible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

Classification: NON-CONSTRUCTIVE

---

### Sample 16/50 - [Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Community Forest International purchased a 350-acre old-growth forest from Robena Weatherly. Robena's family has owned the land for generations, dating back to 1812. CFI plans to preserve the forest, using it as part of its carbon offsetting program. 

**Critique**: This should be in past tense and use "at the time of the article" for further accuracy.

**Rationale**: The critique provides specific guidance on how to improve the answer by suggesting a change to past tense and the inclusion of the phrase "at the time of the article" for accuracy. These are concrete changes that can be made directly to the existing text without needing additional information from the source material. The editor can revise the answer to past tense and add the suggested phrase to enhance the accuracy and clarity of the summary.

**Classification**: Constructive

---

### Sample 17/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: A doctor visits a couple who want a female doctor; upon reading their gen-pref results, the doctor tells them that they're having a boy. The female starts crying, and the doctor suggests an abortion.

**Critique**: This doesn't capture the story at all and needs to be rewritten totally. 

**Rationale**: The critique states that the current answer does not capture the story at all and needs to be completely rewritten. However, it does not provide any specific information or details about what the correct story should include. Without additional information or guidance on what the correct content should be, it is impossible to improve the answer without referring back to the source material. Therefore, the critique does not provide enough information to make a concrete improvement to the answer.

**Classification**: Non-Constructive

---

### Sample 18/50 - [Constructive]

**Question**: Does the narrator experience betrayal?

**Answer**: Yes, the narrator experiences betrayal from his former brother who is now a nationalist and has defected. The brother is happy not to shoot the narrator on their final goodbye and understands that he is simply "just a soldier" and does not understand the "big picture."

**Critique**: The second sentence might not be necessary at all.

**Rationale**: The critique suggests that the second sentence might not be necessary, which provides a clear action to improve the answer by potentially removing it. This can be done without needing to refer back to the source material, as the critique directly addresses the content of the answer and suggests a specific change (removal of the second sentence).

**Classification**: Constructive

---

### Sample 19/50 - [Constructive]

**Question**: Which all countries were mentioned in the presentation for having restrictions on press freedom?

**Answer**: The mentioned countries were: Turkey, Mexico, and Egypt.

**Critique**: The answer doesn't mention Russia and Pakistan.

**Rationale**: The critique provides specific information by naming additional countries, Russia and Pakistan, that were mentioned in the presentation. With this information, I can improve the answer by adding these countries to the list without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 20/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: James Butler works an ordinary job in an ordinary office, and interacts with the ordinary edition of himself through a transparent glass wall. He dedicates himself to catching glimpses of the extraordinary James Butler's smile. When the ordinary James Butler finally passes away, the extraordinary James Butler finally crosses the glass wall and dies smiling.

**Critique**: James Butler wishes his life could be extraordinary. He does not interact with this extraordinary life, merely exists knowing that the other side exists.

**Rationale**: The critique provides additional context about James Butler's desires and his lack of interaction with the extraordinary life. However, it does not specify how to incorporate this information into the existing summary. Without specific guidance on what to add or change, the editor cannot make a concrete improvement to the answer without referring back to the source material to understand how these elements fit into the overall narrative.

**Classification**: Non-Constructive

---

### Sample 21/50 - [Non-Constructive]

**Question**: Write a ~7 sentence summary.

**Answer**: Max asks where the narrator was the previous night. The narrator gives evasive answers because she does not want him to get involved in her "mess". Her friend Nina invites her to the party. She enjoys the party but there are disturbing rumors of her hit her ear. She notices Nina yelling, but the worst that happens at first. She finds that Nina is on her back with Todd standing over her. Then he punches her. The narrator does not react.

**Critique**: This summary needs to be re-written as it is awkwardly phrased and has details that do not need to be included. 

**Rationale**: The critique indicates that the summary should be re-written due to awkward phrasing and unnecessary details. However, it does not specify which parts are awkward or which details are unnecessary. Without specific guidance on what to change or remove, I cannot make a concrete improvement to the answer. I would need to refer to the source material to understand the context and determine how to rephrase the summary or which details to omit.

**Classification**: Non-Constructive

---

### Sample 22/50 - [Unexpected]

**Question**: Describe the narrator's encounter with the Martians.

**Answer**: The narrator's ship is attacked by Martians, who are intent on conquering Earth. The crew is killed, except for the narrator, who manages to kill one Martian before being overpowered. The remaining two are killed by other crew members. The ship returns to Earth, but the narrator is not a member of the crew, but rather a passenger on the mission.

**Critique**: The answer describes Aigstar's response, not the truth.

**Rationale**: The critique indicates that the answer provided is incorrect because it describes "Aigstar's response" rather than the truth. However, the critique does not provide any specific information or details about what the correct encounter with the Martians should be. Without additional information or specific corrections, it is impossible to improve the answer based solely on the critique. The editor would need to refer back to the source material to understand what the true encounter was and how to accurately describe it.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that the answer provided is incorrect because it describes "Aigstar's response" rather than the truth. However, the critique does not provide any specific information or details about what the correct encounter with the Martians should be. Without additional information or specific corrections, it is impossible to improve the answer based solely on the critique. The editor would need to refer back to the source material to understand what the true encounter was and how to accurately describe it.

Classification: NON-CONSTRUCTIVE

---

### Sample 23/50 - [Constructive]

**Question**: Write a ~1 sentence summary.

**Answer**: A man-mountain leads a group of people to a lake where they are going to drown a child.

**Critique**: "A man-mountain leads a group of people to a lake where they are going to drown a child." - they were not going to drown the child. It appeared that way, but this looks more like a baptism.

**Rationale**: The critique provides specific information that the event described in the answer is not an actual drowning but rather resembles a baptism. This allows for a concrete improvement to the answer by changing the description of the event from "drown a child" to something more accurate, like "perform a baptism." Therefore, the critique gives enough information to revise the answer without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 24/50 - [Unexpected]

**Question**: What is the narrator's predator?

**Answer**: The narrator's predator is another fish that got to the glowing light first and claimed it as their own.

**Critique**: It is not correct that the bigger fish got to the glowing light first and claimed it as their own

**Rationale**: The critique points out that the information in the answer is incorrect, but it does not provide the correct information or any details that would allow for a concrete improvement to the answer. Without knowing what the correct predator is, you cannot revise the answer accurately. Therefore, you would need to refer back to the source material to determine the correct predator.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the information in the answer is incorrect, but it does not provide the correct information or any details that would allow for a concrete improvement to the answer. Without knowing what the correct predator is, you cannot revise the answer accurately. Therefore, you would need to refer back to the source material to determine the correct predator.

Classification: NON-CONSTRUCTIVE

---

### Sample 25/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Why did Trump aides want dirt on Rhodes and Khal?

**Answer**: They wanted to reverse the Iran Deal.

**Critique**: Trump was the one who wanted to reverse the deal. The dirt was wanted on the two former aides in connection with Trump’s goal of reversing the Iran deal.

**Rationale**: The critique provides specific information that clarifies the relationship between Trump's goal and the desire for dirt on Rhodes and Khal. It specifies that Trump himself wanted to reverse the Iran Deal and that the dirt on the two former aides was sought in connection with this goal. This allows for a more precise answer to be constructed without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 26/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

Why do art critics think the statue is inferior?

**Answer**: because they thought the statue was unremarkable.

**Critique**: Circular logic--does not answer the question.

**Rationale**: The critique points out that the answer uses circular logic and does not actually explain why art critics think the statue is inferior. However, the critique does not provide any specific information or details that could be used to improve the answer. Without additional information about the reasons art critics find the statue unremarkable, it is not possible to improve the answer based solely on the critique. Therefore, the source material would be needed to provide a more detailed explanation.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the answer uses circular logic and does not actually explain why art critics think the statue is inferior. However, the critique does not provide any specific information or details that could be used to improve the answer. Without additional information about the reasons art critics find the statue unremarkable, it is not possible to improve the answer based solely on the critique. Therefore, the source material would be needed to provide a more detailed explanation.

Classification: NON-CONSTRUCTIVE

---

### Sample 27/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: Carroll Wales was an art restorer and conservator of paintings, icons, frescoes, and murals. He specialized in the conservation of early Christian Byzantine art and worked on restoration projects in the Middle East, Europe and the United States.

**Critique**: When Wales existed is omitted.

**Rationale**: The critique points out that the time period during which Carroll Wales existed is missing from the answer. However, it does not provide specific information about the dates or time period that should be included. Without knowing the specific years or time frame, I cannot improve the answer to include this information. Therefore, I would need to refer back to the source material to find the relevant dates or time period to add to the summary.

**Classification**: Non-Constructive

---

### Sample 28/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What will be offered at the Stadium of Light?

**Answer**: No information.

**Critique**: No, the input explicitly says that there will be "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter"

**Rationale**: The critique provides specific details about what will be offered at the Stadium of Light: "a special warm-room complete with places to sleep, hot food and hot drinks for those in need of shelter." With this information, I can improve the answer by including these details without needing to refer back to the original source material.

**Classification**: Constructive

---

### Sample 29/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

mistake

**Answer**: Eric CrossAgario. He can't find the right charger.

**Critique**: there is no question being asked.

**Rationale**: The critique points out that there is no question being asked, which is a fundamental issue with the task setup. However, without a question, it is impossible to determine what the answer should be or how to improve it. The critique does not provide any information on what the question might be or how to adjust the answer accordingly. Therefore, you cannot make a concrete improvement to the answer without knowing the original question or having additional context from the source material.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that there is no question being asked, which is a fundamental issue with the task setup. However, without a question, it is impossible to determine what the answer should be or how to improve it. The critique does not provide any information on what the question might be or how to adjust the answer accordingly. Therefore, you cannot make a concrete improvement to the answer without knowing the original question or having additional context from the source material.

Classification: NON-CONSTRUCTIVE

---

### Sample 30/50 - [Unexpected]

**Question**: Answer the following question based on the above passage:

Who is the producer of the Lord of the Rings series?

**Answer**: New Line Cinema

**Critique**: While New Line Cinema is involved in the production, they are not the main producers.

**Rationale**: The critique indicates that New Line Cinema is involved but not the main producer, yet it does not provide the name of the main producer. Without knowing who the main producer is, I cannot improve the answer. I would need to refer back to the source material to find out the correct information about the main producer.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique indicates that New Line Cinema is involved but not the main producer, yet it does not provide the name of the main producer. Without knowing who the main producer is, I cannot improve the answer. I would need to refer back to the source material to find out the correct information about the main producer.

Classification: NON-CONSTRUCTIVE

---

### Sample 31/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How long is the Canadian Birkebeiner?

**Answer**: The Canadian Birkebeiner is a one-day cross-country marathon event with races from 2 km to 55 km in distance. The main event is 55 km.

**Critique**: It misses to mention that the main event is three races, two 55km and one 31km.

**Rationale**: The critique provides specific information about the main event, stating that it consists of three races: two 55 km races and one 31 km race. This allows for a concrete improvement to the answer by specifying the structure of the main event without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 32/50 - [Unexpected]

**Question**: Write a ~5 sentence summary.

**Answer**: Danny Lee Fread was an American hydraulic engineer and Senior Research Hydrologist, best known for his computer-based mathematical simulation programs for rainfall and runoff to forecast the flow of flooding rivers and dam failures.

**Critique**: Not up to five sentences.

**Rationale**: The critique points out that the answer is not up to five sentences, but it does not provide any specific information or content that could be added to expand the answer to meet the requirement. Without additional details or guidance on what to include, it is not possible to improve the answer to a five-sentence summary without referring back to the source material for more information about Danny Lee Fread's work or achievements.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that the answer is not up to five sentences, but it does not provide any specific information or content that could be added to expand the answer to meet the requirement. Without additional details or guidance on what to include, it is not possible to improve the answer to a five-sentence summary without referring back to the source material for more information about Danny Lee Fread's work or achievements. 

Classification: NON-CONSTRUCTIVE

---

### Sample 33/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

When was 'O sicco first arrested and why?

**Answer**: In the 1990s, Antonio De Luca Bossa - or 'O sicco - was arrested and charged with involvement in a massacre. The massacre was led by the Sarno clan with 'O sicco acting as a trusted member of the Sarno clan. However, De Luca Bossa decided to create his own clan and a bloody war ensued for the control of the territory. Eventually, 'O sicco was arrested and sentenced to life in prison.

**Critique**: It is omitted that six people died in the massacre.

**Rationale**: The critique provides specific information that can be directly added to the current answer to improve it. The critique mentions that six people died in the massacre, which is a concrete detail that can be included without needing to refer back to the source material. Therefore, the critique allows for a specific enhancement of the answer.

**Classification**: Constructive

---

### Sample 34/50 - [Unexpected]

**Question**: What era is this narration set in?

**Answer**: A. 1700s 
B. 1800s 
C. 1900s 
D. 2007
E. 2497 

E. 2497

**Critique**: Multiple incorrect answers listed as choices.

**Rationale**: The critique points out that there are multiple incorrect answers listed as choices, but it does not specify which ones are incorrect or what the correct answer should be. Without knowing which specific choices are incorrect or what the correct answer is, I cannot make a concrete improvement to the answer. I would need to refer back to the source material to determine the correct era for the narration.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique points out that there are multiple incorrect answers listed as choices, but it does not specify which ones are incorrect or what the correct answer should be. Without knowing which specific choices are incorrect or what the correct answer is, I cannot make a concrete improvement to the answer. I would need to refer back to the source material to determine the correct era for the narration.

Classification: NON-CONSTRUCTIVE

---

### Sample 35/50 - [Unexpected]

**Question**: Write a ~3 sentence summary.

**Answer**: Jerry and Brian are a happy couple, but when Jerry's friend Janice dies, Brian starts to cry and Jerry leaves.

**Critique**: Jerry does not leave

**Rationale**: The critique provides specific information that directly contradicts a part of the current answer. By stating that "Jerry does not leave," it allows for a concrete improvement to the answer by removing or correcting the part about Jerry leaving. This can be done without needing to refer back to the source material, as the critique gives clear guidance on what is incorrect.

**Classification**: Unexpected

**Raw Response**: Rationale: The critique provides specific information that directly contradicts a part of the current answer. By stating that "Jerry does not leave," it allows for a concrete improvement to the answer by removing or correcting the part about Jerry leaving. This can be done without needing to refer back to the source material, as the critique gives clear guidance on what is incorrect.

Classification: CONSTRUCTIVE

---

### Sample 36/50 - [Constructive]

**Question**: Write a ~4 sentence summary.

**Answer**: Sharon is married to Mike, a writer for a popular newspaper company in New York. She is aware that he is cheating on her with Melissa, a coworker. Sharon decides to kill Mike by poisoning his potato soup. She is shocked when he dies in her arms, and she realizes that the poison she used was tasteless and would kill him in his sleep.

**Critique**: Sharon is not aware that he is cheating on her: she simply believes that.

**Rationale**: The critique provides specific information that Sharon is not aware of Mike's infidelity but only believes it. This allows for a concrete improvement to the answer by changing the wording to reflect that Sharon believes Mike is cheating, rather than stating it as a fact. This change can be made without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 37/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

Who is steering Miller's legal fight now that it is heading to the U.S. Court of Appeals?

**Answer**: The lawyers representing Andrew Miller are steering his legal fight now that it is heading to the U.S. Court of Appeals. These lawyers are affiliated with veteran Washington legal group that has a history of taking on Democrats, as well as longstanding Republican donors.

**Critique**: The answer's wording implies the legal group challenges both Democrats and Republican donors, which is wrong. The group is backed by Republican donors.

**Rationale**: The critique provides specific information about the error in the answer. It clarifies that the legal group is backed by Republican donors, rather than challenging them. This allows for a concrete improvement to the answer by correcting the implication without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 38/50 - [Constructive]

**Question**: Are there other characters in the story?

**Answer**: The boy and the men with apparently fine boots.

**Critique**: There is no mention of the man, the main character. 

**Rationale**: The critique specifies that the main character, "the man," is missing from the answer. With this information, you can improve the answer by adding "the man" to the list of characters without needing to refer back to the source material. The critique provides enough detail to make a concrete improvement to the answer.

**Classification**: Constructive

---

### Sample 39/50 - [Constructive]

**Question**: When was Patsy's first film?

**Answer**: 1983

**Critique**: 1983 was her first television role ('In 1983 she had debut in television'), so replace with the correct answer: 1986 ('1986 _El cachas de oro_ Selena')

**Rationale**: The critique provides specific information that allows for a concrete improvement to the answer. It specifies that 1983 was her first television role and that her first film was in 1986, naming the film as "El cachas de oro" and the role as "Selena." With this information, I can revise the answer to accurately reflect her first film role without needing to consult the source material.

**Classification**: Constructive

---

### Sample 40/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What is the story's genre?

**Answer**: Science fiction. The sudden event has a supernatural cause and the story deals with an apocalyptic event.

**Critique**: 'Supernatural' should read 'scientific'

**Rationale**: The critique provides specific information that allows for a concrete improvement to the answer. By changing the word 'supernatural' to 'scientific,' the answer can be corrected to better reflect the genre of science fiction. This change can be made without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 41/50 - [Non-Constructive]

**Question**: Why does the narrator want to leave everything behind?

**Answer**: The narrator has a sense of apathy about the life that she has been living and the current state of her living space. She wants to rid her life of external things to make something new and worthwhile out of her life.

**Critique**: We don't know the narrator' gender.

**Rationale**: The critique points out an issue with the assumption of the narrator's gender in the answer. However, it does not provide any specific information to correct or improve the answer regarding the narrator's gender. Without knowing the correct gender from the source material, I cannot make a concrete improvement to the answer. The critique does not provide enough information to address the issue without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 42/50 - [Non-Constructive]

**Question**: Write a ~2 sentence summary.

**Answer**: President Trump accused Democrats who did not applaud during his State of the Union address of treason, saying they would rather see Trump do badly than do well. Trump also contrasted Democrats' reactions to his State of the Union with the enthusiastic support from Republicans. He also criticized Pelosi for calling the bonuses some companies are giving employees as a result of Trump's tax cuts "crumbs," saying she wants to give all of Americans' money away. Trump then likened Pelosi to Hillary Clinton, saying she is the Democrats' "secret weapon."

**Critique**: There are too many sentences. 

**Rationale**: The critique indicates that the answer should be more concise by reducing the number of sentences. However, it does not specify which information should be prioritized or omitted to achieve this. Without guidance on what content is essential or extraneous, I cannot determine how to condense the answer effectively without referring back to the source material to understand the key points. Therefore, I cannot make a concrete improvement to the answer using only the question, current answer, and critique.

**Classification**: Non-Constructive

---

### Sample 43/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: The narrator persuades people to be wise about recycled pizza boxes. They say that because pizza boxes are made of corrugated cardboard, they are recyclable. The reason some pizza boxes are not recyclable is that the juicy toppings and cheese stick to the pizza box. Once they are caked with oil or grease, they are difficult to recycle.

Additionally, pizza boxes usually have moisture, which could harbor mold and bacteria if composted. One way to avoid such events is to ensure the pizza box is pest free. Properly disposing them will be helpful, too.

**Critique**: The oil is what causes problems when composting too, and "properly disposing them" is the subject of the article

**Rationale**: The critique provides specific information that can be used to improve the answer. It mentions that oil causes problems when composting, which can be added to the explanation about why pizza boxes are difficult to recycle. Additionally, it highlights that "properly disposing them" is the subject of the article, suggesting that the answer should focus more on disposal methods. These details allow for a concrete improvement to the answer without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 44/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

How do the boy and the mother feel about each other?

**Answer**: The boy and his mother feel deeply connected to each other, but they also feel hurt and confusion because he left for awhile. However, both remain hopeful that he will return and their relationship can continue to grow.

**Critique**: "Slowly, quickly, coldly he spoke to his mother. "Fine," he would say. "You're not my mother," he would say." is evidence of the terms on which the son left his mother. Correct the answer to reflect that the boy denies the connection with his mother.

**Rationale**: The critique provides specific evidence from the text that indicates the boy denies the connection with his mother, which contradicts the current answer's claim of a deep connection. Using this information, I can revise the answer to reflect the boy's denial of the connection without needing to refer back to the source material. The critique gives enough detail to make a concrete improvement to the answer.

**Classification**: Constructive

---

### Sample 45/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: A man in a trail hears a car approaching. It's a dark blue Cobra. The man waits with a concealed weapon. A tall man pulls out and he places a said weapon beside him on the passenger seat, and then climbs out of the car and walk toward the trail. The two meet, the tall man walks up to the weathered man. Both have weapons: the weathered man a silenced Glock and the tall man a Marlin 1984 rifle; the weathered man holds it back on the trail, and the tall man resumes walking to the base of the trail. The two meet there, each clutching a gun and a knife, with a lot of tension in the air.

**Critique**: The two never meet. 

**Rationale**: The critique provides specific information that directly contradicts a key element of the current answer. It states that "the two never meet," which allows for a concrete revision of the answer. Without needing to refer back to the source material, the editor can adjust the summary to reflect that the two characters do not actually meet, thus improving the accuracy of the answer.

**Classification**: Constructive

---

### Sample 46/50 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What is his academic pedigree?

**Answer**: His undergraduate degree is a BA from the University of Toronto, his master's degree is a Ph. D. from York University. He also has a postgraduate diploma from Humber College.

**Critique**: The claim that he has a postgraduate degree from Humber College is unattested.

**Rationale**: The critique points out that the claim about the postgraduate diploma from Humber College is unattested, but it does not provide any specific information on what should replace or correct this part of the answer. Without additional details or a specific correction, I cannot improve the answer regarding his academic pedigree. I would need to refer back to the source material to verify or correct the information about the postgraduate diploma.

**Classification**: Non-Constructive

---

### Sample 47/50 - [Constructive]

**Question**: Write a ~6 sentence summary.

**Answer**: An old man walks through the marble memorials of heroes from a bloody past. In the heart of the memorial is a statue of the daughter he lost in a global war, his grief pushing him to the ground in torment. He remembers all the hope he had for her future before he watched the live footage of her dying in battle. Despite all the pain, he resolves to keep going for her sake.

**Critique**: The ending is inaccurate. Rather than resolve to keep going, he curls up and waits to die.

**Rationale**: The critique provides specific information about the ending of the summary, stating that instead of resolving to keep going, the old man curls up and waits to die. This allows for a concrete change to be made to the current answer by altering the last sentence to reflect the accurate ending. The editor can revise the summary to match the critique without needing to refer back to the source material.

**Classification**: Constructive

---

### Sample 48/50 - [Non-Constructive]

**Question**: Write a ~3 sentence summary.

**Answer**: The Democratic Party needs a nominee, but right now it has a train wreck instead. The front-runner seems too old for the job and is poised to lose the first two primary season contests. The woman who was supposed to become the front-runner on the basis of her policy chops is sliding in the polls after botching her health care strategy.

**Critique**: This is a copy and paste job

**Rationale**: The critique states that the answer is a "copy and paste job," but it does not provide any specific information or guidance on how to improve the answer. Without additional details or suggestions, such as what aspects of the summary need to be changed or what specific information should be included, it is impossible to make a concrete improvement to the answer. The critique does not offer enough information to revise the summary without referring back to the source material.

**Classification**: Non-Constructive

---

### Sample 49/50 - [Constructive]

**Question**: Answer the following question based on the above passage:

What do the new owners plan to do with the property?

**Answer**: They are hoping to manage it so that it will cater for some of the neighboring community.

**Critique**: This answer is wrong. They plan to  use it for their carbon offset program and preserve it by putting a "working land conservation easement" on the property. 


**Rationale**: The critique provides specific information about the new owners' plans for the property, including using it for a carbon offset program and preserving it with a "working land conservation easement." This allows for a concrete improvement to the answer without needing to refer back to the source material. The editor can directly incorporate these details into the answer.

**Classification**: Constructive

---

### Sample 50/50 - [Non-Constructive]

**Question**: Write a ~10 sentence summary.

**Answer**: Lucius is stationed at Hadrian's Wall in Britannia, to extend Rome's reach. The native Pict tribes continually assault the Wall, and Lucius worries the Romans are losing this war. One night, an enemy fighter sneaks into the camp and slaughters Lucius. The endless cycle of violence weighs heavy on Lucius and he begins to question the purpose of his existence. Despite continuing to fight, rampant violence makes Lucius reconsider his assumed destiny in faraway Britannia.

**Critique**: Far too self-reflective

**Rationale**: The critique "Far too self-reflective" indicates that the current answer is overly focused on Lucius's internal thoughts and feelings. However, it does not provide specific guidance on what to change or add to make the summary less self-reflective. Without additional information or specific suggestions, it is not possible to concretely improve the answer. The critique lacks the necessary details to make a specific revision without referring back to the source material to understand what other aspects should be included or emphasized instead.

**Classification**: Non-Constructive

---

