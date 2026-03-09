# Natural JOIN

## Learning Objectives

- Understand NATURAL JOIN behavior
- Recognize the risks of using NATURAL JOIN
- Compare NATURAL JOIN with explicit joins
- Apply USING clause as a safer alternative

## Why This Matters

NATURAL JOIN automatically matches columns with the same name, which can be convenient but also dangerous. Understanding its behavior helps you avoid subtle bugs and choose safer alternatives like explicit ON clauses or the USING clause.

## The Concept

### What is NATURAL JOIN?

**NATURAL JOIN** automatically joins tables on all columns with matching names. No ON clause is specified.

```sql
-- Automatically matches on same-named columns
SELECT *
FROM orders
NATURAL JOIN customers;
-- Joins on all columns present in both tables with same name
```

### How It Works

```
orders:              customers:           NATURAL JOIN (on customer_id):
| order_id | customer_id |    | customer_id | name  |    | order_id | customer_id | name  |
|----------|-------------|    |-------------|-------|    |----------|-------------|-------|
| 1        | 101         |    | 101         | Alice |    | 1        | 101         | Alice |
| 2        | 102         |    | 102         | Bob   |    | 2        | 102         | Bob   |
```

### The Problem with NATURAL JOIN

NATURAL JOIN is **dangerous** because:

1. **Unpredictable matching**: Joins on ANY same-named column
2. **Silent failures**: Added columns can break queries
3. **Unexpected results**: Unrelated same-named columns get joined

```sql
-- Scenario: Both tables have 'id' and 'customer_id'
-- orders: id, customer_id, order_date
-- customers: id, customer_id, name

-- NATURAL JOIN matches on BOTH id AND customer_id
-- This is probably NOT what you want!
SELECT * FROM orders NATURAL JOIN customers;
-- Returns nothing if id values don't also match!
```

### NATURAL JOIN vs Explicit JOIN

```sql
-- Dangerous: relies on column name matching
SELECT * FROM orders NATURAL JOIN customers;

-- Safe: explicit join condition
SELECT * 
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

### The USING Clause

A safer middle ground: explicit column list, cleaner syntax:

```sql
-- USING: specify exactly which columns to match
SELECT *
FROM orders
JOIN customers USING (customer_id);
-- Only joins on customer_id, not other same-named columns
```

**USING requirements**:

- Column must exist in both tables
- Column must have the same name
- Only one instance appears in result (unlike ON)

### USING Example

```sql
-- With USING
SELECT order_id, customer_id, name, order_date
FROM orders
JOIN customers USING (customer_id);
-- customer_id appears once in result

-- Equivalent with ON
SELECT o.order_id, o.customer_id, c.name, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
-- Must specify which customer_id to use
```

### When NATURAL JOIN Might Be Safe

In controlled scenarios with well-designed schemas:

```sql
-- Example: Lookup tables designed for natural join
-- countries(country_code, country_name)
-- cities(city_id, city_name, country_code)

SELECT city_name, country_name
FROM cities
NATURAL JOIN countries;
-- Only matching column is country_code - works as expected
```

### Best Practices

| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| NATURAL JOIN | Concise | Unpredictable, fragile | Avoid |
| USING | Clean syntax, explicit | Limited to same-named columns | Use when applicable |
| ON | Most explicit, flexible | More verbose | Preferred default |

## Code Example

Comparing join approaches:

```sql
-- Create tables with intentionally tricky column names
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO categories (id, category_name) VALUES 
    (1, 'Electronics'), (2, 'Clothing');

INSERT INTO products (id, product_name, category_id) VALUES
    (100, 'Laptop', 1),
    (101, 'T-Shirt', 2);

-- NATURAL JOIN: Matches on 'id' AND 'created_at' - NOT what we want!
SELECT * FROM products NATURAL JOIN categories;
-- Returns empty because id=100 doesn't match id=1, etc.

-- Correct with explicit ON
SELECT 
    p.product_name,
    c.category_name
FROM products p
JOIN categories c ON p.category_id = c.id;
-- Returns: Laptop-Electronics, T-Shirt-Clothing

-- Demonstrate USING with proper column names
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO customers (customer_id, name) VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO orders (customer_id) VALUES (1), (1), (2);

-- USING clause (safe, clean)
SELECT order_id, customer_id, name
FROM orders
JOIN customers USING (customer_id);
-- Note: customer_id appears once in output

-- Compared to ON (also safe)
SELECT o.order_id, o.customer_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
-- Must choose which customer_id to include

-- NATURAL JOIN would work here (both only share customer_id)
SELECT * FROM orders NATURAL JOIN customers;
-- Works, but fragile - adding a column with same name would break it

-- Multiple column USING
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);

CREATE TABLE products2 (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

SELECT order_id, product_id, quantity, name
FROM order_items
JOIN products2 USING (product_id);
```

## Key Takeaways

- NATURAL JOIN automatically matches same-named columns
- Dangerous: unexpected columns can break queries
- USING clause is safer: explicitly names join columns
- ON clause is most explicit and flexible
- Prefer explicit ON joins in most cases
- USING is acceptable for simple same-named FK joins

## Additional Resources

- [PostgreSQL NATURAL JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [USING Clause](https://www.postgresql.org/docs/current/sql-select.html)
- [Join Types](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
