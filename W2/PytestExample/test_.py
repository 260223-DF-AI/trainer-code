import pytest

# --- Functions ---

# add function
def add(a, b):
    if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
        raise ValueError("Both arguments must be numbers")
    return a + b

# subtract function
def subtract(a, b):
    if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
        raise ValueError("Both arguments must be numbers")
    return a - b

# multiply function
def multiply(a, b):
    if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
        raise ValueError("Both arguments must be numbers")
    return a * b

# divide function
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# is_even function
def is_even(n):
    if not isinstance(n, (int, float)):
        raise ValueError("Argument must be an integer")
    return n % 2 == 0

# reverse_string function
def reverse_string(s):
    if not isinstance(s, str):
        raise ValueError("Argument must be a string")
    return s[::-1]

# factorial function
def factorial(n):
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

# count_vowels function
def count_vowels(s):
    if not isinstance(s, str):
        raise ValueError("Argument must be a string")
    sum = 0
    for char in s.lower():
        if (char in "aeiou"):
            sum += 1
    return sum


# --- Tests ---

# Test cases for add function
def test_add():
    assert add(10, 10) == 20
    assert add(-1, 1) == 0
    assert add(0, 0) == 0    

# Test cases for subtract function
def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 3) == -3

# Test cases for multiply function
def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0
    assert multiply(-2, 5) == -10

# Test cases for divide function
def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5

# Test case for divide by zero
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)

# Test cases for is_even function
def test_is_even():
    assert is_even(4) == True
    assert is_even(7) == False
    assert is_even(0) == True

# Test cases for reverse_string function
def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"

# Test cases for factorial function
def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120
    assert factorial(3) == 6

# Test case for factorial of negative number
def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)

# Test cases for count_vowels function
def test_count_vowels():
    assert count_vowels("hello") == 2
    assert count_vowels("AEIOU") == 5
    assert count_vowels("xyz") == 0

def test_float():
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)