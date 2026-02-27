# Sets

## Learning Objectives

- Understand what sets are and their properties
- Create sets and perform set operations
- Recognize when to use sets versus lists

## Why This Matters

Sets are collections optimized for membership testing and eliminating duplicates. They provide mathematical set operations like union and intersection, making them powerful tools for data processing and comparison tasks.

## The Concept

### What is a Set?

A **set** is an unordered collection of unique items. Sets automatically eliminate duplicates and provide fast membership testing.

```python
# Creating sets
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}
empty_set = set()  # Note: {} creates an empty dict, not a set
```

### Set Characteristics

- **Unordered:** No guaranteed order; cannot access by index
- **Unique:** No duplicate items
- **Mutable:** Can add and remove items
- **Hashable items only:** Cannot contain lists or other sets

### Creating Sets

```python
# With curly braces
colors = {"red", "green", "blue"}

# From other iterables
from_list = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}
from_string = set("hello")           # {'h', 'e', 'l', 'o'}

# Empty set (must use set())
empty = set()
```

### Automatic Deduplication

```python
numbers = {1, 2, 2, 3, 3, 3, 4}
print(numbers)  # {1, 2, 3, 4}

# Remove duplicates from a list
items = [1, 2, 2, 3, 3, 3]
unique = list(set(items))  # [1, 2, 3]
```

### Modifying Sets

```python
fruits = {"apple", "banana"}

# Add single item
fruits.add("cherry")  # {"apple", "banana", "cherry"}

# Add multiple items
fruits.update(["date", "elderberry"])

# Remove item (raises error if not found)
fruits.remove("banana")

# Remove item (no error if not found)
fruits.discard("grape")

# Remove and return arbitrary item
item = fruits.pop()

# Clear all items
fruits.clear()
```

### Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (all items from both)
print(a | b)         # {1, 2, 3, 4, 5, 6}
print(a.union(b))    # Same

# Intersection (common items)
print(a & b)             # {3, 4}
print(a.intersection(b)) # Same

# Difference (in a but not b)
print(a - b)             # {1, 2}
print(a.difference(b))   # Same

# Symmetric difference (in a or b, but not both)
print(a ^ b)                     # {1, 2, 5, 6}
print(a.symmetric_difference(b)) # Same
```

### Set Comparisons

```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

# Subset (all elements of a are in b)
print(a <= b)         # True
print(a.issubset(b))  # True

# Superset (all elements of b are in a)
print(b >= a)           # True
print(b.issuperset(a))  # True

# Disjoint (no common elements)
c = {6, 7, 8}
print(a.isdisjoint(c))  # True
```

### Membership Testing

Sets provide O(1) average-case membership testing:

```python
large_set = set(range(1000000))

# Very fast
print(999999 in large_set)  # True

# Compare to:
# large_list = list(range(1000000))
# 999999 in large_list  # Much slower for large lists
```

### Iterating Over Sets

```python
colors = {"red", "green", "blue"}

for color in colors:
    print(color)  # Order not guaranteed
```

### Frozensets

An immutable version of set:

```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # Error! Frozensets are immutable

# Can be used as dictionary keys
cache = {frozenset([1, 2]): "value"}
```

### When to Use Sets

| Use Case | Why Sets? |
|----------|-----------|
| Remove duplicates | Automatic deduplication |
| Membership testing | O(1) lookup |
| Set operations | Union, intersection, difference |
| Finding common elements | Intersection |
| Finding unique elements | Difference |

## Summary

- Sets are unordered collections of unique items
- Created with `{}` or `set()` (empty sets require `set()`)
- Automatically remove duplicates
- Support mathematical operations: union, intersection, difference
- Provide fast membership testing (O(1) average)
- Use frozenset for immutable sets

## Additional Resources

- [Python Documentation: Sets](https://docs.python.org/3/library/stdtypes.html#set)
- [Real Python: Sets in Python](https://realpython.com/python-sets/)
- [W3Schools: Python Sets](https://www.w3schools.com/python/python_sets.asp)
