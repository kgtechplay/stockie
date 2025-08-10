from supabase_connect import supabase, supabase_admin, supabase_anon
from import_stock import fetch_stock_data, save_stock_data

def get_ticker(company_name):
    ticker = []
    search_name = "%" + company_name + "%"
    print(search_name)
    value = supabase_anon.table("Company_ticker_all").select("*").eq("name", company_name).execute()
    
    for row in value.data:
        ticker.append([row['cik'],row['ticker'],row['exchange'],row['name']])
    #print(ticker)
   
    return ticker

if __name__ == "__main__":
    A=get_ticker("ADVANCED MICRO DEVICES INC")
    temp=fetch_stock_data(A[0][1],"compact")
    save_stock_data(A[0][1], temp)
    print(A)
    print(type(A))
   
