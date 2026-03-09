# Savepoint

## Learning Objectives

- Understand savepoints as transaction checkpoints
- Create, rollback to, and release savepoints
- Apply savepoints for complex transaction workflows
- Implement error recovery patterns using savepoints

## Why This Matters

Savepoints provide fine-grained control within transactions. When a complex transaction involves multiple steps, a single failure doesn't have to undo everything. Savepoints let you retry failed operations, handle partial failures gracefully, and build robust error handling into your database operations.

## The Concept

### What is a Savepoint?

A savepoint is a named marker within a transaction that allows you to:

- Roll back to that point without aborting the entire transaction
- Create multiple checkpoints throughout a transaction
- Recover from errors without losing all work

```
BEGIN;                          COMMIT;
  |                               |
  v                               v
  +------+-------+-------+--------+
  |  A   |   B   |   C   |   D    |
  +------+-------+-------+--------+
         ^       ^
         |       |
      SAVEPOINT SAVEPOINT
        sp1       sp2
```

### Creating Savepoints

```sql
BEGIN;
    -- Some operations
    INSERT INTO logs (message) VALUES ('Step 1 complete');
    
    -- Create a savepoint
    SAVEPOINT step1_done;
    
    -- More operations
    UPDATE data SET status = 'processing';
    
    -- Another savepoint
    SAVEPOINT step2_done;
    
    -- Continue...
COMMIT;
```

### Rolling Back to Savepoints

```sql
BEGIN;
    INSERT INTO orders (customer_id) VALUES (100);
    SAVEPOINT order_created;
    
    INSERT INTO order_items (order_id, product_id, qty) VALUES (1, 50, 2);
    SAVEPOINT items_added;
    
    INSERT INTO payments (order_id, amount) VALUES (1, 99.99);
    -- Oops, payment system is down!
    
    ROLLBACK TO SAVEPOINT items_added;
    -- Payment undone, but order and items remain
    
    UPDATE orders SET status = 'pending_payment' WHERE order_id = 1;
COMMIT;
```

### Releasing Savepoints

Releasing removes a savepoint without rolling back:

```sql
BEGIN;
    INSERT INTO data (value) VALUES ('A');
    SAVEPOINT sp1;
    
    INSERT INTO data (value) VALUES ('B');
    SAVEPOINT sp2;
    
    -- If we're sure sp1 is no longer needed:
    RELEASE SAVEPOINT sp1;
    -- sp1 is gone, can't roll back to it anymore
    
    -- sp2 still exists
    ROLLBACK TO SAVEPOINT sp2;  -- This works
COMMIT;
```

### Nested Savepoints

Savepoints can be nested within a transaction:

```sql
BEGIN;
    SAVEPOINT outer;
    INSERT INTO t VALUES (1);
    
        SAVEPOINT inner;
        INSERT INTO t VALUES (2);
        
        -- Roll back just the inner work
        ROLLBACK TO SAVEPOINT inner;
    
    -- Value 1 is still staged
    
    INSERT INTO t VALUES (3);
COMMIT;
-- Table contains: 1, 3 (not 2)
```

### Error Recovery Pattern

```sql
BEGIN;
    -- Main operation
    INSERT INTO customers (name, email) VALUES ('Alice', 'alice@email.com');
    SAVEPOINT customer_created;
    
    -- Try to create account
    BEGIN
        INSERT INTO accounts (customer_id, type) VALUES (1, 'premium');
    EXCEPTION WHEN unique_violation THEN
        ROLLBACK TO SAVEPOINT customer_created;
        INSERT INTO accounts (customer_id, type) VALUES (1, 'standard');
    END;
COMMIT;
```

### Retry Pattern with Savepoints

```sql
BEGIN;
    SAVEPOINT before_api_call;
    
    -- Attempt 1
    INSERT INTO external_sync (data, status) VALUES ('payload', 'pending');
    -- Simulate API failure...
    
    ROLLBACK TO SAVEPOINT before_api_call;
    
    -- Attempt 2 with different approach
    INSERT INTO external_sync (data, status, retry_count) 
    VALUES ('payload', 'queued', 1);
COMMIT;
```

### Savepoints After Errors

After a PostgreSQL error, you must rollback to a savepoint to continue:

```sql
BEGIN;
    INSERT INTO users (id, name) VALUES (1, 'Alice');
    SAVEPOINT sp1;
    
    INSERT INTO users (id, name) VALUES (1, 'Bob');  -- Error: duplicate key
    -- Transaction is now in "aborted" state
    
    -- This would fail:
    -- INSERT INTO users (id, name) VALUES (2, 'Carol');
    
    -- Must rollback to savepoint first:
    ROLLBACK TO SAVEPOINT sp1;
    
    -- Now we can continue:
    INSERT INTO users (id, name) VALUES (2, 'Carol');
COMMIT;
-- Alice and Carol exist, Bob does not
```

### Complete Example

```sql
-- Order processing with multiple potential failure points
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER,
    quantity INTEGER
);

CREATE TABLE inventory (
    product_id INTEGER PRIMARY KEY,
    stock INTEGER CHECK (stock >= 0)
);

INSERT INTO inventory VALUES (1, 10), (2, 5), (3, 0);

-- Complex order with savepoints
BEGIN;
    -- Create order
    INSERT INTO orders (customer_id) VALUES (100);
    SAVEPOINT order_created;
    
    -- Add first item
    INSERT INTO order_items (order_id, product_id, quantity) 
    VALUES (1, 1, 2);
    UPDATE inventory SET stock = stock - 2 WHERE product_id = 1;
    SAVEPOINT item1_added;
    
    -- Add second item (might fail)
    INSERT INTO order_items (order_id, product_id, quantity) 
    VALUES (1, 3, 1);
    UPDATE inventory SET stock = stock - 1 WHERE product_id = 3;
    -- Error: stock would be -1
    
    -- Roll back just the second item
    ROLLBACK TO SAVEPOINT item1_added;
    
    -- Mark order as partial
    UPDATE orders SET status = 'partial' WHERE order_id = 1;
    
COMMIT;

-- Verify
SELECT * FROM orders;       -- Order exists with status 'partial'
SELECT * FROM order_items;  -- Only item 1 exists  
SELECT * FROM inventory;    -- Product 1 stock reduced, product 3 unchanged
```

## Key Takeaways

- SAVEPOINT creates a checkpoint within a transaction
- ROLLBACK TO SAVEPOINT undoes work back to that point
- RELEASE SAVEPOINT removes a savepoint
- Savepoints allow partial rollback without aborting transactions
- After an error, rollback to a savepoint to continue
- Use savepoints for complex operations with multiple failure points

## Additional Resources

- [PostgreSQL SAVEPOINT](https://www.postgresql.org/docs/current/sql-savepoint.html)
- [ROLLBACK TO SAVEPOINT](https://www.postgresql.org/docs/current/sql-rollback-to.html)
- [RELEASE SAVEPOINT](https://www.postgresql.org/docs/current/sql-release-savepoint.html)
