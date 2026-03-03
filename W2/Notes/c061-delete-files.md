# Deleting Files

## Learning Objectives

- Delete files and directories using os and pathlib
- Check for file existence before operations
- Handle common file operation errors
- Manage file system operations safely

## Why This Matters

Managing files includes removing them when no longer needed. Temporary files, old logs, and processed data files often need cleanup. Understanding how to safely delete files prevents accidental data loss and handles common edge cases like missing files or permission errors.

## Concept

### Deleting Files with os

```python
import os

# Delete a file
os.remove("unwanted_file.txt")

# Alternative
os.unlink("unwanted_file.txt")  # Same as os.remove()
```

### Checking Before Deleting

Always check if a file exists before deleting:

```python
import os

filename = "old_data.txt"

if os.path.exists(filename):
    os.remove(filename)
    print(f"Deleted: {filename}")
else:
    print(f"File not found: {filename}")
```

### Using pathlib (Recommended)

```python
from pathlib import Path

file_path = Path("unwanted_file.txt")

# Check and delete
if file_path.exists():
    file_path.unlink()
    print(f"Deleted: {file_path}")

# Delete, missing_ok=True ignores missing files
file_path.unlink(missing_ok=True)
```

### Handling Errors

```python
import os

try:
    os.remove("file.txt")
except FileNotFoundError:
    print("File does not exist")
except PermissionError:
    print("No permission to delete this file")
except IsADirectoryError:
    print("Cannot use os.remove() on a directory")
except OSError as e:
    print(f"Error deleting file: {e}")
```

### Deleting Directories

**Empty directories:**

```python
import os

os.rmdir("empty_folder")  # Only works if directory is empty
```

**Directories with contents:**

```python
import shutil

shutil.rmtree("folder_with_contents")  # Deletes everything inside!
```

**Using pathlib:**

```python
from pathlib import Path

# Empty directory
Path("empty_folder").rmdir()

# For non-empty directories, still need shutil
import shutil
shutil.rmtree(Path("folder_with_contents"))
```

### Safe Directory Deletion

```python
import shutil
from pathlib import Path

def safe_delete_directory(path):
    """Delete a directory safely with confirmation."""
    dir_path = Path(path)
    
    if not dir_path.exists():
        print(f"Directory not found: {path}")
        return False
    
    if not dir_path.is_dir():
        print(f"Not a directory: {path}")
        return False
    
    # Count files for safety check
    file_count = sum(1 for _ in dir_path.rglob("*"))
    print(f"Will delete {file_count} items in {path}")
    
    confirm = input("Proceed? (yes/no): ")
    if confirm.lower() == "yes":
        shutil.rmtree(dir_path)
        print("Deleted successfully")
        return True
    
    print("Deletion cancelled")
    return False
```

### Common File Operations

**Rename/Move:**

```python
import os

os.rename("old_name.txt", "new_name.txt")
os.rename("file.txt", "subdir/file.txt")  # Move and/or rename
```

**Copy:**

```python
import shutil

shutil.copy("source.txt", "destination.txt")
shutil.copy2("source.txt", "dest.txt")  # Preserves metadata
shutil.copytree("source_dir", "dest_dir")  # Copy entire directory
```

### Practical Examples

**Clean up temporary files:**

```python
import os
from pathlib import Path

def cleanup_temp_files(directory, extension=".tmp"):
    """Delete all files with given extension in directory."""
    dir_path = Path(directory)
    deleted_count = 0
    
    for file_path in dir_path.glob(f"*{extension}"):
        try:
            file_path.unlink()
            deleted_count += 1
        except OSError as e:
            print(f"Could not delete {file_path}: {e}")
    
    print(f"Deleted {deleted_count} {extension} files")

cleanup_temp_files(".", ".tmp")
```

**Delete files older than N days:**

```python
import os
import time
from pathlib import Path

def delete_old_files(directory, max_age_days):
    """Delete files older than max_age_days."""
    dir_path = Path(directory)
    cutoff_time = time.time() - (max_age_days * 86400)
    
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            if file_path.stat().st_mtime < cutoff_time:
                print(f"Deleting old file: {file_path}")
                file_path.unlink()

delete_old_files("logs", 30)  # Delete files older than 30 days
```

**Safe file replacement:**

```python
import os
from pathlib import Path

def safe_replace(old_file, new_file):
    """Replace old_file with new_file safely."""
    old_path = Path(old_file)
    new_path = Path(new_file)
    backup_path = old_path.with_suffix(".bak")
    
    # Create backup of old file
    if old_path.exists():
        old_path.rename(backup_path)
    
    try:
        # Replace with new file
        new_path.rename(old_path)
    except Exception as e:
        # Restore backup on failure
        if backup_path.exists():
            backup_path.rename(old_path)
        raise e
    
    # Clean up backup
    if backup_path.exists():
        backup_path.unlink()
```

### File Operations Summary

| Operation | os module | pathlib |
|-----------|-----------|---------|
| Delete file | `os.remove(path)` | `Path(path).unlink()` |
| Delete empty dir | `os.rmdir(path)` | `Path(path).rmdir()` |
| Check exists | `os.path.exists(path)` | `Path(path).exists()` |
| Check is file | `os.path.isfile(path)` | `Path(path).is_file()` |
| Check is dir | `os.path.isdir(path)` | `Path(path).is_dir()` |
| Rename | `os.rename(old, new)` | `Path(old).rename(new)` |

## Summary

Use `os.remove()` or `Path.unlink()` to delete files. Use `os.rmdir()` for empty directories or `shutil.rmtree()` for directories with contents (be careful - this deletes everything). Always check if files exist before operations and handle common exceptions like FileNotFoundError and PermissionError. The pathlib module provides a cleaner, object-oriented interface that's generally preferred in modern Python code.

## Resources

- [Python Docs: os module](https://docs.python.org/3/library/os.html)
- [Python Docs: pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python Docs: shutil](https://docs.python.org/3/library/shutil.html)
