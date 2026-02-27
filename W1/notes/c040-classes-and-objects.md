# Classes and Objects

## Learning Objectives

- Understand the relationship between classes and objects
- Create classes with constructors, attributes, and methods
- Instantiate objects and access their properties

## Why This Matters

Object-Oriented Programming (OOP) is a fundamental paradigm in software development. Classes provide blueprints for creating objects that combine data and behavior. Understanding classes is essential for building maintainable, scalable applications.

## The Concept

### What is a Class?

A **class** is a blueprint for creating objects. It defines the attributes (data) and methods (functions) that objects of that type will have.

### What is an Object?

An **object** is an instance of a class. Each object has its own copy of the attributes defined by the class.

### Defining a Class

```python
class Dog:
    pass  # Empty class

# Create an object (instance)
my_dog = Dog()
print(type(my_dog))  # <class '__main__.Dog'>
```

### The Constructor (**init**)

The `__init__` method initializes new objects:

```python
class Dog:
    def __init__(self, name, age):
        self.name = name  # Instance attribute
        self.age = age    # Instance attribute

# Create objects
buddy = Dog("Buddy", 3)
max_dog = Dog("Max", 5)

print(buddy.name)  # Buddy
print(max_dog.age) # 5
```

### Instance Attributes

Attributes belong to individual objects:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

alice = Person("Alice", 30)
bob = Person("Bob", 25)

# Each object has its own attributes
print(alice.name)  # Alice
print(bob.name)    # Bob

# Modify attributes
alice.age = 31
print(alice.age)  # 31
print(bob.age)    # 25 (unchanged)
```

### Instance Methods

Methods define behavior for objects:

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        print(f"{self.name} says Woof!")
    
    def get_age_in_dog_years(self):
        return self.age * 7

buddy = Dog("Buddy", 3)
buddy.bark()  # Buddy says Woof!
print(buddy.get_age_in_dog_years())  # 21
```

### The self Parameter

`self` refers to the current instance. It is automatically passed when calling methods:

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def get_count(self):
        return self.count

c = Counter()
c.increment()
c.increment()
print(c.get_count())  # 2
```

### Class Attributes

Attributes shared by all instances:

```python
class Dog:
    species = "Canis familiaris"  # Class attribute
    
    def __init__(self, name):
        self.name = name  # Instance attribute

buddy = Dog("Buddy")
max_dog = Dog("Max")

# Class attribute is shared
print(buddy.species)    # Canis familiaris
print(max_dog.species)  # Canis familiaris
print(Dog.species)      # Canis familiaris

# Instance attributes are separate
print(buddy.name)  # Buddy
print(max_dog.name)  # Max
```

### Methods with Parameters

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.balance

account = BankAccount("Alice", 100)
account.deposit(50)
print(account.get_balance())  # 150
account.withdraw(30)
print(account.get_balance())  # 120
```

### String Representation (**str**)

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name} is {self.age} years old"

buddy = Dog("Buddy", 3)
print(buddy)  # Buddy is 3 years old
```

### Complete Example

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"

rect = Rectangle(5, 3)
print(rect)             # Rectangle(5x3)
print(rect.area())      # 15
print(rect.perimeter()) # 16
```

## Summary

- Classes are blueprints; objects are instances
- `__init__` is the constructor that initializes objects
- `self` refers to the current instance
- Instance attributes belong to individual objects
- Class attributes are shared across all instances
- Methods define object behavior

## Additional Resources

- [Python Documentation: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Real Python: OOP in Python](https://realpython.com/python3-object-oriented-programming/)
- [W3Schools: Python Classes](https://www.w3schools.com/python/python_classes.asp)
