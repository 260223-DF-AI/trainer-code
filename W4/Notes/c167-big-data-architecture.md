# Big Data Architecture

## Learning Objectives

- Understand Lambda and Kappa architecture patterns
- Learn the difference between batch and stream processing
- Recognize trade-offs in architectural decisions
- Identify when to use each architecture pattern

## Why This Matters

Choosing the right architecture for processing Big Data impacts system complexity, latency requirements, and maintenance burden. Understanding these patterns helps you design data systems that meet business requirements while remaining manageable and cost-effective.

## Concept Explanation

### The Processing Challenge

Big Data processing must handle two types of requirements:

1. **Historical Analysis**: Processing large volumes of existing data
2. **Real-time Analysis**: Processing data as it arrives

Traditional architectures struggled to do both effectively, leading to specialized patterns.

### Batch vs Stream Processing

| Aspect | Batch Processing | Stream Processing |
|--------|------------------|-------------------|
| Data | Bounded (finite) | Unbounded (infinite) |
| Latency | Minutes to hours | Milliseconds to seconds |
| Throughput | Very high | High |
| Completeness | Complete data | Partial/windowed |
| Complexity | Lower | Higher |
| Use Cases | Reporting, ML training | Alerts, monitoring |

### Lambda Architecture

Proposed by Nathan Marz, Lambda Architecture addresses both batch and real-time needs by maintaining parallel pipelines.

```
                    +----------------+
                    |    Data        |
                    |    Sources     |
                    +-------+--------+
                            |
            +---------------+---------------+
            |                               |
            v                               v
    +---------------+               +---------------+
    |    Batch      |               |    Speed      |
    |    Layer      |               |    Layer      |
    +-------+-------+               +-------+-------+
            |                               |
            v                               v
    +---------------+               +---------------+
    |  Batch Views  |               | Real-time     |
    |  (Complete)   |               | Views (Fast)  |
    +-------+-------+               +-------+-------+
            |                               |
            +---------------+---------------+
                            |
                            v
                    +---------------+
                    |   Serving     |
                    |   Layer       |
                    +---------------+
```

**Three Layers:**

1. **Batch Layer**: Processes all historical data and creates complete views
2. **Speed Layer**: Processes real-time data for low-latency results
3. **Serving Layer**: Merges batch and speed outputs for queries

**Advantages:**

- Handles both batch and real-time requirements
- Fault-tolerant (can recompute from raw data)
- Accurate historical views

**Disadvantages:**

- Dual codebase (batch and stream logic)
- Complex to maintain
- Synchronization challenges

### Kappa Architecture

Proposed by Jay Kreps as a simplification of Lambda, Kappa uses streaming for all processing.

```
                    +----------------+
                    |    Data        |
                    |    Sources     |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |   Streaming    |
                    |   Layer        |
                    |   (Kafka)      |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |   Processing   |
                    |   (Flink/Spark)|
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |   Serving      |
                    |   Layer        |
                    +----------------+
```

**Key Principle**: Treat everything as a stream. Historical data is just older stream events.

**Advantages:**

- Single codebase for all processing
- Simpler to maintain
- Easier to reason about

**Disadvantages:**

- Reprocessing requires replaying events
- May be overkill for simple batch needs
- Requires robust streaming infrastructure

### Architecture Comparison

| Aspect | Lambda | Kappa |
|--------|--------|-------|
| Complexity | Higher | Lower |
| Codebase | Dual | Single |
| Reprocessing | Re-run batch job | Replay stream |
| Latency | Real-time possible | Real-time native |
| Historical accuracy | Strong | Depends on retention |
| Maintenance | More effort | Less effort |

### Modern Approaches

Today, many organizations adopt hybrid approaches:

**Lakehouse Architecture:**
Combines data lake flexibility with warehouse structure.

- Delta Lake, Apache Iceberg
- Single storage layer
- ACID transactions on object storage

**Medallion Architecture:**
Organizes data into quality layers.

- Bronze: Raw ingested data
- Silver: Cleaned, conformed data
- Gold: Aggregated, business-level data

```
Source --> Bronze --> Silver --> Gold --> Analytics
          (Raw)     (Clean)   (Aggregate) (BI/ML)
```

### Choosing an Architecture

Consider these factors:

| Requirement | Recommended Pattern |
|-------------|---------------------|
| Real-time only | Kappa |
| Batch only | Simple ETL |
| Both, simple | Lambda |
| Both, complex | Lakehouse |
| Evolving schema | Data Lake |
| Strong consistency | Data Warehouse |

## Code Example

Illustrating batch vs stream processing patterns:

```python
from datetime import datetime
from typing import Iterator, Dict, List

# Batch Processing Pattern
class BatchProcessor:
    """Process data in complete batches."""
    
    def process_daily_sales(self, date: str) -> Dict:
        """
        Process all sales for a complete day.
        Runs once per day, processes millions of records.
        """
        # Read all data for the day
        sales = self.read_sales_data(date)
        
        # Aggregate
        total_revenue = sum(sale['amount'] for sale in sales)
        order_count = len(sales)
        unique_customers = len(set(sale['customer_id'] for sale in sales))
        
        # Store complete view
        result = {
            'date': date,
            'total_revenue': total_revenue,
            'order_count': order_count,
            'unique_customers': unique_customers,
            'processed_at': datetime.now().isoformat()
        }
        
        self.store_daily_summary(result)
        return result


# Stream Processing Pattern
class StreamProcessor:
    """Process data as it arrives."""
    
    def __init__(self):
        self.running_totals = {}
    
    def process_sale_event(self, event: Dict) -> None:
        """
        Process each sale as it happens.
        Updates running totals in real-time.
        """
        date = event['timestamp'][:10]  # YYYY-MM-DD
        
        if date not in self.running_totals:
            self.running_totals[date] = {
                'total_revenue': 0,
                'order_count': 0,
                'customers': set()
            }
        
        # Update running totals
        self.running_totals[date]['total_revenue'] += event['amount']
        self.running_totals[date]['order_count'] += 1
        self.running_totals[date]['customers'].add(event['customer_id'])
        
        # Emit updated view (for real-time dashboard)
        self.emit_update(date, self.running_totals[date])


# Lambda Architecture Pattern
class LambdaArchitecture:
    """Combine batch and stream processing."""
    
    def __init__(self):
        self.batch_processor = BatchProcessor()
        self.stream_processor = StreamProcessor()
    
    def ingest(self, event: Dict) -> None:
        """
        Ingest into both layers.
        """
        # Send to raw storage for batch processing
        self.store_raw(event)
        
        # Also process in real-time
        self.stream_processor.process_sale_event(event)
    
    def query(self, date: str) -> Dict:
        """
        Merge batch and speed views for queries.
        """
        # Try to get from batch layer (complete, accurate)
        batch_view = self.batch_processor.get_daily_summary(date)
        
        if batch_view:
            return batch_view
        
        # Fall back to speed layer (recent, possibly incomplete)
        return self.stream_processor.running_totals.get(date, {})


# Kappa Architecture Pattern (Apache Flink style)
def kappa_pipeline():
    """
    Single stream processing pipeline for all data.
    Pseudocode for Apache Flink/Beam style.
    """
    from apache_beam import Pipeline, DoFn, GroupByKey
    
    class ParseEvent(DoFn):
        def process(self, element):
            import json
            yield json.loads(element)
    
    class ExtractDateKey(DoFn):
        def process(self, element):
            date = element['timestamp'][:10]
            yield (date, element)
    
    class Aggregate(DoFn):
        def process(self, element):
            date, events = element
            events = list(events)
            yield {
                'date': date,
                'total_revenue': sum(e['amount'] for e in events),
                'order_count': len(events)
            }
    
    # Single pipeline handles both historical and real-time
    with Pipeline() as p:
        (
            p
            | 'Read Stream' >> ReadFromKafka(topic='sales')
            | 'Parse' >> beam.ParDo(ParseEvent())
            | 'Window' >> beam.WindowInto(DailyWindows())
            | 'Key by Date' >> beam.ParDo(ExtractDateKey())
            | 'Group' >> beam.GroupByKey()
            | 'Aggregate' >> beam.ParDo(Aggregate())
            | 'Write' >> WriteToBigQuery(table='daily_sales')
        )
```

## Key Takeaways

- Lambda Architecture uses parallel batch and stream layers for complete and real-time views
- Kappa Architecture simplifies by treating everything as a stream
- Batch processing offers completeness; streaming offers low latency
- Modern Lakehouse architectures combine the best of both worlds
- Medallion architecture (Bronze/Silver/Gold) organizes data by quality level
- Choose architecture based on latency requirements, complexity tolerance, and team skills

## Resources

- Nathan Marz on Lambda Architecture: <http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html>
- Kappa Architecture: <https://www.oreilly.com/radar/questioning-the-lambda-architecture/>
- Delta Lake: <https://delta.io/>
- Apache Flink: <https://flink.apache.org/>
