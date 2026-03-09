# DQL: Data Query Language

## Learning Objectives

- Understand SELECT as the primary DQL command
- Recognize the importance of data retrieval
- Learn the basic structure of SELECT statements
- Identify the role of DQL in database operations

## Why This Matters

SELECT is the most frequently used SQL command. While DDL and DML are essential for building and maintaining databases, SELECT is how you extract value from your data. Reports, dashboards, APIs, and applications all rely on DQL to retrieve information. Mastering SELECT is fundamental to working with any database.

## The Concept

### What is DQL?

Data Query Language (DQL) consists of SQL commands used to retrieve data from the database. In practice, DQL has one primary command: SELECT.

While some categorizations include SELECT under DML, we separate it because:

- SELECT is read-only (does not modify data)
- SELECT is the most commonly used SQL command
- Permission models often separate read from write access

### The SELECT Statement

SELECT retrieves data from one or more tables:

```sql
-- Basic structure
SELECT column1, column2, ...
FROM table_name
WHERE conditions
ORDER BY column;
```

### SELECT Basics

**Select All Columns**:

```sql
-- The asterisk (*) selects all columns
SELECT * FROM employees;
```

**Select Specific Columns**:

```sql
-- List only the columns you need
SELECT first_name, last_name, email 
FROM employees;
```

**Column Aliases**:

```sql
-- Rename columns in output
SELECT 
    first_name AS "First Name",
    last_name AS "Last Name",
    salary AS "Annual Salary"
FROM employees;
```

**Expressions in SELECT**:

```sql
-- Calculate values
SELECT 
    first_name,
    last_name,
    salary,
    salary * 12 AS annual_salary,
    salary * 0.05 AS bonus
FROM employees;
```

### Filtering with WHERE

The WHERE clause filters which rows are returned:

```sql
-- Simple condition
SELECT * FROM employees WHERE department = 'Engineering';

-- Multiple conditions
SELECT * FROM employees 
WHERE department = 'Engineering' 
    AND salary > 70000;

-- OR condition
SELECT * FROM products 
WHERE category = 'Electronics' 
    OR category = 'Computers';

-- Range of values
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Pattern matching
SELECT * FROM customers WHERE email LIKE '%@gmail.com';

-- NULL checking
SELECT * FROM employees WHERE manager_id IS NULL;
SELECT * FROM employees WHERE termination_date IS NOT NULL;
```

### Sorting with ORDER BY

ORDER BY controls the order of results:

```sql
-- Ascending order (default)
SELECT * FROM products ORDER BY price;
SELECT * FROM products ORDER BY price ASC;

-- Descending order
SELECT * FROM products ORDER BY price DESC;

-- Multiple columns
SELECT * FROM employees 
ORDER BY department ASC, salary DESC;

-- Order by expression
SELECT * FROM products 
ORDER BY price * quantity DESC;

-- Order by column position
SELECT first_name, last_name FROM employees 
ORDER BY 2;  -- Orders by last_name (2nd column)
```

### Limiting Results

Control how many rows are returned:

```sql
-- Return only first N rows
SELECT * FROM products ORDER BY price DESC LIMIT 10;

-- Skip rows then limit
SELECT * FROM products 
ORDER BY product_id 
LIMIT 10 OFFSET 20;  -- Skip 20, return next 10

-- PostgreSQL/MySQL syntax for pagination
-- Page 3 with 10 items per page
SELECT * FROM products 
ORDER BY product_id 
LIMIT 10 OFFSET 20;
```

### Removing Duplicates

```sql
-- DISTINCT removes duplicate rows
SELECT DISTINCT department FROM employees;

-- DISTINCT on multiple columns
SELECT DISTINCT department, job_title FROM employees;

-- Count distinct values
SELECT COUNT(DISTINCT department) FROM employees;
```

### SELECT Without FROM

PostgreSQL allows SELECT for calculations:

```sql
-- Calculator
SELECT 2 + 2;          -- Result: 4
SELECT 100 * 1.05;     -- Result: 105.00

-- Current date/time
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;

-- PostgreSQL version
SELECT version();
```

### The Power of SELECT

SELECT forms the foundation for more advanced operations covered later this week:

1. **Aggregate Functions**: COUNT, SUM, AVG, MIN, MAX
2. **Grouping**: GROUP BY and HAVING
3. **Joins**: Combining multiple tables
4. **Subqueries**: Nested SELECT statements

These topics will be covered in depth on Thursday.

## Code Example

Practical SELECT queries:

```sql
-- Create sample data
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2)
);

INSERT INTO employees (first_name, last_name, email, department, hire_date, salary) VALUES
    ('Alice', 'Johnson', 'alice@company.com', 'Engineering', '2022-01-15', 85000),
    ('Bob', 'Smith', 'bob@company.com', 'Marketing', '2021-06-01', 72000),
    ('Carol', 'Williams', 'carol@company.com', 'Engineering', '2023-03-10', 90000),
    ('David', 'Brown', 'david@company.com', 'Sales', '2020-09-22', 68000),
    ('Eve', 'Davis', 'eve@company.com', 'Engineering', '2022-07-18', 88000);

-- Basic queries
SELECT * FROM employees;

-- Specific columns
SELECT first_name, last_name, department FROM employees;

-- With calculations
SELECT 
    first_name || ' ' || last_name AS full_name,
    department,
    salary,
    ROUND(salary / 12, 2) AS monthly_salary
FROM employees;

-- Filtered results
SELECT first_name, last_name, salary 
FROM employees 
WHERE department = 'Engineering' 
    AND salary > 85000;

-- Sorted results
SELECT first_name, last_name, salary 
FROM employees 
ORDER BY salary DESC;

-- Top 3 earners
SELECT first_name, last_name, salary 
FROM employees 
ORDER BY salary DESC 
LIMIT 3;

-- Distinct departments
SELECT DISTINCT department FROM employees ORDER BY department;

-- Complex query
SELECT 
    department,
    first_name,
    last_name,
    salary,
    hire_date
FROM employees
WHERE hire_date >= '2022-01-01'
    AND salary BETWEEN 70000 AND 90000
ORDER BY department, salary DESC;
```

## Key Takeaways

- SELECT is the primary (and often only) DQL command
- SELECT retrieves data without modifying the database
- WHERE filters rows; ORDER BY sorts results
- LIMIT controls result set size; OFFSET enables pagination
- DISTINCT removes duplicate rows
- SELECT is the foundation for more advanced query techniques

## Additional Resources

- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [SQL SELECT Tutorial](https://www.w3schools.com/sql/sql_ref_select.asp)
- [Query Optimization Basics](https://www.postgresql.org/docs/current/tutorial-select.html)
