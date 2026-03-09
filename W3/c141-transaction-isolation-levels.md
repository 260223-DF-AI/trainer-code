# Transaction Isolation Levels

## Learning Objectives

- Understand transaction isolation concepts
- Recognize read phenomena (dirty reads, phantom reads, etc.)
- Apply different isolation levels appropriately
- Balance isolation with performance

## Why This Matters

Isolation levels control how transactions interact with each other. Choosing the right level balances data consistency against concurrency. Too little isolation causes data errors; too much isolation reduces performance and may cause deadlocks. Understanding these trade-offs is essential for building reliable, performant database applications.

## The Concept

### The Isolation Problem

When multiple transactions run concurrently, they can interfere:

```
Transaction A:                    Transaction B:
READ balance = 100
                                  WRITE balance = 50
READ balance = ?                  
-- What does A see? 100 or 50?
```

### Read Phenomena

| Phenomenon | Description |
|------------|-------------|
| Dirty Read | Reading uncommitted changes from another transaction |
| Non-Repeatable Read | Reading same row twice gives different values |
| Phantom Read | Query returns different rows when run twice |

### Dirty Read Example

```
Transaction A:                    Transaction B:
                                  BEGIN
                                  UPDATE accounts SET balance = 50 WHERE id = 1
READ balance = 50 (dirty!)        
                                  ROLLBACK (balance is still 100!)
-- A has incorrect data
```

### Non-Repeatable Read Example

```
Transaction A (long running):     Transaction B:
BEGIN
SELECT balance WHERE id = 1
-- Returns 100
                                  BEGIN
                                  UPDATE balance = 50 WHERE id = 1
                                  COMMIT
SELECT balance WHERE id = 1
-- Returns 50 (different!)
```

### Phantom Read Example

```
Transaction A:                    Transaction B:
BEGIN
SELECT * FROM products WHERE price < 100
-- Returns 10 rows
                                  BEGIN
                                  INSERT INTO products (price) VALUES (50)
                                  COMMIT
SELECT * FROM products WHERE price < 100
-- Returns 11 rows (phantom!)
```

### Isolation Levels

| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|------------|----------------|---------|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | Prevented | Possible | Possible |
| REPEATABLE READ | Prevented | Prevented | Possible* |
| SERIALIZABLE | Prevented | Prevented | Prevented |

*PostgreSQL's REPEATABLE READ actually prevents phantom reads too.

### Setting Isolation Level

```sql
-- For a single transaction
BEGIN ISOLATION LEVEL SERIALIZABLE;
    -- statements
COMMIT;

-- Or using SET
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    -- statements
COMMIT;
```

### READ COMMITTED (Default)

Each statement sees only committed data:

```sql
-- Transaction A
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- 100
-- Meanwhile B commits: balance = 50
SELECT balance FROM accounts WHERE id = 1;  -- 50 (changed!)
COMMIT;
```

### REPEATABLE READ

Sees consistent snapshot from start of transaction:

```sql
-- Transaction A
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;  -- 100
-- Meanwhile B commits: balance = 50
SELECT balance FROM accounts WHERE id = 1;  -- Still 100!
COMMIT;
```

### SERIALIZABLE

Strictest level; transactions appear to run sequentially:

```sql
-- Prevents all anomalies
BEGIN ISOLATION LEVEL SERIALIZABLE;
    -- If conflict detected, transaction fails
    -- Must be retried
COMMIT;
```

### When Serializable Fails

```sql
-- Transaction A                  -- Transaction B
BEGIN ISOLATION LEVEL             BEGIN ISOLATION LEVEL
SERIALIZABLE;                     SERIALIZABLE;
SELECT * FROM counters;           SELECT * FROM counters;
UPDATE counters                   UPDATE counters
SET value = value + 1;            SET value = value + 1;
COMMIT;                           -- ERROR: could not serialize
                                  -- due to concurrent update
```

### Choosing an Isolation Level

| Use Case | Recommended Level |
|----------|-------------------|
| Simple reads | READ COMMITTED |
| Reports needing consistency | REPEATABLE READ |
| Financial transactions | SERIALIZABLE |
| High-traffic, simple operations | READ COMMITTED |

### Locking Considerations

Higher isolation may cause more locking:

```sql
-- Explicit locking when needed
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- Locks the row until transaction ends
```

## Code Example

Demonstrating isolation levels:

```sql
-- Setup for demonstration
CREATE TABLE accounts_demo (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    balance DECIMAL(10, 2)
);

INSERT INTO accounts_demo (name, balance) VALUES ('Alice', 100);

-- READ COMMITTED behavior
-- Session 1:
BEGIN;
UPDATE accounts_demo SET balance = 200 WHERE id = 1;
-- Don't commit yet

-- Session 2 (separate connection):
BEGIN;
SELECT balance FROM accounts_demo WHERE id = 1;
-- Returns 100 (can't see uncommitted change)

-- Session 1:
COMMIT;

-- Session 2:
SELECT balance FROM accounts_demo WHERE id = 1;
-- Now returns 200

COMMIT;

-- REPEATABLE READ demonstration
TRUNCATE accounts_demo;
INSERT INTO accounts_demo (name, balance) VALUES ('Alice', 100);

-- Session 1:
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts_demo WHERE id = 1;
-- Returns 100

-- Session 2:
BEGIN;
UPDATE accounts_demo SET balance = 200 WHERE id = 1;
COMMIT;

-- Session 1:
SELECT balance FROM accounts_demo WHERE id = 1;
-- Still returns 100 (snapshot from transaction start)
COMMIT;

-- After commit, new transaction sees 200
SELECT balance FROM accounts_demo WHERE id = 1;
-- Returns 200

-- Serializable conflict example
TRUNCATE accounts_demo;
INSERT INTO accounts_demo (id, name, balance) VALUES (1, 'Counter', 0);

-- This pattern would fail if both run simultaneously at SERIALIZABLE:
-- Both try to increment based on what they read

-- Session 1:
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT balance FROM accounts_demo WHERE id = 1;  -- 0
UPDATE accounts_demo SET balance = 1 WHERE id = 1;
-- Don't commit yet

-- Session 2:
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT balance FROM accounts_demo WHERE id = 1;  -- Also 0
UPDATE accounts_demo SET balance = 1 WHERE id = 1;
-- Blocks waiting for Session 1

-- Session 1:
COMMIT;

-- Session 2:
-- ERROR: could not serialize access due to concurrent update
-- Should retry the transaction

-- Check current isolation level
SHOW transaction_isolation;

-- List running transactions
SELECT pid, state, query FROM pg_stat_activity WHERE state != 'idle';
```

## Key Takeaways

- Isolation levels control transaction interaction
- READ COMMITTED (default) sees only committed data per statement
- REPEATABLE READ sees consistent snapshot for entire transaction
- SERIALIZABLE prevents all anomalies but may fail on conflict
- Higher isolation = more consistency but less concurrency
- Failed SERIALIZABLE transactions should be retried

## Additional Resources

- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html)
- [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
