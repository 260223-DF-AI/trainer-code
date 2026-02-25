# User Input and Output

## Learning Objectives

- Get input from users using the `input()` function
- Display output using the `print()` function
- Format output with f-strings and other methods

## Why This Matters

Interactive programs need to communicate with users. Input allows your program to receive data from users, while output displays results and feedback. These fundamental operations are essential for building any interactive application.

## The Concept

### Output with print()

The `print()` function displays text to the console:

```python
print("Hello, World!")
```

**Output:**

```
Hello, World!
```

#### Printing Multiple Values

Separate values with commas:

```python
name = "Alice"
age = 30
print("Name:", name, "Age:", age)
```

**Output:**

```
Name: Alice Age: 30
```

#### Customizing Separators and Endings

```python
# Custom separator
print("a", "b", "c", sep="-")  # a-b-c

# Custom ending (default is newline)
print("Hello", end=" ")
print("World")  # Hello World (on same line)
```

### Input with input()

The `input()` function pauses execution and waits for user input:

```python
name = input("Enter your name: ")
print("Hello,", name)
```

**Console Interaction:**

```
Enter your name: Alice
Hello, Alice
```

#### Important: input() Returns a String

All input is returned as a string, even numbers:

```python
age = input("Enter your age: ")
print(type(age))  # <class 'str'>
```

To use numeric input, convert it:

```python
age = int(input("Enter your age: "))
price = float(input("Enter the price: "))
```

### String Formatting

#### f-Strings (Recommended)

f-strings (formatted string literals) are the modern, preferred way to format strings:

```python
name = "Alice"
age = 30

# Embed variables directly
print(f"My name is {name} and I am {age} years old.")

# Expressions inside braces
print(f"In 5 years, I will be {age + 5}.")

# Formatting numbers
pi = 3.14159
print(f"Pi to 2 decimals: {pi:.2f}")  # 3.14
```

#### .format() Method

An older but still common approach:

```python
print("Hello, {}!".format(name))
print("{} is {} years old.".format(name, age))
print("{0} said {1}. {0} left.".format("Alice", "goodbye"))
```

#### % Formatting (Legacy)

The oldest method, still seen in older code:

```python
print("Hello, %s!" % name)
print("%s is %d years old." % (name, age))
```

### Escape Characters

Special characters in strings:

| Escape | Description |
|--------|-------------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |

```python
print("Line 1\nLine 2")
print("Column1\tColumn2")
print("She said, \"Hello!\"")
```

### Raw Strings

Prefix with `r` to ignore escape characters:

```python
print(r"C:\Users\name\folder")  # C:\Users\name\folder
```

### Complete Example

```python
# Get user information
name = input("What is your name? ")
age = int(input("How old are you? "))
city = input("Where do you live? ")

# Display formatted output
print(f"\n--- User Profile ---")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"City: {city}")
print(f"In 10 years, you will be {age + 10} years old.")
```

**Sample Output:**

```
What is your name? Alice
How old are you? 25
Where do you live? New York

--- User Profile ---
Name: Alice
Age: 25
City: New York
In 10 years, you will be 35 years old.
```

## Summary

- Use `print()` to display output to the console
- Use `input()` to receive user input (always returns a string)
- Convert input with `int()` or `float()` for numeric operations
- f-strings provide the cleanest way to format output
- Escape characters like `\n` and `\t` add special formatting

## Additional Resources

- [Python Documentation: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html)
- [Real Python: Python print()](https://realpython.com/python-print/)
- [Real Python: Python f-Strings](https://realpython.com/python-f-strings/)
