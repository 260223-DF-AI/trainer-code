# Data Modeling and ERD

## Learning Objectives

- Understand the purpose and process of data modeling
- Learn to read and create Entity-Relationship Diagrams (ERDs)
- Identify entities, attributes, and relationships
- Apply cardinality notation to describe relationships

## Why This Matters

Data modeling is the blueprint phase of database design. Before writing any SQL, you need to understand what data you are storing and how pieces relate to each other. A well-designed data model prevents costly refactoring and ensures your database can answer the business questions it needs to. ERDs are the universal language for communicating database designs.

## The Concept

### What is Data Modeling?

Data modeling is the process of defining:

1. **What** data needs to be stored (entities)
2. **What properties** each entity has (attributes)
3. **How** entities relate to each other (relationships)

### Levels of Data Modeling

```
+--------------------+   +--------------------+   +--------------------+
|    CONCEPTUAL      |-->|      LOGICAL       |-->|     PHYSICAL       |
+--------------------+   +--------------------+   +--------------------+
| High-level view    |   | Detailed structure |   | Implementation     |
| Business entities  |   | Tables & columns   |   | Data types, indexes|
| Main relationships |   | Keys & constraints |   | Storage details    |
| No technical detail|   | Database-agnostic  |   | DBMS-specific      |
+--------------------+   +--------------------+   +--------------------+
```

### Entity-Relationship Diagram (ERD)

An ERD is a visual representation of your data model:

```
+----------------+          +----------------+          +----------------+
|   CUSTOMER     |          |     ORDER      |          |    PRODUCT     |
+----------------+          +----------------+          +----------------+
| customer_id PK |<-------->| order_id    PK |<-------->| product_id  PK |
| first_name     |   1:M    | customer_id FK |   M:N    | name           |
| last_name      |          | order_date     |          | price          |
| email          |          | total          |          | category       |
+----------------+          +----------------+          +----------------+
```

### ERD Components

**Entities (Tables)**:

- Represented as rectangles
- Named with singular nouns (Customer, not Customers)
- Represent things you store data about

**Attributes (Columns)**:

- Listed inside the entity box
- Include data type in logical/physical models
- Mark primary keys (PK) and foreign keys (FK)

**Relationships (Lines)**:

- Connect related entities
- Show how entities reference each other
- Include cardinality notation

### Cardinality Notation

Cardinality describes how many instances of one entity relate to another:

**Crow's Foot Notation**:

```
    1:1 (One-to-One)
    ||---------||
    One        One

    1:M (One-to-Many)
    ||--------<|
    One       Many

    M:N (Many-to-Many)
    |>--------<|
    Many      Many
```

**Examples**:

- Customer to Order: 1:M (one customer has many orders)
- Order to Product: M:N (many orders contain many products)
- Employee to Badge: 1:1 (one employee has one badge)

### Identifying Entities

Ask these questions:

1. What are the main "things" in the business domain?
2. What do we need to store information about?
3. What nouns appear repeatedly in requirements?

**E-commerce Example**:

- Customers
- Products
- Orders
- Categories
- Payments
- Reviews

### Identifying Attributes

For each entity, ask:

1. What information describes this entity?
2. What data points are needed for business operations?
3. What will be searched or reported on?

```sql
-- Example: Customer entity attributes
Customer:
    customer_id     -- Unique identifier (PK)
    first_name      -- Personal info
    last_name
    email           -- Contact (unique)
    phone
    created_at      -- Tracking
    is_active       -- Status
```

### Identifying Relationships

Determine how entities connect:

```
1. Can a Customer exist without an Order?     YES (optional)
2. Can an Order exist without a Customer?     NO (required)
3. Can a Customer have multiple Orders?       YES (1:M)
4. Can an Order have multiple Customers?      NO

Result: Customer 1:M Order (one customer, many orders)
```

### Junction Tables (M:N Relationships)

Many-to-many relationships require a junction table:

```
+----------+         +---------------+         +----------+
|  ORDER   |         |  ORDER_ITEM   |         | PRODUCT  |
+----------+         +---------------+         +----------+
| order_id |<------->| order_id   FK |<------->|product_id|
|          |   1:M   | product_id FK |   M:1   |          |
|          |         | quantity      |         |          |
|          |         | unit_price    |         |          |
+----------+         +---------------+         +----------+

ORDER 1:M ORDER_ITEM M:1 PRODUCT
(Resolves the M:N between Order and Product)
```

## Code Example

Translating an ERD to SQL:

```sql
-- Entity: Customer
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entity: Product
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    stock_quantity INTEGER DEFAULT 0
);

-- Entity: Order (1:M with Customer)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total DECIMAL(10, 2)
);

-- Junction Table: Order Items (resolves M:N between Order and Product)
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

## Key Takeaways

- Data modeling defines entities, attributes, and relationships
- ERDs visualize database structure before implementation
- Cardinality (1:1, 1:M, M:N) describes relationship counts
- Many-to-many relationships require junction tables
- Good data modeling prevents costly redesigns

## Additional Resources

- [Lucidchart ERD Tutorial](https://www.lucidchart.com/pages/er-diagrams)
- [Crow's Foot Notation Guide](https://www.gleek.io/blog/crows-foot-notation)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/tutorial.html)
