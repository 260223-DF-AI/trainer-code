# Multiplicity

## Learning Objectives

- Understand relationship multiplicity (cardinality)
- Identify one-to-one, one-to-many, and many-to-many relationships
- Implement each relationship type in SQL
- Choose the appropriate relationship for business requirements

## Why This Matters

Relationships between tables are the core of relational database design. Understanding multiplicity helps you model real-world scenarios correctly. Choosing the wrong relationship type leads to data issues: either too restrictive (losing valid data) or too permissive (allowing invalid combinations). Getting relationships right is fundamental to database quality.

## The Concept

### What is Multiplicity?

**Multiplicity** (also called cardinality) describes how many instances of one entity can be associated with instances of another entity.

The three main types:

- **One-to-One (1:1)**: One record relates to exactly one record
- **One-to-Many (1:M)**: One record relates to many records
- **Many-to-Many (M:N)**: Many records relate to many records

### One-to-One (1:1)

Each record in Table A relates to exactly one record in Table B.

```
+------------------+          +------------------+
|     EMPLOYEE     |   1:1    |   EMPLOYEE_      |
|                  |----------|   DETAILS        |
| employee_id (PK) |          | employee_id (PK) |
| first_name       |          | ssn              |
| last_name        |          | birth_date       |
+------------------+          | salary           |
                              +------------------+
```

**When to use 1:1**:

- Split a table for performance (frequently vs rarely accessed columns)
- Store sensitive data separately (for security)
- Optional extension of main entity
- Inherited from legacy systems

**Implementation**:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE employee_details (
    employee_id INTEGER PRIMARY KEY REFERENCES employees(employee_id),
    ssn CHAR(11),
    birth_date DATE,
    salary DECIMAL(10, 2)
);
-- The PK being also the FK enforces 1:1
```

### One-to-Many (1:M)

Each record in Table A can relate to many records in Table B.

```
+------------------+          +------------------+
|   DEPARTMENT     |   1:M    |    EMPLOYEE      |
|                  |--------->|                  |
| department_id    |          | employee_id (PK) |
| name             |          | department_id FK |
+------------------+          | name             |
                              +------------------+
One department has many employees
```

**When to use 1:M**:

- Parent-child relationships
- Categories and items
- Customers and orders
- Most common relationship type

**Implementation**:

```sql
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER REFERENCES departments(department_id)
);
-- FK in the "many" side points to the "one" side
```

### Many-to-Many (M:N)

Each record in Table A can relate to many records in Table B, and vice versa.

```
+------------------+          +------------------+          +------------------+
|    STUDENT       |   M:N    |   ENROLLMENT     |   M:1    |    COURSE        |
|                  |<-------->|  (Junction)      |<-------->|                  |
| student_id (PK)  |          | student_id (FK)  |          | course_id (PK)   |
| name             |          | course_id (FK)   |          | title            |
+------------------+          | grade            |          +------------------+
                              +------------------+
Students take many courses; courses have many students
```

**When to use M:N**:

- Students and courses
- Products and orders
- Authors and books
- Tags and articles

**Implementation (requires junction table)**:

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

-- Junction table resolves M:N into two 1:M relationships
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    enrollment_date DATE,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)
);
```

### Determining Multiplicity

Ask these questions:

1. Can one A have multiple B's?
2. Can one B have multiple A's?

```
| A -> B? | B -> A? | Relationship |
|---------|---------|--------------|
| No      | No      | 1:1          |
| Yes     | No      | 1:M (A to B) |
| No      | Yes     | M:1 (B to A) |
| Yes     | Yes     | M:N          |
```

### Optional vs Mandatory

Relationships can be optional or mandatory:

```sql
-- Mandatory: employee MUST have department
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(department_id)
);

-- Optional: employee MAY have department
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES departments(department_id)  -- NULL allowed
);
```

### Self-Referencing Relationships

An entity can have a relationship with itself:

```sql
-- 1:M Self-reference: Employee-Manager
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INTEGER REFERENCES employees(employee_id)
);

-- M:N Self-reference: Friendships
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50)
);

CREATE TABLE friendships (
    user_id_1 INTEGER REFERENCES users(user_id),
    user_id_2 INTEGER REFERENCES users(user_id),
    since_date DATE,
    PRIMARY KEY (user_id_1, user_id_2)
);
```

## Code Example

Implementing all relationship types:

```sql
-- 1:1 Example: User and User Profile
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE user_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(user_id),
    bio TEXT,
    avatar_url VARCHAR(255),
    birth_date DATE
);

-- Insert 1:1 data
INSERT INTO users (username, email) VALUES ('alice', 'alice@email.com');
INSERT INTO user_profiles (user_id, bio) VALUES (1, 'Software developer');

-- 1:M Example: Category and Products
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id)
);

-- Insert 1:M data
INSERT INTO categories (name) VALUES ('Electronics');
INSERT INTO products (name, category_id) VALUES ('Laptop', 1), ('Phone', 1);

-- M:N Example: Products and Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Insert M:N data
INSERT INTO orders DEFAULT VALUES;
INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 1), (1, 2, 2);

-- Query all relationships
SELECT u.username, p.bio 
FROM users u 
LEFT JOIN user_profiles p ON u.user_id = p.user_id;

SELECT c.name AS category, prod.name AS product
FROM categories c
LEFT JOIN products prod ON c.category_id = prod.category_id;

SELECT o.order_id, prod.name, oi.quantity
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products prod ON oi.product_id = prod.product_id;
```

## Key Takeaways

- One-to-One: FK as PK in child table, or unique FK
- One-to-Many: FK in the "many" side (most common)
- Many-to-Many: Requires junction table with two FKs
- Use NOT NULL on FK for mandatory relationships
- Multiplicity directly affects your SQL schema design

## Additional Resources

- [PostgreSQL Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [ER Diagram Cardinality](https://www.lucidchart.com/pages/ER-diagram-symbols-and-meaning)
- [Database Relationships](https://www.geeksforgeeks.org/relationships-in-sql-one-to-one-one-to-many-many-to-many/)
