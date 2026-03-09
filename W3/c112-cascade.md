# CASCADE

## Learning Objectives

- Understand CASCADE behavior for foreign key constraints
- Apply CASCADE DELETE and CASCADE UPDATE appropriately
- Recognize the risks and benefits of cascading actions
- Choose the right referential action for your use case

## Why This Matters

When tables are related through foreign keys, deleting or updating a parent row creates a dilemma: what happens to the child rows? CASCADE automatically propagates changes from parent to child tables, maintaining referential integrity without manual intervention. Understanding when to use CASCADE versus other options is critical for data safety and application design.

## The Concept

### Referential Actions

When a referenced (parent) row is modified, PostgreSQL offers several actions:

| Action | On DELETE | On UPDATE |
|--------|-----------|-----------|
| CASCADE | Delete child rows | Update child foreign keys |
| SET NULL | Set foreign key to NULL | Set foreign key to NULL |
| SET DEFAULT | Set to default value | Set to default value |
| RESTRICT | Prevent deletion | Prevent update |
| NO ACTION | Prevent (deferred check) | Prevent (deferred check) |

### CASCADE DELETE

Automatically deletes child rows when the parent is deleted:

```sql
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER REFERENCES departments(department_id) 
        ON DELETE CASCADE
);

-- Insert data
INSERT INTO departments (name) VALUES ('Engineering'), ('Marketing');
INSERT INTO employees (name, department_id) VALUES 
    ('Alice', 1), ('Bob', 1), ('Carol', 2);

-- Delete department - employees are automatically deleted
DELETE FROM departments WHERE department_id = 1;
-- Alice and Bob are now deleted!

SELECT * FROM employees;  -- Only Carol remains
```

### CASCADE UPDATE

Automatically updates child foreign keys when parent primary key changes:

```sql
CREATE TABLE categories (
    category_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_code VARCHAR(10) REFERENCES categories(category_code) 
        ON UPDATE CASCADE
);

-- Insert data
INSERT INTO categories (category_code, name) VALUES ('ELEC', 'Electronics');
INSERT INTO products (name, category_code) VALUES ('Laptop', 'ELEC');

-- Update category code - product automatically updated
UPDATE categories SET category_code = 'TECH' WHERE category_code = 'ELEC';

SELECT * FROM products;  -- category_code is now 'TECH'
```

### Combining CASCADE DELETE and UPDATE

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    product_name VARCHAR(100),
    quantity INTEGER
);
```

### Alternative: SET NULL

Instead of deleting child rows, set the foreign key to NULL:

```sql
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    project_id INTEGER REFERENCES projects(project_id) 
        ON DELETE SET NULL
);

-- Delete project - tasks remain but project_id becomes NULL
DELETE FROM projects WHERE project_id = 1;
-- Tasks still exist but are now "orphaned" (project_id = NULL)
```

### Alternative: RESTRICT

Prevent deletion if child rows exist:

```sql
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INTEGER REFERENCES authors(author_id) 
        ON DELETE RESTRICT
);

INSERT INTO authors (name) VALUES ('Jane Doe');
INSERT INTO books (title, author_id) VALUES ('Great Book', 1);

-- This fails - cannot delete author with books
DELETE FROM authors WHERE author_id = 1;
-- ERROR: update or delete on table "authors" violates foreign key constraint
```

### When to Use Each Option

| Scenario | Recommended Action |
|----------|-------------------|
| Orders and order items | CASCADE - items meaningless without order |
| Users and their posts | SET NULL or CASCADE - depends on requirements |
| Categories and products | RESTRICT - review products before deleting |
| Audit logs | NO ACTION - never delete referenced data |

### Practical Example

```sql
-- Complete e-commerce example
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) 
        ON DELETE RESTRICT,  -- Can't delete customer with orders
    order_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) 
        ON DELETE CASCADE,   -- Delete items when order deleted
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

-- This works: deleting an order cascades to items
DELETE FROM orders WHERE order_id = 1;

-- This fails: can't delete customer with orders
DELETE FROM customers WHERE customer_id = 1;
```

## Key Takeaways

- CASCADE automatically propagates DELETE and UPDATE to child tables
- SET NULL keeps child rows but clears the foreign key
- RESTRICT prevents deletion/update if child rows exist
- Choose CASCADE for dependent data (items without parent are meaningless)
- Choose RESTRICT when you want to force explicit handling
- Be careful with CASCADE DELETE - it can remove more data than expected

## Additional Resources

- [PostgreSQL Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [Referential Integrity](https://www.postgresql.org/docs/current/tutorial-fk.html)
- [ON DELETE CASCADE Explained](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-foreign-key/)
