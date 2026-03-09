# Not Null

## Learning Objectives

- Understand the NOT NULL constraint
- Recognize when to require values
- Apply NOT NULL appropriately in table design
- Handle NULL vs empty string considerations

## Why This Matters

The NOT NULL constraint is one of the most frequently used constraints in database design. It ensures that essential columns always have a value, preventing incomplete records from entering your database. Understanding when to require data and when to allow NULL is fundamental to creating reliable database schemas.

## The Concept

### What is NOT NULL?

The **NOT NULL** constraint ensures that a column cannot contain NULL values. Every row must have a value for that column.

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,  -- Required
    last_name VARCHAR(50) NOT NULL,   -- Required
    middle_name VARCHAR(50)           -- Optional (NULL allowed)
);

-- Valid
INSERT INTO employees (first_name, last_name) VALUES ('John', 'Doe');

-- Invalid
INSERT INTO employees (first_name, last_name) VALUES (NULL, 'Doe');
-- ERROR: null value in column "first_name" violates not-null constraint
```

### NULL vs Empty String

NULL and empty string are different:

| Value | Meaning | Storage |
|-------|---------|---------|
| NULL | Unknown/missing | No storage |
| '' (empty) | Known to be empty | Stored as empty |

```sql
-- These are different!
INSERT INTO contacts (name, phone) VALUES ('Alice', NULL);   -- Phone unknown
INSERT INTO contacts (name, phone) VALUES ('Bob', '');       -- Has no phone

SELECT * FROM contacts WHERE phone IS NULL;      -- Returns Alice
SELECT * FROM contacts WHERE phone = '';         -- Returns Bob
```

### When to Use NOT NULL

**Always require**:

- Primary keys (automatic)
- Data essential for record identity
- Foreign keys (usually)
- Fields the business logic depends on

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,           -- Auto NOT NULL
    customer_id INTEGER NOT NULL,          -- Must have customer
    order_date DATE NOT NULL,              -- Must have date
    status VARCHAR(20) NOT NULL,           -- Must have status
    shipping_address TEXT,                 -- Optional
    notes TEXT                             -- Optional
);
```

**Allow NULL for**:

- Optional information
- Data not yet available
- Fields with no applicable value

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    description TEXT,              -- Optional
    weight DECIMAL(10,2),          -- N/A for digital products
    discontinued_date DATE         -- NULL if still active
);
```

### Adding NOT NULL Constraint

**On Table Creation**:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

**To Existing Column**:

```sql
-- First, handle existing NULLs
UPDATE customers SET name = 'Unknown' WHERE name IS NULL;

-- Then add constraint
ALTER TABLE customers ALTER COLUMN name SET NOT NULL;
```

**Removing NOT NULL**:

```sql
ALTER TABLE customers ALTER COLUMN name DROP NOT NULL;
```

### NOT NULL with Default Values

Combine NOT NULL with DEFAULT to ensure valid data:

```sql
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    view_count INTEGER NOT NULL DEFAULT 0
);

-- Insert without specifying defaults
INSERT INTO articles (title) VALUES ('My First Article');
-- status = 'draft', created_at = now, view_count = 0
```

### Best Practices

**1. Be explicit**:

```sql
-- Clearly show intent
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL,      -- Explicitly required
    phone VARCHAR(20) NULL            -- Explicitly optional
);
```

**2. Validate at schema level, not just application**:

```sql
-- Database enforces the rule; application cannot skip it
email VARCHAR(100) NOT NULL
```

**3. Use NOT NULL for foreign keys (usually)**:

```sql
-- Mandatory relationship
customer_id INTEGER NOT NULL REFERENCES customers(customer_id)

-- Optional relationship
referrer_id INTEGER REFERENCES users(user_id)  -- NULL if no referrer
```

### Common Mistakes

**Mistake 1**: Making everything NOT NULL

```sql
-- Too restrictive
CREATE TABLE contacts (
    middle_name VARCHAR(50) NOT NULL,  -- Many people don't have middle names!
);
```

**Mistake 2**: Not considering data entry order

```sql
-- shipping_address might not be known at order creation
CREATE TABLE orders (
    shipping_address TEXT NOT NULL  -- Might need to allow NULL initially
);
```

## Code Example

Practical NOT NULL usage:

```sql
-- User registration system
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    -- Required fields (NOT NULL)
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Optional fields (NULL allowed)
    display_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    last_login TIMESTAMP
);

-- Insert with minimal required data
INSERT INTO users (username, email, password_hash)
VALUES ('john_doe', 'john@email.com', 'hashed_password_here');

-- Verify the row
SELECT * FROM users WHERE username = 'john_doe';

-- Try inserting without required field
INSERT INTO users (username, password_hash)
VALUES ('jane_doe', 'another_hash');
-- ERROR: null value in column "email" violates not-null constraint

-- Update optional fields later
UPDATE users 
SET display_name = 'John D.', phone = '555-1234'
WHERE username = 'john_doe';

-- Find users missing optional data
SELECT username, email
FROM users
WHERE display_name IS NULL OR phone IS NULL;

-- Add NOT NULL to existing column
-- Step 1: Fill in missing values
UPDATE users SET display_name = username WHERE display_name IS NULL;
-- Step 2: Add constraint
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
```

## Key Takeaways

- NOT NULL ensures columns always have a value
- Use for required, essential data fields
- Allow NULL for optional or unknown information
- Combine with DEFAULT for automatic value assignment
- NULL and empty string are different concepts

## Additional Resources

- [PostgreSQL NOT NULL](https://www.postgresql.org/docs/current/ddl-constraints.html#id-1.5.4.6.6)
- [Working with NULL](https://www.postgresql.org/docs/current/functions-comparison.html)
- [Default Values](https://www.postgresql.org/docs/current/ddl-default.html)
