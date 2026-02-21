from app.database import connect_db, get_collection
from app.utils.auth_utils import verify_password
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["PYTHONPATH"] = "backend"

connect_db()
users_collection = get_collection("users")

email = "dell6565@gmail.com"
password = "password123" # Assuming this is what the user used for testing

user = users_collection.find_one({"email": email})

if user:
    print(f"Found user: {user.get('email')}")
    stored_hash = user.get('password')
    print(f"Stored hash: {stored_hash}")
    
    try:
        is_valid = verify_password(password, stored_hash)
        print(f"Password 'password123' valid? {is_valid}")
    except Exception as e:
        print(f"Verification error: {e}")
else:
    print(f"User {email} not found")
