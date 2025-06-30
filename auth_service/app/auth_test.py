from auth_service.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

pictures = [
    "C:/Users/franc/Documents/Attendance project/back_end/auth_service/app/sample_picture/front_profile.jpg",
    "C:/Users/franc/Documents/Attendance project/back_end/auth_service/app/sample_picture/right_profile.jpg",
    "C:/Users/franc/Documents/Attendance project/back_end/auth_service/app/sample_picture/second_front_profile.jpg",
    "C:/Users/franc/Documents/Attendance project/back_end/auth_service/app/sample_picture/upward_profile.jpg"
]

def test_sign_in_student():
    files = [("pictures", (f"image{i}.jpg", open(p, "rb"), "image/jpeg")) for i, p in enumerate(pictures)]

    data = {
        "name": "Eyaan",
        "email": "test_student@example.com",
        "password": "691880471",
        "level": 200,
        "student_id": "FE19A033"
    }
    #embeddings are generated succesfully, the verify_face function has not yet been tested
    #to complete the embedding generation test, make sure the response corresponds to the pydantic model

    response = client.post("/auth/sign-in/student", data=data, files=files)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert f"Student {data['name']} registered successfully" in json_data["message"]
    #pytest auth_service/app/auth_test.py -v
