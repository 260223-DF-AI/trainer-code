# Galaxy Schema

## Learning Objectives

- Understand galaxy schema (fact constellation)
- Learn when to use multiple fact tables
- Design schemas with shared dimensions
- Compare galaxy to star and snowflake schemas

## Why This Matters

Real-world data warehouses typically have multiple business processes, each with its own fact table. Galaxy schema describes how these facts share conformed dimensions, enabling enterprise-wide analytics.

## Concept Explanation

### What is Galaxy Schema?

Galaxy schema (also called fact constellation) consists of multiple fact tables sharing conformed dimensions. It represents the enterprise data warehouse with multiple business processes.

```
              +-------------+
              |  dim_date   |
              +------+------+
                     |
    +----------------+----------------+
    |                |                |
+---+---+        +---+---+        +---+---+
| fact_ |        | fact_ |        | fact_ |
| sales |        |invent |        |orders |
+---+---+        +---+---+        +---+---+
    |                |                |
    +----------------+----------------+
                     |
              +------+------+
              | dim_product |
              +-------------+
```

### Components

1. **Multiple Fact Tables**: Each business process has its own fact
2. **Shared Dimensions**: Conformed dimensions connect facts
3. **Process-Specific Dimensions**: Some dimensions are unique to one fact

### Example Galaxy Schema

```sql
-- Shared dimensions
CREATE TABLE dim_date (...);
CREATE TABLE dim_product (...);
CREATE TABLE dim_store (...);

-- Process-specific dimension
CREATE TABLE dim_supplier (...);  -- Only for purchasing

-- Multiple fact tables
CREATE TABLE fact_sales (
    date_key INT64,
    product_key INT64,
    store_key INT64,
    quantity INT64,
    revenue NUMERIC
);

CREATE TABLE fact_inventory (
    date_key INT64,
    product_key INT64,
    store_key INT64,
    on_hand INT64,
    on_order INT64
);

CREATE TABLE fact_purchases (
    date_key INT64,
    product_key INT64,
    supplier_key INT64,  -- Unique to this fact
    quantity INT64,
    cost NUMERIC
);
```

### Cross-Fact Analysis

Galaxy schema enables cross-process queries:

```sql
-- Inventory turnover analysis
SELECT 
    p.category,
    d.month_name,
    SUM(s.quantity) as sold,
    AVG(i.on_hand) as avg_inventory,
    SUM(s.quantity) / AVG(i.on_hand) as turnover
FROM fact_sales s
JOIN fact_inventory i 
    ON s.date_key = i.date_key 
    AND s.product_key = i.product_key
JOIN dim_product p ON s.product_key = p.product_key
JOIN dim_date d ON s.date_key = d.date_key
GROUP BY p.category, d.month_name;
```

### Schema Comparison

| Schema | Facts | Dimensions | Use Case |
|--------|-------|-----------|----------|
| Star | Single | Denormalized | Single process |
| Snowflake | Single | Normalized | Storage-conscious |
| Galaxy | Multiple | Shared conformed | Enterprise warehouse |

### Design Considerations

1. **Identify business processes**: Each process = potential fact
2. **Find shared dimensions**: Date, customer, product
3. **Define grain carefully**: Each fact has its own grain
4. **Consider query patterns**: Which facts are joined together?

## Key Takeaways

- Galaxy schema has multiple fact tables sharing dimensions
- Represents enterprise-wide data warehouse
- Conformed dimensions enable cross-process analysis
- Each fact table models one business process
- Natural evolution of star schema for complex organizations

## Resources

- Fact Constellation: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/>
