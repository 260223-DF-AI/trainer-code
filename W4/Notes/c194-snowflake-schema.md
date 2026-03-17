# Snowflake Schema

## Learning Objectives

- Understand snowflake schema structure
- Compare snowflake to star schema
- Recognize when to use snowflake schema
- Apply normalization in dimensional modeling

## Why This Matters

Snowflake schema is an alternative to star schema that normalizes dimension tables. Understanding when to use each pattern helps you make appropriate design decisions based on your specific requirements.

## Concept Explanation

### Snowflake Schema Structure

```
                              +----------+
                              | dim_year |
                              +----+-----+
                                   |
                        +----------+----------+
                        |    dim_date         |
                        +----------+----------+
                                   |
+----------+          +------------+-----------+          +----------+
| dim_     |          |                        |          |   dim_   |
| customer |--------->|      fact_sales        |<---------|  product |
+----+-----+          |                        |          +----+-----+
     |                +------------------------+               |
+----+-----+                                             +-----+------+
| dim_     |                                             |   dim_     |
| region   |                                             |  category  |
+----------+                                             +------------+
```

### Normalized Dimensions

Unlike star schema's flat dimensions, snowflake normalizes:

```sql
-- Star Schema: Flat dimension
CREATE TABLE dim_product_star (
    product_key INT64,
    product_name STRING,
    category_name STRING,     -- Redundant
    category_desc STRING,     -- Redundant
    subcategory_name STRING   -- Redundant
);

-- Snowflake Schema: Normalized dimensions
CREATE TABLE dim_product (
    product_key INT64,
    product_name STRING,
    subcategory_key INT64  -- FK to subcategory
);

CREATE TABLE dim_subcategory (
    subcategory_key INT64,
    subcategory_name STRING,
    category_key INT64  -- FK to category
);

CREATE TABLE dim_category (
    category_key INT64,
    category_name STRING,
    category_desc STRING
);
```

### Query Comparison

**Star Schema Query:**

```sql
SELECT p.category_name, SUM(f.revenue)
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category_name;
-- 1 join
```

**Snowflake Schema Query:**

```sql
SELECT c.category_name, SUM(f.revenue)
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_subcategory s ON p.subcategory_key = s.subcategory_key
JOIN dim_category c ON s.category_key = c.category_key
GROUP BY c.category_name;
-- 3 joins
```

### Star vs. Snowflake

| Aspect | Star | Snowflake |
|--------|------|-----------|
| Dimensions | Denormalized | Normalized |
| Joins | Fewer | More |
| Query Speed | Faster | Slower |
| Storage | More redundancy | Less redundancy |
| Maintenance | Simpler | More complex |
| User-Friendly | More | Less |

### When to Use Snowflake

1. **Storage constraints**: When redundancy is a concern
2. **Dimension maintenance**: When dimension data changes frequently
3. **Complex hierarchies**: Deep multi-level hierarchies
4. **ETL simplicity**: Easier incremental dimension updates

### When to Prefer Star

1. **Query performance**: Priority on fast queries
2. **User accessibility**: Business users write queries
3. **BI tools**: Many tools expect star schema
4. **Modern warehouses**: Cloud DWH handle redundancy well

### Modern Perspective

With cloud data warehouses:

- Storage is cheap
- Query performance is critical
- Star schema is generally preferred

## Key Takeaways

- Snowflake schema normalizes dimension tables
- Results in more joins but less storage
- Star schema preferred for most analytical workloads
- Use snowflake when maintenance or storage is primary concern
- Modern cloud warehouses favor star schema

## Resources

- Snowflake Schema: <https://www.kimballgroup.com/2008/08/design-tip-105-snowflaking-outriggers-and-avoiding-normalization/>
