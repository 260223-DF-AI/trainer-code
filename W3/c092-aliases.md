# Aliases

## Learning Objectives

- Understand column and table aliases
- Apply aliases for readability and self-joins
- Use aliases with expressions and calculations
- Recognize alias scope and limitations

## Why This Matters

Aliases improve query readability by providing meaningful names for columns, expressions, and tables. They are essential for self-joins, complex subqueries, and creating understandable output. Well-chosen aliases make your SQL easier to read, maintain, and debug.

## The Concept

### What Are Aliases?

An **alias** is an alternative name for a column or table in a query. Aliases exist only for the duration of the query.

### Column Aliases

**Basic syntax**:

```sql
-- Using AS keyword (recommended)
SELECT first_name AS "First Name" FROM employees;

-- Without AS (works but less clear)
SELECT first_name "First Name" FROM employees;

-- Simple alias without quotes
SELECT first_name AS fname FROM employees;
```

**When to quote aliases**:

```sql
-- Quotes required for special characters and spaces
SELECT salary AS "Annual Salary" FROM employees;
SELECT price * quantity AS "Line Total" FROM order_items;

-- Mixed case preserved with quotes
SELECT name AS "productName" FROM products;

-- Without quotes: converted to lowercase
SELECT name AS ProductName FROM products;  -- Becomes productname
```

### Expression Aliases

Name calculated results for clarity:

```sql
SELECT 
    first_name,
    last_name,
    salary,
    salary * 12 AS annual_salary,
    salary * 12 * 0.10 AS annual_bonus,
    first_name || ' ' || last_name AS full_name
FROM employees;
```

### Table Aliases

**Basic syntax**:

```sql
-- Using AS keyword
SELECT e.first_name, e.department
FROM employees AS e;

-- Without AS (common shorthand)
SELECT e.first_name, e.department
FROM employees e;
```

**Why use table aliases**:

1. **Shorter queries**:

```sql
-- Without alias (verbose)
SELECT employees.first_name, employees.last_name, departments.name
FROM employees
JOIN departments ON employees.department_id = departments.department_id;

-- With aliases (concise)
SELECT e.first_name, e.last_name, d.name
FROM employees e
JOIN departments d ON e.department_id = d.department_id;
```

1. **Required for self-joins**:

```sql
-- Find employees and their managers
SELECT 
    e.first_name AS employee,
    m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

1. **Disambiguate same column names**:

```sql
SELECT 
    o.id AS order_id,      -- orders.id
    c.id AS customer_id    -- customers.id
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

### Alias Scope

Aliases are available in:

- ORDER BY clause (yes)
- HAVING clause (sometimes, depends on database)
- WHERE clause (no - runs before SELECT)

```sql
-- Works: ORDER BY with alias
SELECT salary * 12 AS annual_salary
FROM employees
ORDER BY annual_salary;

-- Does NOT work: WHERE with alias
SELECT salary * 12 AS annual_salary
FROM employees
WHERE annual_salary > 100000;  -- ERROR!

-- Workaround: repeat expression
SELECT salary * 12 AS annual_salary
FROM employees
WHERE salary * 12 > 100000;  -- Works

-- Workaround: subquery
SELECT * FROM (
    SELECT salary * 12 AS annual_salary FROM employees
) sub
WHERE annual_salary > 100000;
```

### Best Practices

**1. Use meaningful aliases**:

```sql
-- Good: meaningful abbreviations
SELECT e.first_name, d.name AS dept_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- Avoid: cryptic single letters
SELECT x.first_name, y.name
FROM employees x
JOIN departments y ON x.department_id = y.department_id;
```

**2. Be consistent**:

```sql
-- Pick a pattern and stick with it
-- Pattern 1: first letters
employees e, departments d, orders o

-- Pattern 2: abbreviations
employees emp, departments dept, orders ord
```

**3. Always alias expressions**:

```sql
-- Good: clear output column name
SELECT price * quantity AS line_total FROM order_items;

-- Poor: weird column name in output
SELECT price * quantity FROM order_items;  -- Column named "?column?"
```

## Code Example

Comprehensive alias usage:

```sql
-- Sample tables
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INTEGER,
    manager_id INTEGER,
    salary DECIMAL(10, 2),
    hire_date DATE
);

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    budget DECIMAL(12, 2)
);

-- Insert sample data
INSERT INTO departments (name, budget) VALUES 
    ('Engineering', 500000),
    ('Sales', 300000),
    ('Marketing', 200000);

INSERT INTO employees (first_name, last_name, department_id, manager_id, salary, hire_date) VALUES
    ('Alice', 'Johnson', 1, NULL, 120000, '2020-01-15'),
    ('Bob', 'Smith', 1, 1, 95000, '2021-03-20'),
    ('Carol', 'Williams', 2, 1, 85000, '2022-06-10'),
    ('David', 'Brown', 2, 3, 70000, '2023-02-28'),
    ('Eve', 'Davis', 3, 1, 75000, '2022-09-15');

-- Column aliases for expressions
SELECT 
    first_name AS "First Name",
    last_name AS "Last Name",
    salary AS "Monthly Salary",
    salary * 12 AS "Annual Salary",
    salary * 12 * 0.05 AS "Annual Bonus",
    ROUND(salary / 22, 2) AS "Daily Rate",
    DATE_PART('year', AGE(CURRENT_DATE, hire_date)) AS "Years Employed"
FROM employees;

-- Table aliases for joins
SELECT 
    e.first_name,
    e.last_name,
    d.name AS department,
    d.budget AS dept_budget,
    ROUND(e.salary / d.budget * 100, 2) AS "% of Budget"
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY d.name, e.salary DESC;

-- Self-join with aliases (required)
SELECT 
    emp.first_name AS employee_name,
    emp.salary AS employee_salary,
    mgr.first_name AS manager_name,
    mgr.salary AS manager_salary
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.employee_id
ORDER BY mgr.first_name NULLS FIRST, emp.first_name;

-- Complex query with multiple aliases
SELECT 
    d.name AS department,
    COUNT(e.employee_id) AS headcount,
    SUM(e.salary) AS total_payroll,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    d.budget AS allocated_budget,
    d.budget - SUM(e.salary) AS remaining_budget
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.name, d.budget
ORDER BY remaining_budget DESC;
```

## Key Takeaways

- Column aliases name output columns (use AS for clarity)
- Table aliases shorten queries and are required for self-joins
- Quote aliases containing spaces or special characters
- Aliases cannot be used in WHERE (execution order)
- Always alias calculated expressions for readability
- Choose meaningful, consistent alias names

## Additional Resources

- [PostgreSQL Identifiers](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
- [SELECT Clause](https://www.postgresql.org/docs/current/sql-select.html)
- [Table Aliases](https://www.postgresql.org/docs/current/queries-table-expressions.html)
