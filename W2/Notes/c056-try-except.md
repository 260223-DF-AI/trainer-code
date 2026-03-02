# try-except

## Learning Objectives

- Write try/except blocks to handle exceptions
- Use else and finally clauses appropriately
- Handle multiple exception types
- Apply best practices for exception handling

## Why This Matters

The try/except statement is Python's mechanism for catching and handling exceptions. Mastering its syntax - including else and finally clauses - allows you to write robust code that handles errors without crashing and properly cleans up resources.

## Concept

### Basic try/except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### The Complete Syntax

```python
try:
    # Code that might raise an exception
    risky_operation()
except ExceptionType:
    # Handle the exception
    handle_error()
else:
    # Run if NO exception occurred
    success_action()
finally:
    # ALWAYS runs, exception or not
    cleanup()
```

### Handling Multiple Exceptions

**Separate handlers:**

```python
try:
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print("That's not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

**Same handler for multiple exceptions:**

```python
try:
    data = process_input(user_input)
except (ValueError, TypeError, KeyError):
    print("Invalid input data")
```

**Catching all exceptions (use sparingly):**

```python
try:
    risky_operation()
except Exception as e:
    print(f"An error occurred: {e}")
```

### Accessing the Exception Object

```python
try:
    open("missing.txt")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print(f"Filename: {e.filename}")
```

### The else Clause

Runs only if **no exception** occurred:

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division failed")
else:
    print(f"Result: {result}")  # Only runs if no error
```

**Why use else?**

- Keeps the try block minimal
- Clearly separates error-prone code from success logic
- Exceptions in else block won't be caught by the except

```python
try:
    data = load_data()  # Might fail
except IOError:
    print("Could not load data")
else:
    process(data)  # Only if load succeeded
    save_results()  # Errors here aren't caught above
```

### The finally Clause

**Always runs**, regardless of exceptions:

```python
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("This always runs")
```

**Primary use - cleanup:**

```python
file = None
try:
    file = open("data.txt")
    process(file.read())
except IOError as e:
    print(f"Error: {e}")
finally:
    if file:
        file.close()  # Always close the file
```

### Complete Example

```python
def read_config(filename):
    config = None
    try:
        file = open(filename)
        data = file.read()
        config = parse_config(data)
    except FileNotFoundError:
        print(f"Config file '{filename}' not found")
        config = get_default_config()
    except json.JSONDecodeError as e:
        print(f"Invalid config format: {e}")
        config = get_default_config()
    else:
        print(f"Config loaded successfully from {filename}")
    finally:
        if 'file' in dir() and file:
            file.close()
    
    return config
```

### Raising Exceptions

Use `raise` to throw exceptions:

```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation failed: {e}")
```

### Re-raising Exceptions

Handle an exception, then let it propagate:

```python
try:
    process_data()
except ValueError as e:
    print(f"Logging error: {e}")
    raise  # Re-raise the same exception
```

### Nested try/except

```python
try:
    try:
        result = risky_operation()
    except ValueError:
        result = fallback_operation()
except Exception:
    result = default_value
```

### Best Practices

**1. Be specific:**

```python
# Bad
except:
    pass

# Good
except ValueError as e:
    logger.error(f"Value error: {e}")
```

**2. Don't hide errors:**

```python
# Bad - silently ignores errors
try:
    save_data()
except:
    pass

# Good - at least log it
try:
    save_data()
except IOError as e:
    logger.error(f"Failed to save: {e}")
    show_error_message()
```

**3. Keep try blocks focused:**

```python
# Bad - too much in try block
try:
    data = load_data()
    processed = process(data)
    results = analyze(processed)
    save(results)
except Exception:
    print("Something went wrong")

# Good - focused try blocks
try:
    data = load_data()
except IOError:
    data = default_data

processed = process(data)
results = analyze(processed)

try:
    save(results)
except IOError:
    print("Could not save results")
```

**4. Use context managers when possible:**

```python
# Better than try/finally for file handling
with open("data.txt") as file:
    data = file.read()
# File automatically closed
```

## Summary

Use `try/except` to catch and handle exceptions. The `else` clause runs only when no exception occurs, keeping success logic separate. The `finally` clause always runs, making it ideal for cleanup. Be specific with exception types, don't silently ignore errors, and keep try blocks focused. For resource management, context managers (covered next) are often cleaner than try/finally.

## Resources

- [Python Docs: Handling Exceptions](https://docs.python.org/3/tutorial/errors.html#handling-exceptions)
- [Real Python: try-except](https://realpython.com/python-exceptions/)
- [PEP 3110: Catching Exceptions](https://peps.python.org/pep-3110/)
