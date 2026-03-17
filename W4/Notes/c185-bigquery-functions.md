# BigQuery Functions

## Learning Objectives

- Use string, date, and numeric functions in BigQuery
- Apply aggregate and window functions
- Work with array and struct functions
- Understand BigQuery-specific functions

## Why This Matters

BigQuery provides a rich library of built-in functions that enable powerful data transformations. Understanding these functions allows you to manipulate data efficiently within your queries.

## Concept Explanation

### String Functions

```sql
-- Case conversion
SELECT 
    UPPER('hello') as upper_case,      -- 'HELLO'
    LOWER('HELLO') as lower_case,      -- 'hello'
    INITCAP('hello world') as title;   -- 'Hello World'

-- Concatenation
SELECT 
    CONCAT('Hello', ' ', 'World') as concat_result,
    'Hello' || ' ' || 'World' as pipe_concat,
    CONCAT_WS(', ', 'a', 'b', 'c') as with_separator;  -- 'a, b, c'

-- Substring and length
SELECT 
    LENGTH('Hello'),                    -- 5
    SUBSTR('Hello World', 1, 5),        -- 'Hello'
    LEFT('Hello World', 5),             -- 'Hello'
    RIGHT('Hello World', 5);            -- 'World'

-- Trimming
SELECT 
    TRIM('  hello  '),                  -- 'hello'
    LTRIM('  hello'),                   -- 'hello'
    RTRIM('hello  ');                   -- 'hello'

-- Replacement and splitting
SELECT 
    REPLACE('Hello World', 'World', 'BigQuery'),
    SPLIT('a,b,c', ','),                -- ['a', 'b', 'c'] 
    REGEXP_EXTRACT('user@email.com', r'@(.+)');  -- 'email.com'
```

### Date and Time Functions

```sql
-- Current date/time
SELECT 
    CURRENT_DATE() as today,
    CURRENT_TIMESTAMP() as now,
    CURRENT_DATETIME() as datetime_now;

-- Date extraction
SELECT 
    EXTRACT(YEAR FROM DATE '2024-06-15') as year,
    EXTRACT(MONTH FROM DATE '2024-06-15') as month,
    EXTRACT(DAY FROM DATE '2024-06-15') as day,
    EXTRACT(DAYOFWEEK FROM DATE '2024-06-15') as dow;

-- Date arithmetic
SELECT 
    DATE_ADD(DATE '2024-01-01', INTERVAL 30 DAY),
    DATE_SUB(DATE '2024-01-01', INTERVAL 1 MONTH),
    DATE_DIFF(DATE '2024-12-31', DATE '2024-01-01', DAY) as days_diff;

-- Date truncation
SELECT 
    DATE_TRUNC(DATE '2024-06-15', MONTH),   -- 2024-06-01
    DATE_TRUNC(DATE '2024-06-15', QUARTER), -- 2024-04-01
    DATE_TRUNC(DATE '2024-06-15', YEAR);    -- 2024-01-01

-- Formatting
SELECT 
    FORMAT_DATE('%B %d, %Y', DATE '2024-06-15'),  -- 'June 15, 2024'
    FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP());
```

### Numeric Functions

```sql
-- Rounding
SELECT 
    ROUND(3.14159, 2),      -- 3.14
    FLOOR(3.7),             -- 3
    CEIL(3.2),              -- 4
    TRUNC(3.14159, 2);      -- 3.14

-- Math functions
SELECT 
    ABS(-5),                -- 5
    MOD(10, 3),             -- 1
    POW(2, 3),              -- 8
    SQRT(16),               -- 4
    LOG(100, 10);           -- 2

-- Safe divide (returns NULL instead of error)
SELECT SAFE_DIVIDE(10, 0);  -- NULL instead of error
```

### Aggregate Functions

```sql
SELECT 
    COUNT(*) as total,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    STDDEV(amount) as std_dev,
    APPROX_COUNT_DISTINCT(customer_id) as approx_unique  -- Faster for large data
FROM orders;

-- String aggregation
SELECT 
    customer_id,
    STRING_AGG(product_name, ', ' ORDER BY product_name) as products
FROM orders GROUP BY customer_id;

-- Array aggregation
SELECT 
    customer_id,
    ARRAY_AGG(STRUCT(product_id, quantity)) as items
FROM order_items GROUP BY customer_id;
```

### Window Functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT 
    customer_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_num,
    RANK() OVER (ORDER BY total_amount DESC) as amount_rank
FROM orders;

-- LAG and LEAD
SELECT 
    order_date,
    revenue,
    LAG(revenue) OVER (ORDER BY order_date) as prev_revenue,
    LEAD(revenue) OVER (ORDER BY order_date) as next_revenue,
    revenue - LAG(revenue) OVER (ORDER BY order_date) as change
FROM daily_sales;

-- Running totals
SELECT 
    order_date,
    revenue,
    SUM(revenue) OVER (ORDER BY order_date) as running_total,
    AVG(revenue) OVER (ORDER BY order_date ROWS 6 PRECEDING) as moving_avg_7d
FROM daily_sales;
```

### Array and Struct Functions

```sql
-- Array functions
SELECT 
    ARRAY_LENGTH([1, 2, 3, 4, 5]),           -- 5
    ARRAY_TO_STRING(['a', 'b', 'c'], ','),   -- 'a,b,c'
    ARRAY_REVERSE([1, 2, 3]),                -- [3, 2, 1]
    ARRAY_CONCAT([1, 2], [3, 4]);            -- [1, 2, 3, 4]

-- Accessing array elements
SELECT 
    arr[OFFSET(0)] as first,     -- 0-indexed
    arr[ORDINAL(1)] as first_ord -- 1-indexed
FROM (SELECT [10, 20, 30] as arr);

-- UNNEST to expand arrays
SELECT id, item
FROM my_table, UNNEST(items) as item;
```

### Conditional Functions

```sql
-- CASE expression
SELECT 
    amount,
    CASE 
        WHEN amount < 100 THEN 'Small'
        WHEN amount < 500 THEN 'Medium'
        ELSE 'Large'
    END as size_category
FROM orders;

-- IF function
SELECT IF(status = 'active', 'Yes', 'No') as is_active FROM users;

-- COALESCE and IFNULL
SELECT 
    COALESCE(phone, email, 'No contact') as contact,
    IFNULL(discount, 0) as discount
FROM customers;

-- NULLIF
SELECT NULLIF(value, 0);  -- Returns NULL if value is 0
```

## Code Example

```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
WITH daily_metrics AS (
    SELECT 
        DATE(order_timestamp) as order_date,
        COUNT(*) as orders,
        SUM(total_amount) as revenue
    FROM `project.dataset.orders`
    WHERE order_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    GROUP BY order_date
)
SELECT 
    order_date,
    orders,
    revenue,
    AVG(revenue) OVER (ORDER BY order_date ROWS 6 PRECEDING) as moving_avg_7d,
    revenue - LAG(revenue) OVER (ORDER BY order_date) as daily_change
FROM daily_metrics
ORDER BY order_date
"""

df = client.query(query).to_dataframe()
print(df.tail(10))
```

## Key Takeaways

- String functions: CONCAT, SUBSTR, REPLACE, SPLIT, REGEXP_EXTRACT
- Date functions: DATE_ADD/SUB, DATE_DIFF, DATE_TRUNC, EXTRACT
- Window functions: ROW_NUMBER, LAG/LEAD, SUM OVER for running totals
- Array functions: ARRAY_AGG, UNNEST, ARRAY_LENGTH
- Use SAFE_DIVIDE to avoid division errors

## Resources

- BigQuery Functions: <https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators>
