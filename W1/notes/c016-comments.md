# Comments

## Learning Objectives

- Understand the purpose of comments in code
- Write single-line and multi-line comments in Python
- Learn about docstrings for documentation

## Why This Matters

Comments make your code understandable to others (and to your future self). They explain the "why" behind your code, document complex logic, and improve maintainability. Writing good comments is a professional skill that distinguishes quality code.

## The Concept

### What Are Comments?

**Comments** are text in your code that Python ignores during execution. They are for human readers only.

### Single-Line Comments

Use the hash symbol (`#`) to start a single-line comment:

```python
# This is a comment
print("Hello")  # This is an inline comment
```

Everything after `#` on that line is ignored.

### Multi-Line Comments

Python does not have a dedicated multi-line comment syntax. There are two approaches:

**Approach 1: Multiple Single-Line Comments**

```python
# This is a longer explanation
# that spans multiple lines
# using hash symbols on each line
```

**Approach 2: Multi-Line Strings (Not Assigned)**

```python
"""
This is a multi-line string.
When not assigned to a variable,
it acts like a comment.
"""
```

Note: This second approach creates a string object that is immediately discarded. It works but is not a true comment.

### Docstrings

**Docstrings** are special strings used to document modules, classes, and functions. They are placed immediately after the definition and use triple quotes:

```python
def calculate_area(radius):
    """
    Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle.
    
    Returns:
        The area of the circle.
    """
    return 3.14159 * radius ** 2
```

Docstrings can be accessed programmatically:

```python
print(calculate_area.__doc__)
```

### When to Use Comments

**Good Uses:**

- Explain complex logic or algorithms
- Document assumptions or edge cases
- Provide context for non-obvious decisions
- Mark TODO items or known issues

```python
# Using binary search for O(log n) performance
# Assumes the list is already sorted
result = binary_search(sorted_list, target)

# TODO: Handle negative numbers
```

**Avoid:**

- Stating the obvious
- Explaining what the code does instead of why

```python
# Bad: Increment x by 1
x = x + 1

# Better: Adjust for zero-based indexing
x = x + 1
```

### Commenting Best Practices

| Practice | Description |
|----------|-------------|
| Be concise | Keep comments short and focused |
| Stay current | Update comments when code changes |
| Explain why | Focus on intent, not mechanics |
| Use docstrings | Document public functions and classes |
| Avoid noise | Do not comment obvious code |

### Commented-Out Code

Temporarily disabling code with comments is common during debugging:

```python
# print("Debug output:", value)
process_data(value)
```

However, avoid leaving commented-out code in production. Use version control to track old code instead.

## Summary

- Use `#` for single-line comments
- Use multiple `#` lines or triple-quoted strings for longer explanations
- Docstrings document functions, classes, and modules
- Good comments explain why, not just what
- Keep comments accurate and up-to-date

## Additional Resources

- [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
- [Real Python: Documenting Python Code](https://realpython.com/documenting-python-code/)
- [Python Documentation: Comments](https://docs.python.org/3/tutorial/introduction.html)
