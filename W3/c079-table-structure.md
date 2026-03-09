# Table Structure

## Learning Objectives

- Understand how data is organized in relational tables
- Identify the components of a table (rows, columns, cells)
- Learn terminology: tuples, attributes, fields, records
- Recognize the importance of proper table design

## Why This Matters

Tables are the fundamental building blocks of relational databases. Every piece of data you store and retrieve lives in a table. Understanding table structure is essential before you can effectively design databases, write queries, or optimize performance. This knowledge forms the foundation for everything else in SQL.

## The Concept

### Anatomy of a Table

A table is a two-dimensional structure consisting of:

```
                        TABLE: employees
    +------------+-------------+-----------+------------+--------+
    | employee_id| first_name  | last_name | department | salary |
    +------------+-------------+-----------+------------+--------+
    |     1      | Alice       | Johnson   | Engineering| 85000  |
    |     2      | Bob         | Smith     | Marketing  | 72000  |
    |     3      | Carol       | Williams  | Engineering| 90000  |
    |     4      | David       | Brown     | Sales      | 68000  |
    +------------+-------------+-----------+------------+--------+
    ^                                                             ^
    |_____________________________________________________________|
                            COLUMNS (Attributes)

    Each horizontal line is a ROW (Tuple/Record)
    Each intersection is a CELL (Field Value)
```

### Key Components

| Term | Also Called | Definition |
|------|-------------|------------|
| **Table** | Relation | A collection of related data organized in rows and columns |
| **Column** | Attribute, Field | A vertical structure with a name and data type |
| **Row** | Tuple, Record | A single horizontal entry representing one entity |
| **Cell** | Field Value | The intersection of a row and column; a single value |

### Column Properties

Every column has specific properties:

```sql
CREATE TABLE employees (
    employee_id INTEGER,       -- Column name and data type
    first_name VARCHAR(50),    -- Variable-length string, max 50 chars
    hire_date DATE,            -- Date type
    salary DECIMAL(10, 2),     -- Numeric with precision
    is_active BOOLEAN          -- True/False
);
```

Column properties include:

- **Name**: Unique identifier within the table
- **Data Type**: What kind of values it holds
- **Constraints**: Rules the values must follow
- **Default Value**: Value used if none specified
- **Nullability**: Whether NULL values are allowed

### Row Properties

Each row:

- Represents a single entity or record
- Contains exactly one value per column
- Should be uniquely identifiable (we will cover keys later)
- Is independent of row order

### Table Naming Conventions

Best practices for naming tables:

| Convention | Example | Notes |
|------------|---------|-------|
| Plural nouns | `employees`, `orders` | Represents collections |
| Snake_case | `order_items` | Words separated by underscores |
| Lowercase | `customer_addresses` | Avoids case sensitivity issues |
| Descriptive | `employee_salaries` | Clear purpose |

Avoid:

- Reserved words (`order`, `user`, `select`)
- Spaces or special characters
- Starting with numbers
- Abbreviations unless standard

### Column Naming Conventions

```sql
-- Good column names
CREATE TABLE employees (
    employee_id INTEGER,         -- Descriptive, includes table reference
    first_name VARCHAR(50),      -- Clear meaning
    last_name VARCHAR(50),
    email_address VARCHAR(100),
    hire_date DATE,
    department_id INTEGER        -- Foreign key clearly named
);

-- Avoid these patterns
CREATE TABLE employees (
    id INTEGER,          -- Too generic
    fname VARCHAR(50),   -- Cryptic abbreviation
    col1 VARCHAR(50),    -- Meaningless
    HIRE DATE            -- Spaces not allowed
);
```

### NULL Values

NULL represents the absence of a value:

```sql
-- A row might have NULL values
INSERT INTO employees (employee_id, first_name, last_name, department)
VALUES (5, 'Eve', 'Davis', NULL);  -- No department assigned yet
```

NULL is not:

- Zero
- Empty string
- False

NULL means "unknown" or "not applicable."

## Code Example

Creating a well-structured table:

```sql
-- Create a properly structured employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE
);

-- View the table structure (PostgreSQL)
\d employees

-- Insert sample data
INSERT INTO employees 
    (employee_id, first_name, last_name, email, hire_date, department, salary)
VALUES
    (1, 'Alice', 'Johnson', 'alice@company.com', '2023-01-15', 'Engineering', 85000),
    (2, 'Bob', 'Smith', 'bob@company.com', '2023-03-20', 'Marketing', 72000);

-- View table contents
SELECT * FROM employees;

-- View specific columns
SELECT first_name, last_name, department FROM employees;

-- Count rows in table
SELECT COUNT(*) FROM employees;
```

## Key Takeaways

- Tables are the fundamental data structures in relational databases
- Columns define the attributes; rows contain the data
- Each column has a name, data type, and optional constraints
- Follow naming conventions for maintainability
- NULL represents missing or unknown values

## Additional Resources

- [PostgreSQL CREATE TABLE Documentation](https://www.postgresql.org/docs/current/sql-createtable.html)
- [Database Naming Conventions](https://www.sqlshack.com/learn-sql-naming-conventions/)
- [Understanding NULL in SQL](https://www.postgresql.org/docs/current/functions-comparison.html)
