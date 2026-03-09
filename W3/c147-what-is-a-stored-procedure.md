# What Is a Stored Procedure

## Learning Objectives

- Understand stored procedures and their purpose
- Differentiate stored procedures from functions
- Create stored procedures in PostgreSQL
- Apply stored procedures for common use cases

## Why This Matters

Stored procedures encapsulate business logic in the database layer. They improve security by limiting direct table access, enhance performance by reducing network round trips, and ensure consistent execution of complex operations. Understanding stored procedures is essential for building enterprise applications with centralized business rules.

## The Concept

### What is a Stored Procedure?

A stored procedure is a set of SQL statements stored in the database that can be executed as a unit. It's like a saved script that runs on the server.

```
Application            Database
    |                     |
    | CALL my_procedure() |
    |-------------------->|
    |                     | Execute multiple
    |                     | SQL statements
    |                     |
    |     Result          |
    |<--------------------|
```

### Procedures vs Functions

| Aspect | Procedure | Function |
|--------|-----------|----------|
| Return value | Optional, via OUT params | Required |
| Use in SELECT | No | Yes |
| Transaction control | COMMIT/ROLLBACK allowed | Not allowed |
| Purpose | Actions/side effects | Compute values |
| Call syntax | `CALL procedure()` | `SELECT function()` |

### Creating a Stored Procedure

```sql
CREATE OR REPLACE PROCEDURE procedure_name(
    param1 datatype,
    param2 datatype
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- SQL statements here
END;
$$;
```

### Basic Procedure Example

```sql
-- Simple procedure to add a customer
CREATE OR REPLACE PROCEDURE add_customer(
    p_name VARCHAR,
    p_email VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO customers (name, email, created_at)
    VALUES (p_name, p_email, NOW());
END;
$$;

-- Call the procedure
CALL add_customer('Alice Smith', 'alice@email.com');
```

### Procedure with OUT Parameters

```sql
CREATE OR REPLACE PROCEDURE get_order_stats(
    p_customer_id INTEGER,
    OUT p_total_orders INTEGER,
    OUT p_total_spent DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*), COALESCE(SUM(total), 0)
    INTO p_total_orders, p_total_spent
    FROM orders
    WHERE customer_id = p_customer_id;
END;
$$;

-- Call with OUT parameters
CALL get_order_stats(1, NULL, NULL);
-- Or capture results
DO $$
DECLARE
    v_orders INTEGER;
    v_spent DECIMAL;
BEGIN
    CALL get_order_stats(1, v_orders, v_spent);
    RAISE NOTICE 'Orders: %, Spent: %', v_orders, v_spent;
END;
$$;
```

### Procedure with Transaction Control

Procedures can commit or rollback:

```sql
CREATE OR REPLACE PROCEDURE transfer_funds(
    p_from_account INTEGER,
    p_to_account INTEGER,
    p_amount DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Debit source
    UPDATE accounts SET balance = balance - p_amount
    WHERE account_id = p_from_account;
    
    -- Credit destination
    UPDATE accounts SET balance = balance + p_amount
    WHERE account_id = p_to_account;
    
    -- Commit the transaction
    COMMIT;
    
EXCEPTION
    WHEN others THEN
        ROLLBACK;
        RAISE;
END;
$$;
```

### Procedure with Error Handling

```sql
CREATE OR REPLACE PROCEDURE safe_delete_customer(
    p_customer_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_count INTEGER;
BEGIN
    -- Check for existing orders
    SELECT COUNT(*) INTO v_order_count
    FROM orders WHERE customer_id = p_customer_id;
    
    IF v_order_count > 0 THEN
        RAISE EXCEPTION 'Cannot delete customer with % existing orders', v_order_count;
    END IF;
    
    DELETE FROM customers WHERE customer_id = p_customer_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer % not found', p_customer_id;
    END IF;
    
    RAISE NOTICE 'Customer % deleted successfully', p_customer_id;
END;
$$;
```

### When to Use Stored Procedures

1. **Complex operations** - Multiple statements that must execute together
2. **Business rules** - Enforce logic that shouldn't vary by application
3. **Sensitive operations** - Limit direct table access
4. **Batch processing** - Data migrations, cleanups
5. **Transaction control** - Operations requiring explicit commit/rollback

### Managing Procedures

```sql
-- List procedures
SELECT proname, proargnames, prosrc
FROM pg_proc
WHERE pronamespace = 'public'::regnamespace
  AND prokind = 'p';

-- Drop procedure
DROP PROCEDURE add_customer;
DROP PROCEDURE IF EXISTS add_customer;

-- Drop with parameters (if overloaded)
DROP PROCEDURE add_customer(VARCHAR, VARCHAR);
```

### Complete Example

```sql
-- Order processing procedure
CREATE OR REPLACE PROCEDURE process_order(
    p_customer_id INTEGER,
    p_product_ids INTEGER[],
    p_quantities INTEGER[],
    OUT p_order_id INTEGER,
    OUT p_total DECIMAL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_product_id INTEGER;
    v_quantity INTEGER;
    v_price DECIMAL;
    i INTEGER;
BEGIN
    -- Create order
    INSERT INTO orders (customer_id, order_date, status)
    VALUES (p_customer_id, NOW(), 'pending')
    RETURNING order_id INTO p_order_id;
    
    p_total := 0;
    
    -- Add items
    FOR i IN 1..array_length(p_product_ids, 1) LOOP
        v_product_id := p_product_ids[i];
        v_quantity := p_quantities[i];
        
        -- Get price and check stock
        SELECT price INTO v_price
        FROM products
        WHERE product_id = v_product_id AND stock >= v_quantity;
        
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Product % unavailable or insufficient stock', v_product_id;
        END IF;
        
        -- Add order item
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (p_order_id, v_product_id, v_quantity, v_price);
        
        -- Reduce stock
        UPDATE products SET stock = stock - v_quantity
        WHERE product_id = v_product_id;
        
        p_total := p_total + (v_quantity * v_price);
    END LOOP;
    
    -- Update order total
    UPDATE orders SET total = p_total WHERE order_id = p_order_id;
    
    COMMIT;
EXCEPTION
    WHEN others THEN
        ROLLBACK;
        RAISE;
END;
$$;

-- Usage
CALL process_order(
    1,                      -- customer_id
    ARRAY[101, 102, 103],  -- product_ids
    ARRAY[2, 1, 3],        -- quantities
    NULL, NULL             -- OUT params
);
```

## Key Takeaways

- Stored procedures are reusable SQL statement blocks
- Use CALL to execute procedures
- Procedures can have IN, OUT, and INOUT parameters
- Procedures can control transactions (COMMIT/ROLLBACK)
- Use procedures for complex, multi-step operations
- Functions return values; procedures perform actions

## Additional Resources

- [PostgreSQL CREATE PROCEDURE](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- [PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
- [Control Structures](https://www.postgresql.org/docs/current/plpgsql-control-structures.html)
