# What Is SQL

## Learning Objectives

- Define SQL as a declarative programming language
- Understand the difference between declarative and imperative approaches
- Recognize common SQL dialects and their variations
- Identify the core components of SQL statements

## Why This Matters

Understanding what SQL truly is helps you approach database work with the right mindset. Unlike Python where you write step-by-step instructions, SQL requires thinking in terms of *results* rather than *procedures*. This shift in perspective is fundamental to writing effective queries and designing efficient database solutions.

## The Concept

### SQL: A Declarative Language

SQL is fundamentally different from languages like Python or Java. It is a **declarative language**, meaning you declare *what* result you want, and the database engine determines *how* to achieve it.

**Imperative (Python)**:

```python
# Step-by-step instructions
results = []
for employee in employees:
    if employee.salary > 50000:
        results.append(employee.name)
results.sort()
```

**Declarative (SQL)**:

```sql
-- Declare the desired result
SELECT name
FROM employees
WHERE salary > 50000
ORDER BY name;
```

In SQL, you describe the outcome. The database's query optimizer figures out the most efficient execution plan.

### The Four Main SQL Operations

SQL operations can be categorized using the acronym **CRUD**:

| Operation | SQL Command | Description |
|-----------|-------------|-------------|
| **C**reate | INSERT | Add new records |
| **R**ead | SELECT | Retrieve data |
| **U**pdate | UPDATE | Modify existing records |
| **D**elete | DELETE | Remove records |

### SQL Statement Structure

A typical SQL statement follows this pattern:

```sql
COMMAND column_list
FROM table_name
WHERE conditions
ORDER BY column;
```

Each clause serves a specific purpose:

- **Command**: What operation to perform (SELECT, INSERT, etc.)
- **FROM**: Which table(s) to work with
- **WHERE**: Conditions to filter data
- **ORDER BY**: How to sort results

### SQL Dialects

While SQL is standardized, each database vendor implements extensions and variations:

| Dialect | Database | Notable Features |
|---------|----------|------------------|
| PostgreSQL | PostgreSQL | Arrays, JSON, advanced types |
| T-SQL | SQL Server | Procedural extensions |
| PL/SQL | Oracle | Extensive procedural language |
| MySQL | MySQL/MariaDB | Simplified syntax |
| SQLite | SQLite | Lightweight, file-based |

The core SQL syntax (SELECT, INSERT, UPDATE, DELETE) works across all dialects. Differences appear in:

- Data types available
- Built-in functions
- Procedural extensions
- Advanced features

### Case Sensitivity

SQL has specific rules for case:

```sql
-- Keywords are case-insensitive (both work)
SELECT * FROM employees;
select * from employees;

-- Convention: Keywords UPPERCASE, identifiers lowercase
SELECT first_name, last_name
FROM employees
WHERE department_id = 10;
```

Best practice: Use UPPERCASE for SQL keywords and lowercase for table/column names for readability.

### Comments in SQL

```sql
-- This is a single-line comment

/* This is a
   multi-line comment */

SELECT first_name,  -- inline comment
       last_name
FROM employees;
```

## Code Example

Here is a complete SQL statement demonstrating multiple clauses:

```sql
-- Find high-earning employees in specific departments
SELECT 
    employee_id,
    first_name,
    last_name,
    salary,
    department
FROM 
    employees
WHERE 
    salary >= 75000
    AND department IN ('Engineering', 'Data Science')
ORDER BY 
    salary DESC;
```

This query:

1. Selects specific columns from the employees table
2. Filters for salaries at or above 75,000
3. Further filters for specific departments
4. Orders results by salary in descending order

## Key Takeaways

- SQL is declarative: describe results, not procedures
- CRUD operations (Create, Read, Update, Delete) form the core of SQL
- SQL is standardized but has vendor-specific dialects
- Core syntax transfers across database systems
- Convention uses UPPERCASE for keywords, lowercase for identifiers

## Additional Resources

- [SQL Language Reference - PostgreSQL](https://www.postgresql.org/docs/current/sql.html)
- [ANSI SQL Standards Overview](https://blog.ansi.org/sql-standard-iso-iec-9075-2023-ansi-x3-702/)
- [SQL Style Guide](https://www.sqlstyle.guide/) - Best practices for formatting
