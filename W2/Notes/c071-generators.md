# Generators

## Learning Objectives

- Understand what generators are and how they work
- Create generators using the yield keyword
- Apply generators for memory-efficient iteration
- Recognize when to use generators vs lists

## Why This Matters

Generators let you work with large datasets without loading everything into memory. They're essential for processing big files, streaming data, and building efficient pipelines. Understanding generators transforms how you think about iteration and data processing.

## Concept

### What Is a Generator?

A generator is a function that yields values one at a time instead of returning them all at once. Each time you request the next value, the function resumes where it left off.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

# Usage
for num in count_up_to(5):
    print(num)
# 1
# 2
# 3
# 4
# 5
```

### yield vs return

**return** - Ends the function, returns value:

```python
def get_numbers():
    return [1, 2, 3, 4, 5]  # Returns entire list at once
```

**yield** - Pauses the function, yields value, can resume:

```python
def generate_numbers():
    yield 1  # Pause, yield 1
    yield 2  # Resume, yield 2
    yield 3  # Resume, yield 3
```

### How Generators Work

```python
def simple_generator():
    print("First")
    yield 1
    print("Second")
    yield 2
    print("Third")
    yield 3

gen = simple_generator()      # Creates generator object (nothing runs yet)
print(next(gen))              # First, then 1
print(next(gen))              # Second, then 2
print(next(gen))              # Third, then 3
# print(next(gen))            # Raises StopIteration
```

### Memory Efficiency

**List - All in memory:**

```python
# Creates list of 1 million squares in memory
squares = [x**2 for x in range(1000000)]
```

**Generator - One at a time:**

```python
# Generates squares on demand, minimal memory
squares = (x**2 for x in range(1000000))
```

**Memory comparison:**

```python
import sys

list_comp = [x**2 for x in range(1000)]
gen_exp = (x**2 for x in range(1000))

print(sys.getsizeof(list_comp))  # ~8856 bytes
print(sys.getsizeof(gen_exp))    # ~112 bytes (just the generator object)
```

### Generator Functions

```python
def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

for num in fibonacci(10):
    print(num, end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

### Generator Expressions

Shorthand syntax (like list comprehensions but with parentheses):

```python
# List comprehension - creates list
squares_list = [x**2 for x in range(10)]

# Generator expression - creates generator
squares_gen = (x**2 for x in range(10))

# Use in functions directly (no extra parentheses needed)
total = sum(x**2 for x in range(10))
```

### Practical Examples

**Reading large files:**

```python
def read_large_file(file_path):
    """Read file line by line without loading all into memory."""
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()

# Process without loading entire file
for line in read_large_file("huge_log.txt"):
    if "ERROR" in line:
        print(line)
```

**Infinite sequences:**

```python
def infinite_counter(start=0):
    """Generate numbers forever."""
    n = start
    while True:
        yield n
        n += 1

# Take only what you need
counter = infinite_counter()
for _ in range(5):
    print(next(counter))  # 0, 1, 2, 3, 4
```

**Data pipeline:**

```python
def parse_lines(lines):
    for line in lines:
        yield line.strip().split(",")

def filter_complete(records):
    for record in records:
        if len(record) == 3:
            yield record

def transform(records):
    for name, age, city in records:
        yield {"name": name, "age": int(age), "city": city}

# Chain generators - lazy evaluation
lines = read_large_file("data.csv")
parsed = parse_lines(lines)
complete = filter_complete(parsed)
records = transform(complete)

for record in records:
    print(record)
```

### Generator Methods

```python
def accumulator():
    total = 0
    while True:
        x = yield total
        if x is not None:
            total += x

gen = accumulator()
next(gen)           # Start generator
gen.send(10)        # Send value: 10
gen.send(20)        # Send value: 30
gen.send(5)         # Send value: 35
```

### When to Use Generators

**Use generators when:**

- Working with large datasets
- Reading large files
- Creating infinite sequences
- Building data pipelines
- Memory is a concern

**Use lists when:**

- You need random access (list[5])
- You need to iterate multiple times
- The data is small
- You need list methods (sort, reverse)

## Summary

Generators are functions that yield values one at a time using the `yield` keyword. They're memory-efficient because they generate values on demand instead of storing everything in memory. Create generators with functions that yield or with generator expressions using parentheses. Generators are perfect for large files, data pipelines, and infinite sequences.

## Resources

- [Python Docs: Generators](https://docs.python.org/3/tutorial/classes.html#generators)
- [Real Python: Python Generators](https://realpython.com/introduction-to-python-generators/)
- [PEP 255: Simple Generators](https://peps.python.org/pep-0255/)
