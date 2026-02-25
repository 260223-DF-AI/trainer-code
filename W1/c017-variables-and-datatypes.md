# Variables and Datatypes

## Learning Objectives

- Understand what variables are and how to create them
- Learn about dynamic typing in Python
- Identify Python's core data types

## Why This Matters

Variables are the building blocks of any program. They store data that your code manipulates. Understanding how Python handles variables and data types is fundamental to writing effective programs.

## The Concept

### What is a Variable?

A **variable** is a named reference to a value stored in memory. Think of it as a label attached to a piece of data.

```python
name = "Alice"
age = 30
is_student = True
```

### Creating Variables

In Python, you create a variable by assigning a value:

```python
x = 10          # Integer
pi = 3.14159    # Float
message = "Hi"  # String
```

**Rules for Variable Names:**

- Must start with a letter or underscore (`_`)
- Can contain letters, numbers, and underscores
- Cannot be a Python keyword
- Case-sensitive (`name` and `Name` are different)

**Conventions (PEP 8):**

- Use `lowercase_with_underscores` for variable names
- Be descriptive: `user_age` is better than `x`

### Dynamic Typing

Python is **dynamically typed**, meaning:

- You do not declare a variable's type in advance
- A variable's type is determined by its value at runtime
- A variable can change types during execution

```python
x = 10       # x is an integer
x = "hello"  # x is now a string
x = [1, 2]   # x is now a list
```

### Checking Types

Use the `type()` function to check a variable's type:

```python
x = 42
print(type(x))  # <class 'int'>

y = "hello"
print(type(y))  # <class 'str'>
```

### Core Data Types

#### Numeric Types

| Type | Description | Example |
|------|-------------|---------|
| `int` | Integer (whole number) | `42`, `-7`, `0` |
| `float` | Floating-point (decimal) | `3.14`, `-0.5` |
| `complex` | Complex number | `3+4j` |

```python
count = 100       # int
price = 19.99     # float
z = 2 + 3j        # complex
```

#### Text Type

| Type | Description | Example |
|------|-------------|---------|
| `str` | String (text) | `"hello"`, `'world'` |

```python
greeting = "Hello, World!"
```

#### Boolean Type

| Type | Description | Example |
|------|-------------|---------|
| `bool` | Boolean (True/False) | `True`, `False` |

```python
is_valid = True
has_errors = False
```

#### Sequence Types

| Type | Description | Example |
|------|-------------|---------|
| `list` | Ordered, mutable | `[1, 2, 3]` |
| `tuple` | Ordered, immutable | `(1, 2, 3)` |
| `range` | Sequence of numbers | `range(5)` |

#### Mapping Type

| Type | Description | Example |
|------|-------------|---------|
| `dict` | Key-value pairs | `{"name": "Alice"}` |

#### Set Types

| Type | Description | Example |
|------|-------------|---------|
| `set` | Unordered, unique items | `{1, 2, 3}` |
| `frozenset` | Immutable set | `frozenset({1, 2})` |

#### None Type

| Type | Description | Example |
|------|-------------|---------|
| `NoneType` | Absence of value | `None` |

```python
result = None
```

### Multiple Assignment

Assign multiple variables at once:

```python
x, y, z = 1, 2, 3

# Same value to multiple variables
a = b = c = 0
```

### Type Summary

```python
# Numeric
age = 25              # int
temperature = 98.6    # float

# Text
name = "Python"       # str

# Boolean
is_active = True      # bool

# Collections (covered in detail later)
numbers = [1, 2, 3]   # list
point = (10, 20)      # tuple
unique = {1, 2, 3}    # set
person = {"name": "Alice", "age": 30}  # dict

# None
value = None          # NoneType
```

## Summary

- Variables store data and are created by assignment
- Python uses dynamic typing; types are determined at runtime
- Core types include `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `set`, and `None`
- Use `type()` to check a variable's type
- Follow naming conventions for readable code

## Additional Resources

- [Python Documentation: Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Real Python: Variables in Python](https://realpython.com/python-variables/)
- [W3Schools: Python Data Types](https://www.w3schools.com/python/python_datatypes.asp)
