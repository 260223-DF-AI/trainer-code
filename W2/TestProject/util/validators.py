import re

def is_valid_email(email: str) -> bool: 
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_age(age: int) -> bool: 
    return  0 < age < 120