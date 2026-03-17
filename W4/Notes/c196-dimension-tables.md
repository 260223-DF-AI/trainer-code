# Dimension Tables

## Learning Objectives

- Design effective dimension tables
- Understand surrogate vs. natural keys
- Learn common dimension patterns
- Apply dimension best practices

## Why This Matters

Dimension tables provide the context for analyzing facts. Well-designed dimensions enable intuitive analysis and flexible reporting. They are the key to making data warehouses user-friendly.

## Concept Explanation

### What are Dimension Tables?

Dimension tables contain descriptive attributes that provide context for facts. They answer the "who, what, when, where, why" of business events.

### Anatomy of a Dimension

```sql
CREATE TABLE dim_customer (
    -- Surrogate Key (Primary Key)
    customer_key INT64 NOT NULL,
    
    -- Natural Key (Business Identifier)
    customer_id STRING,
    
    -- Attributes
    first_name STRING,
    last_name STRING,
    full_name STRING,
    email STRING,
    phone STRING,
    
    -- Hierarchies
    city STRING,
    state STRING,
    region STRING,
    country STRING,
    
    -- Derived Attributes
    customer_segment STRING,
    acquisition_channel STRING,
    
    -- Audit Columns
    effective_date DATE,
    end_date DATE,
    is_current BOOL
);
```

### Surrogate vs. Natural Keys

| Key Type | Description | Example |
|----------|-------------|---------|
| Surrogate | System-generated integer | 12345 |
| Natural | Business identifier | CUST-ABC-001 |

**Always use surrogate keys for:**

- Faster joins (integers)
- Independence from source systems
- Historical tracking

### Common Dimensions

#### Date Dimension

Every fact table needs a date dimension:

```sql
CREATE TABLE dim_date (
    date_key INT64,           -- YYYYMMDD format
    full_date DATE,
    year INT64,
    quarter INT64,
    month INT64,
    month_name STRING,
    week_of_year INT64,
    day_of_month INT64,
    day_of_week INT64,
    day_name STRING,
    is_weekend BOOL,
    is_holiday BOOL,
    fiscal_year INT64,
    fiscal_quarter INT64
);
```

#### Product Dimension

```sql
CREATE TABLE dim_product (
    product_key INT64,
    product_id STRING,
    product_name STRING,
    description STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    supplier STRING,
    unit_cost NUMERIC,
    unit_price NUMERIC
);
```

### Dimension Hierarchies

Hierarchies enable drill-down analysis:

```
Geography Hierarchy:
Country -> Region -> State -> City -> Store

Product Hierarchy:
Department -> Category -> Subcategory -> Product

Time Hierarchy:
Year -> Quarter -> Month -> Week -> Day
```

### Role-Playing Dimensions

Same dimension used multiple times:

```sql
-- Order fact with multiple date roles
CREATE TABLE fact_orders (
    order_date_key INT64,     -- -> dim_date
    ship_date_key INT64,      -- -> dim_date (same table)
    delivery_date_key INT64,  -- -> dim_date (same table)
    ...
);
```

### Junk Dimensions

Combine low-cardinality flags:

```sql
-- Instead of many boolean columns in fact
CREATE TABLE dim_transaction_flags (
    flag_key INT64,
    is_online BOOL,
    is_gift BOOL,
    is_promotion BOOL,
    payment_type STRING  -- 'Credit', 'Cash', 'Check'
);
```

### Dimension Best Practices

1. **Use surrogate keys**: System-generated integers
2. **Include natural keys**: Keep business identifiers
3. **Denormalize fully**: Include all descriptive attributes
4. **Provide hierarchies**: Enable drill-down analysis
5. **Add audit columns**: Track data lineage

## Code Example

```python
def create_date_dimension(client, start_date, end_date):
    """Generate a complete date dimension."""
    
    sql = f"""
    CREATE OR REPLACE TABLE dataset.dim_date AS
    SELECT 
        CAST(FORMAT_DATE('%Y%m%d', d) AS INT64) AS date_key,
        d AS full_date,
        EXTRACT(YEAR FROM d) AS year,
        EXTRACT(QUARTER FROM d) AS quarter,
        EXTRACT(MONTH FROM d) AS month,
        FORMAT_DATE('%B', d) AS month_name,
        EXTRACT(WEEK FROM d) AS week_of_year,
        EXTRACT(DAY FROM d) AS day_of_month,
        EXTRACT(DAYOFWEEK FROM d) AS day_of_week,
        FORMAT_DATE('%A', d) AS day_name,
        EXTRACT(DAYOFWEEK FROM d) IN (1, 7) AS is_weekend
    FROM UNNEST(
        GENERATE_DATE_ARRAY('{start_date}', '{end_date}')
    ) AS d
    """
    
    client.query(sql).result()
    print("Date dimension created")
```

## Key Takeaways

- Dimensions provide context for facts (who, what, when, where)
- Use surrogate keys for joins, keep natural keys for reference
- Denormalize to include all descriptive attributes
- Date dimension is essential for every data warehouse
- Role-playing dimensions reuse the same table for different purposes

## Resources

- Dimension Design: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/>
