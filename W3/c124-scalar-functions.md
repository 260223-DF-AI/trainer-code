# Scalar Functions

## Learning Objectives

- Understand the difference between scalar and aggregate functions
- Master common string, numeric, and date functions
- Apply scalar functions to transform data
- Combine functions for complex transformations

## Why This Matters

Scalar functions operate on individual values, transforming each row independently. They are essential for data cleaning, formatting output, performing calculations, and manipulating dates. Mastering these functions enables you to shape query results exactly as needed.

## The Concept

### Scalar vs Aggregate Functions

| Type | Operates On | Returns | Example |
|------|------------|---------|---------|
| Scalar | Single row | One value per row | UPPER('hello') -> 'HELLO' |
| Aggregate | Group of rows | One value per group | SUM(salary) -> 500000 |

```sql
-- Scalar: transforms each row
SELECT UPPER(name) FROM employees;  -- Multiple rows output

-- Aggregate: summarizes rows
SELECT SUM(salary) FROM employees;  -- Single row output
```

### String Functions

**Case Conversion**:

```sql
SELECT UPPER('hello');           -- 'HELLO'
SELECT LOWER('HELLO');           -- 'hello'
SELECT INITCAP('hello world');   -- 'Hello World'
```

**Trimming and Padding**:

```sql
SELECT TRIM('  hello  ');        -- 'hello'
SELECT LTRIM('  hello');         -- 'hello  '
SELECT RTRIM('hello  ');         -- 'hello'
SELECT LPAD('42', 5, '0');       -- '00042'
SELECT RPAD('A', 5, '-');        -- 'A----'
```

**Length and Position**:

```sql
SELECT LENGTH('hello');          -- 5
SELECT CHAR_LENGTH('hello');     -- 5 (same as LENGTH)
SELECT POSITION('l' IN 'hello'); -- 3 (first occurrence)
```

**Extraction and Manipulation**:

```sql
SELECT SUBSTRING('hello world' FROM 1 FOR 5);  -- 'hello'
SELECT LEFT('hello', 3);         -- 'hel'
SELECT RIGHT('hello', 3);        -- 'llo'
SELECT REPLACE('hello', 'l', 'x'); -- 'hexxo'
SELECT REVERSE('hello');         -- 'olleh'
```

**Concatenation**:

```sql
SELECT 'Hello' || ' ' || 'World';  -- 'Hello World'
SELECT CONCAT('Hello', ' ', 'World'); -- 'Hello World'
SELECT CONCAT_WS(', ', 'Alice', 'Bob', 'Carol'); -- 'Alice, Bob, Carol'
```

### Numeric Functions

**Rounding**:

```sql
SELECT ROUND(3.14159, 2);        -- 3.14
SELECT CEIL(3.2);                -- 4 (round up)
SELECT FLOOR(3.8);               -- 3 (round down)
SELECT TRUNC(3.789, 2);          -- 3.78 (truncate)
```

**Absolute and Sign**:

```sql
SELECT ABS(-5);                  -- 5
SELECT SIGN(-5);                 -- -1
SELECT SIGN(0);                  -- 0
SELECT SIGN(5);                  -- 1
```

**Power and Roots**:

```sql
SELECT POWER(2, 3);              -- 8
SELECT SQRT(16);                 -- 4
SELECT MOD(17, 5);               -- 2 (remainder)
```

**Random**:

```sql
SELECT RANDOM();                 -- Random decimal 0-1
SELECT FLOOR(RANDOM() * 100);    -- Random integer 0-99
```

### Date and Time Functions

**Current Date/Time**:

```sql
SELECT CURRENT_DATE;             -- 2024-01-20
SELECT CURRENT_TIME;             -- 14:30:00
SELECT CURRENT_TIMESTAMP;        -- 2024-01-20 14:30:00
SELECT NOW();                    -- Same as CURRENT_TIMESTAMP
```

**Date Extraction**:

```sql
SELECT EXTRACT(YEAR FROM date '2024-01-20');   -- 2024
SELECT EXTRACT(MONTH FROM date '2024-01-20');  -- 1
SELECT EXTRACT(DAY FROM date '2024-01-20');    -- 20
SELECT EXTRACT(DOW FROM date '2024-01-20');    -- Day of week (0=Sun)
SELECT DATE_PART('year', '2024-01-20'::date);  -- 2024
```

**Date Arithmetic**:

```sql
SELECT CURRENT_DATE + 30;        -- 30 days from now
SELECT CURRENT_DATE - INTERVAL '1 month';
SELECT AGE(TIMESTAMP '2024-01-20', TIMESTAMP '2000-01-01');
```

**Date Formatting**:

```sql
SELECT TO_CHAR(CURRENT_DATE, 'Month DD, YYYY');  -- 'January 20, 2024'
SELECT TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD');      -- '2024-01-20'
SELECT TO_CHAR(NOW(), 'HH24:MI:SS');             -- '14:30:00'
```

**Date Truncation**:

```sql
SELECT DATE_TRUNC('month', TIMESTAMP '2024-01-20');  -- 2024-01-01
SELECT DATE_TRUNC('year', TIMESTAMP '2024-01-20');   -- 2024-01-01
SELECT DATE_TRUNC('hour', NOW());                    -- Current hour, no minutes
```

### NULL Handling

```sql
SELECT COALESCE(NULL, 'default');        -- 'default'
SELECT COALESCE(phone, 'No phone');      -- Returns phone or 'No phone'
SELECT NULLIF(0, 0);                     -- NULL (if values match)
SELECT NULLIF(10, 0);                    -- 10 (values don't match)
```

### Type Conversion

```sql
SELECT CAST('123' AS INTEGER);           -- 123
SELECT '123'::INTEGER;                   -- 123 (PostgreSQL shorthand)
SELECT TO_NUMBER('1,234.56', '9,999.99'); -- 1234.56
SELECT TO_DATE('2024-01-20', 'YYYY-MM-DD'); -- date value
```

## Code Example

Practical scalar function usage:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    birth_date DATE,
    balance DECIMAL(10, 2)
);

INSERT INTO customers (email, first_name, last_name, phone, birth_date, balance) VALUES
    ('alice@email.com', 'alice', 'johnson', '555-1234', '1990-05-15', 1500.50),
    ('bob@COMPANY.org', 'BOB', 'Smith', NULL, '1985-08-22', -50.00),
    ('carol@email.com', 'Carol', 'williams', '555-5678', '1995-12-01', 250.00);

-- String transformations
SELECT 
    customer_id,
    INITCAP(first_name) AS first_name,
    UPPER(last_name) AS last_name,
    LOWER(email) AS email,
    COALESCE(phone, 'No phone') AS phone,
    LENGTH(email) AS email_length
FROM customers;

-- Numeric transformations
SELECT 
    customer_id,
    first_name,
    balance,
    ABS(balance) AS abs_balance,
    ROUND(balance, 0) AS rounded_balance,
    CASE WHEN SIGN(balance) >= 0 THEN 'Positive/Zero' ELSE 'Negative' END AS balance_status
FROM customers;

-- Date transformations
SELECT 
    customer_id,
    first_name,
    birth_date,
    EXTRACT(YEAR FROM birth_date) AS birth_year,
    TO_CHAR(birth_date, 'Month DD, YYYY') AS formatted_date,
    AGE(CURRENT_DATE, birth_date) AS age,
    DATE_PART('year', AGE(CURRENT_DATE, birth_date))::INTEGER AS years_old
FROM customers;

-- Combined transformations
SELECT 
    CONCAT(INITCAP(first_name), ' ', UPPER(last_name)) AS full_name,
    SPLIT_PART(email, '@', 2) AS email_domain,
    CASE 
        WHEN DATE_PART('year', AGE(CURRENT_DATE, birth_date)) >= 30 THEN 'Senior'
        ELSE 'Regular'
    END AS customer_tier,
    LPAD(customer_id::TEXT, 6, '0') AS customer_code
FROM customers;
```

## Key Takeaways

- Scalar functions transform individual values (one per row)
- String functions: UPPER, LOWER, TRIM, SUBSTRING, CONCAT
- Numeric functions: ROUND, ABS, POWER, SQRT, MOD
- Date functions: EXTRACT, DATE_TRUNC, TO_CHAR, AGE
- COALESCE handles NULL values with defaults
- CAST or :: converts between data types

## Additional Resources

- [PostgreSQL String Functions](https://www.postgresql.org/docs/current/functions-string.html)
- [PostgreSQL Math Functions](https://www.postgresql.org/docs/current/functions-math.html)
- [PostgreSQL Date/Time Functions](https://www.postgresql.org/docs/current/functions-datetime.html)
