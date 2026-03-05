# Named Tuples

## Learning Objectives

- Create namedtuple classes for structured data
- Access data by name instead of index
- Convert between namedtuples and other formats
- Understand when to use namedtuple vs other options

## Why This Matters

Regular tuples access elements by index, which makes code hard to read: `person[0]`, `person[1]`. Named tuples let you use meaningful names: `person.name`, `person.age`. They're lightweight, immutable, and perfect for representing simple data records.

## Concept

### What Is namedtuple?

namedtuple creates tuple subclasses with named fields:

```python
from collections import namedtuple

# Create a Point type
Point = namedtuple("Point", ["x", "y"])

# Create instances
p = Point(3, 4)
print(p.x)       # 3
print(p.y)       # 4
print(p)         # Point(x=3, y=4)
```

### Creating Named Tuples

```python
from collections import namedtuple

# Different ways to define fields
Point = namedtuple("Point", ["x", "y"])
Point = namedtuple("Point", "x y")
Point = namedtuple("Point", "x, y")

# With defaults (Python 3.7+)
Point = namedtuple("Point", ["x", "y"], defaults=[0, 0])
p = Point()      # Point(x=0, y=0)
p = Point(5)     # Point(x=5, y=0)
```

### Accessing Values

```python
from collections import namedtuple

Person = namedtuple("Person", ["name", "age", "city"])
person = Person("Alice", 30, "NYC")

# By name (readable)
print(person.name)    # Alice
print(person.age)     # 30

# By index (still works)
print(person[0])      # Alice
print(person[1])      # 30

# Unpack like regular tuple
name, age, city = person
```

### Named Tuple Features

**Immutable (like regular tuples):**

```python
person = Person("Alice", 30, "NYC")
# person.age = 31  # Error! Can't modify
```

**Create modified copy with _replace():**

```python
person = Person("Alice", 30, "NYC")
older = person._replace(age=31)
print(older)  # Person(name='Alice', age=31, city='NYC')
```

**Convert to dictionary:**

```python
person = Person("Alice", 30, "NYC")
print(person._asdict())
# {'name': 'Alice', 'age': 30, 'city': 'NYC'}
```

**Get field names:**

```python
print(Person._fields)  # ('name', 'age', 'city')
```

### Practical Examples

**Representing coordinates:**

```python
from collections import namedtuple
import math

Point = namedtuple("Point", ["x", "y"])

def distance(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

origin = Point(0, 0)
target = Point(3, 4)
print(distance(origin, target))  # 5.0
```

**Database records:**

```python
from collections import namedtuple

User = namedtuple("User", ["id", "username", "email", "created_at"])

# Simulate fetching from database
users = [
    User(1, "alice", "alice@example.com", "2024-01-01"),
    User(2, "bob", "bob@example.com", "2024-01-02"),
]

for user in users:
    print(f"{user.username}: {user.email}")
```

**API responses:**

```python
from collections import namedtuple

Response = namedtuple("Response", ["status", "data", "error"])

def api_call():
    # Simulated API response
    return Response(status=200, data={"result": "success"}, error=None)

response = api_call()
if response.status == 200:
    print(response.data)
```

**CSV data:**

```python
from collections import namedtuple
import csv

# Create namedtuple from CSV header
with open("data.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    Row = namedtuple("Row", header)
    
    for row in reader:
        record = Row(*row)
        print(record.name, record.age)
```

### namedtuple vs Alternatives

| Feature | namedtuple | dict | class | dataclass |
|---------|------------|------|-------|-----------|
| Named access | Yes | Yes | Yes | Yes |
| Immutable | Yes | No | Optional | Optional |
| Memory efficient | Yes | No | No | No |
| Type-safe | No | No | Yes | Yes |
| Methods | Limited | N/A | Yes | Yes |

**When to use namedtuple:**

- Simple, immutable data structures
- When you need tuple behavior (hashable, unpacking)
- Memory-efficient records

**Consider dataclasses instead when:**

- You need methods
- You need mutability
- You need type hints

## Summary

namedtuple creates tuple subclasses with named fields, improving code readability over index-based access. Create types with `namedtuple("Name", ["field1", "field2"])`. Access fields by name (`point.x`) or index (`point[0]`). Named tuples are immutable - use `_replace()` to create modified copies. Convert to dict with `_asdict()`. They're ideal for simple, immutable data records.

## Resources

- [Python Docs: namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)
- [Real Python: namedtuple](https://realpython.com/python-namedtuple/)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) (alternative)
