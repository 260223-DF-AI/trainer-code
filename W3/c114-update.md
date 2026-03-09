# UPDATE Statement

## Learning Objectives

- Master UPDATE syntax for modifying existing data
- Apply WHERE clauses to target specific rows
- Update multiple columns and use expressions
- Understand UPDATE with JOINs and subqueries

## Why This Matters

Data changes constantly - prices adjust, statuses update, errors need correction. UPDATE is how you modify existing records without deleting and reinserting them. Knowing how to write precise UPDATE statements prevents accidental mass modifications and keeps your data accurate.

## The Concept

### Basic UPDATE Syntax

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

**Critical**: Always include a WHERE clause unless you intend to update ALL rows.

### Simple UPDATE

```sql
-- Update a single column
UPDATE employees
SET salary = 80000
WHERE employee_id = 1;

-- Update multiple columns
UPDATE employees
SET salary = 85000, department = 'Senior Engineering'
WHERE employee_id = 1;
```

### UPDATE Without WHERE (Dangerous!)

```sql
-- This updates EVERY row in the table!
UPDATE products
SET price = price * 1.10;  -- 10% price increase for all products

-- Always double-check before running UPDATE without WHERE
```

### UPDATE with Expressions

Use calculations and functions in SET:

```sql
-- Increase all salaries by 5%
UPDATE employees
SET salary = salary * 1.05
WHERE department = 'Engineering';

-- Use SQL functions
UPDATE orders
SET status = UPPER(status);

-- Set to current timestamp
UPDATE users
SET last_login = NOW()
WHERE user_id = 42;

-- Concatenate strings
UPDATE customers
SET full_name = first_name || ' ' || last_name;
```

### UPDATE with Multiple Conditions

```sql
-- Multiple conditions with AND
UPDATE products
SET discount = 0.20
WHERE category = 'Electronics' 
  AND stock > 100;

-- Using OR
UPDATE orders
SET status = 'cancelled'
WHERE status = 'pending' 
  AND (order_date < '2024-01-01' OR amount < 10);

-- Using IN
UPDATE employees
SET department = 'Merged Department'
WHERE department IN ('Sales', 'Marketing', 'Business Development');
```

### UPDATE with RETURNING

Get the updated rows back:

```sql
UPDATE products
SET price = price * 0.90
WHERE category = 'Clearance'
RETURNING product_id, name, price;

-- Return all columns
UPDATE employees
SET salary = salary + 5000
WHERE employee_id = 1
RETURNING *;
```

### UPDATE with Subquery

Use a query result to determine what to update:

```sql
-- Update based on a subquery condition
UPDATE orders
SET status = 'priority'
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE membership_level = 'gold'
);

-- Use subquery for the new value
UPDATE products
SET price = (
    SELECT AVG(price) 
    FROM products 
    WHERE category = products.category
)
WHERE price IS NULL;
```

### UPDATE with FROM (Join Update)

Update using data from another table:

```sql
-- PostgreSQL syntax for join update
UPDATE employees e
SET department_name = d.name
FROM departments d
WHERE e.department_id = d.department_id;

-- Update with calculated value from another table
UPDATE order_items oi
SET unit_price = p.current_price
FROM products p
WHERE oi.product_id = p.product_id
  AND oi.order_id = 100;
```

### Safe UPDATE Practices

```sql
-- Step 1: Check what will be updated with SELECT
SELECT * FROM products 
WHERE category = 'Electronics' AND stock < 10;

-- Step 2: Run UPDATE only after verifying
UPDATE products
SET on_sale = TRUE
WHERE category = 'Electronics' AND stock < 10;

-- Use transactions for safety
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- Check the result
SELECT * FROM accounts WHERE account_id = 1;
-- Commit or rollback
COMMIT;  -- or ROLLBACK if something's wrong
```

### Complete Example

```sql
-- Setup
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO products (name, price, stock, category) VALUES
    ('Laptop', 999.99, 50, 'Electronics'),
    ('Mouse', 29.99, 200, 'Electronics'),
    ('Desk', 299.99, 30, 'Furniture'),
    ('Chair', 199.99, 25, 'Furniture');

-- Single update
UPDATE products
SET price = 949.99
WHERE name = 'Laptop';

-- Bulk update with expression
UPDATE products
SET price = price * 1.10
WHERE category = 'Furniture'
RETURNING name, price;

-- Update multiple columns
UPDATE products
SET stock = stock - 10, is_active = FALSE
WHERE stock < 30 AND category = 'Furniture';

-- Verify changes
SELECT * FROM products;
```

## Key Takeaways

- Always use WHERE clause to target specific rows
- Test with SELECT before running UPDATE
- Use expressions and functions in SET for calculations
- RETURNING shows what was actually updated
- Use transactions for safety on important updates
- UPDATE with FROM allows join-based updates

## Additional Resources

- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
- [UPDATE with FROM](https://www.postgresql.org/docs/current/sql-update.html)
- [RETURNING Clause](https://www.postgresql.org/docs/current/dml-returning.html)
