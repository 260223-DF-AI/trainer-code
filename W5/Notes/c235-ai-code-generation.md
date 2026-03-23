# AI-Assisted Code Generation

## Learning Objectives

- Apply AI tools effectively for code generation tasks
- Understand the workflow for generating, reviewing, and refining AI-produced code
- Use best practices to improve the quality of generated code
- Recognize common issues in AI-generated code and how to fix them

## Why This Matters

Code generation is the most impactful daily use case for AI tools. When done well, it can cut development time significantly for routine tasks. When done poorly, it creates technical debt and introduces bugs. This topic teaches you how to generate code effectively and, critically, how to review and refine it.

## The Concept

### The Code Generation Workflow

AI code generation is not a one-step process:

```
1. PROMPT     -->  Write a clear, specific request
2. GENERATE   -->  AI produces code
3. REVIEW     -->  Read and understand every line
4. TEST       -->  Run the code, verify behavior
5. REFINE     -->  Iterate or modify as needed
6. INTEGRATE  -->  Add to your codebase with proper context
```

Skipping any step increases risk. Steps 3 and 4 are where most shortcuts lead to problems.

### Effective Code Generation Prompts

#### Pattern: Full Specification

```
"Write a Python function called `validate_email` that:
- Takes a string parameter `email`
- Returns True if the email matches a valid format
- Uses the re module for regex matching
- Validates: contains @, has domain with dot, 
  no spaces, alphanumeric local part
- Include a docstring with examples
- Include type hints"
```

#### Pattern: Schema-Driven Generation

```
"Given this BigQuery table schema:
  orders (
    order_id INT64,
    customer_id INT64,
    order_date DATE,
    product_id INT64,
    quantity INT64,
    unit_price NUMERIC
  )

Write SQL queries for:
1. Total revenue per customer
2. Monthly revenue trend
3. Top 5 products by units sold
4. Average order value by day of week"
```

#### Pattern: Transform Existing Code

```
"Convert this SQL query to a pandas equivalent:

SELECT customer_id, 
       COUNT(*) as order_count,
       SUM(total_amount) as total_spent
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 5
ORDER BY total_spent DESC"
```

### Reviewing AI-Generated Code

Use this checklist for every piece of AI-generated code:

```
Correctness:
[ ] Does it do what was requested?
[ ] Are edge cases handled (nulls, empty inputs, large data)?
[ ] Are error messages useful and not exposing internals?

Security:
[ ] No hardcoded credentials?
[ ] Input validation present?
[ ] SQL injection prevention (parameterized queries)?
[ ] No overly permissive access?

Style:
[ ] Follows team coding standards?
[ ] Variable names are meaningful?
[ ] Functions are appropriately sized?
[ ] Comments add value (not restating the code)?

Performance:
[ ] No unnecessary loops or redundant operations?
[ ] Efficient data structures used?
[ ] Database queries optimized?
[ ] No N+1 query patterns?

Dependencies:
[ ] Libraries are correct version?
[ ] No unnecessary imports?
[ ] APIs used correctly per current docs?
```

### Common Issues in AI-Generated Code

#### Issue 1: Outdated API Usage

```python
# AI may generate (deprecated):
from google.cloud import bigquery
job = client.run_async_query("my_job", query)

# Correct modern API:
from google.cloud import bigquery
job = client.query(query)
result = job.result()
```

Always verify against the latest documentation.

#### Issue 2: Missing Error Handling

```python
# AI often generates the happy path:
def load_csv(file_path):
    return pd.read_csv(file_path)

# You should add:
def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file with error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )
        df = pd.read_csv(file_path)
        if df.empty:
            logger.warning(f"Empty file: {file_path}")
        return df
    except pd.errors.ParserError as e:
        logger.error(f"Parse error in {file_path}: {e}")
        raise
```

#### Issue 3: Incorrect Assumptions

```sql
-- AI may assume column names or data types:
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month
FROM orders;

-- But BigQuery uses FORMAT_DATE:
SELECT FORMAT_DATE('%Y-%m', order_date) AS month
FROM orders;
```

Always verify syntax matches your specific database or language version.

### Iterating on Generated Code

When the first generation is not quite right:

```
"The function you generated works but has two issues:
1. It does not handle null values in the 'email' column
2. The date parsing assumes MM/DD/YYYY but our data uses 
   YYYY-MM-DD format

Please update the function to fix these issues."
```

Be specific about what needs to change rather than regenerating from scratch.

## Key Takeaways

- Code generation follows a workflow: prompt, generate, review, test, refine, integrate
- Specific prompts with clear specifications produce better code
- Review every line of AI-generated code -- do not accept blindly
- Common issues include outdated APIs, missing error handling, and incorrect assumptions
- Iterate with specific feedback rather than regenerating from scratch

## Additional Resources

- [GitHub Copilot - Code Suggestions](https://docs.github.com/en/copilot/using-github-copilot/getting-code-suggestions-in-your-ide-with-github-copilot)
- [Google - AI-Assisted Coding Best Practices](https://cloud.google.com/blog/products/ai-machine-learning/)
- [ACM - Productivity Assessment of AI Coding Assistants](https://dl.acm.org/doi/10.1145/3597503.3639187)
