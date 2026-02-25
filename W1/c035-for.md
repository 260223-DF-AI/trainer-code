# For Loops

## Learning Objectives

- Iterate over sequences using for loops
- Use enumerate() and zip() for enhanced iteration
- Apply range() with for loops

## Why This Matters

For loops are the most common way to iterate over data in Python. Whether processing lists, reading files, or working with dictionaries, for loops provide clean, readable iteration. Mastering them is essential for effective Python programming.

## The Concept

### Basic For Loop

The `for` loop iterates over each item in a sequence:

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

### Iterating Over Different Types

```python
# Strings
for char in "Hello":
    print(char)  # H, e, l, l, o

# Lists
for num in [1, 2, 3]:
    print(num)

# Tuples
for item in (10, 20, 30):
    print(item)

# Dictionaries (keys by default)
person = {"name": "Alice", "age": 30}
for key in person:
    print(key)  # name, age

# Dictionary values
for value in person.values():
    print(value)  # Alice, 30

# Dictionary items
for key, value in person.items():
    print(f"{key}: {value}")

# Sets
for item in {1, 2, 3}:
    print(item)
```

### Using range()

```python
# Basic range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Start and stop
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# With step
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Countdown
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### enumerate() - Index and Value

```python
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Output:
# 0: apple
# 1: banana
# 2: cherry

# Start from different index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")
```

### zip() - Parallel Iteration

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Output:
# Alice is 25 years old
# Bob is 30 years old
# Charlie is 35 years old

# zip stops at shortest sequence
letters = ["a", "b"]
numbers = [1, 2, 3, 4]
for l, n in zip(letters, numbers):
    print(l, n)  # Only prints a,1 and b,2
```

### break and continue

```python
# break - exit loop early
for num in range(10):
    if num == 5:
        break
    print(num)  # 0, 1, 2, 3, 4

# continue - skip to next iteration
for num in range(5):
    if num == 2:
        continue
    print(num)  # 0, 1, 3, 4
```

### else Clause

The `else` block runs when the loop completes without break:

```python
for num in range(5):
    print(num)
else:
    print("Loop completed")  # Prints

# With break
for num in range(5):
    if num == 3:
        break
else:
    print("Won't print")  # Skipped due to break
```

### Nested For Loops

```python
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()

# Output:
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# (2,0) (2,1) (2,2)
```

### List Comprehensions (Preview)

A concise way to create lists from loops:

```python
# Traditional
squares = []
for x in range(5):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

### Common Patterns

```python
# Accumulator
total = 0
for num in [1, 2, 3, 4, 5]:
    total += num
print(total)  # 15

# Find maximum
nums = [3, 7, 2, 9, 1]
max_val = nums[0]
for num in nums:
    if num > max_val:
        max_val = num
print(max_val)  # 9

# Filter
words = ["apple", "an", "banana", "be"]
long_words = []
for word in words:
    if len(word) > 2:
        long_words.append(word)
print(long_words)  # ['apple', 'banana']
```

## Summary

- `for` loops iterate over sequences (lists, strings, ranges, etc.)
- Use `enumerate()` when you need both index and value
- Use `zip()` to iterate over multiple sequences in parallel
- `break` exits the loop; `continue` skips to the next iteration
- List comprehensions provide concise syntax for creating lists

## Additional Resources

- [Python Documentation: for Statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements)
- [Real Python: Python for Loops](https://realpython.com/python-for-loop/)
- [W3Schools: Python For Loops](https://www.w3schools.com/python/python_for_loops.asp)
