# Lab: Data Analysis with pandas and Visualization

## Overview

In this exercise, you will analyze a real-world dataset using pandas and create visualizations with matplotlib to communicate your findings.

**Mode:** Implementation (Code Lab)
**Estimated Time:** 3-4 hours
**Prerequisites:** Content c062-c066 (Unit Testing, NumPy, matplotlib, pytest, pandas)

---

## Learning Objectives

By completing this exercise, you will be able to:

- Load and explore datasets with pandas
- Clean and transform data for analysis
- Perform aggregations and statistical analysis
- Create meaningful visualizations
- Write tests for data processing functions

---

## The Scenario

You work for an e-commerce analytics team. The marketing department has provided you with order data and wants insights to inform their next campaign. They need:

1. A summary of sales trends
2. Top-performing products and categories
3. Customer purchase patterns
4. Visualizations for the upcoming board presentation

---

## Dataset

Navigate to `starter_code/` where you will find `orders.csv`:

```csv
order_id,customer_id,order_date,product_name,category,quantity,unit_price,region
1001,C001,2024-01-05,Laptop Pro,Electronics,1,1299.99,North
1002,C002,2024-01-05,Wireless Mouse,Electronics,2,29.99,South
1003,C001,2024-01-06,USB Cable,Accessories,3,9.99,North
...
```

---

## Core Tasks

### Task 1: Data Loading and Exploration (30 min)

Create `analysis.py` and implement:

```python
def load_data(filepath):
    """
    Load the orders dataset.
    - Parse dates correctly
    - Handle missing values
    - Return a clean DataFrame
    """
    pass

def explore_data(df):
    """
    Print basic statistics about the dataset:
    - Shape (rows, columns)
    - Data types
    - Missing value counts
    - Basic statistics for numeric columns
    - Date range covered
    """
    pass
```

### Task 2: Data Cleaning and Transformation (45 min)

Add these functions:

```python
def clean_data(df):
    """
    Clean the dataset:
    - Remove duplicates
    - Fill or drop missing values (document your strategy)
    - Standardize text columns (strip whitespace, consistent case)
    - Add calculated columns: 'total_amount' = quantity * unit_price
    """
    pass

def add_time_features(df):
    """
    Add time-based features:
    - day_of_week (0=Monday, 6=Sunday)
    - month
    - quarter
    - is_weekend (boolean)
    """
    pass
```

### Task 3: Analysis Functions (60 min)

Implement these analysis functions:

```python
def sales_by_category(df):
    """
    Calculate total sales and order count by category.
    Returns: DataFrame with columns [category, total_sales, order_count, avg_order_value]
    Sorted by total_sales descending.
    """
    pass

def sales_by_region(df):
    """
    Calculate total sales by region.
    Returns: DataFrame with columns [region, total_sales, percentage_of_total]
    """
    pass

def top_products(df, n=10):
    """
    Find top N products by total sales.
    Returns: DataFrame with columns [product_name, category, total_sales, units_sold]
    """
    pass

def daily_sales_trend(df):
    """
    Calculate daily sales totals.
    Returns: DataFrame with columns [date, total_sales, order_count]
    """
    pass

def customer_analysis(df):
    """
    Analyze customer purchasing behavior.
    Returns: DataFrame with columns [customer_id, total_spent, order_count, 
             avg_order_value, favorite_category]
    """
    pass

def weekend_vs_weekday(df):
    """
    Compare weekend vs weekday sales.
    Returns: Dict with weekend and weekday total sales and percentages.
    """
    pass
```

### Task 4: Visualization (60 min)

Create `visualizations.py` with:

```python
import matplotlib.pyplot as plt

def create_category_bar_chart(category_data, output_path):
    """
    Create a horizontal bar chart of sales by category.
    - Include value labels on bars
    - Use a professional color scheme
    - Save to output_path
    """
    pass

def create_regional_pie_chart(region_data, output_path):
    """
    Create a pie chart showing sales distribution by region.
    - Include percentages
    - Use distinct colors for each region
    - Save to output_path
    """
    pass

def create_sales_trend_line(daily_data, output_path):
    """
    Create a line chart showing daily sales trend.
    - Include moving average (7-day)
    - Mark weekends differently
    - Add proper axis labels and title
    - Save to output_path
    """
    pass

def create_dashboard(df, output_dir):
    """
    Create a multi-panel dashboard with 4 subplots:
    1. Sales by category (bar)
    2. Sales by region (pie)
    3. Daily trend (line)
    4. Top 10 products (horizontal bar)
    
    Save as a single figure.
    """
    pass
```

### Task 5: Write Tests (45 min)

Create `test_analysis.py`:

```python
import pytest
import pandas as pd
from analysis import *

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North']
    })

def test_clean_data_removes_duplicates(sample_data):
    """Test that clean_data removes duplicate rows."""
    pass

def test_sales_by_category_calculation(sample_data):
    """Test that category totals are calculated correctly."""
    pass

def test_top_products_returns_correct_count(sample_data):
    """Test that top_products returns requested number of items."""
    pass

# Add at least 5 more tests
```

### Task 6: Main Script (30 min)

Create `main.py` that:

1. Loads the data
2. Cleans and transforms it
3. Runs all analyses
4. Generates all visualizations
5. Prints a summary report to console

---

## Definition of Done

- [ ] Data loads and cleans without errors
- [ ] All analysis functions return correct results
- [ ] At least 4 visualizations are created
- [ ] Dashboard displays all key metrics
- [ ] At least 8 tests pass
- [ ] Main script runs end-to-end

---

## Stretch Goals (Optional)

1. Add interactive visualizations with plotly
2. Calculate month-over-month growth rates
3. Identify customer segments using clustering
4. Export results to an Excel file with multiple sheets

---

## Submission

1. Run the complete analysis pipeline
2. Save all visualizations to `output/` directory
3. Run tests and ensure all pass
4. Be prepared to explain your findings
