# Constraints Overview

## Learning Objectives

- Understand what database constraints are and why they matter
- Identify the different types of constraints available in SQL
- Apply constraints to ensure data integrity
- Design tables with appropriate constraint combinations

## Why This Matters

Constraints are the guardians of data quality. They enforce business rules at the database level, preventing invalid data from ever entering your system. Without constraints, your application must handle all validation, and bugs or bypasses could corrupt your data. Constraints provide a safety net that works regardless of how data enters the database.

## The Concept

### What Are Constraints?

Constraints are rules applied to columns or tables that restrict what data can be stored. They enforce:

- **Data integrity** - Ensuring data accuracy and consistency
- **Business rules** - Encoding domain logic in the schema
- **Relationships** - Maintaining connections between tables

### Types of Constraints

| Constraint | Purpose | Level |
|------------|---------|-------|
| NOT NULL | Prevents null values | Column |
| UNIQUE | Ensures all values are different | Column/Table |
| PRIMARY KEY | NOT NULL + UNIQUE, identifies rows | Column/Table |
| FOREIGN KEY | References another table | Column/Table |
| CHECK | Validates against a condition | Column/Table |
| DEFAULT | Provides automatic value | Column |

### Constraint Syntax Overview

Constraints can be defined inline (with the column) or at the table level:

```sql
-- Inline constraints
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,           -- Primary key
    name VARCHAR(100) NOT NULL,              -- Not null
    sku VARCHAR(20) UNIQUE,                  -- Unique
    price DECIMAL(10,2) CHECK (price > 0),   -- Check
    category_id INTEGER REFERENCES categories(category_id), -- Foreign key
    created_at TIMESTAMP DEFAULT NOW()       -- Default
);

-- Table-level constraints
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id),      -- Composite primary key
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### NOT NULL Constraint

Ensures a column must have a value:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,  -- Required
    last_name VARCHAR(50) NOT NULL,   -- Required
    middle_name VARCHAR(50)           -- Optional (allows NULL)
);

-- This fails:
INSERT INTO employees (first_name) VALUES ('John');
-- ERROR: null value in column "last_name" violates not-null constraint
```

### UNIQUE Constraint

Ensures all values in a column are different:

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    username VARCHAR(50) UNIQUE
);

-- Multiple columns can be unique together
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    UNIQUE (student_id, course_id)  -- Same student can't enroll twice
);
```

### CHECK Constraint

Validates data against a condition:

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) CHECK (price >= 0),
    discount DECIMAL(3,2) CHECK (discount >= 0 AND discount <= 1),
    stock INTEGER CHECK (stock >= 0)
);

-- Complex check constraint
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CHECK (end_date >= start_date)  -- End must be after start
);
```

### DEFAULT Constraint

Provides an automatic value when none is specified:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert without specifying defaults
INSERT INTO orders (order_id) VALUES (1);
-- order_date, status, and is_active get default values
```

### Combining Constraints

Tables often use multiple constraints together:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    credit_limit DECIMAL(10,2) DEFAULT 1000.00 CHECK (credit_limit >= 0),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## Key Takeaways

- Constraints enforce data integrity at the database level
- NOT NULL requires a value; UNIQUE ensures no duplicates
- PRIMARY KEY combines NOT NULL and UNIQUE for row identification
- FOREIGN KEY maintains relationships between tables
- CHECK validates data against custom conditions
- DEFAULT provides automatic values when not specified
- Constraints can be defined inline or at the table level

## Additional Resources

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [SQL Constraints Tutorial](https://www.w3schools.com/sql/sql_constraints.asp)
- [Data Integrity in Databases](https://www.ibm.com/docs/en/informix-servers/14.10?topic=integrity-data)
