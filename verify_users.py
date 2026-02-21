import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
if not (uri.startswith("postgresql://") or uri.startswith("postgres://")):
    print("Not a postgres URI")
    exit(1)

try:
    conn = psycopg2.connect(uri)
    with conn.cursor() as cur:
        cur.execute("SELECT id, doc FROM users")
        rows = cur.fetchall()
        print(f"Total users in DB: {len(rows)}")
        for row in rows:
            print(f"ID: {row[0]} | Email: {row[1].get('email')}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
