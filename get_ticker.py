from supabase_connect import supabase, supabase_admin, supabase_anon
from import_stock import fetch_stock_data, save_stock_data
import os
from difflib import SequenceMatcher

print("SUPABASE_URL:", os.getenv("supabaseURL"))
print("ANON_KEY starts with:", os.getenv("supabaseKey")[:10])

def get_ticker(company_name):
    ticker = []
    search_name = "%" + company_name + "%"
    print(f"🔍 Searching for company: {company_name}")
    
    try:
        value = supabase_anon.table("Company_ticker_all").select("*").eq("name", company_name).execute()
        
        if not value.data:
            print(f"❌ No company found with exact name: {company_name}")
            print("💡 Try searching with partial name or check spelling")
            return None
        
        print(f"✅ Found {len(value.data)} company(ies)")
        
        for row in value.data:
            ticker.append([row['cik'], row['ticker'], row['exchange'], row['name']])
            print(f"   📊 {row['ticker']} - {row['name']} ({row['exchange']})")
        
        return ticker
        
    except Exception as e:
        print(f"❌ Error searching for company: {e}")
        return None



def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
   

def get_ticker_fuzzy(company_name):
    ticker = []
    n=5
    search_name = "%" + company_name + "%"
     # Fuzzy search using case-insensitive partial match
    value = supabase_anon.table("Company_ticker_all").select("*").ilike("name", search_name).execute()

    # Sort results by string similarity
    sorted_matches = sorted(
            value.data,
            key=lambda row: similarity(company_name, row["name"]),
            reverse=True)
    
    # change the value of n to get the number of top matches
    top_matches = sorted_matches[:n]

    for row in top_matches:
        ticker.append([row['cik'], row['ticker'], row['exchange'], row['name']])
        print(f"   📊 {row['ticker']} - {row['name']} ({row['exchange']})")
    
    return ticker


if __name__ == "__main__":
    A = get_ticker("NVIDIA CORP")
    print(A)
    
    if A is None:
        print("❌ Cannot proceed without company data")
        exit(1)
    
    B = get_ticker_fuzzy("soft")
    print(B)
    
    if B is None:
        print("❌ Cannot proceed without company data")
        exit(1)
    
    #temp = fetch_stock_data(A[0][1], "compact")
    #save_stock_data(A[0][1], temp)
    #print(f"✅ Successfully processed: {A[0]}")
    #print(f"📋 Data type: {type(A)}")