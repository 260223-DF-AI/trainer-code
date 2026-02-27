# Scope

## Learning Objectives

- Understand local, enclosing, global, and built-in scope (LEGB rule)
- Use the global and nonlocal keywords
- Avoid common scope-related errors

## Why This Matters

Scope determines where variables can be accessed in your code. Understanding scope helps you avoid naming conflicts, write cleaner functions, and debug issues related to variable visibility.

## The Concept

### What is Scope?

**Scope** defines the region of code where a variable is accessible. Variables created in one scope may not be visible in another.

### The LEGB Rule

Python searches for names in this order:

1. **L**ocal - Inside the current function
2. **E**nclosing - In enclosing functions (nested functions)
3. **G**lobal - At the module level
4. **B**uilt-in - In Python's built-in namespace

```python
# Built-in scope
# print, len, range, etc.

# Global scope
x = "global"

def outer():
    # Enclosing scope (for inner function)
    x = "enclosing"
    
    def inner():
        # Local scope
        x = "local"
        print(x)  # Uses local x
    
    inner()
    print(x)  # Uses enclosing x

outer()
print(x)  # Uses global x
```

**Output:**

```
local
enclosing
global
```

### Local Scope

Variables created inside a function are local:

```python
def my_function():
    local_var = "I am local"
    print(local_var)

my_function()
# print(local_var)  # NameError: local_var not defined
```

### Global Scope

Variables created at module level are global:

```python
global_var = "I am global"

def my_function():
    print(global_var)  # Can read global variable

my_function()  # I am global
print(global_var)  # I am global
```

### The global Keyword

Modify a global variable from within a function:

```python
counter = 0

def increment():
    global counter  # Declare intent to modify global
    counter += 1

increment()
increment()
print(counter)  # 2
```

**Without global:**

```python
counter = 0

def increment():
    counter = 1  # Creates new local variable, doesn't modify global

increment()
print(counter)  # Still 0
```

### Enclosing Scope (Nested Functions)

```python
def outer():
    message = "Hello from outer"
    
    def inner():
        print(message)  # Accesses enclosing scope
    
    inner()

outer()  # Hello from outer
```

### The nonlocal Keyword

Modify a variable in the enclosing scope:

```python
def outer():
    count = 0
    
    def inner():
        nonlocal count  # Modify enclosing variable
        count += 1
        print(f"Count: {count}")
    
    inner()
    inner()
    print(f"Final: {count}")

outer()
# Count: 1
# Count: 2
# Final: 2
```

### Built-in Scope

Python's built-in names are always available:

```python
# These are in built-in scope
print("Hello")
len([1, 2, 3])
range(10)

# View all built-in names
import builtins
print(dir(builtins))
```

### Shadowing

A local variable can shadow (hide) a global or built-in:

```python
# Shadowing a global
x = 10

def my_func():
    x = 20  # Creates local x, shadows global
    print(x)  # 20

my_func()
print(x)  # 10 (global unchanged)

# Shadowing a built-in (avoid this!)
len = 5  # Shadows built-in len function
# len([1, 2, 3])  # Error! len is now an integer

del len  # Remove shadowing
print(len([1, 2, 3]))  # 3
```

### Common Patterns

```python
# Using global for configuration
DEBUG = False

def set_debug(value):
    global DEBUG
    DEBUG = value

def log(message):
    if DEBUG:
        print(f"DEBUG: {message}")

# Closure with nonlocal
def make_counter():
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

my_counter = make_counter()
print(my_counter())  # 1
print(my_counter())  # 2
print(my_counter())  # 3
```

### Best Practices

- Avoid excessive use of `global` (can make code harder to understand)
- Be mindful of shadowing built-in names
- Use function parameters and return values instead of global state
- Use `nonlocal` sparingly in closures

## Summary

- Python searches for names in order: Local, Enclosing, Global, Built-in (LEGB)
- Local variables are defined inside functions
- Global variables are defined at module level
- Use `global` to modify global variables inside functions
- Use `nonlocal` to modify enclosing scope variables
- Avoid shadowing built-in names

## Additional Resources

- [Python Documentation: Scopes and Namespaces](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)
- [Real Python: Scope in Python](https://realpython.com/python-scope-legb-rule/)
- [W3Schools: Python Scope](https://www.w3schools.com/python/python_scope.asp)
