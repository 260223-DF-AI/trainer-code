# File Handling

## Learning Objectives

- Understand file handling concepts in Python
- Know the difference between text and binary modes
- Use the open() function with different modes
- Apply context managers for safe file handling

## Why This Matters

File operations are fundamental to programming. Applications read configuration files, log events, process data files, and save state. Understanding Python's file handling - especially the `with` statement pattern - ensures your programs handle files safely and efficiently.

## Concept

### Opening Files

Use the `open()` function to create a file object:

```python
# Basic syntax
file = open("filename.txt", "mode")

# Always close when done
file.close()
```

### File Modes

| Mode | Description |
|------|-------------|
| `"r"` | Read (default). File must exist. |
| `"w"` | Write. Creates new or **truncates** existing. |
| `"a"` | Append. Creates new or adds to end. |
| `"x"` | Exclusive create. Fails if file exists. |
| `"r+"` | Read and write. File must exist. |
| `"w+"` | Write and read. Truncates existing. |
| `"a+"` | Append and read. |

Add `"b"` for binary mode:

- `"rb"` - Read binary
- `"wb"` - Write binary

### The Context Manager Pattern

**Always use `with`** for file handling:

```python
# Correct way
with open("data.txt", "r") as file:
    content = file.read()
# File is automatically closed here

# Avoid this pattern
file = open("data.txt", "r")
content = file.read()
file.close()  # Easy to forget, doesn't run if exception occurs
```

### File Object Properties

```python
with open("data.txt", "r") as file:
    print(file.name)       # 'data.txt'
    print(file.mode)       # 'r'
    print(file.closed)     # False
    
print(file.closed)         # True (after exiting with block)
```

### Text vs Binary Mode

**Text mode (default):**

- Reads/writes strings
- Handles encoding (default: UTF-8)
- Converts line endings

```python
with open("text.txt", "r") as file:
    text = file.read()  # Returns str
```

**Binary mode:**

- Reads/writes bytes
- No encoding conversion
- For images, audio, executables, etc.

```python
with open("image.jpg", "rb") as file:
    data = file.read()  # Returns bytes
```

### Encoding

Specify encoding explicitly for text files:

```python
# Read UTF-8 encoded file
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Write with encoding
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Hello, World!")
```

Common encodings:

- `"utf-8"` - Universal, recommended
- `"ascii"` - Basic English characters only
- `"latin-1"` - Western European
- `"cp1252"` - Windows Western European

### File Paths

**Relative paths** - relative to current working directory:

```python
open("data.txt")           # Same directory
open("data/file.txt")      # Subdirectory
open("../file.txt")        # Parent directory
```

**Absolute paths** - full path from root:

```python
open("/home/user/data.txt")          # Linux/Mac
open("C:\\Users\\user\\data.txt")    # Windows
open(r"C:\Users\user\data.txt")      # Raw string (easier on Windows)
```

### Using pathlib (Recommended)

The pathlib module provides an object-oriented approach:

```python
from pathlib import Path

# Create path object
data_file = Path("data") / "file.txt"

# Check if exists
if data_file.exists():
    # Open the file
    with open(data_file, "r") as file:
        content = file.read()
    
# Or use pathlib's read method
content = data_file.read_text()
```

### Error Handling

Handle common file errors:

```python
try:
    with open("data.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File does not exist")
except PermissionError:
    print("No permission to read file")
except IOError as e:
    print(f"I/O error: {e}")
```

### Working with Multiple Files

```python
# Copy file contents
with open("source.txt", "r") as source:
    with open("destination.txt", "w") as dest:
        dest.write(source.read())

# Or on one line
with open("source.txt") as src, open("dest.txt", "w") as dst:
    dst.write(src.read())
```

## Summary

Use `open(filename, mode)` to work with files. Always use the `with` statement (context manager) to ensure files are properly closed. Choose the right mode: `"r"` for reading, `"w"` for writing (overwrites), `"a"` for appending. Add `"b"` for binary files. Specify encoding explicitly for text files. Handle errors with try/except for FileNotFoundError and PermissionError. The following lessons cover specific read and write operations.

## Resources

- [Python Docs: Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python Docs: open()](https://docs.python.org/3/library/functions.html#open)
- [Real Python: Reading and Writing Files](https://realpython.com/read-write-files-python/)
