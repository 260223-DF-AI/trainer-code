# GCP Data Services

## Learning Objectives

- Understand the Google Cloud Platform data services ecosystem
- Learn about Cloud Storage and BigQuery as core data services
- Explore Dataflow, Pub/Sub, and other data processing services
- Recognize GCP's strengths in analytics and machine learning

## Why This Matters

Google Cloud Platform is known for its data analytics and machine learning capabilities, born from Google's internal data infrastructure. BigQuery, in particular, is recognized as a leading serverless data warehouse. GCP will be our primary cloud platform for hands-on exercises in this course, making understanding these services essential.

## Concept Explanation

### GCP Data Services Overview

GCP provides a comprehensive data ecosystem:

```
+------------------+     +------------------+     +------------------+
|    Storage       |     |    Analytics     |     |   Integration    |
+------------------+     +------------------+     +------------------+
| Cloud Storage    |     | BigQuery         |     | Pub/Sub          |
| Persistent Disk  |     | Dataproc         |     | Dataflow         |
| Filestore        |     | Dataflow         |     | Cloud Composer   |
|                  |     | Looker           |     | Data Fusion      |
+------------------+     +------------------+     +------------------+
         |                       |                       |
         +------------+----------+-----------+-----------+
                      |                      |
              +-------v-------+      +-------v-------+
              |   Databases   |      |   ML/AI       |
              +---------------+      +---------------+
              | Cloud SQL     |      | Vertex AI     |
              | Spanner       |      | AutoML        |
              | Firestore     |      | Vision API    |
              | Bigtable      |      | NLP API       |
              +---------------+      +---------------+
```

### Storage Services

#### Cloud Storage

Object storage similar to AWS S3, but with unique features.

**Storage Classes:**

| Class | Use Case | Min Duration | Price/GB/Month |
|-------|----------|--------------|----------------|
| Standard | Frequent access | None | $0.020 |
| Nearline | Monthly access | 30 days | $0.010 |
| Coldline | Quarterly access | 90 days | $0.004 |
| Archive | Yearly access | 365 days | $0.0012 |

**Key Features:**

- Uniform bucket-level access (simplified permissions)
- Object versioning
- Lifecycle management
- Parallel composite uploads for large files
- Requestor pays buckets
- Signed URLs for secure temporary access

#### Data Organization

GCP uses a project-based hierarchy:

```
Organization
    |
    +-- Folder (optional)
         |
         +-- Project
              |
              +-- Bucket
                   |
                   +-- Objects (files)
```

### Analytics Services

#### BigQuery

Serverless, highly scalable data warehouse - a flagship GCP service.

**Key Features:**

- Serverless (no infrastructure to manage)
- Columnar storage
- Separation of storage and compute
- Standard SQL with extensions
- Built-in ML (BigQuery ML)
- Federated queries (external data)
- Streaming inserts
- Geographic data types (BigQuery GIS)

**Pricing Models:**

| Model | Best For | Cost |
|-------|----------|------|
| On-demand | Variable queries | $5/TB scanned |
| Flat-rate | Predictable queries | $2,000/month per 100 slots |
| Editions | Enterprise features | Based on edition |

**Key Concepts:**

- **Datasets**: Containers for tables (like databases)
- **Tables**: Native, external, or views
- **Partitioning**: Time or integer-based for cost/performance
- **Clustering**: Co-locate related data within partitions
- **Slots**: Units of compute capacity

#### Dataproc

Managed Apache Spark and Hadoop service.

**Features:**

- Fast cluster creation (< 90 seconds)
- Per-second billing
- Preemptible VMs for cost savings
- Auto-scaling clusters
- Integrated with GCS, BigQuery
- Optional components (Jupyter, Presto)

**Use Cases:**

- ETL at scale
- Machine learning with Spark MLlib
- Data exploration with Jupyter
- Migrating on-premises Hadoop

#### Dataflow

Fully managed stream and batch data processing based on Apache Beam.

**Key Features:**

- Unified batch and streaming model
- Autoscaling
- Right-fitting (auto worker sizing)
- Exactly-once processing
- Supports Python, Java, Go

**Use Cases:**

- Real-time ETL
- Streaming analytics
- Data enrichment
- CDC (Change Data Capture) processing

### Messaging and Integration

#### Cloud Pub/Sub

Global messaging and event ingestion.

**Features:**

- At-least-once delivery
- Push and pull subscriptions
- Message ordering (optional)
- Dead-letter topics
- Message filtering

**Use Cases:**

- Event-driven architectures
- Streaming data ingestion
- Decoupling services
- Parallel processing fanout

#### Cloud Composer

Managed Apache Airflow for workflow orchestration.

**Features:**

- Fully managed Airflow
- DAG (Directed Acyclic Graph) workflows
- Pre-built operators for GCP services
- Multi-cloud orchestration
- Monitoring and logging

### Database Services

#### Cloud SQL

Managed relational databases.

| Engine | Max Storage | Max Connections |
|--------|-------------|-----------------|
| MySQL | 64 TB | Configurable |
| PostgreSQL | 64 TB | 4,000 |
| SQL Server | 64 TB | Based on edition |

#### Cloud Spanner

Globally distributed, strongly consistent relational database.

**Key Features:**

- Horizontal scaling with strong consistency
- 99.999% availability (multi-region)
- SQL semantics
- Expensive but powerful

**Use Cases:**

- Global financial applications
- Gaming leaderboards
- Inventory management

#### Firestore

Serverless NoSQL document database.

**Modes:**

- Native mode: Mobile/web, real-time sync
- Datastore mode: Server workloads

#### Cloud Bigtable

Managed wide-column NoSQL database.

**Use Cases:**

- Time-series data
- IoT sensor data
- Financial data
- Personalization

## Code Example

Working with GCP data services:

```python
from google.cloud import storage, bigquery, pubsub_v1
import pandas as pd
from io import BytesIO

class GCPDataServices:
    """Interact with GCP data services."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.storage_client = storage.Client(project=project_id)
        self.bq_client = bigquery.Client(project=project_id)
    
    # Cloud Storage Operations
    def upload_to_gcs(self, bucket_name: str, source_file: str, 
                      destination: str):
        """Upload file to Cloud Storage."""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination)
        blob.upload_from_filename(source_file)
        
        return f"gs://{bucket_name}/{destination}"
    
    def upload_dataframe_to_gcs(self, df: pd.DataFrame, bucket_name: str,
                                 destination: str):
        """Upload DataFrame as Parquet to GCS."""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination)
        
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        blob.upload_from_file(buffer, content_type="application/octet-stream")
        return f"gs://{bucket_name}/{destination}"
    
    def list_gcs_objects(self, bucket_name: str, prefix: str = None) -> list:
        """List objects in a bucket."""
        bucket = self.storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]
    
    # BigQuery Operations
    def run_query(self, query: str) -> pd.DataFrame:
        """Run BigQuery query and return DataFrame."""
        return self.bq_client.query(query).to_dataframe()
    
    def load_gcs_to_bigquery(self, gcs_uri: str, table_id: str,
                             write_disposition: str = "WRITE_TRUNCATE"):
        """Load data from GCS to BigQuery."""
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=write_disposition
        )
        
        load_job = self.bq_client.load_table_from_uri(
            gcs_uri,
            table_id,
            job_config=job_config
        )
        
        load_job.result()  # Wait for job
        
        table = self.bq_client.get_table(table_id)
        print(f"Loaded {table.num_rows} rows to {table_id}")
    
    def load_dataframe_to_bigquery(self, df: pd.DataFrame, table_id: str):
        """Load DataFrame directly to BigQuery."""
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            autodetect=True
        )
        
        job = self.bq_client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()
        
        print(f"Loaded {len(df)} rows to {table_id}")
    
    def create_dataset(self, dataset_id: str, location: str = "US"):
        """Create a BigQuery dataset."""
        dataset = bigquery.Dataset(f"{self.project_id}.{dataset_id}")
        dataset.location = location
        
        dataset = self.bq_client.create_dataset(dataset, exists_ok=True)
        print(f"Created dataset {dataset.dataset_id}")


# Pub/Sub operations
class PubSubService:
    """Interact with Cloud Pub/Sub."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
    
    def publish_message(self, topic_id: str, data: dict):
        """Publish a message to a topic."""
        import json
        
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        message_data = json.dumps(data).encode("utf-8")
        
        future = self.publisher.publish(topic_path, message_data)
        message_id = future.result()
        
        return message_id
    
    def publish_batch(self, topic_id: str, records: list):
        """Publish multiple messages."""
        import json
        
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        futures = []
        
        for record in records:
            data = json.dumps(record).encode("utf-8")
            future = self.publisher.publish(topic_path, data)
            futures.append(future)
        
        # Wait for all publishes
        for future in futures:
            future.result()
        
        print(f"Published {len(records)} messages")


# Dataflow example (Apache Beam)
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_dataflow_pipeline():
    """Example Dataflow batch pipeline."""
    options = PipelineOptions(
        runner="DataflowRunner",
        project="my-project",
        region="us-central1",
        temp_location="gs://my-bucket/temp"
    )
    
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read CSV" >> beam.io.ReadFromText("gs://bucket/input.csv")
            | "Parse" >> beam.Map(lambda line: line.split(","))
            | "Transform" >> beam.Map(lambda x: {"name": x[0], "value": int(x[1])})
            | "Write to BQ" >> beam.io.WriteToBigQuery(
                "project:dataset.table",
                schema="name:STRING,value:INTEGER"
            )
        )
```

## Key Takeaways

- Cloud Storage provides durable object storage with multiple classes for cost optimization
- BigQuery is a serverless data warehouse with separation of storage and compute
- Dataflow enables unified batch and streaming processing with Apache Beam
- Pub/Sub provides global messaging for event-driven architectures
- GCP excels in analytics and ML integration (Vertex AI, BigQuery ML)
- Project-based organization simplifies resource management and billing

## Resources

- BigQuery Documentation: <https://cloud.google.com/bigquery/docs>
- Cloud Storage: <https://cloud.google.com/storage/docs>
- Dataflow: <https://cloud.google.com/dataflow/docs>
- GCP Architecture Center: <https://cloud.google.com/architecture>
