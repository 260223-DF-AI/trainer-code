# Dictionaries

## Learning Objectives

- Create and manipulate dictionaries in Python
- Access, add, update, and delete key-value pairs
- Iterate over dictionaries and use common methods

## Why This Matters

Dictionaries are one of Python's most powerful and frequently used data structures. They provide fast key-based lookup and are used for everything from configuration to data transformation. Mastering dictionaries is essential for effective Python programming.

## The Concept

### What is a Dictionary?

A **dictionary** is an unordered collection of key-value pairs. Keys must be unique and immutable (strings, numbers, tuples); values can be anything.

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

empty = {}
```

### Dictionary Characteristics

- **Key-value pairs:** Each entry has a key and an associated value
- **Unique keys:** Keys must be unique; values can repeat
- **Mutable:** Can add, modify, and remove items
- **Fast lookup:** O(1) average-case access by key

### Accessing Values

```python
person = {"name": "Alice", "age": 30}

# Direct access (raises KeyError if missing)
print(person["name"])  # Alice

# get() method (returns None or default if missing)
print(person.get("age"))       # 30
print(person.get("email"))     # None
print(person.get("email", "N/A"))  # N/A
```

### Adding and Updating

```python
person = {"name": "Alice"}

# Add new key
person["age"] = 30

# Update existing key
person["name"] = "Alicia"

# Update multiple keys
person.update({"city": "Boston", "age": 31})

print(person)  # {'name': 'Alicia', 'age': 31, 'city': 'Boston'}
```

### Removing Items

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Remove specific key
del person["city"]

# Remove and return value
age = person.pop("age")  # 30

# Remove and return last inserted item
item = person.popitem()  # ('name', 'Alice')

# Clear all items
person.clear()
```

### Checking Keys

```python
person = {"name": "Alice", "age": 30}

print("name" in person)     # True
print("email" in person)    # False
print("email" not in person)  # True
```

### Dictionary Methods

| Method | Description |
|--------|-------------|
| `keys()` | Returns view of all keys |
| `values()` | Returns view of all values |
| `items()` | Returns view of all (key, value) pairs |
| `get(key, default)` | Returns value or default |
| `pop(key)` | Removes and returns value |
| `update(dict)` | Updates with another dict |
| `clear()` | Removes all items |
| `copy()` | Returns shallow copy |

```python
person = {"name": "Alice", "age": 30}

print(person.keys())    # dict_keys(['name', 'age'])
print(person.values())  # dict_values(['Alice', 30])
print(person.items())   # dict_items([('name', 'Alice'), ('age', 30)])
```

### Iterating Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Iterate over keys
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### Dictionary Comprehensions

```python
# Create dictionary from computation
squares = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter and transform
original = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered = {k: v for k, v in original.items() if v > 2}
# {'c': 3, 'd': 4}
```

### Nested Dictionaries

```python
users = {
    "user1": {
        "name": "Alice",
        "email": "alice@example.com"
    },
    "user2": {
        "name": "Bob",
        "email": "bob@example.com"
    }
}

# Access nested values
print(users["user1"]["email"])  # alice@example.com
```

### Default Values with setdefault

```python
person = {"name": "Alice"}

# Returns existing value
result = person.setdefault("name", "Unknown")  # Alice

# Adds and returns default if key missing
result = person.setdefault("age", 0)  # 0
print(person)  # {'name': 'Alice', 'age': 0}
```

## Summary

- Dictionaries store key-value pairs with fast lookup
- Keys must be unique and immutable
- Use `[]` for access (raises KeyError) or `.get()` for safe access
- Iterate with `.keys()`, `.values()`, or `.items()`
- Dictionary comprehensions provide concise creation syntax

## Additional Resources

- [Python Documentation: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Real Python: Dictionaries](https://realpython.com/python-dicts/)
- [W3Schools: Python Dictionaries](https://www.w3schools.com/python/python_dictionaries.asp)
