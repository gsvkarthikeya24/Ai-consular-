from app.database import connect_db, get_collection
from app.config import settings
import os
from dotenv import load_dotenv

load_dotenv()

connect_db()
users_collection = get_collection("users")

email = "dell6565@gmail.com"
user = users_collection.find_one({"email": email})

if user:
    print(f"Found user: {user.get('email')}")
    print(f"Password hash exists: {bool(user.get('password'))}")
    print(f"Full user keys: {list(user.keys())}")
else:
    print(f"User NOT found: {email}")
