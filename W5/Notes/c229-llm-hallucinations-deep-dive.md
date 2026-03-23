# LLM Hallucinations: Deep Dive

## Learning Objectives

- Analyze why specific types of hallucinations occur in LLMs
- Understand grounding techniques that reduce hallucination risk
- Explore Retrieval-Augmented Generation (RAG) at a conceptual level
- Build a systematic approach to validating LLM outputs

## Why This Matters

Monday introduced the concept of AI hallucinations. Today we go deeper. As you begin using LLMs for real work -- generating SQL, writing documentation, analyzing data patterns -- you need practical strategies for catching and preventing hallucinations. This is especially critical for data professionals, where an incorrect SQL query or fabricated statistic can lead to flawed business decisions.

## The Concept

### Why LLMs Hallucinate: A Deeper Look

LLMs generate text by predicting the most probable next token. This mechanism creates several hallucination patterns:

#### Pattern 1: Plausible Completion

The model completes a pattern it has seen in training, even if the specific completion is fictional:

```
Prompt: "List the configuration options for BigQuery 
         partitioning"

Risk: The model may generate plausible-sounding options 
that do not actually exist in BigQuery, because it has 
seen similar option patterns in documentation for other 
databases.
```

#### Pattern 2: Training Data Conflicts

When training data contains contradictory information, the model may blend sources:

```
Prompt: "What is the maximum context window for Claude?"

Risk: The answer depends on which version and when the 
training data was collected. The model may cite an 
outdated number or mix values from different versions.
```

#### Pattern 3: Confident Gap-Filling

When the model lacks specific knowledge, it fills gaps with plausible-sounding content rather than admitting uncertainty:

```
Prompt: "What Python library does BigQuery use for 
         streaming inserts with exactly-once semantics?"

Risk: The model may invent a library name or attribute 
a feature to a library that does not support it.
```

### Grounding Techniques

Grounding connects LLM responses to verifiable information sources, reducing hallucination risk.

#### Technique 1: Provide Source Material

Include the actual documentation or data in your prompt:

```
"Based ONLY on the following BigQuery documentation, 
answer the question.

Documentation:
[paste relevant documentation section]

Question: What partition types does BigQuery support?"
```

This constrains the model to the provided text rather than its training data.

#### Technique 2: Require Citations

Ask the model to cite where in the provided text it found each claim:

```
"For each statement in your response, indicate which 
paragraph of the provided documentation supports it. 
If a statement is not supported by the provided text, 
clearly mark it as [INFERENCE]."
```

#### Technique 3: Ask for Confidence Levels

```
"For each recommendation, indicate your confidence level:
- HIGH: Well-documented, widely accepted practice
- MEDIUM: Generally accepted but may vary by context
- LOW: Based on limited information, verify before using"
```

### Retrieval-Augmented Generation (RAG)

RAG is an architecture that reduces hallucinations by connecting LLMs to external knowledge bases.

```
Traditional LLM:
  User Question --> LLM --> Answer (from training data only)

RAG Architecture:
  User Question --> Retrieval System --> Relevant Documents
                         |
                         v
                    LLM + Documents --> Grounded Answer
```

#### How RAG Works

1. **Indexing**: Documents are processed and stored in a vector database
2. **Retrieval**: When a user asks a question, similar documents are retrieved
3. **Augmentation**: Retrieved documents are added to the prompt
4. **Generation**: The LLM generates a response grounded in the retrieved documents

#### RAG Example

```
Without RAG:
Q: "What is our company's data retention policy?"
A: [Hallucinated generic policy]

With RAG:
Q: "What is our company's data retention policy?"
System: [Retrieves internal policy document]
A: "According to the Data Governance Policy (v3.2, 
    Section 4.1), data is retained for 7 years for 
    financial records and 3 years for operational data."
```

RAG is a production architecture pattern. As data engineers, you may be asked to build or maintain the data pipeline that feeds a RAG system.

### Systematic Validation Framework

Build a validation workflow for LLM outputs:

```
Step 1: Generate
  AI produces output (code, documentation, analysis)

Step 2: Syntax Check
  Does the code compile? Is the SQL valid?

Step 3: Logic Check
  Does the logic match the requirements?
  Are there edge cases not handled?

Step 4: Reference Check
  Do cited sources exist?
  Are function names and parameters correct?
  Are version-specific features accurate?

Step 5: Test
  Run the code on sample data
  Compare results to known correct answers

Step 6: Peer Review
  Have another team member review
  Fresh eyes catch different issues
```

### Hallucination Risk by Task Type

| Task Type | Hallucination Risk | Mitigation |
| --------- | ------------------ | ---------- |
| Code generation | Medium | Test all generated code |
| SQL queries | Medium | Run against test data first |
| Factual Q&A | High | Cross-reference documentation |
| Documentation | Low-Medium | Review for accuracy |
| Brainstorming | Low (by design) | Creativity is the goal |
| Data analysis | High | Verify calculations independently |

## Key Takeaways

- Hallucinations occur due to pattern completion, training data conflicts, and confident gap-filling
- Grounding techniques (providing source material, requiring citations) reduce hallucination risk
- RAG connects LLMs to external knowledge bases for more accurate responses
- Systematic validation (syntax, logic, reference, test, review) is essential for professional use
- Different task types carry different hallucination risks

## Additional Resources

- [Google Cloud - Grounding with RAG](https://cloud.google.com/vertex-ai/docs/generative-ai/grounding/overview)
- [LangChain - RAG Documentation](https://python.langchain.com/docs/tutorials/rag/)
- [Anthropic - Reducing Hallucinations](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/reduce-hallucinations)
