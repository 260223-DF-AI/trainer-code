# Data Quality in Pipelines

## Learning Objectives

- Understand data quality dimensions
- Implement data validation checks
- Handle data quality failures
- Build data quality into pipelines

## Why This Matters

Data quality issues corrupt downstream analysis and erode trust. Building quality checks into your pipelines catches problems early, before bad data reaches consumers.

## Concept Explanation

### Data Quality Dimensions

| Dimension | Description | Example Check |
|-----------|-------------|---------------|
| Completeness | No missing values | NULL count < threshold |
| Accuracy | Correct values | Email format valid |
| Consistency | Values match across sources | Totals reconcile |
| Timeliness | Data is current | Last update < 24h |
| Uniqueness | No duplicates | Unique key count = row count |
| Validity | Values in allowed range | Status in ('A', 'I', 'P') |

### Basic Validation Checks

```python
def validate_data(df, table_name):
    """Run basic data quality checks."""
    checks = []
    
    # Completeness
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            checks.append({
                'check': 'null_check',
                'column': col,
                'status': 'warning' if count < 10 else 'fail',
                'message': f'{count} null values'
            })
    
    # Uniqueness
    if 'id' in df.columns:
        duplicates = df['id'].duplicated().sum()
        if duplicates > 0:
            checks.append({
                'check': 'uniqueness',
                'column': 'id',
                'status': 'fail',
                'message': f'{duplicates} duplicates'
            })
    
    return checks
```

### SQL-Based Validation

```sql
-- Completeness check
SELECT 
    'completeness' as check_type,
    COUNTIF(customer_id IS NULL) as failures,
    COUNT(*) as total
FROM staging.orders;

-- Uniqueness check
SELECT 
    'uniqueness' as check_type,
    COUNT(*) - COUNT(DISTINCT order_id) as failures,
    COUNT(*) as total
FROM staging.orders;

-- Accuracy check
SELECT 
    'valid_email' as check_type,
    COUNTIF(NOT REGEXP_CONTAINS(email, r'^[^@]+@[^@]+\.[^@]+$')) as failures,
    COUNT(*) as total
FROM staging.customers;

-- Consistency check
SELECT 
    'totals_match' as check_type,
    ABS(SUM(line_total) - order_total) > 0.01 as failures
FROM staging.order_details
GROUP BY order_id, order_total;
```

### Quality Check Framework

```python
class DataQualityChecker:
    """Reusable quality check framework."""
    
    def __init__(self, df):
        self.df = df
        self.results = []
    
    def check_not_null(self, columns):
        for col in columns:
            nulls = self.df[col].isnull().sum()
            self.results.append({
                'check': f'{col}_not_null',
                'passed': nulls == 0,
                'details': f'{nulls} nulls found'
            })
        return self
    
    def check_unique(self, columns):
        dupes = self.df.duplicated(subset=columns).sum()
        self.results.append({
            'check': 'unique_key',
            'passed': dupes == 0,
            'details': f'{dupes} duplicates'
        })
        return self
    
    def check_values_in(self, column, valid_values):
        invalid = ~self.df[column].isin(valid_values)
        count = invalid.sum()
        self.results.append({
            'check': f'{column}_valid_values',
            'passed': count == 0,
            'details': f'{count} invalid values'
        })
        return self
    
    def run(self):
        failures = [r for r in self.results if not r['passed']]
        if failures:
            raise DataQualityException(failures)
        return True

# Usage
(DataQualityChecker(df)
    .check_not_null(['order_id', 'customer_id'])
    .check_unique(['order_id'])
    .check_values_in('status', ['pending', 'shipped', 'delivered'])
    .run())
```

### Handling Failures

| Strategy | When to Use |
|----------|-------------|
| Fail pipeline | Critical data, cannot proceed |
| Quarantine bad rows | Keep good data, isolate bad |
| Alert and continue | Non-critical, monitor trend |
| Auto-fix | Simple issues, transformable |

## Key Takeaways

- Check completeness, accuracy, consistency, and uniqueness
- Build validation into every pipeline stage
- Use frameworks for reusable checks
- Choose appropriate failure handling strategy
- Monitor quality trends over time

## Resources

- Great Expectations: <https://greatexpectations.io/>
