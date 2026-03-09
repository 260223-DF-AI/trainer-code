# Stored Procedure Examples

## Learning Objectives

- Implement common stored procedure patterns
- Build error handling into procedures
- Create procedures for CRUD operations
- Apply procedures for business workflows

## Why This Matters

Seeing practical examples helps you apply stored procedures to real problems. These patterns form the building blocks for database-driven applications. Understanding these examples enables you to create your own procedures that encapsulate complex business logic safely and efficiently.

## The Concept

### Pattern 1: CRUD Operations

```sql
-- Create a complete CRUD interface for customers

-- CREATE
CREATE OR REPLACE PROCEDURE customer_create(
    p_name VARCHAR,
    p_email VARCHAR,
    p_phone VARCHAR DEFAULT NULL,
    OUT p_customer_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO customers (name, email, phone, created_at)
    VALUES (p_name, p_email, p_phone, NOW())
    RETURNING customer_id INTO p_customer_id;
END;
$$;

-- UPDATE
CREATE OR REPLACE PROCEDURE customer_update(
    p_customer_id INTEGER,
    p_name VARCHAR DEFAULT NULL,
    p_email VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers
    SET 
        name = COALESCE(p_name, name),
        email = COALESCE(p_email, email),
        phone = COALESCE(p_phone, phone),
        updated_at = NOW()
    WHERE customer_id = p_customer_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer % not found', p_customer_id;
    END IF;
END;
$$;

-- DELETE (soft delete)
CREATE OR REPLACE PROCEDURE customer_delete(
    p_customer_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers
    SET is_active = FALSE, deleted_at = NOW()
    WHERE customer_id = p_customer_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer % not found', p_customer_id;
    END IF;
END;
$$;
```

### Pattern 2: Bulk Operations

```sql
-- Bulk update prices by category
CREATE OR REPLACE PROCEDURE bulk_price_update(
    p_category VARCHAR,
    p_percentage DECIMAL,
    OUT p_updated_count INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE products
    SET price = price * (1 + p_percentage / 100),
        updated_at = NOW()
    WHERE category = p_category;
    
    GET DIAGNOSTICS p_updated_count = ROW_COUNT;
    
    RAISE NOTICE 'Updated % products in category %', 
        p_updated_count, p_category;
END;
$$;

-- Call
CALL bulk_price_update('Electronics', 10, NULL);  -- 10% increase
```

### Pattern 3: Archiving Data

```sql
-- Archive old orders
CREATE OR REPLACE PROCEDURE archive_old_orders(
    p_days_old INTEGER DEFAULT 365,
    OUT p_archived_count INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_cutoff_date DATE;
BEGIN
    v_cutoff_date := CURRENT_DATE - p_days_old;
    
    -- Copy to archive
    INSERT INTO orders_archive (order_id, customer_id, order_date, total, archived_at)
    SELECT order_id, customer_id, order_date, total, NOW()
    FROM orders
    WHERE order_date < v_cutoff_date;
    
    GET DIAGNOSTICS p_archived_count = ROW_COUNT;
    
    -- Delete archived orders
    DELETE FROM orders WHERE order_date < v_cutoff_date;
    
    COMMIT;
    
    RAISE NOTICE 'Archived % orders older than %', p_archived_count, v_cutoff_date;
END;
$$;
```

### Pattern 4: Business Workflow

```sql
-- Complete order fulfillment workflow
CREATE OR REPLACE PROCEDURE fulfill_order(
    p_order_id INTEGER,
    p_tracking_number VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_status VARCHAR;
    v_customer_email VARCHAR;
BEGIN
    -- Get order info
    SELECT o.status, c.email
    INTO v_current_status, v_customer_email
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_id = p_order_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order % not found', p_order_id;
    END IF;
    
    -- Validate status transition
    IF v_current_status != 'processing' THEN
        RAISE EXCEPTION 'Order must be in processing status. Current: %', v_current_status;
    END IF;
    
    -- Update order
    UPDATE orders
    SET status = 'shipped',
        tracking_number = p_tracking_number,
        shipped_at = NOW()
    WHERE order_id = p_order_id;
    
    -- Log the fulfillment
    INSERT INTO order_history (order_id, action, details, created_at)
    VALUES (p_order_id, 'SHIPPED', 
            jsonb_build_object('tracking', p_tracking_number), NOW());
    
    -- Queue notification (in real app, this triggers async process)
    INSERT INTO notifications (customer_email, type, data, created_at)
    VALUES (v_customer_email, 'ORDER_SHIPPED',
            jsonb_build_object('order_id', p_order_id, 'tracking', p_tracking_number),
            NOW());
    
    COMMIT;
END;
$$;
```

### Pattern 5: Report Generation

```sql
-- Generate monthly sales report
CREATE OR REPLACE PROCEDURE generate_sales_report(
    p_year INTEGER,
    p_month INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_start_date DATE;
    v_end_date DATE;
BEGIN
    v_start_date := make_date(p_year, p_month, 1);
    v_end_date := (v_start_date + INTERVAL '1 month')::DATE;
    
    -- Clear previous report
    DELETE FROM monthly_sales_report
    WHERE report_year = p_year AND report_month = p_month;
    
    -- Generate report
    INSERT INTO monthly_sales_report (
        report_year, report_month, category,
        order_count, total_revenue, avg_order_value
    )
    SELECT 
        p_year,
        p_month,
        p.category,
        COUNT(DISTINCT o.order_id),
        SUM(oi.quantity * oi.unit_price),
        AVG(o.total)
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_date >= v_start_date AND o_order_date < v_end_date
    GROUP BY p.category;
    
    COMMIT;
    
    RAISE NOTICE 'Report generated for %/%', p_year, p_month;
END;
$$;
```

### Pattern 6: Data Cleanup

```sql
-- Clean expired sessions
CREATE OR REPLACE PROCEDURE cleanup_expired_sessions(
    OUT p_deleted_count INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM user_sessions
    WHERE expires_at < NOW();
    
    GET DIAGNOSTICS p_deleted_count = ROW_COUNT;
    
    -- Log cleanup
    INSERT INTO cleanup_log (task_name, records_affected, executed_at)
    VALUES ('session_cleanup', p_deleted_count, NOW());
    
    COMMIT;
END;
$$;

-- Schedule this to run periodically
```

### Pattern 7: Audit Trail

```sql
-- Record all changes with detailed audit
CREATE OR REPLACE PROCEDURE update_with_audit(
    p_table_name VARCHAR,
    p_record_id INTEGER,
    p_field_name VARCHAR,
    p_new_value VARCHAR,
    p_changed_by VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_old_value VARCHAR;
    v_sql TEXT;
BEGIN
    -- Get current value
    v_sql := format('SELECT %I FROM %I WHERE id = $1', p_field_name, p_table_name);
    EXECUTE v_sql INTO v_old_value USING p_record_id;
    
    -- Update the record
    v_sql := format('UPDATE %I SET %I = $1 WHERE id = $2', p_table_name, p_field_name);
    EXECUTE v_sql USING p_new_value, p_record_id;
    
    -- Log the change
    INSERT INTO audit_trail (
        table_name, record_id, field_name, 
        old_value, new_value, changed_by, changed_at
    )
    VALUES (
        p_table_name, p_record_id, p_field_name,
        v_old_value, p_new_value, p_changed_by, NOW()
    );
    
    COMMIT;
END;
$$;
```

### Complete Example: User Management

```sql
-- Complete user management procedures
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Register user
CREATE OR REPLACE PROCEDURE register_user(
    p_username VARCHAR,
    p_password_hash VARCHAR,
    p_email VARCHAR,
    OUT p_user_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (username, password_hash, email)
    VALUES (p_username, p_password_hash, p_email)
    RETURNING user_id INTO p_user_id;
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'Username or email already exists';
END;
$$;

-- Login user (record attempt)
CREATE OR REPLACE PROCEDURE record_login_attempt(
    p_username VARCHAR,
    p_success BOOLEAN,
    OUT p_is_locked BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_success THEN
        UPDATE users
        SET login_attempts = 0, locked_until = NULL
        WHERE username = p_username;
        p_is_locked := FALSE;
    ELSE
        UPDATE users
        SET login_attempts = login_attempts + 1,
            locked_until = CASE 
                WHEN login_attempts >= 4 THEN NOW() + INTERVAL '15 minutes'
                ELSE locked_until
            END
        WHERE username = p_username;
        
        SELECT locked_until > NOW()
        INTO p_is_locked
        FROM users WHERE username = p_username;
    END IF;
END;
$$;
```

## Key Takeaways

- CRUD procedures provide consistent data access patterns
- Bulk operations should report affected row counts
- Workflow procedures orchestrate multi-step processes
- Always include proper error handling
- Use transactions for data consistency
- Logging and auditing should be built into procedures

## Additional Resources

- [PostgreSQL PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
- [Stored Procedure Best Practices](https://www.postgresql.org/docs/current/plpgsql-overview.html)
- [Error Handling](https://www.postgresql.org/docs/current/plpgsql-control-structures.html#PLPGSQL-ERROR-TRAPPING)
