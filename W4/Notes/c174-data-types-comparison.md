# Data Types Comparison

## Learning Objectives

- Compare structured, semi-structured, and unstructured data
- Understand trade-offs for each data type
- Learn which storage and processing tools suit each type
- Apply selection criteria to real-world scenarios

## Why This Matters

Data professionals work with all three data types daily. Choosing the right storage, processing, and analysis approach depends on understanding the characteristics of each type. This knowledge helps you design appropriate data architectures and select the right tools for each use case.

## Concept Explanation

### The Data Type Spectrum

Data exists on a spectrum from fully structured to completely unstructured:

```
   Structured          Semi-Structured        Unstructured
       |                     |                     |
+------+------+       +------+------+       +------+------+
|   Tables    |       |    JSON     |       |   Images    |
|   Fixed     |       |    XML      |       |   Video     |
|   Schema    |       |    YAML     |       |   Text      |
+-------------+       +-------------+       +-------------+
       |                     |                     |
  ~10-20%                ~10-15%               ~70-80%
  of data                of data               of data
```

### Feature Comparison

| Feature | Structured | Semi-Structured | Unstructured |
|---------|------------|-----------------|--------------|
| Schema | Fixed, predefined | Flexible, self-describing | None |
| Storage | RDBMS, DWH | Document DB, Object Store | Object Store, Files |
| Query | SQL | JSON/XML queries | Full-text, AI |
| Examples | Tables, CSV | JSON, XML, Parquet | Images, PDFs, video |
| Percentage | 10-20% | 10-15% | 70-80% |
| Analysis | Straightforward | Moderate complexity | Requires AI/ML |

### Storage Comparison

| Aspect | Structured | Semi-Structured | Unstructured |
|--------|------------|-----------------|--------------|
| Primary Storage | PostgreSQL, BigQuery | MongoDB, S3+Athena | S3, GCS, Blob |
| Format | Tables | JSON, Parquet, Avro | Files (any) |
| Indexing | B-tree, Hash | Document indexes | Full-text, Vector |
| Compression | High (columnar) | Good | Variable |
| Cost | Higher (compute) | Medium | Lower (storage) |

### Processing Comparison

```
Structured Data Pipeline:
Source --> Load to DWH --> SQL Query --> Dashboard

Semi-Structured Data Pipeline:
Source --> Parse JSON --> Transform --> Load to DWH --> Query

Unstructured Data Pipeline:
Source --> Extract (OCR/NLP) --> Enrich --> Index --> Search/Analyze
```

**Processing Requirements:**

| Data Type | CPU | GPU | Complexity |
|-----------|-----|-----|------------|
| Structured | Low-Medium | No | Low |
| Semi-Structured | Medium | Rarely | Medium |
| Unstructured | Medium-High | Often (AI/ML) | High |

### Query Capabilities

**Structured Data:**

```sql
-- Direct, precise queries
SELECT customer_name, SUM(order_total)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_name
HAVING SUM(order_total) > 1000;
```

**Semi-Structured Data:**

```sql
-- BigQuery JSON functions
SELECT 
  JSON_VALUE(data, '$.customer.name') as customer_name,
  CAST(JSON_VALUE(data, '$.total') AS FLOAT64) as total
FROM orders_json
WHERE JSON_VALUE(data, '$.status') = 'completed';
```

**Unstructured Data:**

```python
# Natural language search with embeddings
query = "Find contracts mentioning payment terms over 60 days"
results = vector_search.similarity_search(
    query_embedding=embed(query),
    top_k=10
)
```

### Selection Criteria

**Choose Structured When:**

- Schema is stable and well-defined
- Need for strong data consistency
- Complex relational queries required
- Transactional integrity is critical
- Team is SQL-experienced

**Choose Semi-Structured When:**

- Schema evolves frequently
- Data is hierarchical or nested
- Integrating diverse sources
- Need for flexibility
- Working with APIs/web data

**Choose Unstructured When:**

- Data is inherently unstructured (images, video)
- Need to preserve original format
- AI/ML is required for analysis
- Volume is very high
- Storage cost is primary concern

### Hybrid Architectures

Modern systems often combine all three types:

```
+---------------+     +---------------+     +---------------+
|  Unstructured |     | Semi-Structured|     |   Structured  |
|    (Raw)      |     |   (Enriched)   |     |   (Curated)   |
+---------------+     +---------------+     +---------------+
| - Raw images  |     | - Extracted    |     | - Aggregates  |
| - Documents   | --> |   metadata     | --> | - KPIs        |
| - Logs        |     | - JSON records |     | - Reports     |
+---------------+     +---------------+     +---------------+
     Data Lake           Data Lake            Data Warehouse
```

**Example: Document Processing Pipeline**

1. **Unstructured**: Raw PDF contracts stored in Cloud Storage
2. **Semi-Structured**: Document AI extracts entities to JSON
3. **Structured**: Key terms loaded to BigQuery for analysis

## Code Example

Working with all three data types:

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Union
from enum import Enum
import json

class DataType(Enum):
    STRUCTURED = "structured"
    SEMI_STRUCTURED = "semi-structured"
    UNSTRUCTURED = "unstructured"

@dataclass
class DataCharacteristics:
    data_type: DataType
    has_schema: bool
    is_nested: bool
    storage_recommendation: str
    processing_approach: str

class DataTypeAnalyzer:
    """Analyze and classify data by type."""
    
    def classify(self, data: Any, source_type: str = None) -> DataCharacteristics:
        """Classify data and provide recommendations."""
        
        # Check for structured data
        if self._is_structured(data, source_type):
            return DataCharacteristics(
                data_type=DataType.STRUCTURED,
                has_schema=True,
                is_nested=False,
                storage_recommendation="Use relational DB (PostgreSQL) or data warehouse (BigQuery)",
                processing_approach="Direct SQL queries, no transformation needed"
            )
        
        # Check for semi-structured data
        if self._is_semi_structured(data, source_type):
            return DataCharacteristics(
                data_type=DataType.SEMI_STRUCTURED,
                has_schema=True,  # Self-describing
                is_nested=self._has_nesting(data),
                storage_recommendation="Use document DB (MongoDB) or object storage + query (S3+Athena)",
                processing_approach="Parse and flatten, or query directly with JSON functions"
            )
        
        # Default to unstructured
        return DataCharacteristics(
            data_type=DataType.UNSTRUCTURED,
            has_schema=False,
            is_nested=False,
            storage_recommendation="Use object storage (S3/GCS) with metadata enrichment",
            processing_approach="Extract structure using AI/ML, then load to structured system"
        )
    
    def _is_structured(self, data: Any, source_type: str) -> bool:
        """Check if data is structured."""
        structured_indicators = ['csv', 'sql', 'table', 'database']
        if source_type and any(ind in source_type.lower() for ind in structured_indicators):
            return True
        
        # Check if data is list of flat dicts with consistent keys
        if isinstance(data, list) and len(data) > 0:
            if all(isinstance(item, dict) for item in data):
                first_keys = set(data[0].keys())
                if all(set(item.keys()) == first_keys for item in data):
                    # Check if values are all primitives (not nested)
                    if all(not isinstance(v, (dict, list)) for item in data for v in item.values()):
                        return True
        return False
    
    def _is_semi_structured(self, data: Any, source_type: str) -> bool:
        """Check if data is semi-structured."""
        semi_indicators = ['json', 'xml', 'yaml', 'parquet', 'avro']
        if source_type and any(ind in source_type.lower() for ind in semi_indicators):
            return True
        
        # Check for dict/list with nesting
        if isinstance(data, (dict, list)):
            return True
        
        # Try to parse as JSON
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, (dict, list)):
                    return True
            except json.JSONDecodeError:
                pass
        
        return False
    
    def _has_nesting(self, data: Any) -> bool:
        """Check if data has nested structures."""
        if isinstance(data, dict):
            return any(isinstance(v, (dict, list)) for v in data.values())
        if isinstance(data, list) and len(data) > 0:
            return any(isinstance(item, (dict, list)) for item in data)
        return False


# Example usage
analyzer = DataTypeAnalyzer()

# Structured data example
structured_data = [
    {"id": 1, "name": "John", "age": 30},
    {"id": 2, "name": "Jane", "age": 25},
    {"id": 3, "name": "Bob", "age": 35}
]
result = analyzer.classify(structured_data, "csv")
print(f"Data Type: {result.data_type.value}")
print(f"Storage: {result.storage_recommendation}")

# Semi-structured data example
semi_structured_data = {
    "customer": {
        "id": 1,
        "name": {"first": "John", "last": "Smith"},
        "orders": [
            {"id": "O1", "total": 100},
            {"id": "O2", "total": 200}
        ]
    }
}
result = analyzer.classify(semi_structured_data, "json")
print(f"\nData Type: {result.data_type.value}")
print(f"Has Nesting: {result.is_nested}")
print(f"Processing: {result.processing_approach}")

# Unstructured data example
unstructured_data = b"This is raw PDF binary content..."
result = analyzer.classify(unstructured_data, "pdf")
print(f"\nData Type: {result.data_type.value}")
print(f"Storage: {result.storage_recommendation}")
```

## Key Takeaways

- Structured data (~10-20%) has fixed schema and is best for SQL analytics
- Semi-structured data (~10-15%) is flexible and suits evolving schemas
- Unstructured data (~70-80%) requires AI/ML for meaningful analysis
- Storage choices depend on data type: RDBMS, document stores, or object storage
- Query capabilities vary: SQL for structured, JSON functions for semi-structured, AI for unstructured
- Modern architectures combine all three types in a data lakehouse approach
- Choose data type handling based on schema stability, query patterns, and team skills

## Resources

- Data Types in BigQuery: <https://cloud.google.com/bigquery/docs/nested-repeated>
- MongoDB vs SQL: <https://www.mongodb.com/nosql-explained/nosql-vs-sql>
- Modern Data Stack: <https://moderndatastack.xyz/>
