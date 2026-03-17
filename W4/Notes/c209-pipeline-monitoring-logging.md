# Pipeline Monitoring and Logging

## Learning Objectives

- Implement effective pipeline logging
- Monitor pipeline health and performance
- Set up alerting for failures
- Track data lineage and metrics

## Why This Matters

Monitoring and logging are essential for maintaining reliable pipelines. They help you detect issues quickly, debug problems, and optimize performance.

## Concept Explanation

### Monitoring Levels

| Level | What to Monitor |
|-------|-----------------|
| Infrastructure | CPU, memory, disk |
| Pipeline | Run status, duration |
| Data | Row counts, quality |
| Business | SLA compliance |

### Structured Logging

```python
import logging
import json
from datetime import datetime

class PipelineLogger:
    """Structured logging for pipelines."""
    
    def __init__(self, pipeline_name):
        self.pipeline = pipeline_name
        self.logger = logging.getLogger(pipeline_name)
    
    def log(self, event, **context):
        message = {
            'timestamp': datetime.utcnow().isoformat(),
            'pipeline': self.pipeline,
            'event': event,
            **context
        }
        self.logger.info(json.dumps(message))
    
    def log_task_start(self, task_name):
        self.log('task_start', task=task_name)
    
    def log_task_complete(self, task_name, rows, duration):
        self.log('task_complete', 
                 task=task_name, 
                 rows_processed=rows,
                 duration_seconds=duration)
    
    def log_error(self, task_name, error):
        self.log('task_error', task=task_name, error=str(error))

# Usage
logger = PipelineLogger('daily_sales')
logger.log_task_start('extract')
logger.log_task_complete('extract', rows=10000, duration=45.2)
```

### Key Metrics to Track

```python
class PipelineMetrics:
    """Track pipeline performance metrics."""
    
    def __init__(self):
        self.metrics = {}
    
    def record(self, metric, value, tags=None):
        self.metrics[metric] = {
            'value': value,
            'tags': tags or {},
            'timestamp': datetime.utcnow()
        }
    
    def get_summary(self):
        return self.metrics

# Key metrics
metrics = PipelineMetrics()
metrics.record('rows_extracted', 50000, {'source': 'orders'})
metrics.record('rows_loaded', 49850, {'table': 'fact_sales'})
metrics.record('duration_seconds', 120)
metrics.record('data_freshness_hours', 2)
```

### Alerting Rules

| Condition | Alert Level |
|-----------|-------------|
| Pipeline failed | Critical |
| Duration > 2x normal | Warning |
| Row count = 0 | Critical |
| Row count < 50% normal | Warning |
| Data quality < threshold | Critical |

### Simple Alert Implementation

```python
class AlertManager:
    """Simple alerting for pipelines."""
    
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def check(self, metric, value):
        threshold = self.thresholds.get(metric)
        if threshold and value > threshold:
            self.send_alert(f"{metric} exceeded threshold: {value}")
    
    def send_alert(self, message):
        print(f"ALERT: {message}")
        # In production: send email, Slack, PagerDuty

# Usage
alerts = AlertManager({
    'duration_seconds': 300,
    'error_count': 0
})
alerts.check('duration_seconds', 450)  # Would alert
```

### Pipeline Dashboard Metrics

```sql
-- Query for pipeline monitoring dashboard
SELECT 
    pipeline_name,
    run_date,
    status,
    duration_seconds,
    rows_processed,
    error_message
FROM pipeline_runs
WHERE run_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
ORDER BY run_date DESC;
```

## Key Takeaways

- Use structured logging for searchability
- Track key metrics: duration, row counts, status
- Set up alerts for failures and anomalies
- Monitor at multiple levels: infra, pipeline, data
- Build dashboards for visibility

## Resources

- Datadog: <https://www.datadoghq.com/>
- Prometheus: <https://prometheus.io/>
