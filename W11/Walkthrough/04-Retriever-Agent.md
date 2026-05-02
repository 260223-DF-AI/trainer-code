# Phase 04 — Retriever Agent

**Goal:** turn the current sub-task into a ranked, compressed list of context chunks that the Analyst can synthesize from.

You will fill in `retriever_node` in `agents/retriever.py`. Two sub-skills come together here:

1. **Semantic search** — embed the sub-task, query Pinecone with metadata filtering.
2. **Context compression** — collapse over-long chunks down to the sentences that actually matter, so we don't waste Analyst tokens.

A third step — **re-ranking** the top-K candidates with a cross-encoder — meaningfully improves quality but adds a local PyTorch dependency we've intentionally avoided in favor of Bedrock embeddings. See "Optional: add a reranker" at the end of this phase if you want to plug one in later.

---

## 4.1 Pattern recap — what each step costs

| Step | Latency (rough) | Cost |
|---|---|---|
| Embed query (Bedrock Titan) | ~80 ms | ~$0.02 / 1M tokens |
| Pinecone query (top_k=10) | ~150 ms | tiny per-query fee |
| LLM-based compression | ~1 s | a Bedrock call per chunk if you go LLM-style |

For development we'll use a **rule-based** compressor (sentences whose embedding is closest to the query) so we don't fire 10 Bedrock calls per retrieval. Swap it for `ContextualCompressionRetriever` later if quality demands it.

## 4.2 Reference implementation

Replace the body of `retriever_node` with the code below. Add the imports at the top of the file.

```python
import os

from langchain_aws import BedrockEmbeddings
from pinecone import Pinecone

from agents.state import ResearchState

# Module-level singletons, lazily constructed on first use. Lazy init matters:
# both clients read env vars at construction time, so eager init at import time
# would force every caller (tests, scripts, Lambda cold start) to have AWS_REGION
# and PINECONE_API_KEY set *before* `from agents.retriever import ...` runs.
_embedder = None
_pinecone_index = None


def _get_embedder():
    """Lazy-init so unit tests can monkeypatch before first call."""
    global _embedder
    if _embedder is None:
        _embedder = BedrockEmbeddings(
            model_id=os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
            region_name=os.environ["AWS_REGION"],
        )
    return _embedder


def _get_index():
    """Lazy-init so unit tests can monkeypatch before first call."""
    global _pinecone_index
    if _pinecone_index is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _pinecone_index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
    return _pinecone_index


def _cos_sim(a: list[float], b: list[float]) -> float:
    """Cosine similarity for plain Python lists — avoids a numpy import."""
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _compress(chunk_text: str, query: str, max_sentences: int = 4) -> str:
    """Keep the sentences whose embedding is closest to the query.

    Cheap, deterministic, and good enough to halve token usage on long
    chunks. Replace with an LLM-based compressor if you need higher recall.
    """
    sentences = [s.strip() for s in chunk_text.split(". ") if s.strip()]
    if len(sentences) <= max_sentences:
        return chunk_text
    embedder = _get_embedder()
    query_vec = embedder.embed_query(query)
    sent_vecs = embedder.embed_documents(sentences)
    scores = [_cos_sim(query_vec, sv) for sv in sent_vecs]
    top = sorted(range(len(sentences)), key=lambda i: -scores[i])[:max_sentences]
    top.sort()                                      # preserve original order
    return ". ".join(sentences[i] for i in top)


def retriever_node(state: ResearchState) -> dict:
    """Retrieve and compress."""
    plan = state.get("plan", [])
    idx = state.get("current_subtask_index", 0)
    sub_task = plan[idx] if plan else state["question"]
    log = [f"[retriever] sub-task: {sub_task!r}"]

    # 1) embed + Pinecone semantic search ------------------------------------
    index = _get_index()
    query_vec = _get_embedder().embed_query(sub_task)
    raw = index.query(
        vector=query_vec,
        top_k=10,
        namespace="primary-corpus",
        include_metadata=True,
    )
    matches = raw.get("matches", []) if isinstance(raw, dict) else raw["matches"]
    log.append(f"[retriever] pinecone returned {len(matches)} candidates")

    if not matches:
        return {"retrieved_chunks": [], "scratchpad": log + ["[retriever] no matches"]}

    # 2) compress + structure ------------------------------------------------
    # Pinecone returns matches sorted by cosine score; take top 5.
    chunks = []
    for match in matches[:5]:
        meta = match["metadata"]
        chunks.append({
            "content": _compress(meta["content"], sub_task),
            "relevance_score": float(match.get("score", 0.0)),
            "source": meta.get("source", "unknown"),
            "page_number": meta.get("page_number"),
        })
    log.append(f"[retriever] kept top {len(chunks)} by Pinecone score")
    return {"retrieved_chunks": chunks, "scratchpad": log}
```

## 4.3 Why this pattern

- **`top_k=10` then narrow to 5.** Pinecone is fast; light over-fetch gives the compression step a few extra candidates to choose from without paying for chunks the Analyst will never see.
- **Compression after retrieval, not before.** You only want to spend compression effort on chunks that are actually going to the Analyst.
- **Observability.** Notice every interesting decision lands on `scratchpad`. The reducer in Phase 03 means these append rather than overwrite, so by the end of a run the scratchpad is a full execution trace.

### Optional: add a reranker

The cosine score Pinecone returns is fast but noisy. If retrieval quality looks weak after Phase 11's RAGAS run, slot a reranker between the Pinecone query and the compression step. Two production-friendly options:

- **Cohere Rerank via Bedrock** (`cohere.rerank-v3-5:0`) — keeps everything inside the AWS boundary, no extra dependencies, charged per query.
- **Local CrossEncoder** (`cross-encoder/ms-marco-MiniLM-L-6-v2`) — free at runtime but pulls `sentence-transformers` and `torch` back into the stack, which reintroduces the Windows/Lambda packaging problems we walked away from.

Either way, over-fetch (`top_k=20`) before reranking and narrow to 5 after.

## 4.4 Verify

You can drive `retriever_node` directly without the rest of the graph. Save as `scratch_retriever.py`:

```python
import os
from dotenv import load_dotenv
load_dotenv()

from agents.retriever import retriever_node

state = {
    "question": "Replace this with something your corpus actually contains.",
    "plan": ["Replace this with something your corpus actually contains."],
    "current_subtask_index": 0,
}
out = retriever_node(state)

print("Got", len(out["retrieved_chunks"]), "chunks")
for c in out["retrieved_chunks"]:
    print(f"  [{c['relevance_score']:.3f}] {c['source']}#p{c['page_number']}: "
          f"{c['content'][:80]}...")
```

```bash
python scratch_retriever.py
```

You should see up to 5 chunks with relevance scores between 0.0 and 1.0 (Pinecone cosine similarity) sorted descending. Delete the scratch file when satisfied.

---

Continue to [05-Analyst-Agent.md](05-Analyst-Agent.md).
