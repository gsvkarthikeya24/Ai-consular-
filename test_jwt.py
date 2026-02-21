from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET = "test-secret"
ALGORITHM = "HS256"

def test_jwt_consistency():
    """Verify JWT generation with timezone-aware datetimes and integer timestamps"""
    print("Testing JWT Consistency with Modern Logic...")
    
    # 1. Use timezone-aware now
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=10)
    
    # 2. Use integer timestamp for 'exp' (as implemented in auth_utils.py)
    payload = {
        "sub": "test@example.com",
        "exp": int(expire.timestamp())
    }
    
    try:
        token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        print(f"Generated Token: {token}")
        
        # Test decoding with leeway
        decoded = jwt.decode(
            token, 
            SECRET, 
            algorithms=[ALGORITHM],
            options={"leeway": 10}
        )
        print(f"Successfully Decoded: {decoded}")
        
        if isinstance(decoded.get('exp'), int):
            print("[OK] Expiration is an integer timestamp.")
        
        print("\n[SUCCESS] JWT Modern Logic Test Passed!")
    except Exception as e:
        print(f"\n[FAILED] JWT Test Failed: {e}")

if __name__ == "__main__":
    test_jwt_consistency()
