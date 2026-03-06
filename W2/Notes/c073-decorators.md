# Decorators

## Learning Objectives

- Understand what decorators are and how they work
- Write custom decorators
- Use the @ syntax for decorator application
- Apply common decorator patterns

## Why This Matters

Decorators modify or enhance functions without changing their code. They're used extensively in Python frameworks (Flask routes, pytest fixtures, Django views) and for cross-cutting concerns like logging, caching, and authentication. Understanding decorators is essential for reading and writing idiomatic Python.

## Concept

### What Is a Decorator?

A decorator is a function that takes a function and returns a modified version of it:

```python
def my_decorator(func):
    def wrapper():
        print("Before the function")
        func()
        print("After the function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before the function
# Hello!
# After the function
```

### The @ Syntax

The @ syntax is shorthand for applying a decorator:

```python
@my_decorator
def say_hello():
    print("Hello!")

# Is equivalent to:
def say_hello():
    print("Hello!")
say_hello = my_decorator(say_hello)
```

### Decorators with Arguments

To handle functions with arguments, use *args and **kwargs:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

result = add(2, 3)
# Calling add
# Finished add
# result = 5
```

### Preserving Function Metadata

Use functools.wraps to preserve the original function's metadata:

```python
from functools import wraps

def log_calls(func):
    @wraps(func)  # Preserves name, docstring, etc.
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)  # add (not 'wrapper')
print(add.__doc__)   # Add two numbers.
```

### Decorators That Take Arguments

A decorator with parameters needs an extra layer:

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### Common Decorator Patterns

**Timing decorator:**

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"
```

**Retry decorator:**

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api_call():
    # Might fail sometimes
    pass
```

**Caching decorator:**

```python
from functools import wraps

def cache(func):
    cached_results = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            return cached_results[args]
        result = func(*args)
        cached_results[args] = result
        return result
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Validation decorator:**

```python
from functools import wraps

def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def square_root(x):
    return x ** 0.5
```

### Stacking Decorators

Multiple decorators apply bottom-to-top:

```python
@decorator1
@decorator2
@decorator3
def my_function():
    pass

# Equivalent to:
# my_function = decorator1(decorator2(decorator3(my_function)))
```

### Class-Based Decorators

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Call 1 of say_hello
say_hello()  # Call 2 of say_hello
```

## Summary

Decorators wrap functions to modify their behavior without changing their code. Use the @ syntax to apply decorators. Always use `@functools.wraps` to preserve function metadata. For decorators with parameters, add an extra layer of nesting. Common use cases include logging, timing, caching, validation, and retry logic. Decorators are fundamental to Python frameworks and writing clean, reusable code.

## Resources

- [Real Python: Primer on Decorators](https://realpython.com/primer-on-python-decorators/)
- [Python Docs: functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- [PEP 318: Decorators for Functions](https://peps.python.org/pep-0318/)
