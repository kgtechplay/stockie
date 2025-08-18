import supabase
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("supabaseURL")
key = os.getenv("supabaseKey")
service_key = os.getenv("supabaseServiceKey")

supabase_anon = supabase.create_client(url, key)
supabase_admin = supabase.create_client(url, service_key)

print(supabase_anon )
print(supabase_admin)

res = supabase_anon.table("Company_ticker_all").select("*").limit(1).execute()
print("Anon read result:", res.data)

