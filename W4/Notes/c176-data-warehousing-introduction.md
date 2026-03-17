# Data Warehousing Introduction

## Learning Objectives

- Define data warehousing and its role in business analytics
- Understand the historical evolution of data warehouses
- Learn key characteristics that differentiate data warehouses from operational databases
- Recognize the value data warehousing brings to organizations

## Why This Matters

Data warehousing is the foundation of modern business intelligence and analytics. Organizations rely on data warehouses to consolidate information from multiple sources, enabling comprehensive reporting and data-driven decision making. Understanding data warehousing concepts is essential for anyone working with enterprise data.

## Concept Explanation

### What is a Data Warehouse?

A data warehouse is a centralized repository designed specifically for analytical processing and reporting. It consolidates data from multiple operational systems into a unified view optimized for querying and analysis.

**Definition by Bill Inmon (Father of Data Warehousing):**
> "A data warehouse is a subject-oriented, integrated, time-variant, and non-volatile collection of data in support of management's decision making process."

### Key Characteristics

#### 1. Subject-Oriented

Organized around major business subjects rather than applications.

```
Operational Systems          Data Warehouse
+---------------+            +---------------+
| Order System  |            |   Sales       |
+---------------+     -->    | (customers,   |
| CRM System    |            |  products,    |
+---------------+            |  regions,     |
| Inventory     |            |  time)        |
+---------------+            +---------------+
```

#### 2. Integrated

Combines data from disparate sources with consistent naming, formats, and codes.

**Example - Customer ID Integration:**

| Source | Original Format | Warehouse Format |
|--------|-----------------|-----------------|
| CRM | CUST-12345 | 12345 |
| ERP | C12345 | 12345 |
| Web | user_12345 | 12345 |

#### 3. Time-Variant

Contains historical data for trend analysis and comparison.

- Operational: Current state only
- Warehouse: Historical snapshots over months/years
- Enables: Year-over-year, quarter-over-quarter analysis

#### 4. Non-Volatile

Data is loaded and accessed but rarely updated or deleted.

```
Operational DB:     INSERT, UPDATE, DELETE (constantly)
Data Warehouse:     INSERT (load), SELECT (query)
                    (No changes to historical data)
```

### Historical Evolution

```
1970s-80s: Decision Support Systems (DSS)
    |
    v
1990s: Enterprise Data Warehouses (EDW)
       - Teradata, Oracle, IBM DB2
       - On-premises, proprietary
    |
    v
2000s: Data Marts and OLAP Cubes
       - Departmental warehouses
       - Multidimensional analysis
    |
    v
2010s: Cloud Data Warehouses
       - Redshift (AWS), BigQuery (GCP)
       - Elastic scaling, pay-per-query
    |
    v
2020s: Modern Data Stack
       - Snowflake, Databricks
       - Separation of storage and compute
       - Data Lakehouse architectures
```

### Purpose and Value

**Data Warehouse Goals:**

1. **Single Source of Truth**: Consistent, authoritative data for the organization
2. **Historical Analysis**: Enable trend analysis and comparisons over time
3. **Business Intelligence**: Power dashboards, reports, and KPIs
4. **Self-Service Analytics**: Allow business users to explore data
5. **Decision Support**: Provide data-driven insights for strategy

### Data Warehouse vs. Operational Database

| Aspect | Operational DB | Data Warehouse |
|--------|----------------|----------------|
| Purpose | Run the business | Analyze the business |
| Users | Operational staff | Analysts, executives |
| Data | Current state | Historical |
| Queries | Simple, frequent | Complex, less frequent |
| Updates | Many per second | Batch loads |
| Optimization | Write performance | Read performance |
| Schema | 3NF normalized | Denormalized (star/snowflake) |

### Modern Data Warehouse Architecture

```
+---------------+     +---------------+     +---------------+
| Source        |     | Data          |     | Presentation  |
| Systems       |     | Warehouse     |     | Layer         |
+---------------+     +---------------+     +---------------+
| CRM           |     | Staging Area  |     | BI Tools      |
| ERP           | --> | Integration   | --> | Dashboards    |
| Web Analytics |     | Data Marts    |     | Reports       |
| Flat Files    |     | (Star Schema) |     | Data Apps     |
+---------------+     +---------------+     +---------------+
       ^                     |                     |
       |                     v                     v
       |              +---------------+     +---------------+
       +<------------ | Metadata      |     | Self-Service  |
                      | (Catalog)     |     | Analytics     |
                      +---------------+     +---------------+
```

## Code Example

Conceptual data warehouse example:

```python
from dataclasses import dataclass
from datetime import date
from typing import List, Dict

@dataclass
class SalesWarehouse:
    """Conceptual representation of a sales data warehouse."""
    
    # Dimension tables (descriptive attributes)
    dim_customer: Dict  # customer_id -> customer details
    dim_product: Dict   # product_id -> product details
    dim_date: Dict      # date_id -> date attributes
    dim_store: Dict     # store_id -> store details
    
    # Fact table (measurements/metrics)
    fact_sales: List[Dict]  # Transactions with foreign keys
    
    def query_sales_by_region(self, region: str, year: int) -> Dict:
        """
        Example analytical query:
        Total sales by product category for a region and year.
        
        In SQL:
        SELECT p.category, SUM(f.sales_amount)
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        JOIN dim_store s ON f.store_id = s.store_id
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE s.region = 'West' AND d.year = 2024
        GROUP BY p.category
        """
        results = {}
        
        for sale in self.fact_sales:
            # Get dimension data
            store = self.dim_store.get(sale['store_id'], {})
            date_dim = self.dim_date.get(sale['date_id'], {})
            product = self.dim_product.get(sale['product_id'], {})
            
            # Apply filters
            if store.get('region') != region:
                continue
            if date_dim.get('year') != year:
                continue
            
            # Aggregate
            category = product.get('category', 'Unknown')
            results[category] = results.get(category, 0) + sale['sales_amount']
        
        return results
    
    def time_series_analysis(self, metric: str, grain: str = 'month') -> Dict:
        """
        Historical trend analysis - a core warehouse capability.
        Operational databases typically cannot do this efficiently.
        """
        trends = {}
        
        for sale in self.fact_sales:
            date_dim = self.dim_date.get(sale['date_id'], {})
            
            if grain == 'month':
                key = f"{date_dim['year']}-{date_dim['month']:02d}"
            elif grain == 'quarter':
                key = f"{date_dim['year']}-Q{date_dim['quarter']}"
            else:
                key = str(date_dim['year'])
            
            if key not in trends:
                trends[key] = {'total': 0, 'count': 0}
            
            trends[key]['total'] += sale.get(metric, 0)
            trends[key]['count'] += 1
        
        return trends

# The key difference: historical data enables trend analysis
# that operational systems (with only current data) cannot provide
```

## Key Takeaways

- A data warehouse is a centralized repository optimized for analytical processing
- Key characteristics: subject-oriented, integrated, time-variant, non-volatile
- Data warehouses consolidate data from multiple sources into a unified view
- Unlike operational databases, warehouses optimize for read-heavy analytical queries
- Cloud data warehouses (BigQuery, Snowflake, Redshift) have transformed the landscape
- Data warehouses enable business intelligence, reporting, and data-driven decisions

## Resources

- Bill Inmon's Data Warehouse Institute: <https://www.inmongrouptraining.com/>
- Kimball Group: <https://www.kimballgroup.com/>
- Google BigQuery: <https://cloud.google.com/bigquery>
- Snowflake: <https://www.snowflake.com/>
