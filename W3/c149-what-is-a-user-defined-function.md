# What Is a User-Defined Function

## Learning Objectives

- Understand user-defined functions and their purpose
- Create functions that return single values and tables
- Apply functions in SELECT statements and expressions
- Differentiate between SQL and PL/pgSQL functions

## Why This Matters

User-defined functions extend PostgreSQL's capabilities with custom logic. Unlike stored procedures, functions return values and can be used directly in queries. They're essential for encapsulating calculations, data transformations, and reusable logic that keeps your SQL clean and maintainable.

## The Concept

### What is a User-Defined Function?

A user-defined function (UDF) is a custom function you create that:

- Accepts input parameters
- Performs operations
- Returns a value (scalar, row, or table)
- Can be used in SELECT, WHERE, and other clauses

```sql
-- Using a built-in function
SELECT UPPER('hello');  -- Returns 'HELLO'

-- Using a user-defined function
SELECT calculate_discount(100, 'VIP');  -- Returns 20.00
```

### Functions vs Procedures

| Aspect | Function | Procedure |
|--------|----------|-----------|
| Return value | Required | Optional |
| Use in SELECT | Yes | No |
| Call syntax | `SELECT function()` | `CALL procedure()` |
| Transaction control | No | Yes |
| Side effects | Should avoid | Expected |

### Creating a Simple Function

```sql
CREATE OR REPLACE FUNCTION function_name(parameters)
RETURNS return_type
LANGUAGE sql  -- or plpgsql
AS $$
    -- function body
$$;
```

### SQL Functions (Simplest)

```sql
-- Function using pure SQL
CREATE OR REPLACE FUNCTION get_customer_count()
RETURNS INTEGER
LANGUAGE sql
AS $$
    SELECT COUNT(*)::INTEGER FROM customers;
$$;

-- Use it
SELECT get_customer_count();

-- Function with parameters
CREATE OR REPLACE FUNCTION get_product_price(p_id INTEGER)
RETURNS DECIMAL
LANGUAGE sql
AS $$
    SELECT price FROM products WHERE product_id = p_id;
$$;

SELECT get_product_price(101);
```

### PL/pgSQL Functions (More Powerful)

```sql
CREATE OR REPLACE FUNCTION calculate_discount(
    p_amount DECIMAL,
    p_customer_type VARCHAR
)
RETURNS DECIMAL
LANGUAGE plpgsql
AS $$
DECLARE
    v_discount DECIMAL;
BEGIN
    v_discount := CASE p_customer_type
        WHEN 'VIP' THEN 0.20
        WHEN 'Premium' THEN 0.10
        WHEN 'Regular' THEN 0.05
        ELSE 0.00
    END;
    
    RETURN p_amount * v_discount;
END;
$$;

-- Use in queries
SELECT 
    order_id,
    total,
    calculate_discount(total, customer_type) AS discount,
    total - calculate_discount(total, customer_type) AS final_price
FROM orders;
```

### Functions Returning Multiple Columns

```sql
-- Return a composite type
CREATE TYPE order_summary AS (
    order_count INTEGER,
    total_spent DECIMAL,
    avg_order DECIMAL
);

CREATE OR REPLACE FUNCTION get_customer_summary(p_customer_id INTEGER)
RETURNS order_summary
LANGUAGE plpgsql
AS $$
DECLARE
    v_result order_summary;
BEGIN
    SELECT 
        COUNT(*)::INTEGER,
        COALESCE(SUM(total), 0),
        COALESCE(AVG(total), 0)
    INTO v_result.order_count, v_result.total_spent, v_result.avg_order
    FROM orders
    WHERE customer_id = p_customer_id;
    
    RETURN v_result;
END;
$$;

-- Access individual fields
SELECT (get_customer_summary(1)).total_spent;

-- Or expand all fields
SELECT * FROM get_customer_summary(1);
```

### Table-Returning Functions

```sql
-- Return a table
CREATE OR REPLACE FUNCTION get_top_products(p_limit INTEGER)
RETURNS TABLE (
    product_id INTEGER,
    name VARCHAR,
    units_sold BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.product_id,
        p.name,
        COALESCE(SUM(oi.quantity), 0)
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.name
    ORDER BY SUM(oi.quantity) DESC NULLS LAST
    LIMIT p_limit;
END;
$$;

-- Use like a table
SELECT * FROM get_top_products(10);

-- Join with other tables
SELECT t.*, c.category_name
FROM get_top_products(10) t
JOIN categories c ON t.product_id = c.product_id;
```

### SETOF Functions

```sql
-- Return set of existing type
CREATE OR REPLACE FUNCTION get_active_customers()
RETURNS SETOF customers
LANGUAGE sql
AS $$
    SELECT * FROM customers WHERE is_active = TRUE;
$$;

SELECT * FROM get_active_customers() WHERE name LIKE 'A%';
```

### Immutable, Stable, and Volatile

```sql
-- IMMUTABLE: Same inputs always return same output
CREATE OR REPLACE FUNCTION full_name(first VARCHAR, last VARCHAR)
RETURNS VARCHAR
IMMUTABLE
LANGUAGE sql
AS $$
    SELECT first || ' ' || last;
$$;

-- STABLE: Returns same result within a single query
CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER
STABLE
LANGUAGE sql
AS $$
    SELECT user_id FROM current_session LIMIT 1;
$$;

-- VOLATILE: May return different results (default)
CREATE OR REPLACE FUNCTION random_product()
RETURNS VARCHAR
VOLATILE
LANGUAGE sql
AS $$
    SELECT name FROM products ORDER BY RANDOM() LIMIT 1;
$$;
```

### Function with Default Parameters

```sql
CREATE OR REPLACE FUNCTION format_currency(
    p_amount DECIMAL,
    p_symbol VARCHAR DEFAULT '$',
    p_decimals INTEGER DEFAULT 2
)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN p_symbol || TO_CHAR(p_amount, 'FM999,999,999.' || REPEAT('0', p_decimals));
END;
$$;

SELECT format_currency(1234.567);           -- $1,234.57
SELECT format_currency(1234.567, '€');      -- €1,234.57
SELECT format_currency(1234.567, '¥', 0);   -- ¥1,235
```

### Managing Functions

```sql
-- List functions
\df
-- or
SELECT proname, proargtypes FROM pg_proc WHERE proowner = current_user;

-- Drop function
DROP FUNCTION calculate_discount(DECIMAL, VARCHAR);
DROP FUNCTION IF EXISTS calculate_discount;
```

## Key Takeaways

- Functions return values and can be used in queries
- SQL functions are simple; PL/pgSQL offers more control
- Functions can return scalars, rows, or entire tables
- Use IMMUTABLE/STABLE/VOLATILE for optimization hints
- Default parameters make functions more flexible
- Functions should avoid side effects (use procedures instead)

## Additional Resources

- [PostgreSQL CREATE FUNCTION](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [PL/pgSQL Functions](https://www.postgresql.org/docs/current/plpgsql-structure.html)
- [Function Volatility](https://www.postgresql.org/docs/current/xfunc-volatility.html)
