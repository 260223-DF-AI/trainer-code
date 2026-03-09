# Operators: IN, BETWEEN, LIKE, IS NULL

## Learning Objectives

- Master the IN operator for set membership
- Use BETWEEN for range comparisons
- Apply LIKE for pattern matching
- Handle NULL values with IS NULL and IS NOT NULL

## Why This Matters

These operators extend your filtering capabilities beyond simple equality. They allow you to match values in lists, check ranges, search text patterns, and properly handle missing data. These are used constantly in real-world queries.

## The Concept

### The IN Operator

IN checks if a value matches any value in a list:

```sql
-- Basic IN with values
SELECT * FROM products
WHERE category IN ('Electronics', 'Clothing', 'Books');

-- Equivalent to multiple OR conditions
SELECT * FROM products
WHERE category = 'Electronics' 
   OR category = 'Clothing' 
   OR category = 'Books';

-- IN with numbers
SELECT * FROM orders WHERE status_id IN (1, 2, 3);

-- NOT IN (excludes matches)
SELECT * FROM products
WHERE category NOT IN ('Electronics', 'Clothing');
```

**IN with Subquery**:

```sql
-- Find customers who have placed orders
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Find products never ordered
SELECT * FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
    WHERE product_id IS NOT NULL  -- Important: handle NULLs!
);
```

**NULL caution with NOT IN**:

```sql
-- Dangerous: if subquery returns any NULL, NOT IN returns no rows
SELECT * FROM products
WHERE product_id NOT IN (SELECT product_id FROM discontinued);
-- If discontinued has a NULL product_id, this returns nothing!

-- Safe: use NOT EXISTS instead
SELECT * FROM products p
WHERE NOT EXISTS (SELECT 1 FROM discontinued d WHERE d.product_id = p.product_id);
```

### The BETWEEN Operator

BETWEEN checks if a value falls within a range (inclusive):

```sql
-- Numeric range
SELECT * FROM products
WHERE price BETWEEN 10 AND 50;
-- Same as: price >= 10 AND price <= 50

-- Date range
SELECT * FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- NOT BETWEEN (outside range)
SELECT * FROM products
WHERE price NOT BETWEEN 100 AND 500;
```

**BETWEEN is inclusive**:

```sql
-- Both endpoints are included
SELECT * FROM products WHERE price BETWEEN 10 AND 20;
-- Matches: 10, 15, 20 (all included)
```

**Order matters**:

```sql
-- Correct order (lower value first)
WHERE price BETWEEN 10 AND 50

-- Wrong order (returns no results)
WHERE price BETWEEN 50 AND 10
```

### The LIKE Operator

LIKE performs pattern matching on strings:

**Wildcards**:

| Wildcard | Meaning | Example |
|----------|---------|---------|
| % | Any sequence of characters | 'Jo%' matches 'John', 'Joseph' |
| _ | Any single character | 'Jo_n' matches 'John', 'Joan' |

```sql
-- Starts with
SELECT * FROM customers WHERE name LIKE 'Jo%';
-- Matches: John, Joseph, Joanna

-- Ends with
SELECT * FROM products WHERE name LIKE '%book';
-- Matches: Notebook, Textbook

-- Contains
SELECT * FROM products WHERE description LIKE '%wireless%';
-- Matches: Wireless Mouse, Premium Wireless Headphones

-- Single character wildcard
SELECT * FROM products WHERE sku LIKE 'AB_C';
-- Matches: AB1C, AB2C, ABXC

-- Combining wildcards
SELECT * FROM employees WHERE email LIKE '%@%.com';
```

**Case sensitivity**:

```sql
-- LIKE is case-sensitive by default
SELECT * FROM products WHERE name LIKE 'A%';  -- Matches Apple, not apple

-- Use ILIKE for case-insensitive (PostgreSQL)
SELECT * FROM products WHERE name ILIKE 'a%';  -- Matches Apple AND apple

-- Or use LOWER/UPPER
SELECT * FROM products WHERE LOWER(name) LIKE 'a%';
```

**Escaping special characters**:

```sql
-- Find literal % or _
SELECT * FROM products WHERE name LIKE '%\%%' ESCAPE '\';
-- Matches: 50% Off, 20% Discount

SELECT * FROM products WHERE sku LIKE 'A\_B%' ESCAPE '\';
-- Matches: A_B123
```

### IS NULL and IS NOT NULL

Standard comparison operators do not work with NULL:

```sql
-- WRONG: These never match NULL
SELECT * FROM employees WHERE manager_id = NULL;  -- Returns nothing
SELECT * FROM employees WHERE manager_id != NULL; -- Returns nothing

-- CORRECT: Use IS NULL / IS NOT NULL
SELECT * FROM employees WHERE manager_id IS NULL;     -- No manager
SELECT * FROM employees WHERE manager_id IS NOT NULL; -- Has manager
```

**Practical examples**:

```sql
-- Find incomplete records
SELECT * FROM customers WHERE phone IS NULL;

-- Find complete records
SELECT * FROM customers WHERE email IS NOT NULL AND phone IS NOT NULL;

-- Count NULLs
SELECT 
    COUNT(*) AS total,
    COUNT(phone) AS with_phone,
    COUNT(*) - COUNT(phone) AS without_phone
FROM customers;
```

### COALESCE for NULL handling

```sql
-- Replace NULL with default
SELECT 
    name,
    COALESCE(phone, 'No phone') AS phone,
    COALESCE(discount, 0) AS discount
FROM customers;
```

## Code Example

Comprehensive operator usage:

```sql
-- Sample data
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    manager_id INTEGER
);

INSERT INTO employees (name, email, department, salary, hire_date, manager_id) VALUES
    ('Alice Johnson', 'alice@company.com', 'Engineering', 95000, '2020-01-15', NULL),
    ('Bob Smith', 'bob@company.com', 'Engineering', 85000, '2021-03-20', 1),
    ('Carol Williams', 'carol@company.org', 'Sales', 75000, '2022-06-10', 1),
    ('David Brown', 'david@company.com', 'Marketing', 70000, '2023-02-28', 3),
    ('Eve Davis', NULL, 'Sales', 65000, '2023-09-15', 3),
    ('Frank Miller', 'frank@company.com', 'Engineering', 80000, '2022-12-01', 1);

-- IN operator examples
SELECT * FROM employees 
WHERE department IN ('Engineering', 'Sales');

SELECT * FROM employees 
WHERE salary IN (75000, 85000, 95000);

-- BETWEEN examples
SELECT * FROM employees 
WHERE salary BETWEEN 70000 AND 90000;

SELECT * FROM employees 
WHERE hire_date BETWEEN '2022-01-01' AND '2022-12-31';

-- LIKE examples
SELECT * FROM employees 
WHERE name LIKE 'A%';  -- Starts with A

SELECT * FROM employees 
WHERE email LIKE '%@company.com';  -- Ends with @company.com

SELECT * FROM employees 
WHERE name LIKE '%a%';  -- Contains 'a'

SELECT * FROM employees 
WHERE name ILIKE '%SMITH%';  -- Case-insensitive

SELECT * FROM employees 
WHERE name LIKE '___ %';  -- 3-letter first name

-- IS NULL examples
SELECT * FROM employees 
WHERE manager_id IS NULL;  -- Top-level employees

SELECT * FROM employees 
WHERE email IS NOT NULL;  -- Has email

-- Combined operators
SELECT 
    name,
    department,
    salary,
    COALESCE(email, 'No email') AS email
FROM employees
WHERE department IN ('Engineering', 'Sales')
  AND salary BETWEEN 70000 AND 90000
  AND name LIKE '%i%'
ORDER BY salary DESC;
```

## Key Takeaways

- IN: Check membership in a list; be careful with NULL in NOT IN
- BETWEEN: Inclusive range check; order matters (low, high)
- LIKE: Pattern matching with % (any chars) and _ (single char)
- ILIKE: Case-insensitive LIKE (PostgreSQL)
- IS NULL / IS NOT NULL: The only way to compare with NULL
- Use COALESCE to provide defaults for NULL values

## Additional Resources

- [PostgreSQL Comparison Operators](https://www.postgresql.org/docs/current/functions-comparison.html)
- [Pattern Matching](https://www.postgresql.org/docs/current/functions-matching.html)
- [NULL Handling](https://www.postgresql.org/docs/current/functions-comparison.html#FUNCTIONS-COMPARISON-OP-TABLE)
