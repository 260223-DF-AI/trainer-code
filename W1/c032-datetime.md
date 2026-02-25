# Datetime

## Learning Objectives

- Work with dates and times using Python's datetime module
- Create, format, and parse date/time objects
- Perform date arithmetic and comparisons

## Why This Matters

Handling dates and times is essential for logging, scheduling, data analysis, and countless other applications. The datetime module provides the tools you need to work with temporal data accurately.

## The Concept

### The datetime Module

Python's `datetime` module provides classes for working with dates and times:

| Class | Description |
|-------|-------------|
| `date` | Calendar date (year, month, day) |
| `time` | Time of day (hour, minute, second, microsecond) |
| `datetime` | Combined date and time |
| `timedelta` | Duration between two dates/times |

### Importing datetime

```python
from datetime import date, time, datetime, timedelta
```

### Working with Dates

```python
from datetime import date

# Current date
today = date.today()
print(today)  # 2024-01-15 (example)

# Create specific date
birthday = date(1990, 5, 20)
print(birthday)  # 1990-05-20

# Access components
print(today.year)   # 2024
print(today.month)  # 1
print(today.day)    # 15

# Day of week (0=Monday, 6=Sunday)
print(today.weekday())  # 0
print(today.isoweekday())  # 1 (1=Monday, 7=Sunday)
```

### Working with Times

```python
from datetime import time

# Create time
lunch = time(12, 30, 0)
print(lunch)  # 12:30:00

# With microseconds
precise = time(14, 30, 45, 123456)
print(precise)  # 14:30:45.123456

# Access components
print(lunch.hour)   # 12
print(lunch.minute) # 30
print(lunch.second) # 0
```

### Working with Datetime

```python
from datetime import datetime

# Current date and time
now = datetime.now()
print(now)  # 2024-01-15 10:30:45.123456

# Create specific datetime
event = datetime(2024, 12, 25, 18, 0, 0)
print(event)  # 2024-12-25 18:00:00

# Access components
print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)

# Combine date and time
d = date(2024, 6, 15)
t = time(14, 30)
dt = datetime.combine(d, t)
print(dt)  # 2024-06-15 14:30:00
```

### Formatting Dates (strftime)

Convert datetime to string:

```python
from datetime import datetime

now = datetime.now()

# Common format codes
print(now.strftime("%Y-%m-%d"))        # 2024-01-15
print(now.strftime("%d/%m/%Y"))        # 15/01/2024
print(now.strftime("%B %d, %Y"))       # January 15, 2024
print(now.strftime("%I:%M %p"))        # 10:30 AM
print(now.strftime("%A, %B %d, %Y"))   # Monday, January 15, 2024
```

**Common Format Codes:**

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2024 |
| `%m` | Month (01-12) | 01 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour 24h (00-23) | 14 |
| `%I` | Hour 12h (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%p` | AM/PM | PM |
| `%A` | Weekday name | Monday |
| `%B` | Month name | January |

### Parsing Dates (strptime)

Convert string to datetime:

```python
from datetime import datetime

# Parse from string
date_str = "2024-01-15"
dt = datetime.strptime(date_str, "%Y-%m-%d")
print(dt)  # 2024-01-15 00:00:00

# Parse with time
datetime_str = "15/01/2024 14:30"
dt = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
print(dt)  # 2024-01-15 14:30:00
```

### Date Arithmetic with timedelta

```python
from datetime import datetime, timedelta

now = datetime.now()

# Add/subtract time
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
in_2_hours = now + timedelta(hours=2)

# Multiple units
future = now + timedelta(days=30, hours=5, minutes=30)

# Difference between dates
date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 12, 31)
diff = date2 - date1
print(diff.days)  # 365
```

### Comparing Dates

```python
from datetime import datetime

date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 6, 15)

print(date1 < date2)   # True
print(date1 == date2)  # False
print(date1 != date2)  # True
```

## Summary

- Use `date` for dates, `time` for times, `datetime` for both
- `strftime()` formats datetime to string
- `strptime()` parses string to datetime
- `timedelta` enables date arithmetic
- Compare dates with standard comparison operators

## Additional Resources

- [Python Documentation: datetime](https://docs.python.org/3/library/datetime.html)
- [strftime() Reference](https://strftime.org/)
- [Real Python: datetime](https://realpython.com/python-datetime/)
