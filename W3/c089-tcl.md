# TCL: Transaction Control Language

## Learning Objectives

- Understand what transactions are and why they matter
- Master TCL commands: COMMIT, ROLLBACK, SAVEPOINT
- Apply transactions to ensure data integrity
- Recognize when to use explicit transactions

## Why This Matters

Transactions are essential for maintaining data consistency. When multiple related changes must succeed or fail together, transactions ensure you never end up in a partially modified state. Understanding TCL prevents data corruption, especially in financial, inventory, and any system where accuracy is critical.

## The Concept

### What is a Transaction?

A transaction is a sequence of database operations that are treated as a single unit. Either all operations succeed, or none of them do.

Consider a bank transfer:

```
1. Deduct $100 from Account A
2. Add $100 to Account B
```

If step 1 succeeds but step 2 fails, money disappears! Transactions ensure both steps happen or neither does.

### TCL Commands

| Command | Purpose |
|---------|---------|
| BEGIN / START TRANSACTION | Start a transaction |
| COMMIT | Save all changes permanently |
| ROLLBACK | Undo all changes since BEGIN |
| SAVEPOINT | Create a checkpoint within transaction |
| ROLLBACK TO | Undo to a specific savepoint |
| RELEASE SAVEPOINT | Remove a savepoint |

### Basic Transaction Flow

```
BEGIN
   |
   v
+------------------+
| SQL Operations   |  <-- Changes are temporary
| INSERT, UPDATE,  |
| DELETE, etc.     |
+------------------+
   |
   +-----> COMMIT    --> Changes become permanent
   |
   +-----> ROLLBACK  --> Changes are discarded
```

### Transaction Syntax

**Starting a Transaction**:

```sql
-- These are equivalent
BEGIN;
BEGIN TRANSACTION;
START TRANSACTION;
```

**Committing (Saving)**:

```sql
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
    INSERT INTO accounts (name, balance) VALUES ('Bob', 500);
COMMIT;  -- Both inserts are now permanent
```

**Rolling Back (Undoing)**:

```sql
BEGIN;
    DELETE FROM accounts WHERE balance < 0;
    -- Wait, that was a mistake!
ROLLBACK;  -- The DELETE never happened
```

### Auto-Commit Mode

By default, PostgreSQL auto-commits each statement:

```sql
-- Without explicit transaction, this commits immediately
INSERT INTO logs (message) VALUES ('This is permanent');

-- With explicit transaction, you control when to commit
BEGIN;
    INSERT INTO logs (message) VALUES ('This is pending');
    -- Not committed yet, can still rollback
COMMIT;  -- Now it's permanent
```

### SAVEPOINT for Checkpoints

Savepoints allow partial rollbacks:

```sql
BEGIN;
    INSERT INTO orders (customer_id, total) VALUES (1, 100);
    SAVEPOINT order_created;
    
    INSERT INTO order_items (order_id, product_id) VALUES (1, 10);
    INSERT INTO order_items (order_id, product_id) VALUES (1, 20);
    SAVEPOINT items_added;
    
    -- Oops, wrong discount calculation
    UPDATE orders SET total = 80 WHERE order_id = 1;
    
    -- Undo just the update, keep the inserts
    ROLLBACK TO SAVEPOINT items_added;
    
    -- Fix and continue
    UPDATE orders SET total = 90 WHERE order_id = 1;
    
COMMIT;
```

### Transaction Use Cases

**Financial Transfers**:

```sql
BEGIN;
    -- Deduct from source
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    
    -- Add to destination
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
    
    -- Verify both accounts exist
    -- (If either update affected 0 rows, something is wrong)
COMMIT;
```

**Order Processing**:

```sql
BEGIN;
    -- Create order
    INSERT INTO orders (customer_id, order_date, status)
    VALUES (101, CURRENT_DATE, 'pending')
    RETURNING order_id INTO new_order_id;
    
    -- Add items
    INSERT INTO order_items (order_id, product_id, quantity, price)
    VALUES (new_order_id, 1001, 2, 29.99);
    
    -- Reduce inventory
    UPDATE products SET stock = stock - 2 WHERE product_id = 1001;
    
    -- Calculate total
    UPDATE orders SET total = 59.98 WHERE order_id = new_order_id;
    
COMMIT;
```

**Data Migration**:

```sql
BEGIN;
    -- Insert into new table
    INSERT INTO customers_v2 (id, name, email)
    SELECT customer_id, name, email FROM customers_v1;
    
    -- Verify row counts match
    -- SELECT COUNT(*) FROM customers_v1;
    -- SELECT COUNT(*) FROM customers_v2;
    
    -- If counts match, commit; otherwise rollback
COMMIT;
```

### Error Handling

When an error occurs in a transaction:

```sql
BEGIN;
    INSERT INTO orders (order_id, customer_id) VALUES (1, 100);
    INSERT INTO orders (order_id, customer_id) VALUES (1, 200);  -- Error! Duplicate key
    -- Transaction is now aborted
COMMIT;  -- This will fail, must ROLLBACK first

ROLLBACK;  -- Clean up the aborted transaction
```

### Nested Transactions (Savepoints)

PostgreSQL does not have true nested transactions, but savepoints provide similar functionality:

```sql
BEGIN;
    -- Outer operation
    INSERT INTO audit_log (action) VALUES ('Starting batch');
    
    SAVEPOINT batch_start;
    
    -- Try risky operation
    UPDATE accounts SET balance = balance * 1.05;  -- 5% interest
    
    -- If something goes wrong
    -- ROLLBACK TO SAVEPOINT batch_start;
    -- The audit log entry remains, but the update is undone
    
    RELEASE SAVEPOINT batch_start;  -- Merge savepoint into transaction
    
COMMIT;
```

## Code Example

Complete transaction handling:

```sql
-- Create tables for demo
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    balance DECIMAL(10, 2) CHECK (balance >= 0)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    from_account INTEGER REFERENCES accounts(account_id),
    to_account INTEGER REFERENCES accounts(account_id),
    amount DECIMAL(10, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO accounts (name, balance) VALUES 
    ('Alice', 1000.00),
    ('Bob', 500.00),
    ('Carol', 750.00);

-- Successful transfer
BEGIN;
    -- Record the transaction
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (1, 2, 100.00);
    
    -- Move the money
    UPDATE accounts SET balance = balance - 100.00 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 100.00 WHERE account_id = 2;
    
    -- Verify balances
    SELECT * FROM accounts WHERE account_id IN (1, 2);
    
COMMIT;

-- Failed transfer (insufficient funds simulation)
BEGIN;
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (2, 3, 1000.00);  -- Bob only has 600
    
    UPDATE accounts SET balance = balance - 1000.00 WHERE account_id = 2;
    -- This would violate CHECK constraint
    
ROLLBACK;  -- Nothing happened

-- Complex operation with savepoint
BEGIN;
    SAVEPOINT start_state;
    
    UPDATE accounts SET balance = balance * 1.01 WHERE balance > 500;  -- 1% bonus
    
    SAVEPOINT after_bonus;
    
    DELETE FROM accounts WHERE balance < 100;  -- Cleanup inactive
    
    -- Oops, that was wrong!
    ROLLBACK TO SAVEPOINT after_bonus;
    
    -- Continue normally
COMMIT;

-- Check final state
SELECT * FROM accounts ORDER BY account_id;
SELECT * FROM transactions ORDER BY transaction_date;
```

## Key Takeaways

- Transactions group operations into atomic units
- BEGIN starts a transaction; COMMIT saves it; ROLLBACK undoes it
- SAVEPOINT creates checkpoints for partial rollbacks
- Use transactions when multiple operations must succeed together
- Auto-commit is the default; use explicit transactions for safety

## Additional Resources

- [PostgreSQL Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [SAVEPOINT Documentation](https://www.postgresql.org/docs/current/sql-savepoint.html)
- [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
