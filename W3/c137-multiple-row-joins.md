# Multiple Row Joins

## Learning Objectives

- Understand join behavior with duplicate keys
- Handle one-to-many and many-to-many relationships
- Manage row multiplication in joins
- Apply strategies for aggregating joined data

## Why This Matters

When joining tables with one-to-many or many-to-many relationships, a single row from one table can match multiple rows in another, creating row multiplication. Understanding this behavior is essential for accurate reporting and avoiding unexpected result set sizes.

## The Concept

### Row Multiplication in Joins

When one row matches multiple rows, the result expands:

```
customers:           orders:              JOIN result:
| id | name  |       | id | cust_id |     | name  | order_id |
|----|-------|       |----|---------|     |-------|----------|
| 1  | Alice |       | 101| 1       |     | Alice | 101      |
                     | 102| 1       |     | Alice | 102      |
                     | 103| 1       |     | Alice | 103      |

1 customer x 3 orders = 3 result rows
```

### One-to-Many Relationships

```sql
-- One customer, many orders
SELECT c.name, o.order_id, o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
-- If Alice has 5 orders, she appears in 5 rows
```

### Many-to-Many Relationships

With junction tables, multiplication compounds:

```sql
-- students -> enrollments <- courses
SELECT s.name, c.course_name
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id;
-- Each student-course combination is a row
```

### The Multiplication Problem

Row multiplication can cause incorrect aggregates:

```sql
-- WRONG: Alice's name counted multiple times
SELECT c.name, COUNT(*) AS appearance_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
-- Returns order count, not customer count!

-- Example: If you want customer count
SELECT COUNT(DISTINCT c.customer_id) AS customer_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

### Managing Multiplication with DISTINCT

```sql
-- Get unique products ordered (not one per order line)
SELECT DISTINCT p.product_name
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id;

-- Count unique products
SELECT COUNT(DISTINCT p.product_id)
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id;
```

### Aggregating After Join

Aggregate connected data properly:

```sql
-- Customer summary: one row per customer
SELECT 
    c.name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total) AS total_spent,
    AVG(o.total) AS avg_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
-- GROUP BY collapses multiplication back down
```

### When to Join vs Subquery

Sometimes a subquery is cleaner:

```sql
-- Join approach (shows row multiplication then groups)
SELECT 
    p.product_name,
    SUM(oi.quantity) AS total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name;

-- Subquery approach (calculates first, then joins)
SELECT 
    p.product_name,
    sales.total_sold
FROM products p
JOIN (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM order_items
    GROUP BY product_id
) sales ON p.product_id = sales.product_id;
```

### Multi-Level Joins

Multiplication compounds with each join:

```sql
-- categories -> products -> order_items -> orders
-- 1 category x 5 products x 10 orders each = 50 rows per category!

SELECT 
    cat.category_name,
    p.product_name,
    o.order_id,
    oi.quantity
FROM categories cat
JOIN products p ON cat.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id;
```

## Code Example

Understanding and managing row multiplication:

```sql
-- Create tables
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    total DECIMAL(10, 2)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10, 2)
);

-- Insert sample data
INSERT INTO customers (name) VALUES ('Alice'), ('Bob');

INSERT INTO orders (customer_id, order_date, total) VALUES
    (1, '2024-01-01', 100),
    (1, '2024-01-15', 200),
    (1, '2024-02-01', 150),
    (2, '2024-01-10', 75);

INSERT INTO order_items VALUES
    (1, 101, 2, 25), (1, 102, 1, 50),
    (2, 103, 3, 50), (2, 104, 1, 50),
    (3, 101, 1, 25), (3, 105, 5, 25),
    (4, 102, 1, 75);

-- See the multiplication: Alice appears 3 times
SELECT c.name, o.order_id, o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- Further multiplication with order_items
SELECT c.name, o.order_id, oi.product_id, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id;
-- Alice: 3 orders x 2 items each = 6 rows

-- WRONG: Total inflated by row multiplication
SELECT c.name, SUM(o.total) AS wrong_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.name;
-- Alice: 100+100 + 200+200 + 150+150 = 900 (wrong! should be 450)

-- CORRECT: Avoid joining to order_items if not needed
SELECT c.name, SUM(o.total) AS correct_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
-- Alice: 100 + 200 + 150 = 450 (correct)

-- CORRECT: Use DISTINCT or aggregate at right level
SELECT 
    c.name,
    COUNT(DISTINCT o.order_id) AS order_count,
    (SELECT SUM(total) FROM orders WHERE customer_id = c.customer_id) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.name;

-- Pre-aggregate then join (cleanest approach)
WITH order_summary AS (
    SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, os.order_count, os.total_spent
FROM customers c
JOIN order_summary os ON c.customer_id = os.customer_id;
```

## Key Takeaways

- Joins can multiply rows when one row matches many
- One-to-many and many-to-many relationships cause expansion
- Multiplication compounds with each additional join
- Use GROUP BY to collapse back to desired granularity
- Use DISTINCT or COUNT(DISTINCT) for unique counts
- Pre-aggregate in subqueries to avoid multiplication issues

## Additional Resources

- [PostgreSQL Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [GROUP BY](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [DISTINCT](https://www.postgresql.org/docs/current/sql-select.html)
