# Exercise: Prompt Engineering Lab

## Exercise ID: e021

## Overview

In this hands-on lab, you will practice prompt engineering techniques learned today. You will work through progressively complex challenges, applying zero-shot, few-shot, and chain-of-thought prompting patterns to solve data engineering tasks.

## Learning Objectives

- Apply zero-shot prompting for simple, well-defined tasks
- Use few-shot prompting to teach the model domain-specific patterns
- Implement chain-of-thought prompting for multi-step reasoning
- Apply prompt constraints to control output quality

## Prerequisites

- Access to an LLM (ChatGPT, Claude, Gemini, or similar)
- Completed Monday written content on prompt engineering

## Time Estimate

45-60 minutes

---

## Part 1: Zero-Shot Prompting (15 minutes)

### Challenge 1.1: SQL Generation

Using only zero-shot prompting (no examples), write a prompt that generates a BigQuery SQL query to:

- Find the top 5 departments by average salary
- Include the department name, average salary, and employee count
- Only include departments with more than 10 employees
- Order by average salary descending

**Your Task:**

1. Write your prompt
2. Submit it to the LLM
3. Evaluate the output -- does it produce valid BigQuery SQL?
4. If not, refine your prompt and try again
5. Document your original prompt, your refined prompt (if needed), and the final output

### Challenge 1.2: Error Explanation

Write a zero-shot prompt that asks the LLM to explain this error message in plain English and suggest a fix:

```
google.api_core.exceptions.BadRequest: 400 Syntax error: 
Expected end of input but got keyword SELECT at [3:1]
```

**Your Task:**

1. Craft a prompt that provides enough context for a useful explanation
2. Evaluate whether the explanation is accurate
3. Rate the quality of the fix suggestion (1-5 scale)

### Challenge 1.3: Data Dictionary Entry

Write a zero-shot prompt to generate a data dictionary entry for a column called `customer_lifetime_value` in a `dim_customer` table. The entry should include: data type, description, business definition, calculation method, and example values.

**Your Task:**

1. Write the prompt
2. Evaluate whether the output would be useful for a new team member
3. Note what additional context you would need to add to make it more accurate

---

## Part 2: Few-Shot Prompting (15 minutes)

### Challenge 2.1: Column Name Standardization

You need the LLM to convert column names from various formats to snake_case following your team's convention.

**Provide these examples in your prompt:**

- `CustomerFirstName` -> `customer_first_name`
- `order-total-amount` -> `order_total_amount`
- `PRODUCT ID` -> `product_id`

**Then ask it to convert:**

- `ShippingAddress Line1`
- `total_Revenue_YTD`
- `customerEmailAddress`
- `ORDER__STATUS__CODE`

**Your Task:**

1. Write the few-shot prompt with the 3 examples
2. Submit and evaluate: did it follow the pattern correctly for all 4 inputs?
3. Were there any the model struggled with? Why?

### Challenge 2.2: SQL to Documentation

Teach the model to generate documentation from SQL using examples.

**Provide this example:**

Input:

```sql
SELECT customer_id, COUNT(*) as order_count 
FROM orders GROUP BY customer_id
```

Output:

```
Query: Customer Order Count
Purpose: Counts the total number of orders per customer
Tables Used: orders
Output Columns: customer_id, order_count
Aggregation: COUNT grouped by customer_id
```

**Then ask it to document this query:**

```sql
SELECT p.category, 
       DATE_TRUNC(o.order_date, MONTH) as month,
       SUM(o.quantity * p.unit_price) as revenue,
       COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2
```

**Your Task:**

1. Write the prompt with the example
2. Evaluate: did the model follow the documentation format?
3. Is the documentation accurate?

---

## Part 3: Chain-of-Thought Prompting (15 minutes)

### Challenge 3.1: Cost Estimation

Use chain-of-thought prompting to have the LLM estimate BigQuery costs:

**Scenario:**

- You have a table with 500 million rows, each row is approximately 500 bytes
- You run a query that scans 3 columns (out of 20 total columns)
- The query runs 4 times per day
- BigQuery charges $6.25 per TB scanned
- Assume columnar storage distributes data evenly across columns

**Your Task:**

1. Write a prompt that includes "Think through this step by step"
2. Verify each step of the model's calculation
3. Is the final answer reasonable?
4. Did chain-of-thought improve accuracy compared to a direct question?

### Challenge 3.2: Pipeline Debugging

Use chain-of-thought prompting to diagnose this pipeline issue:

**Scenario:**
An ETL pipeline extracts data from a REST API, transforms it with Python, and loads it into BigQuery. The pipeline ran successfully for 30 days, then suddenly started failing with this error:

```
google.api_core.exceptions.Forbidden: 403 Access Denied: 
BigQuery BigQuery: Permission bigquery.tables.create denied
```

Nothing in the pipeline code changed. The GCP project and service account are the same.

**Your Task:**

1. Write a chain-of-thought prompt asking the LLM to reason through possible causes
2. Evaluate the reasoning: are the steps logical?
3. Which root cause does the model identify as most likely?
4. Do you agree? What would you check first?

---

## Part 4: Constraint Application (Optional, 10 minutes)

### Challenge 4.1: Constrained Output

Write a prompt that generates a Python function with ALL of these constraints:

- Function name: `validate_order_data`
- Input: pandas DataFrame
- Must check for: null values, negative amounts, future dates, duplicate IDs
- Output: a dictionary with check results
- Maximum 30 lines of code
- Must include type hints
- Must include a docstring
- No external libraries beyond pandas and datetime

**Your Task:**

1. Write the prompt with all constraints
2. Did the model satisfy ALL constraints?
3. Which constraints were hardest for the model to follow?

---

## Submission

For each challenge, document:

1. Your prompt (original and refined versions)
2. The LLM's output
3. Your evaluation of the output quality (1-5 scale)
4. What you learned about prompting from that challenge

## Reflection Questions

1. Which prompting technique (zero-shot, few-shot, chain-of-thought) produced the best results for data engineering tasks?
2. What made the biggest difference in output quality: specificity, examples, or constraints?
3. When would you choose each technique in your daily work?
