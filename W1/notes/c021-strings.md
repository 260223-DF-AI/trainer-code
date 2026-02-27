# Strings

## Learning Objectives

- Create and manipulate strings in Python
- Use string methods for common operations
- Apply slicing to extract portions of strings
- Format strings using f-strings and other techniques

## Why This Matters

Strings are one of the most commonly used data types. Whether you are processing user input, reading files, or building output, you will work with strings constantly. Mastering string operations is essential for effective Python programming.

## The Concept

### Creating Strings

Strings can be created with single or double quotes:

```python
name = "Alice"
greeting = 'Hello'

# Multi-line strings use triple quotes
message = """This is a
multi-line string."""
```

### String Immutability

Strings are **immutable** - once created, they cannot be changed. Operations on strings return new strings.

```python
s = "hello"
# s[0] = "H"  # Error! Strings are immutable

s = "Hello"  # Creates a new string
```

### Accessing Characters

Use index notation to access individual characters (0-indexed):

```python
word = "Python"
print(word[0])   # P
print(word[1])   # y
print(word[-1])  # n (last character)
print(word[-2])  # o (second to last)
```

### String Slicing

Extract portions of strings with slicing:

```python
text = "Hello, World!"

print(text[0:5])    # Hello
print(text[7:12])   # World
print(text[:5])     # Hello (from start)
print(text[7:])     # World! (to end)
print(text[::2])    # Hlo ol! (every 2nd char)
print(text[::-1])   # !dlroW ,olleH (reversed)
```

**Syntax:** `string[start:end:step]`

### String Length

Use `len()` to get the number of characters:

```python
message = "Hello"
print(len(message))  # 5
```

### String Methods

| Method | Description | Example |
|--------|-------------|---------|
| `upper()` | Convert to uppercase | `"hello".upper()` -> `"HELLO"` |
| `lower()` | Convert to lowercase | `"HELLO".lower()` -> `"hello"` |
| `strip()` | Remove leading/trailing whitespace | `" hi ".strip()` -> `"hi"` |
| `split()` | Split into list | `"a,b,c".split(",")` -> `["a","b","c"]` |
| `join()` | Join list into string | `"-".join(["a","b"])` -> `"a-b"` |
| `replace()` | Replace substring | `"hello".replace("l","x")` -> `"hexxo"` |
| `find()` | Find substring index | `"hello".find("l")` -> `2` |
| `startswith()` | Check prefix | `"hello".startswith("he")` -> `True` |
| `endswith()` | Check suffix | `"hello".endswith("lo")` -> `True` |
| `count()` | Count occurrences | `"hello".count("l")` -> `2` |

```python
text = "  Hello, World!  "

print(text.strip())          # "Hello, World!"
print(text.lower())          # "  hello, world!  "
print(text.replace("World", "Python"))  # "  Hello, Python!  "
print(text.split(","))       # ['  Hello', ' World!  ']
```

### String Concatenation

Join strings with `+`:

```python
first = "Hello"
second = "World"
result = first + " " + second  # "Hello World"
```

Or with `join()`:

```python
words = ["Hello", "World"]
result = " ".join(words)  # "Hello World"
```

### String Formatting with f-Strings

The modern way to embed values in strings:

```python
name = "Alice"
age = 30

print(f"Name: {name}, Age: {age}")
print(f"In hex: {255:#x}")       # 0xff
print(f"Padded: {42:05d}")       # 00042
print(f"Float: {3.14159:.2f}")   # 3.14
```

### Checking String Content

```python
text = "Hello123"

print(text.isalpha())      # False (contains digits)
print(text.isdigit())      # False (contains letters)
print(text.isalnum())      # True (letters and digits)
print("hello".islower())   # True
print("HELLO".isupper())   # True
```

### String Comparison

Strings are compared lexicographically:

```python
print("apple" < "banana")  # True
print("abc" == "abc")      # True
print("ABC" != "abc")      # True (case sensitive)
```

## Summary

- Strings are immutable sequences of characters
- Access characters by index; extract substrings with slicing
- String methods like `upper()`, `split()`, and `replace()` return new strings
- f-strings provide clean, readable formatting
- Use `len()` to get string length

## Additional Resources

- [Python Documentation: String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Real Python: Python Strings](https://realpython.com/python-strings/)
- [W3Schools: Python Strings](https://www.w3schools.com/python/python_strings.asp)
