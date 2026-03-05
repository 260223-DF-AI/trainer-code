text = """
Python is a great programming language.
Python is used for web development.
Python is also used for data science.
Data science is becoming very popular.
"""

colors = ["red", "blue", "red", "green", "blue", "blue", "red", "yellow"]

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

from collections import Counter

count = Counter(words)
print(count)
print(count.most_common(2))

from collections import namedtuple
myToup = ("apple", "banana", "cherry")
Point = namedtuple("Point", ["x", "y", "z"])
Person = namedtuple("Person", ["name", "age", "city"])

origin = Point(0, 0, 0)
target = Point(1, 1, 1)


richard = Person("Richard", 35, "Vero Beach")
# print(richard)
# print(richard.name)
# print(richard.age)
# print(richard.city)

# print(richard[0])
# print(richard[1])
# print(richard[2])

#unpacking
name, age, city = richard
# print(name)
# print(age)
# print(city)

richard = richard._replace(city = "Paris")
# print(richard)

from collections import deque

q = deque(colors)
# print(q)
# print(q.pop())
# print(q)
# print(q.popleft())
# print(q)
# q.append("purple")
# print(q)
q.appendleft("orange")
print(q)

mini = deque(maxlen=5)
mini.append(1)
mini.append(2)
mini.append(3)
mini.append(4)
mini.append(5)
mini.append(6)
print(mini)

recent_logs = deque(maxlen=10)

for log in recent_logs:
    print(log)
    