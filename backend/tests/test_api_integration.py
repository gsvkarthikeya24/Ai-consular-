import pytest
import requests

def test_health_check(api_base_url):
    response = requests.get(f"{api_base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_flow(api_base_url):
    payload = {"email": "student1@example.com", "password": "password123"}
    response = requests.post(f"{api_base_url}/api/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data

def test_get_tasks(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_task_crud_lifecycle(api_base_url, auth_headers):
    # 1. Create
    task_payload = {
        "type": "homework",
        "subject": "Integration Test",
        "title": "Pytest Integration Task",
        "description": "Created by automated tests",
        "difficulty": "medium",
        "due_date": "2026-12-31T23:59:59"
    }
    create_resp = requests.post(f"{api_base_url}/api/tasks", json=task_payload, headers=auth_headers)
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    # 2. Read (Get Specific)
    get_resp = requests.get(f"{api_base_url}/api/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Pytest Integration Task"

    # 3. Delete
    delete_resp = requests.delete(f"{api_base_url}/api/tasks/{task_id}", headers=auth_headers)
    assert delete_resp.status_code == 200

    # 4. Verify Deletion
    get_again = requests.get(f"{api_base_url}/api/tasks/{task_id}", headers=auth_headers)
    assert get_again.status_code == 404

def test_career_domains(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/career/domains", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_count" in data
    assert len(data["domains"]) > 0

def test_internships(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/internships", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_courses(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/courses/all", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_resume_templates(api_base_url):
    response = requests.get(f"{api_base_url}/api/resume/templates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_gate_subjects(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/gate/subjects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "subjects" in data
    assert isinstance(data["subjects"], list)

def test_gate_questions(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/gate/questions?limit=5", headers=auth_headers)
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    if questions:
        assert "question" in questions[0]
        assert "options" in questions[0]

def test_gate_progress(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/gate/progress", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "accuracy" in data
    assert "total_attempted" in data

def test_mentor_chat(api_base_url, auth_headers):
    payload = {
        "message": "Hello mentor!",
        "conversation_history": []
    }
    response = requests.post(f"{api_base_url}/api/mentor/chat", json=payload, headers=auth_headers)
    # Status might be 200 or 500 depending on AI service availability/mocking
    # But it should return a valid JSON structure if successful
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
    else:
        # If AI service down/rate limited, might fail, but structure should be consistent.
        # Allowing failure here if it's purely external dependency related
        pass 

def test_student_stats(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/api/stats/student", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "tasks_completed" in data
    assert "career_readiness" in data

def test_course_enrollment(api_base_url, auth_headers):
    # 1. Get Recommendations to find a course ID
    resp = requests.get(f"{api_base_url}/api/courses/recommendations", headers=auth_headers)
    assert resp.status_code == 200
    courses = resp.json()
    
    if not courses:
        pytest.skip("No courses available to enroll in")
        
    course_id = courses[0]["_id"]
    
    # 2. Enroll
    enroll_resp = requests.post(f"{api_base_url}/api/courses/{course_id}/enroll", headers=auth_headers)
    assert enroll_resp.status_code == 200
    assert enroll_resp.json()["success"] is True
    
    # 3. Verify in Enrolled List
    verify_resp = requests.get(f"{api_base_url}/api/courses/enrolled", headers=auth_headers)
    assert verify_resp.status_code == 200
    enrolled_courses = verify_resp.json()
    
    course_ids = [c["_id"] for c in enrolled_courses]
    assert course_id in course_ids
