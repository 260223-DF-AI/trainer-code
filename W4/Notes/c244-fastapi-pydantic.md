# FastAPI & Pydantic Validation

## Learning Objectives
- Understand Pydantic's role in FastAPI.
- Create data models for request bodies.
- Enforce strict typing and attribute conditions.

## Why This Matters
Data pipelines rely on strictly structured data payloads. When an application posts new data to an API for ingestion, allowing bad or missing values can break following ETL steps or corrupt databases. Pydantic ensures incoming data is structurally validated *before* processing.

## The Concept

### What is Pydantic?
Pydantic is a Python library for data validation and settings management using Python type annotations. FastAPI is fundamentally integrated with Pydantic; it uses Pydantic models to define the shape and types of JSON bodies sent to or received from endpoints.

### Request Body Validation
To receive and validate JSON data from a POST/PUT request, you create a class inheriting from Pydantic's `BaseModel`. FastAPI will automatically:
1. Parse the request body as JSON.
2. Convert and validate the types.
3. Throw code 422 errors for missing or bad fields.

## Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 1. Define the Pydantic Data Model
class UserRecord(BaseModel):
    user_id: int
    user_name: str
    email: str
    active: bool = True  # Default value
    tags: list[str] = []

# 2. Use the model as a type hint in the endpoint
@app.post("/users/")
def create_user(user: UserRecord):
    # 'user' is now an object of type UserRecord with strictly typed attributes
    db_insert_logic = f"Inserting {user.user_name} into DB"
    return {"status": "success", "user_inserted": user}
```

### Advanced Validation
You can add Pydantic constraints using `Field` to restrict ranges:
```python
class Item(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be greater than zero")
```

## Summary
Pydantic acts as the gatekeeper for incoming API data structure. Defining clear data shapes guarantees downstream logic (such as inserting into a database) operates on clean, anticipated payloads.

## Additional Resources
- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic Official Documentation](https://docs.pydantic.dev/)
