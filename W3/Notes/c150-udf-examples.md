# User-Defined Function Examples

## Learning Objectives

- Implement practical UDFs for common scenarios
- Build calculation, formatting, and validation functions
- Create table-returning functions for reporting
- Apply functions to simplify complex queries

## Why This Matters

Practical examples help you recognize where functions fit in your own databases. These patterns can be adapted for date calculations, string manipulation, business rule validation, and data transformation - common needs in every database-driven application.

## The Concept

### Pattern 1: Data Formatting

```sql
-- Format phone number
CREATE OR REPLACE FUNCTION format_phone(p_phone VARCHAR)
RETURNS VARCHAR
IMMUTABLE
LANGUAGE plpgsql
AS $$
DECLARE
    v_digits VARCHAR;
BEGIN
    -- Extract only digits
    v_digits := regexp_replace(p_phone, '[^0-9]', '', 'g');
    
    -- Format based on length
    IF length(v_digits) = 10 THEN
        RETURN '(' || substr(v_digits, 1, 3) || ') ' ||
               substr(v_digits, 4, 3) || '-' ||
               substr(v_digits, 7, 4);
    ELSIF length(v_digits) = 11 THEN
        RETURN '+' || substr(v_digits, 1, 1) || ' (' || 
               substr(v_digits, 2, 3) || ') ' ||
               substr(v_digits, 5, 3) || '-' ||
               substr(v_digits, 8, 4);
    ELSE
        RETURN p_phone;  -- Return original if unknown format
    END IF;
END;
$$;

SELECT format_phone('5551234567');    -- (555) 123-4567
SELECT format_phone('1-555-123-4567'); -- +1 (555) 123-4567
```

### Pattern 2: Date Calculations

```sql
-- Calculate business days between dates
CREATE OR REPLACE FUNCTION business_days_between(
    p_start DATE,
    p_end DATE
)
RETURNS INTEGER
IMMUTABLE
LANGUAGE plpgsql
AS $$
DECLARE
    v_count INTEGER := 0;
    v_current DATE := p_start;
BEGIN
    WHILE v_current <= p_end LOOP
        -- Check if weekday (1=Monday to 7=Sunday)
        IF EXTRACT(ISODOW FROM v_current) < 6 THEN
            v_count := v_count + 1;
        END IF;
        v_current := v_current + 1;
    END LOOP;
    
    RETURN v_count;
END;
$$;

SELECT business_days_between('2024-01-01', '2024-01-15'); -- 11

-- Age calculation with units
CREATE OR REPLACE FUNCTION age_in_units(
    p_birthdate DATE,
    p_unit VARCHAR DEFAULT 'years'
)
RETURNS INTEGER
STABLE
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN CASE lower(p_unit)
        WHEN 'years' THEN EXTRACT(YEAR FROM age(CURRENT_DATE, p_birthdate))::INTEGER
        WHEN 'months' THEN (EXTRACT(YEAR FROM age(CURRENT_DATE, p_birthdate)) * 12 +
                           EXTRACT(MONTH FROM age(CURRENT_DATE, p_birthdate)))::INTEGER
        WHEN 'days' THEN (CURRENT_DATE - p_birthdate)::INTEGER
        ELSE NULL
    END;
END;
$$;

SELECT age_in_units('1990-05-15');           -- 34 (years)
SELECT age_in_units('1990-05-15', 'months'); -- 408
SELECT age_in_units('1990-05-15', 'days');   -- 12345
```

### Pattern 3: Validation Functions

```sql
-- Validate email format
CREATE OR REPLACE FUNCTION is_valid_email(p_email VARCHAR)
RETURNS BOOLEAN
IMMUTABLE
LANGUAGE sql
AS $$
    SELECT p_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
$$;

-- Validate credit card (Luhn algorithm)
CREATE OR REPLACE FUNCTION is_valid_credit_card(p_number VARCHAR)
RETURNS BOOLEAN
IMMUTABLE
LANGUAGE plpgsql
AS $$
DECLARE
    v_digits VARCHAR;
    v_sum INTEGER := 0;
    v_digit INTEGER;
    v_double BOOLEAN := FALSE;
BEGIN
    v_digits := reverse(regexp_replace(p_number, '[^0-9]', '', 'g'));
    
    FOR i IN 1..length(v_digits) LOOP
        v_digit := substr(v_digits, i, 1)::INTEGER;
        
        IF v_double THEN
            v_digit := v_digit * 2;
            IF v_digit > 9 THEN
                v_digit := v_digit - 9;
            END IF;
        END IF;
        
        v_sum := v_sum + v_digit;
        v_double := NOT v_double;
    END LOOP;
    
    RETURN v_sum % 10 = 0;
END;
$$;

SELECT is_valid_email('test@example.com');   -- true
SELECT is_valid_credit_card('4532015112830366'); -- true (test number)
```

### Pattern 4: Business Calculations

```sql
-- Calculate compound interest
CREATE OR REPLACE FUNCTION compound_interest(
    p_principal DECIMAL,
    p_rate DECIMAL,  -- Annual rate as decimal (0.05 = 5%)
    p_years INTEGER,
    p_compounds_per_year INTEGER DEFAULT 12
)
RETURNS DECIMAL
IMMUTABLE
LANGUAGE sql
AS $$
    SELECT ROUND(
        p_principal * POWER(
            1 + (p_rate / p_compounds_per_year),
            p_compounds_per_year * p_years
        ),
        2
    );
$$;

SELECT compound_interest(10000, 0.05, 5);  -- 12833.59

-- Calculate sales tax
CREATE OR REPLACE FUNCTION calculate_tax(
    p_amount DECIMAL,
    p_state VARCHAR DEFAULT 'CA'
)
RETURNS DECIMAL
STABLE
LANGUAGE plpgsql
AS $$
DECLARE
    v_rate DECIMAL;
BEGIN
    SELECT tax_rate INTO v_rate
    FROM state_tax_rates
    WHERE state_code = p_state;
    
    IF NOT FOUND THEN
        v_rate := 0;
    END IF;
    
    RETURN ROUND(p_amount * v_rate, 2);
END;
$$;
```

### Pattern 5: Table-Returning Functions

```sql
-- Date range generator
CREATE OR REPLACE FUNCTION generate_dates(
    p_start DATE,
    p_end DATE
)
RETURNS TABLE (dt DATE)
IMMUTABLE
LANGUAGE sql
AS $$
    SELECT generate_series(p_start, p_end, '1 day'::INTERVAL)::DATE;
$$;

SELECT * FROM generate_dates('2024-01-01', '2024-01-07');

-- Sales report function
CREATE OR REPLACE FUNCTION sales_by_period(
    p_start_date DATE,
    p_end_date DATE,
    p_group_by VARCHAR DEFAULT 'day'  -- day, week, month
)
RETURNS TABLE (
    period DATE,
    order_count BIGINT,
    total_revenue DECIMAL,
    avg_order DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE_TRUNC(p_group_by, o.order_date)::DATE,
        COUNT(*)::BIGINT,
        SUM(o.total),
        AVG(o.total)
    FROM orders o
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    GROUP BY DATE_TRUNC(p_group_by, o.order_date)
    ORDER BY 1;
END;
$$;

SELECT * FROM sales_by_period('2024-01-01', '2024-03-31', 'month');
```

### Pattern 6: Text Manipulation

```sql
-- Title case conversion
CREATE OR REPLACE FUNCTION title_case(p_text VARCHAR)
RETURNS VARCHAR
IMMUTABLE
LANGUAGE sql
AS $$
    SELECT initcap(lower(p_text));
$$;

-- Generate slug from title
CREATE OR REPLACE FUNCTION slugify(p_text VARCHAR)
RETURNS VARCHAR
IMMUTABLE
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN lower(
        regexp_replace(
            regexp_replace(
                trim(p_text),
                '[^a-zA-Z0-9\s-]', '', 'g'  -- Remove special chars
            ),
            '\s+', '-', 'g'  -- Replace spaces with hyphens
        )
    );
END;
$$;

SELECT slugify('Hello World! This is a Test'); -- hello-world-this-is-a-test

-- Mask sensitive data
CREATE OR REPLACE FUNCTION mask_email(p_email VARCHAR)
RETURNS VARCHAR
IMMUTABLE
LANGUAGE plpgsql
AS $$
DECLARE
    v_at_pos INTEGER;
BEGIN
    v_at_pos := position('@' in p_email);
    IF v_at_pos <= 2 THEN
        RETURN '***' || substr(p_email, v_at_pos);
    ELSE
        RETURN substr(p_email, 1, 1) || repeat('*', v_at_pos - 2) || substr(p_email, v_at_pos);
    END IF;
END;
$$;

SELECT mask_email('john.smith@email.com');  -- j*********@email.com
```

### Using Functions in Constraints

```sql
-- Use validation function in CHECK constraint
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT valid_email CHECK (is_valid_email(email))
);

INSERT INTO users (email) VALUES ('valid@email.com');   -- OK
INSERT INTO users (email) VALUES ('invalid-email');     -- Fails
```

## Key Takeaways

- Formatting functions standardize data display
- Validation functions enforce data quality
- Date/time functions simplify temporal calculations
- Table-returning functions enable dynamic reporting
- Functions can be used in CHECK constraints
- Mark IMMUTABLE/STABLE appropriately for performance

## Additional Resources

- [PostgreSQL String Functions](https://www.postgresql.org/docs/current/functions-string.html)
- [Date/Time Functions](https://www.postgresql.org/docs/current/functions-datetime.html)
- [Pattern Matching](https://www.postgresql.org/docs/current/functions-matching.html)
