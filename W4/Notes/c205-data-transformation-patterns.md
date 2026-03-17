# Data Transformation Patterns

## Learning Objectives

- Learn common data transformation patterns
- Apply cleaning, standardization, and enrichment
- Understand aggregation and pivoting
- Handle data type conversions

## Why This Matters

Transformations turn raw data into analytically useful information. Understanding common patterns helps you build robust pipelines that produce high-quality, consistent data.

## Concept Explanation

### Transformation Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Cleaning | Fix data quality issues | Remove nulls, duplicates |
| Standardization | Ensure consistency | Format dates, normalize codes |
| Enrichment | Add context | Join reference data |
| Aggregation | Summarize data | Sum, count, average |
| Derivation | Calculate new fields | Age from birthdate |

### Data Cleaning

```python
def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=['id'])
    
    # Handle nulls
    df['name'] = df['name'].fillna('Unknown')
    df = df.dropna(subset=['required_field'])
    
    # Fix data types
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Trim whitespace
    df['name'] = df['name'].str.strip()
    
    return df
```

### Standardization

```python
def standardize_data(df):
    # Date formats
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # Case normalization
    df['email'] = df['email'].str.lower()
    
    # Code standardization
    status_map = {'A': 'Active', 'I': 'Inactive', 'P': 'Pending'}
    df['status'] = df['status'].map(status_map)
    
    return df
```

### Data Enrichment

```python
def enrich_orders(orders, customers, products):
    # Join with customer data
    enriched = orders.merge(
        customers[['customer_id', 'segment', 'region']],
        on='customer_id',
        how='left'
    )
    
    # Join with product data
    enriched = enriched.merge(
        products[['product_id', 'category', 'brand']],
        on='product_id',
        how='left'
    )
    
    return enriched
```

### Aggregation

```python
def aggregate_sales(df):
    # Group and aggregate
    summary = df.groupby(['region', 'category']).agg({
        'quantity': 'sum',
        'revenue': 'sum',
        'order_id': 'count'
    }).rename(columns={'order_id': 'order_count'})
    
    return summary
```

### Derived Fields

```python
def add_derived_fields(df):
    # Calculate from existing
    df['total'] = df['quantity'] * df['unit_price']
    df['margin'] = (df['revenue'] - df['cost']) / df['revenue']
    
    # Date parts
    df['year'] = df['order_date'].dt.year
    df['quarter'] = df['order_date'].dt.quarter
    
    # Categorization
    df['size_bucket'] = pd.cut(
        df['amount'],
        bins=[0, 100, 500, float('inf')],
        labels=['Small', 'Medium', 'Large']
    )
    
    return df
```

### SQL Transformations

```sql
-- Transformation in SQL (ELT approach)
CREATE TABLE clean_orders AS
SELECT
    order_id,
    customer_id,
    COALESCE(amount, 0) as amount,
    UPPER(TRIM(status)) as status,
    PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    amount * quantity as total,
    CURRENT_TIMESTAMP() as processed_at
FROM raw_orders
WHERE order_id IS NOT NULL
  AND order_date >= '2020-01-01';
```

## Code Example

```python
class DataTransformer:
    """Common transformation patterns."""
    
    def __init__(self, df):
        self.df = df.copy()
    
    def clean(self):
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna(subset=['id'])
        return self
    
    def standardize_dates(self, columns):
        for col in columns:
            self.df[col] = pd.to_datetime(self.df[col])
        return self
    
    def add_derived(self, name, expression):
        self.df[name] = expression(self.df)
        return self
    
    def aggregate(self, group_by, agg_dict):
        self.df = self.df.groupby(group_by).agg(agg_dict).reset_index()
        return self
    
    def result(self):
        return self.df

# Fluent API usage
result = (DataTransformer(raw_data)
    .clean()
    .standardize_dates(['order_date'])
    .add_derived('total', lambda df: df['qty'] * df['price'])
    .result())
```

## Key Takeaways

- Clean: Remove duplicates, handle nulls, fix types
- Standardize: Consistent formats, codes, casing
- Enrich: Add context through joins
- Aggregate: Summarize for reporting
- Derive: Calculate new fields from existing

## Resources

- Pandas Transformations: <https://pandas.pydata.org/docs/user_guide/>
