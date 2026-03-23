# Instructions and Guidelines for LLMs

## Learning Objectives

- Craft effective instructions that produce consistent, high-quality outputs
- Understand the role of system-level guidelines in shaping model behavior
- Apply instruction design patterns for data engineering tasks
- Build reusable prompt templates

## Why This Matters

Well-written instructions are the difference between an AI that produces useful, consistent results and one that gives you something different every time. For data teams, where consistency and precision are non-negotiable -- think SQL output, documentation formats, and analysis structures -- mastering instruction design is a force multiplier.

## The Concept

### The Instruction Hierarchy

LLMs process instructions at multiple levels, from most persistent to most specific:

```
System Instructions (persistent, set once)
    |
    v
Conversation Context (accumulated)
    |
    v
User Message (current request)
```

Each level adds context. Instructions at higher levels generally take precedence, though this varies by model.

### Writing Clear Instructions

#### Imperative Language

Use direct, action-oriented language:

```
Good:  "Write a Python function that..."
Good:  "List the top 5..."
Good:  "Explain the difference between..."

Avoid: "Could you maybe try to..."
Avoid: "I was wondering if..."
Avoid: "It would be nice to have..."
```

#### Structure with Sections

For complex tasks, organize instructions with clear sections:

```
## Task
Generate a data quality report for the given dataset.

## Input
A CSV file with columns: id, name, email, signup_date, status

## Requirements
- Check for null values in each column
- Identify duplicate rows based on 'id'
- Validate email format using regex
- Flag dates in the future

## Output Format
Return a markdown table with columns:
Check Name | Column | Status | Count | Details
```

### Guideline Design Patterns

#### The Persona Pattern

Define who the model should be:

```
You are a senior data engineer with 10 years of experience 
in BigQuery and Python. You follow Google's SQL style guide. 
You always consider query cost optimization. When reviewing 
code, you prioritize correctness, then readability, then 
performance.
```

#### The Rules Pattern

Set explicit behavioral rules:

```
Rules:
1. Always use standard SQL, never legacy SQL
2. Include comments for every CTE and complex expression
3. Use meaningful aliases (not single letters)
4. If the question is ambiguous, ask for clarification
5. Never suggest solutions that require elevated permissions
```

#### The Template Pattern

Provide output templates the model should follow:

```
For each data quality issue found, format your response as:

### [Issue Title]
- **Severity**: HIGH / MEDIUM / LOW
- **Column**: [affected column]
- **Description**: [what the issue is]
- **Impact**: [what could go wrong]
- **Recommendation**: [how to fix it]
```

#### The Workflow Pattern

Define step-by-step processing instructions:

```
Process each request using these steps:
1. Read the SQL query provided
2. Identify the query's purpose in one sentence
3. Check for syntax errors
4. Evaluate performance (note full table scans, missing 
   WHERE clauses, etc.)
5. Provide an optimized version if improvements are possible
6. Explain each change you made and why
```

### Building Reusable Prompt Templates

Create templates you can fill in for recurring tasks:

```
# Template: Code Review

You are a [ROLE] reviewing [LANGUAGE] code.

## Code to Review
[PASTE CODE HERE]

## Focus Areas
- [AREA 1]
- [AREA 2]
- [AREA 3]

## Output Format
For each finding:
- Line number(s)
- Severity (HIGH/MEDIUM/LOW)
- Description
- Suggested fix

## Constraints
- Maximum [N] findings
- Do not suggest style changes unless they affect readability
- [ADDITIONAL CONSTRAINTS]
```

### Common Pitfalls

| Pitfall | Example | Fix |
| ------- | ------- | --- |
| Contradictory instructions | "Be brief" + "Include examples for everything" | Prioritize or remove conflicts |
| Implicit assumptions | "Use the standard format" | Define what "standard" means |
| Missing edge cases | "Convert dates" (what format? what timezone?) | Specify input/output formats |
| Over-engineering | 500-word instruction for a simple task | Match instruction complexity to task complexity |

## Key Takeaways

- Clear, imperative instructions produce better results than polite requests
- Structured instructions with sections improve consistency
- Design patterns (persona, rules, template, workflow) can be combined
- Reusable templates save time and ensure consistency across tasks

## Additional Resources

- [OpenAI - Strategy: Write Clear Instructions](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions)
- [Anthropic - Be Clear and Direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
- [Google - Structure Prompts for Better Results](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
