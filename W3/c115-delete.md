# DELETE Statement

## Learning Objectives

- Master DELETE syntax for removing data from tables
- Apply WHERE clauses to target specific rows
- Understand DELETE with JOINs and subqueries
- Compare DELETE vs TRUNCATE and implement soft deletes

## Why This Matters

Removing data is as important as adding it. Whether cleaning up old records, removing duplicate entries, or processing user deletion requests, DELETE is essential. However, it's also dangerous - a missing WHERE clause can wipe out your entire table. Understanding DELETE thoroughly helps you remove exactly what you intend, nothing more.

## The Concept

### Basic DELETE Syntax

```sql
DELETE FROM table_name
WHERE condition;
```

**Critical: Always include a WHERE clause** unless you truly want to delete all rows.

### Simple DELETE

```sql
-- Delete a specific row
DELETE FROM employees
WHERE employee_id = 42;

-- Delete rows matching a condition
DELETE FROM orders
WHERE status = 'cancelled';

-- Delete with multiple conditions
DELETE FROM products
WHERE category = 'Discontinued' AND stock = 0;
```

### DELETE Without WHERE (Dangerous!)

```sql
-- This deletes EVERY row in the table!
DELETE FROM temp_data;

-- The table structure remains, but all data is gone
```

### DELETE with Multiple Conditions

```sql
-- Using AND
DELETE FROM logs
WHERE log_date < '2023-01-01' AND level = 'DEBUG';

-- Using OR
DELETE FROM notifications
WHERE is_read = TRUE OR created_at < NOW() - INTERVAL '30 days';

-- Using IN
DELETE FROM users
WHERE status IN ('deleted', 'banned', 'inactive');

-- Using NOT IN
DELETE FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);
```

### DELETE with RETURNING

Get back the deleted rows:

```sql
-- Return deleted row IDs
DELETE FROM expired_sessions
WHERE expiry < NOW()
RETURNING session_id;

-- Return all deleted data
DELETE FROM old_orders
WHERE order_date < '2022-01-01'
RETURNING *;

-- Use RETURNING for audit logging
DELETE FROM sensitive_data
WHERE id = 1
RETURNING id, created_at, deleted_by;
```

### DELETE with Subquery

Delete based on a query result:

```sql
-- Delete orders from inactive customers
DELETE FROM orders
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE is_active = FALSE
);

-- Delete products not ordered in the last year
DELETE FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date > NOW() - INTERVAL '1 year'
);
```

### DELETE with USING (Join Delete)

Delete using data from another table:

```sql
-- PostgreSQL syntax for join delete
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.order_id
  AND o.status = 'cancelled';

-- Delete with multiple table conditions
DELETE FROM employees e
USING departments d
WHERE e.department_id = d.department_id
  AND d.is_closed = TRUE;
```

### DELETE vs TRUNCATE

| Aspect | DELETE | TRUNCATE |
|--------|--------|----------|
| WHERE clause | Supported | Not supported |
| Speed | Slower (row by row) | Faster (deallocates) |
| Triggers | Fires DELETE triggers | No row triggers |
| Transaction | Fully logged | Minimal logging |
| Foreign keys | Respects constraints | Requires CASCADE |
| RETURNING | Supported | Not supported |

```sql
-- DELETE: Selective, logged, triggers fire
DELETE FROM logs WHERE log_date < '2023-01-01';

-- TRUNCATE: All rows, fast, no triggers
TRUNCATE TABLE temp_logs;
```

### Soft Delete Pattern

Instead of removing data, mark it as deleted:

```sql
-- Add a deleted column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- "Delete" by setting timestamp
UPDATE users
SET deleted_at = NOW()
WHERE user_id = 42;

-- Query only active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Create a view for convenience
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;
```

Benefits of soft delete:

- Data can be recovered
- Audit trail preserved
- Referential integrity maintained
- Compliance with data retention policies

### Safe DELETE Practices

```sql
-- Step 1: Check what will be deleted
SELECT * FROM products 
WHERE stock = 0 AND last_ordered < '2023-01-01';

-- Step 2: Count rows to be deleted
SELECT COUNT(*) FROM products 
WHERE stock = 0 AND last_ordered < '2023-01-01';

-- Step 3: Delete in a transaction
BEGIN;
DELETE FROM products 
WHERE stock = 0 AND last_ordered < '2023-01-01';
-- Verify with SELECT COUNT(*)
COMMIT;  -- or ROLLBACK
```

### Complete Example

```sql
-- Setup
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    deleted_at TIMESTAMP  -- For soft delete
);

INSERT INTO tasks (title, status, created_at) VALUES
    ('Task 1', 'completed', NOW() - INTERVAL '60 days'),
    ('Task 2', 'pending', NOW() - INTERVAL '30 days'),
    ('Task 3', 'completed', NOW() - INTERVAL '10 days'),
    ('Task 4', 'pending', NOW());

-- Hard delete a specific task
DELETE FROM tasks
WHERE task_id = 1
RETURNING *;

-- Soft delete instead
UPDATE tasks
SET deleted_at = NOW()
WHERE task_id = 2;

-- Delete completed tasks older than 30 days
DELETE FROM tasks
WHERE status = 'completed'
  AND created_at < NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
RETURNING task_id, title;

-- View remaining tasks
SELECT * FROM tasks WHERE deleted_at IS NULL;
```

## Key Takeaways

- Always use WHERE clause to target specific rows
- Test with SELECT before running DELETE
- RETURNING shows exactly what was deleted
- Use USING for join-based deletes
- Consider soft delete for recoverable/auditable data
- Use transactions for safety on important deletions
- DELETE is slower but more flexible than TRUNCATE

## Additional Resources

- [PostgreSQL DELETE](https://www.postgresql.org/docs/current/sql-delete.html)
- [DELETE with USING](https://www.postgresql.org/docs/current/sql-delete.html)
- [Soft Delete Patterns](https://www.brentozar.com/archive/2020/02/what-is-soft-delete/)
