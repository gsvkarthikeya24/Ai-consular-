from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from .config import settings

# MongoDB client
client: MongoClient = None
database: Database = None


def connect_db():
    """Connect to MongoDB with shorter timeout"""
    global client, database
    try:
        # Use shorter timeout for faster feedback
        client = MongoClient(
            settings.mongodb_uri, 
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000
        )
        database = client[settings.database_name]
        # Verify connection
        client.admin.command('ping')
        print(f"[OK] Connected to MongoDB: {settings.database_name}")
    except (ServerSelectionTimeoutError, Exception) as e:
        print(f"[!] Warning: Could not connect to real MongoDB at {settings.mongodb_uri}. Error: {e}")
        print("[INFO] Switching to In-Memory Database (mongomock). Data will NOT persist.")
        
        try:
            import mongomock
            client = mongomock.MongoClient()
            database = client[settings.database_name]
            print(f"[OK] Connected to MOCK MongoDB: {settings.database_name}")
        except ImportError:
            print("[ERROR] mongomock not installed. Please run: pip install mongomock")
            client = None
            database = None


def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("[X] Closed MongoDB connection")


def get_database() -> Database:
    """Get database instance"""
    return database


def is_db_connected() -> bool:
    """Check if database is reachable"""
    global client
    if not client:
        return False
    try:
        client.admin.command('ping')
        return True
    except:
        return False


# Collection references
def get_collection(name: str):
    """Get collection by name, returns None if DB is down"""
    if database is None:
        return None
    return database[name]


def is_mock_mode() -> bool:
    """Check if using mongomock"""
    try:
        import mongomock
        return isinstance(client, mongomock.MongoClient)
    except ImportError:
        return False
