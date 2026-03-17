# Semi-Structured Data

## Learning Objectives

- Define semi-structured data and its characteristics
- Understand common formats: JSON, XML, YAML
- Learn how to work with hierarchical data
- Recognize when to use semi-structured vs. structured formats

## Why This Matters

Semi-structured data has become the dominant format for data exchange, APIs, and configuration. JSON powers web APIs; XML remains prevalent in enterprise systems; logs often follow semi-structured patterns. Understanding these formats is essential for data integration and modern application development.

## Concept Explanation

### What is Semi-Structured Data?

Semi-structured data contains organizational properties (tags, markers, hierarchy) but does not conform to a rigid schema like relational tables. Records can have different fields, and nesting is allowed.

**Key Characteristics:**

- Self-describing with tags or keys
- Flexible schema (schema-on-read)
- Supports nested and hierarchical structures
- Human-readable (usually text-based)
- Variable structure between records

### Comparison to Structured Data

| Aspect | Structured | Semi-Structured |
|--------|------------|-----------------|
| Schema | Fixed, predefined | Flexible, evolving |
| Format | Tables/rows | Hierarchical/nested |
| Fields | Same for all records | Can vary |
| Changes | Migration required | Add fields anytime |
| Query | SQL | JSONPath, XPath, custom |

### Common Formats

#### JSON (JavaScript Object Notation)

The most popular semi-structured format today.

```json
{
  "customer_id": 12345,
  "name": {
    "first": "John",
    "last": "Smith"
  },
  "emails": [
    "john@example.com",
    "john.smith@work.com"
  ],
  "orders": [
    {
      "order_id": "ORD-001",
      "amount": 99.99,
      "items": ["Widget A", "Widget B"]
    }
  ],
  "preferences": {
    "newsletter": true,
    "notifications": {
      "email": true,
      "sms": false
    }
  }
}
```

**Advantages:**

- Native to JavaScript and web
- Lightweight syntax
- Widely supported
- Human-readable

#### XML (Extensible Markup Language)

Older but still prevalent in enterprise systems.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customer id="12345">
  <name>
    <first>John</first>
    <last>Smith</last>
  </name>
  <emails>
    <email type="personal">john@example.com</email>
    <email type="work">john.smith@work.com</email>
  </emails>
  <orders>
    <order id="ORD-001">
      <amount currency="USD">99.99</amount>
      <items>
        <item>Widget A</item>
        <item>Widget B</item>
      </items>
    </order>
  </orders>
</customer>
```

**Advantages:**

- Supports attributes and elements
- Strong validation via XSD
- Well-established in enterprise
- Self-validating structure

#### YAML (YAML Ain't Markup Language)

Popular for configuration files.

```yaml
customer_id: 12345
name:
  first: John
  last: Smith
emails:
  - john@example.com
  - john.smith@work.com
orders:
  - order_id: ORD-001
    amount: 99.99
    items:
      - Widget A
      - Widget B
preferences:
  newsletter: true
  notifications:
    email: true
    sms: false
```

**Advantages:**

- Most human-readable
- Supports comments
- Great for configuration
- Superset of JSON

### Other Semi-Structured Formats

| Format | Use Case |
|--------|----------|
| Parquet | Columnar, analytics |
| Avro | Serialization, schema evolution |
| Protocol Buffers | Efficient binary format |
| Log files | Application/server logs |
| HTML | Web content |

### Working with Semi-Structured Data

**Schema-on-Read:**
Unlike structured data where schema is enforced on write, semi-structured data applies schema when reading:

```
Write: Store raw JSON/XML as-is
Read:  Parse and validate against expected structure
```

**Advantages:**

- Faster ingestion (no validation on write)
- Schema can evolve without migration
- Different applications can interpret differently

**Challenges:**

- No guarantees about structure
- Must handle missing/extra fields
- Validation moved to consuming applications

## Code Example

Working with semi-structured data in Python:

```python
import json
import xml.etree.ElementTree as ET
import yaml
from typing import Any, Dict, Optional
from dataclasses import dataclass

class SemiStructuredHandler:
    """Work with JSON, XML, and YAML data."""
    
    # JSON Operations
    @staticmethod
    def parse_json(json_string: str) -> Dict:
        """Parse JSON string to dictionary."""
        return json.loads(json_string)
    
    @staticmethod
    def to_json(data: Dict, pretty: bool = True) -> str:
        """Convert dictionary to JSON string."""
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)
    
    # XML Operations
    @staticmethod
    def parse_xml(xml_string: str) -> Dict:
        """Parse XML to dictionary (simplified)."""
        root = ET.fromstring(xml_string)
        
        def element_to_dict(element):
            result = {}
            if element.attrib:
                result['@attributes'] = element.attrib
            if element.text and element.text.strip():
                result['@text'] = element.text.strip()
            for child in element:
                child_data = element_to_dict(child)
                if child.tag in result:
                    # Convert to list if duplicate keys
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
            return result if len(result) > 1 or '@text' not in result else result.get('@text', result)
        
        return {root.tag: element_to_dict(root)}
    
    # YAML Operations
    @staticmethod
    def parse_yaml(yaml_string: str) -> Dict:
        """Parse YAML string to dictionary."""
        return yaml.safe_load(yaml_string)
    
    @staticmethod
    def to_yaml(data: Dict) -> str:
        """Convert dictionary to YAML string."""
        return yaml.dump(data, default_flow_style=False)
    
    # Flexible field access
    @staticmethod
    def get_nested(data: Dict, path: str, default: Any = None) -> Any:
        """
        Safely access nested fields.
        Path like 'customer.name.first' or 'orders[0].amount'
        """
        keys = path.replace('[', '.').replace(']', '').split('.')
        current = data
        
        for key in keys:
            if current is None:
                return default
            try:
                if isinstance(current, list):
                    current = current[int(key)]
                elif isinstance(current, dict):
                    current = current.get(key)
                else:
                    return default
            except (IndexError, ValueError, KeyError):
                return default
        
        return current if current is not None else default


# Demonstrate flexible schema
def demonstrate_flexible_schema():
    """Show how semi-structured data handles varying schemas."""
    
    # Record 1: Basic customer
    customer1 = {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com"
    }
    
    # Record 2: More detailed customer (different fields)
    customer2 = {
        "id": 2,
        "name": {
            "first": "Sarah",
            "last": "Johnson",
            "prefix": "Dr."
        },
        "email": "sarah@example.com",
        "phone_numbers": [
            {"type": "mobile", "number": "555-0100"},
            {"type": "work", "number": "555-0101"}
        ],
        "metadata": {
            "source": "website",
            "campaign_id": "SUMMER2024"
        }
    }
    
    # Both are valid - no schema conflict
    customers = [customer1, customer2]
    
    # Handling varying structures
    handler = SemiStructuredHandler()
    
    for customer in customers:
        # Safely access fields that may not exist
        first_name = handler.get_nested(customer, 'name.first')
        if first_name is None:
            # Fall back to simple name
            first_name = customer.get('name', '').split()[0] if isinstance(customer.get('name'), str) else None
        
        phone = handler.get_nested(customer, 'phone_numbers[0].number', 'N/A')
        
        print(f"ID: {customer['id']}, First Name: {first_name}, Phone: {phone}")


# Demonstrate format conversion
def convert_formats():
    """Convert between JSON, YAML, and XML."""
    
    handler = SemiStructuredHandler()
    
    # Original JSON
    json_data = '''
    {
        "product": {
            "id": "PROD-001",
            "name": "Widget",
            "price": 29.99,
            "tags": ["electronics", "sale"]
        }
    }
    '''
    
    # Parse JSON
    data = handler.parse_json(json_data)
    print("Parsed from JSON:")
    print(data)
    
    # Convert to YAML
    yaml_output = handler.to_yaml(data)
    print("\nConverted to YAML:")
    print(yaml_output)


if __name__ == "__main__":
    demonstrate_flexible_schema()
    print("\n" + "="*50 + "\n")
    convert_formats()
```

## Key Takeaways

- Semi-structured data has flexible schema with self-describing structure
- JSON is the dominant format for web APIs and data exchange
- XML remains important in enterprise systems and legacy integrations
- YAML is preferred for human-readable configuration files
- Schema-on-read allows faster ingestion but requires validation at consumption
- Nested and hierarchical structures are first-class citizens
- Semi-structured data bridges the gap between rigid tables and raw text

## Resources

- JSON Specification: <https://www.json.org/>
- XML Tutorial: <https://www.w3schools.com/xml/>
- YAML Specification: <https://yaml.org/spec/>
- JSONPath: <https://goessner.net/articles/JsonPath/>
