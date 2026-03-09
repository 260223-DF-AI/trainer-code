# SQL Command Categories Summary

## Learning Objectives

- Review SQL sublanguage categories
- Understand when to use each category
- Recognize common commands in each category
- Apply appropriate commands for different tasks

## Why This Matters

Understanding SQL command categories helps you organize your knowledge and choose the right tools for each database task. This summary consolidates your Week 3 learning and prepares you for more advanced SQL topics in Week 4.

## The Concept

### SQL Sublanguages Overview

SQL is divided into five sublanguages, each for a specific purpose:

```
+-----------------------------------------------------------------------+
|                         SQL SUBLANGUAGES                              |
+-----------------------------------------------------------------------+
| DDL (Data Definition)   | Define structure: CREATE, ALTER, DROP       |
| DML (Data Manipulation) | Modify data: INSERT, UPDATE, DELETE         |
| DQL (Data Query)        | Retrieve data: SELECT                       |
| DCL (Data Control)      | Manage access: GRANT, REVOKE                |
| TCL (Transaction Control)| Manage transactions: COMMIT, ROLLBACK      |
+-----------------------------------------------------------------------+
```

### DDL - Data Definition Language

**Purpose**: Define and modify database structure

| Command | Purpose |
|---------|---------|
| CREATE | Create objects (tables, indexes, views) |
| ALTER | Modify existing objects |
| DROP | Remove objects |
| TRUNCATE | Remove all rows (keeps structure) |

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN email VARCHAR(100);

DROP TABLE IF EXISTS old_table;

TRUNCATE TABLE logs;
```

### DML - Data Manipulation Language

**Purpose**: Modify data in tables

| Command | Purpose |
|---------|---------|
| INSERT | Add new rows |
| UPDATE | Modify existing rows |
| DELETE | Remove rows |

```sql
INSERT INTO employees (name, email) VALUES ('Alice', 'alice@email.com');

UPDATE employees SET email = 'new@email.com' WHERE employee_id = 1;

DELETE FROM employees WHERE employee_id = 1;
```

### DQL - Data Query Language

**Purpose**: Retrieve and analyze data

| Command | Purpose |
|---------|---------|
| SELECT | Retrieve data from tables |

```sql
SELECT 
    e.name,
    d.department_name,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000
ORDER BY e.salary DESC;
```

**SELECT components**:

- FROM, WHERE, SELECT, ORDER BY (basic clauses)
- GROUP BY, HAVING (aggregation)
- JOIN types (INNER, LEFT, RIGHT, FULL, CROSS)
- Subqueries, UNION, INTERSECT, EXCEPT

### DCL - Data Control Language

**Purpose**: Manage permissions and access

| Command | Purpose |
|---------|---------|
| GRANT | Give permissions |
| REVOKE | Remove permissions |

```sql
GRANT SELECT, INSERT ON employees TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

REVOKE DELETE ON employees FROM app_user;
```

### TCL - Transaction Control Language

**Purpose**: Manage transaction boundaries

| Command | Purpose |
|---------|---------|
| BEGIN | Start transaction |
| COMMIT | Save changes |
| ROLLBACK | Undo changes |
| SAVEPOINT | Create checkpoint |

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

BEGIN;
    INSERT INTO orders (customer_id) VALUES (1);
    SAVEPOINT after_order;
    INSERT INTO order_items (order_id, product_id) VALUES (1, 999);
    ROLLBACK TO SAVEPOINT after_order;
    INSERT INTO order_items (order_id, product_id) VALUES (1, 100);
COMMIT;
```

### Week 3 Topics by Category

**DDL Topics Covered**:

- CREATE TABLE with constraints
- Primary keys, foreign keys, unique, check, not null, default
- Indexes, views
- Schema design, normalization

**DML Topics Covered**:

- INSERT (single row, multiple rows, from SELECT)
- UPDATE (with WHERE, with JOIN)
- DELETE (with WHERE, cascading)

**DQL Topics Covered**:

- Basic SELECT with clauses (FROM, WHERE, ORDER BY)
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Scalar functions (string, numeric, date)
- GROUP BY, HAVING
- Operators (IN, BETWEEN, LIKE, IS NULL)
- Set operations (UNION, INTERSECT, EXCEPT)
- Subqueries
- All JOIN types

**TCL Topics Covered**:

- Transaction basics (BEGIN, COMMIT, ROLLBACK)
- Savepoints
- Isolation levels

### Common Command Patterns

```sql
-- Create, populate, query pattern
CREATE TABLE x (...);
INSERT INTO x VALUES (...);
SELECT * FROM x WHERE ...;

-- Transactional changes pattern
BEGIN;
UPDATE/INSERT/DELETE ...;
COMMIT;

-- Report query pattern
SELECT columns, aggregates
FROM base_table
JOIN related_tables
WHERE filters
GROUP BY dimensions
HAVING aggregate_filters
ORDER BY sort_columns;
```

## Code Example

Demonstrating all categories:

```sql
-- DDL: Create structure
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) CHECK (price > 0),
    stock INTEGER DEFAULT 0
);

CREATE INDEX idx_products_name ON products(name);

-- DML: Add and modify data
INSERT INTO products (name, price, stock) VALUES 
    ('Laptop', 999.99, 10),
    ('Mouse', 29.99, 100),
    ('Keyboard', 79.99, 50);

UPDATE products SET stock = stock - 1 WHERE product_id = 1;

DELETE FROM products WHERE stock = 0;

-- DQL: Query data
SELECT 
    name,
    price,
    stock,
    price * stock AS total_value
FROM products
WHERE price > 50
ORDER BY total_value DESC;

-- Aggregate query
SELECT 
    COUNT(*) AS product_count,
    SUM(stock) AS total_inventory,
    AVG(price) AS avg_price
FROM products;

-- TCL: Transaction control
BEGIN;
    UPDATE products SET stock = stock - 5 WHERE product_id = 1;
    INSERT INTO sales (product_id, quantity) VALUES (1, 5);
COMMIT;

-- DDL: Modify structure
ALTER TABLE products ADD COLUMN category VARCHAR(50);

-- DCL: Grant access (if roles exist)
-- GRANT SELECT ON products TO reporting_user;

-- View current state
SELECT * FROM products;
```

## Key Takeaways

- DDL defines structure: CREATE, ALTER, DROP, TRUNCATE
- DML modifies data: INSERT, UPDATE, DELETE
- DQL retrieves data: SELECT (with all its clauses and features)
- DCL controls access: GRANT, REVOKE
- TCL manages transactions: BEGIN, COMMIT, ROLLBACK, SAVEPOINT
- Understanding categories helps choose the right command

## Additional Resources

- [PostgreSQL SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html)
- [DDL Documentation](https://www.postgresql.org/docs/current/ddl.html)
- [DML Documentation](https://www.postgresql.org/docs/current/dml.html)
- [Querying a Table](https://www.postgresql.org/docs/current/tutorial-select.html)
