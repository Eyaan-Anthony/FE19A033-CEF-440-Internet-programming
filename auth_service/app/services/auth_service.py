from app.models.user import StudentCreate, InstructorCreate, User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from app.db.auth_orm import User, UserRole
from app.db.session import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# ----- Password Hashing Setup -----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # not used directly, but needed

SECRET_KEY = "attendance_project_secret_key"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ----- JWT Token Generation -----
def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")  # Replace with env var later

#get database (SessionLocal)
def get_db():
    db = SessionLocal()
    try:
        yield db    #yield doesn't destroy local variables
    finally:
        db.close()

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")



#actual registration and login logic

def user_login(user_data: User, db: Session):
    user = get_user_by_email(user_data.email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_jwt_token({"sub": user.email, "role": user.role.value})
    return {
        "message": f"Welcome back, {user.name}",
        "access_token": token,
        "role": user.role.value
    }

def student_registration(user_data: StudentCreate, db: Session):
    if get_user_by_email(user_data.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.hashed_password),
        role=UserRole.STUDENT,
        level=user_data.level,
        faculty="N/A"  # Optional or can be taken as input
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt_token({"sub": user_data.email, "role": "student"})
    return {
        "message": f"Student {new_user.name} registered successfully",
        "access_token": token
    }

def instructor_registration(user_data: InstructorCreate, db: Session):
    if get_user_by_email(user_data.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.hashed_password),
        role=UserRole.INSTRUCTOR,
        faculty=user_data.faculty
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt_token({"sub": user_data.email, "role": "instructor"})
    return {
        "message": f"Instructor {new_user.name} registered successfully",
        "access_token": token
    }