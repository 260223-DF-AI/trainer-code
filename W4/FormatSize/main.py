import pandas as pd
import pyarrow
import json
import time
import os

# Create sample data
def create_sample_data(n_rows=100000):
    """Generate sample dataset for format comparison."""
    import random
    
    data = {
        'id': range(n_rows),
        'name': [f'User_{i}' for i in range(n_rows)],
        'age': [random.randint(18, 80) for _ in range(n_rows)],
        'salary': [random.uniform(30000, 150000) for _ in range(n_rows)],
        'department': [random.choice(['Engineering', 'Sales', 'Marketing', 'HR']) 
                      for _ in range(n_rows)],
        'active': [random.choice([True, False]) for _ in range(n_rows)]
    }
    return pd.DataFrame(data)

print("Creating sample data...")
df = create_sample_data(10000000)
print(f"Created DataFrame with {len(df):,} rows")
print(df.head())

start = time.time()

df.to_csv("data/sample_data.csv", index=False)

csv_time = time.time() - start
print("Saved sample data to sample_data.csv")
csv_size = os.path.getsize("data/sample_data.csv")

start_json = time.time()

df.to_json("data/sample_data.json", orient="records", lines=True)

json_time = time.time() - start_json
print("Saved sample data to sample_data.json")
json_size = os.path.getsize("data/sample_data.json")

start_parequet = time.time()

df.to_parquet("data/sample_data.parquet", index=False)

parquet_time = time.time() - start_parequet

print("Saved sample data to sample_data.parquet")
parquet_size = os.path.getsize("data/sample_data.parquet")

print(f"CSV size: {csv_size / 1024 / 1024:.4f} MB")
print(f"JSON size: {json_size / 1024 / 1024:.4f} MB")
print(f"Parquet size: {parquet_size / 1024 / 1024:.4f} MB")

print(f"CSV time: {csv_time:.4f} seconds")
print(f"JSON time: {json_time:.4f} seconds")
print(f"Parquet time: {parquet_time:.4f} seconds")

