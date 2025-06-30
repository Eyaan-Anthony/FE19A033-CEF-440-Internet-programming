from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    student_id: str
    session_id: str
    timestamp: datetime
    latitude: float
    longitude: float

class AttendanceResponse(BaseModel):
    id: int
    student_id: str
    session_id: str
    timestamp: datetime
    status: str  # e.g., "present" or "absent"
