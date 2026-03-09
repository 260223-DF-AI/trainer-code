# Foreign Key

## Learning Objectives

- Understand foreign keys and their role in relationships
- Create foreign key constraints
- Apply CASCADE options appropriately
- Recognize foreign key best practices

## Why This Matters

Foreign keys are the glue that connects your tables. They enforce relationships between data and prevent orphaned records. Without foreign keys, you could have orders pointing to customers that do not exist, or invoices for products that were deleted. Foreign key constraints are essential for maintaining data integrity in relational databases.

## The Concept

### What is a Foreign Key?

A **foreign key** is a column (or columns) in one table that references the primary key of another table. It creates a parent-child relationship between tables.

```
    PARENT TABLE                    CHILD TABLE
+------------------+           +------------------+
|   customers      |           |     orders       |
+------------------+           +------------------+
| customer_id (PK) |<--------->| order_id (PK)    |
| name             |     |     | customer_id (FK) |
| email            |     |     | order_date       |
+------------------+     |     | total            |
                         |     +------------------+
                         |
            Foreign Key References Primary Key
```

### Foreign Key Rules

1. **Referential Integrity**: FK value must exist in the parent table or be NULL
2. **Type Match**: FK column type must match PK column type
3. **Cannot Delete Referenced**: Parent rows cannot be deleted if children reference them (by default)

### Creating Foreign Keys

**Method 1: Inline Definition**:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE
);
```

**Method 2: Table Constraint**:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Method 3: Named Constraint**:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE,
    CONSTRAINT fk_orders_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
);
```

**Adding FK to Existing Table**:

```sql
ALTER TABLE orders 
    ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customer_id) 
    REFERENCES customers(customer_id);
```

### CASCADE Options

What happens when you update or delete a parent row?

| Option | On Delete | On Update |
|--------|-----------|-----------|
| NO ACTION | Error (default) | Error (default) |
| RESTRICT | Error (checked immediately) | Error |
| CASCADE | Delete children too | Update children too |
| SET NULL | Set FK to NULL | Set FK to NULL |
| SET DEFAULT | Set FK to default | Set FK to default |

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- CASCADE delete example
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) 
        REFERENCES orders(order_id)
        ON DELETE CASCADE  -- Delete items when order is deleted
);
```

### When to Use Each CASCADE Option

**NO ACTION/RESTRICT**: Default, safest

```sql
-- Prevent accidental deletions
FOREIGN KEY (department_id) REFERENCES departments(department_id)
-- Must explicitly reassign/delete children first
```

**CASCADE**: Logical parent-child ownership

```sql
-- Order items belong to order
FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE

-- Comments belong to post
FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
```

**SET NULL**: Optional relationship

```sql
-- Employee leaves, keep their created records but clear reference
FOREIGN KEY (created_by) REFERENCES employees(employee_id) ON DELETE SET NULL
```

**SET DEFAULT**: Replace with fallback value

```sql
-- Products: if category deleted, set to 'Uncategorized' (ID = 1)
category_id INTEGER DEFAULT 1,
FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET DEFAULT
```

### Multi-Column Foreign Keys

When referencing a composite primary key:

```sql
-- Parent with composite key
CREATE TABLE store_inventory (
    store_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (store_id, product_id)
);

-- Child referencing composite key
CREATE TABLE inventory_adjustments (
    adjustment_id SERIAL PRIMARY KEY,
    store_id INTEGER,
    product_id INTEGER,
    adjustment_qty INTEGER,
    adjustment_date DATE,
    FOREIGN KEY (store_id, product_id) 
        REFERENCES store_inventory(store_id, product_id)
);
```

### Self-Referencing Foreign Keys

A table can reference itself:

```sql
-- Employee hierarchy (manager is also an employee)
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INTEGER REFERENCES employees(employee_id)
);

-- Organization chart
INSERT INTO employees (name, manager_id) VALUES
    ('CEO', NULL),         -- No manager
    ('VP Sales', 1),       -- Reports to CEO
    ('VP Engineering', 1), -- Reports to CEO
    ('Sales Rep', 2);      -- Reports to VP Sales
```

### Viewing Foreign Keys

```sql
-- Using psql
\d orders

-- Query system catalog
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
    ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name = 'orders';
```

## Code Example

Complete foreign key implementation:

```sql
-- Parent tables
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- Child table with foreign keys
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER,
    price DECIMAL(10, 2),
    CONSTRAINT fk_products_category 
        FOREIGN KEY (category_id) 
        REFERENCES categories(category_id)
        ON DELETE SET NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending',
    CONSTRAINT fk_orders_customer 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT  -- Cannot delete customer with orders
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2),
    CONSTRAINT fk_items_order 
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,  -- Delete items with order
    CONSTRAINT fk_items_product 
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT  -- Cannot delete product in orders
);

-- Insert parent data first
INSERT INTO categories (category_name) VALUES ('Electronics'), ('Clothing');
INSERT INTO customers (name, email) VALUES 
    ('Alice', 'alice@email.com'),
    ('Bob', 'bob@email.com');
INSERT INTO products (name, category_id, price) VALUES 
    ('Laptop', 1, 999.99),
    ('T-Shirt', 2, 29.99);

-- Insert child data
INSERT INTO orders (customer_id) VALUES (1);  -- Alice's order
INSERT INTO order_items (order_id, product_id, quantity, unit_price) 
VALUES (1, 1, 1, 999.99);

-- Try invalid FK (will fail)
INSERT INTO orders (customer_id) VALUES (999);
-- ERROR: insert or update on table "orders" violates foreign key constraint

-- Try to delete customer with order (will fail due to RESTRICT)
DELETE FROM customers WHERE customer_id = 1;
-- ERROR: update or delete on table "customers" violates foreign key constraint

-- Delete order (CASCADE deletes items too)
DELETE FROM orders WHERE order_id = 1;
-- order_items are automatically deleted
```

## Key Takeaways

- Foreign keys create relationships between tables
- They enforce referential integrity (no orphaned rows)
- CASCADE options control behavior on parent changes
- Choose appropriate ON DELETE/UPDATE actions based on business logic
- FK columns should be indexed for performance

## Additional Resources

- [PostgreSQL Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [Referential Integrity](https://www.postgresql.org/docs/current/tutorial-fk.html)
- [CASCADE Options](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
