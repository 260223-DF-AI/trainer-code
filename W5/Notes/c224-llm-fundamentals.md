# LLM Fundamentals

## Learning Objectives

- Explain what a Large Language Model is and how it works
- Understand the transformer architecture at a high level
- Define tokenization and its role in LLM processing
- Identify the relationship between model size, capability, and cost

## Why This Matters

Large Language Models are the technology behind every Gen AI tool you will use as a data professional -- from ChatGPT to GitHub Copilot to BigQuery's natural language features. Understanding how they work, even at a conceptual level, helps you use them more effectively, troubleshoot unexpected behavior, and make informed decisions about which model to use for which task.

## The Concept

### What Is a Large Language Model?

A Large Language Model (LLM) is a type of neural network trained on vast amounts of text data to understand and generate human language. The word "large" refers to two things:

1. **Large training data**: Trained on billions of documents (books, websites, code repositories, scientific papers)
2. **Large parameter count**: Contains billions of adjustable parameters (weights) that encode learned patterns

At its core, an LLM is a next-token predictor. Given a sequence of text, it predicts the most likely next word (or token). This simple mechanism, scaled to billions of parameters, produces remarkably capable language understanding and generation.

### The Transformer Architecture

The transformer is the neural network architecture that powers all modern LLMs. Introduced in the 2017 paper "Attention Is All You Need," it solved the key challenge of processing language: understanding which words in a sentence relate to which other words, regardless of distance.

#### The Attention Mechanism

The key innovation of transformers is "attention" -- the ability to weigh the importance of every word relative to every other word in the input:

```
Input: "The data engineer who designed the pipeline 
        fixed the bug"

Attention helps the model understand:
- "fixed" relates to "engineer" (who fixed it?)
- "the pipeline" relates to "designed" (what was designed?)
- "the bug" relates to "fixed" (what was fixed?)
```

Without attention, earlier models struggled with long-range dependencies -- understanding relationships between words far apart in a sentence.

#### Simplified Transformer Flow

```
Input Text
    |
    v
Tokenization (split into tokens)
    |
    v
Embedding (convert tokens to numbers)
    |
    v
Transformer Layers (attention + processing)
    |  [repeated many times]
    v
Output Probabilities (next token prediction)
    |
    v
Generated Text
```

### Tokenization

Tokenization is the process of breaking text into smaller units (tokens) that the model can process. Tokens are not always complete words:

```
Text: "BigQuery processes petabytes efficiently"

Tokens: ["Big", "Query", " processes", " peta", "bytes", 
         " efficiently"]

Token count: 6 tokens for 5 words
```

**Why tokenization matters:**

- LLMs have token limits (context windows), not word limits
- Code and technical terms often require more tokens than plain English
- Special characters and formatting consume tokens
- Cost is typically calculated per token (both input and output)

**Token estimation rules of thumb:**

- 1 token is approximately 4 characters in English
- 1 token is approximately 0.75 words
- Code typically uses more tokens per line than prose

### Model Size and Capability

| Model Size | Parameters | Typical Use |
| ---------- | ---------- | ----------- |
| Small | 1-7B | Simple tasks, edge deployment, fast inference |
| Medium | 7-70B | General tasks, good balance of capability and cost |
| Large | 70B+ | Complex reasoning, long context, highest capability |

**The trade-off:**

- Larger models are more capable but more expensive to run
- Smaller models are faster but may produce lower-quality outputs
- The right choice depends on your task complexity and budget

### How LLMs Are Trained

#### Pre-Training

The model reads vast amounts of text and learns to predict the next token. This gives it general knowledge about language, facts, and reasoning patterns.

#### Fine-Tuning

After pre-training, the model is trained on specific, curated datasets to improve performance on particular tasks (conversation, code, safety).

#### RLHF (Reinforcement Learning from Human Feedback)

Human raters evaluate model outputs and provide feedback. The model is further trained to produce outputs that humans rate more highly.

```
Pre-Training --> Fine-Tuning --> RLHF --> Deployed Model
(general       (task-specific   (aligned    (ready to use)
 knowledge)     capability)      with human
                                 preferences)
```

### Key Terminology Quick Reference

| Term | Definition |
| ---- | ---------- |
| **Token** | The basic unit of text processed by an LLM |
| **Context Window** | Maximum tokens the model can process at once |
| **Temperature** | Controls randomness in output (0 = deterministic, 1 = creative) |
| **Top-p (nucleus sampling)** | Controls diversity of token selection |
| **Inference** | Using a trained model to generate output |
| **Latency** | Time between sending a prompt and receiving a response |
| **Throughput** | Number of tokens the model can generate per second |

## Key Takeaways

- LLMs are next-token predictors trained on massive text datasets
- The transformer architecture with attention mechanisms is the foundation of all modern LLMs
- Tokenization converts text into processable units and directly affects cost and context limits
- Larger models are more capable but more expensive; choose based on task requirements
- Understanding these fundamentals helps you use AI tools more effectively

## Additional Resources

- [Google - Attention Is All You Need (Original Paper)](https://arxiv.org/abs/1706.03762)
- [OpenAI - Tokenizer Tool](https://platform.openai.com/tokenizer)
- [Hugging Face - Transformer Models](https://huggingface.co/docs/transformers/index)
