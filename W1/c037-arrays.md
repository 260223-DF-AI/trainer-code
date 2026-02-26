# Arrays

## Learning Objectives

- Understand Python's array module
- Compare arrays to lists
- Recognize when to use arrays

## Why This Matters

While Python lists are highly flexible, the `array` module provides a more memory-efficient way to store homogeneous data. Understanding the difference helps you choose the right data structure for performance-critical applications.

## The Concept

### Lists vs Arrays

Python has two main ways to store sequences of items:

| Feature | List | Array |
|---------|------|-------|
| Types | Mixed types allowed | Single type only |
| Flexibility | Very flexible | Type-restricted |
| Memory | Higher overhead | More compact |
| Import | Built-in | Requires `import array` |
| Operations | Rich set of methods | Basic operations |

### When to Use Arrays

- When you have large amounts of homogeneous numeric data
- When memory efficiency matters
- For interoperability with C code

For most purposes, **lists are preferred**. For serious numeric work, NumPy arrays are typically used instead of the built-in array module.

### Creating Arrays

```python
from array import array

# Type codes define the element type
# 'i' = signed integer
# 'f' = float
# 'd' = double

# Integer array
int_array = array('i', [1, 2, 3, 4, 5])
print(int_array)  # array('i', [1, 2, 3, 4, 5])

# Float array
float_array = array('f', [1.0, 2.5, 3.7])
print(float_array)  # array('f', [1.0, 2.5, 3.700000047683716])

# From a list
numbers = [10, 20, 30]
arr = array('i', numbers)
```

### Common Type Codes

| Code | C Type | Python Type | Minimum Size |
|------|--------|-------------|--------------|
| 'b' | signed char | int | 1 byte |
| 'B' | unsigned char | int | 1 byte |
| 'i' | signed int | int | 2 bytes |
| 'I' | unsigned int | int | 2 bytes |
| 'f' | float | float | 4 bytes |
| 'd' | double | float | 8 bytes |

### Accessing Elements

```python
from array import array

arr = array('i', [10, 20, 30, 40, 50])

# Indexing
print(arr[0])   # 10
print(arr[-1])  # 50

# Slicing
print(arr[1:4])  # array('i', [20, 30, 40])
```

### Modifying Arrays

```python
from array import array

arr = array('i', [1, 2, 3])

# Change element
arr[1] = 20
print(arr)  # array('i', [1, 20, 3])

# Append
arr.append(4)
print(arr)  # array('i', [1, 20, 3, 4])

# Extend
arr.extend([5, 6])
print(arr)  # array('i', [1, 20, 3, 4, 5, 6])

# Insert
arr.insert(0, 0)
print(arr)  # array('i', [0, 1, 20, 3, 4, 5, 6])

# Remove
arr.remove(20)
print(arr)  # array('i', [0, 1, 3, 4, 5, 6])

# Pop
last = arr.pop()
print(last)  # 6
```

### Array Methods

```python
from array import array

arr = array('i', [1, 2, 2, 3, 2, 4])

# Count occurrences
print(arr.count(2))  # 3

# Find index
print(arr.index(3))  # 3

# Reverse in place
arr.reverse()
print(arr)  # array('i', [4, 2, 3, 2, 2, 1])

# Convert to list
lst = arr.tolist()
print(lst)  # [4, 2, 3, 2, 2, 1]
```

### Type Enforcement

```python
from array import array

int_arr = array('i', [1, 2, 3])

# This works
int_arr.append(4)

# This raises TypeError
# int_arr.append(3.5)  # Floats not allowed in int array

# This truncates (Python 2 behavior may vary)
# int_arr.append(3.9)  # May truncate to 3
```

### Memory Efficiency

```python
import sys
from array import array

# List of 1000 integers
lst = list(range(1000))
print(sys.getsizeof(lst))  # Around 8856 bytes

# Array of 1000 integers
arr = array('i', range(1000))
print(sys.getsizeof(arr))  # Around 4064 bytes
```

### NumPy Alternative (Preview)

For serious numeric work, NumPy provides better performance:

```python
# NumPy arrays (covered in a later topic)
import numpy as np

np_arr = np.array([1, 2, 3, 4, 5])
```

## Summary

- The `array` module stores homogeneous data more efficiently than lists
- Arrays require a type code to specify the element type
- Arrays support indexing, slicing, and many list-like operations
- For most use cases, lists are more convenient
- For scientific computing, NumPy arrays are preferred

## Additional Resources

- [Python Documentation: array](https://docs.python.org/3/library/array.html)
- [Real Python: array Module](https://realpython.com/python-array/)
- [NumPy Arrays](https://numpy.org/doc/stable/user/basics.creation.html)
