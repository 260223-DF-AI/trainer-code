# The LLM Landscape

## Learning Objectives

- Identify the major LLMs available today and their key characteristics
- Compare GPT, BERT, Claude, Llama, Copilot, and Codeium
- Understand the difference between proprietary and open-source models
- Select appropriate models based on task requirements

## Why This Matters

The LLM landscape is evolving rapidly. As a data professional, you will encounter multiple AI tools and models. Understanding their strengths, limitations, and pricing helps you make informed decisions. Choosing the right model for the right task saves time and money while producing better results.

## The Concept

### The Major Players

#### GPT (Generative Pre-trained Transformer) - OpenAI

GPT is the model family behind ChatGPT and the OpenAI API.

| Version | Key Features |
| ------- | ------------ |
| GPT-3.5 | Fast, affordable, good for simple tasks |
| GPT-4 | Strong reasoning, multimodal (text + images), larger context |
| GPT-4o | Optimized for speed while maintaining GPT-4 quality |

**Strengths**: Strong general reasoning, extensive API ecosystem, wide adoption
**Limitations**: Proprietary, requires API access, can be expensive at scale
**Best for**: General-purpose tasks, complex reasoning, code generation

#### BERT (Bidirectional Encoder Representations from Transformers) - Google

BERT differs fundamentally from GPT. It is an encoder-only model designed for understanding text, not generating it.

**Strengths**: Excellent at classification, sentiment analysis, search ranking
**Limitations**: Not designed for text generation; primarily used in embeddings and NLU
**Best for**: Search engines, text classification, named entity recognition

**Key Distinction**: BERT reads text bidirectionally (both left-to-right and right-to-left), making it excellent at understanding context but not at generating new text.

#### Claude - Anthropic

Claude is designed with a focus on safety, helpfulness, and long-context processing.

| Version | Key Features |
| ------- | ------------ |
| Claude 3 Haiku | Fast, affordable, good for simple tasks |
| Claude 3 Sonnet | Balanced performance and cost |
| Claude 3 Opus | Highest capability, complex reasoning |

**Strengths**: Very long context window (200K tokens), strong at following instructions, emphasis on safety
**Limitations**: Proprietary, can be overly cautious, smaller ecosystem than GPT
**Best for**: Long document analysis, careful instruction following, safety-critical tasks

#### Llama - Meta

Llama is Meta's open-source LLM family.

| Version | Key Features |
| ------- | ------------ |
| Llama 2 | Open-source, 7B to 70B parameters |
| Llama 3 | Improved performance, expanded context |

**Strengths**: Open-source (can be self-hosted), customizable, no API fees when self-hosted
**Limitations**: Requires infrastructure to run, smaller models are less capable than GPT-4/Claude
**Best for**: Organizations needing data privacy, custom fine-tuning, cost-sensitive deployments

#### GitHub Copilot

Copilot is an AI-powered code completion tool built on OpenAI models, integrated directly into IDEs.

**Strengths**: Deep IDE integration, context-aware code suggestions, inline completions
**Limitations**: Subscription-based, primarily focused on code, limited to supported IDEs
**Best for**: Day-to-day coding, boilerplate generation, code completion

We will explore Copilot in depth on Wednesday.

#### Codeium

Codeium is a free alternative to Copilot, offering AI-powered code completion.

**Strengths**: Free tier available, supports many IDEs, privacy-focused options
**Limitations**: Generally less capable than Copilot for complex tasks
**Best for**: Individual developers seeking free AI code assistance

### Proprietary vs Open-Source Models

| Aspect | Proprietary (GPT, Claude) | Open-Source (Llama) |
| ------ | ------------------------- | ------------------- |
| Access | API / subscription | Download and self-host |
| Cost | Per-token pricing | Infrastructure cost only |
| Privacy | Data sent to provider | Data stays on your servers |
| Customization | Limited to API options | Full fine-tuning possible |
| Support | Vendor support included | Community support |
| Updates | Automatic | Manual deployment |

### Choosing the Right Model

Consider these factors when selecting a model:

```
Task Complexity?
    |
    +-- Simple (classification, summarization)
    |   --> GPT-3.5, Claude Haiku, Small Llama
    |
    +-- Medium (code generation, analysis)
    |   --> GPT-4o, Claude Sonnet, Copilot
    |
    +-- Complex (multi-step reasoning, long docs)
        --> GPT-4, Claude Opus, Large Llama

Data Privacy?
    |
    +-- Can send to cloud  --> Any proprietary model
    +-- Must stay on-premises --> Llama (self-hosted)

Budget?
    |
    +-- Per-use pricing OK  --> GPT, Claude APIs
    +-- Fixed cost preferred --> Copilot subscription
    +-- Free needed         --> Codeium, Llama
```

### Benchmarking and Evaluation

Models are often compared using standardized benchmarks:

| Benchmark | What It Measures |
| --------- | ---------------- |
| MMLU | General knowledge across 57 subjects |
| HumanEval | Code generation accuracy |
| GSM8K | Mathematical reasoning |
| HellaSwag | Common sense reasoning |
| TruthfulQA | Resistance to generating false information |

Be cautious with benchmarks. Performance on standardized tests does not always predict performance on your specific use case. Always evaluate models on your actual tasks.

## Key Takeaways

- GPT and Claude are proprietary models strong in general reasoning; Claude excels at long contexts
- BERT is an understanding model, not a generation model -- suited for classification and search
- Llama is open-source and can be self-hosted for data privacy
- Copilot and Codeium are specialized for code within IDEs
- Model selection depends on task complexity, privacy requirements, and budget

## Additional Resources

- [OpenAI - Models Overview](https://platform.openai.com/docs/models)
- [Anthropic - Claude Models](https://docs.anthropic.com/en/docs/about-claude/models)
- [Meta AI - Llama](https://ai.meta.com/llama/)
