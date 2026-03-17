# Fact Tables

## Learning Objectives

- Understand different types of fact tables
- Design effective fact table schemas
- Choose appropriate grain for facts
- Apply fact table best practices

## Why This Matters

Fact tables are the heart of dimensional models. They store the measurements that business users analyze. Understanding fact table design is essential for building effective data warehouses.

## Concept Explanation

### What are Fact Tables?

Fact tables store quantitative data about business events. Each row represents a measurement at a specific grain (level of detail).

### Fact Table Components

```sql
CREATE TABLE fact_sales (
    -- Surrogate Keys (Foreign Keys)
    date_key INT64,
    customer_key INT64,
    product_key INT64,
    store_key INT64,
    
    -- Degenerate Dimensions
    transaction_number STRING,
    
    -- Measures
    quantity INT64,           -- Additive
    unit_price NUMERIC,       -- Non-additive
    discount_amount NUMERIC,  -- Additive
    total_revenue NUMERIC     -- Additive
);
```

### Types of Measures

| Type | Description | Example |
|------|-------------|---------|
| Additive | Can sum across all dimensions | Revenue, quantity |
| Semi-Additive | Can sum across some dimensions | Account balance |
| Non-Additive | Cannot be summed | Unit price, ratio |

### Types of Fact Tables

#### 1. Transaction Fact Table

One row per transaction event:

```sql
-- Each sale is a row
CREATE TABLE fact_sales_transaction (
    date_key INT64,
    customer_key INT64,
    product_key INT64,
    quantity INT64,
    amount NUMERIC
);
-- Grain: One row per line item
```

#### 2. Periodic Snapshot Fact Table

One row per time period:

```sql
-- Daily inventory snapshot
CREATE TABLE fact_inventory_snapshot (
    date_key INT64,
    product_key INT64,
    store_key INT64,
    quantity_on_hand INT64,
    quantity_on_order INT64
);
-- Grain: One row per product/store/day
```

#### 3. Accumulating Snapshot Fact Table

One row per process instance, updated as process progresses:

```sql
CREATE TABLE fact_order_fulfillment (
    order_key INT64,
    order_date_key INT64,
    ship_date_key INT64,      -- Updated when shipped
    delivery_date_key INT64,  -- Updated when delivered
    days_to_ship INT64,
    days_to_deliver INT64
);
-- Grain: One row per order
```

### Choosing Grain

The grain defines what one row represents:

| Grain | Example |
|-------|---------|
| Transaction | One row per sales line item |
| Daily | One row per product per day |
| Monthly | One row per customer per month |

**Best Practice**: Start with the finest grain possible.

### Factless Fact Tables

Record events without measures:

```sql
-- Student class enrollment
CREATE TABLE fact_enrollment (
    date_key INT64,
    student_key INT64,
    course_key INT64,
    instructor_key INT64
    -- No measures, just tracks "who enrolled in what"
);
```

### Fact Table Best Practices

1. **Define grain clearly**: Document what one row means
2. **Use surrogate keys**: Never use natural keys
3. **Avoid wide tables**: Keep facts focused
4. **Consider additivity**: Know how measures aggregate
5. **Partition by date**: Most facts are time-based

## Code Example

```python
from google.cloud import bigquery

def create_fact_table(client, fact_type):
    """Create fact table based on type."""
    
    if fact_type == 'transaction':
        sql = """
        CREATE TABLE dataset.fact_sales (
            date_key INT64,
            customer_key INT64,
            product_key INT64,
            quantity INT64,
            revenue NUMERIC
        )
        PARTITION BY RANGE_BUCKET(date_key, GENERATE_ARRAY(20200101, 20301231, 1))
        """
    elif fact_type == 'snapshot':
        sql = """
        CREATE TABLE dataset.fact_inventory_daily (
            date_key INT64,
            product_key INT64,
            store_key INT64,
            on_hand INT64,
            on_order INT64
        )
        PARTITION BY RANGE_BUCKET(date_key, GENERATE_ARRAY(20200101, 20301231, 1))
        """
    
    client.query(sql).result()
    print(f"Created {fact_type} fact table")
```

## Key Takeaways

- Fact tables store business measurements
- Three types: transaction, periodic snapshot, accumulating snapshot
- Grain defines what one row represents
- Measures can be additive, semi-additive, or non-additive
- Factless facts track events without measures

## Resources

- Fact Table Fundamentals: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/>
