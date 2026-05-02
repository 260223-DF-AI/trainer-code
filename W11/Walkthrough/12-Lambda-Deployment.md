# Phase 12 — Lambda Deployment

**Goal:** ship the Supervisor graph as a `POST /research` HTTP endpoint behind API Gateway via AWS SAM.

You will fill in:
- `deployment/app.py::lambda_handler`
- Environment variables and IAM in `deployment/template.yaml`
- (Verify) `deployment/deploy.sh`

---

## 12.1 The two big practical problems

1. **Package size.** The default Lambda layer cap is 250 MB unzipped. With Bedrock embeddings replacing the local MiniLM model (Phase 01), the project no longer pulls in `torch` or `sentence-transformers`, so a zip deployment is feasible. We still recommend a container image because it gives you headroom if you later add a local reranker or other heavyweight dep — and `sam build` for image packages is the same one-command flow.
2. **Cold start.** Without local model loading, cold starts are dominated by Python import time and Pinecone client init — typically a few seconds. `Timeout: 60` and `MemorySize: 1024` are usually sufficient; bump them if you see throttling.

The reference template below uses the container-image path because it's the more flexible production answer.

## 12.2 `deployment/app.py`

Replace the body of `lambda_handler`:

```python
import json
import logging
import os
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lazy import + module-level so Lambda re-uses warm-state across invocations.
_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        # Import inside the function so cold-start cost is only paid once
        # per container, not at every cold init.
        from agents.supervisor import build_supervisor_graph
        _graph = build_supervisor_graph()
    return _graph


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event: dict, context) -> dict:
    """POST /research handler."""
    try:
        # API Gateway proxy integration delivers the body as a string.
        raw_body = event.get("body") or "{}"
        if isinstance(raw_body, str):
            body = json.loads(raw_body)
        else:
            body = raw_body

        question = (body.get("question") or "").strip()
        if not question:
            return _response(400, {"error": "Missing required field 'question'"})

        # --- input boundary ---
        from middleware.guardrails import detect_injection, sanitize_input
        from middleware.pii_masking import mask_pii
        if detect_injection(question):
            return _response(400, {"error": "Input rejected: possible prompt injection"})
        question = mask_pii(sanitize_input(question))

        # --- invoke graph ---
        graph = _get_graph()
        config = {"configurable": {"thread_id": f"lambda-{uuid.uuid4()}"}}
        result = graph.invoke(
            {"question": question, "user_id": body.get("user_id", "anonymous")},
            config=config,
        )

        # --- output boundary + response shape ---
        analysis = result.get("analysis", {}) or {}
        return _response(200, {
            "answer": mask_pii(analysis.get("answer", "")),
            "citations": analysis.get("citations", []),
            "confidence": result.get("confidence_score", 0.0),
            "fact_check": result.get("fact_check_report", {}),
            "iterations": result.get("iteration_count", 0),
        })

    except Exception as e:
        logger.exception("research failed")
        return _response(500, {"error": str(e)})
```

> Lambda is **not** a great place to do interactive HITL. The container exits when the response is returned. If a request trips a `NodeInterrupt`, treat it as a 503 + `confidence: low` response and have the *client* re-submit with reviewer approval. Wiring real HITL into Lambda requires a step-function-style multi-call flow that's out of scope for this project.

## 12.3 Container image — `deployment/Dockerfile`

Add a new file `deployment/Dockerfile`:

```dockerfile
FROM public.ecr.aws/lambda/python:3.11

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project — note SAM build runs from the deployment dir as CWD.
COPY ../agents      ./agents
COPY ../middleware  ./middleware
COPY ../memory      ./memory
COPY ../deployment/app.py ./app.py

CMD ["app.lambda_handler"]
```

## 12.4 Update `deployment/template.yaml`

Replace the `Resources:` section:

```yaml
Globals:
  Function:
    Timeout: 120
    MemorySize: 2048
    # Runtime is set by the image, not here, when using PackageType: Image.

Parameters:
  PineconeApiKey:
    Type: String
    NoEcho: true
  PineconeIndexName:
    Type: String
    Default: researchflow
  BedrockModelId:
    Type: String
    Default: anthropic.claude-3-haiku-20240307-v1:0
  EmbeddingModelId:
    Type: String
    Default: amazon.titan-embed-text-v2:0
  HitlConfidenceThreshold:
    Type: String
    Default: "0.6"
  MaxRefinementIterations:
    Type: String
    Default: "3"

Resources:
  ResearchFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      Description: Handles /research POST requests
      Environment:
        Variables:
          PINECONE_API_KEY: !Ref PineconeApiKey
          PINECONE_INDEX_NAME: !Ref PineconeIndexName
          BEDROCK_MODEL_ID: !Ref BedrockModelId
          EMBEDDING_MODEL_ID: !Ref EmbeddingModelId
          HITL_CONFIDENCE_THRESHOLD: !Ref HitlConfidenceThreshold
          MAX_REFINEMENT_ITERATIONS: !Ref MaxRefinementIterations
          AWS_REGION: !Ref AWS::Region
      Policies:
        - Statement:
            - Effect: Allow
              Action:
                - bedrock:InvokeModel
                - bedrock:InvokeModelWithResponseStream
              Resource: "*"
      Events:
        ResearchApi:
          Type: Api
          Properties:
            Path: /research
            Method: post
    Metadata:
      Dockerfile: Dockerfile
      DockerContext: .
      DockerTag: v1

Outputs:
  ApiEndpoint:
    Description: "API Gateway endpoint URL for /research"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/research"
```

> The `Resource: "*"` on `bedrock:InvokeModel` is fine for development. For production, scope it to the specific model ARN.

## 12.5 Update `deployment/deploy.sh`

The existing `deploy.sh` is mostly fine but `sam build` for image packages needs Docker. Re-confirm with the parameter overrides:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Read sensitive params from .env or environment.
: "${PINECONE_API_KEY:?PINECONE_API_KEY env var must be set}"

echo "Building SAM application (Docker image)..."
sam build --template-file template.yaml

echo "Deploying to AWS..."
sam deploy \
  --guided \
  --stack-name researchflow \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
      PineconeApiKey="${PINECONE_API_KEY}" \
      PineconeIndexName="${PINECONE_INDEX_NAME:-researchflow}" \
      BedrockModelId="${BEDROCK_MODEL_ID:-anthropic.claude-3-haiku-20240307-v1:0}" \
      EmbeddingModelId="${EMBEDDING_MODEL_ID:-amazon.titan-embed-text-v2:0}"

echo "Deployment complete. Check the Outputs above for your API endpoint."
```

The first `sam deploy --guided` will ask for region, S3/ECR repo, etc., and write a `samconfig.toml`. Subsequent deploys can drop `--guided`.

## 12.6 Smoke-test the deployed endpoint

```bash
curl -X POST <your-api-endpoint> \
  -H "Content-Type: application/json" \
  -d '{"question": "A real question your corpus can answer."}' | jq
```

Expect a JSON response with `answer`, `citations`, `confidence`, `fact_check`, `iterations`.

## 12.7 Clean up when done

Lambda + API Gateway costs are tiny but the ECR image and CloudWatch logs accumulate:

```bash
sam delete --stack-name researchflow
```

Removes everything in one shot.

---

Continue to [13-Demo-and-Presentation.md](13-Demo-and-Presentation.md).
