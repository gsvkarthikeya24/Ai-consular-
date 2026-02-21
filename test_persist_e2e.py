import requests
import json
import secrets

BASE_URL = "http://localhost:8000/api/auth"
test_email = f"test_{secrets.token_hex(4)}@example.com"
test_pwd = "password123"

# 1. Register
print(f"Registering {test_email}...")
reg_data = {
    "name": "Persistence Test",
    "email": test_email,
    "password": test_pwd,
    "branch": "CSE",
    "year": 1,
    "interests": ["Testing"],
    "career_goal": "Job"
}

resp = requests.post(f"{BASE_URL}/register", json=reg_data)
print(f"Register status: {resp.status_code}")
if resp.status_code != 201:
    print(f"Error: {resp.text}")
    exit(1)

# 2. Login
print(f"Logging in {test_email}...")
login_data = {
    "email": test_email,
    "password": test_pwd
}
resp = requests.post(f"{BASE_URL}/login", json=login_data)
print(f"Login status: {resp.status_code}")
if resp.status_code == 200:
    print("SUCCESS: Registered user can log in!")
else:
    print(f"FAILURE: {resp.text}")

# 3. Check DB directly (optional but good)
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGODB_URI")
conn = psycopg2.connect(uri)
with conn.cursor() as cur:
    cur.execute("SELECT id, doc FROM users WHERE doc->>'email' = %s", (test_email.lower(),))
    row = cur.fetchone()
    if row:
        print(f"DB CHECK: User found in DB with ID: {row[0]}")
    else:
        print("DB CHECK: User NOT found in DB!")
conn.close()
