from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.class_session_models import ClassSessionCreate
from db.db import SessionLocal
from services.class_session_service import create_class_session, get_class_session
from db.class_session_orm import ClassSessionDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-session", response_model=ClassSessionCreate)
async def create_session(data: ClassSessionCreate, db: Session = Depends(get_db)):
    try:
        session = create_class_session(db, data)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-session/{session_id}", response_model=ClassSessionCreate)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    try:
        session = get_class_session(db, session_id)
        return session
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

