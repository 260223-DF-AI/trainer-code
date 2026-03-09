# Clauses: FROM, WHERE, SELECT, ORDER BY

## Learning Objectives

- Understand the logical order of SQL clause execution
- Master each core SELECT clause
- Build queries systematically using clause order
- Recognize the difference between written and execution order

## Why This Matters

Understanding how SQL processes clauses helps you write correct, efficient queries. The order you write clauses differs from how the database executes them. Knowing this logical order prevents common errors and helps you optimize query performance.

## The Concept

### SQL Clause Execution Order

**Written order** (how you type it):

```sql
SELECT columns
FROM table
WHERE condition
ORDER BY column;
```

**Execution order** (how database processes it):

```
1. FROM    - Identify source tables
2. WHERE   - Filter rows
3. SELECT  - Choose columns
4. ORDER BY - Sort results
```

This matters because:

- You cannot use column aliases from SELECT in WHERE
- WHERE filters before aggregation happens
- ORDER BY can use column aliases (it runs last)

### The FROM Clause

FROM specifies the data source:

```sql
-- Single table
SELECT * FROM employees;

-- Table with alias
SELECT e.first_name, e.last_name FROM employees e;

-- Multiple tables (join)
SELECT * FROM orders, customers;  -- Cartesian product (usually wrong)

-- Subquery as source
SELECT * FROM (SELECT * FROM products WHERE price > 100) AS expensive_products;
```

### The WHERE Clause

WHERE filters rows before any grouping or selection:

```sql
-- Simple condition
SELECT * FROM products WHERE category = 'Electronics';

-- Multiple conditions
SELECT * FROM employees 
WHERE department = 'Sales' AND salary > 50000;

-- Range
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Pattern matching
SELECT * FROM customers WHERE email LIKE '%@gmail.com';

-- NULL check
SELECT * FROM employees WHERE manager_id IS NULL;

-- IN list
SELECT * FROM products WHERE category IN ('Books', 'Electronics', 'Toys');

-- Subquery
SELECT * FROM customers 
WHERE customer_id IN (SELECT customer_id FROM orders WHERE total > 1000);
```

### The SELECT Clause

SELECT determines which columns appear in output:

```sql
-- All columns
SELECT * FROM employees;

-- Specific columns
SELECT first_name, last_name, email FROM employees;

-- Expressions
SELECT first_name, salary, salary * 1.10 AS new_salary FROM employees;

-- String operations
SELECT first_name || ' ' || last_name AS full_name FROM employees;

-- Conditional
SELECT 
    name,
    CASE 
        WHEN price < 10 THEN 'Budget'
        WHEN price < 50 THEN 'Mid-range'
        ELSE 'Premium'
    END AS price_tier
FROM products;

-- DISTINCT
SELECT DISTINCT department FROM employees;

-- Calculations
SELECT 2 + 2 AS result;
```

### The ORDER BY Clause

ORDER BY sorts the final result set:

```sql
-- Ascending (default)
SELECT * FROM products ORDER BY price;
SELECT * FROM products ORDER BY price ASC;

-- Descending
SELECT * FROM products ORDER BY price DESC;

-- Multiple columns
SELECT * FROM employees ORDER BY department ASC, salary DESC;

-- By column position
SELECT first_name, last_name FROM employees ORDER BY 2;  -- By last_name

-- By alias (allowed because ORDER BY is last)
SELECT first_name || ' ' || last_name AS full_name 
FROM employees 
ORDER BY full_name;

-- By expression
SELECT * FROM products ORDER BY price * quantity DESC;

-- NULL handling
SELECT * FROM employees ORDER BY commission NULLS FIRST;
SELECT * FROM employees ORDER BY commission NULLS LAST;
```

### Common Errors from Execution Order

**Cannot use SELECT alias in WHERE**:

```sql
-- WRONG: alias not available in WHERE
SELECT salary * 12 AS annual_salary FROM employees
WHERE annual_salary > 100000;
-- ERROR: column "annual_salary" does not exist

-- CORRECT: repeat the expression
SELECT salary * 12 AS annual_salary FROM employees
WHERE salary * 12 > 100000;

-- OR use subquery/CTE
SELECT * FROM (
    SELECT salary * 12 AS annual_salary FROM employees
) sub
WHERE annual_salary > 100000;
```

**ORDER BY can use alias**:

```sql
-- This works because ORDER BY runs last
SELECT first_name || ' ' || last_name AS full_name 
FROM employees 
ORDER BY full_name;
```

## Code Example

Building queries step by step:

```sql
-- Sample data
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    sale_date DATE,
    region VARCHAR(50)
);

INSERT INTO sales (product_name, category, quantity, unit_price, sale_date, region) VALUES
    ('Laptop', 'Electronics', 5, 999.99, '2024-01-15', 'North'),
    ('Mouse', 'Electronics', 20, 29.99, '2024-01-16', 'South'),
    ('Chair', 'Furniture', 10, 199.99, '2024-01-16', 'North'),
    ('Desk', 'Furniture', 3, 399.99, '2024-01-17', 'East'),
    ('Monitor', 'Electronics', 8, 349.99, '2024-01-18', 'West'),
    ('Keyboard', 'Electronics', 15, 89.99, '2024-01-18', 'North'),
    ('Lamp', 'Furniture', 12, 49.99, '2024-01-19', 'South');

-- Step 1: FROM (what table?)
SELECT * FROM sales;

-- Step 2: Add WHERE (which rows?)
SELECT * FROM sales 
WHERE category = 'Electronics';

-- Step 3: Refine SELECT (which columns and calculations?)
SELECT 
    product_name,
    quantity,
    unit_price,
    quantity * unit_price AS total_revenue
FROM sales 
WHERE category = 'Electronics';

-- Step 4: Add ORDER BY (sorted how?)
SELECT 
    product_name,
    quantity,
    unit_price,
    quantity * unit_price AS total_revenue
FROM sales 
WHERE category = 'Electronics'
ORDER BY total_revenue DESC;

-- Complex query using all clauses
SELECT 
    region,
    category,
    product_name,
    quantity,
    unit_price,
    quantity * unit_price AS line_total,
    CASE 
        WHEN quantity >= 10 THEN 'High Volume'
        ELSE 'Low Volume'
    END AS volume_category
FROM sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'
    AND unit_price > 25
ORDER BY region, line_total DESC;
```

## Key Takeaways

- FROM runs first: identifies data source
- WHERE runs second: filters rows
- SELECT runs third: calculates and chooses output columns
- ORDER BY runs last: sorts the result
- Cannot use SELECT aliases in WHERE (execution order)
- Can use SELECT aliases in ORDER BY (it runs last)

## Additional Resources

- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [Query Execution Order](https://www.postgresql.org/docs/current/queries-overview.html)
- [WHERE Clause](https://www.postgresql.org/docs/current/queries-table-expressions.html)
