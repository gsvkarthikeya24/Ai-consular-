import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
try:
    conn = psycopg2.connect(uri)
    with conn.cursor() as cur:
        cur.execute("SELECT doc FROM users WHERE doc->>'email' = 'dell6565@gmail.com'")
        row = cur.fetchone()
        if row:
            doc = row[0]
            if isinstance(doc, str):
                doc = json.loads(doc)
            print(f"User: {doc.get('email')}")
            print(f"Password starts with: {doc.get('password')[:10]}...")
            print(f"Is string: {isinstance(doc.get('password'), str)}")
        else:
            print("User not found")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
