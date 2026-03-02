"""Entry point for the application."""

# absolute import
from TestProject.services.user_service import create_user, User

# relative import
#??
from TestProject import util

def main():
    """ Main function for execution."""
    print("Hello from main.py")

    logger = util.setup_logger(__name__)
    logger.info("Main started")

    try: # attempt to execute the code that COULD have an exception
        user = create_user("Rich", "Hawkins", "rich.hawkins@revature.com", 35)
    # else: # if no exception, execute this code
        print(f"Created user {user}")
        print(f"Email: {user.email}")
    except ValueError as e: # if there is an exception, catch it here
        print(f"ValueError creating user: {e}")
    except Exception as e: # if there is an exception, catch it here
        print(f"Exception creating user: {e}")
    # finally: # always execute this code
        # print("Goodbye from main.py")

    try:
        user = create_user("Rich", "Hawkins", "richardhawkinsatrevaturedotcom", -35)
    except ValueError as e:
        print(f"ValueError creating user: {e}")

    logger.info("Main completed successfully")

if __name__ == "__main__":
    main()

# main()