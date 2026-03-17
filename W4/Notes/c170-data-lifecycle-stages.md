# Data Lifecycle Stages

## Learning Objectives

- Understand the complete data lifecycle from creation to deletion
- Learn what happens at each stage of data management
- Recognize roles and responsibilities for each stage
- Identify tools and processes for lifecycle management

## Why This Matters

Data flows through distinct stages, each with different requirements and challenges. Understanding the data lifecycle helps you design systems that properly handle data at every stage, ensure compliance, optimize costs, and maintain data quality throughout its useful life.

## Concept Explanation

### The Data Lifecycle

Data moves through predictable stages from creation to retirement:

```
+----------+     +----------+     +-----------+
|  Create  |---->| Ingest   |---->| Store     |
+----------+     +----------+     +-----------+
                                       |
                                       v
+----------+     +----------+     +-----------+
| Archive  |<----| Analyze  |<----| Process   |
+----------+     +----------+     +-----------+
     |
     v
+----------+
| Destroy  |
+----------+
```

### Stage 1: Data Creation/Collection

Where data originates.

**Sources:**

- **Generated**: IoT sensors, logs, transactions
- **Created**: User input, documents, content
- **Acquired**: Third-party data, APIs
- **Derived**: Calculated from existing data

**Considerations:**

- Define data ownership
- Establish quality at source
- Document metadata
- Ensure consent where required

### Stage 2: Ingestion

Bringing data into your systems.

**Methods:**

| Method | Use Case | Tools |
|--------|----------|-------|
| Batch | Large files, periodic | Airflow, Glue |
| Streaming | Real-time events | Kafka, Pub/Sub |
| API | Third-party sources | Custom, Fivetran |
| CDC | Database replication | Debezium, DMS |

**Considerations:**

- Validate on ingestion
- Handle errors gracefully
- Maintain ordering (if needed)
- Apply initial transformations

### Stage 3: Storage

Persisting data for future use.

**Storage Tiers:**

```
+---------------+     Access Frequency     +---------------+
|     Hot       |  <-- High access    -->  |  Operational  |
+---------------+                          +---------------+

+---------------+     Access Frequency     +---------------+
|     Warm      |  <-- Medium access  -->  |  Analytics    |
+---------------+                          +---------------+

+---------------+     Access Frequency     +---------------+
|     Cold      |  <-- Low access     -->  |  Compliance   |
+---------------+                          +---------------+

+---------------+     Access Frequency     +---------------+
|    Archive    |  <-- Rare access    -->  |  Legal hold   |
+---------------+                          +---------------+
```

**Considerations:**

- Choose appropriate storage class
- Implement lifecycle policies
- Enable redundancy/backup
- Control access

### Stage 4: Processing/Transformation

Making data useful through transformation.

**Common Transformations:**

- Cleaning (remove nulls, fix errors)
- Standardizing (consistent formats)
- Enriching (add derived fields)
- Aggregating (summarize)
- Joining (combine sources)

**Processing Patterns:**

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| ELT | Load raw, transform in warehouse | Modern cloud |
| ETL | Transform before loading | Legacy systems |
| Streaming | Transform in flight | Real-time needs |

### Stage 5: Analysis/Consumption

Extracting value from processed data.

**Consumers:**

- Business intelligence dashboards
- Machine learning models
- Reporting systems
- APIs and applications
- Data scientists (ad-hoc analysis)

**Considerations:**

- Ensure data is discoverable
- Provide self-service access
- Monitor query performance
- Track data lineage

### Stage 6: Archive

Long-term storage for infrequently accessed data.

**Triggers for Archiving:**

- Age-based (data older than X years)
- Access-based (no queries in X months)
- Event-based (project completion)
- Compliance-based (retention requirements)

**Archive Options:**

| Cloud | Service | Retrieval Time |
|-------|---------|----------------|
| GCP | Archive class | Minutes-Hours |
| AWS | Glacier Deep Archive | 12-48 hours |
| Azure | Archive tier | Hours |

### Stage 7: Destruction

Permanently removing data.

**Triggers:**

- Retention period expired
- User request (GDPR right to erasure)
- Legal obligation lifted
- Storage optimization

**Requirements:**

- Verify no legal holds
- Confirm compliance with retention policies
- Log destruction for audit
- Ensure complete removal (all copies)

### Lifecycle Automation

Automating lifecycle transitions:

```
Data Created
    |
    v
[0-30 days: Hot Storage] ----+
                             |
    +------------------------+
    |
    v
[30-90 days: Warm Storage] --+
                             |
    +------------------------+
    |
    v
[90-365 days: Cold Storage] -+
                             |
    +------------------------+
    |
    v
[1-7 years: Archive] --------+
                             |
    +------------------------+
    |
    v
[After retention: Delete]
```

## Code Example

Implementing lifecycle management:

```python
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class StorageClass(Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    ARCHIVE = "archive"

class LifecycleAction(Enum):
    TRANSITION = "transition"
    DELETE = "delete"
    ARCHIVE = "archive"

@dataclass
class LifecycleRule:
    name: str
    age_days: int
    action: LifecycleAction
    target_class: Optional[StorageClass] = None

@dataclass
class DataObject:
    key: str
    created_at: datetime
    last_accessed: datetime
    storage_class: StorageClass
    size_bytes: int

class LifecycleManager:
    """Manage data lifecycle transitions."""
    
    def __init__(self):
        self.rules: List[LifecycleRule] = []
    
    def add_rule(self, rule: LifecycleRule):
        self.rules.append(rule)
    
    def evaluate(self, obj: DataObject) -> List[LifecycleAction]:
        """Determine which actions apply to an object."""
        actions = []
        age_days = (datetime.now() - obj.created_at).days
        
        for rule in self.rules:
            if age_days >= rule.age_days:
                actions.append(rule)
        
        return actions
    
    def apply_lifecycle_rules(self, objects: List[DataObject]) -> dict:
        """Apply lifecycle rules to a list of objects."""
        results = {
            "transitioned": [],
            "deleted": [],
            "unchanged": []
        }
        
        for obj in objects:
            applicable_rules = self.evaluate(obj)
            
            if not applicable_rules:
                results["unchanged"].append(obj.key)
                continue
            
            # Apply the most recent (highest age) rule
            applicable_rules.sort(key=lambda r: r.age_days, reverse=True)
            rule = applicable_rules[0]
            
            if rule.action == LifecycleAction.DELETE:
                self._delete_object(obj)
                results["deleted"].append(obj.key)
            elif rule.action == LifecycleAction.TRANSITION:
                if obj.storage_class != rule.target_class:
                    self._transition_object(obj, rule.target_class)
                    results["transitioned"].append({
                        "key": obj.key,
                        "from": obj.storage_class.value,
                        "to": rule.target_class.value
                    })
                else:
                    results["unchanged"].append(obj.key)
        
        return results
    
    def _transition_object(self, obj: DataObject, target: StorageClass):
        """Transition object to new storage class."""
        print(f"Transitioning {obj.key} from {obj.storage_class.value} to {target.value}")
        # API call to change storage class
        obj.storage_class = target
    
    def _delete_object(self, obj: DataObject):
        """Delete object after retention period."""
        print(f"Deleting {obj.key} (created {obj.created_at})")
        # API call to delete object


# Configure lifecycle rules
manager = LifecycleManager()

manager.add_rule(LifecycleRule(
    name="Move to warm after 30 days",
    age_days=30,
    action=LifecycleAction.TRANSITION,
    target_class=StorageClass.WARM
))

manager.add_rule(LifecycleRule(
    name="Move to cold after 90 days",
    age_days=90,
    action=LifecycleAction.TRANSITION,
    target_class=StorageClass.COLD
))

manager.add_rule(LifecycleRule(
    name="Archive after 1 year",
    age_days=365,
    action=LifecycleAction.TRANSITION,
    target_class=StorageClass.ARCHIVE
))

manager.add_rule(LifecycleRule(
    name="Delete after 7 years",
    age_days=2555,  # ~7 years
    action=LifecycleAction.DELETE
))


# Example GCS lifecycle configuration (JSON)
gcs_lifecycle_config = {
    "lifecycle": {
        "rule": [
            {
                "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
                "condition": {"age": 30}
            },
            {
                "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
                "condition": {"age": 90}
            },
            {
                "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
                "condition": {"age": 365}
            },
            {
                "action": {"type": "Delete"},
                "condition": {"age": 2555}
            }
        ]
    }
}
```

## Key Takeaways

- Data moves through creation, ingestion, storage, processing, analysis, archive, and destruction
- Each stage has specific requirements, tools, and considerations
- Lifecycle policies automate transitions between storage tiers
- Archive storage significantly reduces costs for infrequently accessed data
- Proper data destruction is required for compliance and cost optimization
- Automation reduces operational burden and ensures consistent application of policies

## Resources

- GCP Storage Classes: <https://cloud.google.com/storage/docs/storage-classes>
- AWS S3 Lifecycle: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- Data Lifecycle Management: <https://www.dama.org/cpages/body-of-knowledge>
