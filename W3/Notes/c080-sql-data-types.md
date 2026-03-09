# SQL Data Types

## Learning Objectives

- Understand the importance of data types in SQL
- Learn common data types across different categories
- Recognize differences between database systems
- Choose appropriate data types for different scenarios

## Why This Matters

Selecting the correct data type is one of the most important decisions in database design. Data types affect storage efficiency, query performance, data integrity, and what operations are possible on your data. A poorly chosen data type can lead to bugs, wasted storage, or inability to perform necessary calculations.

## The Concept

### Why Data Types Matter

Data types serve several purposes:

1. **Validation**: Prevent invalid data entry
2. **Storage**: Optimize space usage
3. **Performance**: Enable efficient operations
4. **Semantics**: Convey meaning about the data

### Categories of SQL Data Types

SQL data types fall into these main categories:

```
+------------------------------------------------------------------+
|                        SQL DATA TYPES                             |
+------------------------------------------------------------------+
|           |           |           |           |                   |
|  Numeric  |  String   |   Date    |  Boolean  |  Special          |
|           |           |   /Time   |           |                   |
+-----------+-----------+-----------+-----------+-------------------+
| INTEGER   | CHAR      | DATE      | BOOLEAN   | JSON              |
| BIGINT    | VARCHAR   | TIME      |           | UUID              |
| DECIMAL   | TEXT      | TIMESTAMP |           | ARRAY             |
| REAL      |           | INTERVAL  |           | BYTEA             |
| DOUBLE    |           |           |           |                   |
+-----------+-----------+-----------+-----------+-------------------+
```

### Numeric Types

**Integer Types**:

| Type | Storage | Range |
|------|---------|-------|
| SMALLINT | 2 bytes | -32,768 to 32,767 |
| INTEGER (INT) | 4 bytes | -2.1 billion to 2.1 billion |
| BIGINT | 8 bytes | Very large integers |
| SERIAL | 4 bytes | Auto-incrementing integer |
| BIGSERIAL | 8 bytes | Auto-incrementing big integer |

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,      -- Auto-increment
    quantity INTEGER,                    -- Standard integers
    warehouse_id SMALLINT,              -- Small range values
    global_sku BIGINT                   -- Large identifiers
);
```

**Decimal/Floating Types**:

| Type | Description | Use Case |
|------|-------------|----------|
| DECIMAL(p, s) | Exact precision | Financial data |
| NUMERIC(p, s) | Same as DECIMAL | Money, exact math |
| REAL | 4-byte floating | Scientific data |
| DOUBLE PRECISION | 8-byte floating | Scientific data |

```sql
CREATE TABLE financial_records (
    amount DECIMAL(15, 2),   -- 15 total digits, 2 after decimal
    interest_rate NUMERIC(5, 4),  -- e.g., 0.0525 (5.25%)
    measurement REAL         -- Approximate scientific value
);

-- DECIMAL for money: 123456789012.34 (exact)
-- REAL for science: 3.14159 (approximate)
```

### String Types

| Type | Description | Use Case |
|------|-------------|----------|
| CHAR(n) | Fixed length | Codes, abbreviations |
| VARCHAR(n) | Variable length, max n | Names, addresses |
| TEXT | Unlimited length | Long descriptions |

```sql
CREATE TABLE customers (
    customer_code CHAR(10),      -- Always exactly 10 characters
    first_name VARCHAR(50),      -- Up to 50 characters
    last_name VARCHAR(50),
    bio TEXT                     -- Unlimited text
);
```

**When to use each**:

- `CHAR`: Fixed codes like state abbreviations ('CA', 'NY')
- `VARCHAR`: Most string data with known maximum
- `TEXT`: Large, variable content like articles or descriptions

### Date and Time Types

| Type | Description | Example |
|------|-------------|---------|
| DATE | Date only | '2024-01-15' |
| TIME | Time only | '14:30:00' |
| TIMESTAMP | Date and time | '2024-01-15 14:30:00' |
| TIMESTAMPTZ | With timezone | '2024-01-15 14:30:00-05' |
| INTERVAL | Duration | '1 year 2 months' |

```sql
CREATE TABLE events (
    event_date DATE,                                 -- Just the date
    start_time TIME,                                 -- Just the time
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date and time
    scheduled_at TIMESTAMPTZ                         -- With timezone
);

-- Working with dates
INSERT INTO events (event_date, start_time, scheduled_at)
VALUES ('2024-06-15', '09:00:00', '2024-06-15 09:00:00-04');
```

### Boolean Type

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);

-- Boolean values: TRUE, FALSE, NULL
INSERT INTO users (username, is_active, email_verified)
VALUES ('alice', TRUE, FALSE);

-- Query with boolean
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE is_active;  -- Shorthand
```

### Special Types (PostgreSQL)

```sql
-- UUID: Universally Unique Identifier
CREATE TABLE sessions (
    session_id UUID DEFAULT gen_random_uuid(),
    user_id INTEGER
);

-- JSON: Store JSON documents
CREATE TABLE api_logs (
    log_id SERIAL,
    request_data JSON,
    response_data JSONB  -- Binary JSON, faster queries
);

-- Array: Store multiple values
CREATE TABLE tags (
    post_id INTEGER,
    tag_list TEXT[]  -- Array of text
);
```

## Code Example

Comprehensive table using various data types:

```sql
CREATE TABLE employees (
    -- Identifiers
    employee_id SERIAL PRIMARY KEY,
    employee_uuid UUID DEFAULT gen_random_uuid(),
    
    -- Strings
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_code CHAR(4),
    bio TEXT,
    
    -- Numeric
    salary DECIMAL(10, 2),
    years_experience SMALLINT,
    
    -- Date/Time
    hire_date DATE NOT NULL,
    last_login TIMESTAMP,
    
    -- Boolean
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Special
    skills TEXT[],
    metadata JSONB
);

-- Insert with various data types
INSERT INTO employees (
    first_name, last_name, email, department_code,
    salary, hire_date, skills, metadata
) VALUES (
    'Alice', 'Johnson', 'alice@company.com', 'ENGR',
    85000.00, '2023-01-15',
    ARRAY['Python', 'SQL', 'Docker'],
    '{"level": "senior", "certifications": ["AWS", "GCP"]}'
);
```

## Key Takeaways

- Choose data types that match the nature and range of your data
- Use DECIMAL/NUMERIC for financial data requiring precision
- VARCHAR for variable text, CHAR for fixed codes
- TIMESTAMP for tracking dates and times
- PostgreSQL offers advanced types like UUID, JSON, and arrays

## Additional Resources

- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [Data Type Comparison Chart](https://www.postgresql.org/docs/current/datatype.html#DATATYPE-TABLE)
- [When to Use Which Data Type](https://wiki.postgresql.org/wiki/Don%27t_Do_This#Don.27t_use_char.28n.29)
