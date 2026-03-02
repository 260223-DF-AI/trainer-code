# Exception Handling

## Learning Objectives

- Understand exception handling concepts
- Know when and why to handle exceptions
- Explore the exception class hierarchy
- Create custom exception classes

## Why This Matters

Exception handling allows your program to respond gracefully to errors instead of crashing. It's essential for building robust applications that can handle unexpected situations - like network failures, missing files, or invalid user input - without losing data or frustrating users.

## Concept

### Why Handle Exceptions?

Without exception handling:

```python
def get_user_data():
    user_id = int(input("Enter user ID: "))  # Crashes if user types "abc"
    data = database.get(user_id)             # Crashes if database is down
    return data["name"]                       # Crashes if "name" not in data
```

With exception handling:

```python
def get_user_data():
    try:
        user_id = int(input("Enter user ID: "))
        data = database.get(user_id)
        return data["name"]
    except ValueError:
        print("Please enter a valid number")
    except ConnectionError:
        print("Database unavailable, please try later")
    except KeyError:
        print("User data incomplete")
    return None
```

### The Exception Hierarchy

Understanding the hierarchy helps you catch the right exceptions:

```
BaseException
 +-- SystemExit          # sys.exit()
 +-- KeyboardInterrupt   # Ctrl+C
 +-- Exception           # Base for most errors
      +-- ArithmeticError
      |    +-- ZeroDivisionError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- OSError
      |    +-- FileNotFoundError
      |    +-- PermissionError
      +-- TypeError
      +-- ValueError
```

**Key insight:** Catching a parent class catches all its children:

```python
try:
    # Some code
except LookupError:
    # Catches both IndexError and KeyError
    pass
```

### Exception Handling Philosophy

**EAFP vs LBYL:**

**LBYL** (Look Before You Leap):

```python
# Check first, then act
if key in dictionary:
    value = dictionary[key]
else:
    value = default
```

**EAFP** (Easier to Ask Forgiveness than Permission):

```python
# Try it, handle failure
try:
    value = dictionary[key]
except KeyError:
    value = default
```

Python favors EAFP - it's often cleaner and handles race conditions better.

### Creating Custom Exceptions

Define your own exceptions for domain-specific errors:

```python
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw ${amount}. Balance: ${balance}")

# Usage
def withdraw(account, amount):
    if amount > account.balance:
        raise InsufficientFundsError(account.balance, amount)
    account.balance -= amount

try:
    withdraw(my_account, 1000)
except InsufficientFundsError as e:
    print(f"Failed: {e}")
    print(f"You need ${e.amount - e.balance} more")
```

### Exception Attributes

Exception objects have useful attributes:

```python
try:
    open("missing.txt")
except FileNotFoundError as e:
    print(f"Error message: {e}")
    print(f"Error args: {e.args}")
    print(f"Filename: {e.filename}")
```

### Exception Chaining

When one exception causes another:

```python
try:
    config = load_config()
except FileNotFoundError as e:
    # Chain the original exception
    raise RuntimeError("Configuration failed") from e
```

Output shows both exceptions:

```
FileNotFoundError: config.json not found

The above exception was the direct cause of the following exception:

RuntimeError: Configuration failed
```

### Best Practices

1. **Catch specific exceptions** - Not bare `except:`
2. **Don't suppress exceptions silently** - At least log them
3. **Use custom exceptions** - For application-specific errors
4. **Keep try blocks small** - Only wrap the risky code
5. **Re-raise when appropriate** - Don't hide important errors

```python
# Bad - too broad
try:
    do_something()
except:
    pass

# Good - specific and informative
try:
    data = parse_json(input_text)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON: {e}")
    raise ValidationError("Input must be valid JSON") from e
```

## Summary

Exception handling lets programs respond to errors gracefully. Python's exception hierarchy means catching a parent catches all children. Custom exceptions make your code's error handling clearer and more specific. Follow EAFP style in Python - try the operation and handle exceptions rather than checking conditions first. The next lesson covers the try/except/else/finally syntax in detail.

## Resources

- [Python Docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python Docs: Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Real Python: Exception Handling](https://realpython.com/python-exceptions/)
