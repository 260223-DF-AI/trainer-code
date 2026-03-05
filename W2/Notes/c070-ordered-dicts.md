# Ordered Dicts

## Learning Objectives

- Understand OrderedDict and its history
- Know when OrderedDict is still useful
- Compare OrderedDict with regular dict behavior

## Why This Matters

Understanding OrderedDict helps you work with legacy code and understand Python's evolution. While regular dicts now preserve insertion order (Python 3.7+), OrderedDict still offers unique functionality for order-aware comparisons and reordering operations.

## Concept

### Historical Context

Before Python 3.7, regular dictionaries did not preserve insertion order:

```python
# Python 3.6 and earlier
d = {}
d["b"] = 1
d["a"] = 2
d["c"] = 3
# Order was NOT guaranteed when iterating
```

OrderedDict was created to guarantee order preservation.

### OrderedDict Basics

```python
from collections import OrderedDict

# Create OrderedDict
od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3

# Order is preserved
for key, value in od.items():
    print(key, value)
# first 1
# second 2
# third 3
```

### Regular Dict Now Preserves Order

Since Python 3.7, regular dicts preserve insertion order:

```python
# Python 3.7+
d = {}
d["first"] = 1
d["second"] = 2
d["third"] = 3

# Order is preserved
list(d.keys())  # ['first', 'second', 'third']
```

So why use OrderedDict?

### OrderedDict Unique Features

**1. Order-aware equality:**

```python
from collections import OrderedDict

od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False - different order

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True - regular dict ignores order
```

**2. move_to_end():**

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])

od.move_to_end("a")        # Move to end
print(list(od.keys()))     # ['b', 'c', 'a']

od.move_to_end("c", last=False)  # Move to beginning
print(list(od.keys()))     # ['c', 'b', 'a']
```

**3. popitem() with last parameter:**

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])

od.popitem()              # Pop last: ('c', 3)
od.popitem(last=False)    # Pop first: ('a', 1)
```

### Practical Use Cases

**LRU (Least Recently Used) Cache:**

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

cache = LRUCache(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
cache.get("a")      # Moves "a" to end
cache.put("d", 4)   # Evicts "b" (least recently used)
```

**Order-sensitive comparisons:**

```python
from collections import OrderedDict

def configs_match(config1, config2):
    """Check if configs are equal including key order."""
    return OrderedDict(config1) == OrderedDict(config2)

# Useful when order matters (like in dependency resolution)
deps1 = [("numpy", "1.0"), ("pandas", "2.0")]
deps2 = [("pandas", "2.0"), ("numpy", "1.0")]
print(configs_match(deps1, deps2))  # False
```

### When to Use OrderedDict

**Use OrderedDict when you need:**

- Order-aware equality comparisons
- `move_to_end()` functionality
- `popitem(last=False)` (FIFO behavior)
- Compatibility with Python < 3.7

**Use regular dict when:**

- You just need insertion order preserved
- Order doesn't affect equality
- You're on Python 3.7+

### Performance Comparison

```python
# Memory: OrderedDict uses ~2x memory of regular dict
# Speed: Regular dict is slightly faster for basic operations
```

For most use cases, regular dict is sufficient and preferred.

## Summary

OrderedDict was essential before Python 3.7 for preserving insertion order. Regular dicts now preserve order, but OrderedDict still offers unique features: order-aware equality (`od1 == od2` considers order), `move_to_end()` for reordering, and `popitem(last=False)` for FIFO behavior. Use OrderedDict when these features matter; otherwise, prefer regular dict.

## Resources

- [Python Docs: OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- [Real Python: OrderedDict vs dict](https://realpython.com/python-ordereddict/)
- [PEP 468: Preserving Keyword Argument Order](https://peps.python.org/pep-0468/)
