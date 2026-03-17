# Slowly Changing Dimensions (SCD)

## Learning Objectives

- Understand why dimensions change over time
- Learn SCD Types 1, 2, and 3
- Implement SCD handling strategies
- Choose appropriate SCD type for your use case

## Why This Matters

Dimensions change: customers move, products get reclassified, employees change roles. How you handle these changes determines whether historical analysis remains accurate. SCD techniques preserve historical context in your data warehouse.

## Concept Explanation

### The Problem

```
Original Record (2023):
Customer: John Smith, Region: East

Current Record (2024):
Customer: John Smith, Region: West

Question: When analyzing 2023 sales, 
which region should John's orders appear in?
```

### SCD Types

#### Type 0: Retain Original

Never update the dimension. Keep original values forever.

**Use when**: Values should never change (birth date, original sign-up date)

#### Type 1: Overwrite

Simply overwrite the old value with the new value.

```sql
-- Before
| customer_key | name | region |
| 1            | John | East   |

-- After update
| customer_key | name | region |
| 1            | John | West   |  -- East is lost
```

**Use when**: History doesn't matter for that attribute.

#### Type 2: Add New Row

Create a new row for each change, tracking history with dates.

```sql
-- After update: Two rows for same customer
| customer_key | customer_id | name | region | effective_date | end_date   | is_current |
| 1            | C001        | John | East   | 2020-01-01     | 2024-06-14 | false      |
| 2            | C001        | John | West   | 2024-06-15     | 9999-12-31 | true       |
```

**Use when**: You need to track history accurately.

#### Type 3: Add New Column

Add a column to store the previous value.

```sql
| customer_key | name | current_region | previous_region |
| 1            | John | West           | East            |
```

**Use when**: Only need current and previous values.

### SCD Type 2 Implementation

```sql
-- Update procedure for SCD Type 2
-- Step 1: End-date current record
UPDATE dim_customer
SET 
    end_date = CURRENT_DATE() - 1,
    is_current = false
WHERE customer_id = 'C001'
  AND is_current = true;

-- Step 2: Insert new record
INSERT INTO dim_customer (
    customer_key, customer_id, name, region,
    effective_date, end_date, is_current
)
VALUES (
    NEXT_KEY(), 'C001', 'John', 'West',
    CURRENT_DATE(), '9999-12-31', true
);
```

### Point-in-Time Queries

With SCD Type 2, query historical state:

```sql
-- What region was John in on 2023-06-01?
SELECT region
FROM dim_customer
WHERE customer_id = 'C001'
  AND '2023-06-01' BETWEEN effective_date AND end_date;
-- Returns: East
```

### SCD Type Selection

| Type | History | Storage | Complexity |
|------|---------|---------|------------|
| 0 | No change | Minimal | Lowest |
| 1 | Overwrite | Minimal | Low |
| 2 | Full history | Higher | Moderate |
| 3 | Limited | Moderate | Low |

## Code Example

```python
from datetime import date

def apply_scd_type2(client, customer_id, new_values):
    """Apply SCD Type 2 update."""
    
    # End-date current record
    client.query(f"""
        UPDATE dataset.dim_customer
        SET end_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY),
            is_current = false
        WHERE customer_id = '{customer_id}'
          AND is_current = true
    """).result()
    
    # Insert new record
    client.query(f"""
        INSERT INTO dataset.dim_customer
        (customer_key, customer_id, name, region, 
         effective_date, end_date, is_current)
        SELECT 
            MAX(customer_key) + 1,
            '{customer_id}',
            '{new_values['name']}',
            '{new_values['region']}',
            CURRENT_DATE(),
            DATE '9999-12-31',
            true
        FROM dataset.dim_customer
    """).result()
    
    print(f"SCD Type 2 applied for {customer_id}")
```

## Key Takeaways

- SCD Type 1: Overwrite (no history)
- SCD Type 2: New row with dates (full history)
- SCD Type 3: Previous value column (limited history)
- Choose based on historical analysis requirements
- Type 2 is most common for accurate historical reporting

## Resources

- SCD Techniques: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/>
