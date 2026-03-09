# Normalization

## Learning Objectives

- Understand database normalization and its purpose
- Learn the first three normal forms (1NF, 2NF, 3NF)
- Identify normalization problems in database designs
- Apply normalization to improve database structure

## Why This Matters

Normalization is a systematic approach to organizing database tables to reduce data redundancy and improve data integrity. Poorly normalized databases lead to update anomalies, wasted storage, and inconsistent data. While normalization is fundamental to good database design, understanding when to normalize (and when to denormalize) is a key skill for data professionals.

## The Concept

### What is Normalization?

**Normalization** is the process of organizing database tables to:

- Minimize data redundancy (no unnecessary duplication)
- Eliminate update anomalies (insert, update, delete problems)
- Ensure data dependencies are logical

### The Problem: Denormalized Data

Consider this denormalized table:

```
orders_denormalized:
+----------+-------------+-------------------+------------+--------------+
| order_id | customer_id | customer_name     | product_id | product_name |
+----------+-------------+-------------------+------------+--------------+
|    1     |     101     | Alice Johnson     |    1001    | Laptop       |
|    1     |     101     | Alice Johnson     |    1002    | Mouse        |
|    2     |     102     | Bob Smith         |    1001    | Laptop       |
|    3     |     101     | Alice Johnson     |    1003    | Keyboard     |
+----------+-------------+-------------------+------------+--------------+
```

Problems:

1. **Redundancy**: "Alice Johnson" stored 3 times
2. **Update Anomaly**: Renaming customer requires updating multiple rows
3. **Delete Anomaly**: Deleting order 3 loses Alice's association
4. **Insert Anomaly**: Cannot add customer without an order

### First Normal Form (1NF)

**Requirements**:

- All columns contain atomic (indivisible) values
- No repeating groups or arrays
- Each row is unique (has a primary key)

**Violates 1NF**:

```
| order_id | products              |
|----------|-----------------------|
|    1     | Laptop, Mouse, Cable  |  <- Multiple values in one cell
```

**Satisfies 1NF**:

```
| order_id | product    |
|----------|------------|
|    1     | Laptop     |
|    1     | Mouse      |
|    1     | Cable      |
```

### Second Normal Form (2NF)

**Requirements**:

- Must be in 1NF
- All non-key columns depend on the entire primary key
- No partial dependencies (relevant for composite keys)

**Violates 2NF**:

```
order_items (order_id, product_id, quantity, product_name, product_price)
PK = (order_id, product_id)

product_name depends only on product_id, not the full key!
```

**Satisfies 2NF**:

```
order_items (order_id, product_id, quantity)
products (product_id, product_name, product_price)
```

### Third Normal Form (3NF)

**Requirements**:

- Must be in 2NF
- No transitive dependencies
- Non-key columns depend only on the primary key

**Violates 3NF**:

```
employees (employee_id, department_id, department_name, department_manager)
PK = employee_id

department_name depends on department_id, not employee_id!
```

**Satisfies 3NF**:

```
employees (employee_id, department_id)
departments (department_id, department_name, department_manager)
```

### Normalization Summary

| Form | Requirement | Eliminates |
|------|-------------|------------|
| 1NF | Atomic values, no repeating groups | Column with multiple values |
| 2NF | No partial dependencies | Columns dependent on part of key |
| 3NF | No transitive dependencies | Columns dependent on non-key columns |

### Normalization in Practice

**Before Normalization (Denormalized)**:

```sql
CREATE TABLE orders_denormalized (
    order_id INTEGER,
    order_date DATE,
    customer_id INTEGER,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    product_id INTEGER,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2),
    quantity INTEGER
);
```

**After Normalization (3NF)**:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100) UNIQUE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INTEGER REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

### When NOT to Normalize

Normalization has costs:

- More tables = more joins
- Complex queries may be slower
- Development can be more complex

Consider denormalization for:

- Read-heavy reporting systems
- Performance-critical queries
- Data warehouses (covered in Week 4)

## Code Example

Normalizing a denormalized dataset:

```sql
-- Step 1: Start with denormalized data
CREATE TABLE sales_raw (
    sale_id INTEGER,
    sale_date DATE,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_city VARCHAR(100),
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    unit_price DECIMAL(10,2),
    quantity INTEGER
);

INSERT INTO sales_raw VALUES
    (1, '2024-01-15', 'Alice', 'alice@email.com', 'New York', 'Laptop', 'Electronics', 999.99, 1),
    (2, '2024-01-16', 'Alice', 'alice@email.com', 'New York', 'Mouse', 'Electronics', 29.99, 2),
    (3, '2024-01-16', 'Bob', 'bob@email.com', 'Boston', 'Laptop', 'Electronics', 999.99, 1);

-- Step 2: Create normalized tables
CREATE TABLE customers_norm (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    city VARCHAR(100)
);

CREATE TABLE products_norm (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE sales_norm (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    customer_id INTEGER REFERENCES customers_norm(customer_id),
    product_id INTEGER REFERENCES products_norm(product_id),
    quantity INTEGER NOT NULL
);

-- Step 3: Migrate data
INSERT INTO customers_norm (name, email, city)
SELECT DISTINCT customer_name, customer_email, customer_city
FROM sales_raw;

INSERT INTO products_norm (name, category, price)
SELECT DISTINCT product_name, product_category, unit_price
FROM sales_raw;

INSERT INTO sales_norm (sale_date, customer_id, product_id, quantity)
SELECT 
    s.sale_date,
    c.customer_id,
    p.product_id,
    s.quantity
FROM sales_raw s
JOIN customers_norm c ON s.customer_name = c.name
JOIN products_norm p ON s.product_name = p.name;

-- Step 4: Verify normalized data
SELECT 
    s.sale_id,
    s.sale_date,
    c.name AS customer,
    p.name AS product,
    p.price,
    s.quantity,
    p.price * s.quantity AS total
FROM sales_norm s
JOIN customers_norm c ON s.customer_id = c.customer_id
JOIN products_norm p ON s.product_id = p.product_id;
```

## Key Takeaways

- Normalization reduces redundancy and prevents anomalies
- 1NF: Atomic values, no repeating groups
- 2NF: No partial dependencies on composite keys
- 3NF: No transitive dependencies through non-key columns
- Most OLTP databases should be in 3NF; reporting systems may denormalize

## Additional Resources

- [Database Normalization Explained](https://www.guru99.com/database-normalization.html)
- [Normal Forms in DBMS](https://www.geeksforgeeks.org/normal-forms-in-dbms/)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/current/ddl.html)
