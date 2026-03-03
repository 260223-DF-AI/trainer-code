# Writing and Creating Files

## Learning Objectives

- Write text and data to files
- Create new files safely
- Append data to existing files
- Format output for files

## Why This Matters

Writing files is essential for saving program output, creating reports, logging events, and persisting data. Understanding the difference between write modes - especially write vs append - prevents accidental data loss and ensures your programs save data correctly.

## Concept

### Writing to Files

**write() - Write a string:**

```python
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is line 2.\n")
```

The `"w"` mode:

- Creates the file if it doesn't exist
- **Truncates (erases)** the file if it exists

### Write Mode Warning

**Careful!** Write mode destroys existing content:

```python
# This will ERASE everything in the file!
with open("important_data.txt", "w") as file:
    file.write("New content")
```

### Appending to Files

Use `"a"` mode to add to existing content:

```python
with open("log.txt", "a") as file:
    file.write("New log entry\n")
# Existing content is preserved, new content added at end
```

### Creating Files Safely

Use `"x"` mode to fail if file exists:

```python
try:
    with open("new_file.txt", "x") as file:
        file.write("This is a new file")
except FileExistsError:
    print("File already exists!")
```

### Writing Multiple Lines

**writelines() - Write a list of strings:**

```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

Note: `writelines()` doesn't add newlines - you must include them.

**Using join:**

```python
lines = ["Line 1", "Line 2", "Line 3"]
with open("output.txt", "w") as file:
    file.write("\n".join(lines))
```

### Writing with print()

Use `print()` with the `file` parameter:

```python
with open("output.txt", "w") as file:
    print("Hello, World!", file=file)
    print("This is line 2.", file=file)
    print("Values:", 1, 2, 3, file=file)
```

Advantage: Automatic newlines and easy formatting.

### Formatting Output

```python
name = "Alice"
score = 95.5

with open("report.txt", "w") as file:
    # f-strings
    file.write(f"Student: {name}\n")
    file.write(f"Score: {score:.1f}%\n")
    
    # Format method
    file.write("Results: {} - {:.2f}\n".format(name, score))
```

### Writing Binary Data

```python
# Write bytes
with open("binary.bin", "wb") as file:
    file.write(b"\x00\x01\x02\x03")

# Copy a binary file
with open("source.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

### Writing with pathlib

```python
from pathlib import Path

# Write text
Path("output.txt").write_text("Hello, World!\n")

# Write bytes
Path("data.bin").write_bytes(b"\x00\x01\x02")
```

### Practical Examples

**Writing a log file:**

```python
from datetime import datetime

def log_message(message, filename="app.log"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as file:
        file.write(f"[{timestamp}] {message}\n")

log_message("Application started")
log_message("Processing data...")
log_message("Application finished")
```

**Saving a list of data:**

```python
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

with open("users.txt", "w") as file:
    for user in data:
        file.write(f"{user['name']},{user['age']}\n")
```

**Creating a report:**

```python
def generate_report(title, items, filename):
    with open(filename, "w") as file:
        file.write(f"{'=' * 40}\n")
        file.write(f"{title:^40}\n")
        file.write(f"{'=' * 40}\n\n")
        
        for item in items:
            file.write(f"  - {item}\n")
        
        file.write(f"\nTotal items: {len(items)}\n")

generate_report(
    "Shopping List",
    ["Apples", "Bread", "Milk", "Eggs"],
    "shopping.txt"
)
```

### Buffering and Flushing

Python buffers writes for efficiency. Force immediate writing:

```python
with open("output.txt", "w") as file:
    file.write("Important data")
    file.flush()  # Force write to disk
```

Or use unbuffered mode:

```python
with open("output.txt", "w", buffering=1) as file:  # Line buffered
    file.write("Line 1\n")  # Written immediately
```

### Atomic Writes

For safety, write to a temporary file then rename:

```python
import os

def safe_write(filename, content):
    temp_file = filename + ".tmp"
    with open(temp_file, "w") as file:
        file.write(content)
    os.replace(temp_file, filename)  # Atomic operation
```

## Summary

Use `"w"` mode to write (creates or truncates), `"a"` to append (preserves existing), and `"x"` to create (fails if exists). Remember that write mode erases existing content. Use `write()` for strings, `writelines()` for lists, or `print(file=f)` for easy formatting. Always include newline characters when needed. Use `flush()` to ensure data is written to disk immediately.

## Resources

- [Python Docs: Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Real Python: Reading and Writing Files](https://realpython.com/read-write-files-python/)
- [Python Docs: open()](https://docs.python.org/3/library/functions.html#open)
