import pandas as pd
from datetime import datetime, timedelta

def process_daily_sales(raw_df, cutoff_days=90):
    """
    Process sales data for a given window of time.

    Parameters
    ----------
    raw_df : pandas.DataFrame
        The raw sales data to be processed.
    cutoff_days : int, optional
        The number of days before the current date to include in the processed data.
        Defaults to 90.

    Returns
    -------
    summary : pandas.DataFrame
        A summary of the processed sales data, including total sales, transaction count, and average sale price for each product and month.
    """
    # Create a copy to avoid modifying the original dataframe
    df = raw_df.copy()
    
    # Convert sale_date column to datetime format for proper date operations
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    # Calculate the cutoff date (e.g., 90 days ago from today)
    cutoff = datetime.now() - timedelta(days=cutoff_days)
    
    # Filter to only include sales on or after the cutoff date
    df = df[df['sale_date'] >= cutoff]
    
    # Remove rows with missing product_id or amount (required for aggregation)
    df = df.dropna(subset=['product_id', 'amount'])
    
    # Ensure amounts are non-negative by clipping negative values to 0
    df['amount'] = df['amount'].clip(lower=0)
    
    # Extract month period from sale_date for grouping
    df['month'] = df['sale_date'].dt.to_period('M')
    
    # Group by month and product, calculating aggregate metrics
    summary = df.groupby(['month', 'product_id']).agg(
        total_sales=('amount', 'sum'),
        transaction_count=('amount', 'count'),
        avg_sale=('amount', 'mean')
    ).reset_index()
    
    return summary