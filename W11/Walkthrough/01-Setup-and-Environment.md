# Phase 01 — Setup and Environment

**Goal:** every external dependency the project will use is reachable from your machine before you write a line of agent code.

You will:
1. Create a Python 3.11 virtual environment and install dependencies.
2. Provision a Pinecone serverless index.
3. Confirm AWS Bedrock model access in your region.
4. Fill in `.env`.
5. Smoke-test each external service with a one-liner.

---

## 1.1 Python virtual environment

The Lambda runtime is pinned to `python3.11` in `deployment/template.yaml`, so develop on the same version to avoid wheel/build mismatches.

```bash
# from the project root
python --version          # must report 3.11.x
python -m venv .venv
source .venv/Scripts/activate     # Git Bash on Windows
# .venv\Scripts\activate.bat      # cmd.exe
# .venv\Scripts\Activate.ps1      # PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

## 1.2 Provision Pinecone

The system uses **one** index with **two** namespaces.

1. Sign in at https://app.pinecone.io and create a free Serverless project.
2. Create an index named `researchflow` (matches `PINECONE_INDEX_NAME` in `.env.example`):
   - **Dimensions:** `1024` (matches Bedrock Titan Embeddings V2 default).
   - **Metric:** `cosine`.
   - **Cloud / region:** AWS / `us-east-1` (or wherever your Bedrock is — keep them aligned to reduce latency).
3. Copy the API key from the **API Keys** sidebar.

> You do **not** need to pre-create namespaces. Pinecone creates them on first upsert.

## 1.3 Confirm Bedrock model access

Bedrock requires you to explicitly request access to each model in each region. Even if your AWS user has full IAM permissions, **untoggled models will return `AccessDeniedException`** at runtime.

1. Open the AWS Console → Bedrock → **Model access** in your target region.
2. Request access for at least:
   - `anthropic.claude-3-haiku-20240307-v1:0` (cheap, fast — recommended for development)
   - `anthropic.claude-3-sonnet-20240229-v1:0` (the default in `.env.example`)
   - `amazon.titan-embed-text-v2:0` (used for all embeddings)
3. Wait for "Access granted" (usually under a minute for Anthropic models).

## 1.4 Fill in `.env`

Copy and edit:

```bash
cp .env.example .env
```

Minimum values to fill out before you can run **anything**:

```dotenv
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0   # Haiku = cheap dev runs
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0

PINECONE_API_KEY=...
PINECONE_INDEX_NAME=researchflow

MAX_REFINEMENT_ITERATIONS=2
HITL_CONFIDENCE_THRESHOLD=0.6
SLIDING_WINDOW_SIZE=20
```

LangSmith is optional during development — leave `LANGCHAIN_TRACING_V2=false` until you actually want traces in the cloud dashboard.

## 1.5 Smoke-test the three external services

Save the snippet below as `scratch_smoketest.py` in the project root **but do not commit it** — this is just a sanity check you can throw away after.

```python
"""One-time smoke test. Delete after verifying."""
import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. Pinecone reachable ---
from pinecone import Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
print("Pinecone OK:", index.describe_index_stats())

# --- 2. Bedrock invoke ---
import boto3
client = boto3.client("bedrock-runtime", region_name=os.environ["AWS_REGION"])
import json
response = client.invoke_model(
    modelId=os.environ["BEDROCK_MODEL_ID"],
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 32,
        "messages": [{"role": "user", "content": "Reply with the single word: pong"}],
    }),
)
payload = json.loads(response["body"].read())
print("Bedrock OK:", payload["content"][0]["text"])

# --- 3. Bedrock embeddings reachable ---
from langchain_aws import BedrockEmbeddings
embedder = BedrockEmbeddings(
    model_id=os.environ["EMBEDDING_MODEL_ID"],
    region_name=os.environ["AWS_REGION"],
)
vec = embedder.embed_query("hello world")
print("Embedder OK:", len(vec))
```

```bash
python scratch_smoketest.py
```

Expected output (roughly):

```
Pinecone OK: {'dimension': 1024, 'index_fullness': 0.0, ...}
Bedrock OK: pong
Embedder OK: 1024
```

If any of those fail, fix it now — every later phase depends on these three working.

## 1.6 Verify

You should be able to run all three smoke-test sections without error. Delete the scratch file:

```bash
rm scratch_smoketest.py
```

---

Continue to [02-Document-Ingestion.md](02-Document-Ingestion.md).
