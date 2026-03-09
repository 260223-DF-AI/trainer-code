# Unique Key

## Learning Objectives

- Understand unique constraints and their purpose
- Differentiate unique keys from primary keys
- Implement unique constraints on single and multiple columns
- Apply unique constraints appropriately

## Why This Matters

While primary keys ensure each row has a unique identifier, you often need to enforce uniqueness on other columns as well. Email addresses, usernames, SKU codes, and social security numbers all need to be unique but are not primary keys. Unique constraints prevent duplicate values and are essential for data quality.

## The Concept

### What is a Unique Key?

A **unique key** (or unique constraint) ensures that all values in a column or set of columns are distinct. Unlike primary keys:

- A table can have multiple unique keys
- Unique key columns can contain NULL (usually just one NULL per column)

### Unique vs Primary Key

| Aspect | Primary Key | Unique Key |
|--------|-------------|------------|
| Count per table | Only one | Multiple allowed |
| NULL values | Never allowed | Usually one NULL allowed |
| Purpose | Row identification | Prevent duplicates |
| Implicit index | Yes | Yes |
| Required | One recommended | Optional |

### Creating Unique Constraints

**Method 1: Column Constraint**:

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE
);
```

**Method 2: Table Constraint**:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    sku VARCHAR(20),
    UNIQUE (sku)
);
```

**Method 3: Named Constraint**:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    ssn CHAR(11),
    CONSTRAINT unique_employee_email UNIQUE (email),
    CONSTRAINT unique_employee_ssn UNIQUE (ssn)
);
```

**Adding to Existing Table**:

```sql
ALTER TABLE customers ADD CONSTRAINT unique_email UNIQUE (email);
ALTER TABLE products ADD UNIQUE (sku);
```

### Composite Unique Keys

Enforce uniqueness across multiple columns:

```sql
-- User can have one subscription per service
CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    service_id INTEGER,
    start_date DATE,
    UNIQUE (user_id, service_id)  -- Combination must be unique
);

-- Insert works
INSERT INTO subscriptions (user_id, service_id) VALUES (1, 10);
INSERT INTO subscriptions (user_id, service_id) VALUES (1, 20);  -- OK, different service
INSERT INTO subscriptions (user_id, service_id) VALUES (2, 10);  -- OK, different user

-- Violates unique constraint
INSERT INTO subscriptions (user_id, service_id) VALUES (1, 10);
-- ERROR: duplicate key value violates unique constraint
```

### NULL Handling in Unique Constraints

PostgreSQL allows multiple NULLs in unique columns (because NULL != NULL):

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE  -- NULLs are special
);

INSERT INTO customers (email) VALUES ('alice@email.com');
INSERT INTO customers (email) VALUES (NULL);  -- OK
INSERT INTO customers (email) VALUES (NULL);  -- Also OK! NULLs don't violate unique

INSERT INTO customers (email) VALUES ('alice@email.com');
-- ERROR: duplicate key value violates unique constraint
```

If you want only one NULL, use a partial unique index:

```sql
CREATE UNIQUE INDEX unique_email_not_null 
ON customers (email) 
WHERE email IS NOT NULL;
```

### Common Use Cases

**User Accounts**:

```sql
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE  -- Optional, can be NULL
);
```

**Product Catalogs**:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(20) UNIQUE NOT NULL,
    upc CHAR(12) UNIQUE,  -- Universal Product Code
    name VARCHAR(100)
);
```

**Configuration Tables**:

```sql
CREATE TABLE app_config (
    config_id SERIAL PRIMARY KEY,
    config_key VARCHAR(50) UNIQUE NOT NULL,
    config_value TEXT
);
```

### Unique Index vs Unique Constraint

These are functionally equivalent:

```sql
-- Unique constraint (preferred for documentation)
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);

-- Unique index (same enforcement)
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

Constraints are clearer for data modeling; indexes offer more options (partial indexes, expressions).

### Handling Unique Violations

**Check Before Insert**:

```sql
-- Check if username exists before inserting
SELECT EXISTS(SELECT 1 FROM users WHERE username = 'newuser');
```

**Insert or Ignore (PostgreSQL)**:

```sql
-- ON CONFLICT DO NOTHING
INSERT INTO users (username, email) 
VALUES ('alice', 'alice@email.com')
ON CONFLICT (username) DO NOTHING;
```

**Insert or Update (Upsert)**:

```sql
-- ON CONFLICT DO UPDATE
INSERT INTO users (username, email) 
VALUES ('alice', 'newemail@email.com')
ON CONFLICT (username) 
DO UPDATE SET email = EXCLUDED.email;
```

## Code Example

Comprehensive unique constraint usage:

```sql
-- Create table with multiple unique constraints
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    referral_code CHAR(8),
    CONSTRAINT unique_username UNIQUE (username),
    CONSTRAINT unique_email UNIQUE (email),
    CONSTRAINT unique_phone UNIQUE (phone),
    CONSTRAINT unique_referral UNIQUE (referral_code)
);

-- Valid inserts
INSERT INTO members (username, email, phone, referral_code) 
VALUES ('alice', 'alice@email.com', '555-0001', 'REF00001');

INSERT INTO members (username, email, phone, referral_code) 
VALUES ('bob', 'bob@email.com', '555-0002', 'REF00002');

-- NULL phone is allowed (unique accepts NULL)
INSERT INTO members (username, email, referral_code) 
VALUES ('carol', 'carol@email.com', 'REF00003');

-- Another NULL phone is also allowed
INSERT INTO members (username, email, referral_code) 
VALUES ('dave', 'dave@email.com', 'REF00004');

-- Duplicate username fails
INSERT INTO members (username, email) VALUES ('alice', 'alice2@email.com');
-- ERROR: duplicate key value violates unique constraint "unique_username"

-- Duplicate email fails
INSERT INTO members (username, email) VALUES ('alice2', 'alice@email.com');
-- ERROR: duplicate key value violates unique constraint "unique_email"

-- View all constraints on table
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'members';

-- Upsert example: update email if username exists
INSERT INTO members (username, email, referral_code)
VALUES ('alice', 'alice_new@email.com', 'REF00005')
ON CONFLICT (username)
DO UPDATE SET email = EXCLUDED.email;
```

## Key Takeaways

- Unique constraints prevent duplicate values in columns
- Tables can have multiple unique constraints
- NULL values are typically allowed (multiple NULLs are distinct)
- Use composite unique keys for multi-column uniqueness
- ON CONFLICT handles unique violations gracefully

## Additional Resources

- [PostgreSQL Unique Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS)
- [Unique Indexes](https://www.postgresql.org/docs/current/indexes-unique.html)
- [INSERT ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
