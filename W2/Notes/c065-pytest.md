# pytest

## Learning Objectives

- Write tests using pytest's simple syntax
- Use fixtures for test setup
- Parameterize tests for multiple inputs
- Understand pytest conventions and output

## Why This Matters

pytest is the most popular Python testing framework. Its simple syntax, powerful features, and rich plugin ecosystem make testing easier and more productive than unittest. Most Python projects use pytest, so familiarity with it is essential for professional development.

## Concept

### Why pytest Over unittest?

**unittest:**

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 2, 4)
```

**pytest:**

```python
def test_add():
    assert 2 + 2 == 4
```

pytest is simpler - just use `assert`.

### Installing pytest

```bash
pip install pytest
```

### Writing Tests

```python
# test_example.py

def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(5, 0) == 5
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest test_example.py

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print output
pytest -s
```

### Test Output

```
========================= test session starts ==========================
collected 3 items

test_example.py ...                                              [100%]

========================== 3 passed in 0.01s ===========================
```

Symbols: `.` = passed, `F` = failed, `E` = error

### Better Failure Messages

pytest provides detailed failure information:

```python
def test_strings():
    assert "hello" == "world"
```

Output:

```
    def test_strings():
>       assert "hello" == "world"
E       AssertionError: assert 'hello' == 'world'
E         - world
E         + hello
```

### Testing Exceptions

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Fixtures

Fixtures provide setup and teardown for tests:

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

def test_sum(sample_list):
    assert sum(sample_list) == 15

def test_length(sample_list):
    assert len(sample_list) == 5
```

**Fixture scope:**

```python
@pytest.fixture(scope="function")   # Default: per test
@pytest.fixture(scope="class")      # Per test class
@pytest.fixture(scope="module")     # Per module/file
@pytest.fixture(scope="session")    # Entire test session
```

**Setup and Teardown:**

```python
@pytest.fixture
def database():
    # Setup
    db = connect_database()
    yield db  # Provide to test
    # Teardown
    db.close()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Parameterized Tests

Run the same test with different inputs:

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

This runs 4 tests with different values.

### Markers

Mark tests for special handling:

```python
import pytest

@pytest.mark.slow
def test_big_computation():
    # Slow test
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass
```

Run only marked tests:

```bash
pytest -m slow
pytest -m "not slow"
```

### Test Organization

```
project/
    src/
        calculator.py
    tests/
        __init__.py
        test_calculator.py
        conftest.py         # Shared fixtures
```

**conftest.py - Shared fixtures:**

```python
# tests/conftest.py
import pytest

@pytest.fixture
def calculator():
    from src.calculator import Calculator
    return Calculator()
```

Fixtures in conftest.py are available to all tests.

### Practical Example

```python
# src/user.py
class User:
    def __init__(self, name, email):
        if not name:
            raise ValueError("Name required")
        if "@" not in email:
            raise ValueError("Invalid email")
        self.name = name
        self.email = email
    
    def greet(self):
        return f"Hello, {self.name}!"

# tests/test_user.py
import pytest
from src.user import User

@pytest.fixture
def valid_user():
    return User("Alice", "alice@example.com")

class TestUserCreation:
    def test_valid_user(self, valid_user):
        assert valid_user.name == "Alice"
        assert valid_user.email == "alice@example.com"
    
    def test_empty_name(self):
        with pytest.raises(ValueError, match="Name required"):
            User("", "test@example.com")
    
    def test_invalid_email(self):
        with pytest.raises(ValueError, match="Invalid email"):
            User("Bob", "invalid-email")

class TestUserGreet:
    def test_greet(self, valid_user):
        assert valid_user.greet() == "Hello, Alice!"
    
    @pytest.mark.parametrize("name,expected", [
        ("Bob", "Hello, Bob!"),
        ("Charlie", "Hello, Charlie!"),
    ])
    def test_greet_different_names(self, name, expected):
        user = User(name, f"{name.lower()}@example.com")
        assert user.greet() == expected
```

## Summary

pytest offers simpler syntax than unittest - just use `assert`. Run tests with `pytest` command. Use fixtures for setup/teardown with `@pytest.fixture`. Test exceptions with `pytest.raises()`. Use `@pytest.mark.parametrize` for multiple test cases. Organize shared fixtures in `conftest.py`. pytest's clear output and powerful features make testing more productive.

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Real Python: Testing with pytest](https://realpython.com/pytest-python-testing/)
- [pytest Fixture Reference](https://docs.pytest.org/en/stable/reference/fixtures.html)
