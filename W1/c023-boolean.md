# Boolean

## Learning Objectives

- Understand the boolean data type in Python
- Identify truthy and falsy values
- Use boolean operations in conditions

## Why This Matters

Booleans are the foundation of decision-making in programming. Conditions, loops, and filters all rely on boolean values to determine program flow. Understanding how Python evaluates truthiness is essential for writing effective conditional logic.

## The Concept

### What is a Boolean?

A **boolean** is a data type with only two possible values: `True` or `False`. In Python, the type is called `bool`.

```python
is_active = True
is_complete = False

print(type(is_active))  # <class 'bool'>
```

### Boolean Values

Note that `True` and `False` are capitalized in Python:

```python
# Correct
x = True
y = False

# Incorrect (NameError)
# x = true
# y = false
```

### Comparison Operators Return Booleans

Comparisons evaluate to `True` or `False`:

```python
print(5 > 3)    # True
print(5 == 3)   # False
print(5 != 3)   # True
print(5 <= 5)   # True
```

### Truthy and Falsy Values

In Python, every value has an inherent truthiness. When used in a boolean context (like an `if` statement), values are evaluated as either truthy or falsy.

**Falsy Values (evaluate to `False`):**

- `False`
- `None`
- `0` (integer zero)
- `0.0` (float zero)
- `""` (empty string)
- `[]` (empty list)
- `()` (empty tuple)
- `{}` (empty dictionary)
- `set()` (empty set)

**Truthy Values (evaluate to `True`):**

- Everything else, including:
  - Non-zero numbers
  - Non-empty strings
  - Non-empty collections

```python
# Falsy examples
if 0:
    print("Won't print")

if "":
    print("Won't print")

if []:
    print("Won't print")

# Truthy examples
if 1:
    print("Prints!")

if "hello":
    print("Prints!")

if [1, 2, 3]:
    print("Prints!")
```

### The bool() Function

Explicitly convert values to boolean:

```python
print(bool(0))        # False
print(bool(42))       # True
print(bool(""))       # False
print(bool("hello"))  # True
print(bool([]))       # False
print(bool([1, 2]))   # True
```

### Boolean Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | True if both are True | `True and True` -> `True` |
| `or` | True if at least one is True | `True or False` -> `True` |
| `not` | Inverts the value | `not True` -> `False` |

```python
a = True
b = False

print(a and b)   # False
print(a or b)    # True
print(not a)     # False
print(not b)     # True
```

### Short-Circuit Evaluation

Python stops evaluating as soon as the result is determined:

```python
# 'and' stops at first False
print(False and expensive_function())  # False, function not called

# 'or' stops at first True
print(True or expensive_function())    # True, function not called
```

### Booleans in Conditions

```python
is_logged_in = True
has_permission = False

if is_logged_in and has_permission:
    print("Access granted")
elif is_logged_in:
    print("Please request permission")
else:
    print("Please log in")
```

### Boolean Arithmetic

Booleans can be used in arithmetic (True = 1, False = 0):

```python
print(True + True)   # 2
print(True * 5)      # 5
print(False + 10)    # 10

# Counting True values
values = [True, False, True, True]
print(sum(values))   # 3
```

### Common Patterns

```python
# Check if list is empty
items = []
if not items:
    print("List is empty")

# Check if string has content
name = input("Enter name: ")
if name:
    print(f"Hello, {name}")
else:
    print("No name provided")
```

## Summary

- Booleans are `True` or `False` (capitalized)
- Comparisons and conditions evaluate to booleans
- Truthy/falsy values determine how non-boolean values behave in conditions
- Boolean operators: `and`, `or`, `not`
- Short-circuit evaluation optimizes boolean expressions

## Additional Resources

- [Python Documentation: Boolean Operations](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)
- [Real Python: Python Booleans](https://realpython.com/python-boolean/)
- [W3Schools: Python Booleans](https://www.w3schools.com/python/python_booleans.asp)
