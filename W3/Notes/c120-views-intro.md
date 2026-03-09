# Views

## Learning Objectives

- Understand what database views are
- Create and manage views
- Use views for simplification and security
- Recognize view limitations and use cases

## Why This Matters

Views are virtual tables that present data from underlying tables in different ways. They simplify complex queries, provide a security layer by hiding sensitive columns, and create stable interfaces for applications. Understanding views helps you design more maintainable and secure database systems.

## The Concept

### What is a View?

A **view** is a stored query that acts like a virtual table. It does not store data itself; instead, it executes its defining query each time it is accessed.

```sql
-- Create a view
CREATE VIEW active_customers AS
SELECT customer_id, name, email
FROM customers
WHERE is_active = TRUE;

-- Use like a table
SELECT * FROM active_customers;
```

### Creating Views

**Basic view**:

```sql
CREATE VIEW recent_orders AS
SELECT order_id, customer_id, order_date, total
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';
```

**View with joins**:

```sql
CREATE VIEW order_details AS
SELECT 
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

**View with aggregation**:

```sql
CREATE VIEW monthly_sales AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

### CREATE OR REPLACE

Update a view without dropping it:

```sql
-- Create initial view
CREATE VIEW product_summary AS
SELECT product_id, name, price FROM products;

-- Later, modify without breaking dependencies
CREATE OR REPLACE VIEW product_summary AS
SELECT product_id, name, price, category FROM products;
```

Note: You can add columns but cannot remove or change column order.

### View Use Cases

**1. Simplify complex queries**:

```sql
-- Instead of writing this everywhere:
SELECT c.name, COUNT(o.order_id), SUM(o.total)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Create a view:
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Now just:
SELECT * FROM customer_summary WHERE total_spent > 1000;
```

**2. Hide sensitive columns**:

```sql
-- Base table has sensitive data
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    salary DECIMAL(10, 2),  -- Sensitive
    ssn CHAR(11),           -- Sensitive
    department VARCHAR(50)
);

-- Public view hides sensitive columns
CREATE VIEW employees_public AS
SELECT employee_id, name, email, department
FROM employees;

-- Grant access to view, not table
GRANT SELECT ON employees_public TO app_user;
```

**3. Provide stable interface**:

```sql
-- If table structure changes, update view instead of all queries
CREATE VIEW products_api AS
SELECT 
    product_id AS id,
    name AS title,
    price AS unit_price,
    category AS product_category
FROM products;
-- Applications use view; you can change underlying table
```

### Updatable Views

Simple views can be updated:

```sql
CREATE VIEW active_products AS
SELECT product_id, name, price, category
FROM products
WHERE is_active = TRUE;

-- Insert through view
INSERT INTO active_products (name, price, category)
VALUES ('New Product', 29.99, 'Electronics');
-- Inserts into products table

-- Update through view
UPDATE active_products SET price = 24.99 WHERE product_id = 1;
```

**Restrictions**: Views with joins, aggregates, DISTINCT, GROUP BY, etc. are not usually updatable.

### WITH CHECK OPTION

Prevent inserts/updates that would disappear from the view:

```sql
CREATE VIEW expensive_products AS
SELECT product_id, name, price
FROM products
WHERE price >= 100
WITH CHECK OPTION;

-- This works
INSERT INTO expensive_products (name, price) VALUES ('Premium Item', 150);

-- This fails (violates WHERE condition)
INSERT INTO expensive_products (name, price) VALUES ('Cheap Item', 50);
-- ERROR: new row violates check option for view
```

### Materialized Views

**Materialized views** store the query result for faster access:

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW monthly_stats AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Query it (fast - reads stored data)
SELECT * FROM monthly_stats;

-- Refresh when underlying data changes
REFRESH MATERIALIZED VIEW monthly_stats;

-- Refresh without blocking reads
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_stats;
```

### Managing Views

```sql
-- Drop view
DROP VIEW customer_summary;
DROP VIEW IF EXISTS old_view;

-- Drop with dependent views
DROP VIEW base_view CASCADE;

-- Rename view
ALTER VIEW old_name RENAME TO new_name;

-- Change owner
ALTER VIEW customer_summary OWNER TO admin;
```

## Code Example

Comprehensive view usage:

```sql
-- Create base tables
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,  -- Internal data
    stock INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO categories (name) VALUES ('Electronics'), ('Clothing'), ('Home');
INSERT INTO products (name, category_id, price, cost, stock) VALUES
    ('Laptop', 1, 999.99, 600.00, 50),
    ('Phone', 1, 599.99, 350.00, 100),
    ('T-Shirt', 2, 29.99, 10.00, 200),
    ('Jeans', 2, 79.99, 30.00, 75),
    ('Lamp', 3, 49.99, 15.00, 30);

-- View 1: Product catalog (hides cost)
CREATE VIEW product_catalog AS
SELECT 
    p.product_id,
    p.name AS product_name,
    c.name AS category,
    p.price,
    p.stock,
    CASE WHEN p.stock > 0 THEN 'In Stock' ELSE 'Out of Stock' END AS availability
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.is_active = TRUE;

SELECT * FROM product_catalog;

-- View 2: Inventory management (includes internal data)
CREATE VIEW inventory_report AS
SELECT 
    p.product_id,
    p.name,
    p.stock,
    p.cost,
    p.stock * p.cost AS inventory_value,
    p.price - p.cost AS profit_margin
FROM products p;

SELECT * FROM inventory_report ORDER BY inventory_value DESC;

-- View 3: Low stock alerts
CREATE VIEW low_stock_alert AS
SELECT product_id, name, stock, category_id
FROM products
WHERE stock < 50 AND is_active = TRUE
WITH CHECK OPTION;

SELECT * FROM low_stock_alert;

-- Materialized view for performance
CREATE MATERIALIZED VIEW category_summary AS
SELECT 
    c.name AS category,
    COUNT(p.product_id) AS product_count,
    AVG(p.price) AS avg_price,
    SUM(p.stock) AS total_stock
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.name;

SELECT * FROM category_summary;

-- Refresh materializd view
REFRESH MATERIALIZED VIEW category_summary;
```

## Key Takeaways

- Views are stored queries that act as virtual tables
- Use views to simplify queries, hide data, and provide stable interfaces
- Simple views can be updatable; complex views are read-only
- WITH CHECK OPTION prevents disappearing rows
- Materialized views cache results for performance
- Use CREATE OR REPLACE to modify views safely

## Additional Resources

- [PostgreSQL Views](https://www.postgresql.org/docs/current/sql-createview.html)
- [Materialized Views](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- [Updatable Views](https://www.postgresql.org/docs/current/sql-createview.html#SQL-CREATEVIEW-UPDATABLE-VIEWS)
