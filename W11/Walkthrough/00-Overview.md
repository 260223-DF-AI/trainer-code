# ResearchFlow — Implementation Walkthrough

This walkthrough takes you from the empty scaffold (every function raises `NotImplementedError`) to a fully working multi-agent research assistant deployed on AWS Lambda. It is designed for someone who has built simple LangChain RAG apps with Pinecone and Bedrock, but has not yet used **LangGraph**, **structured output**, or **multi-agent orchestration**.

> The code blocks below are *examples* — you can copy them into the existing stub functions almost verbatim. The walkthrough deliberately does **not** modify any project code; you do that yourself, file by file, as you learn.

---

## How to use this walkthrough

1. Read each phase top-to-bottom **before** typing anything. Each phase ends with a "Verify" section so you know the work is good before moving on.
2. Copy the example code blocks into the corresponding stub function. Read the comments — they explain *why* each piece exists.
3. Run the "Verify" command. If it fails, don't move on. Fix it first.
4. Commit after each phase. You should end up with about 13 well-scoped commits.

---

## Recommended order

| # | File | Phase | Why this order? |
|---|---|---|---|
| 01 | `01-Setup-and-Environment.md` | Local environment, AWS credentials, Pinecone index | Nothing else works without this |
| 02 | `02-Document-Ingestion.md` | `scripts/ingest.py` → load PDF/text → chunk → embed → upsert | The agents need data to retrieve |
| 03 | `03-Graph-State-and-Memory.md` | `agents/state.py` + `memory/store.py` | The "shared contract" the rest of the code reads/writes |
| 04 | `04-Retriever-Agent.md` | `agents/retriever.py` | First agent — exercises Pinecone end-to-end |
| 05 | `05-Analyst-Agent.md` | `agents/analyst.py` + Pydantic structured output | First Bedrock call with schema enforcement |
| 06 | `06-FactChecker-Agent.md` | `agents/fact_checker.py` + HITL interrupt | Final agent — closes the loop |
| 07 | `07-Supervisor-Graph.md` | `agents/supervisor.py` — planner, router, critique, `StateGraph` | Wires the agents together |
| 08 | `08-Middleware.md` | `middleware/pii_masking.py` + `middleware/guardrails.py` | Defense-in-depth for inputs/outputs |
| 09 | `09-Main-CLI.md` | `main.py` | End-to-end local run |
| 10 | `10-Testing.md` | All `tests/test_*.py` | Mocked unit tests for FR/NFR sign-off |
| 11 | `11-RAGAS-Evaluation.md` | `data/golden_dataset.json` + `scripts/evaluate.py` | NFR-1 evaluation gate |
| 12 | `12-Lambda-Deployment.md` | `deployment/app.py` + `template.yaml` + `deploy.sh` | Serverless rollout |
| 13 | `13-Demo-and-Presentation.md` | Recording + slides | Deliverable wrap-up |

---

## Mental model — what you are actually building

You already know how to build a single-call RAG app:

```
question → embed → Pinecone.query → stuff context into prompt → Bedrock.invoke → answer
```

ResearchFlow is the same idea, but with **three specialist LLM calls** orchestrated by a **graph** that can loop and self-correct:

```
                     ┌──── retriever (Pinecone primary-corpus)
question → planner ──┼──── analyst   (Bedrock + structured output)
                     └──── fact_checker (Pinecone fact-check-sources)
                                │
                                ▼
                          critique loop
                       (accept / retry / HITL)
```

The **graph** is just a Python function that takes a `ResearchState` dict, decides which node to call next, and updates the dict. LangGraph adds three things on top:
- **Conditional edges** — pick the next node by inspecting the state (this is the `router`).
- **Checkpointing** — save state at each node so a human reviewer can rewind ("Time Travel").
- **Interrupts** — pause the graph, return control to the caller, and resume on demand (this is HITL).

If you understand those three things you can build the rest. The walkthrough explains each one in the phase where it first matters.

---

## A note on cost

Bedrock Claude calls and Pinecone serverless queries both cost money. The whole walkthrough will fit comfortably in single-digit dollars if you:

- Use **Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`) instead of Sonnet for the Analyst while developing.
- Cap `MAX_REFINEMENT_ITERATIONS=2` while testing.
- Mock Bedrock and Pinecone in unit tests (Phase 10) — never hit live services from `pytest`.
- Tear down the SAM stack (`sam delete --stack-name researchflow`) when you are done with deployment.

---

Continue to [01-Setup-and-Environment.md](01-Setup-and-Environment.md).
