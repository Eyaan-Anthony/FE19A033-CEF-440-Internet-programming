from fastapi import APIRouter, Body, Form, HTTPException, File, UploadFile, Depends
from app.models.user import StudentCreate, InstructorCreate, User, EmailStr
from app.services.auth_service import (
    user_login, student_registration, instructor_registration,
    hash_password, create_jwt_token, get_user_by_email, Session, get_db, get_current_user
)
import httpx
import json
import traceback #for debugging purposes

#endpoint layer here
router = APIRouter()

# ----------- Login Endpoint -------------
@router.post("/log-in")
def login(user_data: dict = Body(...)):
    user = User(**user_data)
    return user_login(user)  # From auth_service


# ----------- Student Sign-up -------------
@router.post("/sign-in/student")
async def register_student(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    level: int = Form(...),
    pictures: list[UploadFile] = File(...)
):
    if len(pictures) < 4:
        raise HTTPException(status_code=400, detail="Please upload at least 4 pictures.")

    # ----- Step 1: Call FCR service -----
    files = [
    ("images", (file.filename, await file.read(), file.content_type))
    for file in pictures
]

    async with httpx.AsyncClient() as client:
        try:
            print(f"[DEBUG] Sending {len(files)} files to FCR service")
            fcr_response = await client.post(
                "http://localhost:8001/fcr/generate-embeddings",
                files= files,
                timeout=10.0
            )
            print(f"[DEBUG] Response Status: {fcr_response.status_code}")
            print(f"[DEBUG] Response Body: {fcr_response.text}")
            fcr_response.raise_for_status()
            embedding = fcr_response.json()["embedding"]
        except httpx.HTTPStatusError as e:
            print("=== FCR SERVICE ERROR ===")
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
            raise HTTPException(status_code=500, detail=f"Facial recognition error: {e.response.text}")
        except Exception as e:
            print("=== GENERAL ERROR ===")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Facial recognition error: {str(e)}")

    # ----- Step 2: Continue registration -----
    hashed_pw = hash_password(password)

    student_data = StudentCreate(
        name=name,
        email=email,
        hashed_password=hashed_pw,
        level=level,
        face_embedding=embedding  # <-- must exist in DB/Pydantic model
    )

    return await student_registration(student_data)  


# ----------- Instructor Sign-up -------------
@router.post("/sign-in/instructor")
async def register_instructor(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    faculty: str = Form(...)
):
    hashed_pw = hash_password(password)

    instructor_data = InstructorCreate(
        name=name,
        email=email,
        hashed_password=hashed_pw,
        faculty=faculty
    )

    return await instructor_registration(instructor_data)


@router.post("/verify")
async def verify_student_identity(
    image: UploadFile = File(...),
    user: dict = Depends(get_current_user),  # <-- inject from token
    db: Session = Depends(get_db)
):
    student = get_user_by_email(user["sub"], db)

    if not student or not student.face_embedding:
        raise HTTPException(status_code=404, detail="Embedding not found")

    # Prepare request
    files = {
        "image": (image.filename, await image.read(), image.content_type),
    }
    data = {
        "stored_embedding": student.face_embedding
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8001/fcr/verify-face",
                files=files,
                data={"stored_embedding": json.dumps(student.face_embedding)}
            )
            response.raise_for_status()
            match = response.json()["match"]
            return {"match": match}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"FCR verification failed: {str(e)}")
