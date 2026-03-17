# Data Modeling Best Practices

## Learning Objectives

- Apply dimensional modeling best practices
- Avoid common design mistakes
- Create maintainable, performant schemas
- Document data models effectively

## Why This Matters

Following best practices ensures your data warehouse is performant, maintainable, and useful for business users. Poor design decisions are costly to fix later.

## Concept Explanation

### Schema Design Best Practices

#### 1. Define Grain First

```
Good: "One row per sales transaction line item per day"
Bad:  "Sales data" (too vague)
```

#### 2. Use Surrogate Keys

```sql
-- Good: Integer surrogate key
CREATE TABLE dim_customer (
    customer_key INT64,  -- Surrogate
    customer_id STRING   -- Natural key preserved
);

-- Bad: Natural key as primary key
CREATE TABLE dim_customer (
    customer_id STRING PRIMARY KEY  -- Bad
);
```

#### 3. Denormalize Dimensions

Include all attributes in dimension, avoid joins:

```sql
-- Good: All attributes in dimension
CREATE TABLE dim_product (
    product_key INT64,
    product_name STRING,
    category STRING,      -- Denormalized
    subcategory STRING    -- Denormalized
);
```

### Fact Table Best Practices

1. **Keep facts focused**: One business process per fact
2. **Store atomic grain**: Most detailed level
3. **Use numeric keys**: Faster joins
4. **Avoid wide facts**: Many dimensions = complex queries
5. **Partition by date**: Most facts are time-based

### Dimension Best Practices

1. **Include natural keys**: For business reference
2. **Add descriptive attributes**: Enable filtering
3. **Support hierarchies**: Enable drill-down
4. **Track history (SCD)**: When business requires it
5. **Create date dimension**: Every warehouse needs it

### Common Mistakes to Avoid

| Mistake | Solution |
|---------|----------|
| Natural keys in joins | Use surrogate keys |
| Insufficient grain | Start with atomic level |
| Missing dimensions | Include who, what, when, where |
| Over-normalization | Denormalize for performance |
| No documentation | Document grain and definitions |

### Documentation

Document these for each table:

```yaml
Table: fact_sales
Grain: One row per sales transaction line item
Business Process: Retail point-of-sale
Refresh: Daily batch at 2 AM EST
Primary Key: Composite (date_key, transaction_id, line_number)
Dimensions:
  - dim_date (date_key)
  - dim_customer (customer_key)
  - dim_product (product_key)
Measures:
  - quantity (additive)
  - unit_price (non-additive)
  - revenue (additive)
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Fact table | fact_* | fact_sales |
| Dimension | dim_* | dim_customer |
| Surrogate key | *_key | customer_key |
| Natural key | *_id | customer_id |
| Foreign key | *_key | customer_key |
| Date column | *_date | order_date |

### Review Checklist

- [ ] Grain defined and documented
- [ ] Surrogate keys for all dimensions
- [ ] Descriptive dimension attributes
- [ ] Date dimension included
- [ ] Measures categorized (additive/semi/non)
- [ ] SCD strategy defined
- [ ] Naming conventions followed
- [ ] Documentation complete

## Key Takeaways

- Define grain clearly before designing
- Always use surrogate keys, preserve natural keys
- Denormalize dimensions for query performance
- Document everything: grain, refresh, definitions
- Follow consistent naming conventions
- Review designs against checklist before implementing

## Resources

- Kimball Design Tips: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/>
