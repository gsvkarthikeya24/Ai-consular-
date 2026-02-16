import requests
import json

# Test login endpoint for regular student
url = "http://localhost:8000/api/auth/login"
data = {
    "email": "student1@example.com",
    "password": "password123"
}

print("Testing login endpoint for regular student...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("-" * 50)

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'response'):
        print(f"Response text: {e.response.text}")
