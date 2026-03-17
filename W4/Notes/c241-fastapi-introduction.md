# FastAPI Introduction

## Learning Objectives
- Understand what FastAPI is and its core benefits.
- Differentiate between ASGI and WSGI.
- Understand the role of Uvicorn in running FastAPI applications.

## Why This Matters
In the modern data ecosystem, data is only as good as its accessibility. While data lakes and warehouses store massive amounts of data, applications and end-users need a reliable, efficient way to consume it. FastAPI has become the industry standard for building high-performance, asynchronous Data APIs in Python, bridging the gap between stored data and active applications.

## The Concept

### What is FastAPI?
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. It is built on top of **Starlette** (for the web parts) and **Pydantic** (for the data parts).

### Key Features
- **High Performance:** On par with NodeJS and Go, thanks to ASGI.
- **Fast Code:** Speeds up development times by up to 300%.
- **Fewer Bugs:** Reduces about 40% of human-induced errors.
- **Automatic Documentation:** Zero configuration for interactive docs (Swagger/OpenAPI).

### ASGI vs WSGI
Traditional Python web frameworks like Flask and Django use **WSGI** (Web Server Gateway Interface), which is synchronous and handles requests one at a time per thread. FastAPI uses **ASGI** (Asynchronous Server Gateway Interface), allowing it to handle asynchronous operations and concurrent connections or long-polling tasks far more efficiently.

### Uvicorn
FastAPI is the *framework*, but it needs an execution server. **Uvicorn** is a lightning-fast ASGI server that runs the FastAPI application code. Together, they provide the backend foundation for high-throughput responses.

## Code Example

To install and run a basic FastAPI app (covered in the next topic), you generally install both:

```bash
pip install fastapi uvicorn
```

## Summary
FastAPI leverages type hinting to provide speed, validation, and documentation. Its ASGI nature makes it ideal for handling heavy loads, making it perfect for delivering data from analytical pipelines.

## Additional Resources
- [Official FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
