# Generator Expressions

## Learning Objectives

- Write generator expressions for inline generation
- Compare generator expressions with list comprehensions
- Apply generator expressions in common patterns
- Understand lazy evaluation benefits

## Why This Matters

Generator expressions provide a concise way to create generators without defining a function. They're perfect for single-use iterations and as arguments to functions like sum(), max(), and any(). Understanding when to use generator expressions instead of list comprehensions improves both code clarity and performance.

## Concept

### Generator Expressions vs List Comprehensions

The only syntax difference is brackets vs parentheses:

```python
# List comprehension - square brackets
squares_list = [x**2 for x in range(10)]

# Generator expression - parentheses
squares_gen = (x**2 for x in range(10))
```

But the behavior is very different:

```python
# List: All values computed and stored immediately
print(type(squares_list))  # <class 'list'>

# Generator: Values computed on demand
print(type(squares_gen))   # <class 'generator'>
```

### Lazy Evaluation

Generator expressions compute values only when needed:

```python
# List comprehension - runs immediately
def loud_square(x):
    print(f"Squaring {x}")
    return x ** 2

# All 5 calls happen immediately
list_result = [loud_square(x) for x in range(5)]
# Squaring 0
# Squaring 1
# Squaring 2
# Squaring 3
# Squaring 4

# Generator - nothing happens yet
gen_result = (loud_square(x) for x in range(5))
# (silence)

# Values computed on demand
next(gen_result)  # Squaring 0, returns 0
next(gen_result)  # Squaring 1, returns 1
```

### Using with Functions

Generator expressions are ideal as function arguments:

```python
# Sum of squares
total = sum(x**2 for x in range(100))  # No extra parentheses needed

# Any/all
has_even = any(x % 2 == 0 for x in [1, 3, 4, 7])  # True
all_positive = all(x > 0 for x in [1, 2, 3])       # True

# Max/min
max_length = max(len(word) for word in ["hello", "world", "python"])

# Join
csv_line = ",".join(str(x) for x in [1, 2, 3, 4, 5])  # "1,2,3,4,5"
```

### Filtering with Conditions

```python
# Even numbers only
evens = (x for x in range(20) if x % 2 == 0)

# Filter and transform
upper_long = (word.upper() for word in words if len(word) > 3)

# Complex conditions
valid_users = (
    user 
    for user in users 
    if user.active and user.age >= 18
)
```

### Nested Generator Expressions

```python
# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = (num for row in matrix for num in row)
list(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Nested with condition
positive_coords = (
    (x, y) 
    for x in range(-5, 6) 
    for y in range(-5, 6) 
    if x > 0 and y > 0
)
```

### One-Time Use

Generators are exhausted after one iteration:

```python
gen = (x**2 for x in range(5))

# First iteration works
print(list(gen))  # [0, 1, 4, 9, 16]

# Second iteration - empty!
print(list(gen))  # []
```

If you need to iterate multiple times, use a list.

### Practical Examples

**Find first match:**

```python
# Stops at first match (efficient for large data)
first_even = next((x for x in numbers if x % 2 == 0), None)
```

**Process file lines:**

```python
# Memory-efficient file processing
line_lengths = (len(line) for line in open("file.txt"))
avg_length = sum(line_lengths) / count
```

**Filter and count:**

```python
# Count without creating a list
error_count = sum(1 for line in log_lines if "ERROR" in line)
```

**Memory comparison:**

```python
import sys

# List: stores all values
list_comp = [x**2 for x in range(10000)]
print(sys.getsizeof(list_comp))  # ~87624 bytes

# Generator: stores only the expression
gen_exp = (x**2 for x in range(10000))
print(sys.getsizeof(gen_exp))    # ~112 bytes
```

### When to Use Each

| Use Case | Use List Comp | Use Gen Exp |
|----------|--------------|-------------|
| Need multiple iterations | Yes | No |
| Need random access | Yes | No |
| Large data, single pass | No | Yes |
| Function argument (sum, any) | No | Yes |
| Need list methods | Yes | No |
| Memory constrained | No | Yes |

```python
# Good: Generator for single pass
total = sum(x**2 for x in range(1000000))

# Good: List when you need it later
squares = [x**2 for x in range(100)]
print(max(squares))
print(min(squares))
print(squares[50])
```

## Summary

Generator expressions use parentheses instead of brackets and create generators that compute values lazily. They're perfect as function arguments where you don't need to keep the results: `sum(x for x in items)`. Use generator expressions for single-pass operations and large data; use list comprehensions when you need the result multiple times or need list methods. The memory savings can be dramatic for large datasets.

## Resources

- [Python Docs: Generator Expressions](https://docs.python.org/3/tutorial/classes.html#generator-expressions)
- [PEP 289: Generator Expressions](https://peps.python.org/pep-0289/)
- [Real Python: List Comprehensions and Generators](https://realpython.com/list-comprehension-python/)
