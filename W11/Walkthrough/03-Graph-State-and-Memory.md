# Phase 03 — Graph State and Memory

**Goal:** lock down the **shared data contract** that every node will read from and write to, and stand up the cross-thread Store interface.

This phase is short on lines of code but high on impact. The single most common LangGraph bug is "node B can't see what node A wrote because the field is missing from `ResearchState`". Define the schema fully *now*.

You will edit:
- `agents/state.py` — extend `ResearchState`
- `memory/store.py` — implement Store-backed user prefs and history

---

## 3.1 Why TypedDict and not a class?

LangGraph treats the state as a **dict-like object that gets merged at every node**. Each node returns a partial dict, and LangGraph shallow-merges that dict into the running state. A `TypedDict` gives you type hints without breaking that protocol.

A common follow-up question: *"What if I want a list field to append rather than overwrite?"* Use `Annotated[list, operator.add]` — LangGraph reads the annotation and applies the reducer on merge. We use that for `scratchpad` and `plan_status` below.

## 3.2 Extending `ResearchState`

The fields the README spec calls out are already present, but a few are missing for HITL/critique to work cleanly. Replace the `ResearchState` body in `agents/state.py` with:

```python
from typing import Annotated, TypedDict
from operator import add


class ResearchState(TypedDict, total=False):
    """Shared state for the Supervisor graph.

    `total=False` lets nodes return partial dicts without LangGraph
    complaining about missing keys.
    """
    # --- inputs ---
    question: str
    user_id: str

    # --- planner output ---
    plan: list[str]
    current_subtask_index: int

    # --- retrieval / analysis / verification ---
    retrieved_chunks: list[dict]
    analysis: dict                  # serialized AnalysisResult
    fact_check_report: dict         # serialized FactCheckReport

    # --- loop control ---
    confidence_score: float
    iteration_count: int
    needs_hitl: bool                # True → critique routes to HITL interrupt

    # --- observability — uses the `add` reducer so each node APPENDS ---
    scratchpad: Annotated[list[str], add]
```

Two important details:
- `total=False` means every key is optional. Without it, LangGraph errors out when the planner returns just `{"plan": [...]}`.
- `Annotated[list[str], add]` makes `scratchpad` accumulate. Without the reducer, every node's scratchpad write would overwrite the prior one.

## 3.3 The Store interface — what it actually does

LangGraph's `Store` is a key-value store that lives **outside any single graph thread**. A "thread" in LangGraph terms is one conversation; the Store survives across them.

- **Namespace** — a tuple, e.g. `("users", "alice")`. Acts like a folder.
- **Key** — a string within that namespace, e.g. `"preferences"`.
- **Value** — any JSON-serializable dict.

For development you'll use `InMemoryStore`. The exact same interface works against a Postgres-backed store in production (`PostgresStore`) — that's the whole point of the abstraction.

## 3.4 `memory/store.py` reference implementation

Replace the four stubs with:

```python
from langgraph.store.memory import InMemoryStore

# Module-level singleton — one Store across the whole process.
# In Lambda you would swap this for PostgresStore so memory survives
# between invocations.
_store = InMemoryStore()

DEFAULT_PREFERENCES = {
    "verbosity": "normal",         # "concise" | "normal" | "verbose"
    "trusted_sources": [],
}


def get_user_preferences(user_id: str) -> dict:
    """Read prefs for a user, or return defaults if absent."""
    namespace = ("users", user_id)
    item = _store.get(namespace, "preferences")
    return item.value if item else dict(DEFAULT_PREFERENCES)


def save_user_preferences(user_id: str, preferences: dict) -> None:
    """Overwrite the preferences blob for this user."""
    _store.put(("users", user_id), "preferences", preferences)


def get_query_history(user_id: str, limit: int = 5) -> list[str]:
    """Return the most recent N queries this user has asked.

    History is stored as a single list under one key — fine for a few
    thousand entries; switch to per-query keys + a search index past that.
    """
    item = _store.get(("users", user_id, "history"), "queries")
    if not item:
        return []
    return item.value[-limit:]


def append_query(user_id: str, question: str) -> None:
    """Append `question` to this user's history."""
    namespace = ("users", user_id, "history")
    item = _store.get(namespace, "queries")
    history = item.value if item else []
    history.append(question)
    _store.put(namespace, "queries", history)
```

## 3.5 Verify

A quick REPL check:

```python
from memory.store import (
    save_user_preferences, get_user_preferences,
    append_query, get_query_history,
)

save_user_preferences("alice", {"verbosity": "verbose", "trusted_sources": ["nytimes.com"]})
print(get_user_preferences("alice"))
# → {'verbosity': 'verbose', 'trusted_sources': ['nytimes.com']}

append_query("alice", "What is the GDP of France?")
append_query("alice", "What is the population of France?")
print(get_query_history("alice"))
# → ['What is the GDP of France?', 'What is the population of France?']

print(get_user_preferences("bob"))
# → defaults
```

If all four operations work, you have a usable Store. We will plug it into the Planner in Phase 07 (the Planner reads history + prefs to do dynamic few-shot prompting).

---

Continue to [04-Retriever-Agent.md](04-Retriever-Agent.md).
