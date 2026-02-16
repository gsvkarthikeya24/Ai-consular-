"""
Check database status and see what users exist
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import connect_db, get_collection, is_mock_mode, is_db_connected

print("Connecting to database...")
connect_db()

print(f"\nDatabase connected: {is_db_connected()}")
print(f"Using mock mode (mongomock): {is_mock_mode()}")

users_collection = get_collection("users")
if users_collection is not None:
    user_count = users_collection.count_documents({})
    print(f"\nTotal users in database: {user_count}")
    
    if user_count > 0:
        print("\nUsers in database:")
        for user in users_collection.find({}, {"_id": 0, "email": 1, "name": 1, "role": 1}):
            print(f"  - {user.get('email')} ({user.get('role')}) - {user.get('name')}")
    else:
        print("\n⚠️  No users found in database! Demo data was not seeded.")
else:
    print("\n❌ Database connection failed or collection is None")
