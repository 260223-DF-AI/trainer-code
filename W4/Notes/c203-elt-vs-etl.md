# ELT vs ETL

## Learning Objectives

- Understand the difference between ETL and ELT
- Learn when to use each approach
- Recognize the shift to ELT in cloud environments
- Apply the appropriate pattern for your use case

## Why This Matters

The choice between ETL and ELT significantly impacts your data architecture. With cloud data warehouses, ELT has become the preferred approach, leveraging powerful compute engines for transformations.

## Concept Explanation

### ETL vs ELT

```
ETL (Traditional):
Source -> Extract -> Transform -> Load -> Warehouse
                        ^
                   Processing
                   (external)

ELT (Modern):
Source -> Extract -> Load -> Transform -> Warehouse
                                ^
                           Processing
                           (in-warehouse)
```

### Key Differences

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform location | External | In warehouse |
| Processing engine | Spark, Python | SQL, warehouse |
| Storage | Transform before store | Store then transform |
| Flexibility | Fixed transformations | Iterative transforms |
| Historical data | What you designed | Raw data preserved |

### Why ELT for Cloud?

1. **Cheap storage**: Store raw data affordably
2. **Powerful compute**: Warehouses handle transformations
3. **Flexibility**: Re-transform as needs change
4. **Speed**: Load first, transform in parallel
5. **Simplicity**: SQL-based transformations

### ELT Pattern

```python
# ELT: Load raw data, transform in warehouse

# 1. Extract and Load (minimal processing)
def extract_load():
    raw_data = extract_from_source()
    load_to_raw_layer(raw_data)  # Store as-is

# 2. Transform in warehouse (SQL)
TRANSFORM_SQL = """
CREATE OR REPLACE TABLE dataset.clean_orders AS
SELECT 
    order_id,
    customer_id,
    PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    ROUND(amount, 2) as amount
FROM dataset.raw_orders
WHERE order_id IS NOT NULL
"""
```

### Data Transformation Tools for ELT

| Tool | Description |
|------|-------------|
| dbt | SQL-based transformations |
| Dataform | BigQuery transformations |
| SQLMesh | Open-source alternative |

### dbt Example

```sql
-- models/staging/stg_orders.sql
SELECT
    order_id,
    customer_id,
    order_date,
    ROUND(amount, 2) as amount
FROM {{ source('raw', 'orders') }}
WHERE order_id IS NOT NULL

-- models/marts/fct_daily_sales.sql
SELECT
    DATE(order_date) as sale_date,
    COUNT(*) as orders,
    SUM(amount) as revenue
FROM {{ ref('stg_orders') }}
GROUP BY sale_date
```

### When to Use Each

**Use ETL when:**

- Complex transformations (ML, API calls)
- Data reduction needed before storage
- Legacy on-premise systems
- Sensitive data must be masked before loading

**Use ELT when:**

- Cloud data warehouse available
- Need raw data preservation
- SQL can handle transformations
- Flexibility for future changes

## Code Example

```python
class ELTPipeline:
    """Modern ELT pattern."""
    
    def __init__(self, warehouse_client):
        self.client = warehouse_client
    
    def extract_and_load(self, source, target_raw):
        """Load raw data to warehouse."""
        data = source.read()
        self.client.load(data, target_raw)
    
    def transform(self, sql_file):
        """Transform using SQL in warehouse."""
        with open(sql_file) as f:
            sql = f.read()
        self.client.execute(sql)
    
    def run(self):
        # EL: Extract and Load raw
        self.extract_and_load(source, 'raw.orders')
        
        # T: Transform in warehouse
        self.transform('transforms/staging.sql')
        self.transform('transforms/marts.sql')
```

## Key Takeaways

- ETL transforms before loading; ELT transforms after loading
- ELT is preferred for cloud data warehouses
- ELT preserves raw data for flexibility
- Tools like dbt enable SQL-based transformations
- Choose based on transformation complexity and infrastructure

## Resources

- dbt: <https://www.getdbt.com/>
- ELT vs ETL: <https://cloud.google.com/bigquery/docs/migration/pipelines>
