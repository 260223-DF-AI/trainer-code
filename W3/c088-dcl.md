# DCL: Data Control Language

## Learning Objectives

- Understand DCL commands: GRANT and REVOKE
- Learn to manage user permissions
- Apply the principle of least privilege
- Recognize common permission patterns

## Why This Matters

Database security is critical in any organization. DCL commands control who can do what with your data. A single misconfigured permission can expose sensitive information or allow unauthorized modifications. Understanding GRANT and REVOKE helps you implement proper access controls and maintain data security.

## The Concept

### What is DCL?

Data Control Language (DCL) consists of SQL commands that manage access permissions. DCL determines which users can perform which operations on which objects.

### DCL Commands

| Command | Purpose |
|---------|---------|
| GRANT | Give permissions to users/roles |
| REVOKE | Remove permissions from users/roles |

### Understanding Permissions

PostgreSQL permissions (also called privileges) include:

| Permission | Applies To | Allows |
|------------|------------|--------|
| SELECT | Tables, Views, Sequences | Read data |
| INSERT | Tables | Add new rows |
| UPDATE | Tables | Modify existing rows |
| DELETE | Tables | Remove rows |
| TRUNCATE | Tables | Remove all rows |
| REFERENCES | Tables | Create foreign keys |
| USAGE | Schemas, Sequences | Access objects |
| CREATE | Databases, Schemas | Create new objects |
| ALL | Various | All available permissions |

### GRANT Syntax

```sql
-- Grant specific permission
GRANT permission ON object TO user;

-- Grant multiple permissions
GRANT permission1, permission2, ... ON object TO user;

-- Grant to multiple users
GRANT permission ON object TO user1, user2;

-- Grant with grant option (user can grant to others)
GRANT permission ON object TO user WITH GRANT OPTION;
```

### GRANT Examples

**Table Permissions**:

```sql
-- Allow reading data
GRANT SELECT ON employees TO report_user;

-- Allow modifying data
GRANT INSERT, UPDATE, DELETE ON orders TO app_user;

-- Allow all operations on a table
GRANT ALL ON products TO admin_user;

-- Allow select on all tables in schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
```

**Schema Permissions**:

```sql
-- Allow access to schema objects
GRANT USAGE ON SCHEMA hr TO hr_user;

-- Allow creating objects in schema
GRANT CREATE ON SCHEMA development TO developer;

-- Combined: can use and create
GRANT USAGE, CREATE ON SCHEMA reports TO analyst;
```

**Database Permissions**:

```sql
-- Allow connecting to database
GRANT CONNECT ON DATABASE company TO app_user;

-- Allow creating new schemas
GRANT CREATE ON DATABASE company TO lead_developer;
```

### REVOKE Syntax

```sql
-- Revoke specific permission
REVOKE permission ON object FROM user;

-- Revoke all permissions
REVOKE ALL ON object FROM user;

-- Revoke grant option only (keep permission)
REVOKE GRANT OPTION FOR permission ON object FROM user;
```

### REVOKE Examples

```sql
-- Remove select permission
REVOKE SELECT ON employees FROM former_employee;

-- Remove multiple permissions
REVOKE INSERT, UPDATE ON orders FROM contractor;

-- Remove all permissions
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM guest_user;

-- Remove schema access
REVOKE USAGE ON SCHEMA hr FROM sales_team;
```

### Roles and Users

PostgreSQL uses roles to manage permissions:

```sql
-- Create a role (group of permissions)
CREATE ROLE read_only;
CREATE ROLE data_entry;
CREATE ROLE full_access;

-- Grant permissions to roles
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO data_entry;
GRANT ALL ON ALL TABLES IN SCHEMA public TO full_access;

-- Assign roles to users
GRANT read_only TO analyst_user;
GRANT data_entry TO clerk_user;
GRANT full_access TO admin_user;

-- Remove role from user
REVOKE data_entry FROM clerk_user;
```

### Default Privileges

Set permissions for future objects:

```sql
-- Future tables in schema inherit these grants
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO read_only;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE ON SEQUENCES TO app_user;
```

### Principle of Least Privilege

Grant only the permissions needed:

```sql
-- BAD: Too permissive
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_user;

-- GOOD: Specific permissions
GRANT SELECT ON products TO app_user;
GRANT SELECT, INSERT ON orders TO app_user;
GRANT SELECT, INSERT, UPDATE ON order_items TO app_user;
```

### Common Permission Patterns

**Read-Only Reporting User**:

```sql
CREATE ROLE reporting_ro;
GRANT USAGE ON SCHEMA public TO reporting_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporting_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT ON TABLES TO reporting_ro;
```

**Application User**:

```sql
CREATE ROLE app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

**Developer Read-Only to Production**:

```sql
CREATE ROLE dev_readonly;
GRANT CONNECT ON DATABASE production TO dev_readonly;
GRANT USAGE ON SCHEMA public TO dev_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO dev_readonly;
-- NO insert, update, delete!
```

## Code Example

Complete permission management workflow:

```sql
-- Create roles for different access levels
CREATE ROLE app_readonly;
CREATE ROLE app_readwrite;
CREATE ROLE app_admin;

-- Create a user and assign role
CREATE USER analyst_alice WITH PASSWORD 'secure_password';
GRANT app_readonly TO analyst_alice;

CREATE USER developer_bob WITH PASSWORD 'another_password';
GRANT app_readwrite TO developer_bob;

-- Set up schema permissions
GRANT USAGE ON SCHEMA public TO app_readonly, app_readwrite, app_admin;

-- Table permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_admin;

-- Sequence permissions (for auto-increment)
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_readwrite, app_admin;

-- Set defaults for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO app_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_readwrite;

-- View permissions
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY grantee, table_name;

-- Later: revoke access when employee leaves
REVOKE app_readwrite FROM developer_bob;
DROP USER developer_bob;
```

## Key Takeaways

- GRANT gives permissions; REVOKE removes them
- Use roles to manage groups of permissions
- Apply the principle of least privilege
- Set default privileges for future objects
- Always test permissions before production deployment

## Additional Resources

- [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- [PostgreSQL Role System](https://www.postgresql.org/docs/current/user-manag.html)
- [Database Security Best Practices](https://www.postgresql.org/docs/current/ddl-priv.html)
