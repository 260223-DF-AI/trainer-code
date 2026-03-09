# Equi and Theta Joins

## Learning Objectives

- Understand the difference between equi-joins and theta joins
- Recognize when to use each type of join condition
- Apply non-equality comparisons in join operations
- Identify real-world use cases for theta joins

## Why This Matters

While most joins use equality conditions (equi-joins), some scenarios require comparing values using other operators. Understanding theta joins expands your ability to solve complex data problems, such as finding ranges, matching intervals, or comparing sequential values. These techniques are essential for analytics, reporting, and business intelligence queries.

## The Concept

### What is an Equi-Join?

An **equi-join** uses only equality (=) to match rows between tables. This is the most common type of join.

```sql
-- Equi-join: Match on equal values
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id;
--                                    ^^^ equality only
```

### What is a Theta Join?

A **theta join** uses any comparison operator (=, <, >, <=, >=, <>) to match rows. "Theta" (θ) represents any comparison operator.

```sql
-- Theta join: Match using any comparison
SELECT *
FROM table1 t1
JOIN table2 t2 ON t1.value < t2.value;
--                        ^^^ non-equality comparison
```

### Comparison Operators in Joins

| Operator | Meaning | Example |
|----------|---------|---------|
| = | Equal | Exact match |
| <> or != | Not equal | Exclude matches |
| < | Less than | Before, lower |
| > | Greater than | After, higher |
| <= | Less than or equal | Up to and including |
| >= | Greater than or equal | From and including |

### Theta Join Examples

**Range-Based Join (Between Boundaries)**

```sql
-- Products within price ranges
CREATE TABLE price_tiers (
    tier_name VARCHAR(20),
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2)
);

INSERT INTO price_tiers VALUES
    ('Budget', 0, 50),
    ('Standard', 50.01, 200),
    ('Premium', 200.01, 1000);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

INSERT INTO products (name, price) VALUES
    ('Mouse', 29.99),
    ('Keyboard', 79.99),
    ('Monitor', 299.99);

-- Theta join: Find tier for each product
SELECT p.name, p.price, t.tier_name
FROM products p
JOIN price_tiers t ON p.price >= t.min_price 
                   AND p.price <= t.max_price;
```

Result:

```
name     | price  | tier_name
---------|--------|----------
Mouse    | 29.99  | Budget
Keyboard | 79.99  | Standard
Monitor  | 299.99 | Premium
```

**Historical Data Queries**

```sql
-- Find tax rate valid at time of order
CREATE TABLE tax_rates (
    rate_id SERIAL PRIMARY KEY,
    rate DECIMAL(5,2),
    effective_from DATE,
    effective_to DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE,
    amount DECIMAL(10,2)
);

-- Theta join: Match orders to applicable tax rates
SELECT o.order_id, o.order_date, o.amount, t.rate
FROM orders o
JOIN tax_rates t ON o.order_date >= t.effective_from
                 AND o.order_date <= t.effective_to;
```

**Comparison Between Rows**

```sql
-- Find employees who earn more than their managers
SELECT e.name AS employee, 
       e.salary AS employee_salary,
       m.name AS manager, 
       m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;  -- Theta condition in WHERE
```

### Non-Equality Join (Exclusion)

```sql
-- Find all pairs of products in different categories
SELECT p1.name AS product1, p2.name AS product2
FROM products p1
JOIN products p2 ON p1.category_id <> p2.category_id
                 AND p1.product_id < p2.product_id;  -- Avoid duplicates
```

### Combining Equi and Theta Conditions

```sql
-- Orders with shipping based on price tier AND region
SELECT o.order_id, o.total, s.shipping_cost
FROM orders o
JOIN shipping_rates s ON o.region_id = s.region_id           -- Equi
                      AND o.total >= s.min_order_amount      -- Theta
                      AND o.total < s.max_order_amount;      -- Theta
```

### Performance Considerations

Theta joins can be less efficient than equi-joins:

- Equi-joins can use hash joins and index lookups
- Theta joins often require nested loop or merge joins
- Non-equality conditions limit optimization options

```sql
-- Optimize with indexes where possible
CREATE INDEX idx_price ON products(price);
CREATE INDEX idx_date ON orders(order_date);
```

### Complete Example

```sql
-- Salary bands and employees
CREATE TABLE salary_bands (
    band_id SERIAL PRIMARY KEY,
    band_name VARCHAR(20),
    min_salary INTEGER,
    max_salary INTEGER
);

INSERT INTO salary_bands (band_name, min_salary, max_salary) VALUES
    ('Entry', 30000, 50000),
    ('Mid', 50001, 80000),
    ('Senior', 80001, 120000),
    ('Executive', 120001, 999999);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    salary INTEGER
);

INSERT INTO employees (name, salary) VALUES
    ('Alice', 45000),
    ('Bob', 72000),
    ('Carol', 95000),
    ('Dave', 150000);

-- Equi-join equivalent (if we had band_id in employees)
-- SELECT e.name, b.band_name FROM employees e
-- JOIN salary_bands b ON e.band_id = b.band_id;

-- Theta join (based on salary ranges)
SELECT e.name, e.salary, b.band_name
FROM employees e
JOIN salary_bands b ON e.salary >= b.min_salary 
                    AND e.salary <= b.max_salary
ORDER BY e.salary;

-- Result:
-- name  | salary | band_name
-- ------|--------|----------
-- Alice | 45000  | Entry
-- Bob   | 72000  | Mid
-- Carol | 95000  | Senior
-- Dave  | 150000 | Executive
```

## Key Takeaways

- Equi-joins use only equality (=) to match rows
- Theta joins use any comparison operator (<, >, <=, >=, <>)
- Range-based matching requires theta joins
- Common uses: price tiers, date ranges, salary bands
- Theta joins may be slower - consider performance implications
- Many theta joins can be rewritten using BETWEEN for readability

## Additional Resources

- [PostgreSQL JOIN Syntax](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [Join Types Explained](https://www.postgresql.org/docs/current/tutorial-join.html)
- [Query Performance](https://www.postgresql.org/docs/current/performance-tips.html)
