# functools Module

## Learning Objectives

- Use functools.partial for function specialization
- Apply functools.lru_cache for memoization
- Understand functools.reduce for cumulative operations
- Apply functools.wraps in decorators

## Why This Matters

The functools module provides higher-order functions that work on or return other functions. These tools - partial functions, caching, and reduce - are essential for functional programming patterns and optimizing performance. You've already seen `@wraps` in decorators; now learn the full power of functools.

## Concept

### functools.partial

Create a new function with some arguments pre-filled:

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27
```

**Practical uses:**

```python
from functools import partial

# Pre-configure a function
def greet(greeting, name):
    return f"{greeting}, {name}!"

say_hello = partial(greet, "Hello")
say_hi = partial(greet, "Hi")

print(say_hello("Alice"))  # Hello, Alice!
print(say_hi("Bob"))       # Hi, Bob!

# With callbacks
def log_message(level, message):
    print(f"[{level}] {message}")

log_error = partial(log_message, "ERROR")
log_info = partial(log_message, "INFO")

log_error("Something went wrong")  # [ERROR] Something went wrong
log_info("Process started")        # [INFO] Process started
```

### functools.lru_cache

Memoization decorator that caches function results:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# First call computes, subsequent calls use cache
print(fibonacci(100))  # Instant (would be very slow without cache)

# Cache info
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# Clear cache
fibonacci.cache_clear()
```

**Parameters:**

```python
@lru_cache(maxsize=None)   # Unlimited cache
@lru_cache(maxsize=128)    # Limited to 128 entries (default)
@lru_cache(maxsize=1)      # Cache only the most recent call
```

**Practical use:**

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_from_database(user_id):
    """Expensive database query - cache results."""
    print(f"Fetching user {user_id} from database...")
    # Simulate database query
    return {"id": user_id, "name": f"User {user_id}"}

# First call hits database
user = get_user_from_database(42)  # Fetching user 42...

# Second call uses cache
user = get_user_from_database(42)  # (no output - from cache)
```

### functools.reduce

Apply a function cumulatively to sequence items:

```python
from functools import reduce

# Sum: ((((1+2)+3)+4)+5) = 15
result = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print(result)  # 15

# Product: ((((1*2)*3)*4)*5) = 120
product = reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
print(product)  # 120

# With initial value
result = reduce(lambda x, y: x + y, [1, 2, 3], 10)  # 10 + 1+2+3 = 16
```

**Practical examples:**

```python
from functools import reduce

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda a, b: a + b, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]

# Find maximum
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(maximum)  # 9

# Compose dictionaries
dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
merged = reduce(lambda a, b: {**a, **b}, dicts)
print(merged)  # {'a': 1, 'b': 2, 'c': 3}
```

**Note:** For simple operations, built-in functions are often clearer:

```python
# Prefer built-ins when available
sum([1, 2, 3, 4, 5])       # Instead of reduce with +
max([1, 2, 3, 4, 5])       # Instead of reduce with comparison
```

### functools.wraps

Preserve original function metadata in decorators:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Copies __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """This is the docstring."""
    pass

print(example.__name__)  # example (not 'wrapper')
print(example.__doc__)   # This is the docstring.
```

Without `@wraps`, the decorated function loses its identity.

### functools.total_ordering

Generate comparison methods from **eq** and one other:

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade

# Now all comparison operators work
s1 = Student("Alice", 85)
s2 = Student("Bob", 90)

print(s1 < s2)   # True
print(s1 <= s2)  # True (generated)
print(s1 > s2)   # False (generated)
print(s1 >= s2)  # False (generated)
```

### functools.cache (Python 3.9+)

Simpler version of lru_cache with unlimited cache:

```python
from functools import cache

@cache
def expensive_computation(x):
    print(f"Computing {x}...")
    return x ** 2

expensive_computation(5)  # Computing 5... -> 25
expensive_computation(5)  # (from cache) -> 25
```

Equivalent to `@lru_cache(maxsize=None)`.

## Summary

functools provides essential higher-order function tools. Use `partial()` to create specialized functions with pre-filled arguments. Apply `@lru_cache` for automatic memoization of expensive function calls. Use `reduce()` for cumulative operations (though built-ins like `sum()` are often better). Always use `@wraps` in decorators to preserve function metadata. These tools enable functional programming patterns and performance optimization.

## Resources

- [Python Docs: functools](https://docs.python.org/3/library/functools.html)
- [Real Python: Python functools](https://realpython.com/python-functools/)
- [Python lru_cache Guide](https://realpython.com/lru-cache-python/)
