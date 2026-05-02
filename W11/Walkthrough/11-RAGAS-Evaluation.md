# Phase 11 — RAGAS Evaluation

**Goal:** produce a quantitative quality report on at least 10 question/answer/context triples (NFR-1) using RAGAS metrics.

You will:
1. Replace the placeholder `data/golden_dataset.json` with real entries.
2. Implement `generate_predictions` and `run_ragas_evaluation` in `scripts/evaluate.py`.
3. Run the pipeline and capture the scores in your project documentation.

---

## 11.1 Building a credible Golden Dataset

Each entry needs:
- `question` — a question your corpus actually contains evidence for.
- `ground_truth_answer` — the answer **you** wrote, derived from the corpus, with citations.
- `ground_truth_contexts` — the *exact* passage(s) that support the answer.

Aim for 10–20 entries that span:
- ≥3 simple lookup questions (one fact, one source).
- ≥3 multi-hop questions (require combining two passages).
- ≥2 questions where the corpus does NOT have the answer (the system should produce low confidence).
- ≥2 ambiguous/contested questions (tests fact-checker's `Inconclusive` path).

Replace `data/golden_dataset.json` with at least 10 real entries:

```json
[
  {
    "question": "When did Apollo 11 land on the moon?",
    "ground_truth_answer": "Apollo 11's lunar module Eagle landed on July 20, 1969 at 20:17 UTC.",
    "ground_truth_contexts": [
      "On July 20, 1969, the lunar module Eagle, with Neil Armstrong and Buzz Aldrin aboard, landed in the Sea of Tranquility at 20:17 UTC."
    ]
  }
]
```

> Don't fabricate contexts. RAGAS faithfulness compares the generated answer to the *retrieved* contexts, but context_precision compares the *retrieved* contexts to the *ground-truth* contexts you supply here. Garbage in, garbage out.

## 11.2 The RAGAS metrics in plain English

| Metric | Question it answers | High score means |
|---|---|---|
| **Faithfulness** | Does the answer actually follow from the retrieved context? | No hallucination. |
| **Answer Relevancy** | Does the answer address the question (vs. drifting)? | The model stayed on topic. |
| **Context Precision** | Of the chunks the retriever returned, how many were actually relevant? | Good ranking. |
| (optional) **Context Recall** | How much of the necessary evidence was retrieved at all? | Good coverage. |

The README requires the first three. Adding `context_recall` is essentially free and gives you a more honest picture — include it if you have time.

## 11.3 Implementation — `scripts/evaluate.py`

Replace the bodies of `generate_predictions` and `run_ragas_evaluation`.

```python
from datasets import Dataset                           # pip install datasets
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

from agents.supervisor import build_supervisor_graph


def generate_predictions(dataset: list[dict]) -> list[dict]:
    """Run the Supervisor graph on every golden question, capture answer + contexts."""
    graph = build_supervisor_graph()
    out = []
    for i, entry in enumerate(dataset):
        config = {"configurable": {"thread_id": f"eval-{i}"}}
        try:
            result = graph.invoke(
                {"question": entry["question"], "user_id": "evaluator"},
                config=config,
            )
        except Exception as e:
            print(f"  [warn] entry {i} failed: {e}")
            out.append({"question": entry["question"], "answer": "", "contexts": []})
            continue
        analysis = result.get("analysis", {}) or {}
        contexts = [c["content"] for c in result.get("retrieved_chunks", [])]
        out.append({
            "question": entry["question"],
            "answer": analysis.get("answer", ""),
            "contexts": contexts,
            "ground_truth": entry["ground_truth_answer"],
        })
        print(f"  [{i+1}/{len(dataset)}] done")
    return out


def run_ragas_evaluation(predictions: list[dict], golden: list[dict]) -> dict:
    """Score predictions with RAGAS — faithfulness, relevancy, precision."""
    ds = Dataset.from_list(predictions)
    result = evaluate(
        ds,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )
    # `result` is a RAGASResult; `.to_pandas()` gives per-row, but we want
    # the aggregate summary as a flat dict.
    return {k: float(v) for k, v in result._scores_dict.items()}
```

> The exact RAGAS API moves between minor versions. If `_scores_dict` changes name in your installed version, `print(result)` and read what attributes it exposes — typically `.to_pandas().mean()` works as a fallback.

## 11.4 Run it

```bash
python scripts/evaluate.py --golden-dataset ./data/golden_dataset.json
```

Sample output:

```
📊 RAGAS Evaluation Results:
----------------------------------------
  faithfulness              0.8214
  answer_relevancy          0.7890
  context_precision         0.6321
----------------------------------------
```

## 11.5 What "good" looks like

For a small RAG system over a focused corpus, target:
- **Faithfulness ≥ 0.80** — most claims supported by context.
- **Answer Relevancy ≥ 0.75** — answers stay on-topic.
- **Context Precision ≥ 0.60** — re-ranker is doing its job.

Below those, common fixes:
- Faithfulness low → tighten the Analyst system prompt; raise temperature penalty for off-context speculation.
- Relevancy low → planner's sub-tasks may be too broad; ask the planner for more specific phrasings.
- Precision low → bump `top_k`, sharpen the re-ranker, or raise `chunk_size` so each chunk is more self-contained.

## 11.6 Save the report

Capture the scores in your README or a `reports/ragas-YYYY-MM-DD.md` file. The rubric requires the scores to be reported as part of the documentation, so keep at least one snapshot in the repo.

Tip: `evaluate(...).to_pandas().to_markdown()` produces a copy-paste-ready per-row table for your final write-up.

---

Continue to [12-Lambda-Deployment.md](12-Lambda-Deployment.md).
