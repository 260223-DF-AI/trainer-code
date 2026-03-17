# Azure Data Services

## Learning Objectives

- Understand the Azure data services ecosystem
- Learn about Azure storage options: Blob Storage, Data Lake Storage
- Explore Azure Synapse Analytics and data integration services
- Recognize Azure's unique strengths in enterprise integration

## Why This Matters

Microsoft Azure is the second-largest cloud provider and is particularly strong in enterprise environments due to Microsoft's existing relationships with large organizations. Azure's data services integrate well with Microsoft tools like Power BI, Excel, and SQL Server. Understanding Azure data services is essential for data professionals working in Microsoft-centric environments.

## Concept Explanation

### Azure Data Services Overview

Azure organizes data services into a cohesive ecosystem:

```
+------------------+     +------------------+     +------------------+
|    Storage       |     |    Analytics     |     |   Integration    |
+------------------+     +------------------+     +------------------+
| Blob Storage     |     | Synapse Analytics|     | Data Factory     |
| Data Lake Gen2   |     | HDInsight        |     | Logic Apps       |
| Files            |     | Databricks       |     | Event Grid       |
| Managed Disks    |     | Stream Analytics |     | Service Bus      |
+------------------+     +------------------+     +------------------+
         |                       |                       |
         +------------+----------+-----------+-----------+
                      |                      |
              +-------v-------+      +-------v-------+
              |   Databases   |      |   ML/BI       |
              +---------------+      +---------------+
              | SQL Database  |      | Azure ML      |
              | Cosmos DB     |      | Power BI      |
              | PostgreSQL    |      | Cognitive Svcs|
              | MySQL         |      | Purview       |
              +---------------+      +---------------+
```

### Storage Services

#### Azure Blob Storage

Object storage for unstructured data, similar to AWS S3.

**Access Tiers:**

| Tier | Use Case | Access Latency |
|------|----------|----------------|
| Hot | Frequent access | Milliseconds |
| Cool | Infrequent (30+ days) | Milliseconds |
| Cold | Rarely accessed (90+ days) | Milliseconds |
| Archive | Long-term (180+ days) | Hours |

**Key Features:**

- Hierarchical namespace (optional)
- Blob versioning and soft delete
- Immutable storage for compliance
- Lifecycle management policies
- Integration with Azure CDN

#### Azure Data Lake Storage Gen2

Enterprise data lake built on Blob Storage with hierarchical file system semantics.

**Key Features:**

- HDFS-compatible access
- Fine-grained ACL permissions
- Optimized for analytics workloads
- Native integration with Synapse, Databricks
- Cost-effective with blob pricing

**When to Use:**

- Big data analytics workloads
- Data lake architectures
- Hadoop/Spark workloads
- Need for directory-level permissions

### Analytics Services

#### Azure Synapse Analytics

Unified analytics platform combining data warehousing and big data analytics.

**Components:**

| Component | Purpose |
|-----------|---------|
| Dedicated SQL Pool | Traditional data warehouse |
| Serverless SQL Pool | Query data lake ad-hoc |
| Apache Spark Pool | Big data processing |
| Data Explorer Pool | Log/telemetry analytics |
| Pipelines | Data integration/orchestration |

**Key Features:**

- Unified workspace for all analytics
- Code-free data pipelines
- Direct query of external data (Data Lake, Cosmos DB)
- Power BI integration
- Deep Azure ecosystem integration

#### Azure HDInsight

Managed open-source analytics clusters.

**Supported Frameworks:**

- Apache Hadoop
- Apache Spark
- Apache Hive
- Apache Kafka
- Apache HBase

#### Azure Databricks

Premium Apache Spark platform with enhanced features.

**Advantages:**

- Collaborative notebooks
- MLflow integration
- Delta Lake support
- Unity Catalog for governance
- Optimized Spark runtime

#### Azure Stream Analytics

Real-time stream processing service.

**Features:**

- SQL-based query language
- Windowing functions (tumbling, hopping, sliding)
- Integration with Event Hubs, IoT Hub
- Outputs to multiple destinations
- Built-in machine learning

### Data Integration Services

#### Azure Data Factory

Cloud ETL service for data integration at scale.

**Components:**

- **Linked Services**: Connection to data stores
- **Datasets**: Data structures
- **Pipelines**: Orchestrated activities
- **Data Flows**: Visual ETL transformations
- **Integration Runtime**: Compute for execution

**Key Features:**

- 90+ built-in connectors
- Mapping data flows (code-free ETL)
- Git integration for version control
- Monitoring and alerting
- Hybrid connectivity (on-premises)

### Database Services

#### Azure SQL Database

Fully managed SQL Server in the cloud.

**Deployment Options:**

| Option | Use Case |
|--------|----------|
| Single Database | Isolated databases |
| Elastic Pool | Multiple DBs sharing resources |
| Managed Instance | Near 100% SQL Server compatibility |

**Key Features:**

- Automatic tuning
- Built-in intelligence
- High availability (99.99% SLA)
- Automatic backups
- Geo-replication

#### Azure Cosmos DB

Globally distributed, multi-model NoSQL database.

**APIs Supported:**

- Core (SQL)
- MongoDB
- Cassandra
- Gremlin (Graph)
- Table

**Key Features:**

- Multi-region writes
- Guaranteed single-digit millisecond latency
- 5 consistency levels
- Automatic scaling

### Governance and Catalog

#### Microsoft Purview

Unified data governance service.

**Capabilities:**

- Data catalog and discovery
- Data lineage tracking
- Sensitivity labeling
- Access policies
- Compliance reporting

## Code Example

Working with Azure data services using Python SDKs:

```python
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.synapse.spark import SparkClient
import pandas as pd
from io import BytesIO

class AzureDataServices:
    """Interact with Azure data services."""
    
    def __init__(self, storage_account: str, synapse_workspace: str = None):
        self.credential = DefaultAzureCredential()
        self.storage_account = storage_account
        
        # Blob Storage client
        self.blob_service = BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=self.credential
        )
        
        self.synapse_workspace = synapse_workspace
    
    # Blob Storage Operations
    def upload_dataframe(self, df: pd.DataFrame, container: str, 
                         blob_name: str, format: str = "parquet"):
        """Upload DataFrame to Blob Storage."""
        container_client = self.blob_service.get_container_client(container)
        
        if format == "parquet":
            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            data = buffer.getvalue()
        else:
            data = df.to_csv(index=False).encode()
        
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        
        print(f"Uploaded to https://{self.storage_account}.blob.core.windows.net"
              f"/{container}/{blob_name}")
    
    def download_dataframe(self, container: str, blob_name: str) -> pd.DataFrame:
        """Download blob as DataFrame."""
        blob_client = self.blob_service.get_blob_client(container, blob_name)
        data = blob_client.download_blob().readall()
        
        if blob_name.endswith(".parquet"):
            return pd.read_parquet(BytesIO(data))
        else:
            return pd.read_csv(BytesIO(data))
    
    def list_blobs(self, container: str, prefix: str = None) -> list:
        """List blobs in container."""
        container_client = self.blob_service.get_container_client(container)
        blobs = container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blobs]
    
    def set_blob_tier(self, container: str, blob_name: str, tier: str):
        """Change blob access tier."""
        blob_client = self.blob_service.get_blob_client(container, blob_name)
        blob_client.set_standard_blob_tier(tier)  # Hot, Cool, Cold, Archive
        print(f"Set {blob_name} to {tier} tier")


# Azure Synapse SQL example
import pyodbc

def query_synapse(server: str, database: str, query: str) -> pd.DataFrame:
    """Query Azure Synapse SQL pool."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server}.sql.azuresynapse.net;"
        f"DATABASE={database};"
        "Authentication=ActiveDirectoryInteractive;"
    )
    
    with pyodbc.connect(conn_str) as conn:
        return pd.read_sql(query, conn)


# Azure Data Factory trigger example
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import DefaultAzureCredential

def trigger_adf_pipeline(subscription_id: str, resource_group: str,
                         factory_name: str, pipeline_name: str):
    """Trigger an Azure Data Factory pipeline."""
    credential = DefaultAzureCredential()
    
    adf_client = DataFactoryManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )
    
    run_response = adf_client.pipelines.create_run(
        resource_group_name=resource_group,
        factory_name=factory_name,
        pipeline_name=pipeline_name
    )
    
    return run_response.run_id


# Cosmos DB example
from azure.cosmos import CosmosClient

def query_cosmos(endpoint: str, key: str, database: str, 
                 container: str, query: str) -> list:
    """Query Azure Cosmos DB."""
    client = CosmosClient(endpoint, credential=key)
    db = client.get_database_client(database)
    cont = db.get_container_client(container)
    
    items = list(cont.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    
    return items
```

## Key Takeaways

- Azure Data Lake Storage Gen2 provides enterprise data lake capabilities with HDFS compatibility
- Synapse Analytics unifies data warehousing, big data, and data integration in one workspace
- Data Factory offers robust ETL/ELT with extensive connectors and visual data flows
- Azure excels in enterprise integration, particularly with Microsoft tools (Power BI, Office)
- Cosmos DB provides globally distributed NoSQL with multiple API options
- Purview adds unified governance across the data estate

## Resources

- Azure Data Services Documentation: <https://docs.microsoft.com/en-us/azure/>
- Synapse Analytics: <https://docs.microsoft.com/en-us/azure/synapse-analytics/>
- Azure Data Factory: <https://docs.microsoft.com/en-us/azure/data-factory/>
- Azure Architecture Center: <https://docs.microsoft.com/en-us/azure/architecture/>
