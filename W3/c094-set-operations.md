# Set Operations: UNION, INTERSECT, EXCEPT

## Learning Objectives

- Understand SQL set operations
- Apply UNION to combine result sets
- Use INTERSECT to find common rows
- Use EXCEPT to find differences
- Distinguish between ALL and DISTINCT variants

## Why This Matters

Set operations combine results from multiple queries. They are essential for comparing datasets, merging data from different sources, and finding differences between tables. These operations follow mathematical set theory and provide powerful data manipulation capabilities.

## The Concept

### What Are Set Operations?

Set operations combine the results of two or more SELECT statements:

| Operation | Returns |
|-----------|---------|
| UNION | All rows from both queries (removes duplicates) |
| UNION ALL | All rows from both queries (keeps duplicates) |
| INTERSECT | Only rows that appear in both queries |
| EXCEPT | Rows in first query that are not in second |

### Requirements for Set Operations

Both queries must have:

1. Same number of columns
2. Compatible data types in corresponding columns

```sql
-- Valid: Same columns, same types
SELECT name, email FROM customers
UNION
SELECT name, email FROM suppliers;

-- Invalid: Different column counts
SELECT name, email, phone FROM customers
UNION
SELECT name, email FROM suppliers;  -- ERROR
```

### UNION

Combines results and removes duplicates:

```sql
-- Get all unique names from both tables
SELECT name FROM customers
UNION
SELECT name FROM employees;

-- If alice@email.com appears in both, it appears once
SELECT email FROM customers
UNION
SELECT email FROM suppliers;
```

**UNION ALL** keeps duplicates (faster):

```sql
-- Keep all rows, including duplicates
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;
-- If 'New York' appears 5 times in customers 
-- and 3 times in suppliers, result has 8 'New York' rows
```

**When to use each**:

- UNION: When you need distinct values
- UNION ALL: When you need all rows or know there are no duplicates (better performance)

### INTERSECT

Returns only rows that appear in both queries:

```sql
-- Products in both tables
SELECT product_name FROM current_products
INTERSECT
SELECT product_name FROM bestsellers;

-- Customers who are also suppliers
SELECT email FROM customers
INTERSECT
SELECT email FROM suppliers;
```

**INTERSECT ALL** (keeps duplicate count):

```sql
-- If 'Laptop' appears 3 times in A and 2 times in B
-- INTERSECT ALL returns 'Laptop' twice
SELECT product FROM table_a
INTERSECT ALL
SELECT product FROM table_b;
```

### EXCEPT

Returns rows in the first query that are not in the second:

```sql
-- Customers who are not employees
SELECT email FROM customers
EXCEPT
SELECT email FROM employees;

-- Products we sell but competitors don't
SELECT product_name FROM our_products
EXCEPT
SELECT product_name FROM competitor_products;

-- Order matters!
-- This gives employees who are not customers (different result)
SELECT email FROM employees
EXCEPT
SELECT email FROM customers;
```

**EXCEPT ALL**:

```sql
-- If 'Laptop' appears 5 times in A and 2 times in B
-- EXCEPT ALL returns 'Laptop' 3 times (5-2)
SELECT product FROM table_a
EXCEPT ALL
SELECT product FROM table_b;
```

### Column Names in Results

Result column names come from the first query:

```sql
SELECT product_name AS item, price AS cost FROM products
UNION
SELECT service_name, rate FROM services;
-- Result columns are named: item, cost
```

### ORDER BY with Set Operations

ORDER BY applies to the entire result (must come last):

```sql
-- Sort the combined result
SELECT name, email FROM customers
UNION
SELECT name, email FROM suppliers
ORDER BY name;  -- Applies to entire UNION result

-- Cannot ORDER BY individual queries
SELECT name, email FROM customers ORDER BY name  -- Wrong position
UNION
SELECT name, email FROM suppliers;  -- Error!
```

### Multiple Set Operations

Chain operations (processed left to right):

```sql
-- (A UNION B) EXCEPT C
SELECT email FROM customers
UNION
SELECT email FROM suppliers
EXCEPT
SELECT email FROM blocked_list;

-- Use parentheses for explicit ordering
(SELECT email FROM customers
 INTERSECT
 SELECT email FROM vip_list)
UNION
SELECT email FROM premium_members;
```

## Code Example

Comprehensive set operations:

```sql
-- Sample tables
CREATE TABLE current_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE potential_customers (
    lead_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE churned_customers (
    customer_id INTEGER,
    name VARCHAR(100),
    email VARCHAR(100),
    churn_date DATE
);

INSERT INTO current_customers (name, email, city) VALUES
    ('Alice', 'alice@email.com', 'New York'),
    ('Bob', 'bob@email.com', 'Boston'),
    ('Carol', 'carol@email.com', 'Chicago'),
    ('David', 'david@email.com', 'New York');

INSERT INTO potential_customers (name, email, city) VALUES
    ('Eve', 'eve@email.com', 'Boston'),
    ('Frank', 'frank@email.com', 'Miami'),
    ('Alice', 'alice@email.com', 'New York'),  -- Already a customer
    ('Grace', 'grace@email.com', 'Chicago');

INSERT INTO churned_customers (customer_id, name, email, churn_date) VALUES
    (5, 'Henry', 'henry@email.com', '2023-06-15'),
    (6, 'Alice', 'alice@email.com', '2022-01-10');  -- Re-acquired

-- UNION: All unique emails across current and potential
SELECT email, 'Current' AS source FROM current_customers
UNION
SELECT email, 'Potential' FROM potential_customers
ORDER BY email;

-- UNION ALL: All rows (shows alice@email.com twice)
SELECT name, city FROM current_customers
UNION ALL
SELECT name, city FROM potential_customers;

-- INTERSECT: People who are both current and potential (already converted)
SELECT email FROM current_customers
INTERSECT
SELECT email FROM potential_customers;
-- Returns: alice@email.com

-- EXCEPT: Potential customers who are not current customers
SELECT email FROM potential_customers
EXCEPT
SELECT email FROM current_customers;
-- Returns: eve, frank, grace

-- EXCEPT: Current customers who never churned
SELECT email FROM current_customers
EXCEPT
SELECT email FROM churned_customers;
-- Returns: bob, carol, david (alice is in churned)

-- Find cities with either current or potential customers
SELECT city FROM current_customers
UNION
SELECT city FROM potential_customers;
-- Returns: Boston, Chicago, Miami, New York

-- Cities with both current AND potential customers
SELECT city FROM current_customers
INTERSECT
SELECT city FROM potential_customers;
-- Returns: Boston, Chicago, New York

-- Report: Customer status
SELECT email, 'Active' AS status FROM current_customers
UNION
SELECT email, 'Churned' FROM churned_customers
WHERE email NOT IN (SELECT email FROM current_customers)
ORDER BY email;
```

## Key Takeaways

- UNION combines queries, removes duplicates
- UNION ALL keeps all rows (faster, use when possible)
- INTERSECT returns rows in both queries
- EXCEPT returns rows in first query not in second
- Both queries must have same number of compatible columns
- ORDER BY comes last and applies to entire result

## Additional Resources

- [PostgreSQL UNION](https://www.postgresql.org/docs/current/sql-select.html#SQL-UNION)
- [PostgreSQL INTERSECT](https://www.postgresql.org/docs/current/sql-select.html#SQL-INTERSECT)
- [PostgreSQL EXCEPT](https://www.postgresql.org/docs/current/sql-select.html#SQL-EXCEPT)
