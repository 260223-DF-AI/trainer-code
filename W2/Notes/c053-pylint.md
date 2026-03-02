# pylint

## Learning Objectives

- Understand the purpose of code linting
- Install and run pylint on Python code
- Interpret pylint messages and scores
- Configure pylint for your project

## Why This Matters

Code quality matters. pylint analyzes your Python code for errors, style issues, and potential bugs before they cause problems. It enforces consistent coding standards, catches common mistakes, and helps teams maintain clean, readable code. Using linters is standard practice in professional development environments.

## Concept

### What Is Linting?

Linting is the process of analyzing code for:

- Syntax errors
- Style violations (PEP 8)
- Potential bugs
- Code smells (suspicious patterns)
- Unused variables and imports

### Installing pylint

```bash
pip install pylint
```

### Running pylint

**On a single file:**

```bash
pylint my_script.py
```

**On a module/package:**

```bash
pylint my_package/
```

**On multiple files:**

```bash
pylint file1.py file2.py
```

### Understanding the Output

Consider this code:

```python
# bad_code.py
import os
import sys

def Calculate_Sum(a,b):
    x = 10
    return a+b

class myClass:
    def __init__(self):
        self.Value = 1
```

Running `pylint bad_code.py` produces:

```
************* Module bad_code
bad_code.py:1:0: W0611: Unused import os (unused-import)
bad_code.py:2:0: W0611: Unused import sys (unused-import)
bad_code.py:4:0: C0103: Function name "Calculate_Sum" doesn't conform to snake_case naming style (invalid-name)
bad_code.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
bad_code.py:5:4: W0612: Unused variable 'x' (unused-variable)
bad_code.py:8:0: C0103: Class name "myClass" doesn't conform to PascalCase naming style (invalid-name)
bad_code.py:8:0: C0115: Missing class docstring (missing-class-docstring)
bad_code.py:10:8: C0103: Attribute name "Value" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 0.00/10
```

### Message Types

| Code | Type | Meaning |
|------|------|---------|
| C | Convention | Style/PEP 8 violation |
| R | Refactor | Code smell, needs refactoring |
| W | Warning | Potential problem |
| E | Error | Likely bug |
| F | Fatal | Prevented pylint from running |

### The pylint Score

pylint rates your code from -10 to 10:

- 10: Perfect
- 7-9: Good
- 5-7: Needs improvement
- <5: Significant issues

### Fixing the Example

```python
# good_code.py
"""Module for mathematical operations."""


def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b


class MyCalculator:
    """A simple calculator class."""

    def __init__(self):
        """Initialize the calculator with default value."""
        self.value = 1
```

Now: `Your code has been rated at 10.00/10`

### Common pylint Messages

**Naming Conventions:**

- `C0103`: Invalid name (not following conventions)
- Use `snake_case` for functions/variables
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants

**Documentation:**

- `C0114`: Missing module docstring
- `C0115`: Missing class docstring
- `C0116`: Missing function docstring

**Unused Code:**

- `W0611`: Unused import
- `W0612`: Unused variable
- `W0613`: Unused argument

**Style:**

- `C0301`: Line too long (>100 characters)
- `C0303`: Trailing whitespace
- `C0304`: Missing final newline

### Configuring pylint

Create a `.pylintrc` file in your project:

```bash
# Generate default config
pylint --generate-rcfile > .pylintrc
```

**Common configurations:**

```ini
[MESSAGES CONTROL]
# Disable specific warnings
disable=C0114,  # Missing module docstring
        C0116,  # Missing function docstring
        W0612   # Unused variable

[FORMAT]
# Maximum line length
max-line-length=120

[DESIGN]
# Maximum number of arguments for function/method
max-args=6

# Maximum number of local variables
max-locals=20
```

### Inline Disabling

Disable warnings for specific lines:

```python
import os  # pylint: disable=unused-import

def my_function(unused_arg):  # pylint: disable=unused-argument
    pass

# Disable for a block
# pylint: disable=invalid-name
x = 10
Y = 20
# pylint: enable=invalid-name
```

### Integrating with IDEs

Most IDEs support pylint integration:

**VS Code:**

1. Install Python extension
2. Open Settings
3. Search "pylint"
4. Enable "Python > Linting: Pylint Enabled"

The IDE will show pylint warnings as you type.

### Other Python Linters

| Tool | Focus |
|------|-------|
| **pylint** | Comprehensive, strict |
| **flake8** | PEP 8 + basic checks, faster |
| **mypy** | Type checking |
| **black** | Code formatting (auto-fix) |
| **isort** | Import sorting (auto-fix) |

Many projects use multiple tools together.

### Practical Workflow

```bash
# 1. Write code
# 2. Run pylint
pylint my_module.py

# 3. Fix issues
# 4. Run again until clean

# For CI/CD, require minimum score
pylint my_module.py --fail-under=8.0
```

## Summary

pylint analyzes Python code for errors, style issues, and potential bugs. Run it with `pylint file.py` and interpret the output using message codes (C=convention, W=warning, E=error). Configure with `.pylintrc` or inline comments to customize checks. Aim for high scores and integrate pylint into your development workflow and CI/CD pipeline for consistent code quality.

## Resources

- [pylint Documentation](https://pylint.pycqa.org/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Real Python: Python Code Quality](https://realpython.com/python-code-quality/)
