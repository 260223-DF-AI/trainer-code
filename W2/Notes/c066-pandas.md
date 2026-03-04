# pandas

## Learning Objectives

- Understand DataFrames and Series
- Load and explore data
- Filter, select, and transform data
- Perform basic data analysis

## Why This Matters

pandas is the standard tool for data manipulation in Python. It's used daily by data scientists and analysts for cleaning, transforming, and analyzing data. Whether working with spreadsheets, databases, or API responses, pandas makes data work intuitive and efficient.

## Concept

### What Is pandas?

pandas provides two main data structures:

- **Series**: 1D labeled array (like a column)
- **DataFrame**: 2D labeled table (like a spreadsheet)

### Installing pandas

```bash
pip install pandas
```

### Creating DataFrames

```python
import pandas as pd

# From dictionary
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
}
df = pd.DataFrame(data)
print(df)
#       name  age     city
# 0    Alice   25      NYC
# 1      Bob   30       LA
# 2  Charlie   35  Chicago
```

### Reading Data

```python
# CSV file
df = pd.read_csv("data.csv")

# Excel file
df = pd.read_excel("data.xlsx")

# JSON
df = pd.read_json("data.json")

# SQL (requires sqlalchemy)
df = pd.read_sql("SELECT * FROM users", connection)
```

### Exploring Data

```python
# First few rows
df.head()        # First 5 rows
df.head(10)      # First 10 rows

# Last few rows
df.tail()

# Basic info
df.info()        # Column types, non-null counts
df.describe()    # Statistical summary (count, mean, std, etc.)

# Shape and columns
print(df.shape)      # (rows, columns)
print(df.columns)    # Column names
print(df.dtypes)     # Data types
```

### Selecting Data

```python
# Single column (returns Series)
df["name"]
df.name            # Same thing (if column name is valid identifier)

# Multiple columns (returns DataFrame)
df[["name", "age"]]

# Rows by index
df.iloc[0]         # First row
df.iloc[0:3]       # First 3 rows
df.iloc[-1]        # Last row

# Rows by label
df.loc[0]          # Row with label 0

# Specific cell
df.iloc[0, 1]      # Row 0, column 1
df.loc[0, "name"]  # Row 0, column "name"
```

### Filtering Data

```python
# Boolean filtering
adults = df[df["age"] >= 18]

# Multiple conditions
young_nyc = df[(df["age"] < 30) & (df["city"] == "NYC")]

# Using query
result = df.query("age >= 25 and city == 'NYC'")

# Filter by values in list
selected = df[df["city"].isin(["NYC", "LA"])]
```

### Adding and Modifying Columns

```python
# New column
df["is_adult"] = df["age"] >= 18

# Calculated column
df["birth_year"] = 2024 - df["age"]

# Apply function
df["name_upper"] = df["name"].apply(str.upper)

# Rename columns
df.rename(columns={"name": "full_name"}, inplace=True)
```

### Handling Missing Data

```python
# Check for missing values
df.isnull().sum()       # Count NaN per column

# Drop rows with any NaN
df.dropna()

# Drop rows where specific column is NaN
df.dropna(subset=["age"])

# Fill missing values
df.fillna(0)                     # Fill all with 0
df["age"].fillna(df["age"].mean())  # Fill with mean
```

### Grouping and Aggregation

```python
# Group by and aggregate
df.groupby("city")["age"].mean()

# Multiple aggregations
df.groupby("city").agg({
    "age": ["mean", "min", "max"],
    "name": "count"
})

# Value counts
df["city"].value_counts()
```

### Sorting

```python
# Sort by column
df.sort_values("age")                    # Ascending
df.sort_values("age", ascending=False)   # Descending

# Sort by multiple columns
df.sort_values(["city", "age"])

# Sort by index
df.sort_index()
```

### Saving Data

```python
# To CSV
df.to_csv("output.csv", index=False)

# To Excel
df.to_excel("output.xlsx", index=False)

# To JSON
df.to_json("output.json")
```

### Practical Example

```python
import pandas as pd

# Load sales data
sales = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"],
    "product": ["Widget", "Gadget", "Widget", "Gadget"],
    "quantity": [10, 5, 15, 8],
    "price": [9.99, 19.99, 9.99, 19.99]
})

# Add calculated column
sales["revenue"] = sales["quantity"] * sales["price"]

# Summary statistics
print("Total Revenue:", sales["revenue"].sum())
print("Average Order:", sales["quantity"].mean())

# Revenue by product
product_revenue = sales.groupby("product")["revenue"].sum()
print("\nRevenue by Product:")
print(product_revenue)

# Best selling day
daily_sales = sales.groupby("date")["revenue"].sum()
best_day = daily_sales.idxmax()
print(f"\nBest selling day: {best_day}")

# Filter high-value transactions
high_value = sales[sales["revenue"] > 100]
print("\nHigh-value transactions:")
print(high_value)
```

## Summary

pandas provides DataFrames for tabular data manipulation. Read data with `pd.read_csv()`, explore with `head()`, `info()`, and `describe()`. Select columns with `df["column"]` and rows with `iloc` or `loc`. Filter with boolean conditions like `df[df["age"] > 25]`. Group data with `groupby()` and aggregate with functions like `mean()` and `sum()`. pandas integrates well with NumPy and matplotlib for complete data analysis workflows.

## Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Real Python: pandas Tutorial](https://realpython.com/pandas-python-explore-dataset/)
