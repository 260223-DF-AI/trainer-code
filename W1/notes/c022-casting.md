# Casting

## Learning Objectives

- Understand type conversion (casting) in Python
- Convert between numeric types, strings, and other data types
- Handle potential errors during conversion

## Why This Matters

Data often comes in one type but needs to be used as another. User input arrives as strings, but you may need integers for calculations. Casting allows you to convert between types, enabling your programs to work with data flexibly.

## The Concept

### What is Casting?

**Casting** (or type conversion) is the process of converting a value from one data type to another. Python provides built-in functions for common conversions.

### Conversion Functions

| Function | Converts To | Example |
|----------|-------------|---------|
| `int()` | Integer | `int("42")` -> `42` |
| `float()` | Float | `float("3.14")` -> `3.14` |
| `str()` | String | `str(100)` -> `"100"` |
| `bool()` | Boolean | `bool(1)` -> `True` |
| `list()` | List | `list("abc")` -> `["a","b","c"]` |
| `tuple()` | Tuple | `tuple([1,2])` -> `(1, 2)` |
| `set()` | Set | `set([1,1,2])` -> `{1, 2}` |

### Converting to Integer

```python
# From string
x = int("42")      # 42

# From float (truncates, does not round)
x = int(3.9)       # 3
x = int(-3.9)      # -3

# From boolean
x = int(True)      # 1
x = int(False)     # 0

# From string with different base
x = int("1010", 2)  # 10 (binary)
x = int("ff", 16)   # 255 (hexadecimal)
```

### Converting to Float

```python
# From string
x = float("3.14")  # 3.14

# From integer
x = float(42)      # 42.0

# Scientific notation
x = float("1e5")   # 100000.0
```

### Converting to String

```python
# From integer
s = str(42)        # "42"

# From float
s = str(3.14)      # "3.14"

# From boolean
s = str(True)      # "True"

# From list
s = str([1, 2, 3]) # "[1, 2, 3]"
```

### Converting to Boolean

Most values convert to `True`; only specific "falsy" values convert to `False`:

**Falsy Values:**

- `None`
- `0`, `0.0`
- Empty sequences: `""`, `[]`, `()`, `{}`
- Empty set: `set()`

```python
bool(1)       # True
bool(0)       # False
bool("hello") # True
bool("")      # False
bool([1, 2])  # True
bool([])      # False
```

### Converting Between Collections

```python
# String to list
list("hello")           # ['h', 'e', 'l', 'l', 'o']

# List to tuple
tuple([1, 2, 3])        # (1, 2, 3)

# List to set (removes duplicates)
set([1, 2, 2, 3, 3])    # {1, 2, 3}

# Set to list
list({3, 1, 2})         # [1, 2, 3] (order may vary)
```

### Handling Conversion Errors

Not all conversions are valid. Invalid conversions raise errors:

```python
# This works
int("123")

# This raises ValueError
# int("hello")

# Safe conversion with error handling
user_input = "abc"
try:
    number = int(user_input)
except ValueError:
    print("Invalid number")
```

### Implicit vs Explicit Conversion

**Explicit Conversion (Casting):** You call a function to convert:

```python
x = int("42")
```

**Implicit Conversion:** Python automatically converts during operations:

```python
x = 5 + 2.0  # int 5 becomes float 5.0
print(type(x))  # <class 'float'>
```

### Common Patterns

```python
# Converting user input to number
age = int(input("Enter your age: "))

# Converting list of strings to integers
str_nums = ["1", "2", "3"]
int_nums = [int(x) for x in str_nums]  # [1, 2, 3]

# Building a string from parts
price = 19.99
message = "Total: $" + str(price)
```

## Summary

- Casting converts values from one type to another
- Use `int()`, `float()`, `str()`, `bool()` for common conversions
- Invalid conversions raise `ValueError` or `TypeError`
- Python performs some implicit conversions automatically
- Always validate user input before converting

## Additional Resources

- [Python Documentation: Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Real Python: Type Conversion](https://realpython.com/python-type-conversion/)
- [W3Schools: Python Casting](https://www.w3schools.com/python/python_casting.asp)
