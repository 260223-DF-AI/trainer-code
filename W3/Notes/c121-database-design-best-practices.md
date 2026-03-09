# Database Design Best Practices

## Learning Objectives

- Apply best practices for database schema design
- Recognize common design mistakes
- Implement robust, maintainable database structures
- Balance theory with practical considerations

## Why This Matters

Good database design prevents problems before they occur. Poor design leads to performance issues, data quality problems, and maintenance nightmares. The principles covered in this topic synthesize everything you have learned this week into actionable guidelines for creating professional-quality database schemas.

## The Concept

### Core Design Principles

```
+------------------------------------------------------------------+
|                   DATABASE DESIGN PRINCIPLES                      |
+------------------------------------------------------------------+
|  1. Normalize to 3NF (then denormalize if needed)                 |
|  2. Use meaningful, consistent naming                             |
|  3. Define all constraints explicitly                             |
|  4. Choose appropriate data types                                 |
|  5. Plan for growth and change                                    |
|  6. Document your design                                          |
+------------------------------------------------------------------+
```

### Naming Conventions

**Tables**:

```sql
-- Good: Plural, lowercase, underscores
CREATE TABLE customers (...);
CREATE TABLE order_items (...);
CREATE TABLE user_profiles (...);

-- Avoid: Mixed case, abbreviations, singular
CREATE TABLE Customer (...);
CREATE TABLE ord_itm (...);
CREATE TABLE tblUsers (...);
```

**Columns**:

```sql
-- Good: Descriptive, lowercase, underscores
customer_id, first_name, created_at, is_active

-- Avoid: Vague, inconsistent
id, fname, created, active  -- Too short
CustomerFirstName  -- Mixed case
```

**Convention patterns**:

| Object Type | Pattern | Example |
|-------------|---------|---------|
| Primary Key | table_id | customer_id |
| Foreign Key | referenced_table_id | customer_id |
| Boolean | is_*, has_* | is_active, has_shipped |
| Date/Time | *_at,*_date | created_at, order_date |
| Indexes | idx_table_column | idx_orders_customer |
| Constraints | pk_, fk_, uq_, chk_ | pk_orders, fk_orders_customer |

### Data Type Selection

**Use appropriate sizes**:

```sql
-- Good: Sized appropriately
first_name VARCHAR(50),      -- Names rarely exceed 50
country_code CHAR(2),        -- ISO codes are exactly 2
price DECIMAL(10, 2),        -- Currency needs precision
event_id BIGSERIAL,          -- High-volume table

-- Avoid: Oversized or wrong type
name VARCHAR(10000),         -- Wasting space
price FLOAT,                 -- Precision issues for money
age VARCHAR(10),             -- Use INTEGER
```

**Common mappings**:

| Data | Recommended Type |
|------|------------------|
| Money/Currency | DECIMAL(10,2) or NUMERIC |
| Identifiers | SERIAL, BIGSERIAL, or UUID |
| Boolean flags | BOOLEAN |
| Short text (fixed) | CHAR(n) |
| Short text (variable) | VARCHAR(n) |
| Long text | TEXT |
| Dates | DATE |
| Timestamps | TIMESTAMP or TIMESTAMPTZ |
| JSON data | JSONB |

### Always Define Constraints

**Be explicit about all rules**:

```sql
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    
    -- Named constraints
    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) ON DELETE RESTRICT,
    CONSTRAINT chk_orders_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered')),
    CONSTRAINT chk_orders_positive_total CHECK (total >= 0)
);
```

### Avoid Common Mistakes

**1. Missing indexes on foreign keys**:

```sql
-- FK creates relationship but NOT an index
ALTER TABLE orders ADD CONSTRAINT fk_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- Add index separately for JOIN performance
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**2. Storing calculated values unnecessarily**:

```sql
-- Avoid: Storing what can be calculated
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    subtotal DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    total DECIMAL(10, 2)  -- This is subtotal + tax!
);

-- Better: Calculate when needed or use generated column
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    subtotal DECIMAL(10, 2),
    tax_rate DECIMAL(5, 4),
    total DECIMAL(10, 2) GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) STORED
);
```

**3. Using the wrong relationship type**:

```sql
-- Mistake: Many products in one cell
CREATE TABLE orders (
    product_list VARCHAR(500)  -- "1,2,3,4"
);

-- Correct: Junction table
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

**4. No audit trail**:

```sql
-- Always include tracking columns
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    -- Audit columns
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER
);
```

### Plan for Change

**Use soft deletes**:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,  -- Soft delete: set to FALSE
    deleted_at TIMESTAMP             -- When it was "deleted"
);

-- Don't actually delete
UPDATE products SET is_active = FALSE, deleted_at = NOW() WHERE product_id = 1;

-- All queries filter for active
SELECT * FROM products WHERE is_active = TRUE;
```

**Version sensitive data**:

```sql
CREATE TABLE price_history (
    price_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    price DECIMAL(10, 2),
    effective_from DATE NOT NULL,
    effective_to DATE,
    CONSTRAINT valid_date_range CHECK (effective_to IS NULL OR effective_to >= effective_from)
);
```

### Documentation

**Comment objects**:

```sql
COMMENT ON TABLE orders IS 'Customer purchase orders';
COMMENT ON COLUMN orders.status IS 'Order lifecycle status: pending, processing, shipped, delivered';
COMMENT ON CONSTRAINT chk_orders_status ON orders IS 'Restricts status to valid values';
```

**Maintain entity relationship diagrams (ERDs)**.

## Code Example

Well-designed schema example:

```sql
-- Domain enums for type safety
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE TYPE user_role AS ENUM ('customer', 'admin', 'support');

-- Core tables with all best practices
CREATE TABLE users (
    user_id SERIAL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role user_role NOT NULL DEFAULT 'customer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_users PRIMARY KEY (user_id),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT chk_users_email_format CHECK (email LIKE '%@%.%')
);
COMMENT ON TABLE users IS 'Application user accounts';

CREATE TABLE customers (
    customer_id SERIAL,
    user_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id),
    CONSTRAINT fk_customers_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT uq_customers_user UNIQUE (user_id)
);
CREATE INDEX idx_customers_user ON customers(user_id);

CREATE TABLE orders (
    order_id SERIAL,
    customer_id INTEGER NOT NULL,
    status order_status NOT NULL DEFAULT 'pending',
    subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
    tax DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    ordered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT chk_orders_positive_amounts CHECK (subtotal >= 0 AND tax >= 0 AND total >= 0),
    CONSTRAINT chk_orders_total CHECK (total = subtotal + tax)
);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status != 'delivered';

-- View for common query pattern
CREATE VIEW active_orders AS
SELECT 
    o.order_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    u.email,
    o.status,
    o.total,
    o.ordered_at
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN users u ON c.user_id = u.user_id
WHERE o.status NOT IN ('delivered', 'cancelled');

COMMENT ON VIEW active_orders IS 'Orders requiring attention (not delivered or cancelled)';
```

## Key Takeaways

- Follow consistent naming conventions throughout your schema
- Choose appropriate data types; avoid over-sizing
- Define all constraints explicitly with meaningful names
- Index foreign key columns for JOIN performance
- Include audit columns (created_at, updated_at) on all tables
- Use soft deletes and versioning for sensitive data
- Document your schema with comments

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/index.html)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)
- [Naming Conventions](https://www.postgresql.org/docs/current/sql-syntax-lexical.html)
