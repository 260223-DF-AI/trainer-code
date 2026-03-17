# Creating FastAPI Routes

## Learning Objectives
- Instantiate a FastAPI application.
- Understand decorators for mapping HTTP methods.
- Create basic GET and POST endpoints.

## Why This Matters
Routes are the address system of your API. Just like you need a directory to find a file, a user needs a route address to consume data. Setting up routes is the first step in creating endpoints to interact with your data pipelines or databases.

## The Concept

### The FastAPI Instance
Every FastAPI application starts with an instance of the `FastAPI` class. This instance is the main point of interaction for creating routes and configuring the app.

### Decorators
In Python, decorators are prefixed with `@`. In FastAPI, they map Python functions to specific HTTP methods (like GET or POST) and endpoints paths (like `/` or `/data`).

- `@app.get("/")`: Maps a function to handle HTTP GET requests to the root path.
- `@app.post("/submit")`: Maps a function to handle HTTP POST requests.

## Code Example

### Basic FastAPI App (`main.py`)

```python
from fastapi import FastAPI

# 1. Instantiate the app
app = FastAPI()

# 2. Add @app decorator for route mapping
@app.get("/")
def read_root():
    # 3. Return a dictionary (automatically serialized to JSON)
    return {"message": "Hello World"}

@app.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0"}
```

### Running the Application
To run the application with Uvicorn:

```bash
uvicorn main:app --reload
```
- `main`: Referencing the `main.py` file name.
- `app`: Referring to the `app` variable inside the file.
- `--reload`: Auto-updates the server when the file changes (ideal for development).

## Summary
Instantiating FastAPI and defining simple Python functions with route decorators is all that is strictly required to build responsive REST APIs. Returns are automatically converted to JSON for the client.

## Additional Resources
- [FastAPI Routing](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [HTTP Methods Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
