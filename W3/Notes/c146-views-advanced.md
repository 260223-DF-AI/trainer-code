# Views - Advanced Features

## Learning Objectives

- Create views for complex query encapsulation
- Understand materialized views for performance
- Implement updatable views with proper rules
- Apply views for security and data abstraction

## Why This Matters

Views provide a powerful abstraction layer over your database. They simplify complex queries, enforce security boundaries, and present data in application-friendly formats. Materialized views can dramatically improve performance for expensive queries. Understanding views helps you design cleaner, more maintainable database interfaces.

## The Concept

### What is a View?

A view is a virtual table based on a SQL query. It doesn't store data but retrieves it dynamically when queried.

```
View = Saved Query + Table Interface
```

### Creating Views

```sql
-- Simple view
CREATE VIEW active_customers AS
SELECT customer_id, name, email
FROM customers
WHERE is_active = TRUE;

-- Complex view with joins
CREATE VIEW order_summary AS
SELECT 
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    SUM(oi.quantity * oi.unit_price) AS total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, c.name, o.order_date;
```

### Using Views

```sql
-- Query like a table
SELECT * FROM active_customers WHERE name LIKE 'A%';

-- Join with other tables
SELECT v.*, p.name AS product
FROM order_summary v
JOIN products p ON v.product_id = p.product_id;
```

### Updatable Views

Simple views on single tables can be updatable:

```sql
CREATE VIEW california_customers AS
SELECT customer_id, name, email, state
FROM customers
WHERE state = 'CA';

-- Insert through view
INSERT INTO california_customers (name, email, state)
VALUES ('Alice', 'alice@email.com', 'CA');

-- Update through view
UPDATE california_customers SET email = 'new@email.com' WHERE customer_id = 1;

-- Delete through view
DELETE FROM california_customers WHERE customer_id = 1;
```

### WITH CHECK OPTION

Prevent inserts/updates that would disappear from the view:

```sql
CREATE VIEW california_customers AS
SELECT customer_id, name, email, state
FROM customers
WHERE state = 'CA'
WITH CHECK OPTION;

-- This fails - row wouldn't appear in view
INSERT INTO california_customers (name, email, state)
VALUES ('Bob', 'bob@email.com', 'NY');
-- Error: new row violates check option
```

### Materialized Views

Store query results for faster access:

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW sales_by_month AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- Query is instant (reads stored data)
SELECT * FROM sales_by_month WHERE month >= '2024-01-01';

-- Refresh when underlying data changes
REFRESH MATERIALIZED VIEW sales_by_month;

-- Refresh without blocking reads
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_by_month;
```

### Materialized View Features

```sql
-- Create with index for faster access
CREATE MATERIALIZED VIEW product_stats AS
SELECT 
    p.product_id,
    p.name,
    COUNT(oi.item_id) AS times_ordered,
    SUM(oi.quantity) AS total_quantity
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name;

-- Add unique index for concurrent refresh
CREATE UNIQUE INDEX idx_product_stats_id ON product_stats(product_id);

-- Now concurrent refresh works
REFRESH MATERIALIZED VIEW CONCURRENTLY product_stats;
```

### Security Views

Hide sensitive columns:

```sql
-- Full employee table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    salary DECIMAL(10,2),
    ssn VARCHAR(11),
    hire_date DATE
);

-- View without sensitive data
CREATE VIEW employee_directory AS
SELECT employee_id, name, email, hire_date
FROM employees;

-- Grant access to view, not table
REVOKE ALL ON employees FROM PUBLIC;
GRANT SELECT ON employee_directory TO reporting_role;
```

### Row-Level Security with Views

```sql
-- Managers see only their team
CREATE VIEW my_team AS
SELECT * FROM employees
WHERE manager_id = CURRENT_USER_ID();

-- Regional data access
CREATE VIEW regional_orders AS
SELECT * FROM orders
WHERE region = GET_USER_REGION();
```

### Replacing Views

```sql
-- Modify view definition
CREATE OR REPLACE VIEW active_customers AS
SELECT customer_id, name, email, phone
FROM customers
WHERE is_active = TRUE AND verified = TRUE;
```

### Managing Views

```sql
-- List views
\dv
-- or
SELECT table_name FROM information_schema.views 
WHERE table_schema = 'public';

-- View definition
\d+ active_customers
-- or
SELECT definition FROM pg_views WHERE viewname = 'active_customers';

-- Drop views
DROP VIEW active_customers;
DROP VIEW IF EXISTS active_customers CASCADE;

-- Drop materialized view
DROP MATERIALIZED VIEW sales_by_month;
```

### Complete Example

```sql
-- Setup tables
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),  -- Sensitive!
    stock INTEGER
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    sale_price DECIMAL(10,2),
    order_date DATE
);

-- Regular view for product catalog (hides cost)
CREATE VIEW product_catalog AS
SELECT product_id, name, category, price, stock
FROM products
WHERE stock > 0;

-- Materialized view for sales analytics
CREATE MATERIALIZED VIEW product_performance AS
SELECT 
    p.product_id,
    p.name,
    p.category,
    COUNT(oi.item_id) AS total_orders,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    COALESCE(SUM(oi.quantity * oi.sale_price), 0) AS revenue,
    COALESCE(SUM(oi.quantity * (oi.sale_price - p.cost)), 0) AS profit
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category;

CREATE UNIQUE INDEX idx_perf_product ON product_performance(product_id);

-- Query the views
SELECT * FROM product_catalog WHERE category = 'Electronics';
SELECT * FROM product_performance ORDER BY profit DESC LIMIT 10;

-- Refresh materialized view nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY product_performance;
```

## Key Takeaways

- Views encapsulate complex queries as virtual tables
- Simple views on single tables can be updated
- WITH CHECK OPTION enforces view constraints on inserts
- Materialized views store results for fast access
- Use REFRESH MATERIALIZED VIEW to update stored data
- Views provide security by hiding sensitive columns
- Replace views with CREATE OR REPLACE VIEW

## Additional Resources

- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [Materialized Views](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- [Updatable Views](https://www.postgresql.org/docs/current/sql-createview.html#SQL-CREATEVIEW-UPDATABLE-VIEWS)
