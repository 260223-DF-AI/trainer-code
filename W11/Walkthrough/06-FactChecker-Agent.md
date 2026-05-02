# Phase 06 — Fact-Checker Agent

**Goal:** independently verify the Analyst's claims against the *separate* `fact-check-sources` namespace, and decide whether the answer can ship or needs human review.

You will fill in `fact_checker_node` in `agents/fact_checker.py`, plus the `ClaimVerdict` and `FactCheckReport` Pydantic models that define the report schema.

---

## 6.1 Why a separate namespace?

If the Fact-Checker queries the same corpus the Retriever did, all it can do is confirm "yes, the chunk we already used says what we said it said". That's circular. Real verification means consulting a *second source set* — typically a curated, smaller, higher-trust collection.

Examples of what to put in `fact-check-sources`:
- Authoritative reference works (encyclopedias, standards docs).
- Peer-reviewed papers if the corpus is gray literature.
- Internal "source of truth" docs (e.g., compliance policies) if the corpus is general team knowledge.

## 6.2 The "extract claims" step

The Analyst returns one big `answer` string. To check it claim-by-claim you have two options:

1. **LLM-based extraction.** Ask Bedrock "list each factual claim in this answer as a sentence". Robust but adds a second LLM call.
2. **Cheap split.** Treat each sentence as one claim. Loses some nuance but gets you to a working pipeline fast.

We'll start with the cheap split. Upgrade later if RAGAS faithfulness scores look weak (Phase 11).

## 6.3 The "verify each claim" step

For each claim:
1. Embed the claim text.
2. Query `fact-check-sources` with `top_k=3`.
3. Ask a small Bedrock call: "Does this evidence support, contradict, or fail to address this claim?" — return one of three labels.
4. Aggregate verdicts into an overall confidence score.

> Prefer **Haiku** here — three-class classification is exactly the kind of cheap, latency-sensitive task Haiku was designed for.

## 6.4 Reference implementation

Replace the body of `fact_checker_node`. Add the imports near the top.

```python
import os
import re

from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone
from pydantic import BaseModel, Field

from agents.state import ResearchState


class ClaimVerdict(BaseModel):
    claim: str
    verdict: str = Field(pattern=r"^(Supported|Unsupported|Inconclusive)$")
    evidence: str


class FactCheckReport(BaseModel):
    verdicts: list[ClaimVerdict] = Field(default_factory=list)
    overall_confidence: float = Field(ge=0.0, le=1.0)


_VERDICT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict fact-checker. Given a claim and supporting evidence, "
     "decide one of: Supported, Unsupported, Inconclusive.\n"
     "  • Supported = the evidence directly states or strongly implies the claim.\n"
     "  • Unsupported = the evidence contradicts the claim.\n"
     "  • Inconclusive = the evidence is silent on the claim.\n"
     "Quote a short snippet from the evidence as your justification.\n\n"
     "Output schema: return JSON with 'verdict' (one of the three labels above, "
     "exactly as spelled) and 'evidence' (a short string snippet from the input)."),
    ("human",
     "Claim: {claim}\n\nEvidence:\n{evidence}"),
])


class _SingleVerdict(BaseModel):
    """Schema the verdict-LLM is forced into."""
    verdict: str = Field(
        pattern=r"^(Supported|Unsupported|Inconclusive)$",
        description="Exactly one of: Supported, Unsupported, Inconclusive",
    )
    evidence: str = Field(
        description="A short quoted snippet from the evidence justifying the verdict",
    )


_embedder = None
_pinecone_index = None
_verdict_llm = None


def _lazy_init():
    """Module-level singletons; lets unit tests monkeypatch."""
    global _embedder, _pinecone_index, _verdict_llm
    if _embedder is None:
        _embedder = BedrockEmbeddings(
            model_id=os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
            region_name=os.environ["AWS_REGION"],
        )
    if _pinecone_index is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _pinecone_index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
    if _verdict_llm is None:
        _verdict_llm = ChatBedrock(
            model_id=os.environ.get(
                "FACT_CHECK_MODEL_ID",
                "anthropic.claude-3-haiku-20240307-v1:0",
            ),
            region_name=os.environ["AWS_REGION"],
            model_kwargs={"max_tokens": 256, "temperature": 0.0},
        )


def _split_into_claims(answer: str) -> list[str]:
    """Heuristic claim extraction — split on sentence boundaries."""
    sentences = re.split(r"(?<=[.!?])\s+", answer.strip())
    return [s for s in sentences if len(s) > 20]


def _verify_claim(claim: str) -> ClaimVerdict:
    query_vec = _embedder.embed_query(claim)
    raw = _pinecone_index.query(
        vector=query_vec, top_k=3,
        namespace="fact-check-sources",
        include_metadata=True,
    )
    matches = raw.get("matches", []) if isinstance(raw, dict) else raw["matches"]
    if not matches:
        return ClaimVerdict(claim=claim, verdict="Inconclusive",
                            evidence="No supporting documents found.")

    evidence_block = "\n\n---\n\n".join(
        m["metadata"].get("content", "") for m in matches
    )
    chain = _VERDICT_PROMPT | _verdict_llm.with_structured_output(_SingleVerdict)
    out: _SingleVerdict = chain.invoke({"claim": claim, "evidence": evidence_block})
    return ClaimVerdict(claim=claim, verdict=out.verdict, evidence=out.evidence)


def fact_checker_node(state: ResearchState) -> dict:
    """Verify each claim from the Analyst's answer; emit a confidence-weighted report."""
    _lazy_init()
    log = ["[fact_checker] starting verification"]

    analysis = state.get("analysis") or {}
    answer = analysis.get("answer", "")
    claims = _split_into_claims(answer)
    log.append(f"[fact_checker] extracted {len(claims)} claims")

    if not claims:
        report = FactCheckReport(verdicts=[], overall_confidence=0.0)
        return {
            "fact_check_report": report.model_dump(),
            "confidence_score": 0.0,
            "needs_hitl": True,
            "scratchpad": log + ["[fact_checker] no claims, escalating to HITL"],
        }

    verdicts = [_verify_claim(c) for c in claims]
    counts = {"Supported": 0, "Unsupported": 0, "Inconclusive": 0}
    for v in verdicts:
        counts[v.verdict] = counts.get(v.verdict, 0) + 1

    # Confidence = (supported - unsupported) / total, clamped to [0, 1].
    total = max(len(verdicts), 1)
    raw = (counts["Supported"] - counts["Unsupported"]) / total
    overall = max(0.0, min(1.0, raw))

    threshold = float(os.environ.get("HITL_CONFIDENCE_THRESHOLD", 0.6))
    needs_hitl = overall < threshold or counts["Unsupported"] > 0

    report = FactCheckReport(verdicts=verdicts, overall_confidence=overall)
    log.append(
        f"[fact_checker] supported={counts['Supported']}, "
        f"unsupported={counts['Unsupported']}, inconclusive={counts['Inconclusive']}, "
        f"overall={overall:.2f}, hitl={needs_hitl}"
    )

    return {
        "fact_check_report": report.model_dump(),
        "confidence_score": overall,
        "needs_hitl": needs_hitl,
        "scratchpad": log,
    }
```

> **Field descriptions + an explicit "Output schema" line in the prompt** show up here for the same reason as in [Phase 05](05-Analyst-Agent.md) — Haiku-3 is the recommended model for this node and its structured-output reliability is fragile without both reinforcements. If you keep seeing `pydantic_core.ValidationError` on `_SingleVerdict`, set `FACT_CHECK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0` in `.env`. (`FACT_CHECK_MODEL_ID` is read separately from `BEDROCK_MODEL_ID` so you can keep the Analyst on Sonnet and still try Haiku here.)

## 6.5 Where the actual interrupt happens

Note that `fact_checker_node` only **records** that HITL is needed (`"needs_hitl": True`). The graph-level `interrupt()` call is in the Supervisor's critique node — see Phase 07. Putting the interrupt there (not here) keeps the policy ("when do we stop?") separate from the evidence ("what did we find?").

## 6.6 Time Travel — the LangGraph mechanic

LangGraph's `Time Travel` requires:

1. The graph compiled with a checkpointer (we'll use `MemorySaver` in dev, `DynamoDBSaver` for Lambda).
2. Every `invoke` call passing a `config={"configurable": {"thread_id": "..."}}`.
3. To rewind: call `graph.update_state(config, values, as_node="<node_name>")` — this drops a new checkpoint that re-enters the graph from that node.

You'll wire the checkpointer in Phase 07. The fact-checker doesn't have to do anything special — checkpoints are automatic.

## 6.7 Verify

Save the snippet below as `scratch_factcheck.py` at the **project root** (not inside `agents/` — relative imports break from inside the package).

```python
import os
from dotenv import load_dotenv
load_dotenv()                                    # must run BEFORE agent imports

from agents.retriever import retriever_node
from agents.analyst import analyst_node
from agents.fact_checker import fact_checker_node

state = {
    "question": "Question your corpus can answer.",
    "plan": ["Question your corpus can answer."],
    "current_subtask_index": 0,
}
state.update(retriever_node(state))
state.update(analyst_node(state))
state.update(fact_checker_node(state))

print("Overall confidence:", state["confidence_score"])
print("Needs HITL:", state["needs_hitl"])
for v in state["fact_check_report"]["verdicts"]:
    print(f"  [{v['verdict']}] {v['claim'][:60]}...")
```

```bash
python scratch_factcheck.py
```

> **Why `load_dotenv()` first.** The agent modules read environment variables (`AWS_REGION`, `PINECONE_API_KEY`, etc.) when their clients are constructed. Even with the lazy-init pattern from Phase 04, the env vars need to be present by the time the first node runs. Calling `load_dotenv()` *after* the agent imports is fine for lazy-init code, but putting it first is the safe habit — it works regardless of whether a given module does eager or lazy construction.

You should see one verdict per claim. If everything is `Inconclusive`, your `fact-check-sources` namespace is too small or off-topic — add a few directly relevant documents.

---

Continue to [07-Supervisor-Graph.md](07-Supervisor-Graph.md).
