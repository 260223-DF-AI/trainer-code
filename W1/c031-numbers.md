# Numbers

## Learning Objectives

- Understand Python's numeric types: int, float, and complex
- Perform arithmetic and mathematical operations
- Use the math module for advanced calculations

## Why This Matters

Numbers are fundamental to programming. Whether you are calculating totals, processing data, or building algorithms, understanding how Python handles numeric types enables you to write accurate and efficient code.

## The Concept

### Numeric Types

Python has three built-in numeric types:

| Type | Description | Example |
|------|-------------|---------|
| `int` | Integer (whole numbers) | `42`, `-7`, `0` |
| `float` | Floating-point (decimals) | `3.14`, `-0.001` |
| `complex` | Complex numbers | `3+4j` |

### Integers (int)

Integers have unlimited precision in Python:

```python
x = 42
y = -17
big = 9999999999999999999999999999

print(type(x))  # <class 'int'>
```

### Integer Representations

```python
# Decimal (default)
decimal = 255

# Binary (prefix 0b)
binary = 0b11111111  # 255

# Octal (prefix 0o)
octal = 0o377  # 255

# Hexadecimal (prefix 0x)
hexadecimal = 0xff  # 255

# Convert to different bases
print(bin(255))  # 0b11111111
print(oct(255))  # 0o377
print(hex(255))  # 0xff
```

### Floats (float)

Floating-point numbers represent decimals:

```python
pi = 3.14159
temperature = -40.0
tiny = 0.000001

# Scientific notation
scientific = 1.5e6    # 1500000.0
small = 2.5e-3        # 0.0025

print(type(pi))  # <class 'float'>
```

### Float Precision

Floats have limited precision due to binary representation:

```python
# Precision issues
print(0.1 + 0.2)  # 0.30000000000000004

# For precise decimal math, use the decimal module
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
```

### Complex Numbers

Complex numbers have real and imaginary parts:

```python
z = 3 + 4j

print(z.real)      # 3.0
print(z.imag)      # 4.0
print(abs(z))      # 5.0 (magnitude)

# Complex arithmetic
z1 = 2 + 3j
z2 = 1 - 1j
print(z1 + z2)     # (3+2j)
print(z1 * z2)     # (5+1j)
```

### Arithmetic Operations

```python
a = 10
b = 3

print(a + b)   # 13 (addition)
print(a - b)   # 7 (subtraction)
print(a * b)   # 30 (multiplication)
print(a / b)   # 3.333... (division)
print(a // b)  # 3 (floor division)
print(a % b)   # 1 (modulus)
print(a ** b)  # 1000 (exponentiation)
```

### Built-in Numeric Functions

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(abs(-42))         # 42
print(round(3.7))       # 4
print(round(3.14159, 2))  # 3.14
print(min(numbers))     # 1
print(max(numbers))     # 9
print(sum(numbers))     # 31
print(pow(2, 10))       # 1024
```

### The math Module

```python
import math

# Constants
print(math.pi)      # 3.141592653589793
print(math.e)       # 2.718281828459045

# Common functions
print(math.sqrt(16))     # 4.0
print(math.ceil(3.2))    # 4
print(math.floor(3.8))   # 3
print(math.log(100, 10)) # 2.0
print(math.log10(100))   # 2.0
print(math.exp(1))       # 2.718...

# Trigonometry (radians)
print(math.sin(math.pi / 2))  # 1.0
print(math.cos(0))            # 1.0
print(math.radians(180))      # 3.14159...
print(math.degrees(math.pi))  # 180.0
```

### Type Conversion

```python
# Float to int (truncates)
print(int(3.9))      # 3
print(int(-3.9))     # -3

# Int to float
print(float(42))     # 42.0

# String to number
print(int("42"))     # 42
print(float("3.14")) # 3.14
```

### Infinity and NaN

```python
import math

# Infinity
inf = float("inf")
print(inf > 999999999)  # True
print(math.isinf(inf))  # True

# Not a Number
nan = float("nan")
print(math.isnan(nan))  # True
print(nan == nan)       # False (NaN is never equal to itself)
```

## Summary

- Python has three numeric types: `int`, `float`, `complex`
- Integers have unlimited precision
- Floats have limited precision; use `Decimal` for precision
- The `math` module provides advanced mathematical functions
- Use `abs()`, `round()`, `min()`, `max()`, `sum()` for common operations

## Additional Resources

- [Python Documentation: Numeric Types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [Python math Module](https://docs.python.org/3/library/math.html)
- [Real Python: Numbers in Python](https://realpython.com/python-numbers/)
