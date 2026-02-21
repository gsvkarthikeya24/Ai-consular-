from app.database import connect_db, get_collection
from app.utils.auth_utils import hash_password, verify_password
from app.models.user import UserCreate
import os
from dotenv import load_dotenv

load_dotenv()
connect_db()
users = get_collection("users")

# 1. Clean up
email_reg = "CaseTest@Example.Com"
email_login = "casetest@example.com"
pwd = "mypassword123"
users.delete_many({"email": email_reg.lower()})

# 2. Simulate /register route with normalization
print(f"Registering with {email_reg}...")
email_normalized = email_reg.lower()
user_dict = {
    "name": "Case Test",
    "email": email_normalized,
    "password": hash_password(pwd),
    "role": "student"
}
users.insert_one(user_dict)

# 3. Simulate /login route with normalization
print(f"Logging in with {email_login}...")
email_login_norm = email_login.lower()
found_user = users.find_one({"email": email_login_norm})

if found_user:
    is_valid = verify_password(pwd, found_user.get("password"))
    print(f"Login successful for {email_login}? {is_valid}")
else:
    print(f"User {email_login} NOT found")
