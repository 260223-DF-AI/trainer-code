# Measures and Aggregations

## Learning Objectives

- Understand types of measures in dimensional models
- Learn aggregation rules and behaviors
- Apply appropriate aggregation techniques
- Handle special cases in aggregations

## Why This Matters

Measures are the numeric values that business users analyze. Understanding how different measures aggregate across dimensions is essential for accurate analysis and avoiding common pitfalls.

## Concept Explanation

### Types of Measures

#### Additive Measures

Can be summed across all dimensions:

```sql
-- Revenue, quantity, cost - can sum across any dimension
SELECT 
    region,
    SUM(revenue) as total_revenue,
    SUM(quantity) as total_units
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY region;
```

Examples: Revenue, quantity, cost, profit

#### Semi-Additive Measures

Can sum across some dimensions, but not all (usually not time):

```sql
-- Account balance - can sum across accounts, NOT across time
-- Correct: Sum balances across customers on a specific date
SELECT SUM(balance) FROM fact_account_balance WHERE date_key = 20240115;

-- Incorrect: Sum balances across dates makes no sense
SELECT SUM(balance) FROM fact_account_balance;  -- Wrong!

-- For time: Use average or point-in-time
SELECT AVG(balance) FROM fact_account_balance;
```

Examples: Account balance, inventory level, headcount

#### Non-Additive Measures

Cannot be summed meaningfully:

```sql
-- Unit price - summing makes no sense
-- Correct: Use average or weighted average
SELECT 
    category,
    AVG(unit_price) as avg_price,
    SUM(quantity * unit_price) / SUM(quantity) as weighted_avg_price
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY category;
```

Examples: Price, ratio, percentage, temperature

### Aggregation Functions

| Function | Use Case |
|----------|----------|
| SUM | Additive measures |
| AVG | Averages, non-additive |
| COUNT | Record counts |
| COUNT DISTINCT | Unique counts |
| MIN/MAX | Range values |
| STDDEV | Variability |

### Derived Measures

Calculate from other measures:

```sql
SELECT 
    region,
    SUM(revenue) as revenue,
    SUM(cost) as cost,
    SUM(revenue) - SUM(cost) as profit,
    (SUM(revenue) - SUM(cost)) / NULLIF(SUM(revenue), 0) * 100 as margin_pct
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY region;
```

### Pre-Aggregated vs. Calculated

| Approach | Pros | Cons |
|----------|------|------|
| Pre-aggregated | Fast queries | Storage, staleness |
| Calculated | Always current | Query time |

## Code Example

```python
def calculate_measures(client, dimensions):
    """Calculate measures with proper aggregation."""
    
    dim_cols = ', '.join(dimensions)
    
    sql = f"""
    SELECT 
        {dim_cols},
        -- Additive
        SUM(quantity) as total_quantity,
        SUM(revenue) as total_revenue,
        -- Non-additive (weighted average)
        SUM(quantity * unit_price) / SUM(quantity) as avg_unit_price,
        -- Derived
        SUM(revenue) - SUM(cost) as gross_profit,
        SAFE_DIVIDE(SUM(revenue) - SUM(cost), SUM(revenue)) * 100 as margin_pct
    FROM dataset.fact_sales
    GROUP BY {dim_cols}
    """
    
    return client.query(sql).to_dataframe()
```

## Key Takeaways

- Additive measures can sum across all dimensions
- Semi-additive measures cannot sum across time
- Non-additive measures require averages or other functions
- Use NULLIF or SAFE_DIVIDE to handle division by zero
- Derived measures should be calculated, not stored

## Resources

- Measure Types: <https://www.kimballgroup.com/2008/08/design-tip-105-snowflaking-outriggers-and-avoiding-normalization/>
