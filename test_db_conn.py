import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_DB_URL1")
assert url, "SUPABASE_DB_URL missing"

try:
    conn = psycopg2.connect(url)
    print("✅ Successfully connected to Supabase Postgres DB")
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("Current time:", cur.fetchone()[0])
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
