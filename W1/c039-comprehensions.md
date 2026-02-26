# Comprehensions

## Learning Objectives

- Write list, dictionary, and set comprehensions
- Transform data concisely using comprehension syntax
- Apply conditions to filter elements in comprehensions

## Why This Matters

Comprehensions are one of Python's most powerful and Pythonic features. They allow you to create new collections by transforming and filtering existing data in a single, readable line. Mastering comprehensions will make your code more concise, expressive, and often faster than traditional loops.

## Concept

### What Are Comprehensions?

Comprehensions provide a compact way to create collections (lists, dictionaries, sets) from existing iterables. They combine the creation of a new collection with a loop and optional filtering, all in a single expression.

### List Comprehensions

The most common type of comprehension creates a new list:

```python
# Traditional loop approach
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension equivalent
squares = [x ** 2 for x in range(10)]
# Result: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

**Syntax:** `[expression for item in iterable]`

### Adding Conditions

Filter elements using an `if` clause:

```python
# Only even numbers
evens = [x for x in range(20) if x % 2 == 0]
# Result: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Squares of even numbers only
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
# Result: [0, 4, 16, 36, 64]
```

**Syntax:** `[expression for item in iterable if condition]`

### Conditional Expressions

Use if-else within the expression itself:

```python
# Label numbers as even or odd
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# Result: ['even', 'odd', 'even', 'odd', 'even']
```

**Note:** Conditional expression (ternary) goes before `for`, while filtering condition goes after.

### Nested Loops

Comprehensions can include multiple `for` clauses:

```python
# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# Result: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create coordinate pairs
coords = [(x, y) for x in range(3) for y in range(3)]
# Result: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
```

### Dictionary Comprehensions

Create dictionaries using key-value pairs:

```python
# Create a dictionary of squares
squares_dict = {x: x ** 2 for x in range(6)}
# Result: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
# Result: {1: 'a', 2: 'b', 3: 'c'}

# Filter and transform
words = ["hello", "world", "python", "code"]
word_lengths = {word: len(word) for word in words if len(word) > 4}
# Result: {'hello': 5, 'world': 5, 'python': 6}
```

**Syntax:** `{key_expr: value_expr for item in iterable}`

### Set Comprehensions

Create sets using curly braces (without key-value pairs):

```python
# Unique squares
unique_squares = {x ** 2 for x in [-3, -2, -1, 0, 1, 2, 3]}
# Result: {0, 1, 4, 9}

# First letters
words = ["apple", "banana", "apricot", "cherry"]
first_letters = {word[0] for word in words}
# Result: {'a', 'b', 'c'}
```

**Syntax:** `{expression for item in iterable}`

### Practical Examples

**Processing Data:**

```python
# Convert temperatures from Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(c * 9/5) + 32 for c in celsius]
# Result: [32.0, 50.0, 68.0, 86.0, 104.0]
```

**Cleaning Data:**

```python
# Strip whitespace and convert to lowercase
raw_names = ["  Alice ", "BOB  ", " Charlie"]
clean_names = [name.strip().lower() for name in raw_names]
# Result: ['alice', 'bob', 'charlie']
```

**Extracting Fields:**

```python
# Get names from a list of dictionaries
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
names = [user["name"] for user in users]
# Result: ['Alice', 'Bob', 'Charlie']
```

### When to Use Comprehensions

**Use comprehensions when:**

- Creating a new collection from an existing iterable
- The logic is simple (one or two conditions)
- Readability is maintained

**Avoid comprehensions when:**

- The logic is complex (multiple nested conditions)
- Side effects are needed (like printing)
- The expression spans multiple lines

```python
# Too complex - use a regular loop instead
# BAD: Hard to read
result = [x if x > 0 else -x for x in data if x != 0 and x % 2 == 0]

# BETTER: Use a loop for complex logic
result = []
for x in data:
    if x != 0 and x % 2 == 0:
        result.append(x if x > 0 else -x)
```

## Summary

Comprehensions offer a concise, Pythonic way to create lists, dictionaries, and sets. List comprehensions use `[expression for item in iterable]`, dictionary comprehensions use `{key: value for item in iterable}`, and set comprehensions use `{expression for item in iterable}`. Add conditions with `if` to filter elements. While powerful, keep comprehensions simple; if they become hard to read, a traditional loop is often better.

## Resources

- [Python Docs: List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Real Python: List Comprehensions](https://realpython.com/list-comprehension-python/)
- [PEP 274: Dict Comprehensions](https://peps.python.org/pep-0274/)
