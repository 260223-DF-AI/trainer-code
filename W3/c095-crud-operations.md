# CRUD Operations

## Learning Objectives

- Understand CRUD as the four fundamental database operations
- Map CRUD to SQL commands (INSERT, SELECT, UPDATE, DELETE)
- Apply CRUD concepts to database application design
- Recognize CRUD patterns in real-world applications

## Why This Matters

CRUD (Create, Read, Update, Delete) is the backbone of virtually every database-driven application. Whether you're building a web app, mobile app, or enterprise system, your interaction with the database boils down to these four operations. Understanding CRUD helps you design better APIs, plan database schemas, and communicate effectively with other developers about data operations.

## The Concept

### What is CRUD?

CRUD is an acronym representing the four basic operations you can perform on persistent data:

| Operation | Meaning | SQL Command | HTTP Method |
|-----------|---------|-------------|-------------|
| **C**reate | Add new data | INSERT | POST |
| **R**ead | Retrieve data | SELECT | GET |
| **U**pdate | Modify existing data | UPDATE | PUT/PATCH |
| **D**elete | Remove data | DELETE | DELETE |

### CRUD and SQL Commands

Each CRUD operation maps directly to a SQL command you've already learned:

**Create - INSERT**

```sql
-- Create a new record
INSERT INTO products (name, price, category)
VALUES ('Laptop', 999.99, 'Electronics');
```

**Read - SELECT**

```sql
-- Read records
SELECT name, price FROM products WHERE category = 'Electronics';

-- Read all records
SELECT * FROM products;

-- Read with conditions
SELECT * FROM products WHERE price > 500 ORDER BY price DESC;
```

**Update - UPDATE**

```sql
-- Update existing records
UPDATE products 
SET price = 899.99 
WHERE name = 'Laptop';

-- Update multiple fields
UPDATE products 
SET price = 799.99, category = 'Sale Items'
WHERE product_id = 1;
```

**Delete - DELETE**

```sql
-- Delete specific records
DELETE FROM products WHERE product_id = 1;

-- Delete with conditions
DELETE FROM products WHERE category = 'Discontinued';
```

### CRUD in Application Design

When designing applications, you typically create functions or endpoints for each CRUD operation:

```
Application Layer          Database Layer
-----------------          --------------
createProduct()     -->    INSERT INTO products...
getProduct()        -->    SELECT FROM products...
getAllProducts()    -->    SELECT * FROM products...
updateProduct()     -->    UPDATE products...
deleteProduct()     -->    DELETE FROM products...
```

### Complete CRUD Example

```sql
-- Setup: Create a table for our CRUD operations
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- CREATE: Add new customers
INSERT INTO customers (name, email) VALUES ('Alice Smith', 'alice@email.com');
INSERT INTO customers (name, email) VALUES ('Bob Jones', 'bob@email.com');
INSERT INTO customers (name, email) VALUES ('Carol White', 'carol@email.com');

-- READ: Retrieve customers
SELECT * FROM customers;
SELECT name, email FROM customers WHERE customer_id = 1;
SELECT * FROM customers ORDER BY created_at DESC;

-- UPDATE: Modify customer information
UPDATE customers 
SET email = 'alice.smith@newemail.com' 
WHERE customer_id = 1;

-- Verify the update
SELECT * FROM customers WHERE customer_id = 1;

-- DELETE: Remove a customer
DELETE FROM customers WHERE customer_id = 3;

-- Verify the delete
SELECT * FROM customers;
```

### CRUD Best Practices

1. **Always use WHERE with UPDATE and DELETE** - Without it, you'll affect all rows
2. **Validate data before CREATE** - Ensure data meets constraints
3. **Use transactions for multiple operations** - Keep data consistent
4. **Consider soft deletes** - Mark records as inactive instead of removing them

```sql
-- Soft delete example
UPDATE customers SET is_active = FALSE WHERE customer_id = 1;

-- Query only active records
SELECT * FROM customers WHERE is_active = TRUE;
```

## Key Takeaways

- CRUD represents the four fundamental data operations: Create, Read, Update, Delete
- These map directly to SQL: INSERT, SELECT, UPDATE, DELETE
- CRUD is universal across programming languages and frameworks
- Understanding CRUD helps design consistent APIs and database interfaces
- Always use WHERE clauses with UPDATE and DELETE to avoid unintended changes

## Additional Resources

- [PostgreSQL INSERT Documentation](https://www.postgresql.org/docs/current/sql-insert.html)
- [PostgreSQL UPDATE Documentation](https://www.postgresql.org/docs/current/sql-update.html)
- [PostgreSQL DELETE Documentation](https://www.postgresql.org/docs/current/sql-delete.html)
