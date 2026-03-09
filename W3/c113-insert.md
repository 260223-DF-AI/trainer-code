# INSERT Statement

## Learning Objectives

- Master INSERT syntax for adding data to tables
- Insert single rows, multiple rows, and data from queries
- Handle conflicts and defaults during insertion
- Apply INSERT best practices for data integrity

## Why This Matters

INSERT is how data enters your database. Whether you're loading initial data, capturing user input, or migrating from another system, you'll use INSERT constantly. Understanding its variations helps you write efficient data loading scripts and build robust applications that properly populate databases.

## The Concept

### Basic INSERT Syntax

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

### Single Row Insert

```sql
-- Insert with explicit column list (recommended)
INSERT INTO employees (first_name, last_name, department, salary)
VALUES ('Alice', 'Smith', 'Engineering', 75000);

-- Insert all columns in order (fragile - avoid)
INSERT INTO employees 
VALUES (1, 'Bob', 'Jones', 'Marketing', 65000);
```

**Best Practice**: Always specify column names explicitly. It prevents errors when table structure changes.

### Multiple Row Insert

Insert several rows in one statement:

```sql
INSERT INTO products (name, price, category)
VALUES 
    ('Laptop', 999.99, 'Electronics'),
    ('Mouse', 29.99, 'Electronics'),
    ('Desk', 299.99, 'Furniture'),
    ('Chair', 199.99, 'Furniture');
```

This is more efficient than multiple single-row inserts.

### INSERT with DEFAULT Values

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    order_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'
);

-- Use default values
INSERT INTO orders (customer_name)
VALUES ('John Doe');
-- order_date and status get their defaults

-- Explicitly use DEFAULT keyword
INSERT INTO orders (customer_name, order_date, status)
VALUES ('Jane Doe', DEFAULT, 'processing');
```

### INSERT with SELECT (Subquery)

Copy data from another table or query:

```sql
-- Copy all rows from one table to another
INSERT INTO archived_orders (order_id, customer_name, order_date)
SELECT order_id, customer_name, order_date
FROM orders
WHERE order_date < '2024-01-01';

-- Insert aggregated data
INSERT INTO monthly_sales (month, total)
SELECT DATE_TRUNC('month', order_date), SUM(amount)
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

### INSERT with RETURNING

Get back the inserted data (especially useful for auto-generated IDs):

```sql
-- Return the generated ID
INSERT INTO customers (name, email)
VALUES ('Alice', 'alice@email.com')
RETURNING customer_id;

-- Return multiple columns
INSERT INTO products (name, price)
VALUES ('New Product', 49.99)
RETURNING product_id, name, price;

-- Return all columns
INSERT INTO orders (customer_id, total)
VALUES (1, 150.00)
RETURNING *;
```

### INSERT with ON CONFLICT (Upsert)

Handle duplicate key conflicts:

```sql
-- Do nothing on conflict
INSERT INTO users (user_id, username, email)
VALUES (1, 'alice', 'alice@email.com')
ON CONFLICT (user_id) DO NOTHING;

-- Update on conflict (upsert)
INSERT INTO inventory (product_id, quantity)
VALUES (1, 100)
ON CONFLICT (product_id) 
DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity;
```

### Handling NULL Values

```sql
-- Explicit NULL
INSERT INTO employees (first_name, last_name, middle_name)
VALUES ('Alice', 'Smith', NULL);

-- Omit column to get NULL (if no default)
INSERT INTO employees (first_name, last_name)
VALUES ('Bob', 'Jones');
-- middle_name will be NULL
```

### Complete Example

```sql
-- Create table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    credit_limit DECIMAL(10,2) DEFAULT 1000.00,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Single insert with RETURNING
INSERT INTO customers (name, email)
VALUES ('Alice Smith', 'alice@example.com')
RETURNING customer_id, name, created_at;

-- Multiple insert
INSERT INTO customers (name, email, credit_limit)
VALUES 
    ('Bob Jones', 'bob@example.com', 2000.00),
    ('Carol White', 'carol@example.com', 1500.00),
    ('David Brown', 'david@example.com', DEFAULT);

-- Insert with conflict handling
INSERT INTO customers (name, email, credit_limit)
VALUES ('Alice Smith', 'alice@example.com', 3000.00)
ON CONFLICT (email) 
DO UPDATE SET credit_limit = EXCLUDED.credit_limit
RETURNING *;

-- Verify
SELECT * FROM customers;
```

## Key Takeaways

- Always specify column names in INSERT statements
- Use multi-row INSERT for efficiency when adding many rows
- INSERT...SELECT copies data from queries into tables
- RETURNING gives back the inserted data (great for getting generated IDs)
- ON CONFLICT handles duplicate key scenarios (upsert pattern)
- Omitting a column uses NULL or the DEFAULT value

## Additional Resources

- [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)
- [INSERT with ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
- [RETURNING Clause](https://www.postgresql.org/docs/current/dml-returning.html)
