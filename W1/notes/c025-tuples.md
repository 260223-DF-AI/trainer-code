# Tuples

## Learning Objectives

- Understand what tuples are and how they differ from lists
- Create and access tuple elements
- Use tuple packing and unpacking

## Why This Matters

Tuples provide an immutable way to group related data. They are useful when you need to ensure data integrity, return multiple values from functions, or use collections as dictionary keys. Understanding when to use tuples versus lists is an important skill.

## The Concept

### What is a Tuple?

A **tuple** is an ordered, immutable collection of items. Once created, a tuple cannot be modified.

```python
# Creating tuples
point = (3, 4)
colors = ("red", "green", "blue")
mixed = (1, "hello", 3.14)
single = (42,)  # Note the comma for single-item tuple
empty = ()
```

### Tuple vs List

| Aspect | Tuple | List |
|--------|-------|------|
| Syntax | `()` | `[]` |
| Mutability | Immutable | Mutable |
| Performance | Slightly faster | Slightly slower |
| Use case | Fixed data | Dynamic data |
| Hashable | Yes (if contents are) | No |

### Creating Tuples

```python
# With parentheses
coordinates = (10, 20)

# Without parentheses (tuple packing)
coordinates = 10, 20

# From other iterables
t = tuple([1, 2, 3])  # (1, 2, 3)
t = tuple("hello")    # ('h', 'e', 'l', 'l', 'o')

# Single element (comma required)
single = (5,)
not_a_tuple = (5)  # This is just the integer 5
```

### Accessing Elements

Indexing and slicing work the same as lists:

```python
colors = ("red", "green", "blue", "yellow")

print(colors[0])     # red
print(colors[-1])    # yellow
print(colors[1:3])   # ('green', 'blue')
```

### Immutability

Tuples cannot be changed after creation:

```python
point = (3, 4)
# point[0] = 5  # TypeError: 'tuple' object does not support item assignment

# To "modify" a tuple, create a new one
point = (5, point[1])  # (5, 4)
```

### Tuple Unpacking

Extract tuple values into variables:

```python
# Basic unpacking
point = (3, 4)
x, y = point
print(x)  # 3
print(y)  # 4

# Unpacking in loops
points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"x={x}, y={y}")

# Extended unpacking with *
first, *rest = (1, 2, 3, 4, 5)
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

# Swapping values
a, b = 1, 2
a, b = b, a  # a=2, b=1
```

### Tuple Methods

Tuples have only two methods (due to immutability):

```python
t = (1, 2, 3, 2, 4, 2)

# Count occurrences
print(t.count(2))  # 3

# Find index
print(t.index(3))  # 2
```

### Tuple Operations

```python
# Concatenation
a = (1, 2)
b = (3, 4)
c = a + b  # (1, 2, 3, 4)

# Repetition
d = (0,) * 5  # (0, 0, 0, 0, 0)

# Membership
print(2 in (1, 2, 3))  # True

# Length
print(len((1, 2, 3)))  # 3
```

### Common Use Cases

#### Returning Multiple Values

```python
def get_dimensions():
    return (1920, 1080)

width, height = get_dimensions()
```

#### Dictionary Keys

Tuples can be dictionary keys (lists cannot):

```python
locations = {
    (40.7128, -74.0060): "New York",
    (34.0522, -118.2437): "Los Angeles"
}
```

#### Named Tuples (Preview)

For more readable tuples, Python provides `namedtuple`. We will explore this in a later topic on modules.

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)  # 3 4
```

## Summary

- Tuples are ordered, immutable collections
- Created with parentheses or comma-separated values
- Access elements with indexing and slicing (same as lists)
- Cannot be modified after creation
- Tuple unpacking extracts values into variables
- Use tuples for fixed data, returning multiple values, and dictionary keys

## Additional Resources

- [Python Documentation: Tuples](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [Real Python: Lists and Tuples](https://realpython.com/python-lists-tuples/)
- [W3Schools: Python Tuples](https://www.w3schools.com/python/python_tuples.asp)
