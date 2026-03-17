# Star Schema

## Learning Objectives

- Understand star schema structure and components
- Design effective star schemas
- Learn when star schema is appropriate
- Apply star schema best practices

## Why This Matters

Star schema is the most common dimensional modeling pattern. Its simplicity makes it ideal for analytical workloads, enabling fast queries and intuitive data exploration for business users.

## Concept Explanation

### Star Schema Structure

```
                        +----------+
                        | dim_date |
                        +----+-----+
                             |
+----------+          +------+------+          +----------+
| dim_     |          |             |          | dim_     |
| customer |--------->| fact_sales  |<---------| product  |
+----------+          |             |          +----------+
                      +------+------+
                             |
                        +----+-----+
                        | dim_store|
                        +----------+
```

The star schema gets its name from the star-like appearance when diagrammed: a central fact table surrounded by dimension tables.

### Components

#### Central Fact Table

```sql
CREATE TABLE fact_sales (
    -- Surrogate keys (FK to dimensions)
    date_key INT64 NOT NULL,
    customer_key INT64 NOT NULL,
    product_key INT64 NOT NULL,
    store_key INT64 NOT NULL,
    
    -- Measures
    quantity INT64,
    unit_price NUMERIC(10,2),
    discount_percent NUMERIC(5,2),
    total_revenue NUMERIC(12,2),
    
    -- Degenerate dimension
    transaction_id STRING
)
PARTITION BY date_key;
```

#### Surrounding Dimension Tables

```sql
CREATE TABLE dim_date (
    date_key INT64 PRIMARY KEY,
    full_date DATE,
    year INT64,
    quarter INT64,
    month INT64,
    month_name STRING,
    week INT64,
    day_of_week INT64,
    day_name STRING,
    is_weekend BOOL,
    is_holiday BOOL
);

CREATE TABLE dim_product (
    product_key INT64 PRIMARY KEY,
    product_id STRING,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    supplier STRING,
    unit_cost NUMERIC(10,2)
);

CREATE TABLE dim_customer (
    customer_key INT64 PRIMARY KEY,
    customer_id STRING,
    customer_name STRING,
    email STRING,
    segment STRING,
    region STRING,
    country STRING
);

CREATE TABLE dim_store (
    store_key INT64 PRIMARY KEY,
    store_id STRING,
    store_name STRING,
    city STRING,
    state STRING,
    country STRING,
    store_type STRING
);
```

### Star Schema Query

```sql
SELECT 
    d.year,
    d.quarter,
    p.category,
    s.region,
    SUM(f.total_revenue) as revenue,
    SUM(f.quantity) as units_sold
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_store s ON f.store_key = s.store_key
WHERE d.year = 2024
GROUP BY d.year, d.quarter, p.category, s.region
ORDER BY d.quarter, revenue DESC;
```

### Key Design Principles

1. **Denormalization**: Dimensions contain redundant data
2. **Surrogate Keys**: Integer keys for joins (not business keys)
3. **Single Join Path**: Each dimension connects directly to fact
4. **Wide Dimensions**: Many attributes per dimension

### Advantages

| Advantage | Description |
|-----------|-------------|
| Simple Queries | Few joins, intuitive SQL |
| Fast Performance | Optimized for aggregations |
| User-Friendly | Business users understand it |
| BI Tool Compatible | Works with all analytics tools |
| Flexible | Easy to add dimensions |

### When to Use Star Schema

- Analytical/reporting workloads
- Data warehouse implementations
- BI dashboards and reports
- Ad-hoc analysis

## Code Example

```python
def create_star_schema_tables(client):
    """Create a star schema in BigQuery."""
    
    # Date dimension
    client.query("""
        CREATE OR REPLACE TABLE dataset.dim_date AS
        SELECT 
            FORMAT_DATE('%Y%m%d', d) AS date_key,
            d AS full_date,
            EXTRACT(YEAR FROM d) AS year,
            EXTRACT(QUARTER FROM d) AS quarter,
            EXTRACT(MONTH FROM d) AS month,
            FORMAT_DATE('%B', d) AS month_name
        FROM UNNEST(GENERATE_DATE_ARRAY('2020-01-01', '2030-12-31')) AS d
    """).result()
    
    print("Star schema created")
```

## Key Takeaways

- Star schema has a central fact table surrounded by dimensions
- Dimensions are fully denormalized (redundant data allowed)
- Uses surrogate keys for efficient joins
- Simple structure enables fast queries and easy understanding
- Best for analytical workloads and BI tools

## Resources

- Star Schema: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/>
