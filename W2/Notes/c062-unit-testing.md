# Unit Testing

## Learning Objectives

- Understand unit testing concepts and benefits
- Write tests using Python's unittest module
- Structure tests with test cases and assertions
- Run and interpret test results

## Why This Matters

Testing ensures your code works correctly and continues to work as it evolves. Unit tests catch bugs early, provide documentation of expected behavior, and give confidence when refactoring. Testing is a core professional skill - most development teams require tests for new code.

## Concept

### What Is Unit Testing?

Unit testing verifies that individual units of code (functions, methods, classes) work correctly in isolation. A unit test:

- Tests one specific piece of functionality
- Runs automatically
- Produces a pass or fail result
- Is repeatable and independent

### The unittest Module

Python includes the `unittest` module:

```python
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative_numbers(self):
        result = add(-1, -1)
        self.assertEqual(result, -2)
    
    def test_add_zero(self):
        result = add(5, 0)
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()
```

### Test Structure

1. **Test Case**: A class inheriting from `unittest.TestCase`
2. **Test Method**: A method starting with `test_`
3. **Assertion**: A check that verifies expected behavior

### Common Assertions

| Assertion | Description |
|-----------|-------------|
| `assertEqual(a, b)` | a == b |
| `assertNotEqual(a, b)` | a != b |
| `assertTrue(x)` | bool(x) is True |
| `assertFalse(x)` | bool(x) is False |
| `assertIsNone(x)` | x is None |
| `assertIsNotNone(x)` | x is not None |
| `assertIn(a, b)` | a in b |
| `assertRaises(exc)` | Exception is raised |
| `assertAlmostEqual(a, b)` | a == b (within delta) |

### Testing Exceptions

```python
class TestDivision(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            result = 10 / 0
    
    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            result = "hello" + 5
```

### Setup and Teardown

Run code before/after each test:

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Runs before each test method."""
        self.db = Database()
        self.db.connect()
    
    def tearDown(self):
        """Runs after each test method."""
        self.db.disconnect()
    
    def test_insert(self):
        self.db.insert({"name": "Alice"})
        self.assertEqual(self.db.count(), 1)
```

Class-level setup:

```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in class."""
        cls.connection = create_connection()
    
    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in class."""
        cls.connection.close()
```

### Running Tests

**From command line:**

```bash
# Run a test file
python -m unittest test_module.py

# Run all tests in a directory
python -m unittest discover

# Verbose output
python -m unittest -v test_module.py
```

**Test output:**

```
test_add_negative_numbers (test_calculator.TestAddFunction) ... ok
test_add_positive_numbers (test_calculator.TestAddFunction) ... ok
test_add_zero (test_calculator.TestAddFunction) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Organizing Tests

Typical project structure:

```
my_project/
    my_module/
        __init__.py
        calculator.py
    tests/
        __init__.py
        test_calculator.py
```

### Practical Example

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# test_calculator.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add_integers(self):
        self.assertEqual(self.calc.add(5, 3), 8)
    
    def test_add_floats(self):
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=7)
    
    def test_divide_normal(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```

### Best Practices

1. **Test one thing per test** - Clear failure messages
2. **Use descriptive names** - `test_add_negative_numbers_returns_sum`
3. **Keep tests independent** - Each test should run in isolation
4. **Arrange-Act-Assert** - Setup, execute, verify
5. **Test edge cases** - Zero, negative, empty, None

```python
def test_example(self):
    # Arrange
    calculator = Calculator()
    
    # Act
    result = calculator.add(5, 3)
    
    # Assert
    self.assertEqual(result, 8)
```

## Summary

Unit testing verifies individual code units work correctly. Use Python's `unittest` module to write test cases with assertions like `assertEqual` and `assertRaises`. Organize tests in classes inheriting from `TestCase`, with methods starting with `test_`. Use `setUp` and `tearDown` for common setup. Run tests with `python -m unittest`. While unittest is built-in, pytest (covered later this week) offers a simpler syntax many teams prefer.

## Resources

- [Python Docs: unittest](https://docs.python.org/3/library/unittest.html)
- [Real Python: Getting Started with Testing](https://realpython.com/python-testing/)
- [Python Testing with unittest](https://docs.python.org/3/library/unittest.html#organizing-tests)
