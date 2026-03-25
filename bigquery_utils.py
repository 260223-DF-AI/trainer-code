import pandas as pd
from google.cloud import bigquery

# option number 1 - leverage te context of the file you're working on to provide information to the AI!

# Function to connect to BigQuery and run a query, returning resulst as a DataFrame
def run_query(query):
    client = bigquery.Client()
    df = client.query(query).to_dataframe()
    return df

def check_null_values(df: pd.DataFrame, column: str) -> int:
    """count null values in a column."""
    return df[column].isnull().sum()

def check_duplicate_values(df: pd.DataFrame, column: str) -> int:
    """count duplicate values in a column."""
    return df[column].duplicated().sum()


def get_stations_from_bigquery():
    # connect to bigquery client
    client = bigquery.Client()

    # draft an sql query to get the top five stations in the citibike dataset
    query = """
    SELECT
        start_station_name,
        start_station_id,
        COUNT(*) AS num_trips
    FROM `bigquery-public-data.new_york_citibike.citibike_trips`
    GROUP BY start_station_name, start_station_id
    ORDER BY num_trips DESC
    LIMIT 5
    """

    # run the query
    df = client.query(query).to_dataframe()

    return df


def get_all_stations_from_bigquery():
    # connect to bigquery client
    client = bigquery.Client()

    # draft an sql query to get all unique stations (both start and end) in the citibike dataset
    query = """
    SELECT DISTINCT
        station_name,
        station_id
    FROM (
        SELECT
            start_station_name AS station_name,
            start_station_id AS station_id
        FROM `bigquery-public-data.new_york_citibike.citibike_trips`
        UNION DISTINCT
        SELECT
            end_station_name AS station_name,
            end_station_id AS station_id
        FROM `bigquery-public-data.new_york_citibike.citibike_trips`
    )
    ORDER BY station_name
    """

    # run the query
    df = client.query(query).to_dataframe()

    return df 