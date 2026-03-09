# CREATE, DROP, and TRUNCATE

## Learning Objectives

- Understand the purpose and behavior of CREATE, DROP, and TRUNCATE
- Differentiate between removing data vs. removing structure
- Apply each command appropriately based on requirements
- Recognize the implications of each command on data and schema

## Why This Matters

These three DDL commands are fundamental to database administration. Knowing when to use DROP vs. TRUNCATE vs. DELETE can mean the difference between a quick cleanup and accidentally destroying your entire table structure. Understanding their behaviors helps prevent costly mistakes and enables efficient database maintenance.

## The Concept

### Overview

| Command | Purpose | Removes Data | Removes Structure | Can Rollback* |
|---------|---------|--------------|-------------------|---------------|
| CREATE | Build new objects | N/A | N/A | Yes |
| DROP | Remove objects entirely | Yes | Yes | Yes |
| TRUNCATE | Remove all rows quickly | Yes | No | Limited |

*Rollback behavior depends on database and transaction settings

### CREATE - Building Database Objects

CREATE defines new database objects:

```sql
-- Create a database
CREATE DATABASE company_db;

-- Create a schema
CREATE SCHEMA sales;

-- Create a table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    hire_date DATE DEFAULT CURRENT_DATE
);

-- Create with IF NOT EXISTS (prevents errors)
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

### DROP - Removing Objects Completely

DROP removes the entire object including its structure and all data:

```sql
-- Drop a table (removes structure AND all data)
DROP TABLE employees;

-- Drop only if exists (prevents errors)
DROP TABLE IF EXISTS employees;

-- Drop a database
DROP DATABASE company_db;

-- Drop a schema
DROP SCHEMA sales;

-- Drop with CASCADE (removes dependent objects)
DROP TABLE departments CASCADE;
```

**Warning**: DROP is permanent and removes the table definition. You cannot recover without a backup.

### TRUNCATE - Removing All Rows

TRUNCATE removes all data but keeps the table structure:

```sql
-- Remove all rows from a table
TRUNCATE TABLE employees;

-- Truncate and reset identity/serial counter
TRUNCATE TABLE employees RESTART IDENTITY;

-- Truncate multiple tables
TRUNCATE TABLE orders, order_items;

-- Truncate with CASCADE (handles foreign keys)
TRUNCATE TABLE departments CASCADE;
```

### TRUNCATE vs. DELETE

| Aspect | TRUNCATE | DELETE |
|--------|----------|--------|
| Speed | Very fast (deallocates pages) | Slower (row by row) |
| WHERE clause | Not supported | Supported |
| Triggers | Does not fire row triggers | Fires row triggers |
| Transaction log | Minimal logging | Full logging |
| Identity reset | Can reset with RESTART IDENTITY | Does not reset |
| Rollback | Depends on database | Always possible |

```sql
-- DELETE: Removes specific rows, can use WHERE
DELETE FROM employees WHERE department = 'Sales';

-- TRUNCATE: Removes ALL rows, no conditions
TRUNCATE TABLE employees;
```

### Practical Examples

```sql
-- Create a test table
CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    value VARCHAR(50)
);

-- Insert some data
INSERT INTO test_data (value) VALUES ('A'), ('B'), ('C');
SELECT * FROM test_data;  -- Shows 3 rows

-- TRUNCATE: Remove all data, keep structure
TRUNCATE TABLE test_data RESTART IDENTITY;
SELECT * FROM test_data;  -- Shows 0 rows

-- Table still exists, can insert again
INSERT INTO test_data (value) VALUES ('X');
SELECT * FROM test_data;  -- id starts at 1 again

-- DROP: Remove the table entirely
DROP TABLE test_data;
SELECT * FROM test_data;  -- ERROR: table does not exist

-- Recreate for future use
CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    value VARCHAR(50)
);
```

### Safety with IF EXISTS and IF NOT EXISTS

```sql
-- Safe drop - won't error if table doesn't exist
DROP TABLE IF EXISTS old_backup_table;

-- Safe create - won't error if table already exists
CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Key Takeaways

- CREATE builds new database objects (databases, schemas, tables)
- DROP removes objects entirely including structure and data
- TRUNCATE removes all rows but preserves table structure
- TRUNCATE is faster than DELETE for removing all rows
- Use IF EXISTS/IF NOT EXISTS for safer scripts
- Always backup before using DROP or TRUNCATE in production

## Additional Resources

- [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL DROP TABLE](https://www.postgresql.org/docs/current/sql-droptable.html)
- [PostgreSQL TRUNCATE](https://www.postgresql.org/docs/current/sql-truncate.html)
