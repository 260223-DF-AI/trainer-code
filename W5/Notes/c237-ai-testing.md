# AI-Assisted Testing

## Learning Objectives

- Use AI tools to generate unit tests, integration tests, and test data
- Apply test-driven development patterns with AI assistance
- Recognize the strengths and limitations of AI-generated tests
- Build a testing workflow that combines AI generation with human judgment

## Why This Matters

Testing is one of the areas where AI assistance provides the most immediate value. Writing tests is repetitive, time-consuming, and often skipped under deadline pressure. AI can generate comprehensive test suites in minutes, covering standard cases, edge cases, and even error scenarios. For data engineers, AI-assisted testing means faster validation of pipelines, queries, and transformations.

## The Concept

### Why AI Excels at Test Generation

Tests follow predictable patterns, making them ideal for AI generation:

- Given-When-Then structure is consistent
- Edge cases follow common categories (null, empty, boundary, type errors)
- Test assertions map directly to function behavior
- Boilerplate setup code is highly repetitive

### Generating Tests from Code

#### Pattern: Function to Tests

```
Prompt:
"Generate pytest test cases for this function. Include tests 
for normal operation, edge cases, and error conditions:

def calculate_discount(subtotal: float, tier: str) -> float:
    rates = {
        'bronze': 0.05,
        'silver': 0.10,
        'gold': 0.15,
        'platinum': 0.20
    }
    if subtotal < 0:
        raise ValueError('Subtotal cannot be negative')
    if tier not in rates:
        raise ValueError(f'Unknown tier: {tier}')
    return round(subtotal * rates[tier], 2)"
```

AI generates tests covering:

- Each tier with a standard subtotal
- Zero subtotal
- Negative subtotal (expects ValueError)
- Invalid tier (expects ValueError)
- Rounding precision edge cases

#### Pattern: Schema to Data Validation Tests

```
Prompt:
"Generate Python tests for validating data loaded into 
this BigQuery table:

Table: analytics.daily_sales
Columns:
  sale_date DATE NOT NULL
  store_id STRING NOT NULL
  product_id STRING NOT NULL
  quantity INT64 NOT NULL (must be > 0)
  unit_price NUMERIC NOT NULL (must be >= 0)
  total_amount NUMERIC (computed: quantity * unit_price)

Generate tests that verify:
1. No null values in NOT NULL columns
2. quantity is always positive
3. unit_price is non-negative
4. total_amount equals quantity * unit_price
5. sale_date is not in the future
6. No duplicate (sale_date, store_id, product_id) rows"
```

### AI-Assisted Test-Driven Development

Reverse the typical flow -- write what you want tested, let AI implement:

```
Step 1: You define the requirements

"I need a function called clean_phone_numbers that:
- Takes a list of phone strings
- Removes all non-digit characters
- Removes country code (leading 1 for US)
- Returns only valid 10-digit US numbers
- Returns a list of cleaned phone strings"

Step 2: AI generates tests

Step 3: You review and approve the tests

Step 4: AI generates the implementation

Step 5: You verify the code passes all tests
```

### Generating Test Data

AI can create realistic test data:

```
Prompt:
"Generate a Python function that creates a test DataFrame 
mimicking a sales transactions table with:
- 100 rows
- Columns: transaction_id, customer_id (from pool of 20), 
  product_id (from pool of 10), transaction_date (last 30 
  days), amount (10.00-500.00)
- Include deliberate quality issues:
  - 5 rows with null customer_id
  - 3 duplicate transaction_ids
  - 2 rows with negative amounts
  - 1 row with a future date

Use numpy and pandas with a fixed random seed for 
reproducibility."
```

### Testing SQL Queries

AI can help test SQL logic:

```
Prompt:
"I have this BigQuery query:

WITH ranked AS (
  SELECT customer_id, order_date, total,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id 
      ORDER BY order_date DESC
    ) as rn
  FROM orders
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1

Generate test cases using a sample orders DataFrame to 
verify this query logic in pandas, checking:
1. Each customer appears exactly once
2. The row shown is the most recent order per customer
3. Handles customers with only one order
4. Handles ties in order_date correctly"
```

### Limitations of AI-Generated Tests

| Limitation | Description | Mitigation |
| ---------- | ----------- | ---------- |
| Missing business context | AI does not know your domain rules | Add domain-specific test cases manually |
| Surface-level coverage | Tests may check obvious cases only | Review for coverage gaps |
| Incorrect assertions | Tests may assert wrong expected values | Run and verify each test |
| Missing integration scenarios | AI tests individual functions, not workflows | Add integration tests manually |
| Unrealistic test data | Generated data may not match production patterns | Use production-like test datasets |

### Building Your Testing Workflow

```
1. Write the function specification (what it should do)
2. Generate tests with AI
3. Review tests for:
   - Correct expected values
   - Missing edge cases
   - Business logic coverage
4. Add domain-specific tests manually
5. Generate implementation (or write manually)
6. Run tests and iterate
7. Add tests to CI/CD pipeline
```

## Key Takeaways

- AI excels at generating standard test cases, edge cases, and test data
- AI-generated tests require human review for correct assertions and business logic coverage
- Test-driven development with AI means writing specs first, generating tests, then implementing
- SQL logic can be tested using AI-generated pandas equivalents
- Combine AI-generated tests with manually written domain-specific tests

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Google Testing Blog](https://testing.googleblog.com/)
- [Martin Fowler - Testing Strategies](https://martinfowler.com/articles/practical-test-pyramid.html)
