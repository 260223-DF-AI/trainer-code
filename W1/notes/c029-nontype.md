# Nontype (None)

## Learning Objectives

- Understand the `None` value in Python
- Recognize when `None` is used
- Check for `None` correctly

## Why This Matters

`None` is Python's way of representing the absence of a value. It is used extensively for default parameters, indicating missing data, and as the return value of functions that do not explicitly return anything. Understanding `None` is essential for writing robust Python code.

## The Concept

### What is None?

`None` is a special singleton value that represents "nothing" or "no value." It is the only instance of the `NoneType` class.

```python
x = None
print(type(x))  # <class 'NoneType'>
```

### None is a Singleton

There is only one `None` object in Python. All variables assigned to `None` reference the same object:

```python
a = None
b = None
print(a is b)  # True (same object)
```

### Common Uses of None

#### 1. Default Function Parameters

```python
def greet(name=None):
    if name is None:
        print("Hello, Guest!")
    else:
        print(f"Hello, {name}!")

greet()         # Hello, Guest!
greet("Alice")  # Hello, Alice!
```

#### 2. Functions Without Explicit Return

Functions that do not return a value implicitly return `None`:

```python
def display(message):
    print(message)

result = display("Hello")
print(result)  # None
```

#### 3. Representing Missing Data

```python
user = {
    "name": "Alice",
    "email": None,  # No email provided
    "age": 25
}

if user["email"] is None:
    print("Email not provided")
```

#### 4. Initializing Variables

```python
result = None  # Will be assigned later

# ... some processing ...

if some_condition:
    result = compute_value()
```

### Checking for None

Always use `is` or `is not` to check for `None`, not `==`:

```python
x = None

# Correct
if x is None:
    print("x is None")

if x is not None:
    print("x has a value")

# Works but not recommended
if x == None:  # Less explicit, can be overridden
    pass
```

### None in Boolean Context

`None` is falsy:

```python
x = None

if not x:
    print("x is falsy")  # Prints

# But be careful - 0, "", [] are also falsy
# Use explicit None checks when needed
```

### None vs Other Values

| Value | Type | Boolean Value |
|-------|------|---------------|
| `None` | NoneType | False |
| `0` | int | False |
| `""` | str | False |
| `[]` | list | False |
| `False` | bool | False |

### Common Patterns

```python
# Optional parameter with mutable default
def add_item(item, items=None):
    if items is None:
        items = []  # Create new list if none provided
    items.append(item)
    return items

# Never use mutable default like this:
# def add_item(item, items=[]):  # Bug! Shared list

# Dictionary get with default
data = {"name": "Alice"}
email = data.get("email")  # Returns None if key missing
email = data.get("email", "N/A")  # Returns "N/A" if missing
```

### None and Type Hints

When using type hints, `None` is specified with `Optional` or union syntax:

```python
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    # Returns dict if found, None if not
    if user_exists(user_id):
        return get_user(user_id)
    return None
```

## Summary

- `None` represents the absence of a value
- It is a singleton - there is only one `None` object
- Use `is None` and `is not None` for checks
- Functions without return statements return `None`
- `None` is falsy but distinct from other falsy values

## Additional Resources

- [Python Documentation: None](https://docs.python.org/3/library/constants.html#None)
- [Real Python: Null in Python](https://realpython.com/null-in-python/)
- [W3Schools: Python None](https://www.w3schools.com/python/ref_keyword_none.asp)
