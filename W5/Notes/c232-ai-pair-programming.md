# Introduction to AI Pair Programming

## Learning Objectives

- Define AI pair programming and how it differs from traditional pair programming
- Understand the roles of human and AI in pair programming
- Identify effective patterns for AI pair programming sessions
- Recognize when AI pair programming adds value and when it does not

## Why This Matters

Pair programming has been a proven practice in software development for decades. AI pair programming takes this concept further by providing a tireless, knowledgeable partner available at any time. For data professionals who often work independently on pipelines and queries, AI pair programming provides a collaborator who can catch errors, suggest alternatives, and accelerate development.

## The Concept

### What Is AI Pair Programming?

Traditional pair programming involves two developers working at one workstation:

- **Driver**: Writes the code
- **Navigator**: Reviews, suggests, and thinks about strategy

AI pair programming replaces the human navigator with an AI:

- **Human (Driver)**: Provides direction, makes decisions, reviews output
- **AI (Navigator)**: Suggests code, catches errors, provides alternatives

### How AI Pair Programming Works in Practice

#### Real-Time Code Completion

As you type, the AI suggests completions:

```python
# You type:
def load_data_to_bigquery(

# AI suggests:
def load_data_to_bigquery(
    df: pd.DataFrame, 
    project_id: str, 
    dataset_id: str, 
    table_id: str
) -> int:
    """Load a pandas DataFrame to BigQuery.
    
    Args:
        df: DataFrame to load
        project_id: GCP project ID
        dataset_id: BigQuery dataset name
        table_id: Target table name
        
    Returns:
        Number of rows loaded
    """
    client = bigquery.Client(project=project_id)
    ...
```

You review the suggestion, accept what is correct, and modify what is not.

#### Conversational Problem Solving

When you encounter a challenge, you describe it to the AI:

```
You: "I need to deduplicate records in BigQuery where 
     multiple rows have the same customer_id but different 
     timestamps. I want to keep only the most recent row 
     for each customer."

AI: "You can use ROW_NUMBER() with a window function:

SELECT * EXCEPT(rn)
FROM (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id 
      ORDER BY timestamp DESC
    ) AS rn
  FROM your_table
)
WHERE rn = 1"
```

### Effective AI Pair Programming Patterns

#### Pattern 1: Scaffold and Fill

Ask AI to generate the structure, then fill in the details yourself:

```
Prompt: "Create a Python class skeleton for an ETL 
pipeline with methods for extract, transform, load, 
and validate. Include docstrings but leave method 
bodies empty."

Your role: Implement each method with your business logic
```

#### Pattern 2: Explain and Extend

Give AI existing code to understand, then ask for extensions:

```
Step 1: "Explain what this function does: [paste code]"
Step 2: "Now add error handling for network timeouts"
Step 3: "Add retry logic with exponential backoff"
```

#### Pattern 3: Rubber Duck with Intelligence

Use AI as a sounding board that can actually respond:

```
"I am designing a data pipeline that needs to process 
10 million records daily. I am considering two approaches:
1. Batch processing at midnight
2. Micro-batches every 15 minutes

What are the trade-offs of each approach for BigQuery?"
```

#### Pattern 4: Test-Driven with AI

Write the test first, let AI implement:

```
"Here is my test:

def test_clean_customer_data():
    input_df = pd.DataFrame({
        'name': ['  John  ', 'JANE', None],
        'email': ['john@test.com', 'invalid', 'jane@test.com']
    })
    result = clean_customer_data(input_df)
    assert len(result) == 2  # null name removed
    assert result.iloc[0]['name'] == 'John'  # trimmed
    assert result.iloc[1]['name'] == 'Jane'  # title case

Write the clean_customer_data function that passes this test."
```

### When AI Pair Programming Works Best

| Scenario | Effectiveness |
| -------- | ------------- |
| Writing boilerplate code | High |
| Exploring unfamiliar APIs | High |
| Debugging error messages | High |
| Generating test cases | High |
| Designing system architecture | Medium |
| Implementing complex algorithms | Medium |
| Writing performance-critical code | Low |
| Handling proprietary business logic | Low |

### When to Work Without AI

- When learning a new concept (doing it yourself builds understanding)
- When working with highly sensitive data
- When the task requires deep domain expertise the AI lacks
- When you need guaranteed correctness (formal verification, safety-critical systems)

## Key Takeaways

- AI pair programming provides a tireless collaborator for code suggestions and problem-solving
- The human remains the decision-maker; AI is the accelerator
- Effective patterns include scaffold-and-fill, explain-and-extend, and test-driven approaches
- AI pair programming is most effective for boilerplate, APIs, debugging, and testing
- Maintain your own skills by programming without AI regularly

## Additional Resources

- [GitHub - What Is AI Pair Programming?](https://github.com/features/copilot)
- [Martin Fowler - On Pair Programming](https://martinfowler.com/articles/on-pair-programming.html)
- [ACM - AI-Assisted Code Generation](https://dl.acm.org/doi/10.1145/3597503.3639187)
