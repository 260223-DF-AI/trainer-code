# Default

## Learning Objectives

- Understand DEFAULT constraints and their usage
- Apply different types of default values
- Use expressions and functions as defaults
- Recognize best practices for default values

## Why This Matters

Default values simplify data entry and ensure consistent initial states. Instead of requiring explicit values for every column, defaults automatically fill in common or initial values. This reduces code duplication in applications, prevents NULL values in columns that should have data, and documents the expected standard state of new records.

## The Concept

### What is a DEFAULT Constraint?

A **DEFAULT** constraint specifies the value to use when no value is provided during INSERT.

```sql
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert without specifying defaults
INSERT INTO articles (title) VALUES ('My First Article');
-- status = 'draft', view_count = 0, created_at = current time
```

### Types of Default Values

**Literal Values**:

```sql
status VARCHAR(20) DEFAULT 'pending'
quantity INTEGER DEFAULT 0
is_active BOOLEAN DEFAULT TRUE
price DECIMAL(10,2) DEFAULT 0.00
```

**Current Date/Time**:

```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
modified_at DATE DEFAULT CURRENT_DATE
created_time TIME DEFAULT CURRENT_TIME
```

**Function Results**:

```sql
-- UUID generation
id UUID DEFAULT gen_random_uuid()

-- Computed value
discount_rate NUMERIC DEFAULT 0.05
```

**NULL (Explicit)**:

```sql
-- Explicitly state NULL is the default
optional_field VARCHAR(100) DEFAULT NULL
```

### Column-Level DEFAULT

Applied directly in column definition:

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'member',
    credits INTEGER DEFAULT 100,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Adding/Modifying DEFAULT

```sql
-- Add default to existing column
ALTER TABLE products ALTER COLUMN status SET DEFAULT 'available';

-- Change existing default
ALTER TABLE products ALTER COLUMN status SET DEFAULT 'active';

-- Remove default
ALTER TABLE products ALTER COLUMN status DROP DEFAULT;
```

### DEFAULT with NOT NULL

Combine for guaranteed values:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- These are equivalent when inserting:
INSERT INTO orders DEFAULT VALUES;
INSERT INTO orders (status, priority, created_at) VALUES ('pending', 1, CURRENT_TIMESTAMP);
```

### Using DEFAULT in INSERT

**Explicit DEFAULT keyword**:

```sql
INSERT INTO products (name, price, quantity)
VALUES ('New Product', 29.99, DEFAULT);
-- quantity gets its default value
```

**INSERT DEFAULT VALUES**:

```sql
-- Insert row using all defaults (rarely useful)
INSERT INTO logs DEFAULT VALUES;
```

### Computed Defaults

Use expressions for dynamic defaults:

```sql
CREATE TABLE inventory (
    item_id SERIAL PRIMARY KEY,
    item_code VARCHAR(20) DEFAULT 'ITEM-' || to_char(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS'),
    expiry_date DATE DEFAULT CURRENT_DATE + INTERVAL '1 year',
    fiscal_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE)
);
```

### Sequences as Defaults

SERIAL is syntactic sugar for sequence + default:

```sql
-- SERIAL is equivalent to:
CREATE SEQUENCE products_product_id_seq;
CREATE TABLE products (
    product_id INTEGER DEFAULT nextval('products_product_id_seq')
);
ALTER SEQUENCE products_product_id_seq OWNED BY products.product_id;
```

### Best Practices

**1. Use meaningful defaults**:

```sql
-- Good: Status starts as pending
status VARCHAR(20) DEFAULT 'pending'

-- Avoid: Arbitrary default
status VARCHAR(20) DEFAULT 'x'
```

**2. Combine with NOT NULL for required defaults**:

```sql
is_active BOOLEAN NOT NULL DEFAULT TRUE
-- Cannot be NULL, defaults to TRUE
```

**3. Document business logic**:

```sql
-- New accounts get 30-day trial
trial_end_date DATE DEFAULT CURRENT_DATE + INTERVAL '30 days'
```

**4. Use for audit columns**:

```sql
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
created_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER
```

### GENERATED ALWAYS Columns

PostgreSQL 12+ supports generated columns:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2),
    tax_rate DECIMAL(5,4) DEFAULT 0.0825,
    price_with_tax DECIMAL(10,2) GENERATED ALWAYS AS (price * (1 + tax_rate)) STORED
);
-- price_with_tax is computed automatically
```

## Code Example

Comprehensive default usage:

```sql
-- E-commerce order system with defaults
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) DEFAULT 'ORD-' || to_char(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS'),
    customer_id INTEGER NOT NULL,
    
    -- Status and workflow
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Monetary (defaults to zero)
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    tax DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    shipping DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    
    -- Optional with no default (NULL)
    shipped_at TIMESTAMP,
    tracking_number VARCHAR(50),
    notes TEXT
);

-- Simple insert - most columns use defaults
INSERT INTO orders (customer_id) VALUES (101);

SELECT * FROM orders;

-- Insert with some explicit values
INSERT INTO orders (customer_id, priority, notes)
VALUES (102, 2, 'Rush order');

SELECT order_id, order_number, status, priority, created_at, notes
FROM orders;

-- Using DEFAULT keyword explicitly
INSERT INTO orders (customer_id, status, priority)
VALUES (103, DEFAULT, 3);  -- status defaults to 'pending'

-- View column defaults
SELECT column_name, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;

-- Modify a default
ALTER TABLE orders ALTER COLUMN priority SET DEFAULT 2;

-- New inserts use new default
INSERT INTO orders (customer_id) VALUES (104);
SELECT order_id, priority FROM orders WHERE customer_id = 104;
-- priority = 2
```

## Key Takeaways

- DEFAULT provides automatic values when none specified
- Combine with NOT NULL for guaranteed population
- Use CURRENT_TIMESTAMP, CURRENT_DATE for tracking
- Can use expressions and functions for computed defaults
- GENERATED ALWAYS creates automatically computed columns

## Additional Resources

- [PostgreSQL DEFAULT](https://www.postgresql.org/docs/current/ddl-default.html)
- [Generated Columns](https://www.postgresql.org/docs/current/ddl-generated-columns.html)
- [ALTER TABLE SET DEFAULT](https://www.postgresql.org/docs/current/sql-altertable.html)
