# Reading Files

## Learning Objectives

- Read entire files into memory
- Read files line by line
- Use different read methods appropriately
- Process large files efficiently

## Why This Matters

Reading data from files is one of the most common programming tasks. Whether loading configuration, processing logs, or analyzing data, you need to know the right method to read files efficiently. Understanding when to read all at once versus line by line can make the difference between a fast program and one that crashes from memory exhaustion.

## Concept

### Reading Entire File

**read() - Get all content as one string:**

```python
with open("data.txt", "r") as file:
    content = file.read()
    print(content)
```

**read(size) - Read specific number of characters:**

```python
with open("data.txt", "r") as file:
    chunk = file.read(100)  # First 100 characters
    print(chunk)
```

### Reading Lines

**readline() - Read one line:**

```python
with open("data.txt", "r") as file:
    first_line = file.readline()
    second_line = file.readline()
    print(first_line)
```

**readlines() - Get all lines as a list:**

```python
with open("data.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line, end="")  # Lines include '\n'
```

### Iterating Over Lines (Recommended)

The most memory-efficient way to read a file:

```python
with open("data.txt", "r") as file:
    for line in file:
        print(line, end="")
```

This reads one line at a time - perfect for large files.

### Stripping Newlines

Lines include the newline character:

```python
with open("data.txt", "r") as file:
    for line in file:
        clean_line = line.strip()  # Remove whitespace and newline
        print(clean_line)

# Or while reading
with open("data.txt", "r") as file:
    lines = [line.strip() for line in file]
```

### Practical Examples

**Count lines in a file:**

```python
with open("data.txt", "r") as file:
    line_count = sum(1 for line in file)
    print(f"Total lines: {line_count}")
```

**Search for a pattern:**

```python
with open("log.txt", "r") as file:
    for line_number, line in enumerate(file, 1):
        if "ERROR" in line:
            print(f"Line {line_number}: {line.strip()}")
```

**Read into a list of records:**

```python
# CSV-like file: name,age,city
users = []
with open("users.txt", "r") as file:
    for line in file:
        name, age, city = line.strip().split(",")
        users.append({
            "name": name,
            "age": int(age),
            "city": city
        })
```

### File Position

The file object tracks its current position:

```python
with open("data.txt", "r") as file:
    print(file.tell())        # Current position: 0
    
    file.read(10)
    print(file.tell())        # Position: 10
    
    file.seek(0)              # Go back to beginning
    print(file.tell())        # Position: 0
```

### Reading Binary Files

```python
# Read an image file
with open("image.jpg", "rb") as file:
    data = file.read()
    print(f"File size: {len(data)} bytes")

# Read in chunks
with open("large_file.bin", "rb") as file:
    while chunk := file.read(8192):  # 8KB chunks
        process(chunk)
```

### Reading with pathlib

```python
from pathlib import Path

# Read entire text file
content = Path("data.txt").read_text()

# Read as lines
lines = Path("data.txt").read_text().splitlines()

# Read binary
data = Path("image.jpg").read_bytes()
```

### Handling Large Files

For files too large to fit in memory:

```python
# Bad - loads entire file into memory
with open("huge_file.txt", "r") as file:
    content = file.read()  # Might crash!

# Good - process line by line
with open("huge_file.txt", "r") as file:
    for line in file:
        process(line)

# Good - read in chunks
def read_in_chunks(file_path, chunk_size=8192):
    with open(file_path, "r") as file:
        while chunk := file.read(chunk_size):
            yield chunk
```

### Common Patterns

**Check if file is empty:**

```python
with open("data.txt", "r") as file:
    first_char = file.read(1)
    if not first_char:
        print("File is empty")
```

**Skip header line:**

```python
with open("data.csv", "r") as file:
    header = file.readline()  # Skip header
    for line in file:
        process(line)
```

**Read last N lines:**

```python
from collections import deque

def tail(filename, n=10):
    with open(filename, "r") as file:
        return list(deque(file, n))
```

## Summary

Use `read()` for small files you need entirely, `readline()` for one line at a time, and `for line in file` for memory-efficient iteration. Lines include newline characters - use `strip()` to remove them. For large files, always iterate or read in chunks rather than loading everything into memory. Use `seek()` and `tell()` to navigate within files.

## Resources

- [Python Docs: Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)
- [Real Python: Reading and Writing Files](https://realpython.com/read-write-files-python/)
- [Python Docs: pathlib](https://docs.python.org/3/library/pathlib.html)
