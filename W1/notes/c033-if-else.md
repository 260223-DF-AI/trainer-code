# If-Else

## Learning Objectives

- Write conditional statements using if, elif, and else
- Understand how conditions are evaluated
- Use nested conditionals appropriately

## Why This Matters

Conditional statements allow your programs to make decisions. Based on conditions, your code can take different paths, enabling everything from simple validations to complex business logic. Understanding conditionals is fundamental to programming.

## The Concept

### The if Statement

The `if` statement executes code only when a condition is True:

```python
age = 18

if age >= 18:
    print("You are an adult")
```

### The if-else Statement

Add an `else` clause to handle the False case:

```python
age = 16

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

### The if-elif-else Statement

Use `elif` (else if) for multiple conditions:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")  # Your grade is: B
```

### How Conditions Work

- Conditions are evaluated from top to bottom
- The first True condition executes; remaining conditions are skipped
- `else` is optional and catches all remaining cases

```python
x = 15

if x < 10:
    print("Less than 10")
elif x < 20:
    print("Less than 20")  # This prints
elif x < 30:
    print("Less than 30")  # Skipped (previous was True)
```

### Truthy and Falsy Values

Conditions do not need to be boolean expressions:

```python
name = "Alice"

if name:
    print(f"Hello, {name}")  # Executes (non-empty string is truthy)

items = []

if not items:
    print("List is empty")  # Executes (empty list is falsy)
```

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

### Logical Operators

```python
age = 25
has_license = True

# and - both must be True
if age >= 18 and has_license:
    print("You can drive")

# or - at least one must be True
if age < 13 or age > 65:
    print("Discount available")

# not - inverts the condition
if not has_license:
    print("Get a license first")
```

### Nested Conditionals

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
    else:
        print("ID required")
else:
    print("Must be 18 or older")
```

### Conditional Expression (Ternary)

A one-line if-else:

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # adult

# Equivalent to:
if age >= 18:
    status = "adult"
else:
    status = "minor"
```

### Common Patterns

```python
# Checking None
value = None
if value is None:
    print("No value provided")

# Checking type
data = "hello"
if isinstance(data, str):
    print("It's a string")

# Multiple values
color = "red"
if color in ["red", "green", "blue"]:
    print("Primary color")

# Range check
x = 50
if 0 <= x <= 100:
    print("Valid percentage")
```

### Best Practices

- Keep conditions simple and readable
- Avoid deeply nested conditionals (consider refactoring)
- Use early returns to reduce nesting
- Use `elif` instead of nested `if` when appropriate

## Summary

- `if` executes code when a condition is True
- `elif` provides additional conditions
- `else` handles all remaining cases
- Conditions can use comparison and logical operators
- Truthy/falsy values work directly in conditions
- Ternary expressions provide one-line conditionals

## Additional Resources

- [Python Documentation: if Statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements)
- [Real Python: Conditional Statements](https://realpython.com/python-conditional-statements/)
- [W3Schools: Python If...Else](https://www.w3schools.com/python/python_conditions.asp)
