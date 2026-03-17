# BigQuery Data Types

## Learning Objectives

- Learn the data types available in BigQuery
- Understand when to use each data type
- Work with complex types: ARRAY, STRUCT
- Apply best practices for schema design

## Why This Matters

Choosing the right data types is crucial for query performance, storage efficiency, and data integrity. BigQuery supports a rich set of data types including complex nested structures.

## Concept Explanation

### Data Type Categories

| Category | Types |
|----------|-------|
| Numeric | INT64, FLOAT64, NUMERIC, BIGNUMERIC |
| String | STRING, BYTES |
| Date/Time | DATE, TIME, DATETIME, TIMESTAMP |
| Boolean | BOOL |
| Complex | ARRAY, STRUCT |
| Specialized | GEOGRAPHY, JSON, INTERVAL |

### Numeric Types

| Type | Use Case | Example |
|------|----------|---------|
| INT64 | IDs, counts | `customer_id INT64` |
| FLOAT64 | Scientific data | `temperature FLOAT64` |
| NUMERIC | Financial data | `price NUMERIC(15,2)` |
| BIGNUMERIC | High precision | 76 digits precision |

**Best Practice**: Use NUMERIC for money, never FLOAT64.

```sql
CREATE TABLE transactions (
    amount NUMERIC(15, 2),
    tax NUMERIC(15, 2)
);
```

### Date and Time Types

| Type | Description | Example |
|------|-------------|---------|
| DATE | Calendar date | `2024-01-15` |
| TIME | Time of day | `14:30:00` |
| DATETIME | Date + Time (no TZ) | `2024-01-15 14:30:00` |
| TIMESTAMP | Absolute UTC time | `2024-01-15 14:30:00 UTC` |

```sql
SELECT 
    DATE '2024-01-15' as report_date,
    CURRENT_TIMESTAMP() as now,
    EXTRACT(YEAR FROM DATE '2024-01-15') as year;
```

### ARRAY Type

Store ordered lists:

```sql
CREATE TABLE users (
    user_id INT64,
    tags ARRAY<STRING>,
    scores ARRAY<INT64>
);

-- Query arrays
SELECT 
    user_id,
    ARRAY_LENGTH(tags) as tag_count,
    'premium' IN UNNEST(tags) as is_premium
FROM users;

-- Expand arrays
SELECT user_id, tag
FROM users, UNNEST(tags) as tag;
```

### STRUCT Type

Store nested records:

```sql
CREATE TABLE orders (
    order_id INT64,
    customer STRUCT<id INT64, name STRING, email STRING>,
    order_date DATE
);

-- Query struct fields
SELECT 
    order_id,
    customer.name as customer_name
FROM orders;
```

### Nested and Repeated

Combine ARRAY and STRUCT for hierarchies:

```sql
CREATE TABLE orders_nested (
    order_id INT64,
    items ARRAY<STRUCT<
        product_id STRING,
        quantity INT64,
        price NUMERIC
    >>
);

-- Query nested data
SELECT 
    order_id,
    (SELECT SUM(quantity) FROM UNNEST(items)) as total_items
FROM orders_nested;
```

## Code Example

```python
from google.cloud import bigquery

def create_schema() -> list:
    return [
        bigquery.SchemaField('order_id', 'INT64', mode='REQUIRED'),
        bigquery.SchemaField('created_at', 'TIMESTAMP'),
        bigquery.SchemaField('total', 'NUMERIC'),
        bigquery.SchemaField('shipping_address', 'STRUCT', fields=[
            bigquery.SchemaField('city', 'STRING'),
            bigquery.SchemaField('state', 'STRING'),
        ]),
        bigquery.SchemaField('items', 'STRUCT', mode='REPEATED', fields=[
            bigquery.SchemaField('product_id', 'STRING'),
            bigquery.SchemaField('quantity', 'INT64'),
        ]),
    ]
```

## Key Takeaways

- Use INT64 for IDs; NUMERIC for financial data
- TIMESTAMP for UTC time; DATE/DATETIME for calendar time
- ARRAY stores lists; STRUCT stores nested records
- Combine ARRAY and STRUCT for one-to-many relationships

## Resources

- BigQuery Data Types: <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types>
