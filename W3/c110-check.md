# Check

## Learning Objectives

- Understand CHECK constraints and their purpose
- Create column-level and table-level CHECK constraints
- Apply CHECK constraints for data validation
- Recognize limitations and alternatives

## Why This Matters

CHECK constraints provide a way to enforce custom business rules directly in the database. While NOT NULL handles presence and UNIQUE handles uniqueness, CHECK handles validity. By validating data at the database level, you prevent invalid data from ever being stored, regardless of which application or script accesses the database.

## The Concept

### What is a CHECK Constraint?

A **CHECK constraint** specifies a condition that must be true for any value in a column. If an INSERT or UPDATE would make the condition false, the operation is rejected.

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10, 2) CHECK (price >= 0),  -- No negative prices
    quantity INTEGER CHECK (quantity >= 0)    -- No negative quantities
);
```

### Column-Level CHECK

Applied to a single column:

```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) CHECK (salary > 0),
    age INTEGER CHECK (age BETWEEN 18 AND 100),
    hire_date DATE CHECK (hire_date <= CURRENT_DATE)
);
```

### Table-Level CHECK

Can reference multiple columns:

```sql
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT valid_dates CHECK (end_date >= start_date)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2),
    sale_price DECIMAL(10,2),
    CONSTRAINT valid_sale_price CHECK (sale_price IS NULL OR sale_price < price)
);
```

### Named CHECK Constraints

Name your constraints for better error messages:

```sql
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    balance DECIMAL(12, 2),
    CONSTRAINT positive_balance CHECK (balance >= 0),
    CONSTRAINT reasonable_balance CHECK (balance <= 999999999.99)
);

-- Error will reference constraint name:
-- ERROR: new row violates check constraint "positive_balance"
```

### Common CHECK Patterns

**Range Validation**:

```sql
CHECK (age >= 0 AND age <= 150)
CHECK (age BETWEEN 0 AND 150)
CHECK (rating BETWEEN 1 AND 5)
CHECK (percentage >= 0 AND percentage <= 100)
```

**Enumeration (Limited Values)**:

```sql
CHECK (status IN ('pending', 'approved', 'rejected'))
CHECK (priority IN ('low', 'medium', 'high', 'critical'))
CHECK (gender IN ('M', 'F', 'O'))
```

**Pattern Validation**:

```sql
CHECK (email LIKE '%@%.%')
CHECK (phone ~ '^[0-9]{3}-[0-9]{3}-[0-9]{4}$')  -- PostgreSQL regex
CHECK (sku ~ '^[A-Z]{3}-[0-9]{4}$')
```

**Comparison with Other Columns**:

```sql
CHECK (start_date <= end_date)
CHECK (sale_price < regular_price)
CHECK (min_value <= max_value)
```

**Complex Logic**:

```sql
CHECK (
    (discount_type = 'percentage' AND discount_value <= 100)
    OR (discount_type = 'fixed' AND discount_value <= price)
)
```

### Adding CHECK to Existing Table

```sql
-- Add check constraint
ALTER TABLE products ADD CONSTRAINT chk_positive_price CHECK (price > 0);

-- With validation of existing data (default)
ALTER TABLE products ADD CONSTRAINT chk_quantity CHECK (quantity >= 0);

-- Skip validation of existing data (dangerous but faster)
ALTER TABLE products ADD CONSTRAINT chk_stock 
    CHECK (stock >= 0) NOT VALID;

-- Drop constraint
ALTER TABLE products DROP CONSTRAINT chk_positive_price;
```

### CHECK vs ENUM

PostgreSQL offers two approaches for limited values:

**CHECK Constraint**:

```sql
status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'deleted'))
```

**PostgreSQL ENUM Type**:

```sql
CREATE TYPE status_type AS ENUM ('active', 'inactive', 'deleted');
status status_type NOT NULL
```

| Aspect | CHECK | ENUM |
|--------|-------|------|
| Add new value | Easy | Requires ALTER TYPE |
| Remove value | Easy | Difficult |
| Type safety | String | Dedicated type |
| Storage | Full string | 4 bytes |

### Limitations of CHECK

CHECK constraints cannot:

- Reference other tables (use triggers or FK instead)
- Call user-defined functions (in some databases)
- Reference other rows in the same table (use triggers)

```sql
-- This WON'T work (references another table):
CHECK (department_id IN (SELECT department_id FROM departments))

-- Use foreign key instead:
FOREIGN KEY (department_id) REFERENCES departments(department_id)
```

## Code Example

Comprehensive CHECK constraint usage:

```sql
-- Create table with various CHECK constraints
CREATE TABLE job_applications (
    application_id SERIAL PRIMARY KEY,
    applicant_name VARCHAR(100) NOT NULL 
        CHECK (LENGTH(applicant_name) >= 2),
    email VARCHAR(100) NOT NULL 
        CHECK (email LIKE '%@%.%'),
    phone VARCHAR(20) 
        CHECK (phone ~ '^[0-9]{3}-[0-9]{3}-[0-9]{4}$'),
    years_experience INTEGER 
        CHECK (years_experience >= 0 AND years_experience <= 50),
    salary_expectation DECIMAL(10, 2) 
        CHECK (salary_expectation > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'reviewing', 'interview', 'offer', 'rejected', 'hired')),
    applied_date DATE NOT NULL DEFAULT CURRENT_DATE
        CHECK (applied_date <= CURRENT_DATE),
    available_date DATE,
    CONSTRAINT future_availability CHECK (available_date IS NULL OR available_date >= CURRENT_DATE),
    CONSTRAINT experience_salary_match CHECK (
        salary_expectation IS NULL 
        OR years_experience IS NULL 
        OR salary_expectation >= (40000 + years_experience * 2000)
    )
);

-- Valid inserts
INSERT INTO job_applications (applicant_name, email, years_experience, salary_expectation, status)
VALUES ('Alice Johnson', 'alice@email.com', 5, 60000, 'pending');

INSERT INTO job_applications (applicant_name, email, phone)
VALUES ('Bob Smith', 'bob@email.com', '555-123-4567');

-- Invalid inserts (will fail)
-- Invalid email
INSERT INTO job_applications (applicant_name, email)
VALUES ('Test User', 'invalid-email');
-- ERROR: violates check constraint

-- Invalid status
INSERT INTO job_applications (applicant_name, email, status)
VALUES ('Test User', 'test@email.com', 'unknown');
-- ERROR: violates check constraint

-- Negative experience
INSERT INTO job_applications (applicant_name, email, years_experience)
VALUES ('Test User', 'test@email.com', -5);
-- ERROR: violates check constraint

-- View all constraints
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'job_applications'::regclass;
```

## Key Takeaways

- CHECK constraints enforce custom validation rules
- Can validate ranges, patterns, and multi-column conditions
- Name constraints for clearer error messages
- Cannot reference other tables (use FK or triggers)
- Use column-level for single-column checks, table-level for multi-column

## Additional Resources

- [PostgreSQL CHECK Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS)
- [Pattern Matching](https://www.postgresql.org/docs/current/functions-matching.html)
- [ALTER TABLE ADD CONSTRAINT](https://www.postgresql.org/docs/current/sql-altertable.html)
