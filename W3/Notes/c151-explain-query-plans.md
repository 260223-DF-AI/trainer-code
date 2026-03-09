# EXPLAIN and Query Plans

## Learning Objectives

- Use EXPLAIN to understand query execution plans
- Interpret query plan output and cost estimates
- Identify performance bottlenecks through plan analysis
- Apply EXPLAIN ANALYZE for actual execution statistics

## Why This Matters

Query plans reveal how PostgreSQL actually executes your queries. Understanding plans helps you identify why queries are slow, verify that indexes are being used, and make informed optimization decisions. EXPLAIN is an essential tool for any developer working with databases at scale.

## The Concept

### What is a Query Plan?

A query plan is PostgreSQL's strategy for executing a query. It shows:

- Which tables and indexes are accessed
- The order of operations
- Estimated costs and row counts
- Join methods and scan types

### Basic EXPLAIN

```sql
EXPLAIN SELECT * FROM customers WHERE email = 'alice@email.com';
```

Output:

```
                                    QUERY PLAN
----------------------------------------------------------------------------------
Seq Scan on customers  (cost=0.00..18.50 rows=1 width=72)
  Filter: (email = 'alice@email.com'::text)
```

### EXPLAIN ANALYZE

Runs the query and shows actual execution statistics:

```sql
EXPLAIN ANALYZE SELECT * FROM customers WHERE email = 'alice@email.com';
```

Output:

```
                                    QUERY PLAN
----------------------------------------------------------------------------------
Seq Scan on customers  (cost=0.00..18.50 rows=1 width=72)
                       (actual time=0.015..0.089 rows=1 loops=1)
  Filter: (email = 'alice@email.com'::text)
  Rows Removed by Filter: 499
Planning Time: 0.085 ms
Execution Time: 0.107 ms
```

### Reading Query Plans

```
Node Type (cost=startup..total rows=estimated width=bytes)
         (actual time=startup..total rows=actual loops=iterations)
```

| Field | Meaning |
|-------|---------|
| cost | Estimated work (arbitrary units) |
| rows | Estimated/actual rows returned |
| width | Average row size in bytes |
| actual time | Real execution time in ms |
| loops | Times the node was executed |

### Scan Types

**Sequential Scan** - Reads entire table:

```sql
EXPLAIN SELECT * FROM products;
-- Seq Scan on products (cost=0.00..18.50 rows=500 width=72)
```

**Index Scan** - Uses an index:

```sql
CREATE INDEX idx_products_id ON products(product_id);
EXPLAIN SELECT * FROM products WHERE product_id = 100;
-- Index Scan using idx_products_id on products
```

**Index Only Scan** - Gets all data from index:

```sql
CREATE INDEX idx_products_price ON products(price);
EXPLAIN SELECT price FROM products WHERE price > 100;
-- Index Only Scan using idx_products_price on products
```

**Bitmap Scan** - For multiple index conditions:

```sql
EXPLAIN SELECT * FROM products 
WHERE category = 'Electronics' OR category = 'Furniture';
-- Bitmap Heap Scan on products
--   Recheck Cond: (category = ANY (...))
--   -> Bitmap Index Scan on idx_products_category
```

### Join Types

**Nested Loop** - For small result sets:

```sql
EXPLAIN SELECT * FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.name = 'Alice';
-- Nested Loop
--   -> Index Scan on customers (1 row)
--   -> Index Scan on orders (few rows)
```

**Hash Join** - For larger datasets:

```sql
EXPLAIN SELECT * FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id;
-- Hash Join
--   -> Seq Scan on customers (hash table built)
--   -> Seq Scan on orders (probed against hash)
```

**Merge Join** - For sorted data:

```sql
EXPLAIN SELECT * FROM table1 t1
JOIN table2 t2 ON t1.id = t2.id
ORDER BY t1.id;
-- Merge Join
--   -> Index Scan on table1
--   -> Index Scan on table2
```

### EXPLAIN Options

```sql
-- Include buffer usage
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM products;

-- Format as JSON
EXPLAIN (FORMAT JSON) SELECT * FROM products;

-- Verbose output
EXPLAIN (VERBOSE) SELECT * FROM products;

-- All options
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT TEXT)
SELECT * FROM products WHERE price > 100;
```

### Identifying Problems

**Missing Index** (Sequential Scan with Filter):

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 500;
-- Seq Scan on orders (actual rows=10000)
--   Filter: (customer_id = 500)
--   Rows Removed by Filter: 9990

-- Fix: Add index
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Poor Estimates** (estimated vs actual rows differ):

```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE rare_column = 'value';
-- Index Scan (rows=1000 actual rows=2)
-- Fix: ANALYZE products;
```

**Sorting Large Results**:

```sql
EXPLAIN ANALYZE SELECT * FROM orders ORDER BY total DESC;
-- Sort (actual rows=100000)
--   Sort Method: external merge (uses disk!)
-- Fix: Add index for ORDER BY
```

### Complete Example

```sql
-- Setup
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total DECIMAL(10,2),
    status VARCHAR(20)
);

-- Insert 100k rows
INSERT INTO orders (customer_id, order_date, total, status)
SELECT 
    (random() * 1000)::INTEGER,
    CURRENT_DATE - (random() * 365)::INTEGER,
    (random() * 1000)::DECIMAL(10,2),
    CASE (random() * 3)::INTEGER 
        WHEN 0 THEN 'pending' 
        WHEN 1 THEN 'shipped' 
        ELSE 'delivered' 
    END
FROM generate_series(1, 100000);

-- Before optimization
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE customer_id = 500 AND status = 'shipped';
-- Seq Scan... actual time=0.020..15.234 rows=30

-- Create indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);

-- After optimization
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE customer_id = 500 AND status = 'shipped';
-- Bitmap Heap Scan... actual time=0.050..0.123 rows=30

-- Composite index is even better
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE customer_id = 500 AND status = 'shipped';
-- Index Scan... actual time=0.020..0.045 rows=30
```

## Key Takeaways

- EXPLAIN shows the query plan without running it
- EXPLAIN ANALYZE runs the query and shows actual stats
- Sequential scans on large tables indicate missing indexes
- Compare estimated vs actual rows to identify stale statistics
- Use BUFFERS to see memory/disk usage
- High cost operations are optimization candidates

## Additional Resources

- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [Query Planning](https://www.postgresql.org/docs/current/runtime-config-query.html)
