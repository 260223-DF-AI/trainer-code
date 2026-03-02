# Math Module

## Learning Objectives

- Use Python's math module for mathematical operations
- Apply common mathematical functions
- Work with constants like pi and e
- Understand when to use math vs built-in operations

## Why This Matters

The math module provides access to mathematical functions beyond basic arithmetic. Whether you're calculating distances, working with angles, or processing scientific data, these functions are essential. Understanding the math module prepares you for more advanced numerical work with libraries like NumPy.

## Concept

### Importing the Math Module

```python
import math

# Or import specific functions
from math import sqrt, pi, ceil
```

### Mathematical Constants

```python
import math

print(math.pi)    # 3.141592653589793
print(math.e)     # 2.718281828459045
print(math.tau)   # 6.283185307179586 (2 * pi)
print(math.inf)   # Positive infinity
print(math.nan)   # Not a Number
```

### Basic Mathematical Functions

**Power and Roots:**

```python
import math

# Square root
print(math.sqrt(16))       # 4.0
print(math.sqrt(2))        # 1.4142135623730951

# Power (alternative to **)
print(math.pow(2, 3))      # 8.0

# Exponential (e^x)
print(math.exp(1))         # 2.718281828459045
print(math.exp(2))         # 7.38905609893065
```

**Logarithms:**

```python
# Natural logarithm (base e)
print(math.log(math.e))    # 1.0
print(math.log(10))        # 2.302585092994046

# Logarithm base 10
print(math.log10(100))     # 2.0
print(math.log10(1000))    # 3.0

# Logarithm base 2
print(math.log2(8))        # 3.0
print(math.log2(1024))     # 10.0

# Logarithm with custom base
print(math.log(8, 2))      # 3.0
```

### Rounding Functions

```python
import math

x = 4.7
y = -4.7

# Round up (ceiling)
print(math.ceil(x))        # 5
print(math.ceil(y))        # -4

# Round down (floor)
print(math.floor(x))       # 4
print(math.floor(y))       # -5

# Truncate (remove decimal, toward zero)
print(math.trunc(x))       # 4
print(math.trunc(y))       # -4
```

### Trigonometric Functions

Angles are in **radians**, not degrees:

```python
import math

# Convert degrees to radians
angle_deg = 45
angle_rad = math.radians(angle_deg)

# Trigonometric functions (input in radians)
print(math.sin(angle_rad))  # 0.7071067811865476
print(math.cos(angle_rad))  # 0.7071067811865476
print(math.tan(angle_rad))  # 0.9999999999999999

# Inverse trigonometric functions
print(math.asin(0.5))       # 0.5235987755982989 (radians)
print(math.degrees(math.asin(0.5)))  # 30.0 (degrees)

# Convert radians to degrees
print(math.degrees(math.pi))  # 180.0
```

### Other Useful Functions

```python
import math

# Absolute value (also built-in abs())
print(math.fabs(-5.5))      # 5.5

# Factorial
print(math.factorial(5))    # 120 (5 * 4 * 3 * 2 * 1)

# Greatest common divisor
print(math.gcd(48, 18))     # 6

# Check for special values
print(math.isnan(math.nan)) # True
print(math.isinf(math.inf)) # True
print(math.isfinite(10.5))  # True

# Hypotenuse (sqrt(x^2 + y^2))
print(math.hypot(3, 4))     # 5.0
```

### Practical Examples

**Calculate Circle Properties:**

```python
import math

radius = 5

circumference = 2 * math.pi * radius
area = math.pi * radius ** 2

print(f"Radius: {radius}")
print(f"Circumference: {circumference:.2f}")
print(f"Area: {area:.2f}")
```

**Distance Between Two Points:**

```python
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Or use hypot
def distance_v2(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

print(distance(0, 0, 3, 4))  # 5.0
```

**Compound Interest:**

```python
import math

principal = 1000
rate = 0.05  # 5%
years = 10
n = 12  # Monthly compounding

amount = principal * math.pow(1 + rate/n, n * years)
print(f"After {years} years: ${amount:.2f}")
```

### Math vs Built-in Functions

Python has some built-in functions that overlap with math:

```python
# Built-in
abs(-5)       # Works with int and float
pow(2, 3)     # Can take modulo: pow(2, 3, 5) = 3
round(4.5)    # Banker's rounding

# Math module
math.fabs(-5) # Always returns float
math.pow(2, 3) # Always returns float
# math has no round equivalent
```

## Summary

The math module provides mathematical functions beyond basic arithmetic. Use `math.sqrt()` for square roots, `math.log()` for logarithms, and trigonometric functions like `math.sin()` (which use radians). Constants like `math.pi` and `math.e` are available. Rounding functions include `math.ceil()`, `math.floor()`, and `math.trunc()`. For heavy numerical work, NumPy (covered later this week) offers even more capabilities.

## Resources

- [Python Docs: math](https://docs.python.org/3/library/math.html)
- [Real Python: Python math Module](https://realpython.com/python-math-module/)
- [W3Schools: Python Math](https://www.w3schools.com/python/module_math.asp)
