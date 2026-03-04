# NumPy

## Learning Objectives

- Understand NumPy arrays and their advantages
- Create and manipulate arrays
- Perform vectorized operations
- Apply common array functions

## Why This Matters

NumPy is the foundation of scientific computing in Python. It provides fast, memory-efficient arrays that power data science, machine learning, and scientific applications. Understanding NumPy is essential for working with pandas (covered later) and most data analysis tools.

## Concept

### What Is NumPy?

NumPy (Numerical Python) provides:

- Multi-dimensional arrays (ndarray)
- Vectorized operations (fast, no loops)
- Mathematical functions
- Linear algebra operations

### Installing NumPy

```bash
pip install numpy
```

### Creating Arrays

```python
import numpy as np

# From a list
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # [1 2 3 4 5]

# 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)
# [[1 2 3]
#  [4 5 6]]

# Special arrays
zeros = np.zeros(5)           # [0. 0. 0. 0. 0.]
ones = np.ones(3)             # [1. 1. 1.]
full = np.full(4, 7)          # [7 7 7 7]
range_arr = np.arange(0, 10, 2)  # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5)  # [0.   0.25 0.5  0.75 1.  ]
```

### Array Properties

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)    # (2, 3) - 2 rows, 3 columns
print(arr.ndim)     # 2 - number of dimensions
print(arr.size)     # 6 - total elements
print(arr.dtype)    # int64 - data type
```

### Indexing and Slicing

```python
arr = np.array([1, 2, 3, 4, 5])

# Single element
print(arr[0])       # 1
print(arr[-1])      # 5

# Slicing
print(arr[1:4])     # [2 3 4]
print(arr[:3])      # [1 2 3]
print(arr[::2])     # [1 3 5]

# 2D indexing
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, 0])     # 1
print(matrix[1, 2])     # 6
print(matrix[:, 0])     # [1 4 7] - first column
print(matrix[0, :])     # [1 2 3] - first row
print(matrix[0:2, 1:3]) # [[2 3] [5 6]] - submatrix
```

### Vectorized Operations

Operations apply to all elements without loops:

```python
arr = np.array([1, 2, 3, 4, 5])

# Arithmetic
print(arr + 10)      # [11 12 13 14 15]
print(arr * 2)       # [ 2  4  6  8 10]
print(arr ** 2)      # [ 1  4  9 16 25]

# Between arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)         # [5 7 9]
print(a * b)         # [ 4 10 18]
```

### Mathematical Functions

```python
arr = np.array([1, 4, 9, 16, 25])

print(np.sqrt(arr))      # [1. 2. 3. 4. 5.]
print(np.log(arr))       # [0.   1.39 2.20 2.77 3.22]
print(np.exp([1, 2]))    # [2.72 7.39]
print(np.sin([0, np.pi/2]))  # [0. 1.]
```

### Aggregate Functions

```python
arr = np.array([1, 2, 3, 4, 5])

print(np.sum(arr))       # 15
print(np.mean(arr))      # 3.0
print(np.median(arr))    # 3.0
print(np.std(arr))       # 1.41
print(np.min(arr))       # 1
print(np.max(arr))       # 5

# 2D aggregation
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(np.sum(matrix, axis=0))  # [5 7 9]  - sum columns
print(np.sum(matrix, axis=1))  # [6 15]   - sum rows
```

### Reshaping Arrays

```python
arr = np.arange(12)

# Reshape 1D to 2D
matrix = arr.reshape(3, 4)
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Flatten 2D to 1D
flat = matrix.flatten()
print(flat)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# Transpose
print(matrix.T)
# [[ 0  4  8]
#  [ 1  5  9]
#  [ 2  6 10]
#  [ 3  7 11]]
```

### Boolean Indexing

```python
arr = np.array([1, 2, 3, 4, 5, 6])

# Create boolean mask
mask = arr > 3
print(mask)               # [False False False  True  True  True]

# Filter using mask
print(arr[mask])          # [4 5 6]
print(arr[arr > 3])       # [4 5 6] - shorthand

# Multiple conditions
print(arr[(arr > 2) & (arr < 5)])  # [3 4]
```

### Why NumPy Is Fast

Python lists are slow for numerical operations:

```python
# Python list - slow
python_list = list(range(1000000))
result = [x * 2 for x in python_list]  # Creates new list, iterates

# NumPy array - fast
numpy_array = np.arange(1000000)
result = numpy_array * 2  # Vectorized, no Python loop
```

NumPy operations run in optimized C code, making them 10-100x faster.

### Practical Example

```python
import numpy as np

# Student scores
scores = np.array([
    [85, 90, 78],  # Student 1: Math, Science, English
    [92, 88, 95],  # Student 2
    [78, 82, 80],  # Student 3
    [90, 85, 88]   # Student 4
])

# Calculate statistics
print("Mean per subject:", np.mean(scores, axis=0))
print("Mean per student:", np.mean(scores, axis=1))
print("Highest score:", np.max(scores))
print("Students with avg > 85:", np.sum(np.mean(scores, axis=1) > 85))
```

## Summary

NumPy provides fast, efficient array operations for numerical computing. Create arrays with `np.array()`, `np.zeros()`, `np.arange()`, etc. Access elements with indexing and slicing. Perform vectorized operations without loops. Use aggregate functions like `sum()`, `mean()`, `std()`. Boolean indexing filters arrays based on conditions. NumPy is the foundation for data science libraries like pandas.

## Resources

- [NumPy Documentation](https://numpy.org/doc/stable/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Real Python: NumPy Tutorial](https://realpython.com/numpy-tutorial/)
