# contact_book.py - Contact Book Application
# Starter code for e003-exercise-data-structures

"""
Contact Book Application
------------------------
A simple contact management system using Python data structures.

Data Structure:
- Each contact is a dictionary with: name, phone, email, category, created_at
- All contacts are stored in a list

Complete the TODO sections below to finish the application.
"""

from datetime import datetime

# =============================================================================
# Initialize Contact Book
# =============================================================================
contacts = []


# =============================================================================
# TODO: Task 1 - Create the Contact Book
# =============================================================================

def add_contact(contacts, name, phone, email, category):
    """
    Add a new contact to the contact book.
    
    Args:
        contacts: The list of all contacts
        name: Contact's full name
        phone: Contact's phone number
        email: Contact's email address
        category: One of: friend, family, work, other
    
    Returns:
        The created contact dictionary
    """
    # TODO: Create a contact dictionary with all fields
    # TODO: Add created_at timestamp using datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # TODO: Append to contacts list
    # TODO: Return the new contact
    pass


# =============================================================================
# TODO: Task 2 - Display Contacts
# =============================================================================

def display_all_contacts(contacts):
    """
    Display all contacts in a formatted table.
    
    Output format:
    =============================================
                CONTACT BOOK (X contacts)
    =============================================
    #  | Name            | Phone         | Category
    ---|-----------------|---------------|----------
    1  | Alice Johnson   | 555-123-4567  | friend
    ...
    """
    # TODO: Print header with contact count
    # TODO: Print table headers
    # TODO: Loop through contacts and print each row
    # TODO: Print footer
    pass


def display_contact_details(contact):
    """
    Display detailed information for a single contact.
    
    Output format:
    --- Contact Details ---
    Name:     [name]
    Phone:    [phone]
    Email:    [email]
    Category: [category]
    Added:    [created_at]
    ------------------------
    """
    # TODO: Print formatted contact details
    pass


# =============================================================================
# TODO: Task 3 - Search Functionality
# =============================================================================

def search_by_name(contacts, query):
    """
    Find contacts whose name contains the query string.
    Case-insensitive search.
    
    Returns:
        List of matching contacts
    """
    # TODO: Filter contacts where query is in name (case-insensitive)
    # Hint: Use list comprehension and .lower()
    pass


def filter_by_category(contacts, category):
    """
    Return all contacts in a specific category.
    
    Returns:
        List of contacts matching the category
    """
    # TODO: Filter contacts by category
    pass


def find_by_phone(contacts, phone):
    """
    Find a contact by exact phone number.
    
    Returns:
        The contact dictionary if found, None otherwise
    """
    # TODO: Search for contact with matching phone
    pass


# =============================================================================
# TODO: Task 4 - Update and Delete
# =============================================================================

def update_contact(contacts, phone, field, new_value):
    """
    Update a specific field of a contact.
    
    Args:
        contacts: The list of all contacts
        phone: Phone number to identify the contact
        field: The field to update (name, phone, email, or category)
        new_value: The new value for the field
    
    Returns:
        True if updated, False if contact not found
    """
    # TODO: Find contact by phone
    # TODO: Update the specified field
    # TODO: Return success/failure
    pass


def delete_contact(contacts, phone):
    """
    Delete a contact by phone number.
    
    Returns:
        True if deleted, False if not found
    """
    # TODO: Find and remove contact with matching phone
    pass


# =============================================================================
# TODO: Task 5 - Statistics
# =============================================================================

def display_statistics(contacts):
    """
    Display statistics about the contact book.
    
    Output:
    --- Contact Book Statistics ---
    Total Contacts: X
    By Category:
      - Friends: X
      - Family: X
      - Work: X
      - Other: X
    Most Recent: [name] (added [date])
    -------------------------------
    """
    # TODO: Count total contacts
    # TODO: Count contacts by category
    # TODO: Find most recently added contact
    pass


# =============================================================================
# STRETCH GOAL: Interactive Menu
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n========== CONTACT BOOK ==========")
    print("1. View all contacts")
    print("2. Add new contact")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. View statistics")
    print("0. Exit")
    print("==================================")


def main():
    """Main function with interactive menu."""
    # TODO: Implement menu loop
    # Use while True and break on exit choice
    pass


# =============================================================================
# Test Code - Add sample data and test functions
# =============================================================================

if __name__ == "__main__":
    print("Contact Book Application")
    print("=" * 40)
    
    # TODO: Add at least 5 sample contacts
    # add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "friend")
    
    # TODO: Test your functions
    # display_all_contacts(contacts)
    # results = search_by_name(contacts, "alice")
    # etc.
    
    # STRETCH: Uncomment to run interactive menu
    # main()
