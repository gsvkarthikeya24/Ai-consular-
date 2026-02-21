from typing import Any
from .config import settings

# Database client
client: Any = None
database: Any = None


def connect_db():
    """Connect to MongoDB or PostgreSQL"""
    global client, database
    try:
        if settings.is_postgres:
            from .postgres_adapter import PostgresClient
            client = PostgresClient(settings.mongodb_uri)
            database = client[settings.database_name]
            print(f"[OK] Connected to PostgreSQL: {settings.database_name}")
        else:
            from pymongo import MongoClient
            client = MongoClient(
                settings.mongodb_uri, 
                serverSelectionTimeoutMS=2000,
                connectTimeoutMS=2000
            )
            database = client[settings.database_name]
            # Verify connection
            client.admin.command('ping')
            print(f"[OK] Connected to MongoDB: {settings.database_name}")
    except Exception as e:
        print(f"[!] Warning: Could not connect to database at {settings.mongodb_uri}. Error: {e}")
        
        if not settings.is_postgres:
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
        else:
            print("[ERROR] PostgreSQL connection failed. No mock available for Postgres.")
            client = None
            database = None


def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("[X] Closed MongoDB connection")


def get_database() -> Any:
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
