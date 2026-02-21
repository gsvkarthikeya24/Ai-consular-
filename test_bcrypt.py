import bcrypt

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

pwd = "testpassword123"
hashed = hash_password(pwd)
print(f"Hashed: {hashed}")
valid = verify_password(pwd, hashed)
print(f"Is valid: {valid}")

# Test with the exact hash from DB (if it was password123)
db_hash = "$2b$12$jOCIYy07GaZl8qH/as3VsOIo0v3nWSShrj3pyiDGJE/KqumIpljRe"
print(f"DB Hash valid for 'password123'? {verify_password('password123', db_hash)}")
