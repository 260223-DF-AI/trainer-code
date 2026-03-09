# Indexes - Performance Optimization

## Learning Objectives

- Understand how indexes improve query performance
- Create and manage various types of indexes
- Apply indexing strategies for common query patterns
- Analyze when indexes help and when they hurt

## Why This Matters

Indexes are the primary tool for query performance optimization. A well-designed index can turn a query that takes minutes into one that returns instantly. As your data grows, proper indexing becomes essential for maintaining application responsiveness. Understanding indexes separates database novices from professionals.

## The Concept

### What is an Index?

An index is a data structure that improves the speed of data retrieval operations. Like a book's index, it helps the database find data without scanning every row.

```
Without Index:                  With Index:
+-------------------+           +-------------------+
| Table: 1M rows    |           | Index: sorted     |
| Scan all rows     |           | Binary search     |
| Time: O(n)        |           | Time: O(log n)    |
+-------------------+           +-------------------+
```

### Creating Indexes

```sql
-- Basic index on a single column
CREATE INDEX idx_customers_email ON customers(email);

-- Index on multiple columns (composite index)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Unique index (enforces uniqueness)
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Index with specific method
CREATE INDEX idx_locations_geo ON locations USING GiST(coordinates);
```

### Types of Indexes

| Type | Use Case | PostgreSQL Syntax |
|------|----------|------------------|
| B-tree | Default, equality and range | `USING btree` (default) |
| Hash | Equality only | `USING hash` |
| GiST | Geometric, full-text | `USING gist` |
| GIN | Arrays, JSON, full-text | `USING gin` |
| BRIN | Large tables, sequential data | `USING brin` |

### B-tree Index (Default)

Best for equality and range queries:

```sql
CREATE INDEX idx_products_price ON products(price);

-- These queries use the index:
SELECT * FROM products WHERE price = 50;
SELECT * FROM products WHERE price > 100;
SELECT * FROM products WHERE price BETWEEN 50 AND 100;
SELECT * FROM products ORDER BY price LIMIT 10;
```

### Composite Index

Index on multiple columns:

```sql
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Uses index (leftmost columns):
SELECT * FROM orders WHERE customer_id = 100;
SELECT * FROM orders WHERE customer_id = 100 AND order_date > '2024-01-01';

-- Does NOT use index well (missing leftmost column):
SELECT * FROM orders WHERE order_date > '2024-01-01';
```

**Rule**: Put the most frequently filtered column first.

### Partial Index

Index only a subset of rows:

```sql
-- Index only active products
CREATE INDEX idx_active_products ON products(name) WHERE is_active = TRUE;

-- Index only recent orders
CREATE INDEX idx_recent_orders ON orders(customer_id) 
WHERE order_date > '2024-01-01';
```

Partial indexes are smaller and faster.

### Expression Index

Index on an expression or function:

```sql
-- Index on lowercase email for case-insensitive search
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Query must use same expression:
SELECT * FROM users WHERE LOWER(email) = 'alice@email.com';

-- Index on year for date filtering
CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));
```

### Index Usage with EXPLAIN

Check if your queries use indexes:

```sql
-- Show query plan
EXPLAIN SELECT * FROM customers WHERE email = 'alice@email.com';

-- Show actual execution time
EXPLAIN ANALYZE SELECT * FROM customers WHERE email = 'alice@email.com';
```

```
                                    QUERY PLAN
--------------------------------------------------------------------------
Index Scan using idx_customers_email on customers
    Index Cond: (email = 'alice@email.com')
    Actual Time: 0.050..0.051 rows=1 loops=1
```

### When NOT to Use Indexes

Indexes have overhead:

```sql
-- Indexes slow down writes
INSERT INTO products (name, price) VALUES ('New Product', 50);
-- Must update all relevant indexes

-- Small tables don't benefit
-- Full table scan may be faster than index lookup

-- Low cardinality columns
-- Index on gender ('M', 'F') rarely helpful
```

### Managing Indexes

```sql
-- List indexes on a table
\di products
-- or
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';

-- Drop an index
DROP INDEX idx_products_price;
DROP INDEX IF EXISTS idx_products_price;

-- Rebuild an index
REINDEX INDEX idx_products_price;
REINDEX TABLE products;

-- Create index without blocking writes
CREATE INDEX CONCURRENTLY idx_products_name ON products(name);
```

### Index Strategy Best Practices

1. **Index columns used in WHERE clauses**
2. **Index columns used in JOIN conditions**
3. **Index columns used in ORDER BY**
4. **Don't over-index** - each index slows writes
5. **Monitor and remove unused indexes**
6. **Use composite indexes for multi-column queries**

### Complete Example

```sql
-- Create table with likely query patterns
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    total DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO orders (customer_id, order_date, status, total)
SELECT 
    (random() * 1000)::INTEGER,
    CURRENT_DATE - (random() * 365)::INTEGER,
    CASE (random() * 3)::INTEGER 
        WHEN 0 THEN 'pending' 
        WHEN 1 THEN 'shipped' 
        ELSE 'delivered' 
    END,
    (random() * 1000)::DECIMAL(10,2)
FROM generate_series(1, 100000);

-- Without index
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 500;
-- Seq Scan... Time: 50ms

-- Add index
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- With index
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 500;
-- Index Scan... Time: 0.5ms (100x faster!)

-- Composite index for common query
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date DESC);

-- Fast query:
SELECT * FROM orders 
WHERE customer_id = 500 
ORDER BY order_date DESC 
LIMIT 10;
```

## Key Takeaways

- Indexes dramatically speed up SELECT queries
- B-tree is the default and most common index type
- Composite indexes should have frequently filtered columns first
- Partial indexes reduce size by indexing only relevant rows
- Expression indexes support function-based filtering
- Indexes slow down INSERT, UPDATE, DELETE operations
- Use EXPLAIN ANALYZE to verify index usage

## Additional Resources

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- [EXPLAIN Documentation](https://www.postgresql.org/docs/current/sql-explain.html)
