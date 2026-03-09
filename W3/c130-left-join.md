# LEFT JOIN

## Learning Objectives

- Understand LEFT JOIN behavior
- Write LEFT JOIN queries
- Handle NULL values in LEFT JOIN results
- Recognize when to use LEFT JOIN vs INNER JOIN

## Why This Matters

LEFT JOIN preserves all rows from the left table regardless of whether they have matches. This is essential for finding records without relationships, generating complete reports, and ensuring no data is lost during joins.

## The Concept

### What is LEFT JOIN?

**LEFT JOIN** (or LEFT OUTER JOIN) returns all rows from the left table, plus matching rows from the right table. Unmatched rows from the right table result in NULL values.

```
customers (left):    orders (right):      LEFT JOIN result:
| id | name  |       | id | cust_id |     | name  | order_id |
|----|-------|       |----|---------|     |-------|----------|
| 1  | Alice |       | 101| 1       |     | Alice | 101      |
| 2  | Bob   |       | 102| 2       |     | Alice | 103      |
| 3  | Carol |       | 103| 1       |     | Bob   | 102      |
                                          | Carol | NULL     |

Carol is included even though she has no orders
```

### Basic Syntax

```sql
-- Full syntax
SELECT columns
FROM left_table
LEFT OUTER JOIN right_table ON left_table.column = right_table.column;

-- Short syntax (OUTER is optional)
SELECT columns
FROM left_table
LEFT JOIN right_table ON left_table.column = right_table.column;
```

### LEFT JOIN Examples

**Basic usage**:

```sql
-- All customers, with their orders if they have any
SELECT c.name, o.order_id, o.total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**Handling NULL values**:

```sql
SELECT 
    c.name,
    COALESCE(o.order_id::TEXT, 'No orders') AS order_info,
    COALESCE(o.total, 0) AS total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

### Finding Records Without Matches

Common pattern: Find rows in the left table that have no corresponding rows in the right table:

```sql
-- Customers with no orders
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Products never ordered
SELECT p.name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- Employees without departments
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id
WHERE d.department_id IS NULL;
```

### LEFT JOIN vs INNER JOIN

| Scenario | Use |
|----------|-----|
| Need ALL left records | LEFT JOIN |
| Only care about matches | INNER JOIN |
| Finding orphan records | LEFT JOIN + WHERE ... IS NULL |
| Complete reports | LEFT JOIN |

```sql
-- INNER JOIN: Only customers WITH orders
SELECT c.name, COUNT(o.order_id)
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
-- Carol (no orders) excluded

-- LEFT JOIN: All customers, including those without orders
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
-- Carol appears with count = 0
```

### Multiple LEFT JOINs

Chain LEFT JOINs carefully:

```sql
SELECT 
    c.name AS customer,
    o.order_id,
    p.name AS product
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id;
-- Preserves all customers throughout the chain
```

### LEFT JOIN with Aggregation

```sql
-- Order count per customer (including zeros)
SELECT 
    c.name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```

### Join Condition vs WHERE

Be careful with filter placement:

```sql
-- WRONG: WHERE filters out NULL rows
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total > 100;
-- Customers without orders are excluded!

-- CORRECT: Put condition in ON clause
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.total > 100;
-- Customers without high-value orders show NULL, but are included
```

## Code Example

Comprehensive LEFT JOIN usage:

```sql
-- Create tables
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INTEGER REFERENCES authors(author_id),
    published_year INTEGER
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(book_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT
);

-- Insert sample data
INSERT INTO authors (name) VALUES 
    ('Alice Author'), ('Bob Writer'), ('Carol Creator');

INSERT INTO books (title, author_id, published_year) VALUES
    ('SQL Basics', 1, 2022),
    ('Advanced SQL', 1, 2023),
    ('Database Design', 2, 2021);
-- Carol has no books

INSERT INTO reviews (book_id, rating, review_text) VALUES
    (1, 5, 'Great book!'),
    (1, 4, 'Very helpful'),
    (3, 3, 'Okay');
-- 'Advanced SQL' has no reviews

-- All authors with their books (if any)
SELECT 
    a.name AS author,
    b.title AS book,
    b.published_year
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
ORDER BY a.name, b.published_year;
-- Carol appears with NULL book

-- Authors without books
SELECT a.name AS author_without_books
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
WHERE b.book_id IS NULL;
-- Returns: Carol Creator

-- All books with their reviews (if any)
SELECT 
    b.title,
    r.rating,
    r.review_text
FROM books b
LEFT JOIN reviews r ON b.book_id = r.book_id
ORDER BY b.title;
-- 'Advanced SQL' appears with NULL review

-- Book statistics (including books with no reviews)
SELECT 
    b.title,
    COUNT(r.review_id) AS review_count,
    COALESCE(ROUND(AVG(r.rating), 1), 0) AS avg_rating
FROM books b
LEFT JOIN reviews r ON b.book_id = r.book_id
GROUP BY b.book_id, b.title
ORDER BY avg_rating DESC;

-- Complete author-book-review chain
SELECT 
    a.name AS author,
    COALESCE(b.title, 'No books') AS book,
    COALESCE(r.rating::TEXT, 'No reviews') AS rating
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
LEFT JOIN reviews r ON b.book_id = r.book_id
ORDER BY a.name, b.title;
```

## Key Takeaways

- LEFT JOIN keeps all rows from the left table
- Non-matching right rows produce NULL values
- Use WHERE ... IS NULL to find unmatched records
- LEFT OUTER JOIN and LEFT JOIN are identical
- Place additional filters in ON clause to preserve left rows
- Essential for finding orphan records and complete reports

## Additional Resources

- [PostgreSQL LEFT JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Outer Joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
- [COALESCE](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-COALESCE-NVL-IFNULL)
