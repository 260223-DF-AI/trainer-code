# Operators

## Learning Objectives

- Understand the different types of operators in Python
- Use arithmetic, comparison, logical, and assignment operators
- Recognize membership and identity operators

## Why This Matters

Operators are the tools you use to perform calculations, make comparisons, and control logic in your programs. Mastering operators enables you to write expressive, efficient code.

## The Concept

### Arithmetic Operators

Perform mathematical operations:

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `5 / 2` | `2.5` |
| `//` | Floor Division | `5 // 2` | `2` |
| `%` | Modulus (remainder) | `5 % 2` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

```python
a = 10
b = 3

print(a + b)   # 13
print(a / b)   # 3.333...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000
```

### Comparison Operators

Compare values and return `True` or `False`:

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `==` | Equal | `5 == 5` | `True` |
| `!=` | Not equal | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater or equal | `5 >= 5` | `True` |
| `<=` | Less or equal | `3 <= 5` | `True` |

```python
x = 10
y = 5

print(x == y)   # False
print(x > y)    # True
print(x != y)   # True
```

### Logical Operators

Combine boolean expressions:

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `and` | True if both are True | `True and False` | `False` |
| `or` | True if at least one is True | `True or False` | `True` |
| `not` | Inverts the boolean | `not True` | `False` |

```python
a = True
b = False

print(a and b)  # False
print(a or b)   # True
print(not a)    # False
```

### Assignment Operators

Assign and update values:

| Operator | Equivalent | Example |
|----------|------------|---------|
| `=` | Assign | `x = 5` |
| `+=` | `x = x + y` | `x += 3` |
| `-=` | `x = x - y` | `x -= 3` |
| `*=` | `x = x * y` | `x *= 3` |
| `/=` | `x = x / y` | `x /= 3` |
| `//=` | `x = x // y` | `x //= 3` |
| `%=` | `x = x % y` | `x %= 3` |
| `**=` | `x = x ** y` | `x **= 3` |

```python
x = 10
x += 5   # x is now 15
x *= 2   # x is now 30
```

### Membership Operators

Check if a value exists in a sequence:

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `in` | True if value is in sequence | `3 in [1, 2, 3]` | `True` |
| `not in` | True if value is not in sequence | `4 not in [1, 2, 3]` | `True` |

```python
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)      # True
print("grape" not in fruits)  # True
```

### Identity Operators

Check if two variables refer to the same object in memory:

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | True if same object | `a is b` |
| `is not` | True if not same object | `a is not b` |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)      # True (same values)
print(a is b)      # False (different objects)
print(a is c)      # True (same object)
```

### Operator Precedence

Python follows standard mathematical precedence:

1. `**` (exponentiation)
2. `*`, `/`, `//`, `%`
3. `+`, `-`
4. Comparison operators
5. `not`
6. `and`
7. `or`

Use parentheses to control order:

```python
result = (2 + 3) * 4  # 20, not 14
```

## Summary

- Arithmetic operators perform math: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Comparison operators compare values: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logical operators combine booleans: `and`, `or`, `not`
- Assignment operators update values: `=`, `+=`, `-=`, etc.
- Membership operators check sequences: `in`, `not in`
- Identity operators check object identity: `is`, `is not`

## Additional Resources

- [Python Documentation: Expressions](https://docs.python.org/3/reference/expressions.html)
- [W3Schools: Python Operators](https://www.w3schools.com/python/python_operators.asp)
- [Real Python: Operators and Expressions](https://realpython.com/python-operators-expressions/)
