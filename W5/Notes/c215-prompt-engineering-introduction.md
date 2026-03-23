# Introduction to Prompt Engineering

## Learning Objectives

- Define prompt engineering and its significance
- Understand the anatomy of an effective prompt
- Identify the core principles that make prompts effective
- Recognize prompt engineering as a professional skill

## Why This Matters

Prompt engineering is the art and science of communicating effectively with AI systems. As Gen AI tools become standard in the workplace, the ability to write clear, precise prompts directly determines how useful these tools are. A well-crafted prompt can save hours of work. A poor prompt produces irrelevant or inaccurate output. For data professionals, prompt engineering unlocks the full potential of AI-assisted coding, analysis, and documentation.

## The Concept

### What Is Prompt Engineering?

A prompt is the input you provide to a generative AI model. Prompt engineering is the practice of designing and refining that input to get the most useful output.

Think of it this way: the AI model is a highly capable but extremely literal assistant. It will do exactly what you ask -- but only if you ask clearly. Prompt engineering is learning how to ask clearly.

### The Anatomy of a Prompt

An effective prompt typically contains some or all of these elements:

```
+------------------+
|   Role/Context   |  "You are a senior data engineer..."
+------------------+
|   Task           |  "Write a SQL query that..."
+------------------+
|   Constraints    |  "Use BigQuery syntax. No subqueries."
+------------------+
|   Input Data     |  "The table has columns: id, name, date..."
+------------------+
|   Output Format  |  "Return the result as a markdown table."
+------------------+
```

Not every prompt needs all five elements, but being explicit about each produces better results.

### Core Principles of Effective Prompts

#### 1. Be Specific

Vague prompts produce vague results.

| Weak Prompt | Strong Prompt |
| ----------- | ------------- |
| "Tell me about databases" | "Explain the difference between OLTP and OLAP databases, with one example of each" |
| "Write code" | "Write a Python function that reads a CSV file and returns a pandas DataFrame with null rows removed" |

#### 2. Provide Context

The model has no memory of your project unless you supply it. Context reduces ambiguity.

```
Without context:
  "Convert this to Parquet"

With context:
  "I have a CSV file with 10 million rows containing sales 
   transactions. Convert this to Parquet format using Python 
   and pyarrow, optimizing for analytical queries that filter 
   by date and product_category."
```

#### 3. Specify the Output Format

Tell the model exactly how you want the response structured.

```
"List the top 5 BigQuery optimization techniques.
Format your response as a numbered list with a one-sentence 
explanation for each technique."
```

#### 4. Iterate and Refine

Prompt engineering is iterative. If the first response is not what you need:

- Add more constraints
- Provide an example of desired output
- Break the task into smaller steps
- Clarify ambiguous terms

### Prompt Patterns

Prompts generally fall into common patterns:

| Pattern | Description | Example |
| ------- | ----------- | ------- |
| Instruction | Direct command | "Summarize this article in 3 sentences" |
| Role-play | Assign a persona | "You are a database administrator. Review this schema." |
| Template | Fill-in-the-blank | "Given [data], produce [output] in [format]" |
| Chain-of-thought | Step-by-step reasoning | "Think through this problem step by step" |
| Few-shot | Provide examples | "Here are 2 examples. Now do the same for..." |

We will explore several of these patterns in detail throughout today's content.

## Key Takeaways

- Prompt engineering is the skill of communicating effectively with AI models
- Good prompts are specific, contextual, and format-aware
- The five elements of a prompt are: role, task, constraints, input data, and output format
- Prompt engineering is iterative -- expect to refine your prompts

## Additional Resources

- [OpenAI - Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google - Introduction to Prompt Design](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
- [Anthropic - Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
