# Phase 05 — Analyst Agent

**Goal:** synthesize retrieved chunks into a structured, cited answer using AWS Bedrock Claude — with **Pydantic-validated output** so the Fact-Checker and Critique nodes can rely on the schema.

You will fill in `analyst_node` in `agents/analyst.py`, plus the `Citation` and `AnalysisResult` Pydantic models that define the Analyst's output contract.

---

## 5.1 The structured-output trick

Bedrock Claude doesn't have an OpenAI-style `response_format=json_schema` knob, but Anthropic's [tool-use feature](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) gives you the same effect: declare a tool whose input schema *is* your Pydantic schema, and instruct the model to call it. The model is then forced into your shape.

This is exactly how `langchain-aws`'s `ChatBedrock.with_structured_output()` works under the hood. We'll use that wrapper — much less code than building a tool-call payload manually.

## 5.2 Prompt design — citations matter

The Analyst's contract says **every claim must cite a source**. Don't trust the model to do this on its own — make the prompt make it impossible to comply *without* citing. Pattern: number the chunks in the prompt, tell the model to cite by number, and require at least one citation per sentence.

## 5.3 Reference implementation

Replace the body of `analyst_node` with the code below, and add the `Citation` / `AnalysisResult` models alongside it. Add the imports near the top.

```python
import os

from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from agents.state import ResearchState


class Citation(BaseModel):
    source: str = Field(description="Source filename, e.g. 'Artemis_II.pdf'")
    page_number: int | None = Field(
        default=None,
        description="Page number within the source, if known",
    )


class AnalysisResult(BaseModel):
    answer: str = Field(description="The synthesized answer to the user's question")
    citations: list[Citation] = Field(
        default_factory=list,
        description=(
            "A list of citation objects. Each object MUST have a 'source' string "
            "and an optional 'page_number' integer. Do NOT return a single string."
        ),
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Self-assessed confidence on a 0.0–1.0 scale",
    )


_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a research analyst. Synthesize a precise answer to the user's "
     "question using ONLY the numbered context chunks below. Every factual "
     "claim must cite at least one chunk by its source filename and page. "
     "If the context does not support an answer, say so explicitly and set "
     "confidence below 0.4.\n\n"
     "Self-assess your confidence on a 0.0–1.0 scale where:\n"
     "  • 0.9+ = direct quote answers the question\n"
     "  • 0.6–0.9 = answer is supported by the context but requires inference\n"
     "  • <0.6 = context is partial, conflicting, or off-topic\n\n"
     "Output schema: return JSON with 'answer' (string), 'citations' "
     "(a JSON array of objects, each with 'source' and 'page_number'), "
     "and 'confidence' (number 0.0–1.0). Never return citations as a single string."),
    ("human",
     "Question: {question}\n\n"
     "Sub-task: {sub_task}\n\n"
     "Context chunks:\n{context_block}"),
])


def _format_chunks(chunks: list[dict]) -> str:
    """Render retrieved chunks into a numbered, citeable block."""
    lines = []
    for i, c in enumerate(chunks, start=1):
        page = f", p.{c['page_number']}" if c.get("page_number") else ""
        lines.append(f"[{i}] (source: {c['source']}{page})\n{c['content']}")
    return "\n\n".join(lines)


def analyst_node(state: ResearchState) -> dict:
    """Synthesize a structured answer from the retrieved context."""
    chunks = state.get("retrieved_chunks", [])
    log = [f"[analyst] synthesizing from {len(chunks)} chunks"]

    if not chunks:
        empty = AnalysisResult(
            answer="No relevant context was retrieved; cannot answer reliably.",
            citations=[],
            confidence=0.0,
        )
        return {
            "analysis": empty.model_dump(),
            "confidence_score": 0.0,
            "scratchpad": log + ["[analyst] short-circuit: no chunks"],
        }

    plan = state.get("plan", [])
    idx = state.get("current_subtask_index", 0)
    sub_task = plan[idx] if plan else state["question"]

    # ChatBedrock + structured output — the LLM is forced into AnalysisResult.
    llm = ChatBedrock(
        model_id=os.environ["BEDROCK_MODEL_ID"],
        region_name=os.environ["AWS_REGION"],
        model_kwargs={"max_tokens": 1024, "temperature": 0.2},
    )
    chain = _PROMPT | llm.with_structured_output(AnalysisResult)

    result: AnalysisResult = chain.invoke({
        "question": state["question"],
        "sub_task": sub_task,
        "context_block": _format_chunks(chunks),
    })
    log.append(f"[analyst] confidence={result.confidence:.2f}, "
               f"citations={len(result.citations)}")

    return {
        "analysis": result.model_dump(),
        "confidence_score": float(result.confidence),
        "scratchpad": log,
    }
```

## 5.4 Why these specific choices

- **`temperature=0.2`** — research synthesis wants stable, repeatable outputs, not creativity.
- **`max_tokens=1024`** — enough for a multi-paragraph answer with citations; raise if your domain needs longer answers.
- **Numbered chunks `[1] [2] ...`** — gives the model a stable handle to reference. The Pydantic schema asks for `source` + `page_number`, but the prompt cue makes it likely the model emits accurate ones.
- **Field descriptions, not bare types** — `with_structured_output` ships the Pydantic schema to Bedrock as a tool definition, and `Field(description=...)` text appears in that schema. Without it, weaker models (Haiku especially) sometimes flatten `citations: list[Citation]` into a single string echoing the input chunks. The descriptions plus the explicit "Output schema" line in the system prompt are belt-and-suspenders against that failure mode.
- **Empty-context short circuit** — if retrieval returned nothing, don't waste a Bedrock call. Just emit a low-confidence "I cannot answer" result and let the Critique node handle it.
- **`model_dump()` not the Pydantic object** — LangGraph state is a TypedDict of plain dicts. Stuffing Pydantic models into it will deserialize incorrectly when checkpointed.

> If you still see `pydantic_core._pydantic_core.ValidationError` on the `citations` field after the changes above, you've hit Haiku-3's structured-output ceiling. Switch the Analyst to Sonnet for higher reliability — set `BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0` in `.env` (request model access in the Bedrock console first) and keep Haiku for the cheap classifier work in Phase 06.

## 5.5 Streaming (optional)

The README calls out streaming responses (FR-4). `ChatBedrock.stream(...)` works just like `.invoke(...)` but yields chunks. You **cannot** stream into structured output (the schema needs the full response to validate), so the typical pattern is:

- During interactive sessions: call `llm.stream(...)` for the *raw* answer to surface text to the UI live, then call `.invoke()` on the structured chain in parallel for the validated result.
- During graph execution: just use the structured `.invoke()` shown above. The Lambda/CLI shell doesn't need true streaming.

For the deliverable a working `.invoke()` is sufficient. Mention streaming in your demo as a future-work item if you don't get to it.

## 5.6 Verify

```python
import os
from dotenv import load_dotenv
load_dotenv()

from agents.retriever import retriever_node
from agents.analyst import analyst_node

state = {
    "question": "Question your corpus can actually answer.",
    "plan": ["Question your corpus can actually answer."],
    "current_subtask_index": 0,
}
state.update(retriever_node(state))
state.update(analyst_node(state))
import json
print(json.dumps(state["analysis"], indent=2))
print("Confidence:", state["confidence_score"])
```

You should see a structured dict with `answer`, `citations` (a list of `{source, page_number, excerpt}`), and `confidence`. If `citations` is empty, sharpen the system prompt — usually adding "You MUST cite at least one chunk" does it.

---

Continue to [06-FactChecker-Agent.md](06-FactChecker-Agent.md).
