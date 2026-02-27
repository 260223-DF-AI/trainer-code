# Functions

## Learning Objectives

- Define and call functions in Python
- Use parameters and return values
- Understand default arguments and keyword arguments

## Why This Matters

Functions are the building blocks of organized, reusable code. They allow you to encapsulate logic, reduce repetition, and make your programs more readable and maintainable. Understanding functions is essential for any programming task.

## The Concept

### Defining a Function

Use the `def` keyword to define a function:

```python
def greet():
    print("Hello, World!")

# Call the function
greet()  # Output: Hello, World!
```

### Parameters and Arguments

Functions can accept input values:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Hello, Alice!
greet("Bob")    # Hello, Bob!
```

### Multiple Parameters

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

### Return Values

Functions can return values using `return`:

```python
def square(x):
    return x ** 2

result = square(4)
print(result)  # 16

# Multiple return values (as tuple)
def get_dimensions():
    return 1920, 1080

width, height = get_dimensions()
```

### Default Arguments

Provide default values for optional parameters:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Welcome")     # Welcome, Bob!
```

### Keyword Arguments

Call functions using parameter names:

```python
def describe_person(name, age, city):
    print(f"{name} is {age} years old from {city}")

# Positional arguments
describe_person("Alice", 30, "NYC")

# Keyword arguments (order does not matter)
describe_person(city="Boston", name="Bob", age=25)

# Mixed (positional must come first)
describe_person("Charlie", city="LA", age=35)
```

### *args - Variable Positional Arguments

Accept any number of positional arguments:

```python
def add_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add_all(1, 2, 3))        # 6
print(add_all(1, 2, 3, 4, 5))  # 15
```

### **kwargs - Variable Keyword Arguments

Accept any number of keyword arguments:

```python
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
# name: Alice
# age: 30
# city: NYC
```

### Combining Parameters

```python
def example(required, *args, default="value", **kwargs):
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Default: {default}")
    print(f"Kwargs: {kwargs}")

example("hello", 1, 2, 3, default="custom", x=10, y=20)
```

### Docstrings

Document your functions with docstrings:

```python
def calculate_area(radius):
    """
    Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle.
    
    Returns:
        The area of the circle.
    """
    return 3.14159 * radius ** 2

# Access docstring
print(calculate_area.__doc__)
```

### Return vs Print

- `return` sends a value back to the caller
- `print` displays output but returns `None`

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)   # Prints 5
print(x)              # None

y = add_return(2, 3)  # Returns 5
print(y)              # 5
```

### Early Return

```python
def check_age(age):
    if age < 0:
        return "Invalid age"
    if age < 18:
        return "Minor"
    return "Adult"

print(check_age(25))  # Adult
print(check_age(-5))  # Invalid age
```

### Functions as Objects

Functions are first-class objects:

```python
def greet(name):
    return f"Hello, {name}"

# Assign to variable
say_hello = greet
print(say_hello("Alice"))  # Hello, Alice

# Pass as argument
def apply(func, value):
    return func(value)

print(apply(greet, "Bob"))  # Hello, Bob
```

## Summary

- Define functions with `def`, parameters, and optionally `return`
- Use default values for optional parameters
- Keyword arguments allow flexible calling order
- `*args` accepts variable positional arguments
- `**kwargs` accepts variable keyword arguments
- Document functions with docstrings

## Additional Resources

- [Python Documentation: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Real Python: Defining Functions](https://realpython.com/defining-your-own-python-function/)
- [W3Schools: Python Functions](https://www.w3schools.com/python/python_functions.asp)
