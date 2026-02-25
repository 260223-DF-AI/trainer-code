# Namespaces

## Learning Objectives

- Understand what namespaces are in Python
- Distinguish between local, global, and built-in namespaces
- Recognize how Python resolves names

## Why This Matters

Namespaces prevent naming conflicts and help organize your code. Understanding how Python looks up names enables you to write cleaner code and debug issues related to variable visibility and shadowing.

## The Concept

### What is a Namespace?

A **namespace** is a mapping from names to objects. Think of it as a dictionary where keys are variable names and values are the objects they reference.

```python
# When you write:
x = 10
# Python creates an entry in a namespace: {"x": 10}
```

### Types of Namespaces

Python has three main namespaces:

#### 1. Built-in Namespace

Contains Python's built-in functions and exceptions (e.g., `print`, `len`, `TypeError`). This namespace is created when the interpreter starts and exists until it terminates.

```python
# These are in the built-in namespace
print("Hello")
len([1, 2, 3])
```

#### 2. Global Namespace

Contains names defined at the top level of a module or script. Created when the module is imported or the script runs, and lasts until the program ends.

```python
# This is in the global namespace
message = "Hello"

def greet():
    print(message)  # Accesses global 'message'
```

#### 3. Local Namespace

Contains names defined inside a function. Created when the function is called and destroyed when the function returns.

```python
def my_function():
    # This is in the local namespace
    local_var = 42
    print(local_var)

my_function()
# print(local_var)  # Error! local_var doesn't exist here
```

### Namespace Hierarchy

```
+---------------------------+
|    Built-in Namespace     |
|  (print, len, int, etc.)  |
+---------------------------+
            |
+---------------------------+
|    Global Namespace       |
|  (your module variables)  |
+---------------------------+
            |
+---------------------------+
|    Local Namespace        |
|  (function variables)     |
+---------------------------+
```

### Name Resolution (LEGB Rule)

When you use a name, Python searches in this order:

1. **L**ocal - Inside the current function
2. **E**nclosing - In enclosing functions (for nested functions)
3. **G**lobal - At the module level
4. **B**uilt-in - In Python's built-in namespace

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # Prints "local"
    
    inner()

outer()
```

### Viewing Namespaces

Use built-in functions to inspect namespaces:

```python
# View global namespace
print(globals())

# View local namespace (inside a function)
def show_locals():
    a = 1
    b = 2
    print(locals())  # {'a': 1, 'b': 2}

show_locals()

# View built-in namespace
import builtins
print(dir(builtins))
```

### Shadowing

A name in a local namespace can **shadow** a name in an outer namespace:

```python
len = 10  # Shadows the built-in len function

# len([1, 2, 3])  # Error! len is now an integer

del len  # Remove the shadowing
print(len([1, 2, 3]))  # Works again: 3
```

**Best Practice:** Avoid shadowing built-in names.

### The `global` Keyword

We will cover the `global` keyword in more detail later in the week when we discuss scope, which builds on namespace concepts.

## Summary

- A namespace is a mapping from names to objects
- Python has built-in, global, and local namespaces
- Name resolution follows the LEGB rule: Local, Enclosing, Global, Built-in
- Avoid shadowing built-in names to prevent confusion

## Additional Resources

- [Python Documentation: Namespaces and Scope](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)
- [Real Python: Namespaces and Scope](https://realpython.com/python-namespaces-scope/)
- [GeeksforGeeks: Namespaces in Python](https://www.geeksforgeeks.org/namespaces-and-scope-in-python/)
