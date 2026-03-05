# Counters

## Learning Objectives

- Use Counter to count hashable objects
- Apply Counter methods for common operations
- Combine and manipulate Counters

## Why This Matters

Counting occurrences is a common programming task - from word frequency analysis to tracking inventory. Counter provides an optimized, readable way to handle counting that would otherwise require manual dictionary management.

## Concept

### What Is Counter?

Counter is a dict subclass for counting hashable objects:

```python
from collections import Counter

# Count elements in a list
colors = ["red", "blue", "red", "green", "blue", "blue"]
count = Counter(colors)
print(count)  # Counter({'blue': 3, 'red': 2, 'green': 1})
```

### Creating Counters

```python
from collections import Counter

# From a list
Counter(["a", "b", "a", "c"])
# Counter({'a': 2, 'b': 1, 'c': 1})

# From a string
Counter("mississippi")
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# From keyword arguments
Counter(a=2, b=1, c=3)
# Counter({'c': 3, 'a': 2, 'b': 1})

# From a dictionary
Counter({"red": 3, "blue": 2})
```

### Accessing Counts

```python
from collections import Counter

count = Counter(["a", "b", "a", "c", "a"])

# Get count of an element
print(count["a"])      # 3
print(count["b"])      # 1
print(count["z"])      # 0 (missing keys return 0, not KeyError)
```

### Counter Methods

**most_common(n):**

```python
count = Counter("abracadabra")
print(count.most_common(3))  # [('a', 5), ('b', 2), ('r', 2)]
print(count.most_common())   # All elements, sorted by count
```

**elements():**

```python
count = Counter(a=2, b=3)
list(count.elements())  # ['a', 'a', 'b', 'b', 'b']
```

**total():** (Python 3.10+)

```python
count = Counter(a=2, b=3, c=1)
count.total()  # 6
```

### Updating Counters

**update() - Add counts:**

```python
count = Counter(a=2, b=1)
count.update(["a", "c"])     # From iterable
count.update(b=2, c=1)       # From keywords
print(count)  # Counter({'a': 3, 'b': 3, 'c': 2})
```

**subtract() - Remove counts:**

```python
count = Counter(a=4, b=3)
count.subtract(["a", "a", "b"])
print(count)  # Counter({'a': 2, 'b': 2})
```

### Counter Arithmetic

```python
c1 = Counter(a=3, b=2)
c2 = Counter(a=1, b=2, c=1)

# Addition
c1 + c2  # Counter({'a': 4, 'b': 4, 'c': 1})

# Subtraction (keeps only positive counts)
c1 - c2  # Counter({'a': 2})

# Intersection (minimum)
c1 & c2  # Counter({'a': 1, 'b': 2})

# Union (maximum)
c1 | c2  # Counter({'a': 3, 'b': 2, 'c': 1})
```

### Practical Examples

**Word frequency in text:**

```python
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the fox"
words = text.lower().split()
word_count = Counter(words)

print("Most common words:")
for word, count in word_count.most_common(5):
    print(f"  {word}: {count}")
```

**Character frequency:**

```python
from collections import Counter

def analyze_password(password):
    counts = Counter(password)
    print(f"Unique characters: {len(counts)}")
    print(f"Most common: {counts.most_common(3)}")
    print(f"Has numbers: {any(c.isdigit() for c in counts)}")

analyze_password("password123")
```

**Inventory tracking:**

```python
from collections import Counter

# Starting inventory
inventory = Counter(apple=10, banana=5, orange=8)

# Sales
sales = ["apple", "apple", "banana", "orange", "apple"]
inventory.subtract(sales)

# Restock
inventory.update(banana=10, grape=15)

# Check low stock
low_stock = [item for item, count in inventory.items() if count < 5]
print(f"Low stock: {low_stock}")
```

**Finding duplicates:**

```python
from collections import Counter

def find_duplicates(items):
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]

numbers = [1, 2, 3, 2, 4, 3, 5, 3]
print(find_duplicates(numbers))  # [2, 3]
```

## Summary

Counter is a dict subclass for counting hashable objects. Create it from iterables, strings, or keyword arguments. Access counts with bracket notation - missing keys return 0. Use `most_common()` for ranked results and `elements()` to expand back to a list. Update counts with `update()` and `subtract()`. Counter supports arithmetic operations for combining counts.

## Resources

- [Python Docs: Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [Real Python: Python Counter](https://realpython.com/python-counter/)
