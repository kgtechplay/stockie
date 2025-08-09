import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_stock_data(symbol, output_size='compact'):
    """
    Fetch daily stock data for a given symbol from Alpha Vantage API
    
    Args:
        symbol (str): Stock symbol (e.g., 'IBM', 'AAPL', 'MSFT')
        output_size (str): 'compact' for last 100 data points, 'full' for full history
    
    Returns:
        pandas.DataFrame: DataFrame with daily stock data
    """
    # Get API key from environment variable
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in your .env file")
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize={output_size}'
    r = requests.get(url)
    data = r.json()
    
    # Check for API errors
    if 'Error Message' in data:
        raise ValueError(f"API Error: {data['Error Message']}")
    
    if 'Note' in data:
        print(f"API Note: {data['Note']}")
    
    # Extract the daily time series
    time_series = data.get("Time Series (Daily)", {})
    
    if not time_series:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series, orient="index")
    
    # Make the date a column instead of the index
    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date (newest first)
    df.sort_values('date', ascending=False, inplace=True)
    
    return df

def save_stock_data(symbol, df, filename=None):
    """
    Save stock data to CSV file
    
    Args:
        symbol (str): Stock symbol
        df (pandas.DataFrame): DataFrame to save
        filename (str, optional): Custom filename. If None, uses default format
    """
    if filename is None:
        filename = f"{symbol.lower()}_daily.csv"
    
    df.to_csv(filename, index=False)
    print(f"Saved {filename} with {len(df)} rows")

# Example usage
if __name__ == "__main__":
    # Fetch data for IBM (original example)
    try:
        df = fetch_stock_data('IBM')
        save_stock_data('IBM', df)
        
        # You can also fetch data for other symbols
        # df_aapl = fetch_stock_data('AAPL')
        # save_stock_data('AAPL', df_aapl)
        
    except Exception as e:
        print(f"Error: {e}")