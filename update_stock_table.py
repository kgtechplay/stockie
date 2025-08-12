from supabase_connect import supabase, supabase_admin, supabase_anon
from get_ticker import get_ticker
from import_stock import fetch_stock_data, save_stock_data
import json
import pandas as pd
import os
import psycopg2
from psycopg2 import connect
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_DB_URL")
assert DB_URL, "Missing SUPABASE_DB_URL in .env"

def insert_stock_data(ticker: str, name: str, exchange: str):
    ticker = ticker.upper()
    csv_path = f"{ticker.lower()}_daily.csv"

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    print(f"\nLoading {csv_path} into Supabase...")

    df = pd.read_csv(csv_path)

    # Clean and prepare data
    df.columns = [c.strip().lower() for c in df.columns]
    rename_map = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }
    df = df.rename(columns=rename_map)

    required = ['date', 'open', 'high', 'low', 'close', 'volume']
    df = df[required]
    df['ticker'] = ticker
    df['name'] = name
    df['exchange'] = exchange
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # Ensure correct column order for insertion
    df = df[['ticker', 'date', 'exchange', 'name', 'open', 'high', 'low', 'close', 'volume']]
    rows = df.dropna(subset=['date']).to_records(index=False).tolist()

    # Insert into Supabase
    inserted = 0
    try:
        with connect(DB_URL) as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO stock_data (ticker, date, exchange, name, open, high, low, close, volume)
                    VALUES %s
                    ON CONFLICT (ticker, date) DO NOTHING;
                """
                execute_values(cur, insert_query, rows, page_size=500)
                inserted = cur.rowcount
            conn.commit()
        print(f"✅ Inserted {inserted} new rows for {ticker}")
    except Exception as e:
        print(f"❌ Failed to insert for {ticker}: {e}")





if __name__ == "__main__":
    company_name="ADVANCED MICRO DEVICES INC"
    comp_details=get_ticker(company_name)
    df =fetch_stock_data(comp_details[0][1], "full")
    save_stock_data(comp_details[0][1], df)
    insert_stock_data(comp_details[0][1], comp_details[0][3], comp_details[0][2])

