"""Some helper functions for string and data manipulation."""

def format_name(first, last):
    """Format a fullname from the first and last names."""
    return f"{first} {last}"

def truncate(text, length=50):
    """Truncate text to a certain length."""
    if len(text) <= length:
        return text
    else:
        return text[:length] + "..."
    
DEFAULT_ENCODING = "utf-8"