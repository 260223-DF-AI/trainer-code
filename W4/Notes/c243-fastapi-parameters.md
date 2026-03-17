# Path and Query Parameters

## Learning Objectives
- Differentiate between Path Parameters and Query Parameters.
- Understand how FastAPI automatically handles variable typing.
- Create parametric endpoints to return filterable data.

## Why This Matters
Applications rarely need the entire dataset; they usually need specific records (e.g., User ID 5) or filtered lists (e.g., items where quantity > 10). Parametric endpoints allow your Data API to serve tailored slices of data rather than full tables.

## The Concept

### Path Parameters
Path parameters are part of the URL path itself and are useful for identifying a specific resource. They are bound within the decorator string using curly braces `{}` and passed to the function as arguments.

### Query Parameters
Query parameters are key-value pairs appended after the `?` in a URL. They are often used for filtering, sorting, or pagination of a collection of data. In FastAPI, any function argument that is *not* declared in the decorator path is assumed to be a query parameter.

## Code Example

```python
from fastapi import FastAPI

app = FastAPI()

# --- Path Parameter Example ---
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # FastAPI automatically casts item_id to an integer
    return {"item_id": item_id, "category": "General"}

# --- Path + Query Parameter Example ---
@app.get("/users/{user_id}/logs")
def read_user_logs(user_id: int, limit: int = 10, offset: int = 0):
    # 'limit' and 'offset' are query parameters with default values
    # Example URL: /users/5/logs?limit=5&offset=10
    return {
        "user_id": user_id,
        "parameters": {"limit": limit, "offset": offset},
        "message": f"Returning logs offset {offset}"
    }
```

### Type Hints and Validation
Notice the use of type hints (`limit: int`). FastAPI uses these to:
- Automatically parse incoming string parameters into Python integers.
- Throw high-quality validation errors to the client if the type conversion fails (e.g., passing `"abc"` instead of `10`).

## Summary
Use path parameters for selecting unique items, and query parameters for filtering large sets. FastAPI's type hinting ensures data integrity before your application logic has to process the variable.

## Additional Resources
- [FastAPI Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
