# AI-Assisted Debugging

## Learning Objectives

- Use AI tools to diagnose and fix code errors efficiently
- Apply structured debugging prompts for consistent results
- Understand how AI interprets error messages and stack traces
- Build a debugging workflow that combines AI speed with human judgment

## Why This Matters

Debugging is where developers spend a significant portion of their time. A cryptic error message can consume hours of investigation. AI tools can parse error messages, identify likely causes, and suggest fixes in seconds. For data professionals working with complex SQL queries, Python pipelines, and distributed systems, AI-assisted debugging is a massive time saver. However, it requires knowing how to present the problem clearly and how to evaluate the suggested fix.

## The Concept

### How AI Processes Error Messages

When you share an error message with an AI, it:

1. Parses the error type (syntax, runtime, logic)
2. Identifies the likely component that failed
3. Matches the error pattern against known issues
4. Suggests one or more fixes based on common solutions

The quality of the AI's diagnosis depends directly on how much context you provide.

### Structuring a Debug Prompt

#### Minimal Prompt (Poor Results)

```
"Fix this error: TypeError"
```

The AI has almost nothing to work with.

#### Good Debug Prompt

```
"I am getting this error when running my ETL pipeline:

Error:
TypeError: cannot concatenate 'NoneType' to str

Code context:
def build_table_ref(project, dataset, table):
    return project + '.' + dataset + '.' + table

Called with:
build_table_ref('my-project', None, 'customers')

Environment: Python 3.10, running on Windows

What is causing this and how should I fix it?"
```

#### Best Debug Prompt

```
"I am getting this error in my data pipeline:

## Error
TypeError: cannot concatenate 'NoneType' to str (line 24)

## Full Stack Trace
[paste complete stack trace]

## Relevant Code
[paste the function and its callers]

## What I Expected
The function should build a BigQuery table reference string.

## What I Have Tried
- Verified project and table are set correctly
- The error occurs only when processing config from YAML

## Environment
- Python 3.10.12
- pandas 2.1.4
- google-cloud-bigquery 3.14.1
- Windows 11"
```

### Common Debug Scenarios for Data Professionals

#### Scenario 1: SQL Query Errors

```
Prompt:
"This BigQuery query returns an error:

Query:
SELECT customer_id, 
       COUNTIF(status = 'completed') / COUNT(*) AS completion_rate
FROM orders
GROUP BY customer_id

Error:
No matching signature for function COUNTIF for argument 
types: BOOL, INT64

How do I fix this?"
```

#### Scenario 2: Data Type Mismatches

```
Prompt:
"My pandas merge is producing unexpected results:

left_df has customer_id as int64
right_df has customer_id as string

After left merge, I am getting all NaN values in the 
right columns. Both DataFrames have matching customer_id 
values when I check manually.

What is the issue?"
```

#### Scenario 3: Performance Issues

```
Prompt:
"This BigQuery query runs for 45 minutes and scans 
2 TB of data. How can I optimize it?

Query:
[paste query]

Table info:
- orders: 500M rows, partitioned by order_date, 
  clustered by customer_id
- customers: 10M rows, no partitioning

The query mostly filters by date range and customer segment."
```

### AI Debug Workflow

```
Step 1: Reproduce the error
  - Confirm you can trigger the error consistently
  
Step 2: Gather context
  - Full error message and stack trace
  - Relevant code
  - Environment details
  
Step 3: Ask AI
  - Use structured prompt template
  - Include what you have already tried
  
Step 4: Evaluate the suggestion
  - Does the fix address the root cause or just the symptom?
  - Could the fix introduce new issues?
  - Is the fix consistent with your codebase patterns?
  
Step 5: Apply and test
  - Implement the fix
  - Verify the original error is resolved
  - Run related tests to check for regressions
  
Step 6: Document
  - Add a code comment explaining the fix
  - Update error handling if appropriate
```

### When AI Debugging Falls Short

| Scenario | Why AI Struggles | What to Do Instead |
| -------- | ---------------- | ------------------ |
| Race conditions | AI cannot observe runtime timing | Use debugging tools, add logging |
| Environment-specific issues | AI does not have your environment | Check environment config manually |
| Data-dependent bugs | AI cannot see your data | Inspect actual data values |
| Intermittent failures | AI cannot reproduce | Add monitoring and alerting |
| Security incidents | Sharing details may be risky | Consult security team directly |

### Debugging Best Practices

1. **Include the full error message** -- partial errors lead to wrong diagnoses
2. **Show the code context** -- the error line alone is rarely enough
3. **Describe expected vs actual behavior** -- this frames the problem correctly
4. **Mention what you have tried** -- prevents the AI from repeating failed attempts
5. **Verify fixes independently** -- do not blindly apply AI suggestions

## Key Takeaways

- AI can significantly accelerate debugging when given proper context
- Structured debug prompts (error, code, expected behavior, what was tried) produce the best results
- AI is most effective for syntax errors, type mismatches, and common patterns
- AI struggles with environment-specific, data-dependent, and intermittent issues
- Always verify AI-suggested fixes and check for regressions

## Additional Resources

- [Python Debugging Guide](https://docs.python.org/3/library/pdb.html)
- [BigQuery Troubleshooting Guide](https://cloud.google.com/bigquery/docs/troubleshooting-errors)
- [VS Code Debugging Documentation](https://code.visualstudio.com/docs/editor/debugging)
