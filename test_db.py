from pymongo import MongoClient
import sys

def test_conn(host):
    print(f"Testing {host}...")
    try:
        client = MongoClient(host, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print(f"SUCCESS: Connected to {host}")
        return True
    except Exception as e:
        print(f"FAILED: {host} - {e}")
        return False

if __name__ == "__main__":
    test_conn("mongodb://localhost:27017")
    test_conn("mongodb://127.0.0.1:27017")
