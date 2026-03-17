# Automated API Documentation

## Learning Objectives
- Locate automatic Swagger documentation endpoints.
- Understand how OpenAPI standards are generated automatically.
- Differentiate between Swagger UI and ReDoc displays.

## Why This Matters
An API is only useful if other developers know how to call it. Manually maintaining API documentation is prone to drift, lag, and errors as routes change. FastAPI solves this by generating live, interactive documentation updating dynamically as code develops.

## The Concept

### Interactive Docs with Swagger UI
By default, FastAPI generates a fully interactive, responsive documentation page for your API. It reads your decorators, Pydantic models, and docstrings to create rich descriptions directly from files.

- **Endpoint access:** Usually at **`/docs`** on your locally hosted app address (e.g., `http://127.0.0.1:8000/docs`).
- **Functionality:** Users can interactively test API calls immediately inside the browser using "Try it Out" panels.

### Static Docs with ReDoc
FastAPI also presents an alternative view adhering closely to static documentation pages ideal for print-outs or clean reviews.

- **Endpoint access:** Usually at **`/redoc`** (e.g., `http://127.0.0.1:8000/redoc`).

### OpenAPI Standard
FastAPI compiles your framework into an **OpenAPI** compliant JSON scheme definition automatically.

## Code Example

To generate rich descriptions, utilize standard Python docstrings and attribute descriptions:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data", tags=["Analytics"])
def fetch_analytics():
    """
    Fetch high-level aggregate analytics.
    
    Returns:
    - **Total Records Managed**
    - **Pipeline Status**
    """
    return {"records": 4500000, "status": "nominal"}
```
The text placed in the triple quotes (`"""`) is extracted and beautifully formatted inside Swagger UI `/docs` automatically!

## Summary
FastAPI completely reduces documentation overhead. Always leverage docstrings and meaningful type annotations to make interactive Swagger documentation useful for client developers.

## Additional Resources
- [FastAPI Interactive Documentation Examples](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs)
- [OpenAPI Initiative](https://www.openapis.org/)
