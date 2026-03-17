# File Types Overview

## Learning Objectives

- Understand common data file formats and their characteristics
- Learn when to use CSV, JSON, Parquet, Avro, and ORC
- Compare row-based vs. columnar storage formats
- Make informed format selections for different use cases

## Why This Matters

The choice of file format significantly impacts storage costs, query performance, and processing efficiency. Understanding format characteristics helps you optimize data pipelines and make appropriate trade-offs between human readability, compression, and analytical performance.

## Concept Explanation

### File Format Categories

Data file formats fall into two main categories:

```
+------------------+     +------------------+
|   Row-Based      |     |   Columnar       |
+------------------+     +------------------+
| CSV              |     | Parquet          |
| JSON             |     | ORC              |
| Avro             |     | (Avro columnar)  |
+------------------+     +------------------+
| Better for:      |     | Better for:      |
| - Full row read  |     | - Column queries |
| - Streaming      |     | - Aggregations   |
| - Human reading  |     | - Analytics      |
+------------------+     +------------------+
```

### CSV (Comma-Separated Values)

The simplest and most universal format.

**Example:**

```csv
customer_id,name,email,total_orders
1,John Smith,john@example.com,15
2,Jane Doe,jane@example.com,23
3,Bob Wilson,bob@example.com,8
```

**Characteristics:**

| Aspect | Value |
|--------|-------|
| Type | Text, row-based |
| Schema | Header row (optional) |
| Compression | Not built-in |
| Human Readable | Yes |
| Type Support | Strings only |

**Pros:**

- Universal compatibility
- Human-readable and editable
- Simple to generate

**Cons:**

- No type information
- Inefficient for analytics
- No compression
- Inconsistent handling of special characters

**Use When:**

- Exchanging data with non-technical users
- Simple data exports
- Legacy system integration

### JSON (JavaScript Object Notation)

Self-describing, flexible format for semi-structured data.

**Example:**

```json
[
  {
    "customer_id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "orders": [
      {"id": "O1", "amount": 99.99}
    ]
  }
]
```

**Characteristics:**

| Aspect | Value |
|--------|-------|
| Type | Text, row-based |
| Schema | Self-describing |
| Compression | Not built-in |
| Human Readable | Yes |
| Type Support | String, Number, Boolean, Array, Object, Null |

**Pros:**

- Supports nested structures
- Self-describing
- Web-native

**Cons:**

- Verbose (key names repeated)
- Inefficient for analytics
- Parsing overhead

**Use When:**

- API responses
- Configuration files
- Document-oriented data

### JSON Lines (NDJSON)

One JSON object per line, better for streaming.

**Example:**

```json
{"customer_id": 1, "name": "John Smith", "total": 99.99}
{"customer_id": 2, "name": "Jane Doe", "total": 149.99}
{"customer_id": 3, "name": "Bob Wilson", "total": 49.99}
```

**Use When:**

- Streaming data ingestion
- Log files
- Large datasets that need line-by-line processing

### Parquet

Columnar format optimized for analytics.

**Characteristics:**

| Aspect | Value |
|--------|-------|
| Type | Binary, columnar |
| Schema | Embedded |
| Compression | Built-in (Snappy, Gzip, LZ4) |
| Human Readable | No |
| Type Support | Rich (including nested) |

**Storage Layout:**

```
Parquet File:
+-------------------+
| Row Group 1       |
| +---------------+ |
| | Column A      | |  <- All values for column A together
| +---------------+ |
| | Column B      | |  <- All values for column B together
| +---------------+ |
| | Column C      | |  <- All values for column C together
| +---------------+ |
+-------------------+
| Row Group 2       |
| ...               |
+-------------------+
| Footer (Schema)   |
+-------------------+
```

**Pros:**

- Excellent compression (10x smaller than CSV)
- Column pruning (read only needed columns)
- Schema enforcement
- Predicate pushdown

**Cons:**

- Not human-readable
- Requires special tools to read
- Overhead for small files

**Use When:**

- Data warehouse storage
- Analytical queries
- Spark/Pandas workloads
- Long-term data lake storage

### Avro

Row-based format with schema evolution support.

**Characteristics:**

| Aspect | Value |
|--------|-------|
| Type | Binary, row-based |
| Schema | Separate (JSON schema) |
| Compression | Built-in |
| Human Readable | No (schema is readable) |
| Type Support | Rich |

**Schema Example:**

```json
{
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "customer_id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"]}
  ]
}
```

**Pros:**

- Schema evolution (add/remove fields)
- Compact binary format
- Fast serialization/deserialization
- Good for streaming

**Cons:**

- Not columnar (full row reads)
- Not as compact as Parquet for analytics
- Requires schema management

**Use When:**

- Kafka message serialization
- Schema evolution is critical
- Row-level processing

### ORC (Optimized Row Columnar)

Columnar format, similar to Parquet.

**Characteristics:**

| Aspect | Value |
|--------|-------|
| Type | Binary, columnar |
| Schema | Embedded |
| Compression | Built-in (Zlib, Snappy, LZO) |
| Human Readable | No |
| Origin | Hive ecosystem |

**Pros:**

- Excellent for Hive workloads
- Strong compression
- ACID transaction support

**Cons:**

- Less universal than Parquet
- Primarily Hadoop ecosystem

### Format Comparison

| Feature | CSV | JSON | Parquet | Avro | ORC |
|---------|-----|------|---------|------|-----|
| Compression | None | None | Excellent | Good | Excellent |
| Read Speed (Analytics) | Slow | Slow | Fast | Medium | Fast |
| Schema | None | Self | Embedded | External | Embedded |
| Human Readable | Yes | Yes | No | No | No |
| Nested Data | No | Yes | Yes | Yes | Yes |
| Column Pruning | No | No | Yes | No | Yes |
| Ecosystem | Universal | Web | Analytics | Streaming | Hadoop |

## Code Example

Working with different file formats in Python:

```python
import pandas as pd
import json
from pathlib import Path

class FileFormatDemo:
    """Demonstrate different file formats."""
    
    def __init__(self):
        # Sample data
        self.data = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'name': ['John Smith', 'Jane Doe', 'Bob Wilson'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
            'total_orders': [15, 23, 8],
            'total_spent': [1500.50, 2345.00, 899.99]
        })
    
    def save_csv(self, path: str):
        """Save as CSV."""
        self.data.to_csv(path, index=False)
        return Path(path).stat().st_size
    
    def save_json(self, path: str):
        """Save as JSON."""
        self.data.to_json(path, orient='records', indent=2)
        return Path(path).stat().st_size
    
    def save_jsonl(self, path: str):
        """Save as JSON Lines."""
        self.data.to_json(path, orient='records', lines=True)
        return Path(path).stat().st_size
    
    def save_parquet(self, path: str):
        """Save as Parquet with compression."""
        self.data.to_parquet(path, compression='snappy')
        return Path(path).stat().st_size
    
    def compare_formats(self, base_path: str) -> dict:
        """Compare file sizes across formats."""
        results = {}
        
        formats = {
            'CSV': (f'{base_path}.csv', self.save_csv),
            'JSON': (f'{base_path}.json', self.save_json),
            'JSON Lines': (f'{base_path}.jsonl', self.save_jsonl),
            'Parquet': (f'{base_path}.parquet', self.save_parquet)
        }
        
        for name, (path, save_func) in formats.items():
            size = save_func(path)
            results[name] = size
        
        return results
    
    def read_performance_test(self, path_prefix: str, iterations: int = 100):
        """Compare read performance."""
        import time
        
        results = {}
        
        # Test CSV
        start = time.time()
        for _ in range(iterations):
            pd.read_csv(f'{path_prefix}.csv')
        results['CSV'] = (time.time() - start) / iterations
        
        # Test JSON
        start = time.time()
        for _ in range(iterations):
            pd.read_json(f'{path_prefix}.json')
        results['JSON'] = (time.time() - start) / iterations
        
        # Test Parquet
        start = time.time()
        for _ in range(iterations):
            pd.read_parquet(f'{path_prefix}.parquet')
        results['Parquet'] = (time.time() - start) / iterations
        
        return results
    
    def column_pruning_demo(self, parquet_path: str):
        """
        Demonstrate Parquet column pruning.
        Only reads specified columns from disk.
        """
        # Read only specific columns - efficient
        df = pd.read_parquet(parquet_path, columns=['customer_id', 'total_spent'])
        return df


# Usage
demo = FileFormatDemo()
sizes = demo.compare_formats('/tmp/data_comparison')

print("File Size Comparison:")
for format_name, size in sizes.items():
    print(f"  {format_name}: {size:,} bytes")

# At scale (millions of rows), expect:
# Parquet: 10-30% of CSV size
# JSON: 150-200% of CSV size
```

## Key Takeaways

- CSV is universal but inefficient; use for simple data exchange
- JSON is flexible for semi-structured data; use for APIs and configs
- Parquet is optimal for analytics with excellent compression and column pruning
- Avro excels at schema evolution; use for streaming and Kafka
- ORC is similar to Parquet; preferred in Hadoop/Hive environments
- Choose row-based (CSV, JSON, Avro) for full-row access and streaming
- Choose columnar (Parquet, ORC) for analytical queries and data lakes

## Resources

- Apache Parquet: <https://parquet.apache.org/>
- Apache Avro: <https://avro.apache.org/>
- Apache ORC: <https://orc.apache.org/>
- Pandas I/O: <https://pandas.pydata.org/docs/reference/io.html>
