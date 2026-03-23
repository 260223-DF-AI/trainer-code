# Interaction and Dialogue State

## Learning Objectives

- Understand how LLMs manage conversation context
- Explain context windows and their limitations
- Design effective multi-turn conversations with AI
- Manage dialogue state for complex tasks

## Why This Matters

Most real-world AI interactions are not single questions. They are conversations that build on previous messages. Understanding how LLMs track (and lose) context across a conversation is critical for getting reliable results, especially when working through complex data engineering tasks that span multiple steps.

## The Concept

### How LLMs Track Conversations

LLMs do not have memory in the human sense. When you have a conversation with an AI, it processes the entire conversation history as a single input each time you send a message:

```
Message 1: "Create a customers table in BigQuery"
Message 2: "Now add an index on email"  
Message 3: "Show me the final schema"

What the model actually sees on Message 3:
[System prompt] + [Message 1] + [Response 1] + 
[Message 2] + [Response 2] + [Message 3]
```

Each new message includes everything that came before. The model re-reads the entire conversation to generate each response.

### Context Windows

A context window is the maximum amount of text (measured in tokens) that an LLM can process at once. Tokens are roughly equivalent to word fragments:

| Model | Context Window | Approximate Words |
| ----- | -------------- | ----------------- |
| GPT-3.5 | 4,096 tokens | ~3,000 words |
| GPT-4 | 8,192-128K tokens | ~6,000-96,000 words |
| Claude 3 | 200K tokens | ~150,000 words |
| Gemini 1.5 | 1M+ tokens | ~750,000 words |

**What happens when you exceed the context window:**

- Older messages are dropped (truncated)
- The model loses context from earlier in the conversation
- Responses may contradict previous statements

### Designing Effective Multi-Turn Conversations

#### Strategy 1: Summarize Before Continuing

When a conversation gets long, summarize the key context:

```
"To summarize what we have so far:
- We created a dim_customer table with SCD Type 2
- We wrote the MERGE statement for updates
- We tested with 3 sample records

Now, let's create the dim_product table following 
the same pattern."
```

#### Strategy 2: Self-Contained Messages

For critical steps, include all necessary context in each message rather than relying on conversation history:

```
Less reliable:
"Now do the same for the orders table"

More reliable:
"Create a BigQuery CREATE TABLE statement for a 
fact_orders table with columns: order_key (INT64), 
date_key (STRING), customer_key (INT64), 
product_key (INT64), quantity (INT64), 
total_amount (NUMERIC). Partition by 
PARSE_DATE('%Y%m%d', date_key)."
```

#### Strategy 3: Break Complex Tasks into Steps

Instead of one massive prompt, break work into a dialogue:

```
Step 1: "List the tables needed for a retail data warehouse"
Step 2: "For the fact_sales table, what should the grain be?"
Step 3: "Write the DDL for fact_sales based on our discussion"
Step 4: "Now review the DDL for any issues"
```

### Dialogue Patterns for Data Engineering

#### The Research Pattern

```
You: "What are the best practices for BigQuery partitioning?"
AI: [Provides overview]
You: "Given a table with 500M rows and queries mostly 
     filtering by date and region, which approach do you 
     recommend?"
AI: [Provides specific recommendation]
You: "Write the DDL implementing that approach"
```

#### The Debug Pattern

```
You: "This query is returning incorrect results: [query]"
AI: [Identifies potential issues]
You: "The issue is in the JOIN. Here's the schema: [schema]"
AI: [Provides corrected query]
You: "The fix works. Now optimize it for performance."
```

#### The Build Pattern

```
You: "Help me design a data pipeline for daily sales data"
AI: [Proposes architecture]
You: "Let's implement the extraction step first"
AI: [Writes extraction code]
You: "Good. Now the transformation step."
AI: [Writes transformation code]
```

### State Management Tips

1. **Start fresh for unrelated tasks** -- do not carry over a long conversation about ETL when switching to a prompt about SQL optimization
2. **Pin critical information** -- repeat important schemas or requirements periodically
3. **Use explicit references** -- say "the dim_customer table from Step 2" rather than "that table"
4. **Number your steps** -- it helps both you and the model track where you are

## Key Takeaways

- LLMs re-read the entire conversation for each response; they do not truly "remember"
- Context windows have limits; exceeding them causes information loss
- Summarizing, self-contained messages, and step-by-step approaches improve reliability
- Different dialogue patterns (research, debug, build) suit different tasks

## Additional Resources

- [Anthropic - Long Context Tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)
- [OpenAI - Managing Conversation History](https://platform.openai.com/docs/guides/conversation)
- [Google - Designing Multi-Turn Prompts](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)
