# Fine-Tuning and Conditioning

## Learning Objectives

- Understand few-shot prompting and chain-of-thought reasoning
- Distinguish between prompt conditioning and model fine-tuning
- Apply few-shot patterns to improve output quality
- Use chain-of-thought prompting for complex reasoning tasks

## Why This Matters

When zero-shot prompting does not produce the quality or consistency you need, conditioning techniques let you teach the model through examples within the prompt itself. These techniques are especially valuable for data tasks that require specific formatting, domain terminology, or multi-step reasoning -- all common in data engineering.

## The Concept

### Few-Shot Prompting

Few-shot prompting provides examples of desired input-output pairs before asking the model to process new input. The model uses these examples to infer the pattern.

#### One-Shot Example

```
Convert column names from camelCase to snake_case.

Example:
Input: customerFirstName
Output: customer_first_name

Now convert:
Input: orderTotalAmount
```

The model sees the pattern and produces: `order_total_amount`

#### Few-Shot Example

```
Classify these SQL operations by their sublanguage:

Example 1:
Statement: CREATE TABLE users (id INT)
Classification: DDL

Example 2:
Statement: INSERT INTO users VALUES (1, 'John')
Classification: DML

Example 3:
Statement: SELECT * FROM users
Classification: DQL

Now classify:
Statement: DROP INDEX idx_users_email
```

By providing three examples, the model learns the classification pattern and correctly identifies this as DDL.

### Chain-of-Thought Prompting

Chain-of-thought prompting asks the model to show its reasoning step by step before arriving at an answer. This dramatically improves accuracy for complex tasks.

#### Without Chain-of-Thought

```
Prompt: "A data pipeline runs every 6 hours. If it processes 
         150,000 rows per run and each row is 2KB, how much 
         data does it process per day?"

Response: "1.2 million rows, 2.4 GB" 
          (may be correct but reasoning is hidden)
```

#### With Chain-of-Thought

```
Prompt: "A data pipeline runs every 6 hours. If it processes 
         150,000 rows per run and each row is 2KB, how much 
         data does it process per day?
         
         Think through this step by step."

Response:
"Step 1: Runs per day = 24 hours / 6 hours = 4 runs
Step 2: Total rows = 4 runs x 150,000 rows = 600,000 rows
Step 3: Data per day = 600,000 rows x 2 KB = 1,200,000 KB
Step 4: Convert to GB = 1,200,000 KB / 1,000,000 = 1.2 GB

Answer: 600,000 rows and approximately 1.2 GB per day."
```

The reasoning is transparent and verifiable.

### Prompt Conditioning vs Model Fine-Tuning

These are two different approaches to customizing model behavior:

| Aspect | Prompt Conditioning | Model Fine-Tuning |
| ------ | ------------------- | ----------------- |
| How | Add examples/instructions in the prompt | Retrain the model on custom data |
| Cost | Free (just prompt design) | Expensive (compute resources) |
| Speed | Immediate | Hours to days of training |
| Persistence | Per-conversation only | Permanent model changes |
| Skill needed | Prompt engineering | ML engineering |
| Best for | Most use cases | Domain-specific, high-volume tasks |

For most data professionals, prompt conditioning is sufficient. Fine-tuning is typically done by ML engineering teams for production applications.

### System Prompts

Many LLM interfaces support system prompts (also called system messages) that set the overall behavior for the entire conversation:

```
System Prompt:
"You are a BigQuery SQL expert. All queries you write must use 
standard SQL syntax. Always include comments. When you encounter 
ambiguity, ask clarifying questions rather than making assumptions."

User Prompt:
"Write a query to find duplicate records in a customer table."
```

The system prompt acts as permanent conditioning for the conversation.

### Practical Patterns for Data Work

#### Pattern: Format Enforcement with Examples

```
Generate a data dictionary entry for each column.

Example:
Column: order_date
Type: DATE
Description: The date the order was placed by the customer
Nullable: No
Example Value: 2024-01-15

Now generate entries for: customer_id, total_amount, ship_status
```

#### Pattern: Step-by-Step Analysis

```
Analyze this ETL pipeline failure. Think through each step:

1. What is the error message saying?
2. What are the possible root causes?
3. What information would you need to diagnose further?
4. What is the most likely fix?

Error: "BigQuery job failed: Table not found: 
project.staging.customer_raw"
```

## Key Takeaways

- Few-shot prompting uses examples to teach the model desired patterns
- Chain-of-thought prompting improves accuracy by requiring step-by-step reasoning
- Prompt conditioning is practical and free; fine-tuning is for specialized, high-volume needs
- System prompts set persistent behavior for entire conversations

## Additional Resources

- [Google Research - Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Prompt Engineering Guide - Few-Shot Prompting](https://www.promptingguide.ai/techniques/fewshot)
- [OpenAI - Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
