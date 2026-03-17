# Data Loading Strategies

## Learning Objectives

- Learn different data loading strategies
- Understand full refresh vs. incremental loads
- Apply upsert and merge patterns
- Handle idempotent loading

## Why This Matters

How you load data affects pipeline reliability, performance, and data consistency. Choosing the right loading strategy ensures efficient updates without duplicates or data loss.

## Concept Explanation

### Loading Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Full Refresh | Replace all data | Dimension tables, small tables |
| Append | Add new rows | Fact tables, logs |
| Upsert | Insert or update | SCD Type 1 |
| Merge | Insert, update, delete | SCD Type 2 |

### Full Refresh

Replace entire table contents:

```python
def full_refresh(data, table_name):
    """Replace table with new data."""
    client.query(f"TRUNCATE TABLE {table_name}")
    load_data(data, table_name)
```

```sql
-- BigQuery
CREATE OR REPLACE TABLE dataset.dim_products AS
SELECT * FROM staging.products;
```

### Append Loading

Add new rows to existing table:

```python
def append_load(data, table_name):
    """Append data to table."""
    load_data(data, table_name, mode='append')
```

```sql
-- BigQuery
INSERT INTO dataset.fact_sales
SELECT * FROM staging.new_sales;
```

### Upsert (Insert or Update)

Update existing rows, insert new ones:

```sql
-- BigQuery MERGE for upsert
MERGE dataset.dim_customers AS target
USING staging.customers AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
    UPDATE SET
        name = source.name,
        email = source.email,
        updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, created_at)
    VALUES (source.customer_id, source.name, source.email, CURRENT_TIMESTAMP());
```

### Merge with Delete

Handle inserts, updates, and deletes:

```sql
MERGE dataset.products AS target
USING staging.products AS source
ON target.product_id = source.product_id
WHEN MATCHED AND source._deleted = true THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET name = source.name
WHEN NOT MATCHED THEN
    INSERT (product_id, name) VALUES (source.product_id, source.name);
```

### Idempotent Loading

Same load can run multiple times safely:

```python
def idempotent_load(data, table, date_partition):
    """Delete then insert for idempotency."""
    # Delete existing data for this partition
    client.query(f"""
        DELETE FROM {table}
        WHERE partition_date = '{date_partition}'
    """)
    
    # Insert new data
    load_data(data, table)
```

### Write Dispositions

| Disposition | Behavior |
|-------------|----------|
| WRITE_TRUNCATE | Replace table |
| WRITE_APPEND | Add to table |
| WRITE_EMPTY | Fail if table exists |

## Code Example

```python
class DataLoader:
    """Handle different loading strategies."""
    
    def __init__(self, client):
        self.client = client
    
    def full_refresh(self, data, table):
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        self.client.load_table_from_dataframe(data, table, job_config=job_config)
    
    def append(self, data, table):
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        self.client.load_table_from_dataframe(data, table, job_config=job_config)
    
    def upsert(self, source_table, target_table, key_column):
        self.client.query(f"""
            MERGE {target_table} AS t
            USING {source_table} AS s
            ON t.{key_column} = s.{key_column}
            WHEN MATCHED THEN UPDATE SET *
            WHEN NOT MATCHED THEN INSERT *
        """).result()
```

## Key Takeaways

- Full refresh: Simple, best for small tables
- Append: Efficient for fact tables and logs
- Upsert: Handles updates, prevents duplicates
- Merge: Full CRUD support including deletes
- Make loads idempotent for reliability

## Resources

- BigQuery DML: <https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax>
