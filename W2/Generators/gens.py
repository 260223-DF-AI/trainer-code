import sys

def count_up_to(n):

    for i in range(n):
    #     print(i)
        yield i

gen = count_up_to(1)

while(True):
    try:
        print(next(gen))
    except StopIteration:
        print("Done")
        break

square_list = [x**2 for x in range(1000000)]

print(f"Size of square_list: {sys.getsizeof(square_list) / 1000000}" + " MB")
val = 1000
print(f"Size of val: {sys.getsizeof(val)}" + " Bytes")

square_gen = (x**2 for x in range(1000000))

print(f"Size of square_gen: {sys.getsizeof(square_gen)}" + " Bytes")

print()

# fibonacci sequence 
# 0 1 1 2 3 5 8 13 21 34 55 89
def fibonacci(n):
    # initializations - only happening once
    a = 0
    b = 1
    c = 0
    count = 0

    # for i in range(n):
    while (count < n):
        # loop
        c = a + b
        count += 1

        yield c
        a = b
        b = c

# seq = fibonacci(10)
# while(True):
#     try:
#         print(next(seq))
#     except StopIteration:
#         print("Done")
#         break

for i in fibonacci(10):
    print(i)

print()

filePath = "./../../data/sample.csv"

def read_the_biggie(file):
    with open(file, "r") as f:
        for line in f:
            yield line

def parse_lines(lines):
    for line in lines:
        yield line.strip().split(",")

def filter_records(records):
    for record in records:
        if len(record) == 3:
            yield record

def transform_records(records):
    for name, age, city in records:
        yield {"name": name, "age": int(age), "city": city}



lines = read_the_biggie(filePath)
parsed = parse_lines(lines)
filtered = filter_records(parsed)
transformed = transform_records(filtered)

for record in transformed:
    print(record)