import requests
import sys
import json

BASE_URL = "http://localhost:8000"

def test_login():
    print(f"[*] Testing Login at {BASE_URL}/api/auth/login...")
    payload = {
        "email": "student1@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        if response.status_code == 200:
            print("[OK] Login successful!")
            data = response.json()
            token = data.get("access_token")
            user = data.get("user")
            print(f"     Token received: {token[:10]}...")
            print(f"     User: {user['name']} ({user['email']})")
            return token
        else:
            print(f"[FAIL] Login failed with status {response.status_code}")
            print(f"       Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] Could not connect to {BASE_URL}. Is the backend running?")
        return None

def test_get_tasks(token):
    print(f"\n[*] Testing Get Tasks at {BASE_URL}/api/tasks...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        print(f"[OK] Fetched {len(tasks)} tasks.")
        if tasks:
            print(f"     Sample Task: {tasks[0].get('title')}")
    else:
        print(f"[FAIL] Failed to fetch tasks. Status: {response.status_code}")
        print(f"       Response: {response.text}")

def test_career_domains(token):
    print(f"\n[*] Testing Get Career Domains at {BASE_URL}/api/career/domains...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/career/domains", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Fetched {data.get('total_count', 0)} career domains.")
        else:
            print(f"[FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_internships(token):
    print(f"\n[*] Testing Get Internships at {BASE_URL}/api/internships...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/internships", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Fetched {len(data)} internships.")
        else:
            print(f"[FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_courses(token):
    print(f"\n[*] Testing Get All Courses at {BASE_URL}/api/courses/all...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/courses/all", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Fetched {len(data)} courses.")
        else:
            print(f"[FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_resume_templates():
    print(f"\n[*] Testing Get Resume Templates at {BASE_URL}/api/resume/templates...")
    try:
        response = requests.get(f"{BASE_URL}/api/resume/templates")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Fetched {len(data)} resume templates.")
        else:
            print(f"[FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_mentor_chat(token):
    print(f"\n[*] Testing Mentor Chat at {BASE_URL}/api/mentor/chat...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "message": "How do I prepare for technical interviews?",
        "conversation_history": []
    }
    try:
        response = requests.post(f"{BASE_URL}/api/mentor/chat", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Mentor replied: {data.get('response')[:50]}...")
        else:
            print(f"[FAIL] Status: {response.status_code}")
            print(f"       Response: {response.text}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_stats(token):
    print(f"\n[*] Testing Student Stats at {BASE_URL}/api/stats/student...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/stats/student", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Stats fetched. Tasks Completed: {data.get('tasks_completed')}")
        else:
            print(f"[FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

def test_tasks_flow(token):
    print(f"\n[*] Testing Tasks Workflow at {BASE_URL}/api/tasks...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create Task
    task_id = None
    try:
        payload = {
            "type": "homework",
            "subject": "Test Subject",
            "title": "Test Task for Verification",
            "description": "This is a temporary task created by the verification script.",
            "difficulty": "medium",
            "due_date": "2026-12-31T23:59:59"
        }
        resp = requests.post(f"{BASE_URL}/api/tasks", json=payload, headers=headers)
        if resp.status_code == 201:
            task_data = resp.json()
            task_id = task_data.get("id")
            print(f"[OK] Created Task ID: {task_id}")
        else:
            print(f"[FAIL] Create Task Failed: {resp.status_code} - {resp.text}")
            return
            
        # 2. Get Tasks
        resp = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        if resp.status_code == 200:
            tasks = resp.json()
            found = any(t['id'] == task_id for t in tasks)
            if found:
                print(f"[OK] Task {task_id} found in list.")
            else:
                print(f"[FAIL] Task {task_id} NOT found in list.")
        
        # 3. Delete Task
        if task_id:
            resp = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
            if resp.status_code == 200:
                print(f"[OK] Task {task_id} deleted successfully.")
            else:
                print(f"[FAIL] Delete Task Failed: {resp.status_code}")

    except Exception as e:
        print(f"[FAIL] Error in Tasks Workflow: {e}")

def test_course_enrollment(token):
    print(f"\n[*] Testing Course Enrollment at {BASE_URL}/api/courses...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get Recommendations to find a course ID
    try:
        resp = requests.get(f"{BASE_URL}/api/courses/recommendations", headers=headers)
        if resp.status_code != 200 or not resp.json():
            print("[SKIP] No courses available to enroll in.")
            return

        course_id = resp.json()[0]["_id"]
        print(f"     Attempting to enroll in course: {course_id}")
        
        # 2. Enroll
        enroll_resp = requests.post(f"{BASE_URL}/api/courses/{course_id}/enroll", headers=headers)
        if enroll_resp.status_code == 200:
            print(f"[OK] Enrollment request successful: {enroll_resp.json().get('message')}")
        else:
            print(f"[FAIL] Enrollment failed: {enroll_resp.status_code}")
            return
            
        # 3. Verify in Enrolled List
        verify_resp = requests.get(f"{BASE_URL}/api/courses/enrolled", headers=headers)
        if verify_resp.status_code == 200:
            enrolled_courses = verify_resp.json()
            is_enrolled = any(c['_id'] == course_id for c in enrolled_courses)
            if is_enrolled:
                print(f"[OK] Verified course {course_id} is in enrolled list.")
            else:
                print(f"[FAIL] Course {course_id} NOT found in enrolled list.")
        else:
            print(f"[FAIL] Failed to fetch enrolled courses: {verify_resp.status_code}")
            
    except Exception as e:
        print(f"[FAIL] Error in Course Enrollment: {e}")

if __name__ == "__main__":
    print("=== API Verification Script ===")
    token = test_login()
    if token:
        test_get_tasks(token) # Keep existing basic check
        test_career_domains(token)
        test_internships(token)
        test_courses(token)
        test_resume_templates()
        
        # New Tests
        test_mentor_chat(token)
        test_stats(token)
        test_tasks_flow(token)
        test_course_enrollment(token)
    else:
        sys.exit(1)
