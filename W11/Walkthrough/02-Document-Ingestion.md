# Phase 02 — Document Ingestion Pipeline

**Goal:** turn a directory of PDFs/text files into vectors in Pinecone, partitioned into the **two** namespaces the system requires.

You will fill in four functions in `scripts/ingest.py`:

| Function | Job |
|---|---|
| `load_documents` | Read PDF + `.txt` files into LangChain `Document` objects |
| `chunk_documents` | Split with `RecursiveCharacterTextSplitter` |
| `generate_embeddings` | Batch-embed with Bedrock Titan Embeddings V2 |
| `upsert_to_pinecone` | Push vectors + metadata under the chosen namespace |

> Keep the two corpora **separate**. The Fact-Checker's verification only means something if it queries an *independent* source set from the Retriever (FR-1, FR-5).

---

## 2.1 Why batched embeddings?

Bedrock's embedding endpoint is one HTTP call per text — there is no batch endpoint. For a few hundred chunks, sequential calls finish in under a minute and `BedrockEmbeddings.embed_documents` handles the loop for you. For larger corpora, wrap it in a `concurrent.futures.ThreadPoolExecutor` (~8 workers) to overlap network latency. Don't go too wide or you'll trip Bedrock's per-region throughput limits.

## 2.2 Why store rich metadata?

Pinecone returns metadata alongside each match. The Analyst uses it to produce citations (`source` + `page_number`). Without metadata at ingestion time, you have no way to cite later — you just get a vector ID and content.

## 2.3 Reference implementation

Copy this into `scripts/ingest.py`, replacing the four stub bodies. Imports go at the top of the file.

```python
import datetime
import hashlib
from pathlib import Path

from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone


def load_documents(input_dir: str) -> list:
    """Walk a directory and load every PDF and .txt file as Document objects.

    PyPDFLoader returns one Document per page (page_number lives in
    metadata['page']). TextLoader returns a single Document for the whole file,
    so we synthesize a page_number = 1 to keep the schema uniform.
    """
    docs = []
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    for path in root.rglob("*"):
        if path.suffix.lower() == ".pdf":
            for page_doc in PyPDFLoader(str(path)).load():
                page_doc.metadata["source"] = path.name
                page_doc.metadata["page_number"] = page_doc.metadata.get("page", 0) + 1
                docs.append(page_doc)
        elif path.suffix.lower() in (".txt", ".md"):
            for d in TextLoader(str(path), encoding="utf-8").load():
                d.metadata["source"] = path.name
                d.metadata["page_number"] = 1
                docs.append(d)

    print(f"Loaded {len(docs)} document pages from {input_dir}")
    return docs


def chunk_documents(documents: list) -> list:
    """Split each Document into ~800-character chunks with 100-char overlap.

    Overlap reduces the chance that a single fact gets split across the chunk
    boundary in a way that hurts retrieval recall.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    timestamp = datetime.datetime.utcnow().isoformat()
    for doc in documents:
        for i, sub in enumerate(splitter.split_documents([doc])):
            # Deterministic ID — re-running ingestion overwrites instead of
            # bloating the index with duplicates.
            raw_id = f"{sub.metadata['source']}::{sub.metadata['page_number']}::{i}"
            sub.metadata["chunk_id"] = hashlib.md5(raw_id.encode()).hexdigest()
            sub.metadata["timestamp"] = timestamp
            chunks.append(sub)

    print(f"Split into {len(chunks)} chunks")
    return chunks


def generate_embeddings(chunks: list) -> list:
    """Embed every chunk's text via Bedrock Titan Embeddings V2.

    Returns a list of (vector_id, embedding, metadata) tuples ready for upsert.
    The embedding model dimension MUST match your Pinecone index dimension —
    Titan Embeddings V2 is 1024-dim by default.
    """
    embedder = BedrockEmbeddings(
        model_id=os.environ.get("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        region_name=os.environ["AWS_REGION"],
    )
    texts = [c.page_content for c in chunks]
    vectors = embedder.embed_documents(texts)

    out = []
    for chunk, vec in zip(chunks, vectors):
        # Pinecone metadata must be JSON-scalar-compatible — coerce.
        metadata = {
            "content": chunk.page_content,           # store the text for retrieval
            "source": chunk.metadata["source"],
            "page_number": int(chunk.metadata["page_number"]),
            "chunk_id": chunk.metadata["chunk_id"],
            "timestamp": chunk.metadata["timestamp"],
        }
        out.append((chunk.metadata["chunk_id"], vec, metadata))
    return out


def upsert_to_pinecone(embeddings: list, namespace: str) -> None:
    """Upsert in batches of 100 — Pinecone's recommended cap per request."""
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

    BATCH = 100
    for start in range(0, len(embeddings), BATCH):
        batch = embeddings[start:start + BATCH]
        vectors = [
            {"id": vid, "values": vec, "metadata": meta}
            for vid, vec, meta in batch
        ]
        index.upsert(vectors=vectors, namespace=namespace)
    print(f"Upserted {len(embeddings)} vectors into namespace '{namespace}'")
```

> Note the existing `import os` at the top of `scripts/ingest.py` — you do not need to add it again.

## 2.4 Build a tiny corpus

For development you can drop a few small text files into `data/corpus/` and `data/fact_check/`:

```bash
mkdir -p data/fact_check
# put PDFs or .txt files in data/corpus/ and data/fact_check/
```

If you have nothing handy, public-domain Wikipedia exports work well. Pick a topic narrow enough that the Analyst can actually answer questions (e.g. "the Apollo program") rather than the whole encyclopedia.

## 2.5 Run the pipeline twice — once per namespace

```bash
python scripts/ingest.py --input-dir ./data/corpus --namespace primary-corpus
python scripts/ingest.py --input-dir ./data/fact_check --namespace fact-check-sources
```

## 2.6 Verify

In a Python REPL:

```python
import os
from dotenv import load_dotenv
load_dotenv()
from pinecone import Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
stats = pc.Index(os.environ["PINECONE_INDEX_NAME"]).describe_index_stats()
print(stats)
```

You should see two namespaces with non-zero `vector_count`:

```
{'namespaces': {'primary-corpus':       {'vector_count': 314},
                'fact-check-sources':   {'vector_count': 198}}, ...}
```

If both are present and non-zero, ingestion is good.

---

Continue to [03-Graph-State-and-Memory.md](03-Graph-State-and-Memory.md).
