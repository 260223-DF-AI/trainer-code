# RIGHT JOIN

## Learning Objectives

- Understand RIGHT JOIN behavior
- Write RIGHT JOIN queries
- Compare RIGHT JOIN with LEFT JOIN
- Recognize when RIGHT JOIN vs LEFT JOIN is appropriate

## Why This Matters

RIGHT JOIN is the mirror of LEFT JOIN, preserving all rows from the right table. While LEFT JOIN is more commonly used, understanding RIGHT JOIN helps you choose the best approach for your data and sometimes leads to more readable queries.

## The Concept

### What is RIGHT JOIN?

**RIGHT JOIN** (or RIGHT OUTER JOIN) returns all rows from the right table, plus matching rows from the left table. Unmatched rows from the left produce NULL values.

```
orders (left):       customers (right):   RIGHT JOIN result:
| id | cust_id |     | id | name  |       | order_id | name  |
|----|---------|     |----|-------|       |----------|-------|
| 101| 1       |     | 1  | Alice |       | 101      | Alice |
| 102| 2       |     | 2  | Bob   |       | 103      | Alice |
| 103| 1       |     | 3  | Carol |       | 102      | Bob   |
                                          | NULL     | Carol |

Carol is included even though she has no orders
```

### Basic Syntax

```sql
SELECT columns
FROM left_table
RIGHT JOIN right_table ON left_table.column = right_table.column;

-- RIGHT OUTER JOIN is identical
SELECT columns
FROM left_table
RIGHT OUTER JOIN right_table ON left_table.column = right_table.column;
```

### RIGHT JOIN Examples

**Basic usage**:

```sql
-- All departments with their employees (if any)
SELECT e.name AS employee, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.department_id;
```

**Finding records without matches**:

```sql
-- Departments with no employees
SELECT d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.department_id
WHERE e.employee_id IS NULL;
```

### RIGHT JOIN vs LEFT JOIN

RIGHT JOIN and LEFT JOIN are interchangeable by swapping table positions:

```sql
-- These produce identical results:

-- Using RIGHT JOIN
SELECT c.name, o.order_id
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;

-- Using LEFT JOIN (swapped table order)
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

### When to Use RIGHT JOIN

**Prefer LEFT JOIN** in most cases for consistency and readability. Use RIGHT JOIN when:

1. **The main entity is naturally on the right**:

```sql
-- When department summary is the focus
SELECT COUNT(e.emp_id), d.dept_name
FROM employee_assignments ea
JOIN employees e ON ea.emp_id = e.emp_id
RIGHT JOIN departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name;
```

1. **Adding a "master list" at the end of a join chain**:

```sql
-- Ensure all products appear even without sales
SELECT s.sale_date, s.quantity, p.product_name
FROM sales s
RIGHT JOIN products p ON s.product_id = p.product_id;
```

### RIGHT JOIN with Multiple Tables

```sql
-- All departments with optional employee and project info
SELECT 
    d.dept_name,
    e.name AS employee,
    p.project_name
FROM projects p
JOIN assignments a ON p.project_id = a.project_id
JOIN employees e ON a.employee_id = e.employee_id
RIGHT JOIN departments d ON e.department_id = d.department_id;
```

### Consistency Recommendation

Most SQL developers standardize on LEFT JOIN:

```sql
-- Easier to read: LEFT JOIN with main entity first
SELECT 
    d.dept_name,
    COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.dept_name;
```

## Code Example

Comprehensive RIGHT JOIN usage:

```sql
-- Create tables
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category_id INTEGER REFERENCES categories(category_id),
    price DECIMAL(10, 2)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    sale_date DATE
);

-- Insert sample data
INSERT INTO categories (category_name) VALUES 
    ('Electronics'), ('Clothing'), ('Books'), ('Home');

INSERT INTO products (name, category_id, price) VALUES
    ('Laptop', 1, 999.99),
    ('Phone', 1, 599.99),
    ('T-Shirt', 2, 29.99),
    ('Novel', 3, 14.99);
-- Note: 'Home' category has no products

INSERT INTO sales (product_id, quantity, sale_date) VALUES
    (1, 5, '2024-01-15'),
    (2, 10, '2024-01-16'),
    (1, 3, '2024-01-17');
-- Note: T-Shirt and Novel have no sales

-- RIGHT JOIN: All categories with their products
SELECT 
    p.name AS product,
    c.category_name
FROM products p
RIGHT JOIN categories c ON p.category_id = c.category_id
ORDER BY c.category_name;
-- 'Home' appears with NULL product

-- Equivalent LEFT JOIN (preferred style)
SELECT 
    p.name AS product,
    c.category_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
ORDER BY c.category_name;

-- Find empty categories using RIGHT JOIN
SELECT c.category_name AS empty_category
FROM products p
RIGHT JOIN categories c ON p.category_id = c.category_id
WHERE p.product_id IS NULL;
-- Returns: Home

-- All products with their sales (if any) - comparing approaches
-- RIGHT JOIN approach
SELECT 
    s.sale_date,
    s.quantity,
    p.name AS product
FROM sales s
RIGHT JOIN products p ON s.product_id = p.product_id
ORDER BY p.name;

-- Equivalent LEFT JOIN approach (more common)
SELECT 
    s.sale_date,
    s.quantity,
    p.name AS product
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
ORDER BY p.name;

-- Report: All categories with product count and sales
SELECT 
    c.category_name,
    COUNT(DISTINCT p.product_id) AS product_count,
    COALESCE(SUM(s.quantity), 0) AS total_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
RIGHT JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY c.category_name;
```

## Key Takeaways

- RIGHT JOIN preserves all rows from the right table
- LEFT JOIN and RIGHT JOIN are interchangeable by swapping table order
- Most developers prefer LEFT JOIN for consistency
- RIGHT JOIN is useful when the "master" table is naturally on the right
- Use WHERE ... IS NULL to find unmatched records

## Additional Resources

- [PostgreSQL RIGHT JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Outer Joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
- [JOIN Types Comparison](https://www.postgresql.org/docs/current/sql-select.html)
