# Consistency

## Learning Objectives

- Understand data consistency in relational databases
- Recognize types of consistency (transactional, eventual)
- Apply constraints to maintain consistency
- Identify consistency patterns in database design

## Why This Matters

Data consistency ensures your database always contains valid, accurate, and reliable information. Inconsistent data leads to incorrect reports, broken application logic, and lost trust. Understanding how databases maintain consistency helps you design robust systems and troubleshoot data quality issues.

## The Concept

### What is Data Consistency?

**Data consistency** means that data adheres to defined rules and constraints at all times. The database transitions from one valid state to another valid state, never existing in an invalid intermediate state (from the application's perspective).

### Types of Consistency

**1. Transactional Consistency (ACID)**:
Database guarantees consistency within transactions:

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Either both happen or neither does
```

**2. Referential Consistency**:
Foreign keys always point to existing records:

```sql
-- This fails if customer 999 doesn't exist
INSERT INTO orders (customer_id, total) VALUES (999, 100.00);
-- ERROR: violates foreign key constraint
```

**3. Domain Consistency**:
Values fall within acceptable ranges:

```sql
CREATE TABLE products (
    price DECIMAL(10, 2) CHECK (price >= 0),
    quantity INTEGER CHECK (quantity >= 0)
);
```

**4. Entity Consistency**:
Primary keys are unique and never null:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY  -- Unique and NOT NULL
);
```

### Consistency Threats

| Threat | Description | Prevention |
|--------|-------------|------------|
| Duplicate data | Same info stored multiple times | Primary/Unique keys |
| Orphaned records | Child without parent | Foreign keys |
| Invalid values | Out-of-range data | Check constraints |
| Conflicting updates | Race conditions | Transactions |
| Partial updates | Incomplete changes | ACID transactions |

### Maintaining Consistency with Constraints

**Not Null**:

```sql
CREATE TABLE customers (
    name VARCHAR(100) NOT NULL  -- Cannot be empty
);
```

**Check Constraints**:

```sql
CREATE TABLE employees (
    salary DECIMAL(10, 2) CHECK (salary > 0),
    age INTEGER CHECK (age >= 18 AND age <= 120),
    email VARCHAR(100) CHECK (email LIKE '%@%.%')
);
```

**Unique Constraints**:

```sql
CREATE TABLE accounts (
    email VARCHAR(100) UNIQUE
);
```

**Foreign Keys**:

```sql
CREATE TABLE orders (
    customer_id INTEGER REFERENCES customers(customer_id)
);
```

### Application-Level Consistency

Some consistency rules cannot be enforced by constraints alone:

```sql
-- Business rule: Order total must equal sum of line items
-- Cannot be enforced by simple constraint

-- Option 1: Trigger
CREATE OR REPLACE FUNCTION update_order_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders 
    SET total = (
        SELECT SUM(quantity * unit_price) 
        FROM order_items 
        WHERE order_id = NEW.order_id
    )
    WHERE order_id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_order_total
AFTER INSERT OR UPDATE ON order_items
FOR EACH ROW EXECUTE FUNCTION update_order_total();
```

### Consistency vs Availability

In distributed systems, there is a trade-off (CAP theorem):

- **Strong Consistency**: All nodes see the same data at the same time
- **Eventual Consistency**: Data will eventually be consistent across nodes

Traditional relational databases prioritize **strong consistency**. This is appropriate for:

- Financial transactions
- Inventory management
- User authentication

### Checking for Inconsistencies

```sql
-- Find orphaned orders (no customer)
SELECT o.order_id 
FROM orders o 
LEFT JOIN customers c ON o.customer_id = c.customer_id 
WHERE c.customer_id IS NULL;

-- Find orders with incorrect totals
SELECT o.order_id, o.total AS recorded_total, 
       SUM(oi.quantity * oi.unit_price) AS calculated_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.total
HAVING o.total != SUM(oi.quantity * oi.unit_price);

-- Find duplicate emails
SELECT email, COUNT(*) 
FROM customers 
GROUP BY email 
HAVING COUNT(*) > 1;
```

## Code Example

Building a consistent database:

```sql
-- Create tables with consistency constraints
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
    name VARCHAR(100) NOT NULL CHECK (LENGTH(name) >= 2)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (total >= 0)
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    PRIMARY KEY (order_id, product_id)
);

-- Test constraint enforcement
-- These should succeed:
INSERT INTO categories (name) VALUES ('Electronics');
INSERT INTO products (name, category_id, price, stock) VALUES ('Laptop', 1, 999.99, 10);

-- These should fail:
INSERT INTO products (name, category_id, price, stock) VALUES ('Invalid', 1, -10, 5);
-- ERROR: violates check constraint (price > 0)

INSERT INTO products (name, category_id, price, stock) VALUES ('Orphan', 999, 100, 5);
-- ERROR: violates foreign key constraint

-- Verify consistency
SELECT 
    table_name,
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'public'
ORDER BY table_name, constraint_type;
```

## Key Takeaways

- Consistency ensures data always follows defined rules
- Use constraints (PK, FK, UNIQUE, CHECK, NOT NULL) for enforcement
- Transactions maintain consistency during multi-step operations
- Foreign keys prevent orphaned records
- Some complex rules require triggers or application logic

## Additional Resources

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [ACID Properties](https://www.postgresql.org/docs/current/transaction-iso.html)
- [Data Integrity](https://www.postgresql.org/docs/current/ddl-constraints.html)
