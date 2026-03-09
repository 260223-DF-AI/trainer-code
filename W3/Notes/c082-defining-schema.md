# Defining Schema

## Learning Objectives

- Learn how to create and manage database schemas
- Understand schema design principles
- Apply namespace management strategies
- Set up proper schema permissions

## Why This Matters

Proper schema design from the start saves countless hours of refactoring later. Well-organized schemas make databases easier to understand, maintain, secure, and scale. This is especially important in enterprise environments where multiple teams and applications share the same database server.

## The Concept

### Creating Schemas

The basic syntax for creating a schema:

```sql
-- Simple schema creation
CREATE SCHEMA sales;

-- Schema with owner
CREATE SCHEMA hr AUTHORIZATION hr_admin;

-- Schema with objects created inside
CREATE SCHEMA inventory
    CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    )
    CREATE TABLE warehouses (
        warehouse_id SERIAL PRIMARY KEY,
        location VARCHAR(200)
    );
```

### Schema Design Principles

**1. Separation of Concerns**

Each schema should have a clear responsibility:

```sql
-- Separate by business domain
CREATE SCHEMA customers;    -- Customer-related tables
CREATE SCHEMA orders;       -- Order processing
CREATE SCHEMA products;     -- Product catalog
CREATE SCHEMA analytics;    -- Reporting views
CREATE SCHEMA staging;      -- Data import/processing
```

**2. Clear Naming Convention**

```sql
-- Good: Clear, lowercase, descriptive
CREATE SCHEMA user_management;
CREATE SCHEMA financial_reporting;

-- Avoid: Vague or inconsistent
CREATE SCHEMA Stuff;
CREATE SCHEMA misc_data;
```

**3. Minimal Public Schema Usage**

```sql
-- Avoid cluttering public schema
-- Instead, organize into specific schemas

-- Move existing table to another schema
ALTER TABLE public.customers 
    SET SCHEMA customer_data;
```

### Schema Ownership and Permissions

```sql
-- Create schema owned by specific user
CREATE SCHEMA sales AUTHORIZATION sales_team;

-- Grant schema usage
GRANT USAGE ON SCHEMA sales TO app_user;

-- Grant select on all tables in schema
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO reporting_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT SELECT ON TABLES TO reporting_user;

-- Revoke permissions
REVOKE ALL ON SCHEMA sales FROM public;
```

### Managing the Search Path

The search path determines which schemas are searched for unqualified object names:

```sql
-- View current search path
SHOW search_path;

-- Set search path for session
SET search_path TO myschema, public;

-- Set search path permanently for a user
ALTER USER app_user SET search_path TO app, common, public;

-- Set search path for a database
ALTER DATABASE mydb SET search_path TO app, public;
```

### Schema Best Practices

**Organize by Layer**:

```sql
-- Application layers
CREATE SCHEMA api;        -- Views for API consumption
CREATE SCHEMA core;       -- Core business logic tables
CREATE SCHEMA audit;      -- Audit logs
CREATE SCHEMA archive;    -- Historical data
```

**Development Workflow**:

```sql
-- Development environments
CREATE SCHEMA dev;        -- Development work
CREATE SCHEMA test;       -- Testing
CREATE SCHEMA staging;    -- Pre-production
```

**Multi-tenant Architecture**:

```sql
-- Each tenant gets their own schema
CREATE SCHEMA tenant_acme;
CREATE SCHEMA tenant_globex;
CREATE SCHEMA tenant_initech;
CREATE SCHEMA shared;     -- Common reference data
```

### Viewing Schema Information

```sql
-- List all schemas
SELECT schema_name 
FROM information_schema.schemata
ORDER BY schema_name;

-- List all objects in a schema
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'sales'
ORDER BY table_name;

-- View schema owner
SELECT nspname AS schema_name, 
       pg_get_userbyid(nspowner) AS owner
FROM pg_namespace
WHERE nspname NOT LIKE 'pg_%';
```

### Renaming and Dropping Schemas

```sql
-- Rename a schema
ALTER SCHEMA old_name RENAME TO new_name;

-- Drop empty schema
DROP SCHEMA empty_schema;

-- Drop schema with all contents (CAREFUL!)
DROP SCHEMA obsolete_schema CASCADE;

-- Check if schema exists before dropping
DROP SCHEMA IF EXISTS maybe_exists;
```

## Code Example

Complete schema setup for an e-commerce application:

```sql
-- Create schemas for different domains
CREATE SCHEMA customers;
CREATE SCHEMA products;
CREATE SCHEMA orders;
CREATE SCHEMA analytics;

-- Create tables in appropriate schemas
CREATE TABLE customers.accounts (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products.items (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    inventory_count INTEGER DEFAULT 0
);

CREATE TABLE orders.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers.accounts(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2)
);

CREATE TABLE orders.order_items (
    order_id INTEGER REFERENCES orders.orders(order_id),
    product_id INTEGER REFERENCES products.items(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id)
);

-- Create analytics view
CREATE VIEW analytics.daily_sales AS
SELECT 
    DATE(order_date) AS sale_date,
    COUNT(*) AS order_count,
    SUM(total) AS total_sales
FROM orders.orders
GROUP BY DATE(order_date);

-- Set up roles and permissions
CREATE ROLE app_readonly;
GRANT USAGE ON SCHEMA customers, products, orders, analytics TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA customers TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA products TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA orders TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO app_readonly;
```

## Key Takeaways

- Use CREATE SCHEMA to create new schemas with optional ownership
- Design schemas around business domains or technical layers
- Manage the search path for convenient unqualified object access
- Use GRANT/REVOKE to control schema-level permissions
- Prefer organized schemas over cluttering the public schema

## Additional Resources

- [PostgreSQL CREATE SCHEMA](https://www.postgresql.org/docs/current/sql-createschema.html)
- [Schema Design Patterns](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Role-Based Access Control](https://www.postgresql.org/docs/current/ddl-priv.html)
