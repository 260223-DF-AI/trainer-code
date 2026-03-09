# Referential Integrity

## Learning Objectives

- Understand referential integrity and its importance
- Recognize how databases enforce integrity
- Handle integrity violations
- Apply integrity rules in database design

## Why This Matters

Referential integrity ensures your data remains consistent and connected. Without it, you could have orders for customers that do not exist, or invoices for deleted products. Referential integrity is the database's promise that relationships between tables remain valid. Understanding this concept is essential for building reliable systems.

## The Concept

### What is Referential Integrity?

**Referential integrity** is a property of data stating that all references are valid. In practice, this means:

- Every foreign key value must match an existing primary key value (or be NULL)
- No "orphaned" records can exist

```
VALID STATE:                        INVALID STATE (No RI):
+----------+     +----------+       +----------+     +----------+
| customers |     |  orders  |       | customers |     |  orders  |
+----------+     +----------+       +----------+     +----------+
| id: 1    |<----| cust: 1  |       | id: 1    |     | cust: 1  |
| id: 2    |<----| cust: 2  |       | id: 2    |     | cust: 2  |
|          |     | cust: 1  |       |          |     | cust: 99 | <- ORPHAN!
+----------+     +----------+       +----------+     +----------+
                                                         No customer 99!
```

### How Databases Enforce Referential Integrity

The database automatically enforces RI through foreign key constraints:

**1. On INSERT (Child Table)**:

```sql
-- Customer 99 doesn't exist
INSERT INTO orders (customer_id, total) VALUES (99, 100.00);
-- ERROR: insert or update on table "orders" violates foreign key constraint
-- DETAIL: Key (customer_id)=(99) is not present in table "customers"
```

**2. On UPDATE (Child Table)**:

```sql
-- Cannot change FK to non-existent value
UPDATE orders SET customer_id = 99 WHERE order_id = 1;
-- ERROR: violates foreign key constraint
```

**3. On DELETE (Parent Table)**:

```sql
-- Cannot delete parent with dependent children (default behavior)
DELETE FROM customers WHERE customer_id = 1;
-- ERROR: update or delete on table "customers" violates foreign key constraint
-- DETAIL: Key (customer_id)=(1) is still referenced from table "orders"
```

**4. On UPDATE (Parent Table)**:

```sql
-- Cannot change PK if children reference it (default behavior)
UPDATE customers SET customer_id = 100 WHERE customer_id = 1;
-- ERROR: cannot because orders table references this
```

### Handling Integrity Violations

When you need to make changes that would violate RI:

**Option 1: Handle Children First**:

```sql
-- Delete children, then parent
DELETE FROM order_items WHERE order_id = 1;
DELETE FROM orders WHERE order_id = 1;
DELETE FROM customers WHERE customer_id = 1;
```

**Option 2: Use CASCADE**:

```sql
-- Defined in schema
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
-- Children deleted automatically with parent
```

**Option 3: Set NULL**:

```sql
-- Defined in schema
FOREIGN KEY (manager_id) REFERENCES employees(employee_id) ON DELETE SET NULL
-- Children's FK becomes NULL when parent deleted
```

### Deferred Constraints

Sometimes you need to temporarily violate RI during complex operations:

```sql
-- Make constraint deferrable
ALTER TABLE orders 
    ADD CONSTRAINT fk_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    DEFERRABLE INITIALLY DEFERRED;

-- Now constraints are checked at COMMIT, not immediately
BEGIN;
    -- Insert order before customer (normally would fail!)
    INSERT INTO orders (order_id, customer_id, total) VALUES (100, 999, 50.00);
    -- Insert the customer
    INSERT INTO customers (customer_id, name) VALUES (999, 'New Customer');
COMMIT;  -- Constraints checked here - it passes because customer exists now
```

### Self-Referential Integrity

Tables can reference themselves:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INTEGER REFERENCES employees(employee_id)
);

-- CEO has no manager (NULL is allowed)
INSERT INTO employees (name, manager_id) VALUES ('CEO', NULL);

-- Manager must exist
INSERT INTO employees (name, manager_id) VALUES ('VP', 1);  -- OK
INSERT INTO employees (name, manager_id) VALUES ('VP', 99); -- ERROR
```

### Circular References

Sometimes tables reference each other:

```sql
-- Problem: A references B, B references A
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    manager_id INTEGER  -- Will reference employees
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department_id INTEGER REFERENCES departments(department_id)
);

-- Add the other direction after both tables exist
ALTER TABLE departments 
    ADD CONSTRAINT fk_dept_manager 
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id);

-- Use deferred constraints or NULL initial values to populate
INSERT INTO departments (name, manager_id) VALUES ('Engineering', NULL);
INSERT INTO employees (name, department_id) VALUES ('John', 1);
UPDATE departments SET manager_id = 1 WHERE department_id = 1;
```

### Checking for Orphaned Records

If you inherit a database without proper constraints:

```sql
-- Find orders with non-existent customers
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Find products with invalid categories
SELECT p.product_id, p.name, p.category_id
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
WHERE p.category_id IS NOT NULL AND c.category_id IS NULL;
```

### Fixing Orphaned Records

```sql
-- Option 1: Delete orphaned records
DELETE FROM orders 
WHERE customer_id NOT IN (SELECT customer_id FROM customers);

-- Option 2: Set FK to NULL
UPDATE orders SET customer_id = NULL
WHERE customer_id NOT IN (SELECT customer_id FROM customers);

-- Option 3: Create placeholder parent
INSERT INTO customers (customer_id, name) VALUES (0, 'Unknown Customer');
UPDATE orders SET customer_id = 0
WHERE customer_id NOT IN (SELECT customer_id FROM customers WHERE customer_id != 0);
```

## Code Example

Demonstrating referential integrity:

```sql
-- Create tables with RI constraints
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INTEGER NOT NULL,
    CONSTRAINT fk_books_author 
        FOREIGN KEY (author_id) 
        REFERENCES authors(author_id)
        ON DELETE RESTRICT
);

-- Valid insertions (maintain RI)
INSERT INTO authors (name) VALUES ('Jane Austen');
INSERT INTO books (title, author_id) VALUES ('Pride and Prejudice', 1);

-- Invalid insertion (violates RI)
INSERT INTO books (title, author_id) VALUES ('Unknown Book', 999);
-- ERROR: insert or update violates foreign key constraint

-- Cannot delete referenced author
DELETE FROM authors WHERE author_id = 1;
-- ERROR: update or delete violates foreign key constraint

-- Fix: Delete books first, then author
DELETE FROM books WHERE author_id = 1;
DELETE FROM authors WHERE author_id = 1;
-- SUCCESS

-- Verify integrity with query
SELECT 
    b.book_id,
    b.title,
    CASE 
        WHEN a.author_id IS NULL THEN 'ORPHANED!'
        ELSE a.name 
    END AS author
FROM books b
LEFT JOIN authors a ON b.author_id = a.author_id;
```

## Key Takeaways

- Referential integrity ensures all FK values exist in parent tables
- Databases enforce RI automatically through FK constraints
- Violations are blocked by default; use CASCADE options for automatic handling
- Deferred constraints allow temporary violations within transactions
- Always check for orphaned records when inheriting legacy databases

## Additional Resources

- [PostgreSQL Foreign Key Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Deferrable Constraints](https://www.postgresql.org/docs/current/sql-set-constraints.html)
- [Data Integrity](https://www.postgresql.org/docs/current/ddl-constraints.html)
