# HAVING

## Learning Objectives

- Understand the difference between WHERE and HAVING
- Apply HAVING to filter grouped results
- Use HAVING with aggregate functions
- Combine WHERE and HAVING effectively

## Why This Matters

HAVING is essential for filtering aggregated data. While WHERE filters individual rows before grouping, HAVING filters groups after aggregation. This distinction is crucial for queries like "show departments with more than 10 employees" or "find products with total sales over $1000."

## The Concept

### WHERE vs HAVING

| Clause | Filters | Runs | Example |
|--------|---------|------|---------|
| WHERE | Individual rows | Before GROUP BY | `WHERE salary > 50000` |
| HAVING | Groups | After GROUP BY | `HAVING COUNT(*) > 10` |

```
Query Execution Order:
1. FROM     - Get data
2. WHERE    - Filter rows
3. GROUP BY - Create groups
4. HAVING   - Filter groups
5. SELECT   - Choose output
6. ORDER BY - Sort results
```

### Basic HAVING Syntax

```sql
SELECT column, aggregate_function(column)
FROM table
GROUP BY column
HAVING aggregate_condition;

-- Example: Departments with more than 5 employees
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

### HAVING with Different Aggregates

```sql
-- Groups with average salary above threshold
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000;

-- Categories with total revenue over 10000
SELECT category, SUM(price * quantity) AS revenue
FROM sales
GROUP BY category
HAVING SUM(price * quantity) > 10000;

-- Products ordered less than 5 times (low performers)
SELECT product_id, COUNT(*) AS order_count
FROM order_items
GROUP BY product_id
HAVING COUNT(*) < 5;
```

### HAVING vs WHERE: When to Use Each

**Use WHERE** for conditions on individual rows:

```sql
-- Sales by active employees only
SELECT department, SUM(sales_amount)
FROM employees
WHERE is_active = TRUE    -- Filter rows
GROUP BY department;
```

**Use HAVING** for conditions on aggregates:

```sql
-- Departments with high total sales
SELECT department, SUM(sales_amount) AS total_sales
FROM employees
GROUP BY department
HAVING SUM(sales_amount) > 100000;  -- Filter groups
```

**Common mistake**:

```sql
-- WRONG: Cannot use aggregate in WHERE
SELECT department, COUNT(*)
FROM employees
WHERE COUNT(*) > 5    -- ERROR!
GROUP BY department;

-- CORRECT: Use HAVING for aggregates
SELECT department, COUNT(*)
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

### Combining WHERE and HAVING

Filter at both levels for refined results:

```sql
-- High-performing departments (only counting active employees)
SELECT department, COUNT(*) AS active_count, AVG(salary) AS avg_salary
FROM employees
WHERE is_active = TRUE           -- First: filter to active only
GROUP BY department
HAVING COUNT(*) >= 3             -- Then: only groups with 3+ active
ORDER BY avg_salary DESC;
```

```sql
-- 2024 orders by category, only showing categories with 1000+ revenue
SELECT 
    category,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
FROM orders
WHERE order_date >= '2024-01-01'  -- Filter rows to 2024
GROUP BY category
HAVING SUM(total) >= 1000         -- Filter groups by revenue
ORDER BY revenue DESC;
```

### Multiple HAVING Conditions

Combine conditions with AND/OR:

```sql
-- Departments with many employees AND high average salary
SELECT department, COUNT(*) AS cnt, AVG(salary) AS avg_sal
FROM employees
GROUP BY department
HAVING COUNT(*) > 10 AND AVG(salary) > 50000;

-- Products with either high sales OR low inventory
SELECT product_id, SUM(quantity) AS sold, MAX(stock) AS current_stock
FROM sales s
JOIN inventory i ON s.product_id = i.product_id
GROUP BY s.product_id
HAVING SUM(quantity) > 100 OR MAX(stock) < 10;
```

### HAVING without GROUP BY

HAVING can be used without GROUP BY when treating the whole table as one group:

```sql
-- Check if table has at least 100 rows
SELECT COUNT(*) AS total_employees
FROM employees
HAVING COUNT(*) >= 100;
-- Returns row only if condition is met
```

## Code Example

Comprehensive HAVING usage:

```sql
-- Sample data
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    salesperson VARCHAR(100),
    region VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    sale_date DATE
);

INSERT INTO sales (product_name, category, salesperson, region, quantity, unit_price, sale_date) VALUES
    ('Laptop', 'Electronics', 'Alice', 'North', 5, 999.99, '2024-01-15'),
    ('Mouse', 'Electronics', 'Bob', 'South', 20, 29.99, '2024-01-16'),
    ('Chair', 'Furniture', 'Alice', 'North', 10, 199.99, '2024-01-16'),
    ('Desk', 'Furniture', 'Carol', 'East', 3, 399.99, '2024-01-17'),
    ('Monitor', 'Electronics', 'Bob', 'West', 8, 349.99, '2024-01-18'),
    ('Keyboard', 'Electronics', 'Alice', 'North', 15, 89.99, '2024-01-18'),
    ('Lamp', 'Furniture', 'Bob', 'South', 12, 49.99, '2024-01-19'),
    ('Headphones', 'Electronics', 'Carol', 'East', 25, 79.99, '2024-01-19'),
    ('Tablet', 'Electronics', 'Alice', 'North', 7, 599.99, '2024-01-20'),
    ('Bookshelf', 'Furniture', 'Bob', 'South', 4, 149.99, '2024-01-20');

-- Categories with high revenue
SELECT 
    category,
    COUNT(*) AS sales_count,
    SUM(quantity * unit_price) AS revenue
FROM sales
GROUP BY category
HAVING SUM(quantity * unit_price) > 3000
ORDER BY revenue DESC;

-- Salespeople with more than 2 sales
SELECT 
    salesperson,
    COUNT(*) AS sales_count,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY salesperson
HAVING COUNT(*) > 2
ORDER BY total_revenue DESC;

-- Combine WHERE and HAVING
-- Electronics category only, with high average order value
SELECT 
    product_name,
    COUNT(*) AS times_sold,
    AVG(quantity * unit_price) AS avg_order_value
FROM sales
WHERE category = 'Electronics'
GROUP BY product_name
HAVING AVG(quantity * unit_price) > 1000
ORDER BY avg_order_value DESC;

-- Regions with diverse product mix (more than 2 categories)
SELECT 
    region,
    COUNT(DISTINCT category) AS categories_sold,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
GROUP BY region
HAVING COUNT(DISTINCT category) >= 2;

-- Multiple HAVING conditions
SELECT 
    salesperson,
    region,
    COUNT(*) AS sales,
    SUM(quantity) AS units,
    SUM(quantity * unit_price) AS revenue
FROM sales
GROUP BY salesperson, region
HAVING COUNT(*) >= 2 AND SUM(quantity * unit_price) > 1000
ORDER BY revenue DESC;
```

## Key Takeaways

- WHERE filters rows before grouping
- HAVING filters groups after aggregation
- Use HAVING with aggregate functions (COUNT, SUM, AVG, etc.)
- Cannot use aggregates in WHERE clause
- Combine WHERE and HAVING for multi-level filtering
- HAVING runs after GROUP BY in execution order

## Additional Resources

- [PostgreSQL HAVING](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [WHERE vs HAVING](https://www.postgresql.org/docs/current/tutorial-agg.html)
- [Query Execution Order](https://www.postgresql.org/docs/current/queries-overview.html)
