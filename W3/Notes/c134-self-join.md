# Self JOIN

## Learning Objectives

- Understand self-join concept and purpose
- Write queries that join a table to itself
- Apply self-joins for hierarchical and comparative data
- Use table aliases to distinguish instances

## Why This Matters

Self-joins allow you to compare rows within the same table. This is essential for hierarchical data (employees and managers), finding duplicates, comparing records, and analyzing relationships where both entities are stored in the same table.

## The Concept

### What is a Self-Join?

A **self-join** is when a table is joined to itself. Each instance of the table is given a different alias to distinguish them.

```sql
-- Find employees and their managers (both in employees table)
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id;
--   ^^^^^^^^^ first instance   ^^^^^^^^^ second instance
```

### Why Self-Join?

Common scenarios:

1. **Hierarchical data**: Employee-manager, category-subcategory
2. **Finding duplicates**: Compare rows to find matches
3. **Sequential analysis**: Compare row N to row N+1
4. **Relationships within table**: Friendships, referrals

### Self-Join Syntax

Always use table aliases:

```sql
SELECT 
    alias1.column AS name1,
    alias2.column AS name2
FROM table_name alias1
JOIN table_name alias2 ON alias1.column = alias2.column;
```

### Employee-Manager Hierarchy

The classic self-join example:

```sql
-- Table structure
-- employees(employee_id, name, manager_id)
-- manager_id references employee_id

-- Find employees with their managers
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
INNER JOIN employees m ON e.manager_id = m.employee_id;
-- Top-level managers (NULL manager_id) excluded

-- Include top-level managers
SELECT 
    e.name AS employee,
    COALESCE(m.name, 'No Manager') AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

### Finding Duplicates

Compare rows within the same table:

```sql
-- Find customers with same email
SELECT c1.customer_id, c1.email
FROM customers c1
JOIN customers c2 ON c1.email = c2.email
WHERE c1.customer_id < c2.customer_id;

-- Find products with same price
SELECT p1.name AS product1, p2.name AS product2, p1.price
FROM products p1
JOIN products p2 ON p1.price = p2.price
WHERE p1.product_id < p2.product_id;  -- Avoid A-A and A-B, B-A duplicates
```

### Comparing Rows

Find related records:

```sql
-- Products in same category but different price
SELECT 
    p1.name AS product1,
    p2.name AS product2,
    p1.category,
    p1.price AS price1,
    p2.price AS price2
FROM products p1
JOIN products p2 
    ON p1.category = p2.category 
    AND p1.price < p2.price
ORDER BY p1.category, p1.price;
```

### Sequential Data Analysis

Compare consecutive records:

```sql
-- Daily sales compared to previous day
SELECT 
    t.sale_date,
    t.total AS today_sales,
    y.total AS yesterday_sales,
    t.total - y.total AS difference
FROM daily_sales t
JOIN daily_sales y ON t.sale_date = y.sale_date + 1;
```

### Hierarchical Queries

For deep hierarchies, use recursive CTEs (covered in Week 4):

```sql
-- Find all reports (direct and indirect)
WITH RECURSIVE reports AS (
    SELECT employee_id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.employee_id, e.name, e.manager_id, r.level + 1
    FROM employees e
    JOIN reports r ON e.manager_id = r.employee_id
)
SELECT * FROM reports ORDER BY level, name;
```

## Code Example

Comprehensive self-join usage:

```sql
-- Create employees table with hierarchy
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INTEGER REFERENCES employees(employee_id),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE
);

INSERT INTO employees (name, manager_id, department, salary, hire_date) VALUES
    ('Alice', NULL, 'Executive', 150000, '2018-01-15'),
    ('Bob', 1, 'Engineering', 100000, '2019-03-20'),
    ('Carol', 1, 'Sales', 90000, '2019-06-10'),
    ('David', 2, 'Engineering', 80000, '2020-02-28'),
    ('Eve', 2, 'Engineering', 85000, '2020-09-15'),
    ('Frank', 3, 'Sales', 75000, '2021-04-01');

-- Employee-Manager relationships
SELECT 
    e.name AS employee,
    e.department,
    e.salary,
    COALESCE(m.name, 'No Manager') AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY m.name NULLS FIRST, e.name;

-- Find employees who earn more than their manager
SELECT 
    e.name AS employee,
    e.salary AS employee_salary,
    m.name AS manager,
    m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;

-- Employees with same hire year
SELECT 
    e1.name AS employee1,
    e2.name AS employee2,
    EXTRACT(YEAR FROM e1.hire_date) AS year
FROM employees e1
JOIN employees e2 
    ON EXTRACT(YEAR FROM e1.hire_date) = EXTRACT(YEAR FROM e2.hire_date)
    AND e1.employee_id < e2.employee_id;

-- Salary comparison within same department
SELECT 
    e1.name AS employee1,
    e2.name AS employee2,
    e1.department,
    e1.salary AS salary1,
    e2.salary AS salary2,
    e1.salary - e2.salary AS diff
FROM employees e1
JOIN employees e2 
    ON e1.department = e2.department
    AND e1.salary > e2.salary
ORDER BY e1.department, diff DESC;

-- Manager chain (one level)
SELECT 
    e.name AS employee,
    m.name AS manager,
    mm.name AS managers_manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN employees mm ON m.manager_id = mm.employee_id
ORDER BY e.name;

-- Count of direct reports per manager
SELECT 
    m.name AS manager,
    COUNT(e.employee_id) AS direct_reports,
    AVG(e.salary) AS avg_team_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
GROUP BY m.employee_id, m.name
ORDER BY direct_reports DESC;
```

## Key Takeaways

- Self-joins connect a table to itself using aliases
- Essential for hierarchical data (employee-manager)
- Use different aliases to distinguish table instances
- Often combined with inequality comparison (id < id) to avoid duplicates
- LEFT JOIN preserves records without matches (top-level)
- Recursive CTEs handle deep hierarchies better

## Additional Resources

- [PostgreSQL Self Joins](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Recursive Queries](https://www.postgresql.org/docs/current/queries-with.html)
- [Table Aliases](https://www.postgresql.org/docs/current/sql-select.html)
