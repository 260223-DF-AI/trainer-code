# Dimensional Modeling Introduction

## Learning Objectives

- Define dimensional modeling and its purpose
- Understand the Kimball methodology
- Learn terms: facts, dimensions, measures, attributes
- Recognize why dimensional modeling enables analytics

## Why This Matters

Dimensional modeling is the foundation of data warehouse design. It creates data structures optimized for analytical queries, enabling business users to explore data intuitively. This approach has been the standard for data warehousing for over 30 years.

## Concept Explanation

### What is Dimensional Modeling?

Dimensional modeling is a technique for designing data warehouses that organizes data into facts (measurements) and dimensions (context). It prioritizes query performance and user understanding over storage efficiency.

**Origin**: Developed by Ralph Kimball in the 1990s, it remains the most widely used approach for analytical data modeling.

### Core Concepts

```
Dimensional Model:

+----------+       +-------------+       +----------+
|   WHO    |       |    WHAT     |       |   WHEN   |
| Customer |------>| Sales Fact  |<------| Date     |
+----------+       +-------------+       +----------+
                         ^
                         |
                   +----------+
                   |  WHERE   |
                   |  Store   |
                   +----------+
```

### Facts vs. Dimensions

| Concept | Description | Example |
|---------|-------------|---------|
| Fact | Measurable event/transaction | Sales, clicks, calls |
| Dimension | Context/descriptive attributes | Customer, product, time |
| Measure | Numeric value in fact | Revenue, quantity, duration |
| Attribute | Descriptive field in dimension | Name, category, region |

### Fact Tables

Fact tables store measurements of business processes:

```sql
-- Example fact table
CREATE TABLE fact_sales (
    -- Foreign keys to dimensions
    date_key INT64,
    customer_key INT64,
    product_key INT64,
    store_key INT64,
    
    -- Measures (what we analyze)
    quantity INT64,
    unit_price NUMERIC,
    discount_amount NUMERIC,
    revenue NUMERIC,
    
    -- Degenerate dimensions
    order_number STRING
);
```

**Fact Table Characteristics:**

- Many rows (millions/billions)
- Narrow (few columns)
- Contains foreign keys to dimensions
- Contains numeric measures
- Often partitioned by date

### Dimension Tables

Dimension tables provide context for facts:

```sql
-- Example dimension table
CREATE TABLE dim_customer (
    customer_key INT64,  -- Surrogate key
    customer_id STRING,  -- Natural key
    name STRING,
    email STRING,
    segment STRING,
    region STRING,
    city STRING,
    state STRING,
    country STRING,
    registration_date DATE
);
```

**Dimension Table Characteristics:**

- Fewer rows (thousands to millions)
- Wide (many columns)
- Contains descriptive attributes
- Contains surrogate and natural keys
- Changes slowly (SCD)

### Why Dimensional Modeling?

#### 1. Query Performance

Pre-joined data requires fewer joins:

```sql
-- Dimensional model: simple query
SELECT 
    d.month_name,
    p.category,
    SUM(f.revenue) as total_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.month_name, p.category;
```

#### 2. User Understanding

Business users naturally think in dimensions:

- "Sales **by** region"
- "Revenue **over** time"
- "Orders **per** customer"

#### 3. Flexibility

Dimensions can be added without restructuring:

```sql
-- Add a new dimension to existing fact
ALTER TABLE fact_sales ADD COLUMN campaign_key INT64;
```

### Kimball vs. Inmon

| Aspect | Kimball | Inmon |
|--------|---------|-------|
| Approach | Bottom-up | Top-down |
| Structure | Star schemas | Normalized EDW |
| Focus | Business process | Enterprise model |
| Time to Value | Faster | Slower |
| Complexity | Simpler | More complex |

### Dimensional Modeling Process

1. **Choose business process**: Sales, inventory, HR
2. **Identify grain**: One row = one transaction
3. **Choose dimensions**: Who, what, when, where
4. **Identify facts**: Measures to analyze

## Code Example

```python
from dataclasses import dataclass
from typing import List

@dataclass
class DimensionalModel:
    """Represents a dimensional model design."""
    business_process: str
    grain: str
    dimensions: List[str]
    facts: List[str]
    
    def describe(self):
        print(f"Business Process: {self.business_process}")
        print(f"Grain: {self.grain}")
        print(f"Dimensions: {', '.join(self.dimensions)}")
        print(f"Facts: {', '.join(self.facts)}")

# Example: Sales model
sales_model = DimensionalModel(
    business_process="Retail Sales",
    grain="One row per sales transaction line item",
    dimensions=["Date", "Customer", "Product", "Store", "Promotion"],
    facts=["Quantity", "Unit Price", "Discount", "Revenue", "Cost"]
)

sales_model.describe()
```

## Key Takeaways

- Dimensional modeling organizes data into facts (measurements) and dimensions (context)
- Facts contain numeric measures; dimensions contain descriptive attributes
- Star schemas optimize for analytical queries over storage efficiency
- Business users naturally think in dimensional terms
- The four-step process: business process, grain, dimensions, facts

## Resources

- The Data Warehouse Toolkit (Kimball): <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/>
