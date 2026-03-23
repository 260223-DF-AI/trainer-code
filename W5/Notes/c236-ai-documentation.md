# AI-Assisted Documentation

## Learning Objectives

- Use AI tools to generate technical documentation efficiently
- Create data dictionaries, READMEs, and API docs with AI assistance
- Apply review workflows to ensure AI-generated documentation is accurate
- Build documentation habits that leverage AI as an accelerator

## Why This Matters

Documentation is one of the most neglected aspects of software development. Developers know it is important but consistently deprioritize it. AI dramatically lowers the effort barrier. What once took an hour of tedious writing can now be a 10-minute generate-and-review process. For data professionals, well-documented schemas, pipelines, and processes are essential for team collaboration and knowledge transfer.

## The Concept

### Types of Documentation AI Can Generate

| Document Type | AI Effectiveness | Human Effort Needed |
| ------------- | ---------------- | ------------------- |
| Code comments and docstrings | High | Light review |
| README files | High | Moderate editing |
| Data dictionaries | High | Verification against actual schema |
| API documentation | Medium-High | Verify accuracy of endpoints |
| Architecture docs | Medium | Significant review and context addition |
| Runbooks and SOPs | Medium | Verify procedures work as described |
| Decision records | Low | High -- requires human context |

### Generating READMEs

```
Prompt:
"Generate a README.md for a Python ETL pipeline project with 
the following structure:

etl_pipeline/
  config.py        - Configuration dataclass
  extract.py       - CSV and API extraction
  transform.py     - Pandas transformations
  load.py          - BigQuery loading
  validate.py      - Data quality checks
  pipeline.py      - Main orchestrator
  requirements.txt - Dependencies

Include sections: Overview, Prerequisites, Setup, Usage, 
Configuration, Project Structure, Testing, Contributing.
The project uses Python 3.10+, pandas, google-cloud-bigquery."
```

The AI generates a complete README. You then:

1. Verify the setup instructions work
2. Add project-specific details
3. Include team conventions
4. Update any incorrect assumptions

### Generating Data Dictionaries

```
Prompt:
"Create a data dictionary for this BigQuery table. For each 
column, provide: Name, Type, Description, Nullable, 
Example Value.

CREATE TABLE retail.dim_customer (
  customer_key INT64 NOT NULL,
  customer_id STRING NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  city STRING,
  state STRING,
  loyalty_tier STRING,
  signup_date DATE,
  effective_from DATE NOT NULL,
  effective_to DATE NOT NULL,
  is_current BOOL NOT NULL
);"
```

The AI generates a formatted data dictionary. You verify:

- Descriptions match actual business usage
- Example values are realistic
- Nullable flags match the schema
- Business terminology is correct

### Generating Code Comments

#### Docstrings from Code

```
Prompt:
"Generate a Google-style docstring for this function:

def merge_customer_records(
    current_df: pd.DataFrame,
    updates_df: pd.DataFrame,
    key_column: str = 'customer_id'
) -> pd.DataFrame:
    merged = current_df.merge(
        updates_df, on=key_column, how='outer',
        suffixes=('_current', '_update')
    )
    for col in updates_df.columns:
        if col != key_column:
            merged[col] = merged[f'{col}_update'].fillna(
                merged[f'{col}_current']
            )
    return merged.drop(
        columns=[c for c in merged.columns 
                 if c.endswith(('_current', '_update'))]
    )"
```

#### Inline Comments for Complex Code

```
Prompt:
"Add clear inline comments to this SQL query explaining 
each section:

WITH daily_stats AS (
  SELECT DATE(created_at) AS stat_date,
         COUNT(*) AS total_orders,
         SUM(amount) AS total_revenue,
         COUNT(DISTINCT customer_id) AS unique_customers
  FROM orders
  WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY 1
),
running_avg AS (
  SELECT stat_date, total_orders, total_revenue,
         AVG(total_revenue) OVER (
           ORDER BY stat_date 
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
         ) AS seven_day_avg
  FROM daily_stats
)
SELECT * FROM running_avg
WHERE total_revenue > seven_day_avg * 1.5
ORDER BY stat_date"
```

### Building a Documentation Workflow

```
Step 1: Write the code
Step 2: Generate documentation with AI
Step 3: Review for accuracy
Step 4: Add context AI cannot know:
        - Why decisions were made
        - Known limitations
        - Team-specific conventions
        - Links to related documents
Step 5: Commit documentation alongside code
```

### Documentation Templates

Create reusable prompt templates for your team:

#### Pipeline Documentation Template

```
"Document this ETL pipeline using this template:

# [Pipeline Name]

## Purpose
[What this pipeline does and why]

## Schedule
[When it runs]

## Data Flow
[Source] --> [Transformations] --> [Destination]

## Dependencies
[What must run before this pipeline]

## Error Handling
[What happens on failure]

## Contact
[Who to reach out to for issues]

Pipeline code: [paste code]"
```

### Best Practices

1. **Generate, do not write from scratch** -- let AI handle the first draft
2. **Always review** -- AI documentation can describe what code does but may miss why
3. **Add human context** -- decisions, trade-offs, and history require human input
4. **Keep documentation near the code** -- docstrings and inline comments over external wikis
5. **Update documentation when code changes** -- regenerate affected sections

## Key Takeaways

- AI dramatically reduces the effort needed to create documentation
- READMEs, data dictionaries, and code comments are high-value AI documentation targets
- Always review AI-generated docs for accuracy and add human context
- Create reusable prompt templates for consistency across team documentation
- Document alongside code changes, not as a separate effort

## Additional Resources

- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Write the Docs - Documentation Guide](https://www.writethedocs.org/guide/)
- [GitHub - Documenting Your Project](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
