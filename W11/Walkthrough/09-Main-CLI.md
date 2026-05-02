# Phase 09 — Main CLI

**Goal:** wire everything together so `python main.py --question "..."` runs the full pipeline end-to-end with input/output sanitization and HITL handling.

You will fill in `main()` in `main.py`.

---

## 9.1 What `main` has to do

1. Load `.env`.
2. Sanitize and PII-mask the user's question.
3. Build the supervisor graph.
4. Invoke it with a `thread_id` so checkpoints are addressable.
5. If the run pauses on a `NodeInterrupt`, prompt the human reviewer at the terminal and resume.
6. Pretty-print the structured report (PII-masking the output too).

## 9.2 Reference implementation

Replace the body of `main()` in `main.py`. Add the imports:

```python
import json
import uuid

from langgraph.errors import GraphInterrupt

from agents.supervisor import build_supervisor_graph
from middleware.guardrails import detect_injection, sanitize_input
from middleware.pii_masking import mask_pii
```

Then the function body:

```python
def main() -> None:
    load_dotenv()
    args = parse_args()

    # --- 1) input boundary ---------------------------------------------------
    if detect_injection(args.question):
        print("Input rejected: possible prompt injection.")
        return
    question = mask_pii(sanitize_input(args.question))

    # --- 2) graph + addressable thread --------------------------------------
    graph = build_supervisor_graph()
    thread_id = f"cli-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "question": question,
        "user_id": args.user_id,
    }

    # --- 3) invoke, handling HITL interrupts --------------------------------
    try:
        result = graph.invoke(initial_state, config=config)
    except GraphInterrupt as interrupt:
        # NodeInterrupt percolates up wrapped in GraphInterrupt.
        print("\n=== HUMAN-IN-THE-LOOP REVIEW REQUIRED ===")
        print(f"Reason: {interrupt}")
        # Show the reviewer the current state so they can decide.
        snapshot = graph.get_state(config)
        analysis = snapshot.values.get("analysis", {})
        print("\nDraft answer:\n", analysis.get("answer", "<empty>"))
        decision = input("\nApprove answer as-is? [y/n]: ").strip().lower()
        if decision != "y":
            print("Rejected by reviewer. Aborting.")
            return
        # Override the state to mark approved, then resume.
        graph.update_state(config, {"needs_hitl": False, "confidence_score": 1.0})
        result = graph.invoke(None, config=config)

    # --- 4) output boundary --------------------------------------------------
    analysis = result.get("analysis", {})
    safe_answer = mask_pii(analysis.get("answer", ""))

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(safe_answer)
    print("\nCITATIONS")
    for c in analysis.get("citations", []):
        page = f", p.{c['page_number']}" if c.get("page_number") else ""
        print(f"  • {c['source']}{page}: {c.get('excerpt','')[:120]}")
    print(f"\nCONFIDENCE: {result.get('confidence_score', 0.0):.2f}")
    print(f"ITERATIONS: {result.get('iteration_count', 0)}")

    if args.verbose:
        print("\nSCRATCHPAD")
        for line in result.get("scratchpad", []):
            print(" ", line)

    if result.get("fact_check_report"):
        print("\nFACT-CHECK REPORT")
        for v in result["fact_check_report"]["verdicts"]:
            print(f"  [{v['verdict']}] {v['claim'][:80]}")
```

## 9.3 Why a fresh `thread_id` per CLI invocation?

- Without a thread_id, every run uses the default thread — checkpoints accumulate forever.
- With a fresh UUID per run, each CLI invocation has an isolated checkpoint history that can be replayed/inspected without colliding.
- For a "conversational" mode, you'd reuse the thread_id across questions — that's how the Store-backed history becomes useful.

## 9.4 Verify

```bash
python main.py --question "A real question your corpus can answer." --verbose
```

You should see the answer, citations, confidence, iteration count, and a full scratchpad trace. The first run typically takes 8–15 seconds (model loading + Bedrock + Pinecone). Subsequent runs in the same process would be faster, but each `python main.py` invocation is cold.

If a run trips the HITL interrupt, you'll see an interactive prompt — type `y` to accept and continue, anything else to abort.

---

Continue to [10-Testing.md](10-Testing.md).
