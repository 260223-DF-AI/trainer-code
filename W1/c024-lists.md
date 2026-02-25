# Lists

## Learning Objectives

- Create and manipulate lists in Python
- Access elements using indexing and slicing
- Use common list methods for adding, removing, and modifying elements

## Why This Matters

Lists are one of Python's most versatile data structures. They allow you to store collections of items, iterate over data, and perform countless operations. Understanding lists is essential for data manipulation and processing.

## The Concept

### What is a List?

A **list** is an ordered, mutable collection of items. Lists can contain items of any type, including mixed types.

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]
mixed = [1, "hello", 3.14, True]
empty = []
```

### List Characteristics

- **Ordered:** Items maintain their insertion order
- **Mutable:** You can modify, add, and remove items
- **Allows duplicates:** Items can appear more than once
- **Heterogeneous:** Can contain different types

### Accessing Elements

Use index notation (0-indexed):

```python
fruits = ["apple", "banana", "cherry", "date"]

print(fruits[0])    # apple
print(fruits[2])    # cherry
print(fruits[-1])   # date (last item)
print(fruits[-2])   # cherry (second to last)
```

### Slicing Lists

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])    # [2, 3, 4]
print(numbers[:4])     # [0, 1, 2, 3]
print(numbers[6:])     # [6, 7, 8, 9]
print(numbers[::2])    # [0, 2, 4, 6, 8] (every 2nd)
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reversed)
```

### Modifying Lists

Lists are mutable - you can change individual elements:

```python
colors = ["red", "green", "blue"]
colors[1] = "yellow"
print(colors)  # ["red", "yellow", "blue"]
```

### Common List Methods

| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add item to end | `lst.append(4)` |
| `insert(i, x)` | Insert at position | `lst.insert(0, "first")` |
| `extend(iter)` | Add all items from iterable | `lst.extend([4, 5])` |
| `remove(x)` | Remove first occurrence | `lst.remove("a")` |
| `pop(i)` | Remove and return item at index | `lst.pop(0)` |
| `clear()` | Remove all items | `lst.clear()` |
| `index(x)` | Find index of item | `lst.index("a")` |
| `count(x)` | Count occurrences | `lst.count(5)` |
| `sort()` | Sort in place | `lst.sort()` |
| `reverse()` | Reverse in place | `lst.reverse()` |
| `copy()` | Return shallow copy | `new = lst.copy()` |

```python
items = [3, 1, 4, 1, 5]

items.append(9)        # [3, 1, 4, 1, 5, 9]
items.insert(0, 2)     # [2, 3, 1, 4, 1, 5, 9]
items.remove(1)        # [2, 3, 4, 1, 5, 9] (removes first 1)
popped = items.pop()   # 9; items is [2, 3, 4, 1, 5]
items.sort()           # [1, 2, 3, 4, 5]
```

### List Operations

```python
# Concatenation
a = [1, 2]
b = [3, 4]
c = a + b              # [1, 2, 3, 4]

# Repetition
d = [0] * 5            # [0, 0, 0, 0, 0]

# Membership
print(2 in [1, 2, 3])  # True

# Length
print(len([1, 2, 3]))  # 3
```

### Iterating Over Lists

```python
fruits = ["apple", "banana", "cherry"]

# Simple iteration
for fruit in fruits:
    print(fruit)

# With index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

### List Comprehensions

A concise way to create lists:

```python
# Traditional approach
squares = []
for x in range(5):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

### Nested Lists

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0])       # [1, 2, 3]
print(matrix[1][2])    # 6
```

## Summary

- Lists are ordered, mutable collections that allow duplicates
- Access elements with indexing (0-indexed) and slicing
- Methods like `append()`, `remove()`, and `sort()` modify lists in place
- List comprehensions provide concise syntax for creating lists
- Lists can be nested to create multi-dimensional structures

## Additional Resources

- [Python Documentation: Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Real Python: Python Lists](https://realpython.com/python-lists-tuples/)
- [W3Schools: Python Lists](https://www.w3schools.com/python/python_lists.asp)
