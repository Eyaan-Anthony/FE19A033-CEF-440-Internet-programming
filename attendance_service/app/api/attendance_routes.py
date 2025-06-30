from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.service.attendance_service import mark_attendance, get_attendance_stats
from app.models.attendance_model import AttendanceCreate, AttendanceResponse
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mark-attendance", response_model=AttendanceResponse)
async def mark_attendance_route(data: AttendanceCreate):
    try:
        return await mark_attendance(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def stats(session_id: str = None):
    try:
        stats = get_attendance_stats(session_id=session_id)
        return JSONResponse(content={"data": stats})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))