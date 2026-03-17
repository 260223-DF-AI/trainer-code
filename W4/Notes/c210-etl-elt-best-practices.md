# ETL/ELT Best Practices

## Learning Objectives

- Apply ETL/ELT design best practices
- Build reliable, maintainable pipelines
- Optimize for performance and cost
- Follow industry standards

## Why This Matters

Following best practices ensures your pipelines are reliable, maintainable, and scalable. These guidelines come from real-world experience and help you avoid common pitfalls.

## Concept Explanation

### Design Principles

| Principle | Description |
|-----------|-------------|
| Idempotency | Same input produces same output |
| Atomicity | All or nothing execution |
| Modularity | Small, focused tasks |
| Observability | Full visibility into execution |
| Documentation | Clear, up-to-date docs |

### Idempotent Pipelines

```python
def idempotent_load(data, table, partition_date):
    """Safe to run multiple times."""
    # Delete existing data for this partition
    delete_partition(table, partition_date)
    
    # Insert new data
    insert_data(data, table)
    
# Each run produces the same result
```

### Error Handling

```python
def robust_task(func):
    """Decorator for robust error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RecoverableError as e:
            log_warning(f"Recoverable error: {e}")
            raise  # Let orchestrator retry
        except Exception as e:
            log_error(f"Fatal error: {e}")
            alert_team(e)
            raise
    return wrapper

@robust_task
def process_data():
    # Your logic here
    pass
```

### Configuration Management

```python
# config.yaml
pipelines:
  sales:
    source: "postgres://db/sales"
    target: "bigquery://project.dataset.sales"
    schedule: "0 2 * * *"
    
# Load config
import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)
```

### Testing Pipelines

| Test Type | What to Test |
|-----------|--------------|
| Unit | Individual functions |
| Integration | Component connections |
| Data | Transformations produce expected output |
| End-to-end | Full pipeline with sample data |

```python
def test_transformation():
    input_data = pd.DataFrame({'amount': [100, 200]})
    result = transform(input_data)
    
    assert 'total' in result.columns
    assert result['total'].sum() == 300
```

### Performance Optimization

1. **Partition large tables**: Reduce scan costs
2. **Incremental loads**: Process only new data
3. **Parallel execution**: Run independent tasks concurrently
4. **Efficient SQL**: Avoid SELECT *, use WHERE
5. **Compression**: Store data compressed

### Checklist

- [ ] Pipelines are idempotent
- [ ] Error handling with retries
- [ ] Logging at each stage
- [ ] Alerting for failures
- [ ] Documentation current
- [ ] Tests cover key logic
- [ ] Incremental where possible
- [ ] Data quality checks included
- [ ] Monitoring dashboard exists
- [ ] Recovery procedures documented

### Common Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Hardcoded values | Use configuration |
| Silent failures | Log and alert |
| No retries | Implement retry logic |
| Monolithic tasks | Break into smaller tasks |
| No testing | Test all transformations |

## Key Takeaways

- Make pipelines idempotent for safe reruns
- Handle errors gracefully with retries and alerts
- Use configuration files, not hardcoded values
- Test transformations and full pipelines
- Document everything including recovery procedures
- Monitor and alert on key metrics

## Resources

- The Data Engineering Cookbook: <https://github.com/andkret/Cookbook>
