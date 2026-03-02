# Regular Expressions (Regex)

## Learning Objectives

- Understand what regular expressions are and when to use them
- Write basic regex patterns for common use cases
- Use Python's re module for pattern matching
- Apply regex to validate and extract data

## Why This Matters

Regular expressions are a powerful tool for text processing. They're used to validate user input (emails, phone numbers), search and extract patterns from text, and perform complex find-and-replace operations. While they have a learning curve, regex skills are invaluable for data cleaning and text manipulation.

## Concept

### What Are Regular Expressions?

Regular expressions (regex) are patterns that describe sets of strings. They're used to:

- Validate input formats (email, phone, dates)
- Search for patterns in text
- Extract specific information
- Replace text matching patterns

### The re Module

```python
import re
```

### Basic Pattern Matching

```python
import re

text = "The quick brown fox jumps over the lazy dog"

# Check if pattern exists
if re.search("fox", text):
    print("Found 'fox' in text")

# Find all matches
matches = re.findall("the", text, re.IGNORECASE)
print(matches)  # ['The', 'the']
```

### Special Characters (Metacharacters)

| Character | Meaning | Example |
|-----------|---------|---------|
| `.` | Any character except newline | `a.c` matches "abc", "a1c" |
| `^` | Start of string | `^Hello` matches "Hello world" |
| `$` | End of string | `world$` matches "Hello world" |
| `*` | 0 or more repetitions | `ab*c` matches "ac", "abc", "abbc" |
| `+` | 1 or more repetitions | `ab+c` matches "abc", "abbc" (not "ac") |
| `?` | 0 or 1 repetition | `ab?c` matches "ac", "abc" |
| `\` | Escape special character | `\.` matches literal "." |

### Character Classes

| Pattern | Meaning |
|---------|---------|
| `[abc]` | a, b, or c |
| `[^abc]` | NOT a, b, or c |
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit |
| `[a-zA-Z0-9]` | Any alphanumeric |

### Predefined Character Classes

| Pattern | Meaning | Equivalent |
|---------|---------|------------|
| `\d` | Any digit | `[0-9]` |
| `\D` | Non-digit | `[^0-9]` |
| `\w` | Word character | `[a-zA-Z0-9_]` |
| `\W` | Non-word character | `[^a-zA-Z0-9_]` |
| `\s` | Whitespace | `[ \t\n\r\f\v]` |
| `\S` | Non-whitespace | `[^ \t\n\r\f\v]` |

### Quantifiers

| Pattern | Meaning |
|---------|---------|
| `{n}` | Exactly n times |
| `{n,}` | n or more times |
| `{n,m}` | Between n and m times |

```python
import re

# Match exactly 3 digits
re.search(r'\d{3}', '123')     # Match
re.search(r'\d{3}', '12')      # No match

# Match 2-4 letters
re.search(r'[a-z]{2,4}', 'abc')  # Match
```

### Common re Functions

```python
import re

text = "Contact: email@example.com and test@domain.org"

# re.search() - Find first match
match = re.search(r'\w+@\w+\.\w+', text)
if match:
    print(match.group())  # email@example.com

# re.findall() - Find all matches
emails = re.findall(r'\w+@\w+\.\w+', text)
print(emails)  # ['email@example.com', 'test@domain.org']

# re.sub() - Replace matches
result = re.sub(r'\w+@\w+\.\w+', '[EMAIL]', text)
print(result)  # Contact: [EMAIL] and [EMAIL]

# re.split() - Split by pattern
parts = re.split(r'\s+', "Hello   World")
print(parts)  # ['Hello', 'World']

# re.match() - Match at beginning only
re.match(r'Hello', 'Hello World')  # Match
re.match(r'World', 'Hello World')  # No match (not at beginning)
```

### Using Groups

Parentheses create capture groups:

```python
import re

text = "John Smith, age 30"

# Extract name and age
pattern = r'(\w+) (\w+), age (\d+)'
match = re.search(pattern, text)

if match:
    print(match.group(0))   # Full match: John Smith, age 30
    print(match.group(1))   # First group: John
    print(match.group(2))   # Second group: Smith
    print(match.group(3))   # Third group: 30
    print(match.groups())   # All groups: ('John', 'Smith', '30')

# Named groups
pattern = r'(?P<first>\w+) (?P<last>\w+), age (?P<age>\d+)'
match = re.search(pattern, text)
print(match.group('first'))  # John
print(match.group('last'))   # Smith
```

### Raw Strings

Always use raw strings (r"...") for regex patterns to avoid escape issues:

```python
# Without raw string (problematic)
pattern = "\\d+"  # Need double backslash

# With raw string (preferred)
pattern = r"\d+"  # Single backslash works
```

### Practical Examples

**Email Validation:**

```python
import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

print(is_valid_email("user@example.com"))  # True
print(is_valid_email("invalid-email"))     # False
```

**Phone Number Extraction:**

```python
import re

text = "Call me at 555-123-4567 or (555) 987-6543"

# Match different phone formats
pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
phones = re.findall(pattern, text)
print(phones)  # ['555-123-4567', '(555) 987-6543']
```

**Password Validation:**

```python
import re

def validate_password(password):
    """
    Password must:
    - Be at least 8 characters
    - Contain at least one uppercase
    - Contain at least one lowercase
    - Contain at least one digit
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

print(validate_password("Abc12345"))  # True
print(validate_password("abc12345"))  # False (no uppercase)
```

### Compilation for Performance

If using the same pattern multiple times, compile it:

```python
import re

# Compile once
email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

# Use many times
email_pattern.match("user@example.com")
email_pattern.match("another@domain.org")
```

## Summary

Regular expressions are patterns for matching and manipulating text. Use the re module with functions like `search()`, `findall()`, `sub()`, and `match()`. Common patterns include `\d` for digits, `\w` for word characters, and `\s` for whitespace. Quantifiers like `*`, `+`, and `{n,m}` control repetition. Groups capture parts of matches. Always use raw strings (r"pattern") for regex patterns.

## Resources

- [Python Docs: re](https://docs.python.org/3/library/re.html)
- [Real Python: Regular Expressions](https://realpython.com/regex-python/)
- [Regex101 - Online Tester](https://regex101.com/)
