"""Utils package - provides helper methods and logging configuration."""

from .helpers import format_name, truncate
from .validators import is_valid_email, is_valid_age
from .logger import setup_logger

__all__ = [
    "is_valid_email",
    "is_valid_age"
]