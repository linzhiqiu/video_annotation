#!/usr/bin/env python3
"""
Analyze critiques from OpenAI Self-Critique and MM-RLHF datasets.
Classifies critiques as Constructive or Non-Constructive using GPT-4o.
"""

import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Classification prompt template
JUDGE_PROMPT_TEMPLATE = """You are evaluating whether a critique is CONSTRUCTIVE or NON-CONSTRUCTIVE.

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

**Important: Think creatively about implications**
Some critiques don't explicitly tell you what to do but strongly imply it:
- "Jerry does not leave" → Remove the part about Jerry leaving (CONSTRUCTIVE)
- "We don't know the narrator's gender" → Use "they" instead of "he/she" (CONSTRUCTIVE)
- "The sentence is unnecessary" but multiple sentences exist → Which sentence? (NON-CONSTRUCTIVE)
- "Second sentence is irrelevant" → Remove the second sentence (CONSTRUCTIVE)
- "First seven chapters are suitable for undergrad, book as a whole for grad students" → Implies chapters 8+ exceed novice (CONSTRUCTIVE)
- "Statement cannot be confirmed and spelling is incorrect" → Fix spelling, remove unconfirmed statement (CONSTRUCTIVE)

**Critical distinctions:**
1. If answer is ALREADY GOOD and critique ONLY confirms it (purely positive, no problems mentioned):
   - "Answer correctly and accurately" → CONSTRUCTIVE (confirms it's good, keep as is)
   - "Correct answer" → CONSTRUCTIVE (no changes needed)
   - "Comprehensive analysis" → CONSTRUCTIVE (praise only)
   - "The answer is correct" → CONSTRUCTIVE (affirmation only)

2. If critique mentions ANY problem, even while being positive:
   - "Correct answer, no description" → NON-CONSTRUCTIVE (what description?)
   - "Answer correctly, needs more detail" → NON-CONSTRUCTIVE (what details?)
   - "Good but missing X" without specifying X → NON-CONSTRUCTIVE

3. If critique says something is WRONG but doesn't tell you what's RIGHT:
   - "Everything beyond first sentence is inaccurate" → What IS accurate? (NON-CONSTRUCTIVE)
   - "This cannot be confirmed" → What CAN be confirmed? (NON-CONSTRUCTIVE)
   
4. If critique IMPLIES what's correct through contrast:
   - "First seven for undergrad, whole book for grad" → Clearly implies 8+ are advanced (CONSTRUCTIVE)
   - "Cannot be confirmed + spelling wrong" → Fix spelling + remove unconfirmed part (CONSTRUCTIVE)

**Examples to illustrate the principle:**

Example 1:
Question: "What did she accomplish?"
Answer: "She won awards in 2001 and 2004."
Critique: "Could also mention the organizations she founded."
→ NON-CONSTRUCTIVE (Which organizations? Need the source)

Example 2:
Question: "What did she accomplish?"
Answer: "She won awards in 2001 and 2004."
Critique: "Should mention she founded UNESCO and WHO."
→ CONSTRUCTIVE (Specific organizations provided)

Example 3:
Question: "Why did she donate?"
Answer: "She was born in China."
Critique: "She was born in California, not China."
→ NON-CONSTRUCTIVE (Doesn't help answer WHY she donated; need source for the reason)

Example 4:
Answer: "The narrator is a keen sergeant. He admires the Germans. He is confident he will survive."
Critique: "The second sentence is irrelevant."
→ CONSTRUCTIVE (Remove the second sentence)

Example 5:
Answer: "Jerry and Brian are happy, but when Janice dies, Brian cries and Jerry leaves."
Critique: "Jerry does not leave."
→ CONSTRUCTIVE (Remove or correct the part about Jerry leaving)

Example 6:
Answer: "The narrator lives in a small house. She wants to leave."
Critique: "We don't know the narrator's gender."
→ CONSTRUCTIVE (Change "she" to "they")

Example 7:
Answer: "Accurate, detailed description of the setting."
Critique: "The description is accurate."
→ CONSTRUCTIVE (Confirms answer is good; purely positive, no problems mentioned)

Example 7b:
Answer: "Brief description."
Critique: "Correct answer, no description."
→ NON-CONSTRUCTIVE (Says "correct" but also says problem: "no description" - what description is needed?)

Example 7c:
Answer: "The puppies are interacting."
Critique: "Answer correctly and accurately."
→ CONSTRUCTIVE (Purely positive affirmation; action = keep as is)

Example 8:
Question: "What chapters exceed novice level?"
Answer: "The first seven chapters."
Critique: "First seven are for undergrads, whole book for grad students."
→ CONSTRUCTIVE (Implies chapters 8+ exceed novice)

Example 9:
Answer: "Primoš is in urban area. Has trails and museum."
Critique: "Urban area statement cannot be confirmed. Spelling of Primož is wrong."
→ CONSTRUCTIVE (Fix spelling, remove unconfirmed statement)

Example 10:
Answer: "Complex narrative with several key points."
Critique: "Everything beyond first sentence is inaccurate."
→ NON-CONSTRUCTIVE (What IS accurate then? Need source to know what to write)

**Your task:**
Apply the test literally. Think about what the critique implies. Can you write a better answer using ONLY the question, current answer, and critique?

Format your response as:
Rationale: [Explain whether you can or cannot improve the answer without the source, and why. If you can improve it, briefly state how.]
Classification: [Constructive or Non-Constructive]

Question:
{question}

Answer:
{answer}

Critique:
{critique}"""


def load_openai_data(file_path: Path, sample_count: int, seed: int, task_type: str = None) -> Tuple[List[Dict], int, int]:
    """Load and sample from OpenAI self-critique dataset.
    
    Args:
        file_path: Path to the data file
        sample_count: Number of samples to take
        seed: Random seed
        task_type: 'summarization', 'qa', or None for all
    
    Returns:
        (samples, total_dataset_size, filtered_dataset_size)
    """
    random.seed(seed)
    
    all_samples = []
    total_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            is_summarization = item.get('is_topic_based_summarization', False)
            
            # Filter by task type if specified
            if task_type == 'summarization' and not is_summarization:
                continue
            elif task_type == 'qa' and is_summarization:
                continue
            
            questions = item.get('data', {}).get('questions', [])
            
            for q in questions:
                question_text = q.get('question', '')
                answers = q.get('answers', [])
                
                for ans in answers:
                    answer_text = ans.get('answer', '')
                    critiques = ans.get('feedback', {}).get('critiques', [])
                    
                    total_count += 1
                    
                    # Skip if no critiques
                    if not critiques:
                        continue
                    
                    # Take the first critique
                    critique_text = critiques[0].get('text', '')
                    
                    all_samples.append({
                        'question': question_text,
                        'answer': answer_text,
                        'critique': critique_text,
                        'is_summarization': is_summarization
                    })
    
    filtered_size = len(all_samples)
    
    # Sample
    if sample_count == -1:
        # Use full dataset
        print(f"Using full dataset: {filtered_size} samples")
        return all_samples, total_count, filtered_size
    elif len(all_samples) < sample_count:
        print(f"Warning: Only {len(all_samples)} samples available, requested {sample_count}")
        return all_samples, total_count, filtered_size
    
    return random.sample(all_samples, sample_count), total_count, filtered_size


def load_mmrlhf_data(file_path: Path, sample_count: int, seed: int) -> Tuple[List[Dict], int]:
    """Load and sample from MM-RLHF dataset (video only).
    Returns (samples, total_dataset_size)
    """
    random.seed(seed)
    
    all_samples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            
            # Filter: only video items
            if 'video' not in item:
                continue
            
            question = item.get('question', '')
            models_output = item.get('models_output', [])
            score_reasons = item.get('score_reasons', [])
            
            # Check the relationship between models_output and score_reasons
            # Based on your example, it can vary - sometimes N+1, sometimes equal
            # We'll take the minimum to be safe and pair them up
            num_pairs = min(len(models_output), len(score_reasons))
            
            # Zip the available pairs
            for i in range(num_pairs):
                all_samples.append({
                    'question': question,
                    'answer': models_output[i],
                    'critique': score_reasons[i]
                })
    
    total_size = len(all_samples)
    
    # Sample
    if sample_count == -1:
        # Use full dataset
        print(f"Using full dataset: {total_size} samples")
        return all_samples, total_size
    elif len(all_samples) < sample_count:
        print(f"Warning: Only {len(all_samples)} samples available, requested {sample_count}")
        return all_samples, total_size
    
    return random.sample(all_samples, sample_count), total_size


def classify_answer_quality(critique: str, model: str = "gpt-4o-2024-08-06") -> str:
    """
    Classify whether a critique indicates the answer is good or needs improvement.
    Returns: "Good" or "Needs Improvement"
    """
    prompt = f"""You are classifying whether a critique indicates the answer is GOOD or NEEDS IMPROVEMENT.

**Classification rules:**

GOOD (answer is already correct/acceptable, no changes needed):
- Critique is purely positive: "Correct answer", "Answer correctly", "Accurate description", "The answer is correct"
- Critique praises without suggesting problems: "Comprehensive analysis", "Very detailed"
- Empty or minimal positive feedback with no issues mentioned

NEEDS IMPROVEMENT (answer has problems, missing info, or should be changed):
- Critique points out errors: "This is false", "Incorrect", "The description is wrong"
- Critique says something is missing: "Missing X", "Should mention Y", "Omitted that Z", "No description"
- Critique suggests changes: "Should be more detailed", "Too simple", "Needs analysis"
- Critique is mixed (positive + negative): "Correct answer, no description" → Has a problem (missing description)

**Key principle:** If the critique mentions ANY problem, gap, or suggestion for improvement → NEEDS IMPROVEMENT
If critique is ONLY positive with no issues → GOOD

Return ONLY: "Good" or "Needs Improvement"

Critique:
{critique}"""
    
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        if "Good" in result and "Needs" not in result:
            return "Good"
        elif "Needs" in result or "Improvement" in result:
            return "Needs Improvement"
        else:
            return "Needs Improvement"  # Default to needs improvement if unclear
            
    except Exception as e:
        print(f"Error classifying answer quality: {e}")
        return "Needs Improvement"


def classify_critique(question: str, answer: str, critique: str, model: str = "gpt-4o-2024-08-06") -> Tuple[str, str, str]:
    """
    Classify a critique using GPT-4o.
    Returns (label, rationale, raw_response)
    label is one of: "Constructive", "Non-Constructive", "Unexpected"
    """
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        question=question,
        answer=answer,
        critique=critique
    )
    
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200
        )
        
        raw_response = response.choices[0].message.content.strip()
        
        # Parse rationale and classification
        rationale = ""
        label = "Unexpected"
        
        # Split by lines and look for Classification
        lines = raw_response.split('\n')
        for line in lines:
            if line.startswith("Rationale:"):
                rationale = line.replace("Rationale:", "").strip()
            elif line.startswith("Classification:"):
                classification_text = line.replace("Classification:", "").strip()
                # Handle both "Constructive" and "CONSTRUCTIVE", "Non-Constructive" and "NON-CONSTRUCTIVE"
                classification_upper = classification_text.upper()
                if "CONSTRUCTIVE" in classification_upper and "NON-CONSTRUCTIVE" not in classification_upper and "NON" not in classification_upper:
                    label = "Constructive"
                elif "NON-CONSTRUCTIVE" in classification_upper or "NON CONSTRUCTIVE" in classification_upper:
                    label = "Non-Constructive"
        
        # Fallback: check if these words appear anywhere in the response
        if label == "Unexpected":
            response_upper = raw_response.upper()
            # Count occurrences to handle "Non-Constructive" vs just "Constructive"
            if "NON-CONSTRUCTIVE" in response_upper or "NON CONSTRUCTIVE" in response_upper:
                label = "Non-Constructive"
            elif "CONSTRUCTIVE" in response_upper:
                label = "Constructive"
        
        # If we couldn't parse rationale properly, use full response
        if not rationale:
            rationale = raw_response
            
        return label, rationale, raw_response
            
    except Exception as e:
        print(f"Error classifying critique: {e}")
        return "Unexpected", str(e), str(e)


def print_examples(samples: List[Dict], num_examples: int = 5):
    """Print random examples to console."""
    random_examples = random.sample(samples, min(num_examples, len(samples)))
    
    print("\n" + "="*80)
    print(f"Randomly Selected Examples ({len(random_examples)}):")
    print("="*80 + "\n")
    
    for i, sample in enumerate(random_examples, 1):
        print(f"{'='*20} Example {i}/{len(random_examples)} {'='*20}")
        print(f"Question: {sample['question']}")
        print(f"\nAnswer: {sample['answer']}")
        print(f"\nCritique: {sample['critique']}")
        print()


def generate_report(
    dataset_name: str,
    samples: List[Dict],
    seed: int,
    timestamp: str,
    output_path: Path,
    total_dataset_size: int,
    filtered_dataset_size: int = None,
    task_type: str = None
):
    """Generate markdown report."""
    
    # Calculate statistics
    total = len(samples)
    constructive = sum(1 for s in samples if s['label'] == 'Constructive')
    non_constructive = sum(1 for s in samples if s['label'] == 'Non-Constructive')
    unexpected = sum(1 for s in samples if s['label'] == 'Unexpected')
    
    constructive_pct = (constructive / total * 100) if total > 0 else 0
    non_constructive_pct = (non_constructive / total * 100) if total > 0 else 0
    unexpected_pct = (unexpected / total * 100) if total > 0 else 0
    
    # For MM-RLHF, also calculate by answer quality
    is_mmrlhf = dataset_name == 'mm_rlhf'
    if is_mmrlhf and samples and 'answer_quality' in samples[0]:
        good_samples = [s for s in samples if s.get('answer_quality') == 'Good']
        needs_improvement_samples = [s for s in samples if s.get('answer_quality') == 'Needs Improvement']
        
        good_constructive = sum(1 for s in good_samples if s['label'] == 'Constructive')
        good_non_constructive = sum(1 for s in good_samples if s['label'] == 'Non-Constructive')
        
        ni_constructive = sum(1 for s in needs_improvement_samples if s['label'] == 'Constructive')
        ni_non_constructive = sum(1 for s in needs_improvement_samples if s['label'] == 'Non-Constructive')
    else:
        good_samples = []
        needs_improvement_samples = []
    
    # Separate samples by label for non-MM-RLHF
    unexpected_samples = [s for s in samples if s['label'] == 'Unexpected']
    constructive_samples = [s for s in samples if s['label'] == 'Constructive']
    non_constructive_samples = [s for s in samples if s['label'] == 'Non-Constructive']
    
    # Get random examples for each category (up to 20 each) for non-MM-RLHF
    unexpected_examples = random.sample(unexpected_samples, min(20, len(unexpected_samples)))
    constructive_examples = random.sample(constructive_samples, min(20, len(constructive_samples)))
    non_constructive_examples = random.sample(non_constructive_samples, min(20, len(non_constructive_samples)))
    
    # Generate report header
    task_info = f" ({task_type})" if task_type else ""
    report = f"""# Critique Analysis Report

## Dataset Information
- **Dataset**: {dataset_name}{task_info}
- **Total Dataset Size**: {total_dataset_size} critique samples"""
    
    if filtered_dataset_size is not None and filtered_dataset_size != total_dataset_size:
        report += f"\n- **Filtered Dataset Size** ({task_type}): {filtered_dataset_size} critique samples"
    
    report += f"""
- **Sampled for Analysis**: {total} samples
- **Random Seed**: {seed}
- **Timestamp**: {timestamp}

## Classification Prompt

The following prompt was used to classify critiques:

```
{JUDGE_PROMPT_TEMPLATE}
```

## Classification Statistics

### Overall Statistics

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | {constructive} | {constructive_pct:.2f}% |
| Non-Constructive | {non_constructive} | {non_constructive_pct:.2f}% |
| Unexpected | {unexpected} | {unexpected_pct:.2f}% |
| **Total** | {total} | 100.00% |

"""

    if is_mmrlhf and good_samples:
        good_total = len(good_samples)
        ni_total = len(needs_improvement_samples)
        
        good_const_pct = (good_constructive / good_total * 100) if good_total > 0 else 0
        good_nonconst_pct = (good_non_constructive / good_total * 100) if good_total > 0 else 0
        
        ni_const_pct = (ni_constructive / ni_total * 100) if ni_total > 0 else 0
        ni_nonconst_pct = (ni_non_constructive / ni_total * 100) if ni_total > 0 else 0
        
        report += f"""### Statistics by Answer Quality

**Good Answers** (critique says answer is correct/acceptable):

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | {good_constructive} | {good_const_pct:.2f}% |
| Non-Constructive | {good_non_constructive} | {good_nonconst_pct:.2f}% |
| **Total** | {good_total} | 100.00% |

**Needs Improvement Answers** (critique says answer has issues):

| Label | Count | Percentage |
|-------|-------|------------|
| Constructive | {ni_constructive} | {ni_const_pct:.2f}% |
| Non-Constructive | {ni_non_constructive} | {ni_nonconst_pct:.2f}% |
| **Total** | {ni_total} | 100.00% |

"""

    if unexpected > 0:
        report += f"\n⚠️ **Warning**: {unexpected} samples received unexpected responses from the classifier.\n\n"
    
    # Add sample examples section
    report += "## Sample Examples\n\n"
    
    # For MM-RLHF, show examples by answer quality
    if is_mmrlhf and good_samples:
        # Good answers section
        good_constructive_samples = [s for s in samples if s.get('answer_quality') == 'Good' and s['label'] == 'Constructive']
        good_non_constructive_samples = [s for s in samples if s.get('answer_quality') == 'Good' and s['label'] == 'Non-Constructive']
        
        good_const_examples = random.sample(good_constructive_samples, min(20, len(good_constructive_samples))) if good_constructive_samples else []
        good_nonconst_examples = random.sample(good_non_constructive_samples, min(20, len(good_non_constructive_samples))) if good_non_constructive_samples else []
        
        # Needs improvement section
        ni_constructive_samples = [s for s in samples if s.get('answer_quality') == 'Needs Improvement' and s['label'] == 'Constructive']
        ni_non_constructive_samples = [s for s in samples if s.get('answer_quality') == 'Needs Improvement' and s['label'] == 'Non-Constructive']
        
        ni_const_examples = random.sample(ni_constructive_samples, min(20, len(ni_constructive_samples))) if ni_constructive_samples else []
        ni_nonconst_examples = random.sample(ni_non_constructive_samples, min(20, len(ni_non_constructive_samples))) if ni_non_constructive_samples else []
        
        # Always show all 4 sections (even if some are empty)
        
        # Good answers - Constructive
        report += f"### Good Answers - Constructive ({len(good_const_examples)} shown)\n\n"
        if good_const_examples:
            for i, example in enumerate(good_const_examples, 1):
                report += f"#### Good Answer - Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Answer Quality**: {example.get('answer_quality', 'N/A')}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
        else:
            report += "No examples in this category.\n\n"
        
        # Good answers - Non-Constructive
        report += f"### Good Answers - Non-Constructive ({len(good_nonconst_examples)} shown)\n\n"
        if good_nonconst_examples:
            for i, example in enumerate(good_nonconst_examples, 1):
                report += f"#### Good Answer - Non-Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Answer Quality**: {example.get('answer_quality', 'N/A')}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
        else:
            report += "No examples in this category.\n\n"
        
        # Needs Improvement - Constructive
        report += f"### Needs Improvement Answers - Constructive ({len(ni_const_examples)} shown)\n\n"
        if ni_const_examples:
            for i, example in enumerate(ni_const_examples, 1):
                report += f"#### Needs Improvement - Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Answer Quality**: {example.get('answer_quality', 'N/A')}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
        else:
            report += "No examples in this category.\n\n"
        
        # Needs Improvement - Non-Constructive
        report += f"### Needs Improvement Answers - Non-Constructive ({len(ni_nonconst_examples)} shown)\n\n"
        if ni_nonconst_examples:
            for i, example in enumerate(ni_nonconst_examples, 1):
                report += f"#### Needs Improvement - Non-Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Answer Quality**: {example.get('answer_quality', 'N/A')}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
        else:
            report += "No examples in this category.\n\n"
    else:
        # Original logic for non-MM-RLHF datasets
        # Unexpected examples (if any)
        if unexpected_examples:
            report += f"### Unexpected Samples ({len(unexpected_examples)} shown)\n\n"
            for i, example in enumerate(unexpected_examples, 1):
                report += f"#### Unexpected Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += f"**Raw Response**: {example.get('raw_response', 'N/A')}\n\n"
                report += "---\n\n"
        
        # Non-Constructive examples
        if non_constructive_examples:
            report += f"### Non-Constructive Samples ({len(non_constructive_examples)} shown)\n\n"
            for i, example in enumerate(non_constructive_examples, 1):
                report += f"#### Non-Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
        
        # Constructive examples
        if constructive_examples:
            report += f"### Constructive Samples ({len(constructive_examples)} shown)\n\n"
            for i, example in enumerate(constructive_examples, 1):
                report += f"#### Constructive Example {i}\n\n"
                report += f"**Question**: {example['question']}\n\n"
                report += f"**Answer**: {example['answer']}\n\n"
                report += f"**Critique**: {example['critique']}\n\n"
                report += f"**Rationale**: {example.get('rationale', 'N/A')}\n\n"
                report += f"**Classification**: {example['label']}\n\n"
                report += "---\n\n"
    
    # All samples in sequence
    report += "## All Samples (Complete Sequence)\n\n"
    for i, sample in enumerate(samples, 1):
        report += f"### Sample {i}/{total} - [{sample['label']}]\n\n"
        report += f"**Question**: {sample['question']}\n\n"
        report += f"**Answer**: {sample['answer']}\n\n"
        report += f"**Critique**: {sample['critique']}\n\n"
        
        # Add answer quality for MM-RLHF
        if is_mmrlhf and 'answer_quality' in sample:
            report += f"**Answer Quality**: {sample.get('answer_quality', 'N/A')}\n\n"
        
        report += f"**Rationale**: {sample.get('rationale', 'N/A')}\n\n"
        report += f"**Classification**: {sample['label']}\n\n"
        if sample['label'] == 'Unexpected':
            report += f"**Raw Response**: {sample.get('raw_response', 'N/A')}\n\n"
        report += "---\n\n"
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze critiques from OpenAI Self-Critique and MM-RLHF datasets"
    )
    parser.add_argument(
        '--dataset',
        choices=['openai_self_critique', 'openai_self_critique_summarization', 'openai_self_critique_qa', 'mm_rlhf'],
        required=True,
        help='Dataset to analyze'
    )
    parser.add_argument(
        '--sample_count',
        type=int,
        default=50,
        help='Number of samples to randomly select. Use -1 for full dataset (default: 50)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    args = parser.parse_args()
    
    # Set random seed
    random.seed(args.seed)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Generate run directory name based on whether we're sampling or using full dataset
    if args.sample_count == -1:
        run_dir = f"full_dataset_{timestamp}"
    else:
        run_dir = f"seed{args.seed}_{timestamp}"
    
    # Setup paths - assuming script runs from parent of other_datasets/
    base_dir = Path('other_datasets')
    
    # Determine task type and paths
    task_type = None
    if args.dataset == 'openai_self_critique_summarization':
        task_type = 'summarization'
        data_file = base_dir / 'openai_self_critique/dataset/critiques/test.jsonl'
        output_dir = base_dir / 'openai_self_critique/analysis' / 'summarization' / run_dir
        dataset_name = 'openai_self_critique'
    elif args.dataset == 'openai_self_critique_qa':
        task_type = 'qa'
        data_file = base_dir / 'openai_self_critique/dataset/critiques/test.jsonl'
        output_dir = base_dir / 'openai_self_critique/analysis' / 'qa' / run_dir
        dataset_name = 'openai_self_critique'
    elif args.dataset == 'openai_self_critique':
        # Run both summarization and QA separately
        print(f"\n{'='*80}")
        print("Running analysis for BOTH summarization and QA tasks")
        print(f"{'='*80}\n")
        
        for task in ['summarization', 'qa']:
            print(f"\n{'='*80}")
            print(f"Processing {task.upper()} task")
            print(f"{'='*80}\n")
            
            task_output_dir = base_dir / 'openai_self_critique/analysis' / task / run_dir
            task_output_dir.mkdir(parents=True, exist_ok=True)
            
            data_file = base_dir / 'openai_self_critique/dataset/critiques/test.jsonl'
            
            print(f"Loading {task} data from {data_file}...")
            samples, total_dataset_size, filtered_dataset_size = load_openai_data(
                data_file, args.sample_count, args.seed, task
            )
            print(f"✅ Total dataset size: {total_dataset_size} critique samples")
            print(f"✅ Filtered dataset size ({task}): {filtered_dataset_size} critique samples")
            print(f"✅ Loaded {len(samples)} samples for analysis")
            
            # Print examples
            print_examples(samples, num_examples=5)
            
            # Classify
            print(f"\n{'='*80}")
            print(f"Classifying {task} critiques with GPT-4o...")
            print(f"{'='*80}\n")
            
            for i, sample in enumerate(samples, 1):
                if i % 10 == 0:
                    print(f"Progress: {i}/{len(samples)}")
                
                label, rationale, raw_response = classify_critique(
                    sample['question'],
                    sample['answer'],
                    sample['critique']
                )
                sample['label'] = label
                sample['rationale'] = rationale
                sample['raw_response'] = raw_response
            
            print(f"✅ Classified all {len(samples)} samples\n")
            
            # Save sampled data
            sampled_data_path = task_output_dir / 'sampled_data.jsonl'
            with open(sampled_data_path, 'w', encoding='utf-8') as f:
                for sample in samples:
                    f.write(json.dumps(sample, ensure_ascii=False) + '\n')
            
            print(f"✅ Sampled data saved to: {sampled_data_path}")
            
            # Generate report
            report_path = task_output_dir / 'report.md'
            generate_report(
                'openai_self_critique',
                samples,
                args.seed,
                timestamp,
                report_path,
                total_dataset_size,
                filtered_dataset_size,
                task
            )
            
            # Print summary
            constructive = sum(1 for s in samples if s['label'] == 'Constructive')
            non_constructive = sum(1 for s in samples if s['label'] == 'Non-Constructive')
            unexpected = sum(1 for s in samples if s['label'] == 'Unexpected')
            
            print(f"\n{'='*80}")
            print(f"Summary for {task.upper()}:")
            print(f"{'='*80}")
            print(f"Constructive: {constructive} ({constructive/len(samples)*100:.2f}%)")
            print(f"Non-Constructive: {non_constructive} ({non_constructive/len(samples)*100:.2f}%)")
            print(f"Unexpected: {unexpected} ({unexpected/len(samples)*100:.2f}%)")
            print(f"{'='*80}\n")
        
        print(f"\n{'='*80}")
        print("✅ Completed analysis for both summarization and QA tasks!")
        print(f"{'='*80}\n")
        return
        
    else:  # mm_rlhf
        data_file = base_dir / 'mm_rlhf/data.jsonl'
        output_dir = base_dir / 'mm_rlhf/analysis' / run_dir
        dataset_name = 'mm_rlhf'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Analyzing {args.dataset} dataset")
    print(f"Sample count: {args.sample_count}")
    print(f"Random seed: {args.seed}")
    if task_type:
        print(f"Task type: {task_type}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*80}\n")
    
    # Load data
    print(f"Loading data from {data_file}...")
    if 'openai' in args.dataset:
        samples, total_dataset_size, filtered_dataset_size = load_openai_data(
            data_file, args.sample_count, args.seed, task_type
        )
        print(f"✅ Total dataset size: {total_dataset_size} critique samples")
        if task_type:
            print(f"✅ Filtered dataset size ({task_type}): {filtered_dataset_size} critique samples")
        print(f"✅ Loaded {len(samples)} samples for analysis")
    else:
        samples, total_dataset_size = load_mmrlhf_data(data_file, args.sample_count, args.seed)
        filtered_dataset_size = total_dataset_size
        print(f"✅ Total dataset size: {total_dataset_size} critique samples")
        print(f"✅ Loaded {len(samples)} samples for analysis")
    
    # Print examples
    print_examples(samples, num_examples=5)
    
    # Classify all samples
    print(f"\n{'='*80}")
    print("Classifying critiques with GPT-4o...")
    print(f"{'='*80}\n")
    
    # For MM-RLHF, do two-stage classification
    if dataset_name == 'mm_rlhf':
        print("Stage 1: Classifying answer quality (Good vs Needs Improvement)...")
        for i, sample in enumerate(samples, 1):
            if i % 10 == 0:
                print(f"Progress: {i}/{len(samples)}")
            
            quality = classify_answer_quality(sample['critique'])
            sample['answer_quality'] = quality
        
        print(f"\n✅ Completed answer quality classification")
        good_count = sum(1 for s in samples if s['answer_quality'] == 'Good')
        needs_improvement_count = sum(1 for s in samples if s['answer_quality'] == 'Needs Improvement')
        print(f"Good answers: {good_count}")
        print(f"Needs improvement: {needs_improvement_count}\n")
        
        print("Stage 2: Classifying constructiveness...")
    
    for i, sample in enumerate(samples, 1):
        if i % 10 == 0:
            print(f"Progress: {i}/{len(samples)}")
        
        label, rationale, raw_response = classify_critique(
            sample['question'],
            sample['answer'],
            sample['critique']
        )
        sample['label'] = label
        sample['rationale'] = rationale
        sample['raw_response'] = raw_response
    
    print(f"✅ Classified all {len(samples)} samples\n")
    
    # Save sampled data
    sampled_data_path = output_dir / 'sampled_data.jsonl'
    with open(sampled_data_path, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"✅ Sampled data saved to: {sampled_data_path}")
    
    # Generate report
    report_path = output_dir / 'report.md'
    generate_report(
        dataset_name,
        samples,
        args.seed,
        timestamp,
        report_path,
        total_dataset_size,
        filtered_dataset_size if task_type else None,
        task_type
    )
    
    # Print summary
    constructive = sum(1 for s in samples if s['label'] == 'Constructive')
    non_constructive = sum(1 for s in samples if s['label'] == 'Non-Constructive')
    unexpected = sum(1 for s in samples if s['label'] == 'Unexpected')
    
    print(f"\n{'='*80}")
    print("Summary:")
    print(f"{'='*80}")
    print(f"Constructive: {constructive} ({constructive/len(samples)*100:.2f}%)")
    print(f"Non-Constructive: {non_constructive} ({non_constructive/len(samples)*100:.2f}%)")
    print(f"Unexpected: {unexpected} ({unexpected/len(samples)*100:.2f}%)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()