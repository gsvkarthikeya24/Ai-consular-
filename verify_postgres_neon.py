import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.database import connect_db, get_database, is_db_connected
from app.config import settings

def test_postgresql():
    print(f"Testing connection to: {settings.mongodb_uri}")
    print(f"Is Postgres: {settings.is_postgres}")
    
    connect_db()
    
    if not is_db_connected():
        print("FAILED: Could not connect to database")
        return
    
    print("SUCCESS: Connected to database")
    
    # Test basic CRUD
    db = get_database()
    test_col = db["test_collection"]
    
    print("Testing insert_one...")
    test_col.insert_one({"name": "Test User", "email": "test@example.com", "data": [1, 2, 3]})
    
    print("Testing find_one...")
    doc = test_col.find_one({"email": "test@example.com"})
    print(f"Found doc: {doc}")
    
    if doc and doc["name"] == "Test User":
        print("SUCCESS: CRUD test passed")
    else:
        print("FAILED: CRUD test failed")
    
    # Cleanup
    print("Cleaning up...")
    test_col.delete_many({"email": "test@example.com"})
    print("Cleanup done")

if __name__ == "__main__":
    test_postgresql()
