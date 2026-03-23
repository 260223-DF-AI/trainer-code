# Understanding AI Hallucinations

## Learning Objectives

- Define AI hallucinations and understand why they occur
- Identify common types of hallucinations
- Apply detection strategies to verify AI outputs
- Implement mitigation techniques to reduce hallucination risk

## Why This Matters

AI hallucinations are one of the most significant risks when using LLMs professionally. A model can generate SQL that looks correct but produces wrong results. It can cite documentation that does not exist. It can describe API features that were never implemented. For data professionals, where accuracy is paramount, understanding and detecting hallucinations is not optional -- it is a core competency.

## The Concept

### What Are AI Hallucinations?

An AI hallucination occurs when a model generates content that is factually incorrect, fabricated, or inconsistent with reality, while presenting it with the same confidence as accurate information.

The term "hallucination" is borrowed from psychology: the model perceives (generates) things that are not there. It is important to understand that the model is not lying intentionally. It is generating statistically probable text based on patterns, and sometimes those patterns lead to fabricated content.

### Why Hallucinations Happen

LLMs predict the next token based on probability. They do not verify facts or check sources. Several factors contribute:

| Factor | Description |
| ------ | ----------- |
| **Statistical generation** | The model generates probable text, not verified facts |
| **Training data gaps** | Topics with limited training data produce less reliable outputs |
| **Training data cutoff** | The model does not know about events after its training date |
| **Overconfidence** | The model presents uncertain outputs with high confidence |
| **Pattern completion** | The model fills gaps by completing patterns, even with fabricated details |

### Common Types of Hallucinations

#### Factual Hallucinations

The model states something as fact that is incorrect:

```
Prompt: "What SQL function does BigQuery use for 
         regular expressions?"
Hallucinated Response: "BigQuery uses REGEX_EXTRACT()"
Correct Answer: "BigQuery uses REGEXP_EXTRACT()"
```

Small but significant differences that can break real code.

#### Citation Hallucinations

The model invents sources that do not exist:

```
Prompt: "Cite the research paper that introduced 
         the Star Schema concept"
Hallucinated Response: "Smith, J. (1995). 'Star Schema 
Design Patterns.' Journal of Data Warehousing, 12(3)."
Reality: This paper does not exist. The concept was 
popularized by Ralph Kimball in "The Data Warehouse 
Toolkit" (1996).
```

#### API and Syntax Hallucinations

The model creates function signatures or parameters that do not exist:

```
Prompt: "How do I set a partition expiration in BigQuery?"
Hallucinated Response: "Use ALTER TABLE SET OPTIONS(
         partition_expiration=30)"
Reality: The correct syntax is 
         "partition_expiration_days = 30"
```

#### Logical Hallucinations

The model produces reasoning that sounds correct but contains flaws:

```
Prompt: "If Table A has 100 rows and Table B has 50 rows, 
         how many rows does an INNER JOIN produce?"
Hallucinated Response: "An inner join produces 5,000 rows"
Reality: The result depends on the join condition and 
matching rows. It could be 0 to 5,000 rows.
```

### Detection Strategies

#### 1. Verify Against Documentation

Always cross-reference AI-generated syntax, function names, and API calls against official documentation.

#### 2. Test the Code

Never deploy AI-generated code without running it:

```
Step 1: AI generates SQL query
Step 2: Run a dry run in BigQuery (check syntax)
Step 3: Run on a small sample dataset
Step 4: Validate results against known answers
Step 5: Deploy to production only after validation
```

#### 3. Check for Overconfidence Signals

Be skeptical when the model:

- Provides very specific numbers without showing calculations
- Claims something is "always" or "never" the case
- Cites specific papers, versions, or dates without prompting
- Provides suspiciously detailed historical accounts

#### 4. Ask for Sources

```
Prompt: "Provide the BigQuery documentation URL for 
         partition pruning"
```

If the model provides a URL, verify it actually exists before trusting it.

#### 5. Use Self-Verification Prompts

Ask the model to check its own work:

```
"Review the SQL query you just generated. Are there 
any syntax errors, logical issues, or BigQuery-specific 
concerns?"
```

This does not eliminate hallucinations but can catch some errors.

### Mitigation Techniques

1. **Provide reference material** -- include documentation snippets in your prompt
2. **Use few-shot examples** -- show correct examples to anchor the model
3. **Constrain the output** -- limit scope to reduce opportunity for fabrication
4. **Require citations** -- ask the model to cite its reasoning
5. **Implement human review** -- never skip manual verification for critical outputs
6. **Use RAG (Retrieval-Augmented Generation)** -- ground model responses in actual data

## Key Takeaways

- Hallucinations are fabricated outputs presented as facts
- They occur because LLMs generate probable text, not verified truth
- Common hallucination types include factual, citation, syntax, and logical errors
- Detection requires verification against authoritative sources and testing
- Mitigation combines prompt design, constraints, and human review

## Additional Resources

- [Anthropic - Reducing Hallucinations](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/reduce-hallucinations)
- [Google - Grounding AI Responses](https://cloud.google.com/vertex-ai/docs/generative-ai/grounding/overview)
- [OpenAI - Safety Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
