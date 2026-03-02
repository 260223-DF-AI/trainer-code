# Python Project Structure

## Learning Objectives

- Organize Python code into packages
- Understand the role of `__init__.py`
- Create executable packages with `__main__.py`
- Follow Python project layout conventions

## Why This Matters

Professional Python projects aren't single files - they're organized collections of modules grouped into packages. Understanding project structure is essential for building maintainable applications, collaborating with teams, and publishing your own libraries. A well-organized project is easier to test, debug, and extend.

## Concept

### Packages vs Modules

A **module** is a single `.py` file. A **package** is a directory containing multiple modules and a special `__init__.py` file.

```
my_project/
    main.py
    utils/              # This is a package
        __init__.py
        strings.py      # This is a module
        numbers.py      # This is a module
```

### The `__init__.py` File

The `__init__.py` file marks a directory as a Python package. It can be empty or contain initialization code:

```python
# utils/__init__.py

# Option 1: Empty file (just marks as package)

# Option 2: Import submodules for easier access
from .strings import clean_text
from .numbers import calculate_average

# Option 3: Define package-level variables
__version__ = "1.0.0"
__all__ = ["clean_text", "calculate_average"]
```

With proper `__init__.py`, you can import like this:

```python
# Instead of:
from utils.strings import clean_text

# You can do:
from utils import clean_text
```

### Importing from Packages

```python
# Absolute imports (preferred)
from my_project.utils.strings import clean_text
from my_project.utils import numbers

# Relative imports (within the same package)
from .strings import clean_text      # Same directory
from ..helpers import validate       # Parent directory
```

### The `__main__.py` File

The `__main__.py` file makes a package executable:

```python
# my_package/__main__.py
from .core import main_function

if __name__ == "__main__":
    main_function()
```

Now you can run the package directly:

```bash
python -m my_package
```

### Recommended Project Layout

A typical Python project structure:

```
my_project/
    README.md               # Project documentation
    requirements.txt        # Dependencies
    setup.py               # Package installation config
    
    my_package/            # Main source code
        __init__.py
        __main__.py        # Entry point
        core.py
        utils/
            __init__.py
            helpers.py
    
    tests/                 # Test files
        __init__.py
        test_core.py
        test_helpers.py
    
    docs/                  # Documentation
        index.md
    
    .gitignore            # Git ignore patterns
```

### Example: Building a Package

Let's create a simple calculator package:

```
calculator/
    __init__.py
    __main__.py
    operations.py
    advanced.py
```

```python
# calculator/operations.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# calculator/advanced.py
import math

def power(base, exponent):
    return base ** exponent

def square_root(n):
    return math.sqrt(n)
```

```python
# calculator/__init__.py
from .operations import add, subtract, multiply, divide
from .advanced import power, square_root

__version__ = "1.0.0"
```

```python
# calculator/__main__.py
from . import add, subtract

def main():
    print("Calculator Package Demo")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")

if __name__ == "__main__":
    main()
```

Now you can use it:

```python
# As an import
from calculator import add, multiply
print(add(5, 3))  # 8

# As an executable
# $ python -m calculator
```

### The `__all__` Variable

Control what gets exported when using `from package import *`:

```python
# calculator/__init__.py
__all__ = ["add", "subtract", "multiply", "divide"]

# Only these will be imported with:
# from calculator import *
```

## Summary

Packages are directories containing modules and an `__init__.py` file. Use `__init__.py` to mark directories as packages and control imports. Add `__main__.py` to make packages executable with `python -m package_name`. Follow standard project layouts for maintainability. Use absolute imports for clarity and `__all__` to control public interfaces.

## Resources

- [Python Docs: Packages](https://docs.python.org/3/tutorial/modules.html#packages)
- [Real Python: Python Application Layouts](https://realpython.com/python-application-layouts/)
- [Python Packaging User Guide](https://packaging.python.org/)
