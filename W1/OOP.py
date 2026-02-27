class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self): # to be overridden!
        raise NotImplementedError("Subclasses must implement speak()")

    def __str__(self):
        return f"{self.name}, {self.age}"
    
    def describe(self):
        return (f"I am {self.name}.")

class Dog(Animal): # this is the dog class

    
    # functions/behaviors
    def __init__(self, name, age, legs, fluffieness): # attributes/parameters/proerties/variables
        super().__init__(name, age)
        self.legs = legs
        self.fluffieness = fluffieness

    def __str__(self):
        return f"{self.name}, {self.age}, {self.legs}, {self.fluffieness}" # "<name>, <age>"

    def __repr__(self):
        return f"dog name = {self.name}, age = {self.age}, legs = {self.legs}, fluffieness = {self.fluffieness}" # "dog name = <name>, age = <age>"

    def speak(self):
        return "Woof!"
    
    def rollontheground(self):
        return f"*Rolling on the ground, being {self.fluffieness} of fluffies*"
   

d = Dog("Fido", 3, 4, "very fluffy")
print(d)
print(repr(d))
print(d.speak())
print(d.rollontheground())
print(d.describe())

class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def speak(self):
        return super().describe() +"Meow!"
    
    def describe(self):
        return f"I am a cat."
        
c = Cat("Whiskers", 2)
print(c.speak())
print(c.describe())

class Groot(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)

    def speak(self):
        return "I am Groot!"
    
    def __str__(self):
        return f"still groot"
    
    def add(a,b,c):
        print(a)
        print(b)
        print(c)
        return c + b

    
g = Groot("Groot", 1000)
print(g.speak())
print(g.describe())

print()
print( "+" * 25)
print(g.add(1,2))