# ACID Properties

## Learning Objectives

- Understand the four ACID properties of database transactions
- Explain how each property ensures data integrity
- Recognize ACID violations and their consequences
- Apply ACID concepts to database design decisions

## Why This Matters

ACID properties are the foundation of reliable database systems. They guarantee that transactions are processed reliably, even when systems crash, power fails, or multiple users access data simultaneously. Understanding ACID helps you design systems that maintain data integrity under any circumstances - critical for financial systems, e-commerce, healthcare, and any application where data accuracy matters.

## The Concept

### What is ACID?

ACID is an acronym for four properties that guarantee reliable transaction processing:

| Property | Meaning | Ensures |
|----------|---------|---------|
| **A**tomicity | All or nothing | Complete transactions only |
| **C**onsistency | Valid states only | Data integrity maintained |
| **I**solation | No interference | Concurrent safety |
| **D**urability | Permanent changes | Survives failures |

### Atomicity - All or Nothing

A transaction is atomic: either ALL operations succeed, or NONE do. There's no partial completion.

```sql
-- Bank transfer example
BEGIN;
    UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;
-- Either BOTH updates happen or NEITHER does
```

**Without Atomicity**: If the system crashed after the first UPDATE, money would disappear - debited from one account but never credited to another.

```
Atomic Transaction:
+------------------+     +------------------+
| Debit Account 1  | --> | Credit Account 2 |
+------------------+     +------------------+
         |                       |
         +-----------+-----------+
                     |
              [Both or Neither]
```

### Consistency - Valid States Only

A transaction transforms the database from one valid state to another. All rules (constraints, triggers, cascades) are enforced.

```sql
-- Consistency enforced by constraints
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    balance DECIMAL(10,2) CHECK (balance >= 0)  -- No negative balances
);

BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
    -- If this would make balance negative, the entire transaction fails
COMMIT;
```

**Without Consistency**: Business rules could be violated - negative balances, orphaned records, invalid data states.

### Isolation - No Interference

Concurrent transactions don't see each other's uncommitted changes. Each transaction appears to run alone.

```sql
-- Transaction A                  -- Transaction B
BEGIN;                            BEGIN;
SELECT balance FROM accounts      SELECT balance FROM accounts
WHERE account_id = 1;             WHERE account_id = 1;
-- Returns 1000                   -- Also returns 1000

UPDATE accounts                   
SET balance = 500                 
WHERE account_id = 1;             

                                  -- B still sees 1000 (isolation)
                                  
COMMIT;
                                  -- Now B would see 500 on next read
                                  COMMIT;
```

**Without Isolation**: Transactions could read partial updates, leading to incorrect calculations and data corruption.

### Durability - Permanent Changes

Once a transaction commits, the changes survive any subsequent failure - power outage, crash, hardware failure.

```sql
BEGIN;
    INSERT INTO important_records (data) VALUES ('Critical Data');
COMMIT;
-- At this point, even if the server crashes immediately,
-- 'Critical Data' will be there when system recovers
```

**How it works**: Database writes to transaction logs before confirming commit. On recovery, logs are replayed to restore committed transactions.

### ACID in Practice

```sql
-- Complete ACID example: Order processing
CREATE TABLE inventory (
    product_id INTEGER PRIMARY KEY,
    quantity INTEGER CHECK (quantity >= 0)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES inventory(product_id),
    quantity INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Atomic, Consistent order placement
BEGIN;
    -- Reserve inventory
    UPDATE inventory 
    SET quantity = quantity - 5 
    WHERE product_id = 101;
    
    -- Create order
    INSERT INTO orders (product_id, quantity, status)
    VALUES (101, 5, 'confirmed');
    
    -- If inventory check fails (quantity would go negative),
    -- the entire transaction rolls back
COMMIT;
-- Durable: Once committed, this order exists permanently
-- Isolated: Other transactions don't see this until commit
```

### ACID Violations and Their Consequences

| Violation | Consequence |
|-----------|-------------|
| No Atomicity | Partial operations, inconsistent state |
| No Consistency | Invalid data, broken business rules |
| No Isolation | Race conditions, phantom reads, lost updates |
| No Durability | Data loss on failure |

### When ACID Matters Most

- **Financial transactions** - Money transfers must be atomic
- **Inventory systems** - Stock counts must stay consistent
- **Booking systems** - Can't double-book resources
- **Healthcare records** - Patient data must be accurate and durable
- **E-commerce** - Orders and payments must match

### Trade-offs

Some systems sacrifice ACID for performance (NoSQL databases often use "eventual consistency"). PostgreSQL is fully ACID-compliant, making it ideal for applications where data integrity is paramount.

## Key Takeaways

- **Atomicity**: Transactions are all-or-nothing
- **Consistency**: Database moves only between valid states
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes are permanent
- ACID guarantees are essential for reliable data systems
- PostgreSQL is fully ACID-compliant

## Additional Resources

- [PostgreSQL Reliability](https://www.postgresql.org/docs/current/wal-reliability.html)
- [Transaction Processing](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [ACID Properties Explained](https://www.ibm.com/docs/en/cics-ts/5.4?topic=processing-acid-properties-transactions)
