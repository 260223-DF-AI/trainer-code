# Constraint Naming and Management

## Learning Objectives

- Understand the importance of constraint naming
- Apply consistent naming conventions
- Manage constraints effectively
- Query constraint metadata

## Why This Matters

As databases grow, managing constraints becomes increasingly important. Well-named constraints make error messages understandable, simplify maintenance, and document the database schema. Without clear naming, debugging constraint violations is frustrating and time-consuming.

## The Concept

### Why Name Constraints?

Compare these error messages:

**Auto-generated name**:

```
ERROR: duplicate key value violates unique constraint "users_email_key"
```

**Well-named constraint**:

```
ERROR: duplicate key value violates unique constraint "uq_users_email"
```

Named constraints:

- Produce clearer error messages
- Are easier to reference in ALTER statements
- Document business rules
- Follow consistent patterns

### Naming Conventions

Common patterns for constraint names:

| Constraint Type | Pattern | Example |
|----------------|---------|---------|
| Primary Key | pk_table | pk_orders |
| Foreign Key | fk_table_column | fk_orders_customer_id |
| Unique | uq_table_column | uq_users_email |
| Check | chk_table_rule | chk_products_positive_price |
| Not Null | (not named) | - |
| Default | (not named) | - |

### Creating Named Constraints

**Primary Key**:

```sql
CREATE TABLE orders (
    order_id SERIAL,
    order_date DATE,
    CONSTRAINT pk_orders PRIMARY KEY (order_id)
);
```

**Foreign Key**:

```sql
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Unique**:

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    username VARCHAR(50),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT uq_users_username UNIQUE (username)
);
```

**Check**:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2),
    quantity INTEGER,
    CONSTRAINT chk_products_positive_price CHECK (price > 0),
    CONSTRAINT chk_products_non_negative_qty CHECK (quantity >= 0)
);
```

### Managing Constraints

**Add Constraint**:

```sql
ALTER TABLE employees 
    ADD CONSTRAINT uq_employees_email UNIQUE (email);

ALTER TABLE orders 
    ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE products 
    ADD CONSTRAINT chk_price_positive CHECK (price > 0);
```

**Drop Constraint**:

```sql
ALTER TABLE employees DROP CONSTRAINT uq_employees_email;
ALTER TABLE orders DROP CONSTRAINT fk_orders_customer;
ALTER TABLE products DROP CONSTRAINT chk_price_positive;
```

**Rename Constraint**:

```sql
ALTER TABLE users RENAME CONSTRAINT users_email_key TO uq_users_email;
```

### Querying Constraint Information

**View table constraints**:

```sql
SELECT 
    constraint_name,
    constraint_type,
    table_name
FROM information_schema.table_constraints
WHERE table_schema = 'public' AND table_name = 'orders';
```

**View constraint details**:

```sql
-- Get constraint definition
SELECT 
    conname AS constraint_name,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'orders'::regclass;
```

**View foreign key relationships**:

```sql
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
    ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public';
```

### Enabling/Disabling Constraints

**Disable for bulk load**:

```sql
-- Disable foreign key checks (PostgreSQL session-level)
SET session_replication_role = 'replica';

-- Perform bulk operations
COPY large_table FROM '/path/to/data.csv';

-- Re-enable
SET session_replication_role = 'origin';
```

**Enable/Disable triggers**:

```sql
ALTER TABLE orders DISABLE TRIGGER ALL;
-- Do operations
ALTER TABLE orders ENABLE TRIGGER ALL;
```

### Validating Constraints

When adding constraints to tables with existing data:

```sql
-- Add constraint without validating existing data
ALTER TABLE products 
    ADD CONSTRAINT chk_positive_price CHECK (price > 0) NOT VALID;

-- Later, validate existing data
ALTER TABLE products VALIDATE CONSTRAINT chk_positive_price;
```

## Code Example

Complete constraint management:

```sql
-- Create tables with well-named constraints
CREATE TABLE departments (
    department_id SERIAL,
    name VARCHAR(100) NOT NULL,
    budget DECIMAL(12, 2),
    CONSTRAINT pk_departments PRIMARY KEY (department_id),
    CONSTRAINT uq_departments_name UNIQUE (name),
    CONSTRAINT chk_departments_positive_budget CHECK (budget >= 0)
);

CREATE TABLE employees (
    employee_id SERIAL,
    email VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL,
    salary DECIMAL(10, 2),
    hire_date DATE,
    CONSTRAINT pk_employees PRIMARY KEY (employee_id),
    CONSTRAINT uq_employees_email UNIQUE (email),
    CONSTRAINT fk_employees_department FOREIGN KEY (department_id) 
        REFERENCES departments(department_id) ON DELETE RESTRICT,
    CONSTRAINT chk_employees_positive_salary CHECK (salary > 0),
    CONSTRAINT chk_employees_hire_date CHECK (hire_date <= CURRENT_DATE)
);

-- View all constraints
SELECT 
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_type;

-- Test constraint violation
INSERT INTO departments (name, budget) VALUES ('Engineering', 1000000);
INSERT INTO employees (email, department_id, salary, hire_date)
VALUES ('invalid', 999, 50000, CURRENT_DATE);
-- ERROR: insert or update on table "employees" violates 
--        foreign key constraint "fk_employees_department"

-- Drop and recreate constraint with different rule
ALTER TABLE employees DROP CONSTRAINT fk_employees_department;
ALTER TABLE employees 
    ADD CONSTRAINT fk_employees_department FOREIGN KEY (department_id) 
    REFERENCES departments(department_id) ON DELETE SET NULL;

-- View constraint definitions
SELECT 
    conname,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'employees'::regclass;

-- Clean up: drop all constraints (example)
-- ALTER TABLE employees DROP CONSTRAINT pk_employees;
-- ALTER TABLE employees DROP CONSTRAINT uq_employees_email;
-- etc.
```

## Key Takeaways

- Name all constraints for clarity and maintainability
- Use consistent naming conventions (pk_, fk_, uq_, chk_)
- Query information_schema to view constraint metadata
- Use NOT VALID for adding constraints to large tables
- Named constraints are easier to modify and reference

## Additional Resources

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [System Catalogs](https://www.postgresql.org/docs/current/catalogs.html)
