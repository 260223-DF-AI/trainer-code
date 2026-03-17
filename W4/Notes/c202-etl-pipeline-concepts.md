# ETL Pipeline Concepts

## Learning Objectives

- Define ETL and its role in data engineering
- Understand the E-T-L stages
- Learn common ETL patterns and tools
- Compare batch vs. streaming ETL

## Why This Matters

ETL (Extract, Transform, Load) pipelines are the foundation of data engineering. They move data from operational systems to analytical environments, enabling business intelligence and data-driven decisions.

## Concept Explanation

### What is ETL?

ETL stands for Extract, Transform, Load - the three stages of moving data from sources to targets.

```
+----------+     +-----------+     +--------+     +-----------+
| Source   | --> | Extract   | --> |Transform| --> | Load      |
| Systems  |     |           |     |         |     |           |
+----------+     +-----------+     +---------+     +-----------+
                      |                |                |
                      v                v                v
                 Raw data        Cleaned data    Target system
                 as-is           transformed     warehouse/lake
```

### The Three Stages

#### Extract

Pull data from source systems:

```python
# Example: Extract from multiple sources
def extract_data():
    # From database
    orders = query_database("SELECT * FROM orders WHERE date > yesterday")
    
    # From API
    weather = call_api("https://api.weather.com/daily")
    
    # From files
    logs = read_files("s3://bucket/logs/*.json")
    
    return orders, weather, logs
```

**Source Types:**

- Databases (PostgreSQL, MySQL, Oracle)
- APIs (REST, GraphQL)
- Files (CSV, JSON, Parquet)
- Streaming (Kafka, Pub/Sub)

#### Transform

Clean, validate, and reshape data:

```python
def transform_orders(raw_orders):
    # Clean
    cleaned = raw_orders.dropna(subset=['order_id', 'customer_id'])
    
    # Standardize
    cleaned['order_date'] = pd.to_datetime(cleaned['order_date'])
    cleaned['amount'] = cleaned['amount'].round(2)
    
    # Enrich
    cleaned['order_month'] = cleaned['order_date'].dt.to_period('M')
    
    # Aggregate
    summary = cleaned.groupby('customer_id').agg({
        'amount': 'sum',
        'order_id': 'count'
    })
    
    return cleaned, summary
```

**Common Transformations:**

- Data cleaning (nulls, duplicates)
- Type conversion
- Standardization (formats, codes)
- Aggregation
- Joining/enrichment
- Derived fields

#### Load

Write data to target systems:

```python
def load_to_warehouse(data, table_name, mode='append'):
    # Load to BigQuery
    data.to_gbq(
        destination_table=f'dataset.{table_name}',
        if_exists=mode
    )
```

**Load Strategies:**

- Full refresh (replace all)
- Incremental (append new)
- Upsert (update or insert)
- Merge (SCD Type 2)

### Batch vs. Streaming

| Aspect | Batch ETL | Streaming ETL |
|--------|-----------|---------------|
| Frequency | Scheduled | Continuous |
| Latency | Hours | Seconds |
| Data volume | Large batches | Small events |
| Tools | Spark, Airflow | Kafka, Flink |
| Use case | Reporting | Real-time |

### Common ETL Tools

| Category | Tools |
|----------|-------|
| Orchestration | Airflow, Prefect, Dagster |
| Processing | Spark, dbt, Pandas |
| Streaming | Kafka, Flink, Dataflow |
| Cloud | Dataflow, Glue, Data Factory |

## Code Example

```python
from datetime import datetime

class ETLPipeline:
    def __init__(self, source, target):
        self.source = source
        self.target = target
    
    def extract(self):
        """Extract data from source."""
        return self.source.read()
    
    def transform(self, raw_data):
        """Transform raw data."""
        # Clean
        cleaned = raw_data.dropna()
        # Transform
        cleaned['processed_at'] = datetime.now()
        return cleaned
    
    def load(self, data):
        """Load to target."""
        self.target.write(data)
    
    def run(self):
        """Execute ETL pipeline."""
        raw = self.extract()
        transformed = self.transform(raw)
        self.load(transformed)
        print(f"ETL complete: {len(transformed)} rows")

# Usage
pipeline = ETLPipeline(source=DatabaseSource(), target=BigQueryTarget())
pipeline.run()
```

## Key Takeaways

- ETL: Extract from sources, Transform data, Load to targets
- Extract handles diverse sources (DBs, APIs, files)
- Transform cleans, validates, and reshapes data
- Load writes to warehouses, lakes, or other targets
- Choose batch for scheduled loads, streaming for real-time

## Resources

- ETL Overview: <https://cloud.google.com/learn/what-is-etl>
