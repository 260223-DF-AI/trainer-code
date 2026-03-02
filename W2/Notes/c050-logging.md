# Logging

## Learning Objectives

- Understand why logging is preferred over print statements
- Configure Python's logging module
- Use different logging levels appropriately
- Format and direct log output

## Why This Matters

In production applications, print statements aren't enough. Logging provides a flexible way to record what your application is doing, when problems occur, and how to debug issues. Proper logging is essential for monitoring applications, debugging in production, and maintaining audit trails.

## Concept

### Why Not Just Use Print?

**print() limitations:**

- No severity levels
- No timestamps
- Hard to turn off
- Difficult to redirect to files
- No context information

**Logging advantages:**

- Severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Timestamps and formatting
- Easy to enable/disable
- Can output to files, network, etc.
- Includes context (module, line number, etc.)

### Basic Logging

```python
import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)

# Log messages at different levels
logging.debug("Detailed information for debugging")
logging.info("General information about program execution")
logging.warning("Something unexpected happened")
logging.error("A more serious problem occurred")
logging.critical("A critical error - program may crash")
```

### Logging Levels

| Level | Value | Description |
|-------|-------|-------------|
| DEBUG | 10 | Detailed diagnostic information |
| INFO | 20 | Confirmation that things work as expected |
| WARNING | 30 | Something unexpected, but not an error |
| ERROR | 40 | A problem that prevented a function from working |
| CRITICAL | 50 | A serious error; program may not continue |

Setting a level means that level and above are logged:

```python
# Only WARNING and above will be logged
logging.basicConfig(level=logging.WARNING)

logging.debug("Won't appear")    # Below threshold
logging.info("Won't appear")     # Below threshold
logging.warning("Will appear")   # Meets threshold
logging.error("Will appear")     # Above threshold
```

### Formatting Log Messages

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Application started")
# Output: 2024-01-15 10:30:45,123 - INFO - Application started
```

**Common format placeholders:**

| Placeholder | Description |
|-------------|-------------|
| `%(asctime)s` | Timestamp |
| `%(levelname)s` | Level name (INFO, ERROR, etc.) |
| `%(message)s` | The log message |
| `%(name)s` | Logger name |
| `%(filename)s` | Source file name |
| `%(lineno)d` | Line number |
| `%(funcName)s` | Function name |

### Logging to a File

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='w'  # 'w' = overwrite, 'a' = append
)

logging.info("This goes to the file")
```

### Logging to Both Console and File

```python
import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

# Set levels for handlers
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Use the logger
logger.debug("Debug message - file only")
logger.info("Info message - console and file")
logger.error("Error message - console and file")
```

### Creating Named Loggers

Best practice is to create a logger for each module:

```python
import logging

# Create a logger with the module's name
logger = logging.getLogger(__name__)

def my_function():
    logger.info("Function called")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.error("Division by zero!", exc_info=True)
```

### Logging Exceptions

```python
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    result = 10 / 0
except ZeroDivisionError:
    # Log with stack trace
    logging.exception("An error occurred")
    
    # Or use exc_info=True
    logging.error("An error occurred", exc_info=True)
```

### Practical Example

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_order(order_id, amount):
    logger.info(f"Processing order {order_id}")
    
    if amount <= 0:
        logger.warning(f"Invalid amount for order {order_id}: {amount}")
        return False
    
    if amount > 10000:
        logger.warning(f"Large order detected: {order_id}, amount: {amount}")
    
    try:
        # Simulate processing
        logger.debug(f"Validating order {order_id}")
        logger.debug(f"Charging amount: {amount}")
        logger.info(f"Order {order_id} completed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to process order {order_id}", exc_info=True)
        return False

# Test
process_order("ORD-001", 150)
process_order("ORD-002", -50)
process_order("ORD-003", 15000)
```

### Logging Best Practices

1. **Use appropriate levels** - Don't log everything as INFO
2. **Include context** - Log relevant data with messages
3. **Don't log sensitive data** - Never log passwords, tokens, PII
4. **Use structured logging** - Consider JSON format for parsing
5. **Configure at startup** - Set up logging early in your application

## Summary

Logging is superior to print statements for production code. Use `logging.basicConfig()` for simple configuration or create handlers for complex setups. Choose appropriate levels: DEBUG for diagnostics, INFO for normal operation, WARNING for unexpected events, ERROR for problems, and CRITICAL for severe issues. Format logs with timestamps and context, and output to both console and files as needed.

## Resources

- [Python Docs: logging](https://docs.python.org/3/library/logging.html)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Real Python: Logging in Python](https://realpython.com/python-logging/)
