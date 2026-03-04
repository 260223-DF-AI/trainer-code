print("hello world")

sample_data = """Name,Age,City,
Richard,35,Vero Beach,
Dylan,26,Flossmoor,
Charles,22,Glen Ellyn,
Lee,22,Dallas,
Jaisal,23,Morton Grove,
Tim,25,West Dundee,
Ben,23,Atkinson,
Joey,23,Lasalle,
Isabelle,22,Long Grove,
Dio,24,London,
Lucas,23,Lindenhurst,
Alec,31,Des Plaines,
Magan,22,Vernon Hills,
Danielle,22,Plainfields,
Andy,24,Darien,
Andrew,22,East Brunswick,
"""

with open("data/sample.csv", "w") as f:
    f.write(sample_data)

print("created the file")
print()

with open("data/sample.csv", "r") as f:
    content = f.read()
    print(content)
    print(f"number of characters: {len(content)}")


records = []
with open("data/sample.csv", "r") as f:
    # line_count = len(f)

    # for line in f:
    #     print(line)

    for i, line in enumerate(f):
        if i == 0:
            continue # we would need to do 
# something here to read the column names from the first line
        entry = line.split(",")[:-1]
        records.append({
            "name": entry[0],
            "age": entry[1],
            "city": entry[2],
        })

print(records)
        
def save_report(data, filename):
    with open(filename, "w") as f:
        f.write(f"Personal Information Report\n\n")
        for record in data:
            f.write(f"Name: {record['name']}\n")
            f.write(f"Age: {record['age']}\n")
            f.write(f"City: {record['city']}\n\n")
            f.write(f"-"*20 + "\n")
        f.write(f"Number of records: {len(data)}")

save_report(records, "data/report.txt")

def append_logs(message, filename = "data/app.log"):
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(filename, "a") as f:

        f.write(f"{timestamp} | {message}\n")


append_logs("User logged in")
append_logs("User logged out")
append_logs("User logged in")