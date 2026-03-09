# Subqueries

## Learning Objectives

- Understand what subqueries are and when to use them
- Write subqueries in SELECT, FROM, and WHERE clauses
- Distinguish between correlated and non-correlated subqueries
- Use EXISTS, IN, and comparison operators with subqueries

## Why This Matters

Subqueries enable complex data retrieval that would otherwise require multiple queries or application logic. They allow you to filter based on aggregations, compare values across tables, and build sophisticated analysis queries. Mastering subqueries significantly expands your SQL capabilities.

## The Concept

### What is a Subquery?

A **subquery** (or inner query) is a query nested inside another query. The outer query uses the result of the inner query.

```sql
-- Find products with above-average price
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
--             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--             This is the subquery
```

### Types of Subqueries

| Type | Returns | Used With |
|------|---------|-----------|
| Scalar | Single value | =, >, <, etc. |
| Row | Single row | = (row), IN |
| Table | Multiple rows/columns | IN, EXISTS, FROM |

### Subquery in WHERE Clause

**Scalar subquery (single value)**:

```sql
-- Products above average price
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Orders placed after the last order from customer 1
SELECT * FROM orders
WHERE order_date > (SELECT MAX(order_date) FROM orders WHERE customer_id = 1);
```

**List subquery (multiple values with IN)**:

```sql
-- Customers who have placed orders
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Products never ordered
SELECT * FROM products
WHERE product_id NOT IN (SELECT product_id FROM order_items);
```

**EXISTS subquery**:

```sql
-- Customers with at least one order
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Customers with no orders
SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

### Subquery in FROM Clause

Creates a derived table (must be aliased):

```sql
-- Find departments with above-average headcount
SELECT department, employee_count
FROM (
    SELECT department, COUNT(*) AS employee_count
    FROM employees
    GROUP BY department
) AS dept_counts
WHERE employee_count > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(*) AS cnt FROM employees GROUP BY department
    ) AS avg_calc
);
```

### Subquery in SELECT Clause

Calculates a value for each row:

```sql
-- Show each employee's salary compared to department average
SELECT 
    first_name,
    department,
    salary,
    (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e1.department) AS dept_avg
FROM employees e1;

-- Show each order with customer name
SELECT 
    order_id,
    order_date,
    (SELECT name FROM customers c WHERE c.customer_id = o.customer_id) AS customer_name
FROM orders o;
```

### Correlated vs Non-Correlated Subqueries

**Non-correlated**: Runs once, independently of outer query

```sql
-- Subquery runs once, returns one value
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

**Correlated**: Runs once per row of outer query

```sql
-- Subquery references outer query (e1.department)
SELECT * FROM employees e1
WHERE salary > (
    SELECT AVG(salary) FROM employees e2 
    WHERE e2.department = e1.department  -- References outer query!
);
```

### ALL, ANY, SOME

Compare to all/any values from subquery:

```sql
-- Higher than ALL prices in Electronics
SELECT * FROM products
WHERE price > ALL (SELECT price FROM products WHERE category = 'Electronics');

-- Higher than ANY price in Electronics (same as > MIN)
SELECT * FROM products
WHERE price > ANY (SELECT price FROM products WHERE category = 'Electronics');

-- SOME is alias for ANY
SELECT * FROM products
WHERE price > SOME (SELECT price FROM products WHERE category = 'Electronics');
```

### Common Subquery Patterns

**1. Top N per group**:

```sql
-- Highest paid employee per department
SELECT * FROM employees e1
WHERE salary = (
    SELECT MAX(salary) FROM employees e2 
    WHERE e2.department = e1.department
);
```

**2. Compare to aggregate**:

```sql
-- Products selling above category average
SELECT * FROM products p
WHERE price > (
    SELECT AVG(price) FROM products 
    WHERE category = p.category
);
```

**3. Existence checks**:

```sql
-- Active products (have been ordered recently)
SELECT * FROM products p
WHERE EXISTS (
    SELECT 1 FROM order_items oi 
    JOIN orders o ON oi.order_id = o.order_id
    WHERE oi.product_id = p.product_id 
    AND o.order_date > CURRENT_DATE - INTERVAL '30 days'
);
```

## Code Example

Comprehensive subquery usage:

```sql
-- Sample tables
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);

-- Insert sample data
INSERT INTO products VALUES
    (1, 'Laptop', 'Electronics', 999),
    (2, 'Mouse', 'Electronics', 30),
    (3, 'Chair', 'Furniture', 200),
    (4, 'Desk', 'Furniture', 400),
    (5, 'Monitor', 'Electronics', 350);

INSERT INTO orders VALUES
    (1, 101, '2024-01-15'),
    (2, 102, '2024-01-20');

INSERT INTO order_items VALUES
    (1, 1, 1), (1, 2, 2),
    (2, 3, 1);

-- Scalar subquery: products above average price
SELECT name, price,
       (SELECT AVG(price) FROM products) AS avg_price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- IN subquery: products that have been ordered
SELECT * FROM products
WHERE product_id IN (SELECT product_id FROM order_items);

-- NOT IN: products never ordered
SELECT * FROM products
WHERE product_id NOT IN (SELECT product_id FROM order_items);

-- EXISTS: categories with expensive products
SELECT DISTINCT category FROM products p1
WHERE EXISTS (
    SELECT 1 FROM products p2 
    WHERE p2.category = p1.category AND p2.price > 300
);

-- Correlated: products above their category average
SELECT name, category, price,
       (SELECT AVG(price) FROM products p2 WHERE p2.category = p1.category) AS cat_avg
FROM products p1
WHERE price > (SELECT AVG(price) FROM products p2 WHERE p2.category = p1.category);

-- FROM clause: category statistics
SELECT category, product_count, total_value
FROM (
    SELECT category,
           COUNT(*) AS product_count,
           SUM(price) AS total_value
    FROM products
    GROUP BY category
) AS category_stats
WHERE product_count >= 2;

-- Complex: orders with their total value
SELECT 
    o.order_id,
    o.order_date,
    (SELECT SUM(p.price * oi.quantity) 
     FROM order_items oi 
     JOIN products p ON oi.product_id = p.product_id 
     WHERE oi.order_id = o.order_id) AS order_total
FROM orders o;
```

## Key Takeaways

- Subqueries are queries nested inside other queries
- Use scalar subqueries with comparison operators (=, >, <)
- Use list subqueries with IN, NOT IN
- EXISTS checks for row presence (often faster than IN)
- Correlated subqueries reference the outer query; run per row
- Subqueries in FROM create derived tables (need aliases)

## Additional Resources

- [PostgreSQL Subqueries](https://www.postgresql.org/docs/current/functions-subquery.html)
- [EXISTS](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS)
- [Scalar Subqueries](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
