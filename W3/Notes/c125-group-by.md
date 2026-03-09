# GROUP BY

## Learning Objectives

- Understand how GROUP BY creates row groups
- Combine GROUP BY with aggregate functions
- Apply grouping to multiple columns
- Recognize GROUP BY rules and common errors

## Why This Matters

GROUP BY is the mechanism that enables aggregate functions to work on subsets of data. Without GROUP BY, you can only get totals for an entire table. With GROUP BY, you can break down data by category, region, time period, or any other dimension. This is the foundation of all data analysis and reporting.

## The Concept

### What Does GROUP BY Do?

GROUP BY divides rows into groups based on column values. Aggregate functions then operate on each group separately.

```
Without GROUP BY:                 With GROUP BY:
+------------+-------+            +------------+-------+--------+
| department | salary|            | department | COUNT | SUM    |
+------------+-------+            +------------+-------+--------+
| Sales      | 50000 |            | Sales      |   3   | 160000 |
| Sales      | 55000 |    -->     | Eng        |   2   | 150000 |
| Sales      | 55000 |            +------------+-------+--------+
| Eng        | 70000 |
| Eng        | 80000 |
+------------+-------+
```

### Basic GROUP BY Syntax

```sql
SELECT column, aggregate_function(column)
FROM table
GROUP BY column;

-- Example
SELECT department, COUNT(*), AVG(salary)
FROM employees
GROUP BY department;
```

### GROUP BY Rules

**Rule 1: Non-aggregated columns must be in GROUP BY**

```sql
-- WRONG: first_name not in GROUP BY
SELECT department, first_name, COUNT(*)
FROM employees
GROUP BY department;
-- ERROR: column "first_name" must appear in GROUP BY clause

-- CORRECT: Include first_name in GROUP BY
SELECT department, first_name, COUNT(*)
FROM employees
GROUP BY department, first_name;
```

**Rule 2: GROUP BY runs after WHERE**

```sql
-- Filter first, then group
SELECT department, COUNT(*)
FROM employees
WHERE salary > 50000    -- Filter rows first
GROUP BY department;    -- Then group remaining rows
```

### Multi-Column GROUP BY

Group by multiple columns for more granular analysis:

```sql
-- Sales by region and year
SELECT 
    region,
    EXTRACT(YEAR FROM sale_date) AS year,
    SUM(amount) AS total_sales
FROM sales
GROUP BY region, EXTRACT(YEAR FROM sale_date)
ORDER BY region, year;

-- Employees by department and role
SELECT 
    department,
    job_title,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department, job_title
ORDER BY department, job_title;
```

### GROUP BY with Expressions

You can group by calculated values:

```sql
-- Group by year
SELECT 
    EXTRACT(YEAR FROM order_date) AS order_year,
    COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date);

-- Group by price range
SELECT 
    CASE 
        WHEN price < 50 THEN 'Budget'
        WHEN price < 200 THEN 'Mid-range'
        ELSE 'Premium'
    END AS price_tier,
    COUNT(*) AS product_count
FROM products
GROUP BY 
    CASE 
        WHEN price < 50 THEN 'Budget'
        WHEN price < 200 THEN 'Mid-range'
        ELSE 'Premium'
    END;

-- Or use column position (less readable)
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    COUNT(*)
FROM orders
GROUP BY 1;  -- Groups by first SELECT column
```

### GROUP BY vs DISTINCT

Both can find unique values, but GROUP BY allows aggregation:

```sql
-- DISTINCT: Just unique values
SELECT DISTINCT department FROM employees;

-- GROUP BY: Unique values with aggregates
SELECT department, COUNT(*) FROM employees GROUP BY department;

-- For simple uniqueness, DISTINCT is clearer
-- For aggregation, GROUP BY is required
```

### NULL in GROUP BY

NULLs are grouped together:

```sql
SELECT category, COUNT(*)
FROM products
GROUP BY category;
-- One row for NULL category containing all products without category
```

### GROUPING SETS, ROLLUP, CUBE

Advanced grouping options:

```sql
-- ROLLUP: Hierarchical totals
SELECT 
    region,
    category,
    SUM(sales)
FROM sales_data
GROUP BY ROLLUP (region, category);
-- Returns: (region, category), (region), and grand total

-- CUBE: All combinations
SELECT 
    region,
    category,
    SUM(sales)
FROM sales_data
GROUP BY CUBE (region, category);
-- Returns all possible groupings

-- GROUPING SETS: Specific groupings
SELECT 
    region,
    category,
    SUM(sales)
FROM sales_data
GROUP BY GROUPING SETS ((region), (category), ());
-- Returns: by region, by category, and grand total
```

## Code Example

Comprehensive GROUP BY usage:

```sql
-- Create sample data
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    product_category VARCHAR(50),
    region VARCHAR(50),
    amount DECIMAL(10, 2)
);

INSERT INTO orders (customer_id, order_date, product_category, region, amount) VALUES
    (1, '2024-01-15', 'Electronics', 'North', 500),
    (2, '2024-01-16', 'Electronics', 'South', 300),
    (1, '2024-01-17', 'Clothing', 'North', 100),
    (3, '2024-02-01', 'Electronics', 'East', 450),
    (2, '2024-02-15', 'Clothing', 'South', 200),
    (1, '2024-02-20', 'Home', 'North', 350),
    (4, '2024-03-01', 'Electronics', 'West', 600),
    (3, '2024-03-10', 'Clothing', 'East', 150);

-- Simple GROUP BY
SELECT product_category, COUNT(*) AS order_count, SUM(amount) AS total_sales
FROM orders
GROUP BY product_category
ORDER BY total_sales DESC;

-- Multi-column GROUP BY
SELECT 
    region,
    product_category,
    COUNT(*) AS order_count,
    SUM(amount) AS total_sales
FROM orders
GROUP BY region, product_category
ORDER BY region, product_category;

-- GROUP BY with expression
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    COUNT(*) AS orders,
    SUM(amount) AS revenue
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;

-- GROUP BY with CASE
SELECT 
    CASE 
        WHEN amount < 200 THEN 'Small'
        WHEN amount < 400 THEN 'Medium'
        ELSE 'Large'
    END AS order_size,
    COUNT(*) AS order_count,
    AVG(amount) AS avg_amount
FROM orders
GROUP BY 
    CASE 
        WHEN amount < 200 THEN 'Small'
        WHEN amount < 400 THEN 'Medium'
        ELSE 'Large'
    END;

-- ROLLUP for subtotals
SELECT 
    COALESCE(region, 'All Regions') AS region,
    COALESCE(product_category, 'All Categories') AS category,
    SUM(amount) AS total
FROM orders
GROUP BY ROLLUP (region, product_category)
ORDER BY region NULLS LAST, product_category NULLS LAST;
```

## Key Takeaways

- GROUP BY divides rows into groups for aggregation
- All non-aggregated SELECT columns must appear in GROUP BY
- WHERE filters before grouping; use HAVING to filter after
- Can group by expressions and calculated values
- NULL values are grouped together as one group
- ROLLUP and CUBE provide hierarchical and multi-dimensional grouping

## Additional Resources

- [PostgreSQL GROUP BY](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [Aggregate Expressions](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES)
- [GROUPING SETS](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUPING-SETS)
