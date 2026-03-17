# BigQuery Datasets and Tables

## Learning Objectives

- Understand BigQuery's organizational hierarchy
- Learn how to create and manage datasets
- Work with different table types in BigQuery
- Apply best practices for dataset and table organization

## Why This Matters

Proper organization of datasets and tables is fundamental to managing data in BigQuery. Understanding the hierarchy and table types helps you design efficient, maintainable, and cost-effective data architectures.

## Concept Explanation

### BigQuery Resource Hierarchy

```
Google Cloud Organization
         |
    +----+----+
    |         |
 Project A  Project B
    |         |
+---+---+   +---+---+
|       |   |       |
Dataset1 Dataset2  Dataset3
    |       |         |
+---+---+  +---+    +---+---+
|   |   |    |      |   |   |
T1  T2  V1   T3     T4  T5  T6

T = Table
V = View
```

### Projects

The top-level container for BigQuery resources:

- **Billing unit**: Costs are tracked at project level
- **Access control**: IAM permissions at project level
- **Resource isolation**: Datasets can't span projects
- **Naming**: `project-id.dataset.table`

### Datasets

Datasets are containers for tables and views:

**Creating a Dataset:**

```sql
-- SQL DDL
CREATE SCHEMA IF NOT EXISTS `project-id.my_dataset`
OPTIONS (
    description = 'Analytics data for sales team',
    location = 'US',
    default_table_expiration_days = 90
);
```

```python
from google.cloud import bigquery

client = bigquery.Client()

dataset_id = f"{client.project}.my_dataset"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
dataset.description = "Analytics data for sales team"
dataset.default_table_expiration_ms = 90 * 24 * 60 * 60 * 1000  # 90 days

dataset = client.create_dataset(dataset, exists_ok=True)
```

**Dataset Properties:**

| Property | Description |
|----------|-------------|
| Location | Region/multi-region (US, EU, us-east1) |
| Default Expiration | Auto-delete tables after N days |
| Labels | Key-value metadata for organization |
| Access Control | Dataset-level permissions |

### Table Types

BigQuery supports several table types:

```
+-------------------+    +-------------------+    +-------------------+
|   Native Tables   |    | External Tables   |    |      Views        |
+-------------------+    +-------------------+    +-------------------+
| Data stored in BQ |    | Data in GCS/other |    | Logical, no data  |
| Managed storage   |    | Federated queries |    | SQL definition    |
| Partitioned/Clust |    | Schema on read    |    | Standard/Material |
+-------------------+    +-------------------+    +-------------------+
```

#### 1. Native Tables

Standard BigQuery tables with managed storage:

```sql
-- Create from query results
CREATE OR REPLACE TABLE `project.dataset.sales_summary` AS
SELECT 
    customer_id,
    SUM(amount) as total_amount,
    COUNT(*) as order_count
FROM `project.dataset.orders`
GROUP BY customer_id;

-- Create with schema definition
CREATE TABLE `project.dataset.customers` (
    customer_id INT64 NOT NULL,
    name STRING,
    email STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

#### 2. External Tables

Query data without loading into BigQuery:

```sql
-- External table pointing to GCS
CREATE EXTERNAL TABLE `project.dataset.external_logs`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://my-bucket/logs/*.parquet']
);

-- External table with Hive partitioning
CREATE EXTERNAL TABLE `project.dataset.partitioned_logs`
WITH PARTITION COLUMNS (
    year INT64,
    month INT64
)
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://bucket/logs/*'],
    hive_partition_uri_prefix = 'gs://bucket/logs/'
);
```

**When to Use External Tables:**

- Query infrequently accessed data
- Data must remain in original location
- Avoid data loading overhead
- Join BigQuery data with external data

#### 3. Views

Logical tables defined by SQL query:

```sql
-- Standard view
CREATE VIEW `project.dataset.active_customers` AS
SELECT * FROM `project.dataset.customers`
WHERE status = 'active' AND last_order_date > DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY);

-- Authorized view (secure access)
-- Grants access to view even if user can't query underlying tables
```

#### 4. Materialized Views

Pre-computed views for better performance:

```sql
CREATE MATERIALIZED VIEW `project.dataset.daily_sales_mv` AS
SELECT 
    DATE(order_date) as day,
    product_id,
    SUM(quantity) as total_quantity,
    SUM(revenue) as total_revenue
FROM `project.dataset.orders`
GROUP BY day, product_id;

-- Automatic refresh, incrementally updated
-- Queries automatically use MV when beneficial
```

**Materialized View Benefits:**

- Faster query performance
- Automatic incremental refresh
- Query optimizer uses them automatically
- Cost savings on repeated aggregations

### Partitioning

Divide tables into segments for better performance:

```sql
-- Partition by date column
CREATE TABLE `project.dataset.events`
PARTITION BY DATE(event_timestamp)
AS SELECT * FROM `project.staging.events`;

-- Partition by ingestion time
CREATE TABLE `project.dataset.logs`
PARTITION BY _PARTITIONDATE
OPTIONS (partition_expiration_days = 30);

-- Integer range partitioning
CREATE TABLE `project.dataset.customers`
PARTITION BY RANGE_BUCKET(customer_id, GENERATE_ARRAY(0, 1000000, 1000));
```

**Partition Pruning:**

```sql
-- Query only scans relevant partitions
SELECT * FROM `project.dataset.events`
WHERE DATE(event_timestamp) = '2024-01-15';
-- Scans only the 2024-01-15 partition, not entire table
```

### Clustering

Sort data within partitions for better locality:

```sql
CREATE TABLE `project.dataset.orders`
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, product_id
AS SELECT * FROM `project.staging.orders`;
```

**Best Practices for Clustering:**

- Use columns frequently in WHERE or JOIN
- Order by selectivity (most selective first)
- Maximum 4 clustering columns
- Re-cluster as data changes

## Code Example

Managing datasets and tables programmatically:

```python
from google.cloud import bigquery
from datetime import datetime, timedelta
from typing import List, Optional

class BigQueryManager:
    """Manage BigQuery datasets and tables."""
    
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
    
    def create_dataset(
        self, 
        name: str, 
        location: str = "US",
        description: str = "",
        expiration_days: Optional[int] = None
    ) -> str:
        """Create a new dataset."""
        dataset_id = f"{self.project_id}.{name}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location
        dataset.description = description
        
        if expiration_days:
            dataset.default_table_expiration_ms = (
                expiration_days * 24 * 60 * 60 * 1000
            )
        
        dataset = self.client.create_dataset(dataset, exists_ok=True)
        return f"Created dataset: {dataset.dataset_id}"
    
    def create_partitioned_table(
        self,
        dataset: str,
        table: str,
        schema: List[bigquery.SchemaField],
        partition_field: str,
        cluster_fields: Optional[List[str]] = None
    ) -> str:
        """Create a partitioned and optionally clustered table."""
        table_id = f"{self.project_id}.{dataset}.{table}"
        table_ref = bigquery.Table(table_id, schema=schema)
        
        # Time partitioning
        table_ref.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=partition_field
        )
        
        # Clustering
        if cluster_fields:
            table_ref.clustering_fields = cluster_fields
        
        table_ref = self.client.create_table(table_ref, exists_ok=True)
        return f"Created table: {table_ref.table_id}"
    
    def create_external_table(
        self,
        dataset: str,
        table: str,
        gcs_uris: List[str],
        file_format: str = "PARQUET"
    ) -> str:
        """Create an external table pointing to GCS."""
        table_id = f"{self.project_id}.{dataset}.{table}"
        table_ref = bigquery.Table(table_id)
        
        external_config = bigquery.ExternalConfig(file_format)
        external_config.source_uris = gcs_uris
        external_config.autodetect = True
        
        table_ref.external_data_configuration = external_config
        
        table_ref = self.client.create_table(table_ref, exists_ok=True)
        return f"Created external table: {table_ref.table_id}"
    
    def list_tables(self, dataset: str) -> List[dict]:
        """List all tables in a dataset."""
        dataset_ref = f"{self.project_id}.{dataset}"
        tables = []
        
        for table in self.client.list_tables(dataset_ref):
            full_table = self.client.get_table(table)
            tables.append({
                'table_id': table.table_id,
                'type': table.table_type,
                'num_rows': full_table.num_rows,
                'size_gb': full_table.num_bytes / (1024**3) if full_table.num_bytes else 0,
                'partitioned': full_table.time_partitioning is not None,
                'clustered': full_table.clustering_fields is not None
            })
        
        return tables


# Usage example
manager = BigQueryManager('my-project')

# Create analytics dataset
manager.create_dataset(
    name='analytics',
    location='US',
    description='Core analytics tables'
)

# Create a partitioned and clustered table
schema = [
    bigquery.SchemaField('order_id', 'INT64', mode='REQUIRED'),
    bigquery.SchemaField('customer_id', 'INT64'),
    bigquery.SchemaField('order_date', 'DATE'),
    bigquery.SchemaField('amount', 'FLOAT64'),
    bigquery.SchemaField('product_id', 'STRING'),
]

manager.create_partitioned_table(
    dataset='analytics',
    table='orders',
    schema=schema,
    partition_field='order_date',
    cluster_fields=['customer_id', 'product_id']
)

# List tables
tables = manager.list_tables('analytics')
for t in tables:
    print(f"{t['table_id']}: {t['num_rows']} rows, {t['size_gb']:.2f} GB")
```

## Key Takeaways

- BigQuery hierarchy: Project > Dataset > Table/View
- Datasets are containers with location, access control, and default settings
- Native tables store data in BigQuery; external tables query GCS directly
- Views are logical; materialized views are pre-computed for performance
- Partitioning enables query pruning by date or integer range
- Clustering sorts data within partitions for locality
- Combine partitioning and clustering for optimal performance

## Resources

- BigQuery Datasets: <https://cloud.google.com/bigquery/docs/datasets>
- Table Types: <https://cloud.google.com/bigquery/docs/tables-intro>
- Partitioned Tables: <https://cloud.google.com/bigquery/docs/partitioned-tables>
- Clustering: <https://cloud.google.com/bigquery/docs/clustered-tables>
