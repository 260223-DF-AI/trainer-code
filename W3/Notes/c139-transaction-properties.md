# Transaction Properties

## Learning Objectives

- Understand the lifecycle of a database transaction
- Identify transaction states and transitions
- Apply transaction management techniques
- Recognize implicit vs explicit transactions

## Why This Matters

Transactions are the building blocks of reliable database operations. Understanding how transactions work - their states, behaviors, and lifecycle - helps you write applications that maintain data integrity even during failures. This knowledge is essential for debugging transaction-related issues and designing robust database interactions.

## The Concept

### What is a Transaction?

A transaction is a logical unit of work containing one or more database operations that must be treated as a single, indivisible action.

```
Transaction = [ Operation 1 + Operation 2 + ... + Operation N ]
                              ↓
              Either ALL succeed or ALL fail
```

### Transaction Lifecycle

A transaction goes through several states during its lifetime:

```
       +--------+
       | BEGIN  |
       +--------+
            |
            v
    +---------------+
    |    ACTIVE     |<--+
    +---------------+   |
            |           | (more operations)
            v           |
    +---------------+   |
    | Operations... |---+
    +---------------+
            |
    +-------+-------+
    |               |
    v               v
+--------+    +-----------+
| COMMIT |    | ROLLBACK  |
+--------+    +-----------+
    |               |
    v               v
+--------+    +-----------+
|COMMITTED|   | ABORTED   |
+--------+    +-----------+
```

### Transaction States

| State | Description |
|-------|-------------|
| Active | Transaction is executing |
| Partially Committed | Final operation done, awaiting commit |
| Committed | Successfully completed and saved |
| Failed | Error occurred during execution |
| Aborted | Rolled back due to failure |

### Implicit vs Explicit Transactions

**Implicit (Autocommit)**

By default, PostgreSQL commits each statement automatically:

```sql
-- Each statement is its own transaction
INSERT INTO users (name) VALUES ('Alice');  -- Committed immediately
INSERT INTO users (name) VALUES ('Bob');    -- Committed immediately
-- If second fails, first is already saved
```

**Explicit Transactions**

Group multiple statements into one transaction:

```sql
BEGIN;
    INSERT INTO users (name) VALUES ('Alice');
    INSERT INTO users (name) VALUES ('Bob');
    -- Both are uncommitted and invisible to others
COMMIT;
-- Now both are saved together
```

### Transaction Boundaries

```sql
-- BEGIN starts a transaction
BEGIN;
-- or
BEGIN TRANSACTION;
-- or
START TRANSACTION;

-- COMMIT ends and saves
COMMIT;
-- or
COMMIT TRANSACTION;

-- ROLLBACK ends and discards
ROLLBACK;
-- or
ROLLBACK TRANSACTION;
```

### Transaction Behavior

**Changes are Invisible Until Commit**

```sql
-- Session 1                    -- Session 2
BEGIN;
INSERT INTO data VALUES (1);
                                SELECT * FROM data;
                                -- Does NOT see the new row
COMMIT;
                                SELECT * FROM data;
                                -- Now sees the row
```

**Errors Abort the Transaction**

```sql
BEGIN;
    INSERT INTO users (id, name) VALUES (1, 'Alice');
    INSERT INTO users (id, name) VALUES (1, 'Bob');  -- Error: duplicate key
    -- Transaction is now in aborted state
COMMIT;  -- This actually does a ROLLBACK because transaction failed
```

### Read-Only Transactions

```sql
-- Declare a read-only transaction
BEGIN READ ONLY;
    SELECT * FROM sensitive_data;
    -- INSERT, UPDATE, DELETE would fail
COMMIT;

-- Useful for:
-- - Consistent snapshots for reporting
-- - Preventing accidental modifications
-- - Performance optimization
```

### Deferrable Transactions

```sql
-- For long-running read-only queries
BEGIN READ ONLY DEFERRABLE;
    -- May wait for a clean snapshot
    -- Then runs without blocking or being blocked
    SELECT * FROM large_table;
COMMIT;
```

### Nested Operations (Savepoints)

While PostgreSQL doesn't support true nested transactions, savepoints provide similar functionality:

```sql
BEGIN;
    INSERT INTO orders (id) VALUES (1);
    
    SAVEPOINT before_items;
    INSERT INTO order_items (order_id, item) VALUES (1, 'A');
    
    -- Oops, wrong item
    ROLLBACK TO SAVEPOINT before_items;
    
    INSERT INTO order_items (order_id, item) VALUES (1, 'B');
COMMIT;
-- Order exists with item 'B', not 'A'
```

### Complete Example

```sql
-- Demo transaction properties
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10,2) CHECK (balance >= 0)
);

CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Successful transaction
BEGIN;
    INSERT INTO accounts (name, balance) VALUES ('Alice', 1000);
    INSERT INTO audit_log (action) VALUES ('Created Alice account');
COMMIT;
-- Both committed

-- Failed transaction (rolled back)
BEGIN;
    UPDATE accounts SET balance = balance - 2000 WHERE name = 'Alice';
    -- Error: violates CHECK constraint (balance would be -1000)
    INSERT INTO audit_log (action) VALUES ('Withdrew from Alice');
ROLLBACK;
-- Neither operation happened

-- Verify
SELECT * FROM accounts;      -- Alice still has 1000
SELECT * FROM audit_log;     -- Only creation log exists

-- Read-only example
BEGIN READ ONLY;
    SELECT name, balance FROM accounts;
    -- UPDATE accounts SET balance = 0;  -- Would fail
COMMIT;
```

## Key Takeaways

- Transactions group operations into atomic units
- BEGIN/START TRANSACTION opens a transaction
- COMMIT saves changes; ROLLBACK discards them
- By default, PostgreSQL auto-commits each statement
- Errors during a transaction cause automatic rollback
- READ ONLY transactions prevent modifications
- Savepoints allow partial rollback within a transaction

## Additional Resources

- [PostgreSQL Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [BEGIN Documentation](https://www.postgresql.org/docs/current/sql-begin.html)
- [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
