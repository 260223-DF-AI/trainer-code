# BigQuery Loading Data

## Learning Objectives

- Learn different methods to load data into BigQuery
- Understand batch vs. streaming ingestion
- Use the Console, CLI, and Python for data loading
- Apply best practices for data ingestion

## Why This Matters

Getting data into BigQuery is the first step in any analytics workflow. Understanding the various loading methods helps you choose the right approach for your data volume, frequency, and format.

## Concept Explanation

### Loading Methods Overview

| Method | Best For | Latency | Cost |
|--------|----------|---------|------|
| Console Upload | Small files, ad-hoc | Minutes | Free |
| bq CLI | Automation, scripts | Minutes | Free |
| Client Libraries | Applications | Minutes | Free |
| Streaming | Real-time | Seconds | Per row |
| Storage Transfer | Scheduled, large | Hours | Free |
| Dataflow | Complex transforms | Minutes | Dataflow cost |

### Loading from Google Cloud Storage

```sql
-- Load from GCS using SQL
LOAD DATA OVERWRITE mydataset.orders
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://bucket/orders/*.parquet']
);

-- Load with schema
LOAD DATA INTO mydataset.customers
FROM FILES (
  format = 'CSV',
  uris = ['gs://bucket/customers.csv'],
  skip_leading_rows = 1
);
```

### Using bq CLI

```bash
# Load CSV with auto-detect schema
bq load --autodetect \
  --source_format=CSV \
  mydataset.orders \
  gs://bucket/orders.csv

# Load Parquet
bq load --source_format=PARQUET \
  mydataset.orders \
  gs://bucket/orders/*.parquet

# Load with explicit schema
bq load --source_format=CSV \
  --skip_leading_rows=1 \
  mydataset.orders \
  gs://bucket/orders.csv \
  order_id:INTEGER,customer_id:INTEGER,amount:NUMERIC

# Append vs replace
bq load --replace ...  # Overwrite table
bq load ...            # Append (default)
```

### Python Client Library

```python
from google.cloud import bigquery

client = bigquery.Client()

# Load from GCS
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

load_job = client.load_table_from_uri(
    "gs://bucket/data/*.parquet",
    "project.dataset.table",
    job_config=job_config,
)

load_job.result()  # Wait for completion
print(f"Loaded {load_job.output_rows} rows")

# Load from DataFrame
import pandas as pd

df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

job = client.load_table_from_dataframe(df, "project.dataset.table", job_config=job_config)
job.result()
```

### Streaming Inserts

For real-time data ingestion:

```python
from google.cloud import bigquery

client = bigquery.Client()
table_id = "project.dataset.events"

rows = [
    {"event_id": "1", "event_type": "click", "timestamp": "2024-01-15T10:30:00"},
    {"event_id": "2", "event_type": "view", "timestamp": "2024-01-15T10:30:01"},
]

errors = client.insert_rows_json(table_id, rows)
if errors:
    print(f"Errors: {errors}")
else:
    print("Rows inserted successfully")
```

**Streaming Considerations:**

- Higher cost than batch loading
- Buffer time before queryable (~seconds)
- 1 MB row size limit
- Best for real-time dashboards

### External Tables

Query without loading:

```sql
CREATE EXTERNAL TABLE dataset.external_orders
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bucket/orders/*.parquet']
);

-- Query directly
SELECT * FROM dataset.external_orders WHERE order_date > '2024-01-01';
```

### Best Practices

1. **Use Parquet or Avro** for large datasets (compressed, columnar)
2. **Batch load** when possible (cheaper than streaming)
3. **Partition tables** by date for better performance
4. **Use wildcards** to load multiple files: `gs://bucket/*.parquet`
5. **Enable schema auto-detect** for quick exploration

## Key Takeaways

- Batch loading from GCS is free and efficient for most use cases
- Streaming inserts are for real-time data but cost more
- Use Parquet format for best compression and performance
- External tables allow querying without loading

## Resources

- Loading Data: <https://cloud.google.com/bigquery/docs/loading-data>
