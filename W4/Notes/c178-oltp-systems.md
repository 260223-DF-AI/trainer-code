# OLTP Systems

## Learning Objectives

- Define OLTP (Online Transaction Processing) and its purpose
- Understand key characteristics of OLTP systems
- Learn about normalization and ACID properties
- Recognize common OLTP use cases and technologies

## Why This Matters

OLTP systems power the day-to-day operations of businesses, handling transactions like orders, payments, and inventory updates. Understanding OLTP helps you recognize why these systems are designed differently from analytical systems and why data must be transformed when moving to a data warehouse.

## Concept Explanation

### What is OLTP?

OLTP (Online Transaction Processing) refers to systems designed to manage real-time transactional data. These systems handle the operational workload of an organization, processing individual transactions quickly and reliably.

**Key Purpose**: "Run the business" through fast, reliable transaction processing.

### Characteristics of OLTP Systems

```
OLTP System Traits:

+------------------+     +------------------+     +------------------+
| High Volume      |     | Fast Response    |     | Data Integrity   |
| Transactions     |     | Time             |     | (ACID)           |
+------------------+     +------------------+     +------------------+
| Thousands/sec    |     | Milliseconds     |     | Never lose data  |
| Small operations |     | Sub-second       |     | Always consistent|
+------------------+     +------------------+     +------------------+
```

#### 1. High Transaction Volume

OLTP systems handle many concurrent transactions:

- E-commerce: Thousands of orders per minute
- Banking: Millions of ATM/card transactions daily
- Airlines: Simultaneous booking requests

#### 2. Fast Response Time

Transactions must complete quickly:

- User expects immediate feedback
- Typical target: < 100ms response time
- Must handle peak load without degradation

#### 3. ACID Compliance

Transactions must be reliable:

| Property | Description | Example |
|----------|-------------|---------|
| **A**tomicity | All or nothing | Transfer either completes or fails entirely |
| **C**onsistency | Valid state to valid state | Account balance never goes negative |
| **I**solation | Transactions don't interfere | Two users can't buy the same last item |
| **D**urability | Committed data persists | Power failure doesn't lose completed orders |

### Data Model: Normalized (3NF)

OLTP systems use highly normalized schemas to:

- Minimize data redundancy
- Prevent update anomalies
- Optimize write performance

**Example: E-Commerce Normalized Schema**

```
customers               orders               order_items          products
+-----------+          +----------+          +------------+        +----------+
| customer_ |          | order_id |          | item_id    |        | product_ |
|   id (PK) |<------+  | (PK)     |<------+  | (PK)       |        |   id(PK) |
| email     |       |  | customer_|       |  | order_id   |------->| name     |
| name      |       |  |   id(FK) |       +--| product_id |        | category |
| address   |       +--| order_   |          | quantity   |        | price    |
+-----------+          |   date   |          | unit_price |        +----------+
                       | status   |          +------------+
                       +----------+
```

**Benefits of Normalization:**

- No duplicate customer data in orders
- Product price changes don't affect historical orders
- Easy to update customer email in one place

### Common OLTP Operations

OLTP queries are simple and targeted:

```sql
-- Insert new order
INSERT INTO orders (customer_id, order_date, status)
VALUES (12345, CURRENT_TIMESTAMP, 'PENDING');

-- Update inventory
UPDATE products 
SET stock_quantity = stock_quantity - 1
WHERE product_id = 'SKU-001';

-- Read single customer
SELECT * FROM customers 
WHERE customer_id = 12345;

-- Update order status
UPDATE orders 
SET status = 'SHIPPED', shipped_date = CURRENT_TIMESTAMP
WHERE order_id = 98765;
```

**Note**: Queries target specific records by primary key. Aggregations and analytics are rare.

### OLTP Technologies

| Category | Examples |
|----------|----------|
| Relational | PostgreSQL, MySQL, Oracle, SQL Server |
| Distributed SQL | CockroachDB, TiDB, YugabyteDB |
| Cloud Managed | Amazon RDS, Cloud SQL, Azure SQL |

### Typical Workload Pattern

```
OLTP Workload:

Reads:  70% simple lookups (SELECT by primary key)
Writes: 30% inserts and updates

Query Complexity:
+--------+
|  Low   |||||||||||||||||||||||||||||||||  90%
+--------+
| Medium |||||  8%
+--------+
|  High  ||  2%
+--------+
```

### Indexes in OLTP

OLTP systems rely heavily on indexes for fast lookups:

```sql
-- Primary key index (implicit)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date TIMESTAMP
);

-- Index for frequent queries
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
```

**Trade-off**: More indexes speed reads but slow writes.

## Code Example

OLTP transaction handling in Python:

```python
import psycopg2
from contextlib import contextmanager
from typing import Optional
from dataclasses import dataclass

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float

class OLTPOrderSystem:
    """Demonstrates OLTP transaction patterns."""
    
    def __init__(self, connection_string: str):
        self.conn_string = connection_string
    
    @contextmanager
    def transaction(self):
        """
        Context manager for ACID transactions.
        Ensures atomicity: all or nothing.
        """
        conn = psycopg2.connect(self.conn_string)
        conn.autocommit = False
        try:
            yield conn
            conn.commit()  # Durability
        except Exception as e:
            conn.rollback()  # Atomicity
            raise e
        finally:
            conn.close()
    
    def place_order(self, customer_id: int, items: list[OrderItem]) -> Optional[int]:
        """
        Place an order with ACID guarantees.
        
        This transaction must:
        - Create order record
        - Add order items
        - Decrease inventory
        - All or nothing (atomicity)
        """
        with self.transaction() as conn:
            cursor = conn.cursor()
            
            # 1. Create order
            cursor.execute("""
                INSERT INTO orders (customer_id, order_date, status)
                VALUES (%s, CURRENT_TIMESTAMP, 'PENDING')
                RETURNING order_id
            """, (customer_id,))
            order_id = cursor.fetchone()[0]
            
            # 2. Add items and update inventory
            for item in items:
                # Check stock (isolation - prevents overselling)
                cursor.execute("""
                    SELECT stock_quantity FROM products
                    WHERE product_id = %s
                    FOR UPDATE  -- Row lock for isolation
                """, (item.product_id,))
                
                stock = cursor.fetchone()[0]
                if stock < item.quantity:
                    raise ValueError(f"Insufficient stock for product {item.product_id}")
                
                # Add order item
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item.product_id, item.quantity, item.unit_price))
                
                # Decrease inventory
                cursor.execute("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity - %s
                    WHERE product_id = %s
                """, (item.quantity, item.product_id))
            
            return order_id
    
    def get_customer(self, customer_id: int) -> dict:
        """
        Simple point lookup - typical OLTP read.
        Fast due to primary key index.
        """
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_id, name, email, created_at
                FROM customers
                WHERE customer_id = %s
            """, (customer_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'customer_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'created_at': row[3]
                }
            return None
    
    def update_order_status(self, order_id: int, new_status: str) -> bool:
        """
        Simple update - typical OLTP write.
        """
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders 
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE order_id = %s
            """, (new_status, order_id))
            
            return cursor.rowcount > 0
```

## Key Takeaways

- OLTP systems manage real-time transactional data for daily operations
- Designed for high volume, fast response time, and ACID compliance
- Use normalized (3NF) schemas to minimize redundancy and ensure consistency
- Queries are simple, targeting specific records by primary key
- Indexes on frequently queried columns are critical for performance
- Common OLTP databases: PostgreSQL, MySQL, Oracle, SQL Server
- OLTP data must be transformed for analytical use in data warehouses

## Resources

- PostgreSQL Documentation: <https://www.postgresql.org/docs/>
- ACID Properties: <https://www.postgresql.org/docs/current/transaction-iso.html>
- Database Normalization: <https://www.guru99.com/database-normalization.html>
