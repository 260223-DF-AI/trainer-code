# Errors in Python

## Learning Objectives

- Distinguish between syntax errors and exceptions
- Read and interpret Python tracebacks
- Identify common error types
- Understand the error hierarchy

## Why This Matters

Errors are inevitable in programming. Understanding what different errors mean and how to read tracebacks is essential for debugging. Knowing the difference between syntax errors (caught before running) and exceptions (occur during execution) helps you fix problems faster and write more robust code.

## Concept

### Types of Errors

Python has two main categories of errors:

1. **Syntax Errors** - Detected before code runs
2. **Exceptions** - Occur during code execution

### Syntax Errors

Syntax errors occur when Python can't parse your code:

```python
# Missing colon
if True
    print("Hello")
# SyntaxError: expected ':'

# Mismatched parentheses
print("Hello"
# SyntaxError: '(' was never closed

# Invalid syntax
x = = 5
# SyntaxError: invalid syntax
```

Python catches syntax errors before running any code. You must fix them before the program can execute.

### Exceptions

Exceptions occur during program execution when something goes wrong:

```python
# Division by zero
result = 10 / 0
# ZeroDivisionError: division by zero

# Accessing missing key
data = {"name": "Alice"}
print(data["age"])
# KeyError: 'age'

# Invalid type operation
"hello" + 5
# TypeError: can only concatenate str (not "int") to str
```

### Reading Tracebacks

When an exception occurs, Python prints a traceback:

```python
def divide(a, b):
    return a / b

def calculate():
    result = divide(10, 0)
    return result

calculate()
```

Output:

```
Traceback (most recent call last):
  File "example.py", line 8, in <module>
    calculate()
  File "example.py", line 5, in calculate
    result = divide(10, 0)
  File "example.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
```

**Reading from bottom to top:**

1. Error type and message: `ZeroDivisionError: division by zero`
2. Line that caused it: `return a / b` in `divide()`
3. Call that led there: `divide(10, 0)` in `calculate()`
4. Original call: `calculate()` in main code

### Common Exception Types

| Exception | Cause |
|-----------|-------|
| `TypeError` | Wrong type for operation |
| `ValueError` | Right type, wrong value |
| `NameError` | Variable not defined |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key not found |
| `AttributeError` | Object has no such attribute |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File doesn't exist |
| `ImportError` | Module can't be imported |
| `IndentationError` | Incorrect indentation |

### Examples of Each

```python
# TypeError
len(42)  # int has no len()

# ValueError
int("hello")  # Can't convert "hello" to int

# NameError
print(undefined_variable)

# IndexError
my_list = [1, 2, 3]
print(my_list[10])

# KeyError
my_dict = {"a": 1}
print(my_dict["b"])

# AttributeError
"hello".non_existent_method()

# ZeroDivisionError
10 / 0

# FileNotFoundError
open("nonexistent.txt")

# ImportError
import nonexistent_module
```

### The Exception Hierarchy

Python exceptions form a hierarchy:

```
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- Exception
      +-- ArithmeticError
      |    +-- ZeroDivisionError
      |    +-- OverflowError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- TypeError
      +-- ValueError
      +-- OSError
      |    +-- FileNotFoundError
      +-- ...
```

This hierarchy matters when handling exceptions, which we'll cover in the next lesson.

### Preventing Common Errors

**Check before accessing:**

```python
# Instead of risking KeyError
value = my_dict.get("key", "default")

# Instead of risking IndexError
if index < len(my_list):
    value = my_list[index]

# Instead of risking TypeError
if isinstance(value, int):
    result = value + 10
```

**Validate input:**

```python
def divide(a, b):
    if b == 0:
        return None  # Or raise a custom error
    return a / b
```

## Summary

Python has syntax errors (detected before running) and exceptions (occur during execution). Tracebacks show the call stack from bottom to top, with the actual error at the bottom. Common exceptions include TypeError, ValueError, KeyError, IndexError, and ZeroDivisionError. Understanding error messages helps you debug faster. The next lesson covers how to handle exceptions gracefully.

## Resources

- [Python Docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python Docs: Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Real Python: Python Exceptions](https://realpython.com/python-exceptions/)
