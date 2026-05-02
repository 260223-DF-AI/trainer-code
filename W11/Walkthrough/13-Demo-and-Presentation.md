# Phase 13 — Demo and Presentation

**Goal:** wrap the deliverables and produce a clear 10-minute presentation that hits every rubric item.

---

## 13.1 Final deliverables checklist

Cross-reference these with the README's checklist before submitting.

- [ ] All 13 stub functions filled in; `pytest tests/ -v` is green.
- [ ] Both Pinecone namespaces populated (`primary-corpus`, `fact-check-sources`).
- [ ] `python main.py --question "..."` produces a structured answer with citations and confidence.
- [ ] Golden dataset has 10+ real entries (not the placeholder).
- [ ] RAGAS report stored in repo (e.g., `reports/ragas-YYYY-MM-DD.md`).
- [ ] AWS Lambda + API Gateway deployed (or a local SAM run if cost is a concern; demo from `sam local start-api`).
- [ ] README updated with: how to ingest, how to run, how to evaluate, how to deploy.
- [ ] Recorded or live 10-minute demo.

## 13.2 README updates

The committed `README.md` is the spec — keep it untouched as a contract. Add a *Project Notes* section at the bottom (or a separate `RUN.md`) covering:

- Which corpus you used and why.
- Your final RAGAS scores with a brief commentary on what you'd improve next.
- Any deviations from the spec (e.g., "used Haiku instead of Sonnet for cost", "skipped streaming because…") and the reasoning.
- Cost notes: rough $ spent during dev, biggest line items.

## 13.3 Demo script (10 minutes)

A concrete plan:

| Minute | What to show | Why it lands |
|---|---|---|
| 0:00 – 1:00 | The problem statement and the multi-agent shape (architecture diagram from the README). | Sets up "why three agents not one". |
| 1:00 – 3:00 | Live `python main.py --question "..."` on a known-good question. Show the scratchpad. | Concrete proof the graph runs end-to-end. |
| 3:00 – 4:00 | `python main.py --question "..."` on a question your corpus *can't* answer — show low confidence triggering HITL. Type `n` at the prompt to demo the rejection path. | Demonstrates HITL + critique loop. |
| 4:00 – 5:30 | Open `agents/supervisor.py` — walk through the planner → router → critique pattern; explain conditional edges and the `MemorySaver`. | Shows you understand the framework, not just `pip install`'d it. |
| 5:30 – 7:00 | Show `tests/test_supervisor.py` running green. Highlight that `NodeInterrupt` is asserted with no real Bedrock call. | Hits NFR-2 (mocked tests). |
| 7:00 – 8:30 | RAGAS scores on the golden dataset; briefly compare runs with different `MAX_REFINEMENT_ITERATIONS`. | Hits NFR-1. |
| 8:30 – 9:30 | `curl` the deployed API Gateway endpoint, show the JSON response. | Closes the deliverable. |
| 9:30 – 10:00 | "What I'd do next" — streaming, real LLM-based claim extraction, `PostgresStore` for cross-process memory. | Shows you know the limits of what you built. |

## 13.4 Talking points the rubric is likely to grade

Make sure you mention each of these explicitly:

- **Adaptive RAG.** Your retriever picks namespaces based on context (primary vs fact-check); the planner decides *whether* a sub-task needs retrieval at all.
- **Plan-and-Execute.** Planner produces a sub-task list; the graph executes them in turn.
- **Critique Node + self-refinement.** Loop bound by `MAX_REFINEMENT_ITERATIONS`; demonstrate one retry actually happening.
- **HITL with Time Travel.** `NodeInterrupt` + `graph.update_state(...)` resumes from a checkpoint.
- **Cross-thread memory.** `Store` namespaces; show `get_query_history` returning prior questions.
- **Structured output.** `AnalysisResult` Pydantic schema; show validation kicks in (introduce a typo into the prompt and demo the validation error).
- **PII masking + injection guardrails.** Demo a malicious-looking input being rejected.
- **Observability.** LangSmith link if you enabled it; otherwise the scratchpad serves the same purpose locally.

## 13.5 Pitfalls to avoid in the recording

- **Live LLM calls failing on stage.** Pre-record successful runs, or have a backup `--mock` flag that returns canned responses. A 30-second Bedrock cold-start kills the energy of a 10-minute demo.
- **Reading bullets verbatim.** Talk through the architecture diagram instead.
- **Claiming faithfulness > 0.95.** Reviewers will ask how. Honest 0.80 with a discussion of trade-offs reads much better.

## 13.6 Final commit hygiene

Before tagging your final commit:

```bash
ruff check .                  # lint
ruff format --check .         # formatting
pytest tests/ -v              # all green
sam validate --template-file deployment/template.yaml
```

Tag it:

```bash
git tag -a v1.0 -m "ResearchFlow v1.0 — final delivery"
git push origin v1.0
```

---

You're done. Walk through the [`Walkthrough/00-Overview.md`](00-Overview.md) one more time as a self-checklist, then submit.
