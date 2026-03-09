# Schema

## Learning Objectives

- Define what a database schema is
- Understand the purpose of schemas in database organization
- Distinguish between schema and database
- Learn how schemas provide namespace separation

## Why This Matters

As databases grow in complexity, organization becomes critical. Schemas provide a logical way to group related database objects together, similar to how you organized Python code into modules and packages in Week 2. Understanding schemas helps you design databases that are maintainable, secure, and scalable.

## The Concept

### What is a Schema?

A **schema** is a logical container within a database that groups related objects together. Think of it as a namespace or folder that organizes:

- Tables
- Views
- Indexes
- Stored procedures
- Functions
- Sequences

### Schema vs. Database

```
+--------------------------------------------------+
|                    DATABASE SERVER                |
|                                                   |
|  +----------------+     +----------------+        |
|  |   Database A   |     |   Database B   |        |
|  |                |     |                |        |
|  | +------------+ |     | +------------+ |        |
|  | | Schema 1   | |     | | Schema 1   | |        |
|  | |  - tables  | |     | |  - tables  | |        |
|  | +------------+ |     | +------------+ |        |
|  |                |     |                |        |
|  | +------------+ |     | +------------+ |        |
|  | | Schema 2   | |     | | Schema 2   | |        |
|  | |  - tables  | |     | |  - tables  | |        |
|  | +------------+ |     | +------------+ |        |
|  +----------------+     +----------------+        |
+--------------------------------------------------+
```

**Database**: A complete collection of data and objects
**Schema**: A logical grouping within a database

### Why Use Schemas?

1. **Organization**: Group related tables logically
2. **Security**: Grant permissions at the schema level
3. **Namespace**: Avoid naming conflicts between applications
4. **Multi-tenancy**: Separate data for different clients
5. **Migration**: Easier to move entire schemas between databases

### Common Schema Patterns

**By Application Function**:

```
database: company_db
    schema: hr           -- Human resources tables
    schema: finance      -- Financial tables
    schema: inventory    -- Inventory management
    schema: sales        -- Sales and orders
```

**By Environment**:

```
database: app_db
    schema: production   -- Live data
    schema: staging      -- Testing data
    schema: archive      -- Historical data
```

**By Tenant (Multi-tenant)**:

```
database: saas_app
    schema: tenant_001   -- Client A data
    schema: tenant_002   -- Client B data
    schema: shared       -- Common reference data
```

### The Public Schema

In PostgreSQL, the default schema is `public`. If you create a table without specifying a schema, it goes into `public`:

```sql
-- These are equivalent
CREATE TABLE employees (...);
CREATE TABLE public.employees (...);
```

### Fully Qualified Names

Reference objects using the full path: `schema.object_name`

```sql
-- Fully qualified table reference
SELECT * FROM hr.employees;
SELECT * FROM finance.accounts;
SELECT * FROM sales.orders;
```

### Search Path

PostgreSQL uses a **search path** to find objects:

```sql
-- View current search path
SHOW search_path;
-- Result: "$user", public

-- Set search path for current session
SET search_path TO hr, public;

-- Now you can reference hr tables without prefix
SELECT * FROM employees;  -- Finds hr.employees
```

## Code Example

Creating and using schemas in PostgreSQL:

```sql
-- Create schemas
CREATE SCHEMA hr;
CREATE SCHEMA finance;
CREATE SCHEMA sales;

-- Create a table in a specific schema
CREATE TABLE hr.employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    hire_date DATE
);

CREATE TABLE finance.accounts (
    account_id SERIAL PRIMARY KEY,
    account_name VARCHAR(100),
    balance DECIMAL(15, 2)
);

-- Query from specific schema
SELECT * FROM hr.employees;

-- List all schemas
SELECT schema_name 
FROM information_schema.schemata;

-- List tables in a specific schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'hr';

-- Drop a schema (must be empty)
DROP SCHEMA hr;

-- Drop schema and all its objects
DROP SCHEMA hr CASCADE;
```

## Key Takeaways

- A schema is a logical container for database objects
- Schemas provide namespace separation within a database
- The default schema in PostgreSQL is `public`
- Use fully qualified names: `schema.table_name`
- Schemas help organize, secure, and manage database objects

## Additional Resources

- [PostgreSQL Schemas Documentation](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Schema Design Best Practices](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATTERNS)
- [Managing Schemas in pgAdmin](https://www.pgadmin.org/docs/pgadmin4/latest/schema_dialog.html)
