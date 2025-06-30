from pydantic import BaseModel
from datetime import datetime

class ClassSessionCreate(BaseModel):
    course_name: str
    instructor_id: str
    location_lat: float
    location_lng: float
    start_time: datetime
    end_time: datetime

class ClassSessionResponse(BaseModel):
    id: int
    course_name: str
    instructor_id: str
    location_lat: float
    location_lng: float
    start_time: datetime
    end_time: datetime


