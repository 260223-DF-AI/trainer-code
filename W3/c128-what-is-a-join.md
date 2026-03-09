# Introduction to JOINs

## Learning Objectives

- Understand why joins are necessary
- Recognize the purpose of combining tables
- Identify the basic join concept
- Prepare for learning specific join types

## Why This Matters

Relational databases store data across multiple related tables to reduce redundancy and maintain data integrity. Joins are the mechanism that brings this distributed data back together. Without joins, you would need separate queries and manual data combination. Joins are fundamental to working with relational databases.

## The Concept

### Why Do We Need JOINs?

In normalized databases, related data is split across tables:

```
customers table:                  orders table:
+-------------+------------+      +----------+-------------+--------+
| customer_id | name       |      | order_id | customer_id | total  |
+-------------+------------+      +----------+-------------+--------+
|     1       | Alice      |      |    101   |      1      | 150.00 |
|     2       | Bob        |      |    102   |      2      |  75.50 |
|     3       | Carol      |      |    103   |      1      | 200.00 |
+-------------+------------+      +----------+-------------+--------+
```

Problem: How do we see "Alice, Order #101, $150.00" in one row?

Solution: **JOIN the tables**.

### What is a JOIN?

A **JOIN** combines rows from two or more tables based on a related column:

```sql
SELECT customers.name, orders.order_id, orders.total
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id;

-- Result:
-- | name  | order_id | total  |
-- |-------|----------|--------|
-- | Alice | 101      | 150.00 |
-- | Bob   | 102      | 75.50  |
-- | Alice | 103      | 200.00 |
```

### The Join Condition

The **ON** clause specifies how tables are related:

```sql
-- Match rows where customer_id is the same in both tables
JOIN orders ON customers.customer_id = orders.customer_id
```

This is typically:

- Primary key from one table
- Foreign key from another table

### Types of JOINs

SQL provides several join types for different scenarios:

| JOIN Type | Returns |
|-----------|---------|
| INNER JOIN | Only matching rows from both tables |
| LEFT JOIN | All rows from left table, matching from right |
| RIGHT JOIN | All rows from right table, matching from left |
| FULL JOIN | All rows from both tables |
| CROSS JOIN | All possible combinations (Cartesian product) |

### Visualizing JOINs

```
      A       B
    +---+   +---+
    | 1 |   | 2 |
    | 2 |   | 3 |
    | 3 |   | 4 |
    +---+   +---+

INNER JOIN (only matching):     2, 3
LEFT JOIN (all from A):         1, 2, 3
RIGHT JOIN (all from B):        2, 3, 4
FULL JOIN (all from both):      1, 2, 3, 4
CROSS JOIN (all combinations):  1-2, 1-3, 1-4, 2-2, 2-3, 2-4, 3-2, 3-3, 3-4
```

### Basic JOIN Syntax

```sql
SELECT column_list
FROM table1
JOIN table2 ON table1.column = table2.column;
```

With table aliases (preferred):

```sql
SELECT c.name, o.order_id, o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

### Multiple Joins

Chain joins to combine more than two tables:

```sql
SELECT c.name, o.order_id, p.product_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

### Join vs Subquery

Many scenarios can use either approach:

```sql
-- Using JOIN
SELECT c.name, o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- Using subquery
SELECT 
    c.name,
    (SELECT SUM(total) FROM orders o WHERE o.customer_id = c.customer_id) AS total
FROM customers c;
```

Joins are typically more readable and often more efficient for combining data.

## Code Example

Introduction to joining tables:

```sql
-- Create related tables
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    total DECIMAL(10, 2)
);

-- Insert sample data
INSERT INTO customers (name, email) VALUES
    ('Alice Johnson', 'alice@email.com'),
    ('Bob Smith', 'bob@email.com'),
    ('Carol Williams', 'carol@email.com');

INSERT INTO orders (customer_id, order_date, total) VALUES
    (1, '2024-01-15', 150.00),
    (2, '2024-01-16', 75.50),
    (1, '2024-01-17', 200.00),
    (2, '2024-01-18', 125.00);

-- Query each table separately
SELECT * FROM customers;
SELECT * FROM orders;

-- JOIN to see customer info with their orders
SELECT 
    c.name AS customer_name,
    c.email,
    o.order_id,
    o.order_date,
    o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.name, o.order_date;

-- Notice: Carol has no orders, so she doesn't appear
-- We'll address this with LEFT JOIN in the next topic
```

## Key Takeaways

- JOINs combine data from multiple related tables
- The ON clause specifies the matching condition (usually PK = FK)
- INNER JOIN returns only matching rows
- Different join types handle non-matching rows differently
- Table aliases make join queries more readable
- Joins are essential for working with normalized databases

## Additional Resources

- [PostgreSQL JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [Visual Representation of SQL Joins](https://blog.codinghorror.com/a-visual-explanation-of-sql-joins/)
- [Join Types](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
