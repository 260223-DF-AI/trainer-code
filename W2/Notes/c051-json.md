# JSON

## Learning Objectives

- Understand JSON format and its use cases
- Parse JSON strings into Python objects
- Convert Python objects to JSON strings
- Read and write JSON files

## Why This Matters

JSON (JavaScript Object Notation) is the universal data exchange format of the web. APIs return JSON, configuration files use JSON, and data is stored in JSON. As a developer, you'll constantly work with JSON data from web services, databases, and files. Python's json module makes this seamless.

## Concept

### What Is JSON?

JSON is a lightweight, text-based data format. It's human-readable and language-independent:

```json
{
    "name": "Alice",
    "age": 30,
    "is_student": false,
    "courses": ["Python", "SQL", "Data Science"],
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
```

### JSON Data Types

| JSON Type | Python Type |
|-----------|-------------|
| object | dict |
| array | list |
| string | str |
| number (int) | int |
| number (real) | float |
| true/false | True/False |
| null | None |

### Importing the json Module

```python
import json
```

### Parsing JSON (String to Python)

Use `json.loads()` to parse a JSON string:

```python
import json

json_string = '{"name": "Alice", "age": 30, "active": true}'

# Parse JSON string to Python dict
data = json.loads(json_string)

print(data)           # {'name': 'Alice', 'age': 30, 'active': True}
print(data['name'])   # Alice
print(type(data))     # <class 'dict'>
```

### Converting to JSON (Python to String)

Use `json.dumps()` to convert Python objects to JSON:

```python
import json

data = {
    'name': 'Bob',
    'age': 25,
    'hobbies': ['reading', 'coding'],
    'active': True,
    'balance': None
}

# Convert to JSON string
json_string = json.dumps(data)
print(json_string)
# {"name": "Bob", "age": 25, "hobbies": ["reading", "coding"], "active": true, "balance": null}
```

### Formatting JSON Output

```python
import json

data = {'name': 'Alice', 'courses': ['Python', 'SQL']}

# Pretty print with indentation
formatted = json.dumps(data, indent=4)
print(formatted)
# {
#     "name": "Alice",
#     "courses": [
#         "Python",
#         "SQL"
#     ]
# }

# Sort keys alphabetically
sorted_json = json.dumps(data, indent=2, sort_keys=True)
```

### Reading JSON Files

Use `json.load()` (no 's') to read from a file:

```python
import json

# Read JSON from file
with open('config.json', 'r') as file:
    config = json.load(file)

print(config['database']['host'])
```

### Writing JSON Files

Use `json.dump()` (no 's') to write to a file:

```python
import json

data = {
    'users': [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'}
    ],
    'settings': {
        'theme': 'dark',
        'notifications': True
    }
}

# Write JSON to file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
```

### Handling JSON Errors

```python
import json

invalid_json = '{"name": "Alice", age: 30}'  # Missing quotes around age

try:
    data = json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    # JSON parsing error: Expecting property name enclosed in double quotes...
```

### Working with Nested JSON

```python
import json

json_data = '''
{
    "company": "TechCorp",
    "employees": [
        {"name": "Alice", "department": "Engineering"},
        {"name": "Bob", "department": "Sales"}
    ]
}
'''

data = json.loads(json_data)

# Access nested data
company = data['company']
first_employee = data['employees'][0]['name']
departments = [emp['department'] for emp in data['employees']]

print(f"Company: {company}")
print(f"First employee: {first_employee}")
print(f"Departments: {departments}")
```

### Custom JSON Encoding

Some Python types aren't JSON serializable by default:

```python
import json
from datetime import datetime, date

data = {
    'event': 'Meeting',
    'date': datetime.now()
}

# This fails!
# json.dumps(data)  # TypeError: datetime is not JSON serializable

# Solution 1: Convert manually
data['date'] = data['date'].isoformat()
json.dumps(data)

# Solution 2: Custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

json.dumps({'date': datetime.now()}, cls=DateTimeEncoder)
```

### Practical Examples

**API Response Handling:**

```python
import json

# Simulating an API response
api_response = '''
{
    "status": "success",
    "data": {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
}
'''

response = json.loads(api_response)

if response['status'] == 'success':
    for user in response['data']['users']:
        print(f"User {user['id']}: {user['name']}")
```

**Configuration Files:**

```python
import json

def load_config(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_config(config, filepath):
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)

# Usage
config = load_config('settings.json')
config['theme'] = 'light'
save_config(config, 'settings.json')
```

## Summary

JSON is the standard data exchange format for web applications. Use `json.loads()` to parse JSON strings to Python objects and `json.dumps()` to convert Python to JSON strings. For files, use `json.load()` and `json.dump()`. Format output with `indent` and `sort_keys` parameters. Handle parsing errors with try/except for `JSONDecodeError`. Custom types like datetime require special encoding.

## Resources

- [Python Docs: json](https://docs.python.org/3/library/json.html)
- [Real Python: Working with JSON](https://realpython.com/python-json/)
- [JSON.org Specification](https://www.json.org/)
