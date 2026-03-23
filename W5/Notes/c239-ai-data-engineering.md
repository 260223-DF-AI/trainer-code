# AI for Data Engineering

## Learning Objectives

- Apply AI tools specifically to data engineering workflows
- Use AI for SQL optimization, schema design, and pipeline development
- Understand how AI integrates with BigQuery and cloud data tools
- Build AI-enhanced data engineering practices

## Why This Matters

Data engineering is where AI tools deliver some of the most practical value. Writing SQL, designing schemas, debugging pipelines, and generating documentation are all tasks you perform daily. AI can accelerate each one. This topic connects everything you have learned this week to the specific tools and techniques of your data engineering practice.

## The Concept

### AI in the Data Engineering Lifecycle

```
Data Engineering Lifecycle:
Generation --> Storage --> Ingestion --> Transformation --> Serving

AI Can Help At Every Stage:
Generation:     Generate synthetic test data
Storage:        Design schemas, optimize storage formats
Ingestion:      Write extraction scripts, parse APIs  
Transformation: Write SQL/Python transforms, optimize queries
Serving:        Generate documentation, build dashboards
```

### AI-Assisted SQL Development

#### Schema Design

```
Prompt:
"Design a BigQuery star schema for an e-commerce analytics 
platform. Include:
- fact_orders (grain: one row per order line item)
- dim_customer (SCD Type 2)
- dim_product (with product category hierarchy)
- dim_date (calendar and fiscal attributes)
- dim_store (for multichannel: online, physical)

Requirements:
- Use INT64 surrogate keys
- Include audit columns (_loaded_at, _source_file)
- Partition fact table by order_date
- Cluster by store_key, product_key
- Generate CREATE TABLE statements in BigQuery SQL"
```

#### Query Generation

```
Prompt:
"Write a BigQuery query that:
1. Calculates customer Recency, Frequency, and Monetary 
   (RFM) segments
2. Uses the orders table (customer_id, order_date, 
   total_amount)
3. Defines recency as days since last order
4. Frequency as total order count
5. Monetary as total spend
6. Assigns each customer a score of 1-5 for each metric 
   using NTILE
7. Concatenates scores into an RFM segment string"
```

#### Query Optimization

```
Prompt:
"Optimize this BigQuery query for cost and performance:

SELECT c.customer_name, o.order_date, o.total_amount,
       p.product_name, p.category
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
AND p.category = 'Electronics'
ORDER BY o.total_amount DESC

The orders table has 500M rows, partitioned by order_date, 
clustered by product_id. Customers table has 10M rows. 
Products table has 50K rows.

Suggest: partition pruning, join order, column selection, 
and any other optimizations."
```

### AI-Assisted Pipeline Development

#### ETL Script Generation

```
Prompt:
"Write a Python ETL script that:
1. Extracts data from a REST API endpoint (paginated, 
   100 records per page)
2. Transforms JSON response into a flat DataFrame
3. Adds metadata columns (extract_timestamp, source_url)
4. Loads to BigQuery using the append disposition
5. Includes error handling, retry logic (3 attempts with 
   exponential backoff), and logging

Use: requests, pandas, google-cloud-bigquery
Follow Google Python Style Guide"
```

#### Data Quality Checks

```
Prompt:
"Generate Python data quality check functions for a 
BigQuery table analytics.fact_orders:

Checks needed:
1. Row count is within expected range (100K-150K per day)
2. No null values in required columns (order_id, 
   customer_key, order_date)
3. order_date is within expected range (yesterday)
4. total_amount has no negative values
5. Referential integrity: all customer_keys exist 
   in dim_customer
6. No duplicate order_ids

Return results as a list of dicts with: check_name, 
status (PASS/FAIL), details, row_count_affected"
```

### AI for Data Documentation

#### Automated Data Lineage Documentation

```
Prompt:
"Given these three SQL transformation queries, document 
the data lineage showing which source columns feed into 
which target columns:

Query 1 (staging): [paste query]
Query 2 (transform): [paste query]  
Query 3 (load): [paste query]

Format as a markdown table with columns:
Target Table | Target Column | Source Table | Source Column | Transformation"
```

#### Pipeline Runbook Generation

```
Prompt:
"Generate a runbook for this ETL pipeline:
- Runs daily at 2 AM UTC via Cloud Scheduler
- Extracts from Salesforce API
- Loads to BigQuery dataset: production.salesforce_raw
- Downstream consumers: analytics.dim_opportunity, 
  analytics.fact_activities

Include sections for:
- Normal operation monitoring
- Common failure scenarios and fixes
- Escalation procedures
- Recovery steps for data issues"
```

### BigQuery-Specific AI Use Cases

| Task | AI Approach |
| ---- | ----------- |
| Partition strategy | Describe query patterns, let AI recommend |
| Clustering selection | Provide common WHERE/JOIN clauses for analysis |
| Cost estimation | Describe query and table sizes for estimate |
| UDF development | Generate JavaScript or SQL UDFs from requirements |
| Scheduled queries | Generate scheduled query configurations |
| Access control | Generate IAM policy recommendations from requirements |

### Building an AI-Enhanced Data Practice

```
Daily Workflow:
Morning:  Review pipeline status
          Use AI to investigate any failures
          
Midday:   Development work
          Use AI for code generation and review
          
Afternoon: Documentation and testing
           Use AI to generate docs and test cases
           
End of day: Code review
            Use AI for initial review, human for final
```

## Key Takeaways

- AI tools apply to every stage of the data engineering lifecycle
- SQL development (schema design, query writing, optimization) is the highest-value use case
- Pipeline development benefits from AI-generated boilerplate and error handling
- Data documentation (lineage, runbooks, dictionaries) becomes feasible with AI assistance
- Build AI into your daily workflow as an accelerator, not a replacement

## Additional Resources

- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices-performance-overview)
- [dbt - Analytics Engineering Guide](https://docs.getdbt.com/guides)
- [Google Cloud - AI for Data Analytics](https://cloud.google.com/solutions/ai-analytics)
