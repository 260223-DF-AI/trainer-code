# Prompt Constraints

## Learning Objectives

- Understand how constraints shape AI output
- Apply constraints for format, length, tone, and scope
- Use negative constraints to exclude unwanted behavior
- Combine multiple constraints for precise control

## Why This Matters

Without constraints, LLM outputs tend to be verbose, generic, and unpredictable in format. Constraints transform an AI from an unfocused assistant into a precision tool. For data professionals who need consistent, structured outputs -- SQL in a specific dialect, documentation in a specific format, analysis at a specific depth -- constraints are essential.

## The Concept

### What Are Prompt Constraints?

Constraints are explicit rules or boundaries you include in a prompt to control the model's output. They narrow the space of possible responses, making outputs more predictable and useful.

### Types of Constraints

#### Format Constraints

Control the structure of the output:

```
"List the results as a markdown table with columns: 
Metric Name, Value, Status"

"Return only valid JSON with the following structure:
{
  'table_name': string,
  'columns': [{'name': string, 'type': string}]
}"

"Format the output as a numbered list with no more 
than 5 items"
```

#### Length Constraints

Control the volume of output:

```
"Explain data normalization in exactly 3 sentences."

"Provide a summary of no more than 100 words."

"Write a one-paragraph description."
```

#### Tone and Style Constraints

Control the voice and register:

```
"Explain this concept as if talking to a junior developer 
who has completed SQL training but has no cloud experience."

"Use a professional, technical tone suitable for 
documentation."

"Avoid jargon. Use plain language."
```

#### Scope Constraints

Limit what the model should and should not cover:

```
"Focus only on BigQuery. Do not mention other cloud 
data warehouses."

"Cover only the extraction phase of ETL. Do not discuss 
transformation or loading."

"Answer based solely on the information provided below. 
Do not use outside knowledge."
```

#### Negative Constraints

Explicitly state what to avoid:

```
"Do not include any code examples."

"Do not suggest deprecated methods."

"Do not reference paid tools or services."

"Do not make assumptions about the user's operating system."
```

### Combining Constraints

The most effective prompts layer multiple constraint types:

```
"You are a BigQuery expert.

Task: Write a query that calculates monthly revenue by product 
category for 2024.

Constraints:
- Use standard SQL (not legacy SQL)
- Use the table: project.dataset.sales
- Include comments explaining each section
- Do not use subqueries; use CTEs instead
- Output only the SQL query, no explanation
- The query must be under 30 lines"
```

### Constraints in Practice: Data Engineering Examples

#### Generating DDL

```
"Generate a BigQuery CREATE TABLE statement for a customer 
dimension table. 

Constraints:
- Include at least 8 columns
- Use appropriate BigQuery data types
- Add a surrogate key column named customer_key
- Partition by signup_date
- Cluster by loyalty_tier
- Include column descriptions using OPTIONS"
```

#### Code Review

```
"Review the following Python function for data quality issues.

Constraints:
- Focus only on data validation concerns
- Ignore code style and formatting
- List findings as bullet points
- Rate severity as LOW, MEDIUM, or HIGH
- Limit response to 5 findings maximum"
```

### Common Mistakes with Constraints

| Mistake | Problem | Fix |
| ------- | ------- | --- |
| Too few constraints | Output is unpredictable | Add format and scope constraints |
| Contradictory constraints | Model picks one, ignores the other | Review for logical consistency |
| Over-constraining | Model cannot satisfy all constraints | Prioritize the most important ones |
| Vague constraints | "Keep it short" is subjective | "No more than 100 words" is measurable |

## Key Takeaways

- Constraints are the most powerful tool for controlling AI output
- The five constraint types are: format, length, tone, scope, and negative
- Layering multiple constraints produces precise, predictable results
- Make constraints measurable and specific rather than vague

## Additional Resources

- [Anthropic - Prompt Engineering: Be Specific](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
- [OpenAI - Best Practices for Prompt Engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Google - Improving Prompt Quality](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
