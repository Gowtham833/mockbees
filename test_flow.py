import requests
import time
import uuid

BASE_URL = "http://127.0.0.1:8000/api"


def wait_for_server(timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = requests.get("http://127.0.0.1:8000/api/health", timeout=2)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False


def run_test():
    print("Starting E2E Validation...")
    if not wait_for_server():
        print("Backend server is not reachable at http://127.0.0.1:8000")
        return False
    
    # 1. Register
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    print(f"Registering user: {email}")
    res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": password
    })
    if res.status_code != 200:
        print("Registration failed:", res.text)
        return False
    print("Registration successful!")

    # 2. Login
    print("Logging in...")
    res = requests.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": password
    })
    if res.status_code != 200:
        print("Login failed:", res.text)
        return False
    
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful!")

    # 3. Get Categories
    print("Fetching categories...")
    res = requests.get(f"{BASE_URL}/exams/categories", headers=headers)
    if res.status_code != 200:
        print("Failed to fetch categories:", res.text)
        return False
    
    categories = res.json()
    if not categories:
        print("No categories found!")
        return False
    
    category_id = categories[0]["id"]
    print(f"Fetched categories. Using category ID: {category_id}")

    # 4. Get Exams for Category
    res = requests.get(f"{BASE_URL}/exams/categories/{category_id}", headers=headers)
    exams = res.json()["exams"]
    if not exams:
        print("No exams found for category!")
        return False
    
    exam_id = exams[0]["id"]
    print(f"Fetched exams. Using exam ID: {exam_id}")

    # 5. Generate Mock Test
    print("Generating Mock Test (calling Groq API)...")
    res = requests.post(f"{BASE_URL}/mock-tests/generate", headers=headers, json={
        "exam_id": exam_id,
        "num_questions": 2
    })
    
    if res.status_code != 200:
        print("Mock test generation failed:", res.text)
        return False
        
    test_data = res.json()
    attempt_id = test_data["id"]
    questions = test_data["questions"]
    print(f"Mock test generated successfully! Attempt ID: {attempt_id}, Questions: {len(questions)}")
    
    # 6. Submit Test
    print("Submitting test...")
    answers = []
    for q in questions:
        answers.append({
            "question_id": q["id"],
            "selected_answer": "A",
            "time_spent_seconds": 10,
            "is_marked_for_review": False
        })
        
    res = requests.post(f"{BASE_URL}/mock-tests/{attempt_id}/submit", headers=headers, json={
        "answers": answers,
        "time_spent": 120
    })
    
    if res.status_code != 200:
        print("Test submission failed:", res.text)
        return False
        
    result = res.json()
    print(f"Test submitted successfully! Score: {result['score']}")
    
    print("E2E Validation Completed Successfully!")
    return True

if __name__ == "__main__":
    run_test()
