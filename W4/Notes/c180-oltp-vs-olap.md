# OLTP vs. OLAP

## Learning Objectives

- Compare OLTP and OLAP systems comprehensively
- Understand when to use each type of system
- Recognize how data flows between OLTP and OLAP
- Apply selection criteria to real-world scenarios

## Why This Matters

Organizations need both OLTP and OLAP systems. Understanding their differences helps you design appropriate data architectures, choose the right tools for each use case, and explain the need for data warehouses to stakeholders.

## Concept Explanation

### Side-by-Side Comparison

| Aspect | OLTP | OLAP |
|--------|------|------|
| **Purpose** | Run the business | Analyze the business |
| **Users** | Operational staff, applications | Analysts, executives |
| **Queries** | Simple, targeted | Complex, aggregated |
| **Data** | Current state | Historical |
| **Updates** | Frequent (real-time) | Batch (periodic) |
| **Response Time** | Milliseconds | Seconds to minutes |
| **Concurrency** | Thousands of users | Dozens of users |
| **Schema** | Normalized (3NF) | Denormalized (Star) |
| **Optimization** | Write performance | Read performance |

### Visual Comparison

```
OLTP System                          OLAP System
+------------------+                 +------------------+
|  Application     |                 |  BI Dashboard    |
|  (Orders, CRM)   |                 |  (Analytics)     |
+--------+---------+                 +--------+---------+
         |                                    |
         v                                    v
+------------------+                 +------------------+
|  INSERT          |                 |  SELECT          |
|  UPDATE          |                 |  GROUP BY        |
|  DELETE          |                 |  JOIN            |
|  SELECT (by PK)  |                 |  Aggregations    |
+--------+---------+                 +--------+---------+
         |                                    |
         v                                    v
+------------------+                 +------------------+
|  Normalized      |                 |  Star Schema     |
|  Tables          |                 |  Fact/Dimensions |
|  (3NF)           |                 |  (Denormalized)  |
+------------------+                 +------------------+
```

### Query Pattern Comparison

**OLTP Query (Point Lookup):**

```sql
-- Find a specific customer's current order status
SELECT order_id, status, shipping_address
FROM orders
WHERE customer_id = 12345
  AND order_id = 98765;

-- Execution: ~5ms, uses index
```

**OLAP Query (Aggregation):**

```sql
-- Analyze sales trends by region and product category
SELECT 
    c.region,
    p.category,
    d.year,
    d.quarter,
    SUM(f.revenue) as total_revenue,
    SUM(f.quantity) as units_sold,
    AVG(f.discount_percent) as avg_discount
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE d.year IN (2023, 2024)
GROUP BY c.region, p.category, d.year, d.quarter
ORDER BY d.year DESC, d.quarter DESC, total_revenue DESC;

-- Execution: ~5-30 seconds, full table scans
```

### Data Model Comparison

**OLTP: Normalized Design**

```
orders          order_items       products         customers
+--------+     +----------+      +----------+     +----------+
|order_id|<-+  |item_id   |   +->|product_id|     |customer_ |
|customer|  +--| order_id |   |  |name      |<----| id       |
|date    |     |product_id|---+  |price     |     |name      |
|status  |     |quantity  |      |category_ |     |email     |
+--------+     |price     |      |   id(FK) |     +----------+
               +----------+      +----------+
                                      |
                                 +----------+
                                 |categories|
                                 +----------+
                                 |category_ |
                                 |   id     |
                                 |name      |
                                 +----------+

Multiple tables, normalized to 3NF
```

**OLAP: Denormalized Star Schema**

```
                    dim_date
                    +----------+
                    |date_id   |
                    |full_date |
                    |year      |
                    |quarter   |
                    |month     |
                    +----+-----+
                         |
dim_customer             |              dim_product
+----------+             |              +----------+
|customer_ |             |              |product_id|
|   id     |      +------+------+       |name      |
|name      |----->|  fact_sales |<------|category  |
|region    |      |  date_id    |       |brand     |
|segment   |      |  customer_id|       |price     |
+----------+      |  product_id |       +----------+
                  |  quantity   |
                  |  revenue    |
                  +-------------+

Fewer tables, attributes pre-joined into dimensions
```

### Performance Trade-offs

| Operation | OLTP Optimized | OLAP Optimized |
|-----------|----------------|----------------|
| INSERT single row | Milliseconds | N/A (batch) |
| UPDATE single row | Milliseconds | Rare/prohibited |
| Point lookup | Milliseconds (indexed) | Slower |
| Scan entire table | Very slow | Optimized |
| Aggregation | Resource intensive | Optimized |
| JOIN many tables | Can be slow | Pre-joined data |

### Data Flow: OLTP to OLAP

```
+-------------+     +-------------+     +-------------+
|   OLTP      |     |   ETL/ELT   |     |   OLAP      |
|  Systems    |     |  Pipeline   |     |  System     |
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Orders  --->|---->| Transform   |---->| fact_sales  |
| Products--->|     | Clean       |     | dim_product |
| Customers-->|     | Aggregate   |     | dim_customer|
| Inventory-->|     | Load        |     | dim_date    |
|             |     |             |     |             |
+-------------+     +-------------+     +-------------+
      |                   |                   |
      v                   v                   v
  Current Data       Batch Process       Historical Data
  Write-Heavy        Nightly/Hourly        Read-Heavy
  Normalized         Transformation        Denormalized
```

### When to Use Each

**Choose OLTP When:**

- Processing individual transactions
- Requiring real-time data updates
- Supporting operational applications
- Needing ACID compliance
- Handling high concurrency writes

**Choose OLAP When:**

- Running complex analytical queries
- Analyzing historical trends
- Supporting business intelligence
- Generating reports and dashboards
- Performing ad-hoc exploration

## Code Example

Demonstrating OLTP vs. OLAP patterns:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class SystemCharacteristics:
    system_type: str
    typical_query: str
    response_time: str
    data_freshness: str
    user_type: str

class SystemSelector:
    """Help select between OLTP and OLAP systems."""
    
    OLTP = SystemCharacteristics(
        system_type="OLTP",
        typical_query="SELECT * FROM orders WHERE order_id = ?",
        response_time="< 100ms",
        data_freshness="Real-time",
        user_type="Operational staff, applications"
    )
    
    OLAP = SystemCharacteristics(
        system_type="OLAP",
        typical_query="SELECT region, SUM(revenue) FROM sales GROUP BY region",
        response_time="Seconds to minutes",
        data_freshness="Periodic batch (hourly/daily)",
        user_type="Analysts, executives"
    )
    
    @classmethod
    def recommend(cls, requirements: Dict) -> SystemCharacteristics:
        """
        Recommend OLTP or OLAP based on requirements.
        
        Requirements dict keys:
        - query_type: 'point_lookup' | 'aggregation'
        - update_frequency: 'realtime' | 'batch'
        - data_scope: 'current' | 'historical'
        - user_type: 'operational' | 'analytical'
        """
        oltp_score = 0
        olap_score = 0
        
        if requirements.get('query_type') == 'point_lookup':
            oltp_score += 2
        elif requirements.get('query_type') == 'aggregation':
            olap_score += 2
        
        if requirements.get('update_frequency') == 'realtime':
            oltp_score += 2
        elif requirements.get('update_frequency') == 'batch':
            olap_score += 1
        
        if requirements.get('data_scope') == 'current':
            oltp_score += 1
        elif requirements.get('data_scope') == 'historical':
            olap_score += 2
        
        if requirements.get('user_type') == 'operational':
            oltp_score += 1
        elif requirements.get('user_type') == 'analytical':
            olap_score += 2
        
        return cls.OLTP if oltp_score > olap_score else cls.OLAP


# Usage examples
scenarios = [
    {
        "name": "Check customer order status",
        "requirements": {
            "query_type": "point_lookup",
            "update_frequency": "realtime",
            "data_scope": "current",
            "user_type": "operational"
        }
    },
    {
        "name": "Q4 sales analysis by region",
        "requirements": {
            "query_type": "aggregation",
            "update_frequency": "batch",
            "data_scope": "historical",
            "user_type": "analytical"
        }
    },
    {
        "name": "Real-time inventory update",
        "requirements": {
            "query_type": "point_lookup",
            "update_frequency": "realtime",
            "data_scope": "current",
            "user_type": "operational"
        }
    },
    {
        "name": "Customer cohort retention analysis",
        "requirements": {
            "query_type": "aggregation",
            "update_frequency": "batch",
            "data_scope": "historical",
            "user_type": "analytical"
        }
    }
]

for scenario in scenarios:
    recommendation = SystemSelector.recommend(scenario["requirements"])
    print(f"{scenario['name']}: {recommendation.system_type}")
    print(f"  Response time: {recommendation.response_time}")
    print(f"  User type: {recommendation.user_type}")
    print()
```

## Key Takeaways

- OLTP and OLAP serve fundamentally different purposes
- OLTP runs the business with real-time transactions; OLAP analyzes the business
- OLTP uses normalized schemas for write efficiency; OLAP uses denormalized for reads
- Data flows from OLTP to OLAP through ETL/ELT pipelines
- Organizations need both systems working together
- Choose OLTP for transactions, OLAP for analytics
- Modern architectures increasingly blur these lines with HTAP systems

## Resources

- OLTP vs OLAP: <https://www.oracle.com/database/what-is-oltp/>
- Data Warehouse Design: <https://www.kimballgroup.com/>
- HTAP Systems: <https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing>
