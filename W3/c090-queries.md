# Queries

## Learning Objectives

- Write basic SELECT queries to retrieve data
- Use WHERE clauses to filter results
- Apply operators for complex conditions
- Build practical queries for real-world scenarios

## Why This Matters

Queries are how you extract information from databases. Every report, every dashboard, every API response starts with a query. This topic brings together the DQL concepts and prepares you for the more advanced query techniques coming later this week. Strong query skills are essential for any data-related role.

## The Concept

### Query Fundamentals

A query asks the database a question and returns matching data:

```sql
-- The question: "Who works in Engineering?"
SELECT first_name, last_name 
FROM employees 
WHERE department = 'Engineering';
```

### SELECT Clause Options

**Selecting Columns**:

```sql
-- All columns
SELECT * FROM employees;

-- Specific columns
SELECT first_name, last_name FROM employees;

-- With aliases
SELECT first_name AS "First", last_name AS "Last" FROM employees;

-- Expressions
SELECT 
    first_name,
    salary,
    salary * 12 AS annual_salary
FROM employees;
```

**String Concatenation**:

```sql
-- Combine columns
SELECT first_name || ' ' || last_name AS full_name FROM employees;

-- With literals
SELECT 'Employee: ' || first_name || ' ' || last_name AS description 
FROM employees;
```

### WHERE Conditions

**Comparison Operators**:

```sql
-- Equality
SELECT * FROM products WHERE category = 'Electronics';

-- Inequality
SELECT * FROM products WHERE price <> 0;  -- or !=

-- Greater/Less than
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE hire_date >= '2023-01-01';

-- Between (inclusive range)
SELECT * FROM products WHERE price BETWEEN 10 AND 50;

-- NOT BETWEEN
SELECT * FROM products WHERE price NOT BETWEEN 10 AND 50;
```

**Logical Operators**:

```sql
-- AND: Both conditions must be true
SELECT * FROM employees 
WHERE department = 'Sales' AND salary > 60000;

-- OR: Either condition can be true
SELECT * FROM products 
WHERE category = 'Electronics' OR category = 'Computers';

-- NOT: Negates a condition
SELECT * FROM orders WHERE NOT status = 'cancelled';

-- Complex combinations
SELECT * FROM employees 
WHERE (department = 'Engineering' OR department = 'Data Science')
    AND salary >= 80000
    AND hire_date > '2022-01-01';
```

**IN Operator**:

```sql
-- Match any value in a list
SELECT * FROM employees 
WHERE department IN ('Engineering', 'Data Science', 'Product');

-- NOT IN
SELECT * FROM orders 
WHERE status NOT IN ('cancelled', 'refunded');
```

**NULL Handling**:

```sql
-- IS NULL
SELECT * FROM employees WHERE manager_id IS NULL;

-- IS NOT NULL
SELECT * FROM products WHERE description IS NOT NULL;

-- COALESCE: Replace NULL with default
SELECT 
    product_name,
    COALESCE(description, 'No description') AS description
FROM products;
```

**Pattern Matching with LIKE**:

```sql
-- % matches any sequence of characters
SELECT * FROM customers WHERE email LIKE '%@gmail.com';
SELECT * FROM products WHERE name LIKE 'Widget%';  -- Starts with Widget
SELECT * FROM products WHERE name LIKE '%Pro%';    -- Contains Pro

-- _ matches exactly one character
SELECT * FROM products WHERE sku LIKE 'A___';      -- A followed by 3 chars
SELECT * FROM customers WHERE phone LIKE '555-___-____';

-- ILIKE for case-insensitive (PostgreSQL)
SELECT * FROM customers WHERE name ILIKE '%john%';

-- Escape special characters
SELECT * FROM products WHERE name LIKE '%50\%%' ESCAPE '\';  -- Contains "50%"
```

### Sorting Results

```sql
-- Single column
SELECT * FROM products ORDER BY price;

-- Descending
SELECT * FROM products ORDER BY price DESC;

-- Multiple columns
SELECT * FROM employees ORDER BY department, salary DESC;

-- By expression
SELECT *, price * quantity AS total 
FROM order_items 
ORDER BY price * quantity DESC;

-- NULL handling
SELECT * FROM employees ORDER BY manager_id NULLS FIRST;
SELECT * FROM employees ORDER BY manager_id NULLS LAST;
```

### Limiting Results

```sql
-- First N rows
SELECT * FROM products ORDER BY price DESC LIMIT 10;

-- With offset (for pagination)
SELECT * FROM products 
ORDER BY product_id 
LIMIT 20 OFFSET 40;  -- Page 3 with 20 per page

-- Get a single row
SELECT * FROM employees WHERE employee_id = 123 LIMIT 1;
```

### Practical Query Patterns

**Finding specific records**:

```sql
-- Find by ID
SELECT * FROM orders WHERE order_id = 12345;

-- Find by email
SELECT * FROM customers WHERE email = 'john@example.com';
```

**Searching text**:

```sql
-- Product search
SELECT * FROM products 
WHERE name ILIKE '%laptop%' 
   OR description ILIKE '%laptop%'
ORDER BY price;
```

**Date ranges**:

```sql
-- Orders this month
SELECT * FROM orders 
WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE)
    AND order_date < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month';

-- Last 7 days
SELECT * FROM activities 
WHERE activity_date >= CURRENT_DATE - INTERVAL '7 days';
```

**Status filtering**:

```sql
-- Active items only
SELECT * FROM products WHERE is_active = TRUE;

-- Multiple statuses
SELECT * FROM orders 
WHERE status IN ('pending', 'processing', 'shipping')
ORDER BY order_date;
```

## Code Example

Building progressively complex queries:

```sql
-- Sample tables
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_email VARCHAR(100),
    order_date DATE,
    status VARCHAR(20),
    total DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO products (name, category, price, stock) VALUES
    ('Laptop Pro', 'Electronics', 1299.99, 50),
    ('Wireless Mouse', 'Electronics', 29.99, 200),
    ('Office Chair', 'Furniture', 299.99, 30),
    ('USB Cable', 'Electronics', 9.99, 500),
    ('Standing Desk', 'Furniture', 599.99, 15);

INSERT INTO orders (customer_email, order_date, status, total) VALUES
    ('alice@email.com', '2024-01-15', 'completed', 1329.98),
    ('bob@email.com', '2024-01-16', 'pending', 299.99),
    ('carol@email.com', '2024-01-16', 'cancelled', 29.99),
    ('alice@email.com', '2024-01-17', 'completed', 609.98);

-- Query examples
-- Find expensive electronics
SELECT name, price 
FROM products 
WHERE category = 'Electronics' AND price > 100
ORDER BY price DESC;

-- Low stock items
SELECT name, stock 
FROM products 
WHERE stock < 50 AND is_active = TRUE
ORDER BY stock;

-- Search products
SELECT * FROM products 
WHERE name ILIKE '%desk%' OR name ILIKE '%chair%';

-- Recent completed orders
SELECT customer_email, order_date, total 
FROM orders 
WHERE status = 'completed' 
    AND order_date >= '2024-01-01'
ORDER BY order_date DESC;

-- Orders by email domain
SELECT * FROM orders 
WHERE customer_email LIKE '%@email.com'
ORDER BY total DESC
LIMIT 5;

-- Complex filter
SELECT 
    name,
    category,
    price,
    stock,
    price * stock AS inventory_value
FROM products
WHERE (category = 'Electronics' AND price < 50)
   OR (category = 'Furniture' AND stock > 20)
ORDER BY inventory_value DESC;
```

## Key Takeaways

- SELECT retrieves data; specify columns or use * for all
- WHERE filters rows using comparison and logical operators
- Use LIKE/ILIKE for pattern matching
- IS NULL/IS NOT NULL for handling NULL values
- ORDER BY sorts results; LIMIT controls result count
- Combine conditions with AND, OR, and parentheses

## Additional Resources

- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [Pattern Matching](https://www.postgresql.org/docs/current/functions-matching.html)
- [Comparison Operators](https://www.postgresql.org/docs/current/functions-comparison.html)
