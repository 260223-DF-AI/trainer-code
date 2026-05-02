# Phase 10 — Unit Tests with Mocks

**Goal:** ship a test suite that runs **without any live cloud calls** (NFR-2) and validates the contracts each agent has with the rest of the system.

You will fill in:
- `tests/test_retriever.py`
- `tests/test_analyst.py`
- `tests/test_supervisor.py`

The test stubs are already organized one-class-per-module.

---

## 10.1 Mocking strategy

Three external surfaces to mock:

| Surface | Where to patch |
|---|---|
| Pinecone client | `agents.retriever._pinecone_index`, `agents.fact_checker._pinecone_index` |
| Bedrock chat | the `ChatBedrock` import inside the agent module — patch `agents.analyst.ChatBedrock`, etc. |
| Sub-agent functions | `agents.supervisor.retriever_node` etc. (router tests) |

Use `monkeypatch` (pytest's built-in) for module-level singletons; `unittest.mock.patch` for classes.

## 10.2 `tests/test_retriever.py`

Replace each `pass` body. You can either keep the existing class or add a `pytest` `conftest.py` fixture for the mock — class-method form below to match the scaffold.

```python
from unittest.mock import patch, MagicMock

import pytest


def _fake_match(content, score, source="doc.pdf", page=1):
    return {"id": f"id-{content[:5]}",
            "score": score,
            "metadata": {"content": content, "source": source, "page_number": page}}


class TestRetrieverAgent:

    def _patched_index(self, matches):
        index = MagicMock()
        index.query.return_value = {"matches": matches}
        return index

    def test_returns_structured_chunks(self, monkeypatch):
        from agents import retriever
        monkeypatch.setattr(
            retriever, "_get_index",
            lambda: self._patched_index([
                _fake_match("Apollo 11 landed on the Moon in 1969.", 0.91),
                _fake_match("Apollo 13 had an oxygen tank failure.",     0.87),
            ]),
        )
        out = retriever.retriever_node({
            "question": "When did Apollo 11 land?",
            "plan": ["When did Apollo 11 land?"],
            "current_subtask_index": 0,
        })
        assert "retrieved_chunks" in out
        assert len(out["retrieved_chunks"]) >= 1
        for c in out["retrieved_chunks"]:
            for k in ("content", "relevance_score", "source", "page_number"):
                assert k in c

    def test_applies_reranking(self, monkeypatch):
        from agents import retriever
        # Pinecone returns the WRONG order; rerank should reshuffle.
        monkeypatch.setattr(
            retriever, "_get_index",
            lambda: self._patched_index([
                _fake_match("Completely unrelated text about gardening.", 0.99),
                _fake_match("Apollo 11 landed on the Moon in July 1969.", 0.10),
            ]),
        )
        out = retriever.retriever_node({
            "question": "When did Apollo 11 land?",
            "plan": ["When did Apollo 11 land?"],
            "current_subtask_index": 0,
        })
        # Top-1 after rerank should be the actually-relevant chunk.
        assert "Apollo" in out["retrieved_chunks"][0]["content"]

    def test_applies_context_compression(self, monkeypatch):
        from agents import retriever
        long = ". ".join([f"Sentence {i} about Apollo." for i in range(20)])
        monkeypatch.setattr(
            retriever, "_get_index",
            lambda: self._patched_index([_fake_match(long, 0.9)]),
        )
        out = retriever.retriever_node({
            "question": "Apollo summary",
            "plan": ["Apollo summary"],
            "current_subtask_index": 0,
        })
        assert len(out["retrieved_chunks"][0]["content"]) < len(long)

    def test_handles_empty_results(self, monkeypatch):
        from agents import retriever
        monkeypatch.setattr(retriever, "_get_index", lambda: self._patched_index([]))
        out = retriever.retriever_node({
            "question": "anything",
            "plan": ["anything"],
            "current_subtask_index": 0,
        })
        assert out["retrieved_chunks"] == []
```

## 10.3 `tests/test_analyst.py`

The Analyst test patches `ChatBedrock` so no real Bedrock call fires. We make the chain return a pre-built `AnalysisResult`.

```python
from unittest.mock import MagicMock, patch
from agents.analyst import AnalysisResult, Citation


class TestAnalystAgent:

    def _stub_result(self):
        return AnalysisResult(
            answer="Apollo 11 landed on July 20, 1969 [1].",
            citations=[Citation(source="apollo.pdf", page_number=12,
                                excerpt="Apollo 11 landed on July 20, 1969.")],
            confidence=0.88,
        )

    def test_returns_validated_analysis_result(self):
        with patch("agents.analyst.ChatBedrock") as MockChat:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = self._stub_result()
            instance = MockChat.return_value
            instance.with_structured_output.return_value = mock_chain
            # The chain is _PROMPT | llm.with_structured_output(...) — make
            # the | operator return our chain.
            instance.with_structured_output.return_value.__ror__ = (
                lambda self_, other: mock_chain
            )

            from agents.analyst import analyst_node
            out = analyst_node({
                "question": "When did Apollo 11 land?",
                "plan": ["When did Apollo 11 land?"],
                "current_subtask_index": 0,
                "retrieved_chunks": [
                    {"content": "Apollo 11 landed on July 20, 1969.",
                     "source": "apollo.pdf", "page_number": 12,
                     "relevance_score": 9.1}
                ],
            })
        assert "analysis" in out
        assert out["confidence_score"] == 0.88
        assert out["analysis"]["citations"][0]["source"] == "apollo.pdf"

    def test_short_circuits_when_no_chunks(self):
        from agents.analyst import analyst_node
        out = analyst_node({
            "question": "x",
            "plan": ["x"],
            "current_subtask_index": 0,
            "retrieved_chunks": [],
        })
        assert out["confidence_score"] == 0.0
        assert out["analysis"]["citations"] == []
```

> The trick with `__ror__` patches the `_PROMPT | llm.with_structured_output(...)` pipe operator. If you'd rather avoid that, refactor `analyst_node` to call `chain = _build_chain()` and patch `_build_chain` directly.

## 10.4 `tests/test_supervisor.py`

Router and critique are pure-Python — no mocks needed for those. Planner needs `ChatBedrock` patched.

```python
import os
from unittest.mock import patch, MagicMock

import pytest
from langgraph.errors import NodeInterrupt


class TestSupervisorRouting:

    def test_router_selects_retriever(self):
        from agents.supervisor import router
        assert router({"plan": ["x"]}) == "retriever"

    def test_router_selects_analyst(self):
        from agents.supervisor import router
        assert router({
            "plan": ["x"],
            "retrieved_chunks": [{"content": "..."}],
        }) == "analyst"

    def test_router_selects_fact_checker(self):
        from agents.supervisor import router
        assert router({
            "plan": ["x"],
            "retrieved_chunks": [{"content": "..."}],
            "analysis": {"answer": "yes"},
        }) == "fact_checker"

    def test_critique_accepts_when_confidence_high(self, monkeypatch):
        monkeypatch.setenv("HITL_CONFIDENCE_THRESHOLD", "0.6")
        monkeypatch.setenv("MAX_REFINEMENT_ITERATIONS", "3")
        from agents.supervisor import critique_node, _critique_router
        out = critique_node({"confidence_score": 0.9, "iteration_count": 0,
                             "needs_hitl": False})
        # Should not raise.
        from langgraph.graph import END
        assert _critique_router({**out, "confidence_score": 0.9,
                                  "needs_hitl": False}) == END

    def test_critique_retries_when_confidence_low(self, monkeypatch):
        monkeypatch.setenv("HITL_CONFIDENCE_THRESHOLD", "0.6")
        monkeypatch.setenv("MAX_REFINEMENT_ITERATIONS", "3")
        from agents.supervisor import critique_node
        out = critique_node({"confidence_score": 0.3, "iteration_count": 0,
                             "needs_hitl": False})
        assert out["iteration_count"] == 1
        assert out["retrieved_chunks"] == []      # state was cleared for retry

    def test_critique_triggers_hitl_at_max_iter(self, monkeypatch):
        monkeypatch.setenv("HITL_CONFIDENCE_THRESHOLD", "0.6")
        monkeypatch.setenv("MAX_REFINEMENT_ITERATIONS", "2")
        from agents.supervisor import critique_node
        with pytest.raises(NodeInterrupt):
            critique_node({"confidence_score": 0.3, "iteration_count": 2,
                           "needs_hitl": True})
```

## 10.5 Run them

```bash
pytest tests/ -v
```

Target: all green, no network calls. If pytest hangs, something is hitting the real Pinecone/Bedrock — find which test and add the missing mock.

## 10.6 Optional — LangSmith evaluator harness

NFR-2 mentions validating against the Golden Dataset using LangSmith evaluators. Once Phase 11 is done, you can hook a LangSmith dataset into a `pytest` parametrize to run the same Q&A through the graph and assert RAGAS scores stay above a threshold:

```python
@pytest.mark.parametrize("entry", load_golden_dataset("data/golden_dataset.json"))
def test_golden_entry(entry):
    pytest.skip("integration; run separately with pytest -m integration")
```

Mark them `integration` and skip in default CI; run on demand.

---

Continue to [11-RAGAS-Evaluation.md](11-RAGAS-Evaluation.md).
