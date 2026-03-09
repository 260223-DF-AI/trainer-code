# What Is a Database

## Learning Objectives

- Define a database and its core purpose
- Distinguish between database and DBMS
- Understand database instances and their lifecycle
- Recognize the role of databases in applications

## Why This Matters

Before diving deeper into SQL syntax, you need to understand the foundational concept of what a database actually is. This clarity helps you understand how applications interact with data storage and why databases are structured the way they are. Every application you build or support will rely on one or more databases.

## The Concept

### Definition of a Database

A **database** is an organized collection of structured data stored electronically. More specifically:

- **Organized**: Data follows a defined structure
- **Collection**: Multiple related pieces of information
- **Structured**: Data conforms to a model (relational, in our case)
- **Electronically stored**: Persisted on disk/storage systems

### Database vs. DBMS

These terms are often confused:

```
+-----------------------------------------------------------+
|                DATABASE MANAGEMENT SYSTEM (DBMS)           |
|                                                            |
|   +------------------+    +------------------+             |
|   |   Database A     |    |   Database B     |             |
|   |   (data files)   |    |   (data files)   |             |
|   +------------------+    +------------------+             |
|                                                            |
|   Query Engine | Transaction Manager | Security Manager    |
|   Buffer Pool  | Recovery System     | Lock Manager        |
+-----------------------------------------------------------+
```

| Term | Definition | Example |
|------|------------|---------|
| **Database** | The actual data and structure | "company_db" |
| **DBMS** | Software managing the database | PostgreSQL, MySQL |
| **Instance** | Running process of the DBMS | PostgreSQL server |

### Database Files

A database consists of multiple files on disk:

```
/var/lib/postgresql/data/
    base/                    -- Database files
        16384/              -- One database
            12345           -- Table data file
            12346           -- Index file
    pg_wal/                 -- Transaction logs
    pg_log/                 -- Server logs
    postgresql.conf         -- Configuration
```

You rarely interact with these files directly; the DBMS manages them for you.

### Creating and Managing Databases

```sql
-- Create a new database
CREATE DATABASE company_db;

-- Create with specific settings
CREATE DATABASE analytics_db
    WITH OWNER = data_team
    ENCODING = 'UTF8'
    TEMPLATE = template0;

-- List all databases (psql command)
\l

-- Connect to a database
\c company_db

-- Drop (delete) a database
DROP DATABASE test_db;
```

### Database Lifecycle

```
     CREATE              USE                MAINTAIN            DROP
        |                 |                    |                  |
        v                 v                    v                  v
+---------------+   +------------+   +----------------+   +------------+
| Define schema |-->| Insert,    |-->| Backup, Index, |-->| Archive or |
| Create tables |   | Query,     |   | Optimize,      |   | Delete     |
| Set up users  |   | Update     |   | Monitor        |   |            |
+---------------+   +------------+   +----------------+   +------------+
```

### System vs. User Databases

Most DBMS installations include system databases:

**PostgreSQL System Databases**:

- `postgres`: Default database for administration
- `template0`: Clean template (read-only)
- `template1`: Default template for new databases

**User Databases**:

- Created by developers/admins
- Contain application data
- Can be backed up, restored, moved

### Database Connection

Applications connect to databases using connection strings:

```
# PostgreSQL connection string format
postgresql://username:password@host:port/database_name

# Example
postgresql://app_user:secret123@localhost:5432/company_db

# Components:
# - Protocol: postgresql://
# - Username: app_user
# - Password: secret123
# - Host: localhost
# - Port: 5432 (default PostgreSQL port)
# - Database: company_db
```

### Multiple Databases vs. Single Database

**Multiple Databases** (when to use):

- Completely separate applications
- Different clients/tenants with data isolation
- Regulatory/compliance requirements

**Single Database with Schemas** (when to use):

- Related applications sharing data
- Microservices needing some shared tables
- Easier administration and backup

## Code Example

Database management operations:

```sql
-- Connect to PostgreSQL (as superuser)
psql -U postgres

-- View current database
SELECT current_database();

-- View current user
SELECT current_user;

-- Create a new database
CREATE DATABASE ecommerce_db;

-- View all databases with details
SELECT 
    datname AS database_name,
    pg_size_pretty(pg_database_size(datname)) AS size,
    datistemplate AS is_template
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Grant permissions to a user
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO app_user;

-- Connect to the new database
\c ecommerce_db

-- Create a table (we're now in ecommerce_db)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- View database statistics
SELECT * FROM pg_stat_database WHERE datname = 'ecommerce_db';
```

## Key Takeaways

- A database is an organized collection of structured data
- DBMS is the software; the database is the data itself
- Databases are created, used, maintained, and eventually retired
- PostgreSQL includes system databases and user databases
- Applications connect to databases using connection strings

## Additional Resources

- [PostgreSQL CREATE DATABASE](https://www.postgresql.org/docs/current/sql-createdatabase.html)
- [Database Administration Basics](https://www.postgresql.org/docs/current/admin.html)
- [Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
