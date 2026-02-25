# Binary Type

## Learning Objectives

- Understand bytes and bytearray types in Python
- Convert between strings and bytes
- Recognize use cases for binary data

## Why This Matters

Binary data is essential when working with files, network communication, and low-level data processing. Understanding bytes and bytearrays enables you to handle binary files, encode/decode text, and work with protocols that require raw byte manipulation.

## The Concept

### What are Binary Types?

Python provides two built-in binary types:

- **bytes:** Immutable sequences of bytes (0-255)
- **bytearray:** Mutable sequences of bytes

### Creating Bytes

```python
# From a literal (prefix with b)
data = b"hello"

# From a list of integers (0-255)
data = bytes([72, 101, 108, 108, 111])  # b'Hello'

# From a string with encoding
data = "hello".encode("utf-8")  # b'hello'

# Empty bytes
empty = bytes()  # or b""

# Null bytes
zeros = bytes(5)  # b'\x00\x00\x00\x00\x00'
```

### Creating Bytearrays

```python
# From bytes
ba = bytearray(b"hello")

# From a list of integers
ba = bytearray([72, 101, 108, 108, 111])

# From string with encoding
ba = bytearray("hello", "utf-8")

# Empty or zero-filled
empty = bytearray()
zeros = bytearray(5)
```

### Bytes vs Bytearray

| Aspect | bytes | bytearray |
|--------|-------|-----------|
| Mutability | Immutable | Mutable |
| Syntax | `b"..."` | `bytearray(...)` |
| Modification | Cannot change | Can modify in place |
| Hashable | Yes | No |

### Accessing Elements

```python
data = b"Hello"

# Individual bytes return integers
print(data[0])     # 72 (ASCII for 'H')
print(data[1])     # 101 (ASCII for 'e')

# Slicing returns bytes
print(data[1:4])   # b'ell'
```

### Modifying Bytearrays

```python
ba = bytearray(b"hello")

# Modify single byte
ba[0] = 72  # Change 'h' to 'H' (ASCII 72)
print(ba)  # bytearray(b'Hello')

# Append
ba.append(33)  # Add '!' (ASCII 33)
print(ba)  # bytearray(b'Hello!')

# Extend
ba.extend(b" World")
print(ba)  # bytearray(b'Hello! World')
```

### Converting Between Bytes and Strings

```python
# String to bytes (encoding)
text = "Hello, World!"
data = text.encode("utf-8")
print(data)  # b'Hello, World!'

# Bytes to string (decoding)
data = b"Hello, World!"
text = data.decode("utf-8")
print(text)  # Hello, World!

# Specify encoding for non-ASCII
unicode_text = "Hello"
utf8_bytes = unicode_text.encode("utf-8")
utf16_bytes = unicode_text.encode("utf-16")
```

### Common Encodings

| Encoding | Description |
|----------|-------------|
| `utf-8` | Variable-length Unicode, most common |
| `utf-16` | Fixed 2-4 bytes per character |
| `ascii` | 7-bit, English characters only |
| `latin-1` | 8-bit, Western European |

### Hexadecimal Representation

```python
data = b"Hello"

# To hex string
hex_str = data.hex()  # '48656c6c6f'

# From hex string
data = bytes.fromhex("48656c6c6f")  # b'Hello'
```

### Use Cases

```python
# Reading binary files
with open("image.png", "rb") as f:
    image_data = f.read()

# Writing binary files
with open("output.bin", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# Network data
# (Often used with sockets and protocols)

# Checksum/hash operations
import hashlib
hash_value = hashlib.sha256(b"hello").hexdigest()
```

### Bytes Operations

```python
data = b"Hello, World!"

# Length
print(len(data))  # 13

# Membership
print(b"World" in data)  # True

# Concatenation
combined = b"Hello" + b" " + b"World"

# Repetition
repeated = b"ab" * 3  # b'ababab'
```

## Summary

- `bytes` is an immutable sequence of integers (0-255)
- `bytearray` is a mutable version of bytes
- Use `.encode()` to convert strings to bytes
- Use `.decode()` to convert bytes to strings
- Binary types are essential for files, networking, and low-level data handling

## Additional Resources

- [Python Documentation: Binary Sequence Types](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
- [Real Python: Bytes Objects](https://realpython.com/python-strings/#bytes-objects)
- [Python bytes() Function](https://www.programiz.com/python-programming/methods/built-in/bytes)
