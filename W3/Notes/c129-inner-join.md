# INNER JOIN

## Learning Objectives

- Understand INNER JOIN behavior
- Write INNER JOIN queries
- Recognize when to use INNER JOIN
- Understand the implications of excluding non-matching rows

## Why This Matters

INNER JOIN is the most common and fundamental join type. It returns only the rows where a match exists in both tables. Understanding INNER JOIN is essential because it forms the basis for understanding all other join types.

## The Concept

### What is INNER JOIN?

**INNER JOIN** returns only rows where the join condition is satisfied in both tables. Rows without a match in either table are excluded.

```
customers:           orders:              INNER JOIN result:
| id | name  |       | id | cust_id |     | name  | order_id |
|----|-------|       |----|---------|     |-------|----------|
| 1  | Alice |       | 101| 1       |     | Alice | 101      |
| 2  | Bob   |       | 102| 2       |     | Alice | 103      |
| 3  | Carol |       | 103| 1       |     | Bob   | 102      |
                                          
Carol (id=3) has no orders, so excluded from result
```

### Basic Syntax

```sql
-- Explicit INNER JOIN
SELECT columns
FROM table1
INNER JOIN table2 ON table1.column = table2.column;

-- JOIN without INNER keyword (same behavior)
SELECT columns
FROM table1
JOIN table2 ON table1.column = table2.column;
```

### INNER JOIN Examples

**Basic join**:

```sql
SELECT c.name, o.order_id, o.total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

**With additional conditions**:

```sql
SELECT c.name, o.order_id, o.total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total > 100;
```

**Multiple columns in join condition**:

```sql
SELECT *
FROM table1 t1
INNER JOIN table2 t2 ON t1.col1 = t2.col1 AND t1.col2 = t2.col2;
```

### Multiple INNER JOINs

Chain joins to combine multiple tables:

```sql
SELECT 
    c.name AS customer,
    o.order_id,
    p.name AS product,
    oi.quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

### When to Use INNER JOIN

Use INNER JOIN when:

- You only want rows that have matches in both tables
- Missing relationships indicate data problems (you want to exclude them)
- You need complete data from both tables for your analysis

```sql
-- Products with their categories (only if category exists)
SELECT p.name, c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id;

-- Employees with their departments
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;
```

### Understanding Non-Matches

INNER JOIN excludes rows without matches:

```sql
-- If a customer has no orders:
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
-- Customer with no orders will NOT appear

-- If a product has no category_id:
SELECT p.name, c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id;
-- Product with NULL category_id will NOT appear
```

### INNER JOIN vs Comma Syntax

Old style (avoid in modern SQL):

```sql
-- Old comma syntax
SELECT c.name, o.order_id
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;

-- Modern explicit JOIN (preferred)
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

The explicit JOIN syntax is clearer and separates join conditions from filters.

### Self-Join with INNER JOIN

Join a table to itself:

```sql
-- Find employees and their managers
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
INNER JOIN employees m ON e.manager_id = m.employee_id;
-- Only employees WITH managers appear (excludes top-level)
```

## Code Example

Comprehensive INNER JOIN usage:

```sql
-- Create tables
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    dept_id INTEGER REFERENCES departments(dept_id),
    manager_id INTEGER
);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100)
);

CREATE TABLE assignments (
    emp_id INTEGER REFERENCES employees(emp_id),
    project_id INTEGER REFERENCES projects(project_id),
    role VARCHAR(50),
    PRIMARY KEY (emp_id, project_id)
);

-- Insert sample data
INSERT INTO departments (dept_name) VALUES ('Engineering'), ('Sales'), ('Marketing');

INSERT INTO employees (name, dept_id, manager_id) VALUES
    ('Alice', 1, NULL),     -- Engineering, no manager
    ('Bob', 1, 1),          -- Engineering, reports to Alice
    ('Carol', 2, 1),        -- Sales, reports to Alice
    ('David', NULL, 1);     -- No department, reports to Alice

INSERT INTO projects (project_name) VALUES ('Website Redesign'), ('Mobile App'), ('API v2');

INSERT INTO assignments (emp_id, project_id, role) VALUES
    (1, 1, 'Lead'), (1, 2, 'Reviewer'),
    (2, 1, 'Developer'), (2, 3, 'Developer'),
    (3, 1, 'PM');

-- Basic INNER JOIN
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
-- David excluded (no department)

-- Multiple INNER JOINs
SELECT 
    e.name AS employee,
    d.dept_name AS department,
    p.project_name AS project,
    a.role
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
INNER JOIN assignments a ON e.emp_id = a.emp_id
INNER JOIN projects p ON a.project_id = p.project_id
ORDER BY e.name, p.project_name;

-- Self-join
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
INNER JOIN employees m ON e.manager_id = m.emp_id;
-- Alice excluded (no manager)

-- INNER JOIN with aggregation
SELECT 
    d.dept_name,
    COUNT(e.emp_id) AS employee_count,
    STRING_AGG(e.name, ', ') AS employees
FROM departments d
INNER JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;
```

## Key Takeaways

- INNER JOIN returns only matching rows from both tables
- Non-matching rows are excluded from the result
- JOIN without INNER keyword defaults to INNER JOIN
- Use table aliases for cleaner syntax
- INNER JOIN is the most restrictive join type
- Chain multiple INNER JOINs for complex queries

## Additional Resources

- [PostgreSQL INNER JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
- [JOIN Syntax](https://www.postgresql.org/docs/current/sql-select.html)
- [Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
