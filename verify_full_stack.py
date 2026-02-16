import requests
import sys
import time

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def check_backend():
    print(f"Checking Backend at {BACKEND_URL}...")
    try:
        resp = requests.get(f"{BACKEND_URL}/health")
        if resp.status_code == 200:
            print("[OK] Backend is reachable (Health Check Passed)")
        else:
            print(f"[FAIL] Backend health check returned {resp.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Backend not reachable")
        # Try waiting a bit if it's just starting up
        return False
    return True

def check_frontend():
    print(f"Checking Frontend at {FRONTEND_URL}...")
    try:
        resp = requests.get(FRONTEND_URL)
        if resp.status_code == 200:
            print("[OK] Frontend is reachable")
        else:
            print(f"[FAIL] Frontend returned {resp.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Frontend not reachable")
        return False
    return True

def test_login():
    print("\nTesting Login API...")
    url = f"{BACKEND_URL}/api/auth/login"
    payload = {
        "email": "student1@example.com",
        "password": "password123"
    }
    
    try:
        # We need to set Content-Type
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=payload, headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            if "access_token" in data:
                print(f"[OK] Login Successful! Token received.")
                return True
            else:
                print("[FAIL] Login successful but no token in response")
        else:
            print(f"[FAIL] Login failed with status {resp.status_code}")
            print(f"     Response: {resp.text}")
    except Exception as e:
        print(f"[FAIL] Login request error: {e}")
    return False

if __name__ == "__main__":
    print("=== Full Stack Connectivity Check ===\n")
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    login_ok = False
    if backend_ok:
        login_ok = test_login()
    else:
        print("\n[SKIP] Skipping login test due to backend failure")
    
    print("\n=== Summary ===")
    print(f"Backend:  {'[PASS]' if backend_ok else '[FAIL]'}")
    print(f"Frontend: {'[PASS]' if frontend_ok else '[FAIL]'}")
    print(f"API/DB:   {'[PASS]' if backend_ok and login_ok else '[FAIL]'}")
