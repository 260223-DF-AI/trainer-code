# BigQuery Python Integration

## Learning Objectives

- Use the BigQuery Python client library
- Execute queries and process results
- Load data from DataFrames
- Handle errors and job management

## Why This Matters

Python is the primary language for data engineering and analytics. Mastering the BigQuery Python client enables you to build data pipelines, automate tasks, and integrate BigQuery with other tools.

## Concept Explanation

### Installation and Setup

```bash
pip install google-cloud-bigquery pandas pyarrow db-dtypes
```

### Authentication

```python
from google.cloud import bigquery

# Default credentials (ADC)
client = bigquery.Client()

# Explicit project
client = bigquery.Client(project='my-project')

# Service account
client = bigquery.Client.from_service_account_json('key.json')
```

### Running Queries

```python
from google.cloud import bigquery

client = bigquery.Client()

# Simple query
query = """
SELECT name, SUM(amount) as total
FROM `project.dataset.orders`
GROUP BY name
LIMIT 10
"""

results = client.query(query)

for row in results:
    print(f"{row.name}: {row.total}")
```

### Query to DataFrame

```python
import pandas as pd

query = """
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as events
FROM `project.dataset.events`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date
"""

df = client.query(query).to_dataframe()
print(df.head())
```

### Parameterized Queries

```python
from google.cloud.bigquery import ScalarQueryParameter

query = """
SELECT * FROM `project.dataset.orders`
WHERE customer_id = @customer_id
  AND order_date >= @start_date
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        ScalarQueryParameter("customer_id", "INT64", 12345),
        ScalarQueryParameter("start_date", "DATE", "2024-01-01"),
    ]
)

results = client.query(query, job_config=job_config)
```

### Loading Data

```python
# From DataFrame
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [30, 25, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

table_id = 'project.dataset.users'

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()  # Wait for completion

print(f"Loaded {job.output_rows} rows")
```

```python
# From GCS
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
)

uri = 'gs://bucket/data/*.parquet'
table_id = 'project.dataset.table'

job = client.load_table_from_uri(uri, table_id, job_config=job_config)
job.result()
```

### Creating Tables

```python
schema = [
    bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
]

table = bigquery.Table("project.dataset.new_table", schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    field="created_at"
)

table = client.create_table(table)
```

### Error Handling

```python
from google.api_core.exceptions import NotFound, BadRequest

try:
    results = client.query(query).result()
except NotFound as e:
    print(f"Table not found: {e}")
except BadRequest as e:
    print(f"Query error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Job Management

```python
# Check job status
job = client.query(query)

print(f"Job ID: {job.job_id}")
print(f"State: {job.state}")

job.result()  # Wait for completion

print(f"Bytes processed: {job.total_bytes_processed}")
print(f"Bytes billed: {job.total_bytes_billed}")
```

## Code Example

```python
from google.cloud import bigquery
import pandas as pd

class BigQueryHelper:
    def __init__(self, project_id):
        self.client = bigquery.Client(project=project_id)
    
    def query_to_df(self, sql):
        return self.client.query(sql).to_dataframe()
    
    def load_df(self, df, table_id, mode='WRITE_TRUNCATE'):
        job_config = bigquery.LoadJobConfig(
            write_disposition=mode
        )
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        return job.output_rows

# Usage
bq = BigQueryHelper('my-project')
df = bq.query_to_df("SELECT * FROM dataset.table LIMIT 100")
print(df)
```

## Key Takeaways

- Use `google-cloud-bigquery` for Python integration
- `to_dataframe()` converts results to pandas DataFrame
- Parameterized queries prevent SQL injection
- Load data from DataFrames or GCS
- Handle errors with try/except

## Resources

- Python Client: <https://cloud.google.com/python/docs/reference/bigquery/latest>
