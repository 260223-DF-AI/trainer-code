# Cloud Computing Service Types

## Learning Objectives

- Understand the three primary cloud service models: IaaS, PaaS, SaaS
- Identify what each model provides versus customer responsibilities
- Recognize common examples of each service type
- Determine which service model fits specific use cases

## Why This Matters

Understanding cloud service models helps you make informed decisions about where to invest engineering effort. Choosing between IaaS, PaaS, and SaaS affects development speed, operational overhead, cost structure, and the level of control you have over your infrastructure. For data professionals, this directly impacts how you design and deploy data pipelines, warehouses, and analytics platforms.

## Concept Explanation

### The Cloud Service Stack

Cloud services are categorized based on what the provider manages versus what the customer controls. Think of it as a stack where each layer builds upon the previous:

```
+------------------+
|   Applications   |  <-- SaaS (Provider manages all)
+------------------+
|      Data        |
+------------------+
|     Runtime      |  <-- PaaS (Provider manages platform)
+------------------+
|    Middleware    |
+------------------+
|       O/S        |
+------------------+
|  Virtualization  |  <-- IaaS (Provider manages infrastructure)
+------------------+
|     Servers      |
+------------------+
|     Storage      |
+------------------+
|    Networking    |
+------------------+
```

### Infrastructure as a Service (IaaS)

IaaS provides virtualized computing resources over the internet. You rent IT infrastructure (servers, VMs, storage, networks) on a pay-as-you-go basis.

**Provider Manages:**

- Physical hardware
- Networking infrastructure
- Data centers
- Virtualization layer

**Customer Manages:**

- Operating system
- Middleware and runtime
- Applications
- Data

**Common Examples:**

- Amazon EC2 (virtual machines)
- Google Compute Engine
- Azure Virtual Machines
- AWS S3 (storage)

**Use Cases:**

- Custom application hosting
- Development and test environments
- High-performance computing
- Disaster recovery infrastructure

### Platform as a Service (PaaS)

PaaS provides a platform for developing, running, and managing applications without the complexity of building and maintaining infrastructure.

**Provider Manages:**

- Everything in IaaS, plus:
- Operating system
- Middleware
- Runtime environment

**Customer Manages:**

- Applications
- Data

**Common Examples:**

- Google App Engine
- AWS Elastic Beanstalk
- Azure App Service
- Heroku
- Google Cloud Functions (serverless)

**Use Cases:**

- Rapid application development
- API development and hosting
- Automated scaling applications
- Microservices architectures

### Software as a Service (SaaS)

SaaS delivers complete software applications over the internet, accessible via web browser. The provider manages everything.

**Provider Manages:**

- Everything (infrastructure, platform, application)

**Customer Manages:**

- User configuration
- Data input

**Common Examples:**

- Google Workspace (Gmail, Docs, Sheets)
- Microsoft 365
- Salesforce
- Slack
- Tableau Online

**Use Cases:**

- Email and collaboration
- Customer relationship management
- Business intelligence dashboards
- Productivity applications

### Comparison Matrix

| Aspect | IaaS | PaaS | SaaS |
|--------|------|------|------|
| Control Level | High | Medium | Low |
| Flexibility | Maximum | Moderate | Minimal |
| Management Effort | High | Low | None |
| Development Speed | Slow | Fast | N/A |
| Customization | Unlimited | Limited | Minimal |
| Target Audience | IT Admins | Developers | End Users |
| Scaling | Manual/Scripted | Automatic | Automatic |

### The Shared Responsibility Model

Each service model defines a different boundary of responsibility:

```
                    Customer Responsibility
                    ^
                    |  IaaS: OS, Runtime, Apps, Data
                    |  PaaS: Apps, Data
                    |  SaaS: Data only
                    |
    +---------------+---------------+---------------+
    |     IaaS      |     PaaS      |     SaaS      |
    +---------------+---------------+---------------+
                    |
                    v
                    Provider Responsibility
```

## Code Example

Here is how you might deploy an application on different service models:

```python
# IaaS Approach: Full control, more setup
# You manage the VM, install dependencies, configure everything

# 1. Create VM
# gcloud compute instances create my-vm --machine-type=e2-medium

# 2. SSH and install dependencies
# pip install flask gunicorn

# 3. Deploy and run manually
# gunicorn --bind 0.0.0.0:8080 app:app

# ---

# PaaS Approach: Just deploy your code
# app.yaml for Google App Engine
"""
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

instance_class: F2
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
"""

# Deploy with one command:
# gcloud app deploy

# ---

# SaaS Approach: No code, just configuration
# Example: Using Google Data Studio (now Looker Studio)
# - Connect to data source via UI
# - Build dashboards with drag-and-drop
# - Share via URL
```

## Key Takeaways

- IaaS provides maximum control but requires managing OS and runtime
- PaaS abstracts infrastructure, letting developers focus on code
- SaaS delivers ready-to-use applications with minimal management
- The choice between models depends on control needs versus operational overhead
- Most organizations use a mix of all three service types

## Resources

- Azure Service Models: <https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-iaas-paas-saas/>
- GCP Service Types: <https://cloud.google.com/docs/overview/cloud-platform-services>
- AWS Service Categories: <https://aws.amazon.com/types-of-cloud-computing/>
