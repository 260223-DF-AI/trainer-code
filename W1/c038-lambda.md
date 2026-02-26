# Lambda Functions

## Learning Objectives

- Understand what lambda functions are
- Write simple lambda expressions
- Use lambdas with map(), filter(), and sorted()

## Why This Matters

Lambda functions provide a concise way to create small, anonymous functions. They are especially useful with higher-order functions like `map()`, `filter()`, and `sorted()`, enabling functional programming patterns in Python.

## The Concept

### What is a Lambda Function?

A **lambda function** is a small, anonymous function defined with the `lambda` keyword. Unlike regular functions defined with `def`, lambdas are written in a single expression.

```python
# Regular function
def square(x):
    return x ** 2

# Equivalent lambda
square = lambda x: x ** 2

print(square(5))  # 25
```

### Lambda Syntax

```python
lambda arguments: expression
```

- `lambda` keyword introduces the function
- `arguments` are comma-separated (like regular functions)
- `expression` is evaluated and returned (no `return` keyword)

### Examples

```python
# Single argument
double = lambda x: x * 2
print(double(5))  # 10

# Multiple arguments
add = lambda a, b: a + b
print(add(3, 4))  # 7

# No arguments
greet = lambda: "Hello!"
print(greet())  # Hello!

# Conditional expression
classify = lambda x: "even" if x % 2 == 0 else "odd"
print(classify(7))  # odd
```

### Lambda with map()

Apply a function to every item in an iterable:

```python
numbers = [1, 2, 3, 4, 5]

# Using lambda
squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

# Equivalent list comprehension
squares = [x ** 2 for x in numbers]
```

### Lambda with filter()

Filter items based on a condition:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# Equivalent list comprehension
evens = [x for x in numbers if x % 2 == 0]
```

### Lambda with sorted()

Customize sorting with a key function:

```python
# Sort strings by length
words = ["apple", "pie", "banana", "cat"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)  # ['pie', 'cat', 'apple', 'banana']

# Sort dictionaries by value
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
by_age = sorted(people, key=lambda p: p["age"])
print(by_age)  # Bob (25), Alice (30), Charlie (35)

# Reverse sort
by_age_desc = sorted(people, key=lambda p: p["age"], reverse=True)
```

### Lambda with reduce()

Reduce a sequence to a single value:

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda a, b: a + b, numbers)
print(total)  # 15

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5
```

### Lambda Limitations

Lambdas are restricted to single expressions:

```python
# Cannot use statements
# lambda x: print(x); return x  # Syntax error

# Cannot use multiple statements
# lambda x:
#     y = x + 1
#     return y  # Syntax error

# Use def for complex logic
def complex_logic(x):
    y = x + 1
    z = y * 2
    return z
```

### When to Use Lambdas

**Good uses:**

- Short operations with `map()`, `filter()`, `sorted()`
- Callbacks that need simple logic
- One-off functions used immediately

**Avoid when:**

- Logic is complex or multiline
- Function needs to be reused (define with `def`)
- Readability suffers

### Lambda vs def

```python
# Lambda - quick, inline
sorted(items, key=lambda x: x.value)

# def - reusable, documented
def get_value(item):
    """Return the value attribute of the item."""
    return item.value

sorted(items, key=get_value)
```

## Summary

- Lambda creates small, anonymous functions
- Syntax: `lambda arguments: expression`
- Useful with `map()`, `filter()`, `sorted()`, and `reduce()`
- Limited to single expressions
- Use `def` for complex or reusable functions

## Additional Resources

- [Python Documentation: Lambda Expressions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions)
- [Real Python: Lambda Functions](https://realpython.com/python-lambda/)
- [W3Schools: Python Lambda](https://www.w3schools.com/python/python_lambda.asp)
