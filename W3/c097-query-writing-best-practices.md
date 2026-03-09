# Query Writing Best Practices

## Learning Objectives

- Apply best practices for writing SQL queries
- Structure queries for readability and maintainability
- Optimize queries for performance
- Avoid common mistakes and anti-patterns

## Why This Matters

Well-written SQL queries are easier to understand, debug, and maintain. Following best practices helps teams collaborate effectively and prevents performance problems. As queries become more complex, good habits become increasingly important.

## The Concept

### Query Readability

**Use consistent formatting**:

```sql
-- Good: Clear structure
SELECT 
    e.first_name,
    e.last_name,
    d.department_name,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000
    AND d.department_name != 'Archived'
ORDER BY e.salary DESC;

-- Poor: Cramped, hard to read
SELECT e.first_name, e.last_name, d.department_name, e.salary FROM employees e JOIN departments d ON e.department_id = d.department_id WHERE e.salary > 50000 AND d.department_name != 'Archived' ORDER BY e.salary DESC;
```

### Naming Conventions

**Use meaningful aliases**:

```sql
-- Good: Clear abbreviations
SELECT 
    cust.name AS customer_name,
    ord.order_date,
    prod.name AS product_name
FROM customers cust
JOIN orders ord ON cust.customer_id = ord.customer_id
JOIN order_items oi ON ord.order_id = oi.order_id
JOIN products prod ON oi.product_id = prod.product_id;

-- Poor: Cryptic single letters
SELECT a.name, b.order_date, c.name
FROM customers a, orders b, order_items x, products c
WHERE ...;
```

### Explicit is Better Than Implicit

```sql
-- Good: Explicit JOIN syntax
SELECT *
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;

-- Avoid: Implicit join (comma syntax)
SELECT *
FROM orders o, customers c
WHERE o.customer_id = c.customer_id;

-- Good: Explicit columns in SELECT
SELECT first_name, last_name, email FROM users;

-- Avoid in production: SELECT *
SELECT * FROM users;  -- Column changes can break code
```

### Performance Considerations

**Index-friendly WHERE clauses**:

```sql
-- Good: Index can be used
WHERE created_date >= '2024-01-01'

-- Poor: Function prevents index use
WHERE YEAR(created_date) = 2024

-- Good: Direct comparison
WHERE email = 'test@example.com'

-- Poor: LIKE with leading wildcard can't use index
WHERE email LIKE '%@example.com'
```

**Select only needed columns**:

```sql
-- Good: Only columns you need
SELECT customer_id, name, email FROM customers;

-- Poor: Fetches all columns
SELECT * FROM customers;
```

**Use appropriate joins**:

```sql
-- Use EXISTS instead of IN for large subqueries
-- Good:
SELECT * FROM products p
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.product_id = p.product_id);

-- Can be slower with large datasets:
SELECT * FROM products
WHERE product_id IN (SELECT product_id FROM orders);
```

### Avoiding Common Mistakes

**Handle NULL correctly**:

```sql
-- WRONG: NULL comparison
WHERE status != 'active'  -- Never matches NULL!

-- CORRECT: Explicit NULL handling
WHERE status != 'active' OR status IS NULL
```

**Avoid division by zero**:

```sql
-- WRONG: Can crash
SELECT total / count AS average FROM stats;

-- CORRECT: Handle zero denominator
SELECT 
    CASE WHEN count = 0 THEN 0 ELSE total / count END AS average
FROM stats;

-- Or use NULLIF
SELECT total / NULLIF(count, 0) AS average FROM stats;
```

**Be careful with GROUP BY**:

```sql
-- WRONG: Ambiguous result
SELECT department, first_name, AVG(salary)  -- Which first_name?
FROM employees
GROUP BY department;

-- CORRECT: All non-aggregate columns in GROUP BY
SELECT department, first_name, AVG(salary)
FROM employees
GROUP BY department, first_name;
```

### Query Organization

**Use CTEs for complex queries**:

```sql
-- Good: Clear, step-by-step logic
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(total) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
),
avg_sales AS (
    SELECT AVG(revenue) AS avg_monthly
    FROM monthly_sales
)
SELECT 
    ms.month,
    ms.revenue,
    a.avg_monthly,
    ms.revenue - a.avg_monthly AS variance
FROM monthly_sales ms
CROSS JOIN avg_sales a
ORDER BY ms.month;
```

**Break complex logic into views**:

```sql
-- Create reusable view
CREATE VIEW active_customer_orders AS
SELECT c.*, o.order_id, o.total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE;

-- Use in queries
SELECT * FROM active_customer_orders WHERE total > 100;
```

### Testing and Validation

```sql
-- Always test with LIMIT first
SELECT * FROM large_table WHERE complex_condition LIMIT 10;

-- Check row counts
SELECT COUNT(*) FROM table_before_change;
-- Make change
SELECT COUNT(*) FROM table_after_change;

-- Use EXPLAIN to understand query plan
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';
```

## Code Example

Applying best practices:

```sql
-- Example: Monthly sales report with rankings
-- Good: Well-structured, documented query

-- Define data boundaries
WITH date_range AS (
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE - INTERVAL '12 months') AS start_date,
        DATE_TRUNC('month', CURRENT_DATE) AS end_date
),

-- Calculate monthly sales per product
monthly_product_sales AS (
    SELECT 
        DATE_TRUNC('month', o.order_date) AS sale_month,
        p.product_id,
        p.name AS product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    CROSS JOIN date_range dr
    WHERE o.order_date >= dr.start_date 
      AND o.order_date < dr.end_date
    GROUP BY 
        DATE_TRUNC('month', o.order_date),
        p.product_id,
        p.name,
        p.category
),

-- Rank products within each month
ranked_sales AS (
    SELECT 
        sale_month,
        product_id,
        product_name,
        category,
        units_sold,
        revenue,
        RANK() OVER (
            PARTITION BY sale_month 
            ORDER BY revenue DESC
        ) AS monthly_rank
    FROM monthly_product_sales
)

-- Final output: Top 5 products per month
SELECT 
    TO_CHAR(sale_month, 'YYYY-MM') AS month,
    monthly_rank AS rank,
    product_name,
    category,
    units_sold,
    revenue,
    ROUND(revenue / NULLIF(units_sold, 0), 2) AS avg_unit_price
FROM ranked_sales
WHERE monthly_rank <= 5
ORDER BY sale_month DESC, monthly_rank;

-- Alternative approach: Simple query following best practices
SELECT 
    c.name AS customer_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent,
    COALESCE(ROUND(AVG(o.total), 2), 0) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC
LIMIT 10;
```

## Key Takeaways

- Format queries consistently with proper indentation
- Use meaningful table aliases
- Prefer explicit JOINs over comma syntax
- Select only the columns you need
- Handle NULL values explicitly
- Use CTEs to break complex queries into steps
- Test with LIMIT and EXPLAIN before running on large data
- Avoid anti-patterns like functions in WHERE or SELECT *

## Additional Resources

- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [EXPLAIN Analysis](https://www.postgresql.org/docs/current/using-explain.html)
- [Query Planning](https://www.postgresql.org/docs/current/planner-optimizer.html)
