import json
import pandas as pd

def convert_json_to_csv(json_file_path, csv_file_path):
    """
    Convert company_tickers_exchange.json to CSV format
    
    Args:
        json_file_path (str): Path to the JSON file
        csv_file_path (str): Path for the output CSV file
    """
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Extract fields and data
        fields = data.get('fields', [])
        records = data.get('data', [])
        
        # Create DataFrame
        df = pd.DataFrame(records, columns=fields)
        
        # Save to CSV
        df.to_csv(csv_file_path, index=False)
        
        print(f"Successfully converted {json_file_path} to {csv_file_path}")
        print(f"Total records: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Display first few rows
        print("\nFirst 5 rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"Error converting file: {e}")
        return None

if __name__ == "__main__":
    # Convert the JSON file to CSV
    json_file = "company_tickers_exchange.json"
    csv_file = "company_tickers_exchange.csv"
    
    df = convert_json_to_csv(json_file, csv_file)
