# Range

## Learning Objectives

- Understand the `range()` function and its parameters
- Use ranges in loops and list generation
- Recognize range as a memory-efficient sequence

## Why This Matters

The `range()` function is fundamental for creating sequences of numbers, especially for loops. It generates values on-demand rather than storing them all in memory, making it efficient for large sequences.

## The Concept

### What is Range?

`range()` is a built-in function that returns an immutable sequence of numbers. It is commonly used for looping a specific number of times.

### Range Syntax

```python
range(stop)             # 0 to stop-1
range(start, stop)      # start to stop-1
range(start, stop, step) # start to stop-1, stepping by step
```

### Basic Usage

```python
# range(stop) - starts at 0
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
```

### Negative Step

Count backwards:

```python
for i in range(10, 0, -1):
    print(i)  # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1

for i in range(5, -1, -1):
    print(i)  # 5, 4, 3, 2, 1, 0
```

### Range is a Sequence

Range objects support indexing and slicing:

```python
r = range(10)

print(r[0])      # 0
print(r[-1])     # 9
print(r[2:5])    # range(2, 5)
print(5 in r)    # True
print(len(r))    # 10
```

### Converting to List

Range objects are not lists, but can be converted:

```python
numbers = list(range(5))      # [0, 1, 2, 3, 4]
evens = list(range(0, 10, 2)) # [0, 2, 4, 6, 8]
```

### Memory Efficiency

Range objects do not store all values in memory; they generate them on demand:

```python
# This uses minimal memory
r = range(1000000000)  # One billion numbers

# This would use gigabytes of memory
# big_list = list(range(1000000000))  # Don't do this!

# Accessing elements is still fast
print(r[999999999])  # 999999999
```

### Common Patterns

```python
# Iterate n times
n = 5
for _ in range(n):
    print("Hello")

# Generate indices for a list
fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# Better: use enumerate instead
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# Create a list of numbers
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]
```

### Range in Conditional Expressions

```python
r = range(1, 10)

# Check membership
if 5 in r:
    print("5 is in range")

# Check min/max
print(min(r))  # 1
print(max(r))  # 9
print(sum(r))  # 45
```

### Range Comparison

```python
# Ranges with same values are equal
print(range(5) == range(0, 5))       # True
print(range(5) == range(0, 5, 1))    # True

# Different ranges
print(range(5) == range(1, 6))       # False
```

## Summary

- `range()` generates sequences of numbers on demand
- Syntax: `range(stop)`, `range(start, stop)`, `range(start, stop, step)`
- Negative step values count backwards
- Range is memory-efficient - it does not store all values
- Convert to list with `list(range(...))` when needed
- Use `enumerate()` when you need both index and value

## Additional Resources

- [Python Documentation: range()](https://docs.python.org/3/library/stdtypes.html#range)
- [Real Python: Python range()](https://realpython.com/python-range/)
- [W3Schools: Python Range](https://www.w3schools.com/python/ref_func_range.asp)
