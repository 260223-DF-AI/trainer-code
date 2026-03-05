sales_data = [
    # ["date", "product", "category", "quantity", "price", "region"],
    ["2024-01-01", "Widget A", "Electronics", "10", "29.99", "North"],
    ["2024-01-01", "Widget B", "Electronics", "5", "49.99", "South"],
    ["2024-01-02", "Gadget X", "Accessories", "15", "14.99", "North"],
    ["2024-01-02", "Widget A", "Electronics", "8", "29.99", "East"],
    ["2024-01-03", "Gadget Y", "Accessories", "20", "19.99", "West"],
    ["2024-01-03", "Widget B", "Electronics", "12", "49.99", "North"],
    ["2024-01-04", "Widget A", "Electronics", "6", "29.99", "South"],
    ["2024-01-04", "Gadget X", "Accessories", "25", "14.99", "East"],
    ["2024-01-05", "Widget B", "Electronics", "9", "49.99", "West"],
    ["2024-01-05", "Gadget Y", "Accessories", "18", "19.99", "North"],
    ["2024-01-06", "Widget A", "Electronics", "14", "29.99", "East"],
    ["2024-01-06", "Gadget X", "Accessories", "22", "14.99", "South"],
    ["2024-01-07", "Widget B", "Electronics", "7", "49.99", "North"],
    ["2024-01-07", "Gadget Y", "Accessories", "16", "19.99", "West"],
]


import pandas as pd

sales = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"],
    "product": ["Widget", "Gadget", "Widget", "Gadget"],
    "quantity": [10, 5, 15, 8],
    "price": [9.99, 19.99, 9.99, 19.99]
})

#print(sales)

df = pd.DataFrame( data=sales_data )
df.columns = ["date", "product", "category", "quantity", "price", "region"] 

#print(df)

#print(df.info())

#print(df.describe())

#print(df.dtypes)

df["date"] = pd.to_datetime(df["date"])
df["quantity"]  = df["quantity"].astype(int)
df["price"] = df["price"].astype(float)
# print(df.dtypes)
df["total_sales"] = df["quantity"] * df["price"]

#display on specific columns
#print(df[["date","total_sales"]])

filtered_df = df[(df["category"] == "Electronics") & (df["region"] == "North")]

filetered_df = df.query("category == 'Electronics' and region == 'North'")
# print(filtered_df)

print(df.groupby("region")["total_sales"].sum())
print(df["quantity"].sum())

print(df.shape[0])