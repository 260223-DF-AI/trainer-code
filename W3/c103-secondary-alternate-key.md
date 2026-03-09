# Secondary and Alternate Keys

## Learning Objectives

- Understand candidate keys and key selection
- Differentiate between primary, alternate, and secondary keys
- Recognize the importance of alternate keys in design
- Apply secondary keys for query optimization

## Why This Matters

Not every potential unique identifier becomes the primary key. Understanding terminology around candidate keys, alternate keys, and secondary keys helps you communicate with database professionals and make informed design decisions. These concepts also affect how you index and query your data.

## The Concept

### Key Terminology

```
+------------------------------------------------------------------+
|                       KEY HIERARCHY                               |
+------------------------------------------------------------------+
|                                                                    |
|  CANDIDATE KEYS (all columns/sets that COULD be primary key)      |
|       |                                                            |
|       +----> PRIMARY KEY (the chosen one)                         |
|       |                                                            |
|       +----> ALTERNATE KEYS (candidate keys not chosen)           |
|                                                                    |
|  SECONDARY KEYS (columns indexed for frequent searches)           |
|                                                                    |
+------------------------------------------------------------------+
```

### Candidate Keys

A **candidate key** is any column or set of columns that could serve as the primary key:

- Uniquely identifies each row
- Contains no NULL values
- Is minimal (no subset could also be a key)

```sql
-- This table has multiple candidate keys:
CREATE TABLE employees (
    employee_id SERIAL,      -- Candidate key (chosen as PK)
    ssn CHAR(11) UNIQUE,     -- Candidate key (alternate)
    email VARCHAR(100) UNIQUE, -- Candidate key (alternate)
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);
-- employee_id, ssn, and email could each uniquely identify rows
```

### Primary Key Selection

From candidate keys, one is chosen as the primary key. Selection criteria:

| Factor | Preference |
|--------|------------|
| Stability | Values that never change |
| Simplicity | Single column over composite |
| Size | Smaller data types |
| Meaningless | Surrogate over natural keys |
| Automation | Auto-generated preferred |

```sql
-- Usually choose surrogate key as primary
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,  -- Chosen: auto-generated, never changes
    ssn CHAR(11) UNIQUE NOT NULL,    -- Alternate: could change, privacy concerns
    email VARCHAR(100) UNIQUE        -- Alternate: likely to change
);
```

### Alternate Keys

**Alternate keys** are candidate keys that were not selected as the primary key. They are typically implemented as UNIQUE constraints:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,   -- Surrogate key (chosen)
    sku VARCHAR(20) UNIQUE NOT NULL, -- Alternate key (business identifier)
    upc CHAR(12) UNIQUE,             -- Alternate key (universal product code)
    name VARCHAR(100)
);

-- Both sku and upc uniquely identify products
-- product_id was chosen for internal consistency
```

### Secondary Keys (Search Keys)

**Secondary keys** are columns that are indexed for frequent searching but do not enforce uniqueness. They optimize query performance:

```sql
-- Secondary keys are created with indexes
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(20)
);

-- Secondary indexes for common searches
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);

-- These are "secondary keys" - used for searching, not uniqueness
```

### Natural vs Surrogate as Primary Key

**Natural Key** (Use business data):

```sql
CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY,  -- ISO code is natural key
    country_name VARCHAR(100) NOT NULL
);
-- Pro: Meaningful, already unique
-- Con: Could change (country codes have changed historically)
```

**Surrogate Key** (Generate artificial):

```sql
CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_code CHAR(2) UNIQUE NOT NULL,  -- Now an alternate key
    country_name VARCHAR(100) NOT NULL
);
-- Pro: Never changes, simple, consistent
-- Con: Requires joining to get meaningful identifier
```

### When to Use Each

**Choose Surrogate Primary Key when**:

- Natural keys might change
- Natural keys are large (long strings)
- Business doesn't have guaranteed unique identifier
- Consistency across tables is important

**Keep Natural Key as Primary when**:

- Key is truly stable (ISO codes, etc.)
- Key is small and simple
- External systems require the key
- Lookup tables where meaning is the point

### Composite Alternate Keys

Sometimes multiple columns together form an alternate key:

```sql
CREATE TABLE employee_certifications (
    certification_id SERIAL PRIMARY KEY,  -- Surrogate
    employee_id INTEGER NOT NULL,
    certification_type VARCHAR(50) NOT NULL,
    issue_date DATE,
    expiry_date DATE,
    -- Alternate key: employee can have only one of each cert type
    UNIQUE (employee_id, certification_type)
);
```

## Code Example

Demonstrating different key types:

```sql
-- Create table with multiple candidate keys
CREATE TABLE students (
    -- Primary Key (chosen)
    student_id SERIAL PRIMARY KEY,
    
    -- Alternate Keys (other candidates)
    ssn CHAR(11) UNIQUE,           -- Could be PK but privacy concerns
    student_email VARCHAR(100) UNIQUE NOT NULL,  -- Could be PK but changes
    
    -- Regular attributes
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    enrollment_date DATE,
    major VARCHAR(50)
);

-- Secondary Keys (indexes for searching)
CREATE INDEX idx_students_name ON students(last_name, first_name);
CREATE INDEX idx_students_major ON students(major);
CREATE INDEX idx_students_enrollment ON students(enrollment_date);

-- Insert some data
INSERT INTO students (ssn, student_email, first_name, last_name, major) VALUES
    ('111-22-3333', 'alice@univ.edu', 'Alice', 'Johnson', 'Computer Science'),
    ('222-33-4444', 'bob@univ.edu', 'Bob', 'Smith', 'Mathematics'),
    ('333-44-5555', 'carol@univ.edu', 'Carol', 'Williams', 'Computer Science');

-- Query using primary key (fast, unique)
SELECT * FROM students WHERE student_id = 1;

-- Query using alternate key (fast, unique)
SELECT * FROM students WHERE student_email = 'alice@univ.edu';
SELECT * FROM students WHERE ssn = '111-22-3333';

-- Query using secondary key (fast, may return multiple)
SELECT * FROM students WHERE major = 'Computer Science';
SELECT * FROM students WHERE last_name = 'Smith';

-- Query without index (slower on large tables)
SELECT * FROM students WHERE first_name = 'Alice';
-- Note: We have index on (last_name, first_name) but this query
-- cannot use it efficiently because first_name is second in the index

-- View indexes on table
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'students';
```

## Key Takeaways

- Candidate keys are all columns that could uniquely identify rows
- Primary key is the chosen candidate key
- Alternate keys are candidate keys not selected as primary
- Secondary keys are indexed columns for search optimization
- Most tables use surrogate primary keys with natural alternate keys

## Additional Resources

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Key Types in Database Design](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Index Selection](https://www.postgresql.org/docs/current/indexes-types.html)
