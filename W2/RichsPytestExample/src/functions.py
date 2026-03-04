class Functions:

    def __init__(self):
        pass

    # add function
    def add(self,a, b):
        if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
            raise ValueError("Both arguments must be numbers")
        return a + b

    # subtract function
    def subtract(self, a, b):
        if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
            raise ValueError("Both arguments must be numbers")
        return a - b

    # multiply function
    def multiply(self, a, b):
        if (not isinstance(a, (int, float)) or not isinstance(b, (int, float))):
            raise ValueError("Both arguments must be numbers")
        return a * b

    # divide function
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    # is_even function
    def is_even(self, n):
        if not isinstance(n, (int, float)):
            raise ValueError("Argument must be an integer")
        return n % 2 == 0

    # reverse_string function
    def reverse_string(self, s):
        if not isinstance(s, str):
            raise ValueError("Argument must be a string")
        return s[::-1]

    # factorial function
    def factorial(self, n):
        if n < 0: #*
            raise ValueError("Factorial not defined for negative numbers")#*
        if n == 0: #*
            return 1 #*
        return n * factorial(n - 1) #*

    # count_vowels function
    def count_vowels(self, s):
        if not isinstance(s, str):
            raise ValueError("Argument must be a string")
        sum = 0
        for char in s.lower():
            if (char in "aeiou"):
                sum += 1
        return sum

    def is_odd(self, n):
        return n % 2 == 1