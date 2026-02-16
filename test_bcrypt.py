from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test hashing short passwords
test_passwords = ["admin123", "password123", "demo123"]

print("Testing bcrypt hashing...")
for pwd in test_passwords:
    print(f"\nPassword: {pwd}")
    print(f"Length: {len(pwd)} bytes")
    print(f"UTF-8 bytes: {len(pwd.encode('utf-8'))} bytes")
    try:
        hashed = pwd_context.hash(pwd)
        print(f"Hash: {hashed[:50]}...")
        print(f"Hash length: {len(hashed)}")
        print("✓ Success!")
    except Exception as e:
        print(f"✗ Error: {e}")
