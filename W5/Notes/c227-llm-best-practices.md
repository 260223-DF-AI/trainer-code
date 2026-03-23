# LLM Best Practices

## Learning Objectives

- Apply proven patterns for interacting with LLMs effectively
- Structure prompts for consistent, high-quality outputs
- Implement output validation and iteration workflows
- Avoid common pitfalls that reduce LLM effectiveness

## Why This Matters

The difference between a productive AI-assisted developer and a frustrated one often comes down to how they interact with the model. Best practices transform LLMs from unpredictable novelties into reliable productivity tools. These patterns apply regardless of which specific model you use.

## The Concept

### Best Practice 1: Start Simple, Then Iterate

Begin with a simple prompt and refine based on the output:

```
Iteration 1:
"Write a SQL query to find top customers"

  --> Too vague, model makes assumptions

Iteration 2:
"Write a BigQuery SQL query to find the top 10 customers 
by total purchase amount in the orders table"

  --> Better, but missing schema details

Iteration 3:
"Write a BigQuery SQL query to find the top 10 customers 
by total purchase amount.
Table: project.analytics.orders
Columns: order_id (INT64), customer_id (INT64), 
         order_date (DATE), total_amount (NUMERIC)
Sort descending. Include customer_id and total."

  --> Clear, specific, actionable
```

### Best Practice 2: Use Structured Prompts

Organize complex prompts with clear sections:

```
## Context
I am building an ETL pipeline in Python that loads 
daily sales data from CSV files into BigQuery.

## Task
Write the transformation function that:
1. Removes duplicate rows based on order_id
2. Converts date strings (MM/DD/YYYY) to DATE objects
3. Validates that total_amount is positive
4. Adds a processed_timestamp column

## Constraints
- Use pandas
- Input is a DataFrame with columns: order_id, 
  order_date, customer_id, total_amount
- Return the cleaned DataFrame
- Log the number of rows removed at each step

## Output Format
Python function with docstring and type hints
```

### Best Practice 3: Validate Everything

Never trust AI output without verification:

```
Validation Checklist:
[ ] Does the code syntax compile/run?
[ ] Does the logic match what was requested?
[ ] Are edge cases handled?
[ ] Are there security vulnerabilities?
[ ] Does it use the correct library versions?
[ ] Are the function/variable names appropriate?
```

### Best Practice 4: Provide Reference Material

When working with specific APIs or schemas, include the relevant documentation:

```
"Using the BigQuery Python client library, write code 
to create a partitioned table.

Reference (from the official docs):
- Use bigquery.Client() for connection
- Use bigquery.Table() for table reference
- TimePartitioning() for partition config
- table.time_partitioning = TimePartitioning(
      type_=TimePartitioningType.DAY,
      field='date_column'
  )"
```

This grounds the model in actual documentation rather than potentially outdated training data.

### Best Practice 5: Break Complex Tasks into Steps

Do not ask an LLM to build an entire system in one prompt:

```
Bad approach:
"Build a complete ETL pipeline with error handling, 
logging, scheduling, and monitoring."

Good approach:
Step 1: "Design the pipeline architecture 
         (components and data flow)"
Step 2: "Write the extraction module"
Step 3: "Write the transformation module"
Step 4: "Write the loading module"
Step 5: "Add error handling to each module"
Step 6: "Add logging throughout"
```

### Best Practice 6: Specify What You Do NOT Want

Negative instructions can be as important as positive ones:

```
"Generate a SQL query for customer analysis.

Do NOT:
- Use subqueries (use CTEs instead)
- Use SELECT * (specify columns explicitly)
- Use legacy SQL syntax
- Include any comments about the query
- Wrap the output in explanatory text"
```

### Best Practice 7: Use Temperature Appropriately

Most AI interfaces allow you to adjust "temperature":

| Temperature | Behavior | Best For |
| ----------- | -------- | -------- |
| 0.0-0.3 | Deterministic, consistent | Code generation, SQL, factual Q&A |
| 0.4-0.7 | Balanced | General writing, analysis |
| 0.8-1.0 | Creative, varied | Brainstorming, creative content |

For data engineering tasks, lower temperatures generally produce more reliable results.

### Common Pitfalls to Avoid

| Pitfall | Problem | Solution |
| ------- | ------- | -------- |
| Blind trust | Deploying AI code without testing | Always test and review |
| Prompt fatigue | Accepting poor output instead of iterating | Refine until quality is acceptable |
| Context overflow | Pasting entire codebases | Share only relevant sections |
| Version assumptions | AI suggests deprecated syntax | Specify your tool versions |
| One-and-done | Using a single prompt for complex tasks | Break into steps |

## Key Takeaways

- Start simple and iterate rather than crafting perfect prompts immediately
- Structure complex prompts with clear sections
- Always validate AI output before using it
- Include reference material to ground responses in current documentation
- Break complex tasks into manageable steps

## Additional Resources

- [Anthropic - Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [OpenAI - Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google - Prompt Design Best Practices](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
