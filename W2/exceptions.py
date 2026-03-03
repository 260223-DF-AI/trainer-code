def divide (a,b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
    except TypeError:
        print("Unsupported operand type(s)")
    except Exception as e:
        print(f"Something went wrong: {e}")
    else:
        print("Success")
        print(result)
    finally:
        print("Completed dividing")

print("Starting:")
divide(10,2)
divide(10,"2")
divide(10,0)


class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class InsufficientFundsError(Exception):
    """Raised when there are not enough funds."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.deficit = amount - balance
        super().__init__(
            f"Insufficient funds: {self.deficit}"
            f"Balance: {self.balance}"
            f"Amount: {self.amount}"
        )

class BankAccount:
    """Simple bank account with custom exceptions."""
    def __init__(self, owner, balance = 0):
        self.balance = balance
        self.owner = owner

    def withdraw(self, amount: float) -> float:
        if not isinstance(amount, (int, float)):
            raise ValidationError("Amount must be a float")
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return float(self.balance)

    def deposit(self, amount: float) -> float:
        if (type(amount) is not int) and (type(amount) is not float):
            raise ValidationError("Amount must be a float")
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        self.balance += amount
        return float(self.balance)
    
account = BankAccount("Bob", 1000)

print("happy path")
print(account.deposit(500))
print(account.withdraw(500))

print("unhappy path")
try:
    print(account.deposit(-250))
except ValidationError as e:
    print(e)

try:
    print(account.withdraw("250"))
except ValidationError:
    print("Amount must be a float")

try:    
    print(account.withdraw(2500))
except InsufficientFundsError as e:
    print(e)


def load_config(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Config file '{filename}' not found")
    
print("Exception Chaining:")
try:
    config = load_config("nonexistant.json")
except RuntimeError as e:
    print("Caught RuntimeError")
    print(e)
except Exception as e:
    print("Caught Exception")
    print(e)
    print(e.__class__.__name__)



class DatabaseConnection:
    """Simulated database connection."""
    def __init__(self, host):
        self.host = host
        self.connected = False

    def connect(self):
        print(f"Connecting to {self.host}")
        self.connected = True
    
    def disconnect(self):
        print(f"Disconnecting from {self.host}")
        self.connected = False
    
    def query(self, sql):
        if not self.connected:
            raise RuntimeError(f"Not connected to {self.host}")
        print(f"Querying {self.host} with {sql}")

        if "DROP" in sql.upper():
            raise PermissionError(f"Refused to execute {sql}")
        
        return ["Result 1", "Result 2", "Result 3"]
    
db = DatabaseConnection("localhost")

try:
    db.connect()
    results = db.query("SELECT * FROM users")
    print(results)

    results = db.query("DROP TABLE users")
    print(results)

    db.disconnect()
except PermissionError as e:
    print(e)
except RuntimeError as e:
    print(e)

finally:
    if db.connected:
        db.disconnect()