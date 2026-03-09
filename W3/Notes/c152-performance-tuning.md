# Performance Tuning

## Learning Objectives

- Apply systematic performance optimization techniques
- Optimize queries for speed and efficiency
- Configure database settings for better performance
- Identify and resolve common performance issues

## Why This Matters

As data grows, poorly optimized queries can bring applications to a halt. Performance tuning is the difference between a query that takes 10 seconds and one that takes 10 milliseconds. Understanding these techniques helps you build applications that scale and maintain responsiveness as data volumes increase.

## The Concept

### The Performance Tuning Process

```
1. Identify → 2. Measure → 3. Analyze → 4. Optimize → 5. Verify
     |             |            |            |            |
   Slow query   EXPLAIN      Find cause   Apply fix    Measure again
```

### Indexing Strategies

**Index High-Selectivity Columns**:

```sql
-- Good: email has unique or near-unique values
CREATE INDEX idx_users_email ON users(email);

-- Less helpful: status has only 3 distinct values
CREATE INDEX idx_users_status ON users(status);  -- May not help
```

**Covering Indexes**:

```sql
-- Index includes all columns needed by query
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, total);

-- Query can use Index Only Scan
SELECT order_date, total FROM orders WHERE customer_id = 100;
```

**Partial Indexes**:

```sql
-- Index only active records
CREATE INDEX idx_active_users ON users(email) WHERE is_active = TRUE;

-- Much smaller than full index
SELECT * FROM users WHERE email = 'alice@email.com' AND is_active = TRUE;
```

### Query Optimization

**Select Only Needed Columns**:

```sql
-- Bad: fetches unnecessary data
SELECT * FROM orders WHERE customer_id = 100;

-- Better: only what you need
SELECT order_id, order_date, total FROM orders WHERE customer_id = 100;
```

**Use LIMIT for Large Results**:

```sql
-- Without limit: returns millions of rows
SELECT * FROM log_entries ORDER BY created_at DESC;

-- With limit: fast
SELECT * FROM log_entries ORDER BY created_at DESC LIMIT 100;
```

**Avoid Functions on Indexed Columns**:

```sql
-- Bad: Can't use index on email
SELECT * FROM users WHERE LOWER(email) = 'alice@email.com';

-- Better: Create expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Or store normalized data
SELECT * FROM users WHERE email_lower = 'alice@email.com';
```

**Use EXISTS Instead of IN for Subqueries**:

```sql
-- Slower with large subquery results
SELECT * FROM products p
WHERE p.category_id IN (SELECT category_id FROM categories WHERE active = TRUE);

-- Faster: EXISTS stops after first match
SELECT * FROM products p
WHERE EXISTS (
    SELECT 1 FROM categories c 
    WHERE c.category_id = p.category_id AND c.active = TRUE
);
```

### Join Optimization

**Join Order Matters**:

```sql
-- Start with the most selective table
SELECT *
FROM small_table s           -- 100 rows
JOIN medium_table m ON s.id = m.s_id   -- 10,000 rows
JOIN large_table l ON m.id = l.m_id;   -- 1,000,000 rows
```

**Ensure Indexes on Join Columns**:

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Joins will use indexes
SELECT * FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id;
```

### Database Configuration

**Key Settings** (postgresql.conf):

```sql
-- View current settings
SHOW shared_buffers;
SHOW work_mem;
SHOW effective_cache_size;

-- Memory for shared cache (25% of RAM typical)
-- shared_buffers = 4GB

-- Memory per operation (sorting, hashing)
-- work_mem = 256MB

-- Planner estimate of OS cache
-- effective_cache_size = 12GB
```

**Connection Pooling**:

```
Application --> Connection Pool --> Database
              (PgBouncer/PgPool)
              
Reduces connection overhead, handles many clients efficiently
```

### Table Maintenance

**Update Statistics**:

```sql
-- Update statistics for a table
ANALYZE orders;

-- Update all tables
ANALYZE;

-- Combined vacuum and analyze
VACUUM ANALYZE orders;
```

**Reclaim Space**:

```sql
-- Remove dead tuples
VACUUM orders;

-- Reclaim disk space (locks table)
VACUUM FULL orders;
```

**Rebuild Indexes**:

```sql
-- Rebuild a specific index
REINDEX INDEX idx_orders_date;

-- Rebuild all indexes on a table
REINDEX TABLE orders;

-- Online reindex (no locks)
REINDEX INDEX CONCURRENTLY idx_orders_date;
```

### Monitoring Queries

**Find Slow Queries**:

```sql
-- Enable slow query logging
-- log_min_duration_statement = 1000  -- Log queries > 1 sec

-- Find currently running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';

-- Kill a slow query
SELECT pg_cancel_backend(pid);  -- Graceful
SELECT pg_terminate_backend(pid);  -- Force
```

**Index Usage Statistics**:

```sql
-- Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;

-- Find missing indexes (sequential scans on large tables)
SELECT schemaname, relname, seq_scan, seq_tup_read,
       idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC;
```

### Caching Strategies

**Materialized Views**:

```sql
-- Cache expensive query results
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    SUM(total) AS revenue,
    COUNT(*) AS orders
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh when data changes
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_summary;
```

**Application-Level Caching**:

```
Application --> Cache (Redis/Memcached) --> Database
                     |
              Quick for repeated queries
```

### Complete Optimization Example

```sql
-- Original slow query
EXPLAIN ANALYZE
SELECT 
    c.name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_at >= '2024-01-01'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC NULLS LAST
LIMIT 100;
-- Execution time: 2500ms

-- Step 1: Add indexes
CREATE INDEX idx_customers_created ON customers(created_at);
CREATE INDEX idx_orders_customer ON orders(customer_id);
-- Execution time: 800ms

-- Step 2: Analyze tables
ANALYZE customers;
ANALYZE orders;
-- Execution time: 600ms

-- Step 3: Create covering index
CREATE INDEX idx_orders_customer_total ON orders(customer_id, total);
-- Execution time: 200ms

-- Step 4: Consider materialized view for dashboard
CREATE MATERIALIZED VIEW customer_stats AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

CREATE UNIQUE INDEX idx_customer_stats ON customer_stats(customer_id);
-- Query from view: 5ms
```

## Key Takeaways

- Index columns used in WHERE, JOIN, and ORDER BY
- Select only the columns you need
- Use EXPLAIN ANALYZE to identify bottlenecks
- Keep statistics up to date with ANALYZE
- Monitor slow queries and unused indexes
- Consider caching for frequently-run expensive queries
- Test changes and measure impact

## Additional Resources

- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html)
- [Monitoring Statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)
