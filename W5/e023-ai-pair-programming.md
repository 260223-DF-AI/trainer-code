# Exercise: AI Pair Programming Session (Collaborative Project)

## Exercise ID: e023

## Overview

In this collaborative exercise, you will work in pairs to build a small data application using AI pair programming techniques. One person acts as the "Director" (defining requirements and reviewing output), while the other acts as the "Operator" (interacting with the AI tool and writing code). Halfway through, switch roles.

## Learning Objectives

- Practice AI pair programming in a collaborative setting
- Use Copilot or an alternative AI tool to accelerate development
- Apply the generate-review-refine workflow in a team context
- Build a working data utility using AI assistance

## Prerequisites

- GitHub Copilot or Codeium installed in VS Code
- Python 3.10+ with pandas installed
- Completed Wednesday written content on AI tools and Copilot

## Time Estimate

60-90 minutes (collaborative)

---

## The Project: Data Quality Dashboard Generator

You will build a Python script that:

1. Reads a CSV file
2. Performs automated data quality checks
3. Generates a formatted Markdown report
4. Outputs the report to a file

### Project Structure

```
data-quality-checker/
  main.py              # Entry point
  quality_checks.py    # Data quality check functions
  report_generator.py  # Markdown report generation
  sample_data.csv      # Test data (you create this)
  output/
    report.md          # Generated report
```

---

## Phase 1: Setup and Sample Data (10 minutes)

**Role: Both partners collaborate**

### Step 1: Create Project Directory

Create the project structure shown above.

### Step 2: Generate Sample Data

Use AI to generate sample data with deliberate quality issues:

```
Prompt suggestion:
"Generate a Python script that creates a CSV file with 
50 rows of sample customer order data. Include columns: 
order_id, customer_name, email, order_date, amount, status.

Include these deliberate data quality issues:
- 3 rows with null customer_name
- 2 duplicate order_ids
- 2 rows with negative amounts
- 1 row with an invalid email (no @ symbol)
- 1 row with a future date
- 1 row with status value not in (pending, completed, cancelled)"
```

---

## Phase 2: Quality Check Functions (20 minutes)

**Role: Partner A = Director, Partner B = Operator**

### Requirements (Director defines these)

Create `quality_checks.py` with functions that check for:

1. **Null values**: Count nulls per column
2. **Duplicates**: Find duplicate rows based on a key column
3. **Negative values**: Flag negative values in numeric columns
4. **Date validation**: Check for future dates
5. **Email validation**: Validate email format

### Instructions for the Operator

1. Open `quality_checks.py` in VS Code
2. Write descriptive comments for each function BEFORE letting Copilot suggest code
3. Let Copilot generate the function body
4. Director reviews each suggestion before accepting
5. Test each function against the sample data

### Expected Function Signatures

```python
def check_nulls(df: pd.DataFrame) -> dict:
    """Check for null values in each column."""
    pass

def check_duplicates(df: pd.DataFrame, key_column: str) -> dict:
    """Find duplicate rows based on a key column."""
    pass

def check_negative_values(df: pd.DataFrame, numeric_columns: list) -> dict:
    """Flag negative values in specified numeric columns."""
    pass

def check_future_dates(df: pd.DataFrame, date_column: str) -> dict:
    """Check for dates in the future."""
    pass

def check_email_format(df: pd.DataFrame, email_column: str) -> dict:
    """Validate email format in the specified column."""
    pass
```

### Director's Review Checklist

For each AI-generated function:

- [ ] Does the function signature match requirements?
- [ ] Is edge case handling present (empty DataFrame, missing columns)?
- [ ] Are return values consistent and useful?
- [ ] Would you trust this function for production data?

---

## Phase 3: Report Generator (20 minutes)

**Role: SWITCH -- Partner B = Director, Partner A = Operator**

### Requirements (Director defines these)

Create `report_generator.py` that:

1. Takes the results from all quality checks
2. Generates a Markdown report with:
   - Header with timestamp
   - Summary statistics (total rows, total issues found)
   - Detailed results for each check
   - A severity rating (PASS / WARNING / FAIL)
   - Recommendations for each issue found

### Instructions for the Operator

1. Use Copilot Chat to discuss the report structure
2. Write comments describing each section
3. Let Copilot generate the implementation
4. Director reviews for readability and completeness

### Expected Output Format

The generated report should look something like:

```markdown
# Data Quality Report

**Generated**: 2024-01-15 14:30:00
**File**: sample_data.csv
**Total Rows**: 50

## Summary

| Check | Status | Issues Found |
| ----- | ------ | ------------ |
| Null Values | WARNING | 3 |
| Duplicates | FAIL | 2 |
| Negative Values | WARNING | 2 |
| Future Dates | WARNING | 1 |
| Email Format | WARNING | 1 |

## Detailed Results

### Null Values - WARNING
...
```

---

## Phase 4: Main Script and Integration (15 minutes)

**Role: Both partners collaborate**

### Create `main.py`

Use AI to generate the main script that:

1. Reads the CSV file
2. Runs all quality checks
3. Generates the report
4. Saves it to `output/report.md`
5. Prints a summary to the console

### Integration Testing

1. Run the complete pipeline
2. Verify the output report is correct
3. Compare AI-generated quality findings against your known data issues
4. Fix any bugs found during integration

---

## Phase 5: Reflection (10 minutes)

### Discussion Questions (Both Partners)

1. How did AI pair programming differ from traditional pair programming?
2. Which functions did Copilot generate most accurately?
3. What required the most human intervention?
4. How did the Director-Operator dynamic work with AI?
5. What would you do differently next time?

### Document Your Experience

| Metric | Value |
| ------ | ----- |
| Total functions generated by AI | |
| Functions accepted as-is | |
| Functions requiring modification | |
| Functions rewritten from scratch | |
| Estimated time saved vs manual coding | |
| Overall AI contribution quality (1-10) | |

---

## Bonus Challenges (If Time Permits)

1. **Add a new check**: Implement an outlier detection check using statistical methods (z-score or IQR)
2. **Improve the report**: Add ASCII bar charts to the report for visual impact
3. **Error handling**: Add comprehensive error handling and logging to the pipeline
4. **Configuration**: Make the checks configurable via a YAML file

## Submission

Submit the complete project directory including:

- All Python source files
- The sample data CSV
- The generated report
- A brief reflection document (answers to Phase 5 questions)
