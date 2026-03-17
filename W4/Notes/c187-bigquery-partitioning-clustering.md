# BigQuery Partitioning and Clustering

## Learning Objectives

- Understand table partitioning strategies
- Learn how clustering improves query performance
- Combine partitioning and clustering effectively
- Apply best practices for large tables

## Why This Matters

Partitioning and clustering are critical for managing large datasets in BigQuery. They reduce query costs by limiting the data scanned and improve performance for common query patterns.

## Concept Explanation

### Partitioning Overview

Partitioning divides a table into segments based on a column value:

```
Full Table Scan (No Partitioning):
[=====================================] 100 TB scanned

Partitioned Table (query WHERE date = '2024-01-15'):
[===][===][===][XXX][===][===][===]
                 ^
            Only 1 partition scanned (~1 TB)
```

### Partitioning Types

| Type | Column Type | Example |
|------|-------------|---------|
| Time (DATE/TIMESTAMP) | DATE, TIMESTAMP, DATETIME | `PARTITION BY DATE(timestamp)` |
| Ingestion Time | Automatic | `PARTITION BY _PARTITIONDATE` |
| Integer Range | INT64 | `PARTITION BY RANGE_BUCKET(id, ...)` |

### Creating Partitioned Tables

```sql
-- Partition by DATE column
CREATE TABLE dataset.events
PARTITION BY DATE(event_timestamp)
AS SELECT * FROM raw_events;

-- Partition by ingestion time
CREATE TABLE dataset.logs
PARTITION BY _PARTITIONDATE
OPTIONS (
    partition_expiration_days = 90
);

-- Integer range partitioning
CREATE TABLE dataset.customers
PARTITION BY RANGE_BUCKET(customer_id, GENERATE_ARRAY(0, 1000000, 10000));

-- Require partition filter
CREATE TABLE dataset.sales
PARTITION BY DATE(sale_date)
OPTIONS (
    require_partition_filter = true
);
```

### Partition Pruning

BigQuery automatically prunes partitions when filtering:

```sql
-- Full table scan (bad)
SELECT * FROM events;

-- Partition pruning (good)
SELECT * FROM events
WHERE DATE(event_timestamp) = '2024-01-15';

-- Multiple partitions
SELECT * FROM events
WHERE event_timestamp BETWEEN '2024-01-01' AND '2024-01-31';
```

### Clustering

Clustering sorts data within partitions for locality:

```sql
CREATE TABLE dataset.orders
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, product_category
AS SELECT * FROM raw_orders;
```

**How Clustering Works:**

```
Partition: 2024-01-15
+----------------------------------+
| customer_id | product_category  |
+----------------------------------+
| 1001        | Electronics       |
| 1001        | Electronics       |
| 1002        | Clothing          |
| 1002        | Clothing          |
| 1003        | Electronics       |
+----------------------------------+
Data sorted by clustering columns
```

### Clustering Best Practices

1. **Order by filter frequency**: Most filtered columns first
2. **Maximum 4 columns**: More columns = less benefit
3. **High cardinality first**: customer_id before status
4. **Common filter patterns**: Match query WHERE clauses

```sql
-- Good: Most filtered columns first
CLUSTER BY customer_id, region, category

-- Query benefits from clustering
SELECT * FROM orders
WHERE customer_id = 12345
  AND region = 'West';
```

### Combining Partitioning and Clustering

```sql
CREATE TABLE dataset.sales
PARTITION BY DATE(sale_date)
CLUSTER BY store_id, product_id
AS SELECT * FROM raw_sales;

-- Optimal query: uses both
SELECT SUM(amount)
FROM sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND store_id = 'STORE-001';
```

### Monitoring Partition and Cluster Usage

```sql
-- Check bytes scanned with INFORMATION_SCHEMA
SELECT 
    total_bytes_processed,
    total_slot_ms,
    query
FROM `project.region-us`.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY);
```

## Code Example

```python
from google.cloud import bigquery

client = bigquery.Client()

# Create partitioned and clustered table
schema = [
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("customer_id", "INT64"),
    bigquery.SchemaField("product_id", "STRING"),
    bigquery.SchemaField("order_date", "DATE"),
    bigquery.SchemaField("amount", "NUMERIC"),
]

table = bigquery.Table("project.dataset.orders", schema=schema)

table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="order_date",
    expiration_ms=365 * 24 * 60 * 60 * 1000  # 1 year
)

table.clustering_fields = ["customer_id", "product_id"]
table.require_partition_filter = True

table = client.create_table(table)
print(f"Created table with partitioning and clustering")
```

## Key Takeaways

- Partition by date for time-series data (most common)
- Cluster by frequently filtered columns
- Order clustering columns by filter frequency
- Use `require_partition_filter` to prevent accidental full scans
- Monitor bytes scanned to verify optimizations

## Resources

- Partitioned Tables: <https://cloud.google.com/bigquery/docs/partitioned-tables>
- Clustered Tables: <https://cloud.google.com/bigquery/docs/clustered-tables>
