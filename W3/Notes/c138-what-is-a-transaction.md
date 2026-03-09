# Transactions

## Learning Objectives

- Understand what transactions are and why they matter
- Apply BEGIN, COMMIT, and ROLLBACK
- Implement savepoints for partial rollback
- Recognize transaction isolation concepts

## Why This Matters

Transactions ensure database operations are completed reliably. They protect against partial failures, maintain data consistency, and allow you to safely make complex changes. Understanding transactions is essential for building reliable applications that handle financial data, inventory, or any operation where data integrity is critical.

## The Concept

### What is a Transaction?

A **transaction** is a sequence of database operations treated as a single unit. Transactions follow the ACID properties:

| Property | Description |
|----------|-------------|
| **A**tomicity | All or nothing - all operations succeed or all fail |
| **C**onsistency | Database moves from valid state to valid state |
| **I**solation | Concurrent transactions don't interfere |
| **D**urability | Committed changes survive system failures |

### Basic Transaction Syntax

```sql
BEGIN;  -- or START TRANSACTION
    -- SQL statements here
COMMIT;  -- Save all changes

-- Or to cancel:
BEGIN;
    -- SQL statements here
ROLLBACK;  -- Undo all changes
```

### Transaction Model

```
BEGIN                        COMMIT
  |                            |
  v                            v
  +----------------------------+
  |     Transaction Scope      |
  +----------------------------+
       All operations are:
       - Invisible to others until COMMIT
       - Undone if ROLLBACK
```

### COMMIT Example

Save changes permanently:

```sql
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
    INSERT INTO accounts (name, balance) VALUES ('Bob', 500);
COMMIT;
-- Both inserts are now permanent
```

### ROLLBACK Example

Undo all changes:

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
    UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
    -- Oops, something's wrong!
ROLLBACK;
-- Neither update happened
```

### Classic Transfer Example

Money transfer must be atomic:

```sql
BEGIN;
    -- Debit source
    UPDATE accounts SET balance = balance - 500 
    WHERE account_id = 1;
    
    -- Credit destination
    UPDATE accounts SET balance = balance + 500 
    WHERE account_id = 2;
    
    -- Record the transfer
    INSERT INTO transfers (from_id, to_id, amount) 
    VALUES (1, 2, 500);
COMMIT;
-- All three succeed together or none do
```

### Savepoints

Create checkpoints within a transaction:

```sql
BEGIN;
    INSERT INTO orders (customer_id) VALUES (1);
    SAVEPOINT after_order;
    
    INSERT INTO order_items (order_id, product_id, qty) VALUES (1, 100, 2);
    -- Problem with this item!
    ROLLBACK TO SAVEPOINT after_order;
    
    -- Try different item
    INSERT INTO order_items (order_id, product_id, qty) VALUES (1, 200, 1);
COMMIT;
-- Order created with second item, first item never happened
```

### Transaction Isolation

Transactions can be isolated from each other at different levels:

| Level | Description |
|-------|-------------|
| READ UNCOMMITTED | Can see uncommitted changes (dirty reads) |
| READ COMMITTED | Only sees committed changes (PostgreSQL default) |
| REPEATABLE READ | Consistent snapshot for duration |
| SERIALIZABLE | Strictest; transactions appear sequential |

```sql
-- Set isolation level for transaction
BEGIN ISOLATION LEVEL REPEATABLE READ;
    -- Statements
COMMIT;
```

### Autocommit Mode

PostgreSQL commits each statement automatically unless in a transaction:

```sql
-- This is immediately committed
INSERT INTO logs (message) VALUES ('Event occurred');

-- These are grouped
BEGIN;
    INSERT INTO logs (message) VALUES ('Step 1');
    INSERT INTO logs (message) VALUES ('Step 2');
COMMIT;
```

### Transaction in Error Handling

PostgreSQL aborts transactions on error:

```sql
BEGIN;
    INSERT INTO products (product_id, name) VALUES (1, 'Test');
    INSERT INTO products (product_id, name) VALUES (1, 'Duplicate');
    -- ERROR: duplicate key violation
    -- Transaction is now in failed state
COMMIT;  -- This will actually ROLLBACK

-- Must explicitly rollback to continue
ROLLBACK;
```

## Code Example

Comprehensive transaction usage:

```sql
-- Create tables
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10, 2) CHECK (balance >= 0)
);

CREATE TABLE transfers (
    transfer_id SERIAL PRIMARY KEY,
    from_account INTEGER REFERENCES accounts(account_id),
    to_account INTEGER REFERENCES accounts(account_id),
    amount DECIMAL(10, 2),
    transfer_date TIMESTAMP DEFAULT NOW()
);

-- Initial data
INSERT INTO accounts (name, balance) VALUES 
    ('Alice', 1000),
    ('Bob', 500),
    ('Carol', 750);

-- Basic transaction
BEGIN;
    UPDATE accounts SET balance = balance * 1.05;  -- 5% interest
COMMIT;

SELECT * FROM accounts;

-- Transfer with transaction
BEGIN;
    -- Check balance first
    DO $$
    DECLARE
        current_balance DECIMAL(10, 2);
    BEGIN
        SELECT balance INTO current_balance 
        FROM accounts WHERE account_id = 1;
        
        IF current_balance < 200 THEN
            RAISE EXCEPTION 'Insufficient funds';
        END IF;
    END $$;
    
    UPDATE accounts SET balance = balance - 200 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 200 WHERE account_id = 2;
    INSERT INTO transfers (from_account, to_account, amount) VALUES (1, 2, 200);
COMMIT;

SELECT * FROM accounts;
SELECT * FROM transfers;

-- Savepoint example
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Dave', 300);
    SAVEPOINT added_dave;
    
    UPDATE accounts SET balance = balance + 1000000 WHERE name = 'Dave';
    -- Wait, that's wrong!
    ROLLBACK TO SAVEPOINT added_dave;
    
    UPDATE accounts SET balance = balance + 100 WHERE name = 'Dave';
COMMIT;

SELECT * FROM accounts WHERE name = 'Dave';
-- Dave has 400 (300 initial + 100), not 1,000,300

-- Rollback example
BEGIN;
    DELETE FROM accounts WHERE name = 'Carol';
    -- Changed my mind!
ROLLBACK;

SELECT * FROM accounts WHERE name = 'Carol';
-- Carol still exists

-- Failed transaction example
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Eve', 100);
    UPDATE accounts SET balance = balance - 10000 WHERE name = 'Eve';
    -- ERROR: new row violates check constraint (balance >= 0)
ROLLBACK;

SELECT * FROM accounts WHERE name = 'Eve';
-- Eve was never created
```

## Key Takeaways

- Transactions group operations into atomic units (all or nothing)
- BEGIN starts, COMMIT saves, ROLLBACK cancels
- Savepoints allow partial rollback within a transaction
- PostgreSQL auto-commits individual statements outside transactions
- On error, PostgreSQL aborts the transaction
- Use transactions for any multi-statement operation that must succeed together

## Additional Resources

- [PostgreSQL Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [SAVEPOINT](https://www.postgresql.org/docs/current/sql-savepoint.html)
