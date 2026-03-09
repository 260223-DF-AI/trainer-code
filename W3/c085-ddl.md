# DDL: Data Definition Language

## Learning Objectives

- Master DDL commands: CREATE, ALTER, DROP, TRUNCATE
- Understand when to use each DDL command
- Apply DDL to define database structure
- Recognize DDL's impact on schema and transactions

## Why This Matters

DDL commands are the foundation of database development. Every table, index, and constraint you create uses DDL. As a data professional, you will frequently create new structures, modify existing ones, and occasionally remove obsolete objects. Understanding DDL is essential for implementing any database design.

## The Concept

### What is DDL?

Data Definition Language (DDL) consists of SQL commands that define, modify, and remove database structures. DDL operates on the **schema** (metadata) rather than the data itself.

### DDL Commands Overview

| Command | Purpose | Example |
|---------|---------|---------|
| CREATE | Build new objects | `CREATE TABLE ...` |
| ALTER | Modify existing objects | `ALTER TABLE ... ADD COLUMN` |
| DROP | Delete objects permanently | `DROP TABLE ...` |
| TRUNCATE | Remove all rows quickly | `TRUNCATE TABLE ...` |

### CREATE

The CREATE command builds new database objects:

```sql
-- Create a table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    salary DECIMAL(10, 2)
);

-- Create a schema
CREATE SCHEMA hr;

-- Create an index
CREATE INDEX idx_employees_email ON employees(email);

-- Create a view
CREATE VIEW active_employees AS
SELECT * FROM employees WHERE is_active = TRUE;

-- Create with IF NOT EXISTS (prevents error if exists)
CREATE TABLE IF NOT EXISTS logs (
    log_id SERIAL PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP
);
```

### ALTER

The ALTER command modifies existing objects:

**Table Modifications**:

```sql
-- Add a column
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- Drop a column
ALTER TABLE employees DROP COLUMN phone;

-- Rename a column
ALTER TABLE employees RENAME COLUMN email TO email_address;

-- Change column data type
ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12, 2);

-- Add a constraint
ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary >= 0);

-- Drop a constraint
ALTER TABLE employees DROP CONSTRAINT chk_salary;

-- Set/remove default
ALTER TABLE employees ALTER COLUMN is_active SET DEFAULT TRUE;
ALTER TABLE employees ALTER COLUMN is_active DROP DEFAULT;

-- Set not null
ALTER TABLE employees ALTER COLUMN first_name SET NOT NULL;
ALTER TABLE employees ALTER COLUMN nickname DROP NOT NULL;

-- Rename table
ALTER TABLE employees RENAME TO staff;
```

**Other ALTER Operations**:

```sql
-- Rename a schema
ALTER SCHEMA old_name RENAME TO new_name;

-- Change table owner
ALTER TABLE employees OWNER TO hr_admin;

-- Move table to another schema
ALTER TABLE public.employees SET SCHEMA hr;
```

### DROP

The DROP command permanently removes objects:

```sql
-- Drop a table (CAREFUL!)
DROP TABLE old_records;

-- Drop with IF EXISTS (no error if missing)
DROP TABLE IF EXISTS temp_data;

-- Drop with CASCADE (removes dependent objects)
DROP TABLE employees CASCADE;

-- Drop other objects
DROP SCHEMA temporary_schema;
DROP INDEX idx_employees_email;
DROP VIEW old_report;

-- Drop multiple tables
DROP TABLE table1, table2, table3;
```

**DROP vs TRUNCATE vs DELETE**:

| Operation | Removes | Can Rollback | Resets IDs | Speed |
|-----------|---------|--------------|------------|-------|
| DROP | Table + Data | Not typically | N/A | Fast |
| TRUNCATE | Data only | Sometimes | Yes | Fast |
| DELETE | Selected rows | Yes | No | Slow |

### TRUNCATE

The TRUNCATE command efficiently removes all rows:

```sql
-- Remove all data from a table
TRUNCATE TABLE staging_data;

-- Truncate multiple tables
TRUNCATE TABLE log1, log2, log3;

-- Truncate with identity reset
TRUNCATE TABLE orders RESTART IDENTITY;

-- Truncate with cascade (truncates child tables too)
TRUNCATE TABLE parent_table CASCADE;
```

**When to use TRUNCATE**:

- Clearing staging/temporary tables
- Resetting test data
- Faster than DELETE for all rows
- Reclaims storage immediately

### DDL and Transactions

In PostgreSQL, DDL is transactional (unlike many other databases):

```sql
BEGIN;
    CREATE TABLE test_table (id INT);
    INSERT INTO test_table VALUES (1);
    -- Oops, made a mistake
ROLLBACK;
-- Table creation is undone!

-- However, be careful:
BEGIN;
    DROP TABLE important_data;  -- This can be rolled back...
COMMIT;
-- ...but after COMMIT, it's permanent!
```

### Best Practices

1. **Always use IF EXISTS / IF NOT EXISTS** in scripts:

```sql
DROP TABLE IF EXISTS old_table;
CREATE TABLE IF NOT EXISTS new_table (...);
```

1. **Test DDL in development first**
2. **Back up before DROP or TRUNCATE**
3. **Use transactions for complex changes**
4. **Document schema changes**

## Code Example

Complete DDL workflow:

```sql
-- Create initial structure
CREATE SCHEMA IF NOT EXISTS inventory;

CREATE TABLE inventory.products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0),
    quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Later: Modify the structure
ALTER TABLE inventory.products 
    ADD COLUMN category VARCHAR(50),
    ADD COLUMN supplier_id INTEGER;

ALTER TABLE inventory.products
    ADD CONSTRAINT chk_quantity CHECK (quantity >= 0);

CREATE INDEX idx_products_category 
    ON inventory.products(category);

-- Create a related table
CREATE TABLE inventory.suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100)
);

-- Add foreign key relationship
ALTER TABLE inventory.products
    ADD CONSTRAINT fk_supplier
    FOREIGN KEY (supplier_id) REFERENCES inventory.suppliers(supplier_id);

-- Clean up old data
TRUNCATE TABLE inventory.products RESTART IDENTITY CASCADE;

-- Remove obsolete objects
DROP INDEX IF EXISTS idx_products_old;
DROP TABLE IF EXISTS inventory.deprecated_table;
```

## Key Takeaways

- CREATE builds new database objects
- ALTER modifies existing objects (columns, constraints, names)
- DROP permanently removes objects (use with caution)
- TRUNCATE quickly removes all rows from a table
- PostgreSQL DDL is transactional (can be rolled back before COMMIT)
- Always use IF EXISTS / IF NOT EXISTS for safer scripts

## Additional Resources

- [PostgreSQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL DROP TABLE](https://www.postgresql.org/docs/current/sql-droptable.html)
