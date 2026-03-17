# OLAP Systems

## Learning Objectives

- Define OLAP (Online Analytical Processing) and its purpose
- Understand key characteristics of OLAP systems
- Learn about denormalization and optimizations for analytics
- Recognize common OLAP use cases and technologies

## Why This Matters

OLAP systems power business intelligence, reporting, and data-driven decision making. Unlike OLTP systems that run the business, OLAP systems help analyze the business. Understanding OLAP helps you design and use analytical systems effectively.

## Concept Explanation

### What is OLAP?

OLAP (Online Analytical Processing) refers to systems designed for complex analytical queries on historical data. These systems support business intelligence by enabling multidimensional analysis across large datasets.

**Key Purpose**: "Analyze the business" through complex queries on historical data.

### Characteristics of OLAP Systems

```
OLAP System Traits:

+------------------+     +------------------+     +------------------+
| Complex Queries  |     | Historical Data  |     | Aggregations     |
+------------------+     +------------------+     +------------------+
| Multi-table JOINs|     | Years of history |     | SUM, AVG, COUNT  |
| GROUP BY         |     | Time-series      |     | Window functions |
| Analytics        |     | Trend analysis   |     | Rollups          |
+------------------+     +------------------+     +------------------+
```

#### 1. Complex Analytical Queries

OLAP queries typically:

- Join multiple tables
- Aggregate large datasets
- Apply complex filters
- Use window functions and CTEs

#### 2. Historical Data Focus

OLAP systems store extensive history:

- Years or decades of data
- Enables trend analysis and comparison
- Data rarely updated after loading

#### 3. Read-Optimized

Unlike OLTP's read/write balance:

- Queries far outnumber writes
- Batch data loading (nightly/hourly)
- Optimized for full table scans

### Data Model: Denormalized (Star Schema)

OLAP systems use denormalized schemas for query performance:

**Star Schema Example**

```
                           dim_date
                           +------------+
                           | date_id    |
                           | full_date  |
                           | year       |
                           | quarter    |
                           | month      |
                           | day_of_week|
                           +-----+------+
                                 |
dim_customer                     |                    dim_product
+------------+                   |                    +------------+
| customer_id|                   |                    | product_id |
| name       |                   |                    | name       |
| segment    |----+              |              +-----| category   |
| region     |    |              |              |     | brand      |
+------------+    |              |              |     +------------+
                  |              |              |
                  |       +------+------+       |
                  |       |  fact_sales |       |
                  +------>| date_id     |<------+
                          | customer_id |
                          | product_id  |
                          | quantity    |
                          | revenue     |
                          | discount    |
                          +-------------+
```

**Benefits of Denormalization:**

- Fewer joins in queries
- Faster query execution
- Simpler SQL for analysts
- Pre-computed attributes (customer segment, date parts)

### Common OLAP Operations

OLAP queries aggregate and analyze:

```sql
-- Total sales by region and quarter
SELECT 
    c.region,
    d.year,
    d.quarter,
    SUM(f.revenue) as total_revenue,
    COUNT(DISTINCT f.customer_id) as unique_customers
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year >= 2022
GROUP BY c.region, d.year, d.quarter
ORDER BY d.year, d.quarter, total_revenue DESC;

-- Year-over-year growth by product category
WITH yearly_sales AS (
    SELECT 
        p.category,
        d.year,
        SUM(f.revenue) as revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY p.category, d.year
)
SELECT 
    current.category,
    current.year,
    current.revenue,
    prior.revenue as prior_year_revenue,
    (current.revenue - prior.revenue) / prior.revenue * 100 as yoy_growth
FROM yearly_sales current
LEFT JOIN yearly_sales prior 
    ON current.category = prior.category 
    AND current.year = prior.year + 1;
```

### OLAP Technologies

| Category | Examples |
|----------|----------|
| Cloud Data Warehouses | BigQuery, Snowflake, Redshift |
| On-premises | Teradata, Oracle Analytics, Vertica |
| Open Source | ClickHouse, Apache Druid, DuckDB |
| OLAP Cubes | SQL Server Analysis Services |

### Workload Pattern

```
OLAP Workload:

Reads:  99% complex analytical queries
Writes: 1% batch loads

Query Complexity:
+--------+
|  Low   |||||  10%
+--------+
| Medium |||||||||||||  30%
+--------+
|  High  |||||||||||||||||||||||||||||||  60%
+--------+
```

### OLAP Optimization Techniques

#### Columnar Storage

Store data by column rather than row:

```
Row Storage:
[1, John, 100] [2, Jane, 200] [3, Bob, 150]

Columnar Storage:
[1, 2, 3]               <- IDs
[John, Jane, Bob]       <- Names  
[100, 200, 150]         <- Amounts
```

**Benefits:**

- Only read columns needed for query
- Better compression (similar values together)
- Vectorized processing

#### Partitioning

Divide large tables by a key (usually date):

```sql
-- BigQuery partitioning
CREATE TABLE sales_archive
PARTITION BY DATE(sale_date)
AS SELECT * FROM fact_sales;

-- Query only scans relevant partitions
SELECT SUM(revenue) FROM sales_archive
WHERE sale_date >= '2024-01-01';  -- Only scans 2024+ partitions
```

#### Clustering

Sort data within partitions for locality:

```sql
-- BigQuery clustering
CREATE TABLE fact_sales
PARTITION BY DATE(sale_date)
CLUSTER BY customer_id, product_id
AS SELECT * FROM raw_sales;
```

## Code Example

OLAP query patterns in Python:

```python
from google.cloud import bigquery
from typing import List, Dict
import pandas as pd

class OLAPAnalytics:
    """Demonstrates OLAP query patterns."""
    
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute analytical query and return DataFrame."""
        return self.client.query(query).to_dataframe()
    
    def sales_by_dimension(self, dimensions: List[str], 
                          metrics: List[str], 
                          filters: Dict = None) -> pd.DataFrame:
        """
        Flexible OLAP query builder.
        
        Example:
        sales_by_dimension(
            dimensions=['region', 'quarter'],
            metrics=['revenue', 'quantity'],
            filters={'year': 2024}
        )
        """
        dim_cols = ', '.join(dimensions)
        metric_exprs = ', '.join([f'SUM({m}) as total_{m}' for m in metrics])
        
        query = f"""
            SELECT 
                {dim_cols},
                {metric_exprs}
            FROM `analytics.fact_sales` f
            JOIN `analytics.dim_customer` c ON f.customer_id = c.customer_id
            JOIN `analytics.dim_product` p ON f.product_id = p.product_id
            JOIN `analytics.dim_date` d ON f.date_id = d.date_id
        """
        
        if filters:
            conditions = [f"{k} = {repr(v)}" for k, v in filters.items()]
            query += " WHERE " + " AND ".join(conditions)
        
        query += f" GROUP BY {dim_cols}"
        
        return self.execute_query(query)
    
    def time_series_analysis(self, metric: str, 
                             grain: str = 'month') -> pd.DataFrame:
        """
        Trend analysis over time - core OLAP capability.
        """
        date_extract = {
            'day': 'DATE(sale_date)',
            'month': "DATE_TRUNC(sale_date, MONTH)",
            'quarter': "DATE_TRUNC(sale_date, QUARTER)",
            'year': "DATE_TRUNC(sale_date, YEAR)"
        }
        
        query = f"""
            SELECT 
                {date_extract[grain]} as period,
                SUM({metric}) as value,
                SUM({metric}) - LAG(SUM({metric})) OVER (ORDER BY {date_extract[grain]}) as period_change,
                (SUM({metric}) - LAG(SUM({metric})) OVER (ORDER BY {date_extract[grain]})) 
                    / LAG(SUM({metric})) OVER (ORDER BY {date_extract[grain]}) * 100 as pct_change
            FROM `analytics.fact_sales`
            GROUP BY period
            ORDER BY period
        """
        
        return self.execute_query(query)
    
    def cohort_analysis(self) -> pd.DataFrame:
        """
        Customer cohort analysis - complex OLAP query.
        """
        query = """
            WITH first_purchase AS (
                SELECT 
                    customer_id,
                    DATE_TRUNC(MIN(sale_date), MONTH) as cohort_month
                FROM `analytics.fact_sales`
                GROUP BY customer_id
            ),
            monthly_activity AS (
                SELECT 
                    f.customer_id,
                    fp.cohort_month,
                    DATE_TRUNC(f.sale_date, MONTH) as activity_month,
                    DATE_DIFF(DATE_TRUNC(f.sale_date, MONTH), fp.cohort_month, MONTH) as months_since_first
                FROM `analytics.fact_sales` f
                JOIN first_purchase fp ON f.customer_id = fp.customer_id
            )
            SELECT 
                cohort_month,
                months_since_first,
                COUNT(DISTINCT customer_id) as active_customers
            FROM monthly_activity
            GROUP BY cohort_month, months_since_first
            ORDER BY cohort_month, months_since_first
        """
        
        return self.execute_query(query)


# Usage example
analytics = OLAPAnalytics('my-project')

# Multidimensional analysis
df = analytics.sales_by_dimension(
    dimensions=['region', 'category'],
    metrics=['revenue', 'quantity'],
    filters={'year': 2024}
)
print(df)

# Time series trend
trend = analytics.time_series_analysis('revenue', grain='month')
print(trend)
```

## Key Takeaways

- OLAP systems are designed for complex analytical queries on historical data
- Use denormalized star/snowflake schemas for query performance
- Optimized for reads with batch data loading
- Columnar storage enables efficient analytical queries
- Partitioning and clustering improve query performance
- Common OLAP systems: BigQuery, Snowflake, Redshift, ClickHouse
- OLAP enables business intelligence, trend analysis, and data-driven decisions

## Resources

- Star Schema Design: <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/star-schema-olap-cube/>
- BigQuery Optimization: <https://cloud.google.com/bigquery/docs/best-practices-performance-overview>
- Columnar Databases: <https://www.vertica.com/about/columnar-database/>
