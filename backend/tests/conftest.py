import pytest
import requests
import sys
import os

# Add the project root to python path to import app modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def auth_token(api_base_url):
    """Get authentication token for tests"""
    payload = {
        "email": "student1@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{api_base_url}/api/auth/login", json=payload)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to {api_base_url}. Is the backend running?")
    except Exception as e:
        pytest.fail(f"Authentication failed: {e}")

@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
