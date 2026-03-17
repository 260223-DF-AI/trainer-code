# Cloud Pricing Models

## Learning Objectives

- Understand pay-as-you-go and consumption-based pricing
- Learn about reserved capacity and commitment discounts
- Explore spot/preemptible instance pricing
- Develop cost optimization strategies for cloud workloads

## Why This Matters

Cloud pricing is complex and can lead to unexpected costs if not properly understood. Data workloads, with their variable compute needs and large storage requirements, are particularly sensitive to pricing choices. Understanding pricing models enables you to architect cost-effective solutions and avoid bill shock.

## Concept Explanation

### Pricing Fundamentals

Cloud providers charge for resources based on consumption. The three main pricing dimensions are:

1. **Compute**: CPU time, memory, GPU usage
2. **Storage**: Data at rest, by storage class
3. **Network**: Data transfer, especially egress

### Pay-As-You-Go (On-Demand)

The default pricing model with no upfront commitment.

**Characteristics:**

- Billed per second, minute, or hour
- No minimum commitment
- Full flexibility to scale up/down
- Highest per-unit cost

**Best For:**

- Variable workloads
- Development and testing
- Short-term projects
- Unpredictable demand

**Example Pricing (approximate):**

| Instance Type | AWS | GCP | Azure |
|--------------|-----|-----|-------|
| 4 vCPU, 16 GB | $0.17/hr | $0.15/hr | $0.17/hr |
| 8 vCPU, 32 GB | $0.34/hr | $0.30/hr | $0.34/hr |

### Reserved Capacity

Commit to usage for 1-3 years in exchange for significant discounts.

**AWS Reserved Instances:**

- 1-year: ~30-40% savings
- 3-year: ~50-60% savings
- Payment options: All upfront, partial, no upfront

**GCP Committed Use Discounts:**

- 1-year: ~37% savings
- 3-year: ~55% savings
- Flexible across machine types in same region

**Azure Reserved Instances:**

- 1-year: ~30-40% savings
- 3-year: ~50-60% savings
- Exchangeable within same region

**Best For:**

- Steady-state production workloads
- Predictable capacity needs
- Long-running databases and applications

### Spot/Preemptible Instances

Excess capacity at steep discounts, but can be terminated with short notice.

| Provider | Name | Savings | Notice Time |
|----------|------|---------|-------------|
| AWS | Spot Instances | Up to 90% | 2 minutes |
| GCP | Preemptible VMs | Up to 80% | 30 seconds |
| GCP | Spot VMs | Up to 91% | 30 seconds |
| Azure | Spot VMs | Up to 90% | 30 seconds |

**Best For:**

- Fault-tolerant workloads
- Batch processing
- CI/CD pipelines
- Data processing with checkpointing

### Storage Pricing

Storage costs vary by class and access frequency:

**GCP Cloud Storage:**

| Class | Price/GB/Month | Min Duration | Use Case |
|-------|---------------|--------------|----------|
| Standard | $0.020 | None | Frequent access |
| Nearline | $0.010 | 30 days | Monthly access |
| Coldline | $0.004 | 90 days | Quarterly access |
| Archive | $0.0012 | 365 days | Yearly access |

**Additional Costs:**

- Operations (reads, writes, lists)
- Data retrieval (for cold storage)
- Early deletion fees

### Network/Data Transfer Pricing

**Egress Costs (data leaving cloud):**

- First 1 GB/month: Free
- 1 GB - 1 TB: ~$0.12/GB
- 1 TB - 10 TB: ~$0.11/GB
- 10+ TB: Volume discounts available

**Key Points:**

- Ingress (data into cloud) is typically free
- Same-region transfer is often free
- Cross-region transfer incurs charges
- Internet egress is the most expensive

### Data Warehouse Pricing

BigQuery example (on-demand):

- Storage: $0.02/GB/month (active), $0.01/GB/month (long-term)
- Queries: $5 per TB scanned
- Streaming inserts: $0.01 per 200 MB

BigQuery Slots (capacity pricing):

- Fixed compute capacity
- $0.04/slot-hour (on-demand)
- Flat-rate: $2,000/month for 100 slots

### Cost Optimization Strategies

#### 1. Right-Sizing

Match instance size to actual workload needs:

```python
# Analyze resource utilization
def recommend_instance_size(current_type: str, avg_cpu: float, avg_memory: float):
    if avg_cpu < 20 and avg_memory < 30:
        return "Downsize by 50%"
    elif avg_cpu < 40 and avg_memory < 50:
        return "Downsize by 25%"
    elif avg_cpu > 80 or avg_memory > 80:
        return "Upsize by 25%"
    else:
        return "Current size appropriate"
```

#### 2. Auto-Scaling

Scale resources based on demand:

```yaml
# Kubernetes HPA for data processing
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-processor
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

#### 3. Lifecycle Policies

Automate storage class transitions:

```python
from google.cloud import storage

def set_lifecycle_rules(bucket_name: str):
    """Configure automatic storage class transitions."""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    
    bucket.lifecycle_rules = [
        {
            "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
            "condition": {"age": 30, "matchesStorageClass": ["STANDARD"]}
        },
        {
            "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
            "condition": {"age": 90, "matchesStorageClass": ["NEARLINE"]}
        },
        {
            "action": {"type": "Delete"},
            "condition": {"age": 365}
        }
    ]
    
    bucket.patch()
    print(f"Lifecycle rules applied to {bucket_name}")
```

## Code Example

Building a cost estimation tool:

```python
from dataclasses import dataclass
from typing import List

@dataclass
class CloudResource:
    name: str
    resource_type: str
    region: str
    hours_per_month: float
    
class CostEstimator:
    """Estimate cloud costs for data workloads."""
    
    # GCP pricing (approximate)
    PRICING = {
        "compute": {
            "n2-standard-4": 0.194,
            "n2-standard-8": 0.388,
            "n2-highmem-4": 0.262,
        },
        "storage": {
            "standard": 0.020,
            "nearline": 0.010,
            "coldline": 0.004,
        },
        "bigquery": {
            "query_per_tb": 5.00,
            "storage_active": 0.020,
            "storage_longterm": 0.010,
        }
    }
    
    def estimate_compute(self, instance_type: str, hours: float, 
                         use_preemptible: bool = False) -> float:
        """Estimate compute costs."""
        base_rate = self.PRICING["compute"].get(instance_type, 0.20)
        
        if use_preemptible:
            base_rate *= 0.20  # 80% discount
        
        return base_rate * hours
    
    def estimate_storage(self, gb: float, storage_class: str = "standard") -> float:
        """Estimate monthly storage costs."""
        rate = self.PRICING["storage"].get(storage_class, 0.020)
        return gb * rate
    
    def estimate_bigquery(self, storage_gb: float, query_tb_per_month: float) -> dict:
        """Estimate BigQuery costs."""
        storage_cost = storage_gb * self.PRICING["bigquery"]["storage_active"]
        query_cost = query_tb_per_month * self.PRICING["bigquery"]["query_per_tb"]
        
        return {
            "storage": storage_cost,
            "queries": query_cost,
            "total": storage_cost + query_cost
        }
    
    def compare_pricing_options(self, instance_type: str, 
                                 hours_per_month: float) -> dict:
        """Compare on-demand, reserved, and preemptible pricing."""
        base = self.PRICING["compute"].get(instance_type, 0.20)
        monthly_hours = hours_per_month
        
        return {
            "on_demand": base * monthly_hours,
            "1yr_reserved": base * monthly_hours * 0.63,
            "3yr_reserved": base * monthly_hours * 0.45,
            "preemptible": base * monthly_hours * 0.20,
            "recommendation": self._get_recommendation(monthly_hours)
        }
    
    def _get_recommendation(self, monthly_hours: float) -> str:
        if monthly_hours >= 720:  # 24/7 usage
            return "Consider 3-year reserved for maximum savings"
        elif monthly_hours >= 400:
            return "Consider 1-year reserved"
        elif monthly_hours < 200:
            return "On-demand or preemptible recommended"
        else:
            return "Evaluate based on workload predictability"


# Usage example
estimator = CostEstimator()

# Data pipeline cost estimate
pipeline_costs = {
    "compute": estimator.estimate_compute("n2-standard-8", 200, use_preemptible=True),
    "storage": estimator.estimate_storage(500, "standard"),
    "bigquery": estimator.estimate_bigquery(100, 2.0)
}

print(f"Monthly pipeline costs: ${sum([pipeline_costs['compute'], pipeline_costs['storage'], pipeline_costs['bigquery']['total']]):.2f}")
```

## Key Takeaways

- Pay-as-you-go offers flexibility but highest unit costs
- Reserved instances provide 30-60% savings for predictable workloads
- Spot/preemptible instances offer up to 90% savings for fault-tolerant jobs
- Storage class selection significantly impacts costs for large datasets
- Network egress is often overlooked but can be a major cost driver
- Regular right-sizing and lifecycle policies are essential for cost control

## Resources

- GCP Pricing Calculator: <https://cloud.google.com/products/calculator>
- AWS Pricing Calculator: <https://calculator.aws/>
- Azure Pricing Calculator: <https://azure.microsoft.com/en-us/pricing/calculator/>
- FinOps Best Practices: <https://www.finops.org/framework/>
