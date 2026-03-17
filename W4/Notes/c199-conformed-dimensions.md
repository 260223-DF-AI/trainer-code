# Conformed Dimensions

## Learning Objectives

- Understand conformed dimensions and their purpose
- Learn how to design consistent dimensions
- Apply conformed dimensions across fact tables
- Enable cross-process analysis

## Why This Matters

Conformed dimensions enable consistent analysis across different business processes. When multiple fact tables share the same dimension, you can create reports that span processes (e.g., comparing sales to inventory).

## Concept Explanation

### What are Conformed Dimensions?

Conformed dimensions are dimensions shared identically across multiple fact tables or data marts. They have the same keys, attributes, and values.

```
                    +-------------+
                    | dim_date    |  <- Shared by all facts
                    +------+------+
                           |
      +--------------------+--------------------+
      |                    |                    |
+-----+-----+        +-----+-----+        +-----+-----+
| fact_sales|        |fact_invent|        |fact_orders|
+-----------+        +-----------+        +-----------+
```

### Benefits

1. **Consistent Analysis**: Same definition everywhere
2. **Cross-Process Reporting**: Join facts through shared dimensions
3. **Single Source of Truth**: One definition, many uses
4. **Reduced Redundancy**: Maintain once, use everywhere

### Example: Date Dimension

The date dimension is the most common conformed dimension:

```sql
-- Same dim_date used by all processes
CREATE TABLE dim_date (
    date_key INT64,
    full_date DATE,
    year INT64,
    quarter INT64,
    month INT64,
    month_name STRING,
    is_holiday BOOL
);

-- Used by sales
SELECT d.month_name, SUM(s.revenue)
FROM fact_sales s JOIN dim_date d ON s.date_key = d.date_key
GROUP BY d.month_name;

-- Used by inventory
SELECT d.month_name, AVG(i.on_hand)
FROM fact_inventory i JOIN dim_date d ON i.date_key = d.date_key
GROUP BY d.month_name;
```

### Cross-Process Analysis

Conformed dimensions enable combining facts:

```sql
-- Compare sales to inventory using conformed product dimension
SELECT 
    p.category,
    SUM(s.quantity) as sold,
    AVG(i.on_hand) as avg_inventory,
    SUM(s.quantity) / AVG(i.on_hand) as turnover
FROM fact_sales s
JOIN fact_inventory i 
    ON s.product_key = i.product_key 
    AND s.date_key = i.date_key
JOIN dim_product p ON s.product_key = p.product_key
GROUP BY p.category;
```

### Conformed vs. Non-Conformed

| Aspect | Conformed | Non-Conformed |
|--------|-----------|---------------|
| Keys | Same across facts | Different per fact |
| Attributes | Identical | May differ |
| Analysis | Cross-process | Single process |
| Maintenance | Centralized | Distributed |

### Creating Conformed Dimensions

1. **Identify shared concepts**: Date, customer, product
2. **Define standard attributes**: Same columns everywhere
3. **Use consistent keys**: Same surrogate key system
4. **Maintain centrally**: Single ETL process

## Code Example

```python
def create_conformed_dimension(client, dim_name, columns):
    """Create and register a conformed dimension."""
    
    # Create the dimension table
    col_defs = ', '.join([f"{c['name']} {c['type']}" for c in columns])
    
    sql = f"""
    CREATE TABLE IF NOT EXISTS dataset.{dim_name} ({col_defs})
    """
    
    client.query(sql).result()
    print(f"Conformed dimension {dim_name} created")

# Usage
create_conformed_dimension(client, 'dim_date', [
    {'name': 'date_key', 'type': 'INT64'},
    {'name': 'full_date', 'type': 'DATE'},
    {'name': 'year', 'type': 'INT64'},
    {'name': 'quarter', 'type': 'INT64'},
    {'name': 'month', 'type': 'INT64'},
])
```

## Key Takeaways

- Conformed dimensions are shared identically across fact tables
- Enable cross-process analysis and consistent reporting
- Date and customer are the most common conformed dimensions
- Require centralized governance and maintenance
- Essential for enterprise data warehouse architecture

## Resources

- Conformed Dimensions: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/>
