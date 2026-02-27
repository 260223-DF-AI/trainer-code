# OOP Concepts

## Learning Objectives

- Understand the four pillars of Object-Oriented Programming
- Recognize encapsulation, abstraction, inheritance, and polymorphism
- Apply OOP principles to Python code

## Why This Matters

Object-Oriented Programming provides a powerful way to organize code, model real-world entities, and build scalable systems. Understanding these core principles helps you design better software and collaborate effectively with other developers.

## The Concept

### The Four Pillars of OOP

1. **Encapsulation** - Bundling data and methods together
2. **Abstraction** - Hiding complexity, exposing essentials
3. **Inheritance** - Creating new classes from existing ones
4. **Polymorphism** - Using a unified interface for different types

---

### 1. Encapsulation

Encapsulation bundles data (attributes) and methods that operate on that data within a class. It also controls access to internal state.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # Convention: _ means "protected"
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
    
    def get_balance(self):
        return self._balance

# Users interact through methods, not directly with _balance
account = BankAccount("Alice", 100)
account.deposit(50)
print(account.get_balance())  # 150
```

**Access Conventions:**

- `public` - No underscore, accessible everywhere
- `_protected` - Single underscore, internal use suggested
- `__private` - Double underscore, name mangling applied

---

### 2. Abstraction

Abstraction hides complex implementation details and exposes only the necessary interface.

```python
class EmailService:
    def send_email(self, to, subject, body):
        """Simple interface - complexity is hidden."""
        self._validate_address(to)
        self._format_message(subject, body)
        self._connect_to_server()
        self._transmit()
    
    def _validate_address(self, address):
        # Internal complexity hidden
        pass
    
    def _format_message(self, subject, body):
        # Internal complexity hidden
        pass
    
    def _connect_to_server(self):
        # Internal complexity hidden
        pass
    
    def _transmit(self):
        # Internal complexity hidden
        pass

# User only needs to know the simple interface
email = EmailService()
email.send_email("bob@example.com", "Hello", "Hi Bob!")
```

---

### 3. Inheritance

Inheritance allows a class to inherit attributes and methods from another class.

```python
# Parent class (base class)
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass  # To be overridden

# Child class (derived class)
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")

print(dog.speak())  # Buddy says Woof!
print(cat.speak())  # Whiskers says Meow!
```

We will explore inheritance in more depth in the next topic.

---

### 4. Polymorphism

Polymorphism allows objects of different classes to be treated through the same interface.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Duck:
    def speak(self):
        return "Quack!"

# Polymorphism in action
def make_speak(animal):
    print(animal.speak())

animals = [Dog(), Cat(), Duck()]
for animal in animals:
    make_speak(animal)

# Output:
# Woof!
# Meow!
# Quack!
```

**Duck Typing:** In Python, if it walks like a duck and quacks like a duck, it is a duck. The type does not matter as long as the object has the required methods.

---

### Bringing It Together

```python
class Shape:
    """Abstract base - defines interface (Abstraction)."""
    def area(self):
        raise NotImplementedError
    
    def perimeter(self):
        raise NotImplementedError

class Rectangle(Shape):
    """Inherits from Shape (Inheritance)."""
    
    def __init__(self, width, height):
        # Data bundled with class (Encapsulation)
        self._width = width
        self._height = height
    
    def area(self):
        return self._width * self._height
    
    def perimeter(self):
        return 2 * (self._width + self._height)

class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius
    
    def area(self):
        return 3.14159 * self._radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self._radius

# Polymorphism - same interface, different implementations
def print_info(shape):
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.perimeter()}")

shapes = [Rectangle(5, 3), Circle(4)]
for shape in shapes:
    print_info(shape)
    print()
```

---

### Magic (Dunder) Methods

Python uses special methods surrounded by double underscores (like `__init__`) to integrate custom classes with built-in functionality. These are commonly called **magic methods** or **dunder** (double underscore) methods. You rarely call these methods directly yourself; instead, Python calls them under the hood when you use built-in functions or operators on your objects.

#### 1. Initialization

- `__init__(self, ...)`: Initializes a newly created object.

#### 2. String Representation

- `__str__(self)`: Defines the human-readable string representation (used by `print()` or `str()`).
- `__repr__(self)`: Defines the unambiguous, developer-readable string representation (used for debugging/logging).

#### 3. Mathematical Operators

You can make your objects work with standard math operators:

- `__add__(self, other)`: Allows `obj1 + obj2`
- `__sub__(self, other)`: Allows `obj1 - obj2`
- `__mul__(self, other)`: Allows `obj1 * obj2`
- `__truediv__(self, other)`: Allows `obj1 / obj2`

#### 4. Comparison Operators

You can define how objects should be compared against each other:

- `__eq__(self, other)`: Allows `obj1 == obj2`
- `__lt__(self, other)`: Allows `obj1 < obj2`
- `__gt__(self, other)`: Allows `obj1 > obj2`

#### 5. Emulating Containers and Collections

You can make your object act like a list or dictionary:

- `__len__(self)`: Allows `len(obj)` to return the size.
- `__getitem__(self, key)`: Allows indexing or dictionary lookups, like `obj[key]` or `obj[0]`.

#### 6. Iteration and Context Managers

- `__iter__(self)`: Returns an iterator object to allow loops (`for item in obj:`).
- `__enter__(self)` / `__exit__(self, ...)`: Creates a context manager for the `with` statement (e.g., `with open(file):`).

Magic methods are what make custom Python objects feel native and intuitive to use, allowing them to work naturally with standard operators (`+`, `==`) and built-in functions.

---

### Benefits of OOP

- **Modularity:** Classes are self-contained units
- **Reusability:** Inheritance promotes code reuse
- **Flexibility:** Polymorphism enables flexible designs
- **Maintainability:** Encapsulation limits change impact

## Summary

- **Encapsulation:** Bundle data and methods, control access
- **Abstraction:** Hide complexity, expose simple interface
- **Inheritance:** Create new classes based on existing ones
- **Polymorphism:** Same interface, different implementations
- **Magic Methods:** Use dunder methods (e.g., `__init__`, `__str__`) to hook into built-in Python behaviors
- Python supports all four pillars of OOP

## Additional Resources

- [Real Python: OOP Concepts](https://realpython.com/python3-object-oriented-programming/)
- [Python Documentation: Classes](https://docs.python.org/3/tutorial/classes.html)
- [GeeksforGeeks: OOP in Python](https://www.geeksforgeeks.org/python-oops-concepts/)
