# Context Managers

## Learning Objectives

- Understand what context managers are and why they're useful
- Use the `with` statement for resource management
- Create custom context managers using classes and contextlib
- Apply context managers for common use cases

## Why This Matters

Context managers ensure resources are properly acquired and released, even when errors occur. They're essential for working with files, database connections, locks, and network resources. The `with` statement you'll use constantly for file handling is powered by context managers.

## Concept

### The Problem Context Managers Solve

Without context managers:

```python
file = open("data.txt")
try:
    data = file.read()
    process(data)
finally:
    file.close()  # Must remember to close!
```

With context managers:

```python
with open("data.txt") as file:
    data = file.read()
    process(data)
# File is automatically closed, even if an exception occurs
```

### The with Statement

The `with` statement:

1. Acquires the resource (calls `__enter__`)
2. Provides it to your code
3. Releases it when done (calls `__exit__`), even on error

```python
with open("data.txt", "r") as file:
    content = file.read()
# file.close() is called automatically here
```

### Multiple Context Managers

```python
# Multiple with statements
with open("input.txt") as infile:
    with open("output.txt", "w") as outfile:
        outfile.write(infile.read())

# Or on one line
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())
```

### How Context Managers Work

A context manager is any object with `__enter__` and `__exit__` methods:

```python
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        return self  # Value assigned to 'as' variable
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")
        return False  # Don't suppress exceptions

# Usage
with MyContextManager() as manager:
    print("Inside context")

# Output:
# Entering context
# Inside context
# Exiting context
```

### The __exit__ Parameters

`__exit__` receives exception information:

- `exc_type`: Exception class (or None)
- `exc_value`: Exception instance (or None)
- `traceback`: Traceback object (or None)

```python
class ErrorLogger:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False  # Re-raise exceptions

with ErrorLogger():
    raise ValueError("Something went wrong")
# Prints: An error occurred: Something went wrong
# Then re-raises the exception
```

Return `True` from `__exit__` to suppress the exception (use carefully!).

### Practical Example: Database Connection

```python
class DatabaseConnection:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.connection = None
    
    def __enter__(self):
        self.connection = connect(self.host, self.database)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        return False

# Usage
with DatabaseConnection("localhost", "mydb") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
# Connection is automatically closed
```

### Using contextlib

The contextlib module provides utilities for creating context managers:

__@contextmanager decorator:__

```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield  # Where the 'with' block runs
    end = time.time()
    print(f"Elapsed: {end - start:.2f} seconds")

with timer():
    # Some operation
    import time
    time.sleep(1)
# Prints: Elapsed: 1.00 seconds
```

__With a value:__

```python
from contextlib import contextmanager

@contextmanager
def open_file(path, mode):
    file = open(path, mode)
    try:
        yield file  # Value provided to 'as'
    finally:
        file.close()

with open_file("data.txt", "r") as f:
    content = f.read()
```

### contextlib Utilities

__suppress - Ignore specific exceptions:__

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("might_not_exist.txt")
# No error if file doesn't exist
```

__redirect_stdout - Capture print output:__

```python
from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print("This goes to the string")

output = f.getvalue()
```

__closing - Add close() support:__

```python
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("https://example.com")) as page:
    content = page.read()
```

### Common Context Managers

| Type | Example |
|------|---------|
| Files | `open("file.txt")` |
| Locks | `threading.Lock()` |
| Database | `sqlite3.connect("db.sqlite")` |
| Network | `socket.socket()` |
| Decimal | `decimal.localcontext()` |

### Best Practices

1. __Prefer `with` for resources__ - Files, connections, locks
2. __Keep the block focused__ - Do only what needs the resource
3. __Use contextlib for custom managers__ - Decorator is often cleaner
4. __Don't suppress exceptions carelessly__ - Only when explicitly intended

## Summary

Context managers handle resource acquisition and cleanup automatically using the `with` statement. They implement `__enter__` (setup) and `__exit__` (cleanup) methods. Use contextlib's `@contextmanager` decorator for simpler custom managers. Context managers ensure cleanup happens even when exceptions occur, making them essential for working with files, connections, and other resources.

## Resources

- [Python Docs: Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python Docs: contextlib](https://docs.python.org/3/library/contextlib.html)
- [Real Python: Context Managers](https://realpython.com/python-with-statement/)
