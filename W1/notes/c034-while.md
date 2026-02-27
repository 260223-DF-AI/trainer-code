# While Loops

## Learning Objectives

- Understand the syntax and behavior of while loops
- Use break and continue to control loop execution
- Avoid infinite loops

## Why This Matters

While loops execute code repeatedly as long as a condition is True. They are essential when you do not know in advance how many iterations you need, such as waiting for user input or processing data until a condition is met.

## The Concept

### Basic While Loop

The `while` loop repeats as long as its condition is True:

```python
count = 0

while count < 5:
    print(count)
    count += 1

# Output: 0, 1, 2, 3, 4
```

### How While Works

1. Check the condition
2. If True, execute the body
3. Return to step 1
4. If False, exit the loop

```python
# Countdown example
n = 5

while n > 0:
    print(n)
    n -= 1

print("Blast off!")
```

### The break Statement

Exit the loop immediately:

```python
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
    print(f"You entered: {user_input}")

print("Loop ended")
```

### The continue Statement

Skip to the next iteration:

```python
n = 0

while n < 10:
    n += 1
    if n % 2 == 0:
        continue  # Skip even numbers
    print(n)

# Output: 1, 3, 5, 7, 9
```

### The else Clause

The `else` block runs when the loop completes normally (not via break):

```python
n = 0

while n < 5:
    print(n)
    n += 1
else:
    print("Loop completed normally")

# With break
while n < 10:
    if n == 7:
        break
    n += 1
else:
    print("This won't print")  # Skipped due to break
```

### Avoiding Infinite Loops

An infinite loop occurs when the condition never becomes False:

```python
# DANGER: Infinite loop (don't run this)
# while True:
#     print("Forever...")

# Common mistakes:
# 1. Forgetting to update the loop variable
# 2. Condition that can never be False
# 3. Logic errors in the condition

# Safe pattern with break
while True:
    data = get_next_item()
    if data is None:
        break  # Exit when no more data
    process(data)
```

### Common Patterns

```python
# User input validation
while True:
    try:
        age = int(input("Enter your age: "))
        if age > 0:
            break
        print("Age must be positive")
    except ValueError:
        print("Please enter a number")

# Processing until condition
items = [1, 2, 3, 4, 5]
while items:
    item = items.pop()
    print(f"Processing: {item}")

# Sentinel value
total = 0
while True:
    value = int(input("Enter number (0 to stop): "))
    if value == 0:
        break
    total += value
print(f"Total: {total}")
```

### While vs For

- Use `while` when you do not know how many iterations you need
- Use `for` when iterating over a known sequence
- `while True` with `break` is common for input validation

```python
# When to use while
attempts = 0
password = ""
while password != "secret" and attempts < 3:
    password = input("Password: ")
    attempts += 1

# When to use for
for item in items:
    process(item)
```

### Nested While Loops

```python
row = 0
while row < 3:
    col = 0
    while col < 3:
        print(f"({row},{col})", end=" ")
        col += 1
    print()  # New line
    row += 1

# Output:
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# (2,0) (2,1) (2,2)
```

## Summary

- `while` loops repeat while a condition is True
- Use `break` to exit the loop immediately
- Use `continue` to skip to the next iteration
- Always ensure the loop can terminate (avoid infinite loops)
- Use `while True` with `break` for input validation patterns

## Additional Resources

- [Python Documentation: while Statements](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)
- [Real Python: Python while Loops](https://realpython.com/python-while-loop/)
- [W3Schools: Python While Loops](https://www.w3schools.com/python/python_while_loops.asp)
