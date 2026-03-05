# Collections Module

## Learning Objectives

- Understand the collections module's purpose
- Know when to use specialized container types
- Apply collections for common programming patterns

## Why This Matters

Python's built-in data structures (list, dict, set, tuple) cover most needs, but the collections module provides specialized alternatives that are more efficient or convenient for specific tasks. Using the right collection type makes your code cleaner and faster.

## Concept

### What Is the Collections Module?

The collections module provides specialized container data types that extend Python's built-in containers:

| Type | Purpose |
|------|---------|
| `Counter` | Count hashable objects |
| `namedtuple` | Tuple with named fields |
| `OrderedDict` | Dict that remembers insertion order |
| `defaultdict` | Dict with default values |
| `deque` | Double-ended queue |

### Importing from Collections

```python
from collections import Counter, namedtuple, OrderedDict, defaultdict, deque
```

### Overview Examples

**Counter - Count occurrences:**

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)
print(count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count.most_common(2))  # [('apple', 3), ('banana', 2)]
```

**namedtuple - Readable tuples:**

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)  # 3 4
```

**defaultdict - Dict with defaults:**

```python
from collections import defaultdict

counts = defaultdict(int)
for word in words:
    counts[word] += 1  # No KeyError, defaults to 0
```

**deque - Efficient double-ended queue:**

```python
from collections import deque

d = deque([1, 2, 3])
d.appendleft(0)   # [0, 1, 2, 3]
d.append(4)       # [0, 1, 2, 3, 4]
d.popleft()       # [1, 2, 3, 4]
```

### When to Use Each

| Use Case | Collection |
|----------|------------|
| Count elements in a list | Counter |
| Create struct-like objects | namedtuple |
| Dict that needs default values | defaultdict |
| Remember dict insertion order | OrderedDict (or regular dict in 3.7+) |
| Fast append/pop from both ends | deque |

### defaultdict in Detail

Avoids KeyError by providing default values:

```python
from collections import defaultdict

# Default to empty list
groups = defaultdict(list)
for name, group in [("Alice", "A"), ("Bob", "B"), ("Charlie", "A")]:
    groups[group].append(name)
# {'A': ['Alice', 'Charlie'], 'B': ['Bob']}

# Default to 0
counts = defaultdict(int)
for item in ["a", "b", "a", "c", "a"]:
    counts[item] += 1
# {'a': 3, 'b': 1, 'c': 1}

# Default to set
word_indices = defaultdict(set)
words = ["apple", "banana", "apple"]
for i, word in enumerate(words):
    word_indices[word].add(i)
# {'apple': {0, 2}, 'banana': {1}}
```

### deque in Detail

Efficient for operations at both ends:

```python
from collections import deque

# Create deque
d = deque([1, 2, 3])

# Add elements
d.append(4)        # Right end: [1, 2, 3, 4]
d.appendleft(0)    # Left end: [0, 1, 2, 3, 4]

# Remove elements
d.pop()            # From right: 4
d.popleft()        # From left: 0

# Rotate
d = deque([1, 2, 3, 4, 5])
d.rotate(2)        # [4, 5, 1, 2, 3]
d.rotate(-2)       # [1, 2, 3, 4, 5]

# Fixed-size deque (sliding window)
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
print(recent)      # deque([2, 3, 4], maxlen=3)
```

The following lessons cover Counter, namedtuple, and OrderedDict in detail.

## Summary

The collections module extends Python's built-in containers. Use Counter for counting, namedtuple for readable data structures, defaultdict to avoid KeyError, and deque for efficient double-ended queues. These specialized types make common patterns easier and more efficient. The next lessons explore Counter, namedtuple, and OrderedDict in depth.

## Resources

- [Python Docs: collections](https://docs.python.org/3/library/collections.html)
- [Real Python: Python Collections](https://realpython.com/python-collections-module/)
- [Python Counter Tutorial](https://realpython.com/python-counter/)
