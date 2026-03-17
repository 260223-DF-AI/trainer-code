# Components of Big Data

## Learning Objectives

- Identify the core components of a Big Data ecosystem
- Understand the role of storage, processing, analytics, and visualization
- Learn about common tools in each component category
- Recognize how components work together in an architecture

## Why This Matters

Big Data is not a single technology but an ecosystem of interconnected components. Understanding these components helps you design end-to-end data solutions and select the right tools for each stage of the data lifecycle. This knowledge is fundamental to building scalable, maintainable data platforms.

## Concept Explanation

### The Big Data Technology Stack

A complete Big Data solution consists of four primary layers:

```
+-------------------------------------------------------+
|                    VISUALIZATION                       |
|   (Dashboards, Reports, Data Apps)                    |
+-------------------------------------------------------+
                          ^
                          |
+-------------------------------------------------------+
|                      ANALYTICS                         |
|   (Query Engines, ML, Statistical Analysis)           |
+-------------------------------------------------------+
                          ^
                          |
+-------------------------------------------------------+
|                     PROCESSING                         |
|   (Batch, Stream, ETL/ELT)                            |
+-------------------------------------------------------+
                          ^
                          |
+-------------------------------------------------------+
|                      STORAGE                           |
|   (Data Lakes, Warehouses, Databases)                 |
+-------------------------------------------------------+
                          ^
                          |
+-------------------------------------------------------+
|                      INGESTION                         |
|   (Data Collection, Streaming, Batch Loads)           |
+-------------------------------------------------------+
```

### 1. Data Ingestion

How data enters the system.

**Batch Ingestion:**

- Scheduled file transfers (FTP, SFTP)
- Database replication
- API bulk extracts
- File uploads

**Stream Ingestion:**

- Event streaming (Kafka, Pub/Sub)
- Log collection (Fluentd, Logstash)
- IoT data streams
- Real-time APIs

| Tool | Type | Use Case |
|------|------|----------|
| Apache Kafka | Streaming | High-throughput event ingestion |
| Apache Flume | Batch/Stream | Log aggregation |
| AWS Kinesis | Streaming | AWS ecosystem streaming |
| GCP Pub/Sub | Streaming | GCP ecosystem messaging |
| Apache NiFi | Both | Visual data flow management |

### 2. Data Storage

Where data resides and how it is organized.

**Data Lakes:**
Raw, unprocessed data in native format.

- Cloud object storage (S3, GCS, Azure Blob)
- Hadoop HDFS
- Delta Lake, Apache Iceberg (table formats)

**Data Warehouses:**
Structured, processed data optimized for analysis.

- Google BigQuery
- Snowflake
- Amazon Redshift
- Azure Synapse

**Operational Databases:**
Real-time transactional data.

- PostgreSQL, MySQL
- MongoDB, Cassandra
- Redis (caching)

**Storage Format Comparison:**

| Storage Type | Schema | Query Speed | Cost | Best For |
|--------------|--------|-------------|------|----------|
| Data Lake | Flexible | Variable | Low | Raw data, ML |
| Data Warehouse | Fixed | Fast | Medium | Analytics, BI |
| RDBMS | Fixed | Fast | High | Transactions |
| NoSQL | Flexible | Fast | Medium | Application data |

### 3. Data Processing

Transforming raw data into usable formats.

**Batch Processing:**
Process large volumes of accumulated data.

- Apache Spark
- Apache Hadoop MapReduce
- Google Dataflow (batch mode)
- AWS Glue

**Stream Processing:**
Process data as it arrives in real-time.

- Apache Flink
- Apache Kafka Streams
- Google Dataflow (streaming)
- Apache Storm

**Processing Comparison:**

| Aspect | Batch | Stream |
|--------|-------|--------|
| Latency | Minutes to hours | Milliseconds to seconds |
| Throughput | Very high | High |
| Complexity | Lower | Higher |
| Use Case | Historical analysis | Real-time dashboards |
| Data completeness | Complete | Partial (windowed) |

**ETL/ELT Tools:**

- Apache Airflow (orchestration)
- dbt (transformation)
- Fivetran, Airbyte (connectors)
- Talend, Informatica (enterprise)

### 4. Analytics and Query Engines

Making sense of processed data.

**SQL Query Engines:**

- Presto/Trino (distributed SQL)
- Apache Hive (SQL on Hadoop)
- BigQuery (serverless SQL)
- Spark SQL

**Machine Learning Platforms:**

- Google Vertex AI
- AWS SageMaker
- Azure Machine Learning
- MLflow (open source)

**Statistical Tools:**

- Python (pandas, scikit-learn)
- R
- Julia

### 5. Visualization and BI

Presenting insights to stakeholders.

**Business Intelligence:**

| Tool | Strength |
|------|----------|
| Tableau | Visual analytics |
| Power BI | Microsoft integration |
| Looker | Semantic modeling |
| Metabase | Open-source, SQL-focused |
| Superset | Open-source, Python-based |

**Dashboarding:**

- Grafana (time-series)
- Kibana (Elasticsearch)
- Custom web apps (Streamlit, Dash)

### Component Integration

These components work together in a data pipeline:

```
Source Systems        Processing             Analytics        Consumption
     |                    |                     |                 |
     v                    v                     v                 v
+---------+         +---------+           +---------+       +---------+
|   CRM   |-------->| Ingest  |---------->|  Query  |------>|Dashboard|
+---------+         | (Kafka) |           |(BigQuery|       |(Tableau)|
                    +---------+           +---------+       +---------+
+---------+              |                     |
|   ERP   |-------->     |                     |
+---------+              v                     v
                    +---------+           +---------+       +---------+
+---------+         |Transform|---------->|   ML    |------>| API     |
|  Logs   |-------->| (Spark) |           |(Vertex) |       | App     |
+---------+         +---------+           +---------+       +---------+
                         |
                         v
                    +---------+
                    | Storage |
                    | (GCS/BQ)|
                    +---------+
```

## Code Example

Demonstrating component interaction:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Component interfaces
class DataIngester(ABC):
    @abstractmethod
    def ingest(self, source: str) -> List[Dict]:
        pass

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: List[Dict]) -> List[Dict]:
        pass

class DataStorage(ABC):
    @abstractmethod
    def store(self, data: List[Dict], destination: str) -> None:
        pass

class DataAnalyzer(ABC):
    @abstractmethod
    def analyze(self, query: str) -> List[Dict]:
        pass


# Example implementations
class KafkaIngester(DataIngester):
    """Stream ingestion from Kafka."""
    def __init__(self, bootstrap_servers: str, topic: str):
        from confluent_kafka import Consumer
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'big-data-pipeline'
        })
        self.consumer.subscribe([topic])
    
    def ingest(self, source: str = None) -> List[Dict]:
        import json
        messages = []
        # Poll for messages
        for _ in range(100):  # Batch of 100
            msg = self.consumer.poll(1.0)
            if msg and not msg.error():
                messages.append(json.loads(msg.value()))
        return messages


class SparkProcessor(DataProcessor):
    """Batch processing with Spark."""
    def __init__(self):
        from pyspark.sql import SparkSession
        self.spark = SparkSession.builder.appName("Pipeline").getOrCreate()
    
    def process(self, data: List[Dict]) -> List[Dict]:
        from pyspark.sql.functions import col, upper
        
        df = self.spark.createDataFrame(data)
        
        # Apply transformations
        processed = df \
            .filter(col("value").isNotNull()) \
            .withColumn("name", upper(col("name")))
        
        return processed.collect()


class BigQueryStorage(DataStorage):
    """Store data in BigQuery."""
    def __init__(self, project_id: str):
        from google.cloud import bigquery
        self.client = bigquery.Client(project=project_id)
    
    def store(self, data: List[Dict], destination: str) -> None:
        table_ref = self.client.get_table(destination)
        errors = self.client.insert_rows_json(table_ref, data)
        if errors:
            raise Exception(f"Insert errors: {errors}")


class BigQueryAnalyzer(DataAnalyzer):
    """Query data from BigQuery."""
    def __init__(self, project_id: str):
        from google.cloud import bigquery
        self.client = bigquery.Client(project=project_id)
    
    def analyze(self, query: str) -> List[Dict]:
        result = self.client.query(query)
        return [dict(row) for row in result]


# Pipeline orchestration
class BigDataPipeline:
    """Orchestrate data flow through components."""
    
    def __init__(
        self,
        ingester: DataIngester,
        processor: DataProcessor,
        storage: DataStorage,
        analyzer: DataAnalyzer
    ):
        self.ingester = ingester
        self.processor = processor
        self.storage = storage
        self.analyzer = analyzer
    
    def run_batch(self, source: str, destination: str):
        """Execute batch pipeline."""
        print(f"Ingesting from {source}")
        raw_data = self.ingester.ingest(source)
        print(f"Ingested {len(raw_data)} records")
        
        print("Processing data")
        processed_data = self.processor.process(raw_data)
        print(f"Processed {len(processed_data)} records")
        
        print(f"Storing to {destination}")
        self.storage.store(processed_data, destination)
        print("Pipeline complete")
    
    def query(self, sql: str) -> List[Dict]:
        """Query stored data."""
        return self.analyzer.analyze(sql)
```

## Key Takeaways

- Big Data ecosystems have five key components: ingestion, storage, processing, analytics, and visualization
- Ingestion handles both batch and streaming data from various sources
- Storage includes data lakes (raw), warehouses (processed), and databases (operational)
- Processing transforms data through batch or stream paradigms
- Analytics extracts insights using SQL, ML, and statistical tools
- Visualization presents findings to stakeholders via BI tools and dashboards
- Components must integrate seamlessly for an effective data platform

## Resources

- Apache Spark: <https://spark.apache.org/>
- Apache Kafka: <https://kafka.apache.org/>
- dbt Documentation: <https://docs.getdbt.com/>
- Modern Data Stack: <https://moderndatastack.xyz/>
