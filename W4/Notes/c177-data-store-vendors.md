# Data Store Vendors

## Learning Objectives

- Survey major cloud data warehouse vendors
- Compare Snowflake, Redshift, BigQuery, and Synapse
- Understand key differentiators and strengths of each platform
- Learn criteria for selecting a data warehouse solution

## Why This Matters

Choosing the right data warehouse platform is a significant architectural decision with long-term implications for cost, performance, and team productivity. Understanding vendor offerings helps you make informed recommendations and work effectively with different platforms you may encounter in your career.

## Concept Explanation

### Major Cloud Data Warehouse Vendors

The cloud data warehouse market is dominated by four major players:

```
+---------------+     +---------------+     +---------------+     +---------------+
|   Snowflake   |     |    BigQuery   |     |    Redshift   |     |    Synapse    |
+---------------+     +---------------+     +---------------+     +---------------+
| Independent   |     |    Google     |     |     AWS       |     |   Microsoft   |
| Multi-cloud   |     |     GCP       |     |               |     |     Azure     |
+---------------+     +---------------+     +---------------+     +---------------+
```

### Snowflake

**Overview:**
Cloud-native data warehouse that runs on AWS, Azure, and GCP.

**Key Features:**

- Virtual warehouses (separate compute clusters)
- Zero-copy cloning
- Time travel (historical data recovery)
- Data sharing across organizations
- Supports semi-structured data (JSON, Avro, Parquet)

**Architecture:**

```
+-------------------+
|  Cloud Services   |  <- Authentication, metadata, optimization
+-------------------+
         |
+-------------------+
| Virtual Warehouses|  <- Compute (scalable, independent)
| (XS, S, M, L, XL) |
+-------------------+
         |
+-------------------+
|  Centralized      |  <- Storage (separated from compute)
|     Storage       |
+-------------------+
```

**Strengths:**

- True separation of storage and compute
- Near-instant scaling
- Multi-cloud portability
- Strong data sharing capabilities
- Excellent for concurrent workloads

**Pricing Model:**

- Storage: Per TB per month
- Compute: Credits per second of warehouse time
- Predictable with commitment discounts

### Google BigQuery

**Overview:**
Serverless, fully managed data warehouse with no infrastructure to manage.

**Key Features:**

- Serverless (no clusters to manage)
- Slot-based or on-demand pricing
- Built-in ML (BigQuery ML)
- Streaming inserts
- Federated queries to external data
- Native GIS support

**Architecture:**

```
+-------------------+
|   Dremel Engine   |  <- Distributed query execution
+-------------------+
         |
+-------------------+
|  Columnar Storage |  <- Capacitor format
|   (Colossus FS)   |
+-------------------+
         |
+-------------------+
|  Jupiter Network  |  <- High-speed data transfer
+-------------------+
```

**Strengths:**

- Truly serverless (zero management)
- Excellent for ad-hoc analytics
- Petabyte scale with ease
- Strong ML integration
- No cluster tuning required

**Pricing Model:**

- On-demand: Per TB scanned
- Flat-rate: Monthly slot reservations
- Storage: Per TB per month

### Amazon Redshift

**Overview:**
AWS's fully managed, petabyte-scale data warehouse.

**Key Features:**

- RA3 nodes (storage/compute separation)
- Redshift Spectrum (query S3 data)
- Concurrency scaling
- Federated queries
- Machine learning integration

**Architecture:**

```
+-------------------+
|   Leader Node     |  <- Query planning, coordination
+-------------------+
         |
+-------------------+
|  Compute Nodes    |  <- Query execution
|  (DC2, RA3)       |
+-------------------+
         |
+-------------------+
|   Managed Storage |  <- (RA3 only) or local SSD (DC2)
+-------------------+
```

**Strengths:**

- Deep AWS ecosystem integration
- Mature, proven technology
- Excellent for existing AWS customers
- Strong price/performance
- Redshift Spectrum for data lake queries

**Pricing Model:**

- On-demand: Per node per hour
- Reserved: 1-3 year commitments
- Serverless: Per RPU-hour

### Azure Synapse Analytics

**Overview:**
Microsoft's unified analytics platform combining warehouse and big data.

**Key Features:**

- Dedicated SQL pools (provisioned)
- Serverless SQL pools (on-demand)
- Apache Spark pools
- Data integration (Synapse Pipelines)
- Power BI integration

**Architecture:**

```
+-------------------+
|  Synapse Studio   |  <- Unified workspace
+-------------------+
         |
    +----+----+
    |         |
+-------+ +-------+
|Dedicated| |Serverless|  <- SQL Pools
| Pool   | |  Pool   |
+-------+ +-------+
    |         |
+-------------------+
|    Data Lake      |  <- Storage (ADLS Gen2)
+-------------------+
```

**Strengths:**

- Unified analytics workspace
- Seamless Power BI integration
- Serverless and provisioned options
- Strong for Microsoft ecosystem
- Combined data warehouse and Spark

**Pricing Model:**

- Dedicated: Per DWU per hour
- Serverless: Per TB processed
- Spark: Per vCore per hour

### Vendor Comparison Matrix

| Feature | Snowflake | BigQuery | Redshift | Synapse |
|---------|-----------|----------|----------|---------|
| Serverless | No (managed) | Yes | Partial | Partial |
| Multi-cloud | Yes | GCP only | AWS only | Azure only |
| Separation | Full | Full | RA3 only | Partial |
| Streaming | Snowpipe | Native | Kinesis | Event Hub |
| ML Built-in | Limited | Strong | SageMaker | Azure ML |
| Data Sharing | Native | Limited | S3 | ADLS |

### Selection Criteria

When choosing a data warehouse vendor, consider:

#### 1. Existing Cloud Investment

| Situation | Recommendation |
|-----------|----------------|
| AWS-native org | Redshift |
| GCP-native org | BigQuery |
| Azure-native org | Synapse |
| Multi-cloud strategy | Snowflake |

#### 2. Workload Patterns

| Pattern | Best Fit |
|---------|----------|
| Ad-hoc, variable | BigQuery (on-demand) |
| Consistent, predictable | Snowflake / Redshift |
| Mixed analytics + ML | Synapse / BigQuery |

#### 3. Team Skills

| Skills | Best Fit |
|--------|----------|
| SQL-focused | BigQuery, Snowflake |
| AWS expertise | Redshift |
| Microsoft/Power BI | Synapse |

## Code Example

Connecting to different data warehouses:

```python
# Snowflake connection
import snowflake.connector

def query_snowflake(query: str, account: str, user: str, password: str):
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse='COMPUTE_WH',
        database='ANALYTICS',
        schema='PUBLIC'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# BigQuery connection
from google.cloud import bigquery

def query_bigquery(query: str, project_id: str):
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]


# Redshift connection
import psycopg2

def query_redshift(query: str, host: str, database: str, user: str, password: str):
    conn = psycopg2.connect(
        host=host,
        port=5439,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Synapse connection
import pyodbc

def query_synapse(query: str, server: str, database: str):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Authentication=ActiveDirectoryInteractive;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
```

## Key Takeaways

- Four major cloud DWH vendors: Snowflake, BigQuery, Redshift, Synapse
- Snowflake offers multi-cloud and true compute/storage separation
- BigQuery provides serverless simplicity with no infrastructure management
- Redshift integrates deeply with AWS and offers flexible node types
- Synapse unifies analytics with strong Microsoft ecosystem integration
- Select based on: existing cloud, workload patterns, team skills, and pricing model
- All platforms converging toward separation of storage and compute

## Resources

- Snowflake Documentation: <https://docs.snowflake.com/>
- BigQuery Documentation: <https://cloud.google.com/bigquery/docs>
- Redshift Documentation: <https://docs.aws.amazon.com/redshift/>
- Synapse Documentation: <https://docs.microsoft.com/en-us/azure/synapse-analytics/>
