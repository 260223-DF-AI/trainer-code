# Example Solutions: Python Project Setup

These are example solutions for the e006 Project Setup exercise.

---

## Solution: Project Structure

Create the following directory structure:

```bash
mkdir -p task_manager/src/task_manager/models
mkdir -p task_manager/src/task_manager/utils
mkdir -p task_manager/tests
```

---

## Solution: Virtual Environment Setup

```bash
# Create virtual environment
cd task_manager
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify
which python  # Should show venv path
```

---

## Solution: requirements.txt

```txt
colorama==0.4.6
pytest==7.4.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Solution: .gitignore

```gitignore
# Virtual environment
venv/
.venv/
env/

# Python cache
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Distribution
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
```

---

## Solution: src/task_manager/models/task.py

```python
"""Task model for the task manager application."""

from datetime import datetime
from typing import Optional


class Task:
    """Represents a task in the task manager."""
    
    _id_counter = 0
    
    def __init__(
        self, 
        title: str, 
        description: str = "", 
        completed: bool = False
    ):
        """
        Initialize a new Task.
        
        Args:
            title: The task title (required)
            description: Optional task description
            completed: Whether the task is completed
        """
        Task._id_counter += 1
        self.id = Task._id_counter
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False
    
    def to_dict(self) -> dict:
        """
        Convert task to dictionary representation.
        
        Returns:
            Dictionary with task data
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """Return formatted string representation."""
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}. {self.title}"
    
    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"
```

---

## Solution: src/task_manager/utils/validators.py

```python
"""Validation utilities for the task manager."""


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_title(title: str) -> str:
    """
    Validate a task title.
    
    Args:
        title: The title to validate
        
    Returns:
        The cleaned title
        
    Raises:
        ValidationError: If title is invalid
    """
    if not title:
        raise ValidationError("Title cannot be empty")
    
    title = title.strip()
    
    if len(title) == 0:
        raise ValidationError("Title cannot be only whitespace")
    
    if len(title) > 100:
        raise ValidationError("Title must be 100 characters or less")
    
    return title


def validate_description(description: str) -> str:
    """
    Validate a task description.
    
    Args:
        description: The description to validate
        
    Returns:
        The cleaned description
    """
    if description is None:
        return ""
    
    description = description.strip()
    
    if len(description) > 500:
        raise ValidationError("Description must be 500 characters or less")
    
    return description
```

---

## Solution: src/task_manager/utils/formatters.py

```python
"""Formatting utilities for the task manager."""

from datetime import datetime
from typing import List

# Try to import colorama for colored output
try:
    from colorama import Fore, Style, init
    init()
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False


def format_date(dt: datetime) -> str:
    """
    Format a datetime object to a readable string.
    
    Args:
        dt: The datetime to format
        
    Returns:
        Formatted date string
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def format_task_list(tasks: List) -> str:
    """
    Format a list of tasks for display.
    
    Args:
        tasks: List of Task objects
        
    Returns:
        Formatted string representation
    """
    if not tasks:
        return "No tasks found."
    
    lines = ["=" * 40]
    lines.append("TASK LIST")
    lines.append("=" * 40)
    
    for task in tasks:
        if HAS_COLOR:
            if task.completed:
                status = f"{Fore.GREEN}[DONE]{Style.RESET_ALL}"
            else:
                status = f"{Fore.YELLOW}[TODO]{Style.RESET_ALL}"
        else:
            status = "[DONE]" if task.completed else "[TODO]"
        
        lines.append(f"{status} {task.id}. {task.title}")
        
        if task.description:
            lines.append(f"      {task.description[:50]}...")
    
    lines.append("=" * 40)
    lines.append(f"Total: {len(tasks)} tasks")
    
    return "\n".join(lines)


def format_task_detail(task) -> str:
    """
    Format a single task with full details.
    
    Args:
        task: The Task object to format
        
    Returns:
        Detailed formatted string
    """
    status = "Completed" if task.completed else "Pending"
    created = format_date(task.created_at)
    
    return f"""
Task #{task.id}
-----------
Title: {task.title}
Status: {status}
Created: {created}
Description: {task.description or 'No description'}
""".strip()
```

---

## Solution: src/task_manager/__init__.py

```python
"""Task Manager package - A simple CLI task management application."""

from task_manager.models.task import Task
from task_manager.utils.validators import validate_title, ValidationError
from task_manager.utils.formatters import format_task_list, format_date

__version__ = "1.0.0"
__all__ = [
    "Task",
    "validate_title",
    "ValidationError",
    "format_task_list",
    "format_date"
]
```

---

## Solution: src/task_manager/__main__.py

```python
"""Entry point for the task manager CLI."""

from task_manager.models.task import Task
from task_manager.utils.formatters import format_task_list, format_task_detail
from task_manager.utils.validators import validate_title, ValidationError


def print_welcome():
    """Print welcome message."""
    print("=" * 40)
    print("       TASK MANAGER CLI v1.0")
    print("=" * 40)
    print()


def print_menu():
    """Print the main menu."""
    print("\nOptions:")
    print("  1. Add a task")
    print("  2. List all tasks")
    print("  3. Mark task complete")
    print("  4. Delete a task")
    print("  5. Exit")
    print()


def main():
    """Main function to run the CLI."""
    tasks = []
    
    print_welcome()
    
    while True:
        print_menu()
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            # Add task
            try:
                title = input("Enter task title: ")
                title = validate_title(title)
                description = input("Enter description (optional): ")
                task = Task(title, description)
                tasks.append(task)
                print(f"\nTask #{task.id} created successfully!")
            except ValidationError as e:
                print(f"\nError: {e}")
        
        elif choice == "2":
            # List tasks
            print("\n" + format_task_list(tasks))
        
        elif choice == "3":
            # Mark complete
            if not tasks:
                print("\nNo tasks to complete.")
                continue
            try:
                task_id = int(input("Enter task ID to complete: "))
                task = next((t for t in tasks if t.id == task_id), None)
                if task:
                    task.mark_complete()
                    print(f"\nTask #{task_id} marked complete!")
                else:
                    print(f"\nTask #{task_id} not found.")
            except ValueError:
                print("\nPlease enter a valid number.")
        
        elif choice == "4":
            # Delete task
            if not tasks:
                print("\nNo tasks to delete.")
                continue
            try:
                task_id = int(input("Enter task ID to delete: "))
                task = next((t for t in tasks if t.id == task_id), None)
                if task:
                    tasks.remove(task)
                    print(f"\nTask #{task_id} deleted!")
                else:
                    print(f"\nTask #{task_id} not found.")
            except ValueError:
                print("\nPlease enter a valid number.")
        
        elif choice == "5":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
```

---

## Solution: tests/test_task.py

```python
"""Tests for the Task model."""

import pytest
from task_manager.models.task import Task


class TestTask:
    """Test cases for the Task class."""
    
    def test_create_task_basic(self):
        """Test creating a basic task."""
        task = Task("Test Task")
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
    
    def test_create_task_with_description(self):
        """Test creating a task with description."""
        task = Task("My Task", "This is a description")
        assert task.title == "My Task"
        assert task.description == "This is a description"
    
    def test_mark_complete(self):
        """Test marking a task complete."""
        task = Task("Test")
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True
    
    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task("Test Task", "Description")
        data = task.to_dict()
        
        assert data["title"] == "Test Task"
        assert data["description"] == "Description"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
    
    def test_str_representation(self):
        """Test string representation."""
        task = Task("My Task")
        assert "My Task" in str(task)
        assert "[ ]" in str(task)
        
        task.mark_complete()
        assert "[x]" in str(task)
```

---

## Running the Project

```bash
# From project root
cd task_manager

# Run the CLI
python -m task_manager

# Run tests
pytest tests/ -v
```

---

## Expected Output

```
$ python -m task_manager
========================================
       TASK MANAGER CLI v1.0
========================================

Options:
  1. Add a task
  2. List all tasks
  3. Mark task complete
  4. Delete a task
  5. Exit

Enter choice (1-5): 1
Enter task title: Learn Python
Enter description (optional): Complete the Python course

Task #1 created successfully!
```
