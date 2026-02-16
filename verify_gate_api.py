import requests
import sys
import json

BASE_URL = "http://localhost:8000"

def test_gate_endpoints():
    print("=== Testing GATE API Endpoints ===")
    
    # 1. Login
    print("[*] Logging in...")
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={"email": "student1@example.com", "password": "password123"})
        if resp.status_code != 200:
            print(f"[FAIL] Login failed: {resp.status_code}")
            return
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        return

    # 2. Get Subjects
    print("\n[*] Testing Get Subjects...")
    resp = requests.get(f"{BASE_URL}/api/gate/subjects", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[OK] Subjects for {data.get('branch')}: {len(data.get('subjects', []))}")
    else:
        print(f"[FAIL] Get Subjects failed: {resp.status_code}")

    # 3. Get Questions
    print("\n[*] Testing Get Questions...")
    resp = requests.get(f"{BASE_URL}/api/gate/questions?limit=5", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[OK] Fetched {len(data)} questions.")
        if data:
            print(f"     Sample: {data[0].get('question')[:50]}...")
            question_id = data[0].get("question_id")
            
            # 4. Submit Answer
            if question_id:
                print(f"\n[*] Testing Submit Answer for QID: {question_id}...")
                payload = {
                    "question_id": question_id,
                    "selected_answer": 0,
                    "time_taken": 30
                }
                sub_resp = requests.post(f"{BASE_URL}/api/gate/submit-answer", json=payload, headers=headers)
                if sub_resp.status_code == 200:
                    res = sub_resp.json()
                    print(f"[OK] Submission successful. Correct: {res.get('correct')}")
                else:
                    print(f"[FAIL] Submit Answer failed: {sub_resp.status_code}")
    else:
        print(f"[FAIL] Get Questions failed: {resp.status_code}")

    # 5. Get Progress
    print("\n[*] Testing Get Progress...")
    resp = requests.get(f"{BASE_URL}/api/gate/progress", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[OK] Progress fetched. Accuracy: {data.get('accuracy')}%")
    else:
        print(f"[FAIL] Get Progress failed: {resp.status_code}")

    # 6. Get Resources (New Endpoint)
    print("\n[*] Testing Get Resources...")
    resp = requests.get(f"{BASE_URL}/api/gate/resources", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[OK] Fetched {len(data)} resource categories.")
        if data:
            print(f"     Sample Category: {data[0].get('subject')}")
            print(f"     Resources count: {len(data[0].get('resources', []))}")
    else:
        print(f"[FAIL] Get Resources failed: {resp.status_code}")

if __name__ == "__main__":
    test_gate_endpoints()
