# Critique Analysis Report

## Dataset Information
- **Dataset**: openai_self_critique
- **Total Samples**: 50
- **Random Seed**: 42
- **Timestamp**: 20251015_0110

## Classification Prompt

The following prompt was used to classify critiques:

```
You are evaluating the QUALITY of a critique given a question and an answer.

Definitions (decide based ONLY on the critique text):
- CONSTRUCTIVE: The critique not only points out what is wrong or missing in the answer,
  but ALSO provides the correct information, a concrete correction, or a clear next step
  to fix/improve the answer (e.g., "It should be white, not black", "Add X", "Replace Y with Z").
- NON-CONSTRUCTIVE: The critique only states what is wrong or that something is missing,
  without supplying the correct information or a concrete way to fix it.

Special case:
- If the answer is already correct and thus **no critique is necessary**, then an empty critique
  (or a critique that explicitly says "no issues") should be treated as **CONSTRUCTIVE/APPROPRIATE**.

Now return exactly one token: either
  "Constructive"  or  "Non-Constructive"

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
| Constructive | 5 | 10.00% |
| Non-Constructive | 45 | 90.00% |
| Unexpected | 0 | 0.00% |
| **Total** | 50 | 100.00% |


## Sample Examples (5 Random Samples)

### Example 1/5 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about Pierce?

**Answer**: Pierce is a childhood friend of Josh. He is a menacing presence, but Josh vouches for him, saying he's not that bad. Josh and Sana also seem to be interested in him.

**Critique**: Doesn't fully answer the question

**Classification**: Non-Constructive

---

### Example 2/5 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

What does the text say about the school Jeffery goes to?

**Answer**: No answer

**Critique**: No response is provided for this question; a response needs to be created. 

**Classification**: Non-Constructive

---

### Example 3/5 - [Non-Constructive]

**Question**: Who is the child in the story?

**Answer**: The child in the story is a young boy.

**Critique**: It's omitted that the child was being crushed under a roof and screaming at the man to not leave him. 

**Classification**: Non-Constructive

---

### Example 4/5 - [Non-Constructive]

**Question**: Answer the following question based on the above passage:

Summarize Whistler's activities during the 1970s.

**Answer**: He moved to Hawaii and completed a doctorate in botany from the University of Hawaii at Manoa, focusing on Samoan plant life, in 1979. He lived in Samoa during the 1970s before the logging and tourism led to the deforestation of the country's rainforests.

**Critique**: The answer should mention Whistler's time in the Peace Corps.

**Classification**: Non-Constructive

---

### Example 5/5 - [Non-Constructive]

**Question**: When was Olivewood established?

**Answer**: Olivewood was established in 2018.

**Critique**: The answer does not provide the full context (the area has been producing films since the 1950s).

**Classification**: Non-Constructive

---

