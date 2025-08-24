import os
import requests
import psycopg2
from datetime import datetime
def fetch_and_store_stock_data():
    """
    Fetch daily stock data from Alpha Vantage and insert into Postgres.
    """
    # Read environment variables
    api_key = os.getenv("API_KEY")
    symbol = os.getenv("STOCK_SYMBOL", "AAPL")  # default stock if not set
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_name = os.getenv("POSTGRES_DB", "stocks")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    if not api_key:
        raise ValueError("API_KEY not set in environment")
    # Alpha Vantage API endpoint
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=compact"
    )
    # Fetch stock data
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        raise Exception(f"Error fetching data: {data}")
    time_series = data["Time Series (Daily)"]
    # Connect to Postgres
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_pass
    )
    cur = conn.cursor()
    # Ensure table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            id SERIAL PRIMARY KEY,
            symbol TEXT,
            date DATE,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume BIGINT
        )
    """)
    # Insert each row
    for date_str, values in time_series.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        cur.execute("""
            INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO NOTHING
        """, (
            symbol,
            date_obj,
            values["1. open"],
            values["2. high"],
            values["3. low"],
            values["4. close"],
            values["6. volume"]
        ))
    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted {len(time_series)} rows for {symbol}")
