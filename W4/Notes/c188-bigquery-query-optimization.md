# BigQuery Query Optimization

## Learning Objectives

- Identify common query performance issues
- Apply optimization techniques
- Use EXPLAIN and query statistics
- Reduce query costs effectively

## Why This Matters

Optimizing BigQuery queries reduces costs (on-demand pricing) and improves performance. Understanding query execution helps you write efficient SQL that scales to petabytes.

## Concept Explanation

### Cost Factors

BigQuery on-demand pricing charges per TB scanned:

| Factor | Impact on Cost |
|--------|----------------|
| Columns selected | More columns = more bytes |
| Partitions scanned | More partitions = more bytes |
| Table size | Larger tables = higher cost |

### Optimization Techniques

#### 1. Select Only Needed Columns

```sql
-- Bad: Scans all columns
SELECT * FROM large_table;

-- Good: Scans only needed columns
SELECT customer_id, order_date, amount FROM large_table;
```

#### 2. Use Partition Filters

```sql
-- Bad: Full table scan
SELECT * FROM events;

-- Good: Partition pruning
SELECT * FROM events
WHERE DATE(event_timestamp) = '2024-01-15';
```

#### 3. Avoid Functions on Partitioned Columns

```sql
-- Bad: Can't use partition pruning
SELECT * FROM events
WHERE EXTRACT(YEAR FROM event_timestamp) = 2024;

-- Good: Direct comparison
SELECT * FROM events
WHERE event_timestamp >= '2024-01-01'
  AND event_timestamp < '2025-01-01';
```

#### 4. Use Approximate Aggregations

```sql
-- Exact (slower for large data)
SELECT COUNT(DISTINCT customer_id) FROM orders;

-- Approximate (faster, <1% error)
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM orders;
```

#### 5. Avoid Self-Joins When Possible

```sql
-- Bad: Self-join is expensive
SELECT a.*, b.*
FROM orders a
JOIN orders b ON a.customer_id = b.customer_id;

-- Good: Use window functions
SELECT 
    *,
    LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order
FROM orders;
```

#### 6. Filter Early

```sql
-- Bad: Filter after join
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date > '2024-01-01';

-- Good: Filter before join (or let optimizer handle it)
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > '2024-01-01'
)
SELECT * FROM recent_orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

### Using EXPLAIN

```sql
-- Dry run to estimate bytes
SELECT 
    total_bytes_processed
FROM `project.region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'your-job-id';

-- Use BigQuery console "Dry Run" feature
-- Or Python client:
```

```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(dry_run=True)

query = "SELECT * FROM dataset.large_table"
job = client.query(query, job_config=job_config)

print(f"Bytes to process: {job.total_bytes_processed:,}")
print(f"Estimated cost: ${job.total_bytes_processed / 1e12 * 6.25:.4f}")
```

### Query Plan Analysis

In BigQuery Console, click "Execution Details" to see:

- Stage timing
- Shuffle bytes
- Slot utilization

### Materialized Views

Pre-compute expensive aggregations:

```sql
CREATE MATERIALIZED VIEW dataset.daily_sales_mv AS
SELECT 
    DATE(order_timestamp) as order_date,
    SUM(amount) as total_amount,
    COUNT(*) as order_count
FROM dataset.orders
GROUP BY order_date;

-- Queries automatically use MV when beneficial
SELECT * FROM dataset.daily_sales_mv
WHERE order_date > '2024-01-01';
```

### Best Practices Summary

| Practice | Benefit |
|----------|---------|
| Select specific columns | Reduce bytes scanned |
| Use partition filters | Scan fewer partitions |
| Cluster on filter columns | Better data locality |
| Approximate functions | Faster for estimates |
| Materialized views | Pre-computed aggregates |
| Avoid SELECT * | Reduce unnecessary data |

## Key Takeaways

- Select only needed columns to reduce bytes scanned
- Always filter on partitioned columns
- Use APPROX functions for estimates
- Check query costs with dry runs
- Materialized views speed up repeated aggregations

## Resources

- Query Optimization: <https://cloud.google.com/bigquery/docs/best-practices-performance-overview>
