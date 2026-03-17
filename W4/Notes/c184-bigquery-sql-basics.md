# BigQuery SQL Basics

## Learning Objectives

- Write SELECT queries in BigQuery
- Use WHERE, ORDER BY, and LIMIT clauses
- Apply aggregate functions with GROUP BY
- Understand BigQuery-specific SQL features

## Why This Matters

SQL is the primary interface to BigQuery. Mastering BigQuery SQL enables you to query petabyte-scale datasets efficiently and take advantage of BigQuery-specific optimizations and functions.

## Concept Explanation

### Basic SELECT Query

```sql
-- Simple query
SELECT 
    column1,
    column2,
    column3
FROM `project.dataset.table`
WHERE condition = true
ORDER BY column1 DESC
LIMIT 100;
```

**BigQuery Naming Convention:**

```
`project-id.dataset_name.table_name`
          ^^^^^^^^^^^^^^^^^^^^^^^^^
          Fully qualified table name
```

### SELECT Variations

```sql
-- Select all columns
SELECT * FROM `project.dataset.customers`;

-- Select specific columns with aliases
SELECT 
    customer_id AS id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email
FROM `project.dataset.customers`;

-- Select with expressions
SELECT 
    product_name,
    price,
    quantity,
    price * quantity AS total_value
FROM `project.dataset.products`;

-- DISTINCT values
SELECT DISTINCT category FROM `project.dataset.products`;
```

### WHERE Clause

```sql
-- Comparison operators
SELECT * FROM orders WHERE total_amount > 100;
SELECT * FROM orders WHERE status = 'shipped';
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- Multiple conditions
SELECT * FROM orders 
WHERE status = 'pending' 
  AND total_amount > 50
  AND order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);

-- IN operator
SELECT * FROM products 
WHERE category IN ('Electronics', 'Appliances', 'Computers');

-- LIKE for pattern matching
SELECT * FROM customers 
WHERE email LIKE '%@gmail.com';

-- BETWEEN for ranges
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31';

-- IS NULL / IS NOT NULL
SELECT * FROM customers WHERE phone IS NOT NULL;
```

### ORDER BY and LIMIT

```sql
-- Single column sort
SELECT * FROM orders ORDER BY order_date DESC;

-- Multiple column sort
SELECT * FROM products 
ORDER BY category ASC, price DESC;

-- LIMIT and OFFSET
SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 10;  -- First 10 rows

SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 10 OFFSET 20;  -- Rows 21-30
```

### Aggregate Functions

```sql
-- Basic aggregates
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order
FROM orders;

-- GROUP BY
SELECT 
    status,
    COUNT(*) as order_count,
    SUM(total_amount) as total_amount
FROM orders
GROUP BY status;

-- GROUP BY with multiple columns
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- HAVING (filter after aggregation)
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(total_amount) as total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5 AND SUM(total_amount) > 1000;
```

### JOINs

```sql
-- INNER JOIN
SELECT 
    o.order_id,
    c.name as customer_name,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- LEFT JOIN
SELECT 
    c.name,
    COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;

-- Multiple JOINs
SELECT 
    o.order_id,
    c.name as customer,
    p.name as product,
    oi.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

### Common Table Expressions (CTEs)

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC(order_date, MONTH) as month,
        SUM(total_amount) as revenue
    FROM orders
    GROUP BY month
),
monthly_growth AS (
    SELECT 
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) as prev_month,
        revenue - LAG(revenue) OVER (ORDER BY month) as growth
    FROM monthly_sales
)
SELECT * FROM monthly_growth ORDER BY month;
```

### Subqueries

```sql
-- Subquery in WHERE
SELECT * FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders
    WHERE total_amount > 1000
);

-- Subquery in SELECT
SELECT 
    customer_id,
    name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
FROM customers c;

-- Subquery in FROM
SELECT category, avg_price
FROM (
    SELECT category, AVG(price) as avg_price
    FROM products
    GROUP BY category
) 
WHERE avg_price > 50;
```

## Code Example

```python
from google.cloud import bigquery

client = bigquery.Client()

# Basic query execution
query = """
SELECT 
    DATE_TRUNC(order_date, MONTH) as month,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01'
GROUP BY month
ORDER BY month
"""

results = client.query(query).to_dataframe()
print(results)
```

## Key Takeaways

- Use fully qualified table names: `project.dataset.table`
- WHERE filters rows; HAVING filters groups after aggregation
- GROUP BY enables aggregations; combine with HAVING for filtering
- CTEs (WITH clause) improve readability for complex queries
- JOINs combine data from multiple tables

## Resources

- BigQuery SQL Reference: <https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax>
