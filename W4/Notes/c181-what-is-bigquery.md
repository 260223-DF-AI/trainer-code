# What is BigQuery

## Learning Objectives

- Define BigQuery and its position in the analytics landscape
- Understand BigQuery's serverless architecture
- Learn key features and capabilities
- Recognize when BigQuery is the right choice

## Why This Matters

BigQuery is Google Cloud's flagship analytics platform and one of the most widely used cloud data warehouses. Understanding BigQuery is essential for data professionals working in GCP environments and provides a foundation for modern analytical practices.

## Concept Explanation

### What is BigQuery?

BigQuery is a fully managed, serverless data warehouse that enables scalable analysis of petabyte-scale datasets. It uses SQL for queries and requires no infrastructure management.

**Key Definition:**
> BigQuery is a serverless, highly scalable, and cost-effective cloud data warehouse designed for business agility.

### Position in the Analytics Ecosystem

```
Data Sources                 BigQuery                  Consumption
+-------------+             +--------+                 +-------------+
| Applications|             |        |                 | BI Tools    |
| Databases   |----ETL/ELT->|BigQuery|<----Queries-----| (Looker)    |
| Files (GCS) |             |        |                 | Data Apps   |
| Streaming   |             |        |                 | ML Pipelines|
+-------------+             +--------+                 +-------------+
```

### Serverless Architecture

Unlike traditional data warehouses, BigQuery is fully serverless:

| Aspect | Traditional DWH | BigQuery |
|--------|-----------------|----------|
| Clusters | You manage | Google manages |
| Scaling | Manual/scheduled | Automatic |
| Maintenance | Your team | Google |
| Patching | Required | Not needed |
| Idle costs | Pay for unused capacity | Pay for storage only |

**What "Serverless" Means:**

- No servers to provision or manage
- No cluster sizing decisions
- Automatic scaling based on workload
- Focus on data and queries, not infrastructure

### BigQuery Architecture

```
+-----------------------------------------------------+
|                    BigQuery Service                  |
+-----------------------------------------------------+
|  +---------------+  +---------------+  +-----------+|
|  | Query Engine  |  | Storage Engine|  | ML Engine ||
|  | (Dremel)      |  | (Capacitor)   |  | (BQML)    ||
|  +-------+-------+  +-------+-------+  +-----+-----+|
|          |                  |                |      |
+----------+------------------+----------------+------+
           |                  |                |
    +------v------+    +------v------+   +----v----+
    | Distributed |    | Columnar    |   | ML      |
    | Execution   |    | Storage     |   | Training|
    | (Slots)     |    | (Colossus)  |   |         |
    +-------------+    +-------------+   +---------+
                             |
                    +--------v--------+
                    | Jupiter Network |
                    | (Petabit scale) |
                    +-----------------+
```

**Key Components:**

1. **Dremel Engine**: Distributed query execution
2. **Capacitor**: Columnar storage format
3. **Colossus**: Distributed file system
4. **Jupiter**: High-speed network fabric

### Core Features

#### 1. Separation of Storage and Compute

```
Storage                     Compute
+------------------+       +------------------+
| Your Data        |       | Query Slots      |
| (Always on)      | <---> | (On demand)      |
| Pay per TB/month |       | Pay per query    |
+------------------+       +------------------+
```

Benefits:

- Store petabytes affordably
- Scale compute independently
- No over-provisioning

#### 2. Standard SQL Support

BigQuery uses standard SQL (SQL:2011 compliant):

```sql
-- Familiar SQL syntax
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(total_amount) as lifetime_value
FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
HAVING lifetime_value > 1000
ORDER BY lifetime_value DESC
LIMIT 100;
```

#### 3. Built-in ML (BigQuery ML)

Train and deploy ML models using SQL:

```sql
-- Create a linear regression model
CREATE OR REPLACE MODEL `project.dataset.predict_sales`
OPTIONS(model_type='linear_reg') AS
SELECT
    feature1,
    feature2,
    target_column
FROM `project.dataset.training_data`;

-- Make predictions
SELECT * FROM ML.PREDICT(
    MODEL `project.dataset.predict_sales`,
    (SELECT * FROM `project.dataset.new_data`)
);
```

#### 4. Streaming Inserts

Real-time data ingestion:

```python
from google.cloud import bigquery

client = bigquery.Client()
table_id = "project.dataset.table"

rows_to_insert = [
    {"column1": "value1", "column2": 123},
    {"column1": "value2", "column2": 456},
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if errors:
    print(f"Errors: {errors}")
```

#### 5. Federated Queries

Query external data without loading:

```sql
-- Query data directly from Cloud Storage
SELECT * FROM EXTERNAL_QUERY(
    "us-east4.connection_id",
    "SELECT * FROM external_table"
);

-- Query Parquet files in GCS
SELECT * FROM `project.dataset.external_table`
-- External table pointing to gs://bucket/path/*.parquet
```

### Pricing Models

BigQuery offers two pricing models:

| Model | Best For | How It Works |
|-------|----------|--------------|
| On-Demand | Variable workloads | Pay per TB scanned |
| Flat-Rate | Predictable workloads | Pay for slot reservations |

**On-Demand Pricing:**

- First 1 TB/month free
- $6.25 per TB scanned after
- Pay only for what you use
- No commitments

**Flat-Rate Pricing:**

- Purchase slot commitments (100+ slots)
- Monthly or annual
- Predictable costs
- Better for high-volume analytics

### When to Use BigQuery

**Ideal Use Cases:**

- Large-scale data analytics
- Ad-hoc data exploration
- Business intelligence dashboards
- Machine learning on structured data
- Real-time analytics with streaming
- Geospatial analysis

**Consider Alternatives When:**

- Sub-second latency required (consider Bigtable)
- Heavy transactional workload (consider Cloud SQL)
- Small datasets (might be overkill)
- Complex event processing (consider Dataflow)

## Code Example

Basic BigQuery operations in Python:

```python
from google.cloud import bigquery
from datetime import datetime
from typing import List, Dict

class BigQueryClient:
    """Demonstrate BigQuery operations."""
    
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
    
    def run_query(self, sql: str) -> List[Dict]:
        """Execute a query and return results."""
        query_job = self.client.query(sql)
        results = query_job.result()
        return [dict(row) for row in results]
    
    def get_query_stats(self, sql: str) -> Dict:
        """Execute query and return statistics."""
        query_job = self.client.query(sql)
        query_job.result()  # Wait for completion
        
        return {
            'bytes_billed': query_job.total_bytes_billed,
            'bytes_processed': query_job.total_bytes_processed,
            'slot_milliseconds': query_job.slot_millis,
            'execution_time': (query_job.ended - query_job.started).total_seconds()
        }
    
    def load_from_gcs(self, gcs_uri: str, dataset: str, table: str):
        """Load data from Cloud Storage."""
        table_id = f"{self.project_id}.{dataset}.{table}"
        
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        
        load_job = self.client.load_table_from_uri(
            gcs_uri, table_id, job_config=job_config
        )
        load_job.result()  # Wait for completion
        
        return f"Loaded {load_job.output_rows} rows to {table_id}"
    
    def create_dataset(self, dataset_name: str, location: str = "US"):
        """Create a new dataset."""
        dataset_id = f"{self.project_id}.{dataset_name}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location
        
        dataset = self.client.create_dataset(dataset, exists_ok=True)
        return f"Created dataset {dataset.dataset_id}"


# Usage
client = BigQueryClient('my-project')

# Run an analytical query
results = client.run_query("""
    SELECT 
        FORMAT_DATE('%Y-%m', order_date) as month,
        COUNT(*) as orders,
        SUM(total_amount) as revenue
    FROM `my-project.analytics.orders`
    WHERE order_date >= '2024-01-01'
    GROUP BY month
    ORDER BY month
""")

for row in results:
    print(f"{row['month']}: {row['orders']} orders, ${row['revenue']:.2f}")

# Get query cost estimate
stats = client.get_query_stats("SELECT * FROM `my-project.analytics.large_table`")
cost_estimate = (stats['bytes_billed'] / 1e12) * 6.25  # $6.25 per TB
print(f"Estimated cost: ${cost_estimate:.4f}")
```

## Key Takeaways

- BigQuery is a serverless, fully managed cloud data warehouse
- No infrastructure to manage: automatic scaling and maintenance
- Uses standard SQL for queries with petabyte-scale support
- Separation of storage and compute enables cost-effective scaling
- Built-in ML, streaming, and federated query capabilities
- Two pricing models: on-demand (per TB) and flat-rate (slot reservations)
- Ideal for large-scale analytics, BI, and ad-hoc exploration

## Resources

- BigQuery Documentation: <https://cloud.google.com/bigquery/docs>
- BigQuery Pricing: <https://cloud.google.com/bigquery/pricing>
- BigQuery Best Practices: <https://cloud.google.com/bigquery/docs/best-practices-performance-overview>
- BigQuery Dremel Paper: <https://research.google/pubs/pub36632/>
