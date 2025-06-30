from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from .db import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    session_id = Column(String, index=True)
    timestamp = Column(DateTime)
    face_verified = Column(Boolean)
    location_verified = Column(Boolean)
    status = Column(String)  # "Present" if both verifications passed
