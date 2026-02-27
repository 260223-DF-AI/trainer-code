# Iterators

## Learning Objectives

- Understand what iterators are in Python
- Distinguish between iterables and iterators
- Create custom iterators using __iter__ and __next__

## Why This Matters

Iterators are the mechanism behind Python's `for` loops and comprehensions. Understanding how they work enables you to create memory-efficient data processing pipelines and build custom iterable objects.

## The Concept

### Iterables vs Iterators

- __Iterable:__ An object that can be iterated over (e.g., list, string, dict)
- __Iterator:__ An object that produces values one at a time

```python
# List is an iterable
my_list = [1, 2, 3]

# Get an iterator from the iterable
my_iterator = iter(my_list)

# Get values one at a time
print(next(my_iterator))  # 1
print(next(my_iterator))  # 2
print(next(my_iterator))  # 3
# print(next(my_iterator))  # StopIteration error
```

### How for Loops Work

Under the hood, `for` loops use iterators:

```python
# This for loop...
for item in [1, 2, 3]:
    print(item)

# ...is equivalent to:
iterator = iter([1, 2, 3])
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

### The iter() and next() Functions

```python
# iter() creates an iterator
text = "Hello"
iterator = iter(text)

# next() gets the next value
print(next(iterator))  # H
print(next(iterator))  # e
print(next(iterator))  # l
print(next(iterator))  # l
print(next(iterator))  # o

# Provide default to avoid StopIteration
print(next(iterator, "END"))  # END
```

### Creating a Custom Iterator

Implement `__iter__` and `__next__` methods:

```python
class Counter:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

# Use the custom iterator
for num in Counter(1, 5):
    print(num)  # 1, 2, 3, 4
```

### Iterator Protocol

Any object that implements these methods is an iterator:

- `__iter__()`: Returns the iterator object (usually `self`)
- `__next__()`: Returns the next value or raises `StopIteration`

### Iterable vs Iterator Behavior

```python
my_list = [1, 2, 3]

# Iterable can be iterated multiple times
for x in my_list:
    print(x)
for x in my_list:
    print(x)

# Iterator is exhausted after one pass
my_iter = iter(my_list)
print(list(my_iter))  # [1, 2, 3]
print(list(my_iter))  # [] (exhausted)
```

### Practical Example: Fibonacci Iterator

```python
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.a >= self.limit:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value

# Generate Fibonacci numbers up to 100
for fib in Fibonacci(100):
    print(fib, end=" ")
# Output: 0 1 1 2 3 5 8 13 21 34 55 89
```

### Built-in Iterators

Many Python objects return iterators:

```python
# File objects are iterators
with open("file.txt") as f:
    for line in f:
        print(line)

# map() returns an iterator
squares = map(lambda x: x**2, [1, 2, 3])
print(next(squares))  # 1
print(next(squares))  # 4

# filter() returns an iterator
evens = filter(lambda x: x % 2 == 0, range(10))
print(list(evens))  # [0, 2, 4, 6, 8]

# zip() returns an iterator
pairs = zip([1, 2], ['a', 'b'])
print(next(pairs))  # (1, 'a')
```

### Memory Efficiency

Iterators process one item at a time, making them memory-efficient:

```python
# Creates list in memory (may use GB for large range)
# big_list = list(range(1000000000))

# Iterator uses minimal memory
big_range = range(1000000000)  # Just an iterator
for i in big_range:
    if i > 5:
        break
    print(i)
```

### Generators (Preview)

Generators are a simpler way to create iterators. We will explore them in more depth in future topics:

```python
def count_up_to(max):
    current = 1
    while current <= max:
        yield current
        current += 1

for num in count_up_to(5):
    print(num)  # 1, 2, 3, 4, 5
```

## Summary

- Iterables can be looped over; iterators produce values one at a time
- Use `iter()` to get an iterator, `next()` to get values
- Custom iterators implement `__iter__` and `__next__`
- `StopIteration` signals the end of iteration
- Iterators are memory-efficient for large data

## Additional Resources

- [Python Documentation: Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Real Python: Iterators and Generators](https://realpython.com/introduction-to-python-generators/)
- [W3Schools: Python Iterators](https://www.w3schools.com/python/python_iterators.asp)
