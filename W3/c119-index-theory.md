# Index

## Learning Objectives

- Understand what database indexes are
- Learn how indexes improve query performance
- Create and manage indexes
- Recognize when to use (and not use) indexes

## Why This Matters

Indexes are crucial for database performance. Without proper indexes, queries must scan entire tables to find matching rows, which becomes extremely slow as data grows. Understanding indexes helps you write faster queries and design efficient database schemas. However, indexes have trade-offs that you must understand.

## The Concept

### What is an Index?

An **index** is a data structure that improves the speed of data retrieval operations. It works like a book's index: instead of reading every page to find a topic, you look up the topic in the index to find the specific page numbers.

```
Without Index (Table Scan):
+----+----------+------------+
| id | name     | department |  Search for 'Engineering'
+----+----------+------------+  Must check EVERY row
| 1  | Alice    | Sales      |  <- Check
| 2  | Bob      | Engineering|  <- Check (MATCH!)
| 3  | Carol    | Marketing  |  <- Check
| 4  | David    | Engineering|  <- Check (MATCH!)
| ...| ...      | ...        |  <- Check all rows
+----+----------+------------+

With Index:
department_index:
Engineering -> rows 2, 4
Marketing   -> row 3
Sales       -> row 1

Search: Jump directly to rows 2 and 4!
```

### Creating Indexes

**Basic index**:

```sql
CREATE INDEX idx_employees_department ON employees(department);

CREATE INDEX idx_orders_customer ON orders(customer_id);

CREATE INDEX idx_products_name ON products(name);
```

**Unique index** (also enforces uniqueness):

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Multi-column (composite) index**:

```sql
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

**Partial index** (only index some rows):

```sql
CREATE INDEX idx_orders_pending ON orders(order_date) 
WHERE status = 'pending';
```

### Index Types in PostgreSQL

| Type | Use Case |
|------|----------|
| B-tree | Default, general purpose, equality and range |
| Hash | Equality comparisons only |
| GiST | Geometric data, full-text search |
| GIN | Arrays, JSONB, full-text search |
| BRIN | Very large tables with natural ordering |

```sql
-- B-tree (default)
CREATE INDEX idx_btree ON products(price);

-- Hash (equality only)
CREATE INDEX idx_hash ON users USING hash(email);

-- GIN for JSONB
CREATE INDEX idx_jsonb ON documents USING gin(data);

-- GIN for full-text search
CREATE INDEX idx_fulltext ON articles USING gin(to_tsvector('english', content));
```

### When Indexes Help

Indexes speed up:

```sql
-- WHERE clauses
SELECT * FROM employees WHERE department = 'Engineering';

-- JOIN conditions
SELECT o.*, c.name 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id;

-- ORDER BY
SELECT * FROM products ORDER BY price;

-- DISTINCT and GROUP BY
SELECT DISTINCT category FROM products;
SELECT department, COUNT(*) FROM employees GROUP BY department;
```

### When Indexes Hurt

Indexes have costs:

1. **Storage**: Indexes take disk space
2. **Write performance**: INSERT, UPDATE, DELETE must update indexes
3. **Maintenance**: Large indexes need periodic maintenance

**Avoid over-indexing**:

```sql
-- Too many indexes on one table
CREATE INDEX idx1 ON orders(customer_id);
CREATE INDEX idx2 ON orders(order_date);
CREATE INDEX idx3 ON orders(status);
CREATE INDEX idx4 ON orders(total);
-- Each INSERT now updates 4 indexes!
```

### Index Column Order Matters

For composite indexes, column order is critical:

```sql
CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date);

-- This uses the index:
SELECT * FROM orders WHERE customer_id = 100;
SELECT * FROM orders WHERE customer_id = 100 AND order_date > '2024-01-01';

-- This may NOT use the index efficiently:
SELECT * FROM orders WHERE order_date > '2024-01-01';
-- (date is second column, not first)
```

Rule: Put more frequently filtered columns first.

### Managing Indexes

**View existing indexes**:

```sql
-- psql command
\di

-- Query system catalog
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'orders';
```

**Drop index**:

```sql
DROP INDEX idx_employees_department;
DROP INDEX IF EXISTS idx_old_index;
```

**Rename index**:

```sql
ALTER INDEX idx_old_name RENAME TO idx_new_name;
```

**Rebuild index**:

```sql
REINDEX INDEX idx_employees_department;
REINDEX TABLE employees;  -- All indexes on table
```

### Checking Index Usage

```sql
-- See if query uses index
EXPLAIN SELECT * FROM employees WHERE department = 'Engineering';

-- More detail
EXPLAIN ANALYZE SELECT * FROM employees WHERE department = 'Engineering';

-- Check index statistics
SELECT 
    indexrelname,
    idx_scan,  -- Number of index scans
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public';
```

## Code Example

Index creation and usage:

```sql
-- Create table with data
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert sample data
INSERT INTO products (name, category, price, stock)
SELECT 
    'Product ' || i,
    CASE WHEN i % 3 = 0 THEN 'Electronics'
         WHEN i % 3 = 1 THEN 'Clothing'
         ELSE 'Home' END,
    (random() * 500)::DECIMAL(10,2),
    (random() * 100)::INTEGER
FROM generate_series(1, 10000) AS i;

-- Check query without index
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';
-- Likely shows: Seq Scan (sequential scan of all rows)

-- Create index
CREATE INDEX idx_products_category ON products(category);

-- Check query with index
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';
-- Should show: Index Scan or Bitmap Index Scan

-- Composite index for common query pattern
CREATE INDEX idx_products_category_price 
ON products(category, price);

-- Uses composite index
EXPLAIN ANALYZE 
SELECT * FROM products 
WHERE category = 'Electronics' AND price < 100;

-- Partial index for active products only
CREATE INDEX idx_products_active 
ON products(category, price)
WHERE is_active = TRUE;

-- View all indexes on products table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'products';

-- Check index usage statistics
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE relname = 'products';
```

## Key Takeaways

- Indexes dramatically speed up SELECT queries
- But they slow down INSERT, UPDATE, DELETE operations
- Create indexes on frequently filtered/joined columns
- Column order in composite indexes matters
- Use EXPLAIN ANALYZE to verify index usage
- Avoid over-indexing; each index has a cost

## Additional Resources

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
