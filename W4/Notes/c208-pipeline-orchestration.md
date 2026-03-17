# Pipeline Orchestration

## Learning Objectives

- Understand pipeline orchestration concepts
- Learn DAG-based workflow management
- Apply scheduling and dependency handling
- Compare orchestration tools

## Why This Matters

Orchestration coordinates the execution of pipeline tasks, managing dependencies, schedules, and failures. It transforms individual scripts into reliable, production-ready workflows.

## Concept Explanation

### What is Orchestration?

Orchestration manages the execution of tasks in a workflow:

```
DAG: Daily Sales Pipeline

  extract_orders --> transform_orders --+
                                        |
  extract_products --> transform_prods --+--> load_warehouse --> send_report
                                        |
  extract_customers --> transform_cust -+
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| DAG | Directed Acyclic Graph of tasks |
| Task | Single unit of work |
| Dependency | Task B runs after Task A |
| Schedule | When pipeline runs |
| Trigger | What starts the pipeline |

### Common Orchestration Tools

| Tool | Type | Best For |
|------|------|----------|
| Apache Airflow | Open-source | Complex workflows |
| Prefect | Open-source | Python-native |
| Dagster | Open-source | Data assets |
| Cloud Composer | GCP managed | GCP ecosystem |
| Cloud Workflows | GCP | Simple workflows |

### Airflow Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_sales_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    extract = PythonOperator(
        task_id='extract_sales',
        python_callable=extract_sales_data,
    )
    
    transform = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales_data,
    )
    
    load = PythonOperator(
        task_id='load_warehouse',
        python_callable=load_to_warehouse,
    )
    
    # Define dependencies
    extract >> transform >> load
```

### Scheduling Patterns

```python
# Cron expressions
schedule_interval='0 2 * * *'     # Daily at 2 AM
schedule_interval='0 */4 * * *'   # Every 4 hours
schedule_interval='0 0 * * 0'     # Weekly on Sunday
schedule_interval='0 0 1 * *'     # Monthly on 1st
```

### Error Handling

```python
with DAG('pipeline', ...) as dag:
    
    task = PythonOperator(
        task_id='risky_task',
        python_callable=risky_function,
        retries=3,
        retry_delay=timedelta(minutes=5),
        on_failure_callback=alert_on_failure,
    )
    
def alert_on_failure(context):
    """Send alert when task fails."""
    task_id = context['task_instance'].task_id
    send_alert(f"Task {task_id} failed")
```

### Best Practices

1. **Idempotent tasks**: Can rerun safely
2. **Atomic tasks**: Do one thing well
3. **Clear dependencies**: Explicit task ordering
4. **Meaningful names**: Self-documenting DAGs
5. **Failure alerts**: Know when things break

## Code Example

```python
from datetime import datetime

class SimplePipelineOrchestrator:
    """Basic orchestration pattern."""
    
    def __init__(self):
        self.tasks = []
        self.results = {}
    
    def add_task(self, name, func, depends_on=None):
        self.tasks.append({
            'name': name,
            'func': func,
            'depends_on': depends_on or []
        })
    
    def run(self):
        completed = set()
        
        while len(completed) < len(self.tasks):
            for task in self.tasks:
                if task['name'] in completed:
                    continue
                
                # Check dependencies
                deps_met = all(d in completed for d in task['depends_on'])
                if not deps_met:
                    continue
                
                # Execute task
                print(f"Running: {task['name']}")
                self.results[task['name']] = task['func']()
                completed.add(task['name'])
        
        return self.results

# Usage
pipeline = SimplePipelineOrchestrator()
pipeline.add_task('extract', extract_data)
pipeline.add_task('transform', transform_data, depends_on=['extract'])
pipeline.add_task('load', load_data, depends_on=['transform'])
pipeline.run()
```

## Key Takeaways

- Orchestration manages task execution, dependencies, and schedules
- DAGs define task relationships without cycles
- Airflow is the most popular open-source orchestrator
- Handle failures with retries and alerts
- Make tasks idempotent for reliable reruns

## Resources

- Apache Airflow: <https://airflow.apache.org/>
