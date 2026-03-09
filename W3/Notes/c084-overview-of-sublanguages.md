# Overview of SQL Sublanguages

## Learning Objectives

- Identify the five SQL sublanguages
- Understand the purpose of each sublanguage
- Recognize which commands belong to each category
- Know when to use each sublanguage

## Why This Matters

SQL is not a single uniform language but rather a collection of specialized sublanguages, each designed for a specific purpose. Understanding this categorization helps you organize your knowledge, predict what permissions you need for different operations, and communicate clearly with database administrators and team members.

## The Concept

### The Five SQL Sublanguages

SQL commands are grouped into five sublanguages based on their function:

```
+-------------------------------------------------------------------+
|                         SQL LANGUAGE                               |
+-------------------------------------------------------------------+
|                                                                    |
|  +-------+   +-------+   +-------+   +-------+   +-------+        |
|  |  DDL  |   |  DML  |   |  DQL  |   |  DCL  |   |  TCL  |        |
|  +-------+   +-------+   +-------+   +-------+   +-------+        |
|  Define    | Modify    | Query     | Control   | Manage           |
|  Structure | Data      | Data      | Access    | Transactions     |
|            |           |           |           |                   |
|  CREATE    | INSERT    | SELECT    | GRANT     | COMMIT           |
|  ALTER     | UPDATE    |           | REVOKE    | ROLLBACK         |
|  DROP      | DELETE    |           |           | SAVEPOINT        |
|  TRUNCATE  |           |           |           |                   |
+-------------------------------------------------------------------+
```

### DDL: Data Definition Language

**Purpose**: Define and modify database structure

| Command | Description |
|---------|-------------|
| CREATE | Create new objects (tables, schemas, indexes) |
| ALTER | Modify existing objects |
| DROP | Remove objects |
| TRUNCATE | Remove all data from a table |

```sql
-- DDL Examples
CREATE TABLE employees (id INT, name VARCHAR(50));
ALTER TABLE employees ADD COLUMN email VARCHAR(100);
DROP TABLE old_records;
TRUNCATE TABLE temporary_data;
```

**Key Characteristics**:

- Changes schema/metadata
- Usually auto-committed (cannot be rolled back easily)
- Requires elevated privileges

### DML: Data Manipulation Language

**Purpose**: Add, modify, and remove data within tables

| Command | Description |
|---------|-------------|
| INSERT | Add new rows |
| UPDATE | Modify existing rows |
| DELETE | Remove rows |

```sql
-- DML Examples
INSERT INTO employees VALUES (1, 'Alice', 'alice@email.com');
UPDATE employees SET email = 'new@email.com' WHERE id = 1;
DELETE FROM employees WHERE id = 1;
```

**Key Characteristics**:

- Modifies data, not structure
- Can be part of transactions
- Can be rolled back before commit

### DQL: Data Query Language

**Purpose**: Retrieve data from the database

| Command | Description |
|---------|-------------|
| SELECT | Query and retrieve data |

```sql
-- DQL Examples
SELECT * FROM employees;
SELECT name, email FROM employees WHERE id > 100;
SELECT COUNT(*) FROM orders WHERE status = 'complete';
```

**Key Characteristics**:

- Read-only operations
- Does not modify data
- Most commonly used SQL command

> Note: Some textbooks include SELECT as part of DML. We separate it here because querying (reading) is fundamentally different from manipulation (writing).

### DCL: Data Control Language

**Purpose**: Manage access permissions

| Command | Description |
|---------|-------------|
| GRANT | Give permissions to users |
| REVOKE | Remove permissions from users |

```sql
-- DCL Examples
GRANT SELECT ON employees TO report_user;
GRANT ALL PRIVILEGES ON orders TO app_user;
REVOKE DELETE ON employees FROM intern_user;
```

**Key Characteristics**:

- Security-focused
- Managed by database administrators
- Controls who can do what

### TCL: Transaction Control Language

**Purpose**: Manage database transactions

| Command | Description |
|---------|-------------|
| COMMIT | Save transaction changes permanently |
| ROLLBACK | Undo transaction changes |
| SAVEPOINT | Create checkpoint within transaction |

```sql
-- TCL Examples
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Or if something goes wrong:
ROLLBACK;
```

**Key Characteristics**:

- Ensures data integrity
- Groups operations atomically
- Enables recovery from errors

### Sublanguage Summary

| Sublanguage | Purpose | Key Commands | Permission Level |
|-------------|---------|--------------|------------------|
| DDL | Structure | CREATE, ALTER, DROP | Admin |
| DML | Data Changes | INSERT, UPDATE, DELETE | User |
| DQL | Data Retrieval | SELECT | User |
| DCL | Permissions | GRANT, REVOKE | Admin |
| TCL | Transactions | COMMIT, ROLLBACK | User |

### Typical Operation Flow

```
1. DDL: Create table structure
   CREATE TABLE orders (...)

2. DML: Insert initial data
   INSERT INTO orders (...)

3. DQL: Query data for reports
   SELECT * FROM orders WHERE ...

4. DML: Update as needed
   UPDATE orders SET status = 'shipped' WHERE ...

5. TCL: Commit when complete
   COMMIT
```

## Code Example

A complete workflow using all sublanguages:

```sql
-- DDL: Create structure
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2)
);

-- DCL: Grant permissions (as admin)
GRANT SELECT, INSERT, UPDATE ON products TO app_user;
GRANT SELECT ON products TO report_user;

-- TCL: Start a transaction
BEGIN;

-- DML: Insert data
INSERT INTO products (name, price) VALUES ('Widget A', 19.99);
INSERT INTO products (name, price) VALUES ('Widget B', 29.99);

-- DQL: Verify the data
SELECT * FROM products;

-- TCL: Commit the transaction
COMMIT;

-- Later: DML update
UPDATE products SET price = 24.99 WHERE name = 'Widget A';

-- DDL: Modify structure (add column)
ALTER TABLE products ADD COLUMN category VARCHAR(50);
```

## Key Takeaways

- DDL defines structure (CREATE, ALTER, DROP)
- DML manipulates data (INSERT, UPDATE, DELETE)
- DQL retrieves data (SELECT)
- DCL controls access (GRANT, REVOKE)
- TCL manages transactions (COMMIT, ROLLBACK)
- Understanding sublanguages helps organize SQL knowledge

## Additional Resources

- [PostgreSQL SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html)
- [SQL Language Categories](https://www.geeksforgeeks.org/sql-ddl-dql-dml-dcl-tcl-commands/)
- [Transaction Control](https://www.postgresql.org/docs/current/tutorial-transactions.html)
