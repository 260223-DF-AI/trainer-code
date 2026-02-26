# this is a comment!
# anything that is "commented out" will not execute!

""" 
This is a block or multi-line comment!
it's awesome for adding a more complex description of what you program does!
"""

value = 2+3 # we can add commenting to the end of the line to tell what we were doing!
name = "Richard"
print("Hello " + name)
name = "Andrew"
print("Hello " + name)
print(value)

# functions!
def greet(name):
    print("Hello " + name)
    print(f"Hello {name}")

greet("Richard")


# functions with lists
def acceptList(mylist):
    print("start function")
    for item in mylist:
        print(item)
    print("end function")

def expandedList(arg):
    print("start function")
    print(arg)
    print("end function")

mylist = ["apple", "banana", "cherry", "date", "elderberry", "fig"]

print(mylist) # print the whole list            ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']
print(*mylist) # print each item in the list    apple banana cherry date elderberry fig
print(mylist[:]) # print the whole list         ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']
print(mylist[1:4]) # print from index 1 to 3    ['banana', 'cherry', 'date']
print(mylist[::-1]) # print the list in reverse ['fig', 'elderberry', 'date', 'cherry', 'banana', 'apple']

print()

print("Call function")
[expandedList(x) for x in mylist]   # call the function for each item in the list
print("returned from function")


## Lambda Functions
mynumberlist = [1, 2, 3, 4, 5]


print()
square = lambda x: x * x

print(square(5))

add = lambda x, y: x + y

print(add(5, 5))

# the square brackets show/denote that we're going to deal with a list
# the square(x) is the function, but is the "results"
# the for loop is kinda backwards, but still works!
mysqaurednumbers = [square(x) for x in mynumberlist]

"""
mysqaurednumbers = []
for x in mynumberlist:
    square(x)
    mysqaurednumbers.append(square(x))
"""
print(mysqaurednumbers)


# Some more fun with collections, lambdas, and some collection functions.
print(f"/n/n")

"""
Create a list of numbers.
Without changing the original list, 
produce a new list of the squares of the numbers.
"""



"""
Using the original list,
create a new list of the numbers that are even.
"""