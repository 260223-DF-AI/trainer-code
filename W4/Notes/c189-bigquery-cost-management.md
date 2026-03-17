# BigQuery Cost Management

## Learning Objectives

- Understand BigQuery pricing models
- Monitor and control query costs
- Apply cost optimization strategies
- Set up budget alerts and quotas

## Why This Matters

BigQuery costs can grow quickly with large datasets and frequent queries. Understanding pricing and implementing cost controls ensures predictable spending and efficient resource utilization.

## Concept Explanation

### Pricing Models

| Model | How It Works | Best For |
|-------|--------------|----------|
| On-Demand | $6.25 per TB scanned | Variable workloads |
| Flat-Rate | Monthly slot reservations | Predictable, high-volume |

### On-Demand Pricing Details

- **Query**: $6.25 per TB (first 1 TB/month free)
- **Storage**: $0.02 per GB/month (active), $0.01 per GB/month (long-term)
- **Streaming**: $0.01 per 200 MB

### Cost Estimation

```sql
-- Check historical query costs
SELECT 
    user_email,
    DATE(creation_time) as query_date,
    SUM(total_bytes_billed) / POW(1024, 4) as tb_billed,
    SUM(total_bytes_billed) / POW(1024, 4) * 6.25 as estimated_cost
FROM `project.region-us`.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY user_email, query_date
ORDER BY estimated_cost DESC;
```

### Cost Control Strategies

#### 1. Use Dry Runs

```python
from google.cloud import bigquery

client = bigquery.Client()
job_config = bigquery.QueryJobConfig(dry_run=True)

query = "SELECT * FROM dataset.large_table"
job = client.query(query, job_config=job_config)

tb_billed = job.total_bytes_processed / (1024**4)
cost = tb_billed * 6.25
print(f"Estimated cost: ${cost:.4f}")
```

#### 2. Set Maximum Bytes Billed

```python
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=10 * 1024**3  # 10 GB limit
)

try:
    job = client.query(query, job_config=job_config)
    result = job.result()
except Exception as e:
    print(f"Query exceeded limit: {e}")
```

#### 3. Use Partitioning and Clustering

Reduces bytes scanned = lower costs.

#### 4. Cache Query Results

BigQuery caches results for 24 hours. Same query = no charge.

```python
job_config = bigquery.QueryJobConfig(
    use_query_cache=True  # Default is True
)
```

### Setting Quotas

In Google Cloud Console:

1. Go to IAM & Admin > Quotas
2. Filter for BigQuery
3. Set daily/monthly query limits

### Budget Alerts

```python
from google.cloud import billing_v1

# Set up budget alerts via Cloud Console or API
# Alert when spending reaches threshold
```

### Cost Monitoring Dashboard

```sql
-- Create a cost monitoring view
CREATE VIEW dataset.query_costs AS
SELECT 
    DATE(creation_time) as date,
    user_email,
    COUNT(*) as query_count,
    SUM(total_bytes_processed) / POW(1024, 3) as gb_processed,
    SUM(total_bytes_billed) / POW(1024, 4) * 6.25 as estimated_cost
FROM `project.region-us`.INFORMATION_SCHEMA.JOBS
WHERE job_type = 'QUERY'
GROUP BY date, user_email;
```

### Best Practices

| Strategy | Implementation |
|----------|----------------|
| Partition tables | Reduce scanned data |
| Select specific columns | Avoid SELECT * |
| Use dry runs | Estimate before running |
| Set byte limits | Prevent runaway queries |
| Monitor regularly | Track spending trends |

## Key Takeaways

- On-demand: Pay per TB scanned ($6.25/TB)
- Use dry runs to estimate costs before execution
- Set maximum_bytes_billed to prevent expensive queries
- Partitioning and clustering reduce costs significantly
- Monitor costs via INFORMATION_SCHEMA

## Resources

- BigQuery Pricing: <https://cloud.google.com/bigquery/pricing>
- Cost Controls: <https://cloud.google.com/bigquery/docs/custom-quotas>
