# Zero-Shot Prompting

## Learning Objectives

- Define zero-shot prompting and understand when to use it
- Distinguish zero-shot from few-shot and multi-shot approaches
- Write effective zero-shot prompts for common data tasks
- Recognize the strengths and limitations of zero-shot prompting

## Why This Matters

Zero-shot prompting is the simplest and most common way to interact with LLMs. Every time you type a question into ChatGPT or ask Copilot for a code suggestion without providing examples, you are using zero-shot prompting. Mastering this technique is the foundation for all other prompt engineering strategies.

## The Concept

### What Is Zero-Shot Prompting?

Zero-shot prompting means asking a model to perform a task without providing any examples of the desired output. You rely entirely on the model's pre-trained knowledge and your clear description of the task.

```
Zero-shot: "Classify this text as positive, negative, or neutral: 
            'The data pipeline ran successfully with no errors.'"

Output: "Positive"
```

The model has never seen this specific text before, but it understands the classification task from its training.

### Zero-Shot vs Few-Shot vs Multi-Shot

| Approach | Examples Provided | When to Use |
| -------- | ----------------- | ----------- |
| Zero-shot | None | Simple, well-defined tasks |
| One-shot | 1 example | Tasks needing format clarification |
| Few-shot | 2-5 examples | Complex or domain-specific tasks |
| Multi-shot | Many examples | Highly specialized patterns |

### Writing Effective Zero-Shot Prompts

#### Technique 1: Clear Task Statement

Start with an explicit verb that defines the action:

```
"Summarize the following SQL query in plain English:
SELECT department, AVG(salary) 
FROM employees 
GROUP BY department 
HAVING AVG(salary) > 70000;"
```

#### Technique 2: Role Assignment

Assigning a role gives the model context about expertise level and perspective:

```
"You are a senior data engineer reviewing a junior developer's code.
Identify potential performance issues in this BigQuery query:
[query here]"
```

#### Technique 3: Output Specification

Define exactly what the output should look like:

```
"Convert the following CSV header into a BigQuery CREATE TABLE statement.
Use appropriate data types. Output only the SQL, no explanation.

Header: order_id,customer_name,order_date,total_amount,is_shipped"
```

### Zero-Shot Prompting for Data Tasks

#### Data Analysis

```
Prompt: "Analyze this error message from a failed ETL pipeline run 
         and suggest three possible root causes:
         
         ERROR: Null value in column 'customer_id' violates 
         not-null constraint on table 'dim_customer'"
```

#### SQL Generation

```
Prompt: "Write a BigQuery SQL query that finds the top 10 customers 
         by total purchase amount in the last 30 days. The orders 
         table has columns: order_id, customer_id, order_date, 
         total_amount. Use CURRENT_DATE() for today."
```

#### Documentation

```
Prompt: "Write a one-paragraph description for a data dictionary 
         entry for a column called 'churn_risk_score' in a 
         customer analytics table. It contains values from 0 to 100."
```

### When Zero-Shot Falls Short

Zero-shot prompting may produce suboptimal results when:

- The task requires a very specific output format the model has not commonly seen
- The domain is highly specialized (medical, legal, financial regulations)
- The task involves applying custom business rules
- Precision and consistency are critical

In these cases, providing examples (few-shot prompting) or additional constraints will improve results.

## Key Takeaways

- Zero-shot prompting gives instructions without examples
- It works best for well-defined tasks that rely on common knowledge
- Clear verbs, role assignment, and output specification improve zero-shot results
- When zero-shot is insufficient, escalate to few-shot prompting

## Additional Resources

- [Prompt Engineering Guide - Zero-Shot](https://www.promptingguide.ai/techniques/zeroshot)
- [OpenAI Cookbook - Techniques to Improve Reliability](https://cookbook.openai.com/articles/techniques_to_improve_reliability)
- [Google Cloud - Prompt Design Strategies](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
