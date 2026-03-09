# Atomicity

## Learning Objectives

- Understand atomicity as an ACID property
- Recognize how atomicity prevents partial updates
- Apply transactions to ensure atomic operations
- Identify scenarios requiring atomicity

## Why This Matters

Atomicity guarantees that database operations are "all or nothing." Either every operation in a transaction completes successfully, or none of them take effect. This is critical for operations like financial transfers, order processing, and any multi-step database changes where partial completion would corrupt data.

## The Concept

### What is Atomicity?

**Atomicity** is the first property of ACID (Atomicity, Consistency, Isolation, Durability). It ensures that:

- A transaction is an indivisible unit of work
- All operations within the transaction succeed OR all fail
- There is no "in-between" state visible to other transactions

### The Atomicity Problem

Without atomicity, partial failures cause data corruption:

```
Bank Transfer: Move $100 from Account A to Account B

Without Atomicity:
1. Deduct $100 from Account A  [SUCCESS]
2. ** SYSTEM CRASH **
3. Add $100 to Account B       [NEVER HAPPENS]

Result: $100 has vanished!

With Atomicity:
1. BEGIN TRANSACTION
2. Deduct $100 from Account A  [SUCCESS]
3. ** SYSTEM CRASH **
4. ROLLBACK (automatic)        [Account A restored]

Result: No money lost, system recovers
```

### Transaction Boundaries

Atomicity is achieved through explicit transactions:

```sql
-- Define atomic boundary
BEGIN;
    -- All operations inside are treated as one unit
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    INSERT INTO transfers (from_id, to_id, amount) VALUES (1, 2, 100);
COMMIT;  -- All succeed together

-- Or on failure:
ROLLBACK;  -- All are undone together
```

### Automatic Atomicity

Individual SQL statements are atomic by default:

```sql
-- This single UPDATE is atomic
UPDATE employees SET salary = salary * 1.05;
-- Either ALL employees get raise or NONE do

-- Multiple rows are affected atomically
DELETE FROM orders WHERE status = 'cancelled';
-- Either ALL cancelled orders deleted or NONE
```

### When Atomicity Matters

**Financial Transactions**:

```sql
BEGIN;
    -- Withdraw from one account
    UPDATE accounts SET balance = balance - 500 WHERE id = 1;
    -- Deposit to another
    UPDATE accounts SET balance = balance + 500 WHERE id = 2;
    -- Record the transaction
    INSERT INTO transaction_log (from_id, to_id, amount) VALUES (1, 2, 500);
COMMIT;
```

**Order Processing**:

```sql
BEGIN;
    -- Create order
    INSERT INTO orders (customer_id, total) VALUES (101, 150.00);
    -- Add line items
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 10, 2);
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 20, 1);
    -- Decrease inventory
    UPDATE products SET stock = stock - 2 WHERE product_id = 10;
    UPDATE products SET stock = stock - 1 WHERE product_id = 20;
COMMIT;
```

**User Registration**:

```sql
BEGIN;
    -- Create user account
    INSERT INTO users (email, password_hash) VALUES ('new@email.com', 'hash123');
    -- Create user profile
    INSERT INTO profiles (user_id, display_name) VALUES (LASTVAL(), 'New User');
    -- Create default settings
    INSERT INTO user_settings (user_id, theme) VALUES (LASTVAL(), 'light');
COMMIT;
```

### Handling Failures

Use error handling to ensure rollback on failure:

```sql
BEGIN;
    -- Attempt operations
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    
    -- Check for issues (e.g., insufficient funds check done earlier)
    -- If problem detected:
    -- ROLLBACK;
    
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### Savepoints for Partial Atomicity

Savepoints allow partial rollback within an atomic transaction:

```sql
BEGIN;
    INSERT INTO orders (customer_id) VALUES (1);
    SAVEPOINT after_order;
    
    -- Try to add premium shipping
    INSERT INTO shipping (order_id, type) VALUES (1, 'express');
    -- If unavailable in their region:
    ROLLBACK TO SAVEPOINT after_order;
    
    -- Fall back to standard shipping
    INSERT INTO shipping (order_id, type) VALUES (1, 'standard');
COMMIT;
-- The order is created either way
```

### Nested Operations

Nested operations participate in the outer transaction's atomicity:

```sql
BEGIN;
    INSERT INTO invoices (customer_id, amount) VALUES (1, 500);
    
    -- This function might do multiple inserts
    -- All become part of current transaction
    SELECT create_line_items(1, 'PROD-001', 5);
    SELECT create_line_items(1, 'PROD-002', 3);
    
    -- If ANY operation fails, ALL are rolled back
COMMIT;
```

## Code Example

Demonstrating atomicity:

```sql
-- Create test tables
CREATE TABLE bank_accounts (
    account_id SERIAL PRIMARY KEY,
    account_holder VARCHAR(100),
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)
);

CREATE TABLE transfers (
    transfer_id SERIAL PRIMARY KEY,
    from_account INTEGER REFERENCES bank_accounts(account_id),
    to_account INTEGER REFERENCES bank_accounts(account_id),
    amount DECIMAL(10, 2) NOT NULL,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO bank_accounts (account_holder, balance) VALUES 
    ('Alice', 1000.00),
    ('Bob', 500.00);

SELECT * FROM bank_accounts;

-- Atomic transfer (succeeds)
BEGIN;
    UPDATE bank_accounts SET balance = balance - 100 WHERE account_id = 1;
    UPDATE bank_accounts SET balance = balance + 100 WHERE account_id = 2;
    INSERT INTO transfers (from_account, to_account, amount) VALUES (1, 2, 100);
COMMIT;

SELECT * FROM bank_accounts;
-- Alice: 900, Bob: 600

-- Atomic transfer (fails - insufficient funds would be caught by CHECK)
BEGIN;
    UPDATE bank_accounts SET balance = balance - 2000 WHERE account_id = 1;
    -- This will fail due to CHECK constraint
COMMIT;
-- ERROR: new row violates check constraint

-- Account balances unchanged because transaction rolled back
SELECT * FROM bank_accounts;
-- Alice: 900, Bob: 600 (no change)

-- Manual rollback example
BEGIN;
    UPDATE bank_accounts SET balance = balance - 50 WHERE account_id = 1;
    -- Check balance (hypothetically)
    -- Something is wrong, abort:
ROLLBACK;

SELECT * FROM bank_accounts;
-- Alice: 900, Bob: 600 (no change)

-- View transfer history
SELECT 
    t.transfer_id,
    a1.account_holder AS from_account,
    a2.account_holder AS to_account,
    t.amount,
    t.transfer_date
FROM transfers t
JOIN bank_accounts a1 ON t.from_account = a1.account_id
JOIN bank_accounts a2 ON t.to_account = a2.account_id;
```

## Key Takeaways

- Atomicity means all-or-nothing execution of transactions
- BEGIN...COMMIT wraps multiple statements in one atomic unit
- Failures automatically rollback all changes in the transaction
- Individual SQL statements are atomic by themselves
- Use savepoints for partial rollback within a transaction

## Additional Resources

- [PostgreSQL Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [ACID Properties](https://en.wikipedia.org/wiki/ACID)
- [Transaction Management](https://www.postgresql.org/docs/current/mvcc.html)
