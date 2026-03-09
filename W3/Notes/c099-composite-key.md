# Composite Key

## Learning Objectives

- Understand what composite keys are
- Identify when to use composite keys
- Implement composite primary keys
- Recognize advantages and disadvantages

## Why This Matters

While single-column primary keys work for most tables, some scenarios require multiple columns together to uniquely identify a row. Composite keys are essential for junction tables (many-to-many relationships) and situations where no single column provides uniqueness. Understanding when and how to use them is crucial for proper database design.

## The Concept

### What is a Composite Key?

A **composite key** (also called a compound key) is a primary key consisting of two or more columns. Together, these columns uniquely identify each row, even though individually they may contain duplicate values.

```
+------------------------------------------------------------------+
|     COMPOSITE KEY = Column A + Column B (+ Column C, etc.)        |
+------------------------------------------------------------------+
| order_id | product_id | quantity |                                |
|----------|------------|----------|                                |
|    1     |    100     |    2     | <-- (1, 100) is unique         |
|    1     |    101     |    1     | <-- (1, 101) is unique         |
|    2     |    100     |    3     | <-- (2, 100) is unique         |
+------------------------------------------------------------------+
  Neither order_id nor product_id is unique alone,
  but their combination is unique.
```

### Creating Composite Keys

```sql
-- Composite primary key syntax
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id)
);

-- With named constraint
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE,
    grade CHAR(2),
    CONSTRAINT pk_enrollments PRIMARY KEY (student_id, course_id)
);

-- Adding composite key to existing table
ALTER TABLE cart_items 
    ADD PRIMARY KEY (cart_id, product_id);
```

### When to Use Composite Keys

**1. Junction Tables (Many-to-Many Relationships)**:

```sql
-- Students enrolled in courses
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    semester VARCHAR(20),
    grade DECIMAL(3, 2),
    PRIMARY KEY (student_id, course_id)
);

-- Authors of books (one book can have multiple authors)
CREATE TABLE book_authors (
    book_id INTEGER REFERENCES books(book_id),
    author_id INTEGER REFERENCES authors(author_id),
    author_order INTEGER,  -- 1 for first author, 2 for second, etc.
    PRIMARY KEY (book_id, author_id)
);

-- Product categories (product can be in multiple categories)
CREATE TABLE product_categories (
    product_id INTEGER REFERENCES products(product_id),
    category_id INTEGER REFERENCES categories(category_id),
    PRIMARY KEY (product_id, category_id)
);
```

**2. Natural Compound Identifiers**:

```sql
-- Time-series data
CREATE TABLE stock_prices (
    symbol CHAR(5),
    trade_date DATE,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    PRIMARY KEY (symbol, trade_date)
);

-- Store inventory per location
CREATE TABLE store_inventory (
    store_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    last_restock_date DATE,
    PRIMARY KEY (store_id, product_id)
);
```

**3. Versioned or Historical Data**:

```sql
-- Price history
CREATE TABLE price_history (
    product_id INTEGER,
    effective_date DATE,
    price DECIMAL(10, 2),
    PRIMARY KEY (product_id, effective_date)
);

-- Address history
CREATE TABLE address_history (
    customer_id INTEGER,
    address_version INTEGER,
    street VARCHAR(200),
    city VARCHAR(100),
    PRIMARY KEY (customer_id, address_version)
);
```

### Composite Key vs Surrogate Key

You can use either approach for junction tables:

**Option A: Composite Primary Key**:

```sql
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

**Option B: Surrogate Key + Unique Constraint**:

```sql
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    UNIQUE (order_id, product_id)
);
```

| Aspect | Composite Key | Surrogate Key |
|--------|---------------|---------------|
| Simplicity | Cleaner schema | Extra column |
| Foreign keys | More complex | Simpler reference |
| Index size | Can be larger | Typically smaller |
| ORM compatibility | Sometimes issues | Usually better |
| Multiple same-product | Not possible | Possible if needed |

### Column Order in Composite Keys

Order matters for index utilization:

```sql
-- If PRIMARY KEY (order_id, product_id)
-- Efficient: WHERE order_id = X
-- Efficient: WHERE order_id = X AND product_id = Y
-- Inefficient: WHERE product_id = Y

-- Put more frequently queried column first
CREATE TABLE activity_log (
    user_id INTEGER,
    activity_time TIMESTAMP,
    activity_type VARCHAR(50),
    PRIMARY KEY (user_id, activity_time)
);
-- Optimized for "all activities for user X" queries
```

### Querying with Composite Keys

```sql
-- Insert with composite key
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (1, 100, 2, 29.99);

-- Select specific row
SELECT * FROM order_items 
WHERE order_id = 1 AND product_id = 100;

-- Update specific row
UPDATE order_items 
SET quantity = 3 
WHERE order_id = 1 AND product_id = 100;

-- Delete specific row
DELETE FROM order_items 
WHERE order_id = 1 AND product_id = 100;
```

## Code Example

Complete composite key implementation:

```sql
-- Main tables
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER DEFAULT 3
);

-- Junction table with composite key
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)
);

-- Insert sample data
INSERT INTO students (name, email) VALUES
    ('Alice Smith', 'alice@university.edu'),
    ('Bob Johnson', 'bob@university.edu');

INSERT INTO courses (course_code, course_name, credits) VALUES
    ('CS101', 'Introduction to Programming', 3),
    ('CS201', 'Data Structures', 4),
    ('MATH101', 'Calculus I', 4);

-- Enroll students (composite key at work)
INSERT INTO enrollments (student_id, course_id) VALUES
    (1, 1),  -- Alice in CS101
    (1, 2),  -- Alice in CS201
    (2, 1),  -- Bob in CS101
    (2, 3);  -- Bob in MATH101

-- Query enrollments
SELECT 
    s.name AS student,
    c.course_code,
    c.course_name,
    e.enrollment_date
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY s.name, c.course_code;

-- Try duplicate enrollment (will fail)
INSERT INTO enrollments (student_id, course_id) VALUES (1, 1);
-- ERROR: duplicate key value violates unique constraint

-- Update grade using composite key
UPDATE enrollments 
SET grade = 'A' 
WHERE student_id = 1 AND course_id = 1;

-- Find all courses for a student
SELECT c.* FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
WHERE e.student_id = 1;
```

## Key Takeaways

- Composite keys use multiple columns to uniquely identify rows
- Ideal for junction tables in many-to-many relationships
- Column order affects index efficiency
- Can be replaced with surrogate key + unique constraint when preferred
- All columns in composite key cannot be NULL

## Additional Resources

- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Database Design Keys](https://www.postgresql.org/docs/current/tutorial-fk.html)
- [Indexing Composite Keys](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
