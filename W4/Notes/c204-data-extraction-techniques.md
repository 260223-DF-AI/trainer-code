# Data Extraction Techniques

## Learning Objectives

- Learn different data extraction methods
- Understand full vs. incremental extraction
- Apply change data capture (CDC) concepts
- Handle various source types

## Why This Matters

Efficient data extraction is the foundation of any pipeline. The extraction method affects data freshness, source system load, and pipeline complexity. Choosing the right approach balances these factors.

## Concept Explanation

### Extraction Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| Full | Extract all data each time | Small tables, dimension data |
| Incremental | Extract only new/changed | Large tables, frequent updates |
| CDC | Capture changes as they happen | Real-time, minimal impact |

### Full Extraction

Extract entire table every run:

```python
def full_extract(source_table):
    """Extract all rows from source."""
    return db.query(f"SELECT * FROM {source_table}")
```

**Pros:**

- Simple to implement
- Guarantees completeness
- Good for small tables

**Cons:**

- Slow for large tables
- Heavy load on source
- Redundant data transfer

### Incremental Extraction

Extract only new or changed records:

```python
def incremental_extract(source_table, watermark_column, last_value):
    """Extract rows since last run."""
    return db.query(f"""
        SELECT * FROM {source_table}
        WHERE {watermark_column} > '{last_value}'
    """)

# Usage
last_run = get_watermark('orders')
new_orders = incremental_extract('orders', 'updated_at', last_run)
update_watermark('orders', datetime.now())
```

**Watermark Strategies:**

- Timestamp-based: `WHERE updated_at > last_run`
- ID-based: `WHERE id > last_id`
- Partition-based: Extract new partitions only

### Change Data Capture (CDC)

Capture changes from database logs:

```
Database    Transaction    CDC Tool      Target
            Log
+------+    +------+      +------+      +------+
|INSERT| -> |  Log | ->   |Debezium| -> |Kafka | -> Warehouse
|UPDATE|    |entry |      |        |    |      |
|DELETE|    +------+      +------+      +------+
+------+
```

**CDC Benefits:**

- Near real-time updates
- Minimal source impact
- Captures deletes
- Full change history

### Source-Specific Extraction

#### Database Sources

```python
import sqlalchemy

def extract_from_db(connection_string, query):
    engine = sqlalchemy.create_engine(connection_string)
    return pd.read_sql(query, engine)
```

#### API Sources

```python
import requests

def extract_from_api(url, params):
    response = requests.get(url, params=params)
    return response.json()
```

#### File Sources

```python
def extract_from_files(path, format):
    if format == 'csv':
        return pd.read_csv(path)
    elif format == 'parquet':
        return pd.read_parquet(path)
    elif format == 'json':
        return pd.read_json(path)
```

### Choosing Extraction Method

| Factor | Full | Incremental | CDC |
|--------|------|-------------|-----|
| Table size | Small | Large | Any |
| Update frequency | Low | Medium | High |
| Source impact | High | Medium | Low |
| Complexity | Low | Medium | High |
| Delete detection | Yes | Difficult | Yes |

## Code Example

```python
class DataExtractor:
    """Handle various extraction methods."""
    
    def __init__(self, source_config):
        self.config = source_config
    
    def full_extract(self, table):
        return self._query(f"SELECT * FROM {table}")
    
    def incremental_extract(self, table, watermark_col, last_value):
        return self._query(f"""
            SELECT * FROM {table}
            WHERE {watermark_col} > '{last_value}'
        """)
    
    def _query(self, sql):
        # Execute query against source
        return execute_query(self.config, sql)

# Usage
extractor = DataExtractor(config)

# Small dimension table - full extract
customers = extractor.full_extract('customers')

# Large fact table - incremental
last_run = get_watermark('orders')
new_orders = extractor.incremental_extract('orders', 'updated_at', last_run)
```

## Key Takeaways

- Full extraction: Simple but slow for large tables
- Incremental extraction: Efficient, requires watermark column
- CDC: Real-time, captures all changes including deletes
- Choose based on table size, update frequency, and requirements
- Handle different sources (DB, API, files) appropriately

## Resources

- Debezium CDC: <https://debezium.io/>
