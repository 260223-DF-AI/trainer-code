# Structured Data

## Learning Objectives

- Define structured data and its characteristics
- Understand the role of schemas in structured data
- Identify common structured data sources and formats
- Recognize strengths and limitations of structured data

## Why This Matters

Structured data has been the foundation of data management for decades. Relational databases, spreadsheets, and traditional data warehouses all work primarily with structured data. Understanding its characteristics helps you design appropriate storage solutions and recognize when other data formats might be more suitable.

## Concept Explanation

### What is Structured Data?

Structured data is data that adheres to a predefined schema with a consistent format. Every record has the same fields, data types are enforced, and values can be easily mapped to columns and rows.

**Key Characteristics:**

- Fixed schema defined before data entry
- Consistent data types per field
- Organized in rows and columns
- Easily searchable and queryable
- Machine-readable format

### The Schema

A schema defines the structure of data:

```sql
-- Example schema definition
CREATE TABLE customers (
    customer_id    INT PRIMARY KEY,
    first_name     VARCHAR(50) NOT NULL,
    last_name      VARCHAR(50) NOT NULL,
    email          VARCHAR(100) UNIQUE,
    date_of_birth  DATE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Schema Elements:**

- Field names (columns)
- Data types (INT, VARCHAR, DATE)
- Constraints (NOT NULL, UNIQUE, PRIMARY KEY)
- Relationships (foreign keys)

### Common Sources of Structured Data

| Source | Examples |
|--------|----------|
| Relational Databases | PostgreSQL, MySQL, Oracle |
| Spreadsheets | Excel files, Google Sheets |
| CSV Files | Comma-separated values |
| Enterprise Systems | ERP, CRM, HR systems |
| Financial Systems | Transactions, ledgers |

### Representation

Structured data fits naturally in tables:

```
+-------------+------------+-----------+---------------------+
| customer_id | first_name | last_name | email               |
+-------------+------------+-----------+---------------------+
| 1           | John       | Smith     | john.s@example.com  |
| 2           | Sarah      | Johnson   | sarah.j@example.com |
| 3           | Michael    | Williams  | mike.w@example.com  |
+-------------+------------+-----------+---------------------+
```

### Advantages

1. **Easy to Query**: SQL works perfectly with structured data
2. **Strong Consistency**: Data types and constraints ensure quality
3. **Well-Understood**: Decades of tooling and expertise
4. **Efficient Storage**: Known structure enables compression
5. **Indexable**: Fast lookups with B-trees and hash indexes

### Limitations

1. **Inflexible**: Schema changes require migrations
2. **Limited to Tabular**: Cannot easily represent hierarchies
3. **Normalized Complexity**: Many tables with relationships
4. **Scaling Challenges**: Vertical scaling limits

### When to Use Structured Data

**Good Fit:**

- Transactional systems (OLTP)
- Financial data
- Customer records
- Inventory management
- Any data with stable, well-defined schema

**Poor Fit:**

- Rapidly changing requirements
- Hierarchical or nested data
- Unstructured content (documents, media)
- High-variety data sources

## Code Example

Working with structured data in Python:

```python
import pandas as pd
import sqlite3
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class CustomerRecord:
    """Strongly typed structured data representation."""
    customer_id: int
    first_name: str
    last_name: str
    email: str
    date_of_birth: str  # ISO format: YYYY-MM-DD

class StructuredDataHandler:
    """Demonstrate structured data operations."""
    
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._create_schema()
    
    def _create_schema(self):
        """Create structured table with schema."""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                date_of_birth DATE
            )
        ''')
        self.conn.commit()
    
    def insert_customer(self, customer: CustomerRecord) -> bool:
        """Insert structured record with validation."""
        try:
            self.conn.execute('''
                INSERT INTO customers 
                (customer_id, first_name, last_name, email, date_of_birth)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                customer.customer_id,
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.date_of_birth
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Constraint violation: {e}")
            return False
    
    def query_customers(self, where_clause: str = None) -> pd.DataFrame:
        """Query structured data with SQL."""
        query = "SELECT * FROM customers"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        return pd.read_sql(query, self.conn)
    
    def load_from_csv(self, csv_path: str):
        """Load structured CSV data."""
        df = pd.read_csv(csv_path)
        
        # CSV is structured - validate against schema
        required_columns = ['customer_id', 'first_name', 'last_name', 'email']
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        df.to_sql('customers', self.conn, if_exists='append', index=False)
    
    def schema_info(self) -> List[Dict]:
        """Get schema information."""
        cursor = self.conn.execute("PRAGMA table_info(customers)")
        columns = []
        for row in cursor:
            columns.append({
                'position': row[0],
                'name': row[1],
                'type': row[2],
                'nullable': not row[3],  # notnull flag
                'primary_key': bool(row[5])
            })
        return columns


# Demo usage
handler = StructuredDataHandler()

# Insert valid record
customer1 = CustomerRecord(
    customer_id=1,
    first_name="John",
    last_name="Smith",
    email="john@example.com",
    date_of_birth="1990-05-15"
)
handler.insert_customer(customer1)

# Try to insert duplicate email (will fail due to schema constraint)
customer2 = CustomerRecord(
    customer_id=2,
    first_name="Jane",
    last_name="Doe",
    email="john@example.com",  # Duplicate - constraint violation
    date_of_birth="1985-08-22"
)
handler.insert_customer(customer2)  # Returns False

# Query with SQL
results = handler.query_customers("first_name = 'John'")
print(results)

# View schema
print("\nSchema:")
for col in handler.schema_info():
    print(f"  {col['name']}: {col['type']} (PK: {col['primary_key']})")
```

## Key Takeaways

- Structured data follows a predefined schema with consistent format and types
- Schemas define field names, data types, and constraints
- SQL and relational databases are optimized for structured data
- Advantages include easy querying, strong consistency, and efficient storage
- Limitations include inflexibility and difficulty representing hierarchies
- Structured data accounts for approximately 10-20% of all enterprise data

## Resources

- Relational Database Design: <https://www.postgresql.org/docs/current/ddl.html>
- Data Modeling Best Practices: <https://www.dataversity.net/data-modeling-101/>
- Schema Design: <https://www.sqlstyle.guide/>
