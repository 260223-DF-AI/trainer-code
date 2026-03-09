# FULL OUTER JOIN

## Learning Objectives

- Understand FULL OUTER JOIN behavior
- Write FULL JOIN queries
- Identify use cases for FULL JOIN
- Handle NULL values from both sides

## Why This Matters

FULL OUTER JOIN preserves all rows from both tables, which is essential when you need to see the complete picture, including unmatched records on both sides. It is commonly used for data reconciliation, comparing datasets, and finding discrepancies.

## The Concept

### What is FULL OUTER JOIN?

**FULL OUTER JOIN** (or FULL JOIN) returns all rows from both tables. Rows without matches on either side show NULL for the missing columns.

```
left_table:          right_table:         FULL JOIN result:
| id | left_val |    | id | right_val |   | left_val | right_val |
|----|----------|    |----|-----------|   |----------|-----------|
| 1  | A        |    | 2  | X         |   | A        | NULL      |
| 2  | B        |    | 3  | Y         |   | B        | X         |
|    |          |    |    |           |   | NULL     | Y         |

Row 1 (A) has no match in right table
Row 3 (Y) has no match in left table
Row 2 (B, X) matched
```

### Basic Syntax

```sql
SELECT columns
FROM left_table
FULL OUTER JOIN right_table ON left_table.column = right_table.column;

-- OUTER is optional
SELECT columns
FROM left_table
FULL JOIN right_table ON left_table.column = right_table.column;
```

### FULL JOIN Examples

**Compare two datasets**:

```sql
-- All students and all enrollments, showing gaps on both sides
SELECT s.name AS student, e.course_name
FROM students s
FULL JOIN enrollments e ON s.student_id = e.student_id;
```

**Data reconciliation**:

```sql
-- Compare inventory systems
SELECT 
    w1.product_id AS warehouse1_id,
    w1.quantity AS warehouse1_qty,
    w2.product_id AS warehouse2_id,
    w2.quantity AS warehouse2_qty
FROM warehouse1 w1
FULL JOIN warehouse2 w2 ON w1.product_id = w2.product_id;
```

### Finding Discrepancies

FULL JOIN excels at finding unmatched records on both sides:

```sql
-- All discrepancies between two systems
SELECT 
    COALESCE(old.id, new.id) AS record_id,
    old.value AS old_value,
    new.value AS new_value
FROM old_system old
FULL JOIN new_system new ON old.id = new.id
WHERE old.id IS NULL          -- Only in new system
   OR new.id IS NULL          -- Only in old system
   OR old.value != new.value; -- Different values
```

### Combining with COALESCE

Use COALESCE to handle NULLs from both sides:

```sql
SELECT 
    COALESCE(a.id, b.id) AS id,
    COALESCE(a.name, 'Not in A') AS name_a,
    COALESCE(b.name, 'Not in B') AS name_b,
    CASE 
        WHEN a.id IS NULL THEN 'Only in B'
        WHEN b.id IS NULL THEN 'Only in A'
        ELSE 'In Both'
    END AS status
FROM table_a a
FULL JOIN table_b b ON a.id = b.id;
```

### FULL JOIN vs Other Joins

```
INNER JOIN:  Only matched rows
LEFT JOIN:   All left + matched right
RIGHT JOIN:  All right + matched left
FULL JOIN:   All left + all right
```

```sql
-- Given:
-- employees: Alice (dept 1), Bob (dept 2), Carol (dept NULL)
-- departments: Engineering (1), Sales (2), Marketing (3)

-- FULL JOIN shows everything
SELECT e.name, d.dept_name
FROM employees e
FULL JOIN departments d ON e.department_id = d.department_id;

-- Result:
-- Alice, Engineering     (matched)
-- Bob, Sales             (matched)
-- Carol, NULL            (employee without dept)
-- NULL, Marketing        (dept without employees)
```

### Use Cases

1. **Data migration verification**: Compare old and new systems
2. **System reconciliation**: Match records between databases
3. **Finding orphaned data**: Records without relationships
4. **Complete reporting**: Show all data regardless of matches

## Code Example

Comprehensive FULL JOIN usage:

```sql
-- Create tables for data reconciliation scenario
CREATE TABLE system_a (
    record_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    balance DECIMAL(10, 2)
);

CREATE TABLE system_b (
    record_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    balance DECIMAL(10, 2)
);

-- Insert sample data with intentional discrepancies
INSERT INTO system_a VALUES
    (1, 'Alice', 1000.00),
    (2, 'Bob', 500.00),
    (3, 'Carol', 750.00),
    (5, 'Eve', 200.00);   -- Only in System A

INSERT INTO system_b VALUES
    (1, 'Alice', 1000.00),
    (2, 'Bob', 550.00),   -- Different balance
    (3, 'Carol', 750.00),
    (4, 'David', 300.00); -- Only in System B

-- FULL JOIN to see complete picture
SELECT 
    COALESCE(a.record_id, b.record_id) AS id,
    a.customer_name AS name_a,
    a.balance AS balance_a,
    b.customer_name AS name_b,
    b.balance AS balance_b
FROM system_a a
FULL JOIN system_b b ON a.record_id = b.record_id
ORDER BY COALESCE(a.record_id, b.record_id);

-- Identify discrepancies
SELECT 
    COALESCE(a.record_id, b.record_id) AS id,
    COALESCE(a.customer_name, b.customer_name) AS customer,
    CASE 
        WHEN a.record_id IS NULL THEN 'Missing in A'
        WHEN b.record_id IS NULL THEN 'Missing in B'
        WHEN a.balance != b.balance THEN 'Balance mismatch'
        ELSE 'OK'
    END AS status,
    a.balance AS balance_a,
    b.balance AS balance_b
FROM system_a a
FULL JOIN system_b b ON a.record_id = b.record_id
WHERE a.record_id IS NULL 
   OR b.record_id IS NULL 
   OR a.balance != b.balance;

-- Summary statistics
SELECT 
    COUNT(*) AS total_records,
    COUNT(a.record_id) AS in_system_a,
    COUNT(b.record_id) AS in_system_b,
    COUNT(CASE WHEN a.record_id IS NOT NULL AND b.record_id IS NOT NULL THEN 1 END) AS in_both,
    COUNT(CASE WHEN a.record_id IS NULL THEN 1 END) AS only_in_b,
    COUNT(CASE WHEN b.record_id IS NULL THEN 1 END) AS only_in_a
FROM system_a a
FULL JOIN system_b b ON a.record_id = b.record_id;

-- Employee-Department complete picture
CREATE TABLE emp (emp_id INT, name VARCHAR(50), dept_id INT);
CREATE TABLE dept (dept_id INT, dept_name VARCHAR(50));

INSERT INTO emp VALUES (1, 'Alice', 1), (2, 'Bob', 2), (3, 'Carol', NULL);
INSERT INTO dept VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'Marketing');

SELECT 
    e.name AS employee,
    COALESCE(d.dept_name, 'No Department') AS department,
    CASE 
        WHEN e.emp_id IS NULL THEN 'Empty Department'
        WHEN d.dept_id IS NULL THEN 'No Department Assigned'
        ELSE 'Assigned'
    END AS status
FROM emp e
FULL JOIN dept d ON e.dept_id = d.dept_id;
```

## Key Takeaways

- FULL OUTER JOIN returns all rows from both tables
- Unmatched rows show NULL for the missing side
- Essential for data reconciliation and comparison
- Use COALESCE to handle NULLs from both sides
- Combine with WHERE to find discrepancies
- Less common than INNER/LEFT but important for specific use cases

## Additional Resources

- [PostgreSQL FULL JOIN](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Outer Joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM)
- [COALESCE Function](https://www.postgresql.org/docs/current/functions-conditional.html)
