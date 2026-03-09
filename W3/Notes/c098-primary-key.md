# Primary Key

## Learning Objectives

- Define what a primary key is and why it's essential
- Understand the properties of primary keys
- Choose appropriate primary key strategies
- Implement primary keys in table definitions

## Why This Matters

Every table needs a way to uniquely identify each row. The primary key serves this purpose, acting as the "address" for each record in your database. Without primary keys, you cannot reliably update specific records, establish relationships between tables, or ensure data integrity. Understanding primary keys is fundamental to proper database design.

## The Concept

### What is a Primary Key?

A **primary key** is a column (or set of columns) that uniquely identifies each row in a table. It enforces two rules:

1. **Uniqueness**: No two rows can have the same primary key value
2. **Not NULL**: Primary key columns cannot contain NULL values

### Primary Key Properties

```
+------------------------------------------------------------------+
|                       PRIMARY KEY RULES                           |
+------------------------------------------------------------------+
|  1. Must be UNIQUE - no duplicates allowed                        |
|  2. Must be NOT NULL - every row must have a value                |
|  3. Should be IMMUTABLE - value should not change                 |
|  4. Should be MINIMAL - use fewest columns necessary              |
+------------------------------------------------------------------+
```

### Creating Primary Keys

**Single Column Primary Key**:

```sql
-- Method 1: Inline with column
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

-- Method 2: As table constraint
CREATE TABLE products (
    product_id INTEGER NOT NULL,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    PRIMARY KEY (product_id)
);

-- Method 3: Named constraint
CREATE TABLE orders (
    order_id INTEGER NOT NULL,
    order_date DATE,
    CONSTRAINT pk_orders PRIMARY KEY (order_id)
);
```

**Adding Primary Key to Existing Table**:

```sql
ALTER TABLE customers ADD PRIMARY KEY (customer_id);

-- Or with a named constraint
ALTER TABLE customers 
    ADD CONSTRAINT pk_customers PRIMARY KEY (customer_id);
```

### Primary Key Strategies

**1. Natural Keys**:
Use existing business data as the key.

```sql
-- Social Security Number (US)
CREATE TABLE tax_records (
    ssn CHAR(11) PRIMARY KEY,  -- 111-22-3333
    name VARCHAR(100),
    income DECIMAL(12, 2)
);

-- ISBN for books
CREATE TABLE books (
    isbn CHAR(13) PRIMARY KEY,
    title VARCHAR(200),
    author VARCHAR(100)
);

-- Email (if truly unique)
CREATE TABLE user_accounts (
    email VARCHAR(100) PRIMARY KEY,
    password_hash TEXT,
    created_at TIMESTAMP
);
```

**Pros**: Meaningful, already unique
**Cons**: Can change, may have exceptions, privacy concerns

**2. Surrogate Keys**:
Generate artificial keys specifically for identification.

```sql
-- Auto-incrementing integer
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- UUID
CREATE TABLE sessions (
    session_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INTEGER,
    created_at TIMESTAMP
);

-- BIGINT for large tables
CREATE TABLE events (
    event_id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    event_data JSONB
);
```

**Pros**: Never changes, compact, no business meaning to dispute
**Cons**: Extra column, no inherent meaning

### SERIAL vs UUID

| Aspect | SERIAL/BIGSERIAL | UUID |
|--------|------------------|------|
| Size | 4/8 bytes | 16 bytes |
| Readability | Human-readable | Long hex string |
| Sequential | Yes | No |
| Guessable | Yes | No |
| Global uniqueness | Per table | Universal |
| Insert performance | Better | Slightly slower |
| Index size | Smaller | Larger |

### Primary Key Best Practices

1. **Use surrogate keys for most tables**:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,  -- Not order number or date
    order_number VARCHAR(20) UNIQUE,  -- Business identifier
    order_date DATE
);
```

1. **Keep primary keys short**:

```sql
-- Good: Single integer
PRIMARY KEY (product_id)

-- Less ideal: Long composite key
PRIMARY KEY (region, year, category, sequence_number)
```

1. **Never reuse primary key values**:

```sql
-- If you delete row with ID 5, don't reassign ID 5 to a new row
```

1. **Use naming conventions**:

```sql
-- Consistent naming: tablename_id
customer_id, order_id, product_id
```

### Viewing Primary Keys

```sql
-- See table constraints including primary key
\d employees

-- Query system catalog
SELECT 
    constraint_name,
    column_name
FROM information_schema.key_column_usage
WHERE table_name = 'employees';

-- List all primary keys in schema
SELECT 
    tc.table_name,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'PRIMARY KEY'
    AND tc.table_schema = 'public';
```

## Code Example

Implementing primary keys:

```sql
-- Table with SERIAL primary key
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- Table with natural key (use carefully)
CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50)
);

-- Table with UUID primary key
CREATE TABLE api_tokens (
    token_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Insert and verify uniqueness
INSERT INTO departments (department_name, location) VALUES
    ('Engineering', 'Building A'),
    ('Marketing', 'Building B'),
    ('Sales', 'Building C');

SELECT * FROM departments;
-- department_id | department_name | location
-- 1             | Engineering     | Building A
-- 2             | Marketing       | Building B
-- 3             | Sales           | Building C

-- Try to insert duplicate (will fail)
INSERT INTO departments (department_id, department_name) 
VALUES (1, 'Duplicate');
-- ERROR: duplicate key value violates unique constraint "departments_pkey"

-- Try NULL primary key (will fail)
INSERT INTO departments (department_id, department_name) 
VALUES (NULL, 'No ID');
-- ERROR: null value in column "department_id" violates not-null constraint
```

## Key Takeaways

- Primary keys uniquely identify each row in a table
- They enforce uniqueness and NOT NULL constraints
- Surrogate keys (SERIAL, UUID) are preferred over natural keys
- Choose appropriate data type based on table size and access patterns
- Primary keys should never change once assigned

## Additional Resources

- [PostgreSQL PRIMARY KEY](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
- [UUID Generation](https://www.postgresql.org/docs/current/functions-uuid.html)
- [SERIAL Types](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-SERIAL)
