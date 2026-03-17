# Infrastructure as a Service Deep Dive

## Learning Objectives

- Understand the core components of IaaS: compute, storage, and networking
- Learn how virtual machines and containers work in cloud environments
- Explore storage options: block, object, and file storage
- Understand cloud networking concepts: VPCs, subnets, and load balancers

## Why This Matters

IaaS forms the foundation of cloud computing. Even when using higher-level services like data warehouses or managed databases, understanding the underlying infrastructure helps you optimize performance, control costs, and troubleshoot issues. Data engineers frequently work with IaaS components when building custom data pipelines or deploying specialized processing tools.

## Concept Explanation

### Core IaaS Components

IaaS provides three fundamental building blocks:

1. **Compute** - Processing power (virtual machines, containers)
2. **Storage** - Data persistence (block, object, file)
3. **Networking** - Connectivity (VPCs, load balancers, CDNs)

### Compute Services

#### Virtual Machines (VMs)

VMs are virtualized computers running on physical hardware. You choose the operating system, CPU, memory, and disk configuration.

| Provider | Service Name | Key Features |
|----------|-------------|--------------|
| AWS | EC2 | Widest instance variety |
| GCP | Compute Engine | Per-second billing |
| Azure | Virtual Machines | Strong Windows integration |

**Instance Types:**

- **General Purpose**: Balanced CPU/memory (web servers, dev environments)
- **Compute Optimized**: High CPU (batch processing, modeling)
- **Memory Optimized**: High RAM (in-memory databases, caching)
- **Storage Optimized**: High I/O (data warehousing, distributed file systems)
- **GPU Instances**: Graphics processing (ML training, rendering)

#### Containers and Orchestration

Containers package applications with their dependencies for consistent deployment:

- **Container Registries**: Store container images (Docker Hub, GCR, ECR)
- **Container Orchestration**: Manage container deployment (Kubernetes, ECS)
- **Managed Kubernetes**: Provider-managed K8s (GKE, EKS, AKS)

### Storage Services

#### Block Storage

Works like a hard drive attached to a VM. Data is stored in fixed-size blocks.

- Low latency, high performance
- Must be attached to a compute instance
- Supports snapshots for backup
- Examples: AWS EBS, GCP Persistent Disk, Azure Managed Disks

#### Object Storage

Stores data as objects with metadata. Ideal for unstructured data at scale.

- Virtually unlimited scalability
- Accessible via HTTP/API
- Built-in redundancy and durability
- Examples: AWS S3, GCP Cloud Storage, Azure Blob Storage

**Storage Classes:**

| Class | Use Case | Cost | Access Time |
|-------|----------|------|-------------|
| Standard | Frequent access | High | Milliseconds |
| Nearline/IA | Monthly access | Medium | Milliseconds |
| Coldline/Glacier | Yearly access | Low | Minutes-Hours |
| Archive | Rarely accessed | Lowest | Hours |

#### File Storage

Traditional file system accessible by multiple compute instances.

- Shared access across VMs
- Supports standard protocols (NFS, SMB)
- Examples: AWS EFS, GCP Filestore, Azure Files

### Networking

#### Virtual Private Cloud (VPC)

A logically isolated network within the cloud where you deploy resources.

**Components:**

- **Subnets**: Subdivide your VPC by region/zone
- **Route Tables**: Control traffic flow between subnets
- **Internet Gateway**: Enable public internet access
- **NAT Gateway**: Allow private resources to reach internet
- **Security Groups/Firewall Rules**: Control inbound/outbound traffic

#### Load Balancing

Distributes incoming traffic across multiple instances:

- **Layer 4 (TCP/UDP)**: Network-level, fastest
- **Layer 7 (HTTP/HTTPS)**: Application-level, content-aware routing
- **Global vs Regional**: Cross-region or single-region distribution

## Code Example

Provisioning IaaS resources using Infrastructure as Code (Terraform):

```hcl
# main.tf - Terraform configuration for GCP infrastructure

# Configure the Google Cloud provider
provider "google" {
  project = "my-data-project"
  region  = "us-central1"
}

# Create a VPC network
resource "google_compute_network" "data_network" {
  name                    = "data-pipeline-network"
  auto_create_subnetworks = false
}

# Create a subnet
resource "google_compute_subnetwork" "data_subnet" {
  name          = "data-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.data_network.id
}

# Create a compute instance for data processing
resource "google_compute_instance" "data_processor" {
  name         = "data-processor-vm"
  machine_type = "e2-standard-4"  # 4 vCPUs, 16 GB RAM
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100  # GB
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.data_subnet.id
    access_config {}  # Assigns external IP
  }

  metadata_startup_script = <<-EOF
    apt-get update
    apt-get install -y python3-pip
    pip3 install pandas numpy
  EOF
}

# Create a Cloud Storage bucket
resource "google_storage_bucket" "data_lake" {
  name     = "my-project-data-lake"
  location = "US"
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}
```

Python interaction with IaaS resources:

```python
from google.cloud import storage, compute_v1

# Object Storage: Upload data to Cloud Storage
def upload_to_gcs(bucket_name: str, source_file: str, destination: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination)
    blob.upload_from_filename(source_file)
    print(f"Uploaded to gs://{bucket_name}/{destination}")

# Compute: List running instances
def list_instances(project: str, zone: str):
    client = compute_v1.InstancesClient()
    instances = client.list(project=project, zone=zone)
    
    for instance in instances:
        print(f"Name: {instance.name}")
        print(f"  Status: {instance.status}")
        print(f"  Machine Type: {instance.machine_type.split('/')[-1]}")
```

## Key Takeaways

- IaaS provides compute, storage, and networking as building blocks
- Virtual machines offer flexibility; containers provide portability and efficiency
- Storage types serve different needs: block for VMs, object for data lakes, file for shared access
- VPCs provide network isolation and security through firewalls and subnets
- Infrastructure as Code enables reproducible, version-controlled deployments

## Resources

- AWS EC2 Documentation: <https://docs.aws.amazon.com/ec2/>
- GCP Compute Engine: <https://cloud.google.com/compute/docs>
- Azure VMs: <https://docs.microsoft.com/en-us/azure/virtual-machines/>
- Terraform Documentation: <https://www.terraform.io/docs>
