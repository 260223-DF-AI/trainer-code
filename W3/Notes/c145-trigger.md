# Triggers

## Learning Objectives

- Understand what triggers are and when they fire
- Create triggers for common use cases
- Implement trigger functions in PL/pgSQL
- Apply triggers for auditing, validation, and automation

## Why This Matters

Triggers automatically execute code in response to database events. They're invaluable for maintaining audit trails, enforcing complex business rules, automating data updates, and keeping derived data in sync. Understanding triggers helps you build self-maintaining databases that enforce rules regardless of how data is modified.

## The Concept

### What is a Trigger?

A trigger is a database object that automatically executes a function when a specific event occurs on a table.

```
Event (INSERT, UPDATE, DELETE)
         |
         v
    +--------+
    |Trigger |---> Trigger Function
    +--------+
         |
         v
    Table Modified
```

### Trigger Timing

| Timing | Description |
|--------|-------------|
| BEFORE | Execute before the operation |
| AFTER | Execute after the operation |
| INSTEAD OF | Replace the operation (views only) |

### Trigger Events

| Event | Fires On |
|-------|----------|
| INSERT | New row added |
| UPDATE | Row modified |
| DELETE | Row removed |
| TRUNCATE | Table truncated |

### Creating a Trigger

Two steps: Create the function, then create the trigger.

```sql
-- Step 1: Create trigger function
CREATE OR REPLACE FUNCTION update_modified_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 2: Create trigger
CREATE TRIGGER set_modified_timestamp
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_timestamp();
```

### Special Variables in Triggers

| Variable | Description |
|----------|-------------|
| NEW | New row (INSERT/UPDATE) |
| OLD | Old row (UPDATE/DELETE) |
| TG_OP | Operation: INSERT, UPDATE, DELETE |
| TG_TABLE_NAME | Name of the table |

### Audit Trail Trigger

```sql
-- Audit table
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by VARCHAR(100)
);

-- Audit function
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_data)
        VALUES (TG_TABLE_NAME, TG_OP, to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply to table
CREATE TRIGGER products_audit
    AFTER INSERT OR UPDATE OR DELETE ON products
    FOR EACH ROW
    EXECUTE FUNCTION audit_changes();
```

### Validation Trigger

```sql
-- Prevent salary decrease
CREATE OR REPLACE FUNCTION prevent_salary_decrease()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary < OLD.salary THEN
        RAISE EXCEPTION 'Salary cannot be decreased from % to %', 
            OLD.salary, NEW.salary;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_salary
    BEFORE UPDATE ON employees
    FOR EACH ROW
    EXECUTE FUNCTION prevent_salary_decrease();
```

### Auto-Update Trigger

```sql
-- Keep derived column updated
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2)
);

CREATE OR REPLACE FUNCTION calculate_total()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total_price = NEW.quantity * NEW.unit_price;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calc_item_total
    BEFORE INSERT OR UPDATE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION calculate_total();
```

### Conditional Trigger

```sql
-- Only fire when certain columns change
CREATE TRIGGER price_change_audit
    AFTER UPDATE OF price, discount ON products
    FOR EACH ROW
    WHEN (OLD.price IS DISTINCT FROM NEW.price 
       OR OLD.discount IS DISTINCT FROM NEW.discount)
    EXECUTE FUNCTION audit_changes();
```

### Managing Triggers

```sql
-- List triggers on a table
SELECT trigger_name, event_manipulation, action_timing
FROM information_schema.triggers
WHERE event_object_table = 'products';

-- Disable trigger temporarily
ALTER TABLE products DISABLE TRIGGER products_audit;

-- Enable trigger
ALTER TABLE products ENABLE TRIGGER products_audit;

-- Drop trigger
DROP TRIGGER products_audit ON products;
```

### Complete Example

```sql
-- Create tables
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE stock_history (
    history_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    old_stock INTEGER,
    new_stock INTEGER,
    change_amount INTEGER,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Auto-update modified_at
CREATE OR REPLACE FUNCTION update_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_modified
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_modified();

-- Track stock changes
CREATE OR REPLACE FUNCTION log_stock_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.stock IS DISTINCT FROM NEW.stock THEN
        INSERT INTO stock_history (product_id, old_stock, new_stock, change_amount)
        VALUES (NEW.product_id, OLD.stock, NEW.stock, NEW.stock - OLD.stock);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER track_stock
    AFTER UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION log_stock_change();

-- Test
INSERT INTO products (name, price, stock) VALUES ('Laptop', 999, 50);
UPDATE products SET stock = 45 WHERE product_id = 1;
UPDATE products SET stock = 60 WHERE product_id = 1;

SELECT * FROM stock_history;
```

## Key Takeaways

- Triggers execute automatically on database events
- BEFORE triggers can modify data before it's saved
- AFTER triggers are good for auditing and notifications
- Use NEW for new data, OLD for previous data
- Triggers enforce rules regardless of how data is changed
- Test triggers thoroughly - they run on every operation

## Additional Resources

- [PostgreSQL CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- [Trigger Functions](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [Trigger Procedures](https://www.postgresql.org/docs/current/trigger-definition.html)
