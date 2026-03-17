# AWS Data Services

## Learning Objectives

- Understand the AWS data services ecosystem
- Learn about core storage services: S3 and its features
- Explore AWS analytics and data warehouse offerings
- Recognize data integration and processing services

## Why This Matters

Amazon Web Services is the largest cloud provider and offers a comprehensive suite of data services. Many organizations use AWS for their data infrastructure, making familiarity with these services essential for data professionals. Understanding AWS data services helps you architect solutions and communicate effectively with teams using AWS.

## Concept Explanation

### AWS Data Services Overview

AWS organizes data services into several categories:

```
+------------------+     +------------------+     +------------------+
|    Storage       |     |    Analytics     |     |   Integration    |
+------------------+     +------------------+     +------------------+
| S3               |     | Redshift         |     | Glue             |
| EBS              |     | Athena           |     | Data Pipeline    |
| EFS              |     | EMR              |     | AppFlow          |
| Glacier          |     | Kinesis          |     | EventBridge      |
+------------------+     +------------------+     +------------------+
         |                       |                       |
         +------------+----------+-----------+-----------+
                      |                      |
              +-------v-------+      +-------v-------+
              |   Databases   |      |   ML/AI       |
              +---------------+      +---------------+
              | RDS           |      | SageMaker     |
              | DynamoDB      |      | Comprehend    |
              | Aurora        |      | Rekognition   |
              | DocumentDB    |      | Forecast      |
              +---------------+      +---------------+
```

### Storage Services

#### Amazon S3 (Simple Storage Service)

The foundation of AWS data storage - object storage with virtually unlimited scale.

**Key Features:**

- 11 nines (99.999999999%) durability
- Multiple storage classes for cost optimization
- Versioning and lifecycle policies
- Event notifications for automation
- Strong consistency for all operations

**Storage Classes:**

| Class | Use Case | First Byte Latency |
|-------|----------|-------------------|
| S3 Standard | Frequent access | Milliseconds |
| S3 Intelligent-Tiering | Unknown patterns | Milliseconds |
| S3 Standard-IA | Infrequent access | Milliseconds |
| S3 One Zone-IA | Non-critical infrequent | Milliseconds |
| S3 Glacier Instant | Archive with instant access | Milliseconds |
| S3 Glacier Flexible | Archive, hours retrieval | Minutes-Hours |
| S3 Glacier Deep Archive | Long-term archive | 12-48 Hours |

#### S3 Data Lake Features

- **S3 Select**: Query data in place using SQL
- **S3 Access Points**: Simplified access management
- **S3 Object Lambda**: Transform data on retrieval
- **S3 Inventory**: Automated object cataloging

### Analytics Services

#### Amazon Redshift

Fully managed petabyte-scale data warehouse.

**Key Features:**

- Columnar storage for analytics
- Massively parallel processing (MPP)
- Redshift Spectrum: query S3 data directly
- RA3 nodes: separate compute and storage
- Concurrency scaling: handle peak loads

**Use Cases:**

- Business intelligence and reporting
- Complex analytical queries
- Historical data analysis

#### Amazon Athena

Serverless query service for S3 data.

**Key Features:**

- No infrastructure to manage
- Pay per query (per TB scanned)
- Standard SQL (Presto engine)
- Supports CSV, JSON, Parquet, ORC
- Integrates with AWS Glue Data Catalog

**Best For:**

- Ad-hoc querying of data lake
- Quick exploration of S3 data
- Cost-effective for sporadic queries

#### Amazon EMR (Elastic MapReduce)

Managed big data platform for Apache Spark, Hadoop, and more.

**Supported Frameworks:**

- Apache Spark
- Apache Hadoop
- Apache Hive
- Presto
- Apache Flink

#### Amazon Kinesis

Real-time streaming data platform.

| Service | Purpose |
|---------|---------|
| Kinesis Data Streams | Ingest streaming data |
| Kinesis Data Firehose | Load data to destinations |
| Kinesis Data Analytics | Process with SQL/Flink |
| Kinesis Video Streams | Stream video |

### Data Integration Services

#### AWS Glue

Serverless ETL and data catalog service.

**Components:**

- **Data Catalog**: Metadata repository
- **Crawlers**: Auto-discover schema
- **ETL Jobs**: Spark-based transformations
- **DataBrew**: Visual data preparation
- **Workflows**: Orchestrate ETL pipelines

#### AWS Data Pipeline

Orchestration service for data movement and transformation.

### Database Services

#### Relational Databases

| Service | Description |
|---------|-------------|
| RDS | Managed MySQL, PostgreSQL, Oracle, SQL Server |
| Aurora | AWS-native, MySQL/PostgreSQL compatible |
| Aurora Serverless | Auto-scaling Aurora |

#### NoSQL Databases

| Service | Type | Use Case |
|---------|------|----------|
| DynamoDB | Key-value/Document | High-scale applications |
| DocumentDB | Document (MongoDB-compatible) | Content management |
| ElastiCache | In-memory (Redis/Memcached) | Caching, sessions |
| Keyspaces | Wide-column (Cassandra-compatible) | Time-series |
| Neptune | Graph | Relationships, knowledge graphs |

## Code Example

Working with AWS data services using boto3:

```python
import boto3
import pandas as pd
from io import StringIO, BytesIO

class AWSDataServices:
    """Interact with AWS data services."""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.s3 = boto3.client("s3", region_name=region)
        self.athena = boto3.client("athena", region_name=region)
        self.glue = boto3.client("glue", region_name=region)
    
    # S3 Operations
    def upload_dataframe_to_s3(self, df: pd.DataFrame, bucket: str, 
                                key: str, format: str = "parquet"):
        """Upload a DataFrame to S3."""
        if format == "parquet":
            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            buffer.seek(0)
            content_type = "application/octet-stream"
        else:  # CSV
            buffer = StringIO()
            df.to_csv(buffer, index=False)
            buffer = BytesIO(buffer.getvalue().encode())
            content_type = "text/csv"
        
        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=buffer.getvalue(),
            ContentType=content_type
        )
        print(f"Uploaded to s3://{bucket}/{key}")
    
    def read_parquet_from_s3(self, bucket: str, key: str) -> pd.DataFrame:
        """Read a Parquet file from S3."""
        response = self.s3.get_object(Bucket=bucket, Key=key)
        return pd.read_parquet(BytesIO(response["Body"].read()))
    
    # Athena Operations
    def run_athena_query(self, query: str, database: str, 
                         output_bucket: str) -> pd.DataFrame:
        """Execute an Athena query and return results as DataFrame."""
        # Start query
        response = self.athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": f"s3://{output_bucket}/athena-results/"
            }
        )
        
        query_id = response["QueryExecutionId"]
        
        # Wait for completion
        while True:
            status = self.athena.get_query_execution(
                QueryExecutionId=query_id
            )["QueryExecution"]["Status"]["State"]
            
            if status == "SUCCEEDED":
                break
            elif status in ["FAILED", "CANCELLED"]:
                raise Exception(f"Query {status}")
            
            import time
            time.sleep(1)
        
        # Get results
        results = self.athena.get_query_results(QueryExecutionId=query_id)
        
        # Parse to DataFrame
        columns = [col["Name"] for col in 
                   results["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]]
        rows = []
        for row in results["ResultSet"]["Rows"][1:]:  # Skip header
            rows.append([field.get("VarCharValue", "") 
                        for field in row["Data"]])
        
        return pd.DataFrame(rows, columns=columns)
    
    # Glue Catalog Operations
    def get_table_schema(self, database: str, table: str) -> list:
        """Get table schema from Glue Data Catalog."""
        response = self.glue.get_table(DatabaseName=database, Name=table)
        
        columns = response["Table"]["StorageDescriptor"]["Columns"]
        return [{"name": col["Name"], "type": col["Type"]} 
                for col in columns]
    
    def trigger_glue_job(self, job_name: str, arguments: dict = None):
        """Start a Glue ETL job."""
        params = {"JobName": job_name}
        if arguments:
            params["Arguments"] = arguments
        
        response = self.glue.start_job_run(**params)
        return response["JobRunId"]


# Redshift access example
import psycopg2

def query_redshift(host: str, database: str, user: str, 
                   password: str, query: str) -> pd.DataFrame:
    """Query Redshift using psycopg2."""
    conn = psycopg2.connect(
        host=host,
        port=5439,
        database=database,
        user=user,
        password=password
    )
    
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()


# Kinesis streaming example
def put_kinesis_records(stream_name: str, records: list):
    """Send records to Kinesis Data Stream."""
    kinesis = boto3.client("kinesis")
    
    # Format records
    formatted = [
        {
            "Data": json.dumps(record).encode(),
            "PartitionKey": str(record.get("id", hash(str(record))))
        }
        for record in records
    ]
    
    response = kinesis.put_records(
        StreamName=stream_name,
        Records=formatted
    )
    
    print(f"Sent {len(records)} records, "
          f"{response['FailedRecordCount']} failed")
```

## Key Takeaways

- S3 is the foundation of AWS data storage with multiple storage classes for optimization
- Redshift is AWS's data warehouse for complex analytics at scale
- Athena provides serverless querying of S3 data using standard SQL
- Glue offers ETL capabilities and a central data catalog
- Kinesis handles real-time streaming data ingestion and processing
- AWS has database options for every use case: relational, NoSQL, in-memory, graph

## Resources

- AWS Data Services Documentation: <https://docs.aws.amazon.com/>
- S3 Best Practices: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html>
- Redshift Documentation: <https://docs.aws.amazon.com/redshift/>
- AWS Architecture Center: <https://aws.amazon.com/architecture/>
