# Inheritance

## Learning Objectives

- Implement single and multiple inheritance
- Use super() to call parent class methods
- Override methods in child classes

## Why This Matters

Inheritance is a cornerstone of object-oriented programming that promotes code reuse and logical hierarchy. By understanding inheritance, you can build on existing classes, reduce duplication, and create flexible, extensible designs.

## The Concept

### What is Inheritance?

**Inheritance** allows a class (child/derived) to inherit attributes and methods from another class (parent/base). The child class can use, extend, or override the parent's functionality.

### Basic Inheritance

```python
# Parent class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Some sound"

# Child class inherits from Animal
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

# Dog has all Animal attributes and methods
buddy = Dog("Buddy")
print(buddy.name)    # Buddy (inherited attribute)
print(buddy.speak()) # Buddy says Woof! (overridden method)
```

### The super() Function

Use `super()` to call the parent class's methods:

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # Call parent's __init__
        self.breed = breed  # Add new attribute

buddy = Dog("Buddy", 3, "Golden Retriever")
print(buddy.name)   # Buddy
print(buddy.age)    # 3
print(buddy.breed)  # Golden Retriever
```

### Method Overriding

Child classes can override parent methods:

```python
class Animal:
    def speak(self):
        return "Some sound"
    
    def describe(self):
        return f"I am a {type(self).__name__}"

class Dog(Animal):
    def speak(self):  # Override
        return "Woof!"

class Cat(Animal):
    def speak(self):  # Override
        return "Meow!"

dog = Dog()
cat = Cat()
print(dog.speak())     # Woof!
print(cat.speak())     # Meow!
print(dog.describe())  # I am a Dog (inherited, not overridden)
```

### Extending Methods

Call parent method and add functionality:

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def describe(self):
        return f"I am {self.name}"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def describe(self):
        base = super().describe()  # Call parent method
        return f"{base}, a {self.breed}"

buddy = Dog("Buddy", "Golden Retriever")
print(buddy.describe())  # I am Buddy, a Golden Retriever
```

### isinstance() and issubclass()

```python
class Animal:
    pass

class Dog(Animal):
    pass

buddy = Dog()

# Check instance type
print(isinstance(buddy, Dog))     # True
print(isinstance(buddy, Animal))  # True (Dog is an Animal)
print(isinstance(buddy, str))     # False

# Check class hierarchy
print(issubclass(Dog, Animal))    # True
print(issubclass(Animal, Dog))    # False
```

### Multiple Inheritance

A class can inherit from multiple parents:

```python
class Swimmer:
    def swim(self):
        return "Swimming!"

class Flyer:
    def fly(self):
        return "Flying!"

class Duck(Swimmer, Flyer):
    def quack(self):
        return "Quack!"

duck = Duck()
print(duck.swim())   # Swimming!
print(duck.fly())    # Flying!
print(duck.quack())  # Quack!
```

### Method Resolution Order (MRO)

Python determines which method to call using MRO:

```python
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.greet())  # Hello from B

# View the MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

### Complete Example

```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        return "Vehicle starting..."
    
    def __str__(self):
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors
    
    def start(self):
        return f"{self} engine starting... Vroom!"

class ElectricCar(Car):
    def __init__(self, brand, model, doors, battery_capacity):
        super().__init__(brand, model, doors)
        self.battery_capacity = battery_capacity
    
    def start(self):
        return f"{self} powering up silently..."
    
    def charge(self):
        return f"Charging {self.battery_capacity}kWh battery"

tesla = ElectricCar("Tesla", "Model 3", 4, 75)
print(tesla.start())   # Tesla Model 3 powering up silently...
print(tesla.charge())  # Charging 75kWh battery
```

## Summary

- Inheritance creates child classes that inherit from parent classes
- Use `super()` to call parent class methods
- Override methods to customize child class behavior
- Python supports multiple inheritance
- MRO determines method lookup order
- Use `isinstance()` and `issubclass()` to check relationships

## Additional Resources

- [Python Documentation: Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
- [Real Python: Inheritance and Composition](https://realpython.com/inheritance-composition-python/)
- [W3Schools: Python Inheritance](https://www.w3schools.com/python/python_inheritance.asp)
