# DML: Data Manipulation Language

## Learning Objectives

- Master DML commands: INSERT, UPDATE, DELETE
- Write effective data modification statements
- Understand the importance of WHERE clauses
- Apply safe practices when modifying data

## Why This Matters

While DDL defines structure, DML is where you work with actual data. INSERT, UPDATE, and DELETE are the commands you will use to populate tables, correct errors, and maintain data freshness. These commands directly affect your data, so understanding them thoroughly prevents costly mistakes.

## The Concept

### What is DML?

Data Manipulation Language (DML) consists of SQL commands that add, modify, and remove data within existing tables. DML operates on **rows** within tables.

### DML Commands Overview

| Command | Purpose | Affects |
|---------|---------|---------|
| INSERT | Add new rows | New data |
| UPDATE | Modify existing rows | Existing data |
| DELETE | Remove rows | Data removal |

### INSERT

The INSERT command adds new rows to a table:

**Basic INSERT**:

```sql
-- Insert a single row with all columns
INSERT INTO employees (employee_id, first_name, last_name, email, salary)
VALUES (1, 'Alice', 'Johnson', 'alice@company.com', 75000);

-- Insert with only some columns (others get defaults or NULL)
INSERT INTO employees (first_name, last_name)
VALUES ('Bob', 'Smith');

-- Insert without column list (must match table order exactly)
INSERT INTO products VALUES (1, 'Widget', 19.99, 100);
```

**Multiple Row INSERT**:

```sql
-- Insert multiple rows at once
INSERT INTO employees (first_name, last_name, department)
VALUES 
    ('Carol', 'Williams', 'Engineering'),
    ('David', 'Brown', 'Marketing'),
    ('Eve', 'Davis', 'Sales');
```

**INSERT with SELECT**:

```sql
-- Insert data from another table
INSERT INTO employees_archive (employee_id, first_name, last_name, hire_date)
SELECT employee_id, first_name, last_name, hire_date
FROM employees
WHERE termination_date IS NOT NULL;

-- Insert with transformation
INSERT INTO order_summary (year, month, total_orders, total_revenue)
SELECT 
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    COUNT(*),
    SUM(total)
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date);
```

**INSERT with RETURNING**:

```sql
-- Get the inserted data back (especially useful for auto-generated IDs)
INSERT INTO employees (first_name, last_name)
VALUES ('Frank', 'Wilson')
RETURNING employee_id, first_name, last_name;

-- Result: 
-- employee_id | first_name | last_name
-- 7           | Frank      | Wilson
```

### UPDATE

The UPDATE command modifies existing rows:

**Basic UPDATE**:

```sql
-- Update specific rows
UPDATE employees 
SET salary = 80000 
WHERE employee_id = 1;

-- Update multiple columns
UPDATE employees 
SET 
    salary = 85000,
    department = 'Senior Engineering',
    updated_at = CURRENT_TIMESTAMP
WHERE employee_id = 1;
```

**WARNING: Always use WHERE!**

```sql
-- DANGEROUS: Updates ALL rows!
UPDATE employees SET salary = 50000;
-- Every employee now has salary 50000!

-- SAFE: Updates only matching rows
UPDATE employees 
SET salary = 50000 
WHERE department = 'Interns';
```

**UPDATE with Expressions**:

```sql
-- Increase all salaries by 5%
UPDATE employees 
SET salary = salary * 1.05;

-- Conditional update
UPDATE products 
SET price = price * 0.9 
WHERE category = 'Clearance';

-- Update with calculations
UPDATE inventory 
SET stock = stock - 1 
WHERE product_id = 100 AND stock > 0;
```

**UPDATE with Subquery**:

```sql
-- Update based on data from another table
UPDATE employees 
SET department = (
    SELECT department_name 
    FROM departments 
    WHERE departments.department_id = employees.department_id
);

-- Update with FROM clause (PostgreSQL)
UPDATE orders
SET status = 'vip'
FROM customers
WHERE orders.customer_id = customers.customer_id
    AND customers.membership_level = 'platinum';
```

**UPDATE with RETURNING**:

```sql
-- Get updated rows back
UPDATE employees 
SET salary = salary * 1.10 
WHERE department = 'Engineering'
RETURNING employee_id, first_name, salary;
```

### DELETE

The DELETE command removes rows from a table:

**Basic DELETE**:

```sql
-- Delete specific rows
DELETE FROM employees 
WHERE employee_id = 1;

-- Delete with multiple conditions
DELETE FROM orders 
WHERE status = 'cancelled' 
    AND order_date < '2023-01-01';
```

**WARNING: Always use WHERE!**

```sql
-- DANGEROUS: Deletes ALL rows!
DELETE FROM employees;
-- Table is now empty!

-- SAFE: Deletes only matching rows
DELETE FROM employees 
WHERE termination_date < CURRENT_DATE - INTERVAL '7 years';
```

**DELETE with Subquery**:

```sql
-- Delete based on related data
DELETE FROM order_items
WHERE order_id IN (
    SELECT order_id 
    FROM orders 
    WHERE status = 'cancelled'
);

-- Delete using EXISTS
DELETE FROM products
WHERE NOT EXISTS (
    SELECT 1 FROM order_items 
    WHERE order_items.product_id = products.product_id
);
```

**DELETE with RETURNING**:

```sql
-- Get deleted rows (useful for audit logs)
DELETE FROM sessions 
WHERE expires_at < CURRENT_TIMESTAMP
RETURNING session_id, user_id;
```

### Safe Data Modification Practices

1. **Always backup before bulk operations**
2. **Use transactions for safety**:

```sql
BEGIN;
    UPDATE employees SET salary = salary * 1.5 WHERE department = 'Sales';
    -- Check results: SELECT * FROM employees WHERE department = 'Sales';
    -- If wrong: ROLLBACK;
    -- If correct: COMMIT;
COMMIT;
```

1. **Test with SELECT first**:

```sql
-- First, see what will be affected
SELECT * FROM employees WHERE hire_date < '2020-01-01';
-- Then delete
DELETE FROM employees WHERE hire_date < '2020-01-01';
```

1. **Use LIMIT for testing**:

```sql
-- Update just a few rows first
UPDATE products SET price = price * 0.9 
WHERE category = 'Electronics'
LIMIT 5;
```

## Code Example

Complete DML workflow:

```sql
-- Start with a fresh table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- INSERT: Populate the table
INSERT INTO products (name, price, stock, category) VALUES
    ('Laptop', 999.99, 50, 'Electronics'),
    ('Mouse', 29.99, 200, 'Electronics'),
    ('Desk', 199.99, 30, 'Furniture'),
    ('Chair', 149.99, 45, 'Furniture'),
    ('Monitor', 299.99, 75, 'Electronics');

-- Verify
SELECT * FROM products;

-- UPDATE: Modify data
-- 10% discount on electronics
UPDATE products 
SET price = price * 0.90 
WHERE category = 'Electronics'
RETURNING product_id, name, price;

-- Restock low inventory items
UPDATE products 
SET stock = stock + 100 
WHERE stock < 50;

-- DELETE: Remove data
-- Deactivate instead of delete (soft delete)
UPDATE products 
SET is_active = FALSE 
WHERE stock = 0;

-- Actually delete discontinued items
DELETE FROM products 
WHERE category = 'Discontinued'
RETURNING *;
```

## Key Takeaways

- INSERT adds new rows; use RETURNING to get generated values
- UPDATE modifies existing data; always use WHERE to avoid updating all rows
- DELETE removes rows; always use WHERE to avoid deleting all data
- Test modifications with SELECT first
- Use transactions for safe bulk operations
- RETURNING clause helps verify what was affected

## Additional Resources

- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL UPDATE](https://www.postgresql.org/docs/current/sql-update.html)
- [PostgreSQL DELETE](https://www.postgresql.org/docs/current/sql-delete.html)
