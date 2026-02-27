# Python Syntax

## Learning Objectives

- Understand Python's syntax rules and conventions
- Learn about indentation and its role in Python
- Recognize how Python differs from other languages syntactically

## Why This Matters

Python's syntax is designed for readability and simplicity. Unlike many other languages, Python uses indentation to define code blocks rather than braces or keywords. Mastering Python syntax is essential for writing correct, readable code.

## The Concept

### Indentation

Indentation is not optional in Python; it is part of the syntax. Code blocks are defined by their indentation level.

**Correct:**

```python
if True:
    print("This is indented")
    print("Same block")
print("Outside the block")
```

**Incorrect (causes IndentationError):**

```python
if True:
print("Missing indentation")  # Error!
```

**Standard Convention:** Use 4 spaces for each indentation level. Avoid tabs or mixing tabs and spaces.

### Colons

Colons (`:`) introduce code blocks in Python. They appear after:

- Conditional statements (`if`, `elif`, `else`)
- Loops (`for`, `while`)
- Function definitions (`def`)
- Class definitions (`class`)

```python
if condition:
    # block starts after colon
    pass

for item in items:
    # loop body
    pass

def my_function():
    # function body
    pass
```

### Statements and Line Breaks

Each statement typically occupies one line:

```python
x = 5
y = 10
print(x + y)
```

For long statements, you can use a backslash (`\`) for line continuation:

```python
total = 1 + 2 + 3 + \
        4 + 5 + 6
```

Or use parentheses for implicit continuation:

```python
total = (1 + 2 + 3 +
         4 + 5 + 6)
```

### Multiple Statements on One Line

You can use semicolons to place multiple statements on one line, but this is discouraged:

```python
x = 1; y = 2; z = 3  # Works, but not recommended
```

### Case Sensitivity

Python is case-sensitive. `name`, `Name`, and `NAME` are three different variables:

```python
name = "Alice"
Name = "Bob"
print(name)  # Alice
print(Name)  # Bob
```

### Naming Conventions

Python follows these conventions (PEP 8):

| Type | Convention | Example |
|------|------------|---------|
| Variables | lowercase_with_underscores | `user_name` |
| Functions | lowercase_with_underscores | `calculate_total()` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `MAX_SIZE` |
| Classes | CamelCase | `UserAccount` |

### Keywords

Python has reserved keywords that cannot be used as identifiers:

```python
import keyword
print(keyword.kwlist)
```

Common keywords include: `if`, `else`, `for`, `while`, `def`, `class`, `return`, `import`, `True`, `False`, `None`

### Blank Lines

Use blank lines to separate logical sections of code:

- Two blank lines before and after top-level function or class definitions
- One blank line between methods inside a class

```python
def function_one():
    pass


def function_two():
    pass
```

### Syntax Errors

If you violate Python's syntax rules, you get a `SyntaxError`:

```python
if True
    print("Missing colon")  # SyntaxError: expected ':'
```

Python's error messages help you identify and fix syntax problems.

## Summary

- Indentation defines code blocks in Python (use 4 spaces)
- Colons introduce blocks after conditionals, loops, functions, and classes
- Python is case-sensitive
- Follow PEP 8 naming conventions for readable code
- Syntax errors occur when Python's rules are violated

## Additional Resources

- [Python Documentation: Lexical Analysis](https://docs.python.org/3/reference/lexical_analysis.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python: Python Syntax Basics](https://realpython.com/python-first-steps/)
