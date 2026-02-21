from app.database import connect_db, get_collection
from app.utils.auth_utils import hash_password, verify_password
from app.models.user import UserCreate
import os
from dotenv import load_dotenv

load_dotenv()
connect_db()
users = get_collection("users")

# 1. Clean up old test user
email = "persist_test@example.com"
pwd = "mypassword123"
users.delete_many({"email": email})

# 2. Register (Simulate auth.py)
print(f"Registering {email}...")
user_data = UserCreate(
    name="Test User",
    email=email,
    password=pwd,
    branch="CSE",
    year=1,
    interests=["AI"],
    career_goal="Research"
)

user_dict = user_data.model_dump(exclude={"password"})
user_dict.update({
    "password": hash_password(pwd),
    "role": "student"
})

result = users.insert_one(user_dict)
print(f"Inserted ID: {result.inserted_id}")

# 3. Login (Simulate auth.py)
print(f"Logging in {email}...")
found_user = users.find_one({"email": email})

if not found_user:
    print("Error: User not found in DB after registration")
else:
    print(f"User found. Keys: {list(found_user.keys())}")
    stored_hash = found_user.get("password")
    is_valid = verify_password(pwd, stored_hash)
    print(f"Password valid? {is_valid}")
    if not is_valid:
        print(f"Stored hash: {stored_hash}")
        print(f"Re-hashed check: {hash_password(pwd)[:10]}...")
