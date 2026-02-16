import requests
import json

# Test exactly as frontend would
url = "http://localhost:8000/api/auth/login"
headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:5173"  # Simulate frontend origin
}
data = {
    "email": "student.demo@university.edu",
    "password": "demo123"
}

print("Testing login AS IF from frontend...")
print(f"URL: {url}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Data: {json.dumps(data, indent=2)}")
print("-" * 50)

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Check if we got the token
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"\n[SUCCESS] Token received: {token[:50]}...")
    else:
        print(f"\n[FAILED] with status {response.status_code}")
        
except Exception as e:
    print(f"[Error]: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"Response status: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
