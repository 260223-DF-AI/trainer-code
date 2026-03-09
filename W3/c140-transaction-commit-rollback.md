# Transaction Commit and Rollback

## Learning Objectives

- Master COMMIT to save transaction changes permanently
- Use ROLLBACK to undo transaction changes
- Apply SAVEPOINT for partial rollback within transactions
- Implement error handling with proper transaction control

## Why This Matters

COMMIT and ROLLBACK are your tools for controlling transaction outcomes. COMMIT makes changes permanent and visible; ROLLBACK lets you undo mistakes. Understanding these commands is essential for maintaining data integrity, especially when operations fail partway through. Proper use of these commands prevents data corruption and enables graceful error recovery.

## The Concept

### COMMIT - Save Changes

COMMIT ends a transaction successfully, making all changes permanent and visible to other sessions.

```sql
BEGIN;
    INSERT INTO products (name, price) VALUES ('Laptop', 999);
    UPDATE inventory SET stock = stock + 10 WHERE product_id = 1;
COMMIT;
-- Both changes are now permanent
```

After COMMIT:

- Changes are persisted to disk
- Changes become visible to other transactions
- Locks are released
- Transaction cannot be undone

### ROLLBACK - Undo Changes

ROLLBACK ends a transaction by discarding all changes made since BEGIN.

```sql
BEGIN;
    DELETE FROM products WHERE category = 'Electronics';
    -- Oops! That was a mistake!
ROLLBACK;
-- No products were deleted
```

After ROLLBACK:

- All changes since BEGIN are discarded
- Database returns to state before BEGIN
- Locks are released
- As if the transaction never happened

### When to Use Each

**Use COMMIT when:**

- All operations succeeded
- Data is in a valid state
- You want changes to persist

**Use ROLLBACK when:**

- An error occurred
- Business validation failed
- You changed your mind
- Testing/debugging queries

### SAVEPOINT - Partial Rollback

SAVEPOINT creates checkpoints within a transaction for granular control.

```sql
BEGIN;
    INSERT INTO orders (customer_id) VALUES (1);
    SAVEPOINT order_created;
    
    INSERT INTO order_items (order_id, product_id) VALUES (1, 999);
    -- Error: product 999 doesn't exist!
    ROLLBACK TO SAVEPOINT order_created;
    
    INSERT INTO order_items (order_id, product_id) VALUES (1, 100);
COMMIT;
-- Order exists with product 100, not 999
```

### SAVEPOINT Commands

```sql
-- Create a savepoint
SAVEPOINT savepoint_name;

-- Roll back to a savepoint
ROLLBACK TO SAVEPOINT savepoint_name;

-- Release (delete) a savepoint
RELEASE SAVEPOINT savepoint_name;
```

### Error Handling Pattern

```sql
BEGIN;
    -- Attempt risky operation
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    
    -- Check if something went wrong
    -- In application code, you'd check for errors here
    
    -- If error:
    -- ROLLBACK;
    
    -- If success:
    COMMIT;
```

### Multiple Savepoints

```sql
BEGIN;
    INSERT INTO log (message) VALUES ('Starting process');
    SAVEPOINT step1;
    
    UPDATE data SET status = 'processing' WHERE id = 1;
    SAVEPOINT step2;
    
    INSERT INTO results (data_id, result) VALUES (1, 'success');
    SAVEPOINT step3;
    
    -- Roll back to any savepoint
    ROLLBACK TO SAVEPOINT step2;  -- Undo only the INSERT
    
    INSERT INTO results (data_id, result) VALUES (1, 'retry');
COMMIT;
```

### Transaction in Error State

When an error occurs in PostgreSQL, the transaction enters a failed state:

```sql
BEGIN;
    INSERT INTO users (id, name) VALUES (1, 'Alice');
    INSERT INTO users (id, name) VALUES (1, 'Bob');  -- Error: duplicate key
    
    -- Transaction is now in "aborted" state
    SELECT * FROM users;  -- Error: current transaction is aborted
    
    -- Only ROLLBACK works now
ROLLBACK;

-- Or use savepoints to recover
BEGIN;
    SAVEPOINT before_bob;
    INSERT INTO users (id, name) VALUES (1, 'Alice');
    
    SAVEPOINT before_duplicate;
    INSERT INTO users (id, name) VALUES (1, 'Bob');  -- Error
    
    ROLLBACK TO SAVEPOINT before_duplicate;
    -- Transaction is usable again
    
    INSERT INTO users (id, name) VALUES (2, 'Bob');
COMMIT;
```

### Complete Example

```sql
-- Setup
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10,2) CHECK (balance >= 0)
);

INSERT INTO accounts (name, balance) VALUES 
    ('Alice', 1000),
    ('Bob', 500);

-- Successful transfer
BEGIN;
    UPDATE accounts SET balance = balance - 200 WHERE name = 'Alice';
    UPDATE accounts SET balance = balance + 200 WHERE name = 'Bob';
COMMIT;
-- Alice: 800, Bob: 700

-- Failed transfer (insufficient funds)
BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE name = 'Alice';
    -- Error: new balance would be -200, violates CHECK
ROLLBACK;
-- Alice still has 800

-- Transfer with savepoint for audit
BEGIN;
    SAVEPOINT before_transfer;
    
    UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
    UPDATE accounts SET balance = balance + 100 WHERE name = 'Carol';  
    -- Carol doesn't exist, but no error (0 rows affected)
    
    -- Application detects no rows updated for Carol
    ROLLBACK TO SAVEPOINT before_transfer;
    
    -- Log the failed attempt
    INSERT INTO failed_transfers (from_account, to_account, amount, reason)
    VALUES ('Alice', 'Carol', 100, 'Recipient not found');
COMMIT;

-- Verify
SELECT * FROM accounts;
SELECT * FROM failed_transfers;
```

## Key Takeaways

- COMMIT makes transaction changes permanent
- ROLLBACK discards all changes since BEGIN
- SAVEPOINT allows partial rollback within a transaction
- After an error, only ROLLBACK works (unless using savepoints)
- Use transactions to group related operations
- Test with SELECT before committing destructive changes

## Additional Resources

- [PostgreSQL COMMIT](https://www.postgresql.org/docs/current/sql-commit.html)
- [PostgreSQL ROLLBACK](https://www.postgresql.org/docs/current/sql-rollback.html)
- [PostgreSQL SAVEPOINT](https://www.postgresql.org/docs/current/sql-savepoint.html)
