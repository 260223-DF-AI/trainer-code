# CROSS JOIN

## Learning Objectives

- Understand CROSS JOIN (Cartesian product)
- Write CROSS JOIN queries
- Identify appropriate use cases
- Recognize the performance implications

## Why This Matters

CROSS JOIN returns every possible combination of rows from two tables. While often used accidentally (causing massive result sets), it has legitimate uses for generating combinations, creating test data, and building reference tables. Understanding CROSS JOIN helps you avoid it when unintended and use it correctly when needed.

## The Concept

### What is CROSS JOIN?

**CROSS JOIN** produces the Cartesian product of two tables: every row from the first table paired with every row from the second table.

```
table_a:        table_b:        CROSS JOIN result:
| val |         | num |         | val | num |
|-----|         |-----|         |-----|-----|
| A   |         | 1   |         | A   | 1   |
| B   |         | 2   |         | A   | 2   |
                                | B   | 1   |
                                | B   | 2   |

2 rows x 2 rows = 4 result rows
```

### Result Size Warning

CROSS JOIN can produce enormous result sets:

- 100 rows x 100 rows = 10,000 rows
- 1,000 x 1,000 = 1,000,000 rows
- 10,000 x 10,000 = 100,000,000 rows

**Always be intentional when using CROSS JOIN.**

### Basic Syntax

```sql
-- Explicit CROSS JOIN
SELECT columns
FROM table_a
CROSS JOIN table_b;

-- Implicit (comma) syntax
SELECT columns
FROM table_a, table_b;
-- Without WHERE clause, this is a CROSS JOIN
```

### CROSS JOIN Examples

**All combinations**:

```sql
-- All color-size combinations
SELECT colors.name, sizes.name
FROM colors
CROSS JOIN sizes;

-- Result:
-- Red, Small
-- Red, Medium
-- Red, Large
-- Blue, Small
-- Blue, Medium
-- Blue, Large
```

**Generate date ranges**:

```sql
-- All dates in a range
SELECT generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day') AS date;

-- All dates with all products
SELECT d.date, p.product_name
FROM generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day') d(date)
CROSS JOIN products p;
```

### Legitimate Use Cases

**1. Generate combinations for lookup tables**:

```sql
-- Product variants
CREATE TABLE product_variants AS
SELECT 
    p.product_id,
    c.color_id,
    s.size_id
FROM products p
CROSS JOIN colors c
CROSS JOIN sizes s;
```

**2. Calendar with events template**:

```sql
-- Ensure every day-store combination exists
SELECT 
    d.date,
    s.store_id,
    COALESCE(sales.total, 0) AS sales_total
FROM generate_series('2024-01-01', '2024-12-31', '1 day') d(date)
CROSS JOIN stores s
LEFT JOIN sales ON sales.sale_date = d.date AND sales.store_id = s.store_id;
```

**3. Matrix reports**:

```sql
-- All departments vs all projects matrix
SELECT 
    d.dept_name,
    p.project_name,
    COUNT(a.assignment_id) AS assigned_count
FROM departments d
CROSS JOIN projects p
LEFT JOIN assignments a ON d.dept_id = a.dept_id AND p.project_id = a.project_id
GROUP BY d.dept_name, p.project_name;
```

**4. Test data generation**:

```sql
-- Generate test orders
INSERT INTO test_orders (customer_id, product_id)
SELECT c.customer_id, p.product_id
FROM customers c
CROSS JOIN products p
WHERE c.customer_id <= 10 AND p.product_id <= 5;
-- Creates 10 x 5 = 50 test orders
```

### Accidental CROSS JOINs

The old comma syntax can cause accidental cross joins:

```sql
-- Intended: Join orders to customers
-- WRONG: Missing ON/WHERE creates Cartesian product
SELECT * FROM orders, customers;
-- Returns every order x every customer!

-- CORRECT: With explicit join condition
SELECT * FROM orders, customers
WHERE orders.customer_id = customers.customer_id;

-- BEST: Use explicit JOIN
SELECT * 
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id;
```

### CROSS JOIN with WHERE

Adding WHERE filters the Cartesian product:

```sql
-- All possible pairs of employees
SELECT 
    e1.name AS employee1,
    e2.name AS employee2
FROM employees e1
CROSS JOIN employees e2
WHERE e1.employee_id < e2.employee_id;  -- Avoid duplicates and self-pairs
```

## Code Example

Comprehensive CROSS JOIN usage:

```sql
-- Create lookup tables
CREATE TABLE colors (color_id SERIAL PRIMARY KEY, name VARCHAR(20));
CREATE TABLE sizes (size_id SERIAL PRIMARY KEY, name VARCHAR(10));
CREATE TABLE products (product_id SERIAL PRIMARY KEY, name VARCHAR(100));

INSERT INTO colors (name) VALUES ('Red'), ('Blue'), ('Green');
INSERT INTO sizes (name) VALUES ('Small'), ('Medium'), ('Large');
INSERT INTO products (name) VALUES ('T-Shirt'), ('Pants');

-- Generate all product variants
SELECT 
    p.name AS product,
    c.name AS color,
    s.name AS size
FROM products p
CROSS JOIN colors c
CROSS JOIN sizes s
ORDER BY p.name, c.name, s.name;
-- 2 products x 3 colors x 3 sizes = 18 combinations

-- Create SKU table
CREATE TABLE product_skus AS
SELECT 
    p.product_id,
    c.color_id,
    s.size_id,
    CONCAT(
        UPPER(LEFT(p.name, 3)), '-',
        UPPER(LEFT(c.name, 3)), '-',
        UPPER(LEFT(s.name, 1))
    ) AS sku
FROM products p
CROSS JOIN colors c
CROSS JOIN sizes s;

SELECT * FROM product_skus;

-- Sales reporting: ensure all days appear even with no sales
CREATE TABLE stores (store_id SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE daily_sales (store_id INTEGER, sale_date DATE, total DECIMAL(10,2));

INSERT INTO stores (name) VALUES ('Downtown'), ('Mall');
INSERT INTO daily_sales VALUES 
    (1, '2024-01-01', 1000),
    (1, '2024-01-02', 1500),
    (2, '2024-01-02', 800);

-- Complete grid showing zeros for missing days
SELECT 
    s.name AS store,
    d.date,
    COALESCE(ds.total, 0) AS sales
FROM stores s
CROSS JOIN generate_series('2024-01-01'::date, '2024-01-03'::date, '1 day') d(date)
LEFT JOIN daily_sales ds ON s.store_id = ds.store_id AND d.date = ds.sale_date
ORDER BY d.date, s.name;

-- Pair analysis: which products are often bought together?
-- Step 1: Get all product pairs
SELECT 
    p1.name AS product1,
    p2.name AS product2
FROM products p1
CROSS JOIN products p2
WHERE p1.product_id < p2.product_id;  -- Unique pairs only
```

## Key Takeaways

- CROSS JOIN produces all possible row combinations (Cartesian product)
- Result size = rows in table A x rows in table B
- Use intentionally for generating combinations, test data, matrices
- Be careful: missing JOIN condition creates accidental cross join
- Combine with LEFT JOIN for complete grids (all dates, all categories)
- Always consider performance impact before using

## Additional Resources

- [PostgreSQL CROSS JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Cartesian Product](https://en.wikipedia.org/wiki/Cartesian_product)
- [generate_series](https://www.postgresql.org/docs/current/functions-srf.html)
