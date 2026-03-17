# BigQuery Best Practices

## Learning Objectives

- Apply schema design best practices
- Optimize for performance and cost
- Implement security and governance
- Follow operational best practices

## Why This Matters

Following best practices ensures your BigQuery implementation is performant, cost-effective, secure, and maintainable. These guidelines come from real-world experience with petabyte-scale analytics.

## Concept Explanation

### Schema Design Best Practices

#### 1. Use Appropriate Data Types

```sql
-- Good: Correct types
CREATE TABLE orders (
    order_id INT64,           -- Integer IDs
    amount NUMERIC(15,2),     -- Money (not FLOAT64)
    order_date DATE,          -- Date only
    created_at TIMESTAMP,     -- UTC timestamp
    is_shipped BOOL           -- Boolean flags
);

-- Bad: Wrong types
CREATE TABLE orders_bad (
    order_id STRING,          -- Should be INT64
    amount FLOAT64,           -- Loses precision
    order_date STRING,        -- Should be DATE
);
```

#### 2. Denormalize for Analytics

```sql
-- Good: Denormalized for analytics
CREATE TABLE fact_sales AS
SELECT 
    s.sale_id,
    s.amount,
    c.customer_name,
    c.region,
    p.product_name,
    p.category
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON s.product_id = p.product_id;
```

#### 3. Use Nested/Repeated Fields

```sql
-- Good: Single row per order with nested items
CREATE TABLE orders_nested (
    order_id INT64,
    items ARRAY<STRUCT<product_id STRING, qty INT64, price NUMERIC>>
);

-- Avoids joins for common queries
```

### Performance Best Practices

| Practice | Benefit |
|----------|---------|
| Partition by date | Reduce scanned data |
| Cluster by filter columns | Better locality |
| Select specific columns | Lower bytes processed |
| Use approximate functions | Faster for estimates |
| Avoid SELECT * | Reduce unnecessary data |
| Filter early | Less data to process |

### Query Best Practices

```sql
-- Good: Efficient query
SELECT 
    customer_id,
    SUM(amount) as total
FROM orders
WHERE order_date = '2024-01-15'  -- Partition filter
GROUP BY customer_id;

-- Bad: Inefficient query
SELECT *                          -- All columns
FROM orders                       -- No partition filter
WHERE YEAR(order_date) = 2024;    -- Function prevents pruning
```

### Security Best Practices

1. **Use IAM roles**: Grant minimum necessary permissions
2. **Column-level security**: Restrict sensitive columns
3. **Row-level security**: Filter data by user
4. **VPC Service Controls**: Network isolation
5. **Audit logging**: Track data access

```sql
-- Row-level security
CREATE ROW ACCESS POLICY region_filter
ON dataset.sales
GRANT TO ('user:analyst@company.com')
FILTER USING (region = 'West');
```

### Operational Best Practices

1. **Use descriptive names**: `fact_sales`, not `table1`
2. **Add descriptions**: Document tables and columns
3. **Set expiration**: Auto-delete old data
4. **Use labels**: Organize resources
5. **Monitor costs**: Track spending regularly

```sql
-- Add descriptions
ALTER TABLE dataset.orders
SET OPTIONS (
    description = 'Customer orders, partitioned by order_date'
);

ALTER TABLE dataset.orders
ALTER COLUMN amount
SET OPTIONS (
    description = 'Order total in USD'
);
```

### Data Quality Best Practices

```sql
-- Data quality checks
SELECT 
    COUNT(*) as total_rows,
    COUNTIF(order_id IS NULL) as null_ids,
    COUNTIF(amount < 0) as negative_amounts,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
WHERE order_date = CURRENT_DATE();
```

### Summary Checklist

- [ ] Use correct data types (NUMERIC for money)
- [ ] Partition large tables by date
- [ ] Cluster by frequently filtered columns
- [ ] Select only needed columns
- [ ] Filter on partition columns
- [ ] Set maximum_bytes_billed
- [ ] Document tables and columns
- [ ] Implement appropriate security
- [ ] Monitor costs and performance

## Key Takeaways

- Design schemas for analytics: denormalized, nested structures
- Partition and cluster for performance
- Always filter on partition columns
- Implement security at multiple levels
- Document and monitor everything

## Resources

- Best Practices: <https://cloud.google.com/bigquery/docs/best-practices-performance-overview>
