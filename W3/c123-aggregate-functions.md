# Aggregate Functions

## Learning Objectives

- Understand aggregate functions and their purpose
- Master COUNT, SUM, AVG, MIN, MAX
- Apply aggregates with GROUP BY
- Handle NULL values in aggregations

## Why This Matters

Aggregate functions transform multiple rows into summary values. They are essential for reporting, analytics, and any scenario where you need totals, averages, or counts. Every data professional must master these functions to extract meaningful insights from large datasets.

## The Concept

### What Are Aggregate Functions?

**Aggregate functions** operate on sets of rows and return a single value. They collapse multiple rows into a summary.

```
Input Rows:           Aggregate:        Result:
| value |             COUNT(value)        5
|   10  |             SUM(value)         80
|   20  |             AVG(value)         16
|   15  |             MIN(value)         10
|   25  |             MAX(value)         25
|   10  |
+-------+
```

### Core Aggregate Functions

| Function | Description | NULL Handling |
|----------|-------------|---------------|
| COUNT(*) | Count all rows | Includes NULLs |
| COUNT(col) | Count non-NULL values | Ignores NULLs |
| SUM(col) | Sum of values | Ignores NULLs |
| AVG(col) | Average of values | Ignores NULLs |
| MIN(col) | Minimum value | Ignores NULLs |
| MAX(col) | Maximum value | Ignores NULLs |

### COUNT Function

```sql
-- Count all rows
SELECT COUNT(*) FROM employees;

-- Count non-NULL values
SELECT COUNT(email) FROM employees;

-- Count distinct values
SELECT COUNT(DISTINCT department) FROM employees;

-- Count with condition (using FILTER)
SELECT COUNT(*) FILTER (WHERE salary > 50000) AS high_earners FROM employees;
```

### SUM Function

```sql
-- Total salary
SELECT SUM(salary) FROM employees;

-- Sum with condition
SELECT SUM(salary) FROM employees WHERE department = 'Engineering';

-- Sum expression
SELECT SUM(quantity * unit_price) AS total_revenue FROM order_items;

-- Sum distinct values only
SELECT SUM(DISTINCT bonus) FROM employees;
```

### AVG Function

```sql
-- Average salary
SELECT AVG(salary) FROM employees;

-- Average with rounding
SELECT ROUND(AVG(salary), 2) AS avg_salary FROM employees;

-- Average ignores NULL
SELECT AVG(commission) FROM employees;  -- Only counts non-NULL

-- Average treating NULL as zero
SELECT AVG(COALESCE(commission, 0)) FROM employees;
```

### MIN and MAX Functions

```sql
-- Minimum and maximum values
SELECT MIN(price), MAX(price) FROM products;

-- Works with dates
SELECT MIN(hire_date), MAX(hire_date) FROM employees;

-- Works with strings (alphabetical)
SELECT MIN(name), MAX(name) FROM products;

-- Combined in one query
SELECT 
    MIN(salary) AS lowest_salary,
    MAX(salary) AS highest_salary,
    MAX(salary) - MIN(salary) AS salary_range
FROM employees;
```

### Aggregate without GROUP BY

Without GROUP BY, aggregates operate on the entire table:

```sql
SELECT 
    COUNT(*) AS total_employees,
    SUM(salary) AS total_payroll,
    AVG(salary) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees;
```

### Aggregate with GROUP BY

GROUP BY creates groups, and aggregates operate per group:

```sql
-- Count per department
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;

-- Sum per category
SELECT category, SUM(price) AS total_value
FROM products
GROUP BY category;

-- Multiple aggregates
SELECT 
    department,
    COUNT(*) AS headcount,
    SUM(salary) AS total_salary,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;
```

### NULL Handling

Aggregates (except COUNT(*)) ignore NULL values:

```sql
-- Sample data with NULLs
CREATE TABLE test_data (
    id SERIAL,
    value INTEGER
);
INSERT INTO test_data (value) VALUES (10), (20), (NULL), (30), (NULL);

-- COUNT(*) counts all rows: 5
SELECT COUNT(*) FROM test_data;

-- COUNT(value) counts non-NULL: 3
SELECT COUNT(value) FROM test_data;

-- SUM ignores NULL: 60 (not NULL)
SELECT SUM(value) FROM test_data;

-- AVG ignores NULL: 20 (not 12)
SELECT AVG(value) FROM test_data;  -- 60/3 = 20
```

### FILTER Clause (PostgreSQL)

Apply conditions to specific aggregates:

```sql
SELECT 
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_orders,
    COUNT(*) FILTER (WHERE status = 'pending') AS pending_orders,
    SUM(total) FILTER (WHERE status = 'completed') AS completed_revenue
FROM orders;
```

## Code Example

Comprehensive aggregate examples:

```sql
-- Create sample data
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    region VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    sale_date DATE
);

INSERT INTO sales (product_name, category, region, quantity, unit_price, sale_date) VALUES
    ('Laptop', 'Electronics', 'North', 5, 999.99, '2024-01-15'),
    ('Mouse', 'Electronics', 'South', 20, 29.99, '2024-01-16'),
    ('Chair', 'Furniture', 'North', 10, 199.99, '2024-01-16'),
    ('Desk', 'Furniture', 'East', 3, 399.99, '2024-01-17'),
    ('Monitor', 'Electronics', 'West', 8, 349.99, '2024-01-18'),
    ('Keyboard', 'Electronics', 'North', 15, 89.99, '2024-01-18'),
    ('Lamp', 'Furniture', 'South', 12, 49.99, '2024-01-19'),
    ('Headphones', 'Electronics', 'East', 25, 79.99, '2024-01-19');

-- Overall statistics
SELECT 
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT category) AS categories,
    COUNT(DISTINCT region) AS regions,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * unit_price) AS total_revenue,
    ROUND(AVG(quantity * unit_price), 2) AS avg_transaction_value,
    MIN(unit_price) AS lowest_price,
    MAX(unit_price) AS highest_price
FROM sales;

-- By category
SELECT 
    category,
    COUNT(*) AS transactions,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    ROUND(AVG(unit_price), 2) AS avg_price
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- By region
SELECT 
    region,
    COUNT(*) AS transactions,
    SUM(quantity * unit_price) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Using FILTER for conditional aggregates
SELECT 
    COUNT(*) AS all_sales,
    COUNT(*) FILTER (WHERE unit_price > 100) AS premium_sales,
    SUM(quantity * unit_price) AS total_revenue,
    SUM(quantity * unit_price) FILTER (WHERE category = 'Electronics') AS electronics_revenue,
    SUM(quantity * unit_price) FILTER (WHERE category = 'Furniture') AS furniture_revenue
FROM sales;
```

## Key Takeaways

- Aggregate functions collapse multiple rows into single values
- COUNT(*) counts all rows; COUNT(column) counts non-NULLs
- SUM, AVG, MIN, MAX all ignore NULL values
- Without GROUP BY, aggregates work on the entire table
- Use FILTER clause for conditional aggregates in PostgreSQL

## Additional Resources

- [PostgreSQL Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [GROUP BY](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [FILTER Clause](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES)
