# Modules

## Learning Objectives

- Understand what Python modules are and why they exist
- Import modules using different techniques
- Create and use custom modules
- Explore the module search path

## Why This Matters

As programs grow in complexity, organizing code becomes essential. Modules allow you to split your code into separate files, making it easier to maintain, reuse, and share. Every professional Python project uses modules to structure code logically. Understanding modules is the foundation for working with Python's vast ecosystem of packages.

## Concept

### What Is a Module?

A module is simply a Python file (`.py`) containing definitions and statements. Any Python file you create is automatically a module that can be imported by other Python files.

```python
# greetings.py - This file IS a module
def say_hello(name):
    return f"Hello, {name}!"

def say_goodbye(name):
    return f"Goodbye, {name}!"

PI = 3.14159
```

### Importing Modules

There are several ways to import and use modules:

**Basic Import:**

```python
import greetings

message = greetings.say_hello("Alice")
print(message)  # Hello, Alice!
print(greetings.PI)  # 3.14159
```

**Import with Alias:**

```python
import greetings as g

message = g.say_hello("Bob")
```

**Import Specific Items:**

```python
from greetings import say_hello, PI

message = say_hello("Charlie")  # No prefix needed
print(PI)
```

**Import All (Use Sparingly):**

```python
from greetings import *

# All public names are now available directly
# This can cause naming conflicts - use with caution
```

### Built-in Modules

Python comes with many useful built-in modules:

```python
import math
print(math.sqrt(16))  # 4.0
print(math.pi)        # 3.141592653589793

import random
print(random.randint(1, 10))  # Random number 1-10

import datetime
print(datetime.datetime.now())  # Current date and time

import os
print(os.getcwd())  # Current working directory
```

### The Module Search Path

When you import a module, Python searches for it in this order:

1. The current directory
2. PYTHONPATH environment variable directories
3. Standard library directories
4. Site-packages (installed packages)

You can view the search path:

```python
import sys
print(sys.path)
```

### Creating Your Own Modules

Any `.py` file can be a module. Best practices:

```python
# utilities.py

"""Utility functions for data processing."""

def clean_string(text):
    """Remove whitespace and convert to lowercase."""
    return text.strip().lower()

def validate_email(email):
    """Basic email validation."""
    return "@" in email and "." in email

# This code only runs when the file is executed directly
if __name__ == "__main__":
    # Test the module
    print(clean_string("  HELLO  "))
    print(validate_email("test@example.com"))
```

The `if __name__ == "__main__"` block is important - it allows you to include test code that only runs when the file is executed directly, not when imported.

### Module Attributes

Every module has special attributes:

```python
import math

print(math.__name__)  # 'math'
print(math.__doc__)   # Module documentation
print(dir(math))      # List all names defined in module
```

### Packages and `__init__.py`

When projects grow even larger, you can organize multiple related modules into a **package**. A package is simply a directory containing multiple `.py` files and a special file named `__init__.py`.

**What does `__init__.py` do?**

1. It tells Python that the directory should be treated as a package, rather than just a regular folder.
2. It executes automatically when the package is imported, allowing you to run initialization code.
3. It lets you control what gets exposed to the outside world when your package is imported.

Example `__init__.py`:

```python
# __init__.py inside a "utilities" folder

# We can import specific things from our internal modules
from .text_tools import clean_string
from .network_tools import validate_email

# __all__ defines exactly what gets exported when someone does `from utilities import *`
__all__ = ["clean_string", "validate_email"]
```

**What is `__all__`?**
The `__all__` variable is a list of strings defining the "public API" of your module or package. If a user runs `from my_package import *`, Python will only import the names listed in `__all__`. This helps keep the importer's namespace clean and hides internal helper functions.

## Summary

Modules are Python files that contain reusable code. Import them using `import module_name` or `from module import item`. Python searches for modules in the current directory, PYTHONPATH, standard library, and installed packages. Use `if __name__ == "__main__"` to separate importable code from test code. Modules are the building blocks for organizing larger Python projects.

## Resources

- [Python Docs: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Real Python: Python Modules and Packages](https://realpython.com/python-modules-packages/)
- [Python Module Index](https://docs.python.org/3/py-modindex.html)
