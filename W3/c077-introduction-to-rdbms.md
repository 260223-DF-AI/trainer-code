# Introduction to RDBMS

## Learning Objectives

- Define what a Relational Database Management System (RDBMS) is
- Understand the relational model and its principles
- Compare popular RDBMS options available today
- Recognize the components of an RDBMS architecture

## Why This Matters

The relational model has dominated data storage for over four decades because of its reliability, consistency, and flexibility. Understanding how an RDBMS works helps you make informed decisions about database design, query optimization, and system architecture. As a data professional, you will work with relational databases daily.

## The Concept

### What is an RDBMS?

A **Relational Database Management System (RDBMS)** is software that:

- Stores data in structured tables with rows and columns
- Maintains relationships between tables
- Enforces data integrity through constraints
- Processes SQL queries to retrieve and manipulate data
- Manages concurrent access from multiple users
- Provides backup, recovery, and security features

### The Relational Model

The relational model, proposed by Edgar F. Codd in 1970, organizes data into **relations** (tables):

```
                    RELATION (Table)
    +------------------------------------------------+
    |  Column 1  |  Column 2  |  Column 3  |  ...   |
    +------------------------------------------------+
    |   value    |   value    |   value    |  ...   |  <- Tuple (Row)
    |   value    |   value    |   value    |  ...   |  <- Tuple (Row)
    |   value    |   value    |   value    |  ...   |  <- Tuple (Row)
    +------------------------------------------------+
         ^           ^            ^
         |           |            |
       Attributes (Columns)
```

Key terminology:

- **Relation**: A table with rows and columns
- **Tuple**: A single row (record) in a table
- **Attribute**: A column (field) in a table
- **Domain**: The set of valid values for an attribute

### Core RDBMS Principles

1. **Data Independence**: Physical storage is separate from logical structure
2. **Data Integrity**: Constraints ensure data accuracy
3. **ACID Compliance**: Transactions are Atomic, Consistent, Isolated, Durable
4. **Normalization**: Data organized to minimize redundancy
5. **Relationships**: Tables connected through keys

### Popular RDBMS Options

| RDBMS | Vendor | License | Best For |
|-------|--------|---------|----------|
| **PostgreSQL** | Community | Open Source | General purpose, advanced features |
| **MySQL** | Oracle | Open Source/Commercial | Web applications |
| **SQL Server** | Microsoft | Commercial | Enterprise Windows environments |
| **Oracle Database** | Oracle | Commercial | Large enterprise systems |
| **SQLite** | Community | Public Domain | Embedded, mobile apps |
| **MariaDB** | MariaDB | Open Source | MySQL alternative |

### RDBMS Architecture

A typical RDBMS has these components:

```
+------------------------------------------------------------------+
|                          CLIENT LAYER                             |
|  (Applications, SQL Tools, APIs)                                  |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                         QUERY LAYER                               |
|  Parser -> Optimizer -> Execution Engine                          |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                       STORAGE ENGINE                              |
|  Buffer Manager | Transaction Manager | Lock Manager              |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                         STORAGE                                   |
|  Data Files | Index Files | Log Files                             |
+------------------------------------------------------------------+
```

**Query Layer**:

- **Parser**: Validates SQL syntax
- **Optimizer**: Determines most efficient execution plan
- **Execution Engine**: Runs the query

**Storage Engine**:

- **Buffer Manager**: Caches data in memory
- **Transaction Manager**: Ensures ACID properties
- **Lock Manager**: Handles concurrent access

### Why PostgreSQL for This Course

This course uses **PostgreSQL** because:

- Free and open source
- Fully ACID compliant
- Extensive SQL standard support
- Rich data types (JSON, arrays, custom types)
- Excellent documentation
- Strong community support
- Used by many companies (Apple, Spotify, Netflix)

## Code Example

Connecting to PostgreSQL and verifying the installation:

```sql
-- Check PostgreSQL version
SELECT version();

-- List all databases
\l

-- Connect to a database
\c database_name

-- List all tables in current database
\dt

-- Describe a table structure
\d table_name
```

These commands use PostgreSQL's `psql` command-line interface.

## Key Takeaways

- RDBMS stores data in tables with defined relationships
- The relational model provides data independence and integrity
- Popular options include PostgreSQL, MySQL, SQL Server, and Oracle
- RDBMS architecture includes query processing and storage layers
- PostgreSQL is our course standard for its features and accessibility

## Additional Resources

- [PostgreSQL About Page](https://www.postgresql.org/about/)
- [Codd's 12 Rules for RDBMS](https://www.w3resource.com/sql/sql-basic/codd-12-rule-702702.php)
- [DB-Engines RDBMS Ranking](https://db-engines.com/en/ranking/relational+dbms)
